# Catalog, categories, and listings

RaG Trader separates structure from item data:

```text
Catalog.json
  currencies
  trader profiles
  category filename references

Categories\<name>.json
  category display name
  listings
```

This keeps large catalogs manageable and lets several traders reuse same category.

## `Catalog.json`

Compact example:

```json
{
  "Version": 1,
  "DefaultCurrencyId": "euro",
  "Currencies": [
    {
      "Id": "euro",
      "DisplayName": "Euro",
      "Type": "item",
      "CurrencyItems": [
        { "ClassName": "RaG_Euro_1", "Value": 1, "UseQuantity": false },
        { "ClassName": "RaG_Euro_10", "Value": 10, "UseQuantity": false },
        { "ClassName": "RaG_Euro_100", "Value": 100, "UseQuantity": false }
      ]
    }
  ],
  "Traders": [
    {
      "Id": "survival",
      "DisplayName": "Survival Trader",
      "Categories": ["Food", "Tools", "Medical"]
    }
  ]
}
```

### Catalog fields

| Field | Rules and effect |
| --- | --- |
| `Version` | Must be `1`. |
| `DefaultCurrencyId` | Currency used to create price for every listing. If blank and exactly one valid currency exists, that currency becomes default. |
| `Currencies` | Unique currency definitions. See [banking and currencies](banking-and-currencies.md). |
| `Traders` | Unique trader profiles. Profile does not place entity; `Locations.json` does. |
| `Traders[].Id` | Exact value referenced by `Locations.json`. Case-sensitive. |
| `Traders[].DisplayName` | Title sent to trader UI. |
| `Traders[].Categories` | Category filenames without `.json`, in display/load order. |

Current listing schema supports one price pair in default currency. Defining several currencies is useful for account systems or banking, but listing does not provide per-currency price array. Only default currency receives listing `BuyPrice` and `SellPrice`.

## Category files

Path:

```text
$profile:\RaG_Core\Configs\RaG_Trader\Categories\Tools.json
```

Example covering every listing field:

```json
{
  "DisplayName": "Tools",
  "Listings": [
    {
      "ClassName": "Hatchet",
      "AllowDuplicate": false,
      "BuyPrice": 300,
      "SellPrice": 120,
      "Stock": 20,
      "RestockAmount": 2,
      "RestockIntervalSeconds": 900,
      "MinimumHealthPercent": 35.0,
      "DeliveryMode": "inventory",
      "SpawnQuantity": 0,
      "SpawnFullQuantity": true,
      "Attachments": []
    }
  ]
}
```

`DisplayName` appears in UI. Filename `Tools` becomes internal category ID. Category JSON has no explicit `Id` field.

### Category filename rules

- Maximum 64 characters.
- Allowed: `a-z`, `A-Z`, `0-9`, `_`, `-`.
- No spaces, dots, path separators, or `.json` in catalog reference.
- At most 500 unique category files may be referenced.
- Missing referenced file installs from bundled defaults only when bundled file with same name exists.
- Custom missing file stops category loading; restore from backup.

## Listing fields

| Field | Default | Meaning |
| --- | ---: | --- |
| `ClassName` | required | Exact class in `CfgVehicles`, `CfgWeapons`, or `CfgMagazines`. |
| `AllowDuplicate` | `false` | Suppresses duplicate-class warning only when `true` on every copy visible at same trader. Does not merge entries. |
| `BuyPrice` | `-1` | Base player purchase price. Positive enables buying. Use `-1` to disable. |
| `SellPrice` | `-1` | Base trader payout. Positive enables selling. Use `-1` to disable. |
| `Stock` | `-1` | `-1` unlimited; `0` empty; positive value is initial stock and hard maximum. |
| `RestockAmount` | `0` | Units added each restock interval. Must pair with positive interval and finite positive stock. |
| `RestockIntervalSeconds` | `0` | Restock interval, allowed `0` through `86400`. Must pair with positive amount. |
| `MinimumHealthPercent` | `0.0` | Sale eligibility threshold, `0` through `100`. Separate from payout scaling. |
| `DeliveryMode` | `"inventory"` | `"inventory"` or `"ground"`. Ground forces quantity `1`. |
| `SpawnQuantity` | `0` | Positive explicit energy, ammo, or quantity for purchased item. |
| `SpawnFullQuantity` | `true` | When explicit quantity is `0`, fill energy, magazine ammo, or quantity to maximum. |
| `Attachments` | `[]` | Exact classes created as attachments on every purchased entity. Any failure aborts delivery. |

