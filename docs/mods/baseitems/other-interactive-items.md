# Other Interactive Items

## Magazine Pump

The powered Magazine Pump loads or unloads one attached magazine one cartridge at a time.

- **Fill:** put a magazine in its attachment slot and compatible loose ammunition stacks in cargo.
- **Empty:** attach a non-empty magazine; the pump creates or fills matching ammo piles in cargo.
- The pump preserves cartridge type and damage values and applies normal magazine-manipulation wear.

Key classnames: `rag_baseitems_magpump_kit`, `rag_baseitems_magpump`.

## Beer Barrel

Fill the barrel with exactly 20,000 ml of water and attach 10 quantity of `rag_baseitems_beer_hop`. Brewing takes 20 seconds, deletes the hops, and converts the full barrel to beer.

Key classnames: `rag_baseitems_beer_barrel_kit`, `rag_baseitems_beer_hop`.

Beer liquid behavior is supplied by required RaG Core.

## Trash Can

The Trash Can accepts cargo and provides an interaction that removes stored contents. `EnableTrashcanSound` controls its sound. When `EnableClearTrashcanAfterRestart` is enabled, persisted contents are cleared as the object loads after a restart.

Key classnames: `rag_baseitems_trashcan_kit`, `rag_baseitems_trashcan_static_kit`.

## TV and gramophone

- Vintage televisions have start and stop interactions when their power requirements are met.
- A Vintage TV can be converted to the legless kit with a Hand Saw or Hacksaw when its standalone recipe is enabled.
- The gramophone supports start, stop, and volume controls and plays the mod's included music.

## Lighting and electrical items

The source includes table lamps, a lantern with an update/toggle action, a Spotlight, Battery Charger, Cable Reel, Christmas lantern, control units, and electrical wires. The [Solar Panel](solar-panel.md) can power compatible devices.

Workbench electrical recipes consume either `rag_baseitems_control_unit` or `rag_baseitems_electric_wires` in the electronics slot.

## Doorbell, globe, wall pictures, and carpets

- Doorbells provide a ring interaction.
- The globe can be spun.
- Unpainted wall pictures accept multiple spray designs and can be cleaned.
- Carpets accept multiple spray patterns.
- A decorative pumpkin has an optional standalone crafting action.

Their crafting toggles are documented in [Server Configuration](json-file-explanation.md), and Workbench material costs are in [Workbench Recipes](workbench.md).
