# Server Configuration

RaG BaseBuilding generates its configuration under the server profile at:

```text
RaG_Core/Configs/RaG_BaseBuilding/RaG_BaseBuilding.json
```

Boolean settings use `0` for disabled and `1` for enabled. The JSON below is the supplied live server file provided for this wiki update. It is not identical to the clean defaults compiled into the analyzed source.

> [!IMPORTANT]
> Stop the server and back up the working file before editing it. Do not change `Version` or rename keys. Validate the JSON before restarting the server.

## Supplied server configuration

```json
{
    "Version": 2,
    "DisableAllDamage": 0,
    "DisableDamageButDoors": 1,
    "DisableDismantle": 0,
    "DisableCraftVanillaFence": 1,
    "DisableCraftVanillaWatchtower": 1,
    "BaseCanAttachXmasLights": 1,
    "BaseInfiniteLifetime": 0,
    "BaseBuildAnywhere": 1,
    "FlagBuildAnywhere": 1,
    "EnableHideShowInventory": 1,
    "ReturnKitAfterBuilt": 0,
    "EnableBuildHatchLadder": 1,
    "EnableAttachPortableGasLamp": 1,
    "BaseBuildTime": 8.0,
    "BaseDismantleTime": 15.0,
    "BaseBuildToolDamage": 1.0,
    "BaseDismantleToolDamage": 3.0,
    "BaseDestroyToolDamage": 50.0,
    "ToolDamageOnVanillaLockDestroy": 150.0,
    "HologramRotationSpeed": 0.10000000149011612,
    "DisableAllRaGBBKitCrafting": 0,
    "EnableBookKitCrafting": 1,
    "PlanksPerKitCraft": 4.0,
    "NailsPerKitCraft": 10.0,
    "BaseBuildTools": [
        "Hatchet"
    ],
    "BaseDismantleTools": [
        "Hatchet"
    ],
    "BaseDestroyTools": [
        "SledgeHammer"
    ],
    "PartCosts": [
        {
            "Part": "Pillar",
            "NAILS": 5.0,
            "PLANKS": 5.0,
            "LOGS": 1.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "Wall",
            "NAILS": 25.0,
            "PLANKS": 10.0,
            "LOGS": 4.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "DoorFrame",
            "NAILS": 20.0,
            "PLANKS": 10.0,
            "LOGS": 4.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "Door",
            "NAILS": 5.0,
            "PLANKS": 5.0,
            "LOGS": 0.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "HatchFrame",
            "NAILS": 20.0,
            "PLANKS": 10.0,
            "LOGS": 4.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "HatchDoor",
            "NAILS": 5.0,
            "PLANKS": 5.0,
            "LOGS": 0.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "HatchStaircase",
            "NAILS": 20.0,
            "PLANKS": 10.0,
            "LOGS": 0.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "HatchLadder",
            "NAILS": 10.0,
            "PLANKS": 5.0,
            "LOGS": 0.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "GateFrame",
            "NAILS": 20.0,
            "PLANKS": 10.0,
            "LOGS": 2.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "GateDoorLeft",
            "NAILS": 10.0,
            "PLANKS": 10.0,
            "LOGS": 0.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "GateDoorRight",
            "NAILS": 10.0,
            "PLANKS": 10.0,
            "LOGS": 0.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "GateLeftFrame",
            "NAILS": 20.0,
            "PLANKS": 10.0,
            "LOGS": 1.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "GateLeftDoor",
            "NAILS": 10.0,
            "PLANKS": 10.0,
            "LOGS": 0.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "GateRightFrame",
            "NAILS": 20.0,
            "PLANKS": 10.0,
            "LOGS": 1.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "GateRightDoor",
            "NAILS": 10.0,
            "PLANKS": 10.0,
            "LOGS": 0.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "WindowBigFrame",
            "NAILS": 25.0,
            "PLANKS": 10.0,
            "LOGS": 4.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "WindowBig",
            "NAILS": 5.0,
            "PLANKS": 5.0,
            "LOGS": 0.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "WindowSmallFrame",
            "NAILS": 25.0,
            "PLANKS": 10.0,
            "LOGS": 4.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "WindowSmall",
            "NAILS": 5.0,
            "PLANKS": 5.0,
            "LOGS": 0.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "AngledRoof",
            "NAILS": 25.0,
            "PLANKS": 15.0,
            "LOGS": 4.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "AngledRoofEndLeft",
            "NAILS": 5.0,
            "PLANKS": 5.0,
            "LOGS": 0.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "AngledRoofEndRight",
            "NAILS": 5.0,
            "PLANKS": 5.0,
            "LOGS": 0.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "Floor",
            "NAILS": 25.0,
            "PLANKS": 10.0,
            "LOGS": 2.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "Ramp",
            "NAILS": 15.0,
            "PLANKS": 10.0,
            "LOGS": 2.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "Ceiling",
            "NAILS": 25.0,
            "PLANKS": 10.0,
            "LOGS": 2.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "StairCase1",
            "NAILS": 60.0,
            "PLANKS": 15.0,
            "LOGS": 2.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "StairCase2",
            "NAILS": 60.0,
            "PLANKS": 20.0,
            "LOGS": 2.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "Stairs",
            "NAILS": 15.0,
            "PLANKS": 10.0,
            "LOGS": 2.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "Foundation",
            "NAILS": 30.0,
            "PLANKS": 15.0,
            "LOGS": 4.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "LowWall",
            "NAILS": 15.0,
            "PLANKS": 5.0,
            "LOGS": 2.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "WoodStorageFloor",
            "NAILS": 10.0,
            "PLANKS": 5.0,
            "LOGS": 1.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "WoodStorageFrame",
            "NAILS": 10.0,
            "PLANKS": 5.0,
            "LOGS": 0.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "WoodStorageRoof",
            "NAILS": 10.0,
            "PLANKS": 5.0,
            "LOGS": 0.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "SingleDoorFrame",
            "NAILS": 20.0,
            "PLANKS": 10.0,
            "LOGS": 2.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "SingleDoor",
            "NAILS": 5.0,
            "PLANKS": 5.0,
            "LOGS": 0.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "Ladder",
            "NAILS": 10.0,
            "PLANKS": 5.0,
            "LOGS": 0.0,
            "METALSHEETS": 0.0
        },
        {
            "Part": "MetalDoor",
            "NAILS": 5.0,
            "PLANKS": 0.0,
            "LOGS": 0.0,
            "METALSHEETS": 5.0
        }
    ],
    "CraftToggles": [
        {
            "Kit": "CeilingKit",
            "ENABLED": 1
        },
        {
            "Kit": "DoorKit",
            "ENABLED": 1
        },
        {
            "Kit": "FloorKit",
            "ENABLED": 1
        },
        {
            "Kit": "FoundationKit",
            "ENABLED": 1
        },
        {
            "Kit": "GateKit",
            "ENABLED": 1
        },
        {
            "Kit": "GateLeftKit",
            "ENABLED": 1
        },
        {
            "Kit": "GateRightKit",
            "ENABLED": 1
        },
        {
            "Kit": "HatchKit",
            "ENABLED": 1
        },
        {
            "Kit": "LowWallKit",
            "ENABLED": 1
        },
        {
            "Kit": "PillarKit",
            "ENABLED": 1
        },
        {
            "Kit": "RampKit",
            "ENABLED": 1
        },
        {
            "Kit": "RoofKit",
            "ENABLED": 1
        },
        {
            "Kit": "SingleDoorKit",
            "ENABLED": 1
        },
        {
            "Kit": "SmallWindowKit",
            "ENABLED": 1
        },
        {
            "Kit": "Staircase2Kit",
            "ENABLED": 1
        },
        {
            "Kit": "StaircaseKit",
            "ENABLED": 1
        },
        {
            "Kit": "StairsKit",
            "ENABLED": 1
        },
        {
            "Kit": "StepLadder",
            "ENABLED": 1
        },
        {
            "Kit": "WallKit",
            "ENABLED": 1
        },
        {
            "Kit": "WindowKit",
            "ENABLED": 1
        },
        {
            "Kit": "WoodStorageKit",
            "ENABLED": 1
        }
    ]
}
```

