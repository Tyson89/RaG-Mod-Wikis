# Christmas Event

The Christmas module includes a tree, stockings, an Advent calendar, and a powered lantern. Date checks use the server's **UTC calendar date**, not accelerated in-game time.

## Christmas Tree gifts

When `EnableXmasTreeGifts` is enabled, a placed tree checks the configured `ChristmasMonth` and `ChristmasDay`. On that UTC date it spawns the configured number of gift boxes once. Each box receives one random classname from `XmasTreeGifts`.

The number of boxes is controlled by `XmasTreeMinGiftsAmount` and `XmasTreeMaxGiftsAmount`.

## Mining a spruce tree

`EnableMineChristmasTree` adds a six-second action for cuttable spruce (`piceaabies`) world trees. The current code allows this action **outside** the configured Christmas date, converts the world tree into an undecorated RaG Christmas Tree, and removes 20 health from the tool.

That date rule is easy to misread: it is the implementation in the current source, not a documentation typo.

## Stockings

Use a stocking from the player's hands to open it. It spawns random entries from `XmasStockingsGifts`, then deletes the stocking. The current code uses an exclusive upper bound: with minimum `4` and maximum `8`, it produces 4-7 items.

## Advent calendar

- It is interactive only during `ChristmasMonth`.
- A player can open the door matching the current UTC day.
- The calendar produces one random entry from `XmasCalendarsGifts`.
- Its last opened day persists across restart, preventing the same door from paying out again that day.
- It cannot be dismantled during the configured Christmas month.

## Key classnames

```text
rag_baseitems_xmas_tree
rag_baseitems_xmas_stocking
rag_baseitems_xmas_lantern
rag_baseitems_xmas_calendar_kit
```

See [Server Configuration](json-file-explanation.md#christmas-event) for the date, amount, and reward-pool settings.
