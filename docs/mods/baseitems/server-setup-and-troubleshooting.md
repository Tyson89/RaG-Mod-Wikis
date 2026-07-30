# Server Setup and Troubleshooting

## Required mods

[RaG Core](../core/index.md) is a hard dependency. Install and enable Core and Baseitems on the server and every client. Declared addon dependencies control PBO ordering; server mod-list order does not. Do not install the old standalone Liquid Framework; its functionality is in RaG Core.

## First start

1. Start the server once with both mods loaded.
2. Stop it cleanly.
3. Confirm this file exists under the active server profile:

   ```text
   RaG_Core/Configs/RaG_Baseitems/RaG_Baseitems.json
   ```

4. Edit it only while the server is stopped, validate the JSON, and restart.

RaG Baseitems registers its configuration through RaG Core and sends it to clients when they connect. See [Server Configuration](json-file-explanation.md).

## Economy and trader files

Use [Key Classnames](key-classnames.md) as the starting point. For placeable furniture, spawn or sell the `_kit` in most cases. Adding both a kit and its deployed object to the economy usually creates duplicate or bypassed placement behavior.

The source contains 355 public classes, including color variants and deployed forms. Do not bulk-add every public class to `types.xml`.

## Container damage on PVE servers

RaG Baseitems respects DayZ's server setting:

```c
disableContainerDamage = 1;
```

The mod also has its own `DisableDamage` setting. The DayZ setting covers container damage; the mod setting applies to supported RaG Baseitems base classes. Use the mod setting only when you intentionally want the broader behavior.

## Placement problems

If players cannot place kits where your server rules allow:

1. Confirm `enableCfgGameplayFile = 1;` in `serverDZ.cfg`.
2. Open the active `cfggameplay.json`.
3. Review the `HologramData` collision and clipping checks.
4. Validate the file and restart the server.

This changes placement rules server-wide. Do not disable every collision check blindly.

## Codelock

Codelock support is conditional: its actions and separate raid configuration load only when the Codelock mod is present. See [Codelock Integration](codelock-integration.md).

## Common failures

| Symptom | Likely cause |
| --- | --- |
| Server or client script error at startup | RaG Core is missing, outdated, or mismatched between server and clients. |
| Configuration does not change behavior | Wrong profile folder, malformed JSON, or server not restarted. |
| Workbench action is missing | Blueprint not attached, hammer missing, recipe disabled, or materials below the exact threshold. |
| Powered machine will not start | No compatible power connection, required attachment missing, or machine/item ruined. |
| Solar Panel does not supply power | It is under a roof, it is night without a usable truck battery, or the downstream device is off. |
| Codelock action is missing | Codelock is not loaded, attachment is disabled, or the target must be open first. |
| Car lift scan fails on one modded vehicle | That vehicle's damage zones or attachments are configured incompatibly. |

For detailed diagnostics, enable RaG Core debug logging temporarily and reproduce the problem. Disable verbose logging again after collecting the relevant entries.
