# Locations and safe zones

`Locations.json` controls physical trader groups, entity classes, transforms, opening hours, vehicle spawn points, and optional safe zones.

## Structure

```json
{
  "Version": 1,
  "Locations": [
    {
      "Id": "North Market",
      "Enabled": true,
      "Safezone": {
        "Enabled": true,
        "Center": [7500.0, 10.0, 7500.0],
        "Radius": 150.0,
        "BlockIncomingDamage": true,
        "BlockOutgoingDamage": true,
        "ProtectPlayerEquipment": true,
        "DeleteAnimals": true,
        "DeleteInfected": true,
        "BlockWeaponFire": true,
        "BlockExplosives": true,
        "BlockBuilding": true,
        "VehicleSpeedLimitKmh": 30.0,
        "ShowNotifications": true,
        "ExitProtectionSeconds": 30,
        "PreserveHunger": false,
        "PreserveThirst": false,
        "PreserveDisease": false,
        "PreserveTemperature": false,
        "PreserveBleeding": false,
        "ExcludedEntityClasses": []
      },
      "Traders": [
        {
          "TraderId": "tools",
          "EntityClassName": "RaG_TraderTerminal",
          "Attachments": [],
          "Enabled": true,
          "OpeningHoursEnabled": false,
          "OpeningHour": 0,
          "ClosingHour": 24,
          "Position": [7505.0, 10.0, 7500.0],
          "Orientation": [180.0, 0.0, 0.0],
          "VehicleSpawnPoints": []
        }
      ]
    }
  ]
}
```

## Group fields

| Field | Meaning |
| --- | --- |
| `Id` | Unique group name. Runtime trader ID becomes `<group Id>/<TraderId>`. |
| `Enabled` | `false` skips entire group, all traders, and safe zone. |
| `Safezone` | One optional cylindrical safe zone for group. |
| `Traders` | Physical trader entries. |

Group ID may contain spaces. Keep stable: it appears in runtime location IDs and trade logs.

## Trader entry fields

| Field | Rules and effect |
| --- | --- |
| `TraderId` | Must match unique profile `Id` in `Catalog.json`. Only one entry with given trader ID is allowed per group because runtime ID would collide. |
| `EntityClassName` | Exact valid `EntityAI` class. Common choices: survivor class or `RaG_TraderTerminal`. |
| `Attachments` | Survivor clothing, gear, held items, or inventory. Invalid class is validation error. |
| `Enabled` | `false` skips entry. |
| `OpeningHoursEnabled` | Uses world-time hour checks when `true`. |
| `OpeningHour` | `0`–`23`; invalid resets to `0`. Inclusive. |
| `ClosingHour` | `0`–`24`; invalid resets to `24`. Exclusive. |
| `Position` | `[x, y, z]`, exactly three values. |
| `Orientation` | `[yaw, pitch, roll]`, exactly three values. |
| `VehicleSpawnPoints` | Ordered list used by vehicle listings. Each needs valid position and orientation. |

Entity manager first binds exact matching map object within 1 metre. Otherwise it spawns entity. This allows map designers to place terminal/NPC themselves while keeping trade binding in JSON.

## Opening hours

Hours read DayZ world date/time:

- `OpeningHour == ClosingHour`: always open.
- opening less than closing: open from opening inclusive to closing exclusive.
- opening greater than closing: overnight window.

Examples:

```json
{
  "OpeningHoursEnabled": true,
  "OpeningHour": 8,
  "ClosingHour": 20
}
```

Open `08:00` through `19:59` world time.

```json
{
  "OpeningHoursEnabled": true,
  "OpeningHour": 20,
  "ClosingHour": 6
}
```

Open `20:00` through `05:59` world time.

Opening hours and every other `Locations.json` field require a restart; live reload rejects changes to this file. Offer rotations and seasonal months use real UTC instead of world time; see [rotating and seasonal offers](rotating-and-seasonal-offers.md).

Closing applies at catalog checkout too. Menu opened just before close can reject transaction afterward.

## Safe-zone geometry

Zone uses X/Z radius only:

```text
(playerX - centerX)^2 + (playerZ - centerZ)^2 <= radius^2
```

Trigger extends from `-1000` to `+1000` relative to configured Y; protection queries use horizontal radius. Terrain elevation does not reduce horizontal radius. Radius below `1` is corrected to `1`.

Safe-zone center is independent from trader positions. Put center deliberately around market footprint, not blindly on first trader.

## Safe-zone settings

