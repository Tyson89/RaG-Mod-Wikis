# Custom Liquids

RaG Core discovers custom liquids from `CfgLiquidDefinitions`. Third-party addons declare liquid semantics in config; no script registration call is required.

Core automatically applies the declared rules to consumption, container filling, vehicle fueling, radiator filling, persistence migration, display names, and inspect-menu colors.

## Predefined RaG Core liquids

RaG Core already reserves slots `1-23` for the following liquids. Use the numeric type ID in config arrays such as `ragAcceptedLiquidTypes[]`, or use the matching `RaG_Liquids` constant from scripts.

| Liquid | Config class | Script constant | Slot | Type ID |
| --- | --- | --- | ---: | ---: |
| Milk | `Milk` | `RaG_Liquids.LIQUID_MILK` | `1` | `8388608` |
| Honey | `Honey` | `RaG_Liquids.LIQUID_HONEY` | `2` | `16777216` |
| Honey wine | `HoneyWine` | `RaG_Liquids.LIQUID_HONEYWINE` | `3` | `25165824` |
| Red wine | `RedWine` | `RaG_Liquids.LIQUID_WINE_RED` | `4` | `33554432` |
| White wine | `WhiteWine` | `RaG_Liquids.LIQUID_WINE_WHITE` | `5` | `41943040` |
| Aviation gasoline | `AVGas` | `RaG_Liquids.LIQUID_AVGAS` | `6` | `50331648` |
| Whiskey | `Whiskey` | `RaG_Liquids.LIQUID_WHISKEY` | `7` | `58720256` |
| Espresso | `Espresso` | `RaG_Liquids.LIQUID_ESPRESSO` | `8` | `67108864` |
| Coffee | `Coffee` | `RaG_Liquids.LIQUID_COFFEE` | `9` | `75497472` |
| Tea | `Tea` | `RaG_Liquids.LIQUID_TEA` | `10` | `83886080` |
| Motor oil | `MotorOil` | `RaG_Liquids.LIQUID_MOTOROIL` | `11` | `92274688` |
| Energy drink | `EnergyDrink` | `RaG_Liquids.LIQUID_ENERGYDRINK` | `12` | `100663296` |
| Virus | `Virus` | `RaG_Liquids.LIQUID_VIRUS` | `13` | `109051904` |
| Poison | `Poison` | `RaG_Liquids.LIQUID_POISON` | `14` | `117440512` |
| Milk coffee | `MilkCoffee` | `RaG_Liquids.LIQUID_MILKCOFFEE` | `15` | `125829120` |
| Antivenom | `Antivenom` | `RaG_Liquids.LIQUID_ANTIVENOM` | `16` | `134217728` |
| Coolant | `Coolant` | `RaG_Liquids.LIQUID_COOLANT` | `17` | `142606336` |
| Brake fluid | `BrakeFluid` | `RaG_Liquids.LIQUID_BRAKE_FLUID` | `18` | `150994944` |
| Hydraulic fluid | `HydraulicFluid` | `RaG_Liquids.LIQUID_HYDRAULIC_FLUID` | `19` | `159383552` |
| Cooking oil | `CookingOil` | `RaG_Liquids.LIQUID_COOKING_OIL` | `20` | `167772160` |
| Vinegar | `Vinegar` | `RaG_Liquids.LIQUID_VINEGAR` | `21` | `176160768` |
| Apple juice | `AppleJuice` | `RaG_Liquids.LIQUID_APPLE_JUICE` | `22` | `184549376` |
| Orange juice | `OrangeJuice` | `RaG_Liquids.LIQUID_ORANGE_JUICE` | `23` | `192937984` |

These IDs are part of the persistent liquid format. Do not reuse or redefine them. Legacy IDs `600-622` are migration-only values that Core converts to the corresponding current IDs when stored items load.

## Dependency

Your liquid addon must load after both Core patches:

```cpp
requiredAddons[] =
{
    "RaG_Core",
    "RaG_Core_Scripts"
};
```

## Allocate a stable type

Third-party slots are `128` through `255`.

```text
type = slot * 8388608
```

Example: slot `128` produces type `1073741824`.

| Slot range | Owner |
| ---: | --- |
| `1-63` | RaG Core, reserved |
| `64-127` | Official RaG addons, reserved |
| `128-255` | Third-party addons |

Rules:

- Use one unique slot per liquid.
- Coordinate slot ownership with other integrations before release.
- Never change a released type; the value is persisted inside stored items.
- Never use legacy types `600-622`, ordinary small integers, or vanilla liquid bit values.
- Runtime validation reports a collision but cannot resolve it.

Define a matching constant in your own `3_Game` class when scripts need the value:

```c
class MyMod_Liquids
{
    static const int LIQUID_MAPLE_SYRUP = 1073741824;
};
```

Do not patch `RaG_Liquids` just to add third-party constants.

## Declare the liquid

```cpp
class CfgLiquidDefinitions
{
    class MyMod_MapleSyrup
    {
        type = 1073741824;
        displayName = "#STR_MYMOD_MAPLE_SYRUP";

        ragLiquidFramework = 1;
        ragOwner = "MyMod";
        ragColor = 13408563;
        ragLiquidGroups[] = {"Drink", "Food", "MyMod_Maple"};
        ragDrinkable = 1;
        ragFuel = 0;
        ragCoolant = 0;
        ragVehicleFluid = 0;
        ragHazardous = 0;

        flammability = -10;
        liquidFreezeThreshold = -2;
        liquidThawThreshold = 0;
        liquidBoilingThreshold = 105;

        class Nutrition
        {
            fullnessIndex = 1;
            energy = 70;
            water = 30;
            nutritionalIndex = 75;
            toxicity = 0;
            digestibility = 2;
            agents = 0;
            agentsPerDigest = 0;
        };
    };
};
```

