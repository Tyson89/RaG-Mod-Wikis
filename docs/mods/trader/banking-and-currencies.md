# Banking and currencies

RaG Trader supports physical item currencies and account currencies. Prices use whole units of the selected currency.

## Physical currency

The bundled `euro` currency uses `RaG_Euro_1`, `RaG_Euro_2`, `RaG_Euro_5`, `RaG_Euro_10`, `RaG_Euro_20`, `RaG_Euro_50`, `RaG_Euro_100`, and `RaG_Euro_200`. Each value counts per note in a stack. A stack of three value-20 notes is worth 60.

Define currencies in `Trading/Catalog.json`. This object goes in its `Currencies` array.

```json
{
  "Id": "tokens",
  "DisplayName": "Tokens",
  "Type": "item",
  "CurrencyItems": [
    {"ClassName": "RaG_Euro_1", "Value": 1, "UseQuantity": true},
    {"ClassName": "RaG_Euro_5", "Value": 5, "UseQuantity": true}
  ]
}
```

This example assumes those note classes are assigned only to this currency. An item currency needs positive, distinct denominations and a value-1 item for exact change. Set `UseQuantity` to `true` when value is per quantity unit in a supported stack. Set it to `false` when each item instance is one denomination. Use distinct physical classes across currencies.

Eligible notes must be in your carried inventory. Leave room for change or payouts. Whether the trader can drop a payment at your feet depends on server settings and the transaction.

## Account currency

Use `Type: "account"` with an empty `CurrencyItems` array to trade with stored credits. Purchases debit the account and sales credit it. Account currencies work directly at traders or the player market and have no ATM cash denomination. Built-in account credits start at zero.

```json
{
  "Id": "credits",
  "DisplayName": "Credits",
  "Type": "account",
  "CurrencyItems": []
}
```

## `Banking/Settings.json`

Enable `EnableBanking` in the Trader root `Settings.json`, add bank entries for physical currencies, and place `RaG_ATM`. Restart after banking configuration changes.

```json
{
  "Version": 1,
  "DepositFeePercent": 0.0,
  "WithdrawalFeePercent": 0.0,
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

- `MaxBankBalance: -1` leaves the balance uncapped by policy. A nonnegative cap limits incoming funds such as deposits, transfers, and market proceeds.
- `InitialBalance` is a one-time balance for that player and banked currency. It applies when the enabled currency is first initialized. Existing initialized balances keep their value.
- Fees accept `0–100` percent with up to two decimal places. Round each fee up to a whole currency unit. A 101-unit deposit at 2% credits 98. A 101-unit withdrawal at 2% debits 104 and delivers 101 in notes.

## Use an ATM

Select a currency and enter an amount for **Deposit** or **Withdraw**, or use **Deposit all** or **Withdraw all**. The preview shows the fee and how much is credited or debited. Keep room in your inventory when withdrawing. The ATM action uses a 3 m range and the server checks `InteractionDistance`.

## Player-to-player bank transfers

Enable `EnableBankTransfers` alongside `EnableBanking` in root `Settings.json`. At an ATM, select an enabled currency and open **Transfer**. Search by 2–32 characters of the player's name, then verify the selected name and recipient code before confirming. Search includes offline players who have connected before and returns up to 20 matches.

Transfers use stored balance, with no ATM deposit or withdrawal fee. Recipient caps still apply. Both players get receipts. If a transfer is held for recovery, check **History** and ask an admin to inspect it before sending again.

The default account files are `Accounts/<Steam64>.json` in the Trader config directory. Preserve them with `BankDirectory/<Steam64>.json` and `BankTransfers.json`.

## Paying a trader from bank

For a banked item currency, switch between **Pay: Cash** and **Pay: Bank** in the trader's purchase menu. Bank payment debits the selected currency's stored balance. Sales in that currency still pay in physical items. Account currency trades use their account automatically.

## Currency selection and precedence

The base is `DefaultCurrencyId` in `Trading/Catalog.json`. For a static trader, a nonempty location group currency overrides it, then the trader entry currency, then the category currency. For a traveling trader, the category currency overrides the default and the current stop's currency overrides both. A stop price can specify the same effective currency explicitly.

Changing currency leaves the numeric price as configured. For example, a price of 300 with a `credits` override costs 300 credits.
