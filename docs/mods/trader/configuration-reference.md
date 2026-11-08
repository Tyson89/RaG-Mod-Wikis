# JSON configuration reference

All server configuration lives below `$profile:\RaG_Core\Configs\RaG_Trader\`. This map covers every editable field in the eight main files and category files. Follow the linked field tables for defaults, limits, examples, and gameplay behavior.

## File structure and editing rules

| File | Root fields | Detailed reference |
| --- | --- | --- |
| `Settings.json` | `Version` and global feature, economy, delivery, vehicle, and admin settings | [Every root setting](settings-stock-and-pricing.md#settingsjson) |
| `Trading/Catalog.json` | `Version`, `DefaultCurrencyId`, `Currencies`, `Traders` | [Catalog and listings](catalog-and-listings.md), [currencies](banking-and-currencies.md) |
| `Trading/Categories/<name>.json` | `DisplayName`, `CurrencyId`, `Listings` | [Category and listing fields](catalog-and-listings.md#category-files) |
| `Traders/Locations.json` | `Version`, `Locations` | [Locations and safe zones](locations-and-safezones.md) |
| `Routes/Routes.json` | `Version`, `Routes` | [Route and stop fields](traveling-traders-and-routes.md) |
| `Banking/Settings.json` | `Version`, `DepositFeePercent`, `WithdrawalFeePercent`, `Currencies` | [Bank settings](banking-and-currencies.md#bankingsettingsjson) |
| `P2P/Settings.json` | `Version` and market policy fields | [Every market setting](player-market-server.md#p2psettingsjson) |
| `Vehicles/Attachments.json` | `Version`, `Vehicles` | [Vehicle attachment sets](#vehicle-attachment-sets) |
| `Vehicles/Garages.json` | `Version`, `MaxVehiclesPerPlayer`, `AllowVehicleKeyHolders`, `PlatformParkingHeight`, `PlatformSpawnClearance`, `RestrictRetrievalToStorageMeter`, `StandaloneMeters` | [Garage settings](vehicles-keys-and-storage.md#server-setup) |

Keep `Version: 1` in every main file. Missing, different, or malformed versions can reject loading. Category files omit `Version`. Startup copies missing bundled files; it does not overwrite existing customized files or automatically add every new setting to them.

Use JSON booleans (`true`/`false`), numbers for prices and coordinates, quoted strings for identifiers and classes, arrays (`[]`) for lists, and objects (`{}`) for maps. JSON permits neither comments nor trailing commas. An empty string generally means no override, but required IDs and classes cannot be empty. The `-1` sentinel is field-specific: unlimited stock or disabled price, for example. It does not mean unlimited everywhere.

Distinguish **bundled values** from **script initializers for omitted fields**. The bundled `AllowGroundFallback` is `true`, while its script initializer is `false`. Route `RandomStops` is `true` in both. Prefer explicit values for policy that matters to your server. Use [live reload rules](administration-and-recovery.md#live-configuration-reload); restart for structural features, static placement, currencies, banking, market policy, or garage policy.

## Choose the features you need

| Goal | Settings and configuration |
| --- | --- |
| NPC or object shop | `EnableStaticTraders`, catalog profile and categories, enabled location group and trader entry |
| Traveling or event merchant | `EnableRoutes`, enabled route, catalog profile, stops, optional schedule and offer pools |
| Safe trading area | `EnableSafezones`, enabled group or stop `Safezone`, chosen protections |
| Cash and change | Catalog item currency and denominations; banking is optional for ordinary cash trades |
| Stored physical money and ATM | `EnableBanking`, enabled bank currency, placed `RaG_ATM` |
| Transfers to other players | Banking requirements plus `EnableBankTransfers` |
| Virtual credits | Catalog account currency; starts at zero with the built-in account service |
| Player sale listings or wanted orders | `EnableP2P`, market currency and permitted boards; `BuyOrdersEnabled` controls wanted orders separately |
| Finite or player-supplied shops | Listing `InitialStock`, `MaxStock`, optional restock; stock-based prices need `EnableDynamicPricing` |
| Vehicle dealership | Vehicle listings, dealer spawn points, `Vehicles/Attachments.json`, optional purchase keys and wheel locking |
| Garage storage | `EnableVirtualGarage`, suitable meter or platform, `Vehicles/Garages.json` |
| Portable car storage | `EnableVehiclePacking`, assigned car key; ownership policy uses `RestrictVehicleStorageToOwner` |

Placing an ATM, market board, or garage meter does not enable its service. A location's `Objects` array places objects; garage `StandaloneMeters` defines matching areas and does not spawn meters.

## Catalog objects

`Currencies` and `Traders` are arrays in `Trading/Catalog.json`. `DefaultCurrencyId` is the base currency reference. The bundled catalog uses `euro`; when omitted it is empty, with a single-valid-currency fallback. There is no editable catalog-level `Categories` array: profiles reference category filenames instead.

### Currency definitions

| Field | Initializer | Meaning |
| --- | --- | --- |
| `Id` | Empty | Unique currency identifier, referenced by categories, locations, banking, routes, and P2P. |
| `DisplayName` | Empty | Currency label shown to players. Supply a readable name. |
| `Type` | `"item"` | `"item"` for physical denominations or `"account"` for virtual balances. |
| `CurrencyItems` | `[]` | Physical denomination definitions; leave empty for account currency. |
| `CurrencyItems[].ClassName` | Empty | Existing denomination item class. |
| `CurrencyItems[].Value` | `0` | Positive whole currency units per item or quantity unit. Values must be distinct within that currency. |
| `CurrencyItems[].UseQuantity` | `false` | `true` counts supported stack quantity; `false` counts each object once. |

Item currencies require a value-1 denomination. See [cash, change, account currency, and precedence](banking-and-currencies.md).

### Trader profiles and offer pools

| Field | Initializer | Meaning |
| --- | --- | --- |
| `Id` | Empty | Unique profile identifier used by locations and routes. |
| `DisplayName` | Empty | Shop title. |
| `Categories` | `[]` | Category filename stems, without `.json`; these determine the profile's listings. |
| `OfferPools` | `[]` | Optional availability groups; omitted pools leave listed classes unrestricted. |
| `OfferPools[].Id` | Empty | Pool identifier, unique within this profile. |
| `OfferPools[].ClassNames` | `[]` | Ordered offered classes whose availability this pool controls. |
| `OfferPools[].ActiveOffers` | `1` | Number of consecutive classes available in each rotation window. |
| `OfferPools[].RotationHours` | `24` | UTC hours per window. |
| `OfferPools[].Months` | `[]` | UTC months in which pooled offers can trade; empty allows all months. |

See [rotation, seasonal restrictions, and pool limits](rotating-and-seasonal-offers.md). These rules affect both buying and selling.

### Category and listing objects

Each category's `DisplayName` labels its menu category, `CurrencyId` optionally overrides the base currency, and `Listings` contains its offers. Filename supplies category identity.

Every listing field is explained in the [listing field table](catalog-and-listings.md#listing-fields): `ClassName`, `PersistenceId`, `BuyPrice`, `SellPrice`, `AllowDuplicate`, `RequiredItems`, `RequiredLiquidType`, `InitialStock`, `MaxStock`, `RestockAmount`, `RestockIntervalSeconds`, `MinimumHealthPercent`, `DeliveryMode`, `SpawnQuantity`, `SpawnFullQuantity`, and `Attachments`.

See [stock and pricing calculations](settings-stock-and-pricing.md), [contents and liquids](ammo-liquids-and-purchase-contents.md), and [material-cost examples](economy-recipes.md). Shop stock records counts; ordinary resale does not put the submitted item's condition or contents on the shelf. Use P2P to resell the actual stored item.

## Static location objects

`Locations` is an array of groups in `Traders/Locations.json`.

| Group field | Initializer | Meaning |
| --- | --- | --- |
| `Id` | Empty | Unique location group identifier. |
| `Enabled` | `true` | Enables this group; global static-trader switch controls its shop entities and placed objects. |
| `CurrencyId` | Empty | Group currency override. |
| `Traders` | `[]` | Trader entities bound to catalog profiles. |
| `Objects` | `[]` | Placed props and terminals, separate from trader entries. |
| `Safezone` | Disabled zone | Group safe-zone policy, independent of each trader's opening hours. |

The [trader entry table](locations-and-safezones.md#trader-groups) explains `TraderId`, `CurrencyId`, `EntityClassName`, `Enabled`, `OpeningHoursEnabled`, `OpeningHour`, `ClosingHour`, `Attachments`, `VehicleSpawnPoints`, `Position`, and `Orientation`.

Entry initializers are `OpeningHoursEnabled: false`, `OpeningHour: 0`, `ClosingHour: 24`, empty attachments and vehicle points, empty class/profile/currency strings, and `Enabled: true`. Supply valid classes, profile references, and transforms. Opening hour accepts `0–23`, closing hour `0–24`; equal hours stay open. Loadout attachments apply to survivor traders. Static trader entities are made invulnerable; route traders use their route's `Invulnerable` switch.

### Transforms and placed objects

`Position` is `[x, y, z]` in metres: east/west, elevation, north/south. `Orientation` is `[yaw, pitch, roll]` in degrees. Both arrays need exactly three numbers. Vehicle spawn points contain these two fields. Static and route `Objects` add `ClassName` to the transform.

Static objects must derive from `House`; route props use different class restrictions. See [static objects](locations-and-safezones.md#static-location-objects) and [route stop limits](traveling-traders-and-routes.md#stop-fields). A route stop's `Safezone.Center` is absolute, not an offset from its NPC.

### Safe zones

The same safe-zone object is used by groups and stops. The [safe-zone field table](locations-and-safezones.md#safe-zone-settings) explains all fields: `Enabled`, `Center`, `Radius`, `BlockIncomingDamage`, `BlockOutgoingDamage`, `ProtectPlayerEquipment`, `DeleteAnimals`, `DeleteInfected`, `BlockWeaponFire`, `BlockExplosives`, `BlockBuilding`, `VehicleSpeedLimitKmh`, `ShowNotifications`, `ExitProtectionSeconds`, `PreserveHunger`, `PreserveThirst`, `PreserveDisease`, `PreserveTemperature`, `PreserveBleeding`, and `ExcludedEntityClasses`.

## Route objects

`Routes` is an array of traveling merchant definitions. Each definition has a `Stops` array. The [route field table](traveling-traders-and-routes.md#route-fields) explains `Id`, `Enabled`, `TraderId`, `EntityClassName`, `Attachments`, `RandomStops`, `RandomStartStop`, `Loop`, `DepartureGraceSeconds`, `Invulnerable`, `AnnounceArrival`, `AnnounceDeparture`, `AnnounceInChat`, `AnnouncementRadius`, `ShowNextStop`, `ShowMapMarker`, `RestockOnArrival`, `StockMode`, `DeliveryDelaySeconds`, `SpawnRetrySeconds`, and `MaxBlockedSpawnAttempts`.

The [schedule reference](traveling-traders-and-routes.md#schedules-and-clock-selection) covers `ScheduleEnabled`, `ScheduleUsesGameTime`, `ScheduleStartHour`, `ScheduleEndHour`, `ScheduleWeekdays`, `ScheduleMonths`, `ActiveFromDate`, `ActiveUntilDate`, `ScheduleStartMonth`, `ScheduleStartDay`, `ScheduleEndMonth`, and `ScheduleEndDay`. Date bounds default to `0`; annual bounds default to all four fields `0`; weekdays and months default to all days and months. Windows combine: a date must pass every enabled filter.

The [stop field table](traveling-traders-and-routes.md#stop-fields) explains `Id`, `Name`, `Position`, `Orientation`, `WaitMinutes`, `TravelMinutes`, `AllowBuying`, `AllowSelling`, `PurchaseCutoffSeconds`, `SellingCutoffSeconds`, `CurrencyId`, `StockLimits`, `Prices`, `SpawnClearanceRadius`, `AllowedCategories`, `NextStopIds`, `VehicleSpawnPoints`, `Objects`, and `Safezone`.

`Stops[].Prices[]` contains `ClassName`, optional `CurrencyId`, `BuyPrice`, and `SellPrice`. Class must already be offered by the route's profile. Prices default to `-1`; specifying an override replaces both directions, so supply both deliberately. `StockLimits` is a class-to-integer object, not an array of price objects. `VehicleSpawnPoints` and `Objects` use the transforms above. Omitted `Safezone` is `null`; omitted stop filters, prices, stock limits, props, and vehicle points are empty.

## Banking and player market

The [bank settings table](banking-and-currencies.md#bankingsettingsjson) explains every field in `Banking/Settings.json`, including the nested `Currencies[].CurrencyId`, `Enabled`, `MaxBankBalance`, and `InitialBalance` entries. These entries refer to item currencies from the catalog; they do not define new currencies.

The [market settings table](player-market-server.md#p2psettingsjson) explains every field in `P2P/Settings.json`: `CurrencyId`, `MinimumPrice`, `MaximumPrice`, `MaxListingsPerPlayer`, `MaxActiveListings`, `BuyOrdersEnabled`, `MaxBuyOrdersPerPlayer`, `MaxActiveBuyOrders`, `ListingExpirySeconds`, `SettledRetentionSeconds`, `ListingFee`, `SalesCommissionPercent`, `MinimumSalesCommission`, `MinimumConditionPercent`, `InteractionRadius`, `AllowAttachments`, `AllowCargo`, `AllowedClassNames`, `DeniedClassNames`, and `MarketBoardClasses`.

Wanted-order requirements are created through the player market menu and saved in listing journals. They are not extra keys for `P2P/Settings.json`. See [wanted-order requirements](player-market.md#wanted-order-requirements) for their meaning and limits.

## Vehicle attachment sets

`Vehicles/Attachments.json` contains `Version: 1` and `Vehicles`, an array of attachment sets. Each set contains `ClassName` (exact vehicle class) and `Attachments` (ordered part class names). Repeat a wheel class for each fitted wheel. Both strings and slot compatibility must match the actual installed vehicle mod. Empty or missing sets supply no configured parts.

Each set allows up to 500 attachment entries; the whole purchase still shares the 500-object work limit. The validator checks existing vehicle and part classes and attachment slots; incompatible parts can be skipped with a warning. Ordinary listing `Attachments` is a separate field; configure vehicle parts here. See [vehicle purchases](vehicles-keys-and-storage.md#buying-vehicles) for fluids, keys, delivery, and placement.

## Garage sites

The [garage field table](vehicles-keys-and-storage.md#server-setup) explains the root policy in `Vehicles/Garages.json`. The bundled file includes one example in `StandaloneMeters`; its script initializer is an empty array. Example coordinates are not a placed terminal.

Each `StandaloneMeters[]` entry has these fields:

| Field | Initializer | Meaning |
| --- | --- | --- |
| `Id` | Empty | Unique, stable site ID used by stored-vehicle records. |
| `MeterPosition` | `[]` | Expected world position of the placed standalone meter. |
| `ZoneCenter` | `[]` | World center of the oriented parking area. |
| `ZoneSize` | `[]` | Full width, height, and depth of that area in metres. |
| `ZoneYaw` | `0` | Area rotation in degrees; absolute value no greater than 360. |
| `Spawn` | Unset | Retrieval transform containing `Position` and `Orientation`. |
| `AllowedVehicleTypes` | `["Land"]` | Accepted vehicle types: `Land`, `Air`, `Water`, or combined `Land` and `Air`. |

All coordinate arrays contain three numbers within ±100000. `Spawn` must lie inside the parking zone; spawn yaw accepts ±360 and pitch/roll must be zero. See [standalone site geometry, size limits, and meter matching](vehicles-keys-and-storage.md#standalone-meters).

## Generated JSON is saved state

`Stock.json`, `StockDelta.json`, account files, transaction journals, bank directory and transfer files, route state, market records, garage records, receipts, and telemetry are generated state. Their versions and internal recovery fields are separate from configuration `Version: 1`. Treating them as settings can break ownership, balances, or interrupted-operation recovery.

Use the [backup and recovery guide](administration-and-recovery.md#backup-sets) to preserve matching state. Client favorites and recent purchases are saved in the player's local game profile rather than server JSON.

## Source verification

Checked against current files in `I:\DayZ Mods\RaG_Trader` on **8 November 2026**, including local changes above source commit `079261d`. Field coverage includes script configuration models, bundled JSON, validators, runtime services, and player UI. Local source changes include instant route travel, blocked-stop skipping, departure warnings, and map-marker updates; older releases may behave differently. This reference describes that source snapshot.
