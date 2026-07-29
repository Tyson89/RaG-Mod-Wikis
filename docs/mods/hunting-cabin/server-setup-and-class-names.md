# Setup, class names, compatibility, and troubleshooting

## Required mod and load order

[RaG Core](../core/index.md) is a hard dependency declared in `CfgPatches.requiredAddons`. Load both mods on server and every client:

```text
@RaG_Core;@RaG_Hunting_Cabin
```

Actual folder names may differ. Dependency order must not.

## Installation

1. Stop server.
2. Install original RaG Core and RaG Hunting Cabin Workshop releases.
3. Copy both signature keys into server `keys` directory if host does not do that automatically.
4. Add both mods to client/server mod parameter, with Core first.
5. Start server once.
6. Stop it after this file appears:

   ```text
   $profile:\RaG_Core\Configs\RaG_Hunting_Cabin\RaG_Hunting_Cabin.json
   ```

7. Edit generated file if needed, restart, and test full craft-to-build flow.

Generated file is schema for installed build. Back it up during updates and merge custom values into a freshly generated schema when fields change.

## Optional lock compatibility

### CodeLock Mod

Load CodeLock before Hunting Cabin so `CodeLock` conditional source is available:

```text
@RaG_Core;@CodeLock;@RaG_Hunting_Cabin
```

Exact CodeLock folder name may differ. With integration active, this file is also generated:

```text
$profile:\CodeLock\RaG_Hunting_Cabin_CodeLockConfig.json
```

See [Server and CodeLock configuration](server-configuration.md).

### Expansion Code Lock

Hunting Cabin commit `2054740` removed embedded Expansion compatibility on March 7, 2026. Current support is in separate `RaG_Expansion_Compat` source.

Use load order:

```text
@RaG_Core;@DayZ-Expansion...;@RaG_Hunting_Cabin;@RaG_Expansion_Compat
```

Expansion package names vary. Load its base-building component before compatibility mod. Hunting Cabin alone is not current Expansion compatibility.

## Public class names

| Class name | Type | Use |
| --- | --- | --- |
| `rag_hunting_cabin_kit` | Inventory/deployable | Normal player kit. Placement creates material hologram. |
| `rag_hunting_cabin_admin_kit` | Inventory/deployable | Privileged kit. Placement creates finished admin cabin immediately. |
| `rag_hunting_cabin_hologram` | Static material container | Construction site created by normal kit. |
| `rag_hunting_cabin` | Base-building structure | Completed cabin. |
| `rag_temp_materials_box` | Temporary material container | Dismantling refund holder for normal cabin. |

`HuntingCabinLight` is scripted client-side helper, not inventory or economy class.

## Economy and trader entries

Current source ships no Central Economy XML.

For normal player distribution, add only:

```text
rag_hunting_cabin_kit
```

Keep these out of normal economy and traders:

- `rag_hunting_cabin_admin_kit`;
- `rag_hunting_cabin_hologram`;
- `rag_hunting_cabin`;
- `rag_temp_materials_box`;
- `HuntingCabinLight`.

Directly spawning completed cabin or hologram bypasses intended kit flow and can produce bad state. Admin kit intentionally bypasses all material and tool requirements.

## Gameplay configuration

Cabin reads DayZ's `disableBaseDamage` through `CfgGameplayHandler`.

To use `cfggameplay.json`, server must enable:

```text
enableCfgGameplayFile = 1;
```

Then set general value as intended:

```json
"disableBaseDamage": true
```

This affects base-building objects broadly, not only Hunting Cabin.

Cabin kit source already bypasses its normal collision result. If players cannot place ordinary items inside cabin, inspect active `HologramData` collision and roof-clipping checks in `cfggameplay.json`; changing them affects other placement across server.

## Current-source limitations

- Cabin has no cargo capacity.
- No hide/show inventory actions exist.
- No fireplace class, attachment, or scripted fireplace feature exists.
- Door and windows always close after restart.
- Light switch state always resets off after restart.
- Force Synchronize is available to any player when cabin is empty.
- No dedicated JSON setting controls cabin health, damage, dismantle tools, build tools, or action time.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Server reports missing `RaGConfigVersioned`, `RaGConfigIO`, `RaGConfigAPI`, or other RaG Core classes | RaG Core missing, outdated, or loaded after Hunting Cabin. Use matching versions and Core first. |
| Main JSON does not generate | Confirm active server profile, folder permissions, RaG Core startup, and load order. Expected path is `$profile:\RaG_Core\Configs\RaG_Hunting_Cabin\RaG_Hunting_Cabin.json`. |
| Kit recipe missing | Set `CanCraftHuntingCabinKit` to `1`, validate JSON, restart. Recipe still needs at least `10` planks and `50` nails. |
| Kit will not place | Check territory/permission mods and server-side placement overrides. Cabin source bypasses its own collision result, but other systems can deny placement. |
| Build action missing | Attach all four material types with configured quantities, aim at stairs, stand, and use non-ruined hammer or hatchet. |
| Material amount set to zero but build still missing | Expected source behavior. All four material attachments must exist even when configured minimum is zero. |
| Tool ruined after build | Default behavior. `RuinHammerAfterBuilt` applies to hammer and hatchet despite its name. Set it to `0` for `10` health damage instead. |
| Cabin cannot be dismantled | Stand inside, aim at door, remove lock and lights, and use non-ruined crowbar, hatchet, or sledgehammer. |
| Material refunds missing | `GiveBackMaterialsAfterDismantle` must be `1`; admin cabins never return materials. Search cabin's `materials_spawn` side for refund box. |
| Door or windows closed after restart | Expected. Persistence restore explicitly closes open door and every window. |
| Lights are off after restart | Expected. On/off booleans are not saved. |
| Combination lock blocks door | Enter correct combination or destroy lock with hand saw/hacksaw. Five six-second cycles are required. |
| CodeLock JSON missing | CodeLock conditional integration did not compile. Confirm CodeLock loaded before Hunting Cabin on server and clients. |
| Expansion Code Lock does not work | Install current RaG Expansion Compat after Expansion and Hunting Cabin. Embedded support was removed from Hunting Cabin. |
| **Force Synchronize** appears | Cabin is empty. Action recreates cabin to repair sync; it also resets states and admin flag. Do not use casually. |
| Expected storage, hide/show inventory, or fireplace is absent | Current source does not implement those Workshop claims. |

## Safe update rules

- Stop server before editing JSON.
- Preserve `Version` in main config.
- Keep valid JSON and exact key spelling.
- Use whole, non-negative material quantities.
- Test normal and admin dismantling separately.
- Test every enabled lock mod after updates.
- Never distribute admin kit to normal players.
