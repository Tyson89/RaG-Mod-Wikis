# Settings, stock, and pricing

## `Settings.json`

Current default:

```json
{
  "Version": 1,
  "InteractionDistance": 3.0,
  "MaxBasketEntries": 50,
  "RequestCooldownMilliseconds": 250,
  "StockSaveIntervalMilliseconds": 5000,
  "EnableTradeLogging": true,
  "EnableAutomaticRestock": true,
  "EnableDynamicPricing": false,
  "DynamicPriceRangePercent": 25.0,
  "EnableConditionSellPricing": true,
  "EnableQuantitySellPricing": true,
  "MinimumSellPricePercent": 10.0,
  "AllowGroundFallback": true,
  "LockVehicleWheelsOnSpawn": false,
  "RestrictVehicleStorageToOwner": true,
  "AdminSteamIds": [],
  "StrictValidation": true,
  "RunCurrencyRegressionTests": false,
  "RunTransactionRegressionTests": false
}
```

## Settings reference

| Setting | Default | Actual behavior |
| --- | ---: | --- |
| `Version` | `1` | Must match current schema. |
| `InteractionDistance` | `3.0` | Server distance in metres for trader catalog/transactions and ATM transfers. Values below `1.0` become `1.0`. |
| `MaxBasketEntries` | `50` | Maximum distinct basket lines accepted by server, clamped `1`–`100`. Client UI itself caps at 50. |
| `RequestCooldownMilliseconds` | `250` | Per-player delay between accepted transaction/bank requests. Negative becomes `0`. |
| `StockSaveIntervalMilliseconds` | `5000` | Delay used to coalesce dirty stock writes. Minimum `250`. Final dirty state saves at shutdown. |
| `EnableTradeLogging` | `true` | Writes successful trades to dedicated `Trades` log. Failed trades are not audit entries. |
| `EnableAutomaticRestock` | `true` | Enables configured finite-listing restock timers. |
| `EnableDynamicPricing` | `false` | Changes both buy and base sell price from finite-stock ratio. |
| `DynamicPriceRangePercent` | `25.0` | Price swing, clamped `0`–`90`. |
| `EnableConditionSellPricing` | `true` | Multiplies sale payout by item health fraction. |
| `EnableQuantitySellPricing` | `true` | Multiplies payout by ammo, energy, or quantity fraction. |
| `MinimumSellPricePercent` | `10.0` | Floor after condition/quantity factors, clamped `0`–`100`. Final positive payout still at least 1. |
| `AllowGroundFallback` | `true` | Failed inventory purchase and physical-currency creation may spawn on surface at player position. Covers change, sale payout, deposit rollback, and ATM withdrawal. |
| `LockVehicleWheelsOnSpawn` | `false` | Calls slot lock on purchased vehicle wheel attachments. |
| `RestrictVehicleStorageToOwner` | `true` | Only recorded key owner or admin may pack/deploy. Does not restrict lock/unlock. |
| `AdminSteamIds` | `[]` | Steam64 IDs bypass storage ownership plus safe-zone weapon/build/explosive/speed rules. |
| `StrictValidation` | `true` | Any registry error prevents trader registry becoming ready. |
| `RunCurrencyRegressionTests` | `false` | Developer diagnostics at server initialization. Keep off in production. |
| `RunTransactionRegressionTests` | `false` | Developer diagnostics at server initialization. Keep off in production. |

## Transaction limits

Some limits are hardcoded:

- maximum quantity per transaction line: `100`;
- ground-delivery quantity: `1`;
- vehicle quantity: `1`;
- request lock timeout: `30,000` milliseconds;
- client basket: `50` distinct lines;
- server basket: `MaxBasketEntries`, up to `100`.

Raising `MaxBasketEntries` above 50 does not expand current UI basket. It only raises server validation ceiling for compatible clients/integrations.

## Stock model

Each listing has one stock ceiling in category file:

```json
{
  "Stock": -1
}
```

- `-1`: unlimited. Buying and selling do not change it.
- `0`: finite empty listing. Cannot buy; cannot sell because hard ceiling also zero.
- positive: startup maximum and persistent cap.

Finite stock transaction:

- buy subtracts quantity;
- sell adds quantity;
- sell fails if addition exceeds configured cap;
- transaction reserves stock before delivery/payment;
- failure attempts exact rollback.

Stock shared by derived listing ID. It is not per player, trader object, or location.

## `Stock.json`

Path:

