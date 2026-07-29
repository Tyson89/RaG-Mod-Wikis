# Setup, class names, and troubleshooting

## Required mod and load order

[RaG Core](../core/index.md) is required on the server and every client. Load Core first:

```text
@RaG_Core;@RaG_ChickenCoop
```

Actual folder names may differ. Dependency order must not.

## Installation

1. Stop the server.
2. Install the original RaG Core and RaG ChickenCoop Workshop releases.
3. Copy both signature keys into the server's `keys` directory if the host does not do that automatically.
4. Add both mods to the client/server mod parameter, with Core first.
5. Start the server once.
6. Stop it after this file appears:

   ```text
   $profile:\RaG_Core\Configs\RaG_ChickenCoop\RaG_ChickenCoop.json
   ```

7. Edit the generated file, restart, and test a known `Land_misc_chickenCoop`.

The generated file is the schema for the installed build. Preserve a backup during updates and merge custom values into a newly generated schema when fields change.

## Supported coop object

The interaction is attached to this exact world-object class:

```text
Land_misc_chickenCoop
```

That vanilla class is used by chicken-coop objects on official maps and may be reused by community maps. A third-party coop with a different class name is not supported merely because its model looks identical.

`Land_misc_chickenCoop` is a static map object. Do not add it to `types.xml`, traders, or inventory loot.

## Public class names

| Class name | Type | Use |
| --- | --- | --- |
| `rag_egg` | Inventory food | Raw unpeeled egg; cookable and peelable after boiling. |
| `rag_egg_peeled` | Inventory food | Peeled edible egg created by the **Peel** action. |
| `rag_chocolate_bunny` | Inventory food | Non-decaying seasonal food and default coop reward. |
| `rag_gingerbread` | Inventory food | Non-decaying seasonal food and default coop reward. |
| `rag_crazychicken` | Animal AI | Hostile chicken used by the independent ambush roll. |
| `Land_misc_chickenCoop` | Static world object | Vanilla coop class extended with the search action. |

`ChickenTrigger` is an implementation detail attached to a spawned crazy chicken. Do not distribute or place it.

## Economy and placement

The source project ships no official Central Economy XML values.

- No XML entry is needed to make existing supported map coops searchable.
- Coop rewards are created directly by script.
- The four public food classes may be distributed separately through `types.xml`, traders, quests, or rewards if wanted.
- `rag_crazychicken` is designed for the coop ambush. Direct event or admin spawning is possible, but test cleanup and AI load under your server's system.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Server reports missing `RaG_Core` classes or scripts | Core is missing, outdated, or loaded after ChickenCoop. Install matching versions on server and clients, then load Core first. |
| JSON does not generate | Confirm the active server profile, folder permissions, RaG Core startup, and load order. Expected path is `$profile:\RaG_Core\Configs\RaG_ChickenCoop\RaG_ChickenCoop.json`. |
| Coop has no search action | Verify exact object class `Land_misc_chickenCoop`, matching client/server mod versions, and normal action distance. Similar-looking custom coop classes are unsupported. |
| Coop reports it was looted | One completed search consumes that object until it initializes again, normally during a later server startup. |
| Search produces nothing | This is common: default reward failure is 59%. Including the independent chicken roll, default chance of no item and no chicken is 52.51%. |
| Search produces both an item and a chicken | Expected. Reward and chicken use separate rolls. |
| Raising `ChanceToGetFeathers` produces fewer feathers | Expected current behavior. Field name is misleading; higher values favor `ChickenCoopItems`. |
| Config changes seem ten times too strong | Do not use the obsolete `0-10` Workshop scale. Current source defaults are `40`, `50`, and `10` against `0-99` rolls. |
| Reward fails or logs script errors | Keep both arrays non-empty and validate every class name. Load every mod supplying a configured custom class on server and clients. |
| Raw egg has no **Peel** action | Boil it first. Only a boiled `rag_egg` can be peeled. |
| Egg becomes burned when baked or dried | Expected current script behavior. Boiling is the intended route. |
| Crazy chicken gives no skinning action or materials | Expected. `CanBeSkinned()` returns false and configured skinning counts are zero. |

## Safe configuration rules

- Stop the server before editing JSON.
- Keep valid JSON and retain `Version`.
- Keep `ChickenCoopItems` and `ChickenFeathers` non-empty.
- Use valid classes present on server and clients.
- Treat `ChanceToGetItems` and `ChanceToSpawnCrazyChicken` as `0-99` thresholds.
- Treat `ChanceToGetFeathers` as the normal-item share, despite its name.
- Restart after changes; configuration loads during server initialization.
