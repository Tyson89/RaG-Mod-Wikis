# Player guide

## Open a trader

Approach a configured NPC or object and use **Trade**. Stay in range through checkout. A static trader can follow DayZ world opening hours. A traveling trader trades only while present and may stop buying or selling before departure. Check the timer and any stop-specific prices, currencies, or categories.

## Find items

Browse categories or search by item name or class. Use **Search all categories** to search this trader's catalog across categories. Middle-click a card to inspect it. Favorite items and recent purchases help you find the same classes at another trader that offers them.

Select an item and use **Compatible only** to find related attachments, magazines, or ammunition. Clear search or category filters if you expect more matches. Use [clothing try-on or the weapon builder](shopping-tools.md) to preview a purchase.

Check stock, quantity, currency, and the selected offer's purchase contents. Loose ammunition trades by the **round**. Boxes and magazines trade by the **object**. Dynamic pricing and sale condition can change the total, so read the quote for the full selection. See [ammo, liquids, and contents](ammo-liquids-and-purchase-contents.md).

## Buying

Select a listing and quantity, then choose **Buy**. For banked physical currency, choose **Pay: Cash** to spend carried money or **Pay: Bank** to spend the stored balance. Account currencies use their balance automatically.

A purchase can require materials in addition to money. The trader consumes the listed materials for each item bought, or for each round of loose ammo. Check included attachments and fill level before paying.

Purchases normally go into inventory. A ground-delivery listing goes directly to the ground. With ground fallback enabled, inventory overflow, change, and physical payouts can also appear at your feet. Vehicles spawn at the dealer's vehicle point.

## Selling

Select the listing and quantity and choose **Sell**. The trader looks for eligible items of the exact class in your carried inventory. Remove valuable attachments first. A normal sale pays for the listed item and removes the attached items with it. Empty its cargo and any cargo in attachments.

Sale value can depend on condition, ammo, charge, liquid, or stack quantity. Ruined items and items below the listing's health threshold are ineligible. Finite stock must have room for what you sell. Physical-currency sales pay in cash even if you bought from the bank.

For vehicles, see [selling vehicles](vehicles-keys-and-storage.md#selling-vehicles).

## Sell all eligible

**Sell all eligible** opens a server-generated review of eligible cargo across the current trader's catalog. It excludes items in hands, worn items, keys, vehicles, currency, and items with attachments. Check every line, measured quantity, and payout. Cancel if the list contains anything you want to keep.

Confirm within 60 seconds while still in range. The server rechecks the same items and price. If anything changed, request a fresh review. The review can be capped by stock, basket size, and item limits.

## Selection, basket, and checkout

Ctrl-click to select several listings. The quantity field applies to each selected listing. **Add to Basket** saves selected items for purchase, and the basket review lets you edit quantities or remove lines.

- With an empty basket, **Buy** submits the selected listings.
- With a filled basket, **Buy** checks out the basket.
- **Sell** uses the current selection. **Sell all eligible** has its own review.
- Each checkout uses one trade direction and one currency. The interface supports up to 50 basket lines, subject to the server limit. Vehicles and ordinary ground-delivery listings allow one object per line.

## Banking, market, and storage

- Use an ATM to [deposit, withdraw, or transfer](banking-and-currencies.md) banked physical currency.
- Open the [player market](player-market.md) at a market board to buy, list, or collect items and use wanted orders when enabled.
- Use the meter at a [virtual garage](vehicles-keys-and-storage.md#virtual-garage) to store or retrieve a vehicle.

## Receipts and failed transactions

Open **History** at a trader or ATM for your last 50 receipts. Select a receipt and use **Copy** to share its details. One trader basket has one receipt with separate lines.

If the result is unclear, check inventory, nearby ground, balances, and History. For a recovery message, give the server admin the receipt or operation details and wait before sending the same request again.
