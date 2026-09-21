# Ammunition, liquids, and purchase contents

Loose ammunition trades in rounds. Magazines, ammunition boxes, batteries, food, and liquid containers trade as objects with contents. Check both requested quantity and the purchase-contents panel before checkout.

## Trade units at a glance

| Listing | Quantity means | Price and stock unit | Delivered contents |
| --- | --- | --- | --- |
| Loose ammo derived from `Ammunition_Base` | Rounds | One round | Requested rounds split into class-sized stacks. |
| Detachable magazine | Magazine objects | One magazine | Ammo determined by fill settings. |
| Ammunition box | Box objects | One box | Box resources defined by the item class. |
| Food, medicine, nails, or similar quantity item | Objects/stacks | One object | Quantity determined by fill settings. |
| Battery or another Energy Manager item | Objects | One object | Energy determined by fill settings. |
| Liquid-specific bottle/canister | Containers | One container | Required liquid, at configured fill. |
| Car or boat | One vehicle | One vehicle | Exact vehicle profile and configured parts. |

The ammo exception depends on inheritance, not merely an `Ammo_` name. Custom ammo must derive from `Ammunition_Base` to use round trading.

## Loose ammunition trades per round

Add this illustrative listing to a category's `Listings` array:

```json
{
  "ClassName": "Ammo_308Win",
  "BuyPrice": 20,
  "SellPrice": 5,
  "InitialStock": 600,
  "MaxStock": 600,
  "RestockAmount": 60,
  "RestockIntervalSeconds": 1800,
  "MinimumHealthPercent": 25.0,
  "DeliveryMode": "inventory"
}
```

With dynamic pricing disabled:

- Buy quantity 30: receive 30 rounds, pay 600, remove 30 from stock.
- Sell quantity 12 of pristine ammo: receive 60, add 12 to stock.
- `InitialStock: 600` means 600 starting rounds; `MaxStock: 600` caps storage at 600 rounds, not 600 full stacks.
- Restock adds up to 60 rounds every 30 minutes of uptime, capped at 600.
- A fresh finite listing starts full, so buyback initially has no free capacity. Purchases free capacity; restock fills it again.

The maximum request is 10,000 rounds per line. A transaction can still exceed the 500-object work budget because of its other lines, ingredients, delivered stacks, or attachments.

### Stack delivery

The server reads the ammo class's `CfgMagazines` `count` as stack capacity. It creates enough objects for the requested rounds and sets the last stack's remainder exactly.

For an ammo class with capacity 20, buying 45 rounds creates stacks of 20, 20, and 5. The price is for 45 rounds. `SpawnFullQuantity` and `SpawnQuantity` do not multiply the order into full stacks.

`DeliveryMode: "ground"` can create multiple loose-ammo stacks. It does not impose the ordinary one-object restriction. Clear space and collect every stack, especially when several people use the shop.

### Partial stack sales

The server selects eligible exact-class loose-ammo stacks until it reaches the requested round count. It can consume part of the last stack. Unsold rounds remain.

With a 20-round stack and a 12-round sale, eight rounds remain. With stacks of 10 and 20 and a 15-round sale, the exact remainder per stack depends on selection order, but 15 total rounds are sold and 15 remain.

Condition affects the source stacks when `EnableConditionSellPricing` is enabled. At fixed sell price 5, twelve rounds from a 60%-health stack yield `floor(12 × 5 × 0.60) = 36`. A partly filled pristine stack receives the same per-round value as a full pristine stack; fullness is not another deduction.

Ammo loaded inside a magazine belongs to that magazine. Unload it into loose ammo before using a loose-ammo listing. Selling the magazine uses its own listing, ammo fraction, and eligibility rules.

!!! tip "Keep round costs simple"
    `RequiredItems` applies per round. Requiring one token on a 100-round purchase consumes 100 separate token objects. For one voucher per box, sell an ammunition-box object instead and price its contents deliberately.

## Price boxes, magazines, and rounds together

An ammunition box trades as one object. Opening it can produce loose rounds. A loaded magazine can also supply rounds for separate resale. Those routes must agree economically.

For a hypothetical box containing 20 rounds:

```text
loose-ammo SellPrice = 5 per round
value after opening box = 20 × 5 = 100
box BuyPrice = 80 → profitable buy/open/sell route
box BuyPrice = 150 → 50-unit gap before other deductions
```

At a 25% dynamic range, a base-150 finite box could cost as little as 112.5 before buy rounding, while twenty rounds at maximum base sell value could approach 125. Leave a wider gap for independently stocked routes.

The validator compares loose-ammo resale values with enabled purchase listings. It reads recognized `CfgVehicles` box `Resources` and considers dynamic-price bounds where implemented. It does not inspect loaded magazine fill for this check; magazine and weapon packages need manual resale testing. Detected profit disables the purchase listing and reports `BuyPrice permits an ammo resale profit in listing`.

This is not a complete simulation of crafting, attachments, third-party unpacking scripts, every stock trajectory, or custom price hooks. Test:

1. Buy one box, open it, and sell the rounds.
2. Buy one loaded magazine, unload it, and compare round proceeds plus eligible empty-magazine resale.
3. Buy a weapon package, strip supplied attachments, and compare all resale routes.
4. Repeat at the lowest purchase and highest resale conditions available across different traders.

### Partially loaded magazine

