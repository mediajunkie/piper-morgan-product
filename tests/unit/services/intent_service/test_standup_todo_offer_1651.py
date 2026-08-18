"""#1651 — the standup's closing offer BINDS its referent (overdue todo).

PM live 2026-08-18: standup ended with "Want me to … mark that overdue todo
done?", PM said "Yes mark the overdue todo done.", and the acceptance fell to
complete_todo's literal title matching ("I couldn't find a todo matching
'overdue'"). The fix arms the #846 pending-offer carrier with the overdue
todo's id at offer time; acceptance dispatches on the BOUND id.

Layer honesty (m-43): the end-to-end class drives the REAL entry the web
route calls (``IntentService.process_intent``, the #1190/#1411 test idiom),
mocked ONLY at the LLM boundary (explosive — every turn here must resolve
deterministically: turn 1 via the ``_is_standup_query`` claim, turn 2 via the
pending-offer seam), the standup assembler boundary (a deterministic
non-empty summary — the radar sources are not under test), and the todo
SERVICE boundary (an in-memory double; the REAL-Postgres half of the AC lives
in tests/integration/test_standup_todo_offer_1651.py).
"""

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.intent.intent_service import IntentService
from services.intent_service import standup_todo_offer as sto
from services.intent_service.classifier import IntentClassifier
from services.intent_service.standup_todo_offer import (
    STANDUP_COMPLETE_TODO_WORKFLOW,
    STANDUP_TODO_OFFER_KIND,
    build_overdue_todo_offer,
    find_overdue_todos,
    run_standup_complete_todo_workflow,
)
from services.intent_service.workflow_dispatcher import get_action_workflows
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import EffectClass

_USER = "3f7b8a52-1651-4b00-9e00-000000001651"
_NOW = datetime.now(timezone.utc)

PROSE = "Here's your derived standup."


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM. Every turn in
    these tests must resolve deterministically (the standup claim or the
    pending-offer seam, both of which run before classification)."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1651 turns must resolve "
            "deterministically"
        )


def _todo(text, days_overdue=None, todo_id=None, completed=False):
    due = _NOW - timedelta(days=days_overdue) if days_overdue is not None else None
    return SimpleNamespace(
        id=todo_id or str(uuid4()),
        text=text,
        due_date=due,
        completed=completed,
    )


class _FakeTodoService:
    """In-memory double for TodoManagementService (list/complete only)."""

    def __init__(self, todos):
        self.todos = list(todos)
        self.completed_calls = []

    async def list_todos(self, user_id, include_completed=False, **kwargs):
        return [t for t in self.todos if include_completed or not t.completed]

    async def complete_todo(self, todo_id, user_id):
        self.completed_calls.append((str(todo_id), str(user_id)))
        for t in self.todos:
            if str(t.id) == str(todo_id) and not t.completed:
                t.completed = True
                return t
        return None


def _summary():
    summary = MagicMock()
    summary.is_empty.return_value = False
    summary.to_prose.return_value = PROSE
    summary.to_dict.return_value = {"sections": []}
    return summary


@pytest.fixture
def live_service():
    register_default_workflows()
    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


def _wire_todos(service, todos):
    fake = _FakeTodoService(todos)
    service.todo_handlers.todo_service = fake
    return fake


async def _standup_turn(service, sid, message="give me my standup"):
    with patch(
        "services.standup.assembler.build_user_standup_summary",
        new=AsyncMock(return_value=_summary()),
    ):
        return await service.process_intent(
            message=message, session_id=sid, user_id=_USER
        )


# ---------------------------------------------------------------------------
# Machinery: referent resolution + offer builder
# ---------------------------------------------------------------------------


class TestOverdueReferentResolution:
    pytestmark = pytest.mark.asyncio

    async def test_most_overdue_first_and_only_overdue_qualify(self):
        svc = _FakeTodoService(
            [
                _todo("pay the invoice", days_overdue=3),
                _todo("book flights", days_overdue=9),
                _todo("no due date at all"),
                _todo("due next week", days_overdue=-7),  # future
                _todo("already done", days_overdue=20, completed=True),
            ]
        )
        overdue = await find_overdue_todos(svc, _USER)
        assert [t.text for t in overdue] == ["book flights", "pay the invoice"]

    async def test_non_uuid_principal_resolves_no_referent(self):
        svc = _FakeTodoService([_todo("pay the invoice", days_overdue=3)])
        assert await find_overdue_todos(svc, "U-slack-raw-id") == []
        assert await find_overdue_todos(svc, None) == []


