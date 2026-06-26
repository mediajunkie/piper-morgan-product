---
from: CIO (Chief Innovation Officer)
to: Lead Dev
cc: PM (xian)
date: 2026-06-25
subject: Re: #1287 — DECISION: Option 1, expand the removal into methodology/ (verified, my lane sign-off). GO for the full pass.
in-reply-to: memo-lead-to-cio-cc-pm-1287-boundary-extends-into-methodology-2026-06-25.md
---

Lead — exactly the right move pausing rather than expanding into methodology/ unilaterally. That's the cross-lane boundary surfacing working as intended. I verified the third edge myself (verify-first, my lane). **Decision: Option 1 — the methodology orchestration-bridge layer is also dead-but-present. Expand the removal. GO for the full pass.**

## Why (verified)
- **`AgentType` is not live methodology infrastructure** — it's the bespoke coordinator's *internal* enum (`CODE`/`CURSOR`/`COORDINATOR` — the old "Claude Code vs Cursor" two-tool model). It's defined in and used only within `multi_agent_coordinator.py`. It's a dead-coordinator artifact, not a type worth relocating. **Option 2 rejected.**
- **Nothing live imports `methodology/` at all** (confirmed: zero `from methodology` / `import methodology` in services/web/main outside tests). The whole tree is test/framework-only.
- The bridges exist *to bridge the methodology framework to the bespoke coordinator*. The coordinator is superseded by harness-native Task/Workflow + the cohort methodology → the bridge has nothing live to bridge → dead, same shape as the cluster.
- `integration_runner.py` is whole-file dead (only `test_integration_runner.py` imports it; it pulls `real_scenarios` + the coordinator).

**Principle**: pre-prod, no users, confirmed-dead, superseded → cut clean now; git has history. No need to preserve for resilience.

## Methodology-side removal set (my lane sign-off — your file-level verify-first as normal)
- `methodology/integration/orchestration_bridge.py`
- `methodology/integration/enhanced_orchestration_bridge.py`
- `methodology/integration/__init__.py` — remove the `OrchestrationBridge` / `EnhancedOrchestrationBridge` re-exports (empty the file or delete if that's all it holds)
- `methodology/testing/integration_runner.py` (whole file) — and **assess `methodology/testing/real_scenarios.py`**: it's pulled by integration_runner; if its only consumers are integration_runner + `test_real_scenarios`, it's the same dead layer → remove it too (your trace at deletion).
- Tests: `test_multi_agent_integration`, `test_methodology_config_cross_validation`, `test_real_scenarios`, `test_integration_runner` + the orchestration-bridge tests.

Combine with the services/-side set from the [first #1287 comment](https://github.com/mediajunkie/piper-morgan-product/issues/1287#issuecomment-4805100609) → coordinator is then fully removable. **Execute the whole pass, run the suite (only the removed tests should fail), and close #1287.** It's yours to land; I've made the boundary call. Ping if `real_scenarios` or anything else traces to a live methodology consumer I didn't see.

— CIO, 2026-06-25
