# Phase 3 rule-11 sweep — licensing rows, served model (2026-10-09)

Running the gate's new rule 11 over every non-empty pattern list (alpha's 13-token live set) surfaced two
GOs: GUIDANCE_PATTERNS (its last 3 literals) and COMPLETION_HISTORY_PATTERNS (1 of 5). Their licensing
rows were scored one per row on the served router (anthropic:claude-haiku-4-5, resolved post-fallback,
#1620), together with the #1117 phrasings deposited under rule 10. Only these rows are wired into the
gate (Arch's per-row rule, so no bulk swap). The 26-row GUIDANCE-category run the GUIDANCE rows were cut
from is kept, unwired, at `inversion-phase3-guidance-category-rescore-2026-10-09-anthropic.md`. Its 3
MISMATCHes are rows deleted on 10-02 on surface-2 evidence.

**Neither list was deleted.**
- GUIDANCE_PATTERNS: 3/3 MATCH, rule 10/11 clean, but HELD on #1972. The read_canonical rail adapter
  drops offer_hint (#852 continuation for the #814 setup flow) and is_generic_response. The gate holds it
  in `HELD_FOR_CAUSE`.
- COMPLETION_HISTORY_PATTERNS: "When did we launch the beta?" scores check_completion_status @0.72, under
  the 0.8 dispatch threshold. The router would stand down to surface 2, which is the #1117 misroute, so
  the literal is load-bearing.

Variance check on the thinnest GUIDANCE row ("I need to setup my projects", first score 0.85), re-scored n=5
more on the served model: `get_contextual_guidance` @0.92, `get_contextual_guidance` @0.92, `get_contextual_guidance` @0.92, `get_contextual_guidance` @0.92, `get_contextual_guidance` @0.85 (5/5 MATCH).

## REVIEW rows — the router's answers as data (informational, unscored)

| phrase | category | router route @conf | rationale | source |
|---|---|---|---|---|
| when did I complete the onboarding project? | STATUS | `check_completion_status` @0.92 | User asks when past work was completed — completion-history  | probe-row-47 |

## Row detail (asserted rows)

| phrase | category | expected | router route @conf | verdict | note |
|---|---|---|---|---|---|
| I need to setup my projects | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.92 | MATCH |  |
| I want to set up my projects | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| I'd like to set up my portfolio | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.92 | MATCH |  |
| When did I complete the API migration? | STATUS | action:check_completion_status | `check_completion_status` @0.95 | MATCH |  |
| When did I complete the migration? | STATUS | action:check_completion_status | `check_completion_status` @0.95 | MATCH |  |
| When did we launch the beta? | STATUS | action:check_completion_status | `check_completion_status` @0.72 | MATCH |  |
