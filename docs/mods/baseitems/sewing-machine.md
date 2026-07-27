# Sewing Machine

The Sewing Machine repairs one item compatible with DayZ cloth-repair rules. This covers items normally repaired by a Sewing Kit or Leather Sewing Kit, including compatible third-party clothing.

## Requirements

- Deployed Sewing Machine
- Non-ruined sewing needle
- Non-ruined sewing thread
- One compatible item, either in cargo or in one clothing attachment slot
- Machine open

The machine does not require electrical power.

## Operation

1. Open the Sewing Machine.
2. Attach thread and a needle.
3. Add one compatible item.
4. Aim at the machine and select **Repair**.
5. Wait for the 41-second cycle.

For each repaired item, the cycle:

- sets the item to `SewingMachineRepairedHealth`;
- removes 15 thread quantity;
- removes 5 needle health; and
- removes 10 Sewing Machine health.

Oil a non-pristine, non-ruined machine with `rag_baseitems_oil_bottle`. The oil action consumes 50 quantity and restores the machine to pristine.

The Sewing Case stores needles, thread, cushions, and oil bottles.

## Key classnames

```text
rag_baseitems_sewing_machine_kit
rag_baseitems_sewing_needle
rag_baseitems_sewing_thread
rag_baseitems_oil_bottle
rag_baseitems_sewing_case
```

[Watch the Sewing Machine showcase](https://www.youtube.com/watch?v=RXspC1oLqr8)
