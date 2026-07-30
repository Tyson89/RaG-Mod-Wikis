# Server configuration

RaG Viking Pack stores versioned config at:

```text
$profile:\RaG_Core\Configs\RaG_Viking_Pack\RaG_Viking_Pack.json
```

Stop server before editing. Keep valid JSON, retain `Version`, and restart after each change.

## Default version 1 configuration

```json
{
  "Version": 1,
  "CanCraftShelterKit": 1,
  "DisableDamageForPlaceables": 1
}
```

DayZ's JSON serializer represents script booleans as `1` and `0`.

## Settings

| Setting | Default | Actual effect |
| --- | ---: | --- |
| `Version` | `1` | Current schema version. Values below `1` are upgraded and saved as version `1`. |
| `CanCraftShelterKit` | `1` | Enables built-in three-plank plus five-stick shelter recipe. Does not block existing, spawned, traded, or scripted shelter kits. |
| `DisableDamageForPlaceables` | `1` | Calls `SetDamageDisabled(true)` only in `viking_shelter` constructor. It does not currently control table, firepit, sundial, or warbanner damage. |

## Examples

Disable shelter crafting but keep shelter invulnerable:

```json
{
  "Version": 1,
  "CanCraftShelterKit": 0,
  "DisableDamageForPlaceables": 1
}
```

Enable shelter crafting and configured shelter damage:

```json
{
  "Version": 1,
  "CanCraftShelterKit": 1,
  "DisableDamageForPlaceables": 0
}
```

When damage is enabled, shelter uses its config-defined `50000` global health and damage multipliers:

| Damage category | Health multiplier |
| --- | ---: |
| Projectile | `1` |
| Melee | `0.65` |
| Frag grenade | `20` |

These are damage-system coefficients, not fixed damage or guaranteed hit counts.

## No settings for other systems

Current JSON has no controls for:

- lantern burn time, light radius, or fuel;
- raven detection radius, food use, or health loss;
- horn duration or noise;
- Idun health, stamina, or disease removal;
- coin conversion ratios;
- weapon damage;
- placeable kit dismantle tools or action time.

Those values are hard-coded in scripts or `config.cpp`.

## Configuration recovery

If file is missing or invalid:

1. Stop server.
2. Back up broken file.
3. Move it outside active profile config directory.
4. Start server once to generate defaults.
5. Stop server.
6. Merge wanted values into generated schema.
7. Restart and test shelter crafting, placement, damage, and dismantling.