```text
$profile:\RaG_Core\Configs\RaG_Trader\Stock.json
```

Typical file:

```json
{
  "Version": 1,
  "Entries": [
    { "ListingId": "tools_hatchet", "Stock": 8 },
    { "ListingId": "vehicles_civiliansedan", "Stock": 1 }
  ]
}
```

Runtime loader:

- restores valid main file;
- falls back to atomic backup when main invalid;
- drops duplicate/orphan listing IDs;
- normalizes invalid counts to configured listing stock;
- adds new listings at configured stock;
- stores unlimited as `-1`.

Do not hand-edit while server runs. In-memory map can overwrite changes.

### Intentional stock reset

1. Stop server.
2. Back up `Stock.json` and `.bak`.
3. Move both outside active directory.
4. Start server.
5. New state seeds from each listing's `Stock`.

## Automatic restocking

Example:

```json
{
  "ClassName": "TetracyclineAntibiotics",
  "BuyPrice": 250,
  "SellPrice": 80,
  "Stock": 20,
  "RestockAmount": 2,
  "RestockIntervalSeconds": 1800
}
```

Required rules:

- global `EnableAutomaticRestock: true`;
- `Stock > 0`;
- `RestockAmount > 0`;
- `RestockIntervalSeconds > 0` and at most `86400`;
- amount and interval either both enabled or both zero.

Restock adds amount toward configured cap. Timers begin at server initialization. Delayed in-session ticks catch up missed intervals. Restart creates fresh timer; no offline elapsed-time catch-up is stored.

!!! tip "Choose interval around restart cadence"
    If server restarts every three hours, six-hour timer may never fire. Use intervals shorter than normal uptime or rely on manual/event stock resets.

## Dynamic pricing

Only finite positive-stock listings use it. Unlimited stock keeps base price.

Formula:

```text
stockRatio = currentStock / configuredStock
multiplier = 1 + ((0.5 - stockRatio) * 2 * rangePercent / 100)
price = round(basePrice * multiplier), minimum 1
```

With `DynamicPriceRangePercent: 25`:

| Current stock | Multiplier | Base 100 becomes |
| ---: | ---: | ---: |
| full | `0.75` | `75` |
| half | `1.00` | `100` |
| empty | `1.25` | `125` |

Both buy and base sell price follow same stock multiplier. Price is calculated from stock before transaction. Successful result sends refreshed stock and refreshed prices to client.

Strong recommendation: keep buy price comfortably above sell price across full swing. For range `R`, rough anti-arbitrage guard is:

```text
minimum buy = BuyPrice × (1 - R)
maximum sell = SellPrice × (1 + R)
```

Require minimum buy greater than maximum sell, with extra margin for cross-category duplicates.

## Condition and quantity sell pricing

For each sold item:

```text
factor = 1
factor *= health fraction                 when enabled
factor *= ammo/energy/quantity fraction   when enabled
factor = clamp(factor, MinimumSellPricePercent / 100, 1)
payout = round(dynamic base sell price × factor), minimum 1
```

Example: base sell `200`, 60% health, half-full magazine, minimum 10%:

```text
200 × 0.60 × 0.50 = 60
```

If item were 10% health and 10% full, raw factor `1%`; 10% floor makes payout `20`.

`MinimumHealthPercent` controls whether item can be sold at all. It does not change price formula.

!!! tip "Avoid paying for empty consumables"
    Quantity scaling should stay enabled for ammo, batteries, food, liquids, and stack items. Otherwise empty and full items pay same.

## Request locking and cooldown

Server keeps one lock per player identity:

- simultaneous request returns busy;
- accepted requests update cooldown timestamp;
- stuck lock auto-expires after 30 seconds;
- disconnect clears cached request state.

Do not set cooldown too high. UI gives generic “Please wait” message for busy/cooldown.

## Trade logging

Successful buy/sell records:

```text
event=trade|result=0|type=buy|player=<id>|location=<group/trader>|trader=<id>|listing=<id>|currency=<id>|quantity=<n>|unitPrice=<n>|totalPrice=<n>|stock=<n>
```

Path pattern:

```text
$profile:\RaG_Core\Logs\RaG_TraderLogger\Trades_TRADE_YYYY-MM-DD.log
```

Only successful trades enter audit log. Bank transfers use normal Info logging, not trade channel. Error/Warning/Info paths follow [RaG Core logging](../core/logging-api.md).

Keep `EnableTradeLogging: true` on production economies. It is primary audit trail for disputes.
