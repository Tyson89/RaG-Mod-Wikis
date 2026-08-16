# Server configuration

Main configuration path:

```text
$profile:\RaG_Core\Configs\RaG_InfectedHorde\RaG_InfectedHorde.json
```

Stop server before editing. Keep valid JSON and retain `Version`. Restart after changes. First start generates current 104-location Chernarus list.

## Current schema example

Example below uses shortened location list. Generated file contains full defaults.

```json
{
  "Version": 3,
  "ActiveHordeMax": 5,
  "SpawnTime": 25,
  "SpawnChancePercent": 50,
  "DespawnTime": 26,
  "MinInfectedCount": 100,
  "MaxInfectedCount": 200,
  "PauseSpawningBelowFPS": 25,
  "ResumeSpawningAboveFPS": 30,
  "HordeActiveInfectedMax": 500,
  "SpawnOnlyNearPlayers": true,
  "MinimumPlayersOnline": 2,
  "PlayerActivationRadius": 1000,
  "MinimumPlayerSpawnDistance": 20,
  "DeleteOnlyAlive": true,
  "ReleaseHordeLocations": true,
  "SendSpawnMessage": true,
  "SendDespawnMessage": true,
  "SendSpawnLocation": true,
  "HordeSpawnLocations": [
    {
      "m_Name": "Elektrozavodsk",
      "m_Category": "Civilian",
      "m_SpawnAreaSize": 100,
      "m_Enabled": true,
      "m_Position": [10487.0, 2347.0]
    }
  ]
}
```

## Timing and capacity

| Setting | Default | Effect and validation |
| --- | ---: | --- |
| `Version` | `3` | Main schema version. Do not edit manually. |
| `ActiveHordeMax` | `5` | Maximum tracked hordes. `0` disables automatic spawn timer. Negative values become `0`. |
| `SpawnTime` | `25` | Minutes between attempts. Values below `1` become `1`. No immediate first attempt. |
| `SpawnChancePercent` | `50` | Chance per timed attempt after player-count check. Clamped to `0-100`. |
| `DespawnTime` | `26` | Minutes from completed formation to despawn. Negative values become `0`; `0` means wait until all infected die. |
| `MinInfectedCount` | `100` | Inclusive minimum target. Minimum `1`; cannot exceed global cap. |
| `MaxInfectedCount` | `200` | Inclusive maximum target. Raised to minimum when too low and reduced to global cap when too high. |
| `HordeActiveInfectedMax` | `500` | Global reserved population cap across hordes. Minimum `1`. |

`SpawnChancePercent` is literal percentage because code rolls inclusively from `1` through `100`. `0` never passes; `100` always passes.

## Performance and player safety

| Setting | Default | Effect and validation |
| --- | ---: | --- |
| `PauseSpawningBelowFPS` | `25` | Pauses infected creation below this measured server FPS. `0` disables FPS gating; negatives become `0`. |
| `ResumeSpawningAboveFPS` | `30` | Resume threshold. When not greater than active pause threshold, corrected to pause value plus `5`. |
| `SpawnOnlyNearPlayers` | `true` | Requires enough players online, at least one eligible player outside supported safe zones and their Basic Territories area, and an eligible player within location range. |
| `MinimumPlayersOnline` | `2` | Applied only when proximity spawning is enabled. Counts all connected players before protected-area filtering. Values below `1` become `1`. |
| `PlayerActivationRadius` | `1000` | Meters from location center to eligible player. `0` disables range check, but proximity mode still requires at least one eligible player. Negative values become `0`. |
| `MinimumPlayerSpawnDistance` | `20` | Minimum distance between each candidate infected and every living player. `0` disables distance check, not 200-meter line-of-sight check. Negative values become `0`. |

## Cleanup and messages

| Setting | Default | Effect |
| --- | ---: | --- |
| `DeleteOnlyAlive` | `true` | Living infected are always deleted during despawn. `true` leaves corpses; `false` deletes them too. Active-horde corpse cap still applies. |
| `ReleaseHordeLocations` | `true` | Frees location after despawn. `false` leaves it occupied until restart. |
| `SendSpawnMessage` | `true` | Sends global notification after first infected forms. |
| `SendDespawnMessage` | `true` | Sends global notification when horde begins despawn. |
| `SendSpawnLocation` | `true` | Adds location name to both spawn and despawn messages. |

## Automatic sanitation

At startup, invalid location entries are removed; blank categories become `Default`; spawn-area sizes below `1` become `1`; categories without matching loadout become `Default`. Corrected file is saved.

Server log receives one `[ValidationReport]` line with location, category, infected, loot, and capacity counts. `status=INVALID` means no enabled locations or no usable infected loadouts.

## Updating safely

1. Stop server and back up both JSON files.
2. Update RaG Core and RaG Infected Hordes.
3. Move old JSON files outside active config directory.
4. Start once to generate current schemas, then stop.
5. Merge intended custom values and entries into new files.
6. Restart and inspect `[RaG_Hordes]` validation log lines.

Do not overwrite newly generated schemas with whole old files.
