# Vehicles, keys, and storage

RaG Trader has two related systems:

1. buying configured cars and boats at trader spawn points;
2. assigning `RaG_CarKey` to `CarScript` vehicles for locking and portable storage.

Vehicle purchase does not assign a key automatically. Key system supports cars derived from `CarScript`, not boats.

## Vehicle listings

Vehicle class is detected by walking `CfgVehicles` inheritance until `CarScript` or `BoatScript`.

Example:

```json
{
  "ClassName": "OffroadHatchback",
  "AllowDuplicate": false,
  "BuyPrice": 5000,
  "SellPrice": -1,
  "Stock": 2
}
```

Quantity is forced to `1`. Delivery mode and normal ground fallback do not choose vehicle position.

!!! warning "Set vehicle SellPrice to -1"
    Sale collector searches player inventory for matching `ItemBase`. Cars and boats are world transports, not inventory items. Positive default vehicle sell price is not practically usable.

## Vehicle spawn points

Configured on physical trader entry:

```json
{
  "VehicleSpawnPoints": [
    {
      "Position": [7490.0, 10.0, 7505.0],
      "Orientation": [90.0, 0.0, 0.0]
    },
    {
      "Position": [7480.0, 10.0, 7505.0],
      "Orientation": [90.0, 0.0, 0.0]
    }
  ]
}
```

Server tries in listed order. Spawn point must pass box collision approximately `6 × 4 × 10` metres. Safe-zone trigger object is ignored; real collidable object blocks point. If all blocked, purchase fails before payment and stock restores.

### Spawn-point design

- use flat terrain;
- keep 10+ metre separation;
- avoid buildings, trees, map clutter, fences, signs, and parked vehicles;
- orient exit direction away from trader crowd;
- test largest sold truck, not only hatchback;
- provide several fallback points for busy market;
- keep boats in separate water-capable purchase design, but current clearance and general spawn code still need live testing.

## Purchased vehicle setup

After creation:

- global health set to maximum;
- configured attachments created and set full health;
- car fuel, oil, brake, and coolant filled;
- boat fuel filled;
- wheels optionally locked to parent via `LockVehicleWheelsOnSpawn`.

One attachment creation failure logs warning and skips that attachment; vehicle purchase still completes. This differs from normal listing `Attachments`, where any attachment failure aborts item delivery.

Category-listing `Attachments` are not applied to vehicle purchase path. Configure purchased vehicle parts only in `VehicleAttachments.json`.

## `VehicleAttachments.json`

Example:

```json
{
  "Version": 1,
  "Vehicles": [
    {
      "ClassName": "OffroadHatchback",
      "Attachments": [
        "CarBattery",
        "CarRadiator",
        "SparkPlug",
        "HeadlightH7",
        "HeadlightH7",
        "HatchbackHood",
        "HatchbackTrunk",
        "HatchbackDoors_Driver",
        "HatchbackDoors_CoDriver",
        "HatchbackWheel",
        "HatchbackWheel",
        "HatchbackWheel",
        "HatchbackWheel",
        "HatchbackWheel"
      ]
    }
  ]
}
```

Rules:

- `Version` must be `1`.
- Vehicle class must inherit `CarScript` or `BoatScript`.
- Only one profile per exact vehicle class.
- Every attachment class must exist.
- Repeat class for repeated slots such as wheels/headlights.
- Attachment must be compatible with available vehicle slots.

If any class in profile is unknown, entire profile is not registered. Vehicle can still spawn, full health and fluids, but without that profile's attachment set.

## Obtaining and assigning key

Blank key class:

```text
RaG_CarKey
```

Hold non-ruined blank key, target non-ruined unkeyed `CarScript`, use **Assign car key**. Server generates four-part UUID and stores same identity on vehicle/key.

Requirements:

- key unassigned;
- car unassigned;
- car not ruined;
- player identity and name available.

Assignment cannot be cleared or moved to another vehicle. Vehicle/key display name changes to include recorded owner and vehicle name.

Purchased vehicle needs separately obtained blank key. Add `RaG_CarKey` to vehicle/tools trader or loot economy.

## Locking

Matching key can lock when:

- car assigned;
- car currently unlocked;
- engine off;
- every crew seat empty.

