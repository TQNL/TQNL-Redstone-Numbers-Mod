# Redstone Numbers standalone mod

## Current objective

Implement and test Minecraft Java 1.21.11 only, then stop. Start a separate
Git/GitHub repository with no personal information. Do not modify the existing
resource-pack repository, installed Minecraft content, or user worlds.

## Accepted architecture and decisions

- Client-only Fabric Loader + Fabric API. No required renderer/config library.
- Reuse 0-15 artwork as a mod-namespaced bitmap font and submit ordinary
  depth-tested world text. CPU billboarding and a small physical lift replace
  the old shader depth correction. No authored shaders or scene replacements.
- Local world light; optional shader packs may apply normal world-text effects.
- Default range 32 blocks; nearest 8192 labels, both configurable. One unbound
  toggle in Controls; a small JSON config. No server code or custom packets.
- Optional texture-only cosmetic dust pack; independent from number rendering.
- Nearby section index, bounded discovery, one observational block-state hook,
  immutable extracted frame data. Clear on world/unload/toggle transitions.
- If a rendering approach needs substantial special cases, stop and compare
  adapters, dependencies and alternatives after two focused correction attempts.
- Other Minecraft versions are deferred. No automatic continuation.

## Progress and verification

- New local Git repository initialized on main with project-only TQNL author
  identity. Work/runtime data and deliverables are ignored.
- Rendering/config, wire index and one observational mixin implemented.
- Combined Gradle build passes; artifact/privacy audit passes (16 glyphs and
  six-member cosmetic ZIP). No tests have yet run inside Minecraft.
- Gradle9.6.1/Loom1.17.21 wrapper/build configured; font atlas and strict six-member optional
  cosmetic pack generated from selected existing artwork. Java21 target, Loader
  0.19.5, Fabric API0.141.6+1.21.11. Original client remains open and untouched.
- Actual client was observed open before work. It must remain untouched.
- Computer Use backend initialized successfully; live testing is still pending.
- Empty public repository created: https://github.com/TQNL/TQNL-Redstone-Numbers-Mod
  No source pushed yet. Git author is TQNL / public noreply address.
- No Minecraft, renderer-compatibility or performance pass is claimed yet.

## Next steps

Compile, inspect the combined diff, test in isolated Minecraft through Computer
Use, compare minimal and copied installed stacks, verify preservation and privacy,
then commit/publish the completed 1.21.11 milestone and stop.
