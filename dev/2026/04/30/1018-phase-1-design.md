# #1018 Phase 1 Design — Ethics Audit Log Durability

**Status**: Phase 1 design draft, for Architect review
**Author**: Lead Developer
**Date**: 2026-04-30
**Issue**: #1018 ARCH-CLEANUP: Persist ethics audit log to durable storage
**Cluster**: regression targets #1006, #1007, #1008 — verify each as part of Phase 2 acceptance

---

## Problem statement (one paragraph)

`services/ethics/audit_transparency.py` stores ethics audit entries in an in-memory Python list (`self.audit_logs: List[AuditLogEntry]`, max 10,000 entries, 90-day TTL via `cleanup_old_entries()`). All entries are lost on process restart. The user-facing transparency endpoints at `services/api/transparency.py` read from this list, so they can lie after any deploy or crash. `services/ethics/adaptive_boundaries.py` reads the same list to compute pattern frequencies, so confidence scoring resets every restart. Phase 1 specifies the durable replacement.

---

## Storage shape

### New table `ethics_audit_log`

Direct mapping from the existing `AuditLogEntry` dataclass at `services/ethics/audit_transparency.py:63`. Schema:

| Column | Type | Constraint | Notes |
|---|---|---|---|
| `entry_id` | `String(64)` | PK | Existing format `audit_{unix_ts}`; UUID for new entries (collision-resistant). |
| `event_type` | `String(50)` | NOT NULL, index | `ethics_decision` \| `boundary_violation` (today's two values). |
| `timestamp` | `TIMESTAMPTZ` | NOT NULL, index | Decision/violation time. Index for retention sweep + recent-N queries. |
| `session_id` | `String(255)` | nullable, index | For per-session queries (transparency endpoints). |
| `user_id` | `UUID` | nullable, index | For per-user queries; matches existing `audit_logs.user_id` shape (no FK to `users` so audit survives user deletion). |
| `details` | `JSONB` | NOT NULL | Redacted detail payload. JSONB (not JSON) for query performance + index support. |
| `redacted` | `Boolean` | NOT NULL, default `True` | Matches existing `AuditLogEntry.redacted` flag. |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, default `now()` | Insertion time (separate from `timestamp` which is event time). Used by retention sweep to avoid edge cases when `timestamp` is back-dated. |

### Indexes

```sql
CREATE INDEX idx_ethics_audit_session ON ethics_audit_log (session_id);
CREATE INDEX idx_ethics_audit_user_time ON ethics_audit_log (user_id, timestamp DESC);
CREATE INDEX idx_ethics_audit_event_time ON ethics_audit_log (event_type, timestamp DESC);
CREATE INDEX idx_ethics_audit_timestamp ON ethics_audit_log (timestamp);
```

The composite indexes match the actual query patterns in `audit_transparency.py`:
- `get_user_audit_log(session_id)` → `idx_ethics_audit_session`
- `get_system_audit_summary(days)` filters by recent timestamp → `idx_ethics_audit_event_time`
- Retention sweep filters by old `timestamp` → `idx_ethics_audit_timestamp`

### SQLAlchemy model placement

Add `EthicsAuditLogDB(Base, TimestampMixin)` to `services/database/models.py` (next to existing `AuditLog` class at line 204; deliberately distinct table — `audit_logs` is for security/auth events, `ethics_audit_log` is for ethics decisions; the two surfaces have different schemas, different access patterns, different retention).

### Domain model boundary

Existing `AuditLogEntry` dataclass at `services/ethics/audit_transparency.py:63` stays as the domain shape. The DB model maps to/from it via `from_domain()` / `to_domain()` class methods (matches `UploadedFileDB` precedent at `services/database/models.py:773`).

---

## Write path

**Recommendation**: synchronous DB write inside `log_ethics_decision()` and `log_boundary_violation()`.

### Why synchronous (not async queue)

- Per-request, per-decision: at most one ethics-decision write per user request. Volume is low (P1 estimate: <100 writes/min at small scale; <1k/min at any plausible product trajectory).
- DB write latency: PostgreSQL INSERT on a single-row JSONB column with indexed columns is ~1-3ms locally, ~5-10ms over network. **Within the <10ms target in #1018 acceptance criteria #8.**
- Async queue introduces complexity (queue backpressure, dropped messages on shutdown, worker lifecycle) that isn't justified at this scale.
- If ethics-decision write rate ever materially grows, queue can be added without changing the public API of `log_ethics_decision()`.

### Failure mode

Per the existing pattern (`audit_transparency.py:149-155`), `log_ethics_decision()` already swallows exceptions and records a metric — it never raises into the request path. The DB-write version inherits that behavior: on `IntegrityError`, `OperationalError`, etc., log + emit failure metric, continue. The ethics decision still applies; only the durability of the audit record is at risk in the (rare) failure case.

### Code shape

```python
# services/ethics/audit_transparency.py
async def log_ethics_decision(self, decision: EthicalDecision) -> None:
    try:
        entry = AuditLogEntry(...)  # domain model unchanged
        async with AsyncSessionFactory() as session:
            db_entry = EthicsAuditLogDB.from_domain(entry)
            session.add(db_entry)
            await session.commit()
        # metrics + behavior_pattern logging unchanged
    except Exception as e:
        self.metrics.record_audit_trail_entry(success=False)
        self.ethics_logger.log_boundary_violation("audit_log_error", {...})
```

Note: the existing in-memory `_add_audit_entry()` + `self.audit_logs` list is removed in Phase 2. Phase 1 does not address that yet — Phase 1 is design only.

---

## Read path

### Transparency endpoints (`services/api/transparency.py`)

Existing endpoints stay shape-stable; their internals shift from `audit_transparency.get_user_audit_log()` (in-memory list filter) to `EthicsAuditRepository.find_by_session(session_id, limit=50)` (indexed DB query).

| Endpoint | Current call | New call |
|---|---|---|
| `GET /transparency/audit-log/{session_id}` | `audit_transparency.get_user_audit_log(session_id, limit)` | `repo.find_by_session(session_id, limit)` |
| `GET /transparency/audit-summary/{session_id}` | `audit_transparency.get_system_audit_summary(days)` | `repo.summarize_recent(days)` |
| `GET /transparency/stats` | `audit_transparency.get_transparency_stats()` | metrics from repo `count()` + in-memory counters that survive (transparency_requests, redaction_operations, etc.) |
| `POST /transparency/cleanup` | `audit_transparency.cleanup_old_entries()` | `repo.delete_older_than(now - timedelta(days=90))` |

Response shape unchanged — `AuditLogEntry.to_dict()` + the existing Pydantic response models on the endpoints. Frontend isn't affected.

### Repository

New module: `services/database/repositories/ethics_audit_repository.py` (creating the repositories/ subdir; today there's only `services/database/repositories.py` flat file plus a `services/repositories/file_repository.py` reference instance). I'd lean toward keeping all DB repositories under `services/database/repositories/` going forward — Architect's call on whether to land that restructure as part of Phase 2 or defer.

Methods:
- `add(entry: AuditLogEntry) -> None`
- `find_by_session(session_id: str, limit: int = 50) -> List[AuditLogEntry]`
- `find_by_user(user_id: UUID, limit: int = 50) -> List[AuditLogEntry]`
- `summarize_recent(days: int = 30) -> Dict[str, Any]` — aggregation query (count by event_type, count by boundary_type, etc.)
- `delete_older_than(cutoff: datetime) -> int` — returns count deleted
- `count() -> int`

Follows the existing `BaseRepository` pattern at `services/database/repositories.py`. Session managed by caller for callers that already have one; `AsyncSessionFactory()` context manager for callers (like `audit_transparency.py`) that don't.

---

## Retention policy

Replace the on-demand `cleanup_old_entries()` method with a scheduled job following the `BlacklistCleanupJob` pattern (`services/scheduler/blacklist_cleanup_job.py`).

### `EthicsAuditCleanupJob`

- `interval_hours = 24` (matches BlacklistCleanupJob default)
- Each run executes `repo.delete_older_than(now() - timedelta(days=90))`
- Same start/stop pattern (post-#948 fix: `asyncio.current_task()` capture in `start()`, cancel + await in `stop()`)
- Wired into `web/startup.py` lifespan, alongside `BackgroundCleanupPhase` and `AttentionDecayPhase` — likely a new `EthicsAuditCleanupPhase` class

### Manual trigger

Existing `POST /transparency/cleanup` endpoint preserved; instead of calling the in-memory cleanup, it triggers an immediate `repo.delete_older_than()` call (synchronously, so the response confirms the delete count). Useful for ops + tests.

---

## Migration

Single alembic migration adding the `ethics_audit_log` table + indexes.

### Migration shape

```python
# alembic/versions/{hash}_add_ethics_audit_log.py
def upgrade():
    op.create_table(
        "ethics_audit_log",
        sa.Column("entry_id", sa.String(64), primary_key=True),
        sa.Column("event_type", sa.String(50), nullable=False),
        sa.Column("timestamp", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("session_id", sa.String(255), nullable=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("details", postgresql.JSONB, nullable=False),
        sa.Column("redacted", sa.Boolean, nullable=False, default=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("idx_ethics_audit_session", "ethics_audit_log", ["session_id"])
    op.create_index(
        "idx_ethics_audit_user_time",
        "ethics_audit_log",
        ["user_id", sa.text("timestamp DESC")],
    )
    op.create_index(
        "idx_ethics_audit_event_time",
        "ethics_audit_log",
        ["event_type", sa.text("timestamp DESC")],
    )
    op.create_index("idx_ethics_audit_timestamp", "ethics_audit_log", ["timestamp"])

def downgrade():
    op.drop_index("idx_ethics_audit_timestamp", "ethics_audit_log")
    op.drop_index("idx_ethics_audit_event_time", "ethics_audit_log")
    op.drop_index("idx_ethics_audit_user_time", "ethics_audit_log")
    op.drop_index("idx_ethics_audit_session", "ethics_audit_log")
    op.drop_table("ethics_audit_log")
```

### Backfill

N/A — no historical data to preserve (per #1018 issue body). Deployment proceeds: migration creates empty table; first ethics decision after deploy starts populating it.

---

## Cluster regression targets (#1006, #1007, #1008)

Per my Apr 28 cluster overlap memo, the three audit_transparency bugs become regression targets in Phase 2 acceptance criteria:

| Bug | Phase 2 AC verification |
|---|---|
| #1006 datetime offset comparison crash | New code uses TIMESTAMPTZ throughout; no naive-datetime comparisons. Covered by repository unit tests asserting timezone-aware datetimes round-trip cleanly. |
| #1007 PII redaction not applied | Redaction logic continues to run in `log_ethics_decision()` before DB write (`SecurityRedactor` is unchanged). Covered by integration test that writes a decision with PII-shaped strings + reads back via endpoint, asserting `[REDACTED]` markers present. |
| #1008 transparency API await-on-list | New endpoint code is end-to-end async with proper `await session.execute(...)`. Covered by existing endpoint tests post-rewrite. |

On Phase 2 ship: close all four issues with linked regression-test evidence (repo unit tests, integration tests, endpoint tests).

---

## What this design does NOT decide

- **Repository directory layout** (`services/database/repositories/` subdir vs. flat `services/database/repositories.py`). Architect's call; Phase 2 starts with the simpler flat path unless a restructure is desired.
- **Phase 2 sequencing** (migration first vs. repository code first vs. parallel). Implementation order; not a design question.
- **Multi-region durability / replication** — out of #1018 scope per issue body.
- **User-facing UI** for transparency — separate product question per issue body.
- **`adaptive_boundaries.py` integration timing** — adaptive_boundaries reads from `audit_logs` today; once `ethics_audit_log` is durable, adaptive_boundaries can be retargeted in a later phase. Not part of Phase 2 scope; flagged for follow-up.

---

## Sequencing

| Phase | Work | Sizing | Status |
|---|---|---|---|
| **Phase 1** | This design doc + Architect review + ratification | ~half-day to a day | **Awaiting review** |
| **Phase 2** | Alembic migration + EthicsAuditLogDB model + EthicsAuditRepository + audit_transparency.py rewrite + transparency.py endpoint update + EthicsAuditCleanupJob + tests | ~2-3 days | Pending Phase 1 ratification |
| **Phase 3** | Manual restart-survival test + performance verification + adaptive_boundaries integration timing decision | ~1 day | Pending Phase 2 ship |

Closes #1018, #1006, #1007, #1008 on Phase 2 ship.

---

## Open questions for Architect

1. **Repository directory restructure** — land in Phase 2 or defer? Lead lean: defer (smaller Phase 2 surface).
2. **`AsyncSessionFactory()` vs caller-provided session** — `audit_transparency.py` is called from `boundary_enforcer_refactored.py:340` (`await audit_transparency.log_ethics_decision(decision)`) which doesn't have a session today. Acceptable to open one in `log_ethics_decision()`, or should we plumb a session through the call chain?
3. **Adaptive boundaries integration timing** — Phase 3 or separate issue? My read: separate issue, since adaptive_boundaries' read pattern (pattern frequencies across time) wants additional aggregation queries that aren't in Phase 1's repository surface.

— Lead Developer, 2026-04-30 7:30 AM PT
