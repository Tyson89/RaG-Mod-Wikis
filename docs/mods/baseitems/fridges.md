# Fridges

RaG Baseitems provides three powered fridges. They keep food and drinks cold and make perishable food last much longer.

## How to use a fridge

1. Deploy the fridge from its kit.
2. Connect it to a power source.
3. Store supported food or drinks inside.
4. Close the doors to start cooling.

Fridges switch themselves on when connected to working power. They use **0.14 energy per second** and can be powered by compatible sources such as the [Solar Panel](solar-panel.md).

## Cooling and food decay

While powered and closed, a fridge:

- keeps its contents near **4 °C**;
- slows normal DayZ food decay to **15%** of its usual rate;
- gives perishable food roughly **6.7 times longer** before it spoils.

Fridges use the server's vanilla `FoodDecay` value from `globals.xml` as the starting rate. They reduce that rate by 85% while cooling instead of replacing the server setting.

Opening the doors or losing power stops both cooling and the fridge's decay reduction. Closing the doors restores the benefit while power is available.

Each model has a large **10 x 50 inventory grid**. It accepts non-ruined soda cans, bottles, and edible items that support temperature. Other items cannot be stored inside.

All three models work the same and accept a Codelock. See [Codelock Integration](codelock-integration.md).

## Key classnames

| Fridge | Kit classname | Deployed classname |
| --- | --- | --- |
| Old Fridge | `rag_baseitems_fridge_twodoor_old_kit` | `rag_baseitems_fridge_twodoor_old` |
| Jack Daniel's Fridge | `rag_baseitems_jd_fridge_kit` | `rag_baseitems_jd_fridge` |
| Retro Fridge | `rag_baseitems_retro_fridge_kit` | `rag_baseitems_retro_fridge` |

Use kit classnames in the economy or traders. Deployed classnames are the placed objects.
