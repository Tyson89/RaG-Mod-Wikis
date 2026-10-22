# Vanilla DigitalCodeLock

RaG Core extends DayZ's vanilla `DigitalCodeLock` with persistent ownership, remembered access, admin recovery, optional battery-free operation, optional raiding, and support for RaG container classes that expose the dedicated slot. Server operators can also enable it on vanilla fences and tents.

This system uses the vanilla item. It does not require or configure a third-party CodeLock mod.

## Requirements and scope

RaG Core must be installed on both server and clients. Addon ordering comes from Core's `CfgPatches.requiredAddons[]`; changing server `-mod` list order does not control it.

Core manages a lock only when it uses the dedicated attachment slot:

```text
Att_CodeLock_RaG
```

Locks attached through a normal vanilla slot keep vanilla behavior. `EnableRaGDigitalCodeLock` controls Core management globally, while the vanilla fence and tent settings control whether those vanilla targets expose the RaG slot.

Current built-in vanilla targets:

- fully constructed, closed fence gates;
- pitched `MediumTent`;
- pitched `LargeTent`;
- pitched `CarTent`;
- pitched `PartyTent`.

Improvised shelters are not included. A target cannot accept the RaG digital lock while a vanilla digital lock or combination lock occupies a conflicting slot.

## Configuration file

Core creates the server-side file at:

```text
$profile:\RaG_Core\Configs\RaG_Core\DigitalCodeLock.json
```

Stop the server and back up the file before editing it. Keep `Version` unchanged.

Current default schema:

```json
{
    "Version": 5,
    "EnableRaGDigitalCodeLock": 1,
    "DigitalCodeLockAutoLockOnClose": 1,
    "DigitalCodeLockRememberAccess": 1,
    "DigitalCodeLockOwnerOnlyReset": 1,
    "DigitalCodeLockOwnerOnlyRemove": 1,
    "DigitalCodeLockRequireBattery": 0,
    "DigitalCodeLockEnableRaiding": 0,
    "DigitalCodeLockEnableVanillaTents": 0,
    "DigitalCodeLockEnableVanillaFences": 0,
    "DigitalCodeLockDeleteAfterRaid": 0,
    "DigitalCodeLockRaidTimeSeconds": 900.0,
    "DigitalCodeLockRaidIncrements": 5,
    "DigitalCodeLockRaidToolDamage": 100.0,
    "DigitalCodeLockRaidTools": [
        "Hacksaw",
        "HandSaw"
    ],
    "AdminSteamIds": []
}
```

Boolean values use `0` for disabled and `1` for enabled.

## Setting reference

| Setting | Default | Behavior |
| --- | ---: | --- |
| `Version` | `5` | Schema version. Core migrates older files; do not edit it. |
| `EnableRaGDigitalCodeLock` | `1` | Enables all RaG-managed vanilla `DigitalCodeLock` behavior. |
| `DigitalCodeLockAutoLockOnClose` | `1` | Locks a configured lock automatically when its parent closes, if a PIN exists. |
| `DigitalCodeLockRememberAccess` | `1` | Remembers players who successfully enter the PIN and lets them open without another prompt. |
| `DigitalCodeLockOwnerOnlyReset` | `1` | Restricts PIN reset to the recorded owner and configured admins. |
| `DigitalCodeLockOwnerOnlyRemove` | `1` | Restricts lock removal to the recorded owner and configured admins once ownership or a PIN exists. |
| `DigitalCodeLockRequireBattery` | `0` | When disabled, managed locks report full energy and do not need a 9V battery. When enabled, normal battery and energy checks apply. |
| `DigitalCodeLockEnableRaiding` | `0` | Enables the continuous raid action for locked, managed locks. |
| `DigitalCodeLockEnableVanillaTents` | `0` | Enables the RaG attachment slot and lock enforcement on supported vanilla tents. |
| `DigitalCodeLockEnableVanillaFences` | `0` | Enables the RaG attachment slot and lock enforcement on fully constructed vanilla gates. |
| `DigitalCodeLockDeleteAfterRaid` | `0` | Deletes the ruined lock after a successful raid instead of leaving it dropped. |
| `DigitalCodeLockRaidTimeSeconds` | `900` | Total cumulative work time across all raid increments. Valid range: `1` through `86400`. |
| `DigitalCodeLockRaidIncrements` | `5` | Number of completed work intervals needed. Valid range: `1` through `1000`, and cannot exceed raid time in seconds. |
| `DigitalCodeLockRaidToolDamage` | `100` | Health removed from the raid tool after every completed increment. `0` disables tool damage. |
| `DigitalCodeLockRaidTools` | `Hacksaw`, `HandSaw` | Accepted tool base classes. Subclasses also match because Core uses `IsKindOf()`. An empty array is restored to the two defaults. |
| `AdminSteamIds` | Empty | Steam64 IDs allowed to bypass remembered access and perform admin recovery actions. Keep IDs as quoted strings. |