## Supplied file versus source defaults

These values differ from a freshly generated source-default configuration:

| Setting | Supplied file | Source default |
| --- | --- | --- |
| `DisableDamageButDoors` | `1` | `0` |
| `DisableCraftVanillaFence` | `1` | `0` |
| `DisableCraftVanillaWatchtower` | `1` | `0` |
| `BaseBuildAnywhere` | `1` | `0` |
| `FlagBuildAnywhere` | `1` | `0` |
| `BaseBuildTools` | `Hatchet` | `Hatchet`, `Hammer` |
| `BaseDismantleTools` | `Hatchet` | `Hatchet`, `Crowbar` |
| `BaseDestroyTools` | `SledgeHammer` | `SledgeHammer`, `Pickaxe`, `FirefighterAxe`, `WoodAxe` |

The explanations below show the **supplied file value**, because that is what this server will actually use.

## Damage and dismantling

| Setting | Supplied | Explanation |
| --- | ---: | --- |
| `Version` | `2` | Configuration schema version. Do not edit it. |
| `DisableAllDamage` | `0` | Makes all RaG BaseBuilding structures immune to damage when enabled. |
| `DisableDamageButDoors` | `1` | Protects non-door zones on structures that have door/gate parts. Windows are excluded. Direct door-zone damage remains active and explosions are redirected to a primary door zone. |
| `DisableDismantle` | `0` | Prevents players from dismantling RaG BaseBuilding parts. |
| `DisableCraftVanillaFence` | `1` | Disables the vanilla fence crafting recipe. |
| `DisableCraftVanillaWatchtower` | `1` | Disables the vanilla watchtower crafting recipe. |

