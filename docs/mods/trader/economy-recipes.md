# Economy recipes and private testing

Examples below are design starting points, not bundled prices or promises of balance. Add listing objects inside a category's `Listings` array, reference its filename from a trader profile, and bind that profile in `Locations.json`.

Keep examples in separate custom categories. This makes it easier to review prices, avoid duplicate classes, and remove an experiment without dismantling the main catalog.

## Reliable essentials with individual limits

Goal: keep medicine available without one player draining the market.

Save as `Categories\Clinic.json`:

```json
{
  "DisplayName": "Clinic",
  "Listings": [
    {
      "ClassName": "TetracyclineAntibiotics",
      "BuyPrice": 300,
      "SellPrice": -1,
      "Stock": -1,
      "DailyBuyLimit": 2,
      "WeeklyBuyLimit": 8,
      "SpawnFullQuantity": true
    }
  ]
}
```

Add `"Clinic"` to the chosen profile's `Categories`. If that profile already exposes this class through `Medical`, remove the duplicate route or apply the same quotas there. An unrestricted duplicate defeats the intended limit.

Unlimited stock guarantees shared supply; quotas limit each player. Two purchases mean two medicine objects, not two doses. Sell disabled prevents the same shop paying players for these supplies. Check other traders before assuming resale is impossible.

## Finite emergency reserve

Goal: a small reserve replenishes during uptime.

```json
{
  "ClassName": "Morphine",
  "BuyPrice": 250,
  "SellPrice": 60,
  "Stock": 12,
  "RestockAmount": 2,
  "RestockIntervalSeconds": 1800,
  "DailyBuyLimit": 3
}
```

With automatic restock enabled, up to two objects return every thirty minutes, capped at twelve. Stock persists across restarts. A restart does not grant twelve more. New timers begin at startup, so test this against actual restart cadence.

At full stock, the shop cannot buy another Morphine from a player. If always-available buyback matters, use an unlimited sell-only listing at a separate buyback profile; then check its price and quota alongside every purchase route.

## Hunting income with shared bonus

Goal: reward hunting, cap individual income, and give the first deliveries a bonus.

```json
{
  "ClassName": "BearPelt",
  "BuyPrice": -1,
  "SellPrice": 800,
  "Stock": -1,
  "MinimumHealthPercent": 50.0,
  "DailySellLimit": 3,
  "WeeklySellLimit": 12,
  "DemandQuantity": 20,
  "DemandBonusPercent": 50,
  "DemandResetHours": 24
}
```

Unlimited stock keeps buyback open. Quotas control player throughput. Demand rewards twenty objects across the shared listing each UTC day. With default condition pricing, a half-health pelt receives half of its applicable base/bonus price; it is accepted because threshold is inclusive.

Test bonus exhaustion with two players. A quota is personal; demand remaining is communal. Do not describe twenty bonus slots as twenty per player.

## Money plus consumed materials

Goal: require scavenged resources as well as money for a tent.

```json
{
  "ClassName": "MediumTent",
  "BuyPrice": 1500,
  "SellPrice": -1,
  "Stock": 5,
  "DailyBuyLimit": 1,
  "RequiredItems": ["BurlapSack", "BurlapSack", "Rope"],
  "DeliveryMode": "inventory"
}
```

Purchase costs 1500 plus two separate burlap sacks and one rope. Required objects are consumed, including any attached equipment they carry when otherwise eligible. They are not reusable permits. Remove valuables first.

Required class matching is exact. Requirements need removable, non-ruined inventory items without nested cargo and without relevant inventory locks. There is no minimum input quantity or input health percentage beyond non-ruined status. A quantity stack is consumed as an entire object, so avoid stack ingredients when the intended cost is a precise count of units.

Buying two tents would require four sacks, two ropes, and 3000, but this example's daily limit prevents doing so in one day. Basket requirements are collected from inventory before purchases are delivered; buying the rope in the same basket does not provide that basket's ingredient.

!!! tip "Design voucher systems honestly"
    A dedicated token class can act as a consumable purchase voucher. `RequiredItems` cannot express a reusable membership card, reputation threshold, or zero-currency barter. Those behaviors require custom scripting. Keep a positive `BuyPrice` even when a voucher carries most of the economic value.

## Shared network or independent regional shops

For shared global supply, let north and south locations expose the same profile and category. Both see the same listing stock, demand, and profile-based player allowance.

