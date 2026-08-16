# RaG Infected Hordes

RaG Infected Hordes creates configurable infected attacks at named map locations. Server owners control when hordes form, how many infected they contain, which locations can be selected, which infected classes appear, what loot they carry, and when the horde is removed.

[RaG Core](../core/index.md) is a hard dependency. Install and enable both mods on server and clients. Addon dependency declarations control PBO ordering; server `-mod` list order does not.

## Start here

- [Horde lifecycle and performance](gameplay-and-lifecycle.md) explains spawn attempts, player proximity, population limits, formation, FPS protection, corpse cleanup, and despawning.
- [Server configuration](server-configuration.md) documents `RaG_InfectedHorde.json` and every top-level setting.
- [Locations, loadouts, and loot](locations-loadouts-and-loot.md) documents both JSON structures, category matching, weighted infected selection, and loot rolls.
- [Server setup and troubleshooting](server-setup-and-troubleshooting.md) covers installation, first start, safe updates, testing, and failure diagnosis.

## Behavior at a glance

- Automatic spawn attempts run every 25 minutes by default; first attempt is not immediate.
- Each attempt has 50% success chance before location and capacity checks.
- Default horde size is 100-200 infected, with at most five tracked hordes and 500 reserved infected globally.
- By default, at least two players must be online and an eligible player outside supported safe zones and their Basic Territories area must be within 1,000 meters of a free location.
- Infected form gradually, one every 250 milliseconds, and spawning pauses when server FPS falls below 25.
- Spawn points use navmesh and collision checks, stay at least 20 meters from players, and avoid player line of sight within 200 meters.
- Horde locations cannot overlap registered contaminated areas or active RaG Dragons locations.
- Horde lifetime begins only after its full target population forms.
- Location category selects a themed infected and loot loadout.
- Active hordes keep at most 25 tracked corpses; excess corpses are deleted in small batches.

## Files

Both files live below server profile directory:

```text
RaG_Core/Configs/RaG_InfectedHorde/RaG_InfectedHorde.json
RaG_Core/Configs/RaG_InfectedHorde/RaG_InfectedHorde_Loadouts.json
```

## Links

- [RaG Core documentation](../core/index.md)
- [Support RaG Tyson on Ko-fi](https://ko-fi.com/rag_tyson)
