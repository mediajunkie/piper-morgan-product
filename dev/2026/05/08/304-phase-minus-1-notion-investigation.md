# Phase -1 Investigation: Notion Integration Doneness vs. Conversational-Floor Architecture

**Issue**: #1059 (Phase -1 spike gating #304 sub-epic placement)
**Auditor**: Lead Developer
**Date**: 2026-05-08 ~07:10
**Method**: Code inventory + import-graph trace + test collection + dependency check + config-surface read

---

## TL;DR

**Verdict: "close to ready" — not "needs rework", not "superseded".**

The Notion integration is **wired, dependency-resolved, and ~94% tested-passing**. The 1,500+ LOC of code is not dead-archaeology; it's live-but-dormant — gated by feature flag and lacking a provisioned API token in the environment. Activation requires small PM-driven setup (token + flag) plus one stale-test fix and a manual smoke round. Estimated 4-8 hours of actual work, mostly contingent on real-account smoke.

**Sub-epic placement recommendation**: small follow-up issue under **M2f or M2-discovered** (not a multi-week M3/M5 project). The "post-MVP" framing in some inherited notes is incorrect — Notion is in alpha scope per PM ratification, and the work to activate is bounded.

---

## Per-question findings

### Q1: Architecture alignment — does the Notion code still fit the post-floor architecture?

**YES — fits the action-handler path, not the floor-context path.**