| Setting | Default | Actual effect |
| --- | ---: | --- |
| `Enabled` | `false` | Creates zone trigger only when group also enabled and center valid. |
| `Center` | `[]` | `[x,y,z]`; exactly three values required when enabled. |
| `Radius` | `150.0` | Horizontal metres; minimum `1`. |
| `BlockIncomingDamage` | `true` | Blocks player damage when victim inside; also extends incoming protection after exit. Requires non-null damage source. |
| `BlockOutgoingDamage` | `true` | Blocks damage caused by player while inside. |
| `ProtectPlayerEquipment` | `true` | Blocks damage to items rooted on protected player; can continue after exit. |
| `DeleteAnimals` | `true` | Deletes animals entering/staying in trigger and those present at startup. |
| `DeleteInfected` | `true` | Deletes infected entering/staying and those present at startup. |
| `BlockWeaponFire` | `true` | Prevents weapon manager firing while inside. |
| `BlockExplosives` | `true` | Blocks vanilla `ActionArmExplosive`. Does not broadly delete every explosive class or replace incoming-damage protection. |
| `BlockBuilding` | `true` | Blocks vanilla deploy-object and build-part actions. Custom mod actions may need own integration. |
| `VehicleSpeedLimitKmh` | `30.0` | Caps velocity of `CarScript` inside. `0` disables. Negative becomes `0`. |
| `ShowNotifications` | `true` | Sends enter, leave, and exit-expired messages. |
| `ExitProtectionSeconds` | `30` | Protection after leaving last overlapping zone. Negative becomes `0`. |
| `PreserveHunger` | `false` | Pauses hunger modifier tick while inside. |
| `PreserveThirst` | `false` | Pauses thirst modifier tick while inside. |
| `PreserveDisease` | `false` | Pauses immune-system agent-pool tick; does not cure disease. |
| `PreserveTemperature` | `false` | Suppresses heat-comfort tick and restores temperature stats after environment update. |
| `PreserveBleeding` | `false` | Sets bleeding manager blood-loss preservation while inside. Does not remove cuts. |
| `ExcludedEntityClasses` | `[]` | `IsKindOf` exemptions from animal/infected deletion. |

## Incoming and outgoing protection

Damage is denied when:

- victim is inside zone with incoming block; or
- attacker is inside zone with outgoing block; or
- relevant post-exit protection remains.

Source player resolves from damage source itself or its hierarchy root. This covers many held weapons/projectiles. Damage hook requires non-null source, so do not describe zone as universal immunity from falling, environment, hunger, thirst, temperature, or every third-party damage system.

Equipment protection follows owning player position and exit state.

## Exit protection

Timer starts only when player leaves last overlapping safe zone. Entering a zone clears old exit timer.

During timer:

- incoming damage protection follows departed zone's `BlockIncomingDamage`;
- equipment protection follows `ProtectPlayerEquipment`;
- outgoing damage is blocked;
- weapon fire is blocked.

Outgoing and weapon blocks during exit window are unconditional once timer exists. This prevents protected player exploiting grace period to attack others.

Building, explosive arming, vehicle speed, and survival preservation do not continue after exit.

## Admin bypasses

Steam64 IDs in `Settings.json` `AdminSteamIds` bypass:

- weapon-fire block;
- building block;
- explosive-arming block;
- car speed limit;
- key-storage owner restriction.

Admins do not bypass incoming/outgoing damage or equipment protection in current source. They also do not bypass infected/animal deletion.

## Exclusions

Example keep deer but delete other animals:

```json
{
  "DeleteAnimals": true,
  "ExcludedEntityClasses": [
    "Animal_CervusElaphus"
  ]
}
```

Matching uses inheritance. Excluding broad parent can exempt many subclasses. Use narrowest exact parent/class and test.

## Overlapping zones

Player can be inside several triggers. Preservation is active when any containing zone enables matching feature. Protection and action queries inspect containing zones for applicable rules. Exit protection starts only after player leaves final tracked zone.

Avoid accidental overlap with conflicting configs. Same behavior becomes hard to explain and border testing gets messy.

## Practical designs

### Pure trade protection

- incoming/outgoing/equipment protection on;
- weapon/build/explosive blocks on;
- infected/animal deletion on;
- survival preservation off;
- 20–30 second exit protection.

### PvE rest stop

- trade protection on;
- hunger/thirst/temperature preservation on;
- disease/bleeding preservation only if server wants true recovery pause;
- lower speed limit and visible notifications.

### Terminal without safe zone

- `Safezone.Enabled: false`;
- terminal still trades normally;
- ideal for risky black-market location.

## Border test checklist

- enter/leave message fires once;
- shots blocked inside;
- outside shooter cannot damage inside player;
- inside player cannot damage outside target;
- exit grace blocks retaliation and expires on time;
- equipment does not take protected damage;
- custom explosives/build actions behave as expected;
- cars cap speed without severe physics collision;
- infected/animals delete and exclusions survive;
- overlapping zones do not produce confusing timer state.
