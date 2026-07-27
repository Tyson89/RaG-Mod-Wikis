# Car Lift

The Car Lift raises a supported vehicle, scans its damage system, and repairs damage found by that scan.

## Requirements

- Car Lift kit or static Car Lift kit
- Cable Reel and compatible power source for the powered version
- Open, non-ruined `rag_baseitems_notebook`
- Supported vehicle parked on the platform

## Operation

1. Deploy the lift and connect power if required.
2. Attach and open the notebook.
3. Park the vehicle on the platform and stop the engine.
4. Use the front control to raise the lift.
5. Aim at the notebook and start the scan.
6. Wait 17 seconds for the diagnostic.
7. Review the notification, then use the notebook's repair action if damage was found.
8. Lower the vehicle when finished.

## Diagnostic rules

- The lift must be raised, powered, and not already scanning.
- Repair is available only after a completed scan finds repairable damage.
- A scan can damage the notebook when `EnableDamageCarliftNotebook` is enabled.
- `CarliftNotebookDamageAmount` is applied per scan; repair itself does not damage the notebook.
- Lowering or changing the vehicle invalidates the prior diagnostic.
- `CarliftRepairAllAttachments` controls whether compatible damaged attachments are included.
- `EnableCarliftNotifications` controls the player-facing result messages.

## Compatibility

The scan reads the vehicle, its damage zones, and optionally its attachments. Vanilla vehicles and correctly configured modded vehicles work. A third-party vehicle with missing or malformed damage zones can return an incomplete result or an error; the lift cannot compensate for broken vehicle configuration.

## Key classnames

```text
rag_baseitems_carlift_kit
rag_baseitems_carlift_static_kit
rag_baseitems_notebook
```

[Watch the car-lift showcase](https://www.youtube.com/watch?v=XseV4CR7qK8)
