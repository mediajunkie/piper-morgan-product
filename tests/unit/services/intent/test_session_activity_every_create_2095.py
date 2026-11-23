"""#2095 — the session ledger records every record Piper creates (ADR-078 D1 amendment).

xian, alpha e801b1a309, 2026-10-19 13:53: `add todo to review the roadmap`, then "What have I
created this session?" → "We haven't created anything in this session yet." The ledger held
issues and docs only. Arch's amendment: todo_created / reminder_created / project_created with
target_ref kind:<id>; the OQ-3 contract (handlers declare, the observer writes) unchanged; a
completeness pin over the routed create actions.

LAYER: the observer and the recall against an in-memory ledger (the same seam as the 1394 pins);
the todo handlers' side-channel directly; the create paths' declarations by source read (the
completeness pin names its layer). DENOMINATOR: the five action types; four create paths.
"""

import contextlib
import inspect
import types
from unittest.mock import MagicMock

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from services.database.models import SessionActivityDB
from services.database.repositories import SessionActivityRepository
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.session_activity_read import INTERNAL_RECORD_KINDS, LEDGER_ACTION_TYPES

pytestmark = pytest.mark.asyncio

_CONV = "conv-2095"
_USER = "owner-2095"


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


def _self():
    return types.SimpleNamespace(logger=MagicMock())


def _intent():
    from services.domain.models import Intent
    from services.shared_types import IntentCategory

    return Intent(
        original_message="What have I created this session?",
        category=IntentCategory.QUERY,
        action="session_activity_query",
        confidence=0.9,
        context={"original_message": "What have I created this session?", "user_id": _USER},
    )


class TestSideChannelForStringHandlers:
    async def test_remember_created_todo_parks_the_ledger_row(self):
        from services.intent_service.conversation_context import get_or_create_context
        from services.intent_service.todo_handlers import TodoIntentHandlers

        todo = types.SimpleNamespace(id="t-1", text="review the roadmap")
        TodoIntentHandlers._remember_created_todo("sess-2095", _USER, todo, "todo")
        ctx = get_or_create_context("sess-2095", user_id=_USER)
        assert ctx.pending_created_activity == {
            "action_type": "todo_created",
            "target_ref": "todo:t-1",
            "target_title": "review the roadmap",
        }

    async def test_observer_writes_the_parked_row_once(self, sm):
        from services.intent_service.conversation_context import get_or_create_context

        ctx = get_or_create_context(_CONV, user_id=_USER)
        ctx.pending_created_activity = {
            "action_type": "todo_created",
            "target_ref": "todo:t-7",
            "target_title": "review the roadmap",
        }
        result = IntentProcessingResult(
            success=True, message="I've added 'x' to your list.", intent_data={}
        )
        await IntentService._record_session_activity(_self(), _CONV, _USER, result)
        await IntentService._record_session_activity(
            _self(), _CONV, _USER, result
        )  # popped: no second row
        async with sm() as s:
            rows = await SessionActivityRepository(s).list_for_session(_USER, _CONV)
        assert [(r.action_type, r.target_ref) for r in rows] == [("todo_created", "todo:t-7")]
        assert ctx.pending_created_activity is None


class TestRecallNamesTheRecord:
    async def test_every_ledger_kind_has_a_label(self):
        src = inspect.getsource(IntentService._handle_session_activity_query)
        for kind in LEDGER_ACTION_TYPES:
            assert f'"{kind}"' in src, f"recall has no label for {kind}"

    async def test_a_todo_is_named_by_its_title_not_its_id(self, sm):
        async with sm() as s:
            await SessionActivityRepository(s).record(
                owner_id=_USER,
                conversation_id=_CONV,
                action_type="todo_created",
                target_ref="todo:3b1c",
                target_title="review the roadmap",
            )
        res = await IntentService._handle_session_activity_query(_self(), _intent(), "wf", _CONV)
        assert "• a todo: review the roadmap" in res.message
        assert "3b1c" not in res.message
        assert "haven't created anything" not in res.message


class TestEveryRoutedCreateDeclares:
    """Arch's completeness pin. LAYER: source read of each create path; it proves the
    declaration exists, not that the row lands (the two tests above prove the write)."""

    # Arch (#2095 validation): the create set is DERIVED from the registry's verb
    # bridge, and a create action with no handler row here fails the build (the
    # old hasattr(...) else "created_activity" passed on a rename).
    HANDLER_FOR_CREATE_ACTION = {
        "create_todo": (
            "services.intent_service.todo_handlers",
            "TodoIntentHandlers.handle_create_todo",
        ),
        "create_reminder": (
            "services.intent_service.todo_handlers",
            "TodoIntentHandlers.handle_create_reminder",
        ),
        "add_project": (
            "services.intent_service.canonical_handlers",
            "CanonicalHandlers._create_or_report_project",
        ),
        "create_issue": ("services.intent.intent_service", "IntentService._handle_create_issue"),
    }

    def test_create_paths_declare_or_park(self):
        import importlib

        from services.intent_service.action_registry import ACTION_TO_VERB, Verb

        create_actions = sorted(a for a, v in ACTION_TO_VERB.items() if v is Verb.CREATE)
        assert create_actions, "the verb bridge names no create action"
        missing = [a for a in create_actions if a not in self.HANDLER_FOR_CREATE_ACTION]
        assert not missing, f"create actions with no handler row in this pin: {missing}"
        for action in create_actions:
            module_name, dotted = self.HANDLER_FOR_CREATE_ACTION[action]
            obj = importlib.import_module(module_name)
            for part in dotted.split("."):
                assert hasattr(obj, part), f"{action}: {module_name}.{dotted} no longer exists"
                obj = getattr(obj, part)
            src = inspect.getsource(obj)
            assert (
                "created_activity" in src or "_remember_created_todo" in src
            ), f"{action} creates a record without declaring it to the ledger"

    def test_internal_kinds_match_the_action_types(self):
        for kind in INTERNAL_RECORD_KINDS:
            assert f"{kind}_created" in LEDGER_ACTION_TYPES
