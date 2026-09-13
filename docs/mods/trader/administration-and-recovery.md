# Administration, receipts, and recovery

Trader economies depend on consistent persistence. Back up the entire trader state together with DayZ player/world persistence; isolated file restores can duplicate money or disconnect keys from vehicles.

## Validation report

```text
$profile:\RaG_Core\Configs\RaG_Trader\ConfigValidationReport.txt
```

Registry validation checks configuration versions, currency definitions, prices, listing classes, liquid requirements, ammo resale values, offer pools, references, transforms, banking entries, vehicle attachments, and survivor loadouts. Attachment checks create temporary objects to test actual fit.

Report status is `PASSED`, `WARNINGS`, or `FAILED`. Blocking errors prevent registry publication. Warnings deserve review but do not necessarily block startup. Listing-local faults disable the affected listing while valid listings can remain usable. Structural errors in shared configuration block registry publication.

Report groups include missing classes, invalid prices, broken attachments, duplicate entries, unsupported currencies, and general configuration. Read Error/Warning logs too: category-loading failures can occur before report generation, and live-reload restriction details are logged even when the report lacks a dedicated section. Check report timestamp before trusting a previous result.

!!! tip "Fix cause, then validate again"
    An unknown part in `VehicleAttachments.json` can block the whole registry. Check mod availability and exact class first; then attachment slot compatibility. Changing the trader's position cannot fix a catalog or attachment error.

## Admin access

Add quoted Steam64 IDs to `Settings.json`:

```json
{
  "AdminSteamIds": ["76561198000000000"]
}
```

This is a settings fragment. Keep all other settings. Establish the first admin through a server restart; reload authorization uses the currently active admin list, not the candidate file being loaded.

Trader UI exposes **Diagnostics**, **Reload configs**, and **Retry recovery** to listed admins. Reload and recovery requests share a server-wide ten-second cooldown. Wait for the result notification before trying another operation.

## Admin Diagnostics

Open **Diagnostics** from the trader menu as a listed admin. This is a read-only inspection panel; opening it does not reload configuration, retry recovery, or alter balances.

The panel shows registry readiness, recovery-journal readiness, disabled-listing count, pending-transaction count, and paged entries. Select an entry to inspect its details; use **Refresh** after a configuration or recovery operation. Pages contain up to 40 entries, and long detail text is truncated, so retain the full logs and report for investigation.

Entries cover pending journal information, active disabled listings and their first error, and issues from the latest validation attempt. A rejected reload can therefore appear alongside the still-active registry. Check readiness and the actual active listing before assuming a candidate was published.

### Resolve a disabled listing

1. Read its class, listing ID, and first configuration error.
2. Open the corresponding category file. Check exact class, prices, liquid requirement, ingredients, and attachments.
3. For an ammo resale warning, inspect the relevant box resource and loose-ammo prices across the catalog.
4. Correct the entry and use **Reload configs** if only reloadable fields were edited.
5. Refresh Diagnostics, reopen the trader, and test both intended trade directions. Resolving the first error can reveal another problem in the same entry.

Unknown item classes, incompatible listing attachments, and invalid liquid combinations can disable individual listings. Shared currency, location, vehicle-profile, and other structural errors can block the registry. A `WARNINGS` report can therefore describe a working market with unusable items; check disabled counts before accepting it.

If startup fails before the trader UI is usable, diagnose from server files and logs. An in-game panel cannot replace offline repair of a server that never initialized its services.

## Live configuration reload

Reload reads all five main files plus every referenced category, validates them as one candidate, prepares and saves stock, then publishes the candidate. A rejected candidate leaves active configuration in place.

| Config area | Live reload |
| --- | --- |
| Listing prices, stock ceilings, restock fields, materials, liquid requirements | Supported. |
| Category content and trader category references | Supported, with valid existing location references. |
| Trader display names and offer pools | Supported. |
| Global settings and admin list | Supported. |
| Banking fees, enabled bank entries, balance settings | Supported with valid physical currency definitions already in catalog. Existing initial grants are not repeated. |
| Purchased vehicle attachment profiles | Supported for future purchases; existing vehicles are not refitted. |
| `Locations.json`, including loadouts, opening hours, and safe zones | Restart required. |
| Catalog currency definitions or `DefaultCurrencyId` | Restart required. |

### Reload procedure

1. Back up active config and state. Test complex configuration in a separate profile first.
2. Write all candidate files completely. Create any new custom category file before referencing it.
3. Keep locations and currency definitions unchanged for this reload.
4. Log in as an active admin, open trader, and choose **Reload configs** when no transaction is running.
5. Read the result notification and validation logs.
6. Reopen trader. Check a representative purchase, sale, stock count, and policy.

Reload does not install missing defaults. A category file must already exist. Candidate numeric values must satisfy validation; do not rely on startup normalization during reload.

Reload is blocked while a transaction is active, journal is unavailable, or recovery entries remain pending. Use the recovery process below before trying again.

### Stock during reload

- Existing finite listing: keep current stock, capped at the candidate maximum.
- Raised maximum: does not instantly refill existing finite stock.
- Lowered maximum: clamps excess stock down.
- New listing or unlimited-to-finite transition: seed from configured stock.
- Finite-to-unlimited transition: becomes `-1`.
- Removed listing: omitted from prepared state.

