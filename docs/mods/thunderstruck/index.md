# RaG Thunderstruck

RaG Thunderstruck turns severe weather into a server-controlled hazard. When the configured rain and overcast thresholds are met, exposed players can be struck by lightning, lose health, have their equipment damaged, spawn configured items at the impact point, and leave a burning impact area behind.

[RaG Core](../core/index.md) is a hard dependency. Load `RaG_Core` before `RaG_Thunderstruck` on the server and every client.

## Start here

- [Gameplay and protection](gameplay-and-protection.md) explains weather activation, strike chance, damage, the warning icon, safe states, and the tinfoil hat.
- [Server setup and troubleshooting](server-setup-and-troubleshooting.md) covers installation, load order, first start, updates, and common failure modes.
- [Server configuration](server-configuration.md) documents the public `Thunderstruck.json` settings.

## Behavior at a glance

- The server evaluates weather and strike targets centrally.
- Both rain and overcast must meet their configured minimums.
- Snowfall on winter climates uses the configured rain threshold.
- The weather icon is shown only while the weather qualifies and the player is not currently protected.
- Dead or unconscious players, vehicle occupants, and players under a building or roof are not struck.
- Supported safe zones and admin-tool god mode are respected.
- An unruined tinfoil hat absorbs a strike instead of the player taking damage.
- A successful strike can damage worn equipment, weapons, melee items, and the item in the player's hands.
- The impact area is set on fire.
- A server can allow repeated strikes or limit each player to one strike until respawn or restart.

## Links

- [Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=2957868269)
- [RaG Core documentation](../core/index.md)
- [Support RaG Tyson on Ko-fi](https://ko-fi.com/rag_tyson)

!!! warning "No repacking"
    RaG Thunderstruck may not be repacked or reuploaded. Use the original Workshop release.
