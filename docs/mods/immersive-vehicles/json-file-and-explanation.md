# Server Configuration

RaG Immersive Vehicles generates its configuration under the server profile at:

```text
RaG_Core/Configs/RaG_Immersive_Vehicles/RaG_Immersive_Vehicles.json
```

Boolean settings use `0` for disabled and `1` for enabled. The example below matches the version 2 source defaults.

> [!IMPORTANT]
> Stop the server and back up the file before editing. Keep `Version` unchanged, preserve exact key names, validate the JSON, and then restart the server.

## Supplied configuration

```json
{
    "Version": 2,
    "RequireCarJackWheelChange": 1,
    "PlayerInCarCanBeTargetedByAI": 1,
    "EnableSlidingForNonOffroadCars": 1,
    "EnableAnimalDamageOnContact": 1,
    "EnableInfectedDamageOnContact": 1,
    "WheelDamageRoad": 0.0020000000949949028,
    "WheelDamageOffroad": 0.004000000189989805,
    "OffroadVehicles": [
        "Offroad_02",
        "OffroadHatchback",
        "rag_landrover_110_base",
        "rag_zil_130_base",
        "mtvr_base",
        "rag_jeep_willys_base",
        "rag_hummer_Armored_base",
        "rag_gaz69",
        "rag_atv_base",
        "Bicycle_Base",
        "Expansion_Landrover_Base",
        "Snowmobile_Base",
        "Techs_ATV_base",
        "Techs_Hilux_base"
    ],
    "WheelException": [
        "vg7_scorpion",
        "Snowmobile_Base",
        "ExpansionHelicopterScript",
        "Raft",
        "RFFSHeli_base",
        "RFMosquito_mod",
        "Bicycle_Base"
    ],
    "HeatingException": [
        "rag_jeep_willys_base",
        "rag_gaz69",
        "rag_derby_car_base",
        "rag_baja_base",
        "rag_atv_base",
        "vg7_scorpion",
        "Snowmobile_Base",
        "Raft",
        "Bicycle_Base"
    ],
    "AnimalCollisionDamageExceptions": [
        "Horse_Base",
        "Dayz_Doggo",
        "DoggoPuppy_Base"
    ]
}
```

The long wheel-damage decimals are normal serialized 32-bit float values. They represent source defaults of `0.002` and `0.004`.

## General settings

| Setting | Supplied | Behavior |
| --- | ---: | --- |
| `Version` | `2` | Configuration schema version. Do not edit it. |
| `RequireCarJackWheelChange` | `1` | Requires a raised RaG jack before an unlocked, non-spare wheel can be released from a supported vehicle. Wheel exceptions use inherited behavior. |
| `PlayerInCarCanBeTargetedByAI` | `1` | Enables the custom targeting path for occupants whose seat door is not closed, including explicit infected attack handling. |
| `EnableSlidingForNonOffroadCars` | `1` | Enables random traction impulses on diggable surfaces when rain is at least 0.50 and the vehicle is not in `OffroadVehicles`. |
| `EnableAnimalDamageOnContact` | `1` | Allows animal impacts at 6 km/h or faster to damage the vehicle. Bears and cows use the heavy-animal damage cap. |
| `EnableInfectedDamageOnContact` | `1` | Allows infected impacts at 6 km/h or faster to damage the vehicle. |
| `WheelDamageRoad` | `0.0020000000949949028` | Road-surface multiplier used by the two-second RPM-based wheel-wear calculation. |
| `WheelDamageOffroad` | `0.004000000189989805` | Diggable/off-road surface multiplier used by the same wheel-wear calculation. |

## Class lists

Each array contains config.cpp class names. Matching uses `IsKindOf`, so derived classes inherit listed behavior.

| Array | Purpose |
| --- | --- |
| `OffroadVehicles` | Excludes matching classes from the wet off-road sliding impulse. It does not disable wheel wear. |
| `WheelException` | Excludes matching classes from custom wheel wear, random wheel fall-off, jack/removal restrictions, and the mod's 100-second damaged-engine stall check. Use it for boats, helicopters, bicycles, snowmobiles, and unusual wheel systems. |
| `HeatingException` | Removes the heating action from matching classes. Use it for open cabins, ATVs, boats, bicycles, and vehicles that should not provide enclosed-cabin heat. |
| `AnimalCollisionDamageExceptions` | Prevents matching animals from causing vanilla or Immersive Vehicles collision damage to the vehicle. Add animal base classes from any installed mod. |

Animal exception results are cached per concrete animal classname after the first inheritance check, avoiding repeated config searches during frequent contact callbacks.

## List migration behavior

The loader ensures every array exists. Existing built-in defaults for `OffroadVehicles`, `WheelException`, and `HeatingException` are restored when missing.

`AnimalCollisionDamageExceptions` behaves differently:

- New configuration files receive `Horse_Base`, `Dayz_Doggo`, and `DoggoPuppy_Base`.
- Version 1 configurations receive these entries once during migration to version 2.
- Version 2 configurations may remove any animal exception; removed entries stay removed.
- Third-party animal base classes can be added freely.
- Spelling and capitalization must match the DayZ config.cpp classname.

The old wiki used nested objects such as `VehiclesOffroad.VehicleList`. That shape does not match the current source. Use the direct arrays shown above.
