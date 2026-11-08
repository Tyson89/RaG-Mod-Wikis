# P2P Trader

Choose **Player market** at a market board. Everyone on the server shares the same market across boards. Buying a sale listing uses the configured account balance. For a banked currency such as Euro, deposit cash at an ATM first. Wanted orders can also use cash.

## Buy and collect

1. Open **Browse** and search by item name or class. Use category, sort, and page controls to narrow the results.
2. Select an offer and inspect its price, condition, quantity, ammo, liquid, attachments, or cargo where applicable.
3. Confirm the purchase. The market debits your balance and holds the item for pickup.
4. Open **Purchased** and select **Collect item** at a board. Make space for the entire item and its contents.

Browse supports minimum/maximum price and condition filters, plus newest, cheapest, or best-condition sorting. Results have up to 40 offers per page. Inspect included contents before paying: quantity, rounds, charge, liquid, wetness, temperature, frozen status, and food stage may matter as much as health. Contents inspection has separate page and depth controls. Read any incomplete-preview or unavailable-inspection message.

Collection requires inventory space; the market does not use the shop's ground fallback. A successful purchase reserves the item for you until collection.

## List and sell

1. Choose **List item** and select an eligible item from your inventory.
2. Enter your asking price for the whole item. Check the listing fee, commission, and expected payout, then choose **Post listing** to confirm.
3. Use **My listings** to edit an active asking price or cancel a listing. Successful sales normally credit your account automatically, even while offline. **Collect proceeds** retries a pending payout if shown.
4. Cancelled and expired listings go to **Returns**. Collect your item there or relist it directly if it still meets market rules.

Listing stores the actual item and removes it from your inventory. Check any attached or packed gear before you confirm. A stack or partly filled container trades as one item with its current contents.

Posting can charge a nonrefundable listing fee. Commission reduces the final payout. Editing an active price leaves its expiry timer running; directly relisting a returned item starts a fresh timer without another listing fee. If server policy changed and relisting fails, collect the item, adjust its contents, and create a new eligible listing.

## Wanted orders

If your server enables buy orders, select **Create wanted order**. Pick the exact item class, set your offer, and specify any minimum condition, quantity, liquid, ammo, or contents requirements. With a physical currency, the market reserves the full offer from your carried cash if you have enough. Otherwise it takes the full amount from your account. Account currencies always use their account balance.

To fill an order, select a wanted offer in **Browse** and choose a matching item from your inventory. Check the net payout and confirm delivery of the whole item. The requester collects it under **Purchased**.

- **Account-funded order**. The supplier receives the payout in their account. Cancelling or expiring an unfilled order returns the reserved balance to the requester.
- **Cash-funded order**. The supplier chooses **Collect cash** under **Purchased**. For a cancelled or expired unfilled order, the requester chooses **Collect cash** under **Returns**. Leave room in your inventory for the money.

If a purchase, claim, or order shows a recovery message, keep the receipt or listing details and contact an admin before trying the operation again.

## Wanted-order requirements

One order buys one whole item of the exact class. It does not combine several smaller stacks or several items to meet a minimum, and it does not accept a different subclass automatically. Leave unnecessary requirements at zero or unrestricted. Server allow/deny, condition, attachment, and cargo policies still apply.

- **Condition**: minimum health percentage, `0–100`, also subject to the server's minimum.
- **Quantity**: minimum native item quantity, up to `1000000`; magazines use ammunition requirements instead.
- **Liquid**: optional liquid type and minimum native fill quantity, up to `1000000`; the supplied container must match both.
- **Ammunition**: minimum rounds in a magazine or ammunition item, up to `1000000`, subject to that item's actual capacity.
- **Attachments and cargo**: require empty contents or allow contents. Allowing contents does not require any particular attachment and does not override server restrictions.

The full item and any accepted contents pass to the requester. If you want to retain extra contents or excess stack quantity, remove or split them before fulfilling. Cash and bank funds are never combined for one order: enough carried cash selects cash funding; otherwise the full reserve must come from the account.

See [P2P server setup](player-market-server.md) for board placement and market rules.