```json
{
  "ClassName": "Mag_STANAG_30Rnd",
  "BuyPrice": 500,
  "SellPrice": 150,
  "InitialStock": 20,
  "MaxStock": 20,
  "SpawnQuantity": 15,
  "SpawnFullQuantity": false
}
```

Quantity two buys two magazines, each with 15 rounds. It does not buy two rounds or 30 magazines. Positive explicit `SpawnQuantity` wins even if `SpawnFullQuantity` is true.

At fixed pricing and full health, selling one half-full 30-round magazine at base sell 150 yields 75 with quantity scaling. An empty magazine has zero quantity-scaled value. Disabling quantity scaling can give non-splittable empty magazines a value, but that switch affects other eligible objects globally; assess the entire catalog.

## Liquid-specific listings

`RequiredLiquidType` is a `CfgLiquidDefinitions` class name, such as `Gasoline`, rather than a translated display name or numeric liquid bitmask. Matching trims whitespace and compares names case-insensitively, then uses the canonical definition name. The liquid must also be registered in RaG Core's liquid registry.

Example fuel listing:

```json
{
  "ClassName": "CanisterGasoline",
  "BuyPrice": 600,
  "SellPrice": 120,
  "RequiredLiquidType": "Gasoline",
  "InitialStock": -1,
  "MaxStock": -1,
  "SpawnQuantity": 0,
  "SpawnFullQuantity": true,
  "MinimumHealthPercent": 30.0
}
```

A purchase supplies a **container holding gasoline**, not a refill into a carried canister. A sale consumes the matching container and contents. No empty container is returned without custom integration.

For a purchase, the server sets fill quantity, clears initial liquid, and fills with the specified type. A sale requires:

- exact container class;
- positive liquid quantity;
- exact required liquid type;
- normal health, cargo, lock, and removability conditions.

An empty or wrong-liquid canister does not qualify. Matching liquid type does not check every contamination state, quality property, or third-party food-safety rule.

### Fill and price units

`SpawnQuantity` uses the container's native quantity units. Check the class maximum and in-game result before labeling an offer in litres. Explicit liquid purchase fill must be positive and no greater than maximum capacity.

With zero explicit fill, `SpawnFullQuantity: true` uses maximum capacity. With both fill controls inactive, the class's initial quantity remains; a buyable liquid listing must still produce positive contents. Zero initial contents make that purchase invalid.

Prices and stock count containers, not millilitres. Quantity sell pricing scales payout by contents divided by that container's maximum. A half-full pristine container at fixed sell 120 pays 60. This is not a configurable per-litre price shared by different container classes.

### Several liquids in one container class

Create separate listings for each wanted container/liquid combination. A compatible container could have one `Gasoline` entry and one `Diesel` entry. Set `AllowDuplicate: true` on **every** intentional copy of the class at the trader.

The server tests actual container compatibility. A valid liquid definition does not guarantee that a selected bottle accepts it. An invalid combination disables its listing and appears in the validation report.

Liquid names distinguish listings. The `Stock.json` identity map includes the liquid name, preserving variant identities when their order changes. Keep this map with stock backups.

!!! tip "Avoid a catch-all resale loophole"
    Blank `RequiredLiquidType` means no liquid restriction. A generic expensive canister listing can accept contents intended for a cheaper buyback route. Use explicit liquids for contents-based resale. Overlapping generic and liquid-specific entries can also make bulk-sale selection less clear.

### Custom liquid possibilities

Food merchants, fuel depots, and specialist fluid traders can use registered RaG Core or companion-mod liquids when compatible containers exist. Their definitions and items must be present in the active mod set.

1. Find the exact `CfgLiquidDefinitions` name in the mod's current source.
2. Check registration and container compatibility.
3. Add one listing with explicit liquid and fill settings.
4. Read validation output. Fix unknown-liquid, non-container, incompatible-fill, or over-capacity errors.
5. Buy one, inspect liquid and quantity, then test matching, wrong-liquid, and empty sales.
6. Change contents while a sale review is open; confirm a fresh review is required.

## Read purchase contents before checkout

Selected-listing details describe requested objects or rounds, fill per item, required liquid, and included attachments. Repeated attachment classes appear with counts. Vehicle parts come from the exact-class `VehicleAttachments.json` profile.

A 3D preview helps identify an item. Purchase details and server configuration determine supplied contents. A weapon preview is not proof that a magazine, optic, or battery comes with it.

Parent fill settings affect the parent. They do not recursively fill attachments, attach a missing magazine, or insert a battery into an optic. List wanted attachments explicitly and test their creation defaults.

### Batteries and powered equipment

For an Energy Manager item, positive `SpawnQuantity` sets energy units; otherwise full quantity fills maximum energy. It does not control object count. Sale quantity scaling uses remaining energy when applicable.

This allows premium charged equipment, cheaper partially charged supplies, and salvage buyback. Use clearly named categories for otherwise identical packages so players can distinguish the offer. Class-based favorites do not distinguish charge levels.

### Contents test

- Buy quantity one; inspect health, fill, and attachments.
- Buy quantity two where allowed; confirm fill applies per object.
- Compare the server quote, receipt, and wallet change.
- Test a partial sale; confirm inventory remainder.
- Fill inventory and check the selected ground-delivery policy.
- Reopen after reload; confirm the contents description matches future deliveries.

See [pricing](settings-stock-and-pricing.md) for calculations and [economy recipes](economy-recipes.md) for shop designs.
