# Getting Started

## Requirements

Load the mods in this order on the server and clients:

1. `RaG_Core`
2. `RaG_Immersive_Vehicles`

## Useful items

| Item | Class name | Purpose |
| --- | --- | --- |
| Engine oil, 4 L | `rag_engineoil` | Refill the oil system through the vehicle's Engine interaction zone. |
| Oil dipstick | `rag_oil_dipstick` | Display the current oil amount and capacity. |
| Hydraulic car jack | `rag_car_jack` | Lift nearby supported vehicles and permit unlocked wheel removal. |
| Farm jack | `rag_farmjack` | Alternate jack with the same wheel-removal behavior. |

## Before driving

1. Hold `rag_oil_dipstick` and aim at the vehicle's Engine zone.
2. Use **Check Oil Level**. A standard compatible vehicle should report a 4000 ml maximum.
3. If necessary, switch to `rag_engineoil`, keep the engine off, aim at the Engine zone, and refill it.
4. Check that wheels are present and secured.

The dipstick loses 2 health per completed check. Engine-oil containers are destroyed when emptied.

## Default light control

The mod registers **High Beam** on `L`, the same physical key used for normal vehicle lighting:

- use the normal light action for low beams;
- hold/use the High Beam action as the driver to toggle high beams.

High beams require a non-ruined vehicle battery with stored energy. Low beams use a 30-meter light radius; high beams use 60 meters. The binding appears in DayZ's control settings and can be changed.

## Heating

With the engine running, the driver or front passenger can use **Turn On Heating**. Heating is unavailable to classes in `HeatingException`. It stops when the engine stops or the battery is depleted, and it provides no heat comfort when the cabin is exposed.

## Changing a wheel

If `RequireCarJackWheelChange` is enabled:

1. Stop the vehicle and engine.
2. Deploy either jack within roughly 2 meters under the vehicle.
3. Use **Move Up** on the jack.
4. Remove an unlocked, non-spare wheel.
5. Replace and secure the wheel.
6. Use **Move Down** before picking up the jack.

Starting the engine clears the vehicle's lifted/wheel-detach state. A raised jack cannot be put into hands or cargo.
