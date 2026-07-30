# Server configuration

RaG Immersive Wells stores its versioned configuration at:

```text
$profile:\RaG_Core\Configs\RaG_Immersive_Wells\RaG_Immersive_Wells.json
```

Stop server before editing. Keep valid JSON, retain `Version`, and restart after every change.

## Default version 1 configuration

```json
{
  "Version": 1,
  "EnableWellCanTransferCholera": 0,
  "WellWaterChance": 50,
  "WellCholeraChance": 50
}
```

DayZ's JSON serializer represents script boolean as `1` and `0`.

## Settings

| Setting | Default | Actual effect |
| --- | ---: | --- |
| `Version` | `1` | Current schema version. Values below `1` are upgraded and saved as version `1`. |
| `EnableWellCanTransferCholera` | `0` | Enables cholera roll for direct drinking and container filling. Does not affect hand washing. |
| `WellWaterChance` | `50` | Maximum successful inclusive water roll from `0` through `100`. Default gives `51/101`, about 50.5%. |
| `WellCholeraChance` | `50` | Maximum successful cholera roll from `0` through `99`. Used only when transfer is enabled. Default gives 51%. |

Current schema does not validate, clamp, or normalize chance fields.

## Exact water probability

Water availability uses:

```text
Math.RandomIntInclusive(0, 100)
```

All `101` values are possible, and success uses:

```text
roll <= WellWaterChance
```

For values `0` through `100`:

```text
actual chance = (WellWaterChance + 1) / 101
```

| `WellWaterChance` | Actual usable-well chance |
| ---: | ---: |
| `0` | `1/101` = about 0.99% |
| `10` | `11/101` = about 10.89% |
| `50` | `51/101` = about 50.50% |
| `99` | `100/101` = about 99.01% |
| `100` | 100% |

`0` does not disable every ordinary well. Negative values produce no successful ordinary-well rolls, but source does not document or validate them. Use with care. Wells whose script returns `true` from `IsWellException()` ignore this setting and always have water.

## Exact cholera probability

Cholera uses an exclusive upper bound:

```text
Math.RandomInt(0, 100)
```

Results are `0` through `99`; success still uses `<=`. For `0` through `99`, actual chance is `(setting + 1) / 100`. `50` means 51%, and `99` or `100` means 100%.

Disable feature with:

```json
"EnableWellCanTransferCholera": 0
```

Do not rely on `WellCholeraChance: 0` for safe wells; it still gives 1% successful roll when transfer is enabled.

## Recommended examples

All ordinary wells usable, cholera disabled:

```json
{
  "Version": 1,
  "EnableWellCanTransferCholera": 0,
  "WellWaterChance": 100,
  "WellCholeraChance": 50
}
```

About half ordinary wells usable, 11% cholera exposure per applicable completed loop:

```json
{
  "Version": 1,
  "EnableWellCanTransferCholera": 1,
  "WellWaterChance": 50,
  "WellCholeraChance": 10
}
```

## Configuration recovery

If file is invalid or missing:

1. Stop server.
2. Back up broken file.
3. Move it out of active config directory.
4. Start server once to generate defaults.
5. Stop server.
6. Merge wanted values into generated schema.
7. Restart and test multiple wells.

Old Workshop text says file appears in server profile but does not show current RaG Core subdirectory. Current source reads and writes only path documented above.
