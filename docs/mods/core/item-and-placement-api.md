# Item and Placement API

RaG Core provides reusable bases for common placeable objects. Use the narrowest class that matches the object's actual behavior.

## Base-class selection

| Script class | Intended use | Main behavior |
| --- | --- | --- |
| `RaGKitBase` | A deployable kit that creates another item | Placement actions, output spawning, optional health transfer, post-placement hook |
| `RaG_ContainerBase` | A fixed, openable storage object | Persistent synchronized open state, door sounds, inventory visibility, open/close actions |
| `RaG_PlaceableBase` | A movable deployable container | Container behavior plus placement and pickup rules |
| `RaG_StaticBase` | A permanently placed object without usable inventory | Cannot enter hands/cargo, cannot receive cargo or attachments, always reports open |

The matching config base classes have the same names.

## Minimal kit and container

Config definitions:

```cpp
class CfgVehicles
{
    class RaGKitBase;
    class RaG_ContainerBase;

    class MyMod_Storage_Kit : RaGKitBase
    {
        scope = 2;
        displayName = "Storage Kit";
        kitItemName = "MyMod_Storage";
        itemPlacingPos[] = {0, 0, 0};
        itemPlacingOri[] = {0, 0, 0};
    };

    class MyMod_Storage : RaG_ContainerBase
    {
        scope = 2;
        displayName = "Storage";
        kitName = "MyMod_Storage_Kit";
    };
};
```

Script definitions:

```c
class MyMod_Storage_Kit : RaGKitBase
{
};

class MyMod_Storage : RaG_ContainerBase
{
    override string GetOpenSoundSet()
    {
        return "MyMod_Storage_Open_SoundSet";
    }

    override string GetCloseSoundSet()
    {
        return "MyMod_Storage_Close_SoundSet";
    }

    override void UpdateVisualState()
    {
        if (IsOpen())
            SetAnimationPhaseSafe("door", 1.0);
        else
            SetAnimationPhaseSafe("door", 0.0);
    }
};
```

Declare `kitItemName` and `kitName` explicitly. Core has naming fallbacks, but explicit class names are safer and survive later renaming.

## Kit placement lifecycle

When placement completes on the server, `RaGKitBase`:

1. resolves the output through `GetRaGItemName()`
2. creates the object with `ECE_PLACE_ON_SURFACE`
3. applies position and orientation
4. transfers item properties when the output returns `AllowTransferHealth() == true`
5. calls `OnAfterPlacementComplete()`

Override the post-placement hook for addon-specific initialization:

```c
override void OnAfterPlacementComplete(Man player, vector position = "0 0 0", vector orientation = "0 0 0", ItemBase item = null)
{
    super.OnAfterPlacementComplete(player, position, orientation, item);

    MyMod_Storage storage = MyMod_Storage.Cast(item);
    if (storage)
        storage.SetHealth01("", "Health", 1.0);
}
```

Keep authoritative object changes on the server.

## Placement properties

These config properties are read through Core's `ItemBase` extensions:

| Property | Method | Purpose |
| --- | --- | --- |
| `kitItemName` | `GetRaGItemName()` | Class spawned by a kit and projected by the generic hologram path |
| `kitName` | `GetRaGItemKitName()` | Kit recreated by supported dismantling |
| `itemPlacingPos[]` | `GetRaGItemPlacingPos()` | Additional hologram position offset |
| `itemPlacingOri[]` | `GetRaGItemOrientation()` | Additional hologram orientation offset |

`GetRaGHologramItem()` and the `hologramName` convention are used by RaG BaseBuilding's specialized hologram integration. They are not required for a normal Core kit.

## Openable-container hooks

`RaG_ContainerBase` synchronizes and persists its open state. By default, cargo and attachment UI are available only while open.

Useful overrides:

