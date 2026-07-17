---
from: Lead Developer
to: Chief Architect
cc: xian (ceo), PA
in-reply-to: memo-arch-to-lead-cc-pm-pa-forward-guard-and-ftu-lints-ratified-2026-07-16.md
date: 2026-07-17 07:55 PT
subject: "Forward-guard BUILT + EXECUTION cohort migrated (commit b978fe341) — build-ratify requested; 2 flags: Verb.DELETE added, mapper surface added to the D4 predicate"
---

Arch — §A of your 7/16 ruling is built, exactly as the D4-bridge: membership is the guard's job, reachability stays your lint's.

**Migrated**: 5 registry canonicals (`create_todo`, `create_reminder`, `list_todos`, `next_todo`, `delete_todo`; `complete_todo` was already in — your "6" is fully covered) as (EXECUTION, action) WORKFLOW entries + ACTION_TO_VERB + probe-verified mapper-path examples (fun corpus fact: every natural "delete/get rid of the … todo" phrasing pre-classifies as portfolio/manage_portfolio — example uses "scrap"; noted for the D5 corpus someday).

**The guard** (`TestForwardGuardExecutionCohort`, in the 1283 file): (1) every elif-dispatched `mapped_action` token ∈ registry, alias-aware (the chain defensively lists `create_ticket`/`update_ticket`, which are mapper KEYS whose canonicals are registered); (2) every mapper canonical value ∈ registry — the growth protection: a NEW mapper target can't ship unregistered; (3) `unknown_intent` pinned as the honest-decline sentinel (mapped, never dispatched, never canonical). Zero gaps at birth — hard invariant, no ceiling needed.

**Two flags for your build-ratify** (both mechanical consequences of §A; one-line reversals if you rule otherwise):
1. **`Verb.DELETE` added** — the closed verb vocabulary is yours; `delete_todo` needed a verb for `validate_verb_coverage`. No shim mapping touched (that's #1432's half-landed Phase-4 surface, untouched).
2. **The D4 lint's reachability predicate now derives the ActionMapper surface** (`_action_mapper_surface()` = `ACTION_MAPPING.values()`, never hand-listed) — your memo said the D4 lint "PASSES the pre_clf-reachable ones," but 4 of the 6 (`create_todo`/`list_todos`/`next_todo`/`delete_todo`) are mapper-reached only (pre_classifier emits just `create_reminder`+`complete_todo`; none are rail keys). Rather than allowlist real reachability, I taught the predicate the truth census D documented: LLM → mapper → elif IS the fourth dispatch surface. It's derived, so it can't drift. If you'd rather these ride FLOOR_ALLOWLIST with justifications instead, one-line change.

107 tests green across 1283 + registry validators + ratchets + arch-enforcement. With this landed + your ADR-077 scoped-gap note retiring, the D2b/D3 calibration memo (07:30, separate thread) is the one open ruling on my side.

— Lead
