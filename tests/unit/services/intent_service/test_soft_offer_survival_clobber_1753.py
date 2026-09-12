"""#1753 — a soft workflow offer must never clobber a STATE_QUESTION-survived
arm: the ``_pending_flags`` no-clobber guard reads only ``result.intent_data``,
and survival turns compose their result in NORMAL PROCESSING with no flag.

The filed gap (found by the #1654 lane reading the seam composition): every
#1739-adopted seam has a second way an arm can be live when
``_apply_soft_offer`` runs — the STATE_QUESTION survival turn (contract doc
§5a). The seam RE-ARMS the offer silently and lets normal processing answer
the question, so the final result is composed by whatever handler answered
(floor, reminders list, …) and carries no ``*_pending`` flag. If the
ProactivityGate + throttle allow a soft offer on that same turn,
``set_pending_offer`` replaces the survived arm in the one-slot #846 store —
the question silently costs the user their pending ask, exactly the failure
the survival ruling exists to prevent.

Fix under test: THE STORE is the single source of truth for "an arm is live
right now". ``process_intent`` pops the one-slot store at turn start (the
#1529 binding semantic), so any entry present when ``_apply_soft_offer``
considers setting was armed — or re-armed via survival — THIS turn;
``_apply_soft_offer`` peeks (#1595, read-only) and skips the soft offer
honestly instead of replacing the arm. The #1652 flag guard REMAINS (belt;
its pins must not regress) — the store guard covers what flags structurally
cannot: turns whose result the arm's owner never composes.

Layer honesty (m-43): the e2e classes drive the REAL
``IntentService.process_intent`` mocked only at the LLM boundary (explosive —
turns resolve at the pending-offer seam or stubbed classification), the
users.preferences seam, and — for the clobber half — the soft-offer DETECTOR
+ throttle gate stubbed OPEN (the #1652 idiom: what stands between them and
the one-slot store is exactly the guard under test). The guard-unit and
no-over-block classes pin ``_apply_soft_offer`` directly.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service import reminder_clear as rc
from services.intent_service.classifier import IntentClassifier
from services.intent_service.soft_invocation import SoftInvocationResult, WorkflowOffer
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import IntentCategory

_USER = "3f7b8a52-1753-4b00-9e00-000000001753"  # valid UUID: survives principal parsing

_MEETING_ASK = "I could help set up a meeting. Want me to find a time?"

# The clobberer is a DIFFERENT workflow type than either survived arm, so a
# replaced store entry is unambiguous in the asserts.
_CLOBBER_ASK = "I could help you set up a project structure. Want that?"


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM. Every turn in
    these tests must resolve deterministically."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1753 turns must resolve deterministically"
        )


@pytest.fixture
def live_service():
    register_default_workflows()
    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


def _open_soft_offer_conditions(service):
    """Make the soft-offer path WANT to clobber (the #1652 idiom): the
    detector reports an offer on any message and the throttle gate is open.
    What stands between them and the one-slot store is the guard under
    test."""
    service.soft_invocation_detector.detect = MagicMock(
        return_value=SoftInvocationResult(
            has_offer=True,
            offer=WorkflowOffer(
                workflow_type="project_setup",
                offer_message=_CLOBBER_ASK,
                decline_message="No worries.",
                confidence=0.9,
            ),
        )
    )
    service.workflow_offer_service.should_offer = MagicMock(return_value=(True, "gate-open"))


def _close_soft_offer_conditions(service):
    """Shut the gate for follow-up turns whose own behavior is under test
    (the survived arm binding the next answer) — otherwise the accept turn's
    empty store legitimately takes a fresh offer and muddies the asserts."""
    service.workflow_offer_service.should_offer = MagicMock(return_value=(False, "gate-closed"))


def _stub_fallthrough_routing(service, message):
    """After a silent survival re-arm, normal processing answers the turn —
    its routing is not under test. The #1652/#1653 idiom: classification
    returns a low-confidence UNKNOWN and the floor door is patched. The
    patched floor result carries NO ``*_pending`` flag — that flag-less
    composition is the filed gap."""
    from services.intent_service.pre_classifier import MultiIntentResult

    fallback = Intent(
        category=IntentCategory.UNKNOWN,
        action="unknown",
        confidence=0.2,
        original_message=message,
        context={"original_message": message},
    )
    return patch.object(
        service.intent_classifier,
        "classify_multiple",
        new=AsyncMock(return_value=MultiIntentResult(intents=[fallback], original_message=message)),
    ), patch.object(
        service,
        "_handle_unknown_intent",
        new=AsyncMock(
            return_value=IntentProcessingResult(success=True, message="ok", intent_data={})
        ),
    )


def _arm_meeting_offer(service, sid):
    """Arm the registered READ-tier soft offer ("meeting") the way the arm
    site does since 2026-09-09 — rendered ask on the record (#1665)."""
    service.workflow_offer_service.set_pending_offer(
        sid,
        {
            "workflow_type": "meeting",
            "offer_message": _MEETING_ASK,
            "question": _MEETING_ASK,
            "decline_message": "No worries, just let me know if you change your mind.",
            "trigger_message": "we should sync up about the launch",
        },
    )


# ---------------------------------------------------------------------------
# 1. THE filed gap, generic READ kind: the survived arm outlives a turn on
#    which a soft offer fires (e2e, real process_intent)
# ---------------------------------------------------------------------------


class TestGenericReadSurvivalOutlivesSoftOffer:
    pytestmark = pytest.mark.asyncio

    async def test_survived_meeting_arm_is_not_clobbered_by_a_soft_offer(self, live_service):
        """RED pre-fix: the state question re-arms the meeting offer (§5a),
        normal processing composes a flag-less result, and the open
        soft-offer path replaces the survived arm with project_setup in the
        one-slot store."""
        sid = "e2e-1753-read-survival"
        _arm_meeting_offer(live_service, sid)
        _open_soft_offer_conditions(live_service)
        question = "what would that involve?"
        p_classify, p_floor = _stub_fallthrough_routing(live_service, question)
        with p_classify, p_floor:
            await live_service.process_intent(message=question, session_id=sid, user_id=_USER)
        stored = _pending_offers(live_service).get(sid)
        assert stored is not None, "#1753: the soft offer emptied/clobbered the survived arm"
        assert stored["workflow_type"] == "meeting", (
            "#1753: the soft workflow offer REPLACED the STATE_QUESTION-"
            "survived arm in the one-slot store — the question silently cost "
            "the user their pending ask"
        )
        assert stored["question"] == _MEETING_ASK

    async def test_survived_arm_still_binds_the_next_yes_after_the_offer_turn(self, live_service):
        """The survived arm is a live ask across BOTH hazards: the question
        turn AND the soft-offer application. The next bare "yes" dispatches
        the ORIGINAL meeting workflow, not the clobberer."""
        sid = "e2e-1753-read-survival-yes"
        _arm_meeting_offer(live_service, sid)
        _open_soft_offer_conditions(live_service)
        question = "what would that involve?"
        p_classify, p_floor = _stub_fallthrough_routing(live_service, question)
        with p_classify, p_floor:
            await live_service.process_intent(message=question, session_id=sid, user_id=_USER)
        _close_soft_offer_conditions(live_service)
        result = await live_service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert result.success
        # The yes consumed the SURVIVED meeting arm — nothing left pending,
        # and the reply is not the clobberer's copy.
        assert _pending_offers(live_service).get(sid) is None
        assert _CLOBBER_ASK not in (result.message or "")


# ---------------------------------------------------------------------------
# 2. THE filed gap, seam-specific path: the reminder VERB QUESTION survives
#    via the kind-specific fall-through (#1653) — same clobber window
# ---------------------------------------------------------------------------


@pytest.fixture
def pref_store(monkeypatch):
    """In-memory users.preferences JSONB behind collaboration_gate's seam."""
    from services.intent_service import collaboration_gate as cg

    store: dict = {}

    async def _load(user_id):
        return dict(store)

    async def _save(user_id, key, value):
        store[key] = value
        return True

    monkeypatch.setattr(cg, "_load_preferences", _load)
    monkeypatch.setattr(cg, "_save_preference", _save)
    return store


@pytest.fixture
def todo_boundary(monkeypatch):
    """TodoManagementService boundary: list deterministic; mutations
    EXPLOSIVE (nothing may fire from a survived arm)."""
    from datetime import datetime, timezone
    from uuid import uuid4

    from services.domain.models import Todo
    from services.todo.todo_management_service import TodoManagementService

    todos = [
        Todo(
            id=str(uuid4()),
            text="Review the PR",
            priority="medium",
            status="pending",
            completed=False,
            reminder_date=datetime(2026, 9, 12, 9, 0, tzinfo=timezone.utc),
        ),
        Todo(
            id=str(uuid4()),
            text="Call the vendor",
            priority="medium",
            status="pending",
            completed=False,
            reminder_date=datetime(2026, 9, 12, 10, 0, tzinfo=timezone.utc),
        ),
    ]

    async def _list_todos(self, user_id, include_completed=False):
        return list(todos)

    async def _explosive_complete(self, todo_id, user_id):
        raise AssertionError("complete_todo FIRED from a survived arm (#1753)")

    async def _explosive_delete(self, todo_id, user_id):
        raise AssertionError("delete_todo FIRED from a survived arm (#1753)")

    monkeypatch.setattr(TodoManagementService, "list_todos", _list_todos)
    monkeypatch.setattr(TodoManagementService, "complete_todo", _explosive_complete)
    monkeypatch.setattr(TodoManagementService, "delete_todo", _explosive_delete)
    return todos


def _stub_classification(monkeypatch, service, message, action):
    intent = Intent(
        category=IntentCategory.EXECUTION,
        action=action,
        original_message=message,
        confidence=0.95,
        context={"original_message": message},
    )

    async def _classify_multiple(msg, context=None, user_id=None, session_id=None):
        return SimpleNamespace(
            intents=[intent],
            is_multi_intent=False,
            has_greeting=False,
            has_substantive_intent=True,
            primary_intent=intent,
            secondary_intents=[],
        )

    monkeypatch.setattr(service.intent_classifier, "classify_multiple", _classify_multiple)


class TestReminderVerbQuestionSurvivalOutlivesSoftOffer:
    pytestmark = pytest.mark.asyncio

    async def _arm_verb_question(self, monkeypatch, service, sid):
        """Turn 1: 'clear my reminders' arms the #1605 variant-1 verb
        question (the #1653 idiom)."""
        _stub_classification(monkeypatch, service, "clear my reminders", "complete_todo")
        await service.process_intent(message="clear my reminders", session_id=sid, user_id=_USER)
        stored = _pending_offers(service).get(sid)
        assert stored is not None
        assert stored["pending_action"]["kind"] == rc.CLEAR_VERB_QUESTION_KIND
        return stored

    async def test_survived_verb_question_is_not_clobbered_by_a_soft_offer(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """RED pre-fix: 'are you going to delete them?' survives via the
        kind-specific STATE_QUESTION fall-through (#1653) + the generic READ
        branch's silent §5a re-arm — then the open soft-offer path replaces
        the survived verb question in the one-slot store."""
        sid = "e2e-1753-verb-survival"
        await self._arm_verb_question(monkeypatch, live_service, sid)
        _open_soft_offer_conditions(live_service)
        question = "are you going to delete them?"
        p_classify, p_floor = _stub_fallthrough_routing(live_service, question)
        with p_classify, p_floor:
            await live_service.process_intent(message=question, session_id=sid, user_id=_USER)
        stored = _pending_offers(live_service).get(sid)
        assert stored is not None, "#1753: the soft offer emptied/clobbered the survived arm"
        assert stored.get("pending_action", {}).get("kind") == rc.CLEAR_VERB_QUESTION_KIND, (
            "#1753: the soft workflow offer REPLACED the survived reminder "
            "verb question in the one-slot store"
        )

    async def test_survived_verb_question_still_binds_the_next_crisp_answer(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """Across BOTH hazards, the survived verb question is a live ask:
        the next crisp 'delete them' stores the mapping and arms the REAL
        #1190 confirm (delete still explosive-gated behind the yes)."""
        from services.intent_service.destructive_confirm import (
            CONFIRM_PENDING_ACTION_WORKFLOW,
        )
        from services.intent_service.reminder_clear import variant_three_question

        sid = "e2e-1753-verb-survival-answer"
        await self._arm_verb_question(monkeypatch, live_service, sid)
        _open_soft_offer_conditions(live_service)
        question = "are you going to delete them?"
        p_classify, p_floor = _stub_fallthrough_routing(live_service, question)
        with p_classify, p_floor:
            await live_service.process_intent(message=question, session_id=sid, user_id=_USER)
        _close_soft_offer_conditions(live_service)
        result = await live_service.process_intent(
            message="delete them", session_id=sid, user_id=_USER
        )
        assert result.message.startswith(variant_three_question(2))
        record = pref_store["verified_inferences"][rc.inference_key("clear")]
        assert record["value"] == rc.VALUE_DELETE
        stored = _pending_offers(live_service).get(sid)
        assert stored["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW


# ---------------------------------------------------------------------------
# 3. Guard unit pin — the STORE, not the result's flags, is what protects a
#    survival turn at the apply seam
# ---------------------------------------------------------------------------


class TestStoreGuardAtTheApplySeam:
    def test_live_store_entry_short_circuits_before_detection(self, live_service):
        """A live arm in the store with a FLAG-LESS result (the survival-turn
        composition) short-circuits ``_apply_soft_offer`` BEFORE detection —
        message unmodified, store untouched."""
        sid = "unit-1753-store-guard"
        _arm_meeting_offer(live_service, sid)
        _open_soft_offer_conditions(live_service)
        result = IntentProcessingResult(
            success=True,
            message="the answer to the state question",
            intent_data={"category": "unknown", "action": "unknown"},  # no *_pending flag
        )
        out = live_service._apply_soft_offer(result, "what would that involve?", sid)
        assert out.message == "the answer to the state question"
        stored = _pending_offers(live_service)[sid]
        assert stored["workflow_type"] == "meeting"
        assert stored["question"] == _MEETING_ASK
        live_service.soft_invocation_detector.detect.assert_not_called()

    def test_flag_guard_still_holds_no_1652_regression(self, live_service):
        """The #1652 flag belt remains: a flagged result short-circuits even
        with an empty store (the ARM-turn shape, where the arm site already
        returned the store entry and stamped the flag)."""
        sid = "unit-1753-flag-guard"
        _open_soft_offer_conditions(live_service)
        result = IntentProcessingResult(
            success=True,
            message="report text",
            intent_data={"category": "status", "standup_interview_invitation_pending": True},
        )
        out = live_service._apply_soft_offer(result, "any message", sid)
        assert out.message == "report text"
        assert _pending_offers(live_service).get(sid) is None
        live_service.soft_invocation_detector.detect.assert_not_called()


# ---------------------------------------------------------------------------
# 4. No over-block — a genuinely free turn still gets offers
# ---------------------------------------------------------------------------


class TestFreeTurnsStillGetOffers:
    def test_empty_store_and_no_flags_applies_the_offer(self, live_service):
        """The guard must not dampen soft invocation on free turns: empty
        store + flag-less result → the offer applies, message appended,
        store armed with the offer."""
        sid = "unit-1753-free-turn"
        _open_soft_offer_conditions(live_service)
        result = IntentProcessingResult(
            success=True,
            message="here's your answer",
            intent_data={"category": "unknown", "action": "unknown"},
        )
        out = live_service._apply_soft_offer(result, "set up the project", sid)
        assert _CLOBBER_ASK in out.message
        stored = _pending_offers(live_service).get(sid)
        assert stored is not None
        assert stored["workflow_type"] == "project_setup"
        assert stored["question"] == _CLOBBER_ASK
