"""ADR-078 D3 / B4 (#1394) — session-activity recall: routing + handler.

"what did we create this session" is intercepted deterministically at the
pre-classifier (surface 1, D4-safe — no classifier statefulness), routed to
`_handle_session_activity_query`, which reads the owner-scoped ledger.
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
from services.domain.models import Intent  # noqa: E402
from services.intent.intent_service import IntentService  # noqa: E402
from services.intent_service.pre_classifier import PreClassifier  # noqa: E402
from services.shared_types import IntentCategory  # noqa: E402

pytestmark = pytest.mark.asyncio

_CONV = "conv-recall-1"
_USER = "owner-recall"


class TestRouting:
    @pytest.mark.parametrize(
        "phrase",
        [
            "what did we create this session",
            "what have we created",
            "what did we make",
            "what issues did we create",
        ],
    )
    def test_recall_phrases_preclassify_to_session_activity_query(self, phrase):
        intent = PreClassifier().pre_classify(phrase)
        assert intent is not None
        assert intent.action == "session_activity_query"
        assert intent.category == IntentCategory.QUERY

    def test_ship_query_is_not_hijacked(self):
        """The repo-wide 'what did we ship' must NOT route to the session ledger."""
        intent = PreClassifier().pre_classify("what did we ship")
        assert intent is None or intent.action != "session_activity_query"


@pytest_asyncio.fixture
async def sm(monkeypatch):
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


def _intent(user_id):
    ctx = {"original_message": "what did we create this session"}
    if user_id is not None:
        ctx["user_id"] = user_id
    return Intent(category=IntentCategory.QUERY, action="session_activity_query",
                  confidence=1.0, context=ctx)


def _handler_self():
    return types.SimpleNamespace(logger=MagicMock())


class TestHandler:
    async def test_lists_this_sessions_creations(self, sm):
        async with sm() as s:
            repo = SessionActivityRepository(s)
            await repo.record(owner_id=_USER, conversation_id=_CONV,
                              action_type="issue_created",
                              target_ref="mediajunkie/test-piper-morgan#107",
                              target_title="Fix the login bug")
        res = await IntentService._handle_session_activity_query(
            _handler_self(), _intent(_USER), "wf-1", _CONV
        )
        assert res.success
        assert "#107" in res.message
        assert "Fix the login bug" in res.message
        assert res.intent_data["activity_count"] == 1

    async def test_empty_session_says_nothing_created(self, sm):
        res = await IntentService._handle_session_activity_query(
            _handler_self(), _intent(_USER), "wf-1", _CONV
        )
        assert res.success
        assert "haven't created anything" in res.message.lower()

    async def test_no_principal_degrades_honestly(self, sm):
        """D1a — with no signed-in user, we don't read the ledger unscoped."""
        res = await IntentService._handle_session_activity_query(
            _handler_self(), _intent(None), "wf-1", _CONV
        )
        assert res.success
        assert "signed" in res.message.lower()

    async def test_recall_is_owner_scoped(self, sm):
        """Another user's creation in the same conversation is not recalled."""
        async with sm() as s:
            repo = SessionActivityRepository(s)
            await repo.record(owner_id="other-user", conversation_id=_CONV,
                              action_type="issue_created", target_ref="o/r#999")
        res = await IntentService._handle_session_activity_query(
            _handler_self(), _intent(_USER), "wf-1", _CONV
        )
        assert "#999" not in res.message
        assert "haven't created anything" in res.message.lower()
