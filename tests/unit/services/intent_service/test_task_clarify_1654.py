"""#1654 — the no-task clarify ask now ARMS a carrier; its answer binds.

PM live 2026-08-18 (during #1648): handle_create_reminder's OTHER honest ask
— the no-task clarify, "I didn't catch what you'd like to be reminded about",
hit twice via the colon-form parse misses — armed NOTHING, so the answer (a
bare task phrase) orphaned into the routing chain: #1648's class, one
question earlier. The fix mirrors the #1648 time-question carrier with a
task-question kind (``reminder_task_question``): the ask arms; the next
turn's answer binds as the TASK; then either the time is already known from
the original message (rare) and the REAL save runs, or the flow chains into
the EXISTING #1648 time question — the full two-question recovery.

The colon-form PARSE miss itself stays #1606/corpus — these tests only pin
that the ask, once fired, holds its answer.

Layer honesty (m-43): the e2e classes drive the REAL
``IntentService.process_intent`` with an explosive LLM — every pinned turn
must resolve deterministically (offer seam or pre-classifier), because the
live failures happened exactly when a turn escaped to the LLM lane. The
turn-handler classes drive ``handle_reminder_task_turn`` at its seam.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

import pytest

from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.soft_invocation import WorkflowOfferService
from services.intent_service.todo_handlers import (
    _TASK_REASK_TAIL,
    _TIME_ASK,
    CLARIFY_REMINDER_TASK_WORKFLOW,
    REMINDER_TASK_QUESTION_KIND,
    REMINDER_TIME_QUESTION_KIND,
    TodoIntentHandlers,
    build_reminder_task_offer,
    handle_reminder_task_turn,
)
from services.intent_service.workflow_entries import register_default_workflows

GATE = "services.intent_service.collaboration_gate"

_USER = "3f7b8a52-1654-4b00-9e00-000000001654"

# PM's transcript shape: the colon-form miss fires the no-task ask. The
# colon form itself isn't pre-classifier-claimed for "remind me:" (that
# parse gap is #1606) — "set a reminder: …" IS claimed deterministically,
# so it is the e2e trigger that reaches the handler with the LLM explosive.
NO_TASK_NO_TIME = "set a reminder: check the oven"
NO_TASK_TIME_KNOWN = "set a reminder: at 3pm tomorrow"
NO_TASK_TIME_UNBINDABLE = "set a reminder: at 25:99"


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM. Every pinned
    turn must resolve deterministically — the live orphans happened when
    these turns escaped to the LLM lane and the floor claimed them."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1654 turns must resolve "
            "deterministically (offer seam / pre-classifier)"
        )


@pytest.fixture
def svc():
    register_default_workflows()
    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


def _mock_todo_service(svc):
    """Swap the real DB-backed TodoManagementService for a mock that records
    the write. The seam under test is binding/chaining, not persistence."""
    mock = MagicMock()
    mock.create_todo = AsyncMock(
        return_value=SimpleNamespace(id=uuid4(), text="whatever")
    )
    mock.list_todos = AsyncMock(return_value=[])
    svc.todo_handlers.todo_service = mock
    return mock


async def _fire_no_task_ask(svc, sid, message=NO_TASK_NO_TIME):
    """Turn 1: a deterministically-claimed reminder ask whose task can't be
    extracted — the honest no-task clarify, now arming the carrier."""
    with patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})):
        return await svc.process_intent(
            message=message, session_id=sid, user_id=_USER
        )


# ---------------------------------------------------------------------------
# 1. PM's transcript shape, pinned e2e — the ask arms; the answer binds.
# ---------------------------------------------------------------------------


class TestNoTaskClarifyEndToEnd:
    pytestmark = pytest.mark.asyncio

    async def test_no_task_ask_arms_the_task_question(self, svc):
        sid = "e2e-1654-arm"
        _mock_todo_service(svc)
        r1 = await _fire_no_task_ask(svc, sid)
        assert "I didn't catch what you'd like to be reminded about" in r1.message
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["kind"] == REMINDER_TASK_QUESTION_KIND
        assert stored["pending_action"]["original_message"] == NO_TASK_NO_TIME
        # #1665: the armed record carries the rendered ask verbatim.
        assert stored["question"] == r1.message
        # The belt flag rides the result (soft-offer clobber protection).
        assert r1.intent_data.get("reminder_task_question_pending") is True
        assert r1.requires_clarification is True

    async def test_bare_task_answer_chains_into_the_time_question(self, svc):
        """The core AC: a bare task phrase binds and produces the chained
        time question — never an orphaned turn (explosive LLM proves the
        turn resolved at the offer seam)."""
        sid = "e2e-1654-chain"
        mock = _mock_todo_service(svc)
        await _fire_no_task_ask(svc, sid)

        r2 = await svc.process_intent(message="buy milk", session_id=sid, user_id=_USER)
        mock.create_todo.assert_not_awaited()  # no time yet — nothing saved
        assert "**buy milk**" in r2.message
        assert _TIME_ASK in r2.message
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["kind"] == REMINDER_TIME_QUESTION_KIND
        assert stored["pending_action"]["task_text"] == "buy milk"
        # #1665: the chained arm stores the one rendered time ask.
        assert stored["question"] == _TIME_ASK
        assert r2.intent_data.get("reminder_task_bound") is True
        assert r2.intent_data.get("reminder_time_question_pending") is True

    async def test_full_two_question_recovery(self, svc):
        """The AC chaining test: task answer → time question armed → time
        answer → REAL save (row write + 📅 line), offers drained."""
        sid = "e2e-1654-recovery"
        mock = _mock_todo_service(svc)
        await _fire_no_task_ask(svc, sid)
        await svc.process_intent(message="buy milk", session_id=sid, user_id=_USER)

        r3 = await svc.process_intent(
            message="at 3pm tomorrow", session_id=sid, user_id=_USER
        )
        mock.create_todo.assert_awaited_once()
        kwargs = mock.create_todo.await_args.kwargs
        assert kwargs["text"] == "buy milk"
        assert kwargs["reminder_date"] is not None
        assert (kwargs["reminder_date"].hour, kwargs["reminder_date"].minute) == (15, 0)
        assert "Reminder saved" in r3.message
        assert "📅" in r3.message
        assert _pending_offers(svc) == {}

    async def test_answer_carrying_its_own_time_saves_directly(self, svc):
        """An answer that names task AND time ("buy milk at 3pm tomorrow")
        needs no second question — the REAL save runs in one turn, with the
        time expression shed from the saved text."""
        sid = "e2e-1654-answer-time"
        mock = _mock_todo_service(svc)
        await _fire_no_task_ask(svc, sid)
        r2 = await svc.process_intent(
            message="buy milk at 3pm tomorrow", session_id=sid, user_id=_USER
        )
        mock.create_todo.assert_awaited_once()
        kwargs = mock.create_todo.await_args.kwargs
        assert kwargs["text"] == "buy milk"
        assert kwargs["reminder_date"].hour == 15
        assert "Reminder saved" in r2.message
        assert "📅" in r2.message
        assert _pending_offers(svc) == {}

    async def test_time_already_known_saves_on_task_answer(self, svc):
        """The rare half of the AC: the original message carried a bindable
        time ("set a reminder: at 3pm tomorrow" — task lost, time parsed) —
        the task answer completes it and the REAL save runs, no second
        question."""
        sid = "e2e-1654-time-known"
        mock = _mock_todo_service(svc)
        r1 = await _fire_no_task_ask(svc, sid, message=NO_TASK_TIME_KNOWN)
        assert "I didn't catch what you'd like to be reminded about" in r1.message

        r2 = await svc.process_intent(
            message="check the oven", session_id=sid, user_id=_USER
        )
        mock.create_todo.assert_awaited_once()
        kwargs = mock.create_todo.await_args.kwargs
        assert kwargs["text"] == "check the oven"
        assert kwargs["reminder_date"].hour == 15
        assert "Reminder saved" in r2.message
        assert "📅" in r2.message
        assert _pending_offers(svc) == {}

    async def test_unbindable_original_time_chains_with_honest_echo(self, svc):
        """Original carried an explicit-but-unbindable time (at 25:99): the
        task binds, and the chain echoes the inability honestly — never a
        silently-guessed default (#1490 invariant)."""
        sid = "e2e-1654-unbindable-orig"
        mock = _mock_todo_service(svc)
        await _fire_no_task_ask(svc, sid, message=NO_TASK_TIME_UNBINDABLE)
        r2 = await svc.process_intent(
            message="check the oven", session_id=sid, user_id=_USER
        )
        mock.create_todo.assert_not_awaited()
        assert '25:99' in r2.message
        assert _TIME_ASK in r2.message
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["kind"] == REMINDER_TIME_QUESTION_KIND
        assert stored["pending_action"]["task_text"] == "check the oven"

    async def test_imperative_verb_task_phrase_binds(self, svc):
        """The discrimination pin: "check in with the team" is this ask's
        own example copy AND starts with a supplement-regex verb head — it
        must BIND as the task (the #1654 carrier discriminates by
        pre-classifier claim, not by is_command_shaped, precisely so
        imperative task phrases survive)."""
        sid = "e2e-1654-imperative"
        mock = _mock_todo_service(svc)
        await _fire_no_task_ask(svc, sid)
        r2 = await svc.process_intent(
            message="check in with the team", session_id=sid, user_id=_USER
        )
        mock.create_todo.assert_not_awaited()
        assert "**check in with the team**" in r2.message
        assert _TIME_ASK in r2.message
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["task_text"] == "check in with the team"

    async def test_off_intent_command_releases_and_routes(self, svc):
        """The carrier's off-intent rule: a pre-classifier-claimed command
        abandons the question via the pop and routes normally (here the
        deterministic reminder-list handler answers)."""
        sid = "e2e-1654-offintent"
        mock = _mock_todo_service(svc)
        await _fire_no_task_ask(svc, sid)
        r2 = await svc.process_intent(
            message="list my reminders", session_id=sid, user_id=_USER
        )
        mock.create_todo.assert_not_awaited()
        assert "there are none right now" in r2.message
        # The task question is gone — abandoned, not re-armed.
        for stored in _pending_offers(svc).values():
            assert (
                stored["pending_action"].get("kind") != REMINDER_TASK_QUESTION_KIND
            )

    async def test_decline_drops_honestly(self, svc):
        sid = "e2e-1654-decline"
        mock = _mock_todo_service(svc)
        await _fire_no_task_ask(svc, sid)
        r2 = await svc.process_intent(message="no", session_id=sid, user_id=_USER)
        mock.create_todo.assert_not_awaited()
        assert "Nothing was saved" in r2.message
        assert _pending_offers(svc) == {}

    async def test_bare_yes_reasks_and_rearms(self, svc):
        """A bare "yes" doesn't answer "what?" — honest re-ask, re-armed,
        never a silent abandon into the routing chain (#1648 direction 2)."""
        sid = "e2e-1654-bare-yes"
        mock = _mock_todo_service(svc)
        await _fire_no_task_ask(svc, sid)
        r2 = await svc.process_intent(message="yes", session_id=sid, user_id=_USER)
        mock.create_todo.assert_not_awaited()
        assert "No reminder has been saved yet" in r2.message
        assert _TASK_REASK_TAIL in r2.message
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["kind"] == REMINDER_TASK_QUESTION_KIND
        # #1665: the re-armed record's question is the re-ask tail.
        assert stored["question"] == _TASK_REASK_TAIL

    async def test_pure_time_answer_reasks_for_the_task(self, svc):
        """Answering the TASK question with a bare time ("at 3pm") re-asks —
        the time expression must never be saved AS the task."""
        sid = "e2e-1654-pure-time"
        mock = _mock_todo_service(svc)
        await _fire_no_task_ask(svc, sid)
        r2 = await svc.process_intent(message="at 3pm", session_id=sid, user_id=_USER)
        mock.create_todo.assert_not_awaited()
        assert "reads as a time" in r2.message
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["kind"] == REMINDER_TASK_QUESTION_KIND

    async def test_full_restatement_routes_normally(self, svc):
        """A full restatement carries its own task AND time — it must route
        through the real handler (re-extracting both), not bind here."""
        sid = "e2e-1654-restate"
        mock = _mock_todo_service(svc)
        await _fire_no_task_ask(svc, sid)
        with patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})):
            r2 = await svc.process_intent(
                message="remind me to call the vet at 3pm tomorrow",
                session_id=sid,
                user_id=_USER,
            )
        mock.create_todo.assert_awaited_once()
        assert mock.create_todo.await_args.kwargs["text"] == "call the vet"
        assert "Reminder saved" in r2.message
        assert "📅" in r2.message


