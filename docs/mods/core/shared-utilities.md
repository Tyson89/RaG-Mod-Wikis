# Shared Utilities

RaG Core includes small helpers for identity handling, inventory snapshots, pagination, request replay protection, and atomic JSON persistence. Use them as building blocks; they do not replace addon-specific validation or lifecycle code.

## Identity helpers

`RaGIdentityUtility` is available in `3_Game`:

```c
string stableId = RaGIdentityUtility.GetId(identity);
string steam64 = RaGIdentityUtility.GetSteamId(identity);
string logLabel = RaGIdentityUtility.GetLabel(identity);
bool numeric = RaGIdentityUtility.IsNumericIdentifier(value, 32);
```

`GetId()` prefers `PlayerIdentity.GetPlainId()` and falls back to `GetId()`. `GetLabel()` returns the player name plus Steam64 ID for logs. Do not use display names as authorization keys.

## Inventory snapshots

`RaGInventoryUtility` and `RaGInventorySnapshot` are available in `4_World`.

```c
RaGInventorySnapshot snapshot = new RaGInventorySnapshot(player);
int nails = snapshot.CountClass("Nail");
int total = snapshot.Items.Count();
```

The snapshot walks player inventory, item-in-hands, nested attachments, and nested cargo while de-duplicating entities. `CountClass()` is an exact class-name count, not an inheritance check.

Direct helpers:

```c
array<EntityAI> items;
RaGInventoryUtility.CollectPlayerInventory(player, items);

int hierarchyCount = RaGInventoryUtility.CountInventoryHierarchy(container);
int nestedCargoCount = RaGInventoryUtility.CountNestedCargoItems(container);
```

`CountInventoryHierarchy()` includes the root entity. `CountNestedCargoItems()` counts cargo entries on the entity plus cargo entries below its attachments; it does not count the attachment entities themselves.

Inventory state can change after collection. Revalidate authoritative items and quantities on the server immediately before consuming, moving, selling, or rewarding them.

## Paged RPC math

`RaGPagedRPC` is available in `3_Game`:

```c
if (!RaGPagedRPC.IsPageValid(offset, pageSize, 100, 10000))
    return;

int end = RaGPagedRPC.PageEnd(offset, pageSize, totalCount);
int pages = RaGPagedRPC.ChunkCount(totalCount, pageSize);
```

`ChunkCount()` returns at least `1`, including for an empty result. `PageEnd()` returns `-1` for invalid negative inputs or a page size below `1`, and clamps an offset beyond the total to the total.

These helpers validate bounds only. The server must still authorize the request, cap result sizes, and validate the RPC with `RaG_RPCService`.

## Request sequencing and replay protection

`RaGRequestSequence` creates monotonically increasing request IDs and an epoch. When the ID reaches `int.MAX`, the next request advances the epoch and restarts at ID `1`.

`RaGRequestLedger` tracks accepted IDs per identity, detects replays, limits stored receipts, and provides a per-identity execution lock with timeout and cooldown:

```c
ref RaGRequestLedger ledger = new RaGRequestLedger(64, 30000, 1000);

bool replay;
bool canExecute;
bool epochReset;
int retiredRequestId;

if (!ledger.Begin(identityId, requestId, requestEpoch, replay, canExecute, epochReset, retiredRequestId))
    return;

if (replay || !canExecute)
    return;

int result = ledger.TryAcquire(identityId, g_Game.GetTime());
if (result != RaGRequestLedgerAcquireResult.RAG_REQUEST_LEDGER_OK)
    return;

// Perform one authoritative operation.
ledger.Release(identityId);
```

Clear an identity on disconnect with `Clear(identityId)`. Use `ClearAll()` during manager shutdown or mission reset. Always release after the protected operation, including failure paths.

## Atomic JSON persistence

`RaGAtomicJsonIO<T>.Save()` writes to `<path>.tmp`, copies the previous file to `<path>.bak`, then commits the temporary file. `RaGConfigIO<T>` now uses this atomic save path automatically.

```c
string path = RaGCoreFS.StorageDir("MyMod") + "state.json";

MyState state = new MyState();
if (!RaGAtomicJsonIO<MyState>.Save(path, state))
    RaG_CoreLogger.Error("Failed to save state: " + path);
```

Loading and explicit backup loading:

```c
MyState loaded;
if (!RaGAtomicJsonIO<MyState>.Load(path, loaded, new MyState()))
{
    if (!RaGAtomicJsonIO<MyState>.LoadBackup(path, loaded, new MyState()))
        return;
}
```

Use `RaGAtomicRecordJournal<T>` when a multi-step change needs prepare, verify, then commit:

```c
MyState verified;
if (!RaGAtomicRecordJournal<MyState>.Prepare(path, state, verified))
    return;

if (!RaGAtomicRecordJournal<MyState>.Commit(path))
    RaGAtomicRecordJournal<MyState>.Cancel(path);
```

`RaGAtomicRecordJournal<T>.Load()` can restore a valid `.bak` file and preserve the broken primary as `.invalid`. `RaGAtomicRecordIO` and `RaGAtomicClassJsonIO` provide equivalent non-generic `Class` workflows.

All writes are server-only. Treat every `bool` result as meaningful. A failed save or commit must stop the state transition that depended on durable storage.

## Bundled defaults

`RaGBundledFileInstaller.CopyMissing(source, destination)` copies a bundled file only when the destination does not exist. On clients it returns `true` without writing.

Use it for first-run examples or default data, not migrations. It deliberately preserves every existing destination file, including an outdated or invalid one.

## Storage directory

Use Core's module-scoped storage root for runtime state that is not operator configuration:

```c
string storageDir = RaGCoreFS.StorageDir("MyMod");
```

Result:

```text
$profile:\RaG_Core\Storage\MyMod\
```

Use a stable hard-coded module name. Never pass player-controlled path segments, `..`, or separators to `ConfigDir()`, `LogDir()`, or `StorageDir()`.
