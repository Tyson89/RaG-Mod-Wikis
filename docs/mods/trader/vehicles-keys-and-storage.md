# Vehicles, keys, and storage

RaG Trader has three related systems:

1. buying configured cars and boats at trader spawn points;
2. selling packed cars or physical cars/boats under ownership rules;
3. assigning `RaG_CarKey` to `CarScript` vehicles for locking and portable storage.

Vehicle purchase does not assign a key automatically. Key system supports cars derived from `CarScript`, not boats.

## Vehicle listings

Vehicle class is detected by walking `CfgVehicles` inheritance until `CarScript` or `BoatScript`.

Example:

```json
{
  "ClassName": "OffroadHatchback",
  "AllowDuplicate": false,
  "BuyPrice": 5000,
  "SellPrice": 2000,
  "Stock": 2
}
```

Quantity is forced to `1`. Delivery mode and normal ground fallback do not choose vehicle position.

Set `SellPrice: -1` only when vehicle must be buy-only. Positive price enables packed/parked sale rules below.

## Selling vehicles

Vehicle sale quantity is always `1`. Server checks packed vehicle keys first, then physical vehicles around configured spawn points. Exact listing class must match.

### Sell packed keyed car

Carry `RaG_CarKey` that is:

- assigned and marked as containing packed vehicle;
- linked to exact listed class in stored binary;
- owned by current player identity;
- not ruined;
- removable and not blocked by locked inventory.

On successful sale, server consumes submitted key and permanently deletes packed vehicle file. Stored vehicle uses the listing's base/dynamic sell price and its saved global health fraction when condition pricing is enabled. It must meet `MinimumHealthPercent` and cannot be ruined. Fuel, cargo, and individual parts receive no separate payment.

Other matching spare keys are not consumed. They no longer have packed vehicle, but remain assigned to sold identity. Remove them from circulation; they do not become blank keys.

!!! warning "Packed sale ownership is strict"
    `RestrictVehicleStorageToOwner: false` and `AdminSteamIds` affect pack/deploy only. They do not let holder/admin sell another owner's packed vehicle.

### Sell physical car or boat

Park exact class within `6` metres of any `VehicleSpawnPoints` position belonging to current trader. Then meet all conditions:

- no crew in vehicle;
- engine off;
- not ruined;
- global health meets listing `MinimumHealthPercent`;
- ownership check passes.

Ownership:

- assigned `CarScript`: seller must be player recorded at key assignment;
- assigned car whose saved data has no owner ID: matching owner key in seller inventory is fallback proof;
- unassigned car or any boat: seller must be last driver recorded when engine started.

Last-driver record changes every time another player starts engine and persists with vehicle. Fresh unassigned vehicle with engine never started has no seller; start it once before sale.

Physical sale payout follows condition pricing from global health when enabled. Quantity pricing has no vehicle effect. Packed sale applies the same condition setting to saved global health. Packing is not a repair or a route to full-condition resale.

!!! danger "Unload before selling"
    Successful physical sale deletes entire vehicle, attachments, and cargo. Server does not require empty inventory—only empty crew. No separate payment exists for fuel, parts, or contents.

### Sale choice and stock

- If player carries eligible matching packed key, packed vehicle is selected before parked vehicle.
- Finite-stock cap still applies: vehicle sale adds one stock and fails when listing already at cap.
- Sellable filter detects matching packed key or exact-class transport near spawn, but server owns final authorization.
- Basket can include vehicle sale, but each vehicle line quantity remains one.
- Failed payout restores staged packed file/key when rollback succeeds; physical vehicle stays in world until successful commit.

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

Registry validation checks the configured vehicle attachment set using temporary objects; an invalid class or slot fit blocks startup or rejects reload. If a required attachment fails during actual vehicle creation, vehicle configuration fails, the spawned vehicle is deleted, and the purchase rolls back. Ordinary listing attachment failures also abort delivery.

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

A missing profile means no configured parts are supplied. A present but invalid profile is a blocking configuration error, not an accepted way to request a bare vehicle.

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

An ordinary key cannot clear or move its assignment. Authorized admins can reset the deployed vehicle through the separate admin key described below. Vehicle/key display name changes to include recorded owner and vehicle name.

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

Make spare immediately. Losing every matching key leaves no ordinary player recovery flow. A deployed car can be reset by an authorized admin; a packed car still requires recovery of its matching key/state.

## Packing vehicle

Hold matching key, target car, use **Pack vehicle**. `EnableVehiclePacking` must be `true`. When disabled, keys still lock/unlock and existing packed cars can still deploy; storage files are not erased.

Car must:

- have matching assignment;
- not be ruined;
- engine off;
- speed no more than about `1.0` on speedometer;
- have no crew;
- not already be packed under same key ID.

When `RestrictVehicleStorageToOwner: true`, only recorded key owner or Steam64 admin can pack. Owner uses stable identity ID recorded at assignment. Key data without an owner ID falls back to player-name match.

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

Storage format is `4`. Stored data includes assigned owner identity, last-driver identity, and global vehicle health used for sale validation and pricing. Deployment accepts supported formats 1 through 4. If stored data has no sale-health information, selling returns **Deploy and repack this vehicle before selling it**. Deploy, inspect the vehicle, and pack it again to write the required health record. Atomic storage also uses `.bak`, temporary, sale, and deployment tracking files; back up the whole directory rather than only `.bin` files.

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

On success, server restores car at requested transform, persists deployment tracking, removes packed storage, and updates matching keys to not stored. If a storage commit or cleanup fails, preserve companion files and inspect logs before retrying.

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
- restriction/admin bypass does not grant vehicle sale authority.

## Recovery scenarios

### Admin key for deployed cars

`RaG_CarKey_Admin` is a separate item from ordinary player keys. Server checks the holder's Steam64 ID against `Settings.json` `AdminSteamIds`. Possessing the item alone does not authorize a non-admin.

Authorized admin can lock/unlock an assigned deployed car and use **Reset vehicle key**. Reset clears the vehicle's assignment, owner name/ID, last-driver ID, and lock state. It does not turn old player keys into blank keys. Those keys no longer match the reset vehicle.

For a lost-key deployed car:

1. Confirm the intended vehicle and owner; preserve relevant persistence before intervention.
2. Hold non-ruined `RaG_CarKey_Admin` as a listed admin and target the deployed car.
3. Use **Reset vehicle key**.
4. Have the intended owner assign a fresh ordinary `RaG_CarKey`.
5. Craft fresh spares and retire old keys. Check lock/unlock and recorded ownership.

Reset is logged with admin ID, vehicle class, and previous key identity. Admin key cannot be assigned as an ordinary key and is not a universal packed-vehicle recovery token. Do not put it in public loot or normal trader listings.

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
- Unload every vehicle before sale; cargo and parts are deleted unpaid.
- Set vehicle resale values using global health pricing; fuel and separately valuable parts do not receive an extra payout.
- Use wide sell-point spacing and signs so players know exact parking target.
- Do not enable wheel locking until server understands gameplay effect and removal tools.
