# Server Configuration

RaG Baseitems generates its configuration under the server profile at:

```text
RaG_Core/Configs/RaG_Baseitems/RaG_Baseitems.json
```

Boolean settings use `0` for disabled and `1` for enabled.

> [!IMPORTANT]
> Stop the server and back up the working file before editing it. Do not change `Version`, rename keys, or change the internal `Item` identifiers. Validate the JSON before restarting the server.

## Supplied server configuration

The JSON below matches the server file supplied for this wiki update. It is a valid complete schema example, but it is **not** the current source's factory-default output.

The current source defaults differ in these places:

| Setting | Source default | Supplied file |
| --- | ---: | ---: |
| `RepairStationRepairedHealth` | `1` | `0` |
| `SewingMachineRepairedHealth` | `1` | `0` |
| `DisableDamage` | `0` | `1` |
| `EnableWeaponCleanerSound` | `1` | `0` |
| `EnableXmasTreeGifts` | `0` | `1` |
| `XmasTreeMaxGiftsAmount` | `7` | `6` |

The supplied Christmas reward arrays are also customized. Existing server files are loaded as-is; source defaults matter mainly when generating a new configuration or adding a missing field.

```json
{
    "Version": 1,
    "RepairStationRepairedHealth": 0,
    "WeaponCleanerRepairedHealth": 0,
    "SewingMachineRepairedHealth": 0,
    "AmmoCleanerRepairedHealth": 0,
    "TableSawMaxGainedWoodenPlanks": 10,
    "DisableDamage": 1,
    "AlwaysShowProxies": 0,
    "EnableWeaponCleanerSound": 0,
    "EnableTrashcanSound": 1,
    "EnableCarliftNotifications": 1,
    "CarliftRepairAllAttachments": 1,
    "EnableCraftDecoPumpkin": 1,
    "EnableCraftCoffeeCup": 1,
    "EnableCraftCraftPlasticSheets": 1,
    "EnableCraftCraftMetalSheets": 1,
    "EnableCraftCraftVintageTV_NoLegs": 1,
    "EnableDamageCarliftNotebook": 1,
    "EnableClearTrashcanAfterRestart": 1,
    "EnableCoffeeStaminaBoost": 1,
    "CarliftNotebookDamageAmount": 10.0,
    "EnableMineChristmasTree": 0,
    "EnableXmasTreeGifts": 1,
    "XmasTreeMinGiftsAmount": 4,
    "XmasTreeMaxGiftsAmount": 6,
    "XmasStockingsMinGiftsAmount": 4,
    "XmasStockingsMaxGiftsAmount": 8,
    "ChristmasDay": 24,
    "ChristmasMonth": 12,
    "XmasTreeGifts": [
        "rag_baseitems_repair_station_kit",
        "rag_baseitems_workbench_kit",
        "rag_baseitems_magpump_kit",
        "rag_baseitems_weapon_cleaner_kit",
        "rag_baseitems_carlift_kit",
        "rag_baseitems_notebook",
        "rag_baseitems_military_locker_threedoor_kit",
        "rag_baseitems_smoker_kit",
        "rag_baseitems_coffee_machine_kit",
        "rag_baseitems_sewing_machine_kit",
        "rag_baseitems_solarpanel_kit",
        "rag_baseitems_grammophone_kit",
        "rag_baseitems_table_saw_kit",
        "RaG_NailBox",
        "TTC_M82",
        "TTC_GEVAR43_Green",
        "rag_m249",
        "rag_benelli",
        "rag_PKP",
        "rag_fd_338",
        "RaG_MCX_SPEAR",
        "rag_viking_belt",
        "rag_og_huntingbag",
        "rag_og_jacket",
        "rag_og_vest",
        "TTC_M300_BLOOD"
    ],
    "XmasStockingsGifts": [
        "Candycane_Green",
        "Candycane_Red",
        "ZagorkyChocolate",
        "ZagorkyPeanuts",
        "Candycane_RedGreen",
        "ChristmasHeadband_Antlers",
        "SantasBeard",
        "WoolGlovesFingerless_ChristmasBlue",
        "WoolGlovesFingerless_ChristmasRed",
        "Candycane_Yellow"
    ],
    "XmasCalendarsGifts": [
        "Candycane_Green",
        "Candycane_Red",
        "ZagorkyChocolate",
        "ZagorkyPeanuts",
        "Candycane_RedGreen",
        "ChristmasHeadband_Antlers",
        "SantasBeard",
        "WoolGlovesFingerless_ChristmasBlue",
        "WoolGlovesFingerless_ChristmasRed",
        "Candycane_Yellow"
    ],
    "WorkbenchCrafting": [
        {
            "Item": "Flamingo",
            "ENABLED": 1
        },
        {
            "Item": "FishingBox",
            "ENABLED": 1
        },
        {
            "Item": "BeachBall",
            "ENABLED": 1
        },
        {
            "Item": "VolleyBall",
            "ENABLED": 1
        },
        {
            "Item": "AmmoCleaner",
            "ENABLED": 1
        },
        {
            "Item": "MetalAmmoBox",
            "ENABLED": 1
        },
        {
            "Item": "MetalAmmoBoxBlack",
            "ENABLED": 1
        },
        {
            "Item": "MetalAmmoBoxGreen",
            "ENABLED": 1
        },
        {
            "Item": "FirewoodHolder",
            "ENABLED": 1
        },
        {
            "Item": "BarrelFurnace",
            "ENABLED": 1
        },
        {
            "Item": "WateringCan",
            "ENABLED": 1
        },
        {
            "Item": "TrashCan",
            "ENABLED": 1
        },
        {
            "Item": "WallPicture",
            "ENABLED": 1
        },
        {
            "Item": "GrenadeCrate",
            "ENABLED": 1
        },
        {
            "Item": "PistolAmmoCrate",
            "ENABLED": 1
        },
        {
            "Item": "SmallGunCrate",
            "ENABLED": 1
        },
        {
            "Item": "SmokeGrenadeCrate",
            "ENABLED": 1
        },
        {
            "Item": "LargeRifleCrate",
            "ENABLED": 1
        },
        {
            "Item": "LargeShotgunCrate",
            "ENABLED": 1
        },
        {
            "Item": "RifleAmmoCrate",
            "ENABLED": 1
        },
        {
            "Item": "ShotgunAmmoCrate",
            "ENABLED": 1
        },
        {
            "Item": "WellsFargoCrate",
            "ENABLED": 1
        },
        {
            "Item": "LargeSlideCrate",
            "ENABLED": 1
        },
        {
            "Item": "MilitaryCrate",
            "ENABLED": 1
        },
        {
            "Item": "WaterBarrel",
            "ENABLED": 1
        },
        {
            "Item": "Plants",
            "ENABLED": 1
        },
        {
            "Item": "GrindStone",
            "ENABLED": 1
        },
        {
            "Item": "Carpet",
            "ENABLED": 1
        },
        {
            "Item": "DoorBell",
            "ENABLED": 1
        },
        {
            "Item": "CableReel",
            "ENABLED": 1
        },
        {
            "Item": "SpotLight",
            "ENABLED": 1
        },
        {
            "Item": "BatteryCharger",
            "ENABLED": 1
        }
    ]
}
```

