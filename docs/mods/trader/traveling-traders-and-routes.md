# Traveling traders and routes

`Routes.json` turns location groups into traveling markets. A group appears at its configured positions, waits, disappears for the travel interval, then the next group appears. This is scheduled spawning between stops; NPCs do not walk or drive along a physical path.

A route can carry several specialists, use different currencies and prices at each destination, restrict trade directions, replenish stock on arrival, and open only during selected hours or dates. Each stop references an existing `Locations.json` group. The group supplies the NPCs or objects, trader profiles, equipment, positions, opening hours, and fallback vehicle spawn points.

## First working route

Generated defaults include three enabled groups named `Sosnovy Pass`, `Mogilevka`, and `Prison`, plus a disabled route connecting them. With that route disabled, all three groups operate as static markets. Enabling it gives the route control of those groups: only its active stop is present.

1. Stop the server and back up Trader configuration and persistence.
2. Check every referenced group and trader entry in `Locations.json`. Keep the groups enabled. Verify coordinates and clearance on your map.
3. Set the bundled route's `Enabled` to `true`, or use the complete file below.
4. Start the server. Read `ConfigValidationReport.txt`, especially `MOVING TRADERS`, and check route diagnostics.
5. Visit each stop as an ordinary player. Test arrival, purchase, sale, the departure cutoff, and absence during travel.

Complete `Routes.json` using the bundled groups:

```json
{
  "Version": 1,
  "Routes": [
    {
      "Id": "Traveling Traders",
      "Enabled": true,
      "RandomStops": false,
      "RandomStartStop": false,
      "Loop": true,
      "DepartureGraceSeconds": 15,
      "Invulnerable": true,
      "AnnounceArrival": true,
      "AnnounceDeparture": true,
      "AnnounceInChat": false,
      "AnnouncementRadius": 1500.0,
      "ShowNextStop": true,
      "ShowMapMarker": true,
      "RestockOnArrival": false,
      "StockMode": "shared",
      "Stops": [
        { "LocationId": "Sosnovy Pass", "WaitSeconds": 900, "TravelSeconds": 300 },
        { "LocationId": "Mogilevka", "WaitSeconds": 900, "TravelSeconds": 300 },
        { "LocationId": "Prison", "WaitSeconds": 900, "TravelSeconds": 300 }
      ]
    }
  ]
}
```

Each market stays for 15 real minutes. Trade closes for the final 15 seconds, then a 5-minute travel interval starts. The three-stop circuit takes 60 minutes when schedules, blocking, pauses, and recovery do not interrupt it. `TravelSeconds` belongs to the stop being departed.

!!! tip "Keep a separate permanent market"
    Use another location group for an always-available earning route, ATM area, or basic supplies shop. Do not include that group in the traveling route. A group cannot belong to two enabled routes, and a route-controlled group does not also operate as a static shop.

## Route fields

Omitted fields use these defaults. `Version` on the enclosing file is `1`.

| Field | Default | Rules and purpose |
| --- | --- | --- |
| `Id` | required | Stable route identity. Enabled route IDs must be unique after trimming and case-insensitive lookup. |
| `Enabled` | `true` | Enables route validation and control of its groups. At most 32 enabled routes. |
| `Stops` | `[]` | 2–64 stops; each references a unique enabled location group within this route. |
| `RandomStops` | `false` | Chooses a random first stop and random next stops where explicit links do not override selection. |
| `RandomStartStop` | `false` | Randomizes initial stop even when subsequent movement is sequential. Applies when creating fresh state. |
| `Loop` | `true` | Sequential route wraps to its first stop. Explicit links can define their own cycle. |
| `DepartureGraceSeconds` | `15` | Final closure interval; 1–300 seconds and shorter than every stop's wait. |
| `Invulnerable` | `true` | Disables damage to route entities. With `false`, loss of an active entity closes that visit for the whole group. |
| `StockMode` | `"shared"` | `shared`, `route`, or `stop`; see stock scopes below. |
| `RestockOnArrival` | `false` | Adds eligible listings' `RestockAmount` once per arrival, up to capacity. |
| `DeliveryDelaySeconds` | `0` | Wait after arrival before supply is added. 0–604800, and strictly less than every `WaitSeconds - DepartureGraceSeconds`. |
| `ShowNextStop` | `true` | Exposes the next destination in player route status. |
| `ShowMapMarker` | `false` | Adds present route traders to the DayZ map menu. |
| `AnnounceArrival` | `false` | Sends arrival notifications. |
| `AnnounceDeparture` | `false` | Sends departure notifications. |
| `AnnounceInChat` | `false` | Also sends enabled arrival/departure announcements as chat/status messages. |
| `AnnouncementRadius` | `0.0` | 0 means all players; positive radius limits recipients around the first active trader, in metres. Maximum 100000. |
| `SpawnRetrySeconds` | `10` | Retry blocked spawning every 1–3600 seconds. |
| `MaxBlockedSpawnAttempts` | `0` | Optional threshold, 0–10000; 0 disables this threshold. |
| `BlockedStopTimeoutSeconds` | `0` | Optional blocked duration threshold, 0–604800; 0 disables this threshold. |
| `PauseOnBlockedStop` | `true` | Pauses after an enabled blocked-attempt or timeout threshold is reached. With both thresholds zero, no threshold-based pause occurs. |
| `AlertAdminsOnBlockedStop` | `true` | Enables admin alerts for blocked-stop problems. |

