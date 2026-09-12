"""#1654 (#1739 acceptance-contract adoption, epic 3) — the reminder
task/time question seams consult THE predicate; questions never bind.

The filed defect class (fabrication-adjacent, orphaned clarify answer) had
its ARM half fixed earlier under this issue (the carrier + the floor-routing
fix); what remained was the CONSUME half: both kind-specific turn handlers
(``handle_reminder_task_turn`` / ``handle_reminder_time_turn``) still ran
the legacy ``detect_offer_response`` and had NO question-form gate — so
contract axis (a) was violated at both seams, in three live-reachable
shapes (all reproduced RED on 2026-09-12 before the fix):

- task turn, unclaimed question: "what do you mean?" BOUND AS THE TASK —
  the chain replied "Got it — **what do you mean**. When should I remind
  you?" (a state query consumed as an answer).
- task turn, pre-classifier-claimed question: "what reminders do I have?"
  released via the pop and the ARM SILENTLY DROPPED — the user's next bare
  task phrase then orphaned into the routing chain, which is the ISSUE'S
  OWN defect shape resurfacing one turn later (the #1652 finding: the
  off-intent pop silently cost the user the pending ask).
- time turn, time-bearing question: "did I say 3pm?" parsed the clock time
  and SAVED A REMINDER off a state question — an action fired from a turn
  that granted nothing (the worst axis-(a) shape).

Adopted per the #1653/#1652 precedents: both seams consult
``acceptance.evaluate_acceptance`` at their REGISTRY-DECLARED axes
(clarify_reminder_task / clarify_reminder_time: READ×PRIVATE →
LOW_CEREMONY) with the arm-site's stored ask threaded (#1665).
STATE_QUESTION falls through to the generic seam's already-adopted READ
branch — the SILENT §5a survival form (stated in-branch): the arm re-arms,
normal processing answers, and nothing can fire from the survived arm
because the REAL save runs only off a fresh ANSWER turn.

Layer honesty (m-43): the e2e class drives the REAL
``IntentService.process_intent`` with an explosive LLM — every pinned turn
resolves deterministically. The seam classes drive the turn handlers
directly for shapes the explosive harness can't route (questions no
deterministic surface claims).
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.soft_invocation import WorkflowOfferService
from services.intent_service.todo_handlers import (
    _TASK_REASK_TAIL,
    _TIME_ASK,
    REMINDER_TASK_QUESTION_KIND,
    REMINDER_TIME_QUESTION_KIND,
    build_reminder_task_offer,
    build_reminder_time_offer,
    handle_reminder_task_turn,
    handle_reminder_time_turn,
)
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import EffectClass, Outwardness

GATE = "services.intent_service.collaboration_gate"

_USER = "3f7b8a52-1654-4b00-9e00-000000001739"

NO_TASK_NO_TIME = "set a reminder: check the oven"

_TASK_ASK = "what should it say?"
_TIME_ASK_STORED = "when should I remind you?"


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM. Every pinned
    turn must resolve deterministically (offer seam / pre-classifier)."""

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
    mock = MagicMock()
    mock.create_todo = AsyncMock(return_value=SimpleNamespace(id=uuid4(), text="whatever"))
    mock.list_todos = AsyncMock(return_value=[])
    svc.todo_handlers.todo_service = mock
    return mock


async def _fire_no_task_ask(svc, sid, message=NO_TASK_NO_TIME):
    with patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})):
        return await svc.process_intent(message=message, session_id=sid, user_id=_USER)


def _fake_service():
    """Minimal seam double: an offer store + a recording todo service."""
    todo_service = MagicMock()
    todo_service.create_todo = AsyncMock(return_value=SimpleNamespace(id=uuid4(), text="x"))
    return SimpleNamespace(
        workflow_offer_service=WorkflowOfferService(),
        todo_handlers=SimpleNamespace(todo_service=todo_service),
    )


