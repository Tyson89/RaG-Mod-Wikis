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

Default RaG Core enables Error logging and disables Debug, Info, and Warning. Enable Info and Warning while configuring; many useful diagnostics such as blocked vehicle spawn, skipped attachment, duplicate item, and registry summary are not errors.

## Fast symptom table

| Symptom | Check |
| --- | --- |
| Server/client reports missing `RaGConfigVersioned`, `RaGConfigAPI`, `RaGAtomicJsonIO`, `RaGIdentityUtility`, `RaG_RPCService`, or notification icons | RaG Core missing, outdated, or mismatched. Install matching RaG Core on server and every client. |
| No configs generate | Check active server profile, write permissions, RaG Core initialization, and `$profile:\RaG_Core\Configs\RaG_Trader\`. |
| Registry never becomes ready | Read Error log from first initialization line onward. With `StrictValidation: true`, one bad reference disables entire trader registry. |
| Missing category error | Catalog references unsafe/missing filename. Custom missing category is not bundled; restore file. |
| Trader not visible | Entry disabled, group disabled, invalid class/transform, registry failed, or spawn failed. |
| Duplicate trader appears | Map object is farther than 1 metre or class differs from `EntityClassName`, so manager spawns another. Align exact class and position. |
| Trader visible but no **Trade** action | Client has not received location bindings, object not bound, client/server mismatch, or target is wrong entity. Reconnect after checking registry/entity logs. |
| Menu opens then purchase says too far | Server uses configured trader position and `InteractionDistance`; stay close and align bound map object with JSON. |
| Trader closed unexpectedly | Opening hours use accelerated DayZ world hour. Closing hour is exclusive. |
| Search item missing | Category not referenced, class invalid and skipped, wrong trader profile, filter active, or listing price invalid. |
| “Catalog changed; refreshing” | Client revision stale, usually reconnect/reload race. Let UI refresh; persistent repeats suggest version mismatch. |
| Buy price shown but checkout fails “Price unavailable” | Price is `0` or wrong currency. Use positive price or `-1` disable; ensure default currency valid. |
| No inventory capacity | Make room, use explicit ground delivery, or enable `AllowGroundFallback`. With fallback enabled, created items/currency land at player position. |
| Item spawns on ground unexpectedly | Inventory delivery failed and global fallback enabled, or listing uses `DeliveryMode: "ground"`. |
| Purchase vanished after attachment config | One listing attachment failed; whole delivered set rolled back. Verify compatibility and slots. |
| Cannot sell bag/gun/clothing | Empty all cargo, including cargo nested under attachments; check ruin, lock, health threshold, exact class, and removability. Remove attachments anyway because sold parent deletes them without extra payout. |
| Sell payout lower than displayed base | Condition and quantity sell pricing enabled. Empty/damaged item pays less. |
| Cannot sell packed vehicle | Carry assigned key containing exact listed class. Seller must be recorded key owner; key must not be ruined, locked under parent, or non-removable. Storage-owner setting/admin bypass does not override sale ownership. |
| Cannot sell parked vehicle | Use exact listed class within 6 metres of configured trader vehicle spawn point; empty crew; engine off; meet minimum health. Assigned car requires key owner. Unassigned car/boat requires last driver who started engine. |
| Out of stock after restart | `Stock.json` persists finite values. Reset deliberately or configure restock. |
| Restock never happens | Both restock fields required, stock must be finite positive, global restock enabled, and server uptime must reach interval. |
| Dynamic price never changes | Listing uses unlimited stock or feature disabled. Only finite stock changes price. |
| ATM has no currencies | Banking disabled, no enabled matching entry, catalog currency is account type, or registry not ready. |
| ATM transaction says too far | `InteractionDistance` too small or ATM geometry/action point awkward. |
| Deposit fails despite visible notes | Notes ruined, contain cargo/attachments, stack quantity floors to zero, fee makes credited amount zero, or max bank balance reached. |
| Withdrawal fails | Bank lacks amount plus rounded-up fee, payout cannot be represented, or inventory is full while `AllowGroundFallback` is disabled. |
| Initial balance not reapplied | Expected. Currency ID already listed in `InitializedCurrencies`. |
| Vehicle purchase fails | No valid spawn points, collision box blocked, class not valid transport, or all points invalid. |
| Purchased vehicle missing parts | No exact valid profile, profile contains unknown class, or attachment incompatible/slot occupied. Check Warning/Error logs. |
| Car key will not assign | Key already assigned, car already keyed, key/car ruined, target not `CarScript`, or identity missing. |
| Lock action missing | Engine running, crew present, car already locked, or key mismatch. |
| Pack action missing | Car ruined, engine running, moving over threshold, occupied, or key mismatch. |
| Pack denied to spare-key holder | Owner restriction uses original assignment owner; possessing spare does not transfer owner. |
| Deploy action missing | Key does not see stored binary, key unassigned, player swimming/in vehicle, or no packed vehicle. |
| Deployment blocked | Hologram collision, over 10 metres, over 4 metres vertical, water surface, or unsuitable geometry. |
| Packed vehicle fails after mod update | Stored recursive class/state no longer loads. Restore prior mod set/version and deploy before migration. |
| Safe zone inactive | Group/zone disabled, center invalid, radius invalid, registry failure, or trigger initialization error. |
| Fall/environment damage still works | Safe-zone player damage hook requires damage source. It is not universal survival immunity. |
| Custom building/explosive still works | Current hooks cover vanilla deploy/build/arm actions. Third-party actions may bypass without integration. |
| Admin still damage-protected | Expected. Admin bypass covers fire/build/explosive/speed and storage ownership, not damage protection. |

## Strict validation

Recommended production value:

```json
{
  "StrictValidation": true
}
```

Registry errors include:

- unsupported versions;
- missing/duplicate/invalid currency IDs and `CurrencyItems`;
- missing value-1 denomination;
- invalid classes;
- invalid stock/restock/health/delivery fields;
- both prices disabled;
- missing categories;
- invalid trader/category references;
- invalid transforms or vehicle spawn points;
- duplicate group/trader runtime IDs;
- invalid safe-zone center.

With strict false, registry may become ready while invalid entries are skipped. This can create partial, confusing shop. Use only during migration, never as permanent way to ignore bad config.

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
[RaG_Trader] Unknown listing class: <class>
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
7. Restart with strict validation and inspect logs.

For category files, bundled recovery works only for stock filenames shipped by mod. Custom categories need own backup.

## Stock recovery

Stock uses atomic main and backup.

- If main invalid and backup valid, service restores backup.
- Unknown listing IDs drop.
- missing listing seeds from category `Stock`.
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

- strict registry ready with zero errors;
- no unexpected duplicate warnings;
- every trader binds once;
- every opening-hour edge tested;
- representative buy/sell from every category;
- empty, damaged, ruined, locked, and nested sale tested;
- finite stock persists and restores;
- restock fires during real uptime;
- dynamic price range cannot create arbitrage;
- basket failure rolls back;
- every denomination pays and changes exactly;
- ATM deposit/withdraw/full-inventory rollback tested;
- every vehicle class spawns at every location;
- key assign/lock/spare/pack/restart/deploy tested;
- safe-zone borders, exits, admins, vehicles, exclusions tested;
- logs retained and backed up.
