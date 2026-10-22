# RaG Core Developer Wiki

RaG Core is the shared foundation for RaG mods and third-party integrations. It also extends DayZ's vanilla `DigitalCodeLock` with persistent access control, optional vanilla fence and tent support, and configurable raiding.

Server operators should start with [Server configuration](server-configuration.md) and [Vanilla DigitalCodeLock](vanilla-digital-codelock.md). Remaining API pages target DayZ mod developers.

## Integration features

| Feature | Use it when you need | Documentation |
| --- | --- | --- |
| Dependency and script setup | Reliable addon ordering through `requiredAddons[]` | [Getting started](getting-started.md) |
| Vanilla `DigitalCodeLock` | Ownership, remembered access, admin recovery, fences, tents, batteries, and raiding | [Vanilla DigitalCodeLock](vanilla-digital-codelock.md) |
| Versioned JSON configuration | Per-mod files under the shared `RaG_Core/Configs` tree | [Configuration API](configuration-api.md) |
| Buffered per-mod logs | Separate channels, levels, rotation, and retention | [Logging API](logging-api.md) |
| Custom liquids | Drinkable liquids, fuels, coolants, groups, colors, and container rules | [Custom liquids](custom-liquids.md) |
| Reusable item classes | Deployable kits, openable containers, static objects, and placement hooks | [Item and placement API](item-and-placement-api.md) |
| RPC validation and one-time client data | Register RPC metadata, validate receives, and avoid duplicate initial sends | [Connection and RPC helpers](connection-and-rpc-helpers.md) |
| Shared utilities | Atomic persistence, identities, inventory snapshots, pagination, and request replay protection | [Shared utilities](shared-utilities.md) |
| Shared UI and visual assets | Notification icons and registered particle effects | [Notifications and effects](notifications-and-effects.md) |

## Compatibility contract

The documented APIs above are the intended third-party integration surface. Keep your own class names, configuration module names, liquid slots, log channels, and RPC IDs unique.

The following are RaG-internal or reserved and should not be used as third-party extension points:

- `RaG_RPC` numeric IDs
- `RaG_ActivityLogger` channels
- `PluginRaG_BBSnap`, unless your addon explicitly integrates with RaG BaseBuilding
- protected implementation fields in the logger, liquid registry, RPC service, or connection manager
- compile-time sections guarded by another RaG mod's define

Do not copy RaG Core classes into your addon. Declare `RaG_Core` and `RaG_Core_Scripts` as dependencies and compile against the installed mod.

## Recommended path

1. Add the dependency and script modules from [Getting started](getting-started.md).
2. Use [Configuration API](configuration-api.md) for server-owned settings.
3. Give your addon its own [logging channel](logging-api.md).
4. Add only the feature-specific integrations you need.
5. Test client and dedicated-server startup, persistence, reconnects, and dependency resolution before release.

## RaG mod documentation

- [RaG BaseBuilding](../basebuilding/index.md)
- [RaG Baseitems](../baseitems/index.md)
- [RaG Immersive Vehicles](../immersive-vehicles/index.md)
- [RaG Dragons](../dragons/index.md)
- [RaG Thunderstruck](../thunderstruck/index.md)
- [RaG Infected Hordes](../infected-hordes/index.md)

!!! warning "No monetization, repacking, or reuploading"
    RaG Core may be used on an approved monetized server, but the mod itself may not be monetized, repacked, or reuploaded. Use the original Workshop release.
