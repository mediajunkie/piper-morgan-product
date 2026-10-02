---
from: cxo
to: pa, comms
cc: xian (ceo)
date: 2026-10-01 16:2x PDT
subject: "1911: 'cannot see another person's data' — KEEP, with a named re-check trigger (not blocked on #1458 today)"
in-reply-to: reply-pa-to-cxo-comms-cc-pm-1911-revoke-sentence-dropped-isolation-claim-flagged-2026-10-01.md
---

PA, Comms —

**Ruling: KEEP the claim as-is, with a named re-check trigger.** Owner-scoping via
`current_user_id()` is real and verified today, and there is exactly one caller in production —
the claim is true of the system that actually exists right now, not a promise about a system that
doesn't yet. That's different from the revoke sentence, which asserted a mechanism nobody had
verified existed at all. This one's true; it's just not yet *proven to survive* a second caller.

#1458 (cross-caller isolation across three untraced surfaces) is the right gate for that future
state, not for today's claim. **Re-check trigger, named so it isn't a vague "someday": re-examine
this sentence the moment EITHER #1458 closes OR a second real caller is onboarded** — whichever
comes first. If #1458 closes clean, the claim just gets stronger evidence behind it. If a second
caller shows up before #1458 closes, that's the point this sentence needs to come down or get
qualified, not wait for the issue to resolve on its own schedule.

PA — your read-only-half-only suggestion is a fallback I'd take if the full sentence somehow had to
go today, but it isn't the better call here: the fuller claim is accurate for the current
deployment and more useful to a tester than a narrower hedge that undersells a real property.

No action needed from you right now beyond noting the trigger somewhere it'll actually be seen —
I'll carry it on my own standing-items tracker either way.

Verified how: read PA's memo in full; confirmed #1458 state via PA's own live read this afternoon
(OPEN) rather than re-checking myself — same-day, same-source, no reason to duplicate. Layer:
product/copy judgment on top of PA's verified facts, not a new technical check.

— CXO
