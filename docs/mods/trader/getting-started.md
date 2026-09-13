# Player guide

## Open a trader

Approach a configured NPC or terminal and use **Trade**. Server checks configured `InteractionDistance` when opening catalog and again during checkout. Staying beside visible NPC is safest; walking away with menu open causes transaction failure.

Trader can also be closed by configured in-game opening hours. Hours use DayZ world time, not real server clock.

## Find items quickly

Trader UI supports:

- category tabs and optional **Search all categories**;
- search by display name or exact class name;
- **All**, **Buyable**, **Sellable**, **In stock**, **Favorites**, and recent-purchase filters;
- **Sellable only**, which checks current player inventory;
- compatible-item filtering for attachments, magazines, and ammunition;
- paged item cards;
- rotatable and zoomable 3D preview;
- current currency balance, stock, inventory load, prices, and item description.

**In stock** hides only listings at `0`. Unlimited stock displays as **Unlimited**. The restock countdown appears for eligible finite listings below capacity; it estimates replenishment and does not reserve the next delivery.

**Search all categories** expands a non-empty search across this trader's categories. With no search text, the selected category still applies. It never searches another trader's catalog.

### Useful search habits

- Search class fragment when translated display name is unclear.
- Enable **Sellable only** before clearing loot. It checks basic sale eligibility; an item inside a container can qualify, but an item containing cargo cannot. Server still checks stock capacity, liquid contents, and ownership.
- Check quantity before clicking. Ordinary lines allow up to 100 objects; loose ammo allows up to 10,000 rounds. Ground-delivered ordinary items and vehicles allow exactly one. Attachment/material work and basket limits can reduce practical checkout size.
- Read **Estimated total** for the selected quantity. The displayed per-item or per-round base price does not include every condition, contents, or stock adjustment.

## Favorites, recent purchases, and compatibility

Right-click an item card to toggle its favorite status. Favorites track class names, so the same class can match at another trader. Up to 200 favorites and 50 recent purchase classes are retained in the local client profile. These filters only show items available in the current trader's catalog; they do not summon another trader's goods or bypass rotations.

Select an item, then enable **Compatible only** to find related catalog entries. Compatibility checks attachments in both directions, weapon magazines, loose ammunition, and ammunition boxes with recognized contents. Search/category filters still narrow results. Clear those filters when an expected compatible item seems missing.

Compatibility uses temporary preview objects. It helps find matching classes; it does not guarantee room in your actual weapon's occupied slots or account for every custom scripted mod restriction. Buy one and test before buying a large set.

## Read the selected offer

Purchase contents show requested objects or rounds, fill per item, required liquid, and included attachments. Do not assume the 3D preview includes a magazine, battery, or accessory in the price.

Loose-ammo quantity counts **rounds**; magazine and ammo-box quantities count **objects**. A loose-ammo sale can remove part of a stack and leave the remainder. Liquid-specific offers supply the named liquid and accept only matching non-empty containers. See [ammunition and liquid examples](ammo-liquids-and-purchase-contents.md).

Buy and sell totals are requested from the server for the selected quantity. Allow the quote to refresh after changing selection, quantity, or inventory. Sale details show value before deductions, quantity and condition adjustments, any applicable minimum, rounding, and the final payout. Dynamic pricing can charge successive units differently, so multiplying the first unit price by quantity can be wrong.

An item marked **Config error** is disabled by server configuration. Reducing quantity or adding money cannot fix it; give its class and trader location to an admin.

## Buying

Purchase succeeds only when:

- listing has positive buy price;
- trader is open;
- player remains within interaction distance;
- enough stock exists and listing is currently available under offer-pool rules;
- every required material is present and eligible to be consumed;
- player has enough selected currency;
- item can be delivered;
- every configured purchased attachment can be created.

Normal purchases go to player inventory. If inventory delivery fails, server may place item on surface at player position when `AllowGroundFallback` is enabled. Listing with `DeliveryMode: "ground"` always uses ground. Ordinary objects must be purchased one at a time; loose ammo can arrive in several stacks.

Vehicle purchase uses trader's first clear vehicle spawn point. It never goes into inventory. Read [vehicle guide](vehicles-keys-and-storage.md) before buying one.

