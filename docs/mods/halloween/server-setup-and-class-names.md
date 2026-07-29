# Server setup, class names, and troubleshooting

## Required mod and load order

[RaG Core](../core/index.md) is required on the server and every client. Load Core first:

```text
@RaG_Core;@RaG_Halloween
```

Actual folder names can differ, but the dependency order must not.

## Installation

1. Stop the server.
2. Install the original RaG Core and RaG Halloween Workshop releases.
3. Copy both signature keys into the server's `keys` directory if the host does not do that automatically.
4. Add both mods to the client/server mod parameter, with Core first.
5. Start the server once.
6. Stop it after this file is generated:

   ```text
   RaG_Core/Configs/RaG_Halloween/RaG_Halloween.json
   ```

7. Edit the generated file, restart, and test every enabled encounter on a staging server.

The generated file is the schema for the installed build. Preserve it during updates and merge custom values into a newly generated file if the schema changes.

## Main class names

| Class name | Scope | Use |
| --- | ---: | --- |
| `rag_pumpkingrenade` | Public inventory item | Armed non-lethal grenade that produces configured rewards or AI on contact. |
| `rag_spooky_pedestal` | Public world object | Placeable or event-spawned interactive pedestal. |
| `rag_coffin` | Public world object | Large, immovable reward container normally created by the pedestal. |
| `Land_rag_static_dragon` | Protected world object | Decorative animated dragon for editor/admin placement, not normal loot. |

`rag_tombstone_interact_obj`, `BoogiemanTrigger`, and the pedestal light classes are implementation details. Do not add them to `types.xml`, traders, or custom events.

## Distribution and placement

The source project does not ship Central Economy XML or official economy values. Set counts, lifetimes, restock values, categories, and usages for your own server instead of treating third-party examples as mod defaults.

- `rag_pumpkingrenade` can be distributed through your Central Economy, trader, reward, or admin system.
- `rag_spooky_pedestal` can be placed with an editor/admin tool or added to a custom event.
- `rag_coffin` is normally created by an activated pedestal.
- `Land_rag_static_dragon` has protected scope and is intended for editor or compatible admin-tool placement.

An activated pedestal deletes itself after 60 seconds. An untouched pedestal has no script deletion timer; its lifetime depends on the system used to spawn or place it.

## Supported grave objects

The scripts recognize these exact classes and numbered families:

| Source | Supported classes |
| --- | --- |
| Vanilla static objects | `Static_Cemetery_Grave1` through `Static_Cemetery_Grave4`; `Static_Dead_MassGrave_8m`; `Static_Dead_MassGrave_15m`; `Static_Dead_pile1` through `Static_Dead_pile4` |
| Vanilla `StaticObj` objects | `StaticObj_Cemetery_Grave1` through `StaticObj_Cemetery_Grave4`; `StaticObj_Dead_MassGrave_8m`; `StaticObj_Dead_MassGrave_15m`; `StaticObj_Dead_pile1` through `StaticObj_Dead_pile4` |
| Other vanilla object | `Land_Dead_MassGrave` |
| BuilderItems integration | `bldr_Cemetery_Grave1` through `bldr_Cemetery_Grave4`; `bldr_Dead_MassGrave_8m`; `bldr_Dead_MassGrave_15m`; `bldr_Dead_pile1` through `bldr_Dead_pile4` |
| VPP Admin Tools integration | `vbldr_cemetery_grave1` through `vbldr_cemetery_grave4`; `vbldr_dead_massgrave`; `vbldr_dead_massgrave_8m`; `vbldr_dead_massgrave_15m`; `vbldr_dead_pile1` through `vbldr_dead_pile4` |

BuilderItems and VPP classes are available only when their matching integration is compiled and loaded. Custom-placed supported variants use their placed world position for the search interaction and result.

## Supported boogieman objects

The ambush trigger is attached to:

- `Static_Misc_Boogieman`;
- `StaticObj_Misc_Boogieman`;
- `bldr_Misc_Boogieman` with BuilderItems;
- `vbldr_misc_boogieman` with VPP Admin Tools.

The custom boogieman variants use their placed world position for the ambush trigger.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Startup reports missing scripts or `RaG_Core` | Core is missing, outdated, or loaded after Halloween. Both mods must be installed on server and clients. |
| `RaG_Halloween.json` is not generated | Confirm the active server profile, folder permissions, Core's configuration initialization, and the mod load order. |
| A grave has no action | `Tombstone_Enabled` must be `1`, the exact object class must be supported, the one-time initialization roll must pass, and the player must stand upright with a non-ruined shovel in range. |
| A boogieman does nothing | Confirm `BoogieMan_Enabled`, use a supported class, and remember that its 5-meter trigger is consumed after the first player enters. |
| Pumpkin grenade or encounter spawns nothing | Validate every configured classname and keep every active selection array non-empty. Load any mod that supplies a custom class. |
| Too many or too few AI spawn | Check that each minimum is less than or equal to its matching maximum. |
| Pedestal gives fewer coffins after raising its chance | This is the current script behavior. Lower `Pedestal_ChanceToSpawnCoffin` to make coffins more likely. |
| Pedestal remains forever | It deletes 60 seconds after a player uses **Are you Brave?**. An untouched pedestal has no script deletion timer; its lifetime depends on its placement or spawn system. |
| Static dragon cannot be found as loot | It is a decorative `Land_*` object with protected scope, not a normal economy inventory item. Place it with an editor or compatible admin tool. |

## Safe configuration rules

- Stop the server before editing the JSON.
- Keep valid JSON syntax and retain `Version`.
- Keep every list used by an enabled feature non-empty.
- Use valid class names available to both the server and clients.
- Keep minimum values less than or equal to their corresponding maximums.
- Restart after every configuration change; the file is loaded during server initialization.
