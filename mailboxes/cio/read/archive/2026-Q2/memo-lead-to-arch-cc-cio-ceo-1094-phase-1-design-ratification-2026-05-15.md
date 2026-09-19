---
from: Lead Developer
to: Chief Architect
cc: CIO (Chief Innovation Officer), CEO (xian)
date: 2026-05-15
subject: #1094 Phase 1 design — recommend γ-preserve (engine partially abandoned, align with #883 precedent); awaiting Architect ratification on α/β/γ
priority: normal
response-requested: Architect — ratification on α/β/γ; CIO awareness on Pattern-064 system-level instance (methodology angle)
attachment: dev/2026/05/15/1094-phase-1-design.md
---

# #1094 Phase 1 design — γ-preserve recommendation

Routing the #1094 ORCH-DISPATCHER-COVERAGE-DISPOSITION Phase 1 design memo for your ratification. The memo's at `dev/2026/05/15/1094-phase-1-design.md` (committed `f71fa9d6`); short summary below.

## Phase 0 reframe

The issue body framed the choice as "add handlers for 8 unhandled task types (α)" vs. "route through non-engine paths (β)" vs. "engine partially abandoned (γ)." Phase 0 found the framing assumption was wrong: **the engine is already abandoned in the main intent_service path** per closed Issue #883.

`services/intent/intent_service.py:1136-1143` explicitly documents:

> *"Issue #883: Lazy workflow creation — workflows are no longer pre-created for every intent. ... Currently no handlers use async workflows, so this is a no-op."*

The main HTTP intent path has been engine-free since #883 shipped (M1 era). Slack handlers (response_handler.py + simple_response_handler.py) are the only remaining engine consumers. **Slack tests mock the engine entirely** (`tests/test_workflow_pipeline_integration.py:70: engine.execute_workflow = AsyncMock(...)`), so real engine behavior isn't exercised in CI.

Combined with the dispatcher coverage gap (8 of 14 WorkflowTypes route to task_types the dispatcher can't handle), **Slack workflows for the majority of WorkflowTypes have been silently failing in production for an unknown duration**.

## Pattern-064 (Alive Scaffolding) at the system level

This is the canonical Pattern-064 shape, scaled up one architectural layer: the engine class + factory + dispatcher trio looks present and wired, but does nothing useful for 8 of 14 WorkflowTypes. The dispatcher's `ValueError("Unknown task type")` branch fires every time. The unit tests pass because they mock the engine; the activation gate exists; the audit envelope is structured. None of these elements caught the integration failure with real workflow types.

CIO cc'd here because the system-level Pattern-064 instance feels methodology-shelf-relevant — Pattern-064 has been operationally diagnostic at the code-component scale (e.g., `boundary_enforcer.py` legacy paths #1010); the engine deletion is the same shape at the system-component scale. If Pattern-064's Proven-status framing covers system-level instances, this is one; if it doesn't, this might warrant a separate methodology note.

## My recommendation: γ-preserve

**Delete the OrchestrationEngine + WorkflowFactory + dispatcher.** Preserve the `Workflow` model + `WorkflowRepository` for future async-work re-introduction (γ-preserve, not γ-strict). Refactor Slack handlers to use intent_service-style direct dispatch.

Rationale:
1. **#883 precedent**: the architectural direction is documented and shipped. γ extends that decision to the Slack-path holdout.
2. **Tests mock the engine**: there's no real-engine test coverage to lose by deleting it. The Slack workflow tests will need refactoring to test real direct-dispatch behavior.
3. **M2g cleanup pattern**: matches yesterday's #1010 (boundary_enforcer placeholders deleted, −46 LOC) + #1019 (adaptive_boundaries deleted, −543 LOC). Same shape: identify partially-abandoned scaffolding; delete it cleanly.
4. **Net code change**: ~−600 LOC of legacy infrastructure (engine + factory + tests-that-mock-the-engine + dead handler stubs from yesterday's #1092 cleanup).

α (~5-8 days) rejected: duplicates intent_service routing without adding value; contradicts #883.
β (~1 day) acceptable as softer landing — narrow the engine dispatcher to ANALYZE_REQUEST-only and route other types to direct dispatch. But γ-preserve is structurally cleaner and not much more work.

## Where I need your call

1. **α/β/γ**: which path?
2. **γ-preserve vs γ-strict**: if γ — keep the Workflow data model for future async-work surface (γ-preserve, my recommendation) or delete the entire workflow concept including status-polling endpoints (γ-strict)?
3. **Pattern-064 system-level instance**: does it warrant a methodology note (CIO call), an evolution-note on Pattern-064 itself, or just documentation in the eventual close-out commit?

## What I'm NOT asking

- **Not asking for ratification on Phase 2 sequencing details** — that's post-disposition work
- **Not pre-empting workflow-status polling deprecation** — γ-strict is a separate cohort decision, deferred unless ratified now
- **Not relitigating Issue #883** — its precedent stands; this memo only extends it

## Phase 2 estimate

If γ-preserve ratified: ~2-2.5 days Phase 2 (Slack handler refactor + engine class deletion + Workflow tests refactor + briefing update). Multi-session shape per worktree-default discipline.

## Cross-references

- Phase 0 audit context: `dev/2026/05/15/1020-issue-audit.md` (yesterday's #1020 reframe that produced #1094)
- Phase 1 design memo (this filing's substrate): `dev/2026/05/15/1094-phase-1-design.md` (commit `f71fa9d6`)
- Issue #883 (closed M1): lazy-workflow-creation refactor precedent
- Today's #1092 closure (`4092e2b4`): #1094's parent — engine dispatcher cleanup that surfaced this disposition question

— Lead Developer, 2026-05-15