## Repair results and general behavior

Repair-result settings use this condition scale: `0` pristine, `1` worn, `2` damaged, `3` badly damaged, and `4` ruined.

| Setting | Supplied value | Explanation |
| --- | ---: | --- |
| `Version` | `1` | Configuration schema version. Do not edit it. |
| `RepairStationRepairedHealth` | `0` | Resulting condition of items repaired at the Repair Station. |
| `WeaponCleanerRepairedHealth` | `0` | Resulting condition of items repaired in the Weapon Cleaner. |
| `SewingMachineRepairedHealth` | `0` | Resulting condition of items repaired with the Sewing Machine. |
| `AmmoCleanerRepairedHealth` | `0` | Resulting condition of items repaired in the Ammo Cleaner. |
| `TableSawMaxGainedWoodenPlanks` | `10` | Exclusive upper bound used by the Table Saw's random output. `10` currently produces 4-9 planks. Use a value greater than `4`. |
| `DisableDamage` | `1` | Disables damage to supported RaG Baseitems objects. |
| `AlwaysShowProxies` | `0` | Keeps proxy attachments visible instead of hiding them when supported containers close. |

## Sounds, notifications, and car lift

| Setting | Supplied value | Explanation |
| --- | ---: | --- |
| `EnableWeaponCleanerSound` | `0` | Enables the Weapon Cleaner operating sound. |
| `EnableTrashcanSound` | `1` | Enables the Trash Can operating sound. |
| `EnableCarliftNotifications` | `1` | Displays in-game car-lift diagnostic results. |
| `CarliftRepairAllAttachments` | `1` | Allows the car lift to repair all supported damaged vehicle attachments found by the diagnostic. |
| `EnableDamageCarliftNotebook` | `1` | Damages the attached notebook after each diagnostic scan. |
| `CarliftNotebookDamageAmount` | `10.0` | Health damage applied to the notebook after each completed scan. Set `0.0` for no damage without disabling the toggle. |

