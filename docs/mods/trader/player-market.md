# Player market

Player market lets players list individual inventory items for other players to buy. It is separate from NPC traders: listings belong to players, the actual item is stored while listed, and payment moves between account balances. Servers must enable it and place a market board before players can use it.

## Use the market

Approach a placed `StaticObj_Misc_AdvertColumn` and use the **Player market** action. Stay within five metres of a market board for listing, browsing, buying, cancellation, and claims; the server checks distance for each operation. A trader NPC or ATM does not substitute for the board. Any qualifying board accesses the same server-wide listings.

**Browse** shows active offers. Search by item name or class, choose a catalog category, set minimum/maximum price or minimum condition, then sort by newest, cheapest, or best condition. Results use pages of up to 40 listings. A class outside catalog categories appears under **Other**. Category is a browsing aid, not an eligibility rule: players may list other valid inventory items. Inspect the displayed condition, stack quantity, rounds, energy, liquid, attachments, and cargo before buying. A listing represents one actual item; quantity inside that item is not a count of interchangeable shop units.

### List an item

1. Carry the intended item in player inventory. Empty or detach contents if server disallows them.
2. Select item in the market inventory pane. Enter a whole price within server limits and list it.
3. Check **My listings**. Item leaves inventory and remains in market storage until sold or cancelled.

An item must be removable, non-ruined, and outside locked inventory. Car keys and configured physical-currency items cannot be listed. By default, items with attachments or cargo cannot be listed; server can permit either kind of contents. Other mods may also restrict eligible items through `CanListP2PItem`. Remove valuable attachments before listing when they are not meant to go with the sale. Price and listing limits apply per player and across server.

### Buy, claim, or cancel

Buying spends configured market currency from bank/account balance. Carried notes do not pay for a market listing, even when market currency is physical Euro. You cannot buy your own listing. A successful purchase reserves stored item for buyer; open **Purchased** and **Claim item** with enough inventory space. Claim does not use ground fallback. If inventory is full, free space and try claim again while near board.

Seller receives proceeds in account balance. Check **My listings** if proceeds are still pending, and use **Claim proceeds** when offered. A configured maximum bank balance can prevent credit until enough balance room exists. Seller can cancel an active listing, then recover original item through **Returns** → **Claim item**. A sold listing cannot be cancelled. Check History and tabs before repeating a timed-out purchase; a late response may follow a completed charge. If claim reports recovery trouble, preserve listing ID and ask admin to inspect stored item and journal.

!!! tip "Compare real contents"
    A nearly empty magazine, damaged tool, low-charge battery, or partly filled liquid container can look like a cheaper version of a full item. Use listing detail, not name alone. Sellers can use condition and contents to justify price; buyers should compare total usable value.

## Server setup

`$profile:\RaG_Core\Configs\RaG_Trader\P2P.json` is generated with these defaults:

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

Enable market and place `StaticObj_Misc_AdvertColumn` in map/editor data at accessible positions. Test interaction with an ordinary player and leave enough clear space nearby for safe claiming. `CurrencyId` must name a catalog account currency or an item currency with enabled Banking entry. Market prices use one configured currency for all listings. This setting does not convert prices between currencies.

`MinimumPrice` must be positive; `MaximumPrice` must be at least minimum. `MaxListingsPerPlayer` accepts 1–100; `MaxActiveListings` accepts 1–50000. Limits apply to active offers. Keep a lower cap on high-population servers to bound stored item data and the number of live offers. Enabling cargo or attachments lets players sell composite items: test custom items and serializer compatibility, and price entire contents deliberately. Restart server after editing `P2P.json`; ordinary Trader **Reload configs** does not load this file.

Listing journals and item payloads live in `$profile:\RaG_Core\Storage\RaG_Trader\P2P\` as matching `.json` and `.bin` files. Back up both with account data and player persistence. Missing stored items or invalid journals can disable market startup; keep files intact for recovery. [Administration and recovery](administration-and-recovery.md) covers broader account and journal practices.

## Market ideas

- Place boards in guarded hubs to create player exchange points. Market service shares listings across boards; board placement controls where players can act.
- Use scarce NPC stock but allow resale of found items. NPC catalog need not include every player-listed class.
- Keep attachments disabled for simple single-object pricing; enable them for complete kits only after testing serialization and claims.
- Use bank-backed currency so players have reason to deposit earnings and visit ATMs. Pair with [bank transfers](banking-and-currencies.md#player-to-player-bank-transfers) for group trading.
- Tune maximum listings and price ceiling to limit spam and implausible offers. Price is seller-selected; market does not enforce NPC price parity.
