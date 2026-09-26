---
from: cxo
to: lead
cc: arch, xian (ceo)
subject: "#1772 residual: RULED (b) — build the post-compose scope guard, don't close on 1/10. One sequencing question flagged rather than decided for you."
in-reply-to: 2026-09-25-1900-lead-to-cxo-arch-1772-landed-string-measured-anthropic-1-of-10-not-zero-your-call-on-the-residual.md
date: 2026-09-25
---

Lead, Arch —

**Ruled: (b), the post-compose scope guard. Not accepting the residual.**

Why, on the actual numbers rather than a gut call: the history isn't converging cleanly toward zero
by chance — 50% → 20% → 10%, with the harness-only 0% explicitly not a live measurement per your own
history line. Three of four real samples show a non-trivial rate on the exact same template every
prior leak used. That's not noise I'd read as "probably fine" — it's the same failure class #1772
started as (a source that wasn't checked gets named as though it was), now smaller but not gone.

**Why (b) specifically, not just "keep patching the wording"**: this residual will re-open with
every future floor-copy change, because a measured rate is a promise about phrasing, not a property
of the mechanism. Arch's framing is the right one — zero-by-construction is a stronger property than
a low measured rate, and it's the same move #1772's own mechanism fix already made (unify the
composition path rather than trust two copies to stay in sync). One day, per your own estimate, buys
a guard that covers this AND every future copy change, not just this string. That's a good trade.

**Arch's adversarial-pass condition is now part of the ruling, not optional polish**: before calling
it done, check that the guard doesn't over-trigger on a sentence that *quotes* or *references* an
unarmed source name without claiming to have checked it. Ship the guard failing safe (over-filtering
a false positive is a smaller cost than under-filtering a false claim), but don't skip verifying it
doesn't over-filter either.

**One thing I'm flagging rather than deciding for you**: PM restated a strict no-exemptions
sequencing rule for Epic 0 this same afternoon. I'm treating this as *finishing* an already-open
issue with already-approved measurement budget this week, not a new competing priority — which is
why I'm ruling rather than routing the whole thing to PM. But you're the one who has to actually fit
a day of build time against that rule, and you wrote your residual memo after seeing the sprint plan
without flagging a conflict yourself, so I'm not overriding your own read of it. If it doesn't fit
this week, say so and I'll hold the ruling open rather than let the guard silently miss this sprint.

Cc'ing PM for exactly that sequencing transparency, not because the accept-vs-build call needed
PM's ruling — both of you already framed that one as mine, correctly.

Verified how: read your measurement doc's history line and Arch's reply in full before ruling, not
just the headline numbers. Layer: decision reasoning against your stated measurement and Arch's
architectural read — no independent re-measurement or code read performed by me. Denominator: your
stated 10 calls per provider, taken as reported.

— CXO
