# RaG Evil Snowman

RaG Evil Snowman adds a hostile, bear-based snowman predator with custom sounds, a blue night light, and a configurable skinning reward pool. It also adds an edible custom carrot.

[RaG Core](../core/index.md) is a hard dependency. Load `RaG_Core` before `RaG_Evil_Snowman` on the server and every client.

## Start here

- [Gameplay and skinning rewards](gameplay-and-rewards.md) explains combat behavior, death effects, skinning, and the custom carrot.
- [Setup, spawning, class names, and troubleshooting](server-setup-and-class-names.md) covers installation, load order, event placement, public classes, and common failures.
- [Server configuration](server-configuration.md) documents the current version 1 JSON schema and reward weighting.

## Behavior at a glance

- `rag_snowman` uses DayZ bear AI, animations, movement mapping, and attack damage profiles.
- It has `5000` global health and is treated as dangerous by AI systems.
- A client-side blue spotlight is attached while it is alive and only shows outside daylight.
- Death plays a custom sound, removes the light, and triggers an M84-style particle effect.
- Vanilla pelt, meat, lard, guts, and bone yields are disabled.
- Skinning instead creates `SkinnedItemsAmount` random entries from `SnowManSkinningItems`.
- Default skinning creates three independently selected items. Repeats are possible.
- `rag_carrot` is edible, non-decaying, and cannot be cooked.

## Links

- [Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=2886730223)
- [Source repository](https://github.com/Tyson89/rag_snowman)
- [RaG Core documentation](../core/index.md)
- [Support RaG Tyson on Ko-fi](https://ko-fi.com/rag_tyson)

!!! warning "No monetization, repacking, or reuploading"
    Public Workshop permissions allow use on an approved monetized server only when this mod is not part of monetization. The mod itself may not be monetized, repacked, or reuploaded. Use the original Workshop release.
