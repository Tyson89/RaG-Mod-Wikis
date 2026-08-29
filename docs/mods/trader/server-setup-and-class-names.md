# Server setup and class names

## Requirements

[RaG Core](../core/index.md) is hard dependency through `CfgPatches.requiredAddons[]`. Install RaG Core and RaG Trader on server and every client. Use matching builds.

Do not prescribe command-line mod order. DayZ resolves PBO/addon ordering from declared dependencies.

## First installation

1. Stop server.
2. Install original RaG Core and RaG Trader releases.
3. Copy signature keys into server `keys` directory when host does not do this automatically.
4. Enable both mods for server and clients.
5. Start server once.
6. Confirm RaG Trader reports registry ready.
7. Stop server.
8. Edit generated configs under `$profile:\RaG_Core\Configs\RaG_Trader\`.
9. Restart and test every trader, currency, vehicle spawn point, ATM, and safe zone before public use.

## Generated files

Bundled defaults copy only when destination file is missing.

```text
$profile:\RaG_Core\Configs\RaG_Trader\Settings.json
$profile:\RaG_Core\Configs\RaG_Trader\Catalog.json
$profile:\RaG_Core\Configs\RaG_Trader\Locations.json
$profile:\RaG_Core\Configs\RaG_Trader\VehicleAttachments.json
$profile:\RaG_Core\Configs\RaG_Trader\Banking.json
$profile:\RaG_Core\Configs\RaG_Trader\Categories\<Category>.json
```

Runtime state appears after initialization/use:

```text
$profile:\RaG_Core\Configs\RaG_Trader\Stock.json
$profile:\RaG_Core\Configs\RaG_Trader\Accounts\<Steam64>.json
$profile:\RaG_Core\Storage\RaG_Trader\Vehicles\<key-id>.bin
```

Existing config is never overwritten during startup. New bundled category installs only when referenced filename is missing. Custom missing category cannot be recreated from mod bundle.

!!! danger "Back up before update"
    Back up full `RaG_Trader` config, accounts, and vehicle-storage directories. Never replace live custom configs blindly with new defaults. Generate fresh defaults in test profile, then merge schema changes.

## Trader entity placement

Each enabled `Locations.json` entry does one of two things:

1. Finds existing map-placed entity with exact `EntityClassName` within 1 metre of configured position and binds it.
2. If none found, spawns configured entity itself.

Supported trader target is any valid `EntityAI`. Survivor classes receive configured clothing/equipment. Spawned trader is damage-disabled; survivor trader also cannot be destroyed. Spawned entities are deleted during mission shutdown and recreated next start.

### Terminal option

Use `RaG_TraderTerminal` as simple object trader:

```json
{
  "TraderId": "tools",
  "EntityClassName": "RaG_TraderTerminal",
  "Attachments": [],
  "Enabled": true,
  "OpeningHoursEnabled": false,
  "OpeningHour": 0,
  "ClosingHour": 24,
  "Position": [7500.0, 10.0, 7500.0],
  "Orientation": [0.0, 0.0, 0.0],
  "VehicleSpawnPoints": []
}
```

Terminal cannot enter hands, cargo, or receive cargo. It is suitable for unmanned kiosks and custom mapped shops.

### Survivor option

Survivor class example:

```json
{
  "TraderId": "hunting",
  "EntityClassName": "SurvivorM_Mirek",
  "Attachments": [
    "HuntingJacket_Brown",
    "HunterPants_Brown",
    "HikingBootsLow_Beige",
    "HuntingBag",
    "Winchester70"
  ],
  "Enabled": true,
  "OpeningHoursEnabled": false,
  "OpeningHour": 0,
  "ClosingHour": 24,
  "Position": [7500.0, 10.0, 7500.0],
  "Orientation": [180.0, 0.0, 0.0],
  "VehicleSpawnPoints": []
}
```

Attachment creation tries attachment slot, then hands, then inventory. Failed equipment logs warning but trader remains usable.

## ATM placement

`Locations.json` does not spawn ATMs. Place `RaG_ATM` through map editor/loader or mission object code. ATM works anywhere; banking config decides available currencies. Safe zone is not automatic around ATM.

ATM registers as network static object shortly after initialization. Keep it reachable within `InteractionDistance` and avoid placing overlapping geometry in front of interaction point.

## Public class names

| Class | Scope | Purpose |
| --- | ---: | --- |
| `RaG_ATM` | `2` | Placeable banking terminal. |
| `RaG_TraderTerminal` | `2` | Generic configured trader target. |
| `RaG_CarKey` | `2` | Assign, lock/unlock, pack/deploy, and spare-key crafting. |
| `RaG_Euro_1` | `2` | Physical value-1 Euro note. |
| `RaG_Euro_2` | `2` | Physical value-2 Euro note. |
| `RaG_Euro_5` | `2` | Physical value-5 Euro note. |
| `RaG_Euro_10` | `2` | Physical value-10 Euro note. |
| `RaG_Euro_20` | `2` | Physical value-20 Euro note. |
| `RaG_Euro_50` | `2` | Physical value-50 Euro note. |
| `RaG_Euro_100` | `2` | Physical value-100 Euro note. |
| `RaG_Euro_200` | `2` | Physical value-200 Euro note. |

Internal classes not for loot or mapping:

| Class | Scope | Purpose |
| --- | ---: | --- |
| `RaG_TraderTransactionVault` | `1` | Hidden escrow/recovery container. Can appear at player only when rollback cannot restore items. |
| `RaG_Hologram_Car` | `1` | Vehicle-deployment projection. |
| `RaG_MoneyBase` | `0` | Base class for built-in notes. |

## Central Economy and shop possibilities

Source ships no `types.xml`. Server owner decides distribution:

- sell blank `RaG_CarKey` at tool or vehicle trader;
- add Euro notes to loot economy, quests, events, or admin rewards;
- run account-only economy with no physical notes;
- place NPC markets, terminal-only kiosks, remote ATMs, or mixed locations;
- expose same category at several trader locations for shared stock;
- duplicate listing into separate category when independent stock pool is wanted.

## Safe update workflow

1. Stop server.
2. Back up configs and runtime state.
3. Start isolated test profile with new build to generate fresh defaults.
4. Compare schema and class list.
5. Merge wanted custom entries into fresh version-1 files.
6. Run with `StrictValidation: true`.
7. Check Error and Warning logs.
8. Test buy, sell, basket rollback, ATM, vehicle, key, restart persistence, and safe-zone borders.
9. Move tested files to production while server is stopped.
