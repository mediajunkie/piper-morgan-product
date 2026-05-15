# Pattern-070: Cleanup-Job-with-Cancellation-Hygiene

## Status

**Emerging** — Filed 2026-05-15 by Architect per CIO disposition (May 15) following May 15 candidate proposal. Slot 070 allocated after 12l pre-filing slot-availability check (`ls patterns/pattern-NNN-*`); first pattern filed under that discipline. Promotion to Proven contingent on **fourth instance landing and using the four invariants without rediscovery** — Anthropic Dreams Type 1 consolidation pipeline (per PA Phase 3 review May 12 + CEO substrate decision May 12 to build PM-side) is the natural fourth-instance target; promotion to Proven when that ships and naturally adopts the invariants. CIO co-signs the methodology sidecar ("Pattern Formation via Successful Imitation," tracker 12o, drafting Mon May 18 → Tue May 19).

## Product Relevance

**Architecture** — Reusable shape for asynchronous background jobs across PM's domain layer. Users will not encounter this directly; engineers building scheduled or periodic work units will reach for it.

## Context

PM has accumulated several surfaces that need **asynchronous background work without coupling failure modes to request lifecycle**: ethics-audit log cleanup, insight composting, conversation-state lifecycle hygiene, and (prospectively) Type 1 consolidation. Each independently arrived at the same operational shape because the same problem-shape produced the same solution-shape.

The pattern names that convergence so future surfaces facing the same problem-shape have a citable reference rather than re-deriving from first principles.

## Problem

### The Failure Mode

```
Background job runs inside a request transaction
  → request transaction rolls back on job failure
  → unrelated request work is lost

OR

Background job task is abandoned on shutdown
  → in-flight work strands mid-execution
  → next startup finds partial state

OR

Background job fails silently
  → failure isn't logged, metric, or audited
  → debugging requires reconstruction from absence
```

Each of these has burned PM at one time or another. The pattern is the discipline that prevents all three.

### Where the convergence appeared

Three instances appeared in 2026-05-02 → 2026-05-05 (three independent surfaces, no top-down direction):

