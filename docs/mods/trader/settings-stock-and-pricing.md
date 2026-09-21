# Settings, stock, and pricing

## `Settings.json`

Current default:

```json
{
    "Version": 1,
    "InteractionDistance": 3.0,
    "MaxBasketEntries": 50,
    "StockSaveIntervalSeconds": 5,
    "EnableTradeLogging": true,
    "EnableEconomyTelemetry": true,
    "EnableAutomaticRestock": true,
    "EnableDynamicPricing": false,
    "DynamicPriceRangePercent": 25.0,
    "EnableConditionSellPricing": true,
    "EnableQuantitySellPricing": true,
    "MinimumSellPricePercent": 10.0,
    "AllowGroundFallback": true,
    "LockVehicleWheelsOnSpawn": false,
    "EnableVehiclePacking": true,
    "RestrictVehicleStorageToOwner": true,
    "AdminSteamIds": []
}
```

Bundled default enables `AllowGroundFallback`. If omitted from a hand-written settings file, script constructor defaults it to `false`; set it explicitly. Startup normalizes several numeric values below; live reload validates candidate values without that normalization.

## Settings reference

| Setting | Default | Actual behavior |
| --- | ---: | --- |
| `Version` | `1` | Must match current schema. |
| `InteractionDistance` | `3.0` | Server distance in metres for trader catalog/transactions and ATM transfers. Values below `1.0` become `1.0`. |
| `MaxBasketEntries` | `50` | Maximum distinct basket lines accepted by server, clamped `1`–`100`. Client UI itself caps at 50. |
| `StockSaveIntervalSeconds` | `5` | Coalesces dirty stock writes; minimum 1 second. Final dirty state saves at shutdown. |
| `EnableTradeLogging` | `true` | Writes successful trades to dedicated `Trades` log. Failed trades are not audit entries. |
| `EnableAutomaticRestock` | `true` | Enables configured finite-listing restock timers. |
| `EnableDynamicPricing` | `false` | Changes both buy and base sell price from finite-stock ratio. |
| `DynamicPriceRangePercent` | `25.0` | Price swing, clamped `0`–`90`. |
| `EnableConditionSellPricing` | `true` | Multiplies sale payout by item health fraction. |
| `EnableQuantitySellPricing` | `true` | Scales ordinary magazine, energy, or quantity-bearing items by fullness. Splittable quantity items always use quantity scaling. Loose ammo uses round counts instead. |
| `MinimumSellPricePercent` | `10.0` | Condition floor clamped `0`–`100` for items without quantity scaling, loose-ammo rounds, and stored vehicle condition pricing. No floor on quantity-scaled sale lines. |
| `AllowGroundFallback` | `true` | Failed inventory purchase and physical-currency creation may spawn on surface at player position. Covers change, sale payout, deposit rollback, and ATM withdrawal. |
| `LockVehicleWheelsOnSpawn` | `false` | Calls slot lock on purchased vehicle wheel attachments. |
| `RestrictVehicleStorageToOwner` | `true` | Only recorded key owner or admin may pack/deploy. Does not restrict lock/unlock. |
| `AdminSteamIds` | `[]` | Steam64 IDs bypass storage ownership plus safe-zone weapon/build/explosive/speed rules. |
| `EnableEconomyTelemetry` | `true` | Saves aggregate trade statistics, currency flow, and failures. See [administration](administration-and-recovery.md#economy-telemetry). |
| `EnableVehiclePacking` | `true` | Allows packing cars. When false, existing packed cars can still deploy. |

## Transaction limits

Some limits are hardcoded:

- ordinary quantity per transaction line: `100` objects;
- loose-ammo quantity per line: `10,000` rounds;
- ordinary ground-delivery quantity: `1`; loose ammo may deliver several stacks;
- vehicle quantity: `1`;
- request lock timeout: `30,000` milliseconds;
- object-work budget per ordinary checkout: `500`, including purchased objects, configured attachments, and consumed required items; sale checks count inventory hierarchies;
- client basket: `50` distinct lines;
- server basket: `MaxBasketEntries`, up to `100`.

Raising `MaxBasketEntries` above 50 does not expand current UI basket. It only raises server validation ceiling for compatible clients/integrations.

## Stock model

Each listing separates its starting supply from its storage capacity:

```json
{
  "InitialStock": 0,
  "MaxStock": 20
}
```

This shop starts empty and can accept twenty objects from players. Its first customer must sell before anyone can buy.

| InitialStock | MaxStock | Use |
| ---: | ---: | --- |
| `-1` | `-1` | Unlimited supply and buyback. |
| `0` | `20` | Empty player-supplied market or limited buyback counter. |
| `5` | `20` | Five objects available initially, with room for fifteen more. |
| `20` | `20` | Fully stocked shop; no buyback room until goods leave. |
| `0` | `0` | No supply or buyback capacity. |

Both fields must be `-1` for unlimited stock. Otherwise both must be nonnegative and `InitialStock <= MaxStock`. Counts mean rounds for loose ammo, objects for other listings. Set both fields explicitly in finite listings.

`InitialStock` seeds a missing listing; it does not refill an existing stock record on restart or reload. `MaxStock` is the capacity used by buyback checks, replenishment, and dynamic pricing.

Finite stock transaction:

- buy subtracts trade quantity: rounds for loose ammo, objects otherwise;
- sell adds quantity;
- sell fails if addition exceeds configured cap;
- transaction reserves stock before delivery/payment;
- failure attempts exact rollback.

Static shops and routes using `StockMode: "shared"` share stock by derived listing ID. Routes can instead keep separate stock per route/profile or per stop/profile; see [route stock](traveling-traders-and-routes.md#stock-sharing-and-arrival-deliveries). No mode gives each player a personal allowance.

## `Stock.json`

Path:

```text
$profile:\RaG_Core\Configs\RaG_Trader\Stock.json
```

Illustrative file with finite stock and its persisted identity map:

```json
{
  "Version": 1,
  "Entries": [
    { "ListingId": "tools_hatchet", "Stock": 8 },
    { "ListingId": "vehicles_civiliansedan", "Stock": 1 }
  ],
  "ListingIds": {
    "tools_hatchet||1": "tools_hatchet",
    "vehicles_civiliansedan||1": "vehicles_civiliansedan"
  },
  "RouteArrivals": {},
  "ScopedEntries": {}
}
```

Runtime loader:

- restores valid main file;
- falls back to atomic backup when main invalid;
- rejects malformed or duplicate persisted entries during file validation; valid orphan listing IDs are dropped;
- normalizes accepted counts outside the current listing range to configured capacity; values below `-1` make the persisted file invalid;
- adds new listings at `InitialStock`;
- keeps unlimited listings as `-1` in memory; saved entries cover finite listings.

`ScopedEntries` stores route/stop counts and capacities; `RouteArrivals` prevents repeated arrival deliveries. Preserve these maps together with `RouteState.json` when restoring a traveling economy.

Do not hand-edit while server runs. In-memory state can overwrite changes. Preserve `ListingIds` with counts: the identity map reserves assigned IDs for category/class/liquid occurrences, including unlimited listings. It is not a list of stock capacities.

### Intentional stock reset

1. Stop server.
2. Back up `Stock.json` and `.bak`.
3. Move both outside active directory.
4. Start server.
5. New state seeds from each listing's `InitialStock`.

## Automatic restocking

Example:

```json
{
  "ClassName": "TetracyclineAntibiotics",
  "BuyPrice": 250,
  "SellPrice": 80,
  "InitialStock": 20,
  "MaxStock": 20,
  "RestockAmount": 2,
  "RestockIntervalSeconds": 1800
}
```

Required rules:

- global `EnableAutomaticRestock: true`;
- `MaxStock > 0`;
- `RestockAmount > 0`;
- `RestockIntervalSeconds > 0` and at most `86400`;
- amount and interval either both enabled or both zero.

Ordinary automatic restock affects the shared listing stock. Separate `route` and `stop` stock uses arrival deliveries instead; its supply does not gain the ordinary uptime-based increments. `RestockOnArrival` is a separate route switch and can operate with `EnableAutomaticRestock: false`.

Restock adds amount toward configured cap. Timers begin at server initialization. Delayed in-session ticks catch up missed intervals. Restart creates fresh timer; no offline elapsed-time catch-up is stored.

!!! tip "Choose interval around restart cadence"
    If server restarts every three hours, six-hour timer may never fire. Use intervals shorter than normal uptime or rely on manual/event stock resets.

## Dynamic pricing

Only listings with finite positive capacity use dynamic pricing. For route stock, the effective scoped capacity applies, including a stop override. Unlimited stock keeps its base price. `DynamicPriceRangePercent` controls the swing around half stock.

```text
ratio = clamp(stock used for this unit / effective stock capacity, 0, 1)
multiplier = 1 + ((0.5 - ratio) × 2 × rangePercent / 100)
buy unit price = max(1, ceil(BuyPrice × multiplier))
sell base price = max(1, floor(SellPrice × multiplier))
```

A purchase uses stock **before removing each unit**. A sale uses stock **after adding each unit**. Multi-unit totals walk through stock one unit at a time. The first displayed unit price multiplied by quantity is not necessarily the checkout total.

At a 25% range, a full-stock purchase costs 75% of base, a half-stock purchase costs base, and a nearly empty purchase approaches 125%. Empty stock cannot supply a purchase. Selling into an empty shop starts one unit above zero; a sale that fills the shop uses the 75% multiplier.

### Worked multi-item purchase

For `InitialStock: 10`, `MaxStock: 10`, `BuyPrice: 100`, range 25%, and current stock 10:

```text
first object:  stock 10 → ceil(100 × 0.75) = 75
second object: stock  9 → ceil(100 × 0.80) = 80
third object:  stock  8 → ceil(100 × 0.85) = 85
total = 240; remaining stock = 7
```

Buying those three in one line or consecutively follows the same stock steps, provided nothing else changes stock between requests. Loose ammo follows these steps **per round**, even when delivery creates only one stack.

For a sale with `SellPrice: 40` and current stock 7, three pristine non-quantity items use stock 8, 9, and 10: `34 + 32 + 30 = 96`. Condition and quantity deductions apply after each applicable base price.

### Price-gap design

Check all purchase and resale routes, especially independent regional listings. A useful conservative bound is:

```text
lowest purchase base = BuyPrice × (1 - R)
highest resale base  = SellPrice × (1 + R)
```

Here `R` is a fraction: 25% means `0.25`. Keep the lowest purchase price above the highest resale value unless travel-based trade profit is intentional. Include supplied attachments, rounds inside magazines/boxes, crafted outputs, and custom price hooks. The validator's checks do not replace a complete economy audit.

## Condition and quantity sell pricing

`MinimumHealthPercent` decides whether an item may be sold. A value of 50 accepts an item at exactly 50% global health. Ruined items are rejected regardless of threshold. The global condition switch affects payment, not that eligibility threshold.

### Items without quantity scaling

For an ordinary eligible item without active quantity scaling:

```text
health factor = health fraction when EnableConditionSellPricing is true, otherwise 1
factor = clamp(max(health factor, MinimumSellPricePercent / 100), 0, 1)
payout = max(1, floor(applicable base sell price × factor))
```

A Hatchet with base sell 120 and 60% health pays 72 at fixed pricing. With a 10% minimum, a non-ruined 5%-health item pays at the 10% floor if its listing health threshold allows it.

### Magazines, energy, and quantity-bearing items

Quantity scaling uses magazine ammo divided by maximum, electrical energy divided by maximum, or quantity divided by maximum. Magazine ammo takes priority over energy; energy takes priority over ordinary quantity.

It applies when `EnableQuantitySellPricing` is true. A quantity-bearing class with `canBeSplit` also uses it when the setting is false. This prevents splitting a partly filled object into several full-value sales.

```text
raw value per object = applicable base sell price × health factor × fullness
line payout = floor(sum of raw values)
```

There is **no minimum percentage floor** on these quantity-scaled values and no automatic minimum-one payout. A line that rounds to zero cannot complete as a direct sale and is omitted from bulk review. Empty contents contribute zero.

At fixed base sell 200:

- One magazine at 60% health and 50% ammo: `200 × 0.60 × 0.50 = 60`.
- One magazine at 10% health and 10% ammo: `200 × 0.10 × 0.10 = 2`.
- Three of the latter together: `floor(2 + 2 + 2) = 6`.
- Two objects worth 0.6 each in the same line: `floor(1.2) = 1`; separately, each rounds to zero.

Condition scaling can be disabled independently. Fullness still matters when quantity scaling applies. A cheaper partially filled purchase should be compared against its actual resale contents, not a full object's nominal price.

### Loose ammunition and stored cars

Loose ammo is valued by exact rounds sold, not stack fullness. The condition factor and configured condition minimum apply to the source stack; per-round values are summed and rounded down at the end. Unsold rounds remain in their original stack. See [round examples](ammo-liquids-and-purchase-contents.md#loose-ammunition-trades-per-round).

Stored-car pricing reads saved global health. With condition pricing enabled, it applies that fraction and the minimum percentage to the base sell price, then rounds down with a minimum of one. A stored car must independently meet the listing health threshold. See [vehicle sales](vehicles-keys-and-storage.md#selling-vehicles).

!!! tip "Use the sale breakdown"
    The UI's server quote explains value before deductions, quantity deduction, condition deduction, any applicable minimum adjustment, rounding, and the final amount. Use that total when testing. Stock, inventory, and prices can change before checkout, so a quote is not a reservation.

## Request locking and cooldown

Server keeps one lock per player identity:

- simultaneous request returns busy;
- accepted requests update cooldown timestamp;
- stuck lock auto-expires after 30 seconds;
- disconnect clears cached request state.

Accepted transaction and bank requests use a fixed 250-millisecond per-player cooldown. It is not a settings field. UI gives a generic “Please wait” message for busy/cooldown; wait for the current result before retrying.

## Trade logging

Successful buy/sell records include player name and Steam64 ID, bought/sold direction, item name/class, trade quantity, currency, total and unit price, trader/location, remaining stock, and listing ID. Loose-ammo quantity is rounds. Multi-unit dynamic totals need not equal the first unit price multiplied by quantity.

Path pattern:

```text
$profile:\RaG_Core\Logs\RaG_TraderLogger\Trades_TRADE_YYYY-MM-DD.log
```

Only successful trades enter audit log. Bank transfers use normal Info logging, not trade channel. Error/Warning/Info paths follow [RaG Core logging](../core/logging-api.md).

Keep `EnableTradeLogging: true` on production economies. It is primary audit trail for disputes.
