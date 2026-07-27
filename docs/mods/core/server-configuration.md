# Server Configuration

This page is for server operators. Mod authors should use the [Configuration API](configuration-api.md) and [Logging API](logging-api.md) instead of adding fields to `RaG_Core.json`.

The RaG Core configuration controls Core diagnostic and activity logging. It is generated under the server profile at:

```text
RaG_Core/Configs/RaG_Core/RaG_Core.json
```

Boolean settings use `0` for disabled and `1` for enabled.

> [!IMPORTANT]
> Stop the server and back up the working file before editing it. Do not change `Version` or rename keys. Validate the JSON before restarting the server.

## Complete schema example

```json
{
    "Version": 3,
    "EnableDebugLog": 1,
    "EnableInfoLog": 0,
    "EnableWarningLog": 0,
    "EnableErrorLog": 1,
    "EnableCFToolsDismantleLog": 1,
    "EnableCFToolsOpenCloseLog": 1,
    "EnableGeneralActivityLog": 1,
    "EnableVehicleActivityLog": 1,
    "EnableExtendedActivityLog": 1,
    "EnableHeavyExtendedActivityLog": 0
}
```

The values below match the supplied production configuration. They are not hard-coded defaults for every installation.

## Setting reference

| Setting | Example | Explanation |
| --- | ---: | --- |
| `Version` | `3` | Configuration schema version. Do not edit it. |
| `EnableDebugLog` | `1` | Writes diagnostic debug messages used to investigate behavior and configuration problems. |
| `EnableInfoLog` | `0` | Writes general informational messages. |
| `EnableWarningLog` | `0` | Writes warnings for non-fatal problems or unexpected conditions. |
| `EnableErrorLog` | `1` | Writes errors for failed operations and serious problems. |
| `EnableCFToolsDismantleLog` | `1` | Records supported dismantling activity for the CFTools logging integration. |
| `EnableCFToolsOpenCloseLog` | `1` | Records supported open and close activity for the CFTools logging integration. |
| `EnableGeneralActivityLog` | `1` | Records general player and object activity handled by RaG Core. |
| `EnableVehicleActivityLog` | `1` | Records supported vehicle-related activity. |
| `EnableExtendedActivityLog` | `1` | Adds more detailed activity records than the general activity log. |
| `EnableHeavyExtendedActivityLog` | `0` | Enables the highest-volume extended activity logging. Use it only for focused troubleshooting because it can produce substantial output. |

## Recommended use

- Keep `EnableErrorLog` enabled on production servers.
- Enable debug or extended logging when investigating a specific problem.
- Leave `EnableHeavyExtendedActivityLog` disabled during normal operation unless the additional detail is required.
- After changing settings, restart the server and confirm that the expected log output is being produced.

## Troubleshooting

If expected records are missing:

1. Confirm that the relevant setting is `1`.
2. Validate the JSON syntax.
3. Restart the server after the change.
4. Reproduce the relevant activity.
5. Check that any required external logging service, such as CFTools, is configured and available.
