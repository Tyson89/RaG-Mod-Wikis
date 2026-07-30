# Well behavior and cholera

## Water availability

Every server-side object derived from DayZ's `Well` class schedules initialization after `500` milliseconds. Ordinary wells then make one inclusive random roll from `0` through `100`.

```text
usable when roll <= WellWaterChance
```

Default `WellWaterChance: 50` therefore accepts `0` through `50`: `51/101`, or about **50.5%**.

Water state:

- is synchronized from server to clients;
- remains fixed for that object instance;
- is not consumed by drinking, filling, or washing;
- has no recovery timer;
- is not saved by Immersive Wells persistence code.

Static map wells normally initialize and reroll after every server restart. An object deleted and recreated during runtime also rolls again. Changing JSON does not reroll already initialized wells; restart server.

`IsWellException()` bypasses randomization. Current optional RaG Baseitems integration returns `true` for `Land_rag_well`, making that class always usable.

## Working and broken interactions

Mod changes three vanilla action classes:

| Interaction | Working well | Broken well |
| --- | --- | --- |
| Drink directly | Supplies vanilla clean water; optional cholera roll after a completed animation loop. | Action is stopped. |
| Fill a container | Supplies vanilla clean water; optional cholera roll targets container after a completed animation loop. | Action is stopped. |
| Wash bloody hands | Uses vanilla hand-washing result; no cholera roll. | Action is stopped. |

When broken interaction reaches server start, player receives:

```text
This Well seems to be broken. I have to find another one...
```

Clients also hear one non-looping empty-pump sound. Current action conditions can briefly expose normal action prompt because vanilla checks still recognize object as well before mod stops continuation.

Pond, sea, snow, trough, and other non-`Well` water sources keep vanilla behavior. Current container-fill hook checks for successful `Well` cast before applying broken-well logic.

## Pump animation, sound, and particle

Working animated well starts synchronized playing state during drinking, filling, or washing. Clients then:

- animate `Arm` source;
- loop `rag_pump_SoundSet`;
- create RaG Core `EFF_RAG_WELLWATER` particle at configured water position.

When action loop or action ends, state stops, handle resets, sound stops, and particle is removed.

Current source adds `Arm` animation source with a two-second period to:

- `Land_Misc_Well_Pump_Blue`;
- `Land_Misc_Well_Pump_Yellow`.

Particle positions differ for those two vanilla pumps. Other `Well` subclasses use fallback model position `0 1 0` unless their script overrides `GetWaterPosition()`.

One synchronized boolean controls each well, not a count of active users. If multiple players use same well at once, one player's action ending can stop effect while another action remains active.

## Cholera transfer

Cholera code runs only when:

```json
"EnableWellCanTransferCholera": 1
```

After completed direct-drink animation loop, successful roll inserts one `eAgents.CHOLERA` agent into player. After completed fill animation loop, it inserts agent into container in hands. Mod does not replace clean-water liquid type; agent contamination travels with water container.

Hand washing never runs cholera transfer code.

### Exact cholera probability

Cholera uses:

```text
Math.RandomInt(0, 100)
```

Upper bound is excluded, so results are `0` through `99`. Success check uses `<=`.

| `WellCholeraChance` | Actual successful roll |
| ---: | ---: |
| `0` | 1% |
| `10` | 11% |
| `50` | 51% |
| `99` | 100% |
| `100` | 100% |

For values `0` through `99`:

```text
actual chance = (WellCholeraChance + 1) / 100
```

No clean zero-percent value exists inside documented non-negative range while feature is enabled. Set `EnableWellCanTransferCholera` to `0` when wells must be safe.

Roll inserts disease agent exposure. Resulting illness still follows active DayZ disease and immunity systems.
