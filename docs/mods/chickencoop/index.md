# RaG ChickenCoop

RaG ChickenCoop turns vanilla `Land_misc_chickenCoop` map objects into searchable coops. Each search can produce a configured food item or feather reward and can independently spawn a hostile crazy chicken.

The mod also adds:

- cookable and peelable eggs;
- non-decaying gingerbread and chocolate bunnies;
- a custom aggressive chicken with increased health and a close-range shock effect.

[RaG Core](../core/index.md) is a hard dependency. Install and enable both mods on the server and every client. Declared addon dependencies control PBO ordering.

## Start here

- [Searching, food, and the crazy chicken](gameplay.md) explains player interactions, reward flow, egg preparation, and hostile-chicken behavior.
- [Setup, class names, and troubleshooting](server-setup-and-class-names.md) covers installation, dependencies, supported coops, distribution, and common failures.
- [Server configuration](server-configuration.md) documents the current version 1 JSON schema and exact probability calculations.

## Behavior at a glance

- Every supported coop becomes searchable shortly after it initializes.
- Searching needs no tool. Players may stand or crouch and must remain within normal interaction range for the default crafting duration.
- Each coop allows one completed search per initialization cycle.
- Default reward chance is **41%**, not 40%, because the source accepts rolls from `0` through `40`.
- A successful default reward roll is split evenly between `ChickenCoopItems` and `ChickenFeathers`.
- Crazy-chicken chance is a separate roll. A search can produce both a reward and a chicken.
- Default crazy-chicken chance is **11%**, not 10%.
- Boil an unpeeled egg to enable **Peel**. Baking or drying is not a useful preparation route because those states are forced to burned by the current scripts.

## Links

- [Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=2891195807)
- [Source repository](https://github.com/Tyson89/rag_chickencoop)
- [RaG Core documentation](../core/index.md)
- [Support RaG Tyson on Ko-fi](https://ko-fi.com/rag_tyson)

!!! warning "No monetization, repacking, or reuploading"
    Public Workshop permissions allow use on an approved monetized server only when this mod is not part of monetization. The mod itself may not be monetized, repacked, or reuploaded. Use the original Workshop release.
