# Gameplay and encounters

## Pumpkin grenade

`rag_pumpkingrenade` is a non-lethal grenade with no usable pin. It arms itself when created and activates when it contacts another object.

With the default configuration, its explosion produces one of two outcomes:

- **Rewards:** 2-5 random entries from `PumpkinGrenade_Items`.
- **Ambush:** 1-3 random entries from `PumpkinGrenade_SpawnableAI`.

Each selection is independent, so duplicate items or AI can appear. Repeating a classname in a configured array also gives that class additional weight.

The reward objects are created within roughly half a meter of the grenade. The configured AI use the same small spawn area, so do not substitute large creatures without testing collision and placement.

## Searchable graves

When `Tombstone_Enabled` is enabled, each supported grave or corpse-pile object makes one chance roll about 2.5 seconds after it initializes. A successful roll creates an invisible interaction object on the grave.

To search an eligible grave:

1. Equip a non-ruined shovel.
2. Aim at the grave and use **There is something...**
3. Complete the normal dig-stash duration.

The search produces either:

- one random class from `Tombstone_Items`; or
- one random class from `Tombstone_SpawnableAI`.

The interaction object is deleted after use, so that grave cannot be searched again until a later object initialization, normally after a server restart. A grave that fails its initial chance roll has no action.

The default reward chance is approximately 50.5%. The default AI is `ZmbM_Mummy`.

!!! note "Custom-placed grave version"
    Custom-placed grave support is fixed in commit `bd688e0` and later. These builds create and position the interaction helper using the grave's `GetWorldPosition()`. Builds from before that fix can place the helper at world origin and should be updated.

## Boogieman ambush

When `BoogieMan_Enabled` is enabled, supported boogieman props receive a 5-meter player trigger.

The first player to enter it:

1. triggers the witch sound and flash particle;
2. spawns a random amount between `BoogieMan_MinSpawnableAIAmount` and `BoogieMan_MaxSpawnableAIAmount`;
3. selects every spawn independently from `BoogieMan_SpawnableAI`;
4. consumes the trigger.

AI appear 1-2 meters away on each horizontal axis. The prop itself remains, but it does not create another trigger during the same initialization cycle.

Defaults spawn 3-6 mummies.

## Spooky pedestal

Place or event-spawn `rag_spooky_pedestal`. A player can interact with its **Are you Brave?** action once.

The sequence is fixed:

| Time after activation | Event |
| ---: | --- |
| Immediately | Rage mode begins, the gates and lights change, and the activation action is disabled. |
| 6 seconds | Ghost animation, lighting, and sound start. |
| 12 seconds | Cat animation and sound start. |
| 15 seconds | Skull animation and sound start. |
| 24 seconds | The configured coffin-or-AI outcome spawns 3-20 meters away on each horizontal axis. |
| 60 seconds | The pedestal deletes itself. |

The two possible outcomes are:

- **Coffin:** creates `rag_coffin` and fills it with a random amount between `Coffin_MinItemsAmount` and `Coffin_MaxItemsAmount`. Each item is selected independently from `Coffin_Items`.
- **Ambush:** spawns a random amount between `Pedestal_MinSpawnableAIAmount` and `Pedestal_MaxSpawnableAIAmount`. Each class is selected independently from `Pedestal_SpawnableAI`.

The default coffin has a `10 x 100` cargo grid and cannot be moved into hands or cargo.

!!! important "The pedestal chance is reversed"
    `Pedestal_ChanceToSpawnCoffin` is used as a minimum roll: the coffin appears when an inclusive `0-100` roll is **greater than or equal to** the setting. Raising the value makes coffins less likely, not more likely. See [Chance behavior](server-configuration.md#chance-behavior).

## Static dragon

`Land_rag_static_dragon` is an animated decorative object intended for editor or admin-tool placement at traders, castles, and event areas.

It does not:

- fly or navigate;
- attack players;
- take part in the RaG Dragons encounter system;
- produce rewards;
- expose any Halloween JSON settings.