# ---------------------------------------------------------------------------
# 2. Turn-handler seam — edges the e2e layer can't reach cleanly.
# ---------------------------------------------------------------------------


def _fake_service(todo_service=None):
    return SimpleNamespace(
        workflow_offer_service=WorkflowOfferService(),
        todo_handlers=SimpleNamespace(todo_service=todo_service),
    )


def _offer(original_message=NO_TASK_NO_TIME, question="what should it say?"):
    return build_reminder_task_offer(original_message, _USER, question=question)


class TestTaskTurnHandlerSeam:
    pytestmark = pytest.mark.asyncio

    async def test_leading_to_is_stripped_from_the_answer(self):
        """Answers often echo the ask's phrasing: "to buy milk" → task
        "buy milk"."""
        fake = _fake_service()
        result = await handle_reminder_task_turn(
            _offer(),
            "to buy milk",
            session_id="s-1654-to",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is not None
        assert "**buy milk**" in result["message"]
        stored = fake.workflow_offer_service.peek_pending_offer("s-1654-to")
        assert stored["pending_action"]["task_text"] == "buy milk"

    async def test_principal_mismatch_holds_off(self):
        fake = _fake_service()
        result = await handle_reminder_task_turn(
            _offer(),
            "buy milk",
            session_id="s-1654-principal",
            user_id=str(uuid4()),  # a DIFFERENT principal
            intent_service=fake,
        )
        assert result is not None
        assert "nothing has been saved" in result["message"].lower()
        assert result["intent_data"].get("principal_mismatch") is True

    async def test_save_failure_is_honest_and_holds_the_time_question(self):
        """A failed write surfaces as an HONEST failure (never a success
        claim), and the flow holds at the #1648 time question with the task
        still bound — the retry is one short answer away."""
        broken = MagicMock()
        broken.create_todo = AsyncMock(side_effect=RuntimeError("db down"))
        fake = _fake_service(broken)
        result = await handle_reminder_task_turn(
            _offer(original_message=NO_TASK_TIME_KNOWN),
            "check the oven",
            session_id="s-1654-savefail",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is not None
        assert "I had trouble saving it just now" in result["message"]
        assert "Reminder saved" not in result["message"]
        stored = fake.workflow_offer_service.peek_pending_offer("s-1654-savefail")
        assert stored["pending_action"]["kind"] == REMINDER_TIME_QUESTION_KIND
        assert stored["pending_action"]["task_text"] == "check the oven"

    async def test_empty_and_broken_payload_fall_through(self):
        fake = _fake_service()
        assert (
            await handle_reminder_task_turn(
                _offer(),
                "   ",
                session_id="s-1654-empty",
                user_id=_USER,
                intent_service=fake,
            )
            is None
        )

    async def test_arm_failure_keeps_the_ask_honest(self):
        """#1654 chain-arm failure: the reply never claims a binding that
        isn't there — the fallback tail teaches the fresh restatement."""
        exploding = SimpleNamespace(
            workflow_offer_service=SimpleNamespace(
                set_pending_offer=MagicMock(side_effect=RuntimeError("store down"))
            ),
            todo_handlers=SimpleNamespace(todo_service=None),
        )
        result = await handle_reminder_task_turn(
            _offer(),
            "buy milk",
            session_id="s-1654-armfail",
            user_id=_USER,
            intent_service=exploding,
        )
        assert result is not None
        assert "couldn't keep the question open" in result["message"]
        assert result["intent_data"].get("reminder_time_question_pending") is False


# ---------------------------------------------------------------------------
# 3. The offer record + generic-accept landing (wiring), mirroring #1648's.
# ---------------------------------------------------------------------------


class TestReminderTaskOfferWiring:
    def test_offer_record_shape(self):
        offer = build_reminder_task_offer(NO_TASK_NO_TIME, _USER)
        assert offer["workflow_type"] == CLARIFY_REMINDER_TASK_WORKFLOW
        pa = offer["pending_action"]
        assert pa["kind"] == REMINDER_TASK_QUESTION_KIND
        assert pa["original_message"] == NO_TASK_NO_TIME
        assert pa["user_id"] == _USER
        assert "Nothing was saved" in offer["decline_message"]
        # Strings only — the payload must snapshot cleanly (no datetimes).
        assert all(
            v is None or isinstance(v, str) for v in pa.values()
        ), pa

    def test_clarify_workflow_registered_offer_seam_only(self):
        register_default_workflows()
        from services.intent_service.workflow_dispatcher import (
            get_action_workflows,
            get_registered_workflows,
        )

        registered = get_registered_workflows()
        assert "clarify_reminder_task" in registered
        # Offer-seam only: never rail-dispatchable from a classified action.
        assert "clarify_reminder_task" not in get_action_workflows()

    def test_task_question_is_not_a_confirm_kind(self):
        """#1664 table pin: the task question is an OPEN question — it must
        never render '(yes/no)' framing via offer_is_confirm."""
        from services.intent_service import destructive_confirm as dc

        assert REMINDER_TASK_QUESTION_KIND not in dc._CONFIRM_KINDS
        assert dc.offer_is_confirm(build_reminder_task_offer(NO_TASK_NO_TIME, _USER)) is False

    @pytest.mark.asyncio
    async def test_no_task_arm_stores_what_it_says(self):
        """#1665 at the arm site, driven through the real handler: the armed
        record's question IS the returned message (one render)."""
        fake = _fake_service()
        handlers = TodoIntentHandlers()
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        message = await handlers.handle_create_reminder(
            Intent(
                category=IntentCategory.EXECUTION,
                action="create_reminder",
                confidence=1.0,
                original_message=NO_TASK_NO_TIME,
                context={},
            ),
            "sess-1654-1665",
            UUID(_USER),
            intent_service=fake,
        )
        stored = fake.workflow_offer_service.peek_pending_offer("sess-1654-1665")
        assert stored is not None
        assert stored["question"] == message
        assert stored["pending_action"]["kind"] == REMINDER_TASK_QUESTION_KIND


class TestPureTimeResidue1679:
    """#1679 — a pure-time extraction residue is NO task, never a title.

    'set a reminder for tomorrow at 3pm' matched the generic 'for'-form with
    group(1)='tomorrow at 3pm'; the trailing strip shed 'at 3pm' and the
    leading residue 'tomorrow' saved as a reminder literally titled
    'tomorrow' (live deterministic behavior, pre-classifier-claimed). Now the
    residue is recognized as pure time → extraction returns None → the #1654
    task-clarify carrier asks for the task.
    """

    def _handlers(self):
        from services.intent_service.todo_handlers import TodoIntentHandlers

        return TodoIntentHandlers.__new__(TodoIntentHandlers)

    def test_pure_time_residue_returns_none(self):
        h = self._handlers()
        assert h._extract_reminder_text("set a reminder for tomorrow at 3pm") is None
        assert h._extract_reminder_text("remind me about tomorrow") is None

    def test_real_tasks_still_extract(self):
        h = self._handlers()
        assert h._extract_reminder_text("remind me to buy milk tomorrow at 3pm") == "buy milk"
        assert (
            h._extract_reminder_text("set a reminder to call the vendor")
            == "call the vendor"
        )

    def test_task_containing_a_time_word_survives(self):
        # 'tomorrow' inside a real task is not a pure-time residue.
        h = self._handlers()
        assert (
            h._extract_reminder_text("remind me to prep tomorrow's agenda")
            == "prep tomorrow's agenda"
        )
