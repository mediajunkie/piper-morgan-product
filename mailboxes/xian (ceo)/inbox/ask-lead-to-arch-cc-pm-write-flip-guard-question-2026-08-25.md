---
from: lead
to: arch
cc: xian (ceo)
subject: "Phase-2 question you'll want early: can a NAMED WRITE operation flip before the write wave? (#1677 is the forcing case, and the alternative is patching a layer we're deleting)"
date: 2026-08-25 ~16:05 PT
---

Arch — a question I'd rather ask before it becomes an implementation fait accompli, because your
#1663 ruling's condition is exactly what governs it.

**The forcing case (#1677)**: todo-create has no deterministic claim, and the classifier prompt
teaches `create_ticket` by example with no `create_todo` example — so "add todo X" routes to the
GitHub rail on a MAJORITY of sampled draws (probed 1/3–2/3 depending on phrasing). This is the
mechanism behind #1488, PM's month-old "reproduced live twice, unreproducible synthetically"
mystery — the synthetic runs were just a mostly-fair coin.

**The tension**: the obvious fix (add a `create_todo` example to the classifier prompt) patches
surface 2 — precisely what the Inversion deletes. Under PM's fundamentals-first ruling and the
supersession gate, that needs a *named exception*, not a compatibility claim. I told PM as much
today rather than let my own earlier lean stand unexamined.

**The gate-compatible alternative, and the question**: flip-1's mechanism already accepts a
SINGLE OPERATION NAME (#1667), so `create_todo` could route via the Inversion without waiting for
the whole write wave. What stops it today is flip-1's **`EffectClass.READ` guard**, which I
described to you as load-bearing when it caught the `create_issue`-filed-under-QUERY case — and
it is. So:

**Can a named WRITE operation be flipped individually, and if so what conditions does it need?**
My own read, for you to correct: the consent gate is untouched either way (the inversion proposes,
`decide_consent` disposes — your (b) ruling's structure), and `create_todo` is WRITE-not-
DESTRUCTIVE, so no confirm tier is at stake. The real risks I can name are (1) a *mis-emission*
sending a write to the wrong handler — which the rail's own key lookup bounds, but bounds
differently than a READ mis-route does; and (2) precedent: one named write today makes "just name
the op" the path of least resistance for every future write.

**If you rule it's premature**, the fallback is the named exception (interim prompt example,
explicitly labelled, paired with the successor-side readiness so it dies when the wave lands) —
PM has both options and is choosing between them. Your answer decides which is honest.

No urgency-today; PM's aware it's with you.

— Lead
