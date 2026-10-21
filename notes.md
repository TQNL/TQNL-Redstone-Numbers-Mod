# Redstone Numbers standalone mod

## Objective and scope

Continue Minecraft Java 1.21.11 only: match the old shader labels' appearance,
add accessible settings with lighter defaults, and make measured optimizations
using brief tests. Preserve the released0.1.0 and publish the reviewed update.
No later version started.
Original resource-pack project and installed Minecraft content are preserved.

## Current update checkpoint

- User reopened work for shader-like appearance, Mod Menu or Sodium settings,
  lower defaults, and short profiling with measured optimization improvements.
- Source comparison: original glyphs,0.25-block cell and local light already
  match. Excess hover comes from using collision height instead of the actual
  dust plane. Lower native lift uses visible12px ink height; no shader/depth trick.
- Planned0.1.1 defaults16-block range/1024 nearest labels; retain existing saved
  user choices. Native settings screen through optional Mod Menu, no Cloth Config.
- Index edits remove empty allocations/iterators, redundant selected state reads,
  and allocations for losing overflow candidates. Frozen0.1.0 JAR in
  work/qa/baselines. Controlled0.1.1 reference/candidate JARs differ only in
  WireIndex classes, verified by decompressed-member comparison.
- Brief profiles complete: one10s dense and one10s empty per build, fixed32/1024.
  Dense median5.6173 to5.5426ms; empty3.34845 to3.3004ms, but empty mean slightly
  worsens. Small samples, no strong overall FPS claim. CPU profile review pending.
- Minimal Java21 starts without Mod Menu. Actual copied Sodium setup is now
  verified: Mod Menu opens the native form, fresh defaults16/1024 load, and the
  lowered labels display. Minimal F8 shortcut opens it without Mod Menu; Done
  persisted an8-block edit. Runtime cancellation was interrupted by the session
  cap; Cancel/Reset/validation are independently reviewed, not claimed live passes.
- Native dense extraction estimate0.19663 to0.15921ms/frame (-19.03%); text cost
  staysabout0.15ms. Empty results mixed. docs/performance-0.1.1.json contains
  sanitized hashes/statistics; docs/update-0.1.1.md records the exact scope.
- Full build and source/privacy audit pass (69publicfiles/47archive members at
  last check); no unit tests. CandidateJAR SHA256:
  dfdce77ccfadfa4466f52fbfb25ad2c7564f548b2ca46f779e8b3bc6910af4c2.
- Current preservation check:4560 files unchanged, none missing. All owned QA
  clients stopped; no further performance or runtime tests planned.
- Pending only final commit/push and0.1.1 prerelease upload/download hash readback.
- Older results below document the released0.1.0, not the pending update.

## Architecture

- Client-only Fabric Loader + Fabric API; no required Sodium/Iris/Voxy or config library.
- Original 0-15 artwork repacked as a private bitmap font. Native submitText,
  CPU billboarding, slight physical lift, normal depth and local light.
- No authored shaders, pipelines, framebuffers, terrain replacements, fake
  entities, server packets or renderer-specific adapters.
- Nearby loaded-section index, bounded discovery, one observational block-state
  mixin, immutable extracted frames. Current power/light read during extraction.
- Fresh defaults: enabled, range16 blocks, nearest1024 labels, scale1. Existing
  saved choices retained. Native Mod Menu settings, optional API compile-only,
  initially unbound settings and toggle keys. F1 retains labels.
- Below the label cap, skip heap maintenance and sorting. Overflow retains
  bounded nearest selection with deterministic distance/position ties.
- Independent optional dust-only pack with exactly three textures and licenses.

## Relevant files

- src/client/java/dev/tqnl/redstonenumbers/: entrypoint, ModConfig, WireIndex,
  NumberRenderer, SettingsScreen, ModMenuIntegration and observational chunk mixin.
- src/main/resources/assets/redstonenumbers/: namespaced font and 16 glyphs.
- cosmetic/textures/: three original dust textures; tools/package_cosmetic.py
  packages them using only Python standard library.
- tools/build-assets.py optionally reproduces artwork from recorded legacy
  inputs; ordinary builds require no legacy repository.
- tools/audit-release.py: asset allowlist, decompressed binary/source privacy,
  PNG metadata and Git author/committer checks.
