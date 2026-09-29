# Economy recipes and testing

These examples are design starting points, not bundled prices or a promise of balance. Put listing objects inside a category's `Listings` array, reference that filename from a trader profile, and bind the profile in `Locations.json`. Category examples include their wrapper; listing fragments do not replace a whole file.

Start with a few intentional shops. A smaller catalog with clear earning routes is easier to balance than selling every available class.

## Choose an economy pattern

| Server design | Useful controls | Main test |
| --- | --- | --- |
| Accessible survival supplies | Unlimited buy-only essentials | Players can earn their first purchase without already owning paid gear. |
| Scarce military equipment | Finite stock, slow restock, rotating offers | Alternative routes do not flood the market. |
| Hunting or scavenging income | Sell-only categories, health thresholds | Renewable loot and crafting yield acceptable income. |
| Materials-based progression | Positive money price plus consumed `RequiredItems` | Inputs exist before checkout and are consumed correctly. |
| Regional trade routes | Separate category identities and prices | Maximum travel profit is intentional. |
| Fuel and fluid trade | Exact `RequiredLiquidType`, fill settings | Container and contents are valued together. |
| Portable owner garage | Keys, packing, owner restriction | Spares, ownership, and persistence work. |
| Cashless trade | Default account currency | New accounts have a reachable earning route. |

## Reliable essentials

Goal: keep medicine continuously purchasable.

Save as `Categories\Clinic.json`:

```json
{
  "DisplayName": "Clinic",
  "Listings": [
    {
      "ClassName": "TetracyclineAntibiotics",
      "BuyPrice": 300,
      "SellPrice": -1,
      "InitialStock": -1,
      "MaxStock": -1,
      "SpawnFullQuantity": true
    }
  ]
}
```

Add `"Clinic"` to the chosen profile's `Categories`. This sells one full medicine object per quantity unit, not one dose. Unlimited stock prevents shared depletion; it does not cap an individual's purchases.

Sell disabled prevents this listing buying the medicine back. Check other profiles for cheaper purchase or profitable resale routes. Keep essentials outside offer pools when players need dependable access.

## Finite emergency reserve

Goal: replenish a small communal supply during uptime.

```json
{
  "ClassName": "Morphine",
  "BuyPrice": 250,
  "SellPrice": 60,
  "InitialStock": 12,
  "MaxStock": 12,
  "RestockAmount": 2,
  "RestockIntervalSeconds": 1800
}
```

With automatic restock enabled, up to two objects return every thirty minutes, capped at twelve. Long-run supply is up to four objects per hour while below capacity. Players can buy the whole reserve; stock is not a personal allowance.

Stock persists across restarts. Restart does not grant twelve more, and restock timers begin again at startup. Choose an interval shorter than normal uninterrupted server uptime.

At full stock, another player sale is rejected. For continuous buyback, add a separate unlimited sell-only listing with a deliberate price. Restocking adds goods and consumes buyback capacity; it never empties the shop to create room for sales.

## Hunting and scavenging income

Goal: make found loot a dependable currency source.

```json
{
  "ClassName": "BearPelt",
  "BuyPrice": -1,
  "SellPrice": 800,
  "InitialStock": -1,
  "MaxStock": -1,
  "MinimumHealthPercent": 50.0
}
```

Unlimited stock keeps buyback open. At fixed prices with condition pricing enabled, a pristine pelt pays 800 and one at exactly 50% health pays 400. Lower health fails eligibility. Check actual quantity behavior before extending the pattern to meat, fish, food, or stackable goods.

