# P2P Trader server guide

## Set up the market

1. Set `EnableP2P: true` in the Trader root `Settings.json`.
2. Edit `P2P/Settings.json`. Set `CurrencyId` to a currency defined in `Trading/Catalog.json`. A physical currency needs `EnableBanking: true` and an enabled entry in `Banking/Settings.json`. An account currency uses its balance directly.
3. Place a class from `MarketBoardClasses` at each market site. The default is `StaticObj_Misc_AdvertColumn`. Use a placement tool or mission setup that creates an interactable object.
4. Restart and test listing, buying, collecting, and cancelling from ordinary player accounts. If you enable buy orders, test both fulfillment and refund.

One market serves all configured boards. The board action has a 5 m interaction range. The server checks market requests against `InteractionRadius`. The [player guide](player-market.md) covers the menu.

## `P2P/Settings.json`

| Field | Default | Effect |
| --- | --- | --- |
| `Version` | `1` | Configuration schema. |
| `CurrencyId` | `"euro"` | Account balance used for every market transaction. |
| `MinimumPrice`, `MaximumPrice` | `1`, `1000000` | Inclusive price range for whole items. |
| `MaxListingsPerPlayer`, `MaxActiveListings` | `10`, `5000` | Active sale listing caps per player and server. |
| `BuyOrdersEnabled` | `false` | Enables wanted orders. |
| `MaxBuyOrdersPerPlayer`, `MaxActiveBuyOrders` | `5`, `1000` | Separate active wanted-order caps. |
| `ListingExpirySeconds` | `0` | Active lifetime for offers and wanted orders. `0` disables expiration. |
| `SettledRetentionSeconds` | `604800` | Retention for fully settled records, seven days by default. `0` disables timed cleanup. |
| `ListingFee` | `0` | Up-front charge for creating a sale listing. |
| `SalesCommissionPercent`, `MinimumSalesCommission` | `0.0`, `0` | Deducted from sale proceeds and wanted-order payouts. |
| `MinimumConditionPercent` | `0` | Minimum health percentage for traded items. |
| `InteractionRadius` | `5.0` | Board range in metres. Accepts `1–50`. |
| `AllowAttachments`, `AllowCargo` | `false`, `false` | Permit attached items and cargo in traded inventory. |
| `AllowedClassNames`, `DeniedClassNames` | `[]`, `[]` | Inheritance-based item restrictions. Empty allow list accepts any otherwise eligible class. Deny takes priority. |
| `MarketBoardClasses` | `["StaticObj_Misc_AdvertColumn"]` | Board classes. Supply 1–32 entries. |

Per-player caps accept `1–100`. Server caps accept `1–50000`. Expiry and retention accept up to one year in seconds. Class lists apply to nested items as well as the main item. Currency items, ruined items, and protected or unsafe inventory can be rejected.

When commission is positive, the market rounds the percentage charge up, applies the configured minimum, then caps the result at the sale price. A zero percentage disables commission. A wanted order reserves its full price. If fulfilled, the seller receives that price less commission. If cancelled or expired while unfilled, the buyer receives the reservation back.

## Persistence and recovery

Market journals and stored items live under `$profile:\RaG_Core\Storage\RaG_Trader\P2P\`. Each listing uses a `<listing-id>.json` journal and a matching `.bin` when the market holds an item. An open wanted order holds funds until delivery and has no item payload yet.

Keep this directory, including any quarantine records and backups, together with account and player persistence. If the market reports a held or isolated record, check Diagnostics and server logs. Confirm which item and balance operations completed before intervening. See [backup sets](administration-and-recovery.md#backup-sets).
