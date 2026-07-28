# Gameplay and protection

## When Thunderstruck is active

Thunderstruck becomes active when the live weather reaches both `MinRainIntensity` and `MinOvercastIntensity`. Each value uses DayZ's normalized `0.0` to `1.0` scale.

On winter climates, snowfall is evaluated through the rain threshold. Servers do not need a separate snow setting.

The optional thunder icon tells a player that:

1. the configured weather conditions have been reached; and
2. that player is not currently in one of the protected states.

The icon is a warning, not confirmation that the next chance roll will hit the player.

## Strike chance

`HitChanceRange` defines the upper end of the random roll and `HitChance` defines the first successful value. With the published values:

```json
"HitChanceRange": 100,
"HitChance": 99
```

values `99` and `100` are successful. The Workshop describes this as a theoretical 2% chance.

Do not assume that `HitChance` is a direct percentage. Treat the pair as a range and threshold:

- lowering `HitChance` creates more successful values and makes strikes more frequent;
- raising `HitChance` makes strikes less frequent;
- increasing `HitChanceRange` without changing the threshold also changes the probability.

Test aggressive values on a staging server. Weather evaluation and the random roll can run repeatedly while a storm remains active.

## What a strike does

A successful strike:

- reduces player health according to `ReducedPlayerHealth`;
- optionally changes the condition of worn attachments and the item in the player's hands;
- creates every valid class listed in `ThunderstruckItems` at the player's position;
- creates lightning effects and a burning impact area;
- can announce the struck player's name to the server.

The published `ReducedPlayerHealth` value is `0.25`, described by the mod as a 75% health reduction. The allowed range is `0.0` to `1.0`.

`AttachmentsDamageLevel` uses DayZ's five item-condition levels:

| Value | Condition |
| ---: | --- |
| `0` | Pristine |
| `1` | Worn |
| `2` | Damaged |
| `3` | Badly Damaged |
| `4` | Ruined |

The setting only applies when `AllowDamagePlayerAttachments` is `1`. Items that are already ruined stay ruined.

## Protected players

A player is not a valid strike target while any of these conditions applies:

- dead;
- unconscious;
- inside any transport;
- inside a building or covered by a roof;
- inside a supported safe zone;
- protected by supported god mode.

The built-in integrations cover:

- DayZ Expansion Market safe zones;
- Trader by Dr. Jones safe zones;
- TraderPlus safe zones;
- VPP Admin Tools god mode;
- Community Online Tools god mode.

The weather icon is hidden while safe-zone or god-mode protection applies.

## Tinfoil hat

An unruined tinfoil hat protects its wearer from the normal strike damage. The hat loses health on each absorbed hit and stops being useful once ruined.

This protection is equipment-based. Do not use it as a substitute for safe-zone configuration or admin-tool god mode.

## Repeat strikes

`CanGetHitAgain` controls whether the same character remains eligible after surviving a strike:

- `0`: the player can be hit only once until the character respawns or the server restarts;
- `1`: the player can be selected again while the other requirements are met.

This state is not documented as persistent across server restarts.
