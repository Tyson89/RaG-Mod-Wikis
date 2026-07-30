# Server Setup

## Dependency

RaG Core is a hard dependency declared by `RaG_BaseBuilding`. Install and enable both mods on the server and clients. DayZ resolves addon/PBO ordering from declared dependencies, not the server mod-list sequence. Missing or outdated RaG Core scripts can prevent configuration, logging, or placement systems from loading.

## Generated configuration

On startup, the mod uses the server profile path:

```text
RaG_Core/Configs/RaG_BaseBuilding/RaG_BaseBuilding.json
```

Start the server once, stop it, back up the generated file, then edit it. See [Server configuration](server-configuration.md).

## Economy and trader entries

Add the kit classes players should obtain, plus `RaG_BB_Book` if book crafting is intended. The exact list is on [Building parts and class names](building-parts-and-class-names.md).

Do not add these implementation classes to `types.xml` or trader files:

- names ending in `_Hologram`;
- names ending in `_BookHolo`;
- deployed structure classes when you intend players to place kits;
- the internal `RaG_BB_Ladder` used by the floor hatch.

## Optional compatibility

- Codelock Mod: conditional compatibility is included when its `CodeLock` symbol is available.
- BreachingCharge: conditional destruction-type mapping is included when `BREACHINGCHARGE` is available.
- Basic Territories: a guarded build-tool damage hook is present for its SledgeHammer build bonus.

Expansion Code Lock is not referenced in the current source.

## Admin tools

- `RaG_BB_Admin_Hammer` builds in about 0.1 seconds and bypasses normal construction material checks.
- `RaG_BB_Admin_Hatchet` dismantles in about 0.1 seconds, bypasses normal dismantle-tool checks, and exposes the normal destroy action.

Keep these out of normal loot unless that behavior is intentional.

## Troubleshooting

### A kit recipe or book preview is missing

Check `DisableAllRaGBBKitCrafting`, `EnableBookKitCrafting`, and the matching `CraftToggles` entry. The book also needs enough attached planks and nails before its preview action appears.

### A structure will not place

Cycle snap points with **Right Arrow**, adjust height with **Page Up/Page Down**, or toggle snapping with **Down Arrow**. Also verify `BaseBuildAnywhere` and the surrounding collision/territory rules.

### A part will not build

Confirm the player has a class from `BaseBuildTools`, the exact materials for that stage, no conflicting stage, and all prerequisite stages.

### A part will not dismantle

Confirm `DisableDismantle` is off, use a class from `BaseDismantleTools`, remove dependent stages first, and empty wooden storage.

### The JSON is replaced or repaired on startup

Stop the server, validate the JSON syntax and key names, then review RaG Core logs. Do not change `Version` or rename identifiers in `PartCosts` and `CraftToggles`.
