# Limits, rotating offers, and demand

These controls solve different economy problems. Stock controls shared supply; player limits control individual throughput; offer pools control availability; demand bonuses reward particular sales. They can be combined.

## Pick the right control

| Goal | Control | Scope |
| --- | --- | --- |
| Only ten rifles available across the market | `Stock: 10` | Listing ID, shared across traders and locations exposing it. |
| Each player buys at most one rifle per day | `DailyBuyLimit: 1` | Player + trader profile ID + normalized item class. |
| Show two of five rifles at once | Trader `OfferPools` | Trader profile, same selection at its physical locations. |
| Pay extra for the next twenty pelts | `DemandQuantity` and `DemandBonusPercent` | Listing ID, shared by all players and locations. |
| Open black market only at night | Location opening hours | Physical trader entry, DayZ world time. |

## Two clocks

| Feature | Clock |
| --- | --- |
| Opening and closing hours | DayZ world hour, including server time acceleration. |
| Daily quotas | Real UTC calendar day; reset at UTC midnight. |
| Weekly quotas | UTC day number divided into seven-day blocks; Monday UTC boundary. |
| Offer rotation | Real UTC hour number divided by `RotationHours`. |
| Seasonal offer months | Real UTC month, January `1` through December `12`. |
| Demand reset | Real UTC hour number divided by `DemandResetHours`. |
| Automatic restock | Elapsed server uptime; timers restart with the server. |

UTC rotations use fixed calendar boundaries, not time since first visit or server start. Restarting does not reroll offers or reset persisted quotas. Changing world date does not bring a real-December offer into season.

## Per-player trade limits

Add quota fields to a category listing:

```json
{
  "ClassName": "M4A1",
  "BuyPrice": 12000,
  "SellPrice": 3000,
  "Stock": 10,
  "DailyBuyLimit": 1,
  "WeeklyBuyLimit": 3,
  "DailySellLimit": 2,
  "WeeklySellLimit": 5
}
```

Every quota defaults to `-1`:

- `-1`: unlimited for that period and direction.
- `0`: blocks that trade direction through quota validation.
- Positive: maximum purchased or sold objects in the period.
- Values below `-1`: configuration error.

Daily and weekly limits both apply. With daily buy `1` and weekly buy `3`, a player can buy on three separate days, then must wait for the weekly reset. Selling does not refund purchase allowance; buy and sell counters are independent.

Limits count requested objects, not money, rounds, or stack contents. Buying one full magazine uses one allowance. Selling three partial stacks uses three. If daily allowance is two and request quantity is three, the request fails; server does not silently trim it to two.

### Sharing rules

Counter key is `<trader profile Id>/<trimmed lowercase ClassName>`, inside the player's limit file.

- Same profile at two locations: shared player allowance.
- Same class in two categories at one profile: shared counter when those listings have limits.
- Different trader profile: separate allowance, even when stock is shared.
- Different class variant: separate allowance.
- Duplicate listing with all relevant limits set to `-1`: does not enforce or increment that direction's quota.

!!! tip "Close duplicate-listing loopholes"
    Apply matching limits to every route selling the same class when the intended cap is per trader. A second unrestricted listing or separate profile gives players another route. Stock sharing alone does not create a server-wide player quota.

### Admin testing and persistence

`AdminBypassTradeLimits: true` lets `AdminSteamIds` bypass quotas. Use a non-admin test player, or set the bypass to `false`, when testing limits. Admin bypass does not grant free purchases or override stock, opening hours, offer availability, or vehicle ownership.

Limit files:

```text
$profile:\RaG_Core\Storage\RaG_Trader\Limits\<Steam64>.json
```

Allowance is reserved before completing a transaction, persisted, and released on ordinary rollback. Ambiguous journal/rollback failures can retain reservations for recovery. Do not delete the file to fix a generic checkout error: deletion grants fresh allowance and destroys evidence.

## Rotating and seasonal offers

`OfferPools` belongs inside a `Catalog.json` trader profile. Categories still define actual listings, prices, stock, and purchase requirements.

```json
{
  "Id": "weapons",
  "DisplayName": "Arms Dealer",
  "Categories": ["Assault_Rifles"],
  "OfferPools": [
    {
      "Id": "rifle_rotation",
      "ClassNames": ["AKM", "M4A1", "FAL"],
      "ActiveOffers": 1,
      "RotationHours": 24,
      "Months": []
    }
  ]
}
```

