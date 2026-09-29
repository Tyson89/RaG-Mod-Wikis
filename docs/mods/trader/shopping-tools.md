# Clothing try-on and weapon builder

Trader offers two shopping previews for eligible listings. They use currently offered catalog items and show a prospective purchase. They do not reserve stock or freeze prices; checkout still goes through server validation.

## Clothing try-on

Select one buyable, available clothing listing and press **Try On**. The preview copies the character's visible equipment, then shows selected clothing on its supported inventory slot. Move between slots with previous/next, search offered choices, select one item per slot, or clear a slot to show currently equipped item again. The displayed total adds selected listings in one currency. **Buy** purchases the chosen set as a single basket request.

Only clothing from this trader's available catalog, with a compatible player inventory slot and matching currency, appears in the try-on choices. An out-of-stock or disabled listing cannot be used as a purchasable choice. The preview is local visual guidance: a custom model can fail to attach in preview even when its configuration otherwise exists. Check actual slot compatibility, delivery space, stock, and final server result. Purchased pieces go through ordinary purchase delivery; preview does not equip them onto your character.

Tips:

- Preview headgear, mask, vest, and clothing together to check clipping before buying a set.
- Clear a slot when comparing a new piece against what you already wear.
- Empty inventory before a multi-piece purchase; ground fallback can leave separate pieces near your feet.
- Use one currency per outfit. A category with a different currency requires separate checkout.

## Weapon builder

Select one buyable, available `Weapon_Base` listing and press **Build Weapon**. The builder starts from the listed weapon and any configured `IncludedAttachments`. It previews compatible purchasable parts from **Weapon_Parts**, **Weapon_Optics**, **Muzzle_Devices**, **Weapon_Lights**, and **Magazines**. Search or navigate part choices, inspect the weapon model and stat display, then buy the weapon plus chosen parts as one transaction. Up to 12 additional purchased parts fit one build. Conflicting slot choices replace one another in preview.

The stat panel gives a comparison of recoil, sway, muzzle/noise, dispersion, and magazine characteristics from the preview. Modded scripts can change live performance; test final build in play. Displayed total includes weapon and selected purchasable parts; configured included attachments belong to weapon listing. The server rechecks price, stock, compatibility, transaction limits, and delivery at purchase time. If any line fails, the basket does not partially complete. A builder choice does not purchase loose ammo or ammo boxes merely because a magazine fits.

Tips:

- Pick the weapon first, then choose magazine and optic with the intended use in mind. A compatible magazine may be empty unless listing contents specify ammunition.
- Check weapon listing's included attachments before paying for similar parts.
- Compare muzzle device and optic together; occupied slots can rule out combinations even when each part is compatible with base weapon.
- Leave inventory space for weapon and parts. Keep purchase small when custom attachments have unusual inventory behavior.
- Check final in-game weapon and parts after checkout. Preview is a planning tool, not proof that a custom mod's runtime stats match its config numbers.

See [purchase contents](ammo-liquids-and-purchase-contents.md) for supplied magazines, ammunition, and configured attachments, and [player guide](getting-started.md#selection-basket-and-checkout) for normal checkout limits.
