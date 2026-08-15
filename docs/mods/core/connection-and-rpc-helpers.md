# Connection and RPC Helpers

RaG Core provides two related systems:

- `ConnectionManager` prevents duplicate one-time sends during one player connection.
- `RaG_RPCService` registers RPC metadata and validates each received call before its payload is read.

The RPC service does not send calls, serialize payloads, allocate globally unique IDs, or install third-party handlers. Your addon still owns those parts.

!!! warning "Validation is opt-in"
    Registration alone does not protect an RPC. Every receiving `OnRPC()` handler must call `RaG_RPCService.ValidateReceive()` before reading or acting on the payload.

## Register an RPC range

Choose and publish a stable range owned by your addon. Register it on both server and client before any registered RPC can be received:

```c
enum MyModRPC
{
    CONFIG = 24173001,
    INTERACT = 24173002
};

class MyModRPCRegistry
{
    static bool Register()
    {
        if (!RaG_RPCService.RegisterRange("MyMod", 24173000, 24173099))
            return false;

        if (!RaG_RPCService.RegisterRPC(
            "MyMod",
            "Config",
            MyModRPC.CONFIG,
            RaG_RPCDirection.SERVER_TO_CLIENT,
            "PlayerBase"
        ))
            return false;

        return RaG_RPCService.RegisterRPC(
            "MyMod",
            "Interact",
            MyModRPC.INTERACT,
            RaG_RPCDirection.CLIENT_TO_SERVER,
            "MyModInteractable",
            true,
            true,
            false,
            500,
            3.0
        );
    }
};
```

The example range is illustrative, not globally reserved. Collision avoidance remains your responsibility. `RegisterRange()` detects conflicts only among ranges registered in the current game process.

Place the enum in `3_Game`, the registry class in `4_World`, and the startup hooks in `5_Mission` so each reference resolves in script-layer order.

Call the shared registration function from initialization code compiled for both sides. One straightforward `5_Mission` setup is:

```c
modded class MissionServer
{
    void MissionServer()
    {
        MyModRPCRegistry.Register();
    }
};

modded class MissionGameplay
{
    void MissionGameplay()
    {
        MyModRPCRegistry.Register();
    }
};
```

Repeated registration of the same module/range or the same module/name/ID is accepted. Conflicting registrations return `false` and write an error through `RaG_CoreLogger`.

## Registration rules

`RegisterRange(module, range_min, range_max)` rejects:

- an empty module name
- non-positive range values
- a maximum below the minimum
- a second, different range for the same module
- overlap with any registered range

`RegisterRPC()` has this signature:

```c
static bool RegisterRPC(
    string module,
    string name,
    int rpc_id,
    int direction,
    string target_type = "",
    bool require_authenticated_sender = false,
    bool require_alive_sender = false,
    bool require_target_ownership = false,
    int min_interval_ms = 0,
    float max_distance = 0
)
```

It rejects empty names, non-positive IDs, unknown directions, negative limits, conflicting reuse of an ID or module/name pair, and IDs outside the module's registered range. Sender, ownership, rate, and distance rules are valid only for `CLIENT_TO_SERVER` definitions.

Use one of these directions:

| Direction | Accepted receive context |
| --- | --- |
| `RaG_RPCDirection.CLIENT_TO_SERVER` | Server only; multiplayer calls require a sender identity |
| `RaG_RPCDirection.SERVER_TO_CLIENT` | Client only; sender must be `null` |
| `RaG_RPCDirection.SERVER_TO_ALL_CLIENTS` | Client only; sender must be `null` |

The two server-to-client directions describe intended send scope. Receive validation is identical for both.

## Receive validation

Call `ValidateReceive()` before `ctx.Read()`:

```c
modded class PlayerBase
{
    override void OnRPC(PlayerIdentity sender, int rpc_type, ParamsReadContext ctx)
    {
        super.OnRPC(sender, rpc_type, ctx);

        if (rpc_type != MyModRPC.CONFIG)
            return;

        if (!RaG_RPCService.ValidateReceive(sender, this, rpc_type))
            return;

        Param1<MyModClientConfig> payload;
        if (!ctx.Read(payload))
        {
            RaG_RPCService.LogPayloadReadFailure(rpc_type, sender);
            return;
        }

        MyModClientState.SetConfig(payload.param1);
    }
};
```

`ValidateReceive(sender, target, rpc_id)` always checks that the ID is registered. When `target_type` is non-empty, `target` must cast to `EntityAI` and pass `IsKindOf(target_type)`.

