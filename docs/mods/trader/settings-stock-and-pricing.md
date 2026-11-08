# Settings, stock, and pricing

## `Settings.json`

These defaults come from the bundled Trader root `Settings.json`. Keep `"Version": 1`.

| Field | Default | Effect |
| --- | --- | --- |
| `EnableStaticTraders` | `true` | Spawns or binds the configured static traders. |
| `EnableRoutes`, `EnableP2P` | `false`, `false` | Enable traveling traders and the player market. |
| `EnableBanking`, `EnableBankTransfers` | `true`, `true` | Enable ATMs and transfers between players. |
| `EnableSafezones` | `true` | Enables configured zones. Each zone has its own switch. |
| `InteractionDistance` | `3.0` | Server interaction range in metres. Minimum `1.0`. |
| `MaxBasketEntries` | `50` | Server limit per basket, `1–100`. The UI supports up to 50. |
| `StockSaveIntervalSeconds` | `5` | Stock save interval. Minimum `1` second. |
| `EnableTradeLogging`, `EnableEconomyTelemetry` | `true`, `true` | Record completed shop trades and aggregate trade statistics, respectively. |
| `EnableAutomaticRestock` | `true` | Adds ordinary timed supply for eligible shared-stock listings. |
| `EnableDynamicPricing`, `DynamicPriceRangePercent` | `false`, `25.0` | Stock-based price adjustment. Range `0–90` percent. |
| `EnableConditionSellPricing`, `EnableQuantitySellPricing` | `true`, `true` | Scale sale prices by health and contents. |
| `MinimumSellPricePercent` | `10.0` | Floor for condition scaling where applicable. Range `0–100` percent. |
| `AllowGroundFallback` | `true` | Allows eligible deliveries or payouts at the player's feet if inventory placement fails. |
| `LockVehicleWheelsOnSpawn` | `false` | Locks installed car wheels on purchased vehicles. |
| `CreateVehicleKeyOnPurchase` | `true` | Pairs and delivers a key with eligible purchased cars. |
| `EnableVehiclePacking`, `EnableVirtualGarage` | `false`, `true` | Enable packing with car keys and storage at garage platforms. |
| `RestrictVehicleStorageToOwner` | `true` | Restricts key packing and deployment to the owner or an admin. |
| `AdminSteamIds` | `[]` | Quoted Steam64 IDs for admin controls. |

These are the bundled first-start settings. Set `AllowGroundFallback` explicitly: the bundled JSON enables it, but the script's initializer is `false`. Omitting that field is not equivalent to using the shipped file. `AllowGroundFallback` does not override an explicitly configured `DeliveryMode: "ground"`, vehicle spawn checks, or the player market's inventory-only collection.

`Version` must remain `1`. Settings validation clamps `InteractionDistance` to at least `1`, `MaxBasketEntries` to `1–100`, `StockSaveIntervalSeconds` to at least `1`, `DynamicPriceRangePercent` to `0–90`, and `MinimumSellPricePercent` to `0–100`. Check effective values after editing. Use the [reload rules](administration-and-recovery.md#live-configuration-reload) before changing a running server.

A checkout line accepts up to 100 ordinary objects or 10,000 loose rounds. A vehicle or ordinary ground-delivery line has quantity one. The server also limits object work per checkout to 500, including contents or materials it has to process.

## Stock

Use `InitialStock: -1` and `MaxStock: -1` for unlimited supply and buyback. For finite stock, use `0 <= InitialStock <= MaxStock`. Purchases remove units and sales add units. A purchase needs enough stock and a sale needs space under capacity. Units are rounds for loose ammo and objects for everything else.

`InitialStock` applies when a stock record is created. Existing stock persists through restart and reload. Static traders share stock for the same listing ID. Traveling traders can share that stock or use [route or stop stock](traveling-traders-and-routes.md#stock-sharing-and-arrival-deliveries).

## `Stock.json`

The Trader config directory contains `Stock.json` and `StockDelta.json`. The stock snapshot and its delta record counts, assigned listing identities, scoped counts, and applied route deliveries. Keep them with their backups and route state. For an intentional stock reset, stop the server and back up both files and their companions before moving the state out of the active profile. Resetting also affects listing identities and arrival records.

## Automatic restocking

Set a positive `RestockAmount` and `RestockIntervalSeconds` on a listing with finite positive capacity. Intervals can be up to `86400` seconds. With `EnableAutomaticRestock: true`, ordinary stock increases by that amount each interval until full. Restock uses server uptime and begins a fresh timer on startup. Separate route or stop stock uses arrival delivery instead.

## Dynamic pricing

Finite stock with positive capacity can adjust prices. For each unit, use the stock before removing a purchase or after adding a sale.

```text
ratio = stock / capacity
multiplier = 1 + (1 - 2 × ratio) × DynamicPriceRangePercent / 100
purchase unit = max(1, ceil(BuyPrice × multiplier))
base sale unit = max(1, floor(SellPrice × multiplier))
```

At 25% range, full stock and base buy price 100 produce a first unit price of 75. With capacity 10, buying the next two units costs 80 and 85, for 240 total. Unlimited stock uses the base price. A route with a capacity override uses that capacity.

## Condition and quantity sell pricing

For an eligible item without quantity scaling, multiply its base sale price by its health fraction when condition pricing is on. The configured minimum percentage is a floor on that factor. Round down with a minimum payout of one.

For quantity-scaled items, multiply by condition and fullness. Fullness uses magazine rounds, energy, or item quantity in that order. Splittable quantity items still use fullness when the general quantity switch is off. Sum values within the line before rounding down. The condition minimum does not apply to these lines. A line that rounds to zero cannot complete. At a fixed sale price of 200, a half-full magazine with 60% health pays 60.

Loose ammunition uses the exact number of rounds sold, with condition scaling and no stack-fullness factor. Its condition factor also uses `MinimumSellPricePercent`; round values are summed and the line total rounds down, so a line can still be worth zero and fail. Vehicles use global health. Listing `MinimumHealthPercent` governs eligibility separately.

## Trade logging

`EnableTradeLogging` controls completed shop trade entries in the `Trades` audit log. Banking, P2P, garage, recovery, and admin activity have separate [server audit logs](administration-and-recovery.md#server-audit-logs).
