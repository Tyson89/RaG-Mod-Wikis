# P2P Trader server guide

## Set up the market

1. Set `EnableP2P: true` in the Trader root `Settings.json`.
2. Edit `P2P/Settings.json`. Set `CurrencyId` to a currency defined in `Trading/Catalog.json`. A physical currency needs `EnableBanking: true` and an enabled entry in `Banking/Settings.json`. An account currency uses its balance directly.
3. Use the bundled board at Green Mountain or place a class from `MarketBoardClasses` at each custom site. The default is `StaticObj_Misc_AdvertColumn`. Place it through the location group's `Objects` array or your map setup.
4. Restart and test listing, buying, collecting, and cancelling from ordinary player accounts. Test fulfillment and refund for both account and cash orders when using an item currency.

One market serves all configured boards. The board action has a 5 m interaction range. The server checks market requests against `InteractionRadius`. The [player guide](player-market.md) covers the menu.

## `P2P/Settings.json`

| Field | Default | Effect |
| --- | --- | --- |
| `Version` | `1` | Configuration schema. |
| `CurrencyId` | `"euro"` | Currency for all market transactions. Sale listings use account balances. Wanted orders can also use physical items of that currency. |
| `MinimumPrice`, `MaximumPrice` | `1`, `1000000` | Inclusive price range for whole items. |
| `MaxListingsPerPlayer`, `MaxActiveListings` | `10`, `5000` | Active sale listing caps per player and server. |
| `BuyOrdersEnabled` | `true` | Enables wanted orders when the market is on. |
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

When commission is positive, the market rounds the percentage charge up, applies the configured minimum, then caps the result at the sale price. A zero percentage disables commission. Wanted orders reserve the full price and pay the supplier after commission. An unfilled order returns its reservation on cancellation or expiry.

For an item currency, the server uses carried cash when it covers the full order price, otherwise it uses the account for the full amount. Cash funding requires denominations that can deliver both the refund and the net payout. Cash is collected at the board into inventory. Account-funded orders settle to accounts.

## Persistence and recovery

Market journals and stored items live under `$profile:\RaG_Core\Storage\RaG_Trader\P2P\`. Each listing uses a `<listing-id>.json` journal and a matching `.bin` when the market holds an item. An open wanted order holds funds until delivery and has no item payload yet.

Keep this directory, including any quarantine records and backups, together with account and player persistence. Cash reserves and claims also use the Trader `Transactions/` journals. If the market reports a held or isolated record, check Diagnostics and server logs. Confirm which item and balance operations completed before intervening. See [backup sets](administration-and-recovery.md#backup-sets).
