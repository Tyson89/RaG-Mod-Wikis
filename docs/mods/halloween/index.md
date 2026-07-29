# RaG Halloween

RaG Halloween adds four server-controlled encounters and one decorative prop to DayZ:

- a pumpkin grenade that produces either treats or configured AI;
- searchable graves and mass graves;
- one-shot boogieman ambushes;
- an animated spooky pedestal that ends with either a loot coffin or configured AI;
- a static animated dragon for map decoration.

[RaG Core](../core/index.md) is a hard dependency. Load `RaG_Core` before `RaG_Halloween` on the server and every client.

## Start here

- [Gameplay and encounters](gameplay-and-encounters.md) explains every interaction, its timing, and how rewards or AI are selected.
- [Server setup, class names, and troubleshooting](server-setup-and-class-names.md) covers installation, load order, economy setup, supported world objects, and known problems.
- [Server configuration](server-configuration.md) documents the version 1 `RaG_Halloween.json` schema and the actual chance calculations used by the scripts.

## Behavior at a glance

- Pumpkin grenades are armed automatically and activate on contact after being thrown.
- A grenade produces either 2-5 configured reward items or 1-3 configured AI with the defaults.
- Eligible vanilla graves get a searchable interaction at server initialization according to a configured chance.
- Searching a grave with a non-ruined shovel produces one reward or one configured AI, then consumes that interaction.
- Walking within 5 meters of an enabled boogieman prop triggers a sound and particle effect plus 3-6 configured AI, then consumes the trigger.
- The spooky pedestal runs a 60-second animated sequence. Its coffin-or-AI result appears after 24 seconds.
- The static dragon is decorative; it has no encounter, combat, or reward logic.

## Links

- [Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=3045497789)
- [RaG Core documentation](../core/index.md)
- [Support RaG Tyson on Ko-fi](https://ko-fi.com/rag_tyson)

!!! warning "No monetization, repacking, or reuploading"
    RaG Halloween may be used on an approved monetized server, but the mod itself may not be monetized, repacked, or reuploaded. Use the original Workshop release.
