# P2P Trader: player market

Player market lets players list individual inventory items for other players to buy. It is separate from NPC traders: listings belong to players, the actual item is stored while listed, and payment moves between account balances. Servers must enable it and place a market board before players can use it.

## Use the market

Approach a placed `StaticObj_Misc_AdvertColumn` and use the **Player market** action. Stay within five metres of a market board for listing, browsing, buying, cancellation, and claims; the server checks distance for each operation. A trader NPC or ATM does not substitute for the board. Any qualifying board accesses the same server-wide listings.

**Browse** shows active offers. Search by item name or class, choose a catalog category, set minimum/maximum price or minimum condition, then sort by newest, cheapest, or best condition. Results use pages of up to 40 listings. A class outside catalog categories appears under **Other**. Category is a browsing aid, not an eligibility rule: players may list other valid inventory items. Inspect displayed condition, stack quantity, rounds, energy, liquid, attachments, and cargo before buying. A listing represents one actual item; quantity inside that item is not a count of interchangeable shop units.

The four tabs serve different tasks:

| Tab | What appears | Action |
| --- | --- | --- |
| **Browse** | Active listings from all sellers. | Select listing and **Buy**. |
| **My listings** | Your active offers and sold offers needing proceeds action. | Cancel active offer or claim pending proceeds. |
| **Purchased** | Your purchases awaiting item claim, including purchases still being settled. | **Claim item** when offered. |
| **Returns** | Your cancelled offers awaiting item claim. | **Claim item**. |

Once every claim and payment checkpoint is settled, listing can disappear from tabs. Use **History** for recent purchase/sale receipt rather than expecting a permanent sold-listing archive.

### Search and compare offers

Search accepts up to 96 characters and matches display name or class without case sensitivity. Price filters use whole amounts; blank minimum/maximum means no limit. Minimum-condition choices are **Any**, **20%+**, **40%+**, **60%+**, **80%+**, and **100%**. A listing without known condition detail does not pass a positive condition filter. Filters and sort apply to personal tabs too, so clear them when an expected purchase or return seems missing. The menu remembers each tab's query while open; use **Refresh** to request a fresh snapshot. Neither visible offer nor selected row reserves an item.

!!! tip "Use class search for modded items"
    Translated names can be similar or missing. Search known class fragment, clear category, then compare condition and contents. Cheapest sort compares listing prices, not price per round, stack unit, or included attachment.

### List an item

1. Carry the intended item in player inventory. Empty or detach contents if server disallows them.
2. Select item in the market inventory pane. Enter a whole price within server limits and list it.
3. Check **My listings**. Item leaves inventory and remains in market storage until sold or cancelled.

An item must be removable, non-ruined, and outside locked inventory. Car keys and configured physical-currency items cannot be listed. By default, items with attachments or cargo cannot be listed; server can permit either kind of contents. Other mods may also restrict eligible items through `CanListP2PItem`. Inventory pane can show an item the server will reject; visibility is not a listing guarantee. Remove valuable attachments before listing when they are not meant to go with the sale. Price and listing limits apply per player and across server.

Listing stores selected object's actual condition, quantity, ammo, energy, liquid, and permitted contents. It removes that object from your inventory; it is not a duplicate or a shop template. One listing means one item, even if it contains several rounds or cargo objects. Check **My listings** after listing; do not repeat immediately when status is uncertain.

### Buy, claim, or cancel

Buying spends configured market currency from bank/account balance. Carried notes do not pay for a market listing, even when market currency is physical Euro. You cannot buy your own listing. **Buy** acts on selected listing; there is no NPC-trader basket. Check price, currency, condition, and contents before clicking. A successful purchase reserves stored item for buyer; open **Purchased** and **Claim item** with enough inventory space. Claim does not use ground fallback. If inventory is full, free space and try claim again while near board. Claim restores stored item rather than generating a fresh full-condition copy.

Seller receives proceeds in account balance. Check **My listings** if proceeds are still pending, and use **Claim proceeds** when offered. A configured maximum bank balance can prevent credit until enough balance room exists. Seller can cancel an active listing, then recover original item through **Returns** → **Claim item**. A sold listing cannot be cancelled. Check History and tabs before repeating a timed-out purchase; a late response may follow a completed charge. If claim reports recovery trouble, preserve listing ID and ask admin to inspect stored item and journal.

!!! tip "Check both sides after uncertain request"
    Purchase can complete even when menu times out. Refresh **Purchased**, check bank balance and History, then ask admin with listing ID if state remains unclear. Do not press **Buy** again on another copy of the offer to test it.

!!! tip "Compare real contents"
    A nearly empty magazine, damaged tool, low-charge battery, or partly filled liquid container can look like a cheaper version of a full item. Use listing detail, not name alone. Sellers can use condition and contents to justify price; buyers should compare total usable value.

## Server setup

See [P2P Trader server guide](player-market-server.md) for `P2P.json`, board placement, currency requirements, listing limits, persistence, recovery, and test checklist.

## Market ideas

- Place boards in guarded hubs to create player exchange points. Market service shares listings across boards; board placement controls where players can act.
- Use scarce NPC stock but allow resale of found items. NPC catalog need not include every player-listed class.
- Keep attachments disabled for simple single-object pricing; enable them for complete kits only after testing serialization and claims.
- Use bank-backed currency so players have reason to deposit earnings and visit ATMs. Pair with [bank transfers](banking-and-currencies.md#player-to-player-bank-transfers) for group trading.
- Tune maximum listings and price ceiling to limit spam and implausible offers. Price is seller-selected; market does not enforce NPC price parity.
