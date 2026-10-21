# 0.1.1: grounded labels and accessible settings

Minecraft1.21.11 only. The original artwork,0.25-block cell and local lighting
already matched the shader edition. This update corrects the excessive lift:
the actual dust mesh is at0.25/16 blocks, rather than the collision-height1/16
used before. Placement now accounts for the visible12-pixel glyph height and a
small physical clearance. Sampled ink bounds were checked for all16 glyphs.

At scale1, frontal label centre drops from0.2025 to0.11139 blocks above the wire
block origin; overhead centre is0.01764. The original shader centre was0.01569,
but it used a custom depth correction. Native depth requires the ink to stay
above the surface. Exact old depth behaviour and distance filtering are not
reproduced; no shader, custom pipeline or renderer adapter was added.

## Settings

Optional Mod Menu exposes the native settings screen. It was opened through
Mod Menu17.0.1-beta.1 in the copied Sodium0.8.12/Iris1.10.7/Voxy environment.
Without Mod Menu, assign the initially unbound settings key in Controls.
Enabled, distance, label limit and size preview live; Done saves, Cancel/Escape
restores opening values, and Reset previews defaults. Invalid entries disable
Done. No Cloth Config or Sodium-specific hooks are used.

Fresh defaults are16 blocks and1,024 nearest labels, down from32 and8,192.
Saved user choices survive upgrades; Reset adopts the new values.
The no-Mod-Menu shortcut opened the same form in minimal Fabric. Editing distance
and choosing Done persisted8 blocks, confirmed by reading the saved JSON. Cancel,
Reset and validation were independently reviewed; the brief session limit ended
the attempted live cancellation check, so it is not claimed as a runtime pass.

## Brief performance comparison

Two builds had identical0.1.1 rendering/settings and differed only in WireIndex
classes. Both used32 blocks,1,024 labels, Java21, VSync off, unlimited FPS and
the same camera fixtures. Each build had one native10-second F3+L dense capture
and one empty capture; this deliberately short test is descriptive.

The optimized index skips empty iterators/buffers, reuses each selected immutable
position and its freshly read blockstate for lighting, and avoids allocating
losing overflow candidates. No persistent state/light cache was added.

- Dense1,024-wire scene: estimated extraction cost0.197 to0.159ms/frame,
  about19% lower. Text rendering stays approximately0.15ms/frame.
- Dense frame median5.6173 to5.5426ms (-1.33%); mean6.0139 to5.8990ms (-1.91%).
- Empty frame median3.34845 to3.3004ms, but mean3.6629 to3.6766ms worsens slightly.
  No overall empty-scene improvement is established.

Extraction estimates combine rounded profiler shares with native frame samples;
they are not isolated microbenchmarks. No broad FPS claim or reliable5% overhead
bound follows from these short samples. Exact hashes, numeric summaries and
qualifications are in [performance-0.1.1.json](performance-0.1.1.json).

Native captures: [grounded labels](images/v011-grounded-labels.png),
[Mod Menu](images/v011-modmenu.png), [settings](images/v011-settings.png).
The settings capture shows the previously saved32-block benchmark choice.
The release remains a prerelease;0.1.0 is preserved separately.
