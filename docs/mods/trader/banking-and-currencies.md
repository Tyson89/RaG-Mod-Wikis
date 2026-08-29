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
  "Denominations": [
    { "ClassName": "RaG_Euro_1", "Value": 1, "UseQuantity": false },
    { "ClassName": "RaG_Euro_2", "Value": 2, "UseQuantity": false },
    { "ClassName": "RaG_Euro_5", "Value": 5, "UseQuantity": false },
    { "ClassName": "RaG_Euro_10", "Value": 10, "UseQuantity": false },
    { "ClassName": "RaG_Euro_20", "Value": 20, "UseQuantity": false },
    { "ClassName": "RaG_Euro_50", "Value": 50, "UseQuantity": false },
    { "ClassName": "RaG_Euro_100", "Value": 100, "UseQuantity": false },
    { "ClassName": "RaG_Euro_200", "Value": 200, "UseQuantity": false }
  ]
}
```

Each note is one unit because `UseQuantity` is `false`.

## Currency validation

| Field | Rules |
| --- | --- |
| `Id` | Non-empty and unique. Case-sensitive. |
| `DisplayName` | UI label. |
| `Type` | Exactly `"item"` or `"account"`. |
| `Denominations` | Required array. Item currency must contain entries; account currency may use empty array. |
| `ClassName` | Existing class in `CfgVehicles`, `CfgWeapons`, or `CfgMagazines`. Unique inside currency. |
| `Value` | Positive integer, unique inside currency. |
| `UseQuantity` | `false`: each object one denomination unit. `true`: floored item quantity is number of units. |

Item currency must include denomination with value `1`. Server sorts denominations high-to-low, builds payout greedily, and uses value-1 entry to represent any integer remainder.

### Stack currency

Example using quantity stack where each unit is worth 1:

```json
{
  "Id": "nails",
  "DisplayName": "Nails",
  "Type": "item",
  "Denominations": [
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

For purchase, server may take high notes and create exact change. Change and sale payout must fit player inventory. No ground fallback exists for currency creation.

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
      "Denominations": []
    }
  ],
  "Traders": []
}
```

Trades debit/credit persistent account directly. No notes, payout capacity, change, or ATM needed.

Current compact listing schema prices only default currency. Several currencies may exist, but listings do not define several independent price pairs.

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

For direct `account` currency, matching enabled banking entry can also provide initial balance even though currency is not shown at ATM. `MaxBankBalance` is enforced by ATM deposit path, not generic account-currency trade credits.

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
5. Keep or remove `InitializedCurrencies` depending whether initial balance should run again.
6. Start server and verify account.

Removing initialization marker can reapply configured initial amount. Use only for intentional administration.

## ATM placement and distance

Place `RaG_ATM` through map loader/editor or mission code. It is not created by `Locations.json`.

Server checks player-to-ATM distance against `Settings.json` `InteractionDistance`, even though client action target uses 3 metres. Keep global interaction distance at least practical default.

## Multi-currency possibilities and limits

Possible:

- physical Euro trade plus bank;
- physical quest token banked separately;
- account-only credits for all trades;
- several physical currencies shown in ATM;
- one default trade currency plus other bank-only currencies.

Current limit:

- every listing price is tied to one `DefaultCurrencyId`;
- UI currency cycling has little value unless server payload includes prices for that currency;
- no exchange-rate or currency-to-currency conversion feature exists;
- bank does not transfer between players;
- no interest or periodic grants exist.

## Economy tips

- Keep `EnableTradeLogging` on; bank operations need Info log enabled for detailed audit.
- Test inventory-full withdrawal rollback.
- Test overpay/change with every denomination.
- Avoid denomination classes that players can craft or duplicate cheaply unless intentional.
- Keep initial balance low; it is permanent economic injection per new player.
- Set finite `MaxBankBalance` only when cap has real design purpose; it can block deposits after fee calculation.
- Back up account directory before currency IDs or denomination classes change.
