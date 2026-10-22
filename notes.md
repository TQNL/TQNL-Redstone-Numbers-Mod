# Redstone Numbers standalone mod

## Objective and scope

Minecraft Java 1.21.11 only. Add a compact Sodium video settings entry using
its official config API and a native entry for other video settings screens.
Bundle the installed clean-line dust textures as an optional built-in pack,
disabled by default. Reuse previous shader pack branding for mod and pack icons.
Keep rendering untouched, preserve installed content, use Git/public identity,
and verify the requested menus and pack in isolated Computer Use sessions.

## Current update checkpoint: 0.1.2

- Started from released0.1.1 at bff7552a23ea06998e57221621e518619ec603fb.
- Optional Sodium external page uses the supplied official config API, compiled
  against0.8.12. Reese's2.2.3 displays a compact icon/name/version tab. Older
  API icon fallback is source-checked, not runtime-qualified.
- GUI-only Fabric screen events add a20x20 RN shortcut to native/recognized
  replacement video screens. Actual video-button launch provenance supports
  renamed screens. No new mixins or world-rendering changes. Prefer free lower
  left, then header space. Known Sodium/Reese's families use only the API entry.
- Resource Packs lists Redstone Numbers: Clean Lines under Available by default
  (NORMAL activation). Only the three existing textures, verified byte-identical
  to the active installed clean-line packs, plus metadata/icon/credits/licenses.
- Legacy TQNL icon is reused unchanged for mod, Sodium entry, built-in pack and
  cosmetic ZIP. Gradle assembles built-in assets from single committed sources.
- Live Computer Use verification complete: vanilla Fabric Java21 and VulkanMod
  0.6.8 Java21 final footer button opens settings with no overlap. Copied actual
  Sodium0.8.12/Reese's2.2.3 Java25 has compact API tab/icon, opens form and returns;
  Cancel restores an OFF preview to ON. Duplicate Reese's shortcut caught/fixed.
  Vulkan Support overlap caught/fixed, final placement rechecked in both native
  and Vulkan screens. No extra runtime tests planned.
- Native pack menu default-off, enable+save+resource reload, disable+save+reload
  verified. No shaders, legacy number models or unrelated textures bundled.
- docs/update-0.1.2.md and docs/verification-0.1.2.json record scope/limitations;
  four native screenshots in docs/images/v012-*.png. No new performance claim,
  rendering/index files unchanged from0.1.1; Gradle test reports NO-SOURCE.
- Final preservation: all4561 installed files unchanged, none missing; every
  owned QA client stopped after clean saves. Private receipts:
  work/qa/preservation-{before,after}-v012.json and owned-process-final-v012.json.
- Build and source/artifact/privacy audit pass. Final JAR SHA256:
  1342e0f1d36958776bc57777f5673c2918610fd9afd25a49bc62a35cdb2a83e3.
  Cosmetic ZIP SHA256:
  d4c0bd274c247a0c7b856abe2a12446c9b5c78b8860ec965855c5d88c77a1d6d.
- Final publication audit passed79 public files/62 decompressed archive members.
  Published0.1.2 prerelease from source aede5a65a64a7ee909587d07a649b9407a6019ad:
  https://github.com/TQNL/TQNL-Redstone-Numbers-Mod/releases/tag/v0.1.2-mc1.21.11
  All three public downloads fetched without credentials and independently hashed
  against audited local bytes. Receipt: work/release-receipt-v012.json.
- Gradle daemon and all owned QA clients/helpers stopped. No temporary device
  settings changed and no cleanup remains outside ignored work/.
- This update is complete. Stop at Minecraft1.21.11; no later-version work,
  further runtime/performance tests or automatic continuation is scheduled.

## Released 0.1.1

- Grounded label placement uses actual dust plane and visible 12px ink height;
  no shader/depth trick. Fresh defaults 16 blocks/1024 labels; saved choices kept.
- Optional Mod Menu/native form and unbound settings key. Done saves; Cancel
  restores. Minimal and copied Sodium setup verified. Cancellation runtime
  check interrupted by session cap; source reviewed only.
- Controlled short profiles differed only in WireIndex. Dense extraction estimate
  0.19663 to 0.15921 ms/frame (-19.03%); mixed empty results and no strong FPS claim.
  See docs/update-0.1.1.md and docs/performance-0.1.1.json.
- Build/privacy audit passed; 4560 installed files unchanged and none missing.
  All owned QA clients stopped. Release JAR SHA256:
  dfdce77ccfadfa4466f52fbfb25ad2c7564f548b2ca46f779e8b3bc6910af4c2.
- Published source 8ee558e2db0721bea65d96b9e600212dec635603; all three public
  downloads independently rehashed. Private work/release-receipt-v011.json.
  https://github.com/TQNL/TQNL-Redstone-Numbers-Mod/releases/tag/v0.1.1-mc1.21.11

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
- Optional built-in dust-only pack, off by default, and equivalent standalone ZIP;
  exactly three textures, original branding icon and asset licenses.

## Relevant files

- src/client/java/dev/tqnl/redstonenumbers/: entrypoint, ModConfig, WireIndex,
  NumberRenderer, SettingsScreen, ModMenuIntegration, SodiumIntegration,
  VideoSettingsIntegration and observational chunk mixin.
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