Schedule fields are documented [below](#schedules-and-clock-selection). Keep explicit IDs and stop ordering stable because persisted route progress refers to them.

## Stop fields

| Field | Default | Rules and purpose |
| --- | --- | --- |
| `LocationId` | required | Existing enabled `Locations.json` group ID, resolved with trimmed, case-insensitive lookup. Maximum 80 characters. |
| `Name` | location ID | Display label, maximum 80 characters. |
| `WaitSeconds` | `900` | Real seconds at this stop; greater than departure grace and at most 604800. |
| `TravelSeconds` | `300` | Real seconds from this stop to the selected next stop; 1–604800. |
| `AllowBuying` | `true` | Allows player purchases, subject to listing price and all other checks. |
| `AllowSelling` | `true` | Allows player sales, subject to listing price and all other checks. |
| `PurchaseCutoffSeconds` | `0` | Closes purchases this many seconds before departure; nonnegative and shorter than wait. Departure grace still applies. |
| `SellingCutoffSeconds` | `0` | Equivalent cutoff for player sales. |
| `CurrencyId` | `""` | Optional currency override for the whole stop; must exist in catalog. |
| `Prices` | `[]` | Up to 2048 unique exact-class price overrides for classes offered by the group. |
| `StockLimits` | `{}` | Exact-class capacity overrides; only valid with route `StockMode: "stop"`. Up to 2048 entries, each capacity -1–1000000000. |
| `AllowedCategories` | `[]` | Empty permits all profile categories. Otherwise only listed category IDs are available. Each must be offered by this group. Use exact category IDs. |
| `NextStopIndexes` | `[]` | Optional next-stop links, using zero-based indexes into `Stops`. No self-link; every index must exist. |
| `NextStopWeights` | `[]` | Optional selection weights paired with links. Same length as links; each weight 1–1000000. |
| `SpawnClearanceRadius` | `1.5` | Radius around each trader spawn position; 1–50 metres. |
| `ValidateTerrain` | `false` | Requires configured trader height to be within 5 metres of terrain surface. |
| `VehicleSpawnPoints` | `[]` | Optional stop-wide vehicle points, maximum 32. Non-empty array takes priority over individual trader-entry points. |
| `Safezone` | omitted | Optional complete stop-zone override. Omit to inherit the current group's zone; explicitly disable to remove protection at this stop. |

Trader positions and orientations come from the referenced group's trader entries. Vehicle point arrays require three position and three orientation components, each within -100000–100000.

### Buying and selling deadlines

Remaining time must be **greater than** the larger of the route's departure grace and that trade direction's cutoff. At equality, that direction is closed.

For a 900-second stop, grace 15, purchase cutoff 120, and selling cutoff 30:

- Purchases work during the first 780 seconds, then close.
- Sales remain available until 30 seconds remain.
- The route's final 15 seconds are closed to both directions.

This gives players time to finish selling after purchases stop. It does not bypass world-time opening hours, offer pools, missing stock, price validation, or recovery locks. A quote or open basket is not a reservation.

### Local prices and categories

Stop object for the bundled `Mogilevka` group:

```json
{
  "LocationId": "Mogilevka",
  "Name": "Mogilevka Supply Market",
  "WaitSeconds": 1200,
  "TravelSeconds": 240,
  "AllowBuying": true,
  "AllowSelling": true,
  "PurchaseCutoffSeconds": 120,
  "SellingCutoffSeconds": 30,
  "CurrencyId": "euro",
  "AllowedCategories": ["Tools", "Medical"],
  "Prices": [
    { "ClassName": "Hatchet", "BuyPrice": 350, "SellPrice": 90 },
    { "ClassName": "TetracyclineAntibiotics", "BuyPrice": 500, "SellPrice": -1 }
  ]
}
```

Insert this as one stop in a route with at least two stops. The whole referenced group still spawns, but only its `Tools` and `Medical` categories are available. Profiles with no permitted categories do not gain those categories from other profiles.

Price overrides select an exact class, not a listing ID. They affect matching listings at that stop, including multiple variants of that class. Supply both prices deliberately: omitted directions default to `-1`. Zero is invalid for a stop override; use `-1` to disable a direction. A positive sell price cannot exceed a positive buy price. Both `-1` values can close trading for that class at this stop.

The override establishes the base price. Dynamic pricing, sell condition, and quantity deductions still apply. A non-empty price-entry `CurrencyId` must match the effective stop currency; it cannot select an unrelated currency. See [currency precedence](banking-and-currencies.md#currency-selection-and-precedence).

!!! tip "Audit the complete circuit"
    Buying at one stop and selling at another can be an intentional earning route. Compare the cheapest purchase against the highest resale after dynamic pricing, supplied ammunition, attachments, and currency value. Check transport capacity and replenishment rate before deciding how much profit the circuit should generate.

## Stock sharing and arrival deliveries

Stock always belongs to a listing identity. `StockMode` decides which traders share its count:

| Mode | Shared by | Useful for |
| --- | --- | --- |
| `shared` | Every static shop and shared-mode route exposing the same listing ID. | One global supply pool; sales at town can supply the traveling market. |
| `route` | Same route ID and trader profile ID across its stops. | A merchant carrying persistent supply around the circuit. |
| `stop` | Same route ID, trader profile ID, and stop location ID. | Independent regional supplies and destination-specific capacities. |

With `route` or `stop`, two different profiles do not share scoped stock just because both expose the same category. Reusing the same profile at several stops shares its route-mode stock. If you want one merchant's carried supply to stay together, retain the same `TraderId` at those stops.

New scoped records seed from `InitialStock`, capped by their effective capacity. A listing configured as unlimited but given a finite stop capacity starts that scope at the finite capacity. Existing counts survive visits and restarts. Finite capacity reductions clamp excess supply; raising capacity does not automatically fill the extra room.

### Per-stop capacity

Route fragment:

```json
{
  "StockMode": "stop",
  "RestockOnArrival": true,
  "DeliveryDelaySeconds": 60
}
```

Stop fragment for a group offering these classes:

```json
{
  "StockLimits": {
    "Hatchet": 8,
    "TetracyclineAntibiotics": 12
  }
}
```

Classes omitted from `StockLimits` use listing `MaxStock`. A value of `-1` makes that scope unlimited; `0` gives no buying supply or selling capacity. Limits are capacities, not arrival delivery amounts or player quotas.

### Arrival supply

Use this listing inside a referenced category:

```json
{
  "ClassName": "TetracyclineAntibiotics",
  "BuyPrice": 500,
  "SellPrice": 100,
  "InitialStock": 2,
  "MaxStock": 12,
  "RestockAmount": 3,
  "RestockIntervalSeconds": 1800
}
```

With `RestockOnArrival: true`, the merchant adds three units at arrival, or after the configured delivery delay, capped at effective capacity. Arrival does not reset the shelf to twelve. Only valid listings in categories allowed at the current stop, with positive `RestockAmount` and positive effective capacity, receive supply.

The listing must still pass ordinary validation: positive restock amount requires a positive interval, at most 86400 seconds, and finite positive `MaxStock`. The interval controls ordinary shared-stock timers; it is not the arrival countdown.

- `EnableAutomaticRestock` controls uptime-based restocking of shared listing stock.
- Separate `route` and `stop` stock does not receive those ordinary timer increments.
- `RestockOnArrival` operates independently of that global switch.
- A shared-mode route can receive both ordinary timed supply and arrival supply. Count both when balancing it.
- An arrival ID is persisted per trader location to prevent duplicate delivery on restart or repeated processing of the same arrival.
- Multiple profiles exposing the same shared listing can each add arrival supply. Avoid accidental overlap if one delivery per class is intended.

For an arrival-only economy, disable global automatic restock and enable route arrival restock. Static finite shops then need player sales or another deliberate supply source. For a player-supplied caravan, disable both replenishment methods and use `InitialStock: 0` with a positive capacity.

## Sequential, random, and branching travel

Default selection uses the next stop in array order. At the end, `Loop: true` returns to index 0; `Loop: false` finishes the route, removes its traders, and saves a completed paused state.

`RandomStops: true` also randomizes the starting stop. Without explicit links:

- Looping routes choose any other stop; they do not immediately select the current one.
- Non-looping routes choose only a later index and complete at the final stop.
- `RandomStartStop: true` randomizes only fresh starting state when subsequent order should remain sequential.

Explicit links take priority. For stop 0 of a route with three stops:

```json
{
  "NextStopIndexes": [1, 2],
  "NextStopWeights": [3, 1]
}
```

This chooses stop 1 with relative weight 3 and stop 2 with relative weight 1: 75% and 25% per selection. Weights need not sum to 100. Without weights, the first explicit link is selected; multiple links alone do not make selection random. Configure links at other stops too if a complete branching circuit is intended.

Explicit links can create a cycle even with `Loop: false`. To design a route that terminates, ensure its final stop has no links leading back into the circuit. Persisted `NextStopIndex` preserves the chosen destination across restart.

## Schedules and clock selection

Route schedules control whether traders are present. When the schedule closes, the route saves its remaining wait/travel time, removes the active group and zone, and pauses. On reopening it resumes the remaining interval. It does not advance through every missed visit while closed.

| Field | Default | Meaning |
| --- | --- | --- |
| `ScheduleEnabled` | `false` | Enables hour, weekday, month, and recurring month/day filters. |
| `ScheduleStartHour` | `0` | Inclusive opening hour, 0–23. |
| `ScheduleEndHour` | `24` | Exclusive closing hour, 1–24. Must differ from start. |
| `ScheduleWeekdayMask` | `127` | Allowed weekdays, 1–127. |
| `ScheduleMonthMask` | `4095` | Allowed months, 1–4095. |
| `ScheduleUsesServerTime` | `false` | `false`: real UTC. `true`: DayZ world date/time, including its acceleration. It does not mean the host OS timezone. |
| `ScheduleStartMonth`, `ScheduleStartDay` | `0`, `0` | Optional inclusive start of recurring annual date range. |
| `ScheduleEndMonth`, `ScheduleEndDay` | `0`, `0` | Optional inclusive end of recurring annual date range. Supply valid dates at both ends, or leave all four at zero. |
| `ActiveFromDate` | `0` | Optional inclusive absolute date, `YYYYMMDD`. Applies even with `ScheduleEnabled: false`. |
| `ActiveUntilDate` | `0` | Optional inclusive absolute end date, same clock as above. `0` means no bound. |

Enabled filters combine: the current date and hour must satisfy all of them. Ordinary trader-entry opening hours and profile offer pools also remain applicable.

### Weekday and month masks

Add the values of the days or months you want:

| Day | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Value | 1 | 2 | 4 | 8 | 16 | 32 | 64 |

Weekdays are `31`, weekends `96`, every day `127`.

| Month | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Value | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 | 512 | 1024 | 2048 |

Every month is `4095`. October through December is `3584`.

### Weekend evening market

Route fragment, open Saturday and Sunday from 18:00 to 23:59 UTC:

```json
{
  "ScheduleEnabled": true,
  "ScheduleUsesServerTime": false,
  "ScheduleStartHour": 18,
  "ScheduleEndHour": 24,
  "ScheduleWeekdayMask": 96,
  "ScheduleMonthMask": 4095
}
```

An overnight window uses a start greater than its end, for example 20 and 6. The weekday filter checks the current day on both sides of midnight. For Friday-night trade continuing into Saturday, include both Friday and Saturday bits; the mask does not automatically attach Saturday's early hours to Friday.

### Annual winter market

Open December 20 through January 10 inclusive, every day and hour:

```json
{
  "ScheduleEnabled": true,
  "ScheduleUsesServerTime": false,
  "ScheduleStartHour": 0,
  "ScheduleEndHour": 24,
  "ScheduleWeekdayMask": 127,
  "ScheduleMonthMask": 4095,
  "ScheduleStartMonth": 12,
  "ScheduleStartDay": 20,
  "ScheduleEndMonth": 1,
  "ScheduleEndDay": 10
}
```

The annual range can cross New Year. Keep the month mask compatible with both halves. For a one-off event, use absolute bounds such as `ActiveFromDate: 20261220` and `ActiveUntilDate: 20270110` instead; update those dates deliberately for later events.

!!! tip "Know which clock you are testing"
    Route wait, travel, and delivery delays always use real elapsed/calendar seconds. Setting `ScheduleUsesServerTime: true` changes the schedule's calendar, not travel speed. Trader opening hours use world time; offer pool months and rotations use real UTC; ordinary stock timers use server uptime.

## Spawn clearance, protection, and visibility

Every enabled trader position at the current group must pass clearance. The check looks for players/NPCs (`Man`), vehicles (`Transport`), or objects of the trader's exact class within the configured radius. It is not a complete building or geometry collision test. Test walls, furniture, slopes, and vehicle delivery points yourself.

`ValidateTerrain: true` rejects trader positions more than five metres above or below terrain height. Indoor upper floors and raised platforms may deliberately require it to remain false. Correct ground-level coordinates rather than using the switch to hide a bad placement.

Example route fragment for a stop that pauses after prolonged obstruction:

```json
{
  "SpawnRetrySeconds": 10,
  "MaxBlockedSpawnAttempts": 12,
  "BlockedStopTimeoutSeconds": 120,
  "PauseOnBlockedStop": true,
  "AlertAdminsOnBlockedStop": true
}
```

Either configured threshold can trigger the pause. After clearing players and vehicles, inspect diagnostics and resume the route. If no threshold is enabled, or pause-on-blocking is false, retries continue while the stop clock runs; the route can depart before it ever becomes visible.

Route entities are spawned and removed by the route service. Pre-placing the same trader class at the configured point can block arrival instead of being adopted. Keep decorative scenery separate from the route target.

With `Invulnerable: false`, destruction or loss of an active route entity closes the whole visit and removes the route zone. The route waits for its next scheduled transition instead of instantly replacing that trader. Do not assume a vulnerable NPC creates a fully implemented escort mission or reward system.

### Safe zones

An active stop inherits its group's safe zone unless it defines a `Safezone` object. That object replaces the inherited zone; it is not a partial merge with the group. Use a complete deliberate configuration, including centre and radius, when enabling protection. An enabled stop zone requires radius 1–1000 metres and exit protection 0–300 seconds.

On departure, schedule closure, or removal of the visit, the route zone is removed. Permanent protection needs a separate static zone arrangement. Follow the ordinary [safe-zone testing guide](locations-and-safezones.md#border-test-checklist), including border damage, equipment, vehicles, and exit protection.

### Markers and announcements

Map markers show only present traveling traders when `ShowMapMarker` is enabled. They use trader/stop labels and a green marker. The map builds this snapshot on opening; reopen it after movement. No marker traces the journey between stops.

Arrival and departure notifications are individually enabled. `AnnounceInChat` adds chat/status output to those enabled notifications. A positive `AnnouncementRadius` measures distance from the first active trader, not every NPC or the safe-zone boundary. Zero broadcasts to everyone.

## Admin controls

Open **Diagnostics**, select a route entry, and refresh its state before acting. Only IDs in `AdminSteamIds` can operate the controls. Commands are rejected when their route generation is stale, a transaction is active, or recovery is pending.

| Control | Effect |
| --- | --- |
| **Pause route** | Saves remaining time. A present stopped trader can remain available while paused if its opening hours and remaining-time cutoffs allow trade. A paused traveling route remains absent. |
| **Resume route** | Rebuilds the deadline from saved remaining seconds and clears manual/blocked pause. A closed schedule still prevents presence and can pause it again. |
| **Skip stop** | Starts normal travel when stopped. During travel, retains the existing arrival delay. |
| **Depart now** | Ends the current stop and begins travel; requires an open schedule. |
| **Arrive now** | Ends transit and attempts destination arrival; requires an open schedule. Clearance still applies. |
| **Jump to stop** | Creates a fresh arrival at the selected stop with its wait timer. Schedule and clearance still govern actual presence. |

Jumping can trigger stock delivery because it creates a new arrival. Use a test profile when checking repeated arrivals; repeatedly jumping a live market can inject supply. Pause is also not a shop-disable switch: use it to hold a visit or prepare supported edits, with trading rules understood.

Admin actions are recorded in Info logs. A successful state command does not guarantee NPCs are visible; inspect blocked-spawn and schedule status afterward.

## Editing and recovering routes

Persistent state lives here:

```text
$profile:\RaG_Core\Configs\RaG_Trader\RouteState.json
```

It records route configuration, current and selected next stop, wait/travel deadlines, pause reasons, generation, and arrival identity. `Stock.json` separately retains scoped counts and arrival delivery markers. Back up both with the rest of Trader and world/player persistence.

### Live edits

For an affected active route, supported reload requires it to be **paused at a stop**, not traveling. Keep these stable:

- Route array count, IDs/order, and enabled states.
- Stop count and referenced `LocationId` order.
- `StockMode`.
- Stop `Name` values and `StockLimits`.
- All `Locations.json` content and catalog currency definitions/default.

Within those restrictions, candidate validation can accept route prices, permitted categories, cutoffs, schedules, delays, announcements, and other route options. A shorter wait clamps the paused remaining time to the new wait. Reload writes a matching route configuration fingerprint before reinitializing services. Resume deliberately after inspecting the result.

To edit live: pause at a stop, finish active trades/recovery, save complete candidate files, choose **Reload configs**, read the result, refresh diagnostics, then resume. Follow [general reload checks](administration-and-recovery.md#live-configuration-reload) too.

### Restart and configuration mismatch

A restart alone does not reconcile a saved route with arbitrary configuration edits. Saved configuration must match the route definition. A mismatch disables that route and logs the problem rather than silently moving it or resetting its progress.

1. Stop the server and preserve main/backup state plus configuration.
2. Prefer restoring the configuration that matches the saved route when the edit was accidental.
3. For an intentional route reconfiguration, remove only that route's saved entry from the active state while stopped, after preserving a complete backup. Verify main and backup copies are consistent so fallback cannot restore the conflicting entry.
4. Retain other routes, stock identities, accounts, and transaction journals. Do not clear all economy state to fix one route.
5. Restart, inspect the validation report and route logs, and verify its new starting stop and supply. Resetting route state creates a fresh arrival and can permit arrival replenishment against retained stock.

Unreadable route state tries the atomic backup. If usable state cannot be loaded, routes stop with errors; do not delete evidence before investigating. A normal restart retains chosen next destination. If an unpaused deadline expired offline, the service advances from the saved phase; it does not simulate every missed circuit.

Pending transaction recovery defers route processing. Resolve the underlying journal problem through the [recovery guide](administration-and-recovery.md#retry-recovery) before moving the market or resetting stock.

## Practical route designs

| Design | Configuration approach | Test carefully |
| --- | --- | --- |
| Supply caravan | Same profiles across stops; `StockMode: "route"`; small finite supply. | Goods bought at one stop remain absent at the next until replenished. |
| Player-fed market | `InitialStock: 0`, positive capacity, no timed/arrival restock. | Players can reach a sale source before needing to buy. |
| Regional trading circuit | `StockMode: "stop"`, local `Prices` and `StockLimits`. | Round-trip profit, resale capacity, and currency value. |
| Weekend fair | UTC schedule, weekend mask 96, arrival announcements. | Schedule closure pauses progress and removes the zone. |
| Night smuggler | World-time schedule or trader opening hours; no safe zone; optional hidden next stop. | Accelerated world time and route timers use different clocks. |
| Medical relief visit | Medical-only stop, buy-only policy, limited arrival batches, delivery delay. | Empty shelves before supply arrives and purchase cutoff before departure. |
| Branching market | Explicit links with weights. | Every index, reachable stop, and intended termination/cycle. |
| Vulnerable merchant | `Invulnerable: false`, clear no-protection zone policy. | Losing one entity ends the group's visit; scripted quests need an integration. |

Test a full circuit, a restart while stopped, a restart during travel, a blocked spawn, schedule close/reopen, and a purchase near each cutoff before opening the route to players.
