# RaG Trader

!!! info "Not publicly released"
    RaG Trader is in development and is not publicly available. This wiki documents the current development source for private testing and server planning. No public download or release date is announced here.

RaG Trader is a server-authoritative trading, banking, safe-zone, and vehicle-key system. It includes a searchable trader UI, physical Euro notes, persistent stocks and bank accounts, optional dynamic pricing, configurable NPC or terminal traders, vehicle delivery, and portable keyed vehicle storage.

[RaG Core](../core/index.md) is a hard dependency. Install both mods on server and every client. DayZ resolves addon/PBO ordering from declared dependencies; server `-mod` list order does not control it.

## Start here

- [Player guide](getting-started.md) covers trader UI, filters, baskets, buying, selling, banks, and practical player tips.
- [Server setup and class names](server-setup-and-class-names.md) covers installation, generated files, trader placement, ATMs, dependencies, and public classes.
- [Catalog, categories, and listings](catalog-and-listings.md) documents trader profiles, category files, every listing field, delivery, and custom mod items.
- [Settings, stock, and pricing](settings-stock-and-pricing.md) explains global settings, finite stock, restocking, dynamic pricing, item-condition pricing, and trade logs.
- [Locations and safe zones](locations-and-safezones.md) covers trader groups, NPC loadouts, opening hours, safe-zone protections, exclusions, and admin bypasses.
- [Banking and currencies](banking-and-currencies.md) covers physical and account currencies, denomination design, fees, limits, persistence, and ATM placement.
- [Vehicles, keys, and storage](vehicles-keys-and-storage.md) explains vehicle purchase spawns, attachments, keys, locking, spare keys, packing, deployment, and recovery files.
- [Limits, offers, and demand](limits-offers-and-demand.md) explains quotas, UTC schedules, rotating stock selection, seasonal offers, and demand bonuses.
- [Economy recipes and testing](economy-recipes.md) gives worked configurations for essentials, hunters, regional markets, events, and vehicle dealers.
- [Administration and recovery](administration-and-recovery.md) covers live reload, validation reports, receipts, telemetry, journals, and backups.
- [Troubleshooting and recovery](troubleshooting.md) maps common symptoms to exact checks and safe recovery procedures.

## Current default content

Bundled development defaults contain:

- 6 trader profiles: hunting, tools, weapons, clothing, vehicles, and special;
- 45 category files;
- 1,803 listings across the bundled category files;
- one physical Euro currency using 1, 2, 5, 10, 20, 50, 100, and 200-value notes;
- one enabled Sosnovy Pass trader group with 6 survivor traders;
- 20 vanilla vehicle attachment profiles;
- optional banking and safe zones;
- `RaG_CarKey`, vehicle locking, spare-key crafting, and binary vehicle storage.

!!! warning "Defaults are a starting point, not a balanced economy"
    Default catalog exposes a broad range of vanilla classes and uses broad category-level prices. Serious servers should remove unwanted classes, set deliberate vehicle resale values, choose finite stock where scarcity matters, and rebalance buy/sell gaps before launch.

## Important design facts

- Server validates identity, distance, location, trader, listing, price, stock, quantity, and catalog revision. Client UI is not authority.
- Category filename becomes category ID. Listing IDs derive from category ID and class name.
- Stock belongs to listing ID and is shared by every trader/location exposing that listing.
- Basket checkout targets all-or-nothing completion. Failures trigger rollback; unresolved recovery is retained in journals rather than silently discarded.
- Physical currency can be found in hands, clothing, containers, attachments, and nested inventory.
- Purchased vehicles use configured spawn points, not player inventory or ordinary ground fallback.
- Vehicles can be sold packed through owner key or physically from trader vehicle spawn point, subject to ownership checks.
- Vehicle purchases do not automatically assign or include a key.
- Safe zones are optional and independent per location group.
- Admins can reload supported economy settings and categories through trader UI. Locations, opening hours, safe zones, and currency definitions require restart.
- Per-player limits, rotating offers, and seasonal demand use real UTC; opening hours use DayZ world time.
- Purchases can require consumed items in addition to money.
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
