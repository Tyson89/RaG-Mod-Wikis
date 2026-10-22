# Server configuration

RaG Hunting Cabin creates one JSON file:

| File | Created when | Purpose |
| --- | --- | --- |
| `$profile:\RaG_Core\Configs\RaG_Hunting_Cabin\RaG_Hunting_Cabin.json` | Hunting Cabin and RaG Core load correctly | Crafting, build materials, refunds, and roof texture. |

Stop server before editing. Restart after every change.

Vanilla `DigitalCodeLock` behavior is configured globally by RaG Core, not this file. Core adds persistent ownership, remembered access, auto-lock, owner-only controls, admin recovery, optional battery-free operation, and configurable raiding. See [RaG Core: Vanilla DigitalCodeLock](../core/vanilla-digital-codelock.md).

## Main cabin configuration

### Default version 1 configuration

```json
{
  "Version": 1,
  "CanCraftHuntingCabinKit": 1,
  "RuinHammerAfterBuilt": 1,
  "GiveBackMaterialsAfterDismantle": 1,
  "GiveBackKitAfterDismantle": 1,
  "EnableSnowyRoofTexture": 0,
  "NailAmount": 99.0,
  "WoodenPlankAmount": 100.0,
  "WoodenLogAmount": 20.0,
  "StoneAmount": 32.0
}
```

DayZ's JSON serializer represents these script booleans as `1` and `0`.

### Settings

| Setting | Default | Actual effect |
| --- | ---: | --- |
| `Version` | `1` | Current schema version. Values below `1` are upgraded and saved as `1`. |
| `CanCraftHuntingCabinKit` | `1` | Enables built-in `10` planks + `50` nails recipe. Does not block already existing, spawned, traded, or scripted kits. |
| `RuinHammerAfterBuilt` | `1` | Ruins build tool on completion. Despite name, this affects hatchet too. When disabled, action removes `10` tool health. |
| `GiveBackMaterialsAfterDismantle` | `1` | Creates configured materials in refund box when normal cabin is dismantled. Admin cabins never return materials. |
| `GiveBackKitAfterDismantle` | `1` | Returns normal kit for normal cabin and admin kit for admin cabin. |
| `EnableSnowyRoofTexture` | `0` | Applies snowy roof and secondary roof textures when cabin initializes on server. |
| `NailAmount` | `99.0` | Minimum nails on hologram and nail refund quantity. |
| `WoodenPlankAmount` | `100.0` | Minimum wooden planks on hologram and plank refund quantity. |
| `WoodenLogAmount` | `20.0` | Minimum wooden logs on hologram and log refund quantity. |
| `StoneAmount` | `32.0` | Minimum stones on hologram and stone refund quantity. |

### Material behavior and validation

Current schema does not clamp or validate material values.

- Keep values whole and non-negative.
- Every hologram still needs all four attachment types, even when a configured amount is `0`.
- Build deletes complete attached stacks. Excess material is lost.
- Refunds use current config amounts, not material quantities originally attached.
- Refund code converts float settings to integers.
- A refund class is skipped only when its converted amount equals `0`.

Changing material amounts affects existing holograms when build condition is next evaluated. Changing refund amounts affects cabins dismantled after restart/config reload; refunds do not remember original construction cost.

!!! danger "Do not use negative or fractional costs"
    Source accepts them but behavior is bad. Negative minimums make quantity checks trivially pass, while integer conversion can create incorrect or invalid refund quantities.

### Crafting versus construction

Recipe cost is hard-coded:

```text
10 WoodenPlank + 50 Nail
```

Material settings control only hologram build requirement and dismantling refund. They do not alter kit recipe.

## Configuration recovery

If main file is invalid or missing, RaG Core loads default object and may rewrite defaults.

Recovery:

1. Stop server.
2. Back up broken file.
3. Move broken file out of active profile config directory.
4. Start once to generate defaults.
5. Stop server.
6. Merge wanted values carefully.
7. Restart and test.
