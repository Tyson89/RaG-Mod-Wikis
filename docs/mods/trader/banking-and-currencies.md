# Banking and currencies

RaG Trader supports two catalog currency types:

- `item`: physical denomination classes in player inventory;
- `account`: persistent numeric balance with no physical items needed for trade.

ATM bridges configured physical item currency and persistent account balance.

## Default Euro currency

```json
{
  "Id": "euro",
  "DisplayName": "Euro",
  "Type": "item",
  "CurrencyItems": [
    { "ClassName": "RaG_Euro_1", "Value": 1, "UseQuantity": true },
    { "ClassName": "RaG_Euro_2", "Value": 2, "UseQuantity": true },
    { "ClassName": "RaG_Euro_5", "Value": 5, "UseQuantity": true },
    { "ClassName": "RaG_Euro_10", "Value": 10, "UseQuantity": true },
    { "ClassName": "RaG_Euro_20", "Value": 20, "UseQuantity": true },
    { "ClassName": "RaG_Euro_50", "Value": 50, "UseQuantity": true },
    { "ClassName": "RaG_Euro_100", "Value": 100, "UseQuantity": true },
    { "ClassName": "RaG_Euro_200", "Value": 200, "UseQuantity": true }
  ]
}
```

Built-in notes stack up to 500 per object. `UseQuantity: true` makes stack quantity the number of notes: 20 units of `RaG_Euro_50` carry a value of 1000. A stack of 500 value-200 notes carries 100,000. Splitting or combining stacks does not change their total value.

Keep `UseQuantity: true` for the built-in stackable notes. Setting it to false counts an entire stack as one note, regardless of how many notes it contains.

## Currency validation

| Field | Rules |
| --- | --- |
| `Id` | Non-empty and unique, including case-insensitive duplicate checks. Use stable spelling. |
| `DisplayName` | UI label. |
| `Type` | Exactly `"item"` or `"account"`. |
| `CurrencyItems` | Required array. Item currency must contain entries; account currency may use empty array. |
| `ClassName` | Existing class in `CfgVehicles`, `CfgWeapons`, or `CfgMagazines`. Unique inside currency. |
| `Value` | Positive integer, unique inside currency. |
| `UseQuantity` | `false`: each object one denomination unit. `true`: floored item quantity is number of units. |

Item currency must include denomination with value `1`. Server sorts denominations high-to-low, builds payout greedily, and uses value-1 entry to represent any integer remainder.

Use the exact `CurrencyItems` field shown above. An item currency with an empty denomination array fails validation.

### Stack currency

Example using quantity stack where each unit is worth 1:

```json
{
  "Id": "nails",
  "DisplayName": "Nails",
  "Type": "item",
  "CurrencyItems": [
    {
      "ClassName": "Nail",
      "Value": 1,
      "UseQuantity": true
    }
  ]
}
```

Currency item must support meaningful quantity maximum. Payout creates stacks up to class maximum. Debit can reduce partial stack quantity.

## Physical wallet rules

Server scans full player inventory preorder plus item in hands. It recognizes currency in clothing, backpacks, attachments, cargo, and nested storage.

Currency item is ignored when:

- ruined;
- contains attachment;
- contains cargo;
- quantity-mode stack has floor quantity `0`.

For purchase, server may take high notes and create exact change. Change, sale payout, deposit rollback, and ATM withdrawal first try player inventory. With `AllowGroundFallback: true`, created currency that does not fit is placed on surface at player position. With fallback disabled, delivery failure rolls transaction back where supported.

!!! tip "Secure ground payouts immediately"
    Full inventory can turn change, sale proceeds, or ATM withdrawal into world items at player feet. Clear room before large trades and do not transact in crowded or unsafe terrain.

!!! tip "Use compact denomination ladder"
    Too many one-value physical objects create inventory and performance pressure. Provide sensible larger notes while retaining value 1 for exact change.

## Account currency

Example:

```json
{
  "Version": 1,
  "DefaultCurrencyId": "credits",
  "Currencies": [
    {
      "Id": "credits",
      "DisplayName": "Credits",
      "Type": "account",
      "CurrencyItems": []
    }
  ],
  "Traders": []
}
```

Trades debit/credit persistent account directly. No notes, payout capacity, change, or ATM needed. The example shows only currency structure: add actual trader profiles/categories and matching locations for a usable shop.

For account-only operation, use `Banking.json` with `"Enabled": false` and `"Currencies": []`, or keep enabled banking exclusively for separate physical currencies. A default `euro` bank entry referencing a removed catalog currency fails validation.

Account currency can be selected by the catalog default or a location, category, or route-stop override. A listing has one applicable currency at a given shop and stop, with one base price pair.

## `Banking.json`

Default:

```json
{
  "Version": 1,
  "Enabled": true,
  "DepositFeePercent": 0.0,
  "WithdrawalFeePercent": 0.0,
  "AllowDepositAll": true,
  "Currencies": [
    {
      "CurrencyId": "euro",
      "Enabled": true,
      "MaxBankBalance": -1,
      "InitialBalance": 0
    }
  ]
}
```

### Banking fields

| Field | Default | Effect |
| --- | ---: | --- |
| `Version` | `1` | Must match banking schema. |
| `Enabled` | `true` | Master ATM/account initialization switch. |
| `DepositFeePercent` | `0.0` | `0`–`100`; fee rounds up. Deposit credits gross minus fee. |
| `WithdrawalFeePercent` | `0.0` | `0`–`100`; fee rounds up. Withdrawal debits requested plus fee. |
| `AllowDepositAll` | `true` | Exposes Deposit all control in ATM UI. |
| `Currencies[].CurrencyId` | required | Must match catalog item currency for ATM visibility. |
| `Currencies[].Enabled` | `true` | Enables bank storage for currency. |
| `Currencies[].MaxBankBalance` | `-1` | `-1` unlimited; non-negative hard deposit ceiling. Values below `-1` become `-1`. |
| `Currencies[].InitialBalance` | `0` | One-time amount on first initialization, clamped to `0` and max balance. |

