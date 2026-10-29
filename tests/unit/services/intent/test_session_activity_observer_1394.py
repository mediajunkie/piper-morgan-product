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


class TestObserverRetitles:
    """#2201: a rename of something this session created updates the ledger
    row's title (owner-scoped), so the session recap shows the new name."""

    def _retitled_result(
        self, ref="mediajunkie/test-piper-morgan#107", title="Fix the sign-in bug"
    ):
        return IntentProcessingResult(
            success=True,
            message=f"Updated issue #107: {title}",
            intent_data={
                "action": "update_issue",
                "issue_number": 107,
                "retitled_activity": {"target_ref": ref, "target_title": title},
            },
        )

    async def test_rename_retitles_the_created_row(self, sm):
        await IntentService._record_session_activity(
            _observer_self(), session_id=_CONV, user_id=_USER, result=_created_issue_result()
        )
        await IntentService._record_session_activity(
            _observer_self(), session_id=_CONV, user_id=_USER, result=self._retitled_result()
        )
        async with sm() as s:
            rows = await SessionActivityRepository(s).list_for_session(_USER, _CONV)
        assert len(rows) == 1
        assert rows[0].target_title == "Fix the sign-in bug"
        assert rows[0].action_type == "issue_created"

    async def test_rename_by_another_owner_leaves_the_row_alone(self, sm):
        await IntentService._record_session_activity(
            _observer_self(), session_id=_CONV, user_id=_USER, result=_created_issue_result()
        )
        await IntentService._record_session_activity(
            _observer_self(),
            session_id=_CONV,
            user_id="someone-else",
            result=self._retitled_result(),
        )
        async with sm() as s:
            rows = await SessionActivityRepository(s).list_for_session(_USER, _CONV)
        assert rows[0].target_title == "Fix the login bug"

    async def test_rename_of_a_ref_this_session_did_not_create_writes_nothing(self, sm):
        await IntentService._record_session_activity(
            _observer_self(),
            session_id=_CONV,
            user_id=_USER,
            result=self._retitled_result(ref="mediajunkie/test-piper-morgan#999"),
        )
        async with sm() as s:
            rows = await SessionActivityRepository(s).list_for_session(_USER, _CONV)
        assert rows == []


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
