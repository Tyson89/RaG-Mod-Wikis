# Vehicle-Modding Guide

RaG Immersive Vehicles applies most behavior by modding `CarScript`, so derived vehicles receive it automatically. Full compatibility still depends on standard damage zones, attachment slots, memory points, batteries, wheels, and capacity values.

The mod publishes this preprocessor definition for optional compile-time compatibility:

```c
#define RAG_IMMERSIVE_VEHICLES
```

## Compatibility checklist

| Feature | Vehicle requirement | Fallback / failure behavior |
| --- | --- | --- |
| Engine oil capacity | Effective `oilCapacity = 4;` | The dipstick reports **OIL LEVEL ERROR** when capacity is not 4000 ml. |
| Oil refill and dipstick | A View Geometry component that resolves to damage zone `Engine`; retain a valid Engine damage zone. | The interaction does not appear when the component cannot resolve to `Engine`. |
| Oil smoke | Memory point `ptcEnginePos`. | Smoke falls back to the vehicle origin. |
| Interior light | Memory point `light_interior`. | Tries `dmgZone_roof` plus `0 0 0.300`, then `0 1.564 -0.098`. |
| Interior-fan sound | Memory point `dmgZone_windowFront`. | Uses the vehicle's world position and can sound misplaced. |
| Heating integrity | Standard window damage-zone names and attachment slot names containing door/trunk/hatch. | Nonstandard names may bypass exposure checks; slots containing hood are ignored. |
| Seat protection / AI | Working `GetDoorInvSlotNameFromSeatPos()` and `GetCarDoorsState()` mapping. | A nonstandard seat-door map can make targeting inaccurate. |
| Wheel wear and loss | Wheels inherit `CarWheel`; installed slots are listed in `attachments[]`; spare slot names contain `spare`. | Nonstandard wheel types or slots may be skipped. |
| Electrical features | Standard Car Battery or Truck Battery vital-part configuration. | High beam and interior light require usable electrical power. |

## Correct oil capacity

The current action code converts the configured capacity to milliliters and explicitly compares it with `4000`. Use:

```c
class CarScript;
class MyVehicle_Base: CarScript
{
    oilCapacity = 4;
};
```

Do not use `oilCapacity = 1;` for this version. That older wiki recommendation contradicts the current dipstick and 4-liter oil-container implementation.

## Engine interaction zone

Oil actions inspect the aimed View Geometry component and ask DayZ's damage system to resolve it to `Engine`. Provide an Engine selection/component in the appropriate geometry and a normal Engine damage zone in the vehicle config.

## Memory points

Recommended model-space memory points:

- `ptcEnginePos` - low-oil smoke origin;
- `light_interior` - cabin point-light origin;
- `dmgZone_windowFront` - interior-fan sound origin;
- standard left/right headlight and target points inherited by `CarScript`.

If `light_interior` is unavailable, `dmgZone_roof` should be positioned so that adding 0.3 meters vertically places the light inside the cabin.

## Configuration lists

Add the vehicle's stable base class to the relevant direct array:

- `OffroadVehicles` for vehicles that should not receive wet off-road sliding impulses;
- `WheelException` for helicopters, boats, bikes, tracked vehicles, or custom wheel systems;
- `HeatingException` for open cabins and vehicles that should not provide heat.

Matching uses `IsKindOf`, so one base-class entry covers its derived variants. Built-in defaults are reinserted when missing, making the lists additive.
