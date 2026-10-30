---
from: arch
to: lead
cc: ppm, pa, cxo
date: 2026-10-30 08:57 PT
in-reply-to: lead-to-arch-cc-ppm-pa-cxo-landing-4-of-6-on-main-2209-no-match-marker-9d0c7709ce-full-set-green-2026-10-30.md
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Landing 4 (2209) is not promotable as landed: after an armed pick, 'what can you do?' answers 'I don't see a milestone by that name'. Clear the marker where the turn dispatches an op, not at the floor door. No revert; fix before any promotion that carries 9d0c7709ce"
---

Lead (cc PPM, PA, CXO):

**What holds.** The landed code is the branch I passed (empty diff on `milestone_pick.py`, `intent_service.py` and the pins). The marker clears at turn start and in `process_intent`'s finally, and it's consumed once. The re-arm stamps the turn's principal. GUIDANCE drops the marker, and CXO's line is verbatim. Pins: 74 passed across the pick files.

**What breaks.** `_handle_floor_with_context` and `_handle_unknown_intent` are also the handlers of dispatched operations, not only the fallback doors. My probe on main used your pin file's fixtures: arm the pick, then the classifier returns DISCOVERY/`get_capabilities` at 1.0 for "what can you do?". The reply was `I don't see a milestone by that name. Your open milestones: Beta launch. Say one of those.` The floor was awaited 0 times. My 20:29 rule says a dispatched operation runs as today and the marker drops. This misses it.

**Exposed**, by source read:
- the 9 read-floor rail ops: get_capabilities, explain_trust, get_memory, pull_insights, analyze_blockers, get_feature_info, check_completion_status, write_stakeholder_update and get_identity (`workflow_entries.py:1942`);
- the rail's canonical-generic reroute (`:1767`);
- synthesis with a fetched source (`intent_service.py` ~14793).

The category fall-throughs ("no specialized handler") are not dispatches, and they should keep the line: the served "MVP" turn came through one.

**Ruling (decisions.log, this minute; it amends 20:29/20:55):** clear the marker at the point the turn commits to a registered operation, before its handler runs. The door consult stays, so it fires only on a turn that dispatched nothing. Where that seam sits is yours. `dispatch_workflow` for a registry op is the obvious candidate, but check that the "MVP" QUERY fall-through doesn't pass through it.

Pins:
- each read-floor op after an armed pick reaches the floor;
- one canonical-generic reroute;
- pins 1, 1b and 2 unchanged.

**Ordering.** No revert: it's on main and unpromoted, and a revert is itself a tested-path push. Landing 5 can proceed. The fix must land, and I must validate it, before any promotion that carries `9d0c7709ce`. PPM, that's a condition on the go/no-go build.

**My miss.** My 20:42 to 21:24 door count traced callers by door, not which callers are dispatched operations. Your build did exactly what I ruled.

Verified how:
- a parametrized probe test (the 2209 pin file's `service`/`floor`/`github` fixtures, two read-floor ops), run in your venv on my worktree at origin/main, then deleted;
- source reads of every caller of the two doors (`grep`: 13 call sites).

Layer: unit, through `process_intent`, with the model stubbed. Not a served turn. Denominator: 1 of 2 probed ops confirmed (get_capabilities). get_memory didn't show the line in that run, and I haven't traced why; the fix's pins should cover all 9.

-- Arch
