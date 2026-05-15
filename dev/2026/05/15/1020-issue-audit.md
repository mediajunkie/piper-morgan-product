# #1020 ARCH-DESIGN — Phase 0 audit

**Issue**: [#1020](https://github.com/mediajunkie/piper-morgan-product/issues/1020) — Per-task LLM output validation in OrchestrationEngine workflows
**Priority**: `architecture`, `technical-debt`, `M2g` (no explicit priority label)
**Source**: Architect's Apr 27 batch-3 codebase review (Finding IV)
**Date**: 2026-05-15

---

## Pattern-067 verdict: POSITIVE — material misalignment

The body's framing — "add schema validation between steps" — is directionally correct as a future goal, but the audit found **the engine itself has latent bugs that make most of the body's specific task-table claims wrong**. The "no validation between steps" concern is real but moot for the listed task chain (`ANALYZE_REQUEST → EXTRACT_REQUIREMENTS → IDENTIFY_DEPENDENCIES → GENERATE_DOCUMENTATION → EXECUTE_GITHUB_ACTION`) because that chain **cannot complete in the current engine**.

## Latent bugs found in `services/orchestration/engine.py`

### Bug 1: `TaskType.GENERATE_DOCUMENTATION` doesn't exist

`engine.py:380`:
```python
elif task.type == TaskType.GENERATE_DOCUMENTATION:
    output_data = await self._generate_documentation_task(task, workflow)
```

`TaskType` enum (`services/shared_types.py:59-95`) has:
- `GENERATE_DOCUMENT` (line 71) — without the "ATION" suffix
- `GENERATE_GITHUB_ISSUE_CONTENT` (line 76)

No `GENERATE_DOCUMENTATION`. Python evaluates `TaskType.GENERATE_DOCUMENTATION` at the moment the elif is reached → `AttributeError`.

### Bug 2: `TaskType.EXECUTE_GITHUB_ACTION` doesn't exist

`engine.py:382`:
```python
elif task.type == TaskType.EXECUTE_GITHUB_ACTION:
    output_data = await self._execute_github_action_task(task, workflow)
```

`TaskType` has `GITHUB_CREATE_ISSUE` and `ANALYZE_GITHUB_ISSUE` but no `EXECUTE_GITHUB_ACTION`. Same AttributeError shape.

### Bug 3: `llm_client.generate_response()` doesn't exist

`engine.py:463` (inside `_extract_requirements_task`):
```python
response = await self.llm_client.generate_response(prompt)
```

And `engine.py:515` (inside `_generate_documentation_task`):
```python
response = await self.llm_client.generate_response(prompt)
```

`grep -n "def generate_response" services/llm/clients.py` → **zero matches**. `LLMClient` has `complete(task_type, prompt, ...)` but not `generate_response()`. Any branch reaching either method call would AttributeError.

### Bug 4: Dispatcher coverage gap

`engine._execute_task` (lines 367-414) dispatches 5 task types:
- ANALYZE_REQUEST ✅ (real, handler exists)
- EXTRACT_REQUIREMENTS ✅ (real, handler exists — but handler is broken per Bug 3)
- IDENTIFY_DEPENDENCIES ✅ (real, handler exists, no LLM call)
- GENERATE_DOCUMENTATION ❌ (Bug 1)
- EXECUTE_GITHUB_ACTION ❌ (Bug 2)
- ELSE → `raise ValueError(f"Unknown task type: {task.type}")`

`workflow_factory.py` creates these task types in production workflows:
- EXTRACT_WORK_ITEM
- GENERATE_GITHUB_ISSUE_CONTENT
- GITHUB_CREATE_ISSUE
- ANALYZE_GITHUB_ISSUE
- ANALYZE_FILE
- SUMMARIZE
- LIST_PROJECTS
- CREATE_WORK_ITEM
- ANALYZE_REQUEST

**Only ANALYZE_REQUEST overlaps between what the factory creates and what the dispatcher handles.** Every other production task type either crashes at the 4th elif (AttributeError on Bug 1's RHS) or falls through to the ValueError "Unknown task type" branch.

## Why this isn't visible today

Per the body's own note: *"Why this isn't actively breaking: workflow exercise frequency is currently low. The risk is latent until volume picks up."*

The engine IS instantiated in production paths:
- `services/integrations/slack/response_handler.py:149` (OrchestrationEngine())
- `services/integrations/slack/webhook_router.py:78` (OrchestrationEngine())
- `services/intent/intent_service.py:138` (Optional[OrchestrationEngine])
- `services/integrations/slack/simple_response_handler.py:292` calls `orchestration_engine.execute_workflow(workflow.id)`
- `services/integrations/slack/response_handler.py:564` calls `orchestration_engine.execute_workflow(workflow.id)`

So the engine IS reachable through the Slack integration's workflow execution path. The latent bugs would manifest the first time a Slack-triggered workflow tries to run any task type other than ANALYZE_REQUEST.

## What the body asked for (still valid, but premature)

The validation framework the body describes — Pydantic output schemas per LLM-driven task, validation helper in `services/orchestration/validation.py`, failure-handling pattern, audit envelope — is a real and reasonable Phase 1 design. **But it can't be the right next step until the engine actually dispatches tasks correctly.** Adding validation to broken handlers is putting a fence around a hole.

## Three paths

### Path A — Fix latent bugs first, then validation (sequential)

Pre-work: fix Bugs 1–4 (rename/add TaskType values, replace `generate_response` with `complete`, fix dispatcher coverage). Estimate ~1-2 days.
Then proceed with the body's original Phase 1 design + Phase 2 implementation + Phase 3 verification (~4-5 days as filed).

**Total**: ~5-7 days, multi-session.
**Pro**: keeps #1020 as one issue with one scope.
**Con**: confuses two distinct concerns into one body of work; if the engine is partly dead code we should know that before validating; if it's needed but broken we should fix it as its own scope.

### Path B — Split #1020 into latent-bugs fix + validation framework

Close-out #1020 with reframe note. File two replacement issues:
- **#NEW-1 ORCH-ENGINE-LATENT-BUGS**: fix Bugs 1–4 above; tests covering each previously-broken branch; restore dispatcher coverage to match `workflow_factory` task types
- **#NEW-2 ORCH-TASK-OUTPUT-VALIDATION**: the original body's Phase 1-3 plan, post the engine fix

**Total**: same calendar time but two clean scopes.
**Pro**: each issue has a focused, testable scope; matches yesterday's #1010 split-into-#1089 pattern; #NEW-2's design memo will be cleaner once the engine is known-working.
**Con**: extra issue churn.

### Path C — Reframe as engine-cleanup, defer validation

Recognize that #1020's "no validation between steps" framing was downstream of an engine that isn't fully wired. Take this as evidence that orchestration is currently a partial-dead-code surface and clean it up:
- Delete the 2 broken elif branches (Bug 1 + Bug 2 dispatch paths)
- Delete the 2 handler methods they reference (`_generate_documentation_task`, `_execute_github_action_task`) — they call `generate_response` which doesn't exist anyway
- Fix `_extract_requirements_task` to use `complete()` correctly OR remove it if not exercised
- Audit `workflow_factory` task types against engine dispatcher coverage; align both
- Defer the validation framework to post-1.0 when workflow exercise frequency justifies it

**Total**: ~1 day for the cleanup; validation deferred.
**Pro**: matches the M2f Group B (#935/#936) dead-code-deletion shape from May 9; lowest-risk near-term move.
**Con**: defers the validation Architect originally specified — but it was P3, not urgent.

## Recommendation: Path B (split)

The latent bugs are real and need fixing (engine is one Slack-workflow-firing away from a production AttributeError). The validation framework is also real and worth shipping. They're distinct enough scopes that one issue trying to hold both will have messy ACs.

**Path B preserves Architect's original validation intent** (which I read as load-bearing for the LLM-touch boundary principle epic #1016) while not putting validation around a broken dispatcher.

Path C is the M2f-pattern argument (M2g-pattern actually — yesterday's #1010 + #1019 cleanups did exactly this). It's the right call if PM thinks the engine is essentially abandoned. My read says it's not abandoned (Slack handlers reference it), it's just under-exercised.

Path A is the worst of both worlds — bigger PR with two distinct concerns muddled together.

## Audit-cascade Phase 0 self-check

| Template requirement | Status |
|---|---|
| Issue number referenced | ✅ #1020 |
| Pattern-067 check | ✅ POSITIVE — 4 latent bugs documented |
| Body-vs-reality | ✅ all 5 task table claims verified; 2 broken at the TaskType layer, 2 broken at the LLM method layer (depending on counting) |
| Existing infra mapped | ✅ engine.py / validation.py / workflow_factory.py / llm/clients.py / slack handlers |
| Scope questions | ✅ A/B/C with reframe-cadence framing |
| Risk assessment | ✅ Slack-workflow-firing scenario for the AttributeError; Architect's original validation intent preservation |
| Recommended path | ✅ B (split) with rationale; alternative paths noted |

---

## STOP — awaiting PM disposition on A/B/C

The Phase 0 finding is consequential enough that proceeding to a Phase 1 design memo before PM weighs in would be premature. The choice between A/B/C is product-shaped (how do we want to scope the orchestration cleanup vs. the validation framework).

Recommend Path B unless PM signals the engine is essentially abandoned (then Path C) or that one-issue-one-scope is preferred regardless (then Path A).

— Lead Developer, 2026-05-15
