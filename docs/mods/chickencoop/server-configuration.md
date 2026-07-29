# Server configuration

RaG ChickenCoop stores its versioned configuration at:

```text
$profile:\RaG_Core\Configs\RaG_ChickenCoop\RaG_ChickenCoop.json
```

Stop the server before editing. Keep valid JSON, retain `Version`, and restart after every change.

## Default version 1 configuration

```json
{
  "Version": 1,
  "ChanceToGetItems": 40,
  "ChanceToGetFeathers": 50,
  "ChanceToSpawnCrazyChicken": 10,
  "FeatherQuantity": 2.0,
  "ChickenCoopItems": [
    "rag_egg",
    "rag_gingerbread",
    "rag_chocolate_bunny"
  ],
  "ChickenFeathers": [
    "ChickenFeather"
  ]
}
```

## Settings

| Setting | Default | Actual effect |
| --- | ---: | --- |
| `ChanceToGetItems` | `40` | Maximum successful reward roll. Current code rolls `0-99` and succeeds on `roll <= value`, making the default chance 41%. |
| `ChanceToGetFeathers` | `50` | Split point after a successful reward roll. Despite its name, `roll < value` selects `ChickenCoopItems`; the other results select `ChickenFeathers`. Higher values produce **fewer feathers**. |
| `ChanceToSpawnCrazyChicken` | `10` | Maximum successful independent chicken roll. Current code rolls `0-99` and succeeds on `roll <= value`, making the default chance 11%. |
| `FeatherQuantity` | `2.0` | Quantity assigned to a created entry from `ChickenFeathers` when that class supports quantity. |
| `ChickenCoopItems` | Three RaG food classes | Candidate classes for the normal-item branch. One random entry is selected. |
| `ChickenFeathers` | `ChickenFeather` | Candidate classes for the feather branch. One random entry is selected. The array can technically contain any spawnable item class. |

!!! danger "`ChanceToGetFeathers` is backwards"
    Higher `ChanceToGetFeathers` values increase the normal-item branch and reduce the feather branch. `0` means every successful reward uses `ChickenFeathers`; `100` means every successful reward uses `ChickenCoopItems`.

## Exact chance behavior

The current scripts use:

```text
Math.RandomInt(0, 100)
```

DayZ returns an integer from `0` through `99`; the upper bound is excluded.

For `ChanceToGetItems` and `ChanceToSpawnCrazyChicken`, success uses:

```text
roll <= setting
```

For recommended values from `0` through `99`, probability is:

```text
(setting + 1) / 100
```

| Setting | Actual chance |
| ---: | ---: |
| `0` | 1% |
| `10` | 11% |
| `40` | 41% |
| `50` | 51% |
| `99` | 100% |
| `100` | 100% |

There is no clean zero-percent value inside the intended non-negative range because the code uses `<=`. Remove or replace the coop objects, or unload the mod, if searches must be unavailable. Negative values are not validated, but relying on them is brittle.

`ChanceToGetFeathers` uses a different comparison:

```text
roll < ChanceToGetFeathers
```

For values from `0` through `100`:

```text
normal-item share of successful rewards = setting / 100
feather share of successful rewards = (100 - setting) / 100
```

The crazy-chicken roll occurs even when the reward roll fails. It is not part of the reward split.

Current schema does not validate or clamp any chance or quantity field. Keep `FeatherQuantity` within the supported quantity range of every class placed in `ChickenFeathers`.

## Default probability tree

Default reward success is 41%. Default branch split is 50/50:

```text
normal configured item = 41% × 50% = 20.5%
configured feather item = 41% × 50% = 20.5%
no item or feather      = 59%
```

Default crazy-chicken chance is independently 11%. Changing reward settings never changes that roll.

## Arrays and weighting

One random entry is selected from the chosen array. Duplicate class names act as weights.

Example:

```json
"ChickenCoopItems": [
  "rag_egg",
  "rag_egg",
  "Apple"
]
```

On the normal-item branch, `rag_egg` occupies two of three selection slots.

Keep both arrays non-empty. The scripts do not validate an empty array, a bad class name, or failed object creation before trying to place the result on the surface. Bad values can produce no reward and script errors.

Every custom class must exist on both server and clients. Adding a class from another mod makes that mod an operational dependency for the configured server.

## Legacy configuration warning

Old Workshop text describes a `0-10` scale and the field `GetFeatherQuantity`. That is stale.

Current source uses:

- `40`, `50`, and `10` as defaults against `0-99` rolls;
- `FeatherQuantity`, not `GetFeatherQuantity`;
- version `1` under RaG Core's configuration directory.

Do not paste an old example over the generated file. Let the current build generate its schema, then merge only wanted values.
