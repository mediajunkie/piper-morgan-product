# #1094 — Phase 1 Design Memo

**Issue**: [#1094](https://github.com/mediajunkie/piper-morgan-product/issues/1094) — ORCH-DISPATCHER-COVERAGE-DISPOSITION: 8 workflow_factory task types have no engine handler (architectural call)
**Date**: 2026-05-15
**Phase**: 1 — design (α / β / γ disposition with PM ratification)

---

## Major Phase 0 finding: the engine is already abandoned in the main path

The α/β/γ framing assumed the OrchestrationEngine is in active use and the dispatcher gap is a coverage problem. Phase 0 investigation found the precedent for engine-abandonment is **already established and documented**.

`services/intent/intent_service.py:1136-1143`:
```python
# Issue #883: Lazy workflow creation — workflows are no longer pre-created
# for every intent. Instead, handlers that need async work can create
# a workflow on demand via self._create_workflow_with_timeout(intent).
# Currently no handlers use async workflows, so this is a no-op.
# The workflow parameter is set to None; handlers that used workflow_id
# now receive None and pass it through harmlessly.
workflow = None
workflow_id = None  # For fallback error path
```

[Issue #883 (closed)](https://github.com/mediajunkie/piper-morgan-product/issues/883) shipped the lazy-workflow-creation refactor with explicit reframe: "27 of 28 handlers do NOT start async work" and "frontend polls for status on work that doesn't exist." The main HTTP intent path has been engine-free since #883 shipped.

### Who still uses the engine

- **`services/integrations/slack/response_handler.py:558,564`** — `SlackResponseHandler.handle_slack_message` still calls `engine.create_workflow_from_intent` + `engine.execute_workflow`
- **`services/integrations/slack/simple_response_handler.py:288,292`** — `SimpleSlackResponseHandler` same pattern
- **MCP path**: `standup_workflow_skill.py:60` instantiates `SlackDomainService` which constructs `SlackResponseHandler` which uses the engine

Slack tests (`services/integrations/slack/tests/test_workflow_pipeline_integration.py:70`):
```python
engine.execute_workflow = AsyncMock(side_effect=execute_workflow)
```

**The Slack tests mock the engine entirely.** Real engine behavior is never exercised in CI. Combined with the dispatcher's coverage gap (8 of 9 production task types fail through `raise ValueError("Unknown task type")`), this means **Slack workflows have been silently failing in production for any task type other than ANALYZE_REQUEST** — without test coverage to surface the failure.

### Workflow factory's WorkflowType → task type map

From `services/orchestration/workflow_factory.py:294-433`:

| WorkflowType | Task types created | Engine handles? | Production behavior today |
|---|---|---|---|
| CREATE_TICKET | EXTRACT_WORK_ITEM, GENERATE_GITHUB_ISSUE_CONTENT, GITHUB_CREATE_ISSUE | ❌ all 3 | Fails on first task |
| REVIEW_ITEM | ANALYZE_GITHUB_ISSUE | ❌ | Fails immediately |
| ANALYZE_FILE | ANALYZE_FILE | ❌ | Fails immediately |
| GENERATE_REPORT | ANALYZE_FILE or SUMMARIZE | ❌ | Fails immediately |
| LIST_PROJECTS | LIST_PROJECTS | ❌ | Fails immediately |
| CREATE_FEATURE | CREATE_WORK_ITEM | ❌ | Fails immediately |
| CREATE_TASK | CREATE_WORK_ITEM | ❌ | Fails immediately |
| PLAN_STRATEGY | SUMMARIZE | ❌ | Fails immediately |
| ANALYZE_METRICS | ANALYZE_REQUEST | ✅ | Works |
| LEARN_PATTERN | ANALYZE_REQUEST | ✅ | Works |
| ANALYZE_FEEDBACK | ANALYZE_REQUEST | ✅ | Works |
| CONFIRM_PROJECT | ANALYZE_REQUEST | ✅ | Works |
| SELECT_PROJECT | ANALYZE_REQUEST | ✅ | Works |
| (default fallback) | ANALYZE_REQUEST | ✅ | Works |

**Six of fourteen WorkflowTypes route through ANALYZE_REQUEST** (the only working dispatcher branch) and succeed. **The other eight fail.** All eight failing WorkflowTypes are exactly the user-facing-feature types — issue creation, file analysis, project listing, etc.

The intent_service handles all of these via direct dispatch (not the engine) — that's why HTTP-path users don't notice. Slack-path users either don't trigger these WorkflowTypes often, do trigger them and silently get failed workflows, or the Slack handlers have alternate paths that bypass the engine for these cases.

## Three paths reconsidered with Phase 0 evidence

### Option α — Engine grows handlers for all 8 task types

Add `_extract_work_item_task`, `_generate_github_issue_content_task`, `_github_create_issue_task`, `_analyze_github_issue_task`, `_analyze_file_task`, `_summarize_task`, `_list_projects_task`, `_create_work_item_task` to the engine. Each thin-wraps existing domain services.

**Cost**: ~5-8 days. Each handler ~30-50 LOC of wiring + tests.

**Pro**: completes the engine's role as canonical dispatcher.
**Con**: contradicts the #883 precedent (which moved the main path AWAY from the engine). Most domain logic for these task types already lives elsewhere (e.g., GitHub create_issue → `github_integration_router.create_issue`); the handlers would mostly be thin wrappers. Adds a layer over services that already work. The engine becomes a registry-and-dispatcher whose registry duplicates information already in `intent_service`'s intent→handler routing.

### Option β — Engine remains thin; refactor Slack to direct dispatch

Recognize the precedent: intent_service already routes intent → handler without going through the engine. Refactor Slack handlers to follow the same pattern. Reduce the engine to ANALYZE_REQUEST-only (which intent_service uses for its analyses) or remove it entirely from Slack handlers.

**Cost**: ~2-3 days. Slack handlers reroute their `create_workflow_from_intent` + `execute_workflow` calls through direct handler invocation. Workflow persistence (status tracking) either drops or is preserved as a thin layer.

**Pro**: aligns Slack path with intent_service path. Eliminates the silent-failure surface (currently 8 of 14 WorkflowTypes fail silently in Slack). Removes the dispatcher coverage gap by removing the dispatcher rather than expanding it.
**Con**: requires Slack-handler refactoring; workflow-status tracking (DB persistence + status updates) needs explicit decision (drop or preserve).

### Option γ — Engine is partially abandoned; document + freeze + delete

Recognize the engine as architectural legacy from PM-039 (referenced in engine.py comments) that was effectively superseded by Issue #883's lazy-creation refactor. The fact that Slack tests mock the engine entirely confirms: real engine behavior isn't exercised in CI. Delete the engine + factory + Slack-engine-touch entirely; replace Slack handler engine calls with the same direct-dispatch pattern intent_service uses.

**Cost**: ~1-2 days for the cleanup; Slack handler refactoring to match intent_service is the bulk.

**Pro**: cleanest. Matches M2g cleanup pattern (#1010 boundary_enforcer placeholders deleted; #1019 adaptive_boundaries deleted; both were partially-abandoned scaffolding). Aligns Slack path completely with the intent_service pattern. Eliminates ~600 LOC of legacy infrastructure.
**Con**: workflow STATUS tracking (DB persistence, async-work-status-polling-surface) goes away entirely. If we want that surface back when async work surfaces, we rebuild it in a targeted way. (#883's framing — "create workflow when async work actually starts" — suggests we wouldn't actually need it back broadly.)

## Recommendation: γ (with one open scope question)

**Engine partially abandoned → delete it.**

Rationale:
1. **#883 already established the precedent.** The architectural decision to move main-path intent processing OUT of the engine is closed-and-shipped. γ extends that decision to the Slack-path holdout.
2. **Real engine behavior isn't tested in CI.** Slack tests mock the engine; real-engine-against-real-workflow has been silently broken for 8 of 14 WorkflowTypes since some unknown date (probably whenever the factory's task type set drifted from the dispatcher's coverage).
3. **The dispatcher coverage gap exists because the engine's role evaporated.** It's not a "we need to add more handlers" problem; it's a "the dispatcher is the wrong abstraction for what production actually does" problem.
4. **M2g sprint is fundamentally about arch-cleanup.** γ matches yesterday's #1010 + #1019 pattern: identify scaffolding that looked load-bearing but wasn't; delete it cleanly.
5. **Pattern-064 (Alive Scaffolding) at the system level.** The engine looks present and wired but does nothing useful for 8 of 14 WorkflowTypes; the apparent dispatcher is the false signal of safety. Deletion is the canonical remediation.

### Open scope question: workflow-status persistence

γ removes `Workflow` DB persistence and the workflow-status polling surface (currently used by frontend per #883 framing: "Frontend polls for status on work that doesn't exist"). Two sub-options:

- **γ-strict**: Delete the entire `Workflow` model + `WorkflowRepository` + status polling endpoints. Aligns with #883's explicit framing that nothing currently uses it.
- **γ-preserve**: Keep `Workflow` model + DB table (currently empty/orphaned) for FUTURE async-work tracking; delete only the engine + factory + dispatcher. When async work surfaces (Architect's e2e-suite proposal or BYOC long-running calls), we re-introduce orchestration shape in a targeted way.

My read: **γ-preserve** is the safer interim. Keeping the data model around at minimal cost lets us re-introduce orchestration when there's a real surface. γ-strict is the right end-state but doing it inside #1094 expands scope beyond the dispatcher question.

### α is wrong because

Adds handlers for task types whose domain logic already lives elsewhere — duplicates intent_service's routing without adding value. The engine would still be a partial duplicate of intent_service's dispatch model. Investing 5-8 days to complete the engine commits to a model that #883 already moved away from.

### β is acceptable but γ is cleaner

β preserves the engine as a thin shell. Real value: workflow-status tracking surface for ANALYZE_REQUEST workflows. But ANALYZE_REQUEST workflows aren't async (they complete synchronously inside `_analyze_request_task` via `intent_enricher.enrich`); the status tracking is theater. β delivers the engine-narrowing without the structural commitment to delete.

If the cohort wants a softer landing — keep the engine class but narrow its dispatcher to ANALYZE_REQUEST only — that's β. The eventual delete is still right; β just defers it.

## Suggested Phase 2 gameplan (conditional on γ-preserve)

If PM ratifies **γ-preserve**:

- **Phase 2.1** (~0.5 day): refactor `SlackResponseHandler.handle_slack_message` to use intent_service direct dispatch instead of `engine.create_workflow_from_intent` + `engine.execute_workflow`. Match `intent_service.py`'s pattern (lazy workflow, no engine touch unless async work fires).
- **Phase 2.2** (~0.5 day): refactor `SimpleSlackResponseHandler.process_message` same way.
- **Phase 2.3** (~0.5 day): delete `OrchestrationEngine` class + `services/orchestration/engine.py` body (preserve module imports for now via `__init__.py` shim if needed). Delete `WorkflowFactory` + `services/orchestration/workflow_factory.py`. Delete the 13 `Workflow` test files that mock the engine.
- **Phase 2.4** (~0.5 day): tests — verify Slack handler refactor doesn't regress; add tests for direct-dispatch behavior.
- **Phase 2.5** (~0.25 day): documentation — `BRIEFING-ESSENTIAL-ARCHITECT.md` tech-debt note (engine deletion); update PM-039 references if any are load-bearing.
- **Phase 2.6** (optional, deferred): γ-strict — delete `Workflow` model + `WorkflowRepository` + polling endpoints. Defer until an async-work-needing handler emerges.

**Phase 2 total**: ~2-2.5 days for γ-preserve. Down from Architect's β estimate (2-3 days) because the deletion is mechanical-cleanup-shape, not refactor-shape.

If PM ratifies **β** instead: keep the engine class + factory but narrow dispatcher to ANALYZE_REQUEST-only; add a `raise NotImplementedError(f"Task type {type} not supported in current engine surface; route through intent_service direct dispatch")` for the 8 unhandled types. ~1 day total. Even cleaner near-term; defers the structural delete.

## Risks

1. **Workflow-status polling surface dependencies**: if any frontend feature relies on workflow status polling for non-engine work (unlikely per #883), γ breaks it. Mitigation: grep for `/api/v1/workflows/{id}` consumers before deletion.
2. **MCP standup_workflow_skill dependency**: uses SlackDomainService which uses SlackResponseHandler. The MCP skill expects a certain return shape from `handle_slack_message`. Mitigation: preserve return-shape contract during Slack refactor; tests cover the integration.
3. **Issue #883 was M1-era; world may have changed**: technically possible that new async-work needs have emerged since. Mitigation: in Phase 2.1, audit current intent_service handlers to confirm none use async workflow shape.

## Audit-cascade Phase 0 self-check

| Template requirement | Status |
|---|---|
| Issue number referenced | ✅ #1094 |
| Pattern-067 check | ✅ POSITIVE — Phase 0 found #1094's own body framing assumes engine is active; reality (post-#883) is that engine is mostly abandoned. The dispatcher gap is symptomatic, not causal. |
| Body-vs-reality | ✅ all eight task types verified as unhandled; intent_service path confirmed engine-free; Slack path confirmed mocks-the-engine in tests |
| Existing infra mapped | ✅ engine.py / workflow_factory.py / Slack handlers / intent_service.py:1136 / Slack pipeline tests |
| Scope questions | ✅ α/β/γ with γ-preserve vs γ-strict sub-options |
| Risk assessment | ✅ workflow-status polling / MCP dependency / Issue #883 era-dependency |
| Recommended path | ✅ γ-preserve with γ-strict deferred |

---

## STOP — awaiting PM + Architect disposition

Most consequential: **α vs β vs γ**. My recommendation is γ-preserve with explicit deferral of γ-strict to a future async-work-needing-handler trigger.

The architectural question is fundamentally: do we keep maintaining the engine + factory + dispatcher trio when 80% of its surface fails silently in production today and the documented architectural direction (#883) already moved away from it?

Architect ratification needed on the architectural call; PM ratification on the scope (γ-preserve vs γ-strict vs β fallback).

— Lead Developer, 2026-05-15