ATM exposes only catalog currencies with `Type: "item"` and matching enabled bank entry. Account currencies do not appear because they already are stored balances.

ATM UI shows both carried physical balance and stored bank balance for selected currency. Cycling currency refreshes both values.

## Fee math

Fee:

```text
ceil(amount × percent / 100)
```

Deposit 100 at 2.5%:

```text
wallet removes 100
fee = ceil(2.5) = 3
bank credits 97
```

Withdraw 100 at 2.5%:

```text
bank debits 103
wallet receives 100
```

100% deposit fee credits zero and transaction is rejected as invalid amount. High fees make small transactions disproportionately expensive because rounding always goes up.

## Initial balance behavior

Each account records initialized currency IDs. First balance access for enabled bank currency:

1. if currency not initialized and has no prior balance, set `InitialBalance`;
2. mark currency initialized;
3. save account atomically.

Changing `InitialBalance` later does not re-grant players already marked initialized. This prevents restart farming.

Enabled `Banking.json` accepts only known catalog currencies of type `item`. Do not add account currency as a bank entry to grant starting credits: validation rejects it. Direct account currency starts at zero unless balance is provided through controlled account administration or a custom integration. `MaxBankBalance` is an ATM deposit limit, not a generic account-trade credit cap.

## Account persistence

Path:

```text
$profile:\RaG_Core\Configs\RaG_Trader\Accounts\<Steam64>.json
```

Example:

```json
{
  "Version": 1,
  "PlayerId": "76561198000000000",
  "Balances": [
    { "CurrencyId": "euro", "Balance": 12500 }
  ],
  "InitializedCurrencies": ["euro"]
}
```

Identity must resolve to numeric platform ID. Files use atomic save and backup recovery. Treat them as sensitive economic/player data. Never publish directory.

### Granting or resetting balance manually

1. Stop server.
2. Back up player JSON and `.bak`.
3. Edit `Balances` deliberately.
4. Keep `PlayerId` exact.
5. Preserve `InitializedCurrencies` unless deliberately administering first-time physical-bank initialization.
6. Start server and verify account.

Initialization grants only when no balance entry exists. Removing its marker alone does not replace an existing balance. Keep both records consistent; do not use deletion as routine troubleshooting.

## ATM placement and distance

Place `RaG_ATM` through map loader/editor or mission code. It is not created by `Locations.json`.

Server checks player-to-ATM distance against `Settings.json` `InteractionDistance`, even though client action target uses 3 metres. Keep global interaction distance at least practical default.

## Currency selection and precedence

Define each currency once in `Catalog.json`. The effective listing currency follows this order, with each non-empty override replacing the earlier choice:

1. `Catalog.json` → `DefaultCurrencyId`.
2. `Locations.json` → location group's `CurrencyId`.
3. Individual trader entry's `CurrencyId`.
4. Category file's `CurrencyId`.
5. Active route stop's `CurrencyId`.

Route `Prices[]` entries may include `CurrencyId`, but validation requires it to match the effective stop currency for that class. Omit it to inherit. It is not a way to introduce a different currency for one stop-price entry.

Category fragment:

```json
{
  "DisplayName": "Specialist Supplies",
  "CurrencyId": "credits",
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

Use the account currency `credits` defined above and attach this category to a trader profile. A Euro location can then have a credits-only specialist category. A route stop with `CurrencyId: "euro"` overrides that category while visiting the stop.

!!! tip "Clear defaults where inheritance is intended"
    Bundled location groups and their individual trader entries explicitly select `euro`. Setting only a group's currency will not override its entries. Clear an entry's `CurrencyId` to `""` when it should inherit the group. Inspect category overrides too.

Currency selection leaves the numeric price unchanged. A base price of 300 becomes 300 units of the selected currency; no exchange rate is applied. Tune prices around the value and availability of each currency, or use distinct categories/route stop prices.

## Multi-currency possibilities and limits

- Physical Euro shops with ATM savings, plus a separate account-credit specialist.
- Regional currencies selected per location group; individual traders can be exceptions.
- Category-based quest-token shops sharing the same market square.
- Traveling merchants using the currency and price schedule of each destination.
- Several enabled physical currencies stored independently at ATMs.

Each checkout uses one currency. Separate purchases into different baskets when categories use different currencies. Physical-currency shops spend carried items; account-currency shops debit the numeric account. Banking a physical currency does not make that balance directly spendable at its shops.

There is no built-in exchange-rate service, player-to-player bank transfer, interest, or recurring account grant. Currency definitions and the catalog default require a restart. Category currency can reload; location currency requires a restart; route stop currency follows the [paused-route reload rules](traveling-traders-and-routes.md#editing-and-recovering-routes).

## Economy tips

- Keep `EnableTradeLogging` on; bank operations need Info log enabled for detailed audit.
- Test inventory-full withdrawal with ground fallback both enabled and disabled.
- Test overpay/change with every denomination.
- Avoid denomination classes that players can craft or duplicate cheaply unless intentional.
- Keep initial balance low; it is permanent economic injection per new player.
- Set finite `MaxBankBalance` only when cap has real design purpose; it can block deposits after fee calculation.
- Back up account directory before currency IDs or denomination classes change.
