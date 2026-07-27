# Locks, Damage, and Raiding

## Supported locks

| System | Current source status |
| --- | --- |
| Vanilla Combination Lock | Supported on completed door/gate structures and the floor hatch. |
| Codelock Mod | Conditional integration exists under the `CodeLock` compile flag. Windows are excluded. |
| Expansion Code Lock | No support. |

Removing a constructed gate or door stage unlocks its attached vanilla Combination Lock. The Codelock compatibility path also unlocks a Codelock when the protected door stage is dismantled.

## Damage modes

`DisableAllDamage` takes priority and rejects all calculated damage to RaG BaseBuilding structures.

`DisableDamageButDoors` applies only to structures that report a gate/door part, and explicitly excludes windows. In this mode:

- direct damage to non-door zones is rejected;
- direct damage to recognized door zones is processed normally;
- explosion damage is redirected to one available primary door zone using the explosion's highest health damage value.

Do not enable both settings unless total immunity is intentional.

## Dismantling

`DisableDismantle` disables player dismantling. Otherwise, a tool in `BaseDismantleTools` can dismantle a stage when it has no dependent stage. The current system refunds that stage's configured materials at 100%, dropping stacks near the structure.

The shipped source defaults allow `Hatchet` and `Crowbar` and use a 15-second action with 3 points of tool damage. A wooden-storage structure must be empty before it can be dismantled.

The separate floor-hatch ladder is an exception: it has a custom dismantle action registered on Hatchet, Wood Axe, Firefighter Axe, Crowbar, and the admin hatchet. That action does not consult `DisableDismantle` or `BaseDismantleTools`, and it does not refund the ladder materials.

## Destroying and raiding

The mod retains DayZ construction damage/destruction behavior and includes conditional BreachingCharge type mapping for double doors, double gates, left/right gates, and floor hatches.

`ToolDamageOnVanillaLockDestroy` is active and controls tool damage when destroying a vanilla Combination Lock.

The configuration also defines `BaseDestroyTools` and `BaseDestroyToolDamage`, but the analyzed RaG BaseBuilding scripts do not read either value outside config initialization. Treat both as currently inactive schema fields unless another server-side mod deliberately consumes them.
