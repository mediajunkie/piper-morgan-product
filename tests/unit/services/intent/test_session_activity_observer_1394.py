"""ADR-078 OQ-3 (#1394) — the central observer records external creations to the ledger.

The observer at the #1122 turn-recording seam reads a handler's uniform
``intent_data['created_activity']`` and writes ONE owner-scoped session_activity row.
Handlers stay ledger-ignorant. D1a: no principal → no row (never owner-less).
"""

import contextlib
import types
from unittest.mock import MagicMock

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.database.models import SessionActivityDB  # noqa: E402
from services.database.repositories import SessionActivityRepository  # noqa: E402
from services.intent.intent_service import IntentProcessingResult, IntentService  # noqa: E402

pytestmark = pytest.mark.asyncio

_CONV = "conv-obs-1"
_USER = "owner-obs"


@pytest_asyncio.fixture
async def sm(monkeypatch):
    """In-memory ledger store; patch AsyncSessionFactory.session_scope to use it."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: SessionActivityDB.__table__.create(c, checkfirst=True))
    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _scope():
        async with maker() as s:
            yield s

    import services.database.session_factory as sf

    monkeypatch.setattr(sf.AsyncSessionFactory, "session_scope", staticmethod(_scope))
    yield maker
    await engine.dispose()


def _observer_self():
    return types.SimpleNamespace(logger=MagicMock())


def _created_issue_result():
    return IntentProcessingResult(
        success=True,
        message="Created issue #107 in test-piper-morgan: Fix the login bug",
        intent_data={
            "action": "create_issue",
            "issue_number": 107,
            "created_activity": {
                "action_type": "issue_created",
                "target_ref": "mediajunkie/test-piper-morgan#107",
                "target_title": "Fix the login bug",
            },
        },
    )


class TestObserverWrites:
    async def test_created_issue_writes_one_ledger_row(self, sm):
        await IntentService._record_session_activity(
            _observer_self(), session_id=_CONV, user_id=_USER, result=_created_issue_result()
        )
        async with sm() as s:
            rows = await SessionActivityRepository(s).list_for_session(_USER, _CONV)
        assert len(rows) == 1
        assert rows[0].action_type == "issue_created"
        assert rows[0].target_ref == "mediajunkie/test-piper-morgan#107"
        assert rows[0].target_title == "Fix the login bug"
        assert rows[0].owner_id == _USER


class TestObserverGuards:
    async def test_no_principal_writes_nothing(self, sm):
        """D1a — an owner-less result must never create a ledger row."""
        await IntentService._record_session_activity(
            _observer_self(), session_id=_CONV, user_id=None, result=_created_issue_result()
        )
        async with sm() as s:
            # read with any owner: the table is empty
            rows = await SessionActivityRepository(s).list_for_session(_USER, _CONV)
        assert rows == []

    async def test_no_created_activity_writes_nothing(self, sm):
        plain = IntentProcessingResult(
            success=True, message="Here's your answer.", intent_data={"action": "query"}
        )
        await IntentService._record_session_activity(
            _observer_self(), session_id=_CONV, user_id=_USER, result=plain
        )
        async with sm() as s:
            rows = await SessionActivityRepository(s).list_for_session(_USER, _CONV)
        assert rows == []
