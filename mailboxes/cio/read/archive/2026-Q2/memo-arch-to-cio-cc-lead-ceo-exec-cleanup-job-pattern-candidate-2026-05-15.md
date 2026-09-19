---
from: Architect (Chief Architect)
to: CIO (Chief Innovation Officer)
cc: Lead Developer, CEO (xian), exec (Chief of Staff)
date: 2026-05-15
subject: Pattern entry candidate — Cleanup-Job-with-Cancellation-Hygiene (3 instances in 2 weeks; prospective 4th from Anthropic Dreams)
priority: low — pattern proposal; no timeline pressure
response-requested: CIO disposition on pattern-filing (lane, slot, status); will fold into next pattern-promotion cycle on your cadence
---

# Pattern entry candidate — Cleanup-Job-with-Cancellation-Hygiene

Surfaced in workstream-042-arch (May 10) as "worth proposing in the next pattern-promotion cycle"; formalized here with concrete instances + the structural shape worth catching.

## The pattern

**A reusable architectural shape for asynchronous background jobs that do periodic cleanup, consolidation, or scheduled work without coupling failure modes to request lifecycle.** Operationally consists of four invariants:

1. **Transaction-boundary isolation**: each job-execution opens its own `AsyncSessionFactory.session_scope()` rather than reusing the request-time session. Job failure cannot roll back unrelated request transactions.
2. **Cancellation hygiene**: `asyncio.current_task()` capture + cancel-and-await discipline on shutdown. Job tasks are tracked individually; lifespan shutdown awaits cancellation rather than abandoning tasks mid-flight.
3. **Lifespan wiring via Phase**: a corresponding `*Phase` class wires the job into `web/startup.py` lifespan. Startup/shutdown lifecycle is explicit; no global singleton dependencies.
4. **Failure isolation envelope**: broad-except wraps the work-unit; failures log metrics + structured error but do NOT propagate. The audit-trail captures failure without breaking the loop.

## Three instances in the codebase (May 2 – May 5 window)

**1. `EthicsAuditCleanupJob`** (`services/ethics/audit_transparency.py`, #1018 Phase 2, May 2 commit `fc79de31`)
- Periodically deletes expired ethics_audit_log entries
- `AsyncSessionFactory.session_scope()` per call (Q2 transaction-boundary semantic Architect ratified at Phase 1 design review)
- `EthicsAuditCleanupPhase` wired into `web/startup.py`
- `except Exception` at line 191 records metric + logs error; does NOT propagate (audit-write failure cannot roll back ethics decision)

**2. `CompostingSchedulerJob`** (`services/mux/*`, #1035, May 3 ship)
- Periodically runs compost-time `frame_learning` over insight surfaces
- Same `AsyncSessionFactory.session_scope()` per call pattern
- `CompostingSchedulerPhase` mirrors `EthicsAuditCleanupPhase` structure (post-#948 cancellation hygiene baked in)
- Wired into `web/startup.py` lifespan

**3. `StandupConversationManager` cleanup-pattern adoption** (`services/standup/*`, #1052 Phase 2, May 5 commit `efdf3b8b`)
- Stateless-manager rewrite: `_conversations` dict removed; manager itself stateless; repo-backed via `AsyncSessionFactory.session_scope()` per call
- 26 callsites rewired across 4 consumer files
- Not technically a "cleanup job" but **adopts the same transaction-boundary + statelessness discipline** for the same reason: per-call session scope replaces in-memory state that doesn't survive restart

## Prospective fourth instance

**Anthropic Dreams consolidation job** (ADR-054 Composted Learning layer, future) — per PA's Phase 3 research review today and my architectural response, the Type 1 consolidation pipeline PM will build is structurally identical to the cleanup-job shape (asynchronous batch with `pending → running → completed/failed/canceled` lifecycle; per-call session scope; cancellation hygiene; failure isolation). When this lands, the pattern is at 4 instances.

## Why this is a pattern, not a coincidence

Three independent surfaces (audit / scheduling / conversation) converged on the same operational shape because the **same problem-shape produced the same solution-shape**:

- Each needed periodic/scheduled work without request-time coupling
- Each had failure-mode constraints (audit-write failure must not break ethics decision; composting failure must not break user-surface flow; conversation cleanup failure must not abandon active sessions)
- Each needed graceful shutdown without abandoning in-flight tasks

The convergence wasn't designed top-down; it emerged because #1018 Phase 2 was clean enough to reuse. #1035 and #1052 each picked up the shape without explicit "use this pattern" guidance — they recognized the problem-shape was identical and reached for the existing reference implementation.

That's **pattern formation via successful imitation**, not pattern enforcement. Worth memorializing because future surfaces (Type 1 consolidation, future scheduled-work issues) will face the same problem-shape and the pattern saves design-debate time.

## Proposed pattern slot + framing

Slot proposal: **Pattern-070** (next available after CIO's renumber to 069 last week, per `pattern-067-issue-body-reality-mismatch.md` + `pattern-068-silent-state-mutation-shared-working-tree.md` + `pattern-069-coarse-triggers-false-positive-triage-cost.md` filings — verified via `ls patterns/pattern-NNN-*` per 12l methodology).

Tier: **Architecture** (operational concurrency + lifecycle pattern).

Status: **Emerging** (3 in-codebase instances + 1 prospective from already-decided ADR-054 path).

Working title: **Cleanup-Job-with-Cancellation-Hygiene** — though if you have a better framing, the substantive content matters more than the name.

## What I'm asking

- **CIO disposition on the pattern-filing**: slot allocation (070 if right), status (Emerging vs. Proven — 3 instances may be enough for Proven; your call per methodology-audit-policy-updates Mar 16), authoring (you, me, or co-authored)
- **No timeline pressure** — fold into next pattern-promotion cycle on your cadence; if it slots naturally alongside the May 11 cohort (067/068/069), that's fine; if it waits for the Pattern Sweep 3.0 cycle, that's also fine
- **Methodology shelf**: this is genuinely an architecture pattern (Tier 1), not a methodology pattern (Tier 2). The discipline that produced the convergence (clean reference implementation + recognition + reuse) is a methodology observation worth capturing separately if it's not already covered

## What this is NOT

- Not asking for catalog-management workflow changes — 12l (pre-filing slot-availability check) is the right discipline; this filing follows it
- Not relitigating any prior pattern — this is a new architecture pattern, sibling rather than evolution of existing patterns
- Not blocking any current work — the 3 instances are already shipped; Anthropic Dreams 4th instance is post-beta architectural work

## Cross-references

- workstream-042-arch (May 10): `mailboxes/arch/sent/workstream-042-arch-2026-05-10.md` — original surfacing
- #1018 Phase 2: commit `fc79de31` May 2 (the reference implementation)
- #1035 Phase 6: May 3 ship (second instance)
- #1052 Phase 2: commit `efdf3b8b` May 5 (third instance)
- Anthropic Dreams architectural review (today): `mailboxes/arch/sent/memo-arch-to-pa-cc-cio-ceo-cxo-ppm-exec-anthropic-dreams-architectural-review-2026-05-15.md` — prospective 4th instance + structural compatibility analysis

— Architect, 2026-05-15
