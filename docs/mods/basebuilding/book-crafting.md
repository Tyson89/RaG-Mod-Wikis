# Book Crafting

`RaG_BB_Book` is an alternative to the normal plank-and-nail combination recipes. It previews every recipe currently allowed by the server configuration and crafts the selected kit at the player's position.

## Use the book

1. Put the BaseBuilding Book in your hands.
2. Attach wooden planks and nails to the book.
3. Use **Toggle Crafting Preview**.
4. Press **Up Arrow** for the next enabled kit or **Down Arrow** for the previous one.
5. Use the craft action while crouched.

The book is not consumed. Only the configured plank and nail quantities are removed. The crafted kit is created on the ground at the player's position.

## Why a kit is missing

The preview list is built from the live configuration. A kit is absent when any of these conditions applies:

- `DisableAllRaGBBKitCrafting` is enabled.
- `EnableBookKitCrafting` is disabled.
- The kit's `CraftToggles` entry has `ENABLED` set to `0`.
- The configuration failed to load or contains an invalid recipe identifier.

The book requires enough attached materials before the preview action appears. The shipped source default is 4 planks and 10 nails, controlled by `PlanksPerKitCraft` and `NailsPerKitCraft`.

## Server setup

Spawn or add `RaG_BB_Book` to the economy if players should use this workflow. Do not add `_BookHolo` classes; those are temporary client-side preview objects.
