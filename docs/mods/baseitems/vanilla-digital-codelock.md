# Vanilla DigitalCodeLock

RaG Baseitems supports DayZ's vanilla `DigitalCodeLock` on containers that expose the dedicated `Att_CodeLock_RaG` slot. No third-party CodeLock mod is required or supported by this integration.

RaG Core manages locks attached through this slot. It adds:

- persistent ownership and remembered player access;
- automatic locking when a supported container closes;
- owner-only PIN reset and lock removal controls;
- configured admin recovery actions;
- optional battery-free operation;
- configurable raiding, raid tools, tool damage, and ruined-lock deletion.

Core settings apply globally to every RaG-managed vanilla digital lock. Baseitems does not create a separate lock configuration file. See [RaG Core: Vanilla DigitalCodeLock](../core/vanilla-digital-codelock.md) for setup, defaults, storage paths, raiding, and recovery.

## Use

1. Enable `EnableRaGDigitalCodeLock` in Core's `DigitalCodeLock.json`.
2. Put vanilla `DigitalCodeLock` in hands.
3. Attach it to a supported Baseitems container's **CodeLock** slot.
4. Set PIN through vanilla lock interface.

Lock blocks normal container opening while locked. Players with remembered access can open without entering PIN again when `DigitalCodeLockRememberAccess` is enabled. Closing supported container triggers Core auto-lock when `DigitalCodeLockAutoLockOnClose` is enabled and lock has PIN.

## Supported objects

Source exposes `Att_CodeLock_RaG` across many Baseitems storage and workstation classes, including cabinets, chests, crates, drawers, fridges, gun walls, lockers, medical storage, safes, shelves, shelters, workbench, and selected utility objects. Attachment UI is authoritative for specific object or variant.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| **CodeLock** slot is missing | Object or variant does not expose `Att_CodeLock_RaG`, or server/client builds do not match. |
| Lock attaches but RaG actions are missing | `EnableRaGDigitalCodeLock` is disabled, RaG Core is outdated, or server/client Core versions differ. |
| Container does not auto-lock | Enable `DigitalCodeLockAutoLockOnClose`, then confirm lock has PIN and container fully closed. |
| Player must enter PIN every time | Enable `DigitalCodeLockRememberAccess`; existing ownership alone does not grant remembered access. |
| Raid action is missing | Enable `DigitalCodeLockEnableRaiding`, lock target, and hold class listed in `DigitalCodeLockRaidTools`. |
