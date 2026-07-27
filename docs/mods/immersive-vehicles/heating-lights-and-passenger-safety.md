# Heating, Lights, and Passenger Safety

## Vehicle heating

The driver and front passenger can toggle heating while the engine is running, unless the vehicle is listed in `HeatingException`.

Heating switches the player's environment behavior to DayZ's normal `CAR_ENGINE_ON` heat-comfort category only while the passenger compartment remains enclosed. Heat comfort is blocked by:

- any ruined vehicle damage zone whose name contains `window`;
- a ruined window zone on an attached car door;
- an open or missing attachment slot whose name contains `door`, `trunk`, or `hatch`;
- the engine stopping.

Slots containing `hood` are explicitly excluded from the cabin check.

Heating plays a looping interior-fan sound. It consumes battery energy in 100-second updates at a rate derived from the vehicle's recharge value; it switches off when the battery reaches zero.

## Interior light

A warm interior point light switches on when an attached car door is open and the vehicle has usable electrical power. It switches off when no attached door is open or power is unavailable. The light is hidden during daylight.

Vehicle creators should provide `light_interior`. If it is absent, the mod tries `dmgZone_roof` with a 0.3-meter upward offset, then falls back to `0 1.564 -0.098` in model space.

## Low and high beams

The driver can toggle high beams with the **High Beam** input, bound to `L` by default. Turning on high beam also turns on the vehicle lights if necessary.

| Mode | Light radius |
| --- | ---: |
| Low beam | 30 meters |
| High beam | 60 meters |

High beam requires a present, non-ruined Car Battery or Truck Battery with stored energy. Turning high beam off leaves the normal light state available.

## Occupant targeting

When `PlayerInCarCanBeTargetedByAI` is enabled, an occupant can be targeted when the door state for that seat is not closed. The infected attack path is explicitly extended so infected can attack such an exposed occupant.

A closed seat door prevents this custom targeting path. Disabling the setting returns player targeting to the inherited DayZ behavior.
