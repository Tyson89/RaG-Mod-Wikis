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

## Public class names

| Class name | Use |
| --- | --- |
| `rag_pumpkingrenade` | Armed non-lethal grenade that produces configured rewards or AI on contact. |
| `rag_spooky_pedestal` | Placeable or event-spawned interactive pedestal. |
| `rag_coffin` | Large, immovable reward container normally created by the pedestal. |
| `Land_rag_static_dragon` | Decorative animated dragon for editor/admin placement. |

`rag_tombstone_interact_obj`, `BoogiemanTrigger`, and the pedestal light classes are implementation details. Do not add them to `types.xml`, traders, or custom events.

## Central economy examples

### Pumpkin grenade

The mod does not automatically distribute pumpkin grenades. Add `rag_pumpkingrenade` to your economy, trader, or custom reward system.

Example `types.xml` entry:

```xml
<type name="rag_pumpkingrenade">
    <nominal>5</nominal>
    <lifetime>10800</lifetime>
    <restock>1800</restock>
    <min>2</min>
    <quantmin>-1</quantmin>
    <quantmax>-1</quantmax>
    <cost>100</cost>
    <flags count_in_cargo="0" count_in_hoarder="0" count_in_map="1" count_in_player="0" crafted="0" deloot="0"/>
    <category name="containers"/>
    <usage name="Town"/>
    <usage name="Village"/>
    <usage name="School"/>
</type>
```

Tune the nominal and minimum for your server instead of copying those example counts blindly.

### Spooky pedestal

Give event-spawned pedestals an economy lifetime:

```xml
<type name="rag_spooky_pedestal">
    <lifetime>14400</lifetime>
    <flags count_in_cargo="0" count_in_hoarder="0" count_in_map="1" count_in_player="0" crafted="0" deloot="0"/>
</type>
```

Then add the pedestal as a child of a suitable static event, such as a bonfire or Santa crash:

```xml
<child lootmax="0" lootmin="0" max="1" min="1" type="rag_spooky_pedestal"/>
```

Edit the existing event rather than pasting an incomplete replacement event. The pedestal deletes itself 60 seconds after a player activates it, so the parent event controls when another one can appear.

## Supported grave objects

The scripts recognize these vanilla world-object families:

- `Static_Cemetery_Grave1` through `Static_Cemetery_Grave4`;
- `Static_Dead_MassGrave_8m` and `Static_Dead_MassGrave_15m`;
- `Static_Dead_pile1` through `Static_Dead_pile4`;
- equivalent `StaticObj_*` and `Land_Dead_MassGrave` variants;
- equivalent BuilderItems `bldr_*` variants when that integration is compiled;
- equivalent VPP StaticItems `vbldr_*` variants when that integration is compiled.

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
| A grave has no action | `Tombstone_Enabled` must be `1`, the object must be supported, the one-time initialization roll must pass, and the player needs a non-ruined shovel. |
| A boogieman does nothing | Confirm `BoogieMan_Enabled`, use a supported class, and remember that its 5-meter trigger is consumed after the first player enters. |
| Pumpkin grenade or encounter spawns nothing | Validate every configured classname and keep every active selection array non-empty. Load any mod that supplies a custom class. |
| Too many or too few AI spawn | Check that each minimum is less than or equal to its matching maximum. |
| Pedestal gives fewer coffins after raising its chance | This is the current script behavior. Lower `Pedestal_ChanceToSpawnCoffin` to make coffins more likely. |
| Pedestal remains forever | It deletes only after a player uses **Are you Brave?**. An untouched pedestal follows its Central Economy lifetime. |
| Static dragon cannot be found as loot | It is a decorative `Land_*` object with protected scope, not a normal economy inventory item. Place it with an editor or compatible admin tool. |

## Safe configuration rules

- Stop the server before editing the JSON.
- Keep valid JSON syntax and retain `Version`.
- Keep every list used by an enabled feature non-empty.
- Use valid class names available to both the server and clients.
- Keep minimum values less than or equal to their corresponding maximums.
- Restart after every configuration change; the file is loaded during server initialization.