Expected finds per hour multiplied by expected condition-adjusted payout gives an approximate income rate. Include farming, crafting, animal density, travel, and alternative sale routes. Compare estimates with [telemetry](administration-and-recovery.md#economy-telemetry).

For account currency, a reachable sell-only scavenging shop provides the first credits. Do not require an earning item obtainable only by spending credits the player cannot yet earn.

## Money plus consumed materials

Goal: require scavenged materials as well as cash for a tent.

```json
{
  "ClassName": "MediumTent",
  "BuyPrice": 1500,
  "SellPrice": -1,
  "InitialStock": 5,
  "MaxStock": 5,
  "RequiredItems": ["BurlapSack", "BurlapSack", "Rope"],
  "DeliveryMode": "inventory"
}
```

At fixed pricing, one tent costs 1500 plus two separate burlap sacks and one rope. Two tents need 3000, four sacks, and two ropes. Ingredients must already exist before checkout; buying rope in the same basket does not provide that basket's ingredient.

Required objects must be non-ruined, removable, free of nested cargo, and not blocked by inventory locks. They are consumed whole. There is no requirement-specific stack-unit count, fullness, or health threshold beyond non-ruined status. Remove attached valuables first: an eligible parent input can consume its attachments too.

A dedicated token can act as a consumed voucher. Reusable membership cards, reputation gates, or free barter need scripting. Keep a positive buy price for money-plus-material transactions.

!!! tip "Keep ingredients readable"
    Prefer a few clearly named non-stack objects. Large ingredient lists make checkout harder to understand and count toward the 500-object work budget. On loose-ammo listings, ingredients multiply per round, not per delivered stack.

## Ammo counter

Goal: sell exactly the rounds a player needs.

```json
{
  "ClassName": "Ammo_308Win",
  "BuyPrice": 20,
  "SellPrice": 5,
  "InitialStock": 600,
  "MaxStock": 600,
  "RestockAmount": 60,
  "RestockIntervalSeconds": 1800
}
```

With dynamic pricing off, quantity 30 costs 600 and consumes 30 stock. It supplies 30 rounds across normal stack capacity. A partial sale leaves unsold rounds in inventory.

Price every box and loaded magazine yielding these rounds. Cheap boxes plus expensive round buyback can create repeatable profit. See [ammo calculations](ammo-liquids-and-purchase-contents.md#price-boxes-magazines-and-rounds-together).

## Fuel depot

Goal: sell full gasoline canisters and buy matching partial canisters.

```json
{
  "ClassName": "CanisterGasoline",
  "BuyPrice": 600,
  "SellPrice": 120,
  "RequiredLiquidType": "Gasoline",
  "SpawnFullQuantity": true,
  "InitialStock": -1,
  "MaxStock": -1
}
```

One purchase supplies one full canister. One sale consumes a matching non-empty canister. With fixed pricing, full health, and quantity pricing, half capacity pays 60. Wrong-liquid or empty containers fail eligibility.

This is a container trade, not a refill station. Account for the reusable container and fuel availability elsewhere. Liquid matching does not check every contamination or quality state.

For different liquids, add combinations that pass container compatibility validation. Set `AllowDuplicate: true` on every intentional copy of a container class and use clear category labels. See [liquid-specific listings](ammo-liquids-and-purchase-contents.md#liquid-specific-listings).

## Equipment packages

Goal: sell an equipped weapon with predictable contents.

```json
{
  "ClassName": "M4A1",
  "BuyPrice": 4000,
  "SellPrice": 1400,
  "InitialStock": 5,
  "MaxStock": 5,
  "Attachments": [
    "M4_OEBttstck",
    "M4_PlasticHndgrd",
    "M68Optic",
    "M4_Suppressor"
  ]
}
```

This supplies the listed attachments. A magazine or battery is not supplied merely because the weapon or optic accepts one. Parent fill settings do not recursively fill attachments.

Selling an attached weapon pays only the weapon listing and deletes its attachments. Players should strip valuables first. Compare package buy price with the combined separate resale routes for the weapon and attachments.

Every attachment must fit an available slot. Invalid listing attachments disable that listing; actual delivery failure triggers rollback. Test one complete package before bulk purchase.

## Shared markets and regional shops

For shared supply, reference the same category from several profiles or reuse the same profile at multiple locations. All expose the same listing IDs and stocks.

For independent supply, create `North_Tools.json` and `South_Tools.json`. A Hatchet in each gets a separate identity and stock. A different physical location alone does not create another stock pool.

At 25% dynamic range, north base buy 300 can fall to 225 while south base sell 220 can approach 275. Independently stocked routes can therefore pay roughly 50 per object before discrete stock steps and rounding. Returns fall as purchases drain one stock and resale fills the other.

For intentional travel income, choose supply, restock, resale capacity, and travel risk accordingly. Otherwise widen the price gap or remove the duplicate route. Test round trips using actual player transport capacity.

## Player-supplied market

Goal: goods enter the market through player sales, with room for a finite supply.

```json
{
  "ClassName": "Hatchet",
  "BuyPrice": 300,
  "SellPrice": 80,
  "InitialStock": 0,
  "MaxStock": 20,
  "RestockAmount": 0,
  "RestockIntervalSeconds": 0,
  "MinimumHealthPercent": 40.0
}
```

The shop starts empty. One eligible sale adds one stock unit; another player can then buy it. No restock fills the shop automatically. `InitialStock` only seeds a missing stock record, so restarting does not erase the accumulated player supply.

For a permanent buyback counter that accepts at most twenty objects, set `BuyPrice: -1`. It stops buying from players when full. Adding restock would consume its remaining buyback room, not clear it; decide how that capacity should reopen before using this design as a long-term earning route.

Stock stores counts, not the sold physical item. Purchases use the listing's configured spawn contents and normal delivery logic. Do not describe this as a consignment market preserving a seller's exact item, condition, or attachments.

## Traveling economy designs

Use [traveling traders and routes](traveling-traders-and-routes.md) for complete route fields and copyable configurations.

- **Carried supply:** same trader profile across groups, `StockMode: "route"`, finite starting stock. A purchase at one town reduces the same merchant's supply at the next.
- **Regional supply:** `StockMode: "stop"`, distinct stop capacities and prices. Leave resale headroom with `InitialStock` below capacity.
- **Supply drops:** positive listing restock amount/interval, route `RestockOnArrival: true`, optional delivery delay. Disable global automatic restock if arrival should be the only automated supply source.
- **Relief market:** Medical-only stop, `AllowSelling: false`, modest batches, enough wait time for players to reach it after the announcement.
- **Cashless specialist:** account currency on its category; keep an accessible earning route. A stop-wide currency override can replace that choice, so inspect the complete precedence chain.
- **Weekend event:** UTC schedule with weekday mask 96. Use a separate static group if the area needs permanent protection or services between visits.

Balance the full circuit: time waiting and traveling, ordinary restock, arrival deliveries, shared listings across profiles, buyback capacity, denomination value, and dynamic prices. Test with realistic carrying capacity. Repeated admin jumps create fresh arrivals and can distort supply measurements.

## Night dealer and seasonal stock

Give a physical trader `OpeningHoursEnabled: true`, `OpeningHour: 20`, and `ClosingHour: 6` for a DayZ-night shop. Leave its safe zone disabled for a risky visit. Time acceleration makes the window shorter in real time.

Add a profile offer pool for rare goods. `Months: [10]` gates a pool to October in real UTC. `ActiveOffers` equal to pool size shows all seasonal goods together. Visibility does not refill stock.

Identical class order and rotation interval select the same UTC sequence at different profiles. Reorder a second profile's pool to offset it; a separate profile name alone does not randomize offers.

Keep an unrestricted buyback profile if players should resell yesterday's offer. Inactive pools block buying and selling. See [rotating offers](rotating-and-seasonal-offers.md).

## Vehicle dealer and garage policy

Pair exact-class listings with `VehicleAttachments.json` and clear `VehicleSpawnPoints`. With `CreateVehicleKeyOnPurchase: true`, purchased cars receive assigned keys; provide blank `RaG_CarKey` separately for found cars and spare-key crafting. Keep player inventory space or ground fallback available for key delivery.

- **Buy-only dealer:** `SellPrice: -1` prevents resale.
- **Buyback dealer:** positive sell price; explain ownership and the six-metre parking requirement.
- **Physical parking:** `EnableVehiclePacking: false` prevents packing; existing stored cars can still deploy.
- **Owner garage:** packing enabled with `RestrictVehicleStorageToOwner: true`.
- **Shared-key garage:** owner restriction false allows matching-key holders to pack and deploy. Sale ownership remains strict.

Deployed and stored cars use global-health condition pricing when enabled and must meet the health threshold. Packing does not repair a car. Fuel, cargo, and individual parts add no separate payout. Explain this before anyone sells a loaded truck.

Provide clearance for the largest vehicle and suitable water for boats. Purchase points also serve as sale search points: a parked car can block another delivery. Separate road and marine dealers simplify spawn placement.

## Cash, savings, or account credits

Stackable Euro notes create transport and looting choices. Keep `UseQuantity: true` and a value-1 denomination for exact change. Decide whether full-inventory payouts may drop at players' feet.

ATMs bank configured physical currency. Place `RaG_ATM` separately from trader locations. Modest fees create a money sink, but round-up fees disproportionately affect small transactions: 2.5% of a deposit of 10 rounds up to 1.

For cashless trade, use a default account currency and disable banking or keep it only for separate physical currencies. Account currencies start at zero without controlled administration or an integration. For bank-enabled physical currencies, players may select **Pay: Bank** for trader purchases; cash remains the default choice. Sales still pay physical notes. [Player market](player-market.md) purchases use bank/account balance.

## Practical acceptance session

Use an ordinary player and an admin with the intended server/client mod set in a separate profile.

| Test | Expected evidence |
| --- | --- |
| Fresh profile | Files generate; registry, stock, and journal initialize; traders bind once. |
| Report and Diagnostics | No unexpected disabled listings, blocking errors, or unresolved recovery. |
| New player | Reachable earnings fund the intended first supplies. |
| Loose ammo | Prices and stock count rounds; partial sales retain unsold ammo. |
| Magazines and boxes | Fill matches purchase contents; opening/unloading cannot create unintended resale profit. |
| Liquids | Correct contents supplied; wrong-liquid and empty sales fail; matching partial fill prices correctly. |
| Materials | Missing, ruined, nested-cargo, and insufficient distinct inputs fail without completing purchase. |
| Basket failure | One blocked line does not leave an unintended partial purchase or charge. |
| Two players | Shared stock affects the intended profiles and locations. |
| Time controls | World hours, UTC rotations, and uptime restocking behave independently. |
| Full inventory | Delivery, change, payout, withdrawal, and rollback follow the chosen ground policy. |
| Restart | Listing identities, stock, accounts, receipts, and vehicle links remain consistent. |
| Vehicle ownership | Spares, storage restrictions, sale ownership, and admin reset work. |
| Safe-zone border | Protection, exit timer, survival settings, and custom actions match the intended policy. |

For each price test, record starting balances, stock, health and contents, quote, receipt, and final balances. Keep initial tests small, then inspect longer sessions through telemetry. Valid JSON and a successful documentation build cannot replace in-game checks.