Locked car blocks:

- getting in;
- opening outside doors;
- cargo display;
- attachment category display;
- cargo insert/removal;
- attachment insert/removal.

Matching key can unlock locked car. Owner restriction is not checked for lock/unlock: possession of matching key is authority.

Lock is access control, not raid protection. Vehicle still can take damage and other mods/admin tools may move or alter it.

## Spare keys

Combine:

- one assigned `RaG_CarKey`;
- one unassigned `RaG_CarKey`.

Recipe **Make spare car key** takes about one second, consumes neither, and copies assignment to blank key. Both keys operate same vehicle and reflect stored-vehicle state while registered.

Make spare immediately. Losing every matching key leaves no built-in player recovery flow.

## Packing vehicle

Hold matching key, target car, use **Pack vehicle**.

Car must:

- have matching assignment;
- not be ruined;
- engine off;
- speed no more than about `1.0` on speedometer;
- have no crew;
- not already be packed under same key ID.

When `RestrictVehicleStorageToOwner: true`, only recorded key owner or Steam64 admin can pack. Owner uses stable identity ID recorded at assignment. Older key data without ID falls back to player-name match.

Pack process:

1. saves vehicle to temp binary file;
2. commits atomic storage and backup;
3. marks all registered matching keys as containing vehicle;
4. deletes deployed world vehicle only after successful save.

Stored data recursively uses entity `OnStoreSave`/`OnStoreLoad`, preserving vehicle and nested attachment/cargo state, damage zones, key/lock state, and car fluid fractions.

## Storage files

Path:

```text
$profile:\RaG_Core\Storage\RaG_Trader\Vehicles\<id0>_<id1>_<id2>_<id3>.bin
```

Format version currently `2`. Atomic helper may create `.bak` and temporary companion files.

Do not rename or hand-edit binary. Filename is key UUID. Losing storage file makes keys report no packed vehicle. Removing a stored mod class can make recursive restore fail.

## Deploying vehicle

Hold key containing packed vehicle and enter placement mode. `RaG_Hologram_Car` shows placement. Use **Deploy vehicle** when hologram valid.

Server validates:

- key assigned and packed file exists;
- owner/admin authorization when enabled;
- same vehicle not already registered as deployed;
- requested position non-zero;
- within `10` metres of player;
- vertical difference no more than `4` metres;
- not sea or pond surface;
- server hologram collision check passes;
- loaded vehicle key identity matches held key.

On success, server restores car at requested transform, registers it, deletes storage main/backup, and updates matching keys to not stored.

Current deployment forbids water surfaces and restores `CarScript`; portable storage is not boat storage.

## Owner restriction and admins

```json
{
  "RestrictVehicleStorageToOwner": true,
  "AdminSteamIds": [
    "76561198000000000"
  ]
}
```

- `true`: assigned owner/admin can pack or deploy.
- `false`: anyone holding matching key can pack/deploy.
- admins must use exact Steam64 ID.
- restriction does not prevent another matching-key holder locking/unlocking.
- restriction does not transfer ownership when spare key given away.

## Recovery scenarios

### Packed vehicle, key lost

Binary remains but no ordinary player action can address UUID. Restore matching key from persistence/admin backup or recover through controlled server administration. Do not guess filename/key data.

### Deploy fails after mod removal

Stored binary remains because deletion occurs only after successful restore. Re-enable exact vehicle/item mod versions, restart, deploy, unload incompatible cargo, repack, then migrate.

### Key says packed but no file

Key state refreshes from file when registered server-side. Reconnect/restart. If file and backup absent, stored vehicle data is gone.

### Recovery vault appears

`RaG_TraderTransactionVault` concerns failed trade/currency rollback, not vehicle storage. Do not delete before checking contents and logs.

## Operational tips

- Back up vehicle storage with persistence backups.
- Keep exact mod set while vehicles remain packed.
- Tell players to unpack before major vehicle-mod updates.
- Test nested weapons, magazines, fluids, batteries, locks, damage, and cargo after every storage-code update.
- Never place deployment hologram on roofs/ledges despite 4-metre vertical allowance.
- Keep spare key outside vehicle. Key locked inside matching car is useless.
- Do not enable wheel locking until server understands gameplay effect and removal tools.
