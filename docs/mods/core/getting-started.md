# Getting Started

Treat RaG Core as a hard client-and-server dependency when an addon uses any documented API. Declare the dependency in `CfgPatches.requiredAddons[]`; DayZ uses it to resolve addon/PBO ordering.

## Required config dependencies

Add both patch names to your addon that consumes RaG Core:

```cpp
class CfgPatches
{
    class MyMod_Scripts
    {
        units[] = {};
        weapons[] = {};
        requiredVersion = 0.1;
        requiredAddons[] =
        {
            "RaG_Core",
            "RaG_Core_Scripts"
        };
    };
};
```

`RaG_Core` contains the main config and shared assets. The `RaG_Core_Scripts` dependency guarantees Core script-side definitions resolve before the consuming addon.

## Script modules

If your addon uses all three DayZ script layers, define them normally:

```cpp
class CfgMods
{
    class MyMod
    {
        type = "mod";
        dependencies[] = {"Game", "World", "Mission"};

        class defs
        {
            class gameScriptModule
            {
                value = "";
                files[] = {"MyMod/scripts/3_Game"};
            };
            class worldScriptModule
            {
                value = "";
                files[] = {"MyMod/scripts/4_World"};
            };
            class missionScriptModule
            {
                value = "";
                files[] = {"MyMod/scripts/5_Mission"};
            };
        };
    };
};
```

RaG Core exposes the `RAG_CORE` compile define. It is useful only for an optional integration:

```c
#ifdef RAG_CORE
    // Optional RaG Core integration.
#endif
```

If your addon cannot function without Core, use the hard `requiredAddons[]` dependency and do not hide missing dependencies behind a compile guard.

## Runtime dependency resolution

Install and enable RaG Core and the consuming addon on the server and clients. Do not use the server `-mod` sequence as an ordering mechanism. DayZ resolves PBO/addon order from `requiredAddons[]`. Declare only dependencies the addon actually requires.

## Which layer contains each API?

| Script layer | Main integration points |
| --- | --- |
| `3_Game` | `RaGConfigVersioned`, `RaGConfigAPI`, `RaGCoreFS`, `RaG_CoreLogger`, constants, liquid type helpers, notification paths |
| `4_World` | `LiquidFrameworkRegistry`, `RaGKitBase`, container bases, placement hooks, actions, particle use |
| `5_Mission` | `ConnectionManager`, Core manager startup, the `MissionServer.SendModData` extension point |

## First integration test

Before adding gameplay code:

1. Start a dedicated server with Core and the addon enabled.
2. Confirm there are no missing patch, unknown class, or script compile errors.
3. Register one test configuration with the [Configuration API](configuration-api.md).
4. Confirm the JSON appears under `$profile:\RaG_Core\Configs\<module>\`.
5. Connect a client and verify that both sides load the same addon version.

## Naming rules

Use a stable, unique prefix for every public identifier your addon owns:

- CfgPatches classes
- script classes
- config module and file names
- log modules and levels
- custom-liquid classes, groups, and slots
- RPC enum values

RaG Core does not provide a global registry for third-party names or RPC numbers. Collision avoidance remains the addon author's responsibility.
