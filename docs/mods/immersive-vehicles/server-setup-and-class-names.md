# Server Setup and Class Names

## Dependencies

RaG Core and RaG Core Scripts are hard dependencies in the mod config. Install and enable the required mods on the server and clients. DayZ resolves addon/PBO ordering from declared dependencies; server mod-list order does not. Missing or outdated RaG Core can break configuration loading, client synchronization, logging, or the engine-oil liquid type.

## Generated configuration

After the first startup, the configuration is stored under the server profile:

```text
RaG_Core/Configs/RaG_Immersive_Vehicles/RaG_Immersive_Vehicles.json
```

Stop the server before editing it. See [Server configuration](json-file-and-explanation.md).

## Economy and trader class names

| Class name | Description | Shipped size / quantity |
| --- | --- | --- |
| `rag_engineoil` | Custom engine-oil container. | 3x4 inventory; 4000 ml. |
| `rag_oil_dipstick` | Oil-level inspection tool. | 3x1 inventory. |
| `rag_car_jack` | Hydraulic car jack. | 5x3 inventory; 10 kg. |
| `rag_farmjack` | Farm jack with the same lifting behavior. | 2x4 inventory; 10 kg. |

These are the four player-facing `scope=2` item classes added by the mod. Wheel classes in `config.cpp` are vanilla overrides, not new economy items.

## Optional integrations

- VPP Admin Tools: authorized admins can lock or unlock every attached wheel.
- Community Online Tools (`JM_COT`): the same admin actions are available while COT is active.
- Third-party vehicles: features apply through `CarScript` inheritance, subject to the requirements in [Vehicle-modding guide](modding.md).

## Troubleshooting

### Old JSON no longer loads correctly

The current schema uses capital `Version` and direct string arrays named `OffroadVehicles`, `WheelException`, and `HeatingException`. The older nested `VehicleList` shape is wrong for the analyzed source.

### A deleted default list entry returns

This is intentional in the current loader. On every load, missing built-in entries are inserted back into all three arrays and the file is saved. Treat the lists as additive; add compatibility classes instead of trying to remove shipped defaults.

### Oil refill or dipstick action is missing

The vehicle must inherit `CarScript`, expose a View Geometry component that resolves to the `Engine` damage zone, and have a working oil capacity. The engine must be off for refilling.

### Dipstick reports an oil-capacity error

Set the effective vehicle config to `oilCapacity = 4;`. The current dipstick implementation explicitly expects 4000 ml.

### A wheel cannot be removed

Check whether it is locked, whether it is a spare slot, whether the vehicle is in `WheelException`, and whether the jack requirement is enabled. If a jack is required, lower/reposition it directly under the vehicle and raise it again with the engine off.

### Heating action is missing

Only the driver and front passenger receive the action, the engine must be running, and the vehicle must not match `HeatingException`.

### Non-door vehicle repair does nothing

The current `ActionRepairCarPart` completion override handles `CarDoor` targets only and does not fall back to the inherited handler. This cannot be corrected through the Immersive Vehicles JSON.
