# Logging API

RaG Core provides buffered server-side logging with per-module channels, dated files, rotation, and retention. Third-party mods should register their own module instead of writing diagnostics into the RaG Core channel.

## Create a dedicated logger

```c
class MyModLogger : RaG_CoreLogger
{
    static const string MODULE = "MyMod";
    static const string BASE_NAME = "MyMod";
    static const string LEVEL_INFO = "INFO";
    static const string LEVEL_ERROR = "ERROR";

    static void Init(bool infoEnabled, bool errorEnabled)
    {
        #ifdef SERVER
        RegisterChannel(MODULE, BASE_NAME, LEVEL_INFO, infoEnabled, false);
        RegisterChannel(MODULE, BASE_NAME, LEVEL_ERROR, errorEnabled, false);
        #endif
    }

    static bool IsInfo()
    {
        return IsChannelEnabled(MODULE, LEVEL_INFO);
    }

    static void Info(string message)
    {
        #ifdef SERVER
        if (IsChannelEnabled(MODULE, LEVEL_INFO))
            WriteLogEx(LEVEL_INFO, MODULE, BASE_NAME, message);
        #endif
    }

    static void Error(string message)
    {
        #ifdef SERVER
        if (IsChannelEnabled(MODULE, LEVEL_ERROR))
            WriteLogEx(LEVEL_ERROR, MODULE, BASE_NAME, message);
        #endif
    }
};
```

Initialize your channels once after your config is registered:

```c
MyModConfig cfg = RaGConfigAPI<MyModConfig>.Get("MyMod", "MyMod");
MyModLogger.Init(cfg && cfg.EnableInfoLog, true);
```

Then log without performing file I/O yourself:

```c
MyModLogger.Info("Spawn manager initialized");
MyModLogger.Error("Failed to create reward object");
```

## Output layout

The example above writes to:

```text
$profile:\RaG_Core\Logs\MyMod\Info\MyMod_INFO_YYYY-MM-DD.log
$profile:\RaG_Core\Logs\MyMod\Error\MyMod_ERROR_YYYY-MM-DD.log
```

Standard levels map to `Debug`, `Info`, `Warning`, and `Error` subdirectories. Other level names go under `Custom\<level>` unless the module explicitly enables root-level custom logs.

## Custom levels

```c
static const string LEVEL_AUDIT = "AUDIT";

RaG_CoreLogger.SetCustomLogsAtModuleRoot("MyMod", true);
RaG_CoreLogger.RegisterChannel("MyMod", "Audit", LEVEL_AUDIT, true, true);

if (RaG_CoreLogger.IsChannelEnabled("MyMod", LEVEL_AUDIT))
    RaG_CoreLogger.WriteLogEx(LEVEL_AUDIT, "MyMod", "Audit", "Player claimed reward");
```

Use custom levels for genuinely different streams such as audit or economy records, not as substitutes for every class name.

## Runtime behavior

Current Core behavior includes:

- buffered writes with a one-second flush timer
- immediate flush for `ERROR` entries
- automatic dated filenames
- rollover after 50,000 lines
- 30-day retention cleanup
- newline removal from individual messages
- retry after a temporary file-open failure
- a bounded buffer that reports dropped lines instead of growing indefinitely

Core starts and stops the shared flush timer. Third-party mods should register channels, but should not start a second timer or clear the Core logger instance.

## Core convenience methods

These methods write to RaG Core's own diagnostic logs and obey `RaG_Core.json`:

```c
RaG_CoreLogger.Debug("...");
RaG_CoreLogger.Info("...");
RaG_CoreLogger.Warning("...");
RaG_CoreLogger.Error("...");
```

They are useful while working inside RaG modules. A third-party addon should normally use its own channel so server owners can identify and control its output independently.

## Reserved activity channels

`RaG_ActivityLogger` is Core's gameplay activity stream. Its `GENERAL`, `VEHICLE`, and `EXTENDED` channels are reserved for Core-provided activity logging. Do not use them for your addon's diagnostics or custom audit format; register your own module instead.

## Safety rules

- Log on the server only when the record is authoritative.
- Never include authentication tokens, passwords, or private configuration values.
- Avoid writing every frame or every simulation tick.
- Sanitize player-controlled text when it will be consumed by external tooling.
- Expose high-volume channels through your own config and default them off.
