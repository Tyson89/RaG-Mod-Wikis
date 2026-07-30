# Server setup, class names, and troubleshooting

## Required mod

[RaG Core](../core/index.md) is a hard dependency declared by root `Viking_Pack` addon in `CfgPatches.requiredAddons[]`. Install and enable both mods on server and every client. DayZ resolves addon/PBO ordering from declared dependencies; server mod-list order does not.

## Installation

1. Stop server.
2. Install original RaG Core and RaG Viking Pack Workshop releases.
3. Copy both signature keys into server `keys` directory if host does not handle that automatically.
4. Enable both mods for server and clients.
5. Start server once.
6. Stop after this file appears:

   ```text
   $profile:\RaG_Core\Configs\RaG_Viking_Pack\RaG_Viking_Pack.json
   ```

7. Edit generated file if needed, restart, and test item actions plus full kit placement/dismantling.

Use matching server/client builds. Source includes no Central Economy XML, trader file, or example JSON beyond generated RaG Core config.

## Economy rules

- Class names are case-sensitive.
- Add only classes server should distribute.
- Use `_kit` classes for shelter, table, firepit, sundial, and warbanner.
- Keep deployed placeable classes out of normal loot and traders unless bypassing kit flow is deliberate.
- Do not add internal base classes such as `rag_vikingpack_base_kit`, `rag_vikingpack_container_base`, or `rag_viking_coin_base`.
- Raven trigger and proxy classes are implementation details, not economy items.

Current source declares **63 public `CfgVehicles` classes**.

## Placeable classes

| Item | Recommended class | Deployed class |
| --- | --- | --- |
| Viking Shelter | `viking_shelter_kit` | `viking_shelter` |
| Viking Table | `rag_viking_table_kit` | `rag_viking_table` |
| Viking Firepit | `rag_viking_firepit_kit` | `rag_viking_firepit` |
| Viking Sundial | `rag_viking_sundial_kit` | `rag_viking_sundial` |
| Viking Warbanner | `rag_viking_warbanner_kit` | `rag_viking_warbanner` |

## Scripted and utility items

| Class | Display name or use |
| --- | --- |
| `rag_viking_lantern` | Viking Lantern |
| `rag_viking_raven` | Viking Raven |
| `rag_viking_horn` | Viking Horn |
| `rag_viking_idun` | Viking Idun rejuvenator |
| `rag_viking_drinkhorn` | Viking Drinking Horn |
| `rag_viking_mug` | Viking Mug |
| `rag_viking_pot` | Viking Pot |
| `rag_book` | Book of Ragnarok |

## Belt and storage

| Class | Display name or use |
| --- | --- |
| `rag_viking_belt` | Viking Belt |
| `rag_viking_pouch_1` | Small right Viking Pouch |
| `rag_viking_pouch_2` | Large right Viking Pouch |
| `rag_viking_pouch_3` | Large left Viking Pouch |
| `rag_viking_holster` | Viking Holster |
| `rag_coinbag` | Viking Coinbag |
| `rag_viking_leatherbag` | Viking retexture of leather sack backpack; display name is inherited |

## Coins

```text
rag_viking_coin_1
rag_viking_coin_5
rag_viking_coin_10
rag_viking_coin_25
rag_viking_coin_50
rag_viking_coin_100
rag_viking_coin_500
rag_viking_coin_1000
rag_viking_coin_10000
rag_coin
```

`rag_coin` displays as **RaG Coin (50k)** and stacks to `10`. Ancient Viking Coin classes stack to `5000`.

## Weapons and tools

| Class | Display name | Base class |
| --- | --- | --- |
| `rag_viking_axe` | Viking Axe | `WoodAxe` |
| `rag_viking_axe_doubled` | Double Bladed Viking Axe | `WoodAxe` |
| `rag_viking_cleaver_axe` | Viking Cleaver Axe | `WoodAxe` |
| `rag_viking_dragonslayer_axe` | Viking Dragonslayer Axe | `WoodAxe` |
| `rag_viking_dagger` | Viking Dagger | `Sword` |
| `rag_viking_flamberge_sword` | Viking Flamberge Sword | `Sword` |
| `rag_viking_sword` | Viking Sword | `Sword` |
| `rag_viking_halbert` | Viking Halbert | `Spear` |
| `rag_viking_spear` | Viking Spear | `Inventory_Base` |
| `rag_viking_mjolnir` | Mjolnir | `BaseballBat` |
| `rag_viking_hammer` | Viking Warhammer | `SledgeHammer` |
| `rag_viking_bb_hammer` | Viking Hammer | `Hammer` |
| `rag_viking_hatchet` | Viking Hatchet | `Hatchet` |
| `rag_viking_knife` | Viking Knife | `HuntingKnife` |
| `rag_viking_shield` | Viking Shield | `Inventory_Base` |

`rag_viking_halbert` is exact source spelling.

## Clothing and armor

```text
rag_viking_armwrist
rag_viking_boots
rag_viking_bracer
rag_viking_crown_mercia
rag_viking_helmet
rag_viking_helmet2
rag_viking_helmet3
rag_viking_helmet4
rag_viking_helmet5
rag_viking_leather_vest
rag_viking_leather_pants
rag_viking_leather_jacket
rag_viking_leather_gloves
```

All five helmet classes use same **Viking Helmet** display name. Use class suffix to select model.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Missing `RaGConfigVersioned`, `RaGConfigIO`, `RaGKitBase`, or other RaG Core symbols | RaG Core is missing, outdated, or mismatched. Install matching release on server and clients. |
| JSON does not generate | Confirm active server profile, folder permissions, RaG Core startup, and both required mods. Expected path is `$profile:\RaG_Core\Configs\RaG_Viking_Pack\RaG_Viking_Pack.json`. |
| Shelter recipe missing | Set `CanCraftShelterKit` to `1`, use at least three planks plus five sticks, validate JSON, and restart. |
| Kit places nothing | Confirm RaG Core loaded and server log has no `Could not spawn item!` error. Use exact kit class. |
| Placeable cannot be dismantled | Empty cargo and attachments, use non-ruined screwdriver, hammer, or pliers, and check territory permissions. |
| Table display slot missing | Table supports only slots declared in current config; notably no `rag_viking_helmet5`, coin, coinbag, spear, warhammer, or leather-clothing slots. |
| Raven gives no infected warning | Expected for base source. Only infected classes from another mod overriding `ZombieBase.IsSpecialThreat()` can trigger it. |
| Raven disappears | Each unfed warning removes `5` health. Attach any seed stack to `Ravenseed` slot. |
| Raven warning toggle unavailable while worn | Detach raven to hands, toggle warning mode, then reattach to armband. |
| **Add Lard** missing on fresh lantern | Source refreshes `m_CanReceiveUpgrade` only when attachment is detached. Attach rags, keep lantern off, detach rags once, then reattach them. |
| Other lantern recipe missing | Combine exact supported ingredient with `rag_viking_lantern`; lard still needs attached rags and enough unused energy capacity. |
| Lantern cannot enter cargo or release rags | Extinguish it first. Current source blocks both while energy manager is working. |
| Viking firepit will not ignite | Expected. It is static decoration, not fireplace. |
| Coin conversion loses value | Expected current source behavior for final `25 × rag_viking_coin_10000` conversion. |

## Safe update rules

- Stop server before editing JSON.
- Preserve `Version`.
- Use generated file as schema for installed build.
- Back up economy and trader changes before updates.
- Retest every scripted item after server/client mod update.
- Test kit placement and dismantling with normal player permissions.
