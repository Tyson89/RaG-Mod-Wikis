# RaG Wheel of Fortune

RaG Wheel of Fortune adds a placeable prize wheel with 16 result fields, configurable rewards, spin sounds, confetti, jackpot effects, and once-per-day player tracking.

[RaG Core](../core/index.md) is a hard dependency. Install and enable both mods on server and every client. Declared addon dependencies control PBO ordering.

## Start here

- [Gameplay, prizes, and daily limits](gameplay-and-prizes.md) explains spins, field selection, rewards, jackpot effects, and shared daily eligibility.
- [Setup, placement, class names, and troubleshooting](server-setup-and-class-names.md) covers installation, dependencies, placing wheel, public classes, and common failures.
- [Server configuration and spin data](server-configuration.md) documents reward JSON, `WheelData.json`, defaults, validation, and recovery.

## Behavior at a glance

- Players use **Spin Wheel** without holding item.
- Spin lasts random duration from configured `MinSpinningTime` through `MaxSpinningTime`.
- Physical landing field selects one of 15 normal reward settings or jackpot reward array.
- Successful prize spawns on ground at wheel's prize position.
- Normal win plays end sound and confetti. Jackpot plays separate sound and red fireworks effect.
- Each Steam64 ID gets one recorded spin across all placed wheels, not one spin per wheel.
- Spin is recorded before wheel starts. Bad reward class, empty field, or failed landing detection still consumes daily spin.
- Spin history survives restarts in `WheelData.json`.
- Date reset is checked only when spin manager instance starts. Server left running across midnight does not reset list until manager is recreated, normally through server restart.
- No token cost, permission list, configurable spin count, placement kit, or built-in wheel spawner exists.

## Links

- [Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=3308989311)
- [Source repository](https://github.com/Tyson89/rag_wheel_of_fortune)
- [RaG Core documentation](../core/index.md)
- [Support RaG Tyson on Ko-fi](https://ko-fi.com/rag_tyson)

!!! warning "No monetization, repacking, or reuploading"
    Public Workshop permissions allow use on approved monetized server only when this mod is not part of monetization. Mod itself may not be monetized, repacked, or reuploaded. Use original Workshop release.
