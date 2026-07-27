# Codelock Integration

RaG Baseitems contains conditional integration for the Codelock mod. When Codelock is not loaded, these scripts and actions are not compiled into the active game.

## Player use

Supported RaG containers expose an `Att_CombinationLock` slot.

1. Open the supported RaG Baseitem.
2. Put a Codelock in your hands.
3. Use the attach action.
4. Configure and manage the lock through the normal Codelock interface.

Locked items block their normal open action. Support is broad across storage, workstations, garden objects, and powered items, but not every Baseitems classname accepts a lock.

## Separate server configuration

When Codelock is loaded, Baseitems generates:

```text
$profile:\CodeLock\RaG_BaseItems_CodeLockConfig.json
```

The source defaults are:

```json
{
    "RaidTimeInSeconds": 10.0,
    "CanAttach": "true",
    "CanRaid": "false",
    "DeleteLockOnRaid": "false",
    "ToolDamageOnRaid": 100,
    "RaidTools": [
        "Hacksaw"
    ]
}
```

`CanAttach`, `CanRaid`, and `DeleteLockOnRaid` are strings in this legacy file, not JSON booleans. Keep the quotes and use `"true"` or `"false"`.

| Setting | Meaning |
| --- | --- |
| `RaidTimeInSeconds` | Total configured raid duration used by the Baseitems lock-raid action. |
| `CanAttach` | Allows players to attach Codelocks to supported open Baseitems. |
| `CanRaid` | Enables the Baseitems Codelock raid action. |
| `DeleteLockOnRaid` | Deletes the lock when a successful raid completes. |
| `ToolDamageOnRaid` | Damage applied to the raid tool during the process. |
| `RaidTools` | Case-sensitive classnames allowed to raid the lock. |

Stop the server before editing this file. Back it up, validate the JSON, and restart. This configuration is separate from both the main [Baseitems configuration](json-file-explanation.md) and Codelock's own configuration.
