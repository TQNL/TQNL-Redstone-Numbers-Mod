# Settings access and pack visibility:0.1.4

Use `/redstonenumbers` in chat to open the existing settings form. This uses
Fabric's client command API, needs no server permission, and opens on the next
client tick after chat closes. Mod Menu, native Sodium/Reese's controls and the
assignable settings key remain available.

The old video-settings shortcut class and its translations were deleted.
No replacement button, extra menu hook or rendering adapter was added.

**Show built-in resource pack** defaults ON. Set it OFF and restart Minecraft
to remove Clean Redstone Lines from Resource Packs. This only controls the mod's
`redstonenumbers:clean_lines` registration. Pack activation remains default-off;
a hidden pack is unavailable for use. Existing user resource packs and their
native cosmetic textures are unaffected.

All six supported target builds and artifact/privacy audits pass. The exact
[build hashes and verification scope](update-0.1.4.json) distinguish live checks
from build checks. Command/default/cancel/save behaviour was observed on1.21.11;
command and visible/hidden pack menus across restart were observed on26.3 with
Sodium/Reese's present. The four intermediate targets were built and audited.
Rendering/index bytecode matches each target's0.1.3 exactly; the old full renderer
matrix was not rerun. Native Minecraft F2 captures provided visual verification.

Versioned downloads are available under `v0.1.4-mc<game>` in the repository releases.
