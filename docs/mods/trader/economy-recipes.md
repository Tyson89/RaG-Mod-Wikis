# Economy recipes and testing

Add these listing fragments to a category's `Listings` array. Reference that category from the intended profile in `Trading/Catalog.json`. Choose prices and supply for your server.

## Finite essentials

```json
{
  "ClassName": "BandageDressing",
  "BuyPrice": 50,
  "SellPrice": 10,
  "InitialStock": 5,
  "MaxStock": 20,
  "RestockAmount": 2,
  "RestockIntervalSeconds": 1800
}
```

The shop starts with five units. Ordinary restock adds two every 30 minutes of server uptime, up to twenty. Player sales can also refill stock. Set both stock values to `-1` for an unlimited essentials shop.

## Player-supplied stock

```json
{
  "ClassName": "Hatchet",
  "BuyPrice": 300,
  "SellPrice": 80,
  "InitialStock": 0,
  "MaxStock": 20,
  "MinimumHealthPercent": 40.0
}
```

The first unit becomes available after a player sells one. Stock stores counts, and buyers receive items with the configured purchase contents. For trades of the actual submitted item and contents, use the [player market](player-market-server.md).

## Money plus materials

```json
{
  "ClassName": "NailBox",
  "BuyPrice": 120,
  "SellPrice": -1,
  "RequiredItems": ["MetalWire", "MetalWire"]
}
```

Each box costs 120 plus two separate eligible pieces of wire. Buying three boxes needs six pieces. Test missing and locked materials as well as the successful purchase.

## Regional and traveling shops

Reuse the same category for shared stock. Give regional shops separate categories to keep independent counts and prices. For a traveling merchant, use `StockMode: "route"` to carry supply between stops or `"stop"` to track separate stock at each stop. Set `RestockOnArrival` for new supply on arrival. See [route stock](traveling-traders-and-routes.md#stock-sharing-and-arrival-deliveries).

For an event, use a route schedule or [seasonal offer pool](rotating-and-seasonal-offers.md). Static shop opening hours use the DayZ world clock. Offer pool months use UTC.

## Test the economy

1. Buy and sell using an ordinary player account. Compare balances, stock, contents, and receipts.
2. Test purchase and resale loops across every shop that shares the same goods. Include ammo boxes, loaded magazines, attachments, and the extremes of dynamic pricing.
3. Test full inventory, blocked vehicle points, missing materials, and a basket with an invalid line.
4. Check limited stock with two players. Restart and verify stock, balances, and stored vehicles remain consistent.
5. If you enable P2P buy orders or virtual garages, test a wanted-order refund and a store-and-retrieve cycle with the intended server mod set.
