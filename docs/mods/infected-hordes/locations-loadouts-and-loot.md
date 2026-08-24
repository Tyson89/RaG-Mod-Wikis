# Locations, loadouts, attachments, and loot

Main JSON stores locations. Separate loadout JSON stores category-specific infected, attachment, and loot pools:

```text
$profile:\RaG_Core\Configs\RaG_InfectedHorde\RaG_InfectedHorde_Loadouts.json
```

## Location entries

```json
{
  "m_Name": "Custom Airfield",
  "m_Category": "Military",
  "m_SpawnAreaSize": 150,
  "m_Enabled": true,
  "m_Position": [5000.0, 10000.0]
}
```

| Field | Meaning |
| --- | --- |
| `m_Name` | Human-readable name used in logs and optional notifications. Blank names are invalid. |
| `m_Category` | Loadout category. Matching ignores case and surrounding whitespace. |
| `m_SpawnAreaSize` | Horizontal radius in meters around center. Candidate X and Z offsets are each rolled from negative through positive radius, then projected to surface/navmesh. Minimum `1`. |
| `m_Enabled` | `false` preserves entry but excludes it from selection. |
| `m_Position` | Exactly two numbers: world X and Z. Y is calculated from terrain. Zero position is invalid. |

Current Chernarus defaults contain 104 locations. Spawn-area distribution is 86 at `100` meters, 10 at `50`, 3 at `60`, 4 at `70`, and Kalinovka at `200`. Other maps need custom coordinates; default Chernarus list does not adapt automatically.

Default category distribution:

| Category | Locations |
| --- | ---: |
| `Civilian` | 67 |
| `Hunting` | 13 |
| `Military` | 10 |
| `Medical` | 3 |
| `Industrial` | 3 |
| `NBC` | 3 |
| `Police` | 3 |
| `Priest` | 1 |
| `Prisoner` | 1 |

Supported default category names:

```text
Military
Medical
Civilian
Hunting
Industrial
Prisoner
Priest
NBC
Police
Default
```

`Default` does not have its own loadout. It chooses one available loadout category uniformly. Unknown location categories are rewritten to `Default` during validation.

## Loadout file

```json
{
  "Version": 3,
  "HordeLoadouts": [
    {
      "Category": "Military",
      "Infected": [
        {"ClassName": "ZmbM_SoldierNormal", "Weight": 3},
        {"ClassName": "ZmbM_usSoldier_Heavy_Woodland", "Weight": 1}
      ],
      "Attachments": [
        {
          "ClassName": "PlateCarrierVest",
          "Chance": 1.0,
          "ConditionMin": 30,
          "ConditionMax": 70
        }
      ],
      "Loot": [
        {
          "ClassName": "Ammo_762x39",
          "Chance": 4.0,
          "QuantityMin": 5,
          "QuantityMax": 15,
          "ConditionMin": 50,
          "ConditionMax": 90
        }
      ]
    }
  ]
}
```

Keep at least one valid loadout. A loadout with no valid infected entries is removed. `Attachments` and `Loot` may be empty. Duplicate category names are merged case-insensitively, including their infected, attachment, and loot entries.

### Version 3 upgrade

When existing loadout config has `Version` below `3`, mod changes it to `3` and saves file. Any built-in category with missing or empty `Attachments` receives current default attachment entries. Custom categories remain empty, and categories already containing at least one attachment are not supplemented.

To disable attachments after upgrade, empty category's `Attachments` array while retaining `Version: 3`.

## Infected selection

`Weight` is relative, not percentage. For weights `3` and `1`, first class has 75% selection chance and second has 25%. Values below `1` become `1`.

Class must exist in `CfgVehicles` and inherit from `ZombieBase` or `DayZInfected`. Invalid classes are removed at startup. Classes from another mod work only when provider mod is installed on server and clients.

## Attachment selection

Every attachment entry rolls independently for every spawned infected. Entries are processed in array order and created with `CreateAttachment`, so items must fit an available attachment slot. When multiple successful rolls target same slot, earlier attachment occupies it and later creation fails.

| Field | Valid behavior |
| --- | --- |
| `ClassName` | Must exist in `CfgVehicles`, `CfgWeapons`, or `CfgMagazines`. Invalid entries are removed. Class must also be compatible with infected attachment slots at runtime. |
| `Chance` | Percentage clamped to `0-100`. `0` never creates item; `100` always does. |
| `ConditionMin`, `ConditionMax` | Percentage health, clamped to `0-100`; reversed values are swapped. |

Failed creation is logged once per infected-class and attachment-class pair, then repeated failures for that pair are suppressed. Classes from another mod require provider mod on server and clients.

## Loot selection

Every loot entry rolls independently for every spawned infected.

| Field | Valid behavior |
| --- | --- |
| `ClassName` | Must exist in `CfgVehicles`, `CfgWeapons`, or `CfgMagazines`. Invalid entries are removed. |
| `Chance` | Percentage clamped to `0-100`. `0` never creates item; `100` always does. |
| `QuantityMin`, `QuantityMax` | `-1` leaves class default quantity. Non-negative range is applied only to items supporting quantity. `0` becomes `1`; incomplete range copies supplied endpoint; reversed values are swapped. |
| `ConditionMin`, `ConditionMax` | Percentage health, clamped to `0-100`; reversed values are swapped. |

Loot is created in infected cargo. Some valid item classes do not fit particular infected inventory; failed creation is logged once per infected/item pair.

## Default themes

| Category | Default infected theme | Default attachments | Default loot theme |
| --- | --- | --- | --- |
| `Civilian` | Broad civilian pool | Blue Taloon bag, press vest, baseball cap; black sport glasses | Canned food and chips |
| `Military` | Patrol and soldier variants | Green assault bag, plate carrier, MICH helmet, tactical goggles | Rifle/pistol ammunition and bandages |
| `Medical` | Doctors, paramedics, nurses, patients, firefighter | Medical duffel bag, blue scrub hat, thin-frame glasses | Medical supplies |
| `Hunting` | Hunter variants | Hunting bag, hunting vest, olive boonie hat, black sport glasses | `.308` ammunition and hunting knife |
| `Industrial` | Mechanics, construction, industrial, offshore, handyman | Orange dry bag, reflex vest, orange construction helmet, thin-frame glasses | Tools and duct tape |
| `Prisoner` | Prisoner | Orange Taloon bag, prisoner cap, black sport glasses | Handcuff keys and lockpick |
| `Priest` | Priest | Improvised bag, brown flat cap, thin-frame glasses | Rags |
| `NBC` | Grey, yellow, and white NBC infected | Medical canvas bag, Smersh vest, tactical goggles | Filters, charcoal tablets, bandages |
| `Police` | Police and special-force variants | Black sling bag, police vest, police cap, thin-frame glasses | Pistol ammunition, handcuff keys, bandages |

Generated file is authoritative for full class names, chances, and condition ranges. Edit generated file instead of copying shortened example from this page.
