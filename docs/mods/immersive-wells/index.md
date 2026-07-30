# RaG Immersive Wells

RaG Immersive Wells makes DayZ wells less predictable. Each well can be usable or broken after server initialization. Working animated pumps gain a moving handle, pump sound, and water particle. Servers may also let direct drinking or filled containers receive cholera.

[RaG Core](../core/index.md) is a hard dependency. Install and enable both mods on the server and every client. Addon dependencies control PBO ordering; server mod-list order does not.

## Start here

- [Well behavior and cholera](well-behavior-and-cholera.md) explains random water availability, player interactions, audiovisual effects, exact probabilities, and cholera transfer.
- [Setup, compatibility, and troubleshooting](server-setup-and-compatibility.md) covers installation, dependencies, supported well classes, RaG Baseitems integration, custom wells, and common failures.
- [Server configuration](server-configuration.md) documents the current version 1 JSON schema and its unvalidated values.

## Behavior at a glance

- Every ordinary `Well` object rolls its water state once, about `500` milliseconds after initialization.
- Default `WellWaterChance: 50` gives `51` successful results among `101`: about **50.5%**, not exactly 50%.
- Water state does not deplete, recover, or reroll during normal use. Map wells reroll when initialized again, normally after server restart.
- Broken wells stop drinking, container filling, and hand washing. Starting an interaction produces an empty-pump sound and a broken-well message.
- Working vanilla blue and yellow pumps animate their handles and produce a synchronized pump sound and water particle during use.
- Optional cholera transfer affects direct drinking and filled containers. Washing bloody hands does not receive cholera.
- Default cholera support is disabled. When enabled, default `WellCholeraChance: 50` produces a **51%** exposure roll.
- RaG Baseitems `Land_rag_well` is always usable and does not animate when its optional integration compiles.
- Mod adds no inventory items, placeable wells, economy XML, trader entries, or automatic well spawner.

## Links

- [Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=3406196859)
- [Source repository](https://github.com/Tyson89/RaG_Immersive_Wells)
- [RaG Core documentation](../core/index.md)
- [Support RaG Tyson on Ko-fi](https://ko-fi.com/rag_tyson)

!!! warning "No monetization, repacking, or reuploading"
    Public Workshop permissions allow use on an approved monetized server only when this mod is not part of monetization. The mod itself may not be monetized, repacked, or reuploaded.
