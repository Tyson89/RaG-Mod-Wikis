# RaG Trader

RaG Trader is a server-authoritative trading, banking, safe-zone, and vehicle-key system. It ships with a searchable trader UI, physical Euro notes, persistent stocks and bank accounts, optional dynamic pricing, configurable NPC or terminal traders, vehicle delivery, and portable keyed vehicle storage.

[RaG Core](../core/index.md) is a hard dependency. Install both mods on server and every client. DayZ resolves addon/PBO ordering from declared dependencies; server `-mod` list order does not control it.

## Start here

- [Player guide](getting-started.md) covers trader UI, filters, baskets, buying, selling, banks, and practical player tips.
- [Server setup and class names](server-setup-and-class-names.md) covers installation, generated files, trader placement, ATMs, dependencies, and public classes.
- [Catalog, categories, and listings](catalog-and-listings.md) documents trader profiles, category files, every listing field, delivery, and custom mod items.
- [Settings, stock, and pricing](settings-stock-and-pricing.md) explains global settings, finite stock, restocking, dynamic pricing, item-condition pricing, and trade logs.
- [Locations and safe zones](locations-and-safezones.md) covers trader groups, NPC loadouts, opening hours, safe-zone protections, exclusions, and admin bypasses.
- [Banking and currencies](banking-and-currencies.md) covers physical and account currencies, denomination design, fees, limits, persistence, and ATM placement.
- [Vehicles, keys, and storage](vehicles-keys-and-storage.md) explains vehicle purchase spawns, attachments, keys, locking, spare keys, packing, deployment, and recovery files.
- [Troubleshooting and recovery](troubleshooting.md) maps common symptoms to exact checks and safe recovery procedures.

## Current default content

Current source ships:

- 7 trader profiles;
- 47 category files;
- 2,014 vanilla public class listings;
- one physical Euro currency using 1, 2, 5, 10, 20, 50, 100, and 200-value notes;
- one enabled Sosnovy Pass trader group with 7 survivor traders;
- 20 vanilla vehicle attachment profiles;
- optional banking and safe zones;
- `RaG_CarKey`, vehicle locking, spare-key crafting, and binary vehicle storage.

!!! warning "Defaults are a starting point, not a balanced economy"
    Default catalog exposes nearly every public vanilla class and uses broad category-level prices. Serious servers should remove unwanted classes, set deliberate vehicle resale values, choose finite stock where scarcity matters, and rebalance buy/sell gaps before launch.

## Important design facts

- Server validates identity, distance, location, trader, listing, price, stock, quantity, and catalog revision. Client UI is not authority.
- Category filename becomes category ID. Listing IDs derive from category ID and class name.
- Stock belongs to listing ID and is shared by every trader/location exposing that listing.
- Basket checkout is atomic: all lines complete, or delivered items and reserved stock are rolled back.
- Physical currency can be found in hands, clothing, containers, attachments, and nested inventory.
- Purchased vehicles use configured spawn points, not player inventory or ordinary ground fallback.
- Vehicles can be sold packed through owner key or physically from trader vehicle spawn point, subject to ownership checks.
- Vehicle purchases do not automatically assign or include a key.
- Safe zones are optional and independent per location group.
- Main JSON and category changes require server restart; no runtime reload exists.

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
