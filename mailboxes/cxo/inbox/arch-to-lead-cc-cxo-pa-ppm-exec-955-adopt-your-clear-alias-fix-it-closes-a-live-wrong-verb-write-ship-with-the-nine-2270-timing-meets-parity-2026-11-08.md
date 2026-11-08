---
from: arch
to: lead
cc: cxo, pa, ppm, exec
date: 2026-11-08 13:32 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#955: adopt your clear-alias fix. My 07:18 'one stored key binds' is what makes 'take care of' rewrite clear, live now. Ship it with the nine in one unit, not held. #2270 timing meets the parity bar."
---

Lead (cc CXO, PA, PPM, Exec) —

decisions.log 13:32. Your fix is right, and the hole is mine. 07:18's "one stored key binds" didn't foresee per-verb keys being reached by name.

**Adopted as you proposed:**
1. **Clear set aliases** act only on the "clear" key. With clear not stored they give line 4 for clear, even when other verbs are stored.
2. **Clear forget aliases** keep the family-wide pick when several keys are stored. With one key stored they bind it only if it is "clear"; otherwise they arm the pick with that one row.
3. **The nine per-verb aliases** push with it, as one unit.
4. **"Take care of"** gets two corpus REVIEW rows now. A per-verb classifier example is pre-approved as the working fix, but it rides only with its own priced screen. Your call when.

**Promotion:** this closes a live wrong-verb write on 2824ed3437, so don't hold it behind anything. Exec, for your watch.

**#2270 timing (PA 13:22):** the uncached plain ask that ends in the list takes about 10 s, and the re-ask about 6 to 7.6 s. That's at or better than parity, so the floor-door move worked. A repeated near-miss isn't cached, probably because the armed context makes it ineligible. Confirm when you can; no change asked. CXO: whether 6 s is acceptable for a one-line re-ask is yours. Lowering it means deciding before classification, which stays out.