This is one profile object, not a complete catalog. All three classes must exist in categories referenced by that profile.

| Field | Default | Rules |
| --- | --- | --- |
| `Id` | Required | Non-empty and unique within the trader's pools. |
| `ClassNames` | `[]` | 1–1000 entries, each already listed at this trader. |
| `ActiveOffers` | `1` | Between `1` and pool size. |
| `RotationHours` | `24` | `1`–`8760`. |
| `Months` | `[]` | Empty means all year; otherwise values `1`–`12`. |

Maximum 64 pools per trader. A class cannot occur twice in the trader's offer slots, including across pools. Availability applies to every listing of that class at that profile.

### Selection behavior

Selection is deterministic, not random:

```text
first slot = floor(UTC hour number / RotationHours) modulo pool size
active slots = ActiveOffers consecutive entries, wrapping at end
```

With `[AKM, M4A1, FAL]` and two active offers, successive windows select `[AKM, M4A1]`, `[M4A1, FAL]`, then `[FAL, AKM]`. Which window is active now depends on UTC hour number; array position zero is not guaranteed at startup.

Classes outside all pools stay available normally. Classes in an inactive slot or outside their pool's months are hidden from the item list and rejected server-side for **both buying and selling**. Pool rotation does not replenish stock or erase quotas.

!!! tip "Keep essential supplies outside pools"
    Rotate rare rifles, specialist tools, or event goods. Leave basic food, medicine, and blank car keys continuously available if players rely on them. For reliable resale, provide a separate buyback profile without the rotating restriction.

### Seasonal design

Set `Months: [10]` for October, `[12]` for December, or `[12, 1, 2]` for a winter window. Set `ActiveOffers` equal to pool size when every listed seasonal item should appear together.

Months gate the pool; they do not reset its stock at season start. Reusing the same category retains its listing IDs and persisted stock. Plan restocking separately.

## Demand bonuses

Demand rewards the first configured number of sold objects, then returns to ordinary pricing. It does not force a trader to accept more stock than its configured capacity.

```json
{
  "ClassName": "BearPelt",
  "BuyPrice": -1,
  "SellPrice": 800,
  "Stock": -1,
  "MinimumHealthPercent": 50.0,
  "DailySellLimit": 3,
  "DemandQuantity": 20,
  "DemandBonusPercent": 50,
  "DemandResetHours": 24
}
```

Example prices, with dynamic pricing off and full-health pelts:

- First twenty pelts across all players: `800 × 1.5 = 1200` each.
- Later pelts in the same period: `800` each.
- Two bonus slots left, selling three: `1200 + 1200 + 800 = 3200`.
- Daily player quota still limits one player to three sales through that trader profile.

`DemandQuantity: 0` disables demand. Positive demand requires a positive sell price and bonus. `DemandBonusPercent` accepts `0`–`1000`; `DemandResetHours` accepts `0`–`8760`. Zero reset hours gives a persistent one-time demand allocation, not hourly resets.

Price sequence is stock-adjusted base price, demand bonus for eligible objects, optional custom price hook, then applicable condition/quantity scaling. Packed vehicle sales use their current base/demand price without reading stored condition. See [pricing](settings-stock-and-pricing.md#condition-and-quantity-sell-pricing).

Demand remaining is displayed beside listing status. A multi-item sale may mix bonus and ordinary prices; use its total rather than multiplying a displayed bonus unit price by every object.

### Persistence and failure handling

```text
$profile:\RaG_Core\Storage\RaG_Trader\Demand.json
```

Demand is keyed by listing ID. Sharing a category shares demand. Copying its class into another category creates separate demand. Restart retains fulfilled counts. Interrupted reservations are retained as fulfilled during initialization to prevent paying the bonus twice.

Invalid demand data or a failed save blocks demand-enabled sales instead of granting fresh bonuses. Existing corrupt main files are retained for investigation; the backup is not automatically substituted over an existing invalid main. See [recovery](administration-and-recovery.md).

!!! tip "Budget the bonus before enabling it"
    With base payout 800, bonus 50%, and twenty slots, the maximum extra payout for full-value sales is 8000 per period. Check every trader selling pelts or supplying ingredients. A demand reward must not make buying elsewhere and immediately reselling the easiest money source unless that trade route is intentional.
