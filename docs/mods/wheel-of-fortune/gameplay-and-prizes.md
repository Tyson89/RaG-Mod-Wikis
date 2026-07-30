# Gameplay, prizes, and daily limits

## Spinning wheel

Player must be within normal base-building interaction range and target intact `RaG_Wheel_Of_Fortune` with its internal wheel attached. No item in hands is required, and action works from all stance masks.

Action is unavailable while wheel is spinning or during five-second result cooldown. Server then:

1. checks player Steam64 ID against shared daily list;
2. records ID immediately;
3. chooses random spin duration;
4. animates wheel and plays looping spin sound;
5. detects field under arrow when timer ends;
6. creates configured prize on ground;
7. plays normal or jackpot effects;
8. resets wheel five seconds after successful prize creation.

Only one player can use same wheel while its spin or result state is active.

## Daily limit

Limit is hard-coded to one recorded spin per Steam64 ID. It is global to mod instance:

- using another placed wheel does not grant another spin;
- reconnecting does not grant another spin;
- server restart does not clear same-day list;
- changing character does not bypass Steam64 ID check.

Second attempt produces five-second notification:

```text
You have already spun the wheel today.
```

### Midnight limitation

Current code checks calendar date only when `RaG_SpinManager` is constructed. It has no midnight timer and does not call date check for each spin.

If server stays online across midnight, previous-day IDs remain blocked. Restart server after new server-local date begins to initialize manager again and clear old list. Reset date comes from server `GetYearMonthDay`, not player clock or game-world time.

## When spin is consumed

ID is written to `WheelData.json` before animation starts. No rollback exists.

Player loses daily attempt when later processing fails because:

- configured field is empty;
- configured class does not exist;
- created object cannot cast to `ItemBase`;
- prize creation otherwise fails;
- player disconnects during spin.

There is no fallback prize and no automatic retry. Validate every result before opening wheel to players.

## Result fields

Wheel has 16 detected fields:

| Field | Reward source | Default |
| ---: | --- | --- |
| `1` | Random entry from `ItemFieldJackpot` | `NailBox`, `SledgeHammer`, `Hacksaw`, or `Whetstone` |
| `2` | `ItemField2` | `GorkaHelmet` |
| `3` | `ItemField3` | `Canteen` |
| `4` | `ItemField4` | `DuffelBagSmall_Green` |
| `5` | `ItemField5` | `BandageDressing` |
| `6` | `ItemField6` | `TetracyclineAntibiotics` |
| `7` | `ItemField7` | `HuntingOptic` |
| `8` | `ItemField8` | `MedievalBoots` |
| `9` | `ItemField9` | `BDUJacket` |
| `10` | `ItemField10` | `Hammer` |
| `11` | `ItemField11` | `Wrench` |
| `12` | `ItemField12` | `SledgeHammer` |
| `13` | `ItemField13` | `Hatchet` |
| `14` | `ItemField14` | `Screwdriver` |
| `15` | `ItemField15` | `LugWrench` |
| `16` | `ItemField16` | `NailBox` |

Normal fields accept one class each. Assign same class to multiple fields to place that reward on multiple wheel segments. Source does not expose direct probability values and does not guarantee published percentage for any physical field.

Jackpot field makes separate random selection from `ItemFieldJackpot`. Duplicate entries weight jackpot pool. This weighting applies only after wheel lands on field `1`.

## Prize behavior

Prize is created with `ECE_PLACE_ON_SURFACE` at wheel's `spawn_pos` memory point, then placed on surface. It is loose world item:

- not inserted into player inventory;
- not reserved for winner;
- not protected from another player;
- not granted through Central Economy.

Every configured reward must be valid loaded class inheriting `ItemBase`. Classes supplied by another mod make that mod operational dependency for configured server and clients where assets are required.

## Normal and jackpot effects

Normal fields:

- stop spin sound;
- play end sound;
- start RaG Core confetti particle;
- hold result state for five seconds.

Jackpot:

- stop spin sound;
- play jackpot sound;
- play red fireworks explosion particle at prize position;
- optionally broadcast ten-second notification naming player and prize;
- hold result state for five seconds.

Effects are cosmetic. Current wheel code adds no blast or player damage.
