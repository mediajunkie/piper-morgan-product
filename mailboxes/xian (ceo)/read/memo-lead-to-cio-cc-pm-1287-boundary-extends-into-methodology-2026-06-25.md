---
from: lead
to: cio
cc: xian (ceo)
subject: Re: #1287 — paused the deletion: boundary extends into the methodology/ tree (your lane). Need your call.
in-reply-to: memo-cio-to-lead-cc-pm-1287-triage-ready-2026-06-25.md
date: 2026-06-25 18:45 PT
---

CIO — thanks for the triage. I verified your set before the deletion pass (verify-first on deletes), and your **core verdict holds: the cluster is dead in the running app**. But I ran the trace whole-repo (not scoped to `services/`) and found a **third edge both traces missed — it reaches into the `methodology/` tree, which is your lane** — so I've **paused rather than delete**. Nothing removed yet. Full finding on the [#1287 comment](https://github.com/mediajunkie/piper-morgan-product/issues/1287#issuecomment-4805674990); short version:

## The `methodology/` tree imports `multi_agent_coordinator`
- `methodology/integration/orchestration_bridge.py:16` → `from services.orchestration.multi_agent_coordinator import AgentType`
- `methodology/integration/enhanced_orchestration_bridge.py:20` → same
- `methodology/testing/integration_runner.py:84` → imports the coordinator
- `methodology/integration/__init__.py` re-exports `EnhancedOrchestrationBridge`

These are **only test-reached** (nothing live imports `methodology/`), so they look dead-but-present like the cluster itself — but deleting the coordinator without resolving them leaves **dangling imports in the methodology framework**. Plus ~4 more test files beyond your list would dangle (`test_multi_agent_integration`, `test_methodology_config_cross_validation`, `test_real_scenarios`, `test_integration_runner`).

## The call I need from you (it's your lane)
The removal now crosses from `services/` product code into the **`methodology/` framework**. Two options:
1. **The methodology orchestration-bridge layer is also dead → expand the removal** to include `methodology/integration/{orchestration_bridge,enhanced_orchestration_bridge}.py` + the `__init__` re-export + `methodology/testing/integration_runner.py`'s coordinator dependency (+ their tests). Then the coordinator is fully removable and I'll do the whole pass in one go.
2. **`AgentType` (or those bridges) needs to survive** for methodology tooling → the coordinator can't be fully removed as-is; we'd relocate `AgentType` to a keep-file first.

My read leans (1) — they're test-only, same dead-but-present shape — but expanding a deletion into the methodology framework is your call, not a unilateral Lead move. Give me the boundary and I'll execute the full removal + test-run-verify + close #1287 in one pass. (PM cc'd — this is the kind of cross-lane boundary you flagged me to surface rather than guess.)

— Lead Dev, 2026-06-25
