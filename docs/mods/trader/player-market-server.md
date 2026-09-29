# P2P Trader server guide

P2P Trader runs inside RaG Trader. Install RaG Core and RaG Trader on server and clients, provide valid Trader catalog/account setup, enable `P2P.json`, and place market boards. [Player guide](player-market.md) covers shopping, listing, and claims.

## Enable a working market

1. Start server once to generate `$profile:\RaG_Core\Configs\RaG_Trader\P2P.json`, then stop it and back up configuration plus persistence.
2. Choose `CurrencyId` from `Catalog.json`. Account currency works directly. An item currency requires global Banking and that currency's bank entry enabled; market spends stored balance, never notes in inventory.
3. Set `Enabled: true`, price bounds, active-offer limits, and attachment/cargo policy.
4. Place `StaticObj_Misc_AdvertColumn` through map/editor or mission placement at accessible sites. `Locations.json` does not spawn boards. Use exact class and test ordinary player interaction; server accepts operations only within five metres of a qualifying board.
5. Restart server. Test with two ordinary player accounts: deposit or fund currency, list item, buy with second account, claim purchase, check seller proceeds, cancel another offer, and claim return.

The board opens one server-wide market. Several boards can serve different towns; they do not create separate inventories or regional prices. A board may stand near an ATM or NPC shop, but those objects use different actions. Safe-zone protection depends on location/zone setup, not on market board itself.

## `P2P.json`

Bundled file:

```json
{
  "Version": 1,
  "Enabled": false,
  "CurrencyId": "euro",
  "MinimumPrice": 1,
  "MaximumPrice": 1000000,
  "MaxListingsPerPlayer": 10,
  "MaxActiveListings": 5000,
  "AllowAttachments": false,
  "AllowCargo": false
}
```

| Field | Rule | Effect |
| --- | --- | --- |
| `Version` | `1` | Config schema. |
| `Enabled` | Boolean | Disabled market cannot trade; stored listings remain on disk. |
| `CurrencyId` | Nonempty catalog currency ID | All offers use this currency. No automatic currency conversion. Item currency needs enabled bank entry; account currency uses account balance. |
| `MinimumPrice` | Positive integer | Lowest accepted seller price. |
| `MaximumPrice` | At least `MinimumPrice` | Highest accepted seller price. Default 1,000,000. |
| `MaxListingsPerPlayer` | 1–100 | Active offers allowed per seller. Default 10. |
| `MaxActiveListings` | 1–50,000 | Active offers across server. Default 5,000. |
| `AllowAttachments` | Boolean | Allows listing an item containing attachments. Default false. |
| `AllowCargo` | Boolean | Allows listing an item containing cargo. Default false. |

P2P config is registered at server startup; Trader **Reload configs** does not reread it. Restart after edits. A normal Trader catalog reload can refresh market browsing categories, but category changes do not turn P2P settings into live settings.

### Listing policy and practical limits

Server requires item to be in seller's player inventory, removable, non-ruined, and outside locked inventories. Car keys and configured currency-item classes are excluded. `AllowAttachments` and `AllowCargo` are independent: enabling one does not enable other. `CanListP2PItem(PlayerBase player, ItemBase item)` hook can impose additional mod-specific restrictions; default hook returns true. NPC Trader catalog buy/sell prices and stock do not control seller price or whether item class can be listed.

Each offer stores one actual inventory item in escrow. When contents are permitted, item payload can include nested objects; test all custom classes you permit before making composite listings common. A small cap on active listings bounds stored items and browsing work. For mixed-mod servers, start with attachments/cargo disabled, then test known custom gear, magazines, energy items, liquids, and containers in both sale and cancelled-return flows before enabling composite items.

No market fee is applied by P2P service: buyer pays listed amount, seller receives that amount as account credit. For banked item currencies, `MaxBankBalance` can hold proceeds until seller has room. Account balance is required even when players carry enough physical notes. An ATM gives players a route to deposit or withdraw that physical currency. See [banking and transfers](banking-and-currencies.md).

