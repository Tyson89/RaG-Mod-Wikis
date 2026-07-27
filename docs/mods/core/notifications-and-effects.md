# Notifications and Effects

RaG Core includes notification icons and registered particle effects that dependent addons can reference without shipping duplicate assets.

## Notification icons

Send a standard DayZ extended notification with a Core icon:
```c
NotificationSystem.SendNotificationToPlayerIdentityExtended(identity, 10.0, "VEHICLE EVENT", "Your vehicle scan is complete.", RaG_Notifications.CARLIFT_ICON);
```

Available constants:

| Constant | Intended visual |
| --- | --- |
| `RaG_Notifications.FENRIR_ICON` | Fenrir |
| `RaG_Notifications.THUNDER_ICON` | Thunder/lightning |
| `RaG_Notifications.CARLIFT_ICON` | Vehicle lift |
| `RaG_Notifications.BEAR_ICON` | Bear |
| `RaG_Notifications.CAR_ICON` | Vehicle |
| `RaG_Notifications.PVP_ICON` | PvP |
| `RaG_Notifications.WOLF_ICON` | Wolf |
| `RaG_Notifications.ZOMBIE_ICON` | Infected |
| `RaG_Notifications.BLOOD_ICON` | Blood loss |
| `RaG_Notifications.WATER_ICON` | Dehydration |
| `RaG_Notifications.FOOD_ICON` | Starvation |
| `RaG_Notifications.DRAGON_ICON` | Dragon |

These constants resolve to paths under `RaG_Core\data\Notifications\`.

## Registered particles

Core adds particle IDs to `ParticleList`. Examples:

```c
Particle water = ParticleManager.GetInstance().PlayInWorld( ParticleList.EFF_RAG_WELLWATER, spawnPosition);

Particle lantern = Particle.PlayOnObject( ParticleList.VIKING_LANTERN, parentObject, "0 0.5 0", "0 0 0", true);
```

Available IDs include:

| Group | Constants |
| --- | --- |
| Dragon fire | `DRAGON_FIRE_BREATH`, `DRAGON_FIRE_PLAYER`, `DRAGON_FIRE_BALL`, `DRAGON_FIRE_BALL_GROUND`, `DRAGON_FIRE_BALL_IMPACT` |
| Celebration | `EFF_RAG_CONFETTI` |
| Beehive and smoker | `ENV_BEEHIVE_BEES`, `BEEHIVE_SMOKER`, `EFF_SMOKER_UP`, `EFF_SMOKER`, `EFF_SMOKER_DOOR_OPEN` |
| World objects | `EFF_TABLESAW`, `VIKING_LANTERN`, `EFF_RAG_WELLWATER` |
| Hazard and atmosphere | `EFF_TOXICBEAR`, `SPOOKY_AREA_GASS`, `SPOOKY_AREA_GAS_TINY`, `SPOOKY_AREA_GAS_AROUND`, `PEDESTAL_EFF` |

## EffectParticle wrappers

Core also provides ready-made `EffectParticle` classes such as `EffRaGConfetti`, `EffBeeHiveBees`, `EffBeeSmoker`, `EffTableSaw`, `EffRaGWellWater`, and the dragon-fire wrappers.

```c
protected ref EffRaGConfetti m_Confetti;

void PlayConfetti(Object parent)
{
    if (m_Confetti)
        return;

    m_Confetti = new EffRaGConfetti();
    SEffectManager.PlayOnObject(m_Confetti, parent, "0 1 0");
}
```

Store references when the effect lifecycle requires it, and stop or destroy looping effects when the parent is deleted or the feature turns off.

## Temperature-source setters

Core extends `UniversalTemperatureSource` with runtime setters:

```c
source.SetPosition(position);
source.SetFullRange(2.0);
source.SetMaxRange(5.0);
source.SetTemperatureCap(30.0);
source.SetTemperatureItemCap(60.0);
source.SetTemperatureItemCoef(0.5);
source.SetParent(parentEntity);
source.SetEnableOnTemperatureControl(true);
source.SetManualUpdate(false);
```

These methods modify the existing source settings. Your addon is still responsible for constructing the vanilla temperature source correctly and managing its activation and lifetime.

## Asset compatibility

Notification paths and particle constants are convenient shared assets, but they are not a substitute for addon-owned branding. Use Core assets when their meaning matches your feature. If a visual is specific to your addon or part of its identity, ship it in your own PBO.

Do not reference files by Workshop installation path. Use the config/script constants or PBO-relative paths exposed by Core.
