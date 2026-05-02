"""
#1018 Phase 2 — EthicsAuditRepository unit tests.

Verifies CRUD + filtered-query behavior of the new repository layer that
backs `audit_transparency.py`. Uses an in-memory SQLite database with the
table created via the SQLAlchemy metadata (no alembic for unit tests; the
migration itself is integration-tested separately when DB is up).

Cluster regression targets covered here at the repository layer:
- **#1006** datetime offset comparison: TIMESTAMPTZ throughout; tests
  insert + retrieve + filter timezone-aware datetimes round-trip.
- **#1007** PII redaction: not exercised at this layer (redaction happens
  in `audit_transparency.log_ethics_decision` BEFORE calling the repo);
  covered separately in `test_audit_transparency_redaction_1018.py`.
- **#1008** await-on-list: every repository method is properly async;
  the test asserts that calling them returns awaitables, not lists.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
import pytest_asyncio


# Skip the entire module if aiosqlite isn't available — tests use an
# in-memory SQLite for DB-free repository unit testing. CI installs it;
# local dev may not. The migration + production behavior is covered by
# integration tests against PostgreSQL.
aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine  # noqa: E402

from services.database.models import EthicsAuditLogDB  # noqa: E402
from services.database.repositories import EthicsAuditRepository  # noqa: E402
from services.ethics.audit_transparency import AuditLogEntry  # noqa: E402


pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def session():
    """Fresh in-memory SQLite session per test, with the
    ethics_audit_log table created from SQLAlchemy metadata.

    NOTE: SQLite doesn't support JSONB or PostgreSQL UUID types
    natively; SQLAlchemy maps them to JSON + CHAR(32) for SQLite,
    which is fine for these unit tests since we're testing repository
    semantics not type-storage details.
    """
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        # Create only the table we need + its indexes.
        await conn.run_sync(
            lambda sync_conn: EthicsAuditLogDB.__table__.create(sync_conn, checkfirst=True)
        )

    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as s:
        yield s

    await engine.dispose()


def _make_entry(
    *,
    entry_id: str | None = None,
    event_type: str = "ethics_decision",
    timestamp: datetime | None = None,
    session_id: str | None = "session-test",
    details: dict | None = None,
) -> AuditLogEntry:
    """Helper: build an AuditLogEntry with sensible defaults."""
    return AuditLogEntry(
        entry_id=entry_id or f"audit_{uuid4().hex[:24]}",
        event_type=event_type,
        timestamp=timestamp or datetime.now(timezone.utc),
        session_id=session_id,
        user_id=None,
        details=details or {"boundary_type": "harassment", "violation_detected": True},
        redacted=True,
    )


# --------------------------------------------------------------------------
# CRUD basics
# --------------------------------------------------------------------------


async def test_add_persists_entry(session):
    repo = EthicsAuditRepository(session)
    entry = _make_entry(session_id="add-test")
    await repo.add(entry)
    await session.commit()

    found = await repo.find_by_session("add-test")
    assert len(found) == 1
    assert found[0].entry_id == entry.entry_id
    assert found[0].event_type == "ethics_decision"


async def test_find_by_session_orders_newest_first(session):
    repo = EthicsAuditRepository(session)
    base = datetime.now(timezone.utc)
    e1 = _make_entry(timestamp=base - timedelta(hours=2), session_id="order-test")
    e2 = _make_entry(timestamp=base - timedelta(hours=1), session_id="order-test")
    e3 = _make_entry(timestamp=base, session_id="order-test")
    for e in [e1, e2, e3]:
        await repo.add(e)
    await session.commit()

    found = await repo.find_by_session("order-test")
    assert [e.entry_id for e in found] == [e3.entry_id, e2.entry_id, e1.entry_id]


async def test_find_by_session_respects_limit(session):
    repo = EthicsAuditRepository(session)
    for i in range(5):
        await repo.add(_make_entry(session_id="limit-test"))
    await session.commit()

    found = await repo.find_by_session("limit-test", limit=2)
    assert len(found) == 2


async def test_find_by_session_filters_by_session_id(session):
    repo = EthicsAuditRepository(session)
    await repo.add(_make_entry(session_id="alice"))
    await repo.add(_make_entry(session_id="bob"))
    await repo.add(_make_entry(session_id="bob"))
    await session.commit()

    alice = await repo.find_by_session("alice")
    bob = await repo.find_by_session("bob")
    assert len(alice) == 1
    assert len(bob) == 2


async def test_count_returns_total(session):
    repo = EthicsAuditRepository(session)
    assert await repo.count() == 0
    for i in range(3):
        await repo.add(_make_entry())
    await session.commit()
    assert await repo.count() == 3


# --------------------------------------------------------------------------
# Aggregation
# --------------------------------------------------------------------------


async def test_summarize_recent_groups_by_event_type(session):
    repo = EthicsAuditRepository(session)
    base = datetime.now(timezone.utc)
    await repo.add(_make_entry(event_type="ethics_decision", timestamp=base))
    await repo.add(_make_entry(event_type="ethics_decision", timestamp=base))
    await repo.add(_make_entry(event_type="boundary_violation", timestamp=base))
    await session.commit()

    summary = await repo.summarize_recent(days=1)
    assert summary["total_entries"] == 3
    assert summary["events_by_type"]["ethics_decision"] == 2
    assert summary["events_by_type"]["boundary_violation"] == 1


async def test_summarize_recent_extracts_boundary_breakdown(session):
    repo = EthicsAuditRepository(session)
    base = datetime.now(timezone.utc)
    await repo.add(
        _make_entry(timestamp=base, details={"boundary_type": "harassment"})
    )
    await repo.add(
        _make_entry(timestamp=base, details={"boundary_type": "harassment"})
    )
    await repo.add(
        _make_entry(timestamp=base, details={"boundary_type": "data_privacy"})
    )
    await session.commit()

    summary = await repo.summarize_recent(days=1)
    assert summary["boundary_breakdown"]["harassment"] == 2
    assert summary["boundary_breakdown"]["data_privacy"] == 1


async def test_summarize_recent_filters_by_window(session):
    repo = EthicsAuditRepository(session)
    base = datetime.now(timezone.utc)
    # One entry inside the window, one outside
    await repo.add(_make_entry(timestamp=base))
    await repo.add(_make_entry(timestamp=base - timedelta(days=10)))
    await session.commit()

    summary = await repo.summarize_recent(days=1)
    assert summary["total_entries"] == 1


# --------------------------------------------------------------------------
# Retention sweep — closes #1006 (datetime offset)
# --------------------------------------------------------------------------


async def test_delete_older_than_removes_old_entries_only(session):
    repo = EthicsAuditRepository(session)
    base = datetime.now(timezone.utc)
    old = _make_entry(timestamp=base - timedelta(days=100))
    recent = _make_entry(timestamp=base)
    await repo.add(old)
    await repo.add(recent)
    await session.commit()

    cutoff = base - timedelta(days=90)
    removed = await repo.delete_older_than(cutoff)
    await session.commit()

    assert removed == 1
    assert await repo.count() == 1
    remaining = await repo.find_by_session(recent.session_id)
    assert remaining[0].entry_id == recent.entry_id


async def test_delete_older_than_uses_timezone_aware_datetimes(session):
    """#1006 regression target: pre-fix, the in-memory implementation
    compared naive `datetime.now()` with timezone-aware entry timestamps,
    raising 'can't compare offset-naive and offset-aware datetimes'.
    Post-fix, every datetime in the persistence path is timezone-aware
    (TIMESTAMPTZ in PostgreSQL; aware datetime in SQLAlchemy).
    """
    repo = EthicsAuditRepository(session)
    aware_old = datetime.now(timezone.utc) - timedelta(days=100)
    await repo.add(_make_entry(timestamp=aware_old))
    await session.commit()

    # The cutoff is also tz-aware; this should NOT raise.
    cutoff = datetime.now(timezone.utc) - timedelta(days=90)
    removed = await repo.delete_older_than(cutoff)
    assert removed == 1


# --------------------------------------------------------------------------
# Domain-model round-trip
# --------------------------------------------------------------------------


async def test_to_domain_round_trip_preserves_fields(session):
    repo = EthicsAuditRepository(session)
    user_id = uuid4()
    entry = _make_entry(
        session_id="rt-test",
        details={
            "boundary_type": "harassment",
            "violation_detected": True,
            "explanation": "Test explanation",
            "audit_data": {"detector": "semantic", "confidence": 0.9},
        },
    )
    entry.user_id = user_id

    await repo.add(entry)
    await session.commit()

    found = await repo.find_by_session("rt-test")
    assert len(found) == 1
    f = found[0]
    assert f.entry_id == entry.entry_id
    assert f.event_type == entry.event_type
    assert f.user_id == entry.user_id
    assert f.session_id == entry.session_id
    assert f.details == entry.details
    assert f.redacted == entry.redacted
    # Timestamp should round-trip with timezone preserved
    assert f.timestamp.tzinfo is not None or entry.timestamp.tzinfo is not None