- docs/verification.md, docs/performance.json and docs/images/: public evidence.
- work/qa/: ignored private fixtures, native logs/profiles, preservation hashes
  and owned-process records. Never publish raw runtime/profiler files.

## Completed verification: original0.1.0 milestone

- Gradle9.6.1/Loom1.17.21, JDK25 build targeting Java21 passes. Fabric Loader
  0.19.5 and API0.141.6+1.21.11 pinned; Minecraft dependency exactly1.21.11.
- Minimal official Java21 client: all actual powers0-15 and matching glyphs,
  lever updates to0, toggle, F3+T reload, low/opposite/overhead views pass.
- Copied66-mod stack: Sodium0.8.12, Iris1.10.7 shadersOFF, Voxy0.2.16 and other
  installed mods load. Live updates, removal/replacement and travel pass.
  This stack needs Java25 for existing C2ME acceleration modules.
- BSL10.1.8: main labels, opaque occlusion and End/Nether transitions pass;
  actual sixteen-power fixtures assert in each dimension.
- Complementary Reimagined5.9.3: Nether labels and all16 lit End labels pass.
  Test dragon destroyed first rail; disabled mob_griefing in disposable world
  and repeated. No shader source changed.
- Distant Horizons3.3.3: near labels coexist; cap3 selects7/8/9, then0/1/2
  after camera moves. No distant-LOD annotation claim.
- VulkanMod0.6.8: all16 labels/power assertions and labels behind glass pass.
  Underwater view retains native fog; distant labels obscured.
- Computer Use controlled isolated clients and native F2 captures. GPU window
  capture is unreliable here, so native screenshots plus log receipts verify
  visual results. No user worlds/accounts/history copied.
- Fresh no-hardlinks clone at af529bfe847285321753245fb309ee27b7e6b353 builds
  matching artifacts byte-for-byte. Gradle reports test NO-SOURCE; no unit tests.
- JAR SHA256 cb5950cec4914d910b405f80e884d02fbe7f5070f91f32844df1e41376a12cb8.
- Cosmetic SHA256 75546380593908c9f96b6ec525cd61713f04194a456dfb66d5d9464d5377ed68.

## Performance and limits: original0.1.0 milestone

- Dense1024-wire fixed camera: three OFF/ON pairs, +2.25% median aggregate,
  +1.51% pooled mean. Within-condition variation11.93%; paired deltas reach6.51%.
- Empty control: two ON/OFF pairs, +6.43% median and +8.18% pooled mean.
  Below three-capture protocol; earlier unpaired ON excluded.
- The5% performance target is not certified. No performance pass claimed.
  Extraction optimization is consistent with profiler share7.76% to3.09%;
  text-render share stays near2.5%. Raw samples include profiler/scheduling.
- Shader text appearance remains shader-dependent; BSL bloom can wash out text
  over emissive surfaces, and dark local light dims it. Native fog/occlusion
  remain. Sub-tick server changes not received by client cannot be displayed.
- VoxySeedGen warns on synthetic flatworld; this is not a distantLOD test pass.

## Original0.1.0 preservation and publication

- Final hash comparison: all4560 inventoried installed files unchanged, none
  missing. Every owned QA client stopped; original client remains open.
- Five-minute watchdog ended two profiling sessions and one shader session
  after recorded checks. Shader session saved all dimensions before process
  termination; no original client affected. No device setting or helper remains.
- Source, JAR contents, cosmetic ZIP, screenshots and Git identity audited for
  personal paths/credentials/metadata. Only public TQNL noreply identity used.
- Repository: https://github.com/TQNL/TQNL-Redstone-Numbers-Mod
- Published source and prerelease v0.1.0-mc1.21.11:
  https://github.com/TQNL/TQNL-Redstone-Numbers-Mod/releases/tag/v0.1.0-mc1.21.11
- Release source commit70b21ddec070b4bf9bc6c946782f9e92dbac577d. All three public
  downloads (JAR, cosmetic ZIP, SHA256SUMS) fetched without credentials and
  independently rehashed against local audited bytes. All match. Private receipt:
  work/release-receipt.json. Final source/privacy review and diff check pass.
- Milestone implementation and publication finished. Performance qualification
  above remains explicit; no5%certification claimed. Stop at1.21.11. No further
  implementation, version port or automatic continuation is scheduled.
