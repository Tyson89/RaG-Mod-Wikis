# Troubleshooting and recovery

## Log locations

General RaG Trader channels follow RaG Core log layout:

```text
$profile:\RaG_Core\Logs\RaG_TraderLogger\Debug\
$profile:\RaG_Core\Logs\RaG_TraderLogger\Info\
$profile:\RaG_Core\Logs\RaG_TraderLogger\Warning\
$profile:\RaG_Core\Logs\RaG_TraderLogger\Error\
```

Successful trade audit:

```text
$profile:\RaG_Core\Logs\RaG_TraderLogger\Trades_TRADE_YYYY-MM-DD.log
```

Default RaG Core enables Error logging and disables Debug, Info, and Warning. Enable Info and Warning while configuring; many useful diagnostics such as blocked vehicle spawn, disabled listing, duplicate item, and registry summary are not errors.

## Fast symptom table

| Symptom | Check |
| --- | --- |
| Server/client reports missing `RaGConfigVersioned`, `RaGConfigAPI`, `RaGAtomicJsonIO`, `RaGIdentityUtility`, `RaG_RPCService`, or notification icons | RaG Core missing, outdated, or mismatched. Install matching RaG Core on server and every client. |
| No configs generate | Check active server profile, write permissions, RaG Core initialization, and `$profile:\RaG_Core\Configs\RaG_Trader\`. |
| Registry never becomes ready | Read Error log from first initialization line onward. One blocking validation error prevents registry startup; read `ConfigValidationReport.txt` and logs. |
| Missing category error | Catalog references unsafe/missing filename. Custom missing category is not bundled; restore file. |
| Trader not visible | Entry/group disabled, invalid class/transform, registry failed, or spawn failed. For a route, check current stop, travel, schedule, blocked spawn, and saved-state errors. |
| Duplicate trader appears | Map object is farther than 1 metre or class differs from `EntityClassName`, so manager spawns another. Align exact class and position. |
| Trader visible but no **Trade** action | Client has not received location bindings, object not bound, client/server mismatch, or target is wrong entity. Reconnect after checking registry/entity logs. |
| Menu opens then purchase says too far | Server uses configured trader position and `InteractionDistance`; stay close and align bound map object with JSON. |
| Trader closed unexpectedly | Opening hours use accelerated DayZ world hour. Closing hour is exclusive. Route schedules, departure grace, and separate purchase/sale cutoffs can close trade too. |
| Search item missing | Category not referenced, wrong profile, active filter, or inactive/out-of-season pool. Use Search all categories or clear filters. Invalid listings can remain visible with a Config error label. |
| Config error on one item | Read its disabled-listing reason in admin Diagnostics or `ConfigValidationReport.txt`. Check class, prices, liquid compatibility, required items, attachments, and ammo resale values. Other valid listings can remain usable. |
| Ammo purchase gives fewer objects than expected | Loose-ammo quantity counts rounds, delivered across normal stack capacity. It does not count full stacks. |
| Cannot sell the last tiny fragment | Quantity-scaled sale lines round down without a minimum floor. Combine enough eligible contents in the same line for a positive payout. |
| Liquid sale rejected | Check exact container class, positive contents, and exact `RequiredLiquidType`. A visually identical container may hold another liquid. |
| Ammo box disabled despite valid class | Check the ammo resale-profit warning. Box contents can exceed the purchase price when sold as loose rounds. |
| Sale review expired/changed | Reopen review; items, health, ammo, energy, quantities, liquid type, prices, or catalog revision no longer match, or 60 seconds elapsed. |
| Review misses a held item, worn gear, key, or currency | Expected exclusions. Review accepts eligible cargo objects, not every inventory object. |
| Reload rejected | Check candidate validation, pending recovery, active transactions, and restart-only location/currency changes. |
| Trading suspended after interruption | Preserve `Transactions` and related persistence; bring affected players online and follow [journal recovery](administration-and-recovery.md#transaction-journals). |
| “Catalog changed; refreshing” | Client revision stale, usually reconnect/reload race. Let UI refresh; persistent repeats suggest version mismatch. |
| Buy price shown but checkout fails “Price unavailable” | Request a fresh quote. Check positive price, effective location/category/stop currency, current stock, disabled-listing reason, and whether a sale total rounds to zero. Zero configured price disables that direction; use `-1` deliberately. |
| No inventory capacity | Make room, use explicit ground delivery, or enable `AllowGroundFallback`. With fallback enabled, created items/currency land at player position. |
| Item spawns on ground unexpectedly | Inventory delivery failed and global fallback enabled, or listing uses `DeliveryMode: "ground"`. |
| Purchase vanished after attachment config | One listing attachment failed; whole delivered set rolled back. Verify compatibility and slots. |
| Cannot sell bag/gun/clothing | Empty all cargo, including cargo nested under attachments; check ruin, lock, health threshold, exact class, and removability. Remove attachments anyway because sold parent deletes them without extra payout. |
| Sell payout lower than displayed base | Condition and quantity sell pricing enabled. Empty/damaged item pays less. |
| Cannot sell packed vehicle | Carry an eligible owner key for the exact class. Saved vehicle health must be non-ruined and meet the listing threshold. Storage-owner setting/admin bypass does not grant sale ownership. |
| Deploy and repack this vehicle before selling it | Stored data lacks sale-health information. Deploy, inspect, and repack to write that health record; do not edit the binary. |
| Cannot sell parked vehicle | Use exact listed class within 6 metres of configured trader vehicle spawn point; empty crew; engine off; meet minimum health. Assigned car requires key owner. Unassigned car/boat requires last driver who started engine. |
| Out of stock after restart | `Stock.json` persists finite values. Reset deliberately or configure restock. |
| Restock never happens | Shared-stock timers need both restock fields, positive `MaxStock`, global restock enabled, and enough uptime. Separate route/stop stock needs arrival supply; check `RestockOnArrival`, delivery delay, allowed categories, and capacity. |
| Empty shop cannot buy player loot | Check positive `SellPrice`, `InitialStock: 0`, positive `MaxStock`, and effective route capacity. `MaxStock: 0` leaves no buyback room. |
| Currency differs from group setting | Individual trader, category, or route stop overrides it. Bundled trader entries explicitly use `euro`; clear those overrides when inheritance is intended. |
| Dynamic price never changes | Listing uses unlimited stock or feature disabled. Only finite stock changes price. |
| ATM has no currencies | Banking disabled, no enabled matching entry, catalog currency is account type, or registry not ready. |
| ATM transaction says too far | `InteractionDistance` too small or ATM geometry/action point awkward. |
| Deposit fails despite visible notes | Notes ruined, contain cargo/attachments, stack quantity floors to zero, fee makes credited amount zero, or max bank balance reached. |
| Withdrawal fails | Bank lacks amount plus rounded-up fee, payout cannot be represented, or inventory is full while `AllowGroundFallback` is disabled. |
| Wallet ignores most notes in a stack | Built-in Euro denominations need `UseQuantity: true`; false counts one object as one note. Currency definitions require restart. |
| Bank has funds but trader says insufficient funds | For enabled banked physical currency, select **Pay: Bank** before purchase and check selected basket currency. **Pay: Cash** checks carried notes. Account currency uses its balance directly. |
| Transfer recipient missing | Recipient must have joined server at least once. Search 2–32 characters of name, refine if 20 matches fill results, and check selected code suffix. |
| Transfer fails despite sender balance | Check selected banked item currency, recipient `MaxBankBalance` headroom, ATM distance, and pending transaction/recovery. Do not resend a transfer marked pending. |
| Player market action missing | Enable `P2P.json`, restart, and place `StaticObj_Misc_AdvertColumn`. Use board within five metres; ordinary trader/ATM does not open market. |
| Player market item cannot be listed | Check ruin, lock, removability, car-key/currency exclusion, attachment/cargo policy, price bounds, per-player/global limits, and mod hook. |
| Purchased market item not in inventory | Buying reserves item. Open **Purchased** at market board and claim with inventory space. Check History before retrying a timed-out purchase. |
| Initial balance not reapplied | Expected. Currency ID already listed in `InitializedCurrencies`. |
| Vehicle purchase fails | No valid spawn points, collision box blocked, class not valid transport, or all points invalid. For keyed cars, also check key creation, inventory room, and `AllowGroundFallback`. |
| Purchased vehicle missing parts | No exact profile, or actual creation failed despite validation. Invalid configured profiles block registry startup/reload. Check report and Warning/Error logs. |
| Car key will not assign | Key already assigned, car already keyed, key/car ruined, target not `CarScript`, or identity missing. |
| Lock action missing | Engine running, crew present, car already locked, or key mismatch. |
| Pack action missing | `EnableVehiclePacking` false, car ruined, engine running, moving over threshold, occupied, or key mismatch. |
| Pack denied to spare-key holder | Owner restriction uses original assignment owner; possessing spare does not transfer owner. |
| Deploy action missing | Key does not see stored binary, key unassigned, player swimming/in vehicle, or no packed vehicle. |
| Deployment blocked | Hologram collision, over 10 metres, over 4 metres vertical, water surface, or unsuitable geometry. |
| Packed vehicle fails after mod update | Stored recursive class/state no longer loads. Restore prior mod set/version and deploy before migration. |
| Safe zone inactive | Group/zone disabled, center invalid, radius invalid, registry failure, or trigger initialization error. |
| Fall/environment damage still works | Safe-zone player damage hook requires damage source. It is not universal survival immunity. |
| Custom building/explosive still works | Current hooks cover vanilla deploy/build/arm actions. Third-party actions may bypass without integration. |
| Admin still damage-protected | Expected. Admin bypass covers fire/build/explosive/speed and storage ownership, not damage protection. |

## Configuration validation

Validation distinguishes a broken listing from broken shared configuration.

**Listing-local faults** disable the affected entry and report a warning. Examples include unknown listing class, invalid prices, both directions disabled, sell price above enabled buy price, invalid stock/restock/health/delivery fields, invalid required-item classes, incompatible listing attachments, invalid liquid requirements, and detected ammo resale profit. The server disables its prices and restocking. The UI can show the listing with **Config error**; it cannot be traded.

**Blocking faults** prevent registry publication or reject a reload candidate. Examples include unsupported main-file versions, invalid currencies or missing value-1 denomination, missing categories, broken trader references, malformed locations/transforms, duplicate runtime IDs, invalid safe-zone configuration, bad offer pools, invalid banking references, and invalid vehicle attachment profiles or survivor loadouts.

Zero `BuyPrice` or `SellPrice` produces a warning and disables that direction. Use `-1` for an intentionally disabled direction. At least one direction must remain positive for a usable listing.

Read `ConfigValidationReport.txt` and admin **Diagnostics**. After a rejected reload, Diagnostics can show active listing state alongside the latest failed validation attempt; the candidate has not replaced active configuration. Fix the named cause, reload or restart as appropriate, and verify the affected item. See [administration and recovery](administration-and-recovery.md).

## Common exact errors

```text
[RaG_Trader] Unsupported Settings.json version: <n>. Expected: 1
```

Keep `Version: 1`. Do not guess future schema.

```text
[RaG_Trader] Missing category config: <name>
```

Catalog references file that is absent both profile and bundle.

```text
Disabled listing <listing-id>: Unknown listing class: <class>
```

Class missing from active server mod set or misspelled.

```text
[RaG_Trader] Duplicate item at trader location...
```

Same class visible through multiple categories. Remove duplicate or set `AllowDuplicate: true` on every intended copy.

```text
[RaG_Trader] Vehicle spawn point blocked. vehicle=<class> blocker=<class>
```

Clear configured 6 × 4 × 10 area or add fallback points.

```text
[RaG_Trader] Currency rollback created recovery vault for player
```

Automatic rollback could not return escrowed item normally. `RaG_TraderTransactionVault` appears at player position. Secure contents and investigate immediately.

## Configuration recovery

Main configs copy from bundled defaults only when missing.

1. Stop server.
2. Back up broken file and related runtime state.
3. Move broken file outside active folder.
4. Start test server with same build to install bundled default.
5. Stop server.
6. Merge custom values into fresh schema.
7. Restart and require zero blocking validation errors.

For category files, bundled recovery works only for category filenames bundled with the development build. Custom categories need own backup.

## Traveling market problems

Start with the `MOVING TRADERS` validation section, then open the route's Diagnostics entry. A valid route needs at least two different enabled location groups. Each group can belong to only one enabled route.

| Symptom | Check |
| --- | --- |
| All stops appear as static markets | Route is disabled or failed validation and never claimed its groups. Read the route warning; visible NPCs alone do not prove route control. |
| Route disabled after configuration edit | Saved configuration no longer matches. Restore matching configuration or follow the [stopped-server route recovery procedure](traveling-traders-and-routes.md#restart-and-configuration-mismatch). |
| Waiting for clear spawn | Move players, NPCs, and vehicles clear of every trader point. Remove pre-placed copies of route target. Check radius and actual geometry at each configured position. |
| Route remains blocked after clearing area | Refresh diagnostics. `MaxBlockedSpawnAttempts` may have skipped stop; next normal phase may be underway. Use **Jump to stop** deliberately for another visit if needed. Closed schedule can still prevent spawning. |
| Arrived, but shelves remain empty | Arrival supply disabled, delayed, already applied for this arrival, or listing has no valid restock amount/capacity. Player sales may be the intended supply. |
| Route stopped advancing | Check manual/schedule pause, completed non-looping route, pending recovery, and failed state writes. |
| Market vanishes when one NPC dies | Vulnerable routes close the whole visit after losing an active entity. Use `Invulnerable: true` for protected traders or design around the interruption. |
| Schedule opens at the wrong time | Default clock is UTC. `ScheduleUsesServerTime: true` uses DayZ world date/time. Check weekday/month masks and absolute dates together. |
| Friday overnight market closes at midnight | Include Saturday in the weekday mask for Saturday's early hours. Day filters use the current day. |
| Several next-stop links always choose one destination | Set `RandomStops: true` to choose uniformly among `NextStopIndexes`; otherwise first link wins. |
| Non-looping route keeps cycling | Explicit next-stop links can override normal end-of-array completion. Remove the back-link from the intended final stop. |
| Map marker stays at previous stop | Reopen the map for a fresh snapshot. Only present traveling traders receive markers. |
| Admin command asks for refresh | Route generation changed. Refresh Diagnostics and inspect the current state before retrying. |
| Route reload refused despite pause | Pause must be at a stop, not in transit. Route topology, stock mode, stop names, stock limits, and all location content must remain stable. |

Keep `RouteState.json`, `Stock.json`, their backups, and relevant logs together when investigating. Clearing state can create fresh arrival deliveries; it is not a harmless way to refresh a marker or move one blocked NPC.

## Stock recovery

Stock uses atomic main and backup.

- If main invalid and backup valid, service restores backup.
- Unknown listing IDs drop.
- missing listing seeds from category `InitialStock`.
- invalid count normalizes to configured cap.

If deliberate reset needed, stop server and move both `Stock.json` and backup. Never delete live file while server runs.

## Account recovery

Account files are per numeric player ID and also use backups.

If account invalid:

1. stop server;
2. preserve main and backup;
3. verify filename and `PlayerId` match;
4. restore newest valid copy;
5. validate balances non-negative and below integer limit;
6. restart and test ATM/trade.

Do not mass-delete accounts to solve one player problem.

## Vehicle-storage recovery

Packed vehicles are binary. Safe actions:

- preserve main and backup;
- restore exact mod dependencies/classes;
- use matching key;
- deploy vehicle;
- remove incompatible cargo/attachments;
- repack under current environment.

Unsafe actions:

- editing binary manually;
- renaming to another key UUID;
- deleting because deployment failed once;
- changing mod set while valuable vehicles remain packed.

## Production validation checklist

- registry, stock, and journal ready with zero blocking errors;
- no unexpected duplicate warnings;
- every trader binds once;
- every opening-hour edge tested;
- representative buy/sell from every category;
- empty, damaged, ruined, locked, and nested sale tested;
- finite stock and listing identity mappings persist and restore;
- loose ammo buys/sells exact rounds and retains unsold partial stacks;
- liquid purchase fill and matching/wrong-liquid sales tested;
- no unintended disabled listings in Diagnostics;
- restock fires during real uptime;
- dynamic price range cannot create arbitrage;
- basket failure rolls back;
- every denomination pays and changes exactly;
- ATM deposit/withdraw/full-inventory rollback tested;
- every vehicle class spawns at every location;
- key assign/lock/spare/pack/restart/deploy tested;
- safe-zone borders, exits, admins, vehicles, exclusions tested;
- logs retained and backed up.
