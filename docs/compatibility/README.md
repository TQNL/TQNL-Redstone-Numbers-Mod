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

## Completed versions

| Minecraft | Source | Download | Checks |
| --- | --- | --- | --- |
| [1.21.11](1.21.11.json) | [branch](https://github.com/TQNL/TQNL-Redstone-Numbers-Mod/tree/codex/mc-1.21.11) | [release](https://github.com/TQNL/TQNL-Redstone-Numbers-Mod/releases/tag/v0.1.3-mc1.21.11) | 7 tested |
| [26.1](26.1.json) | [branch](https://github.com/TQNL/TQNL-Redstone-Numbers-Mod/tree/codex/mc-26.1) | [release](https://github.com/TQNL/TQNL-Redstone-Numbers-Mod/releases/tag/v0.1.3-mc26.1) | 7 tested |
| [26.1.1](26.1.1.json) | [branch](https://github.com/TQNL/TQNL-Redstone-Numbers-Mod/tree/codex/mc-26.1.1) | [release](https://github.com/TQNL/TQNL-Redstone-Numbers-Mod/releases/tag/v0.1.3-mc26.1.1) | 7 tested |
| [26.1.2](26.1.2.json) | [branch](https://github.com/TQNL/TQNL-Redstone-Numbers-Mod/tree/codex/mc-26.1.2) | [release](https://github.com/TQNL/TQNL-Redstone-Numbers-Mod/releases/tag/v0.1.3-mc26.1.2) | 7 tested |
| [26.2](26.2.json) | [branch](https://github.com/TQNL/TQNL-Redstone-Numbers-Mod/tree/codex/mc-26.2) | [release](https://github.com/TQNL/TQNL-Redstone-Numbers-Mod/releases/tag/v0.1.3-mc26.2) | 6 tested / 1 unavailable |
| [26.3](26.3.json) | [branch](https://github.com/TQNL/TQNL-Redstone-Numbers-Mod/tree/codex/mc-26.3) | [release](https://github.com/TQNL/TQNL-Redstone-Numbers-Mod/releases/tag/v0.1.3-mc26.3) | 6 tested / 1 unavailable |
