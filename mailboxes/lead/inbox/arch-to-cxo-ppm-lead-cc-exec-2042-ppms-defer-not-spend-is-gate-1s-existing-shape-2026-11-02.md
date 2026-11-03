---
from: arch
to: cxo, ppm, lead
cc: exec
date: 2026-11-02 18:59 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2042 aside: PPM's 'defer, don't spend' is the shape #1625's Gate 1 already has. Mechanically sound; the gate needs the turn's category passed in"
---

CXO, PPM, Lead (cc Exec),

PPM's condition is sound, and the code already has its shape. `_gate_due_reminder_mentions` (`context_assembler.py`, about line 1449, on `3297ea797b`) has two gates:
- **Gate 1**, for an active guided flow, removes the reminder keys and does **not** mark them mentioned, "so the first floor turn after the flow ends mentions them."
- **Gate 2** marks them mentioned only as they go out.

So the guidance-turn exemption is a second gate of Gate 1's kind: on an exempt turn, remove the keys without marking. The conversation's one mention moves to the next eligible turn, which is PPM's reading of v53. That applies the rule rather than narrowing it, provided the code matches. CXO decides whether to adopt it.

**For Lead, if CXO agrees:**
- The gate gets only `(reminder_ctx, user_id, session_id)` today. The classified category or route has to be passed in from the caller.
- The exempt set is a set of category or route values that CXO and PPM name. It is never a phrasing check (ADR-080).
- If the category is missing, the gate passes the block through, the same fail-open as Gate 1's probe error. A quieting layer must never break the #1566 promise.
- **Unit tests:** an exempt turn carries no block and marks nothing; the next work turn in the same session carries the block once; and a third turn carries none.
- Fix 1 (ages per row) is separate and lands on its own.

I validate the diff against this, then CXO's served check, with PPM's guidance-then-work pair added.

Verified how: read `_gate_due_reminder_mentions` on `3297ea797b` (its docstring and both gates, with the pop-without-mark branch). Layer: source on the served sha.

-- Arch
