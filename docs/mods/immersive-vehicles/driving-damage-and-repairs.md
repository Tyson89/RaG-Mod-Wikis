# Driving, Damage, and Repairs

## Wet off-road sliding

When `EnableSlidingForNonOffroadCars` is enabled, a vehicle can receive a random traction impulse when all of these conditions are true:

- the engine is running;
- speed is above 7 km/h;
- the current surface is diggable/off-road;
- actual rain intensity is at least 0.50;
- the vehicle does not inherit from a class in `OffroadVehicles`.

The check runs while processing each installed wheel every two seconds. `OffroadVehicles` is therefore an exclusion list for vehicles designed to retain off-road stability.

## Impacts with infected and animals

Contact damage is applied to the vehicle when speed is at least 6 km/h and the corresponding setting is enabled.

Animals matching a config.cpp class in `AnimalCollisionDamageExceptions` are ignored before vanilla or custom vehicle contact damage is queued. Matching uses `IsKindOf`, so listed base classes also cover derived variants. Results are cached per concrete animal classname after the first check.

Damage severity combines:

- 70% normalized vehicle speed between 6 and 46 km/h;
- 30% normalized contact impulse up to 15000.

Normal infected and animals can apply up to 50 damage. Bears and cows are marked as heavy animals and can apply up to 250. Damage targets the contacted vehicle zone; when no valid zone is resolved, only 25% is applied globally. Repeated hits on the same creature have a 250 ms cooldown.

## Ruined attachments

When an unlocked vehicle attachment is ruined, the mod throws it off with the vehicle's local velocity. Exceptions are:

- every `CarWheel`;
- `Offroad_02_Hood`;
- any attachment locked in its slot.

Ruined wheels remain attached, but they still have ruined-wheel handling from DayZ.

## Damaged-engine stalls

Every 100 seconds, a moving, engine-running vehicle outside `WheelException` checks its engine health. When engine health is below DayZ's damaged threshold, the engine has roughly a 50% chance to stop. Low-oil damage can therefore progress into unexpected stalls.

## Repairs

- A Tire Repair Kit cannot repair a wheel while that wheel is mounted on a `CarScript` vehicle. Remove the wheel first.
- The car-part repair completion path is customized for `CarDoor` items. It improves the door by one condition level, never beyond Worn, synchronizes its damage zones, and consumes 25% of a quantity-based repair item.

> [!WARNING]
> The analyzed `ActionRepairCarPart` override does not call the inherited completion handler when the target is not a `CarDoor`. If repairs to other vehicle targets do nothing, that is a limitation of the current source rather than a JSON setting.

## Driver exit behavior

When the driver exits and the vehicle's gear is not neutral, the engine is stopped before the normal exit action completes. Exiting in neutral does not trigger this custom engine stop.

## Sound ranges

The mod sets the base running-engine sound-shader range for the supported vanilla vehicle shader families to 200 meters. Failed-start battery sound shaders remain at 50 meters. Custom oil, fan, and jack sound sets are configured with shorter ranges.
