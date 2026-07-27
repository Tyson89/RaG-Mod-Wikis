# Solar Panel

The Solar Panel provides power during daylight and can use an attached truck battery as night-time storage.

## Setup

1. Deploy `rag_baseitems_solarpanel_kit` outdoors.
2. Make sure there is no roof above it.
3. Attach a `TruckBattery` if power should continue at night.
4. Plug devices directly into one of the four sockets, or use a Cable Reel.

The panel supports plug types `2`, `6`, and `4`.

## Power behavior

- **Daylight, uncovered:** supplies connected devices and charges the attached truck battery at 2 energy per second.
- **Night, usable battery attached:** connected devices draw from the truck battery according to their energy usage.
- **Night, no usable battery:** no output.
- **Roof detected:** generation and battery output both stop.

The shelter check updates periodically. A panel placed under a roof displays a placement warning and cannot deliver power.

## Key classnames

```text
rag_baseitems_solarpanel_kit
rag_baseitems_solarpanel
```