## RaG properties

| Property | Required | Meaning |
| --- | --- | --- |
| `ragLiquidFramework` | Yes | Set to `1` to opt into custom-liquid handling. |
| `ragOwner` | Yes for third parties | Stable addon or author identifier shown in registry diagnostics. |
| `ragColor` | Yes | `0xRRGGBB` display color written as a decimal integer in config. |
| `ragLiquidGroups[]` | Yes | One or more non-empty, case-sensitive group names. |
| `ragDrinkable` | Yes | Allows consumption when `1`. |
| `ragFuel` | Yes | Allows `ActionFillFuel` when `1`. |
| `ragCoolant` | Yes | Allows `ActionFillCoolant` when `1`. |
| `ragVehicleFluid` | Yes | Must be `1` whenever fuel or coolant is enabled. |
| `ragHazardous` | Yes | Exposes hazardous classification through the registry API. |
| `Nutrition` | Yes | Required even for non-drinkable liquids because vanilla systems inspect it. |

Every RaG boolean must be exactly `0` or `1`. Use a literal display name while developing or ship the localization key. Core reports missing and unresolved names.

`RaG_Colors` contains reusable RGB constants for common liquids and materials. Config values still need to be numeric; script constants cannot be referenced directly from `config.cpp`.

## Configure containers

Vanilla `liquidContainerType` continues controlling vanilla liquids. RaG properties separately control custom liquids.

Accept every custom liquid:

```cpp
ragAcceptAllCustomLiquids = 1;
```

Accept selected types:

```cpp
ragAcceptAllCustomLiquids = 0;
ragAcceptedLiquidTypes[] = {1073741824};
```

Accept a group:

```cpp
ragAcceptAllCustomLiquids = 0;
ragAcceptedLiquidGroups[] = {"MyMod_Maple"};
```

Accept selected custom liquids and no vanilla liquid:

```cpp
liquidContainerType = -2147483648;
ragAcceptAllCustomLiquids = 0;
ragAcceptedLiquidTypes[] = {1073741824};
```

`-2147483648` is signed `0x80000000`, an unused vanilla liquid-mask bit. It matches no vanilla liquid while RaG evaluates custom rules.

Important behavior:

- No RaG rule means custom liquids are rejected.
- `ragAcceptAllCustomLiquids=1` overrides type and group allowlists and warns when combined with them.
- Type and group allowlists are additive.
- A non-empty container cannot mix two different liquid types.
- `Bottle_Base` and `Barrel_ColorBase` inherit `ragAcceptAllCustomLiquids=1` from Core.
- Set that property to `0` explicitly on a restricted subclass.
- Keep the normal `liquidContainerType` when the container should also accept selected vanilla liquids.

## Query semantics from scripts

```c
LiquidFrameworkRegistry registry = LiquidFrameworkRegistry.GetLiquidFrameworkRegistry();
int liquidType = item.GetLiquidType();

if (registry.IsCustomLiquid(liquidType))
{
    bool drinkable = registry.IsDrinkableLiquid(liquidType);
    bool fuel = registry.IsFuelLiquid(liquidType);
    bool coolant = registry.IsCoolantLiquid(liquidType);
    bool vehicleFluid = registry.IsVehicleFluid(liquidType);
    bool hazardous = registry.IsHazardousLiquid(liquidType);
}

bool accepted = registry.CanContainerAcceptLiquid(container, liquidType);
LiquidDetailsBase details = registry.GetLiquid(liquidType);
```

`Liquid.GetLiquidConfigProperty()` can read a property by type when direct config access is necessary:

```c
string flammability = Liquid.GetLiquidConfigProperty(liquidType, "flammability");
string energy = Liquid.GetLiquidConfigProperty(liquidType, "energy", true);
```

Prefer the typed registry methods for supported semantics. Raw text property access is easier to misuse.

## Do not register semantics from script

`LiquidFrameworkRegistry.RegisterLiquid()` registers only name/color details. It does not create a full custom definition or set drinkable, fuel, coolant, group, or hazard behavior.

Third-party gameplay liquids should therefore use `CfgLiquidDefinitions` with `ragLiquidFramework=1`. Treat the config definition as the source of truth.

## Automatic behavior

For valid custom definitions, Core automatically:

- blocks consumption unless `ragDrinkable=1`
- enables compatible vehicle fueling for `ragFuel=1`
- enables compatible radiator filling for `ragCoolant=1`
- enforces per-container type and group acceptance
- prevents mixing different liquid types
- migrates RaG legacy liquid types `600-622` when stored items load
- supplies display name and color data to supported UI

## Validation

Enable `EnableDebugLog` in `RaG_Core.json`, then inspect the Core debug log for `[RaG Liquid Framework]`.

The startup registry dump includes type, slot, owner, config class, groups, derived action capabilities, color, and semantic flags. Core also reports duplicate types, invalid ranges, missing properties, invalid booleans, unknown groups/types, and unresolved localization.

Before release, test:

1. Client and dedicated-server startup with no collision or definition errors.
2. Empty and partially filled container acceptance.
3. Rejection of disallowed custom and vanilla liquids.
4. Drink, fuel, coolant, and hazard behavior.
5. Inspect-menu display name and color.
6. Save, restart, transfer, and another restart with the same persisted type.
