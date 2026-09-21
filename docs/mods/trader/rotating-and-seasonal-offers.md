# Rotating and seasonal offers

Offer pools control which classes a trader exposes. Stock controls how much can be traded. Opening hours control when a physical trader accepts customers. Combine these controls for specialist shops, seasonal goods, and scheduled markets.

## Choose the right control

| Goal | Configuration | Scope |
| --- | --- | --- |
| Ten rifles across a network | `InitialStock: 10`, `MaxStock: 10` on a shared listing | Everyone using the listing ID. |
| Return two rifles every half hour | Positive restock amount and interval | Shared listing, during server uptime. |
| Show two of five rifles | `OfferPools` on the trader profile | Every location using that profile. |
| October event goods | Pool `Months: [10]` | Real UTC month. |
| Night-only dealer | Location opening hours | DayZ world hour. |
| Independent northern and southern supply | Separate category files | Separate listing identities. |

Traveling markets add another availability layer: the group must be present, its schedule open, and its stop/category/direction rules satisfied. See [routes](traveling-traders-and-routes.md).

Stock is communal supply. It does not impose a personal daily or weekly allowance. Individual progression or player-specific purchase restrictions require a companion script using the [transaction hooks](catalog-and-listings.md#custom-scripted-possibilities).

## Three clocks

- Opening hours use DayZ world time, including time acceleration.
- Offer rotations and seasonal months use real UTC calendar time.
- Automatic restock uses elapsed server uptime. Restart starts a new timer; offline time does not replenish stock.

Rotation windows are fixed UTC boundaries, not time since first visit. Restarting within the same window selects the same offers. Changing the DayZ world date does not activate a real-December pool.

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

Classes outside all pools stay available normally. Classes in an inactive slot or outside their pool's months are hidden from the item list and rejected server-side for **both buying and selling**. Pool rotation leaves stored stock intact.

!!! tip "Keep essential supplies outside pools"
    Rotate rare rifles, specialist tools, or event goods. Leave basic food, medicine, and blank car keys continuously available if players rely on them. For reliable resale, provide a separate buyback profile without the rotating restriction.

### Seasonal design

Set `Months: [10]` for October, `[12]` for December, or `[12, 1, 2]` for a winter window. Set `ActiveOffers` equal to pool size when every listed seasonal item should appear together.

Months gate the pool; they do not reset its stock at season start. Reusing the same category retains its listing IDs and persisted stock. Plan restocking separately.

## Build a dependable buyback route

An inactive offer blocks both purchase and sale of that class at the profile. To let players sell yesterday's rotation item, expose a separate sell-only category at another profile without that pool. Give that buyback listing a deliberate resale price and usually unlimited stock.

For example, the rotating arms dealer can offer three rare rifles while a recycling trader continuously buys those same classes. Shared categories would also share prices and stock, so use a dedicated buyback category when the policy differs.

## Control the rotation sequence

Array order determines consecutive selections. With two active offers, adjacent entries appear together. Spread similar high-value weapons through the array if each window should have variety. Separate pools can ensure a weapon, a tool, and an event item rotate independently, provided no class appears in more than one pool at the same profile.

Changing only a pool ID or giving another profile the same ordered pool and interval does not create a random offset: the selection formula uses UTC hour, interval, and array position. To offset a second dealer, reorder its class array or choose a different interval. To make independent supplies, also give it separate category files.

## Test an event window

1. Confirm every pool class exists in a category referenced by the profile.
2. Temporarily use `Months: []` and `ActiveOffers` equal to pool size to verify prices, previews, purchase delivery, and buyback.
3. Set the desired active count, interval, and months.
4. Check current real UTC month and hour when evaluating the result.
5. Check the next rotation boundary with the menu reopened. Confirm inactive classes cannot be traded.
6. Inspect stock separately. Making a class visible does not refill it.

Keep essentials, vehicle keys, and emergency repair items outside rotations when players must always be able to obtain them. An event's availability schedule is not its economic budget: use finite stock, restocking, prices, and consumed materials to control supply.
