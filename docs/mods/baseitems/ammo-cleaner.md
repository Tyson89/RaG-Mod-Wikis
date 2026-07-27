# Ammo Cleaner

The Ammo Cleaner repairs one repairable ammunition stack at a time.

## Requirements

- Ammo Cleaner crafted at the [Workbench](workbench.md)
- Electrical power
- Disinfectant Alcohol with at least 20 quantity
- One repairable item derived from `Ammunition_Base` in cargo

## Operation

1. Place the Ammo Cleaner.
2. Connect it to power.
3. Attach Disinfectant Alcohol.
4. Put one compatible ammunition stack in cargo.
5. Start **Clean ammo** and wait for the 20-second cycle.

A completed cycle consumes 20 Disinfectant Alcohol and sets the ammunition to `AmmoCleanerRepairedHealth` from [Server Configuration](json-file-explanation.md). Attachments and cargo are locked while it runs.

The cleaner accepts ammunition, not weapon magazines. Use the [Magazine Pump](other-interactive-items.md#magazine-pump) to load or unload magazines.

## Key classname

```text
rag_baseitems_ammo_cleaner
```
