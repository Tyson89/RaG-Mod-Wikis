# Rotating and seasonal offers

Use `OfferPools` on a trader profile in `Trading/Catalog.json` to show a subset of its classes or make offers seasonal. The profile's category files still define prices, stock, and purchase requirements.

Add this fragment to the profile. Each class must appear in a category referenced by that profile.

```json
{
  "OfferPools": [
    {
      "Id": "winter_rifles",
      "ClassNames": ["AKM", "M4A1", "FAL"],
      "ActiveOffers": 2,
      "RotationHours": 24,
      "Months": [12, 1, 2]
    }
  ]
}
```

| Field | Effect |
| --- | --- |
| `Id` | Unique pool ID within the profile. |
| `ClassNames` | Ordered list of 1–1000 classes. A class can appear in one pool per profile. |
| `ActiveOffers` | Number of consecutive classes active at once, from 1 to pool size. Defaults to 1. |
| `RotationHours` | Duration of a window, from 1 to 8760 hours. Defaults to 24. |
| `Months` | Calendar months 1–12. An empty list allows all months. |

The selection advances one position each window and wraps around the list. The example cycles through pairs of rifles during December, January, and February. The current window uses UTC, so restarting within the window keeps the same selection. Set `ActiveOffers` to the pool size to show every class during the selected months.

An inactive class is unavailable for buying and selling at that profile. Keep a separate unrestricted buyback profile if players need to sell it year-round. Rotation changes availability. Stock and restock still follow the listing and any route rules.