## Market designs

| Goal | Setup | Watch closely |
| --- | --- | --- |
| Small-town exchange | Place boards at staffed hubs; keep default ten active offers per player. | Every board shows same offers. Safe-zone rules need their own location setup. |
| Loot resale economy | Keep scarce NPC stock; let players list eligible found classes at chosen prices. | Market accepts classes outside NPC catalog. Use price and global-listing caps to contain spam. |
| Complete gear kits | Enable attachments and possibly cargo after testing custom classes. | Buyer receives actual stored contents. Inspect serializer recovery and inventory size. |
| Bank-first market | Use enabled banked item currency, place ATMs nearby, and allow Trader **Pay: Bank**. | Players need deposited funds; finite bank ceilings can stall seller proceeds. |
| Account-credit marketplace | Select account currency from catalog and supply balances through controlled integration. | P2P does not mint balances or convert physical notes into account credits. |

Prices are seller-selected, so an NPC buyback price need not anchor player offers. Compare quantity, condition, and rarity before choosing a ceiling. Any form of market manipulation or trading rules beyond listing eligibility needs separate administration or mod hooks.

## Persistence and recovery

Keep these paths in one consistent backup set with DayZ player persistence:

```text
$profile:\RaG_Core\Configs\RaG_Trader\P2P.json
$profile:\RaG_Core\Configs\RaG_Trader\Accounts\<Steam64>.json
$profile:\RaG_Core\Storage\RaG_Trader\P2P\<listing-id>.json
$profile:\RaG_Core\Storage\RaG_Trader\P2P\<listing-id>.bin
$profile:\RaG_Core\Storage\RaG_Trader\History\<Steam64>.json
```

Listing `.json` journals track escrow, buyer payment, seller proceeds, claims, and recovery checkpoints. Matching `.bin` holds actual stored item until claim. File IDs are listing identities; do not rename, delete, or hand-edit one half of a pair to resolve a dispute. Account debit/credit operations use persistent markers so recovery can determine whether money moved. Startup tries valid journal backup; invalid journal or missing unclaimed payload can disable P2P while preserving files. Inspect server Error/Warning logs and backup before intervening.

Pending listing preparation is revisited when seller connects. Purchased item remains in **Purchased** until buyer claims; cancelled item remains in **Returns** until seller claims. Seller proceeds are deposited when settlement succeeds; pending proceeds appear in **My listings**. Buyer claim needs inventory room, with no ground fallback. A receipt supports investigation but does not replace item journal or account state. Fully settled listings may stop appearing in market tabs; recent receipts remain in History subject to its 50-entry cap.

For support, collect listing ID, seller/buyer Steam64 IDs, approximate UTC time, and exact menu message. Compare matching listing journal, item payload, both accounts, and player inventories before refunding or granting replacement. A timed-out purchase can have succeeded; tell buyer to refresh **Purchased** and History rather than pay again. Missing item payload or unreadable journal needs controlled recovery from consistent backup, not a blind market reset.

## Test checklist

- Board opens for ordinary player; walking beyond five metres blocks operations even if menu remains open.
- Item currency: deposit at ATM, purchase from bank balance, inspect exact debit and seller credit. Account currency: test controlled starting balance/integration.
- Two players cannot buy same active listing twice; seller cannot buy own listing.
- Seller reaches per-player cap; server reaches global cap; listing price below/above bounds is rejected.
- Attachment and cargo policy rejects or preserves representative custom items as configured.
- Buyer claims with full inventory, frees space, then claims same stored item once.
- Seller cancels active listing, claims returned item; sold listing cannot be cancelled.
- `MaxBankBalance` blocks proceeds, then seller frees headroom and claims proceeds.
- Restart with active, sold-unclaimed, and returned-unclaimed listings; verify tabs, balances, and item claims.
