# Server setup and class names

## Requirements

Install **RaG Core** and **RaG Trader** on the server and all clients. In `CfgPatches`, `RaG_Trader.requiredAddons[]` declares `DZ_Data`, `DZ_Gear_Camping`, and `RaG_Core`. Any mod that supplies a configured item, vehicle, or object must be available where its classes are used.

## First startup

1. Start the server to copy the bundled configuration into its profile. Stop it before editing the initial setup.
2. Check `Traders/Locations.json` for your map. The bundled Chernarus setup spawns the Green Mountain hub, its terminals, and a separate boat trader.
3. For custom sites, place terminals through the location group's `Objects` array or your map or mission setup. Enable the features you want in `Settings.json`.
4. Start the server. Read `ConfigValidationReport.txt` in the Trader config directory, then test a purchase and a sale as a regular player.

## Configuration files

All paths below are relative to `$profile:\RaG_Core\Configs\RaG_Trader\`. Keep `"Version": 1` in the eight main JSON files. Category files have their own wrapper and omit `Version`.

| File | Controls |
| --- | --- |
| `Settings.json` | Feature switches, pricing, stock saves, and admin IDs |
| `Trading/Catalog.json` | Currencies, trader profiles, category references, and offer pools |
| `Trading/Categories/<Category>.json` | Listings, prices, stock, and purchase contents |
| `Traders/Locations.json` | Static traders, props and terminals, safe zones, and vehicle spawn points |
| `Routes/Routes.json` | Traveling traders, stops, props, and schedules |
| `Banking/Settings.json` | Banked currencies, balance limits, starting balances, and ATM fees |
| `P2P/Settings.json` | Player market boards, limits, fees, and buy orders |
| `Vehicles/Attachments.json` | Parts installed on purchased vehicles |
| `Vehicles/Garages.json` | Garage capacity, access, retrieval rules, and standalone meter sites |

Startup copies missing main files and referenced bundled categories. Create any custom category file before referencing it. See [backup sets](administration-and-recovery.md#backup-sets) for generated state.

Use the [complete JSON reference](configuration-reference.md) to find every editable field, distinguish omitted-field initializers from bundled values, and select the switches needed for each feature. The included positions target Chernarus; they are examples, not automatic map conversion.

## Build a first custom shop

Save `Trading/Categories/Starter_Supplies.json`.

```json
{
  "DisplayName": "Starter Supplies",
  "Listings": [
    {
      "ClassName": "BandageDressing",
      "BuyPrice": 50,
      "SellPrice": 10,
      "InitialStock": 10,
      "MaxStock": 30
    }
  ]
}
```

Add this object to `Traders` in `Trading/Catalog.json`.

```json
{
  "Id": "starter",
  "DisplayName": "Starter Trader",
  "Categories": ["Starter_Supplies"]
}
```

Add this object to `Locations` in `Traders/Locations.json`. Replace the example coordinates with a checked position on your map.

```json
{
  "Id": "Starter Camp",
  "Traders": [
    {
      "TraderId": "starter",
      "EntityClassName": "RaG_TrafficCone",
      "Position": [3000.0, 370.0, 6738.0],
      "Orientation": [0.0, 0.0, 0.0]
    }
  ]
}
```

Restart, approach the cone, and open the trader. The location's `TraderId` selects the catalog profile. The profile selects category files by filename without `.json`.

## Place terminals

| Class | Use |
| --- | --- |
| `RaG_ATM` | ATM. Enable banking and configure at least one physical currency for banking. |
| `StaticObj_Misc_AdvertColumn` | Default player market board. Enable P2P and use a class listed in `MarketBoardClasses`. |
| `RaG_Parking_MeterPlatform` | Virtual garage. Place the combined meter and parking platform on suitable ground or in suitable water. |
| `RaG_Parking_Meter` | Standalone virtual garage meter. Add a matching site in `Vehicles/Garages.json`. |
| `RaG_TrafficCone` | Example object trader. Bind it through a static location entry. |

The RaG objects above use scope `1`. Use placement tools that accept scope-1 classes. To spawn terminals from `Traders/Locations.json`, use [static location objects](locations-and-safezones.md#static-location-objects).

## Class names

- `RaG_CarKey` and `RaG_CarKey_Black`, `RaG_CarKey_Blue`, `RaG_CarKey_Green`, `RaG_CarKey_Pink`, `RaG_CarKey_Red`, `RaG_CarKey_White`, `RaG_CarKey_Yellow` are ordinary keys.
- `RaG_CarKey_Admin` is an admin tool. Lock, unlock, and reset actions check `AdminSteamIds`.
- `RaG_Euro_1`, `RaG_Euro_2`, `RaG_Euro_5`, `RaG_Euro_10`, `RaG_Euro_20`, `RaG_Euro_50`, `RaG_Euro_100`, and `RaG_Euro_200` are physical denominations.
- `RaG_TraderTransactionVault` and `RaG_Hologram_Car` are managed by the mod. Keep them out of loot and map placement.

Trader stock comes from its own configuration and saved counts. Configure Central Economy loot separately if you want players to find notes, keys, or shop goods in the world.

## Modded items and integrations

Catalog items and attachment sets use existing classes supplied by the installed mods. Ordinary listings and vehicle sets select exact classes; a base-class listing does not automatically create offers for every subclass. P2P allow/deny lists intentionally use inheritance matching. Test custom inventory, quantities, liquids, vehicle placement, and attachment slots with the intended server and client mod set.

The virtual garage has an `EXPANSIONMODVEHICLE` integration for supported Expansion vehicle ownership, keys, aircraft, boats, towing, and engine state. This does not make every other dealership, RaG key, or portable-packing operation support every Expansion vehicle class. See [vehicle type limits](vehicles-keys-and-storage.md#compatibility-and-ownership-limits).

Script extensions can customize trader access, offers, prices, delivery, P2P policy, accounts, and stock through `RaG_TraderModdingHooks`. These are integration points, not additional JSON options or a guarantee of compatibility with another economy mod. External account providers must implement contract version `1` with idempotent operations, durable checkpoints, and offline account support. External stock providers need durable stock and compare-and-restore support. Unsupported provider contracts are rejected; check logs and update the integration before enabling trading or recovery.
