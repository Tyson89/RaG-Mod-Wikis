# Gameplay and rewards

## Dragon encounters

The server selects an enabled location, then one position inside that location. The dragon initially spawns 500-707 meters horizontally from that position at world height `800`, flies toward it, and settles around 35 meters above the terrain.

The five automatically selected variants are brown, grey, red, yellow, and orange. Their current gameplay logic and health are identical.

### Default aggression

Dragons do not acquire players, animals, or vehicles through normal AI targeting. At their destination they attack the area with fire breath, which can burn exposed players and infected.

Damaging a dragon changes the encounter:

1. The attacking player becomes the dragon's locked target.
2. The dragon pursues that player while the player remains alive.
3. It can launch a counter-fireball immediately after a hit, with a two-second cooldown between counter-fireballs.
4. Fireballs lead the moving target and land within a randomized area around the predicted position.

## Fire damage

### Fire breath

- Effective trigger radius: 25 meters.
- Player burn duration: 4-20 seconds.
- Player damage: a random 2-5 health per second.
- The same per-second damage is also applied to every non-destroyed worn attachment and the item in the player's hands.
- Players detected inside a building or under a roof are protected from fire breath.

### Fireball ground fire

- Effective trigger radius: 13 meters.
- Lifetime: 15 seconds.
- Player burn duration: 4-12 seconds.
- Player and equipment damage: a random 2-5 health per second.
- Roof checks do not protect against the ground-fire trigger.
- A direct fireball collision applies damage across a vehicle's damage zones and its installed attachments.

Burning also triggers the hot, fever-blur, and heavy-pain symptoms. VPP Admin Tools and Community Online Tools god mode are respected when those integrations are compiled.

Infected burn for 8-25 seconds and take a random 5-15 health damage per second.

## Killing and skinning

The current dragon classes have 10,000 global health. A player kill can produce a global defeat notification and a kill/death log entry, depending on server settings.

Skinning an automatically spawned dragon creates:

- `SkinnedItemsAmount` random selections from `SkinningItems`; duplicate selections are possible.
- One dragon head matching the killed dragon's color.

The supplied defaults select three items from:

- `NorseHelm`
- `Chainmail_Coif`
- `Chainmail`
- `WoodAxe`

The normal skinning table has zero meat, feathers, guts, and bones. The configured reward items and matching head are the intended output.

## Dragon head trophy

When `EnableCraftDragonHeadTrophy` is enabled:

1. Combine 10 nails and 4 wooden planks.
2. Craft `RaG_Dragon_Head_Trophy`.
3. Attach the skinned dragon head to the trophy's **Dragon Head** slot.
4. Place the completed trophy.

The recipe creates the empty trophy; the head is attached afterward. The trophy uses DayZ's `disableBaseDamage` invulnerability setting.

## Dragon egg

`RaG_Dragon_Egg` is a spawnable item, but the current scripts do not drop, hatch, or otherwise consume it. Treat it as an admin, trader, or custom-economy prop unless another mod adds behavior.
