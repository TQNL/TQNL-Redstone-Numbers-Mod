# Redstone Numbers

Client-only redstone power labels for **Minecraft Java 1.21.11**. The sixteen
number glyphs face the camera and sit just above each wire. Minecraft's ordinary
world-text renderer supplies depth testing and local lighting.

[Download the 1.21.11 prerelease](https://github.com/TQNL/TQNL-Redstone-Numbers-Mod/releases/tag/v0.1.1-mc1.21.11)
(JAR, optional cosmetic pack and checksums).

This mod does not replace terrain, sky, water or other scene shaders. It needs
**Fabric Loader 0.19.5+ and Fabric API 0.141.6+1.21.11**. Sodium, Iris, Voxy and
configuration libraries are not required. Other Minecraft versions are not
implemented in this milestone.

## Installation

Put the versioned mod JAR in the instance's `mods` folder alongside Fabric API.
Disable the old Core/Iris/Plain number resource packs and companion number shader
when using this mod; they would add duplicate labels or retain old shader changes.
Choose whichever ordinary resource pack and optional Iris shader you prefer.

The optional **TQNL Redstone Dust Cosmetic** ZIP changes only three dust textures.
It is independent from the mod and adds no numbers or shaders. Keep it zipped in
`resourcepacks` and enable it only if you want that appearance.

## Settings

`config/redstonenumbers.json` is created with these defaults:

```json
{
  "enabled": true,
  "range": 16,
  "maxLabels": 1024,
  "scale": 1.0
}
```

Open **Mods → Redstone Numbers → Configure** with optional Mod Menu installed.
The native settings screen previews valid edits immediately. **Done** saves;
**Cancel** or Escape restores the opening values; **Reset** previews the lighter
defaults. Mod Menu is optional and no extra configuration library is required.

Without Mod Menu, assign **Open Redstone Numbers settings** in Controls. Both that
key and **Toggle Redstone Numbers** start unbound. The toggle's state is saved.
F1 leaves world labels visible. Existing saved settings are preserved when
upgrading; use Reset to adopt the new defaults. Direct JSON edits load on restart.

Range is limited to 1–128 blocks, label count to 1–65,536, and scale to 0.25–4.
Nearby visible labels are prioritized when the configured limit is reached.
Initial discovery is spread across ticks to avoid a large loading spike.

The original quarter-block glyph size and local lighting are retained. Labels
now sit closer to the actual dust plane, matching the old shader's grounded
appearance more closely. Native depth still requires a small physical lift;
the old shader's exact depth correction and distance filtering are not reproduced.

Numbers show the latest blockstates received by the client, including unpowered
zero. They do not simulate server redstone or display unreceived sub-tick pulses.
Opaque blocks occlude them; optional shader packs may apply their ordinary text
lighting and fog. No special through-wall display is used.

## Build

Use JDK 25 to run the pinned Gradle build; output targets Java 21:

```sh
./gradlew build
python tools/package_cosmetic.py
python tools/audit-release.py
```

The mod JAR is in `build/libs`; the optional cosmetic ZIP is in `outputs`.
The cosmetic packer needs only Python 3's standard library. Pillow is needed for
the release audit and legacy artwork repacking. Committed font and dust assets
make ordinary builds independent of the legacy repository.
`tools/build-assets.py --source <legacy-repo>` reproduces those artwork inputs
and invokes the same cosmetic packer.

## Implementation and evidence

The mod keeps a nearby wire-position index, observes successful client block
changes, extracts immutable label data, and submits native text. It introduces
no artificial entities, server packets, terrain rebuilds or custom GPU pipelines.

The [0.1.1 update and measurements](docs/update-0.1.1.md) cover the lower placement,
Mod Menu settings, lighter defaults and brief controlled profiles in Minecraft.
The [0.1.0 verification](docs/verification.md) records the earlier full renderer
matrix, including Iris shaders, Distant Horizons and VulkanMod. Exact versions,
screenshots and limits are kept with their tested milestone.
Project decisions and the current milestone are maintained in [notes.md](notes.md).

Code is MIT; reused artwork has separate terms in [ASSET-LICENSES.md](ASSET-LICENSES.md).
Not an official Minecraft product. Not approved by or associated with Mojang or Microsoft.
