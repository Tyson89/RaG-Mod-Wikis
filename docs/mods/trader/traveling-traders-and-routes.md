# Traveling traders and routes

A traveling trader appears at a stop, trades during its wait window, and disappears while traveling to the next stop. One route defines one trader and its loadout. Each stop defines its own placement, props, trade policy, and optional safe zone.

## First working route

Enable `EnableRoutes` in `Settings.json` and restart. Routes live in `Routes/Routes.json` under the Trader config directory. The bundled route uses the `travelling` profile from `Trading/Catalog.json`. To make a separate route, add an entry to the `Routes` array with 2–64 stops. Use checked coordinates and distinct route and stop IDs.

```json
{
  "Id": "East Coast Market",
  "TraderId": "travelling",
  "EntityClassName": "SurvivorM_Niki",
  "Stops": [
    {
      "Id": "south",
      "Name": "South Coast",
      "Position": [13253.8, 8.3, 6099.7],
      "Orientation": [110.0, 0.0, 0.0],
      "WaitMinutes": 15,
      "TravelMinutes": 5
    },
    {
      "Id": "north",
      "Name": "North Coast",
      "Position": [12900.0, 8.0, 10000.0],
      "Orientation": [0.0, 0.0, 0.0],
      "WaitMinutes": 20,
      "TravelMinutes": 10
    }
  ]
}
```

`TravelMinutes` belongs to the **destination**. This route waits 15 minutes at South Coast, travels 10 minutes to North Coast, waits 20 minutes there, then travels 5 minutes back.

## Route fields

