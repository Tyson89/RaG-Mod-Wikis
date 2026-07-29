# Server configuration

RaG Halloween stores its versioned configuration at:

```text
RaG_Core/Configs/RaG_Halloween/RaG_Halloween.json
```

Stop the server before editing the file. Keep valid JSON syntax, retain `Version`, and restart after every change.

## Default version 1 configuration

```json
{
  "Version": 1,
  "Tombstone_Enabled": 1,
  "Tombstone_ChanceToSpawnRewards": 50,
  "Tombstone_ChanceToDigGrave": 8,
  "Tombstone_Items": [
    "SlicedPumpkin",
    "Zagorky",
    "ZagorkyChocolate",
    "ZagorkyPeanuts",
    "SaltySticks",
    "Crackers",
    "Chips",
    "Banana"
  ],
  "Tombstone_SpawnableAI": [
    "ZmbM_Mummy",
    "ZmbM_Mummy",
    "ZmbM_Mummy",
    "ZmbM_Mummy"
  ],
  "BoogieMan_Enabled": 1,
  "BoogieMan_MinSpawnableAIAmount": 3,
  "BoogieMan_MaxSpawnableAIAmount": 6,
  "BoogieMan_SpawnableAI": [
    "ZmbM_Mummy",
    "ZmbM_Mummy",
    "ZmbM_Mummy",
    "ZmbM_Mummy"
  ],
  "PumpkinGrenade_ChanceToGetRewards": 50,
  "PumpkinGrenade_MinItemsAmount": 2,
  "PumpkinGrenade_MaxItemsAmount": 5,
  "PumpkinGrenade_Items": [
    "Zagorky",
    "ZagorkyChocolate",
    "ZagorkyPeanuts",
    "SaltySticks",
    "Crackers",
    "Chips",
    "Banana"
  ],
  "PumpkinGrenade_MinSpawnableAIAmount": 1,
  "PumpkinGrenade_MaxSpawnableAIAmount": 3,
  "PumpkinGrenade_SpawnableAI": [
    "Animal_CanisLupus_White",
    "Animal_CanisLupus_White",
    "Animal_CanisLupus_White",
    "Animal_CanisLupus_White"
  ],
  "Pedestal_ChanceToSpawnCoffin": 50,
  "Coffin_MinItemsAmount": 3,
  "Coffin_MaxItemsAmount": 6,
  "Coffin_Items": [
    "Zagorky",
    "ZagorkyChocolate",
    "ZagorkyPeanuts",
    "SaltySticks",
    "Crackers",
    "Chips",
    "Banana"
  ],
  "Pedestal_MinSpawnableAIAmount": 1,
  "Pedestal_MaxSpawnableAIAmount": 4,
  "Pedestal_SpawnableAI": [
    "Animal_UrsusArctos",
    "Animal_UrsusArctos",
    "Animal_UrsusArctos",
    "Animal_UrsusArctos"
  ]
}
```

## Settings

### Graves

| Setting | Default | Effect |
| --- | ---: | --- |
| `Tombstone_Enabled` | `1` | Enables the initialization roll and search helper on supported graves. Use `0` or `1`. |
| `Tombstone_ChanceToSpawnRewards` | `50` | Maximum inclusive `0-100` roll that produces one reward. A higher value makes rewards more likely. |
| `Tombstone_ChanceToDigGrave` | `8` | Maximum inclusive `0-100` roll that makes a supported grave searchable when it initializes. |
| `Tombstone_Items` | Eight food classes | Candidate reward classes. One random entry is created after a successful reward outcome. |
| `Tombstone_SpawnableAI` | Four `ZmbM_Mummy` entries | Candidate classes for the non-reward outcome. One random entry is created. |

### Boogieman

| Setting | Default | Effect |
| --- | ---: | --- |
| `BoogieMan_Enabled` | `1` | Enables a one-use 5-meter player trigger on supported boogieman props. Use `0` or `1`. |
| `BoogieMan_MinSpawnableAIAmount` | `3` | Minimum number of AI created by the ambush. |
| `BoogieMan_MaxSpawnableAIAmount` | `6` | Maximum number of AI created by the ambush. |
| `BoogieMan_SpawnableAI` | Four `ZmbM_Mummy` entries | Candidate classes selected independently for each spawn. |

### Pumpkin grenade

