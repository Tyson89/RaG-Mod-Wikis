# Locations, loadouts, and loot

Main JSON stores locations. Separate loadout JSON stores category-specific infected pools and loot:

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

Built-in Chernarus locations use `100` meter spawn areas. Other maps need custom coordinates; default Chernarus list does not adapt automatically.

Supported default category names:

```text
Military
FirstResponder
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
  "Version": 1,
  "HordeLoadouts": [
    {
      "Category": "Military",
      "Infected": [
        {"ClassName": "ZmbM_SoldierNormal", "Weight": 3},
        {"ClassName": "ZmbM_usSoldier_Heavy_Woodland", "Weight": 1}
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

Keep at least one valid loadout. A loadout with no valid infected entries is removed. Duplicate category names are merged case-insensitively.

## Infected selection

`Weight` is relative, not percentage. For weights `3` and `1`, first class has 75% selection chance and second has 25%. Values below `1` become `1`.

Class must exist in `CfgVehicles` and inherit from `ZombieBase` or `DayZInfected`. Invalid classes are removed at startup. Classes from another mod work only when provider mod is installed on server and clients.

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

| Category | Default infected theme | Default loot theme |
| --- | --- | --- |
| `Civilian` | Broad civilian pool | Canned food and chips |
| `Military` | Patrol and soldier variants | Rifle/pistol ammunition and bandages |
| `FirstResponder` | Doctors, paramedics, nurses, patients, firefighter | Medical supplies |
| `Hunting` | Hunter variants | `.308` ammunition and hunting knife |
| `Industrial` | Mechanics, construction, industrial, offshore, handyman | Tools and duct tape |
| `Prisoner` | Prisoner | Handcuff keys and lockpick |
| `Priest` | Priest | Rags |
| `NBC` | Grey, yellow, and white NBC infected | Filters, charcoal tablets, bandages |
| `Police` | Police and special-force variants | Pistol ammunition, handcuff keys, bandages |

Generated file is authoritative full class list. Edit generated file instead of copying shortened example from this page.
