# Ammunition, liquids, and purchase contents

| Listing | Price and stock unit | What the purchase supplies |
| --- | --- | --- |
| Loose ammunition | One round | Requested rounds, split into stacks as needed |
| Magazine | One magazine | A magazine with its configured round count |
| Ammo box | One box | The boxed item with its class-defined contents |
| Liquid container | One container | The container with the configured liquid and fill |
| Powered item | One item | The item with the configured charge, if it has an Energy Manager |
| Vehicle | One vehicle | The vehicle and parts from `Vehicles/Attachments.json` |

## Loose ammunition trades per round

If a round costs 7, buying 60 rounds costs 420 before any dynamic price adjustment. The server creates as many stacks as needed. Selling 12 rounds from a stack of 20 leaves eight rounds in your inventory. Stock changes by the number of rounds, and sale value can scale by the stack's health.

## Price boxes, magazines, and rounds together

Compare the purchase price of a box or filled magazine with the payout for the rounds a player can remove. If a box supplies 20 rounds and each round sells for 6, those rounds alone can pay 120. Factor in dynamic prices and any sale value for the emptied magazine. Validation checks recognized ammo-box resources against loose-ammo resale prices. Test loaded magazines and any custom unloading or unpacking actions in-game.

For a magazine listing, `"SpawnQuantity": 15` supplies 15 rounds per magazine. Buying two creates two magazines with 15 rounds each. When quantity pricing applies, a half-full pristine magazine with a fixed sell price of 150 pays 75.

## Liquid-specific listings

Use a registered `CfgLiquidDefinitions` class name for `RequiredLiquidType`. The container must support the liquid. A purchase delivers the filled container. A sale needs a container of the exact class with a positive amount of the matching liquid.

```json
{
  "ClassName": "CanisterGasoline",
  "BuyPrice": 600,
  "SellPrice": 120,
  "RequiredLiquidType": "Gasoline",
  "SpawnQuantity": 0,
  "SpawnFullQuantity": true,
  "MinimumHealthPercent": 30.0
}
```

Explicit fill uses the item's native quantity units. Keep it within the container's capacity. A half-full pristine canister with a fixed sell price of 120 pays 60 when quantity pricing applies.

To trade the same container class with several liquids, use separate listings with their own `RequiredLiquidType`. Set `AllowDuplicate: true` on each intentional copy. A generic listing with no liquid requirement can accept contents from the other listings, so check overlapping buyback prices.

## Read purchase contents before checkout

A positive `SpawnQuantity` sets rounds, charge, or fill on each purchased item. With `SpawnQuantity: 0`, `SpawnFullQuantity: true` requests maximum contents. If both controls are off, delivery leaves the class's initial contents.

Set `Attachments` to include specific parts with an ordinary item. Parent fill settings apply to the parent. An included magazine or battery uses its own spawn behavior. Check the purchase details and test one delivery when setting up a new class.
