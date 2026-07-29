# Searching, food, and the crazy chicken

## Searching a chicken coop

The mod targets the exact vanilla world-object class `Land_misc_chickenCoop`. About half a second after one initializes on the server, it becomes searchable.

To search:

1. Stand or crouch within normal interaction range.
2. Aim at the coop.
3. Hold the search action for the default crafting duration.

No tool or held item is required.

After completion, the coop is marked looted. Its search action may remain visible, but another attempt stops and reports:

```text
This Chicken Coop appears to be looted already...
```

Search state is synchronized but not persisted. A coop normally becomes searchable again when the world object initializes during a later server startup.

## Search outcomes

Completion makes two independent rolls:

1. **Reward roll:** decides whether anything from the two configured reward arrays appears.
2. **Crazy-chicken roll:** separately decides whether `rag_crazychicken` appears.

This independence matters. One search can produce:

- a normal configured item;
- a configured feather item;
- no reward;
- any of those three results plus a crazy chicken.

With defaults:

| Result | Chance per completed search |
| --- | ---: |
| One entry from `ChickenCoopItems` | 20.5% |
| One entry from `ChickenFeathers` | 20.5% |
| No item or feather | 59% |
| Crazy chicken, independent of reward | 11% |
| Nothing at all: no reward and no chicken | 52.51% |

Rewards are created at the player's world position and placed on the surface. The crazy chicken appears 2.5 meters behind the player.

See [Server configuration](server-configuration.md) before changing chances. Two setting names do not behave as most admins will assume.

## Eggs

### Unpeeled egg

`rag_egg`:

- starts raw with quantity `125`;
- can be cooked, but not on a stick;
- does not decay;
- becomes peelable only in the boiled food stage;
- treats baked and dried states as burned in the current scripts.

Boiling is the intended preparation route. Put a boiled egg in the player's hands and use **Peel** to replace it with `rag_egg_peeled`.

### Peeled egg

`rag_egg_peeled`:

- cannot be cooked again;
- cannot be peeled again;
- does not decay;
- is directly edible.

## Gingerbread and chocolate bunny

`rag_gingerbread` and `rag_chocolate_bunny` are directly edible and do not decay. Both start with quantity `150` and define `200` energy with no water.

They are normal public inventory classes. Server owners may also distribute them through the Central Economy, traders, quests, or reward systems.

## Crazy chicken

`rag_crazychicken` is not a normal passive DayZ chicken:

- it uses an infected-pack behavior template and treats players as targets;
- it has `200` global health;
- its enraged movement allows speeds up to `8`;
- it cannot be skinned, and its configured skinning yields are zero;
- it has a one-meter attached trigger that affects conscious players at close range.

The close-range trigger checks every three seconds. Its internal cooldown is greater than five seconds, so a player who stays inside the trigger can lose `50` shock and receive the light-pain symptom about once every six seconds. The trigger deletes itself after the chicken dies.

Kill or evade it. Do not expect meat, feathers, guts, or bones from skinning.
