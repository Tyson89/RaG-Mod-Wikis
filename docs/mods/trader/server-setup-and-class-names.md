# Server setup and class names

## Requirements

[RaG Core](../core/index.md) is hard dependency through `CfgPatches.requiredAddons[]`. Install RaG Core and RaG Trader on server and every client. Use matching builds.

Do not prescribe command-line mod order. DayZ resolves PBO/addon ordering from declared dependencies.

## Installation and first startup

1. Stop server.
2. Install matching RaG Core and RaG Trader builds.
3. If supplied builds are signed, install their supplied signature keys in server `keys` directory.
4. Enable both mods for server and clients.
5. Start server once.
6. Check `ConfigValidationReport.txt`, then confirm registry, stock, and transaction journal initialize successfully.
7. Stop server.
8. Edit generated configs under `$profile:\RaG_Core\Configs\RaG_Trader\`.
9. Restart and test every trader, currency, vehicle spawn point, ATM, and safe zone before admitting testers.

## Generated files

Bundled defaults copy only when destination file is missing.

```text
$profile:\RaG_Core\Configs\RaG_Trader\Settings.json
$profile:\RaG_Core\Configs\RaG_Trader\Catalog.json
$profile:\RaG_Core\Configs\RaG_Trader\Locations.json
$profile:\RaG_Core\Configs\RaG_Trader\Routes.json
$profile:\RaG_Core\Configs\RaG_Trader\VehicleAttachments.json
$profile:\RaG_Core\Configs\RaG_Trader\Banking.json
$profile:\RaG_Core\Configs\RaG_Trader\Categories\<Category>.json
```

Runtime state appears after initialization/use:

```text
$profile:\RaG_Core\Configs\RaG_Trader\ConfigValidationReport.txt
$profile:\RaG_Core\Configs\RaG_Trader\Stock.json
$profile:\RaG_Core\Configs\RaG_Trader\RouteState.json
$profile:\RaG_Core\Configs\RaG_Trader\Transactions\<transaction-id>.json
$profile:\RaG_Core\Configs\RaG_Trader\Accounts\<Steam64>.json
$profile:\RaG_Core\Storage\RaG_Trader\Vehicles\<key-id>.bin
$profile:\RaG_Core\Storage\RaG_Trader\History\<Steam64>.json
$profile:\RaG_Core\Storage\RaG_Trader\EconomyTelemetry.json
```

Installer preserves existing files. Load hooks can normalize values and save the result. New bundled category installs only when referenced filename is missing. Custom missing category cannot be recreated from mod bundle.

!!! tip "Keep a clean reference profile"
    Generate defaults in an isolated server profile. Keep live custom configurations and complete persistence backups separately. Compare any candidate against that reference before deploying it.

## Build a first custom shop

Use the generated defaults as a working foundation. This exercise adds a small kiosk to an existing location group without replacing currencies or banking.

1. Stop the server and back up both Trader configuration and storage roots.
2. Save the complete category below as `Categories\Starter_Supplies.json`.
3. Append the profile object below to the existing `Catalog.json` `Traders` array. Keep existing currencies, default currency, and other profiles.
4. Duplicate a known working physical trader entry in an enabled location group. Set its `TraderId` to `starter`, its `EntityClassName` to `RaG_TrafficCone`, and its `Attachments` to `[]`.
5. Choose a separate clear position measured on your actual map. Copy all three position and orientation components accurately. Keep `VehicleSpawnPoints: []` for this non-vehicle shop.
6. Restart, read the validation report, and open the trader. Check both purchases and the earning route with an ordinary player.

Complete category:

```json
{
  "DisplayName": "Starter Supplies",
  "Listings": [
    {
      "ClassName": "Rope",
      "BuyPrice": 100,
      "SellPrice": 20,
      "InitialStock": -1,
      "MaxStock": -1
    },
    {
      "ClassName": "RaG_CarKey",
      "BuyPrice": 250,
      "SellPrice": -1,
      "InitialStock": -1,
      "MaxStock": -1
    },
    {
      "ClassName": "BearPelt",
      "BuyPrice": -1,
      "SellPrice": 800,
      "InitialStock": -1,
      "MaxStock": -1,
      "MinimumHealthPercent": 50.0
    }
  ]
}
```

Profile object to append:

```json
{
  "Id": "starter",
  "DisplayName": "Starter Supplies",
  "Categories": ["Starter_Supplies"],
  "OfferPools": []
}
```

These prices illustrate the wiring. Adjust the earning route for your map and starting equipment; bear hunting may be unsuitable for new survivors. Adding another physical entry with the same `TraderId` in one group creates a runtime-ID collision. Use a separate group for another instance of the same profile.

!!! tip "Check three connections"
    File `Starter_Supplies.json` supplies category `Starter_Supplies`. Catalog profile `starter` references that category. The physical entry's `TraderId` references profile `starter`. Matching a display name does not establish either reference.

## Trader entity placement

Each enabled static `Locations.json` entry does one of two things:

1. Finds existing map-placed entity with exact `EntityClassName` within 1 metre of configured position and binds it.
2. If none found, spawns configured entity itself.

Supported trader target is any valid `EntityAI`. Survivor classes receive configured clothing/equipment. Static trader is damage-disabled; survivor trader also cannot be destroyed. Spawned entities are deleted during mission shutdown and recreated next start.

Route-controlled groups spawn only at their active stop and do not bind existing map objects. `Routes.json` controls timing, stop policy, and route invulnerability. See [traveling traders](traveling-traders-and-routes.md).

### Object trader option

Use `RaG_TrafficCone` as a simple object trader target:

```json
{
  "TraderId": "tools",
  "EntityClassName": "RaG_TrafficCone",
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

`RaG_TrafficCone` is a scope-1 `HouseNoDestruct` target supplied by Trader. Configure its placement directly; editor visibility depends on support for scope-1 classes. Choose a survivor with a deliberate loadout when the shop should appear staffed. The coordinates here are illustrative: measure a clear position on your map.

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

Survivor loadout tries attachment slot, then hands, then inventory. Validator creates temporary objects to check equipment. Broken configured loadouts block registry startup or reject reload; fix class names, capacity, and slots before proceeding.

## ATM placement

`Locations.json` does not spawn ATMs. Place `RaG_ATM` through map editor/loader or mission object code. ATM works anywhere; banking config decides available currencies. Safe zone is not automatic around ATM.

ATM registers as network static object shortly after initialization. Keep it reachable within `InteractionDistance` and avoid placing overlapping geometry in front of interaction point.

## Class names

| Class | Scope | Purpose |
| --- | ---: | --- |
| `RaG_ATM` | `1` | Banking terminal for scripted/editor placement; editor must support scope-1 classes. |
| `RaG_TrafficCone` | `1` | Object target usable in a configured trader entry. |
| `RaG_CarKey_Admin` | `2` | Admin lock/unlock/reset tool; server requires holder in `AdminSteamIds`. Keep out of player shops and loot. |
| `RaG_CarKey` | `2` | Assign, lock/unlock, pack/deploy, spare-key crafting, and packed-car sale token. |
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
| `RaG_CarKey_Base` | `0` | Shared normal/admin key base. |
| `RaG_MoneyBase` | `0` | Base class for built-in notes. |

## Central Economy and shop possibilities

Source ships no `types.xml`. Server owner decides distribution:

- sell blank `RaG_CarKey` at tool or vehicle trader;
- add Euro notes to loot economy, quests, events, or admin rewards;
- run account-only economy with no physical notes;
- place NPC markets, terminal-only kiosks, remote ATMs, or mixed locations;
- expose same category at several trader locations for shared stock;
- duplicate listing into separate category when independent stock pool is wanted.

## Configuration acceptance workflow

1. Stop server.
2. Back up configs and runtime state.
3. Start an isolated test profile with the intended build to generate defaults.
4. Check required fields, class availability, and file references.
5. Add the intended custom entries to version-1 files.
6. Require zero blocking validation errors; inspect report and logs.
7. Check Error and Warning logs.
8. Test buy, sell, basket rollback, ATM, vehicle, key, restart persistence, and safe-zone borders.
9. Move tested files to production while server is stopped.
