# Construction Materials

These are the version 2 `PartCosts` values in the supplied server configuration. They also match the analyzed source defaults. Server owners can change them in `RaG_BaseBuilding.json`.

| Internal part | Building stage | Logs | Planks | Nails | Metal sheets |
| --- | --- | ---: | ---: | ---: | ---: |
| `Pillar` | Pillar | 1 | 5 | 5 | 0 |
| `Wall` | Wall | 4 | 10 | 25 | 0 |
| `DoorFrame` | Door frame | 4 | 10 | 20 | 0 |
| `Door` | Door | 0 | 5 | 5 | 0 |
| `HatchFrame` | Floor-hatch frame | 4 | 10 | 20 | 0 |
| `HatchDoor` | Floor-hatch door | 0 | 5 | 5 | 0 |
| `HatchStaircase` | Floor-hatch staircase | 0 | 10 | 20 | 0 |
| `HatchLadder` | Floor-hatch ladder | 0 | 5 | 10 | 0 |
| `GateFrame` | Double-gate frame | 2 | 10 | 20 | 0 |
| `GateDoorLeft` | Double-gate left door | 0 | 10 | 10 | 0 |
| `GateDoorRight` | Double-gate right door | 0 | 10 | 10 | 0 |
| `GateLeftFrame` | Left-gate frame | 1 | 10 | 20 | 0 |
| `GateLeftDoor` | Left-gate door | 0 | 10 | 10 | 0 |
| `GateRightFrame` | Right-gate frame | 1 | 10 | 20 | 0 |
| `GateRightDoor` | Right-gate door | 0 | 10 | 10 | 0 |
| `WindowBigFrame` | Large-window frame | 4 | 10 | 25 | 0 |
| `WindowBig` | Large window | 0 | 5 | 5 | 0 |
| `WindowSmallFrame` | Small-window frame | 4 | 10 | 25 | 0 |
| `WindowSmall` | Small window | 0 | 5 | 5 | 0 |
| `AngledRoof` | Angled roof | 4 | 15 | 25 | 0 |
| `AngledRoofEndLeft` | Left angled-roof end | 0 | 5 | 5 | 0 |
| `AngledRoofEndRight` | Right angled-roof end | 0 | 5 | 5 | 0 |
| `Floor` | Floor | 2 | 10 | 25 | 0 |
| `Ramp` | Ramp | 2 | 10 | 15 | 0 |
| `Ceiling` | Ceiling or flat roof | 2 | 10 | 25 | 0 |
| `StairCase1` | Staircase, style 1 | 2 | 15 | 60 | 0 |
| `StairCase2` | Staircase, style 2 | 2 | 20 | 60 | 0 |
| `Stairs` | Stairs | 2 | 10 | 15 | 0 |
| `Foundation` | Foundation | 4 | 15 | 30 | 0 |
| `LowWall` | Low wall | 2 | 5 | 15 | 0 |
| `WoodStorageFloor` | Wooden-storage floor | 1 | 5 | 10 | 0 |
| `WoodStorageFrame` | Wooden-storage frame | 0 | 5 | 10 | 0 |
| `WoodStorageRoof` | Wooden-storage roof | 0 | 5 | 10 | 0 |
| `SingleDoorFrame` | Single-door frame | 2 | 10 | 20 | 0 |
| `SingleDoor` | Single door | 0 | 5 | 5 | 0 |
| `Ladder` | Ladder | 0 | 5 | 10 | 0 |
| `MetalDoor` | Metal door | 0 | 0 | 5 | 5 |

> [!NOTE]
> Wooden storage is built in three stages. Its combined default cost is 1 log, 15 planks, and 30 nails.

Repairing consumes a reduced percentage of the relevant stage cost, with a minimum of one unit for each material that stage normally uses. Dismantling a normal construction stage refunds its full configured cost as stacks on the ground. Destroying a stage does not use this refund path. The separate floor-hatch ladder uses a custom dismantle action and does not refund its materials.

See [Server configuration](server-configuration.md) for the complete JSON file and explanations of every setting.
