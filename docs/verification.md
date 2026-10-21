# Minecraft 1.21.11 verification

Tests were performed on 21 October 2026 in isolated, newly generated worlds.
Only the production mod JAR was loaded; no test entry point or renderer shim is
included in the release. Native Minecraft screenshots are in `images/`.

## Method

Computer Use operated the test client, entered fixture commands, toggled labels,
reloaded resources and closed each client. Windows window capture returned white
images for this GPU surface. Minecraft's own F2 captures, matched to its saved
screenshot log entries, supplied the visual evidence instead.

The main fixture contains sixteen actual redstone wire blocks powered 15 through
0. Server-side commands assert each real blockstate; those assertions establish
the fixture, while screenshots establish the client labels. A separate dense
fixture asserts all 1,024 actual power-zero wire positions. The numbers themselves
read client blockstates; there is no server integration.

## Functional results

- Minimal Fabric/Java21: all sixteen glyphs match actual powers. Switching the
  lever updates all labels to zero. Toggle off/on and F3+T resource reload pass.
- Opposite, low and overhead views retain camera-facing labels. F1 retains them.
- Removing a wire removes its label and updates the disconnected powers;
  replacing it restores the row. Travelling to an empty distant region and back
  clears and rebuilds the labels.
- Opaque wall occlusion passes with Iris/BSL. Normal local light is retained.
- VulkanMod also retains labels behind glass. The underwater view retains native
  fog; its distant labels were obscured, so no underwater readability claim is made.
- With a three-label limit, Distant Horizons shows the nearest values 7/8/9;
  moving to the end of the rail selects 0/1/2 instead.
- The optional cosmetic ZIP loads alongside the mod and BSL; it adds no labels.

## Renderer coverage

| Environment | Observed result |
| --- | --- |
| Minecraft1.21.11, Fabric Loader0.19.5, Fabric API0.141.6+1.21.11, Java21 | Functional pass |
| Copied 66-mod environment, Sodium0.8.12, Iris1.10.7 shaders OFF, Voxy0.2.16, Java25 | Labels, live changes, removal/replacement and travel pass |
| Sodium0.8.12 + Iris1.10.7 + BSL10.1.8 | Labels and opaque occlusion pass; End/Nether transitions and actual 16-power fixtures pass |
| Sodium0.8.12 + Iris1.10.7 + Complementary Reimagined5.9.3 | Nether labels and all sixteen lit End labels pass; End scene remains intact |
| Distant Horizons3.3.3-1.21.11 + minimal Fabric | Near loaded-block labels and moving nearest-three cap pass |
| VulkanMod0.6.8+1.21.11 + minimal Fabric | All sixteen labels and actual power checks pass; labels behind glass pass |

The copied environment uses Java25 because its C2ME acceleration modules require
it. Its VoxySeedGen add-on reports that it cannot seed-generate the synthetic flat
world. This does not establish distant-LOD correctness. Labels use loaded client
blocks within the configured range; they never annotate distant LOD geometry.

Shader packs control the appearance of ordinary world text. BSL makes the labels
paler in daylight and darker in unlit Nether areas. Bloom over sea lanterns can
wash out the rail and text together. This implementation does not change shader
packs to compensate. These tests do not establish universal renderer support.
Complementary5.9.3 logs an unknown optional biome uniform with Iris1.10.7, but
the inspected Nether and End scenes render. Its first dimension switch requires
shader compilation. The End fixture was repeated with mob griefing disabled
after the test dragon destroyed the first rail. No shader-pack source was edited.

## Performance

The optimized JAR was measured with three alternating OFF/ON pairs in the fixed
1,024-wire scene, VSync off and FPS unlimited. OFF capture medians were
6.6158/6.1295/5.8844ms; ON medians were 6.5941/6.0245/6.2677ms. Comparing the
medians of those captures gives +2.25%; the pooled sample mean gives +1.51%.
Within-condition capture variation reaches 11.93%, and individual paired deltas
range from -1.71% to +6.51%. These results do **not** demonstrate a reliable
overhead bound below 5%, even though the aggregate point estimate is below it.

The earlier first pair was slower. Profiling pointed to wire selection, so the
implementation now skips heap maintenance and sorting when wires fit under the
cap. Extraction's profiler share fell from 7.76% to 3.09%; text feature rendering
stayed near 2.5%. This is consistent with the intended optimization, rather than
proof of a controlled cross-run speedup.

Sanitized capture statistics and hashes are in [performance.json](performance.json).
The native client `ticktime` metric samples the rendering loop, including native
profiler and display/scheduling overhead; it is not isolated GPU timing. Another
pre-existing Minecraft client remained open and was left untouched. Raw profiler
ZIPs are private because they contain runtime/system details.

Empty-scene controls have two captures per condition: ON medians 3.8844/3.6929ms
versus OFF 3.6103/3.5090ms, giving +6.43% median-of-capture-medians and +8.18%
pooled mean. This is fewer than the planned three captures per condition, and its
point estimate exceeds 5%. The earlier orphan ON capture is excluded. The
five-minute test-session watchdog ended this session after the second pair;
these controls are insufficient for a performance pass. **The 5% performance
target is not certified by this milestone.** No extra renderer machinery was
added to pursue that target.

## Publication boundary

Source, original namespaced glyph assets, licenses and synthetic-world screenshots
are public. Accounts, actual worlds, user options/configuration, raw logs and
profiler archives are excluded. Git uses only the TQNL public noreply identity.
Final rehash of all 4,560 inventoried installed files found zero changed or
missing files. Every owned QA client was confirmed stopped; the original
Minecraft client remained open. Tests did not use or modify actual user worlds.

The original resource-pack project is preserved. No later Minecraft version is
implemented in this milestone.

## Reproduction

A clean independent Git clone at `af529bfe847285321753245fb309ee27b7e6b353`
builds without the legacy repository. Gradle build, cosmetic packaging and privacy
audit pass; there are no unit tests (`test NO-SOURCE`). The rebuilt Java21 JAR
and cosmetic ZIP match the live-tested artifacts byte for byte:

```text
cb5950cec4914d910b405f80e884d02fbe7f5070f91f32844df1e41376a12cb8  redstone-numbers-0.1.0+mc1.21.11.jar
75546380593908c9f96b6ec525cd61713f04194a456dfb66d5d9464d5377ed68  TQNL-Redstone-Dust-Cosmetic-mc1.21.11.zip
```