## Standalone crafting and utility toggles

| Setting | Supplied value | Explanation |
| --- | ---: | --- |
| `EnableCraftDecoPumpkin` | `1` | Enables crafting a decorative pumpkin. |
| `EnableCraftCoffeeCup` | `1` | Enables the coffee-cup crafting recipe. |
| `EnableCraftCraftPlasticSheets` | `1` | Enables crafting small plastic sheets. The repeated `Craft` is part of the real key and must not be removed. |
| `EnableCraftCraftMetalSheets` | `1` | Enables crafting small metal sheets. The repeated `Craft` is part of the real key and must not be removed. |
| `EnableCraftCraftVintageTV_NoLegs` | `1` | Enables crafting the legless vintage TV. The repeated `Craft` is part of the real key and must not be removed. |
| `EnableClearTrashcanAfterRestart` | `1` | Clears Trash Can contents after a server restart. |
| `EnableCoffeeStaminaBoost` | `1` | Enables the stamina effect from drinking coffee. |

## Christmas event

Christmas date checks use the real server date and time, not the in-game date.

| Setting | Supplied value | Explanation |
| --- | ---: | --- |
| `EnableMineChristmasTree` | `0` | Enables the Christmas Tree mining or harvesting interaction. |
| `EnableXmasTreeGifts` | `1` | Enables gift-box spawning at the Christmas Tree on the configured date. |
| `XmasTreeMinGiftsAmount` | `4` | Minimum gift boxes spawned at the tree. |
| `XmasTreeMaxGiftsAmount` | `6` | Maximum gift boxes spawned at the tree. |
| `XmasStockingsMinGiftsAmount` | `4` | Minimum items produced when a Christmas stocking is opened. |
| `XmasStockingsMaxGiftsAmount` | `8` | Exclusive upper bound for stocking output in the current code; `8` produces at most 7 items. |
| `ChristmasDay` | `24` | Real calendar day used for the Christmas event. |
| `ChristmasMonth` | `12` | Real calendar month used for the Christmas event. |

The three gift arrays contain DayZ item class names:

| Array | Purpose |
| --- | --- |
| `XmasTreeGifts` | Random item pool for Christmas Tree gift boxes. Each box selects an entry from this list. |
| `XmasStockingsGifts` | Random item pool used when a Christmas stocking is opened. |
| `XmasCalendarsGifts` | Random item pool used by calendar doors, limited to one reward per day. |

Class names are case-sensitive. Custom items require the mod that defines them. Keep minimum amounts less than or equal to the corresponding maximum amounts.

## Workbench crafting

`WorkbenchCrafting` is an array of recipe controls:

- `Item` is the internal recipe identifier. Do not rename it.
- `ENABLED` uses `1` to enable the recipe and `0` to disable it.

| Internal item | Recipe |
| --- | --- |
| `Flamingo` | Flamingo |
| `FishingBox` | Fishing tackle box |
| `BeachBall` | Beach ball |
| `VolleyBall` | Volleyball |
| `AmmoCleaner` | Ammo Cleaner |
| `MetalAmmoBox` | Default metal ammunition box |
| `MetalAmmoBoxBlack` | Black metal ammunition box |
| `MetalAmmoBoxGreen` | Green metal ammunition box |
| `FirewoodHolder` | Firewood holder |
| `BarrelFurnace` | Barrel furnace |
| `WateringCan` | Watering can |
| `TrashCan` | Trash Can |
| `WallPicture` | Wall painting |
| `GrenadeCrate` | Grenade crate |
| `PistolAmmoCrate` | Pistol-ammunition crate |
| `SmallGunCrate` | Small-gun crate |
| `SmokeGrenadeCrate` | Smoke-grenade crate |
| `LargeRifleCrate` | Large-rifle crate |
| `LargeShotgunCrate` | Large-shotgun crate |
| `RifleAmmoCrate` | Rifle-ammunition crate |
| `ShotgunAmmoCrate` | Shotgun-ammunition crate |
| `WellsFargoCrate` | Wells Fargo crate |
| `LargeSlideCrate` | Large slide crate |
| `MilitaryCrate` | Military crate |
| `WaterBarrel` | Water barrel |
| `Plants` | Decorative plants |
| `GrindStone` | Grindstone |
| `Carpet` | Carpets |
| `DoorBell` | Doorbell |
| `CableReel` | Cable reel |
| `SpotLight` | Spotlight |
| `BatteryCharger` | Battery charger |

See [Workbench recipes](workbench.md) for documented material requirements.
