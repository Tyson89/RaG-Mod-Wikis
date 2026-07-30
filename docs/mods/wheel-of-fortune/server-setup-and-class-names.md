# Setup, placement, class names, and troubleshooting

## Required mod

[RaG Core](../core/index.md) is hard dependency declared through `CfgPatches.requiredAddons[]`. Install and enable RaG Core and RaG Wheel of Fortune on server and every client. DayZ resolves addon/PBO ordering from declared dependencies; server `-mod` list order does not.

## Installation

1. Stop server.
2. Install original RaG Core and RaG Wheel of Fortune Workshop releases.
3. Copy signature keys into server `keys` directory if host does not do that automatically.
4. Add both mods to client/server mod set.
5. Start server once.
6. Connect one test player so spin manager initializes.
7. Stop server after these files appear:

   ```text
   $profile:\RaG_Core\Configs\RaG_Wheel_Of_Fortune\RaG_Wheel_Of_Fortune.json
   $profile:\RaG_Core\Configs\RaG_Wheel_Of_Fortune\WheelData.json
   ```

8. Edit reward file if needed.
9. Place at least one `RaG_Wheel_Of_Fortune` through chosen mapping or object-spawn system.
10. Restart and test normal field, jackpot, invalid second attempt, persistence, and next-day reset.

Generated reward file is schema for installed build. Back it up during updates and merge custom values into freshly generated schema when fields change.

Main reward JSON registers during mission initialization. `WheelData.json` appears only when spin manager initializes, normally during first player connection.

## Placement

Current source contains:

- no placement kit;
- no crafting recipe;
- no built-in spawner;
- no Central Economy XML;
- no official placement JSON example;
- no custom persistence implementation.

Place `RaG_Wheel_Of_Fortune` as static world object with admin mapping tool, map editor/loader, or server mission code. Exact persistence and respawn behavior belongs to chosen placement system.

Do not add wheel only to `types.xml` and expect usable map placement. It is building object, not normal loot item.

Leave clear ground around model prize position. Rewards spawn loose on surface and can overlap nearby props or become hard to collect.

## Public class names

| Class name | Type | Use |
| --- | --- | --- |
| `RaG_Wheel_Of_Fortune` | `BuildingSuper` / static wheel base | Place this complete interactive object in world. |
| `RaG_Fortune_Wheel` | `ItemBase` internal attachment | Wheel face automatically created and locked onto base. Do not distribute separately. |

Base schedules attachment creation `250` milliseconds after initialization. If internal wheel is missing, server recreates it and locks attachment slot. Players cannot detach or release it, and attachment UI is hidden.

## Object durability

Base inherits vanilla `HouseNoDestruct`, whose destruction type is `DestructNo`. Mod also configures `500000` global health. Internal wheel has `500000` global health and explicitly ignores frag-grenade health, blood, and shock damage.

This is static attraction, not raidable storage. It exposes no usable cargo and no player-managed attachment slot.

## Multiple wheels

Several bases may be placed. Each object has independent animation and five-second cooldown, but all use same server-wide `WheelData.json`.

Result: one spin per Steam64 ID across all wheels. More wheels increase access and throughput for different players, not daily spins per player.

## Current-source limitations

- Daily spin count is fixed at one.
- Daily reset date is not checked continuously.
- No token, payment, item-in-hand, territory, faction, or permission requirement exists.
- No per-wheel reward profile exists; all wheels share one JSON.
- No prize ownership protection exists.
- No fallback reward or failed-spin refund exists.
- Undetected landing field can leave wheel permanently busy until object recreation or server restart.
- No admin command resets one player.
- No direct odds settings exist.
- No player-facing countdown exists.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Server reports missing `RaGConfigVersioned`, `RaGConfigIO`, `RaGConfigAPI`, `RaGCoreFS`, `RaG_CoreLogger`, `RaG_RPC`, or `EffRaGConfetti` | RaG Core missing, outdated, or mismatched between server and clients. Use matching builds. |
| JSON files do not generate | Confirm active server profile, folder permissions, RaG Core startup, and both mods enabled. Expected folder is `$profile:\RaG_Core\Configs\RaG_Wheel_Of_Fortune\`. |
| Wheel does not appear | Mod has no spawner. Place `RaG_Wheel_Of_Fortune` with map/object system and verify exact class case. |
| **Spin Wheel** action missing | Target base at normal interaction range. Confirm internal `RaG_Fortune_Wheel` exists, wheel is not spinning/cooling down, and client/server mod versions match. |
| Player gets “already spun” on another wheel | Expected. Eligibility is shared across all wheel objects. |
| New calendar day started but player still blocked | Current manager did not recheck date. Restart server after server-local midnight. |
| Player received no prize but daily spin is gone | Check RaG Core error log for field index, empty class, invalid class, or failed object creation. Spin is recorded first. |
| Prize spawns but player cannot find it | Check ground at wheel's `spawn_pos`; clear nearby objects and uneven terrain. Prize is not inserted into inventory. |
| Jackpot field errors | Keep `ItemFieldJackpot` non-empty and use valid `ItemBase` classes. |
| Normal field errors | Keep matching `ItemField2` through `ItemField16` non-empty and valid. |
| Jackpot notification missing | Set `EnableAnnounceJackpot` to `1`; notification occurs only after jackpot prize successfully spawns. |
| Effects or sounds missing for some clients | Confirm clients load matching Wheel and RaG Core builds. RPC drives client effects. |
| Wheel stays busy after spin | Check debug log for wheel index. Empty or invalid reward class calls immediate reset; undetected index (`-1`) does not. Recreate object or restart server. |
| Clearing `WheelData.json` while online changes nothing | In-memory list remains authoritative and may overwrite file. Stop server before state edits. |

## Safe operating rules

- Stop server before editing JSON.
- Keep reward array and every normal field populated.
- Use tested `ItemBase` classes.
- Schedule restart after server-local midnight when exact daily reset matters.
- Keep `WheelData.json` private.
- Test prize spawn area after map changes.
- Retest all configured modded rewards after dependency updates.
