# Server configuration

RaG Evil Snowman stores its versioned configuration at:

```text
$profile:\RaG_Core\Configs\RaG_SnowMan\RaG_SnowMan.json
```

Stop the server before editing. Keep valid JSON, retain `Version`, and restart after every change.

## Default version 1 configuration

```json
{
  "Version": 1,
  "SkinnedItemsAmount": 3,
  "SnowManSkinningItems": [
    "rag_carrot",
    "Banana",
    "BakedBeansCan"
  ]
}
```

## Settings

| Setting | Default | Actual effect |
| --- | --- | --- |
| `Version` | `1` | Current schema version. Values below `1` are upgraded and saved as version `1`. |
| `SkinnedItemsAmount` | `3` | Number of reward creation attempts after a Snowman is skinned. |
| `SnowManSkinningItems` | Three classes | Candidate class names. Each attempt selects one random entry. |

The source does not clamp or validate reward amount. Use `0` to disable custom reward attempts. Negative values also produce no attempts, but `0` states intent clearly. Large values create many world objects at one position and can hurt server performance.

## Selection and weighting

Each reward attempt calls a random selection separately. Duplicate class names act as weights, and one skinning action can select the same entry repeatedly.

Example:

```json
{
  "Version": 1,
  "SkinnedItemsAmount": 4,
  "SnowManSkinningItems": [
    "rag_carrot",
    "rag_carrot",
    "Apple",
    "Pear"
  ]
}
```

Here `rag_carrot` occupies two of four selection slots, so every attempt has a 50% carrot chance. Four attempts do not guarantee four different items.

## Valid reward classes

Keep `SnowManSkinningItems` non-empty and use spawnable `ItemBase` classes available on the server.

When an entry cannot be created as `ItemBase`, the script skips it and writes this RaG Core error:

```text
[RaG_SnowMan]:: [ActionSkinning]:: [OnFinishProgressServer]:: Unable to spawn: <class> - item is either not on the Server, or rag_snowman.json has errors!
```

The log text names `rag_snowman.json`, but current file path is `RaG_Core\Configs\RaG_SnowMan\RaG_SnowMan.json`.

Adding classes from another mod makes that mod an operational dependency. Load it on server and clients when its items have client assets. Bad classes do not fall back to another reward.

!!! danger "Do not leave reward array empty"
    Current code calls `GetRandomElement()` without checking array length. Use `SkinnedItemsAmount: 0` when rewards must be disabled; keep at least one valid entry in the array.

## Legacy path warning

Old Workshop text names:

```text
$profile:\RaG_Snowman\RaG_SnowMan.json
```

That path predates current RaG Core integration. Current source reads and writes only:

```text
$profile:\RaG_Core\Configs\RaG_SnowMan\RaG_SnowMan.json
```

Editing an old file has no effect on current code. Let the installed build generate a fresh file, then merge wanted reward values into it.
