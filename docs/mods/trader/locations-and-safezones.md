# Locations and safe zones

Static trader groups live in `Traders/Locations.json`. Enable `EnableStaticTraders` in root `Settings.json`. Traveling traders have their own placement in [Routes/Routes.json](traveling-traders-and-routes.md).

## Trader groups

Add groups to the top-level `Locations` array. Give each group a unique `Id`. Set `Enabled: false` to disable the group, or disable a single trader in its entry. An optional group `CurrencyId` overrides the catalog default.

| Trader field | Purpose |
| --- | --- |
| `TraderId` | Profile ID in `Trading/Catalog.json`. Use it once per group. |
| `EntityClassName` | Exact survivor or interactable object class. |
| `Position`, `Orientation` | Three numbers each, in DayZ position and orientation order. |
| `Attachments` | Survivor loadout. Each class needs a compatible slot. |
| `Enabled` | Defaults to `true`. |
| `CurrencyId` | Optional currency override. |
| `OpeningHoursEnabled`, `OpeningHour`, `ClosingHour` | Optional DayZ world-time opening hours. |
| `VehicleSpawnPoints` | Optional vehicle positions and orientations. |

The server looks for a nearby unbound entity of the exact class at each static location. If none is available, it spawns one at the configured transform. For a full example, see [first custom shop](server-setup-and-class-names.md#build-a-first-custom-shop).

## Opening hours

With `OpeningHoursEnabled: true`, opening is inclusive and closing is exclusive. `8` to `20` opens from 08:00 through 19:59. `20` to `6` crosses midnight. Equal hours mean always open. The server rechecks hours at checkout.

Restart after editing static locations, survivor loadouts, hours, or safe zones.

## Safe-zone settings

Set `EnableSafezones: true` in root `Settings.json` and add a `Safezone` object to the static group or route stop. Set its `Enabled` to `true`. `Center` is a separate `[x, y, z]` position and `Radius` measures horizontal distance in metres. The bundled static zones have `Enabled: false`.

| Field | Default | Effect |
| --- | --- | --- |
| `Enabled` | `false` | Activates the configured zone. |
| `Center`, `Radius` | `[]`, `150.0` | Supply three coordinates when enabled and check coverage at the border. |
| `BlockIncomingDamage`, `BlockOutgoingDamage` | `true`, `true` | Protect players inside and restrict damage they deal to other players. |
| `ProtectPlayerEquipment` | `true` | Protects items rooted in a protected player's inventory. |
| `DeleteAnimals`, `DeleteInfected` | `true`, `true` | Removes matching wildlife and infected from the zone. |
| `ExcludedEntityClasses` | `[]` | Exempts classes and their descendants from deletion. |
| `BlockWeaponFire` | `true` | Blocks supported weapon firing. |
| `BlockExplosives` | `true` | Blocks supported arming, trigger attachment, grenade unpinning, and remote trigger actions. |
| `BlockBuilding` | `true` | Blocks supported deploy and build actions. |
| `VehicleSpeedLimitKmh` | `30.0` | Caps car speed. `0` disables the cap. |
| `ShowNotifications` | `true` | Shows zone and exit protection notices. |
| `ExitProtectionSeconds` | `30` | Grace period after leaving the last overlapping zone. `0` disables it. |
| `PreserveHunger`, `PreserveThirst`, `PreserveDisease`, `PreserveTemperature`, `PreserveBleeding` | `false` | Pauses the corresponding survival effects in the zone. Existing disease and wounds remain. |

Exit protection follows the departed zone's incoming damage, outgoing damage, equipment, and weapon-fire settings. Building, explosive, speed, and survival restrictions apply inside the zone. Admin IDs bypass the weapon, building, explosive, and car-speed restrictions. Damage protections still apply.

Test the border with an ordinary player, including overlapping zones and any building or weapon mods that supply their own actions.
