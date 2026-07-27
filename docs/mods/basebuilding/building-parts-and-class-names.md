# Building Parts and Class Names

The mod exposes 21 player-craftable kits. Use the exact kit class names below in admin tools, trader files, spawn systems, or economy XML.

| Structure | Kit class name | Construction stages or behavior |
| --- | --- | --- |
| Ceiling / flat roof | `RaG_BB_CeilingKit` | Single ceiling stage. |
| Double door | `RaG_BB_DoorKit` | Frame, wooden door, or metal-door upgrade. |
| Floor | `RaG_BB_FloorKit` | Single floor stage. |
| Foundation | `RaG_BB_FoundationKit` | Single foundation stage. |
| Double gate | `RaG_BB_GateKit` | Frame, left door, and right door. |
| Left gate | `RaG_BB_GateLeftKit` | Frame and left-hinged door. |
| Right gate | `RaG_BB_GateRightKit` | Frame and right-hinged door. |
| Floor hatch | `RaG_BB_Floor_HatchKit` | Frame, hatch door, staircase, or separate ladder. |
| Low wall | `RaG_BB_Low_WallKit` | Single low-wall stage. |
| Pillar | `RaG_BB_PillarKit` | Single pillar stage. |
| Ramp | `RaG_BB_RampKit` | Single ramp stage. |
| Angled roof | `RaG_BB_RoofKit` | Main roof plus optional left and right end pieces. |
| Single door | `RaG_BB_Single_DoorKit` | Frame and door. |
| Small window | `RaG_BB_Window_SmallKit` | Frame and openable window. |
| Staircase, style 2 | `RaG_BB_Staircase_2Kit` | Single staircase stage. |
| Staircase, style 1 | `RaG_BB_StaircaseKit` | Single staircase stage. |
| Stairs | `RaG_BB_StairsKit` | Single stairs stage. |
| Step ladder | `RaG_BB_StepLadderKit` | Deployable and recoverable; no construction stages. |
| Wall | `RaG_BB_WallKit` | Single wall stage. |
| Large window | `RaG_BB_WindowKit` | Frame and openable window. |
| Wooden storage | `RaG_BB_WoodStorageKit` | Floor, frame, and roof; storage appears after the roof stage. |

## Other useful class names

| Item | Class name | Use |
| --- | --- | --- |
| BaseBuilding Book | `RaG_BB_Book` | Book-based kit selection and crafting. |
| Admin hatchet | `RaG_BB_Admin_Hatchet` | Near-instant dismantling and access to the normal destroy action. |
| Admin hammer | `RaG_BB_Admin_Hammer` | Near-instant building without materials and hatch-ladder construction. |

The deployed objects, placement holograms, and `_BookHolo` preview classes also have public config entries, but they are implementation types. Do not add hologram or preview classes to the economy. Spawn or trade the kit classes instead.

The admin tools inherit public item scope from their vanilla parent classes, but they are intended for controlled admin spawning, not normal loot.

## Crafting controls

`CraftToggles` in `RaG_BaseBuilding.json` uses recipe identifiers such as `DoorKit`, `HatchKit`, and `StepLadder`; those identifiers are not item class names. See [Server configuration](server-configuration.md) before editing them.
