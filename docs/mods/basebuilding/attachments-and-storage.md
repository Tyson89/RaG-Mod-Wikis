# Attachments and Storage

Attachment slots vary by structure and construction stage. If a slot is absent, finish the required stage first and confirm that the model supports that attachment.

## Locks

Completed doors, gates, and the floor hatch expose the vanilla Combination Lock slot only when the gate stage is fully built. The structure must be closed before the lock can be attached.

Codelock Mod integration is compiled conditionally when `CodeLock` is present. Codelocks are rejected on window structures, and dismantling a protected door stage unlocks the attached Codelock.

## Camouflage nets and barbed wire

Model-specific parts expose camouflage-net and/or barbed-wire slots. Nets update with opening doors, gates, windows, and roof-end construction. Barbed-wire damage areas are repositioned for moving gate sections.

These attachments are not universal. The inventory UI is the reliable indication that a selected structure supports them.

## Christmas lights and gas lamps

- `BaseCanAttachXmasLights` controls Christmas-light slots on supported structures.
- `EnableAttachPortableGasLamp` controls the portable gas-lamp category on the ceiling / flat-roof structure.
- Attached portable gas lamps disable cast shadows while lit to reduce problematic wall shadows; normal shadow behavior returns when detached.

## Hide and show inventory

When `EnableHideShowInventory` is enabled, a player on the interior side of a structure can use **Show inventory** or **Hide inventory**. Hiding locks the relevant inventory slots and collapses the category in the inventory UI; showing reverses it.

This is an inventory-visibility feature, not a substitute for a lock.

## Wooden storage

`RaG_BB_WoodStorage` is constructed in three stages: floor, frame, and roof. Its storage category becomes available only after the roof stage is built. The structure cannot be dismantled while it contains items.
