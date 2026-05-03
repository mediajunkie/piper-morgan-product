# Gameplan: #1035 MUX-COMPOSTING-ACTIVATION

**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/1035
**Author**: Lead Developer (Claude Code Opus)
**Date**: 2026-05-03
**Template version**: gameplan-template v9.3
**Status**: Draft — pending audit-cascade against template + PM Phase -1 walkthrough

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status** (from spike + this gameplan-prep read):

- [x] Web framework: **FastAPI**, with `StartupManager` orchestrating lifespan phases (`web/startup.py:445`)
- [x] Database: **PostgreSQL via SQLAlchemy async**; `AsyncSessionFactory.session_scope()` per call pattern established in #1018
- [x] Migration tooling: **Alembic** with versions in `alembic/versions/`
- [x] Repository pattern: flat path in `services/database/repositories.py` (Architect Q1 ratification, May 2)
- [x] Scheduler pattern reference: `services/scheduler/ethics_audit_cleanup_job.py` with post-#948 cancellation hygiene
- [x] Testing framework: pytest + asyncio + aiosqlite (graceful skip pattern from #1018)
- [x] Composting classes complete (existence verified in spike):
  - `services/mux/composting_pipeline.py` — `SurfaceableInsight`, `InsightJournal`, `CompostingPipeline`
  - `services/mux/composting_scheduler.py` — `CompostingSchedule`, `CompostingScheduler`, `COMPOSTING_FRAMES`, `frame_learning`
  - `services/mux/compost_bin.py` — `CompostBin`, `CompostBinEntry`
  - `services/mux/composting_models.py` — `CompostingTrigger`, `ExtractedLearning`, `Insight`
  - `services/mux/lifecycle.py` — `LifecycleState`, `CompostingExtractor`
- [x] InsightJournal API surface (`services/mux/composting_pipeline.py:171-392`):
  - `add(insight) → SurfaceableInsight`
  - `get(insight_id) → Optional[SurfaceableInsight]`
  - `async get_unsurfaced(user_id, min_confidence, trust_stage, limit) → List[SurfaceableInsight]` (Push mode query)
  - `async get_for_context(user_id, context_entities, context_topics, trust_stage, limit) → List[SurfaceableInsight]` (Pull mode query)
  - `async mark_surfaced(insight_id, response) → Optional[SurfaceableInsight]`
  - `get_for_object(object_id) → List[SurfaceableInsight]`
  - `count` (property)
  - `clear() → int`
- [x] `SurfaceableInsight.to_dict()` and `from_dict()` already implemented (lines 117-163) — easy bridge to SQLAlchemy model
- [x] Composting NOT wired into startup (verified in spike; `web/startup.py` phase list does NOT include any composting phase)

**Lead Dev's understanding of the task**:

#1035 has three intertwined deliverables:
1. **Persistence**: PostgreSQL table for `SurfaceableInsight` + Alembic migration + `InsightRepository`; `InsightJournal` rewritten to delegate to repository (in-memory `_insights`/`_by_user`/`_by_object` dicts gone). Possibly also persist `CompostBin` queue.
2. **Scheduler activation**: a `CompostingSchedulerPhase` (parallel to `EthicsAuditCleanupPhase`) wraps `CompostingScheduler.maybe_run()` in a periodic loop; lifespan startup/shutdown with post-#948 cancellation hygiene.
3. **Configuration plumbing**: quiet-hours / batch / interval defaults sourced from env or config (per spec: 2-5 AM local, min_pending=5, max_batch=20, min_interval_hours=4).

This is the same architectural shape as #1018 Phase 2, but applied to insights/composting instead of audit transparency. Lifting that pattern is the play.

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

- [x] Multi-file backend change (DB migration + repository + class rewrite + lifespan phase + scheduler-job wrapper + tests)
- [x] Task duration >30 minutes — yes, ~6-10 hours estimated (parallel to #1018 Phase 2 which was a single-day effort)
- [x] Multi-component work — DB + service + scheduler + tests
- [x] Exploratory/risky changes — moderate: schema + scheduler activation
- [ ] Multiple agents in parallel — single agent (Lead Dev)

**Assessment**: **USE WORKTREE** — schema + scheduler change has rollback value; #1030/#1031/#1032/#1033 will sit on top of this branch's work.

```bash
cd /Users/xian/Development/piper-morgan/piper-morgan-product
git worktree add ../piper-morgan-product-1035-composting -b claude/1035-composting-activation main
```

### Part B: PM Verification Required

Questions for PM:

1. **CompostBin queue durability**: persist `CompostBin` items to DB, OR rebuild compost-bin queue at startup from candidate-objects-not-yet-composted? **My lean**: **rebuild at startup**. The composting cycle is forgiving by design (insights re-extract from objects); persistent compost-bin queue adds schema complexity for marginal value. If we lose the compost-bin queue on restart, the next quiet-hours run rebuilds it from objects that meet criteria. PM call.
2. **Scheduler loop ownership**: build a new `CompostingSchedulerJob` wrapper (parallel to `EthicsAuditCleanupJob`) that owns the periodic loop, OR add the loop into `CompostingScheduler` itself? **My lean**: **separate job wrapper** — keeps `CompostingScheduler` testable as a domain class; the lifecycle/loop concern stays in `services/scheduler/`. Mirrors the #1018 split.
3. **Migration ordering**: this migration depends on existing schema (no FK changes); can land independently. Alembic head is currently at `a1018_add_ethics_audit_log` (#1018) — this would be the next migration. Confirm OK to proceed without coordination on migration head sequence with other in-flight work.
4. **ADR-061 alignment**: ADR-061 (composting + ethics scheduling architecture) is in flight from Architect, awaiting PM ratification. Are there decisions in ADR-061 that could change the persistence shape or scheduler discipline before #1035 lands? **STOP-recommend**: Lead Dev re-reads ADR-061 v1.0 in Phase 0; if there are constraints, raise with Architect before starting Phase 1 schema. Confirm OK to proceed with this dependency.
5. **User scoping**: `SurfaceableInsight.user_id` is already on the model — insights are per-user. Phase -1 question: in the current alpha (single user), do we partition by user_id at query time anyway (so the schema is correct from day one even though only one user exists today)? **My lean**: yes; data model should be future-correct.
6. **`InsightJournal.clear()` durability**: current API has a `clear()` method. With persistence, clear should `DELETE FROM insights WHERE user_id = ?` (or admin-only). Confirm semantics: per-user clear vs system-wide clear. **My lean**: per-user (matches existing journal behavior + UI Reset button).

### Part C: Proceed/Revise Decision

- [ ] **PROCEED** — pending PM confirmation on Q1-Q6
- [ ] **REVISE** — if ADR-061 has hard constraints not yet visible
- [ ] **CLARIFY** — if migration ordering coordination is needed

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 1035
   ```

2. **ADR-061 read-through** (per Phase -1 Q4):
   - Locate ADR-061 in `docs/internal/architecture/current/adrs/`
   - Read for any composting-architecture constraints
   - If constraints surface, surface to Architect before Phase 1

3. **Codebase Investigation**:
   ```bash
   # Verify no existing in-flight composting persistence work
   git log --grep="composting\|InsightJournal\|SurfaceableInsight" --oneline | head -20

   # Inventory of consumers of InsightJournal API
   grep -rn "InsightJournal\|SurfaceableInsight\|composting_pipeline" services/ web/ tests/

   # Verify alembic head
   alembic current

   # Run existing composting-related tests as baseline
   pytest tests/unit/services/mux/ -v --collect-only | head -40
   ```

4. **Update GitHub Issue**:
   ```
   ## Status: Investigation Started
   - [ ] ADR-061 read; no blocking constraints
   - [ ] Existing consumers inventoried
   - [ ] Alembic head verified
   - [ ] Phase -1 PM walkthrough complete
   ```

### STOP Conditions

- ADR-061 has decisions that conflict with the persistence/scheduler approach in this gameplan → stop and align with Architect
- In-flight work on InsightJournal persistence by another agent → coordinate
- Alembic head conflict (a parallel migration was filed that would collide) → coordinate before adding migration

---

## Phase 0.5: Frontend-Backend Contract Verification

### Applicability assessment

**Mixed**: this issue does not directly add new endpoints, but it changes the **persistence guarantees** of `InsightJournal`. Downstream issues #1030 (Pull) and #1031 (Passive) will add API endpoints that consume the persistent journal. For this issue's scope, no new contract is added — but the existing/planned `/api/v1/insights*` namespace per the API-prefix convention (#1013) is reserved.

### Required Actions

1. **No frontend-facing changes in this issue**; document that the Phase 0.5 verification is deferred to #1030 / #1031 which will add the endpoints.
2. **Mount-prefix preflight**: verify `/api/v1/insights` is not already taken (spike confirmed only `/insights` UI route exists in `web/api/routes/ui.py:349`; no API route under that prefix).

### STOP Conditions

- If a parallel agent has filed a `/api/v1/insights*` route in flight → coordinate before #1030/#1031 to avoid collision

---

## Phase 0.6: Data Flow & Integration Verification

### Applicability assessment

**Applies** — this is multi-layer: scheduler loop → `CompostingPipeline` → `InsightJournal` → `InsightRepository` → DB; and concurrently scheduler loop → `CompostBin` → `CompostingScheduler.run()`.

### Part A: Data Flow Requirements

| Layer | Needs change? | Source of values |
|-------|---------------|------------------|
| `CompostingSchedulerJob` (NEW, in `services/scheduler/`) | ✅ NEW | Wraps `CompostingScheduler.maybe_run()` in periodic loop; constructed in startup phase |
| `CompostingScheduler` | No change | Existing class; consumed by job wrapper |
| `CompostingPipeline.process(obj, user_id, trigger)` | No change | Existing class |
| `InsightJournal.add()` | ✅ delegates to repo | Was: in-memory dict. New: `await session_scope(): InsightRepository.add()` |
| `InsightJournal.get()` etc. | ✅ delegates to repo | Same shape change |
| `InsightRepository` (NEW) | ✅ NEW | `services/database/repositories.py` (flat path, per #1018) |
| `InsightDB` SQLAlchemy model (NEW) | ✅ NEW | `services/database/models.py` |
| Alembic migration | ✅ NEW | `alembic/versions/aXXXX_add_insight_journal.py` |
| Startup phase: `CompostingSchedulerPhase` | ✅ NEW | `web/startup.py` — register after `EthicsAuditCleanupPhase` |

### Part B: Integration Points Checklist

| Caller | Callee | Verification |
|--------|--------|--------------|
| Lifespan `startup()` | `CompostingSchedulerPhase.startup` | Phase registered in `StartupManager.phases` after `EthicsAuditCleanupPhase` |
| `CompostingSchedulerPhase.startup` | `CompostingSchedulerJob(...)` | Constructor accepts schedule, compost_bin, pipeline; `start()` returns task |
| `CompostingSchedulerJob` (loop) | `CompostingScheduler.maybe_run` | Periodic call (e.g., every hour); logs "skipped"/"ran" results |
| `CompostingScheduler.run` | `CompostingPipeline.process` | Existing wiring |
| `CompostingPipeline.process` | `InsightJournal.add` | Existing wiring; new: `add` is now async + persists |
| `InsightJournal.add` | `AsyncSessionFactory.session_scope()` → `InsightRepository.add` | NEW; matches #1018 pattern |
| `InsightRepository.*` | `AsyncSession` | NEW; flat path |
| Premonition / consumers | `InsightJournal.get_unsurfaced` etc. | Existing API surface; consumer code unchanged (drop-in) |

### Part C: Pattern Adaptation Notes

This issue **explicitly follows the #1018 Phase 2 pattern**. Adaptation table:

| Aspect | #1018 (audit_transparency) | #1035 (composting) | Why different |
|--------|---------------------------|-----|---|
| Domain model | `AuditLogEntry` dataclass | `SurfaceableInsight` dataclass | already exists |
| In-memory storage being replaced | `self.audit_logs: List` | `InsightJournal._insights: Dict` (+ `_by_user`, `_by_object` indices) | dual indexing needs to be preserved through repository |
| New SQLAlchemy model | `EthicsAuditLogDB` | `InsightDB` | parallel pattern |
| New repository | `EthicsAuditRepository` | `InsightRepository` | parallel; user-id partitioning is the major axis |
| New migration | `a1018_add_ethics_audit_log.py` | `aXXXX_add_insight_journal.py` | TIMESTAMPTZ throughout (carried over from #1006 fix) |
| Transaction-boundary | per-call `AsyncSessionFactory.session_scope()` | same | Architect Q2 ratification |
| Scheduler job | `EthicsAuditCleanupJob` (24h interval, 90-day retention sweep) | `CompostingSchedulerJob` (1h interval, calls `maybe_run` to honor quiet-hours) | composting requires periodic check, not strict interval |
| Cancellation hygiene | Capture `asyncio.current_task()` in `start()`; cancel-and-await in `stop()` | same (post-#948) | direct lift |
| Test pattern | aiosqlite importorskip + mock-repo for unit tests | same | direct lift |

**Potential pitfalls from differences**:

1. **`InsightJournal` dual-index loss**: current implementation maintains `_by_user` and `_by_object` dicts as in-memory indices for fast lookup. With repository delegation, these become DB indices on `(user_id)` and `(object_id)`. Migration must include those indices.
2. **`InsightJournal.clear()`**: per Phase -1 Q6, clear is now per-user. Direct API behavior change to surface.
3. **`get_for_context` relevance scoring**: lines 273-347 do Python-side scoring with entity/topic overlap. Two options: (a) fetch all user insights from DB then score in Python (acceptable for MVP scale); (b) push scoring into SQL (bigger change, premature optimization). **Lean**: option (a). Will document.
4. **`mark_surfaced`** mutates state; with persistence, this becomes an UPDATE. Need to ensure same-transaction semantics aren't accidentally lost.
5. **`CompostBin` rebuild on restart** (Phase -1 Q1 lean: rebuild not persist): need a clear rule for "what's compostable on startup" — likely "objects in COMPOSTED state that don't have an InsightJournal entry yet" or similar predicate. Phase 0 of #1035 must verify this is reachable from existing data.

### STOP Conditions

- If Phase 0 reveals InsightJournal has consumers we haven't accounted for → reassess scope
- If existing tests fail due to API timing change (sync `add()` becomes `async add()`) → may need both sync + async paths during transition
- If ADR-061 Q4 surfaces architectural constraint → align before phase 1

---

## Phase 0.7: Conversation Design

### Applicability assessment

**Not applicable** — this is infrastructure/persistence work, not a conversational feature.

### Per audit-cascade skill: PM approval needed to mark inapplicable

**Question for PM**: confirm Phase 0.7 inapplicability. (Same condition as #1034.)

---

## Phase 0.8: Post-Completion Integration

### Applicability assessment

**Partially applicable**: this issue creates new database records (InsightDB rows) but does NOT change user state or trigger downstream user-visible behavior changes from this issue's scope alone. The downstream issues (#1030/#1031/#1032/#1033) are where user-visible behavior begins. So:

| Side Effect | Table | Verified? |
|---|---|---|
| InsightJournal entries persist | `insights` table | ✅ test |
| Composting cycle runs in production | logs `composting_run_complete` | ✅ smoke test |
| User state changes | None | N/A |
| Other features behave differently | None directly (only after #1030/#1031/#1032/#1033) | N/A |

### Per audit-cascade skill: PM approval to mark partial-applicability

**Question for PM**: confirm Phase 0.8 partial-applicability framing. The DB-side checklist applies; the user-state/downstream-features axes do not for this issue alone.

---

## Phases 1-N: Development Work

### Phase 1: ADR-061 alignment + design pass

**Work** (matches Phase 0 Q4 directive):

- [ ] Read ADR-061 v1.0 end-to-end
- [ ] Identify any composting-architecture decisions that constrain persistence/scheduler shape
- [ ] If constraints surface, file a "Lead Dev follow-up to Architect" memo before Phase 2

**Bookend**: comment on #1035 with "Phase 1 ADR-061 alignment complete (or constraints raised)."

### Phase 2: Schema + migration

**Work**:

- [ ] Define `InsightDB` SQLAlchemy model in `services/database/models.py`:
  - `id: UUID PK` (matches `SurfaceableInsight.id`)
  - `object_id: str` (indexed)
  - `user_id: str` (indexed)
  - `created_at: TIMESTAMPTZ` (TIMESTAMPTZ throughout, per #1006 carryover)
  - `learning: JSONB` (serialized `ExtractedLearning`)
  - `surfaced_count: int`
  - `last_surfaced: Optional[TIMESTAMPTZ]`
  - `user_response: Optional[str]`
  - `min_trust_stage: int`
  - `connected_insights: JSONB` (List[str])
  - `context_tags: JSONB` (List[str])
  - `from_domain(insight: SurfaceableInsight) -> InsightDB`
  - `to_domain() -> SurfaceableInsight`
- [ ] Alembic migration `aXXXX_add_insight_journal.py` with: table create + indexes on `(user_id, created_at DESC)`, `(object_id)`
- [ ] Run migration locally; verify roundtrip via test

**Tests**:

- [ ] Unit tests for `InsightDB.from_domain` / `to_domain` roundtrip
- [ ] Migration applies/reverts cleanly

### Phase 3: Repository

**Work**:

- [ ] Add `InsightRepository` to `services/database/repositories.py` with methods mirroring InsightJournal API:
  - `async add(insight: SurfaceableInsight) -> SurfaceableInsight`
  - `async get(insight_id: str) -> Optional[SurfaceableInsight]`
  - `async get_unsurfaced(user_id: str, min_confidence: float, trust_stage: int, limit: int) -> List[SurfaceableInsight]`
  - `async get_for_context(user_id: str, context_entities: List[str], context_topics: List[str], trust_stage: int, limit: int) -> List[SurfaceableInsight]` — fetch all user insights, score in Python (per Phase 0.6 pitfall #3)
  - `async mark_surfaced(insight_id: str, response: str) -> Optional[SurfaceableInsight]`
  - `async get_for_object(object_id: str) -> List[SurfaceableInsight]`
  - `async count(user_id: Optional[str] = None) -> int`
  - `async clear(user_id: str) -> int` (per Q6)

**Tests**:

- [ ] Unit tests with `aiosqlite.importorskip` (graceful skip pattern from #1018)
- [ ] Each method has add → query → assert roundtrip; mark_surfaced verifies update; clear verifies user-scoped delete

### Phase 4: InsightJournal rewrite

**Work**:

- [ ] Update `InsightJournal.__init__` to accept (or default-construct) an `InsightRepository`
- [ ] Each method delegates: `await session_scope() as session: repo = InsightRepository(session); return await repo.METHOD(...)` per call (per #1018 Q2 transaction-boundary)
- [ ] Remove `_insights`, `_by_user`, `_by_object` in-memory state
- [ ] Existing consumers (premonition, etc.) work unchanged

**Tests**:

- [ ] Existing InsightJournal tests rewritten to mock-repo pattern (parallel to `tests/ethics/test_phase3_integration.py` rewrite under #1018)
- [ ] Wiring test: insight added → process restart simulated → insight retrieved (this is the smoke test for "persistence actually works")

### Phase 5: Scheduler activation

**Work**:

- [ ] New `services/scheduler/composting_scheduler_job.py` with `CompostingSchedulerJob`:
  - `__init__(scheduler: CompostingScheduler, interval_seconds: int = 3600, user_id_provider: Callable[[], str])`
  - `async start()` — periodic loop calling `await scheduler.maybe_run(user_id=user_id_provider())`; capture `asyncio.current_task()`
  - `async stop()` — cancel-and-await (post-#948 hygiene)
  - Log skipped (quiet-hour-not-met) and ran (with `CompostingRunResult`)
- [ ] New `CompostingSchedulerPhase` in `web/startup.py`:
  - `startup()`: construct `CompostBin`, `CompostingPipeline`, `CompostingScheduler` (with default schedule), wrap in job, `asyncio.create_task(job.start())`, store on `app.state.composting_scheduler_job` + task
  - `shutdown()`: `await app.state.composting_scheduler_job.stop()`
- [ ] Add to `StartupManager.phases` after `EthicsAuditCleanupPhase`
- [ ] Source schedule config from env / config (with sensible defaults: `quiet_hours=[2,3,4]`, `min_pending=5`, `max_batch=20`, `min_interval_hours=4.0`)

**Tests**:

- [ ] `CompostingSchedulerJob` lifecycle tests (start → run → stop without orphans; cancel mid-loop is sub-second, parallel to `EthicsAuditCleanupJob` tests)
- [ ] Mock `CompostingScheduler.maybe_run` to verify the loop calls it with the right user_id
- [ ] Phase tests (parallel to existing EthicsAuditCleanupPhase tests if present)

### Phase 6: CompostBin behavior on startup

**Work** (per Phase -1 Q1 lean: rebuild not persist):

- [ ] Verify CompostBin starts empty on startup (default constructor behavior — already true, just doc it)
- [ ] If a "rebuild from candidates" path is needed, file as a follow-up issue (out of #1035 scope)

### Phase 7: Tests + verification

**Work**:

- [ ] Repository unit tests pass (Phase 3)
- [ ] InsightJournal integration tests pass (Phase 4)
- [ ] Scheduler-job lifecycle tests pass (Phase 5)
- [ ] Wiring integration test: end-to-end startup → quiet-hours mock → CompostingPipeline.process → InsightRepository.add → DB row written → InsightJournal.get returns the insight (the canonical "did the thing actually work" test)
- [ ] Manual: dev server up; force a composting cycle; verify DB row + log line + InsightJournal.get returns it

### Phase 2a: Routing integration tests

**Not applicable** — no intent/handler/classifier changes.

**Question for PM**: confirm 2a inapplicability per audit-cascade.

### Phase 2b: Wiring integration tests (REQUIRED)

Multi-layer data flow → wiring tests required.

- [ ] Test: `CompostingPipeline.process` → real `InsightJournal.add` → real `InsightRepository.add` → DB row exists (no internals mocked)
- [ ] Test: process restart simulation; insights persisted
- [ ] Test: `InsightJournal.get_unsurfaced(user_id=X)` returns DB-backed list

---

## Phase Z: Final Bookending & Handoff

### Required Actions

1. **GitHub Final Update**:
   ```
   ## Status: Complete - Awaiting PM Approval
   - InsightJournal persistent
   - CompostingScheduler running on startup with quiet-hours config
   - All tests passing (paste output)
   - No regressions in existing composting tests
   - #1030/#1031/#1032/#1033 unblocked
   ```

2. **Documentation**:
   - [ ] If ADR-061 needs amendment based on Phase 1 findings, file follow-up
   - [ ] Update relevant code comments cross-referencing #1035 + #1018 pattern
   - [ ] Add migration note to `docs/internal/architecture/current/` if appropriate

3. **Evidence Compilation**:
   - [ ] Test output (Phases 2-7)
   - [ ] Migration apply/revert output
   - [ ] Server startup log showing `composting_scheduler_started`
   - [ ] DB row verification (psql query)

4. **Handoff to #1030/#1031/#1032/#1033**:
   - [ ] Document on each that pre-work is complete; gameplans can assume `InsightJournal` is durable + `CompostingScheduler` is running

5. **Session log**: complete with all Phase outputs

6. **PM Approval Request**:
   ```
   @PM - #1035 complete:
   - Persistent InsightJournal + CompostingScheduler activation
   - Wiring tests verify end-to-end persistence
   - Four downstream issues unblocked
   - ADR-061 alignment verified (or amendment filed)
   ```

---

## Multi-Agent Coordination Plan

Single agent (Lead Dev). Multi-component but tightly coupled — repository + journal + scheduler must coordinate through Lead Dev.

### Verification Gates

- [ ] Phase 1: ADR-061 aligned (no conflicts surfaced, OR amendments filed)
- [ ] Phase 2: Migration applies/reverts; roundtrip tests pass
- [ ] Phase 3: InsightRepository unit tests pass
- [ ] Phase 4: InsightJournal integration tests pass
- [ ] Phase 5: Scheduler-job lifecycle tests pass
- [ ] Phase 2b: End-to-end wiring tests pass
- [ ] Phase Z: Manual server-up smoke test (force composting cycle, verify DB row)

---

## STOP Conditions (apply throughout)

- ADR-061 conflicts → align before proceeding
- Pre-existing composting consumers depend on sync `add()` → may need both sync+async paths
- Migration head conflict → coordinate
- Existing tests fail for reasons unrelated to scope
- `InsightJournal._by_user` / `_by_object` indices reveal hidden API behavior → reassess

---

## Evidence Requirements

- [ ] `pytest` terminal output for Phases 2-7
- [ ] `alembic upgrade head` + `alembic downgrade -1` output
- [ ] Server startup log line: `composting_scheduler_started`
- [ ] `psql` query showing insight rows after manual cycle
- [ ] git diff of all changes

---

## Effort Estimate

**Overall Size**: Large (parallel to #1018 Phase 2 single-day effort)

| Phase | Estimate |
|-------|----------|
| Phase -1 PM walk | 30 min |
| Phase 0 investigation + ADR-061 read | 45 min |
| Phase 0.5 + 0.6 documentation | 30 min |
| Phase 1 ADR-061 alignment | 30 min |
| Phase 2 schema + migration | 1.5 hr |
| Phase 3 repository | 2 hr |
| Phase 4 InsightJournal rewrite | 1.5 hr |
| Phase 5 scheduler job + phase | 1.5 hr |
| Phase 7 tests + verification | 1.5 hr |
| Phase Z bookend + smoke test | 30 min |
| Total | ~10 hr (~1 working day) |

---

## Dependencies

- [x] Phase -1 spike completed
- [ ] PM Phase -1 walkthrough complete
- [ ] ADR-061 v1.0 read (Phase 0/1)

## Blocks

- #1030 MUX-INSIGHT-PULL
- #1031 MUX-INSIGHT-PASSIVE
- #1032 MUX-INSIGHT-PUSH
- #1033 MUX-COMPOSTED-EXPERIENCE

---

# Audit-Cascade: Gameplan vs gameplan-template v9.3

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Phase -1: Infrastructure Verification | ✅ | Filled with spike findings; six PM Qs queued |
| Phase -1: Worktree Assessment | ✅ | USE WORKTREE — multi-component + downstream issues stage on top |
| Phase -1: PM Verification placeholder | ⚠️ | Six explicit Qs need PM walkthrough before Phase 0 |
| Phase 0: GitHub Issue Verification | ✅ | `gh issue view 1035` step included |
| Phase 0: Codebase Investigation | ✅ | grep + alembic-current + collect-only commands listed |
| Phase 0: ADR-061 read step | ✅ | Added per Phase -1 Q4 |
| Phase 0: Update GitHub Issue | ✅ | Status template included |
| Phase 0: STOP Conditions | ✅ | Three named |
| Phase 0.5: Applicability assessment | ✅ | Mixed; new endpoints deferred to #1030/#1031 |
| Phase 0.5: Mount-prefix preflight | ✅ | `/api/v1/insights` namespace verified clean |
| Phase 0.5: Static-file verification | ✅ | N/A — no static files |
| Phase 0.5: STOP Conditions | ✅ | Documented |
| Phase 0.6: Applicability | ✅ | Applies (multi-layer scheduler → pipeline → journal → repo → DB) |
| Phase 0.6: Data Flow Requirements table | ✅ | Layer-by-layer change matrix included |
| Phase 0.6: Integration Points checklist | ✅ | Full caller→callee table |
| Phase 0.6: Pattern Adaptation Notes | ✅ | Explicit #1018-pattern adaptation table; five pitfalls named |
| Phase 0.6: STOP Conditions | ✅ | Three named |
| Phase 0.7: Conversation Design | ⚠️ | Marked inapplicable per template self-description; **PM approval requested** per audit-cascade skill |
| Phase 0.8: Post-Completion Integration | ⚠️ | Marked partially applicable; DB-side present, user-state/downstream not; **PM approval requested** for partial-applicability framing |
| Phases 1-N: Development with progressive bookending | ✅ | Phases 1-7 + 2a + 2b all defined; bookend example included for Phase 1 |
| Phase 2a: Routing integration tests | ⚠️ | Marked N/A — not intent/classifier work; **PM approval requested** |
| Phase 2b: Wiring integration tests | ✅ | Three end-to-end tests specified |
| Phase Z: GitHub Final Update | ✅ | Template included |
| Phase Z: Documentation Updates | ✅ | ADR amendment path documented |
| Phase Z: Evidence Compilation | ✅ | Listed (test out, migration out, log line, psql, diff) |
| Phase Z: Handoff Preparation | ✅ | Four downstream issues documented |
| Phase Z: Session Completion | ✅ | Listed |
| Phase Z: PM Approval Request | ✅ | Template included |
| Multi-Agent Coordination Plan | ✅ | Single-agent justification given (multi-component but tightly coupled) |
| Verification Gates | ✅ | Listed per Phase |
| STOP Conditions (throughout) | ✅ | Section included |
| Evidence Requirements | ✅ | Five evidence items listed |
| Effort Estimate | ✅ | Per-phase breakdown; total ~10hr / 1 working day |
| Dependencies + Blocks | ✅ | Spike + ADR-061 + four downstreams |
| Test Scope (unit/integration/wiring/perf/regression) | ✅ | Wiring tests required (Phase 2b); regression covered (Phase 4); perf not flagged for MVP |

## Action Required Before Proceeding

Items needing PM input before Phase 0:

1. **Phase -1 Qs 1-6** (compost-bin durability, scheduler-loop ownership, migration ordering, ADR-061 dependency, user-scoping, clear semantics)
2. **Phase 0.7 + 0.8 + 2a inapplicability/partial confirmations** per audit-cascade skill

## Status

**Audit cascade gate: ✅ PASSED 2026-05-03.** All items resolved via PM walkthrough.

---

# PM Audit Walkthrough Dispositions (2026-05-03)

| # | Question | PM disposition |
|---|----------|----------------|
| Q1 | CompostBin queue durability: persist (B) or rebuild on startup (A)? | **Option A — rebuild** ("time well spent now"). No `compost_bin` table; queue rebuilds from candidate-objects. |
| Q2 | Scheduler loop ownership: separate `CompostingSchedulerJob` wrapper (A) or loop inside CompostingScheduler (B)? | **Option A** — separate job wrapper. PM: "good to extend working patterns too" (mirrors #1018 `EthicsAuditCleanupJob`) |
| Q3 | Migration ordering coordination needed? | **Proceed** — no other migrations anticipated; chain off `a1018_add_ethics_audit_log` |
| Q4 | ADR-061 v1.0 dependency: wait for formal ratification or proceed on read-and-align? | **PM verbally ratified ADR-061 May 3**; paperwork pending on PM lane. Lead Dev memo to Architect filed (commit `ab5f72c3`). Read-and-align is sufficient. |
| Q5 | User-scoping: partition by user_id from day one even at single-user alpha? | **Yes** — "anything else is a false economy imho" |
| Q6 | `clear()` semantics: per-user (A) or system-wide (B)? | **Per-user** |
| Q7 | Phase 0.7 N/A + Phase 0.8 partial-applicability + Phase 2a N/A confirmations | **All confirmed** |
