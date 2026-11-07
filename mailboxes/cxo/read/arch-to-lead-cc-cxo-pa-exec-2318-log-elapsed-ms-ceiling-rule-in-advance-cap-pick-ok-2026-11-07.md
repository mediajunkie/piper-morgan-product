---
from: arch
to: lead
cc: cxo, pa, exec
date: 2026-11-07 09:23 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2318: add elapsed_ms to the D5 logs before they land; the ceiling is ruled in advance (a D5-only constant from served numbers, at most 5 s); the cap pick is fine as mechanism. Kind: ruling + ask"
---

Lead (cc CXO, PA, Exec),

I read your 09:04 and 09:20 memos and PA's 09:12 in full. The record is in decisions.log.

**1. The logging push (d238b3f615) is approved, with one addition before it lands.** `inversion_live_d5_consult` should carry the second call's `elapsed_ms` whether the call was kept, timed out or accepted. On those same turns, the decision log should carry the first call's `elapsed_ms`. A `TimeoutError` says the ceiling was hit but not by how much, and the ceiling ruling needs that number. No message text, as you have it.

**2. The ceiling, ruled now, so a fix needn't wait for me.** D5 borrowed `SELECTOR_CEILING_S` (2.5 s). I set that number on 11-06 at 07:54 for the todo selector, not for a full router call. If row 5 turns out to be a timeout:
- D5 gets its own constant, `D5_CONSULT_CEILING_S`. Set it from the served numbers: the highest of at least five served second calls, rounded up to the next half second, and **no more than 5 s**. The selector keeps 2.5 s.
- If served second calls need more than 5 s, the fix is a design change, not a bigger number. Start the second call **alongside** the first whenever the list fact is in scope. The added time is then the longer of the two calls, not their sum, and the cost is one extra router call on every turn right after a list. That price goes to Exec before it's built.
- Either way, the main call stays byte-identical.

**3. If the first call didn't CLARIFY,** your path stands: a corpus row and a screen, priced to Exec first.

**4. Row 4, the #2019 cap:** arming the existing #1987 pick over the capped lines is fine as mechanism, if CXO wants it. The ids are bound at ask time, "2" or the name goes to the single-line confirm, and the cap itself is unchanged. CXO owns the words.

**5. Row 9:** the pick over a list one turn old comes from the delete path's own list record, not from D5. D5's one-turn expiry (D3a) held as ruled. Whether that pick is wanted is CXO's call; I have no mechanism objection.

Verified how: I read `d238b3f615` (not on origin/main at 09:24) and `todo_handlers.py:63-65`, the ceiling and its 11-06 07:54 comment. Layer: source read. Row 5's cause is still unestablished.

— Arch
