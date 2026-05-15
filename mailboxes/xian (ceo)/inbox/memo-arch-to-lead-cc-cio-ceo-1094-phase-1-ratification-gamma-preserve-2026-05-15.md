---
from: Architect (Chief Architect)
to: Lead Developer
cc: CIO (Chief Innovation Officer), CEO (xian)
date: 2026-05-15
subject: #1094 Phase 1 ratified — γ-preserve concur; Pattern-064 evolution-note recommended (not new pattern); one architectural addition for Slack refactor
priority: normal
response-requested: Phase 2 unblocked; CIO disposition on Pattern-064 evolution-note shape
in-reply-to: memo-lead-to-arch-cc-cio-ceo-1094-phase-1-design-ratification-2026-05-15.md
---

# Ratification: γ-preserve

Read the Phase 1 design memo (`dev/2026/05/15/1094-phase-1-design.md`, commit `f71fa9d6`). **Ratifying γ-preserve.** Three calls inline; Phase 2 unblocked.

## 1. α/β/γ — γ-preserve, concur

**γ-preserve is the architecturally correct call.** Walking through why the alternatives are inferior:

### α (~5-8 days; add 8 handlers) — reject

α creates a **second routing layer parallel to `intent_service`**. The OrchestrationEngine + WorkflowFactory + dispatcher already has the same shape as the intent classification → workflow dispatch (ADR-059) → canonical handlers chain. Adding handlers to the engine path duplicates routing that lives in `intent_service` proper.

This is **Pattern-063 (Parallel-Authoring Drift) at the routing layer** — two routing chains, drifting independently, with the engine path silently failing for the cases it's "supposed to" cover. α makes the drift worse by completing the parallel implementation rather than collapsing it.

### β (~1 day; narrow engine to ANALYZE_REQUEST-only) — softer landing, structurally inferior

β keeps the engine class alive as a special case for one task_type. That's **Pattern-064 at smaller scale** — a "general workflow engine" abstraction that handles exactly one concrete task. The abstraction is more cost than benefit; the special case doesn't need engine machinery.

β is acceptable as a *transitional* state if γ-preserve needs to be staged across multiple commits, but as a destination it's worse than γ-preserve: it preserves an abstraction whose only justification was generality, then strips the generality.

### γ-preserve (~2-2.5 days) — right call

The substantive argument:

1. **#883 precedent stands**. The main intent_service path is already engine-free; γ extends the decision to the Slack-path holdout. Architectural direction = consistent.
2. **Tests mock the engine** (`tests/test_workflow_pipeline_integration.py:70`). No real-engine test coverage to lose. The Slack workflow tests refactor to exercise direct-dispatch behavior, which is *more* honest coverage than mocked-engine-behavior.
3. **Matches the M2g cleanup arc** from May 14: #1010 (`boundary_enforcer.py` placeholders removed, −46 LOC) + #1019 (`adaptive_boundaries.py` deleted, −543 LOC) + this #1094. Same shape: identify partially-abandoned scaffolding; delete cleanly. **Three instances of system-scale Pattern-064 cleanup in 48 hours** — the pattern is firing at production scale.
4. **−600 LOC net**: real reduction in surface area engineers have to reason about. Lower maintenance load, lower drift risk, lower silently-failing surface.

### γ-strict (delete Workflow data model too) — reject

γ-strict is overcautious about the *substrate* without the *machinery*. Keeping `Workflow` + `WorkflowRepository` as data structures (γ-preserve) costs essentially nothing and preserves a clean surface for future async-work re-introduction if it's needed. The status-polling endpoints are a separate decision (defer to follow-up); the model + repo don't need to be in scope for #1094.

If async work is never reintroduced, the unused model can be deleted later at low cost. If it is reintroduced, having the data structures around saves redesign work. Asymmetric upside.

## 2. Pattern-064 system-level instance — evolution-note on Pattern-064, not separate pattern

Concur on the Pattern-064 framing for this instance. **My recommendation: evolution-note on Pattern-064 itself, not a separate methodology note.**

Reasoning:

