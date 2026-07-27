# Wheels and Jacks

## Wheel wear

Wheel health is updated every two seconds when the engine is running and speed is above 7 km/h. Spare-wheel slots are ignored.

The calculation uses engine RPM, the wheel's maximum health, and one of these configuration values:

- `WheelDamageRoad` when the surface is not diggable;
- `WheelDamageOffroad` when the surface is diggable.

The mod also raises the global health of six vanilla wheel classes to 200 hit points: Hatchback, Civilian Sedan, Gunter/Hatchback 02, Sedan 02, Truck 01, and Offroad 02 wheels.

## Why a wheel falls off

Every 100 seconds, a moving, engine-running vehicle that is not in `WheelException` checks its attached wheels. Each unlocked, non-spare wheel has a random chance to be thrown off the vehicle.

Secure installed wheels using the vehicle's supported wheel-locking mechanic. A raised jack permits removal only of wheels that are still unlocked; it does not override an inventory-slot lock.

## Hydraulic and farm jacks

Both `rag_car_jack` and `rag_farmjack` are deployable and use the same vehicle detection logic.

- The jack checks approximately 2 meters around its lift point.
- Raising it stops the engine of each nearby supported vehicle and enables wheel detachment.
- Lowering it disables wheel detachment.
- Starting the engine also disables the lifted state.
- Each completed up/down interaction deals 0.5 damage to the jack.
- A raised jack cannot be placed in cargo or taken into hands.
- Classes in `WheelException` ignore the custom jack and wheel-detach handling.

The placement hologram intentionally bypasses collision rejection for both jacks. Place the lift point under the target vehicle, not merely beside it.

## Configuration switch

When `RequireCarJackWheelChange` is `0`, supported unlocked wheels can be removed without raising a jack. Locked wheels and spare-wheel slots keep their normal behavior.

## Admin wheel actions

When compiled with VPP Admin Tools or Community Online Tools, authorized admins receive **[ADMIN] Lock Wheels** and **[ADMIN] Unlock Wheels** actions on vehicles. These iterate all attached `CarWheel` items.

The actions do not appear to ordinary players, and no admin wheel action is available when neither supported admin tool is present.
