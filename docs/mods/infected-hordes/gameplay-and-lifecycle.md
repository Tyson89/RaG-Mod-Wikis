# Horde lifecycle and performance

## Spawn-attempt sequence

When `ActiveHordeMax` is greater than `0`, server starts a repeating timer. First attempt runs after `SpawnTime` minutes, then repeats at that interval.

Each attempt stops at first failed check:

1. Tracked horde count must be below `ActiveHordeMax`.
2. When `SpawnOnlyNearPlayers` is enabled, online player count must meet `MinimumPlayersOnline`.
3. Proximity mode must find at least one living eligible player outside protected areas.
4. Random `1-100` roll must be at or below `SpawnChancePercent`.
5. Remaining global capacity must be at least `MinInfectedCount`.
6. At least one enabled, unoccupied, eligible spawn location must exist.
7. Horde target is rolled inclusively between `MinInfectedCount` and lower of `MaxInfectedCount` or remaining capacity.

Eligible locations are selected uniformly. List order does not change selection chance.

## Player proximity and visibility

With `SpawnOnlyNearPlayers` enabled, initial location selection requires an eligible living player within `PlayerActivationRadius` of location center. Player movement after selection does not stop formation or despawn horde.

Players do not activate proximity-based hordes while inside:

- TraderPlus safe zones;
- Trader safe zones;
- DayZ Expansion Market safe zones;
- a Basic Territories area where that player is a territory member.

`MinimumPlayersOnline` still counts all connected players. Protected-area filtering is a separate check. When every living player is protected, no proximity-based horde can start. These integrations activate only when corresponding mod is present.

Each individual infected spawn candidate must also pass two safeguards:

- It cannot be closer than `MinimumPlayerSpawnDistance` to any living player.
- Within 200 meters, it is rejected when player has unobstructed line of sight to candidate.

These individual safeguards remain active even when `SpawnOnlyNearPlayers` is disabled. Candidate also needs valid navmesh, no blocking collision, and at least 2.5 meters separation from living members of same horde.

## Event overlap protection

Location circles use center point plus `m_SpawnAreaSize` radius.

- Horde location is skipped when its circle overlaps any registered permanent or dynamic vanilla contaminated area.
- When a dynamic contaminated area tries to appear over active horde, event is cancelled using fixed 120-meter contaminated-area radius.
- With RaG Dragons present, horde location is skipped when its circle overlaps active dragon location.

Overlap checks apply before location selection and do not change JSON. If all enabled locations overlap another event, spawn attempt ends without horde.

## Formation and FPS protection

Hordes form at one infected per 250 milliseconds. Work rotates across active hordes. Every infected receives independently selected class and loot from location loadout.

When measured dedicated-server FPS falls below `PauseSpawningBelowFPS`, formation pauses. It resumes only at or above `ResumeSpawningAboveFPS`. Separate pause and resume thresholds prevent rapid toggling near one value.

FPS gating affects infected creation. Despawn deletion and excess-corpse cleanup run before FPS check and continue in batches of three.

## Population limits

`ActiveHordeMax` caps tracked horde objects. `HordeActiveInfectedMax` caps their reserved target population, including infected not created yet. Effective capacity is therefore lower of both limits.

Default values permit five tracked hordes in theory, but 500 global slots and minimum size 100 cap effective simultaneous capacity at five. A larger randomly selected horde consumes more slots and can reduce actual count.

## Lifetime and cleanup

`DespawnTime` is measured in minutes. Countdown starts only after all target infected have spawned.

- Positive value: horde begins despawn after countdown expires.
- `0`: no timed expiry; horde begins despawn once all its infected are dead.
- Ten consecutive spawn failures: incomplete horde begins despawn immediately.

On despawn, tracked entities are processed three at a time. Living infected are always deleted. `DeleteOnlyAlive` controls whether corpses are also deleted. While horde remains active, tracked corpses above 25 are always deleted in batches.

`ReleaseHordeLocations` should normally remain enabled. Disabling it keeps used locations occupied until server restart, so each location can be selected only once per session.

## Notifications

First successfully created infected triggers global **INFECTED HORDE** spawn notification when `SendSpawnMessage` is enabled. Despawn notification uses same title. `SendSpawnLocation` adds location name to both messages.
