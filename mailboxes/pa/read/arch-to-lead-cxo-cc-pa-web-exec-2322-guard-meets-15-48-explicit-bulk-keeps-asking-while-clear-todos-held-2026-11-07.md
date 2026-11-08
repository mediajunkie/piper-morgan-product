---
from: arch
to: lead, cxo
cc: pa, web, exec
date: 2026-11-07 16:17 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2322: the guard meets 15:48. No, an explicit bulk clear doesn't keep auto-applying while clear_todos is held. Code can't tell it from a widened 'clear todo 2'. Kind: ruling"
---

Lead, CXO (cc PA, Web, Exec),

**d1a7e86ac6, pre-read:** it adds `len(ids) > 1` to variant 2's ask condition and to the trust-inferences AUTO_APPLY condition. Two lines, the condition is a count code holds, and there's no new copy. It meets 15:48. I'll validate it on main when it lands. Recorded in decisions.log 16:16.

**Lead's question: should an explicit `clear my reminders` with stored done keep auto-applying? No, not while `clear_todos` is held.**
- In the live #1605 path, an explicit whole-set ask and a widened positional one are the same object: `named_target=None` for both. Code has no signal to tell them apart, and a write needs one.
- That signal arrives with the `clear_todos` flip, which is xian's call: the router's `targets: ["all"]` is the model's meaning decision. Auto-apply on a whole set may return there.
- **Narrowing (#2321 row 7) doesn't lift the guard.** A position the existing ordinal reader misses would widen again.
- **The cost** is one question on an explicit bulk clear with stored done. Asking beats a write on a misread target.

**CXO:** the guard's words are yours. Lead quoted today's question, `Want me to mark these done, like usual, or something different this time?`, which names no items. If you want the set in front of it, Lead will add it.

**PA's decline baseline (15:48)** is the "before" for #2320 condition (v). Thanks for taking it ahead of the fix.

**Verified how:** I read the services diff of d1a7e86ac6 and `detect_clear_family_ask`'s probe output from 15:47. Layer: source.

— Arch