## Placement, lifetime, and attachments

| Setting | Supplied | Explanation |
| --- | ---: | --- |
| `BaseCanAttachXmasLights` | `1` | Allows Christmas lights on supported base parts. |
| `BaseInfiniteLifetime` | `0` | When enabled, sets the structure lifetime to `3888000` seconds (45 days) after storage load. Despite the name, the implementation is a 45-day lifetime, not mathematical infinity. |
| `BaseBuildAnywhere` | `1` | Enables the mod's relaxed placement path for RaG BaseBuilding kits. Other mods and territory rules can still impose checks. |
| `FlagBuildAnywhere` | `1` | Enables the mod's relaxed placement path for flag placement. |
| `EnableHideShowInventory` | `1` | Enables the action used to hide or show supported storage inventories. |
| `ReturnKitAfterBuilt` | `0` | Spawns a new copy of the construction kit at the player's position when the base stage finishes. The built structure remains in place. |
| `EnableBuildHatchLadder` | `1` | Enables the separate floor-hatch ladder build action. Its cost is the `Ladder` entry in `PartCosts`; its custom dismantle action does not refund materials. |
| `EnableAttachPortableGasLamp` | `1` | Shows the portable gas-lamp attachment category on the ceiling / flat-roof structure. |
| `HologramRotationSpeed` | `0.10000000149011612` | Rotation increment used by manual hologram rotation. The long decimal is normal float serialization. |

## Action time and tool wear

| Setting | Supplied | Explanation |
| --- | ---: | --- |
| `BaseBuildTime` | `8.0` | Time required for a build action. |
| `BaseDismantleTime` | `15.0` | Time required for a dismantle action. |
| `BaseBuildToolDamage` | `1.0` | Damage applied to the tool by a build action. |
| `BaseDismantleToolDamage` | `3.0` | Damage applied to the tool by a dismantle action. |
| `BaseDestroyToolDamage` | `50.0` | Present in schema, but the analyzed RaG BaseBuilding scripts do not currently read it. Changing it has no confirmed effect. |
| `ToolDamageOnVanillaLockDestroy` | `150.0` | Tool damage applied when destroying a vanilla lock. |

## Kit crafting

| Setting | Supplied | Explanation |
| --- | ---: | --- |
| `DisableAllRaGBBKitCrafting` | `0` | Disables every normal and book-based RaG BaseBuilding kit recipe. |
| `EnableBookKitCrafting` | `1` | Enables kit preview and crafting through `RaG_BB_Book`. Normal combine recipes are controlled separately by the global and individual toggles. |
| `PlanksPerKitCraft` | `4.0` | Wooden planks required to craft a kit. |
| `NailsPerKitCraft` | `10.0` | Nails required to craft a kit. |

## Tool lists

The following arrays contain DayZ item class names. Add or remove class names to control which tools can perform each action. Class names must be spelled exactly.

| Array | Purpose | Supplied entry |
| --- | --- | --- |
| `BaseBuildTools` | Tools allowed to build parts. | `Hatchet` |
| `BaseDismantleTools` | Tools allowed to dismantle parts. | `Hatchet` |
| `BaseDestroyTools` | Intended list of tools allowed to destroy parts. It is currently defined but not consumed by the analyzed RaG BaseBuilding scripts. | `SledgeHammer` |

## Part costs

Each object in `PartCosts` controls one internal construction stage:

- `Part` is the internal part identifier. Do not rename it.
- `NAILS`, `PLANKS`, `LOGS`, and `METALSHEETS` are the required material amounts.
- Use `0.0` when a material is not required.

The supplied values, which currently match the analyzed source defaults for these entries, are summarized on [Construction materials](construction-materials.md). Repair actions consume a reduced percentage through DayZ's repair-material ratio, with a minimum of one unit for every material used by that stage. Dismantling a normal construction stage refunds the full configured stage cost; the separate floor-hatch ladder is an exception and provides no refund.

## Craft toggles

Each object in `CraftToggles` controls one kit recipe:

- `Kit` is the internal recipe identifier. Do not rename it.
- `ENABLED` uses `1` to enable the recipe and `0` to disable it.

`DisableAllRaGBBKitCrafting` disables the complete group; use individual `CraftToggles` entries when only selected recipes should be unavailable.

Valid `Kit` identifiers are:

`CeilingKit`, `DoorKit`, `FloorKit`, `FoundationKit`, `GateKit`, `GateLeftKit`, `GateRightKit`, `HatchKit`, `LowWallKit`, `PillarKit`, `RampKit`, `RoofKit`, `SingleDoorKit`, `SmallWindowKit`, `Staircase2Kit`, `StaircaseKit`, `StairsKit`, `StepLadder`, `WallKit`, `WindowKit`, and `WoodStorageKit`.

Do not replace these recipe identifiers with item class names. See [Building parts and class names](building-parts-and-class-names.md) for the mapping.