!!! tip "Make space before expensive purchase"
    Inventory is tried first. With ground fallback enabled, item delivery, change, physical sale payout, and ATM withdrawal can appear at your feet when inventory is full. Secure spawned items immediately.

## Selling

Server finds exact configured class in full player inventory traversal, including hands and nested containers. It selects first valid matching items until requested quantity is reached.

Sellable item must:

- inherit `ItemBase`;
- match class name exactly;
- not be ruined;
- meet listing `MinimumHealthPercent`;
- contain no cargo in itself or nested attachment cargo;
- not have locked inventory and not sit under locked parent inventory;
- be removable from current inventory location.

Empty cargo before sale. Attachments themselves do not make parent ineligible, but server pays only parent listing and deletes attached items with sold parent. Remove magazines, optics, batteries, pouches, and other valuable attachments first.

When enabled, sell payout scales independently for each item by:

- health condition;
- magazine ammo fraction;
- electrical energy fraction; or
- quantity fraction.

Condition and quantity factors multiply. Quantity-priced objects are summed within their sale line and rounded down once, with no minimum percentage floor. Very small totals can round to zero and cannot be sold alone. Splittable quantity items remain quantity-priced even if the general quantity switch is off. Loose ammo is valued per round, with condition scaling but no stack-fullness penalty. See [pricing guide](settings-stock-and-pricing.md).

## Selling vehicles

Vehicle listing must have positive `SellPrice`. Sell exactly one by either route:

- packed keyed car: carry assigned key containing that exact stored vehicle; only recorded key owner can sell it;
- deployed car or boat: park exact class within 6 metres of one configured trader vehicle spawn point, empty crew, switch engine off, then sell at its listing.

Assigned car sale requires recorded key owner. Unassigned car or boat sale requires last player who started engine. Starting engine records driver; next driver who starts it becomes seller. Ruined vehicle or one below listing minimum health is rejected.

