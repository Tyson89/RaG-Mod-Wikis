# Workbench

![RaG Baseitems Workbench](https://i.postimg.cc/sxHF2xvV/workbench.png)

Deploy the Workbench from `rag_baseitems_workbench_kit`. Crafting requires:

- `rag_baseitems_workbench_blueprint` attached;
- a non-ruined hammer in the player's hands;
- the exact materials attached to the Workbench; and
- the recipe enabled in [Server Configuration](json-file-explanation.md).

Aim at the `wbcraft` interaction point. The result preview appears before the 15-second craft starts. Every completed craft removes 10 hammer health.

## Material thresholds

These quantities are hard-coded by the current Workbench source:

| Material tier | Minimum | Medium | Maximum |
| --- | ---: | ---: | ---: |
| Small plastic sheets | 10 | 50 | 100 |
| Small metal sheets | 10 | 50 | 100 |
| Nails | 20 | 50 | 100 |
| Wooden planks | 10 | 25 | 50 |

Other fixed requirements are 4 shelter-fabric/tarp quantity, 32 large stones, or 350 plant-crop quantity where listed.

## Recipes

### Plastic and metal items

| Config identifier | Result | Requirements |
| --- | --- | --- |
| `Flamingo` | Flamingo | 50 plastic sheets |
| `FishingBox` | Fishing tackle box | 50 plastic sheets |
| `BeachBall` | Beach ball | 50 plastic sheets |
| `VolleyBall` | Volleyball | 50 plastic sheets |
| `AmmoCleaner` | Ammo Cleaner | 50 plastic sheets + 50 metal sheets |
| `MetalAmmoBox` | Metal ammo box | 50 metal sheets |
| `MetalAmmoBoxBlack` | Black metal ammo box | 50 metal sheets |
| `MetalAmmoBoxGreen` | Green metal ammo box | 50 metal sheets |
| `FirewoodHolder` | Firewood holder kit | 100 metal sheets |
| `WateringCan` | Watering can | 50 metal sheets |
| `DoorBell` | Doorbell kit | 10 metal sheets |

### Crates and storage

| Config identifier | Result | Requirements |
| --- | --- | --- |
| `GrenadeCrate` | Grenade crate | 10 metal sheets + 10 planks + 20 nails |
| `PistolAmmoCrate` | Pistol-ammo crate | 10 metal sheets + 10 planks + 20 nails |
| `SmallGunCrate` | Small gun crate | 10 metal sheets + 10 planks + 20 nails |
| `SmokeGrenadeCrate` | Smoke-grenade crate | 10 metal sheets + 10 planks + 20 nails |
| `LargeRifleCrate` | Large rifle crate | 10 metal sheets + 25 planks + 50 nails |
| `LargeShotgunCrate` | Large shotgun crate | 10 metal sheets + 25 planks + 50 nails |
| `RifleAmmoCrate` | Rifle-ammo crate | 10 metal sheets + 25 planks + 50 nails |
| `ShotgunAmmoCrate` | Shotgun-ammo crate | 10 metal sheets + 25 planks + 50 nails |
| `WellsFargoCrate` | Wells Fargo crate | 10 metal sheets + 25 planks + 50 nails |
| `LargeSlideCrate` | Large slide crate | 10 metal sheets + 25 planks + 50 nails |
| `MilitaryCrate` | Military crate | 10 metal sheets + 25 planks + 50 nails |
| `WaterBarrel` | Water barrel | 10 metal sheets + 25 planks + 50 nails |

### Construction and decoration

| Config identifier | Result | Requirements |
| --- | --- | --- |
| `BarrelFurnace` | Barrel furnace kit | 100 metal sheets + 10 planks + 50 nails |
| `TrashCan` | Trash Can kit | 10 planks + 20 nails |
| `WallPicture` | Unpainted wall picture | 10 planks + 20 nails |
| `Plants` | One of six decorative plants | Plant seed pack + 350 crop quantity |
| `GrindStone` | Grindstone | 32 large stones |
| `Carpet` | Simple rectangular carpet | 4 shelter-fabric/tarp quantity |

The plant recipe deletes both the seed pack and crop item. Select the preview for the plant variant you want before crafting.

### Electrical items

The electronics slot accepts `rag_baseitems_control_unit` or `rag_baseitems_electric_wires`.

| Config identifier | Result | Requirements |
| --- | --- | --- |
| `CableReel` | Cable Reel | 10 plastic sheets + one electronics item |
| `SpotLight` | Spotlight | 10 plastic sheets + one electronics item + one headlight bulb |
| `BatteryCharger` | Battery Charger | 10 metal sheets + one electronics item |

Electronics and headlight attachments are consumed.

## Standalone material recipes

These are ordinary inventory-combine recipes, not Workbench actions:

| Result | Ingredients | Output/tool cost |
| --- | --- | --- |
| Small metal sheets | Metal Plate + Hacksaw or Hand Saw | 60 sheet quantity; saw loses 30 health |
| Small plastic sheets | Pliers + supported plastic item | 10 sheet quantity; plastic item is destroyed; pliers lose 5 health |
| Coffee cup | Paper + small plastic sheet | Paper is destroyed; one plastic-sheet quantity is consumed |
| Legless vintage TV kit | Vintage TV + Hacksaw or Hand Saw | TV is replaced; saw loses 10 health |

The matching `EnableCraft...` settings can disable these recipes.

## Painting wall art

![Painting and cleaning a wall painting](https://i.postimg.cc/6qPRtsx8/paint.png)

Unpainted wall pictures support several spray-paint designs and a cleaning action. Carpets likewise support multiple spray patterns. These actions change the placed object's visual variant; they are separate from Workbench crafting.
