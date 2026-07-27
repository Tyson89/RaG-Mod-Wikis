# Engine Oil

## Initial oil and fuel

When the central economy creates a vehicle, the mod fills both fuel and engine oil with a random value from 0% through 35% of that vehicle's configured capacity. A newly spawned vehicle can therefore be nearly empty.

## Dashboard warning

The vanilla oil warning icon is updated while the engine is running:

| Oil fraction | Dashboard behavior |
| --- | --- |
| Above 50% | Oil warning hidden. |
| Above 10% through 50% | Yellow oil warning. |
| 10% or below | Red oil warning. |

The warning is hidden when the engine is off.

## Driving with low oil

Every two seconds, while the engine is on and the vehicle is moving above 7 km/h:

- oil below 50% causes randomized Engine-zone health damage;
- a damaged engine leaks oil while some oil remains;
- oil at or below 50% produces engine smoke on clients.

The lower the oil fraction, the greater the possible damage. Refill before driving; the dashboard icon is not merely cosmetic.

## Check the oil

Hold `rag_oil_dipstick`, aim at a component that resolves to the `Engine` damage zone, and complete **Check Oil Level**. The result is sent as a notification and the dipstick loses 2 health.

The implementation expects a 4-liter vehicle oil capacity. If the capacity is not 4000 ml, the player receives an **OIL LEVEL ERROR** notification naming the vehicle.

## Refill the oil

Hold `rag_engineoil`, switch the engine off, aim at the Engine zone, and use the refill action. The container holds 4000 ml and accepts only the engine-oil liquid type supplied through RaG Core's liquid system.

The refill action converts 1000 ml in the container to 1 unit of vehicle oil capacity. A third-party vehicle must expose a usable Engine damage zone or the action will not appear.

## Server economy class names

- `rag_engineoil` - custom 4000 ml engine-oil container.
- `rag_oil_dipstick` - oil-level inspection tool.

The mod also extends the vanilla `EngineOil` script with its pouring sound behavior, but `rag_engineoil` is the class explicitly configured and shipped by this mod.