Existing restock deadlines are retained for matching listings where available; a changed interval may take effect after the pending deadline. New restocking listings start a fresh timer. Stable category/class IDs preserve stock associations; the persisted identity map distinguishes liquid variants.

!!! tip "Separate price tuning from layout work"
    Tune prices, stock, and offers with reload. Schedule a restart for NPC relocation, safe-zone borders, opening hours, or currency restructuring. Editing both groups together makes the reload reject the entire candidate.

## Player receipts

**History** displays the player's most recent 50 successful trade receipts, newest first. Select a receipt for details: UTC time, location, currency, buy/sell direction, classes, quantities, prices, and purchase requirements. One basket is one receipt with several lines. Ammo receipt quantities count rounds. Use recorded line totals for dynamic-price purchases and condition-adjusted sales; a single displayed unit figure may not describe every unit in the line.

```text
$profile:\RaG_Core\Storage\RaG_Trader\History\<Steam64>.json
```

Dirty history saves on a five-second interval and during normal cleanup. A crash can lose recent receipt history. History is evidence for players, not an undo button, refund system, full bank statement, or substitute for transaction journals. Turning off trade logging does not turn off receipt history.

## Economy telemetry

`EnableEconomyTelemetry: true` records aggregate server trade activity:

```text
$profile:\RaG_Core\Storage\RaG_Trader\EconomyTelemetry.json
```

Data covers up to 30 UTC days, successful and failed transaction counts, failure reasons, bought/sold quantities by class, currency totals, and top-20 bought/sold lists. Dirty data flushes every 60 seconds and during shutdown.

Interpret `CurrencyFlow.Bought` as money spent by players buying goods, and `CurrencyFlow.Sold` as money paid to players selling goods. These are trade flows, not total server money supply. ATM movements and external rewards are not a complete part of this trade summary.

Per-day tracking caps are 512 item classes and 32 currencies. Overflow activity is counted in untracked fields; counters saturate at the integer maximum and mark saturation. A top list is not exhaustive once tracking caps are reached.

### Useful balancing checks

- Large sale flow with little purchase flow: money accumulates; review sinks and repeatable sale routes.
- One class dominates sales: inspect its loot availability, crafting inputs, condition and quantity pricing, and resale price.
- Repeated stock-limit failures: buyback capacity may be full rather than broken.
- Repeated delivery failures: test inventory space, payout denominations, vehicle clearance, and attachments.
- A supposed rare item dominates purchases: check shared stock, restock rate, duplicate routes, and admin test activity.

Use aggregate data alongside [trade logs](settings-stock-and-pricing.md#trade-logging), not as proof of an individual player's intent.

## Transaction journals

```text
$profile:\RaG_Core\Configs\RaG_Trader\Transactions\<transaction-id>.json
```

Journals record purchase, sale, and bank transaction checkpoints so interrupted work can be reconciled. Entries may reference original balances, reserved stock, delivered/sold entities, recovery vaults, consumed requirements, and packed-vehicle storage. They are operational state; preserve them until recovery completes.

Ordinary failures attempt rollback. A crash, failed persistence write, missing entity, or ambiguous ground-currency movement may need recovery. Never promise that every crash can be repaired automatically: source deliberately retains ambiguous entries and can suspend trading.

### Retry recovery

1. Preserve trader config/state, related player/world persistence, and logs.
2. Read the first journal/recovery error. Correct disk-space, permissions, or missing-mod problems before retrying.
3. Bring affected players online when recovery needs their inventories. Logs identify player and transaction IDs.
4. If trader UI remains available, an active admin can choose **Retry recovery** with no transaction in progress.
5. Read the notification. Pending entries keep trading suspended; successful completion reports trading resumed.
6. Verify player wallet/bank, stock, items, and vehicle files before resolving a dispute or granting compensation.

The retry does not auto-approve entries marked for manual review. If startup journal initialization fails before trader/network services start, the UI route may be unavailable. Preserve files, repair the underlying issue offline, and restart; do not keep searching for a missing button.

!!! warning "Avoid double compensation"
    Manually refunding an interrupted trade before recovery finishes can pay the player twice. Preserve the journal, inspect delivered items and balances, then settle the transaction deliberately.

## Backup sets

Back up these roots together:

```text
$profile:\RaG_Core\Configs\RaG_Trader\
$profile:\RaG_Core\Storage\RaG_Trader\
```

Also retain matching DayZ player/world persistence, mod builds, and server configuration. Include atomic `.bak` files. Stop the server for a consistent manual backup or use an administration method that provides a coherent snapshot.

| State | Consequence of discarding it |
| --- | --- |
| `Stock.json` | Stock reseeds from configured capacities; listing identity mappings are lost. |
| `Accounts` | Bank/account balances and initialization records are lost. |
| `Transactions` | Interrupted-trade evidence and recovery links are lost. |
| `Vehicles` | Keys cannot restore missing stored vehicles. |
| `History` | Player receipts disappear. |
| `EconomyTelemetry.json` | Aggregate balancing data disappears. |

Restore only after assessing which transactions happened after the backup. A stock or account backup can predate completed trades; restoring it alone can alter supply or balances. Avoid publishing player-state directories with example configuration.
