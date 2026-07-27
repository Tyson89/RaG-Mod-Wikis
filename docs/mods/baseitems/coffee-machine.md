# Coffee System

The coffee system consists of a Coffee Machine, Grinder, Hutch, Coffee Jar, Portafilter, bean packs, cups, mugs, and a thermos.

## Setup

1. Deploy the Coffee Machine, Grinder, and Hutch from their kits.
2. Connect the Coffee Machine and Grinder to compatible power.
3. Fill the Coffee Machine with water. Capacity is **2,000 ml**.

## Grind and brew

1. Fill the Grinder with coffee beans and start it.
2. Transfer the ground coffee from the open drawer to the Coffee Jar.
3. Combine the Coffee Jar with an empty Portafilter. This consumes 50 ground-coffee quantity.
4. Attach the filled Portafilter to the coffee or espresso position.
5. Attach an empty compatible mug below it.
6. Start brewing and wait 18 seconds.

Each brew consumes **250 ml of water** and empties the Portafilter. The selected position determines whether the mug receives coffee or espresso.

## Cups and effects

- The disposable coffee cup holds 250 ml.
- Craft one from Paper and a small plastic sheet when `EnableCraftCoffeeCup` is enabled.
- Throwing a filled mug empties it.
- Coffee stamina behavior is controlled by `EnableCoffeeStaminaBoost`.
- Coffee and espresso liquid definitions come from required [RaG Core](../core/index.md); no separate Liquid Framework is needed.

## Key classnames

```text
rag_baseitems_coffee_machine_kit
rag_baseitems_coffee_grinder_kit
rag_baseitems_coffee_hutch_kit
rag_baseitems_coffee_jar
rag_baseitems_coffee_pack
rag_baseitems_portafilter
rag_baseitems_coffee_cup
rag_baseitems_coffee_thermos
```

[Watch the Coffee Machine showcase](https://www.youtube.com/watch?v=ysrej_wwv3c)
