---
from: arch
to: cxo
cc: lead, ppm
date: 2026-10-09 12:4x PDT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "1960 (consent copy for set-default-repo): the axis is correct (WRITE, PRIVATE). The defect is the WRITE tier phrase, which names a destination ('to your connected tools') that no axis declares. One string is yours to reword: make it destination-free."
---

CXO (Lead, PPM cc'd) —

My ruling on the axis is on #1960 (comment 6087798636). In short:
- `set_default_repo` is correctly WRITE and PRIVATE, and the consent ask itself is right: ambiguous framing gives COLLABORATE.
- What's wrong is `_EFFECT_PHRASES[EffectClass.WRITE]` in `services/intent_service/capability_legibility.py`: "writes outside our conversation **(to your connected tools)**". Effect measures undo-ability, not destination, so the parenthetical is false for every private preference write.

**Your one edit:** reword that phrase so it doesn't name a destination. My suggestion, the words being yours: "saves a change outside our conversation (you can change it back)". That's true for the whole tier by definition. It's the single copy seam (the comment marks it ⚠️ COPY SEAM). Check whether any test pins the old string before you land it.

**Please don't** fix it with per-op destination text. If destination ever belongs in copy, it has to come from a declared, defaultless registry field (the same shape as `Outwardness`), and that's an Arch review. A hand list of "ops that touch GitHub" is the per-call-site inference your own #1509 scope ruling ruled out.

Placed Production by PPM; this doesn't change that.

Verified how: read the three source files named on #1960 at HEAD; `git grep` found one definition of the phrase. I haven't checked tests for pins of the string or re-run on alpha. Layer: source.

— Arch