| Hook | Default | Use |
| --- | --- | --- |
| `GetOpenSoundSet()` / `GetCloseSoundSet()` | Empty | Return your SoundSet names. |
| `GetDoorSoundPos()` | `rag_door1` | Return a model memory point used for door sound position. |
| `UpdateVisualState()` | No animation | Apply animation phases or proxy changes after open/close. |
| `UpdateProxyState()` | No operation | Add explicit proxy visibility behavior. |
| `ForceAutoClose()` | `true` | Return `false` to preserve an open state after persistence load. |
| `IsProxyException()` | `false` | Allow open/close actions when targeted through an attachment proxy. |
| `GetPoweredNameCondition()` | `em.CanWork()` | Customize when `(POWERED)` appears in the display name. |

`SetDamageDisabled(true)` rejects calculated damage through the base class. Use it only when your gameplay logic explicitly owns the object's damage state.

## Placeable-container rules

`RaG_PlaceableBase` can be put into cargo when empty and closed. It can be taken into hands under the same conditions unless the class returns `true` from `EnableTakeNonEmptyContainers()`.

```c
class MyMod_PortableBox : RaG_PlaceableBase
{
    override bool EnableTakeNonEmptyContainers()
    {
        return true;
    }
};
```

Allowing pickup while full has balance and persistence consequences. Test nested inventory, reconnects, vehicle cargo, and trader integrations.

## Dismantling

Core registers `ActionDismantleRaGItem` on screwdrivers, hammers, and pliers. The stock action is available for an empty `RaG_ContainerBase`, but excludes `RaG_PlaceableBase`.

On success it:

- creates the class returned by `GetRaGItemKitName()`
- optionally transfers item properties
- deletes the placed object
- damages the tool by 5 health
- records supported Core activity logs

Control special cases with:

```c
override bool AllowDismantleRaGItem()
{
    return !IsPowerAvailable();
}

override string DismantleDeniedMessage()
{
    return "Disconnect power before dismantling.";
}

override bool AllowTransferHealth()
{
    return true;
}
```

`DismantleDeniedMessage()` is shown only when `AllowDismantleRaGItem()` returns `false` after the action begins.

## Placement and repair hooks on ItemBase

Core adds several generic helpers to `ItemBase`:

| Method | Purpose |
| --- | --- |
| `IsPowerAvailable()` | Validates an energy manager, passive stored energy, plug state, and switchability. |
| `ItemIsRepairable()` | Rejects pristine and ruined items. |
| `IsWhetstoneRepairCompatible()` | Checks `repairableWithKits` for the Core whetstone type. |
| `IsWeaponRepairCompatible()` | Checks the weapon repair-kit type. |
| `IsClothRepairCompatible()` | Checks cloth and cloth/leather repair-kit types. |
| `ObstructedAbove()` | Uses DayZ's under-roof test. |
| `IgnoreHologramCollision()` | Bypasses the Core hologram collision result. |

`IgnoreHologramCollision()` removes a safety check. Override it only for an object that deliberately supports overlapping placement.

The obstruction hooks behave as a post-placement warning, not a hard placement rejection:

```c
override bool DenyObstructionAbove()
{
    return true;
}

override string GetBadPlacementTitle()
{
    return "PLACEMENT WARNING";
}

override string GetBadPlacementMessage()
{
    return "This object should not be placed under a roof.";
}

override string GetBadPlacementIconPath()
{
    return RaG_Notifications.THUNDER_ICON;
}
```

Despite the `DenyObstructionAbove()` name, Core currently sends a notification after placement; it does not cancel or delete the object.

## RaG BaseBuilding snapping

Core contains compile-guarded snapping hooks for RaG BaseBuilding, including `CanSnapWall()`, `CanSnapFloor()`, `CanSnapStairs()`, and `CanSnapPillar()`.

Do not treat those hooks as a standalone snapping framework. They require the `RaG_BaseBuilding` compile define, its classes, model memory points, and `PluginRaG_BBSnap`. An addon that integrates with that system should document RaG BaseBuilding as an additional hard dependency.
