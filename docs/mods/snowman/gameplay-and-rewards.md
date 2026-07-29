# Gameplay and skinning rewards

## Evil Snowman

`rag_snowman` is not decorative. It is a hostile predator built on DayZ's bear animal class and `Predator_UrsusArctos` AI template.

Current behavior:

- uses bear AI, skeleton, animation graph, movement mapping, and attack damage profiles;
- can reach the top configured movement speed of `8`;
- returns `true` from `IsDanger()`;
- ignores contaminated-area effects;
- uses custom ambient, roar, attack, capture, release, and death sounds;
- carries a blue spotlight with radius `30` and brightness `6` on clients;
- hides that light during daylight.

Attack events call the vanilla `BearBiteDamage`, `BearLeftPawDamage`, `BearRightPawDamage`, and intimidate variants. Exact player damage comes from the active DayZ version's damage profiles, not a Snowman JSON setting.

## Health and hit zones

Global health is `5000`. The model defines these local zones:

| Zone | Hit points | Melee health multiplier | Projectile health multiplier |
| --- | ---: | ---: | ---: |
| Head | `500` | `0.51` | `0.25` |
| Neck | `600` | `0.15` | `0.25` |
| Belly | `800` | `0.15` | Inherited |
| Pelvis | `1000` | `0.15` | Inherited |
| Legs | `400` | Inherited | Inherited |

These are source config values, not suggested weapon damage or guaranteed shot counts. DayZ damage processing, ammunition, hit components, and inherited animal behavior still apply.

## Light and death effects

Clients attach `rag_snowmanLight` between the model's `beamStart` and `beamEnd` memory points. The spotlight:

- uses blue ambient and diffuse color values of `0.0, 0.4, 1.0`;
- has a `120` degree angle;
- casts shadows;
- is hidden during daylight.

When the Snowman dies, clients:

1. destroy its attached light;
2. play `rag_snowman_dead_SoundSet`;
3. play the `GRENADE_M84` particle at the death position.

The particle is visual. Current Snowman death code does not add separate blast damage.

## Skinning rewards

The normal animal skinning sections intentionally produce no pelt, steaks, lard, guts, or bones. After DayZ finishes the skinning action, Snowman code creates configured rewards at the corpse position.

Default result:

- three random selections;
- each selection comes from `SnowManSkinningItems`;
- default candidates are `rag_carrot`, `Banana`, and `BakedBeansCan`;
- every selection is independent, so duplicate drops can occur.

With the default three unique entries, each selection has a one-third chance of choosing each class. The result is not guaranteed to contain one of each.

See [Server configuration](server-configuration.md) before changing amount or reward list.

## Custom carrot

`rag_carrot` is a public inventory food class:

| Property | Value |
| --- | --- |
| Display name | `Carrot` |
| Initial/max quantity | `200` |
| Inventory size | `1 x 3` |
| Weight | `0` |
| Energy config | `200` |
| Water config | `100` |
| Health | `20` |

It:

- supports normal eating and force-feeding actions;
- is treated as fruit;
- cannot be cooked or cooked on a stick;
- does not decay.

Server owners may distribute it separately through Central Economy, traders, quests, or other reward systems.