| Setting | Default | Effect |
| --- | ---: | --- |
| `PumpkinGrenade_ChanceToGetRewards` | `50` | Maximum inclusive `0-100` roll that selects the reward outcome. A higher value makes rewards more likely. |
| `PumpkinGrenade_MinItemsAmount` | `2` | Minimum reward-item count. |
| `PumpkinGrenade_MaxItemsAmount` | `5` | Maximum reward-item count. |
| `PumpkinGrenade_Items` | Seven food classes | Candidate reward classes selected independently for each item. |
| `PumpkinGrenade_MinSpawnableAIAmount` | `1` | Minimum AI count for the non-reward outcome. |
| `PumpkinGrenade_MaxSpawnableAIAmount` | `3` | Maximum AI count for the non-reward outcome. |
| `PumpkinGrenade_SpawnableAI` | Four white-wolf entries | Candidate classes selected independently for each AI spawn. |

There is no pumpkin-grenade enable setting. Control availability through the Central Economy, traders, and other distribution systems.

### Spooky pedestal and coffin

| Setting | Default | Effect |
| --- | ---: | --- |
| `Pedestal_ChanceToSpawnCoffin` | `50` | Minimum inclusive `0-100` roll that selects the coffin. A higher value makes coffins **less** likely. |
| `Coffin_MinItemsAmount` | `3` | Minimum number of items created in a reward coffin. |
| `Coffin_MaxItemsAmount` | `6` | Maximum number of items created in a reward coffin. |
| `Coffin_Items` | Seven food classes | Candidate classes selected independently for every coffin item. |
| `Pedestal_MinSpawnableAIAmount` | `1` | Minimum AI count for the non-coffin outcome. |
| `Pedestal_MaxSpawnableAIAmount` | `4` | Maximum AI count for the non-coffin outcome. |
| `Pedestal_SpawnableAI` | Four brown-bear entries | Candidate classes selected independently for each AI spawn. |

There is no pedestal enable setting. Remove it from events and admin placements to disable the feature.

## Chance behavior

The scripts roll an integer from `0` through `100`, inclusive. That means there are 101 possible values.

The grave and pumpkin settings succeed when:

```text
roll <= setting
```

Their approximate success probability is:

```text
(setting + 1) / 101
```

| Setting | Approximate success chance |
| ---: | ---: |
| `0` | 0.99% |
| `8` | 8.91% |
| `25` | 25.74% |
| `50` | 50.50% |
| `75` | 75.25% |
| `100` | 100% |

The pedestal uses the opposite comparison:

```text
roll >= Pedestal_ChanceToSpawnCoffin
```

Its approximate coffin probability is:

```text
(101 - setting) / 101
```

| `Pedestal_ChanceToSpawnCoffin` | Approximate coffin chance |
| ---: | ---: |
| `0` | 100% |
| `25` | 75.25% |
| `50` | 50.50% |
| `75` | 25.74% |
| `100` | 0.99% |

Values outside `0-100` are not validated by the current schema. Do not use them to force an outcome; configure distribution or disable the relevant feature instead.

## Arrays and weighting

Every spawn or reward uses a random array element. Duplicate entries act as weights.

For example:

```json
"PumpkinGrenade_SpawnableAI": [
  "ZmbM_Mummy",
  "ZmbM_Mummy",
  "Animal_CanisLupus_White"
]
```

gives the mummy two of the three selection slots. This affects the class chosen for each spawn, not the total spawn count.

Keep arrays non-empty. The current scripts do not guard against an empty selection list or a failed object creation. Invalid classes can therefore produce missing outputs or script errors.

## Minimum and maximum values

The amount fields are passed directly to an inclusive random-number call. Keep every minimum less than or equal to its matching maximum:

- `BoogieMan_MinSpawnableAIAmount` / `BoogieMan_MaxSpawnableAIAmount`
- `PumpkinGrenade_MinItemsAmount` / `PumpkinGrenade_MaxItemsAmount`
- `PumpkinGrenade_MinSpawnableAIAmount` / `PumpkinGrenade_MaxSpawnableAIAmount`
- `Coffin_MinItemsAmount` / `Coffin_MaxItemsAmount`
- `Pedestal_MinSpawnableAIAmount` / `Pedestal_MaxSpawnableAIAmount`

The schema does not clamp unsafe values.