- **`EthicsAuditCleanupJob`** (`services/ethics/audit_transparency.py`, #1018 Phase 2, May 2 commit `fc79de31`) — periodically deletes expired `ethics_audit_log` entries
- **`CompostingSchedulerJob`** (`services/mux/`, #1035, May 3) — periodically runs compost-time `frame_learning` over insight surfaces
- **`StandupConversationManager` cleanup-pattern adoption** (`services/standup/`, #1052 Phase 2, May 5 commit `efdf3b8b`) — stateless-manager rewrite using the same transaction-boundary + statelessness discipline

The convergence is what made the pattern visible — three roles using the same shape without enforcement.

## Solution

### The four operational invariants

1. **Transaction-boundary isolation** — each job-execution opens its own `AsyncSessionFactory.session_scope()` rather than reusing request-time session. Job failure cannot roll back unrelated request transactions.
2. **Cancellation hygiene** — `asyncio.current_task()` capture + cancel-and-await discipline on shutdown. Job tasks are tracked individually; lifespan shutdown awaits cancellation rather than abandoning tasks mid-flight.
3. **Lifespan wiring via Phase** — a corresponding `*Phase` class wires the job into `web/startup.py` lifespan. Startup/shutdown lifecycle is explicit; no global singleton dependencies.
4. **Failure isolation envelope** — broad-except wraps the work-unit; failures log metrics + structured error but do NOT propagate. The audit-trail captures failure without breaking the loop.

### Why these four together

Each invariant prevents a specific failure mode:

| Invariant | Prevents |
|---|---|
| Transaction-boundary isolation | Job failure rolling back unrelated request work |
| Cancellation hygiene | Stranded in-flight tasks on shutdown |
| Lifespan wiring via Phase | Hidden global state; unpredictable startup ordering |
| Failure isolation envelope | Silent failure; debugging-from-absence |

**Together they make the job *safe to add anywhere*.** Without all four, adding a new background job has a known failure surface; with all four, the cost of adding one is low.

## Reference Instances

### Instance 1: `EthicsAuditCleanupJob` (`services/ethics/audit_transparency.py`, May 2)

The reference implementation. #1018 Phase 2 design-review explicitly ratified the Q2 transaction-boundary semantic ("audit-write failure must not roll back ethics decision"). Lifespan wiring: `EthicsAuditCleanupPhase` in `web/startup.py`. Failure isolation: `except Exception as e` at line 191 records metric + logs error; does NOT propagate. This is the clean-enough-to-reuse reference.

### Instance 2: `CompostingSchedulerJob` (`services/mux/`, May 3)

Picked up the shape from #1018 reference. `CompostingSchedulerPhase` mirrors `EthicsAuditCleanupPhase` structure with post-#948 cancellation hygiene baked in. Same `AsyncSessionFactory.session_scope()` per call pattern. No explicit "use pattern-X here" guidance — convergence via successful imitation.

### Instance 3: `StandupConversationManager` cleanup-pattern adoption (`services/standup/`, May 5)

Not technically a periodic cleanup job, but adopts the same transaction-boundary + statelessness discipline for the same reason: per-call session scope replaces in-memory state that doesn't survive restart. The `_conversations` dict was removed; manager itself is stateless; repo-backed via `AsyncSessionFactory.session_scope()` per call. 26 call-sites rewired across 4 consumer files. Demonstrates the pattern's applicability beyond strictly-scheduled work — anywhere request-time state is too coupling, the same shape applies.

### Prospective Instance 4: Anthropic Dreams Type 1 consolidation (post-ADR-054)

Per PA Anthropic Dreams Phase 3 review (May 12) + Architect response (May 15) + CEO substrate decision (May 12 — build PM-side, not Anthropic-substrate-delegated): the Type 1 consolidation pipeline PM will build is structurally identical to the cleanup-job shape — asynchronous batch with `pending → running → completed/failed/canceled` lifecycle, per-call session scope, cancellation hygiene, failure isolation. When this lands, Pattern-070 promotes to Proven.

## Pattern Formation via Successful Imitation

This pattern emerged organically across three independent surfaces (audit / scheduling / conversation) — not via top-down enforcement. The convergence happened because:

1. **#1018 Phase 2 was clean enough to reuse** — the reference implementation was scrutable; engineers reading it could see "what shape this has and why."
2. **The problem-shape was identical** — periodic/scheduled work without request-time coupling, with failure-mode constraints.
3. **No friction to imitate** — the four invariants fit cleanly without requiring a new framework or library; just discipline at instance creation.

CIO's methodology-corpus sidecar ("Pattern Formation via Successful Imitation," tracker 12o) names this discipline directly. The methodology observation is **distinct from this pattern** but explains why this pattern emerged: clean reference implementations + cohort recognition + reuse without enforcement = pattern formation.

When this happens twice or three times, it's worth memorializing the pattern. When it happens once, document the reference implementation; don't reach for a pattern entry.

## Anti-pattern: Cleanup Job Without Hygiene

The negation of this pattern produces specific failure modes:

- **Cleanup job inside request session** → request transactions roll back on cleanup failure
- **Cleanup job without cancel-and-await** → in-flight work stranded on shutdown; next startup confused state
- **Cleanup job as global singleton** → hidden startup ordering dependencies; tests can't isolate
- **Cleanup job with propagated exceptions** → silent observability; failures only visible by their downstream effects

If any of these surface in code review, **the pattern's name + four invariants is the diagnostic vocabulary** for naming the gap.

## Cross-References

- **#1018 Phase 2 reference implementation**: commit `fc79de31` (May 2, 2026)
- **#1035 second instance**: May 3, 2026
- **#1052 Phase 2 third instance**: commit `efdf3b8b` (May 5, 2026)
- **Anthropic Dreams Phase 3 review** (prospective fourth instance): `mailboxes/arch/sent/memo-arch-to-pa-cc-cio-ceo-cxo-ppm-exec-anthropic-dreams-architectural-review-2026-05-15.md`
- **CIO disposition memo** (filing approval): `mailboxes/arch/inbox/memo-cio-to-arch-cc-lead-ceo-exec-pattern-070-cleanup-job-disposition-2026-05-15.md`
- **Architect proposal memo** (origin): `mailboxes/arch/sent/memo-arch-to-cio-cc-lead-ceo-exec-cleanup-job-pattern-candidate-2026-05-15.md`
- **workstream-042-arch original surfacing**: `mailboxes/arch/sent/workstream-042-arch-2026-05-10.md`
- **CIO methodology sidecar (forthcoming)**: tracker 12o — "Pattern Formation via Successful Imitation"
- **Pattern-049 audit-cascade** — adjacent: the cleanup-job discipline is what audit-cascade catches when it surfaces alive-scaffolding instances of incomplete cleanup-job adoption
- **Pattern-064 Extension Without Integration** — adjacent: failure mode of partially-adopted cleanup-job pattern (e.g., transaction-boundary isolation present but cancellation hygiene missing) is itself a Pattern-064 instance at the implementation layer

## Evolution Notes

| Date | Event |
|---|---|
| 2026-05-02 | `EthicsAuditCleanupJob` ships as #1018 Phase 2; reference implementation lands cleanly |
| 2026-05-03 | `CompostingSchedulerJob` ships as #1035; second independent instance |
| 2026-05-05 | `StandupConversationManager` Phase 2 ships as #1052; third independent instance |
| 2026-05-10 | workstream-042-arch flags the three-instance convergence as worth proposing for pattern-promotion cycle |
| 2026-05-12 | PA Anthropic Dreams Phase 3 review surfaces structural compatibility — prospective fourth instance via Type 1 consolidation |
| 2026-05-15 | Architect proposes pattern candidate to CIO with slot 070 + four-invariant framing |
| 2026-05-15 | CIO dispositions: Emerging now, Proven on fourth instance; Architect authors, CIO co-signs methodology sidecar |
| 2026-05-15 | Pattern-070 filed Emerging |
| (future) | Anthropic Dreams Type 1 consolidation pipeline ships; if four invariants are adopted without explicit guidance, promote to Proven |
