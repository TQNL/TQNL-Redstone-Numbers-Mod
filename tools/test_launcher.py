"""Local picker for the project's prepared, isolated Minecraft test runtimes.

Python standard library only. Never reads launcher credentials or real saves.
Prepared runtime/profile caches are intentionally local, not release assets.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
import uuid
import zipfile
from dataclasses import dataclass

ROOT = Path(__file__).absolute().parents[1]
CAMPAIGN = ROOT / "work/multi-version"
STORE = CAMPAIGN / "test-launcher"
GAMES = ("1.21.11", "26.1", "26.1.1", "26.1.2", "26.2", "26.3")
PRESETS = {"Minimal": "minimal", "Sodium + native settings": "sodium",
           "Iris + BSL": "iris_bsl", "Iris + Complementary": "iris_complementary",
           "Voxy": "voxy", "Distant Horizons": "dh", "VulkanMod": "vulkan"}
WORLD = "Redstone Numbers QA"
REQUIRED = {"fabric-api", "redstonenumbers"}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def version_key(value):
    value = str(value).split("+", 1)[0]
    match = re.fullmatch(r"(\d+(?:\.\d+)*)(?:-(.*))?", value)
    if not match:
        raise ValueError(f"Unsupported version format: {value}")
    numbers = tuple(int(x) for x in match[1].split("."))
    tail = match[2]
    return numbers + (0,) * (5 - len(numbers)), tail is None, tuple(
        (0, int(x)) if x.isdigit() else (1, x) for x in re.split(r"[.-]", tail or ""))


def matches(version, requirement):
    """Fabric-style common predicates; unsupported syntax fails explicitly."""
    if isinstance(requirement, list):
        return any(matches(version, x) for x in requirement)
    if "||" in requirement:
        return any(matches(version, x.strip()) for x in requirement.split("||"))
    for token in requirement.split():
        if token == "*":
            continue
        match = re.fullmatch(r"(>=|<=|>|<|=|~|\^)?([\w.+*-]+)", token)
        if not match:
            raise ValueError(f"Unsupported dependency predicate: {token}")
        op, target = match[1] or "=", match[2]
        if re.search(r"(?:^|\.)(?:x|X|\*)$", target):
            prefix = target.rsplit(".", 1)[0] if "." in target else ""
            if prefix and not (version.split("+", 1)[0] == prefix or version.startswith(prefix + ".")):
                return False
            continue
        a, b = version_key(version), version_key(target)
        if op in ("~", "^"):
            nums = [int(x) for x in target.split("-", 1)[0].split("+")[0].split(".")]
            index = max(0, len(nums) - 2) if op == "~" else next((i for i, n in enumerate(nums) if n), len(nums) - 1)
            upper = nums[:index + 1]
            upper[index] += 1
            if not (a >= b and a < version_key(".".join(map(str, upper)))):
                return False
        elif not {"=": a == b, ">=": a >= b, "<=": a <= b, ">": a > b, "<": a < b}[op]:
            return False
    return True


def jar_metadata(path):
    result = []

    def inspect(source, depth=0):
        if depth > 8:
            raise ValueError("Nested mod archive is too deep")
        with zipfile.ZipFile(source) as archive:
            meta = json.loads(archive.read("fabric.mod.json"))
            result.append(meta)
            for child in meta.get("jars", []):
                inspect(io.BytesIO(archive.read(child["file"])), depth + 1)

    inspect(path)
    return tuple(result)


@dataclass
class Mod:
    path: Path
    sha: str
    metadata: tuple
    origin: str

    @property
    def primary(self):
        return self.metadata[0]

    @property
    def label(self):
        m = self.primary
        return f'{m.get("name", m["id"])}  {m["version"]}   [{self.origin}]'


class Catalog:
    def __init__(self, game):
        if game not in GAMES:
            raise ValueError("Choose one of the prepared Minecraft versions")
        self.game, self.mods, self.presets, self.packs = game, {}, {}, {}
        self.base = CAMPAIGN / "clients" / game
        self.runtime = ROOT / "work/qa/cache" if game == "1.21.11" else CAMPAIGN / "runtime" / game
        if not (self.runtime / "launch-config.json").is_file():
            raise ValueError(f"The prepared {game} runtime is missing. This local tool needs this project's QA caches.")
        self.config = read(self.runtime / "launch-config.json")
        self.official = read(self.runtime / "version.json")
        self.visited = set()
        for label, profile in PRESETS.items():
            folder = self.base / profile
            if not (folder / "profile.json").is_file() or (folder / "unavailable.json").exists():
                continue
            self.presets[label] = {self.add(p, label) for p in sorted((folder / "mods").glob("*.jar"))}
            pack = read(folder / "profile.json").get("visual_pack")
            if pack and (folder / "shaderpacks" / pack).is_file():
                self.packs[label] = folder / "shaderpacks" / pack
        if "Minimal" not in self.presets:
            raise ValueError("The minimal QA profile is missing")
        self.core = {key for key in self.presets["Minimal"] if self.mods[key].primary["id"] in REQUIRED}
        if {self.mods[k].primary["id"] for k in self.core} != REQUIRED:
            raise ValueError("The matching standalone mod and Fabric API are missing")
        if game == "1.21.11":
            normal = Path(os.environ.get("APPDATA", str(Path.home()))) / ".minecraft/mods"
            self.presets["My installed mods (copies)"] = set(self.core)
            for p in sorted(normal.glob("*.jar")):
                key = self.add(p, "Installed")
                if self.mods[key].primary["id"] not in REQUIRED:
                    self.presets["My installed mods (copies)"].add(key)

    def add(self, path, origin="Added JAR"):
        path = Path(path).absolute()
        # Deduplicate identical cached copies, including copies in the normal mods folder.
        key = digest(path)
        if key not in self.mods:
            metadata = jar_metadata(path)
            if metadata[0].get("environment") == "server":
                raise ValueError(f"{path.name} is server-only")
            self.mods[key] = Mod(path, key, metadata, origin)
        return key

    def java(self):
        # The existing installed-mod stack contains Java25 native/C2ME modules.
        for game in ("26.3", "26.2", "26.1"):
            p = CAMPAIGN / "runtime" / game / "launch-config.json"
            if p.is_file() and Path(read(p)["java"]).is_file():
                return read(p)["java"], "25"
        return self.config["java"], str(self.official["javaVersion"]["majorVersion"])

    def replace_required(self, key):
        """Allow a freshly built matching mod JAR without two copies of the mod."""
        mod = self.mods[key]
        if mod.primary["id"] not in REQUIRED:
            return set()
        if not matches(self.game, mod.primary.get("depends", {}).get("minecraft", "*")):
            raise ValueError(f"{mod.path.name} does not target Minecraft {self.game}")
        previous = {k for k in self.core if self.mods[k].primary["id"] == mod.primary["id"]}
        self.core = self.core - previous | {key}
        for label in self.presets:
            self.presets[label] = self.presets[label] - previous | {key}
        return previous

    def provided(self, selected):
        provided = {"minecraft": [self.game], "fabricloader": [self.config["loader"]], "java": [self.java()[1]]}
        for key in selected:
            for meta in self.mods[key].metadata:
                if meta.get("environment") == "server":
                    continue
                for alias in [meta["id"], *meta.get("provides", [])]:
                    provided.setdefault(alias, []).append(meta["version"])
        # Fabric chooses one candidate (the highest version) for duplicate nested libraries.
        return {alias: [max(versions, key=version_key)] if len(set(versions)) > 1 else versions[:1]
                for alias, versions in provided.items()}

    def resolve(self, selected):
        selected = set(selected) | self.core
        for _ in range(len(self.mods) + 1):
            top = [self.mods[k].primary["id"] for k in selected]
            duplicates = sorted({x for x in top if top.count(x) > 1})
            if duplicates:
                raise ValueError("Select only one version of: " + ", ".join(duplicates))
            provided = self.provided(selected)
            missing = []
            for key in sorted(selected):
                for meta in self.mods[key].metadata:
                    if meta.get("environment") == "server":
                        continue
                    if meta["version"] != provided[meta["id"]][0]:
                        continue
                    for dep, predicate in meta.get("depends", {}).items():
                        if any(matches(v, predicate) for v in provided.get(dep, [])):
                            continue
                        if dep in provided:
                            raise ValueError(f'{meta["id"]} needs {dep} {predicate}; selected: {", ".join(provided[dep])}. Choose the matching preset or uncheck the conflicting version.')
                        missing.append((meta["id"], dep, predicate))
                    for dep, predicate in meta.get("breaks", {}).items():
                        if any(matches(v, predicate) for v in provided.get(dep, [])):
                            raise ValueError(f'{meta["id"]} conflicts with {dep} {predicate}. Uncheck one of them.')
            if not missing:
                return selected
            added = False
            # Resolve all constraints on a dependency together rather than choosing the first version.
            for dep in sorted({d for _, d, _ in missing}):
                needs = [predicate for _, d, predicate in missing if d == dep]
                candidates = []
                for key, mod in self.mods.items():
                    for meta in mod.metadata:
                        if dep in [meta["id"], *meta.get("provides", [])] and all(matches(meta["version"], p) for p in needs):
                            candidates.append(key)
                            break
                if not candidates:
                    raise ValueError(f'Missing {dep} {needs}. Add its matching Fabric JAR, then check again.')
                chosen = next((k for k in candidates if self.mods[k].primary["id"] == dep), candidates[0])
                selected.add(chosen)
                added = True
            if not added:
                break
        raise ValueError("Dependency selection did not converge")


def instance_path(game, name, selected, pack):
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,39}", name) or name.upper() in {"CON", "PRN", "AUX", "NUL", *[f"{p}{i}" for p in ("COM", "LPT") for i in range(1, 10)]}:
        raise ValueError("Instance name: 1-40 letters, digits, underscores or hyphens; no Windows device names")
    fingerprint = hashlib.sha256(json.dumps([game, sorted(selected), digest(pack) if pack else None]).encode()).hexdigest()[:12]
    base = STORE / "instances"
    path = base / game / f"{name}-{fingerprint}"
    if not path.resolve().is_relative_to(base.resolve()):
        raise ValueError("Instance must stay inside the launcher folder")
    return path


def owned_alive(record):
    pid = int(record["pid"])
    if os.name == "nt":
        folder = str(record["client"]).replace("'", "''")
        code = f"Get-CimInstance Win32_Process -Filter 'ProcessId={pid}' | ForEach-Object {{ if ($_.CommandLine -and $_.CommandLine.Contains('{folder}')) {{ Write-Output 'owned' }} }}"
        result = subprocess.run(["powershell", "-NoProfile", "-Command", code], capture_output=True, text=True, timeout=20, creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode:
            raise ValueError("Could not check whether this test instance is still running")
        return result.stdout.strip() == "owned"
    try:
        return str(record["client"]) in Path(f"/proc/{pid}/cmdline").read_bytes().decode().split("\0")
    except FileNotFoundError:
        return False


def prepare(catalog, name, selected, pack=None):
    selected = catalog.resolve(selected)
    client = instance_path(catalog.game, name, selected, pack)
    if (client / "process.json").exists() and owned_alive(read(client / "process.json")):
        raise ValueError("This exact test instance is already running. Save and quit it before launching again.")
    if client.exists() and not (client / "instance.json").exists():
        raise ValueError("An unrecognized folder already exists here; choose another instance name")
    if client.exists():
        expected = read(client / "instance.json")["mods"]
        actual = {p.name: digest(p) for p in (client / "mods").glob("*.jar")}
        if actual != {r["file"]: r["sha256"] for r in expected}:
            raise ValueError("This instance's mod files were edited outside the picker. Use a new instance name to preserve them.")
        return client, selected
    stage = client.parent / (".preparing-" + uuid.uuid4().hex)
    try:
        populate(catalog, stage, selected, pack, name)
        stage.rename(client)
    finally:
        if stage.exists():
            if not stage.resolve().is_relative_to((STORE / "instances").resolve()):
                raise ValueError("Temporary instance escaped the launcher directory")
            shutil.rmtree(stage)
    return client, selected


def populate(catalog, client, selected, pack, name):
    for folder in ("mods", "config", "shaderpacks", "resourcepacks", "native-cache"):
        (client / folder).mkdir(parents=True, exist_ok=True)
    manifest = []
    for key in sorted(selected):
        mod = catalog.mods[key]
        if digest(mod.path) != key:
            raise ValueError(f"{mod.path.name} changed since scanning. Reopen the launcher.")
        destination = client / "mods" / mod.path.name
        if destination.exists():
            raise ValueError("Two different mods have the same filename; rename an added source JAR first")
        shutil.copy2(mod.path, destination)
        if digest(destination) != key:
            raise ValueError("Mod copy verification failed")
        manifest.append({"id": mod.primary["id"], "version": mod.primary["version"], "file": destination.name, "sha256": key})
    # Copy only synthetic fixture metadata/datapacks, never generated worlds or real saves.
    source = catalog.base / "minimal"
    if not read(source / "profile.json").get("synthetic_identity"):
        raise ValueError("The fixture source must have a synthetic identity")
    world = client / "saves" / WORLD
    fixture = source / "saves" / WORLD
    for rel in ("level.dat", "data/minecraft/world_gen_settings.dat", "data/minecraft/game_rules.dat"):
        p = fixture / rel
        if p.is_file():
            dest = world / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)
    shutil.copytree(fixture / "datapacks", world / "datapacks")
    # Prepared 26.x singleplayer player storage moved out of level.dat.
    for rel in ("players/data", "playerdata"):
        p = fixture / rel / "00000000-0000-0000-0000-000000000001.dat"
        if p.is_file():
            dest = world / rel / p.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)
    if pack:
        shutil.copy2(pack, client / "shaderpacks" / pack.name)
    (client / "config/iris.properties").write_text(f'enableShaders={str(bool(pack)).lower()}\nshaderPack={pack.name if pack else ""}\n', encoding="utf-8")
    save(client / "config/redstonenumbers.json", {"enabled": True, "range": 16, "maxLabels": 1024, "scale": 1.0})
    options_version = next(line for line in (source / "options.txt").read_text(encoding="utf-8").splitlines() if line.startswith("version:"))
    (client / "options.txt").write_text(options_version + '\nresourcePacks:[]\nincompatibleResourcePacks:[]\nrenderDistance:8\nsimulationDistance:5\nmaxFps:120\nenableVsync:false\nfullscreen:false\npauseOnLostFocus:false\nguiScale:3\nsoundCategory_master:0.0\ntutorialStep:none\nonboardAccessibility:false\nkey_key.redstonenumbers.toggle:key.keyboard.f9\nkey_key.redstonenumbers.settings:key.keyboard.f8\n', encoding="utf-8")
    save(client / "instance.json", {"minecraft": catalog.game, "name": name, "mods": manifest, "synthetic_identity": True, "visual_pack": pack.name if pack else None})


def launch(catalog, client, memory):
    if not 2 <= memory <= 12:
        raise ValueError("Choose 2-12 GB RAM")
    cfg, official = catalog.config, catalog.official
    replacements = {"natives_directory": str(client / "native-cache"), "launcher_name": "RedstoneNumbersTest", "launcher_version": "1", "classpath": os.pathsep.join([*cfg["libraries"], cfg["client"]])}
    jvm = []
    for entry in official["arguments"]["jvm"]:
        if isinstance(entry, str):
            values = [entry]
        else:
            allowed = False
            for rule in entry.get("rules", []):
                system = rule.get("os", {})
                if system.get("name", "windows") != ("windows" if os.name == "nt" else "linux"):
                    continue
                if system.get("arch", "x86_64") not in ("x86_64", "amd64") or rule.get("features"):
                    continue
                allowed = rule["action"] == "allow"
            if not allowed:
                continue
            values = entry["value"] if isinstance(entry["value"], list) else [entry["value"]]
        jvm.extend(re.sub(r"\$\{([^}]+)\}", lambda m: replacements[m[1]], value) for value in values)
    java, _ = catalog.java()
    for p in [java, cfg["client"], *cfg["libraries"]]:
        if not Path(p).is_file():
            raise ValueError(f"Prepared runtime file is missing: {p}")
    args = [java, f"-Xmx{memory}G", "-Xss1M", *jvm, *cfg["fabric_jvm"], cfg["main_class"],
            "--username", "RedstoneQA", "--uuid", "00000000000000000000000000000001", "--accessToken", "0",
            "--version", catalog.game, "--gameDir", str(client), "--assetsDir", cfg["assets"], "--assetIndex", cfg["asset_id"],
            "--width", "1280", "--height", "800", "--versionType", "release", "--quickPlaySingleplayer", WORLD]
    if "client" in official.get("logging", {}):
        log = official["logging"]["client"]
        args.insert(2, log["argument"].replace("${path}", str(Path(cfg["assets"]) / "log_configs" / log["file"]["id"])))
    logs = client / "runs" / time.strftime("%Y%m%d-%H%M%S")
    logs.mkdir(parents=True, exist_ok=False)
    with (logs / "stdout.log").open("w") as out, (logs / "stderr.log").open("w") as err:
        process = subprocess.Popen(args, cwd=client, stdout=out, stderr=err, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
    record = {"pid": process.pid, "client": str(client), "logs": str(logs), "synthetic_identity": True}
    save(client / "process.json", record)
    return process, logs


def gui(initial_game="1.21.11"):
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox

    window = tk.Tk()
    window.title("Redstone Numbers — Test Launcher")
    window.geometry("880x740")
    window.minsize(760, 600)
    frame = ttk.Frame(window, padding=16)
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text="Redstone Numbers test instance", font=("Segoe UI", 17, "bold")).pack(anchor="w")
    ttk.Label(frame, text="Separate saves and settings • Local test identity • No five-minute timeout").pack(anchor="w", pady=(4, 16))
    row = ttk.Frame(frame)
    row.pack(fill="x")
    game = tk.StringVar(value=initial_game)
    preset = tk.StringVar(value="Minimal")
    name = tk.StringVar(value="testing")
    memory = tk.IntVar(value=3)
    for label, variable, values, width in [("Minecraft", game, GAMES, 12), ("Preset", preset, (), 30)]:
        ttk.Label(row, text=label).pack(side="left", padx=(0, 6))
        widget = ttk.Combobox(row, textvariable=variable, values=values, state="readonly", width=width)
        widget.pack(side="left", padx=(0, 16))
        if label == "Minecraft":
            version_widget = widget
        else:
            preset_widget = widget
    fields = ttk.Frame(frame)
    fields.pack(fill="x", pady=12)
    ttk.Label(fields, text="Instance name").pack(side="left")
    ttk.Entry(fields, textvariable=name, width=24).pack(side="left", padx=8)
    ttk.Label(fields, text="RAM (GB)").pack(side="left", padx=(12, 0))
    ttk.Spinbox(fields, from_=2, to=12, textvariable=memory, width=4).pack(side="left", padx=8)
    pack_enabled = tk.BooleanVar(value=False)
    ttk.Checkbutton(fields, text="Use preset's visual pack", variable=pack_enabled).pack(side="left", padx=12)
    ttk.Label(frame, text="Select mods. Matching Redstone Numbers + Fabric API are always included.").pack(anchor="w")
    search = tk.StringVar()
    filter_row = ttk.Frame(frame)
    filter_row.pack(fill="x", pady=(8, 0))
    ttk.Label(filter_row, text="Filter mods").pack(side="left", padx=(0, 8))
    ttk.Entry(filter_row, textvariable=search).pack(side="left", fill="x", expand=True)
    box = ttk.Frame(frame)
    box.pack(fill="both", expand=True, pady=8)
    canvas = tk.Canvas(box, highlightthickness=0)
    scrollbar = ttk.Scrollbar(box, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    choices = ttk.Frame(canvas)
    item = canvas.create_window((0, 0), window=choices, anchor="nw")
    choices.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfigure(item, width=e.width))
    window.bind("<MouseWheel>", lambda e: canvas.yview_scroll(-int(e.delta / 120), "units"))
    status = tk.StringVar(value="Loading cached mods…")
    ttk.Label(frame, textvariable=status, wraplength=810).pack(fill="x", pady=8)
    actions = ttk.Frame(frame)
    actions.pack(fill="x")
    state = {"catalog": None, "vars": {}, "client": None, "process": None, "logs": None}
    preferences = STORE / "picker.json"

    def render(selected):
        for child in choices.winfo_children():
            child.destroy()
        state["vars"] = {}
        cat = state["catalog"]
        for key, mod in sorted(cat.mods.items(), key=lambda kv: kv[1].label.casefold()):
            var = tk.BooleanVar(value=key in selected)
            state["vars"][key] = var
            if search.get().casefold() not in (mod.label + " " + mod.path.name + " " + mod.primary["id"]).casefold():
                continue
            ttk.Checkbutton(choices, text=mod.label, variable=var, state="disabled" if key in cat.core else "normal").pack(anchor="w", fill="x", pady=2)

    def select_preset(event=None):
        cat = state["catalog"]
        render(cat.presets[preset.get()])
        pack_enabled.set(preset.get() in cat.packs)
        status.set("Preset selected. You can change individual mods, then Check selection or Launch.")

    def load(event=None):
        try:
            cat = Catalog(game.get())
            state["catalog"] = cat
            preset_widget["values"] = list(cat.presets)
            if preset.get() not in cat.presets:
                preset.set("Minimal")
            select_preset()
        except Exception as exc:
            state["catalog"] = None
            status.set(str(exc))

    def selection():
        cat = state["catalog"]
        if cat is None:
            raise ValueError("No prepared runtime selected")
        selected = cat.resolve({k for k, var in state["vars"].items() if var.get()})
        pack = cat.packs.get(preset.get()) if pack_enabled.get() else None
        if pack_enabled.get() and not pack:
            raise ValueError("This preset has no cached visual pack. Uncheck that option.")
        if pack and not any(cat.mods[k].primary["id"] == "iris" for k in selected):
            raise ValueError("The visual pack needs Iris. Check Iris, or uncheck the visual pack option.")
        return cat, selected, pack

    def check():
        try:
            cat, selected, pack = selection()
            render(selected)
            state["client"] = instance_path(cat.game, name.get(), selected, pack)
            status.set(f"Ready: {len(selected)} mod JARs. Missing dependencies were selected automatically.\n{state['client']}")
            return cat, selected, pack
        except Exception as exc:
            messagebox.showerror("Check selection", str(exc), parent=window)
            return None

    def add():
        if not state["catalog"]:
            return
        files = filedialog.askopenfilenames(parent=window, title="Add matching Fabric mods", filetypes=[("Fabric mod JARs", "*.jar")])
        selected = {k for k, var in state["vars"].items() if var.get()}
        try:
            for path in files:
                key = state["catalog"].add(path)
                selected -= state["catalog"].replace_required(key)
                selected.add(key)
            render(selected)
        except Exception as exc:
            render(selected)
            messagebox.showerror("Add mod", str(exc), parent=window)

    def start():
        result = check()
        if not result:
            return
        cat, selected, pack = result
        try:
            client, selected = prepare(cat, name.get(), selected, pack)
            process, logs = launch(cat, client, memory.get())
            state.update(client=client, process=process, logs=logs)
            save(preferences, {"game": game.get(), "preset": preset.get(), "name": name.get(), "memory": memory.get(), "selected": sorted(selected), "pack": pack_enabled.get(), "added_jars": [str(cat.mods[k].path) for k in selected if cat.mods[k].origin == "Added JAR"]})
            status.set(f"Starting Minecraft {cat.game} — {len(selected)} mod JARs. Logs: {logs}")
            window.after(2000, poll)
        except Exception as exc:
            messagebox.showerror("Launch failed", str(exc), parent=window)

    def poll():
        process = state["process"]
        if process is None:
            return
        code = process.poll()
        if code is not None:
            status.set(f"Minecraft closed (exit {code}). Your test saves/settings remain. Logs: {state['logs']}")
            return
        status.set(f"Minecraft is running. Save and Quit normally when finished. Instance: {state['client']}")
        window.after(3000, poll)

    def open_folder():
        if state["client"] and state["client"].is_dir():
            path = state["client"]
        else:
            STORE.mkdir(parents=True, exist_ok=True)
            path = STORE
        if os.name == "nt":
            os.startfile(path)
        else:
            subprocess.Popen(["xdg-open", str(path)])

    ttk.Button(actions, text="Add JARs…", command=add).pack(side="left")
    ttk.Button(actions, text="Check selection", command=check).pack(side="left", padx=8)
    ttk.Button(actions, text="Open instance folder", command=open_folder).pack(side="left")
    ttk.Button(actions, text="Launch Minecraft", command=start).pack(side="right")
    version_widget.bind("<<ComboboxSelected>>", load)
    preset_widget.bind("<<ComboboxSelected>>", select_preset)
    search.trace_add("write", lambda *args: render({k for k, var in state["vars"].items() if var.get()}) if state["catalog"] else None)
    if preferences.is_file():
        try:
            prefs = read(preferences)
            game.set(prefs["game"])
            preset.set(prefs["preset"])
            name.set(prefs["name"])
            memory.set(prefs["memory"])
            load()
            cat = state["catalog"]
            if cat:
                for path in prefs.get("added_jars", []):
                    if Path(path).is_file():
                        cat.replace_required(cat.add(path))
                render(set(prefs["selected"]) & set(cat.mods) | cat.core)
                pack_enabled.set(prefs["pack"])
        except (KeyError, ValueError, OSError):
            load()
    else:
        load()
    window.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game", choices=GAMES, default="1.21.11")
    parser.add_argument("--list-presets", action="store_true", help="List available prepared presets without starting the GUI")
    args = parser.parse_args()
    if args.list_presets:
        print(json.dumps({label: len(keys) for label, keys in Catalog(args.game).presets.items()}, indent=2))
    else:
        gui(args.game)
