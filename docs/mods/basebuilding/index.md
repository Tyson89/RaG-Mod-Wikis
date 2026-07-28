# RaG BaseBuilding

RaG BaseBuilding adds a modular construction system to DayZ: 21 craftable kits, snap-point placement, configurable material costs, doors and gates, floor hatches, storage, attachments, and admin build tools.

RaG Core is a hard dependency. Load `RaG_Core` before `RaG_BaseBuilding` on both the client and server.

## Player guides

- [Getting started](getting-started.md) - craft, place, and build your first part.
- [Building parts and class names](building-parts-and-class-names.md) - all craftable kits and the types of structures they create.
- [Book crafting](book-crafting.md) - select and craft kits through the BaseBuilding Book.
- [Construction materials](construction-materials.md) - material cost for every construction stage.
- [Attachments and storage](attachments-and-storage.md) - locks, camouflage nets, lights, barbed wire, lamps, and inventory visibility.
- [Locks, damage, and raiding](locks-damage-and-raiding.md) - supported lock systems and server damage rules.

## Server guides

- [Server setup](server-setup.md) - dependency, load order, generated files, economy guidance, and troubleshooting.
- [Server configuration](server-configuration.md) - every `RaG_BaseBuilding.json` setting explained.
- [RaG Core configuration](../core/server-configuration.md) - shared logging and framework settings.
- [Credits and permissions](credits-and-permissions.md) - project history and usage rules.

## What the source currently supports

- Vanilla Combination Locks on completed doors, gates, and the floor hatch.
- Conditional Codelock Mod integration when that mod is loaded.
- Conditional BreachingCharge compatibility.
- Openable doors, gates, windows, and floor hatches; open structures are restored closed after restart.
- Optional Christmas lights on supported parts and a portable gas lamp on the ceiling / flat roof.
- Camouflage nets and barbed wire on model-specific attachment slots.
- Hide/show actions for supported attachment and storage inventories.
- Configurable crafting, material costs, action times, tool wear, placement rules, and damage policy.


## Support the project

[Support RaG Tyson on Ko-fi](https://ko-fi.com/rag_tyson)

!!! warning "No repacking"
    RaG BaseBuilding may not be repacked or reuploaded. Use the original Workshop release.