At least one of `BuyPrice` or `SellPrice` must be positive. `0` is not usable price; use `-1` for deliberate disable.

### Listing IDs

Server derives ID:

```text
lowercase(<category filename>_<ClassName>)
```

Example: `Tools.json` + `Hatchet` becomes `tools_hatchet`.

If same derived ID repeats, later entry receives `_2`, `_3`, and so on. Do not put `Id` in JSON. Stock persistence uses derived ID, so renaming category file or class resets association and leaves old stock entry orphaned.

## Buy-only and sell-only listings

Buy-only:

```json
{
  "ClassName": "LandMineTrap",
  "BuyPrice": 2500,
  "SellPrice": -1,
  "Stock": 3
}
```

Sell-only:

```json
{
  "ClassName": "BearPelt",
  "BuyPrice": -1,
  "SellPrice": 800,
  "Stock": -1,
  "MinimumHealthPercent": 50.0
}
```

For finite stock, selling increases available stock up to `Stock` hard maximum. A sell-only finite listing at full stock rejects sales. Use `Stock: -1` for unlimited sink.

## Purchased quantities and attachments

Spawn setup checks item type in this order:

1. Energy Manager item: set energy.
2. Magazine: set ammo count.
3. Quantity item: set quantity.

`SpawnQuantity > 0` wins. Otherwise `SpawnFullQuantity: true` fills maximum. For ordinary non-quantity items, both settings do nothing.

Full magazine with optic and suppressor:

```json
{
  "ClassName": "M4A1",
  "BuyPrice": 4000,
  "SellPrice": 1400,
  "Stock": 5,
  "SpawnFullQuantity": true,
  "Attachments": [
    "M4_OEBttstck",
    "M4_PlasticHndgrd",
    "M68Optic",
    "M4_Suppressor"
  ]
}
```

Attachment must fit class and available slot. Duplicate attachment class can be repeated when entity has several compatible slots. If one attachment cannot be created, whole item delivery rolls back.

## Ground delivery

```json
{
  "ClassName": "SeaChest",
  "BuyPrice": 1000,
  "SellPrice": 300,
  "Stock": 10,
  "DeliveryMode": "ground"
}
```

Ground item spawns on surface at player position. Purchase quantity must be `1`. Leave clear, level space around trader; avoid roofs, cliffs, water, clutter, and other places where spawned object can overlap or become hard to recover.

Global `AllowGroundFallback` affects failed inventory delivery, physical-currency change and payouts, deposit rollback, and ATM withdrawal. It does not change explicit ground listing.

## Custom mod items

1. Confirm mod is required on server and clients.
2. Use exact public class name.
3. Put listing in dedicated custom category file.
4. Reference category from wanted trader profile.
5. Choose conservative price and stock.
6. Test preview, inventory delivery, ground fallback, attachments, sale eligibility, and restart stock.

Recommended layout:

```text
Categories\MyMod_Weapons.json
Categories\MyMod_Items.json
Categories\MyMod_Vehicles.json
```

Keeping third-party classes separate makes updates and removals much safer.

## Shared and independent stock possibilities

- Same category referenced by several trader profiles: same listing ID, shared stock.
- Same trader profile used at several physical locations: shared stock.
- Same class copied to different category filename: different listing ID, independent stock.
- Same class duplicated inside one trader: separate entries, warning unless every duplicate has `AllowDuplicate: true`.

Use shared stock for global economy. Use separate category files for regional markets.

## Recommended catalog cleanup

Current defaults contain all 2,014 public vanilla tradeable classes. Before production:

- remove debug, obsolete, unwanted opened-food, book, and seasonal entries;
- set deliberate car and boat sell prices; vehicle sales are enabled and ownership rules matter;
- separate rare weapons/ammo into finite-stock categories;
- prevent easy buy-low/sell-high loops across duplicated classes;
- verify all third-party classes after mod updates;
- keep category files small enough for human review;
- version-control production config outside live profile.