class TestOfferBuilder:
    def test_offer_binds_id_and_names_referent(self):
        todo = _todo("pay the invoice", days_overdue=3, todo_id=str(uuid4()))
        built = build_overdue_todo_offer(_USER, "sess-1651", todo, more_overdue=0)
        assert built is not None
        # The copy NAMES the bound referent — never an unbound "that todo".
        assert '"pay the invoice"' in built.question
        assert "(yes/no)" in built.question
        record = built.offer
        assert record["workflow_type"] == STANDUP_COMPLETE_TODO_WORKFLOW
        pa = record["pending_action"]
        assert pa["kind"] == STANDUP_TODO_OFFER_KIND
        assert pa["todo_id"] == str(todo.id)
        assert pa["user_id"] == _USER
        assert '"pay the invoice"' in record["decline_message"]
        assert "Nothing has been changed" in record["decline_message"]

    def test_multiple_overdue_enumerates_count_and_binds_strongest(self):
        todo = _todo("book flights", days_overdue=9)
        built = build_overdue_todo_offer(_USER, "sess-1651", todo, more_overdue=2)
        # m-44: the denominator is stated, the single strongest is named.
        assert "2 more" in built.question
        assert '"book flights"' in built.question
        assert built.offer["pending_action"]["todo_id"] == str(todo.id)

    def test_unarmable_without_session_user_or_id(self):
        todo = _todo("pay the invoice", days_overdue=3)
        assert build_overdue_todo_offer(None, "sess", todo) is None
        assert build_overdue_todo_offer(_USER, None, todo) is None
        no_id = SimpleNamespace(id=None, text="x", due_date=_NOW, completed=False)
        assert build_overdue_todo_offer(_USER, "sess", no_id) is None

    def test_workflow_is_not_rail_reachable(self):
        """action_triggered=False: a classifier emission can never fire the
        bound completion directly."""
        register_default_workflows()
        assert STANDUP_COMPLETE_TODO_WORKFLOW not in get_action_workflows()

    def test_workflow_declares_write_effect(self):
        from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY

        register_default_workflows()
        assert WORKFLOW_REGISTRY[STANDUP_COMPLETE_TODO_WORKFLOW].effect == (
            EffectClass.WRITE
        )


# ---------------------------------------------------------------------------
# Acceptance entry point: bound-id dispatch, principal safety, honest failure
# ---------------------------------------------------------------------------


class TestAcceptanceEntryPoint:
    pytestmark = pytest.mark.asyncio

    def _ctx(self, service_stub, todo, user=_USER):
        return {
            "pending_action": {
                "kind": STANDUP_TODO_OFFER_KIND,
                "action": STANDUP_COMPLETE_TODO_WORKFLOW,
                "user_id": user,
                "todo_id": str(todo.id),
                "todo_text": todo.text,
                "summary": f'mark the overdue todo "{todo.text}" done',
            },
            "intent_service": service_stub,
        }

    def _service_stub(self, todos):
        fake = _FakeTodoService(todos)
        return SimpleNamespace(todo_handlers=SimpleNamespace(todo_service=fake)), fake

    async def test_completes_by_bound_id_never_by_title(self):
        # The todo's title shares NO words with 'overdue' — a title-matching
        # path (the #1651 bug) cannot find it; the bound id must.
        todo = _todo("pay the invoice", days_overdue=3)
        stub, fake = self._service_stub([todo])
        result = await run_standup_complete_todo_workflow(
            session_id="s-1651", user_id=_USER, context=self._ctx(stub, todo)
        )
        assert fake.completed_calls == [(str(todo.id), _USER)]
        assert result["intent_data"]["completed"] is True
        assert result["intent_data"]["todo_id"] == str(todo.id)
        assert "pay the invoice" in result["message"]

    async def test_principal_mismatch_touches_nothing(self):
        todo = _todo("pay the invoice", days_overdue=3)
        stub, fake = self._service_stub([todo])
        other = str(uuid4())
        result = await run_standup_complete_todo_workflow(
            session_id="s-1651", user_id=other, context=self._ctx(stub, todo)
        )
        assert fake.completed_calls == []
        assert result["intent_data"]["principal_mismatch"] is True
        assert "nothing has been changed" in result["message"].lower()

    async def test_vanished_todo_answers_honestly(self):
        todo = _todo("pay the invoice", days_overdue=3)
        stub, fake = self._service_stub([])  # row gone by acceptance time
        result = await run_standup_complete_todo_workflow(
            session_id="s-1651", user_id=_USER, context=self._ctx(stub, todo)
        )
        assert result["intent_data"]["completed"] is False
        assert "couldn't mark" in result["message"]

    async def test_foreign_or_missing_payload_never_fires(self):
        stub, fake = self._service_stub([])
        assert await run_standup_complete_todo_workflow(
            session_id="s", context={}
        ) is None
        assert await run_standup_complete_todo_workflow(
            session_id="s",
            context={
                "pending_action": {"kind": "drafted_issue"},
                "intent_service": stub,
            },
        ) is None
        assert fake.completed_calls == []


