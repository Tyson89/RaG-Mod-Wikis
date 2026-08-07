# Fridges

RaG Baseitems provides three powered fridges. All three use the same cooling, storage, power, and Codelock behavior.

## Setup

1. Deploy the fridge from its `_kit` classname.
2. Put supported food or drink in its cargo.
3. Close the fridge doors.
4. Plug the 15 m power cord into a compatible power source. The fridge switches itself on when power becomes available.

The fridges use plug type `2` and consume **0.14 energy per second**. The [Solar Panel](solar-panel.md) can power compatible devices.

## Cooling and storage

- Each fridge has **10 x 50 cargo slots**.
- Cargo is cooled to **4 °C** while the fridge is powered and closed.
- The cooling check runs every **5 seconds**. Items already between 3.5 °C and 4.5 °C are left unchanged.
- Opening the fridge stops cooling, even when power remains connected. Closing it resumes cooling.
- Losing or disconnecting power stops the fridge. It switches itself on when connected to an active power source and after a server restart when its stored connection has power.
- Cargo accepts non-ruined, temperature-capable soda cans, bottles, and edible items. Other item types are rejected.

Cooling sets item temperature; it does not run a separate custom food-decay timer.

All three fridges accept a Codelock. See [Codelock Integration](codelock-integration.md).

## Key classnames

| Fridge | Kit classname | Deployed classname |
| --- | --- | --- |
| Old Fridge | `rag_baseitems_fridge_twodoor_old_kit` | `rag_baseitems_fridge_twodoor_old` |
| Jack Daniel's Fridge | `rag_baseitems_jd_fridge_kit` | `rag_baseitems_jd_fridge` |
| Retro Fridge | `rag_baseitems_retro_fridge_kit` | `rag_baseitems_retro_fridge` |

Use kit classnames in the economy or traders. Deployed classnames are the placed objects.
