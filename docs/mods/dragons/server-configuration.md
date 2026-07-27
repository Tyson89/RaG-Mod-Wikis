# Server configuration

RaG Dragons stores its versioned server configuration at:

```text
RaG_Core/Configs/RaG_Dragon/RaG_Dragon.json
```

Stop the server before editing the file. Keep valid JSON syntax, retain `Version`, and restart the server after every change.

## Current schema example

This is a complete schema example with a shortened custom location list. A first start generates the full Chernarus list.

```json
{
  "Version": 2,
  "SpawnInterval": 15,
  "MaxActiveDragons": 3,
  "EnableDragonLoopSpawning": 1,
  "EnableDragonKillDeathLog": 1,
  "AnnounceDragonAttackLocation": 1,
  "AnnounceDragonDefeated": 1,
  "EnableCraftDragonHeadTrophy": 1,
  "SkinningItems": [
    "NorseHelm",
    "Chainmail_Coif",
    "Chainmail",
    "WoodAxe"
  ],
  "SkinnedItemsAmount": 3,
  "Locations": [
    {
      "name": "Svetlojarsk",
      "pos": [
        "13935 20 13227"
      ],
      "ENABLED": 1
    },
    {
      "name": "NWAF",
      "pos": [
        "4537 339 9591",
        "5067 339 9777"
      ],
      "ENABLED": 1
    }
  ]
}
```

## Settings

| Setting | Default | Effect |
| --- | ---: | --- |
| `Version` | `2` | Configuration schema version. Do not change it manually. |
| `SpawnInterval` | `15` | Minutes between spawn attempts. `0` or a negative value disables the automatic spawner. |
| `MaxActiveDragons` | `3` | Maximum live dragons tracked by the automatic spawner. Values below `1` are corrected during load. |
| `EnableDragonLoopSpawning` | `1` | Enables the immediate first spawn, repeating timer, and one-second replacement after a tracked dragon dies or is deleted. |
| `EnableDragonKillDeathLog` | `1` | Enables the dedicated `RaG_DragonLogger` kill/death channel. |
| `AnnounceDragonAttackLocation` | `1` | Sends a global **DRAGON UNLEASHED** notification naming the selected location. |
| `AnnounceDragonDefeated` | `1` | Sends the global player-kill notification. In the current code this also gates the dragon-defeat log line. |
| `EnableCraftDragonHeadTrophy` | `1` | Enables the 10-nail and 4-plank trophy-base recipe. |
| `SkinningItems` | Four class names | Pool used for extra skinning rewards. Each draw is independent, so duplicates are possible. |
| `SkinnedItemsAmount` | `3` | Number of random items created when a spawned dragon is skinned. `0` disables the extra-item loop but not the matching head. |
| `Locations` | Chernarus list | Named attack targets. Only entries with `ENABLED` set to `1` participate in random selection. |

Boolean settings should be `0` or `1`.

## Spawn lifecycle

`EnableDragonLoopSpawning` changes more than timer repetition.

### Loop spawning enabled

1. One dragon is spawned immediately during server initialization.
2. Another spawn is attempted every `SpawnInterval` minutes.
3. Attempts stop creating dragons while `MaxActiveDragons` live dragons are tracked.
4. When a tracked dragon dies or is deleted, a replacement attempt runs after one second.

With the defaults, the server starts with one dragon and can reach three over subsequent intervals. Once at the cap, killing one causes a near-immediate replacement.

### Loop spawning disabled

No dragon is spawned immediately. One non-repeating spawn attempt runs after `SpawnInterval` minutes. A dead or deleted dragon is not replaced by the manager.

### Disabling automatic spawning

Set:

```json
"SpawnInterval": 0
```

This prevents both the immediate spawn and timer creation.

## Location entries

Each location has this structure:

```json
{
  "name": "Event Display Name",
  "pos": [
    "7500 100 7500",
    "7600 100 7600"
  ],
  "ENABLED": 1
}
```

| Field | Meaning |
| --- | --- |
| `name` | Text used in announcements and debug logs. |
| `pos` | One or more `X Y Z` target vectors stored as strings. One is selected randomly. |
| `ENABLED` | `1` includes the location; `0` preserves it but excludes it from selection. |

The manager selects a location uniformly, then selects one of that location's positions uniformly. Locations with more position entries therefore do not become more likely to be chosen; only the position within that selected location changes.

The spawn point is generated 500 meters away on one horizontal axis and up to 500 meters away on the other, giving a horizontal distance of roughly 500-707 meters from the target. Its initial world `Y` value is forced to `800`.

## Upgrade note

Schema version 2 renamed the old `Interval` field to `SpawnInterval` and added `MaxActiveDragons`.

An old file containing:

```json
"Interval": 15
```

must use:

```json
"SpawnInterval": 15
```

The obsolete `Interval` key is not read by the current class. During a version upgrade, a missing `SpawnInterval` falls back to `15`, `MaxActiveDragons` is added with `3`, and the file is saved as version `2`.

Do not clear `Locations` to an empty array: the load hook restores the Chernarus defaults when the array is empty.
