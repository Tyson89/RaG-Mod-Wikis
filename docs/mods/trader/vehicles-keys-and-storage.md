# Vehicles, keys, and storage

Vehicle dealers buy and sell vehicles at their configured spawn points. Use a virtual garage at a parking meter, or a matching car key for portable packing when the server enables it.

## Buying vehicles

List the exact vehicle class in a catalog category. The dealer recognizes classes derived from `CarScript`, `BoatScript`, or `MotorbikeScript`. Each vehicle listing trades one vehicle at a time.

Set `VehicleSpawnPoints` on the static trader entry or route stop. The trader uses the first clear point in order. Boats require a point in water. Keep room around each point for spawning and driving away. For a blocked point, check the server warning for the blocking object and its position.

```json
{
  "VehicleSpawnPoints": [
    {"Position": [7490.0, 10.0, 7505.0], "Orientation": [90.0, 0.0, 0.0]}
  ]
}
```

Configure parts per exact vehicle class in `Vehicles/Attachments.json`. Use `"Version": 1` and a `Vehicles` array of objects with `ClassName` and `Attachments`. Repeat a part class for repeated slots such as wheels. A missing entry supplies no configured parts. An invalid part or slot can block configuration validation.

New vehicles and their configured parts start at full health. Cars receive fuel, oil, brake fluid, and coolant. Boats and motorbikes receive fuel. With `CreateVehicleKeyOnPurchase: true`, a purchased `CarScript` gets an assigned `RaG_CarKey`. Look in inventory and, if ground fallback is enabled, at your feet.

## Selling vehicles

For a deployed vehicle, park the exact listed class within 6 m of one of the trader's vehicle points. Switch off the engine and empty all seats. Keyed cars require their assigned owner. Unkeyed cars, boats, and motorbikes require the player recorded when the engine last started. Vehicle condition must meet the listing threshold.

If portable packing is available, carry the matching packed key to sell a stored car. The trader checks packed keys before searching for deployed vehicles. The packed sale requires the assigned owner and consumes the submitted key and vehicle snapshot. Retrieve a vehicle from the virtual garage first if you plan to sell it.

Unload valuables before selling. The sale removes the vehicle, attached parts, and cargo, and pays only for the vehicle. A finite-stock listing also needs room for one more vehicle.

## Virtual garage

### Store and retrieve

1. Park on the garage platform or in the designated area beside a standalone meter. Stop, shut off the engine, and have everyone get out. Detach any towing connections. A helicopter must be landed with rotors stopped.
2. Stand within 3 m of the meter and select **Open virtual garage**.
3. Select the vehicle under **Eligible parked vehicles** and choose **Store vehicle**. The garage stores the vehicle with its attachments and cargo.
4. Return to the meter where you stored the vehicle, select it under **Your stored vehicles**, and choose **Retrieve vehicle**. Keep the retrieval area clear. If your server allows retrieval at other meters, use one that supports your vehicle type and has a suitable surface.

Stored entries show vehicle condition and contents and can be renamed. Clear the name to restore the default label. Your stored list is visible at every meter, including vehicles that must be retrieved elsewhere.

Access uses assigned vehicle ownership or, for unkeyed vehicles the garage registered at purchase, the recorded buyer. Ordinary unkeyed vehicles found in the world need supported ownership before storage. If the server allows matching key holders, storing a vehicle puts it in the storing player's list. Retrieval belongs to the player who stored it.

### Server setup

Set `EnableVirtualGarage: true` in root `Settings.json`. Place a combined `RaG_Parking_MeterPlatform` or a standalone `RaG_Parking_Meter` through the static location's `Objects` array or your map setup. Keep platforms within 5° of level. Use a submerged platform with enough depth for boats. Native cars, boats, and motorbikes are supported. The garage also detects Expansion vehicles when the Expansion vehicle integration is present.

Edit `Vehicles/Garages.json` and restart.

| Field | Default | Accepted values |
| --- | --- | --- |
| `Version` | `1` | `1` |
| `MaxVehiclesPerPlayer` | `20` | `1–100` |
| `AllowVehicleKeyHolders` | `false` | `true` also allows players carrying an eligible matching key to store a vehicle |
| `PlatformParkingHeight` | `8.0` | `2–25` m search height |
| `PlatformSpawnClearance` | `0.15` | `0.05–0.5` m height offset for land retrieval at either meter type |
| `RestrictRetrievalToStorageMeter` | `true` | Require the original meter. Set `false` to allow any suitable meter. |
| `StandaloneMeters` | One example site | Up to 256 site definitions for standalone meters. |

Keep platform positions and standalone meter IDs stable while vehicles are stored. With the retrieval restriction enabled, the server identifies a platform by its world and position and a standalone meter by its world and site ID.

### Standalone meters

Place `RaG_Parking_Meter` within 1 m of its configured `MeterPosition`. The config defines the parking area and retrieval point. Replace the example coordinates with your placement.

```json
{
  "Id": "town_parking",
  "MeterPosition": [5000.0, 100.0, 5000.0],
  "ZoneCenter": [5000.0, 102.0, 5010.0],
  "ZoneSize": [12.0, 6.0, 16.0],
  "ZoneYaw": 0.0,
  "Spawn": {
    "Position": [5000.0, 100.0, 5010.0],
    "Orientation": [0.0, 0.0, 0.0]
  },
  "AllowedVehicleTypes": ["Land"]
}
```

- Use a unique `Id` of 1–64 letters, digits, underscores, or hyphens. IDs are case-insensitive. Keep meter positions more than 2 m apart and each meter within 150 m of its zone center.
- `ZoneSize` is the full width, height, and depth in metres. Width and depth accept `2–120`, and height accepts `2–30`. `ZoneYaw` rotates the box. The spawn point and the vehicle's retrieval footprint must fit inside it.
- Use `Spawn.Orientation` with yaw only. `AllowedVehicleTypes` accepts `Land`, `Air`, or `Water`, or the combination `Land` and `Air`. Water sites need enough depth across the retrieval footprint.

### Saved vehicles

Garage records and snapshots live in `$profile:\RaG_Core\Storage\RaG_Trader\Garage\`. Preserve the whole directory together with world persistence. If a failed store offers cancellation, it returns the garage record to deployed state and leaves the verified original vehicle in the world. For other recovery holds, keep both files and have an admin reconcile the record and world vehicle before taking further action.

## Car keys

Hold a blank `RaG_CarKey` or one of its colored variants and use **Assign car key** on an unkeyed, non-ruined car. A matching key can unlock the car or lock it with the engine off and all seats empty. A locked car blocks entry, outside door access, and inventory changes.

Combine an assigned key with a blank key to make a spare. Both remain in your inventory. If every key is lost, an authorized admin can use `RaG_CarKey_Admin` to reset a deployed car so it can be paired again.

## Portable vehicle packing

Set `EnableVehiclePacking: true` to allow portable packing. Hold the matching key and use **Pack vehicle** on a stopped, non-ruined car with the engine off and nobody inside. When `RestrictVehicleStorageToOwner` is enabled, packing and deployment require the assigned owner or an authorized admin.

To deploy, hold the packed key, enter placement mode, and use **Deploy vehicle** on a clear land surface within 10 m. Keep matching keys and storage files together. Packed cars use `$profile:\RaG_Core\Storage\RaG_Trader\Vehicles\`, separate from garage records.
