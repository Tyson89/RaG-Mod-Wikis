# Getting Started

## Requirements

The server and every connecting client need RaG Core and RaG BaseBuilding. Declared addon dependencies control PBO ordering; server mod-list order does not.

## Craft a kit

There are two supported crafting methods:

- Combine wooden planks with nails and select a kit recipe.
- Put planks and nails into a `RaG_BB_Book`, preview the desired part, and craft it.

The shipped source defaults require **4 wooden planks** and **10 nails** per kit. A server owner can change the amounts or disable individual recipes. See [Book crafting](book-crafting.md) for the book workflow.

## Place the kit

Put the kit in your hands and choose the placement action. The controls below are registered under **RaG BaseBuilding** in DayZ's control settings and can be rebound.

| Default key | Placement action | Book-preview action |
| --- | --- | --- |
| **Down Arrow** | Toggle snapping on or off. | Previous preview. |
| **Up Arrow** | Enable manual rotation at the current snap point. | Next preview. |
| **Right Arrow** | Cycle through valid, unoccupied snap points. | - |
| **Page Up** | Move the hologram upward by a small increment. | - |
| **Page Down** | Move the hologram downward by a small increment. | - |

Snapping starts enabled. The snapping system skips occupied connection points. If placement fails, cycle to another point, adjust the height, or temporarily disable snapping.

## Build the structure

1. Place the kit.
2. Attach the materials requested by the available construction stage: wooden logs, wooden planks, nails, or metal sheets.
3. Hold a tool allowed by `BaseBuildTools` and run the build action.
4. Repeat for every required or optional stage.

The shipped source defaults allow `Hatchet` and `Hammer` for building. Your server's JSON may override that list.

The floor hatch has two access choices after its frame is built: construct its staircase stage or use a Hammer to build the separate hatch ladder. Those choices conflict, so dismantle one before building the other. The separate ladder uses the `Ladder` material cost, but its custom dismantle action does not refund materials. The standalone step ladder is different; place its kit directly and use the **Take to hands** action to convert it back into a kit.

See [Building parts and class names](building-parts-and-class-names.md) and [Construction materials](construction-materials.md) for the available structures and stage costs.
