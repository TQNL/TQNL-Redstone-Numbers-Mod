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
  six-member cosmetic ZIP). Live tests are recorded below.
- Gradle9.6.1/Loom1.17.21 wrapper/build configured; font atlas and strict six-member optional
  cosmetic pack generated from selected existing artwork. Java21 target, Loader
  0.19.5, Fabric API0.141.6+1.21.11. Original client remains open and untouched.
- Actual client was observed open before work. It must remain untouched.
- Computer Use key input verified. Sky returns white GPU window images here,
  so genuine Minecraft F2 screenshots/log receipts are used for visual evidence.
- Minimal official-Java21 runtime passed all16 actual wire power checks, live
  lever-off update to0, F9disable/enable, resource reload, opposite/low/overhead
  sampled views. Native1280x800 captures in docs/images.
- First QA username exceeded vanilla16charlimit; helper corrected to synthetic
  RedstoneQA. This was fixture setup, not mod failure. No world copied from user.
- Minimal client closed through Computer Use Alt-F4 with all dimensions saved.
- Empty public repository created: https://github.com/TQNL/TQNL-Redstone-Numbers-Mod
  No source pushed yet. Git author is TQNL / public noreply address.
- Other renderer compatibility and performance remain pending; no broad claim.

## Next steps

Compile, inspect the combined diff, test in isolated Minecraft through Computer
Use, compare minimal and copied installed stacks, verify preservation and privacy,
then commit/publish the completed 1.21.11 milestone and stop.

## Live actual-stack checkpoint

- All66 installed mod JARs copied/hash-pinned into an isolated newworld. Existing
  C2ME acceleration modules require Java25, so this stage uses the existing
  unmodified JDK25; minimal stage remains verified on official Java21.
- All16 labels display with Sodium0.8.12, Iris1.10.7 installed/shadersOFF,
  Voxy0.2.16, BetterClouds, ImmediatelyFast and copied othermods loaded.
- Removal removes the label and updates powers; replacing restores it. Travel
  outside loaded fixture then return restores all16 labels, with no stale distant
  labels. F1 hides clutter while retaining worldnumbers.
- VoxySeedGen cannot seed-generate this syntheticflatworld; existing addon warning
  is recorded, not treated as a numbermod defect or distantLOD proof.
- Closed actualtest through ComputerUse Alt-F4; saved-world and Voxy worker
  shutdown verified. Native captures are in docs/images.

## Performance and remaining verification

- Native F3+L captures compare the same warmed 1024-wire overhead scene,
  unlimited FPS and VSync off. First pair: enabled median 6.6768ms; disabled
  5.6076ms. This is not a performance pass; repeated captures remain necessary.
- Profiler attributes about 0.52ms additional time to extraction. Correction1
  removes per-frame heap/sorting below the label cap; overflow retains the same
  bounded nearest selection. No rendering change or stale state cache added.
- Original raw captures are private in work/qa; they contain runtime details
  and must not be published. Publish only sanitized derived statistics.
- Corrected JAR SHA256: cb5950cec4914d910b405f80e884d02fbe7f5070f91f32844df1e41376a12cb8.
- BSL10.1.8 + Iris1.10.7 + Sodium0.8.12 + cosmetic ZIP pass main-row labels,
  opaque occlusion and End/Nether transitions. All three dimension power
  fixtures assert actual 0-15 states. BSL bloom over sea lanterns washes out
  text; stone support makes Nether labels visible with normal dark world light.
- Three optimized dense captures each: off medians 6.6158/6.1295/5.8844ms;
  on 6.5941/6.0245/6.2677ms. Median-of-medians delta +2.25%, but within-condition
  range 11.93%; descriptive evidence only, not a precise performance bound.
- Last minimal session hit its five-minute owned-process watchdog after the
  completed dense tests and one empty ON capture. Empty comparison incomplete.
  No original client affected. Need finish empty controls in a new bounded run.
- Complementary, DH/cap, Vulkan tests and final preservation check are next.
- Review found no demonstrated code blocker; an apparent nullable chunk
  callback issue was withdrawn after checking Fabric's TAIL injection semantics.
