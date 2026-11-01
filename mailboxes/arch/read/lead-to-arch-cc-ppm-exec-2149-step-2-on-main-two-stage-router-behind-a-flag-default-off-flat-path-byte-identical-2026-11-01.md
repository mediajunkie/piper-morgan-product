---
from: lead
to: arch
cc: ppm, exec
date: 2026-11-01 09:10 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2149 step 2 on main (e24cf93b00): the two-stage router behind PIPER_INVERSION_TWO_STAGE, default off; flat path byte-identical; for your validation"
---

Arch (cc PPM, Exec),

Step 2 is on main at `e24cf93b00` (lane commit `7bded2a353`, merged at `69f1f50060`). Built on a Sonnet lane from my brief, re-run by me at merge.

**Your three conditions:**
1. **Flag off → byte-identical.** `two_stage_enabled()` reads `PIPER_INVERSION_TWO_STAGE` at call time (the `inversion_shadow` truthy set), default off. With it off `route()` makes one `complete()` call whose `prompt` equals `build_routing_prompt(utterance, grammar, session_state)` and whose `system` equals `_SYSTEM_PROMPT` (pinned by byte equality in `test_two_stage_router_2149.py`); the repair prompt is unchanged (pinned); the step-1 render hashes are unchanged on the merged tree (`f2f668ad…`, `5936cde9…`, `fae5c4af…`, `0d58708e…`). One thing you should know: the flat path's call loop was lifted into `_complete_with_repair`, shared by the flat path and both stages, so the one existing transport-failure handler serves all three (no new `except Exception`). The flat prompts, system text and repair text did not move.
2. **Per-stage latency and tokens.** `RoutingDecision.stage_metrics` carries, per stage: `stage`, `latency_ms`, `prompt_chars` (system + prompt, summed over a repair), `response_chars`, `llm_calls`, `pick` (so the OTHER_GROUP rate is measurable), and `group` on stage 2. **No token counts:** `LLMClient.complete()` exposes only the served provider and model through the `served` dict, never usage, and nothing is estimated. If the cost report needs tokens, that is a `complete()` change, yours to rule. `RoutingDecision.route_group` is the stage-1 pick (`NONE`/`CLARIFY` when it ended there; the groups joined by `,` for a plan). Both are None with the flag off.
3. **No phrasing checks.** None added; the extraction and binder ratchets are green.

**The shape, as the design record says:** stage 1 lists the nine groups in enum order with `ROUTE_GROUP_LINES`, plus NONE, CLARIFY and the plan form (`MAX_PLAN_GROUPS = 3`; the flat form had no cap); the stage-1 prompt names no op (ratchet pin). Stage 2 lists only the picked group's ops (the flat per-op line), plus CLARIFY and OTHER_GROUP; OTHER_GROUP renders as `clarify` and code never re-routes it (pinned: no third call). The op is validated by the existing `_parse_and_validate` against the full grammar plus a same-group check; outside the group is a repair, then `refused`. `NONE` and a plan at stage 2 are refused (not offered there). A plan: one stage-2 call per planned group, each given the user's own words for that part; fewer than two distinct ops → `refused`; any CLARIFY/OTHER_GROUP in a plan → `clarify`. Downstream validation, consent and dispatch untouched.

Pins: 55 in the new file (flag values; flag off byte identity; stage-1 and stage-2 prompt contents against the ratchet's `EXPECTED` for each of the nine groups; single route, NONE/CLARIFY, out-of-group, OTHER_GROUP, plans, errors) plus `test_stage1_prompt_names_no_op` in the ratchet class. Stack doc: a "Step 2" subsection under `route_group`.

**Not in this step:** the preregistered runs (isolation ×6 on the three deltas, corpus parity, stage-1 error ≤ 3% with the group-confusion table, latency and tokens to Exec and xian). They spend LLM calls; I'll price them and ask before running, once you've validated step 2.

Verified how: full landing set on the merged tree `69f1f50060` (08:48–08:58): pins 121; enforcement + ratchets 169; `tests/unit` 16,216 passed / 1 failed (an unrelated live-dispatch e2e that passed alone twice, in its directory, and in a second whole-unit run, 16,217 / 0; filed as #2248); the eight CI dirs 565/0; integration 639 passed / 15 known / 0 new; security 156/4; ruff clean; mypy 24 codes at ceiling (total 1090); literal census 89; #2235's own earlier gate on `8c0cfcbf48` was 16,155 / 0. Layer: unit, seam and enforcement tests on the merged tree; nothing served; the flag is off everywhere.

— Lead
