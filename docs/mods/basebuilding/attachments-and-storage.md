# Attachments and Storage

Attachment slots vary by structure and construction stage. If a slot is absent, finish the required stage first and confirm that the model supports that attachment.

## Locks

Completed doors, gates, and the floor hatch expose vanilla Combination Lock and RaG-managed vanilla `DigitalCodeLock` slots only when gate stage is fully built. Structure must be closed before either lock can be attached, and only one lock can protect it at a time.

RaG Core adds persistent ownership, remembered access, auto-lock, admin recovery, optional battery-free operation, and configurable raiding to vanilla digital lock. Dismantling protected door or gate stage unlocks attached lock. Windows expose neither lock slot. See [RaG Core: Vanilla DigitalCodeLock](../core/vanilla-digital-codelock.md).

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
