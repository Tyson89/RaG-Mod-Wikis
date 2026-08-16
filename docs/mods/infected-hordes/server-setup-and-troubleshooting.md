# Server setup and troubleshooting

## Required mod

[RaG Core](../core/index.md) is required by `CfgPatches.requiredAddons[]`. Install and enable RaG Core and RaG Infected Hordes on server and every client. Server `-mod` list order does not control PBO loading; declared addon dependencies do.

## Installation

1. Stop server.
2. Install original RaG Core and RaG Infected Hordes releases.
3. Copy keys into server `keys` directory when host does not manage them.
4. Add both mods to server/client mod set.
5. Start server once, then stop it.
6. Edit generated files under `RaG_Core/Configs/RaG_InfectedHorde/`.
7. Restart and inspect validation logs before opening server.

## Controlled test

Use staging server. Temporary test values:

```json
"ActiveHordeMax": 1,
"SpawnTime": 1,
"SpawnChancePercent": 100,
"MinInfectedCount": 10,
"MaxInfectedCount": 10,
"HordeActiveInfectedMax": 10,
"MinimumPlayersOnline": 1,
"PlayerActivationRadius": 1000
```

Keep one enabled location near test player. Confirm spawn notification, gradual formation, themed infected, cargo loot, lifetime, despawn notification, and cleanup. Restore production values afterward.

For performance testing, source repository defines 100, 250, and 500 infected presets. Do not begin at 500 on production hardware. Establish baseline first.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Missing dependency or script compile error | RaG Core missing, outdated, or mismatched between server and clients. |
| JSON files not generated | Confirm active server profile, write permission, both mods loaded, and no earlier startup error. Expected folder is `RaG_Core/Configs/RaG_InfectedHorde/`. |
| No horde at server startup | Expected. First attempt waits `SpawnTime` minutes. |
| Attempts run but no horde forms | Check `ActiveHordeMax`, player count, `SpawnChancePercent`, global capacity, enabled locations, proximity, and `[ValidationReport]`. |
| `No free spawn location` | Every location disabled, occupied, too far from players, or absent. On another map, replace Chernarus defaults. |
| Horde stops forming | Check FPS pause log, global population cap, and repeated spawn failures. |
| `No valid spawn position` repeats | Location lacks usable navmesh/open space, area too small, players too close, or candidates remain visible. Move center or increase area. Ten consecutive failures despawn horde. |
| Custom infected disappears from JSON | Class missing or does not inherit `ZombieBase`/`DayZInfected`. Load provider mod on both sides and verify exact class name. |
| Custom loot disappears from JSON | Class missing from supported config roots. Verify exact class and provider mod. |
| Valid loot never appears | Chance rolls independently and item must fit infected cargo. Check warning logs for creation failure. |
| Same location never returns | `ReleaseHordeLocations` is `false`; set `true` or restart server. |
| Bodies vanish during fight | Active horde retains at most 25 tracked corpses. This cap is not configurable. |
| Hordes are smaller/fewer than configured | `HordeActiveInfectedMax` caps reserved total. Raise carefully and watch server FPS. |
| Hordes spawn with unexpected theme | Location category missing/misspelled or lacks matching loadout, so validator changed it to `Default`. |

## Useful log lines

Search server logs for:

```text
[RaG_Hordes]
[ValidationReport]
[CanRunForFPS]
[SpawnOneInfected]
[SpawnFailureSummary]
```

Startup report should show `status=OK`. For support, include main and loadout JSON, report line, exact map, active mod set, connected player count, server FPS, and relevant error block.
