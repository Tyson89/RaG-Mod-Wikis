# Key Classnames

The current source contains 355 public classes, including deployed forms, kits, color variants, and decorative objects. This page lists the operational classnames most server owners need. It is intentionally not a dump of every variant.

## Economy rule of thumb

Spawn or sell the `_kit` for large placeable objects. Use the final classname only for direct Workbench outputs, small inventory items, or when you deliberately want an already-deployed object. Classnames are case-sensitive.

## Workstations

| Item | Recommended inventory/economy classname | Related classname |
| --- | --- | --- |
| Workbench | `rag_baseitems_workbench_kit` | `rag_baseitems_workbench_blueprint` |
| Repair Station | `rag_baseitems_repair_station_kit` | `rag_baseitems_grindstone` |
| Weapon Cleaner | `rag_baseitems_weapon_cleaner_kit` | `rag_baseitems_weapon_solvent`, `rag_baseitems_cleaning_patches` |
| Ammo Cleaner | `rag_baseitems_ammo_cleaner` | Direct Workbench output; no kit in current source |
| Sewing Machine | `rag_baseitems_sewing_machine_kit` | `rag_baseitems_sewing_needle`, `rag_baseitems_sewing_thread`, `rag_baseitems_oil_bottle` |
| Table Saw | `rag_baseitems_table_saw_kit` | `rag_baseitems_sawblade` |
| Static Table Saw | `rag_baseitems_table_saw_static_kit` | Non-electric variant |
| Car Lift | `rag_baseitems_carlift_kit` | `rag_baseitems_notebook` |
| Static Car Lift | `rag_baseitems_carlift_static_kit` | Static variant |
| Smoker | `rag_baseitems_smoker_kit` | Powered/configured variant |
| Static Smoker | `rag_baseitems_smoker_static_kit` | Static variant |

## Power and utility

```text
rag_baseitems_solarpanel_kit
rag_baseitems_fridge_twodoor_old_kit
rag_baseitems_jd_fridge_kit
rag_baseitems_retro_fridge_kit
rag_baseitems_magpump_kit
rag_baseitems_beer_barrel_kit
rag_baseitems_beer_hop
rag_baseitems_trashcan_kit
rag_baseitems_trashcan_static_kit
rag_baseitems_doorbell_kit
rag_baseitems_control_unit
rag_baseitems_electric_wires
rag_baseitems_metal_sheet
rag_baseitems_plastic_sheet
```

## Coffee

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

Coffee mugs have multiple public color/design classnames. Add only the variants you actually want in the economy.

## Sleeping Bags

```text
rag_baseitems_sleepingbag_packed_ckeckered_blue
rag_baseitems_sleepingbag_packed_ckeckered_brown
rag_baseitems_sleepingbag_packed_ckeckered_green
rag_baseitems_sleepingbag_packed_ckeckered_grey
rag_baseitems_sleepingbag_packed_ckeckered_pink
rag_baseitems_sleepingbag_packed_ckeckered_red
rag_baseitems_sleepingbag_packed_rag_edition
```

`ckeckered` is the real source spelling.

## Christmas

```text
rag_baseitems_xmas_tree
rag_baseitems_xmas_stocking
rag_baseitems_xmas_lantern
rag_baseitems_xmas_calendar_kit
```

## Finding a decorative or storage variant

Storage and furniture are split across cabinets, chests, crates, drawers, fridges, gun walls, lockers, medical storage, safes, shelters, and wooden shelves. Decorative content is split across garden, plants, summer, wall pictures, Christmas, buildings, and `others`.

Do not guess a classname from its display name. Read the class declaration in the matching `config.cpp`, or copy the classname from a trusted admin tool, then verify that its class has `scope=2` before adding it to server files.
