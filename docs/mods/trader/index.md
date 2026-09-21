# RaG Trader

RaG Trader is a server-authoritative trading, banking, safe-zone, and vehicle-key system. It includes a searchable trader UI, stackable physical Euro notes, persistent stocks and bank accounts, optional dynamic pricing, configurable NPC or object traders, traveling markets with scheduled stops and local currencies, vehicle delivery, and portable keyed vehicle storage.

[RaG Core](../core/index.md) is a hard dependency. Install both mods on server and every client. DayZ resolves addon/PBO ordering from declared dependencies; server `-mod` list order does not control it.

## Start here

- [Player guide](getting-started.md) covers trader UI, filters, baskets, buying, selling, banks, and practical player tips.
- [Server setup and class names](server-setup-and-class-names.md) covers installation, generated files, trader placement, ATMs, dependencies, and public classes.
- [Catalog, categories, and listings](catalog-and-listings.md) documents trader profiles, category files, every listing field, delivery, and custom mod items.
- [Settings, stock, and pricing](settings-stock-and-pricing.md) explains global settings, finite stock, restocking, dynamic pricing, item-condition pricing, and trade logs.
- [Locations and safe zones](locations-and-safezones.md) covers trader groups, NPC loadouts, opening hours, safe-zone protections, exclusions, and admin bypasses.
- [Traveling traders and routes](traveling-traders-and-routes.md) covers group movement, schedules, branching stops, local prices, supply deliveries, map markers, and admin controls.
- [Banking and currencies](banking-and-currencies.md) covers physical and account currencies, denomination design, fees, limits, persistence, and ATM placement.
- [Vehicles, keys, and storage](vehicles-keys-and-storage.md) explains vehicle purchase spawns, attachments, keys, locking, spare keys, packing, deployment, and recovery files.
- [Ammunition, liquids, and purchase contents](ammo-liquids-and-purchase-contents.md) explains per-round trading, partial stacks, liquid-specific containers, supplied contents, and safe pricing.
- [Rotating and seasonal offers](rotating-and-seasonal-offers.md) explains UTC schedules, rotating selections, seasonal shops, and reliable buyback routes.
- [Economy recipes and testing](economy-recipes.md) gives worked configurations for essentials, hunters, regional markets, events, and vehicle dealers.
- [Administration and recovery](administration-and-recovery.md) covers live reload, validation reports, receipts, telemetry, journals, and backups.
- [Troubleshooting and recovery](troubleshooting.md) maps common symptoms to exact checks and safe recovery procedures.

## Bundled default content

Bundled defaults contain:

- 6 trader profiles: hunting, tools, weapons, clothing, vehicles, and special;
- 60 category files;
- 1,782 listings across the bundled category files;
- one physical Euro currency using 1, 2, 5, 10, 20, 50, 100, and 200-value notes;
- three enabled groups—Sosnovy Pass, Mogilevka, and Prison—with 6 survivor traders each;
- one disabled example route connecting those groups; with the route disabled, the groups operate as static locations;
- 20 vanilla vehicle attachment profiles;
- banking enabled, with zero fees and zero starting balance;
- optional safe-zone configuration for the location groups;
- `RaG_CarKey`, vehicle locking, spare-key crafting, and binary vehicle storage.

!!! warning "Defaults are a starting point, not a balanced economy"
    Default catalog exposes a broad range of vanilla classes and uses broad category-level prices. Serious servers should remove unwanted classes, set deliberate vehicle resale values, choose finite stock where scarcity matters, and rebalance buy/sell gaps before launch.

## Important design facts

- Server validates identity, distance, location, trader, listing, price, stock, quantity, and catalog revision. Client UI is not authority.
- Category filename becomes category ID. Listing identities include category, class, liquid variant, and duplicate occurrence; their assigned IDs persist in `Stock.json`.
- `InitialStock` seeds supply; `MaxStock` limits storage. Static shops share stock by listing ID; routes can share it or isolate it per route/profile or stop/profile.
- Basket checkout targets all-or-nothing completion. Failures trigger rollback; unresolved recovery is retained in journals rather than silently discarded.
- Physical currency can be found in hands, clothing, containers, attachments, and nested inventory.
- Purchased vehicles use configured spawn points, not player inventory or ordinary ground fallback.
- Vehicles can be sold packed through owner key or physically from trader vehicle spawn point, subject to ownership checks.
- Vehicle purchases do not automatically assign or include a key.
- Safe zones are optional and independent per location group.
- Admins can reload supported economy settings and categories through trader UI. Location-file positions, opening hours, zones, and currencies require restart, as do catalog currency definitions. Permitted route edits require the affected route paused at a stop.
- Rotating offers and seasonal months use real UTC; opening hours use DayZ world time. Ordinary restocking uses server uptime. Route schedules choose real UTC or DayZ world time; route wait/travel timers use real seconds.
- Purchases can require consumed items in addition to money. Loose-ammo requirements apply per round.
- Loose ammo prices, quantities, and stock count rounds; magazines and ammo boxes count objects.
- Liquid-specific listings supply the configured liquid and accept only matching non-empty containers.
- Listing configuration faults disable the affected listing. Structural faults can prevent the whole registry from starting.
- Sell all eligible provides a separate confirmation flow for eligible cargo items; direct sales can also consume attached equipment.
- Transaction journals support interrupted-trade recovery. Pending or ambiguous recovery can suspend trading.

## Required addon relationship

`CfgPatches.requiredAddons[]` declares:

```cpp
requiredAddons[] =
{
    "DZ_Data",
    "DZ_Gear_Camping",
    "RaG_Core"
};
```

This relationship, not command-line list order, controls addon initialization.