def _task_offer(question=_TASK_ASK):
    return build_reminder_task_offer(NO_TASK_NO_TIME, _USER, question=question)


def _time_offer(question=_TIME_ASK_STORED):
    return build_reminder_time_offer("buy milk", _USER, question=question)


# ---------------------------------------------------------------------------
# 1. Task-question seam — contract axis (a): questions never bind as tasks.
# ---------------------------------------------------------------------------


class TestTaskTurnAcceptanceSeam:
    pytestmark = pytest.mark.asyncio

    async def test_question_turn_never_binds_as_task(self):
        """RED pre-fix: "what do you mean?" (no deterministic surface claims
        it) fell through the release checks and BOUND as the task — the
        chain confirmed "**what do you mean**". A state question must fall
        through (None → generic seam's adopted READ branch re-arms silently
        and normal processing answers)."""
        fake = _fake_service()
        result = await handle_reminder_task_turn(
            _task_offer(),
            "what do you mean?",
            session_id="s-1654-q1",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is None
        fake.todo_handlers.todo_service.create_todo.assert_not_awaited()
        # No chain arm either — the seam stored nothing on this turn.
        assert fake.workflow_offer_service.peek_pending_offer("s-1654-q1") is None

    async def test_opener_question_without_mark_never_binds(self):
        """Interrogative-opener shape with no "?" (the PM transcript shape
        the contract names) — same axis-(a) gate."""
        fake = _fake_service()
        result = await handle_reminder_task_turn(
            _task_offer(),
            "is that everything you need",
            session_id="s-1654-q2",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is None
        fake.todo_handlers.todo_service.create_todo.assert_not_awaited()

    async def test_crisp_confirm_reasks_instead_of_binding(self):
        """The crisp CONFIRM superset ("confirm", "y") lands ACCEPT at the
        predicate — and an accept doesn't name a task, so it re-asks. RED
        pre-fix: the legacy detector didn't know "confirm", so it BOUND as
        the task text."""
        fake = _fake_service()
        result = await handle_reminder_task_turn(
            _task_offer(),
            "confirm",
            session_id="s-1654-confirm",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is not None
        assert _TASK_REASK_TAIL in result["message"]
        stored = fake.workflow_offer_service.peek_pending_offer("s-1654-confirm")
        assert stored["pending_action"]["kind"] == REMINDER_TASK_QUESTION_KIND
        fake.todo_handlers.todo_service.create_todo.assert_not_awaited()

    async def test_predicate_receives_stored_ask_and_declared_axes(self):
        """#1665 threading + explicit axes pin: the seam consults THE
        predicate with the arm-site's stored ask and the registry-declared
        READ×PRIVATE axes (→ LOW_CEREMONY)."""
        from services.intent_service import acceptance as acceptance_module

        fake = _fake_service()
        real = acceptance_module.evaluate_acceptance
        with patch.object(acceptance_module, "evaluate_acceptance", side_effect=real) as spy:
            await handle_reminder_task_turn(
                _task_offer(question=_TASK_ASK),
                "what do you mean?",
                session_id="s-1654-spy",
                user_id=_USER,
                intent_service=fake,
            )
        assert spy.call_count == 1
        kwargs = spy.call_args.kwargs
        assert kwargs["armed_question"] == _TASK_ASK
        assert kwargs["effect"] == EffectClass.READ
        assert kwargs["outwardness"] == Outwardness.PRIVATE

    async def test_decline_still_falls_through(self):
        """Behavior preservation: "no" falls through to the generic honest
        decline (the predicate's DECLINE vocabulary covers the legacy rows)."""
        fake = _fake_service()
        result = await handle_reminder_task_turn(
            _task_offer(),
            "no",
            session_id="s-1654-no",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is None
        fake.todo_handlers.todo_service.create_todo.assert_not_awaited()

    async def test_bare_task_answer_still_binds(self):
        """Behavior preservation: the ask's whole point — a bare task phrase
        (predicate verdict PASS) binds and chains into the time question."""
        fake = _fake_service()
        result = await handle_reminder_task_turn(
            _task_offer(),
            "buy milk",
            session_id="s-1654-bind",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is not None
        assert "**buy milk**" in result["message"]
        assert _TIME_ASK in result["message"]
        stored = fake.workflow_offer_service.peek_pending_offer("s-1654-bind")
        assert stored["pending_action"]["kind"] == REMINDER_TIME_QUESTION_KIND
        assert stored["pending_action"]["task_text"] == "buy milk"


# ---------------------------------------------------------------------------
# 2. Time-question seam — the same gate, where the stakes are a real WRITE.
# ---------------------------------------------------------------------------


class TestTimeTurnAcceptanceSeam:
    pytestmark = pytest.mark.asyncio

    async def test_time_bearing_question_never_saves(self):
        """RED pre-fix (the worst shape): "did I say 3pm?" carried a
        parseable clock time, so the seam parsed it and SAVED A REMINDER off
        a state question. Axis (a): a question never consents — checked
        BEFORE the time-signal bind."""
        fake = _fake_service()
        result = await handle_reminder_time_turn(
            _time_offer(),
            "did I say 3pm?",
            session_id="s-1654-t1",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is None
        fake.todo_handlers.todo_service.create_todo.assert_not_awaited()

    async def test_uncertain_time_answer_costs_a_turn_not_an_action(self):
        """ "tomorrow at 9?" is question-shaped — under the contract it
        survives as a state question (the arm re-arms at the generic seam;
        a follow-up "at 9" still saves). Deliberate axis-(a) pin: an
        ambiguous acceptance costs a turn, not an action (§5b). RED
        pre-fix: it saved."""
        fake = _fake_service()
        result = await handle_reminder_time_turn(
            _time_offer(),
            "tomorrow at 9?",
            session_id="s-1654-t2",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is None
        fake.todo_handlers.todo_service.create_todo.assert_not_awaited()

    async def test_plain_state_question_falls_through_for_an_answer(self):
        """RED pre-fix: a question with no time signal got the re-ask copy
        ("I still need a time for it") — ignoring what the user asked.
        Post-adoption it falls through so normal processing ANSWERS (the
        generic READ branch re-arms the offer silently, §5a)."""
        fake = _fake_service()
        result = await handle_reminder_time_turn(
            _time_offer(),
            "what was it for again?",
            session_id="s-1654-t3",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is None
        fake.todo_handlers.todo_service.create_todo.assert_not_awaited()

    async def test_predicate_receives_stored_ask_and_declared_axes(self):
        from services.intent_service import acceptance as acceptance_module

        fake = _fake_service()
        real = acceptance_module.evaluate_acceptance
        with patch.object(acceptance_module, "evaluate_acceptance", side_effect=real) as spy:
            await handle_reminder_time_turn(
                _time_offer(question=_TIME_ASK_STORED),
                "what was it for again?",
                session_id="s-1654-tspy",
                user_id=_USER,
                intent_service=fake,
            )
        assert spy.call_count == 1
        kwargs = spy.call_args.kwargs
        assert kwargs["armed_question"] == _TIME_ASK_STORED
        assert kwargs["effect"] == EffectClass.READ
        assert kwargs["outwardness"] == Outwardness.PRIVATE

    async def test_time_answer_still_saves(self):
        """Behavior preservation: a plain time answer (PASS at the
        predicate) still performs the REAL save with the 📅 copy."""
        fake = _fake_service()
        result = await handle_reminder_time_turn(
            _time_offer(),
            "at 3pm tomorrow",
            session_id="s-1654-save",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is not None
        fake.todo_handlers.todo_service.create_todo.assert_awaited_once()
        kwargs = fake.todo_handlers.todo_service.create_todo.await_args.kwargs
        assert kwargs["text"] == "buy milk"
        assert kwargs["reminder_date"].hour == 15
        assert "Reminder saved" in result["message"]
        assert "📅" in result["message"]

    async def test_decline_still_falls_through(self):
        fake = _fake_service()
        result = await handle_reminder_time_turn(
            _time_offer(),
            "no",
            session_id="s-1654-tno",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is None
        fake.todo_handlers.todo_service.create_todo.assert_not_awaited()

    async def test_bare_yes_still_reasks(self):
        """Behavior preservation: ACCEPT doesn't answer "when?" — honest
        re-ask, re-armed (#1648 direction 2)."""
        fake = _fake_service()
        result = await handle_reminder_time_turn(
            _time_offer(),
            "yes",
            session_id="s-1654-tyes",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is not None
        assert "I still need a time" in result["message"]
        stored = fake.workflow_offer_service.peek_pending_offer("s-1654-tyes")
        assert stored["pending_action"]["kind"] == REMINDER_TIME_QUESTION_KIND


# ---------------------------------------------------------------------------
# 3. Arm survival, pinned e2e — the question costs a turn, never the ask.
# ---------------------------------------------------------------------------


class TestArmSurvivalEndToEnd:
    pytestmark = pytest.mark.asyncio

    async def test_task_arm_survives_a_state_question(self, svc):
        """Survival pin. Pre-fix this held only BY COMPOSITION: the seam
        released the pre-classifier-claimed question (None) and the generic
        seam's already-adopted READ branch happened to catch it and re-arm —
        the seam itself had no axis-(a) gate (an UNCLAIMED question bound as
        the task instead; see the seam class). Post-adoption the survival is
        the seam's own STATE_QUESTION verdict, deliberate: the question is
        ANSWERED (deterministic list handler), the arm survives (silent §5a
        re-arm), and the next turn still binds."""
        sid = "e2e-1654-task-survival"
        mock = _mock_todo_service(svc)
        r1 = await _fire_no_task_ask(svc, sid)

        r2 = await svc.process_intent(
            message="what reminders do I have?", session_id=sid, user_id=_USER
        )
        mock.create_todo.assert_not_awaited()
        # The question got a real answer, not a bind and not the re-ask.
        assert "there are none right now" in r2.message
        assert _TASK_REASK_TAIL not in r2.message
        # The arm survived, stored ask intact (#1665).
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["kind"] == REMINDER_TASK_QUESTION_KIND
        assert stored["question"] == r1.message

        # And the recovery still completes: the next bare phrase binds.
        r3 = await svc.process_intent(message="check the oven", session_id=sid, user_id=_USER)
        assert "**check the oven**" in r3.message
        assert _TIME_ASK in r3.message
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["kind"] == REMINDER_TIME_QUESTION_KIND

    async def test_time_arm_survives_a_state_question(self, svc):
        """Same survival contract at the chained time question: the state
        question is answered, the arm (with its bound task) survives, and
        the time answer still performs the REAL save."""
        sid = "e2e-1654-time-survival"
        mock = _mock_todo_service(svc)
        await _fire_no_task_ask(svc, sid)
        await svc.process_intent(message="buy milk", session_id=sid, user_id=_USER)

        r3 = await svc.process_intent(
            message="what reminders do I have?", session_id=sid, user_id=_USER
        )
        mock.create_todo.assert_not_awaited()
        assert "there are none right now" in r3.message
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["kind"] == REMINDER_TIME_QUESTION_KIND
        assert stored["pending_action"]["task_text"] == "buy milk"

        r4 = await svc.process_intent(message="at 3pm tomorrow", session_id=sid, user_id=_USER)
        mock.create_todo.assert_awaited_once()
        kwargs = mock.create_todo.await_args.kwargs
        assert kwargs["text"] == "buy milk"
        assert kwargs["reminder_date"].hour == 15
        assert "Reminder saved" in r4.message
        assert "📅" in r4.message
        assert _pending_offers(svc) == {}