| Fields | Behavior |
| --- | --- |
| `Id`, `Enabled` | Unique route ID, up to 80 characters. `Enabled` defaults to `true`. |
| `TraderId`, `EntityClassName`, `Attachments` | Catalog profile, trader entity, and survivor loadout shared by all stops. Default entity is `SurvivorM_Niki`. |
| `Loop`, `RandomStops`, `RandomStartStop` | Default is a loop in array order, starting at the first stop. See [stop order](#stop-order). |
| `DepartureGraceSeconds` | Closes trade before departure. Default `15`, range `1–300`. |
| `Invulnerable` | Protects the trader entity. Default `true`. |
| `ShowNextStop`, `ShowMapMarker` | Show the next stop in trader details or mark the currently present trader on the DayZ map. Defaults `true` and `false`. |
| `AnnounceArrival`, `AnnounceDeparture`, `AnnounceInChat`, `AnnouncementRadius` | Optional notices. Chat adds a chat message. Radius is in metres, with `0` reaching everyone online. All notice switches default to `false`. |
| `SpawnRetrySeconds`, `MaxBlockedSpawnAttempts` | Default retry every `10` seconds. A positive attempt limit pauses a blocked route. Default `0` retries without a limit. |
| `StockMode`, `RestockOnArrival`, `DeliveryDelaySeconds` | Default `shared`, `false`, and `0`. See [route stock](#stock-sharing-and-arrival-deliveries). |

## Stop fields

| Fields | Behavior |
| --- | --- |
| `Id`, `Name` | ID unique within the route. Display name falls back to ID. Both allow up to 80 characters. |
| `Position`, `Orientation` | Trader transform as two arrays of three numbers. |
| `WaitMinutes`, `TravelMinutes` | Time at this stop and time to reach it. Defaults `15` and `5`. Wait must exceed departure grace. Travel must round to at least one second. Maximum `10080` minutes each. |
| `AllowBuying`, `AllowSelling` | Enable each direction. Both default to `true`. |
| `PurchaseCutoffSeconds`, `SellingCutoffSeconds` | Close each direction this many seconds before departure. The larger of the cutoff and route grace applies. Default `0` uses route grace. |
| `AllowedCategories` | Catalog category IDs from the route's trader profile. Empty allows all its categories. |
| `CurrencyId`, `Prices` | Currency override and optional per-class price overrides. |
| `StockLimits` | Per-class capacity overrides for `StockMode: "stop"`. |
| `NextStopIds` | Optional links to other stops in this route. |
| `SpawnClearanceRadius` | Search radius around trader spawn. Default `1.5` m, range `1–50`. |
| `VehicleSpawnPoints` | Separate transforms for vehicle sales and purchases at this stop. |
| `Objects` | Props with `ClassName`, `Position`, and `Orientation`. Up to 128 per stop. |
| `Safezone` | Optional [safe zone](locations-and-safezones.md#safe-zone-settings) for this stop. |

Prices replace both directions for the specified offered class. Supply both values and use `-1` to disable a direction. Omit `CurrencyId` inside each price to inherit. If set, it must match the effective currency. Example stop fragment:

```json
{
  "CurrencyId": "euro",
  "Prices": [
    {"ClassName": "Hatchet", "BuyPrice": 450, "SellPrice": 160}
  ]
}
```

Players, vehicles, and objects of the trader's exact class can block its spawn. Keep arrival space clear of player traffic. Props and the stop safe zone are removed when the trader leaves.

## Stop order

- Sequential routes follow array order. `Loop: false` ends the route after its last stop.
- `RandomStops: true` with looping picks another stop at random. Without looping it picks a later stop in the array.
- A stop with `NextStopIds` uses those links first. It takes the first link in sequential mode or picks one at random in random mode. Explicit links can create cycles even with `Loop: false`.
- `RandomStartStop` chooses the starting stop when the route initializes without matching saved state.

## Stock sharing and arrival deliveries

| `StockMode` | Inventory |
| --- | --- |
| `shared` | Same stock as static traders offering the same listing. |
| `route` | One separate stock pool for the route, carried between stops. |
| `stop` | Separate stock at each stop. Use `StockLimits` to override capacity for specific classes. |

Capacity `-1` is unlimited. Finite stop stock starts at the listing's `InitialStock`, capped by the effective capacity. Applying a finite stop cap to an unlimited listing starts that stop at capacity. When `RestockOnArrival` is enabled, one arrival adds each eligible listing's `RestockAmount` up to capacity. `DeliveryDelaySeconds` delays this delivery and must leave time before departure grace. The arrival is recorded with stock state so a normal restart does not repeat that delivery. Route and stop stock use these deliveries for replenishment. Ordinary timed restock applies to shared stock.

## Schedules and clock selection

Wait and travel durations use elapsed real time. Schedule filters use UTC by default. Set `ScheduleUsesGameTime: true` to read the DayZ calendar for those filters. `ActiveFromDate` and `ActiveUntilDate` are inclusive `YYYYMMDD` bounds with `0` meaning no bound. They apply even with `ScheduleEnabled: false`.

With `ScheduleEnabled: true`, choose:

- `ScheduleStartHour` (`0–23`) and `ScheduleEndHour` (`1–24`), with start inclusive and end exclusive. Use different values. `0` to `24` covers the full day. A window such as `20` to `6` crosses midnight.
- `ScheduleWeekdays` using Monday `1` through Sunday `7`, and `ScheduleMonths` using January `1` through December `12`. Both default to all values. Each filter uses the current date, including after midnight.
- `ScheduleStartMonth`, `ScheduleStartDay`, `ScheduleEndMonth`, and `ScheduleEndDay` for an inclusive annual window, which can cross New Year. Leave all four at `0` to omit it.

For a UTC weekend evening market, set `ScheduleEnabled: true`, `ScheduleWeekdays: [6, 7]`, `ScheduleStartHour: 18`, and `ScheduleEndHour: 23`.

## Admin controls

Open **Diagnostics** from a trader as an admin. Select a route to see its current or next stop, timers, stock scope, and spawn errors. Use the controls to pause or resume, depart, force the next phase, or jump to a specific stop. A jump starts a new arrival and can trigger a stock delivery. Refresh the panel if the route has advanced since it opened.

## Editing and recovering routes

Route state lives in `$profile:\RaG_Core\Storage\RaG_Trader\Routes\State.json` and `Delta.json` in the same folder. Keep both with `Stock.json`, `StockDelta.json`, and their backups. Route reload flushes state and reinitializes routes. A changed route definition starts that route again with a fresh arrival. Plan edits and stock deliveries together.

For a missing trader, check the global and route switches, schedule, current phase, exact entity class, and spawn clearance. If persistence is unreadable, preserve the files and inspect server logs before restoring a matched backup.
