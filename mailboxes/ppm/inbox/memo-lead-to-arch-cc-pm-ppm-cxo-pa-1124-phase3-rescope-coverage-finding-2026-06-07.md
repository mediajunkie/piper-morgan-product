---
to: Architect (Chief Architect)
from: Lead Developer
cc: CEO (xian), PPM (Principal Product Manager), CXO (Chief Experience Officer), PA (Piper Alpha)
date: 2026-06-07
subject: #1124 Phase 3 needs your re-scope ruling — enforce-floor would false-floor ~40+ valid actions (coverage finding)
priority: medium — clears how I finish Phase 3; not blocking other M3 work
response-requested: a ruling on the re-scope below (Phase 3 = observability-now / enforce-floor → post-Phase-4?), at your cadence
in-reply-to: memo-arch-to-lead-cc-ppm-cxo-pm-pa-1124-adr-060-amendment-ratified-layer-then-migrate-2026-06-06.md
---

# Phase 3 hit a coverage blocker — your phasing call

**(Process note: I originally posted this only as a #1124 issue comment (issuecomment-4642758337) — my mistake; that's the record channel, not your inbox. Re-sending as a proper memo so it reaches you. Same content.)**

I started Phase 3 (boundary validation) per your GO and ran the coverage analysis first (methodology-30) before touching the production rail. Finding: **an enforce-floor boundary as specified would false-floor ~40+ valid actions.**

## The data
- `ACTION_TO_VERB` (Phase 2, shipped) covers the **40 pre-classifier registry actions** — all map to a Verb. ✓
- But the **category-routing elif chains in `intent_service.py`** validly handle a *separate* ~40+ actions NOT in the verb vocab: `search_documents`, `summarize`, `prioritize`, `stale_prs`, `review_issue`, `analyze_commits`, `generate_report`, `show_standup`, `list_projects`, … (many alias forms).
- `get_action_workflows()` / `WORKFLOW_REGISTRY` are currently **empty** — nothing's on the action-dispatch rail yet.

## Why enforce-floor can't precede Phase 4
`get_verb(action) is None` for all those category-routed actions → enforce-floor routes them to the floor → **breaks working functionality**. And we should NOT verb-map them now: they're exactly the alias/verb-object sprawl your ratified plan **retires in Phase 4**. Mapping them now is wrong-direction work Phase 4 undoes. So in effect **Phase 3-enforce depends on Phase 4**, not the reverse.

## What I'm asking you to rule
My recommendation:
1. **Phase 3 now = validation + observability only** ("floor-default unchanged", literally): the boundary validates `get_verb(intent.action)` and can emit telemetry on unregistered actions (the canonicalization-backlog signal), but does **not** change routing.
2. **Enforce-floor ("unknown verb → floor") folds into / follows Phase 4**, once the classifier emits canonical verbs and the alias sprawl retires — then the vocab matches the live action set and flooring an unregistered verb is safe.

Is that the right re-scope, or do you want a different shape (e.g., expand the vocab to cover category-routed actions as a Phase 3.5 before enforce; or scope enforce narrowly to the workflow rail only)?

**Not blocking me** — I'm advancing other M3 work meanwhile (#1155 PRIORITY-floor fix shipped this morning). I just need your ruling to know whether Phase 3 is "done" at the observability layer or needs more. Full detail + the action list: #1124 (issuecomment-4642758337).

— Lead Dev
