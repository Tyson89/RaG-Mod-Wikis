# Player guide

## Open a trader

Approach a configured NPC or terminal and use **Trade**. Server checks configured `InteractionDistance` when opening catalog and again during checkout. Staying beside visible NPC is safest; walking away with menu open causes transaction failure.

Trader can also be closed by configured in-game opening hours. Hours use DayZ world time, not real server clock.

## Find items quickly

Trader UI supports:

- category selection;
- search by display name or exact class name;
- **All**, **Buyable**, **Sellable**, and **In stock** filters;
- **Sellable only**, which checks current player inventory;
- paged item cards;
- rotatable and zoomable 3D preview;
- current currency balance, stock, inventory load, prices, and item description.

**In stock** hides only listings at `0`. Unlimited stock displays as **Unlimited**.

### Useful search habits

- Search class fragment when translated display name is unclear.
- Enable **Sellable only** before clearing loot. It ignores ruined, locked, nested, and below-minimum-health items.
- Check quantity before clicking. Normal transaction allows up to 100 units, but ground-delivered items and vehicles allow exactly one.
- Sell price shown for quantity greater than one is combined preview total for matching inventory items, not a per-item price.

## Buying

Purchase succeeds only when:

- listing has positive buy price;
- trader is open;
- player remains within interaction distance;
- enough stock exists;
- player has enough selected currency;
- item can be delivered;
- every configured purchased attachment can be created.

Normal purchases go to player inventory. If inventory delivery fails, server may place item on surface at player position when `AllowGroundFallback` is enabled. Listing with `DeliveryMode: "ground"` always uses ground and must be purchased one at a time.

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

Condition and quantity factors multiply. Configured minimum payout percentage then sets floor. See [pricing guide](settings-stock-and-pricing.md).

## Selling vehicles

Vehicle listing must have positive `SellPrice`. Sell exactly one by either route:

- packed keyed car: carry assigned key containing that exact stored vehicle; only recorded key owner can sell it;
- deployed car or boat: park exact class within 6 metres of one configured trader vehicle spawn point, empty crew, switch engine off, then sell at its listing.

Assigned car sale requires recorded key owner. Unassigned car or boat sale requires last player who started engine. Starting engine records driver; next driver who starts it becomes seller. Ruined vehicle or one below listing minimum health is rejected.

Sale deletes whole vehicle and everything inside/attached. Unload cargo, parts, and valuables first. Packed sale also consumes submitted key and stored file. See [vehicle sale details](vehicles-keys-and-storage.md#selling-vehicles).

## Direct trade versus basket

Without **Basket mode**, Buy or Sell sends one listing immediately.

With **Basket mode**:

- one basket contains buys or sells, never both;
- all lines use same currency;
- adding same listing increases its quantity;
- UI holds at most 50 distinct lines;
- server can set lower limit with `MaxBasketEntries`;
- each line still has 100-unit transaction cap;
- one ground-delivery or vehicle line must have quantity `1`;
- sell basket cannot contain same item class through two different listing IDs.

Checkout is atomic. For buy basket, server reserves every stock line, creates every purchase, then takes total payment. For sell basket, it reserves stock capacity, secures every sale item in hidden vault, then pays. Failure triggers rollback.

!!! tip "Use basket for coordinated economy work"
    Basket prevents half-completed loadouts. Good for buying complete kits or selling several loot classes while keeping result all-or-nothing.

## Physical money and change

Default Euro notes are individual items. Trader counts valid notes anywhere in inventory, including hands and nested storage. Ruined notes or notes containing attachments/cargo are not spendable.

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

Hold unassigned `RaG_CarKey`, target unkeyed non-ruined car, and use **Assign car key**. Assignment is permanent.

Matching key can:

- lock car when engine is off and no crew remains;
- unlock car;
- pack stopped, engine-off, empty, non-ruined car into key storage;
- deploy packed car through hologram within 10 metres.

Craft spare by combining one assigned key with one unassigned key. Neither ingredient is consumed; assignment copies to blank key.

Lock blocks entering, opening outside doors, viewing or changing cargo, and changing attachments. Lock does not make vehicle indestructible. Keep spare key somewhere safe.

Read [vehicle, key, and storage details](vehicles-keys-and-storage.md) before packing valuable cargo.