Invalid raid time resets to `900`. Invalid increment count resets to `5`; a count greater than raid seconds is reduced to the raid-seconds value. Invalid negative tool damage resets to `0`.

## Player behavior

The first player who sets a PIN becomes the persistent owner. Setting a new PIN requires entering it twice. The UI also provides a PIN visibility toggle and accepts number-key input.

With remembered access enabled:

1. a correct PIN entry adds that player's Steam64 ID to the authorized list;
2. an authorized player can open the locked parent without reopening the PIN UI;
3. setting a new PIN clears the authorized list;
4. the original owner remains owner through a normal PIN reset.

With remembered access disabled, non-admin players must enter the PIN each time. Ownership still controls reset and removal when those owner-only settings are enabled.

Core prevents a managed lock from entering the locked state while its parent is open. Closing a container, gate, or supported tent triggers auto-lock when enabled. Locked tents hide cargo and block item transfer. Locked gates block opening. Core also blocks gate dismantling while the RaG lock remains attached.

All PIN and management requests are checked on the server. The player must be alive, within the base-building interaction distance, and have a clear interaction ray to the lock or parent. Vanilla brute-force protection still applies.

## Raiding

Raiding requires all of these conditions:

- `EnableRaGDigitalCodeLock` is enabled;
- `DigitalCodeLockEnableRaiding` is enabled;
- the managed lock is attached and locked;
- the player holds a non-ruined configured tool;
- the player remains in a valid interaction position.

Raid time is split evenly across `DigitalCodeLockRaidIncrements`. With defaults, five intervals of 180 seconds produce a total of 900 seconds. Each completed interval:

- removes one increment of lock health;
- damages the tool by `DigitalCodeLockRaidToolDamage`;
- preserves completed damage if the player stops before the next interval finishes.

The final interval unlocks and drops the lock, ruins it, and optionally deletes it. Tool damage is applied on every increment, including the final one.

## Admin recovery

Add exact Steam64 IDs to `AdminSteamIds`:

```json
"AdminSteamIds": [
    "76561198000000000",
    "76561198000000001"
]
```

Configured admins can:

- open without entering the PIN;
- use **Admin Unlock Digital Code Lock**;
- reset the PIN;
- remove the lock;
- recover a lock whose ownership record is missing or unreadable.

Admin rights apply only to enabled RaG-managed locks in `Att_CodeLock_RaG`.

## Persistence

Ownership and remembered access are stored per lock under:

```text
$profile:\RaG_Core\Storage\DigitalCodeLock\<persistent-id>.json
```

Writes use Core's atomic JSON path and retain a `.bak` copy when replacing an existing record. Do not bulk-edit, rename, or delete these files while the server runs.

If a lock has a PIN but its ownership record cannot be loaded, Core fails closed, keeps the lock locked, and logs an ownership error. A configured admin can reset it to rebuild valid ownership data.

## Troubleshooting

### RaG slot does not appear on a vanilla gate

Confirm `DigitalCodeLockEnableVanillaFences` is `1`. Gate must be fully constructed and closed. Remove any conflicting digital or combination lock first.

### RaG slot does not appear on a tent

Confirm `DigitalCodeLockEnableVanillaTents` is `1`. Tent must be pitched and must be one of the four supported vanilla tent classes. Remove any conflicting digital or combination lock first.

### Lock opens but does not auto-lock

Confirm `DigitalCodeLockAutoLockOnClose` is `1`, a PIN exists, and parent reached its closed state. A managed lock cannot lock an open parent.

### PIN UI or action closes immediately

Move within interaction range and target the lock, gate, container, or tent entrance directly. Server rejects remote or obstructed requests even if a client briefly displays the action.

### Raid action does not appear

Confirm raiding is enabled, lock is locked, and held item matches one of `DigitalCodeLockRaidTools`. Class names are case-sensitive. Empty tool arrays are replaced with defaults during config load.

### Owner cannot open without PIN

`DigitalCodeLockRememberAccess` must be enabled. Ownership and remembered access are separate: owner-only permissions can remain active while prompt bypass is disabled.
