# Configuration API

RaG Core provides server-side, versioned JSON storage for other mods. Files are grouped under one predictable profile tree:

```text
$profile:\RaG_Core\Configs\<module>\<file>.json
```

Use `RaGConfigAPI<T>` for normal registration and lookup. Use `RaGConfigIO<T>` inside your config class when it needs to save itself during migration.

## Define a versioned config

```c
class MyModConfig : RaGConfigVersioned
{
    bool EnableFeature = true;
    int MaxObjects = 20;

    void MyModConfig()
    {
        Version = 1;
    }

    override void OnAfterLoad()
    {
        #ifdef SERVER
        bool changed = false;

        // Add migrations when a later release increments Version.
        // if (Version < 2)
        // {
        //     Version = 2;
        //     changed = true;
        // }

        if (changed)
            SaveSelf();
        #endif
    }

    override void SaveSelf()
    {
        #ifdef SERVER
        RaGConfigIO<MyModConfig>.Save("MyMod", "MyMod", this);
        #endif
    }
};
```

Keep `Version` monotonic. Never decrease it or reuse an old version number for a different schema.

## Register during mission startup

```c
modded class MissionServer
{
    override void OnInit()
    {
        super.OnInit();

        MyModConfig cfg;
        RaGConfigAPI<MyModConfig>.Register("MyMod", "MyMod", cfg, new MyModConfig());
    }
};
```

This creates the file with defaults when it is missing, loads an existing file, calls `OnAfterLoad()`, and registers the object for later lookup. Register once. Repeated registration returns the already registered object rather than reloading the disk file.

## Read and save

```c
MyModConfig cfg = RaGConfigAPI<MyModConfig>.Get("MyMod", "MyMod");
if (cfg && cfg.EnableFeature)
{
    // Feature code.
}

// After intentionally changing the in-memory object:
RaGConfigAPI<MyModConfig>.Save("MyMod", "MyMod");
```

`Register`, `Get`, and `Save` are server-only. On clients, the API returns `null` and does not write files.

## Client configuration

The config API does not automatically replicate data. If a client needs selected settings:

1. Keep the authoritative object on the server.
2. Send only the required fields or a serializable config object through your own RPC.
3. Cache the received data in a client-side object owned by your addon.
4. Use [Connection and RPC helpers](connection-and-rpc-helpers.md) to avoid duplicate sends.

Do not make the client read the server profile path.

## File-system helpers

`RaGCoreFS` exposes these paths:

```c
string configDir = RaGCoreFS.ConfigDir("MyMod");
string logDir = RaGCoreFS.LogDir("MyMod");
```

Both helpers create the module directory on the server when needed. Use simple stable module names; do not pass slashes, parent traversal, or user-controlled text.

## Migration rules

- Initialize new fields with safe defaults in the class declaration or constructor.
- Upgrade old versions in ascending order inside `OnAfterLoad()`.
- Call `SaveSelf()` only when the loaded object changed.
- Do not delete unknown production files automatically.
- Back up a config before a destructive schema migration.
- Validate migration on a copy of a real server file.

## Common mistakes

| Mistake | Result |
| --- | --- |
| Calling `Get()` before `Register()` | Returns `null` |
| Using `RaGConfigAPI.Save()` from an early `OnAfterLoad()` migration | The object may not yet be present in the registry; use `RaGConfigIO.Save()` in `SaveSelf()` |
| Expecting automatic client sync | Clients receive nothing until your addon sends it |
| Renaming module or file after release | A second path is created and the old config is ignored |
| Changing field types without migration | Existing JSON may load incorrectly or lose meaning |
