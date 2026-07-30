# Setup, spawning, class names, and troubleshooting

## Required mod

[RaG Core](../core/index.md) is required on the server and every client. Install and enable both mods. Dependency metadata controls addon/PBO ordering; server mod-list order does not.

## Installation

1. Stop the server.
2. Install the original RaG Core and RaG Evil Snowman Workshop releases.
3. Copy both signature keys into the server's `keys` directory if the host does not do that automatically.
4. Add both mods to the client/server mod set.
5. Start the server once.
6. Stop it after this file appears:

   ```text
   $profile:\RaG_Core\Configs\RaG_SnowMan\RaG_SnowMan.json
   ```

7. Edit the generated file if needed.
8. Configure a spawn method for `rag_snowman`, then restart and test.

The generated file is the schema for the installed build. Preserve a backup during updates and merge custom values into a newly generated schema when fields change.

## Spawning

Current source does not automatically spawn Snowmen and contains no official Central Economy XML examples. Installing the mod alone adds the classes but does not guarantee a Snowman encounter.

Use one tested server-side method to create `rag_snowman`, such as:

- a correctly configured animal event and matching spawn or territory data;
- an admin or event framework;
- a custom mission script.

`rag_snowman` is animal AI, not inventory loot. Adding only that class to `types.xml` does not create working predator spawns.

For Central Economy events, start from files matching the active map and DayZ version. Snowman uses a bear predator template, but blindly renaming a bear event is unsafe: event limits, child entries, spawn positions, territories, and map environment data must agree.

## Public class names

| Class name | Type | Use |
| --- | --- | --- |
| `rag_snowman` | Animal AI | Hostile Evil Snowman encounter and skinning target. |
| `rag_carrot` | Inventory food | Non-decaying, non-cookable custom carrot and default skinning reward. |

`rag_snowmanLight` is a scripted client-side light helper. Do not add it to economy, trader, or spawn files.

## Economy and distribution

Current source ships no `types.xml`, `events.xml`, `cfgeventspawns.xml`, `cfgenvironment.xml`, or territory files.

- Snowman reward items are created directly after skinning.
- `rag_carrot` needs no `types.xml` entry when used only as a skinning reward.
- Add `rag_carrot` to economy, traders, quests, or other systems only when separate distribution is wanted.
- Configure Snowman AI spawning through a supported animal/event method, not inventory loot economy.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Server reports missing `RaGConfigVersioned`, `RaGConfigIO`, `RaGConfigAPI`, or `RaG_CoreLogger` | RaG Core is missing, outdated, or mismatched between server and clients. Install matching versions. |
| JSON does not generate | Confirm the active server profile, folder permissions, RaG Core startup, and that both required mods are enabled. Expected path is `$profile:\RaG_Core\Configs\RaG_SnowMan\RaG_SnowMan.json`. |
| Editing old `RaG_Snowman\RaG_SnowMan.json` changes nothing | Expected on current source. Edit the RaG Core path instead. |
| No Snowmen appear | Mod has no automatic spawner or current source XML. Configure `rag_snowman` through a valid animal event, territory setup, event framework, or mission script. |
| Snowman exists but has no custom light | Light is client-side and hidden during daylight. Also verify matching client/server mod versions. |
| Skinning creates fewer items than configured | Validate every reward class. Failed classes are skipped and logged through RaG Core. |
| Skinning creates duplicate items | Expected. Each attempt independently selects from the array. |
| Skinning errors after reward array was emptied | Restore at least one valid entry. To disable rewards, set `SkinnedItemsAmount` to `0`. |
| Custom reward class fails | Confirm exact class spelling, that it inherits `ItemBase`, and that its supplying mod is loaded where required. |
| Snowman drops no meat, pelt, bones, guts, or lard | Expected. Vanilla animal skinning yields are configured with empty classes and zero counts. |
| Snowman attacks like a bear | Expected. It uses bear AI, animations, movement, and damage event profiles. |

## Safe configuration rules

- Stop server before editing JSON.
- Keep valid JSON and retain `Version`.
- Keep `SnowManSkinningItems` non-empty.
- Use valid `ItemBase` classes.
- Use `SkinnedItemsAmount: 0` to disable drops.
- Avoid excessive reward counts.
- Restart after changes; configuration registers during server initialization.
