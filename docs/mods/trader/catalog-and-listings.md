# Catalog, categories, and listings

`Trading/Catalog.json` defines currencies and trader profiles. Each profile references category filenames under `Trading/Categories/`. A static location or route references the profile's `Id` to give it a place in the world.

## Trader profiles

| Catalog field | Purpose |
| --- | --- |
| `Version` | Use `1`. |
| `DefaultCurrencyId` | Base currency. If blank and exactly one valid currency exists, that currency becomes the default. |
| `Currencies` | See [currency definitions](banking-and-currencies.md). |
| `Traders` | Profiles with unique `Id`, menu `DisplayName`, category filename list `Categories`, and optional [`OfferPools`](rotating-and-seasonal-offers.md). |

## Category files

Save this example as `Trading/Categories/Trail_Supplies.json`. Add `"Trail_Supplies"` to the desired profile's `Categories` array.

```json
{
  "DisplayName": "Trail Supplies",
  "Listings": [
    {
      "ClassName": "Hatchet",
      "BuyPrice": 300,
      "SellPrice": 80,
      "InitialStock": 5,
      "MaxStock": 20
    }
  ]
}
```

Use 1–64 letters, digits, underscores, or hyphens in the filename stem. A category may set `CurrencyId` to override the default for its listings. Traders that share a category share its listing IDs and ordinary stock. Use different category files when regional shops need distinct stock or prices.

The category wrapper contains `DisplayName` (menu label), optional `CurrencyId`, and `Listings` (offer objects). Its `Id` comes from the filename; do not add an `Id` or `Version` field. Only categories referenced by profiles are loaded, once per filename, up to 500 files. An unreferenced JSON file creates no shop. Missing or unsafe filenames can skip a category; malformed JSON in a referenced file can reject loading.

## Listing fields

| Field | Default | Effect |
| --- | --- | --- |
| `ClassName` | Required | Exact game or mod item class. |
| `PersistenceId` | Empty | Optional stable listing ID. |
| `AllowDuplicate` | `false` | Set on every intentional copy of a class at the same trader to suppress duplicate warnings. |
| `BuyPrice`, `SellPrice` | `-1`, `-1` | Positive price enables the direction. Use `-1` to disable it. |
| `RequiredItems` | `[]` | Exact class names consumed per item bought or per loose round. Repeat a class to require multiple objects. |
| `RequiredLiquidType` | Empty | Named [liquid](ammo-liquids-and-purchase-contents.md#liquid-specific-listings) supplied on purchase and required on sale. |
| `InitialStock`, `MaxStock` | `-1`, `-1` | Starting count and capacity. Use `-1` for both to make stock unlimited. |
| `RestockAmount`, `RestockIntervalSeconds` | `0`, `0` | Replenishment amount and interval for finite stock. Set both together. |
| `MinimumHealthPercent` | `0.0` | Minimum global health percentage for resale. Ruined items are ineligible. |
| `DeliveryMode` | `"inventory"` | `"inventory"` or `"ground"`. Ground delivery takes one ordinary object or the requested loose rounds. Vehicles use their spawn points. |
| `SpawnQuantity`, `SpawnFullQuantity` | `0`, `true` | Control the initial fill of each purchased item. |
| `Attachments` | `[]` | Classes attached to each purchased object. Vehicle parts come from `Vehicles/Attachments.json`. |

Set at least one positive price. When both prices are enabled, keep `SellPrice` at or below `BuyPrice`. Loose ammo prices are per round. Other prices are per object. Check [ammo price relationships](ammo-liquids-and-purchase-contents.md#price-boxes-magazines-and-rounds-together) when a purchase supplies ammunition that players can resell.

`0` prices are normalized to disabled with a warning; they do not create free offers. `MinimumHealthPercent` accepts `0–100`; `SpawnQuantity` must be nonnegative. `RequiredItems` and `Attachments` each allow up to 500 entries, but the complete checkout still shares the 500-object work limit. Materials are whole eligible objects of the exact class, not quantity units from one stack. Normal sales do not refund the materials spent on purchase.

Listing `Id`, `DisplayName`, `Price`, `LiquidType`, and `ConfigError` are runtime fields, not listing JSON settings. Put currency on the category, location, or route stop; the listing has no configurable `CurrencyId` or nested `Prices` array.

## Listing IDs

The default ID combines category and class in lowercase. For example, `Trail_Supplies.json` and `Hatchet` produce `trail_supplies_hatchet`. The stock identity map distinguishes liquid variants and gives duplicates distinct suffixes. Identical duplicates depend on their occurrence order.

Use `PersistenceId` to pin a listing when several entries share the same category, class, and liquid. Use a unique ID of 1–128 lowercase letters, digits, underscores, or hyphens. To keep existing stock, use the listing's existing ID and pin all affected duplicate entries before reordering. An ID already associated with a different category or class is rejected.

## Custom items

Make the supplying mod available to server and players. Add the exact class to one category, reference the category from the right profile, and check `ConfigValidationReport.txt`. Test purchase, contents, and resale. A preview model alone does not verify attachment fit, item delivery, or liquid compatibility.

See [economy recipes](economy-recipes.md) for finite stock, material costs, and custom shop examples.
