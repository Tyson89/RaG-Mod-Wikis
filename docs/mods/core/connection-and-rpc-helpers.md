# Connection and RPC Helpers

RaG Core provides `ConnectionManager` and a `MissionServer.SendModData()` extension point for sending addon-owned data once per player connection.

It does not allocate RPC IDs, serialize arbitrary objects automatically, or register client handlers for third-party mods. Those parts remain your responsibility.

## One-time send pattern

Choose a unique mod key and a unique RPC value owned by your addon:

The value below is illustrative only; it is not reserved for copy-and-paste use.

```c
enum MyModRPC
{
    CONFIG = 24173001
};
```

Extend `SendModData()` and always call `super`:

```c
modded class MissionServer
{
    override void SendModData(PlayerBase player, PlayerIdentity identity)
    {
        super.SendModData(player, identity);

        if (!player || !identity)
            return;

        ConnectionManager manager = ConnectionManager.GetInstance();
        string identityId = identity.GetId();
        string modKey = "MyMod";

        if (!manager.ShouldSend(modKey, identityId))
            return;

        MyModConfig cfg = RaGConfigAPI<MyModConfig>.Get("MyMod", "MyMod");
        if (!cfg)
            return;

        auto payload = new Param1<MyModConfig>(cfg);
        g_Game.RPCSingleParam(player, MyModRPC.CONFIG, payload, true, identity);
        manager.MarkSent(modKey, identityId);
    }
};
```

Core removes the identity from all tracked mod keys when that player disconnects, allowing a fresh send on the next connection.

## Receive on the client

Your addon must own its client handler:

```c
modded class PlayerBase
{
    override void OnRPC(PlayerIdentity sender, int rpcType, ParamsReadContext ctx)
    {
        super.OnRPC(sender, rpcType, ctx);

        if (rpcType != MyModRPC.CONFIG)
            return;

        Param1<MyModConfig> payload;
        if (!ctx.Read(payload))
            return;

        MyModClientState.SetConfig(payload.param1);
    }
};
```

The receiving type must exist on the client and be safe to serialize. Do not put server-only handles, identities, file paths, or managed runtime services in the replicated object.

## Prefer a narrow payload

Sending the full server config is convenient but often exposes fields the client does not need. A dedicated DTO is safer:

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

Construct it from the authoritative server config and send only those values.

## RPC ownership

RaG Core's `RaG_RPC` values are reserved for RaG mods. Do not append to that enum or reuse its numbers.

For a third-party addon:

- define an enum in your own namespace or prefix
- choose values that do not collide with DayZ, frameworks, RaG, or your dependencies
- publish the chosen range for other addon authors
- never silently change a released RPC number
- validate both client and server are running compatible versions

RaG Core currently has no global RPC allocator. A random-looking number is not proof of uniqueness.

## Ordering and failure rules

- Call `super.SendModData()` so other integrations get their turn.
- Call `super.OnRPC()` before handling your own case.
- Check `player`, `identity`, manager, config, and payload reads.
- Use `identity.GetId()` consistently as the connection-manager key.
- Mark the send only after issuing the RPC.
- Keep RPC handlers small; hand data to an addon-owned state service.
- Never trust client-originated values for authoritative gameplay decisions.

## When not to use ConnectionManager

Use it for data that should be sent once per connection, such as initial client settings. Do not use it for state that changes during play. Dynamic state needs an explicit update RPC, a synchronized variable, or another replication mechanism appropriate to the object.
