# Administration, receipts, and recovery

## Validation report

Read `$profile:\RaG_Core\Configs\RaG_Trader\ConfigValidationReport.txt` after startup or reload. It shows validation results and static trader spawn status. A structural error can block startup. Some faults disable only the affected entry. Read the first error for the specific file, class, or listing, then check the server logs if more detail is needed.

## Admin access and diagnostics

Add quoted Steam64 IDs to `AdminSteamIds` in root `Settings.json`. Restart to authorize the first admin. At a trader, use **Diagnostics** to inspect validation errors, disabled listings, route status, and pending Trader or P2P records. Refresh after an edit or recovery attempt. Route controls can change saved state. See [route admin controls](traveling-traders-and-routes.md#admin-controls).

## Live configuration reload

Use **Reload configs** from the trader menu as an active admin. The server validates the candidate files, saves stock and route state, and refreshes open catalogs. A rejected candidate leaves the active configuration in use. Reload is blocked during active transactions or pending ordinary transaction recovery.

| Config area | Procedure |
| --- | --- |
| Category listings, prices, restock, offer pools, and trader profiles | Live reload. Create referenced category files first. |
| Purchased vehicle attachment sets | Live reload. Applies to later purchases. |
| Routes and stops | Live reload. Changed route definitions reinitialize with a new arrival. |
| Static locations, loadouts, opening hours, and safe zones | Restart. |
| Global switches for static traders, routes, safe zones, banking, bank transfers, P2P, and the garage | Restart. |
| Catalog currencies, bank settings, market settings, and garage settings | Restart. |

For a listing that remains finite, reload preserves its count up to the current capacity. New and newly finite listings start at `InitialStock`. Reopen the trader and check a representative listing after reload.

## Player receipts

**History** holds each player's 50 most recent receipts, covering trader sales and purchases, ATM activity, transfers, and player-market trades. A basket has one receipt with separate lines. Players can copy a receipt from the Trader or ATM menu. Use the receipt ID, time, and trade details to look up the corresponding operation.

## Economy telemetry

With `EnableEconomyTelemetry: true`, the server records aggregate trade counts, failure reasons, item quantities, and currency totals in `EconomyTelemetry.json` under Trader storage. It keeps up to 30 UTC days. Money spent on purchases and money paid for sales are trade flows. Wallets, bank transfers, and unrelated rewards can affect total money in circulation.

## Transaction journals

`Transactions/<transaction-id>.json` records ordinary trade and ATM checkpoints. Bank transfers, P2P, and vehicle storage have their own records. An interrupted operation may be held for review when the server cannot establish which side effects completed.

### Retry recovery

1. Preserve Trader files, the affected world/player persistence, and logs. Check the first error for missing files, write failures, or a missing mod.
2. Have affected players connect if recovery needs access to their inventories.
3. If the trader UI is available, an admin can select **Retry recovery** for ordinary Trader journals. Wait for the result.
4. Reconcile held records with actual items, money, stock, and vehicles before granting compensation. Use [troubleshooting](troubleshooting.md) to locate the subsystem that reported the hold.

## Backup sets

Back up the server while stopped. Keep each set with matching DayZ player and world persistence, plus backups and pending files.

| Root | Contents to preserve |
| --- | --- |
| `$profile:\RaG_Core\Configs\RaG_Trader\` | Configs, `Stock.json`, `StockDelta.json`, `Transactions/`, `Accounts/`, `BankDirectory/`, `BankTransfers.json` |
| `$profile:\RaG_Core\Storage\RaG_Trader\` | `Routes/`, `P2P/`, `Garage/`, `Vehicles/`, `History/`, `EconomyTelemetry.json` |

Restoring a balance, world vehicle, or stock file by itself can conflict with completed operations in the other files.
