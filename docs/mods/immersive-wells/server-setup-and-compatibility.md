# Setup, compatibility, and troubleshooting

## Required mod

[RaG Core](../core/index.md) is a declared hard dependency in `CfgPatches.requiredAddons`. Install and enable both mods on the server and every client. DayZ resolves addon/PBO ordering from declared dependencies; changing the server `-mod` sequence does not change it.

## Installation

1. Stop server.
2. Install original RaG Core and RaG Immersive Wells Workshop releases.
3. Copy both signature keys into server `keys` directory if host does not do that automatically.
4. Add both mods to the client/server mod set.
5. Start server once.
6. Stop it after this file appears:

   ```text
   $profile:\RaG_Core\Configs\RaG_Immersive_Wells\RaG_Immersive_Wells.json
   ```

7. Edit generated file if needed.
8. Restart and test direct drinking, container filling, and hand washing at several wells.

Generated file is schema for installed build. Back it up during updates and merge custom values into freshly generated schema when fields change.

## Supported wells and class names

Immersive Wells adds no new public inventory, economy, trader, or placeable-well class.

It changes DayZ's script base `Well`, so its availability and action logic applies to objects derived from that class. Current config explicitly adds animated `Arm` source to these vanilla world classes:

| Class name | Source | Effect |
| --- | --- | --- |
| `Land_Misc_Well_Pump_Blue` | Vanilla DayZ | Random water state plus supported handle animation, sound, and particle position. |
| `Land_Misc_Well_Pump_Yellow` | Vanilla DayZ | Random water state plus supported handle animation, sound, and particle position. |

Do not add these static map classes to `types.xml`. Mod ships no Central Economy XML and no spawner. Existing map wells receive behavior automatically.

## RaG Baseitems integration

When `rag_baseitems_buildings` compile definition is available, Immersive Wells modifies:

```text
Land_rag_well
```

That well:

- always has water;
- bypasses `WellWaterChance`;
- reports no animated-well effects.

RaG Baseitems is optional. Install and enable it on the server and clients when this well is used. No server mod-list ordering is required.

## Custom-well compatibility

Custom object must inherit DayZ `Well` to receive automatic behavior. Default inherited behavior:

- randomizes water availability;
- expects animated well;
- uses `Arm` animation source;
- places water particle at fallback model-space position `0 1 0`.

Custom-mod author should override as needed:

| Method | Override purpose |
| --- | --- |
| `IsAnimatedWell()` | Return `false` when model has no compatible `Arm` animation. This also prevents Immersive Wells pump sound and particle state from starting. |
| `IsWellException()` | Return `true` when custom well must always have water. |
| `GetWaterPosition()` | Return correct world position for water particle. |

Merely looking like well or returning water liquid type is not enough. Non-`Well` sources do not use random availability or cholera hooks.

## Current-source limitations

- Water state has no persistence record, depletion, recovery timer, or manual reroll command.
- Availability changes need object reinitialization, normally server restart.
- `WellWaterChance: 0` still gives about 0.99% usable chance.
- Enabled `WellCholeraChance: 0` still gives 1% successful exposure roll.
- One shared playing boolean controls each well. Concurrent users can interrupt audiovisual effect for each other.
- Only blue and yellow vanilla pumps receive animation source in this mod config.
- Custom wells need correct overrides for animation and particle placement.
- Broken prompt can appear briefly before continuation is stopped because vanilla action conditions still identify object as water source.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Server reports missing `RaGConfigVersioned`, `RaGConfigIO`, `RaGConfigAPI`, or RaG Core particle symbols | RaG Core is missing, outdated, or mismatched between server and clients. Use matching current builds. |
| JSON does not generate | Confirm the active server profile, folder permissions, RaG Core startup, and that both required mods are enabled. Expected path is `$profile:\RaG_Core\Configs\RaG_Immersive_Wells\RaG_Immersive_Wells.json`. |
| Editing profile-root JSON changes nothing | Current source uses RaG Core config subdirectory. Edit exact path above. |
| Roughly half wells are broken with default config | Expected. Default usable chance is about 50.5%. |
| `WellWaterChance: 0` leaves rare working well | Expected off-by-one behavior. Roll includes zero. |
| Working well has no handle movement | Confirm class is supported blue/yellow vanilla pump. Custom well needs `Arm` animation source or `IsAnimatedWell()` override. |
| Handle moves but no water particle | Verify matching RaG Core/client mod versions. Custom well may need `GetWaterPosition()` override. |
| Pump sound or particle remains active | Another mod may interrupt action lifecycle, or concurrent player state may desynchronize shared playing boolean. Retest alone with only required mods. |
| Cholera never transfers | Set toggle to `1`, validate JSON, restart, then complete direct-drink or fill animation loops. Washing does not transfer it. |
| Cholera affects bottle | Expected. Fill action inserts cholera agent into container, not player. |
| Pond filling breaks | Current source guards non-well targets. Test mod conflict changing `ActionFillBottleBase`; Immersive Wells alone leaves ponds on vanilla path. |
| RaG Baseitems well gets randomized or animates | Optional compile block did not activate. Confirm RaG Baseitems is enabled and use matching current builds. |

## Safe configuration rules

- Stop server before editing JSON.
- Keep valid JSON and retain `Version`.
- Use `0` or `1` for boolean toggle.
- Keep chance values within documented `0-100` range unless exact source edge behavior is intentional.
- Restart after changes.
- Test several wells because availability is randomized per object.
