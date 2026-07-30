# Server setup and troubleshooting

## Required mod

[RaG Core](../core/index.md) is required on the server and every client. Install and enable both mods. Declared addon dependencies control PBO ordering; server mod-list order does not. Use the original Workshop releases; Thunderstruck may not be repacked or reuploaded.

## Installation

1. Stop the server.
2. Install RaG Core and RaG Thunderstruck from the Workshop.
3. Copy each mod's key into the server's `keys` directory when your hosting setup does not do that automatically.
4. Add both mods to the client/server mod set.
5. Start the server once to generate `Thunderstruck.json` in the configured server profile directory.
6. Stop the server and edit the generated file.
7. Restart and test during qualifying weather.

Do not create the configuration from an old web example before first start. The generated file is the installed build's schema and therefore the correct base for that server.

## Updating safely

The Workshop build can add settings that are not present in an older `Thunderstruck.json`.

1. Stop the server and back up the existing file.
2. Update RaG Core and RaG Thunderstruck together.
3. Move the old configuration out of the active profile location.
4. Start once and let the mod generate a fresh file.
5. Stop the server.
6. Merge only your intended custom values into the fresh schema.
7. Start again and check the logs.

Do not overwrite a new generated schema with an old whole-file backup.

## Verification

For a controlled staging test:

- temporarily lower the rain and overcast minimums;
- enable the weather icon;
- use a high strike probability;
- stand outdoors while conscious and outside a vehicle;
- confirm the warning icon, strike effects, configured item spawns, equipment behavior, and any announcement;
- restore production values before reopening the server.

Avoid testing with `ReducedPlayerHealth` at a lethal or near-zero value on a live character.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Server or client reports missing scripts or dependencies | RaG Core is missing, outdated, or mismatched between server and clients. Both mods must be enabled on server and clients. |
| `Thunderstruck.json` is not created | Confirm the active server profile path, file permissions, and that the mod loaded without startup errors. |
| Weather qualifies but no icon appears | `ShowWeatherIcon` must be `1`; the player must also be alive, conscious, exposed, outside a vehicle, outside supported safe zones, and without supported god mode. |
| Icon appears but nobody is struck | The icon means the weather qualifies. Check `HitChanceRange` and `HitChance`; low probability can legitimately produce long gaps. |
| Player is struck under open cover | Protection requires building/interior detection or a roof above the player. Test the specific custom structure; unusual geometry may not register as cover. |
| Winter server never activates the hazard | Snowfall uses `MinRainIntensity`. Confirm the live weather values meet both the rain/snow and overcast thresholds. |
| Player is hit repeatedly | Set `CanGetHitAgain` to `0`. The one-hit state resets on respawn or server restart. |
| Gear is not damaged | `AllowDamagePlayerAttachments` must be `1`; then verify `AttachmentsDamageLevel`. |
| Spawned impact items are missing | Validate every class in `ThunderstruckItems` and load any mod that provides a configured class. |
| Safe-zone player can be hit | Confirm the zone comes from Expansion Market, Trader by Dr. Jones, or TraderPlus, and check for integration/compile errors after updates. |
| Admin can be hit in god mode | Use current VPP Admin Tools or Community Online Tools and inspect startup logs for compatibility errors. |
| Tinfoil hat wearer takes damage | The hat must be equipped and not ruined. Each absorbed hit damages it. |
| Logs are flooded | Return `EnableDebugLogging` to `0` after reproducing the issue. |

## Support evidence

When reporting a reproducible problem, collect:

- server and client script logs from the same session;
- the generated `Thunderstruck.json`, with private server details removed;
- the installed Workshop update timestamps for Core and Thunderstruck;
- the active mod list and installed versions;
- the map and weather mod in use;
- safe-zone or admin tools involved;
- exact steps and whether the player was under cover, in a vehicle, or wearing the tinfoil hat.
