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

`MinimumPrice` must be positive and `MaximumPrice` at least that value. `ListingFee` and `MinimumSalesCommission` accept `0–MaximumPrice`; commission percentage and minimum condition accept `0–100`. Allow and deny lists each accept up to 256 class strings; class and board strings must contain `1–128` characters. Invalid policy can disable market initialization; check logs before opening it to players.

When commission is positive, the market rounds the percentage charge up, applies the configured minimum, then caps the result at the sale price. A zero percentage disables commission. Wanted orders reserve the full price and pay the supplier after commission. An unfilled order returns its reservation on cancellation or expiry.

For a price of 101 and 2% commission, the fee is 3 and the net payout is 98. A minimum commission of 5 raises that fee to 5 and leaves 96. A 100% commission can leave no payout. The sale-listing fee is separate, paid from account balance when posting; cancellation or expiry does not refund it. Editing an active price or directly relisting a returned stored item adds no new listing fee. Wanted orders reserve their offer without a sale-listing fee.

Normal sale proceeds are credited automatically, including for offline sellers. If credit cannot complete, for example because of a bank cap, the item sale can complete with proceeds still pending. **Collect proceeds** retries the pending credit; it does not give a second payout. Keep room under balance caps and inspect recovery messages before manual compensation.

For an item currency, the server uses carried cash when it covers the full order price, otherwise it uses the account for the full amount. Cash funding requires denominations that can deliver both the refund and the net payout. Cash is collected at the board into inventory. Account-funded orders settle to accounts.

## Item contents and expiration

Market policies inspect the entire stored hierarchy for allowed/denied classes and minimum condition. An item may contain at most 128 nested objects in addition to its root. Listing and fulfillment reject RaG vehicle keys, registered currency items, ruined root items, unavailable inventory, and incompatible server policy. Ordinary dealership vehicles belong in vehicle trading, not inventory sale listings.

The market captures condition, quantity, liquid, ammunition, charge, wetness, temperature, frozen status, and food stage where supported. Detailed inspection covers up to four nested levels, with 20 entries per inspection page and up to 32 attachment classes in the assembled preview. A truncated or unavailable inspection is not proof that a container is empty.

`ListingExpirySeconds` sets an absolute lifetime at posting; an active-price edit does not restart it. Direct relisting starts a new lifetime. Expiration returns unsold goods or unfilled order funds; it does not erase uncollected purchases, returns, or proceeds. `SettledRetentionSeconds` applies only after a record is fully settled. Expiry is processed in batches, so a displayed timeout need not mean immediate physical cleanup.

## Persistence and recovery

Market journals and stored items live under `$profile:\RaG_Core\Storage\RaG_Trader\P2P\`. Each listing uses a `<listing-id>.json` journal and a matching `.bin` when the market holds an item. An open wanted order holds funds until delivery and has no item payload yet.

Keep this directory, including any quarantine records and backups, together with account and player persistence. Cash reserves and claims also use the Trader `Transactions/` journals. If the market reports a held or isolated record, check Diagnostics and server logs. Confirm which item and balance operations completed before intervening. See [backup sets](administration-and-recovery.md#backup-sets).
