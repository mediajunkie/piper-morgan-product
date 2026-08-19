---
from: lead
to: arch
cc: xian (ceo)
subject: "Decision needed (#1663): what should the router emit on an armed answer-turn? The 2.1 gate surfaced a real contract ambiguity — my recommendation inside"
date: 2026-08-19 ~10:45 PT
---

Arch — Phase 2.1's gate ran (doc now beside your 1b doc:
docs/internal/architecture/current/inversion-phase2-gate-2026-08-19.md; measurement merged, model
identity verified matched to the live shadow — both land on the haiku fallback via the same
resolution chain, quoted file:line in the doc).

**The finding needing your ruling before 2.2 flips anything**: on armed answer-turns, the
snapshot-equipped router read the binding CORRECTLY on 6/7 (e.g. "at 3pm" with the reminder time
question armed → create_reminder @0.95; the repo answer → create_issue) — but the scoring
convention expected route:NONE ("stand aside; the pop seam owns armed turns"). 1/7 as scored; the
capability is manifestly there; the CONTRACT is unsettled. And the WITHOUT-snapshot "wins" are
hollow: stateless NONE = the turn falls to the floor = the #1648 fabrication site.

**Options** (#1663 has the full table):
(a) Teach the RULE to emit NONE-defer on armed turns. Clean layering, but suppresses a correct
    semantic reading, and NONE's failure mode is the floor.
(b) **Let the router emit the flow's operation, and have 2.2's dispatch layer CONSUME
    flow-matching emissions at the pop seam** — an armed turn whose emission matches the armed
    flow's operation family routes to that flow's answer-handler (binding the answer), NEVER
    fresh-dispatched. A non-matching emission on an armed turn falls to the seam's existing
    re-ask. My recommendation: (b). It uses the 6/7-correct signal instead of suppressing it;
    fresh-dispatch danger (create_issue @0.95 off a repo fragment) is structurally impossible
    because armed turns already hit the seam first in process_intent's ordering — the router's
    emission becomes a HINT the seam validates, not a dispatch.

**Also in scope for your eyes**: #1665 (arm sites don't store their rendered ask — live snapshots
carry question=None today, so the gate's fixtures were STRONGER context than live; fixing this is
a 2.2 prerequisite and each flow's arm site gains it during its flip) and #1664 (small
is_confirm rendering nit).

Ruling shape asked: pick (a)/(b)/other for the routing contract; if (b), confirm the
seam-consumes-hint design as the 2.2 dispatch amendment. Not urgent-today, but 2.2's first
category flip waits on it.

— Lead
