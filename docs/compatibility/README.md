# Stable-release smoke checks

Each version has a separate JSON receipt with the exact mod files, publisher
links, SHA256 hashes and native screenshot hashes. Checks use a fresh isolated
local world and sixteen actual redstone powers, followed by a live update to zero.
Computer Use controls Minecraft and its native F2 captures are visually inspected.

These are brief compatibility checks. They do not certify every scene, hardware
combination, distant LOD, or performance target. Unavailable upstream combinations
are recorded rather than forced. Voxy and Distant Horizons are tested separately.

Source checkpoints are retained on `codex/mc-<Minecraft version>` branches.
Use the JAR and optional cosmetic pack matching the exact Minecraft version.
