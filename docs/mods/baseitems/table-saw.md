# Table Saw

The Table Saw consumes one wooden log and produces individual wooden planks.

## Variants

- `rag_baseitems_table_saw_kit` deploys the powered version.
- `rag_baseitems_table_saw_static_kit` deploys the non-electric static version.

The powered version needs an electrical connection. The static version bypasses the power requirement. Both require a non-ruined Saw Blade.

## Operation

1. Deploy the Table Saw.
2. Attach `rag_baseitems_sawblade`.
3. Connect power if using the powered version.
4. Attach a wooden log.
5. Use the buttons to turn the saw on.

Cutting takes 10 seconds. The log is deleted, the Saw Blade loses 5 health, and the planks spawn beside the saw. If the saw is already idling, attaching another log starts the next cut automatically.

## Plank count: important implementation detail

The code currently calls:

```c
Math.RandomInt(4, TableSawMaxGainedWoodenPlanks())
```

DayZ treats the upper bound as exclusive. Therefore a configured value of `10` produces **4 to 9 planks**, not 4 to 10. Set `TableSawMaxGainedWoodenPlanks` above `4`; a value of `4` leaves no valid random range.

See [Server Configuration](json-file-explanation.md).

## Key classnames

```text
rag_baseitems_table_saw_kit
rag_baseitems_table_saw_static_kit
rag_baseitems_sawblade
```
