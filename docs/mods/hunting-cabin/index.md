# RaG Hunting Cabin

RaG Hunting Cabin adds a placeable, one-piece wooden cabin. Players deploy a kit, attach the configured materials to its hologram, and finish the build with a hammer or hatchet.

The completed cabin provides:

- one openable door and eight independently openable windows;
- an interior light with its own switch;
- an attachment slot and switch for party lights;
- native vanilla combination-lock support;
- optional CodeLock Mod support;
- optional Expansion Code Lock support through the separate RaG Expansion Compat mod;
- configurable crafting, construction costs, dismantling refunds, kit returns, and snowy roof textures.

[RaG Core](../core/index.md) is a hard dependency. Install and enable both mods on the server and every client. Declared addon dependencies control PBO ordering.

## Start here

- [Building, features, and dismantling](building-features-and-dismantling.md) covers kit crafting, construction, doors, windows, lights, damage, and refunds.
- [Setup, class names, compatibility, and troubleshooting](server-setup-and-class-names.md) covers installation, dependencies, economy entries, optional lock mods, and common failures.
- [Server and CodeLock configuration](server-configuration.md) documents both generated JSON files and current source behavior.

## Behavior at a glance

- Default kit recipe: `10` wooden planks plus `50` nails.
- Default build materials: `99` nails, `100` wooden planks, `20` wooden logs, and `32` stones.
- Hammer and hatchet build the cabin. Crowbar, hatchet, and sledgehammer dismantle it.
- Default build behavior ruins the tool used. Despite the setting name `RuinHammerAfterBuilt`, this also ruins a hatchet.
- Door and all eight windows close during persistence restore after a server restart.
- Interior-light and party-light on/off state is not written to persistence and therefore resets off.
- Global cabin health is `50000`. DayZ `disableBaseDamage` makes initialized cabins invulnerable.
- Cabin class has lock and light attachment slots, but no cargo. Current source contains no hide/show-inventory action.
- Current Hunting Cabin source no longer contains native Expansion code. Expansion support lives in separate RaG Expansion Compat source.

## Links

- [Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=3117613872)
- [Source repository](https://github.com/Tyson89/rag_hunting_cabin)
- [RaG Core documentation](../core/index.md)
- [Support RaG Tyson on Ko-fi](https://ko-fi.com/rag_tyson)

!!! warning "No monetization, repacking, or reuploading"
    Public Workshop permissions allow use on an approved monetized server only when this mod is not part of monetization. The mod itself may not be monetized, repacked, or reuploaded. Use the original Workshop release.
