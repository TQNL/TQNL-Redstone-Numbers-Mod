# Redstone Numbers standalone mod

## Objective and scope

User now explicitly authorizes every stable Minecraft release from1.21.11 through
latest, including patches, oldest first. Confirmed range:1.21.11,26.1,26.1.1,
26.1.2,26.2,26.3 (official Mojang manifest,2026-10-22). Build, briefly smoke-test
available renderer/mod combinations, and push each completed version to the repo.
Keep native controls, compact default-off pack, existing appearance and defaults,
minimal rendering intervention, public TQNL identity and installed-content isolation.
Use Computer Use for real-client checks; no broad performance benchmark requested.

## Multi-version checkpoint

- Starting source74dceb889e2944f1c774a531c5c504df293680f5; clean repo.
- Official stable release list recorded privately in work/multi-version/
  mojang-release-scope.json. Snapshots/pre-releases excluded.
- Planned representative combinations: minimal Fabric; Sodium+Reese's+Mod Menu;
  Sodium+Iris (two published visual presets) and Voxy where available; DH;
  VulkanMod separately. Unsupported dependency combinations will be recorded,
  not forced. Historical1.21.11 evidence retained; current0.1.3 smoke comes first.
- Publisher catalog pinned. Latest1.21.11 Sodium0.8.14/RSO2.2.4/Iris1.10.8
  stack is separate from Voxy's exact Sodium0.8.12 older stack.
- 1.21.11 current0.1.3 build passes. Latest Sodium/RSO smoke visually observed
  powered/zero/powered labels and actual16-wire state assertions, native F2 pair.
- Minimal final serial retry passes native F2 powered/zero visuals. Initial
  focus/capture attempts crashed in glfw.dll or stalled in glfwSwapBuffers;
  no mod frame established. Kept native reports private, used text-only window
  inspection and unlimited private client cap for the passing retry. Cause remains
  unproven. Latest Iris1.10.8+BSL10.1.8 and Complementary5.9.3 pass the same brief
  check; Complementary logs an unknown biome-variable warning.
- C: filled during campaign preparation. Moved only this campaign's temporary
  directory to the D: task work directory, keeping work/multi-version as a
  junction. No user files deleted. Future Gradle cache will also use D:.
- Do not start a newer-version build
  until the previous version has its smoke result and Git checkpoint.
- All seven1.21.11 combinations now visually pass powered0-15 and live zero
  update, with server assertions and native F2 hashes in docs/compatibility/
  1.21.11.json. Final owned processes stopped. Artifact/privacy audit passes;
  all4561 installed files unchanged, none missing.
- Next: push1.21.11 checkpoint, then port26.1. Official runtime metadata for
  26.1/26.1.1/26.1.2/26.2 acquired; no later-version build started yet.

## Current update checkpoint: 0.1.3

- User requests no pack hover popup, no obsolete compatibility wording in the
  mod/pack, and actual native Sodium-style settings instead of an external form.
- Fabric source explains popup: title wider than151/157px or extended description
  over two rows. Shorten pack metadata to fit; no tooltip mixin or UI replacement.
- Replace Sodium external page with supported boolean/integer option builders.
  Native host owns styling, search, pending edits, Apply/Undo. Keep optional
  API and existing standalone form for vanilla/Mod Menu/key access.
- Number-size slider uses hundredths (25..400), preserving config field/bounds.
  Existing rendering, defaults, pack ID, icons and optional activation stay.
- Implemented native API controls with a shared storage callback. Build/audit
  pass, including a packaged-text guard against obsolete compatibility wording.
  NumberRenderer and WireIndex bytecode match0.1.2 exactly.
- Reese's2.2.3/Sodium0.8.12 live checks: host-style checkbox/sliders; pending
  checkbox leaves saved JSON unchanged; Undo restores; Apply persists all four
  controls (false/30/10385/1.15). Private work/qa/v013-native-options-result.json.
- English pack title/extended description fit completely; direct hover shows
  no Fabric truncation popup. No tooltip hook/mixin added. Native screenshots
  docs/images/v013-{reeses-native,pack-hover}.png. Owned actual client closed.
- Stock Sodium0.8.12 Java21 without Mod Menu displays the native page correctly.
  Dutch pack hover also has complete text/no popup. Native screenshots added as
  docs/images/v013-{sodium-native,pack-hover-nl}.png. Both clients cleanly saved
  and closed; private configs restored. No more runtime tests planned.
- Preservation comparison: all4561 installed files unchanged, none missing;
  no owned test clients remain. Private receipts preservation-{before,after}-v013
  and owned-process-final-v013 under work/qa. No device settings changed.
- docs/update-0.1.3.md and docs/verification-0.1.3.json record source/runtime
  evidence and limitations. Current packaged text, attribution and README have
  been cleaned; historical verification documents remain historical.
- Final build/review and artifact/privacy audit pass (85 public files,62 archive
  members). Final JAR SHA256:
  b1977e0f61df6a86c27fb9b172d85b209b1a0cda99cd72a3adc8f4a2ad839845.
  Cosmetic ZIP SHA256:
  e81a6437e1fefcf4fcdc6c6f477cf63b2cb95dedac32d061b99210d39ac5c8ec.
- Gradle daemon and QA watchdogs stopped; no outstanding device/workspace cleanup.
- Published0.1.3 prerelease from ac81cc99c5fe207b335619440dc65a9add364829:
  https://github.com/TQNL/TQNL-Redstone-Numbers-Mod/releases/tag/v0.1.3-mc1.21.11
  All three public downloads were fetched without credentials and independently
  rehashed against audited local bytes. Receipt work/release-receipt-v013.json.
- This requested update is complete. Stop at Minecraft1.21.11. No extra tests,
  profiling, later-version port or automatic continuation is scheduled.

## Released 0.1.2

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