For `CLIENT_TO_SERVER`, optional checks mean:

| Option | Check performed |
| --- | --- |
| `require_authenticated_sender` | Sender has an ID and matches its connected `PlayerBase` identity in multiplayer |
| `require_alive_sender` | Sender resolves to a living `PlayerBase` |
| `require_target_ownership` | Target is the player or its hierarchy root player is the sender |
| `min_interval_ms` | Accepted calls from the same identity, RPC ID, and target are separated by at least this interval |
| `max_distance` | Sender is no farther than this distance from the target |

Failed validation returns `false` and logs the reason. Rate-limit warnings are grouped per identity, RPC ID, and target, then throttled to at most one warning every five seconds. Core clears that identity's rate state on disconnect and clears all runtime rate state when the mission finishes.

Validation checks metadata and context, not payload semantics. Keep server-side bounds, permissions, state checks, and authoritative gameplay decisions in your handler.

## One-time send pattern

Use `ConnectionManager` for initial client data that should be sent once per connection:

```c
modded class MissionServer
{
    override void SendModData(PlayerBase player, PlayerIdentity identity)
    {
        super.SendModData(player, identity);

        if (!player || !identity)
            return;

        ConnectionManager manager = ConnectionManager.GetInstance();
        string identity_id = identity.GetId();

        if (!manager || !manager.ShouldSend("MyMod", identity_id))
            return;

        MyModConfig cfg = RaGConfigAPI<MyModConfig>.Get("MyMod", "MyMod");
        if (!cfg)
            return;

        MyModClientConfig client_cfg = new MyModClientConfig(
            cfg.EnableClientEffect,
            cfg.InteractionDistance
        );
        auto payload = new Param1<MyModClientConfig>(client_cfg);

        g_Game.RPCSingleParam(
            player,
            MyModRPC.CONFIG,
            payload,
            true,
            identity
        );
        manager.MarkSent("MyMod", identity_id);
    }
};
```

Always call `super.SendModData()`. Core removes the disconnected identity from every tracked mod key, allowing a fresh send on the next connection. Mark the send only after issuing the RPC.

Do not send the full server config unless the client needs every field. Prefer a narrow serializable DTO:

```c
class MyModClientConfig
{
    bool EnableClientEffect;
    float InteractionDistance;

    void MyModClientConfig(bool effect, float distance)
    {
        EnableClientEffect = effect;
        InteractionDistance = distance;
    }
};
```

Never replicate server-only handles, identities, file paths, secrets, or managed runtime services.

## Registry inspection

Public inspection methods:

- `RaG_RPCService.IsRegistered(rpc_id)` returns whether an ID exists.
- `RaG_RPCService.GetDefinition(rpc_id)` returns its `RaG_RPCDefinition`, or `null`.
- `RaG_RPCService.DumpRegistry()` writes registered definitions at debug level once per process.

Core calls `RaG_RPCService.Init()` during server manager startup. Public registration and validation methods also initialize the built-in registry lazily.

## Reserved RaG ranges

These ranges belong to RaG modules:

| Module | Inclusive range |
| --- | --- |
| `RaG_Core` | `18069000`–`18069099` |
| `RaG_Immersive_Vehicles` | `18069100`–`18069199` |
| `RaG_Wheel_Of_Fortune` | `18069200`–`18069299` |
| `RaG_Hunting_Cabin` | `18069300`–`18069399` |
| `RaG_Baseitems` | `18069400`–`18069499` |
| `RaG_BaseBuilding` | `18069500`–`18069599` |
| `RaG_Dragon` | `18069600`–`18069699` |
| `RaG_Thunderstruck` | `18069700`–`18069799` |
| `RaG_Viking_Pack` | `18069800`–`18069899` |

Existing `RaG_RPC` values outside those ranges are registered internally as legacy IDs. They remain reserved. Do not append to `RaG_RPC`, reuse any RaG ID, or claim a RaG range for a third-party addon.

For your addon:

- use its own prefixed enum and module name
- publish its chosen range
- never silently change a released ID
- register the same definitions on client and server
- reject incompatible client/server versions at an appropriate protocol boundary

RaG Core provides a runtime registry and conflict detection, not a global allocator or central reservation authority.

## When not to use ConnectionManager

Use `ConnectionManager` only for data sent once per connection, such as initial client settings. Dynamic state needs an explicit update RPC, a synchronized variable, or another replication mechanism appropriate to the object.
