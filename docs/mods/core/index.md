# RaG Core Developer Wiki

RaG Core is the shared foundation for RaG mods and third-party integrations. This wiki documents the systems addon authors can build on: versioned configuration files, structured logging, custom liquids, reusable item classes, connection helpers, notifications, and shared effects.

If you only operate a server, see [Server configuration](server-configuration.md). The rest of this wiki is written for DayZ mod developers.

## Integration features

| Feature | Use it when you need | Documentation |
| --- | --- | --- |
| Dependency and script setup | Reliable load order for Game, World, and Mission scripts | [Getting started](getting-started.md) |
| Versioned JSON configuration | Per-mod files under the shared `RaG_Core/Configs` tree | [Configuration API](configuration-api.md) |
| Buffered per-mod logs | Separate channels, levels, rotation, and retention | [Logging API](logging-api.md) |
| Custom liquids | Drinkable liquids, fuels, coolants, groups, colors, and container rules | [Custom liquids](custom-liquids.md) |
| Reusable item classes | Deployable kits, openable containers, static objects, and placement hooks | [Item and placement API](item-and-placement-api.md) |
| One-time client data | Avoid sending the same configuration repeatedly during a connection | [Connection and RPC helpers](connection-and-rpc-helpers.md) |
| Shared UI and visual assets | Notification icons and registered particle effects | [Notifications and effects](notifications-and-effects.md) |

## Compatibility contract

The documented APIs above are the intended third-party integration surface. Keep your own class names, configuration module names, liquid slots, log channels, and RPC IDs unique.

The following are RaG-internal or reserved and should not be used as third-party extension points:

- `RaG_RPC` numeric IDs
- `RaG_ActivityLogger` channels
- `PluginRaG_BBSnap`, unless your addon explicitly integrates with RaG BaseBuilding
- protected implementation fields in the logger, liquid registry, or connection manager
- compile-time sections guarded by another RaG mod's define

Do not copy RaG Core classes into your addon. Declare `RaG_Core` and `RaG_Core_Scripts` as dependencies and compile against the installed mod.

## Recommended path

1. Add the dependency and script modules from [Getting started](getting-started.md).
2. Use [Configuration API](configuration-api.md) for server-owned settings.
3. Give your addon its own [logging channel](logging-api.md).
4. Add only the feature-specific integrations you need.
5. Test client and dedicated-server startup, persistence, reconnects, and load order before release.

## RaG mod documentation

- [RaG BaseBuilding](../basebuilding/index.md)
- [RaG Baseitems](../baseitems/index.md)
- [RaG Immersive Vehicles](../immersive-vehicles/index.md)
- [RaG Dragons](../dragons/index.md)