# ---------------------------------------------------------------------------
# End-to-end through the REAL process_intent (the #1190/#1411 test idiom) —
# PM's transcript, turn for turn.
# ---------------------------------------------------------------------------


class TestEndToEndStandupOfferTurns:
    pytestmark = pytest.mark.asyncio

    async def test_standup_with_overdue_todo_arms_bound_offer(self, live_service):
        """Turn 1: the report renders FIRST and COMPLETE; the closing copy
        names the overdue todo; the #846 store holds the BOUND id."""
        todo = _todo("pay the invoice", days_overdue=3)
        _wire_todos(live_service, [todo])
        sid = "e2e-1651-arm"
        result = await _standup_turn(live_service, sid)
        assert result.message.startswith(f"Good morning! {PROSE}")
        assert '"pay the invoice"' in result.message
        assert "(yes/no)" in result.message
        assert result.intent_data.get("standup_todo_offer_pending") is True
        stored = _pending_offers(live_service).get(sid)
        assert stored is not None
        assert stored["workflow_type"] == STANDUP_COMPLETE_TODO_WORKFLOW
        assert stored["pending_action"]["todo_id"] == str(todo.id)

    async def test_pm_verbatim_acceptance_completes_the_bound_todo(
        self, live_service
    ):
        """Turn 2, PM's exact words: 'Yes mark the overdue todo done.' —
        the bound todo completes; no title matching runs (the todo's title
        contains no word from the acceptance phrase)."""
        todo = _todo("pay the invoice", days_overdue=3)
        fake = _wire_todos(live_service, [todo])
        sid = "e2e-1651-verbatim"
        await _standup_turn(live_service, sid)

        # #1529 ordering: the pending offer must claim the turn before the
        # resume check can.
        async def _explosive_resume(*a, **k):
            raise AssertionError(
                "_check_pending_resume_offer reached — pending offer must "
                "bind the affirmative first (#1529 ordering)"
            )

        live_service._check_pending_resume_offer = _explosive_resume

        result = await live_service.process_intent(
            message="Yes mark the overdue todo done.", session_id=sid, user_id=_USER
        )
        assert fake.completed_calls == [(str(todo.id), _USER)]
        assert todo.completed is True
        assert "pay the invoice" in result.message
        assert _pending_offers(live_service).get(sid) is None  # consumed

    async def test_crisp_yes_completes_the_bound_todo(self, live_service):
        todo = _todo("pay the invoice", days_overdue=3)
        fake = _wire_todos(live_service, [todo])
        sid = "e2e-1651-yes"
        await _standup_turn(live_service, sid)
        result = await live_service.process_intent(
            message="yes", session_id=sid, user_id=_USER
        )
        assert fake.completed_calls == [(str(todo.id), _USER)]
        assert "pay the invoice" in result.message

    async def test_decline_drops_honestly_and_nothing_completes(self, live_service):
        todo = _todo("pay the invoice", days_overdue=3)
        fake = _wire_todos(live_service, [todo])
        sid = "e2e-1651-no"
        await _standup_turn(live_service, sid)
        result = await live_service.process_intent(
            message="no", session_id=sid, user_id=_USER
        )
        assert fake.completed_calls == []
        assert todo.completed is False
        assert '"pay the invoice" stays on your list' in result.message
        assert "Nothing has been changed" in result.message
        assert _pending_offers(live_service).get(sid) is None

    async def test_no_overdue_todo_arms_no_bound_offer(self, live_service):
        """AC: no offer armed when the standup has no actionable referent —
        the trailing ask falls back to the #1591 behavior (the invitation,
        for a first-time user), and whatever is armed is NOT the bound
        completion workflow."""
        _wire_todos(live_service, [_todo("due far in the future", days_overdue=-30)])
        sid = "e2e-1651-none"
        result = await _standup_turn(live_service, sid)
        assert result.intent_data.get("standup_todo_offer_pending") is None
        stored = _pending_offers(live_service).get(sid)
        if stored is not None:  # the #1591 invitation may legitimately arm
            assert stored["workflow_type"] != STANDUP_COMPLETE_TODO_WORKFLOW
        assert "overdue" not in result.message

    async def test_most_overdue_bound_when_multiple_and_count_stated(
        self, live_service
    ):
        """Never an unbound 'that todo': with several overdue, the single
        strongest (most overdue) is bound and the copy enumerates."""
        older = _todo("book flights", days_overdue=9)
        newer = _todo("pay the invoice", days_overdue=3)
        _wire_todos(live_service, [newer, older])
        sid = "e2e-1651-multi"
        result = await _standup_turn(live_service, sid)
        stored = _pending_offers(live_service).get(sid)
        assert stored["pending_action"]["todo_id"] == str(older.id)
        assert '"book flights"' in result.message
        assert "1 more" in result.message

    async def test_todo_read_failure_never_blanks_the_standup(self, live_service):
        """Per-source isolation: a todo-store hiccup renders the complete
        report with the ordinary #1591 trailing — no offer, no error turn."""

        class _ExplodingTodoService:
            async def list_todos(self, *a, **k):
                raise RuntimeError("todo store down")

        live_service.todo_handlers.todo_service = _ExplodingTodoService()
        sid = "e2e-1651-isolated"
        result = await _standup_turn(live_service, sid)
        assert result.success is True
        assert result.message.startswith(f"Good morning! {PROSE}")
        assert result.intent_data.get("standup_todo_offer_pending") is None

    async def test_prose_reply_neither_fires_nor_declines_1631(self, live_service):
        """#1631 at the generic seam: a long prose turn abandons the offer
        via the pop (off-intent) — the bound completion never fires off a
        'yes' substring."""
        todo = _todo("pay the invoice", days_overdue=3)
        fake = _wire_todos(live_service, [todo])
        sid = "e2e-1651-prose"
        await _standup_turn(live_service, sid)
        prose = (
            "Yes and no — I've been meaning to deal with that invoice for a "
            "while, but the vendor said the amount might change after the "
            "contract review wraps, so let's hold off until I hear back from "
            "them later this week."
        )
        assert len(prose) >= 160
        # The abandoned turn re-routes normally; the standup claim won't take
        # it, so it heads for the classifier — stub the LLM lane out by
        # patching classify_multiple (the turn's routing is not under test;
        # what is pinned: nothing fires, the offer is gone).
        from services.intent_service.pre_classifier import MultiIntentResult
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        fallback = Intent(
            category=IntentCategory.UNKNOWN,
            action="unknown",
            confidence=0.2,
            original_message=prose,
            context={"original_message": prose},
        )
        with patch.object(
            live_service.intent_classifier,
            "classify_multiple",
            new=AsyncMock(
                return_value=MultiIntentResult(
                    intents=[fallback], original_message=prose
                )
            ),
        ):
            with patch.object(
                live_service,
                "_handle_unknown_intent",
                new=AsyncMock(
                    return_value=MagicMock(
                        success=True, message="ok", intent_data={}
                    )
                ),
            ):
                await live_service.process_intent(
                    message=prose, session_id=sid, user_id=_USER
                )
        assert fake.completed_calls == []
        assert todo.completed is False
        assert _pending_offers(live_service).get(sid) is None  # popped, gone