The post-floor architecture (#1004 + downstream) didn't replace the action-handler routing surface; it added the conversational floor as a parallel path for ambient/identity/temporal/status queries. Notion's integration sits squarely in the **action-handler path**:

- `services/intent/intent_service.py:2111-2116` — `intent.action ∈ {"search_documents", "find_documents", "search_notion", "update_document"}` routes to `_handle_search_documents_notion` / `_handle_update_document_notion`
- These handlers call `NotionIntegrationRouter.search_notion(...)` (line 2367) which dispatches to either `NotionMCPAdapter` (spatial) or legacy notion plugin based on `FeatureFlags.should_use_spatial_notion()`

**Notion is NOT in `services/intent_service/context_assembler.py`** — confirmed by grep. That's correct. Notion belongs to the action layer, not the floor's context-gathering layer. Different surface, different architectural concern. Both can coexist; they do.

The "78% complete" framing in the original #304 (Aug 2025) was about the integration's *internal* completeness against its own design, not about post-floor compatibility. The post-floor change didn't move Notion's surface — it added a new, orthogonal surface (the floor) for different query categories.

### Q2: Test coverage — what tests exist? Do they pass?

**17 tests collected; 16 pass, 1 fails. The 1 failure is test drift, not code rot.**

Test files:
- `tests/features/test_notion_integration.py`
- `tests/features/test_notion_spatial_integration.py`
- Plus config tests at `tests/config/test_notion_validation.py`, `test_notion_user_config.py`
- Plus integration tests at `tests/integration/test_notion_configuration_integration.py`, `test_notion_config_loading.py`

Sample failure:
```
tests/features/test_notion_spatial_integration.py:47: in test_notion_api_configuration
    result = await adapter.configure_notion_api("test_token")
E   AttributeError: 'NotionMCPAdapter' object has no attribute 'configure_notion_api'
```

This is **stale test API** — the test calls a method that doesn't exist on the adapter. Either the method was renamed/removed during refactoring or the test was written ahead of the code and never reconciled. Same shape as #1054 (morning_standup logger init) and #1056 (KG edge type case mismatch) we fixed Tuesday. Easy fix during activation.

### Q3: Dependency status — does the import graph resolve?

**YES — all imports resolve at module-load time.**

- `notion-client==2.5.0` is in `requirements.txt`; `from notion_client import Client` works in venv
- `services/integrations/spatial_adapter.BaseSpatialAdapter` (parent class) exists
- `services/integrations/mcp/token_counter.TokenCounter` (used in `NotionMCPAdapter.__init__`) exists
- `services/integrations/notion/{config_service,notion_integration_router,notion_plugin,...}` — all present
- `config.notion_config.NotionConfig` — present

No missing modules; no `ImportError` on collection.

### Q4: Configuration surface — what auth/config does activation require?

**Configuration scaffolding is in place; activation needs only a real Notion integration token.**

Existing config surface:
- `config/notion_config.py:NotionConfig` — env-driven loader (`NOTION_API_KEY`, `NOTION_WORKSPACE_ID`)
- `services/integrations/notion/config_service.py:NotionConfigService` — user-scoped config cache (allows per-user tokens)
- `services/integrations/notion/README.md` — documents the auth model (`secret_*` or `ntn_*` integration tokens)
- `FeatureFlags.should_use_spatial_notion()` — runtime toggle between MCP-spatial adapter and legacy plugin

What activation needs:
1. PM creates a Notion integration in the Notion admin UI; copies the token
2. Token added to environment (`.env` or keychain) as `NOTION_API_KEY`
3. Optional: set `NOTION_WORKSPACE_ID` if needing multi-workspace disambiguation
4. Feature flag default reviewed — currently `should_use_spatial_notion()` exists; need to confirm its default is sensible for alpha (likely True for the spatial path)

No new config code needed.

### Q5: Integration points — what production code paths call Notion? Are they consistent with current conventions?

**Substantial wiring; consistent with conventions.**

Production callers (verified via grep):

| File | Role |
|---|---|
| `services/intent/intent_service.py` | Action-handler routing (search_documents / update_document) |
| `services/features/notion_queries.py` | Feature-level query wrapper using `NotionDomainService` |
| `services/domain/notion_domain_service.py` | Domain-service abstraction over the adapter |
| `services/integrations/notion/notion_integration_router.py` | Routing layer (MCP-spatial vs. legacy) |
| `services/integrations/notion/notion_plugin.py` | Plugin registration |
| `services/integrations/mcp/notion_adapter.py` | MCP-spatial adapter (the 867-LOC file the original #304 named) |
| `services/intelligence/spatial/notion_spatial.py` | 8-dimensional spatial intelligence layer (637 LOC) |
| `services/publishing/publisher.py` | Uses Notion as publishing surface |
| `services/integrations/slack/slack_integration_router.py` | Cross-references Notion config |
| `services/intelligence/spatial/gitbook_spatial.py` | Sibling spatial layer; references Notion patterns |
| `services/infrastructure/config/feature_flags.py` | Runtime toggle |

This is **wired** — not stranded code. The router pattern (`NotionIntegrationRouter` with feature-flag dispatch) matches the same shape used by Slack (`slack_integration_router.py`). The intent-handler path uses the same `_handle_X_via_notion` shape used elsewhere in `intent_service.py`. Conventions are respected.

---

## Activation work estimate (the real #304 scope)

If PM authorizes activation, the work is:

| Task | Estimate |
|---|---|
| Fix `test_notion_api_configuration` test drift (rename/remove `configure_notion_api` reference) | 15 min |
| Audit other 17 tests for similar drift; fix as needed | 30 min |
| PM provisions Notion integration token + adds to env | PM, ~15 min |
| Verify `FeatureFlags.should_use_spatial_notion()` default | 5 min |
| Manual smoke: `search_documents` query against live Notion workspace | 30-60 min |
| Manual smoke: `update_document` query against live Notion workspace | 30-60 min |
| Bugfix budget if smoke surfaces issues | 1-2 hours (contingent) |
| Document activation in `services/integrations/notion/README.md` | 15 min |

**Total**: ~4-8 hours of work, mostly small chunks, primarily contingent on whether live-workspace smoke surfaces real bugs vs. clean.

---

## Sub-epic placement recommendation

**M2f (post-floor coverage)** OR **M2-discovered (testing/scoring infra)** — small follow-up shape.

Rationale:
- The work is bounded (4-8 hours)
- Most of it is PM-driven (token provisioning + smoke against real workspace)
- The architectural shape is settled (action-handler path, feature-flag gated)
- It's NOT a multi-week M3 (artifact persistence) or M5 (polish + distro) effort

**NOT recommended**: M3 or M5 — those imply scope this work doesn't need.

PA + PM should ratify the placement. My read is M2f because the activation closes a known gap rather than discovers new infra; but M2-discovered is also defensible if the framing is "operational follow-up to the May 6 Topic 7 walk."

---

## What this investigation did NOT do

- Did not run the workflow against a live Notion workspace (no token in env)
- Did not modify `notion_adapter.py` or `notion_spatial.py`
- Did not fix the 1 failing test (out of scope per #1059 — that's part of activation work)
- Did not propose specific changes to `should_use_spatial_notion()` default
- Did not test `update_document` path; only inventoried it

---

## Recommendation back to PA / PM

1. Update #304 body with **Phase -1 outcome: "close to ready"** + this memo's path
2. PA + PM ratify sub-epic placement (recommend M2f or M2-discovered)
3. After placement: PM provisions the Notion integration token; Lead Dev (or subagent) executes the activation work — it's small enough for a single focused session

Memo ready for distribution to PA inbox + CC PM.

— Lead Developer, 2026-05-08
