# Building, features, and dismantling

## Craft the kit

Combine:

- `10` wooden planks;
- `50` nails.

Choose **Craft Hunting Cabin Kit**. The recipe takes its quantities from code, not JSON, and creates `rag_hunting_cabin_kit` on the ground.

`CanCraftHuntingCabinKit` can disable this recipe. It does not prevent admins, traders, the Central Economy, or other scripts from distributing an existing kit class.

## Place the hologram

Put `rag_hunting_cabin_kit` in hands and use normal placement controls. Deployment consumes the kit and creates `rag_hunting_cabin_hologram`.

Current source forces the kit's placement-collision result to false. Normal placement-permission systems, territory mods, or server-side overrides can still impose their own rules.

An empty hologram can be dismantled by hand from its stairs selection. This deletes the hologram and creates a normal kit at the player's position. Remove every attached material first.

## Attach construction materials

Default requirements:

| Material class | Displayed material | Default quantity |
| --- | --- | ---: |
| `Nail` | Nails | `99` |
| `WoodenPlank` | Wooden planks | `100` |
| `WoodenLog` | Wooden logs | `20` |
| `Stone` | Stones | `32` |

Attach all four stacks to the hologram. Build action appears only when every material attachment exists and every stack meets its configured quantity.

!!! warning "Zero still needs an attachment"
    Source first requires all four attachment objects, then compares quantities. Setting one amount to `0` does not remove that attachment requirement.

Use whole-number quantities. JSON fields are floats, but dismantling refunds convert them to integers.

## Finish construction

Stand near the stairs selection with a non-ruined:

- `Hammer`; or
- `Hatchet`.

Hold **Build**. Action uses DayZ's default deconstruction duration. Completion creates `rag_hunting_cabin` at the hologram position and deletes the hologram with all attached materials.

Do not overfill material stacks. Construction does not preserve excess quantities, and dismantling refunds use configured amounts rather than quantities originally attached.

### Tool damage

Default `RuinHammerAfterBuilt: 1` sets the used build tool to ruined condition.

The setting name is misleading: action applies this to `m_MainItem`, so a hatchet is ruined too. With `RuinHammerAfterBuilt: 0`, build instead removes `10` health from either supported tool.

## Admin kit

`rag_hunting_cabin_admin_kit` places a completed cabin immediately:

- no hologram;
- no material attachments;
- no build tool;
- cabin records itself as an admin cabin.

Admin state persists. Dismantling an admin cabin never returns materials. If kit return is enabled, it returns another admin kit.

Keep this class out of normal loot, traders, and player rewards.

## Door and windows

Door:

- opens from its door selection when no supported lock reports locked;
- closes from the same selection;
- updates navigation mesh after its roughly two-second animation;
- closes during persistence restore after restart.

Eight windows open and close independently. Window actions require the player to be within `5.3` meters of the cabin's center, which effectively limits control to the interior. All eight close during persistence restore after restart.

Open/closed door and window states are saved, but restore code deliberately closes every open part. Restart therefore leaves cabin sealed.

## Interior and party lights

Aim at cabin light switch to control:

- built-in interior light;
- attached party lights, when an item occupies `Lights` attachment slot.

Interior light is a warm client-side point light:

- radius `12`;
- brightness `12`;
- shadows enabled;
- hidden during daylight.

Party-light switch code checks only whether `Lights` slot has an attachment. Cabin source does not check battery or energy state.

Neither light state is written by `OnStoreSave`. After restart, both reset off. Attached party-light item itself uses normal persistence rules.

## Locks

### Vanilla combination lock

Cabin exposes `Att_CombinationLock`. A locked combination lock blocks door opening.

Hand saw and hacksaw can destroy it:

- five progress cycles;
- six seconds per cycle;
- each cycle removes one fifth of lock maximum health;
- normal saw-lock tool damage applies each cycle.

Total uninterrupted action time is about `30` seconds. No Hunting Cabin JSON setting disables or changes this action.

### CodeLock Mod

When CodeLock Mod's `CodeLock` compile symbol exists, cabin adds attach, passcode, owner, guest, admin, and raid actions. Server owners get a second JSON file for attachment and raid behavior.

See [Server and CodeLock configuration](server-configuration.md).

### Expansion Code Lock

Current Hunting Cabin repository removed its embedded Expansion compatibility. Separate RaG Expansion Compat source adds Expansion lock/open state handling when both `RAG_HUNTING_CABIN` and `EXPANSIONMODBASEBUILDING` are defined.

Install that compatibility mod after required RaG and Expansion components. Do not expect current Hunting Cabin alone to handle Expansion Code Locks.

## Damage

Cabin has `50000` global health. Config defines these global armor health multipliers:

| Damage category | Health multiplier |
| --- | ---: |
| Projectile | `1` |
| Melee | `0.65` |
| Frag grenade | `20` |

These are damage-system coefficients, not fixed hit damage or guaranteed shot counts.

When DayZ `disableBaseDamage` is enabled through active gameplay configuration, cabin rejects calculated damage after initialization. Hunting Cabin JSON has no separate damage toggle.

Dedicated **Destroy Hunting Cabin** source exists but is explicitly marked unused and is not registered on cabin or tools. Normal damage destruction and interior dismantling are the current removal paths.

## Dismantle completed cabin

Requirements:

1. Stand inside the Hunting Cabin.
2. Aim at door selection.
3. Empty cabin attachments.
4. Hold a non-ruined crowbar, hatchet, or sledgehammer.
5. Complete **Dismantle**.

Dismantling applies normal DayZ dismantle tool damage and deletes cabin.

Default configuration also:

- returns same kit class at cabin kit-spawn point;
- creates `rag_temp_materials_box` containing configured material quantities for normal cabins.

Refund box cannot be placed in hands or cargo and accepts no extra cargo. It deletes itself when its last attachment is removed. Source class description calls it non-persistent, but script only explicitly deletes it when empty; collect refunds immediately.

## Force Synchronize action

Cabin exposes **Force Synchronize** on door while cabin inventory is empty. Action deletes cabin and recreates it with only:

- position;
- orientation;
- global health.

It does not copy door/window/light state or admin-cabin flag. Use only to repair a visually or physically desynchronized door. This action has no admin permission check.
