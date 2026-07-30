# Gameplay, equipment, and placeables

## Viking Shelter

Combine:

- `3` wooden planks;
- `5` wooden sticks.

Choose **Craft Viking Shelter**. The recipe removes those quantities and creates `viking_shelter_kit` on the ground. `CanCraftShelterKit` controls only this recipe; it does not block existing, spawned, traded, or scripted kits.

Deploy the kit through normal placement controls. RaG Core removes the `_kit` suffix and creates `viking_shelter`.

The completed shelter:

- provides `10 × 50` cargo;
- is always logically open;
- exposes inventory only when standing near the center inside;
- has no open or close action;
- cannot be placed into hands or cargo.

To dismantle it, empty all cargo and use a non-ruined screwdriver, hammer, or pliers. RaG Core uses the normal deconstruction duration, removes `5` tool health, deletes the shelter, and creates `viking_shelter_kit` at the player's position.

`DisableDamageForPlaceables` controls shelter damage. Despite its broad name, current Viking Pack source checks it only in `viking_shelter`.

## Other placeables

| Kit | Deployed class | Actual use |
| --- | --- | --- |
| `rag_viking_firepit_kit` | `rag_viking_firepit` | Use as any Vanilla Fireplace. Create a Fireplace inside by attaching a Firewood. |
| `rag_viking_table_kit` | `rag_viking_table` | Display table with dedicated attachment slots for Viking equipment. It has no general cargo grid. |
| `rag_viking_sundial_kit` | `rag_viking_sundial` | Decorative sundial. No script calculates or displays time, but it can show the approximate time using game rendered shadows. |
| `rag_viking_warbanner_kit` | `rag_viking_warbanner` | Decorative warbanner. |

RaG Core handles deployment and dismantling for these objects. Empty object first, then use screwdriver, hammer, or pliers. Table attachments must therefore be removed before dismantling.

The JSON damage toggle does not control these four objects. Their own `config.cpp` damage definitions remain authoritative.

## Viking Lantern

`rag_viking_lantern` uses an energy manager and an attached `Rag` stack.

### Add rags

Combine a rag with lantern and choose **Refuel Viking Lantern**. Recipe attaches rag or combines it with existing attached stack. It does not add liquid fuel.

Each consumed rag adds `480` seconds of burn energy. Lantern internal energy storage holds `1800` seconds. Quantity bar represents combined stored energy and attached-rag reserve.

### Add lard

Combine lard with lantern and choose **Add Lard**.

- Lantern must have attached rags.
- If lantern is off, attached stack must contain more than one rag.
- If lantern is lit, one attached rag is enough.
- Recipe consumes one attached rag.
- Up to `200` lard quantity can be consumed.
- A full `200`-quantity lard dose adds `900` seconds, limited by remaining internal energy capacity.

### Light and extinguish

Use normal **Light** action with a valid igniter. While lit:

- light radius is configured to `35`;
- lantern cannot be moved into cargo;
- attached rag cannot be released;
- energy drains at one unit per second;
- low reserve fades brightness and radius.

Extinguishing through recipe requires lantern plus at least `100` liquid quantity in one of these container classes:

```text
Pot
CanisterGasoline
DisinfectantAlcohol
Canteen
WaterBottle
Vodka
WaterPouch_ColorBase
Barrel_ColorBase
```

Container's actual liquid must be blood, clean water, river water, or beer. Recipe consumes `100` liquid before soft-skill adjustment, switches lantern off, and sets it to maximum wetness.

## Viking Raven

`rag_viking_raven` occupies armband slot and accepts any `SeedBase` item in its slot.

Use raven in hands to enable or disable warnings, then attach it to armband. Warning mode persists across restarts.

When enabled, server creates a 300-meter trigger around wearer. Warning fires when a creature enters and is either:

- an `AnimalBase` for which `IsDanger()` returns true; or
- a `ZombieBase` for which `IsSpecialThreat()` returns true.

Base Viking Pack implementation returns `false` for every infected. Vanilla infected therefore do not trigger warnings unless another mod overrides `IsSpecialThreat()`.

Each warning:

- plays raven sound on wearer;
- consumes one attached seed when available;
- otherwise removes `5` raven health;
- deletes raven when health reaches destroyed state.

Warning is an entry event, not a continuous proximity alarm. Raven sound shader has a `20`-meter range.

## Viking Horn

Hold `rag_viking_horn` and use **Blow Horn**.

- Action runs for five seconds.
- Sound is synchronized to nearby clients.
- Server adds `shot`-type noise with configured strength `1000` and script multiplier `2.0`.

Horn is not cosmetic silence: noise system can attract AI.

## Viking Idun

`rag_viking_idun` can be used on self or another player. Completed action:

- adds `50` global health, capped by normal health maximum;
- sets stamina to `100`;
- removes all disease agents;
- deletes rejuvenator.

No cooldown or partial-use state exists. Item is consumed once action finishes.

## Coins and coinbag

All Ancient Viking Coin classes stack to `5000`. Dedicated `rag_coinbag` has one attachment slot for each Ancient Viking Coin denomination from `1` through `10000`; it has no cargo grid and does not accept `rag_coin`.

Conversion actions take three seconds and spawn result on ground:

| Input | Quantity consumed | Result |
| --- | ---: | --- |
| `rag_viking_coin_100` | `10` | `rag_viking_coin_1000` |
| `rag_viking_coin_100` | `100` | `rag_viking_coin_10000` |
| `rag_viking_coin_500` | `2` | `rag_viking_coin_1000` |
| `rag_viking_coin_500` | `20` | `rag_viking_coin_10000` |
| `rag_viking_coin_1000` | `10` | `rag_viking_coin_10000` |
| `rag_viking_coin_10000` | `25` | `rag_coin` |

Denominations `1`, `5`, `10`, `25`, and `50` have no built-in conversion actions.

## Containers and wearable storage

| Item | Capacity or behavior |
| --- | --- |
| Viking Drinking Horn | Canteen-derived liquid container, maximum `1500`. |
| Viking Mug | Canteen-derived liquid container, maximum `2000`; shows beer visual only when liquid type is beer and quantity is above zero. |
| Viking Pot | Pot-derived container, maximum `3000` liquid and `6 × 5` cargo. |
| Viking Belt | Worn in hips slot; accepts three pouches, holster, Viking Horn, Drinking Horn, and Coinbag. |
| Small right pouch | `4 × 3` cargo. |
| Large right pouch | `6 × 4` cargo. |
| Large left pouch | `6 × 4` cargo. |
| Viking Holster | Accepts Viking Knife in dedicated `rag_knife` slot. |
| Viking leather backpack | `10 × 12` cargo plus many equipment attachment slots. |

Pouches refuse being placed into belt's cargo, preventing attachment storage from nesting inside parent belt.

## Weapons and defensive equipment

Pack contains axes, swords, dagger, spear, halbert, hammers, Mjolnir, hatchet, knife, and shield. Several use custom melee ammo with custom health, blood, shock, range, and animal multipliers.

Viking Dagger, Viking Sword, and Viking Flamberge Sword are scripted as melee finishers and expose bush-mining, skinning, self-shaving, and target-shaving actions.

Two similar hammer names matter:

| Class | Display name | Base behavior |
| --- | --- | --- |
| `rag_viking_bb_hammer` | Viking Hammer | `Hammer`; intended for construction tasks. |
| `rag_viking_hammer` | Viking Warhammer | `SledgeHammer`; custom melee weapon. |

See [server class-name reference](server-setup-and-class-names.md) before adding equipment to economy or traders.
