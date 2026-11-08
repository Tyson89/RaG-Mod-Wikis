# RaG Trader

RaG Trader adds NPC and object shops, traveling merchants, banking, a player market, and vehicle storage to DayZ. Server owners configure what each trader buys and sells, its currency, stock, and when and where it opens.

## Features and what defines RaG Trader

- **Shopping tools built into the economy.** Search across categories, filter compatible parts, save favorites, review a basket, try clothing on a preview character, and build a weapon with purchased attachments before checkout. Bulk selling has a server-generated item and payout review.
- **Shops with supply and demand.** Use unlimited stock, finite shared stock, player-supplied stock, timed restock, or stock-based prices. Resale can account for condition and contents. Purchases can require money plus materials, include attachments, or supply a specific liquid and fill level. Loose ammunition trades per round.
- **Traveling merchants with local economies.** Merchants appear at scheduled stops with optional props and safe zones. Stops can change categories, currency, prices, buying/selling policy, and stock capacity. Share stock globally, carry it with one route, or keep separate stop inventories. Arrival deliveries, route graphs, announcements, map markers, and seasonal windows make markets change over time.
- **A market for actual player items.** P2P stores the submitted item and its permitted contents. Buyers inspect condition and contents, then collect purchases at any board. Wanted orders reserve funds for an item with specified minimum condition, quantity, liquid, or ammunition. Fees, commission, expiry, and class restrictions are configurable.
- **Cash, accounts, and banking together.** Physical currencies support stacked denominations and change. Account currencies support virtual credits. ATMs handle deposits, withdrawals, fees, and transfers to known players, including offline recipients. Banked cash can pay directly at ordinary shops.
- **Vehicle ownership and storage.** Dealers fit configured parts and can issue car keys. Keys support locking, spare copies, and optional portable car packing. Virtual garages preserve supported vehicles with attachments and cargo, with configurable access, capacity, vehicle types, and retrieval sites.
- **Configurable protection around markets.** Safe zones can protect players and equipment, restrict supported weapon/explosive/building actions, clear wildlife, cap car speed, and pause selected survival effects. Each site chooses its own policy.
- **Tools for operating an economy.** JSON categories, stable listing identities, validation reports, supported live reload, diagnostics, route controls, personal receipts, audit logs, telemetry, and transaction recovery give hosts visibility into trades and failures.

The defining combination is an integrated trading, banking, player-market, and vehicle-storage system with both preview tools for players and detailed economy controls for hosts. Feature availability follows server configuration; transaction journals support reconciliation after interruptions, rather than guaranteeing every failure resolves automatically.

## Players

- [Player guide](getting-started.md) covers browsing, buying, selling, and receipts.
- [Clothing try-on and weapon builder](shopping-tools.md) covers outfit previews and configured weapon purchases.
- [P2P Trader](player-market.md) covers selling your gear, collecting purchases, and fulfilling wanted orders.
- [Vehicles, keys, and storage](vehicles-keys-and-storage.md) covers vehicle trading, garage meters, and portable packing.

## Server owners

- [Setup and class names](server-setup-and-class-names.md) covers required mods, generated files, and your first shop.
- [Complete JSON configuration reference](configuration-reference.md) maps every editable field, nested object, default distinction, and related guide.
- [Catalog, categories, and listings](catalog-and-listings.md) and [Settings, stock, and pricing](settings-stock-and-pricing.md) define the economy.
- [Locations and safe zones](locations-and-safezones.md), [Traveling traders](traveling-traders-and-routes.md), and [Rotating and seasonal offers](rotating-and-seasonal-offers.md) control access and availability.
- [Banking and currencies](banking-and-currencies.md) and [P2P server setup](player-market-server.md) cover balances, transfers, market boards, and market policy.
- [Economy recipes and testing](economy-recipes.md) gives examples for stock, materials, and regional shops.
- [Administration and recovery](administration-and-recovery.md) and [Troubleshooting](troubleshooting.md) cover validation, diagnostics, and saved state.

The bundled Chernarus setup has six shops at Green Mountain and a separate boat trader. Green Mountain includes two ATMs, a garage platform, and a player market board. Traveling traders and the player market are off by default.

Static traders, banking, bank transfers, and virtual garages are enabled in the bundled settings. Dynamic pricing and portable vehicle packing are off. The global safe-zone switch is on, but the bundled static zones are disabled individually. Check the actual configuration on your server before assuming a feature or protection is active.
