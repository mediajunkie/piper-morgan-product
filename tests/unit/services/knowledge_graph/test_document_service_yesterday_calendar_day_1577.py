"""Issue #1577 (time audit F3e) — document_service's 'yesterday' must be the
previous CALENDAR day, not a rolling now-24h window.

Pre-fix, ``find_decisions``/``get_relevant_context`` each computed
``timeframe_start = now - timedelta(days=1)`` locally: at any time other than
exact midnight this clips part of the previous calendar day (and disagreed
with ``temporal_utils.parse_relative_date``'s 'today', which the rest of the
intent-routing stack treats as canonical — #1572).

Fixed 'now' = 2026-09-23 00:30 UTC (TZ pinned to UTC so the server-anchor
fallback is deterministic, mirroring test_user_timezone_1572.py's pattern):
  - OLD (now-24h):        2026-09-22 00:30:00 UTC  (30 min INTO yesterday —
    the first half hour of the previous calendar day is silently excluded)
  - NEW (calendar day):   2026-09-22 00:00:00 UTC  (the whole previous day)

Both entry points (find_decisions' explicit "yesterday" and
get_relevant_context's default) are pinned so a regression in either
reintroduces the "same query, different answer by entry path" bug the issue
is about.
"""

from __future__ import annotations

import os
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

import services.intent_service.temporal_utils as temporal_utils  # noqa: E402
from services.database.models import DocumentDB  # noqa: E402
from services.knowledge_graph.document_service import DocumentService  # noqa: E402

pytestmark = pytest.mark.asyncio

FIXED_UTC = datetime(2026, 9, 23, 0, 30, tzinfo=timezone.utc)

_EXPECTED_YESTERDAY_START = datetime(2026, 9, 22, 0, 0, tzinfo=timezone.utc).timestamp()
_BUGGY_NOW_MINUS_24H = datetime(2026, 9, 22, 0, 30, tzinfo=timezone.utc).timestamp()


class _FixedDatetime(datetime):
    """Pins temporal_utils' `datetime.now()` to FIXED_UTC (same pattern as
    test_user_timezone_1572.py's _FixedDatetime)."""

    @classmethod
    def now(cls, tz=None):
        if tz is not None:
            return FIXED_UTC.astimezone(tz)
        return FIXED_UTC


@pytest.fixture
def frozen_clock(monkeypatch):
    monkeypatch.setattr(temporal_utils, "datetime", _FixedDatetime)
    yield FIXED_UTC


@pytest.fixture
def utc_server():
    """Pin the server-local zone to UTC so the no-tz fallback anchor is
    deterministic on any dev machine (mirrors test_user_timezone_1572.py)."""
    old = os.environ.get("TZ")
    os.environ["TZ"] = "UTC"
    time.tzset()
    yield
    if old is None:
        os.environ.pop("TZ", None)
    else:
        os.environ["TZ"] = old
    time.tzset()


class _RecordingCollection:
    """Fake ChromaDB collection that records the `where` filter of every
    `.query()` call and returns an empty (but well-shaped) result set."""

    def __init__(self):
        self.calls = []

    def query(self, **kwargs):
        self.calls.append(kwargs)
        return {"ids": [[]], "documents": [[]], "metadatas": [[]], "distances": [[]]}

    @property
    def last_gte(self) -> float:
        return self.calls[-1]["where"]["analysis_timestamp"]["$gte"]


class _FakeIngester:
    def __init__(self):
        self.collection = _RecordingCollection()


@pytest_asyncio.fixture
async def svc():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: DocumentDB.__table__.create(c, checkfirst=True))
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @asynccontextmanager
    async def scope():
        async with SessionLocal() as s:
            yield s
            await s.commit()

    ingester = _FakeIngester()
    service = DocumentService(session_scope=scope, ingester=ingester)
    yield service, ingester
    await engine.dispose()


class TestYesterdayIsCalendarDayNotRolling24h1577:
    async def test_find_decisions_yesterday_is_previous_calendar_midnight(
        self, svc, frozen_clock, utc_server
    ):
        """RED before the fix: old code passed now-24h (00:30 UTC, 30 minutes
        INTO the previous day) as the lower bound; the previous calendar day's
        first 30 minutes were silently excluded from 'yesterday'."""
        service, ingester = svc
        await service.find_decisions(topic="", timeframe="yesterday", owner_id=None)

        gte = ingester.collection.last_gte
        assert gte == pytest.approx(_EXPECTED_YESTERDAY_START), (
            f"expected calendar-day midnight {_EXPECTED_YESTERDAY_START}, got {gte} "
            f"(now-24h would give {_BUGGY_NOW_MINUS_24H})"
        )
        assert gte != pytest.approx(_BUGGY_NOW_MINUS_24H)

    async def test_get_relevant_context_default_yesterday_matches_find_decisions(
        self, svc, frozen_clock, utc_server
    ):
        """The other entry point (default timeframe="yesterday") must resolve
        to the SAME instant as find_decisions' explicit "yesterday" — the
        audit's 'same query, different answers by entry path' bug, closed."""
        service, ingester = svc
        await service.get_relevant_context(owner_id=None)  # default timeframe

        gte = ingester.collection.last_gte
        assert gte == pytest.approx(_EXPECTED_YESTERDAY_START)
        assert gte != pytest.approx(_BUGGY_NOW_MINUS_24H)

    async def test_get_relevant_context_explicit_yesterday_matches_default(
        self, svc, frozen_clock, utc_server
    ):
        service, ingester = svc
        await service.get_relevant_context(timeframe="yesterday", owner_id=None)

        gte = ingester.collection.last_gte
        assert gte == pytest.approx(_EXPECTED_YESTERDAY_START)

    async def test_today_is_calendar_midnight_today(self, svc, frozen_clock, utc_server):
        """Sanity check: 'today' (already correct pre-fix) is unchanged by the
        refactor — both entry points now share _calendar_today_start."""
        service, ingester = svc
        expected_today = datetime(2026, 9, 23, 0, 0, tzinfo=timezone.utc).timestamp()

        await service.find_decisions(topic="", timeframe="today", owner_id=None)
        assert ingester.collection.last_gte == pytest.approx(expected_today)

        await service.get_relevant_context(timeframe="today", owner_id=None)
        assert ingester.collection.last_gte == pytest.approx(expected_today)
