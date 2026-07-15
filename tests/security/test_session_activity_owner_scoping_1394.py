"""ADR-078 D1a (#1394) — the session_activity ledger is owner-scoped BY CONSTRUCTION.

The non-negotiable Arch/HOST requirement: a second user's activity must NEVER be
returned, even within the SAME conversation. `SessionActivityRepository.list_for_session`
requires owner_id and always filters on it, so cross-user resolution is unexpressible —
an unscoped ledger read would be a #1366 / ADR-071-class cross-user leak into another
user's resolution context.
"""

import contextlib  # noqa: F401  (kept for parity with sibling async fixtures)

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

pytestmark = pytest.mark.asyncio

_CONV = "conv-shared-1"
_USER_A = "user-a"
_USER_B = "user-b"


@pytest_asyncio.fixture
async def sm():
    """In-memory session_activity store; the repo runs its real owner-scoped query."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: SessionActivityDB.__table__.create(c, checkfirst=True))
    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    yield maker
    await engine.dispose()


class TestLedgerRoundTrip:
    async def test_record_and_read_back(self, sm):
        async with sm() as s:
            await SessionActivityRepository(s).record(
                owner_id=_USER_A,
                conversation_id=_CONV,
                action_type="issue_created",
                target_ref="mediajunkie/test-piper-morgan#107",
                target_title="Fix the login bug",
                turn_id="t1",
            )
        async with sm() as s:
            rows = await SessionActivityRepository(s).list_for_session(_USER_A, _CONV)
        assert len(rows) == 1
        assert rows[0].action_type == "issue_created"
        assert rows[0].target_ref == "mediajunkie/test-piper-morgan#107"
        assert rows[0].target_title == "Fix the login bug"
        assert rows[0].turn_id == "t1"
        assert rows[0].owner_id == _USER_A


class TestOwnerScopingD1a:
    async def test_second_users_activity_is_never_returned(self, sm):
        """THE D1a test: A and B both create in the SAME conversation; A's read
        returns ONLY A's rows. Owner-scoping, not just conversation-scoping."""
        async with sm() as s:
            repo = SessionActivityRepository(s)
            await repo.record(
                owner_id=_USER_A, conversation_id=_CONV,
                action_type="issue_created", target_ref="o/r#107",
            )
            await repo.record(
                owner_id=_USER_B, conversation_id=_CONV,
                action_type="issue_created", target_ref="o/r#999",
            )
        async with sm() as s:
            a_rows = await SessionActivityRepository(s).list_for_session(_USER_A, _CONV)
            b_rows = await SessionActivityRepository(s).list_for_session(_USER_B, _CONV)

        a_refs = {r.target_ref for r in a_rows}
        b_refs = {r.target_ref for r in b_rows}
        # Same shared conversation, but each owner sees ONLY their own creation:
        assert a_refs == {"o/r#107"}
        assert b_refs == {"o/r#999"}
        # The load-bearing assertion — B's activity never leaks into A's context:
        assert "o/r#999" not in a_refs

    async def test_reader_signature_has_no_unscoped_path(self):
        """Guard against a future refactor re-introducing an owner_id=None leak path:
        owner_id must be a required parameter (no default)."""
        import inspect

        sig = inspect.signature(SessionActivityRepository.list_for_session)
        owner_param = sig.parameters["owner_id"]
        assert owner_param.default is inspect.Parameter.empty, (
            "list_for_session.owner_id must stay required — an optional owner is the "
            "silent cross-user-leak default D1a forbids"
        )


class TestRecall:
    async def test_lists_all_this_session_created(self, sm):
        """B4 recall reads the full set for the owner+session."""
        async with sm() as s:
            repo = SessionActivityRepository(s)
            await repo.record(owner_id=_USER_A, conversation_id=_CONV,
                              action_type="issue_created", target_ref="o/r#1")
            await repo.record(owner_id=_USER_A, conversation_id=_CONV,
                              action_type="doc_created", target_ref="doc-2")
        async with sm() as s:
            rows = await SessionActivityRepository(s).list_for_session(_USER_A, _CONV)
        assert {r.target_ref for r in rows} == {"o/r#1", "doc-2"}
