# Repair Station

The Repair Station repairs exactly one item that DayZ considers compatible with a whetstone.

## Requirements

- Deployed Repair Station
- Non-ruined Grindstone attached
- One non-ruined, whetstone-compatible item in cargo
- Station open

It does not require electrical power.

## Operation

1. Open the Repair Station.
2. Attach `rag_baseitems_grindstone`.
3. Put one compatible item in its cargo.
4. Aim at the handle and select **Repair**.
5. Wait for the 20-second cycle to finish.

Each completed cycle removes 5 health from the Grindstone. The item is set to the condition selected by `RepairStationRepairedHealth` in [Server Configuration](json-file-explanation.md).

Compatibility follows the item's whetstone-repair configuration. A modded item that is not compatible with a vanilla whetstone will not be accepted.

## Key classnames

```text
rag_baseitems_repair_station_kit
rag_baseitems_repair_station
rag_baseitems_grindstone
```
