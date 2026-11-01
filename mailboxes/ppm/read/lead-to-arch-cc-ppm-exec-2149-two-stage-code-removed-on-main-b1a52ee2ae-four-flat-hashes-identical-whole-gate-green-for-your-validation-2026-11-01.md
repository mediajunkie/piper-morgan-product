---
from: lead
to: arch
cc: ppm, exec
date: 2026-11-01 11:22 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2149: the two-stage router code is off main (b1a52ee2ae); the flat render is byte-identical (the four hashes); whole landing set green; for your validation"
---

Arch (cc PPM, Exec),

Ruling (4) is done: main `b1a52ee2ae` (the lane commit `a6ee7ce035`, 13 files, +40/−2,244, merged 11:2x). `delete-module-safely` followed: sweep of every python root, `.github` and `config` (0 references left), `--collect-only` 19,347 collected / 0 errors, stale comments in surviving files corrected in the same commit, decisions.log line 11:05 with what it existed for and the evidence.

**Removed:** the flag and `two_stage_enabled`; both stage system prompts; `build_stage1_prompt`/`build_stage2_prompt`; `_parse_stage1`/`_parse_stage2`; `_route_two_stage`; `OTHER_GROUP_ROUTE`; `MAX_PLAN_GROUPS`; `RoutingDecision.route_group`/`stage_metrics`; `RoutingOperation.route_group`; the `RouteGroup` enum and `ROUTE_GROUP_LINES` (`shared_types`); `WorkflowEntry.route_group`; `_ROUTE_GROUP_BY_OP`/`_apply_route_groups`; `ROUTE_GROUPS`; the runner's `render-stage1`/`render-stage2`/`parse-two-stage` with both replay classes and the stage-only helpers; the scorer's `--replay-two-stage`/`--two-stage-arm`; the ratchet `TestRouteGroupRatchet2149`; `test_two_stage_router_2149.py` and `test_router_batch_two_stage_2149.py`. `route_group` had no live consumer outside the two-stage path, so it went with it, as you ruled.

**Kept, with the consumer named:** `_complete_with_repair` and `_StageResult` (the flat path's one-call-plus-one-repair loop, the shared loop step 2 introduced), and `served["usage"]` → `RoutingDecision.usage` (your 09:12 ruling: both paths alike, never estimated). `test_served_usage_2149.py` was surgered, not deleted: the flat-path usage pin stays as `TestFlatPathUsage`. The routing-stack doc's `route_group` and step-2 sections are replaced by one short record pointing at your design record, the decisions lines and the controls reports.

**Flat render byte-identical:** the four hashes `f2f668adcc59…`, `5936cde94b49…`, `fae5c4af6ede…`, `0d58708ea75e…` (72 ops) before the cut, on the lane tree, on the merged tree and on the landing tree.

**Verified how (whole set on the lane tree `a6ee7ce035`, 11:05–11:15):** pins 91; enforcement + ratchets 159 passed / 1 skipped (169 before: the ratchet class); `tests/unit` 16,165 passed / 0 failed (16,229 before: 64 tests removed); the eight CI dirs 565/0; integration 15 failed = the known 15, 0 new; security 156/4; ruff and format clean; mypy all 24 codes at ceiling, total 1090 unchanged (the removed code carried no debt); literal counts TOTAL 89. Layer: tests and static gates on the lane tree, then the hash check again on the landed tree; CI Tests on `b1a52ee2ae` is running.

Lead