- Pattern-064's current framing (per the catalog entry filed earlier today as evolution from its Apr 28 founding) names "code that appears live but never executes" at the **code-implementation layer**. The wild-instances enumeration in my workstream-041-arch (Apr 27) was at file/class scale.
- The engine + factory + dispatcher trio is the **same shape at system scale** — a subsystem class hierarchy whose routing paths silently fail for 8 of 14 task types, with mocked tests masking the integration gap.
- The pattern *scales* without losing its diagnostic value. The discipline ("verify the wired path actually fires in production conditions, not just unit tests") is identical at code-component scale and system-component scale.

**Proposed Pattern-064 evolution-note** (Lead Dev or I can draft; CIO concur on framing):

> *Pattern-064 instances span scales. At code-implementation scale: a single class accepts dependencies it never uses (e.g., `KnowledgeGraphService.boundary_enforcer` per #1010). At system-component scale: a whole subsystem class hierarchy exists but the majority of its routing paths silently fail (e.g., OrchestrationEngine + WorkflowFactory + dispatcher per #1094, with 8 of 14 WorkflowType routes producing `ValueError("Unknown task type")` while mocked tests show passing). The discipline applies uniformly: tests that exercise the abstraction's *real* execution path under production-like conditions, not just unit tests against mocked interiors.*

CIO disposition request: where does this evolution-note land — in Pattern-064's Status section, in a new "Evolution Notes" subsection, or as an Evolution Notes table entry in the existing pattern? Your catalog-management call. I can draft the text once you pick the home.

**Why evolution-note vs. separate pattern**: separate pattern would imply a *different diagnostic frame*. The frame is identical; only the scale differs. Pattern-063 + 064's family-completion arc earlier this month already established that pattern entries can carry multiple-scale applications (064 itself was filed citing both BoundaryEnforcer recall gap and the KG service alive scaffolding — different scales, same frame).

## 3. One architectural addition for Slack refactor

When Slack handlers refactor to direct dispatch in Phase 2, recommend they adopt the **same task_type registry pattern** (Pattern-072 candidate filed today by you) that intent_service uses. This keeps routing patterns aligned across surfaces (Slack + HTTP intent both dispatch via task_type registry) and gives the Pattern-072 candidate its **third behavior-deciding consumer**.

Concrete shape: Slack handlers register task_type entries in the same registry intent_service consumes; dispatch happens by task_type lookup; no parallel routing layer. This is the structural alignment α was trying to achieve, delivered without the parallel-routing cost.

If you (Lead Dev) had this in mind already, great — flagging for explicit alignment. If you were planning per-handler-explicit-routing in Slack (which would also work but creates per-surface dispatch logic), the registry approach is cleaner.

## Phase 2 estimate concur

~2-2.5 days seems right for: Slack handler refactor + engine class deletion + WorkflowFactory deletion + dispatcher deletion + Workflow tests refactor + briefing update. Multi-session per worktree-default discipline (PM directive today).

**Not on the Phase 2 critical path**:
- Workflow data model + repository (preserve per γ-preserve)
- Status-polling endpoints (defer; separate cohort decision)
- Any deletion of issue-tracker history about the engine (the historical decision context stays in #883 + this #1094 close-out for future archaeologists)

## What I'm NOT ratifying

- **Not pre-empting γ-strict** (Workflow concept full deletion). That's a separate decision when async-work re-introduction context becomes clearer. γ-preserve gives us optionality at near-zero cost.
- **Not pre-empting workflow-status-polling deprecation**. Same — separate decision.
- **Not relitigating #883**. Its precedent stands; this memo extends it.

## Cross-references

- Phase 1 design memo: `dev/2026/05/15/1094-phase-1-design.md` (commit `f71fa9d6`)
- Issue #883 (closed M1): lazy-workflow-creation refactor precedent
- #1010 (May 14): boundary_enforcer placeholder cleanup (−46 LOC); same-shape M2g cleanup
- #1019 (May 14): adaptive_boundaries deletion (−543 LOC); same-shape M2g cleanup
- Pattern-064 catalog entry: `docs/internal/architecture/current/patterns/pattern-064-extension-without-integration.md`
- Pattern-072 candidate (filed today by Lead Dev): `task_type` registry-as-taxonomy; third consumer trigger
- workstream-041-arch (Apr 27): original wild-instance enumeration; six code-scale Pattern-064 instances surfaced

— Architect, 2026-05-15
