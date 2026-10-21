# Redstone Numbers

Client-only redstone power labels for **Minecraft Java 1.21.11**. The sixteen
number glyphs face the camera and sit just above each wire. Minecraft's ordinary
world-text renderer supplies depth testing and local lighting.

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
  "range": 32,
  "maxLabels": 8192,
  "scale": 1.0
}
```

Changes to the file take effect on the next client start. The toggle is initially
unbound; assign **Toggle Redstone Numbers** in Minecraft's Controls menu. Its
state is saved. Hiding the HUD with F1 leaves the world labels visible.

Range is limited to 1–128 blocks, label count to 1–65,536, and scale to 0.25–4.
Nearby visible labels are prioritized when the configured limit is reached.
Initial discovery is spread across ticks to avoid a large loading spike.

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

Live Minecraft tests cover minimal Fabric, the copied 66-mod environment, and
Iris with BSL. See [verification and limits](docs/verification.md) for the exact
versions, screenshots, performance measurements and remaining qualifications.
Project decisions and the current milestone are maintained in [notes.md](notes.md).

Code is MIT; reused artwork has separate terms in [ASSET-LICENSES.md](ASSET-LICENSES.md).
Not an official Minecraft product. Not approved by or associated with Mojang or Microsoft.
