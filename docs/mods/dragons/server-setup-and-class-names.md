# Server setup, class names, and troubleshooting

## Required mod and load order

[RaG Core](../core/index.md) is a hard dependency. Load both mods on the server and every client, with Core first:

```text
@RaG_Core;@RaG_Dragons
```

Folder names can differ, but the order must not. The internal patch names are `RaG_Core` and `RaG_Dragon`.

## First start

1. Stop the server.
2. Install and load RaG Core and RaG Dragons.
3. Start the server once.
4. Stop it after the configuration is generated.
5. Edit `RaG_Dragon.json`.
6. Start the server and confirm the selected location in the Core debug log.

The configuration is stored under the server profile:

```text
RaG_Core/Configs/RaG_Dragon/RaG_Dragon.json
```

See [Server configuration](server-configuration.md) before editing it. Configuration and timer changes require a server restart.

## Maps other than Chernarus

The generated defaults contain 63 Chernarus location entries and 69 target positions. They are wrong for other terrains.

For another map:

1. Replace the `Locations` array with entries using that map's coordinates.
2. Keep at least one location object in the array.
3. Use position strings in `X Y Z` order.
4. Start with one enabled test location and verify the attack announcement and debug log.

Do not leave `Locations` empty. The version hook interprets an empty array as missing data and restores all Chernarus defaults. To disable every target temporarily, keep the entries and set each `ENABLED` value to `0`, or set `SpawnInterval` to `0`.

## Class names

### Dragons

| Class name | Use |
| --- | --- |
| `Animal_Dragon_Airborne_Brown` | Brown encounter dragon |
| `Animal_Dragon_Airborne_Grey` | Grey encounter dragon |
| `Animal_Dragon_Airborne_Red` | Red encounter dragon |
| `Animal_Dragon_Airborne_Yellow` | Yellow encounter dragon |
| `Animal_Dragon_Airborne_Orange` | Orange encounter dragon |
| `Animal_Dragon` | Invulnerable idle/static variant; not used by the automatic spawner |

Do not add the airborne dragons to `types.xml` for normal operation. `RaG_DragonManager` creates and tracks them.

### Rewards and props

| Class name | Use |
| --- | --- |
| `RaG_Dragon_Head_Brown` | Brown head reward |
| `RaG_Dragon_Head_Grey` | Grey head reward |
| `RaG_Dragon_Head_Red` | Red head reward |
| `RaG_Dragon_Head_Yellow` | Yellow head reward |
| `RaG_Dragon_Head_Orange` | Orange head reward |
| `RaG_Dragon_Head_Trophy` | Craftable, placeable trophy base |
| `RaG_Dragon_Egg` | Decorative/admin item with no built-in hatching behavior |

Fireball and trigger classes are implementation details. Do not add them to the economy or spawn them through admin events.

## Logs

RaG Dragons uses two logging paths:

- General initialization, timer, target, spawn, and notification diagnostics go through the [RaG Core debug log](../core/server-configuration.md).
- Dragon kills and dragon-caused player deaths use the `RaG_DragonLogger` channel under the RaG Core logs directory.

`EnableDragonKillDeathLog` controls the dedicated kill/death channel. In the current code, disabling `AnnounceDragonDefeated` also suppresses the dragon-defeat log entry; dragon-caused player deaths are still passed to the kill/death channel.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Server or client script errors during startup | RaG Core is missing, outdated, or loaded after RaG Dragons. |
| No configuration file | Confirm the server profile path and that both mods reached `MissionServer.OnInit()`. |
| No dragon ever spawns | `SpawnInterval` must be above `0`, at least one location must be enabled, and the enabled entry needs at least one valid position. |
| Old `Interval` setting has no effect | Rename it to `SpawnInterval`; `Interval` is obsolete in schema version 2. |
| Only one delayed encounter occurs | `EnableDragonLoopSpawning` is `0`; this deliberately schedules one spawn after the interval. |
| Dragons appear at the wrong place | The built-in coordinates are for Chernarus. Replace `Locations` for the active terrain. |
| Expected more simultaneous dragons | Check `MaxActiveDragons`; new loop spawns stop while the live-dragon count is at the cap. |
| Skinning produces missing rewards | Validate every classname in `SkinningItems`. Invalid class names fail to create an item. |
| No trophy recipe | `EnableCraftDragonHeadTrophy` must be `1`, with at least 10 nails and 4 planks available. |
| Fire breath does not burn a player | Roof/building protection or supported admin-tool god mode may be active. |
| A fireball damages a protected player | Ground fire deliberately has no roof check. |
