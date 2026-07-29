# RaG Baseitems

RaG Baseitems adds placeable furniture, storage, workstations, decorations, powered devices, and seasonal systems to DayZ. The current source declares **355 public item classes across 23 content modules**; this wiki focuses on the items that need setup or have gameplay behavior.

## Start here

- [Server setup and troubleshooting](server-setup-and-troubleshooting.md)
- [Server configuration](json-file-explanation.md)
- [Key classnames](key-classnames.md)
- [Codelock integration](codelock-integration.md)
- [Workbench recipes](workbench.md)

## Workstations and utilities

| System | What it does |
| --- | --- |
| [Car lift](carlift.md) | Raises, scans, and repairs supported vehicles. |
| [Repair Station](repair-station.md) | Repairs one whetstone-compatible item using a Grindstone. |
| [Weapon Cleaner](weapon-cleaner.md) | Repairs one weapon-cleaning-kit-compatible item. |
| [Ammo Cleaner](ammo-cleaner.md) | Repairs one ammunition stack using disinfectant and power. |
| [Sewing Machine](sewing-machine.md) | Repairs one compatible clothing item using thread and a needle. |
| [Table Saw](table-saw.md) | Converts wooden logs into planks. |
| [Workbench](workbench.md) | Crafts crates, utilities, decorations, and electrical items. |
| [Coffee system](coffee-machine.md) | Grinds beans and brews coffee or espresso. |
| [Smoker](smoker.md) | Dries meat and fish with wooden-stick fuel. |
| [Solar Panel](solar-panel.md) | Powers devices by day and uses an attached truck battery at night. |

## More interactive systems

- [Sleeping Bags](sleeping-bags.md)
- [Christmas Event](christmas-event.md)
- [Other Interactive Items](other-interactive-items.md): Magazine Pump, Beer Barrel, Trash Can, TV, gramophone, lights, doorbell, paintable wall art, carpets, and more.

## Content categories

The source also includes cabinets, drawers, chests, lockers, safes, fridges, wooden shelves, gun walls, medical storage, shelters, greenhouses, garden objects, plants, wall pictures, summer items, Christmas items, and static building props.

Most large objects are deployed from a `_kit` classname. Workbench outputs and small placeable objects may use their final classname directly. See [Key classnames](key-classnames.md) before editing `types.xml` or trader files.

## Required dependency

**RaG Core is required.** It provides the shared configuration, logging, RPC, and liquid systems used by RaG Baseitems. A separate RaG Liquid Framework installation is obsolete and must not be added.

- [RaG Core wiki](../core/index.md)
- [Discord](https://discord.gg/MRfe4c9h3x)
- [Ko-fi](https://ko-fi.com/rag_tyson)
- [Patreon](https://patreon.com/RaGTyson)

!!! warning "No monetization, repacking, or reuploading"
    RaG Baseitems may be used on an approved monetized server, but the mod itself may not be monetized, repacked, or reuploaded. Use the original Workshop release.