Sale deletes whole vehicle and everything inside/attached. Unload cargo, parts, and valuables first. Packed sale also consumes submitted key and stored file. See [vehicle sale details](vehicles-keys-and-storage.md#selling-vehicles).

## Sell all eligible

Use **Sell all eligible** for a server-generated preview of bulk cargo sales. The review scans this trader's catalog and the player's eligible inventory; it is not limited to the currently selected card or search results.

1. Put loot intended for sale into inventory cargo. Move wanted valuables out of the sale inventory before opening review.
2. Open review and read every class, object count, measured amount, and payout.
3. Cancel if any listed item should be kept. Adjust inventory, then request a fresh review.
4. Confirm within 60 seconds while remaining near the open trader.

Review excludes items in hands, worn/attached items, car keys, vehicles, configured currency classes, and objects with attachments. Cargo objects still need to pass normal ruin, health, nested-cargo, lock, and removability checks. An unattached spare item inside a backpack can be included even if it is valuable to you.

Review selects at most 100 objects per class/liquid line, 500 objects total, and the configured basket line limit. Loose-ammo lines also cap at 10,000 rounds and can select part of a stack. Stock capacity can further reduce the preview. A truncation notice means it is not all eligible loot. Duplicate class/liquid combinations use the first qualifying listing encountered, not automatically the highest-paying listing. Avoid overlapping unrestricted and liquid-specific buyback listings; distinct exact-liquid entries make selection clearer.

Object counts differ from contents: two partly loaded magazines are two objects, while measured quantity reports their combined rounds. Energy-bearing items show accumulated charge percentages; stack/quantity items show combined units.

Confirmation rechecks the same item objects, health, quantity, ammunition, energy, eligibility, and total price. Movement out of inventory, use, damage, a different liquid type, price changes, expiry, or catalog reload can invalidate review. Request another review instead of assuming the old payout remains reserved. Review does not reserve stock capacity or its quoted price.

!!! tip "Use a smaller selection for selective sales"
    Bulk review confirms its whole listed set. If a stock limit or an unwanted class prevents that sale, cancel, select fewer listings or reduce quantity, then use **Sell**.

## Required purchase materials

The selected listing can show required items as well as money. Each required object is consumed per purchased object, or per round for loose ammo; increasing quantity multiplies material requirements. A material need not be pristine, but it must be non-ruined, removable, and free of nested cargo and relevant locks. Empty it and remove attached valuables first.

## Selection, basket, and checkout

Click a card to select it; Ctrl-click cards to select several. The quantity field applies to each selected listing. Review all selected classes before using **Buy** or **Sell**.

- With an empty purchase basket, **Buy** submits the current selection immediately.
- **Sell** submits the current selection as a sale; it does not sell the contents of the purchase basket.
- **Add to Basket** collects the selected buyable listings and their quantities for a later purchase.
- **Remove from Basket** removes selected entries from that purchase basket.
- With a non-empty basket, **Buy** checks out the basket instead of buying the currently selected cards.
- Open the basket review to edit quantities or remove unwanted entries before checkout.
- **Sell all eligible** opens its separate server-generated bulk-sale review; it does not immediately sell everything.

One request contains buys or sells, never both, and uses one currency. Adding an existing purchase listing increases its quantity. UI basket holds at most 50 distinct entries; server can impose a lower `MaxBasketEntries` limit.

Each ordinary line allows up to 100 objects; loose-ammo lines allow up to 10,000 rounds. Ordinary ground-delivery and vehicle lines require quantity one. The object-work budget can reject a large transaction before the line limit: purchased objects, required ingredients, and configured attachments all contribute. Multi-selection sales cannot repeat the same class/liquid combination through different listing IDs. Different exact-liquid variants can use separate lines.

Checkout targets all-or-nothing completion. Server reserves stock and coordinates delivery, payment, ingredients, and sale escrow for the whole request. Failure triggers rollback. An unresolved rollback or interrupted transaction can require administrator recovery; do not keep retrying if recovery errors appear.

!!! tip "Check basket before pressing Buy"
    A basket assembled earlier takes priority over the current card selection. Use its review to verify classes, quantities, and total, especially before purchasing a vehicle or a material-cost item.

## Physical money and change

Default Euro notes stack up to 500 per object. Trader counts the number of notes multiplied by denomination value anywhere in inventory, including hands and nested storage. Ruined notes or notes containing attachments/cargo are not spendable.

Server chooses notes, can overpay with smallest suitable note, and creates exact change from configured denominations. Currency needs value-1 denomination so every integer amount can be represented.

## ATM use

Approach mapped `RaG_ATM` and use **Use ATM**. Choose enabled physical currency, enter amount, then deposit or withdraw.

- Deposit removes entered gross amount from wallet and credits amount minus deposit fee.
- Withdrawal gives entered amount in notes and debits entered amount plus withdrawal fee.
- Fees round up to next whole currency unit.
- **Deposit all** appears only when server allows it.
- ATM shows carried wallet and stored bank balance for selected currency.
- Withdrawal first tries inventory; with ground fallback enabled, notes that do not fit spawn at player position.
- Account balance persists across reconnects and restarts.

## Car keys

Hold unassigned `RaG_CarKey`, target unkeyed non-ruined car, and use **Assign car key**. Ordinary keys cannot clear their own assignment. Admins have a separate vehicle reset tool.

Matching key can:

- lock car when engine is off and no crew remains;
- unlock car;
- pack stopped, engine-off, crew-empty, non-ruined car into key storage when server enables packing;
- deploy packed car through hologram within 10 metres.

Craft spare by combining one assigned key with one unassigned key. Neither ingredient is consumed; assignment copies to blank key.

Lock blocks entering, opening outside doors, viewing or changing cargo, and changing attachments. Lock does not make vehicle indestructible. Keep spare key somewhere safe.

Read [vehicle, key, and storage details](vehicles-keys-and-storage.md) before packing valuable cargo.

## Receipts and failed transactions

Open **History** for the latest 50 successful trade receipts. Select one to inspect UTC time, location, currency, quantities, and line totals. A basket has one receipt. History does not undo trades or refund money.

If the server reports pending recovery, preserve the error and contact its admin with your player ID, approximate UTC time, trader, and intended purchase/sale. Check inventory and the ground before reporting missing delivery. Do not repeat a purchase blindly while its previous outcome is uncertain.
