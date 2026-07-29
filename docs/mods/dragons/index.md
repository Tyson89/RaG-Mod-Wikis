# RaG Dragons

RaG Dragons adds server-driven dragon encounters to DayZ. Dragons fly to configured map locations, burn exposed players and infected, retaliate against attackers with fireballs, and can be skinned for configurable rewards and a color-matched head.

[RaG Core](../core/index.md) is a hard dependency. Load `RaG_Core` before `RaG_Dragon` on the server and every client.

## Start here

- [Gameplay and rewards](gameplay-and-rewards.md) explains encounters, fire damage, hunting, skinning, and trophies.
- [Server setup, class names, and troubleshooting](server-setup-and-class-names.md) covers load order, first start, logs, custom maps, and spawnable classes.
- [Server configuration](server-configuration.md) documents the current version 2 JSON schema and spawn lifecycle.

## Current behavior at a glance

- One of five airborne color variants is selected for each encounter.
- A target is selected from the enabled location entries.
- The dragon approaches the target and starts using fire breath within roughly 100 meters.
- Players, animals, and vehicles are not selected as normal AI targets.
- A player who damages the dragon becomes its target and receives counter-fireballs.
- Dragons have 10,000 global health in the current config.
- Fire damages the player, worn equipment, and the item in the player's hands.
- Fireballs leave a damaging ground-fire area and directly damage vehicles and their attachments.
- A killed airborne dragon can be skinned for configured items and a matching head.

The mod's built-in spawner is configured for Chernarus by default. Other maps need their own target coordinates.

## Links

- [Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=3310715247)
- [RaG Core configuration](../core/server-configuration.md)
- [Support RaG Tyson on Ko-fi](https://ko-fi.com/rag_tyson)

!!! warning "No monetization, repacking, or reuploading"
    RaG Dragons may be used on an approved monetized server, but the mod itself may not be monetized, repacked, or reuploaded. Use the original Workshop release.
