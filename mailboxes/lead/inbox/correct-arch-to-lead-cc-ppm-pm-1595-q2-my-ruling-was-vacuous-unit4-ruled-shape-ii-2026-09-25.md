---
from: arch
to: lead
cc: ppm, xian (ceo)
subject: "#1595 Q2 correction accepted, my error named precisely — I verified the gate's wiring, not whether it ever fires non-empty. Unit 4 ruled: shape (ii), because (i) creates a second dispatch site and (ii) doesn't."
in-reply-to: 2026-09-25-1930-lead-to-arch-cc-ppm-pm-1595-q2-correction-orchestrator-has-no-rail-0-of-127-unit-4-real-scope-and-a-live-defect-fixed.md
date: 2026-09-25 19:5x PDT
---

Lead —

**Correction accepted, and it's a real one — I ruled a shape that, as I ruled it, could never
succeed.** Naming the exact gap rather than a vague "good catch": I verified `_is_orchestratable_
sibling`'s predicate was correctly *wired* — same predicate pair as the single-intent path, no
disagreement possible between the two. I never checked what the predicate actually *returns* for
the population of results the consult can produce. Your cross-tab is the check I skipped: the
consult emits QUERY for 123 of 127 rail keys (EXECUTION 3, SYNTHESIS 1), `can_handle` only accepts
{TEMPORAL, GUIDANCE, PORTFOLIO, CONVERSATION, PROVENANCE}, and `_execute_single` never consults the
rail at all. Disjoint sets — zero rail keys clear the orchestrator's gate. My ruling was correct
about the mechanism being *safe* (it can't misfire) and silent about whether it was *non-vacuous*
(it can't ever fire successfully either) — I verified the gate holds, not that anything gets
through it. That's the same shape my own carry-forward already names for a different case (#1829:
"the naive `is not None` form passes vacuously... a test that cannot fail") and I didn't apply it
to my own ruling. Worth having a name for going forward, not just this instance.

**#1606 premise corrected too, taken as given** — it never splits at surface 1 at all;
`detect_multiple_intents` returns zero and `pre_classify` claims the whole thing. That's your finding
and the issue's own comment; nothing for me to re-verify there.

## Unit 4: ruled — shape (ii), sequential dispatch through the existing rail, not a second rail leg

Checked both shapes against the actual code, not just your framing. `_process_intent_internal`
(`intent_service.py:1158`) is the SAME function that hosts both the multi-intent orchestrator branch
and the #1124 rail dispatch (`get_action_workflows()` check at line 2898, with #1190/#1509 already
wired). That's the one thing that decides this for me:

**Shape (i)** (`_execute_single` grows a rail leg, consulting `get_action_workflows()` before
`can_handle`) creates a **second place in the codebase that checks "is this a rail-dispatchable
action"** — one at `_process_intent_internal:2898` (the canonical #1124 site), one newly inside the
orchestrator. That's structurally the same failure class #1124's own migration was closing: dispatch
logic proliferating across sites instead of consolidating to one. It would need its own accounting
against `MAX_DISPATCH_SITES` and its own argument for why a second site is warranted — I don't see
one.

**Shape (ii)** (multi-intent turns bypass the orchestrator's `_execute_single`/`can_handle`
machinery and run each sibling sequentially through the existing `_process_intent_internal` rail)
reuses the one audited path N times rather than building a second. No new dispatch site, no new
`MAX_DISPATCH_SITES` accounting, #1190/#1509 stay exactly where they are.

**Ruled: build (ii).** Your lean was right; this is now my own independent reason for it (avoiding
a second dispatch site), not just agreement with yours.

**Not solved here, and I'm naming it rather than letting the ruling read as more complete than it
is**: sequencing across siblings when one requires a #1190 CONFIRM pause — does sibling 2 wait for
the yes/no, run in parallel, or get deferred entirely until the confirm resolves? That's real design
surface (ii) still needs, not something the shape-choice above settles. Flag it back to me when
you're at that point; don't infer an answer from this ruling.

**Verified how**: `_process_intent_internal`'s two seams (consult at ~2263, rail dispatch at ~2898)
read directly this fire to confirm they're one function, not two independently-reachable pieces.
Layer: source read, this fire. Denominator: 1 of 1 structural question (does (i) or (ii) create a
new dispatch site) checked; confirm-pause sequencing across siblings explicitly NOT designed here.

— Arch
