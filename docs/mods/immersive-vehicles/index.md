# RaG Immersive Vehicles

RaG Immersive Vehicles adds mechanical consequences and cabin features to DayZ vehicles: working engine oil, wheel wear, jacks and secured wheels, wet-surface sliding, collision damage, heating, interior lights, high beams, and exposed-occupant AI targeting.

RaG Core is a hard dependency. Load `RaG_Core` before `RaG_Immersive_Vehicles` on both the server and every client.

## Player guides

- [Getting started](getting-started.md) - the items, controls, and first maintenance steps.
- [Engine oil](engine-oil.md) - oil warnings, dipstick checks, refilling, leaks, smoke, and engine damage.
- [Wheels and jacks](wheels-and-jacks.md) - wheel wear, removal, locking, wheel loss, and both jack types.
- [Heating, lights, and passenger safety](heating-lights-and-passenger-safety.md) - cabin heat, interior lighting, high beams, and AI attacks through open doors.
- [Driving, damage, and repairs](driving-damage-and-repairs.md) - wet off-road sliding, animal/infected impacts, ruined parts, and repair behavior.

## Server and modding guides

- [Server setup and class names](server-setup-and-class-names.md) - dependency, economy entries, load order, and troubleshooting.
- [Server configuration](json-file-and-explanation.md) - the live version 2 JSON schema and every setting.
- [Vehicle-modding guide](modding.md) - requirements for third-party vehicle compatibility.
- [RaG Core configuration](../core/server-configuration.md) - shared configuration and logging.
- [Showcase video](https://www.youtube.com/watch?v=CEXnwykb5_4)

## Source-backed feature summary

- CE-spawned vehicles start with a random 0-35% of fuel capacity and 0-35% of oil capacity.
- Low oil produces a dashboard warning, smoke, and engine damage while driving.
- Wheels wear every two seconds while the engine is running above 7 km/h; off-road and road rates are configurable.
- Unlocked wheels can detach from a moving vehicle unless its class is in `WheelException`.
- The hydraulic car jack or farm jack can be required before wheel removal.
- Non-off-road vehicles can receive random traction impulses on wet, diggable surfaces.
- Vehicle impacts with infected and animals can damage the contacted vehicle zone; classes in `AnimalCollisionDamageExceptions` are ignored.
- A badly damaged engine on a moving, non-exempt vehicle can stall during the 100-second maintenance update.
- Drivers and front passengers can control heating; open doors, ruined windows, and exposed trunks/hatches prevent heat comfort.
- Powered interior lights follow open attached doors.
- The driver can switch between 30-meter low beams and 60-meter high beams.
- Drivers exiting while the vehicle is not in neutral stop the engine.

Legacy claims about an 8-energy start cost, reduced alternator charging, a 25°C heat cap, or repeated start attempts from damaged vital attachments are not present in the analyzed source and are intentionally omitted.

!!! warning "No monetization, repacking, or reuploading"
    RaG Immersive Vehicles may be used on an approved monetized server, but the mod itself may not be monetized, repacked, or reuploaded. Use the original Workshop release.
