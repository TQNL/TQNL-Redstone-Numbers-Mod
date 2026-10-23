# Redstone Numbers

Client-only redstone power labels for **Minecraft Java 26.3**. The sixteen
number glyphs face the camera and sit just above each wire. Minecraft's ordinary
world-text renderer supplies depth testing and local lighting.

[Download the 26.3 prerelease](https://github.com/TQNL/TQNL-Redstone-Numbers-Mod/releases/tag/v0.1.4-mc26.3)
(JAR, optional cosmetic pack and checksums).

Requires **Fabric Loader 0.19.5+ and Fabric API 0.164.0+26.3**. Sodium, Iris,
Voxy and configuration libraries are optional. This branch targets exactly 26.3.
Earlier completed versions are retained on `codex/mc-<version>` branches;
see the [compatibility receipts](docs/compatibility).

## Installation

Put the versioned mod JAR in the instance's `mods` folder alongside Fabric API.
Disable other packs that already draw redstone power numbers to avoid duplicate
labels. Ordinary texture packs can be used alongside this mod.

The mod includes **Clean Redstone Lines** in Minecraft's **Resource
Packs** menu. It starts disabled. Move it to Selected and choose Done to use the
same clean-line redstone textures as the earlier packs; move it back to disable.
Only three dust textures change. Numbers work with either choice.

Turn **Show built-in resource pack** off in settings to hide this pack from the
menu. It starts ON; pack activation still starts OFF. Restart Minecraft after
changing visibility. A hidden pack is unavailable and cannot stay active.

The separate **TQNL Redstone Dust Cosmetic** ZIP offers the same textures without
the mod. Use either the built-in pack or that ZIP. Both carry the previous TQNL
pack icon, which is also shown for the mod.

## Settings

`config/redstonenumbers.json` is created with these defaults:

```json
{
  "enabled": true,
  "showBuiltinPack": true,
  "range": 16,
  "maxLabels": 1024,
  "scale": 1.0
}
```

Open **Video Settings > Redstone Numbers** in Sodium or Reese's Sodium Options
(choose **Settings** if your layout shows a page row). The host draws its own checkbox and sliders and handles pending
edits, **Apply** and **Undo**. All four options use Sodium's supported config API;
there is no separate form or UI implementation for a Sodium-style menu.

Use **/redstonenumbers** in chat to open the settings form. This is a client
command and needs no server permission. Mod Menu also provides
**Mods > Redstone Numbers > Configure**. This standalone form
previews valid edits immediately: **Done** saves, **Cancel** or Escape restores
the opening values, and **Reset** previews defaults. Neither Sodium nor Mod Menu
is required, and no extra configuration library is used.

Assign **Open Redstone Numbers settings** in Controls for direct access. Both
that key and **Toggle Redstone Numbers** start unbound. The toggle's state is saved.
F1 leaves world labels visible. Existing saved settings are preserved when
upgrading; use Reset to adopt the new defaults. Direct JSON edits load on restart.

Range is limited to 1-128 blocks, label count to 1-65,536, and scale to 0.25-4.
Nearby visible labels are prioritized when the configured limit is reached.
Initial discovery is spread across ticks to avoid a large loading spike.

The quarter-block glyph size and local lighting are retained. Labels sit just
above the dust surface and face the camera, using normal depth and fog.

Numbers show the latest blockstates received by the client, including unpowered
zero. They do not simulate server redstone or display unreceived sub-tick pulses.
Opaque blocks occlude the labels; normal text lighting and fog apply.

## Build

For local interactive testing, double-click **Launch Test Instance.cmd**.
The [test launcher guide](docs/test-launcher.md) explains the mod picker, presets,
separate test saves and required local QA caches.

Use JDK 25 to run the pinned Gradle build; output targets Java 25:

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

The [0.1.3 update](docs/update-0.1.3.md) covers native video options and compact
resource-pack text, including the tested versions and limits.
The [0.1.1 update and measurements](docs/update-0.1.1.md) cover the lower placement,
Mod Menu settings, lighter defaults and brief controlled profiles in Minecraft.
The [0.1.0 verification](docs/verification.md) records the earlier full renderer
matrix, including Iris, Distant Horizons and VulkanMod. Exact versions,
screenshots and limits are kept with their tested milestone.
Project decisions and the current milestone are maintained in [notes.md](notes.md).

Code is MIT; reused artwork has separate terms in [ASSET-LICENSES.md](ASSET-LICENSES.md).
Not an official Minecraft product. Not approved by or associated with Mojang or Microsoft.
