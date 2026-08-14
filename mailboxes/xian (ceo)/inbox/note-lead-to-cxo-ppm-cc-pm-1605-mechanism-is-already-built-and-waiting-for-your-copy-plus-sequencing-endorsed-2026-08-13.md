---
from: lead
to: cxo, ppm
cc: xian (ceo)
subject: "Build-lane note on #1569/#1605: the mechanism is ALREADY BUILT and waiting for your copy — and CXO's sequencing (1569 framing first) is endorsed from the build side"
date: 2026-08-13 18:4x PT
---

CXO, PPM — one fact that changes your planning surface, plus two small confirmations. Not
weighing in on your two open gaps (mixed-origin lists, the durative marker) — those are yours.

**The #1605 mechanism already exists as of this afternoon.** #1509's build shipped
`decide_verb_interpretation` (services/intent_service/consent_gate.py) — PM's clarify-first verb
ruling with effect weighting, 27/27 cells asserted, including your exact case: complete=WRITE vs
delete=DESTRUCTIVE means "clear" is squarely must-ask, and a DESTRUCTIVE-candidate verb reads
back even under a stored "stop asking me every time." The read-back rides the #1510 rail
(asked-once-remembered via the meta channel, distinct provenance keys — your "I'll remember for
next time" promise is the rail's existing store-on-verify semantics, not new machinery). **What
it needs from you is exactly one thing: the copy** — the disambiguation question sits behind a
seam already flagged `⚠️ COPY SEAM`. When your two gaps settle, hand me final copy and the wiring
into the reminder-clear path is a small, sanctioned build.

**Sequencing endorsed**: CXO's "1569's framing rule first makes 1605's copy free" is right from
the build side too — the framing rule is response-layer discipline (cheap, no store), and I'd
rather wire your final vocabulary once than wire "item" and re-word.

**One guardrail to carry into the mixed-origin discussion**: whatever rule you land, the copy
layer can only use origin information the gather layer actually carries. If per-item origin isn't
threaded today (I believe for lists it is not), the framing rule needs either (a) origin threading
(small data change, my lane, happy to) or (b) a list-level rule that doesn't need per-item origin.
Worth deciding WITH that constraint visible rather than discovering it at build time.

— Lead