For independent regional stock, create `North_Tools.json` and `South_Tools.json` with separate listings. The same `Hatchet` class gets IDs `north_tools_hatchet` and `south_tools_hatchet`, with independent stock and demand. Different profiles also give separate player quotas.

Travel-based commerce can use regional prices, but calculate maximum profit before enabling it. At 25% dynamic range, north base buy 300 can fall to 225; south base sell 220 can rise to 275. A 50% demand bonus can raise that sale to about 413 after rounding. That route pays players to shuttle purchases even without finding loot.

If trade-route income is intentional, constrain supply, quotas, travel risk, and reset frequency. If it is not, lower resale prices or remove the duplicate route.

## Night dealer and seasonal stock

Give a physical dealer `OpeningHoursEnabled: true`, `OpeningHour: 20`, and `ClosingHour: 6` for a DayZ-night shop. Add an offer pool to its profile for rotating rare items. Keep basic repair supplies outside that pool.

For seasonal offers, use real UTC `Months` in the pool. World winter and real December are different controls. Set `ActiveOffers` to the full pool size if all seasonal goods should appear together. An inactive pool blocks selling those classes there too.

Use separate profile IDs when different locations should have different rotations. Reusing a profile gives them the same deterministic selection.

## Vehicle dealer with clear ownership rules

Pair exact-class listings with `VehicleAttachments.json` profiles and several clear `VehicleSpawnPoints`. Sell ordinary blank `RaG_CarKey` separately. Vehicle purchases do not automatically supply or assign a key.

Choose policy deliberately:

- Buy-only dealer: `SellPrice: -1` prevents vehicle resale.
- Buyback dealer: positive sell price; explain ownership and the six-metre parking requirement.
- Persistent physical parking: `EnableVehiclePacking: false`; existing packed cars can still deploy.
- Portable owner garage: packing enabled, `RestrictVehicleStorageToOwner: true`.
- Shared-key garage: restriction false; any matching-key holder can pack/deploy, while sale ownership remains strict.

Packed cars sell without stored-condition scaling. Physical cars use condition pricing. A repair/resale economy must account for that difference. Disabling new packing alone does not remove already packed sale routes.

Test each sold vehicle with its actual attachments. Provide space for the largest truck, place boat spawn points on suitable water, and keep roads clear after purchase. A configured sale point is also a purchase point; vehicles parked there can block later deliveries.

## Physical cash or account credits

Physical currency creates looting and transport choices. Use denomination value 1 plus larger values, and decide whether full-inventory payouts may drop at players' feet. Put ATMs where players can reach them; ATMs are placed separately from trader locations.

Account currency avoids note inventory and change. Use one default account currency for trade, configure banking only for physical currencies or disable it, and plan how players first earn credits. Sell-only gathered goods can bootstrap an account economy without starting grants.

Do not make the first earning route require an item that can only be bought with credits the player cannot yet earn. Test from a new, empty account with no admin rewards.

## Private acceptance session

Use ordinary player accounts as well as an admin. Test with the exact server/client mod set intended for the private build.

| Test | What to verify |
| --- | --- |
| Fresh profile | Defaults generate, report has zero blocking errors, expected traders bind once. |
| New player | Can understand the first earning route and obtain the intended starter supplies. |
| Partial stacks | Bulk sale total uses quantity across the line; tiny separate trades do not undermine intended prices. |
| Required materials | Missing, ruined, full-container, and duplicated-input cases fail without charging; successful inputs are consumed. |
| Basket failure | One blocked item/vehicle line does not leave an unintended partial purchase, payment, or consumed material set. |
| Two buyers | Stock and demand are shared as intended; individual limits remain separate. |
| UTC boundary | Quotas, rotations, and demand follow calendar periods, not world time or reconnects. |
| Reload | Supported edits apply; rejected candidate leaves active configuration usable. |
| Full inventory | Delivery, change, bank withdrawal, and rollback behave under selected ground-fallback policy. |
| Restart | Stock, balances, quotas, demand, receipts, and stored vehicle links survive normal shutdown. |
| Key recovery | Admin key restrictions hold; vehicle reset invalidates old matching keys. |
| Safe-zone border | Incoming/outgoing protection, exit timer, survival settings, and custom mod actions match intended policy. |

Keep prices modest while checking correctness, then run longer economy sessions and inspect telemetry. Do not use an admin's successful unlimited checkout as evidence that player quotas work.
