# Server configuration and spin data

RaG Wheel of Fortune creates two files:

| File | Purpose |
| --- | --- |
| `$profile:\RaG_Core\Configs\RaG_Wheel_Of_Fortune\RaG_Wheel_Of_Fortune.json` | Server settings and reward classes. |
| `$profile:\RaG_Core\Configs\RaG_Wheel_Of_Fortune\WheelData.json` | Runtime date and Steam64 IDs that already spun. |

Stop server before editing either file. Restart after changes.

## Reward configuration

### Default version 1 file

```json
{
  "Version": 1,
  "MinSpinningTime": 7.0,
  "MaxSpinningTime": 18.0,
  "EnableAnnounceJackpot": 1,
  "ItemField2": "GorkaHelmet",
  "ItemField3": "Canteen",
  "ItemField4": "DuffelBagSmall_Green",
  "ItemField5": "BandageDressing",
  "ItemField6": "TetracyclineAntibiotics",
  "ItemField7": "HuntingOptic",
  "ItemField8": "MedievalBoots",
  "ItemField9": "BDUJacket",
  "ItemField10": "Hammer",
  "ItemField11": "Wrench",
  "ItemField12": "SledgeHammer",
  "ItemField13": "Hatchet",
  "ItemField14": "Screwdriver",
  "ItemField15": "LugWrench",
  "ItemField16": "NailBox",
  "ItemFieldJackpot": [
    "NailBox",
    "SledgeHammer",
    "Hacksaw",
    "Whetstone"
  ]
}
```

DayZ JSON serializer writes script boolean as `1` or `0`.

### Settings

| Setting | Default | Actual effect |
| --- | ---: | --- |
| `Version` | `1` | Current schema. Values below `1` upgrade and save as `1`. |
| `MinSpinningTime` | `7.0` | Lower bound in seconds for random spin timer and wheel animation phase. |
| `MaxSpinningTime` | `18.0` | Upper bound in seconds for random spin timer and wheel animation phase. |
| `EnableAnnounceJackpot` | `1` | Broadcasts winner name and prize when field `1` succeeds. Does not disable jackpot sound, particle, or prize. |
| `ItemField2` through `ItemField16` | See defaults | Exact class spawned when matching normal field lands. |
| `ItemFieldJackpot` | Four classes | Candidate pool for field `1`; one entry selected randomly. |

Field `1` has no `ItemField1` string. Jackpot array is its only reward source.

## Validation rules

Current source does not clamp times or validate reward list at load.

- Keep times finite, non-negative, and `MinSpinningTime <= MaxSpinningTime`.
- Keep all normal field strings non-empty.
- Keep jackpot array non-empty.
- Use exact class names available on server.
- Use classes inheriting `ItemBase`.
- Avoid prizes too large for clear spawn area.
- Restart and test every field after changing mod set or rewards.

!!! danger "Bad rewards consume spin"
    Spin is recorded before result. Empty or invalid reward logs error, gives no fallback, and still uses player's daily attempt.

!!! danger "Never empty jackpot array"
    Field `1` calls `GetRandomElement()` without array-length guard. Keep at least one valid `ItemBase` class.

## Reward weighting

Two independent methods exist:

1. Put same class in several normal fields. Prize then occupies several physical wheel segments.
2. Repeat class inside `ItemFieldJackpot`. Conditional jackpot selection weights repeated entry.

Example jackpot pool:

```json
"ItemFieldJackpot": [
  "NailBox",
  "NailBox",
  "SledgeHammer",
  "Whetstone"
]
```

When field `1` lands, `NailBox` has two of four array slots. This does not change chance of wheel landing on jackpot field itself.

## `WheelData.json`

Typical runtime file:

```json
{
  "lastClearDate": "2026-07-30",
  "spunIDs": [
    "76561198000000000"
  ]
}
```

| Key | Meaning |
| --- | --- |
| `lastClearDate` | Server calendar date used during last reset, formatted `YYYY-MM-DD`. |
| `spunIDs` | Steam64 IDs already recorded for that date. |

Manager saves file after every new recorded spin. Multiple placed wheels share same file and list.

Treat file as runtime state, not reward config. It contains player platform identifiers; do not publish it.

### Manual reset

To intentionally grant everyone another spin:

1. Stop server.
2. Back up `WheelData.json`.
3. Delete IDs from `spunIDs` while keeping valid JSON, or move file out of active folder.
4. Start server and verify fresh state.

Editing file while server runs is ineffective or unsafe because in-memory state can overwrite it.

## Reset timing

`CheckDailyReset()` runs only during spin manager construction. It compares `lastClearDate` with server calendar date, clears `spunIDs` when different, and saves.

No scheduled midnight check exists. For predictable daily reset, schedule normal server restart after server-local midnight. Client clock and in-game accelerated time do not control reset.

## Error logs

With matching RaG Core logging settings:

```text
[RaG_Wheel_Of_Fortune]:: [SpawnPrize] Empty class for ItemField<field> ! Check RaG_Wheel_Of_Fortune.json
```

```text
[RaG_Wheel_Of_Fortune]:: [SpawnPrize] Error spawning: <class> Check RaG_Wheel_Of_Fortune.json entry: ItemField<field>
```

First covers empty normal field. Second covers unavailable or incompatible prize class. Jackpot failures also use `ItemField1` in log suffix even though JSON key is `ItemFieldJackpot`.

## Configuration recovery

1. Stop server.
2. Back up broken file.
3. Move broken file out of active directory.
4. Start once to generate defaults.
5. Stop server.
6. Merge wanted values into fresh file.
7. Restart and test spins with temporary test accounts before public use.
