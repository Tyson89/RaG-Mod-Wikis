# Troubleshooting and recovery

Start with `$profile:\RaG_Core\Configs\RaG_Trader\ConfigValidationReport.txt`. Check Trader logs under `$profile:\RaG_Core\Logs\RaG_TraderLogger\` and the server RPT for spawn, model, or script errors.

| Symptom | What to check |
| --- | --- |
| Trader does not start | Check RaG Core on server and clients. Confirm `"Version": 1` in the main files, valid JSON, and write access to the profile. Read the first blocking error. |
| Static trader absent | Enable `EnableStaticTraders`, the group, and its trader entry. Check the exact entity class, profile reference, map coordinates, and report's spawn status. |
| Traveling trader absent | Enable `EnableRoutes` and the route. Check schedule, current phase, and spawn clearance in Diagnostics. Move players and vehicles clear of the trader's position. |
| Category missing | Check the filename under `Trading/Categories/` and the profile's `Categories` list. At a route, check the current stop's category filter. |
| Listing greyed out | Check config errors, active offer pool, stock, and whether buying or selling is enabled. |
| Sale rejected | Check the exact class, required liquid, health, remaining quantity, cargo, inventory lock, and stock capacity. Use a fresh review if the items or price changed. |
| Vehicle purchase blocked | Clear the configured spawn points and check vehicle attachments. For boats, check that the point is in water. |
| Vehicle sale rejected | Check exact class, ownership or last driver, engine, occupants, and distance to the dealer's vehicle point. |
| ATM or Transfer absent | Place `RaG_ATM`. Check the banking switches and whether the item currency has an enabled bank entry. |
| Player market unavailable | Enable P2P, check its configured currency, place a permitted board, and test within its interaction radius. |
| Garage vehicle missing from parked list | Check platform bounds and angle, ownership, vehicle support, engine, occupants, towing, and inventory lock. |
| Garage retrieval blocked | Clear the platform and use one that matches the vehicle's land or water requirements. |
| Reload rejected | Check the report, then confirm the edit supports live reload and the server has no pending ordinary transaction recovery. |

## Recovery holds

Stop repeating an operation when it reports a recovery hold. Record the player ID, operation ID or receipt, and approximate time. Preserve related files and inspect what the server already delivered, removed, or credited.

- **Ordinary trade or ATM**. Inspect the transaction journal, stock, player inventory, and account balance. An admin can [retry ordinary recovery](administration-and-recovery.md#retry-recovery).
- **Bank transfer**. Compare both account records with `BankTransfers.json`.
- **Player market**. Keep the listing journal, item payload, and quarantine records with the affected accounts.
- **Vehicle storage**. Keep garage or portable packing files with the world save. Check whether the original vehicle still exists before recovering a snapshot.

See [backup sets](administration-and-recovery.md#backup-sets) for the full paths.
