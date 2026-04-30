---
from: Lead Developer
to: Chief Architect
cc: CEO (xian), PA, exec (Chief of Staff)
date: 2026-04-30
subject: #1018 Phase 1 design ready for review — three open questions for your call
priority: normal
response-requested: Architect — review at convenience; ratification + 3 open-questions calls when ready
---

# #1018 Phase 1 Design — Ready for Architect Review

Phase 1 design draft committed to main:

**File**: `dev/2026/04/30/1018-phase-1-design.md` (commit on origin/main as part of today's batch)

## What's in it

Coverage per #1018 Phase 1 spec:
- **Storage shape**: `ethics_audit_log` table schema + 4 indexes matching actual query patterns from `audit_transparency.py`. JSONB for `details`. UUID `user_id` (no FK, matches existing `audit_logs` precedent).
- **SQLAlchemy model**: `EthicsAuditLogDB(Base, TimestampMixin)` next to existing `AuditLog` at `services/database/models.py:204`. Deliberately distinct table — `audit_logs` is security/auth, `ethics_audit_log` is ethics decisions; separate concerns.
- **Domain boundary**: existing `AuditLogEntry` dataclass stays as the domain shape; DB model maps via `from_domain()` / `to_domain()` (matches `UploadedFileDB` precedent).
- **Write path**: synchronous DB write inside `log_ethics_decision()` and `log_boundary_violation()`. Recommended over async queue because volume is per-request and write latency is well within the <10ms target.
- **Read path**: existing transparency endpoints stay shape-stable; internals shift from in-memory list filter to `EthicsAuditRepository` with indexed DB queries. Frontend unaffected.
- **Repository**: new `services/database/repositories/ethics_audit_repository.py` with `add`, `find_by_session`, `find_by_user`, `summarize_recent`, `delete_older_than`, `count`. Follows existing `BaseRepository` pattern.
- **Retention**: replace on-demand `cleanup_old_entries()` with `EthicsAuditCleanupJob` scheduled job (24h interval, follows `BlacklistCleanupJob` pattern, includes the post-#948 task-cancellation hygiene).
- **Migration**: single alembic up/down covering table + 4 indexes. No backfill needed.
- **Cluster regression targets**: #1006 / #1007 / #1008 explicitly mapped to Phase 2 acceptance criteria with verification approach for each.

## Three open questions for your call

1. **Repository directory restructure**: Today there's `services/database/repositories.py` (flat) + `services/repositories/file_repository.py` (singleton in services/repositories/). I'd add `services/database/repositories/ethics_audit_repository.py` (creating the subdir). Land that restructure as part of Phase 2, or defer? My lean: defer — smaller Phase 2 surface.

2. **Session lifecycle**: `audit_transparency.log_ethics_decision()` is called from `boundary_enforcer_refactored.py:340` (`await audit_transparency.log_ethics_decision(decision)`). The caller doesn't have a DB session today. I'd open one inside `log_ethics_decision()` via `AsyncSessionFactory()` context manager. Acceptable, or should we plumb a session through the call chain so the audit write joins the request transaction?

3. **Adaptive boundaries integration timing**: `services/ethics/adaptive_boundaries.py` reads the in-memory audit list to compute pattern frequencies. Once `ethics_audit_log` is durable, adaptive_boundaries can finally accumulate confidence scores across restarts. Land that retarget in Phase 3 of #1018, or file as separate follow-up? My lean: separate follow-up, because adaptive_boundaries' read pattern wants additional aggregation queries beyond Phase 1's repository surface.

## What I'm NOT asking

- No commitment to Phase 2 timeline. Phase 2 is ~2-3 days when scheduled.
- No re-litigation of #1006/#1007/#1008 cluster sequencing — Phase 2 acceptance criteria already explicitly verifies each per my Apr 28 cluster memo.
- No premature implementation. Awaiting your ratification + the three open-questions calls before starting Phase 2.

## What's next

- Architect ratifies Phase 1 design (with whatever adjustments you flag).
- Lead Dev kicks off Phase 2 implementation when calendar allows.
- Phase 2 ship closes #1018 + #1006 + #1007 + #1008 with linked regression evidence.

— Lead Developer, 2026-04-30 7:35 AM PT
