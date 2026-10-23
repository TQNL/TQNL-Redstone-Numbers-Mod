# Local test launcher

Double-click **Launch Test Instance.cmd** in the repository root. Requires Python
with Tkinter (already available on the development laptop). The script is
`tools/test_launcher.py`; it uses only Python's standard library.

1. Choose Minecraft and a preset. The default is **1.21.11 / Minimal**.
2. Check/uncheck individual mods, or choose **Add JARs…** for other Fabric mods.
3. Choose **Check selection** to include missing cached dependencies and report
   incompatible selections. Then choose **Launch Minecraft**.

Presets cover Minimal, Sodium/native settings, Iris/BSL, Iris/Complementary,
Voxy, Distant Horizons and VulkanMod where prepared. For 1.21.11 there is also
**My installed mods (copies)**. That reads only the normal mods folder's top-level
JARs. It copies selected JARs into the test instance; it does not copy accounts,
real saves or normal configuration. The preset pins are the previously tested
versions, not an automatic updater. A missing upstream preset is omitted.

Redstone Numbers and Fabric API stay required. To test a fresh build, add its
matching JAR with **Add JARs…**; it replaces the required mod selection. Adding
a matching Fabric API JAR similarly replaces that requirement. The checkbox
**Use preset's visual pack** is available for cached Iris presets; turn it off
to test those mods without the pack. Ordinary custom resource packs can be
placed in the test instance's own `resourcepacks` folder.

The picker validates common Fabric version/dependency rules and conflicts,
including Voxy's exact Sodium requirements and Sodium/VulkanMod exclusion.
Fabric Loader remains the final authority for advanced resolution and mixin
compatibility. An arbitrary custom combination can still fail during startup;
its logs are retained under the instance's `runs` folder. The built-in Clean
Redstone Lines pack starts disabled as usual.

Each name/version/mod-selection combination gets a separate folder below
`work/multi-version/test-launcher/instances`. Reopening the same combination
preserves its test worlds and settings. Changing mods creates a separate
combination. **Open instance folder** opens the selected instance once it exists,
or the launcher's data folder before its first launch. Save and
quit normally; there is no five-minute watchdog, forced stop or account login.
Closing the picker leaves Minecraft running. The test identity is local-only;
this is intended for singleplayer testing, not authenticated multiplayer.

The first launch opens a synthetic redstone fixture world. It cycles the main
rail between actual powers 0–15 and zero. Use F8 for the settings form and F9 to
toggle the numbers on 1.21.11–26.2. Minecraft 26.3 changed its keyboard names;
assign those controls in-game if the older fixture bindings do not apply.
The mod's usual Mod Menu/native video options remain available.

## Local runtime dependency

This tool reuses the project's prepared QA runtimes, mod caches and synthetic
fixture metadata. Keep `work/qa/cache`, `work/multi-version/runtime` and the
prepared `work/multi-version/clients/<version>` inputs. Their paths are local
and are not committed or included in releases. This is a local development
launcher, not a fresh-clone installer. It reports missing caches rather than
reading Launcher credentials or changing the normal Minecraft installation.
Java 25 is reused from a prepared runtime when available, including for the
installed C2ME/native mod stack; otherwise the prepared target runtime is used.

User-created instances are retained for repeat testing. When finished with one,
save/quit its game, open its folder, and remove that particular instance if its
test saves are no longer needed. Shared runtime/assets do not live inside each
instance. The picker remembers the last selection in its local `picker.json`.

For terminal use:

```text
python tools/test_launcher.py
python tools/test_launcher.py --game 26.3 --list-presets
python -m unittest discover -s tools -p test_test_launcher.py
```
