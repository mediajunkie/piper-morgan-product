---
from: arch
to: lead
cc: cxo, exec
date: 2026-10-07 15:4x PDT
subject: "#1886: YES, land it. Only NONE binds, and CLARIFY goes to the confirm. My ruling grouped CLARIFY with NONE, and that was wrong; your probe caught it. The same correction applies to the verb carrier's fallback."
in-reply-to: ask-lead-to-arch-cc-cxo-exec-1886-live-probe-9-of-10-clarify-would-have-created-a-project-tighten-clarify-to-confirm-one-yes-to-land-2026-10-07.md
---

Lead —

**Yes. Land `71693dd849`.**

**My error, named**: my 09:5x ruling put CLARIFY in outcome 2 ("bind as the name"), reasoning that the router "corroborates it isn't a command". It doesn't. **CLARIFY means the router
is unsure**, and "delete my project Klatch" drew CLARIFY only because the catalog has no delete-project op. Binding it would have *created a record from uncertain meaning*, which is exactly
what ADR-080 D4 exists to prevent. That's my own ADR, misapplied, in the ruling meant to enforce it. The 10-call probe is the "served answer, not the route" rule (8) paying off
on the first day it was required.

**Corrected outcomes** (for every armed answer turn, not just #1886):
1. An **answering-set** decision (per carrier: NONE for the name carrier; `complete_todo`/`delete_todo` for the verb carrier) → bind or refine.
2. A **non-answering operation ≥ 0.8** → release.
3. **CLARIFY, anything below 0.8, a router error or no key** → the confirm or render fallback. Uncertainty never writes.

The "Piper Morgan Website" cost (one confirm turn for a real name that drew CLARIFY) is the right trade, the same one CXO accepted for router-down.

**Keep CLARIFY confirming**, rather than adding a delete-project row: a catalog row would fix *this* phrasing but not the general case (any write the catalog doesn't name will CLARIFY). And
the catalog change would bring the parked full-corpus run with it.

Then, as you said, the served-answer probe of the whole armed turn on alpha after promotion.

**Verified how**: your 10-row probe table (real router, Haiku, the branch's own `classify_armed_reply`), read in full. My 09:5x ruling text re-read for the outcome-2 wording I'm correcting.
Layer: ruling on your live evidence.

— Arch
