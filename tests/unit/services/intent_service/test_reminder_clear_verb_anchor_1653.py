"""#1653 [MVP] — confirm-greed residue: the verb-question answer shared the
unanchored delete claim (#1650's fix covered the correction window only).

The filed defect: ``reminder_clear._handle_verb_answer_turn`` detected the
delete answer with the same unanchored ``\\bdelete\\b`` substring the
correction window had before #1650 — so with the verb QUESTION armed
("mark it done, or delete it? I'll remember for next time"), a prose aside
that merely MENTIONS deleting (PM's live one-liner, ~95 chars, under the
#1631 floor) read as "the verb means delete" and stored a wrong, STICKY
verb default (actual deletion stayed gated behind the strict #1190 confirm,
so no data loss — but every later "clear" would lead with delete).

The fix is the #1739 acceptance-contract adoption for the reminder_clear
kind-specific turns, axes mapped explicitly:

- The SEAM's armed workflow (``clarify_reminder_clear_verb``) is
  registry-declared READ×PRIVATE → LOW_CEREMONY; a STATE_QUESTION verdict
  falls through to the generic seam's already-adopted READ branch, which
  re-arms SILENTLY (contract doc §5a READ row) and lets normal processing
  answer. Nothing can fire from the survived arm — the delete path still
  runs through the #1190 NAMED_OBJECT confirm.
- The DELETE CLAIM's target action (``clear_reminders_delete``) is
  registry-declared DESTRUCTIVE×PRIVATE → NAMED_OBJECT, so the claim takes
  the #1650 crisp bar: anchored ``_CORRECTION_CLAIM_RE`` (the SAME pattern,
  reused — no new extraction regex) + the #1631 prose floor + never a
  question-shaped turn.
- The COMPLETE claim's target (``complete_todo``) is WRITE×PRIVATE →
  LOW_CEREMONY: word-level detection stands, gated by the prose floor only
  (contract axis (c): asides neither accept nor steal — at every tier).
- The correction window gets the same axis-(a) gate: "delete them?" is a
  state query, not a correction claim.

Issue residue 2 is pinned as DELIBERATE, not fixed: an echo-answer to the
armed destructive confirm ("yes, delete them") is not crisp full-message
affirmative vocabulary, so nothing fires (the pop stands; normal processing
answers). If live use shows users echo verbs often, verb-echo forms (echo
matching the ARMED action's verb) may join the crisp set — a separate,
evidence-gated change.

Layer honesty (m-43): the unit class pins the axes/tier derivation; the
end-to-end classes drive the REAL ``IntentService.process_intent`` (the
#1605/#1650 test idiom), mocked only at the LLM boundary (explosive — turns
must resolve at the pending-offer seam or the stubbed classification), the
TodoManagementService boundary (explosive wherever nothing may mutate), and
the users.preferences JSONB boundary (in-memory dict behind
collaboration_gate's seam — the REAL verified-inference paths run).
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service import reminder_clear as rc
from services.intent_service.acceptance import (
    AcceptanceTier,
    acceptance_tier,
    declared_axes_for_workflow,
)
from services.intent_service.classifier import IntentClassifier
from services.intent_service.destructive_confirm import (
    CONFIRM_PENDING_ACTION_WORKFLOW,
)
from services.intent_service.reminder_clear import variant_three_question
from services.shared_types import EffectClass, IntentCategory, Outwardness

_USER = "3f7b8a52-1653-4b00-9e00-000000001653"  # valid UUID: survives principal parsing

# PM's exact aside, verbatim from the #1650 live transcript (one line,
# ~95 chars — under the #1631 floor, which is what makes anchoring, not the
# prose floor, the operative guard).
PM_ASIDE = (
    "please note that I'll need to figure out later why you thought I "
    "wanted you to delete a project."
)


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1653 turns must resolve deterministically"
        )


@pytest.fixture
def live_service():
    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


def _stub_classification(monkeypatch, service, message, action, category=IntentCategory.EXECUTION):
    """Deterministic classification for the arming turn (the LLM boundary
    stays explosive for everything else)."""
    intent = Intent(
        category=category,
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
    return intent


def _stub_fallthrough_routing(service, message):
    """After a fall-through (silent survival, or an off-intent pop) normal
    processing answers the turn — its routing is not under test. The #1652
    idiom: classification returns a low-confidence UNKNOWN and the floor
    door is patched."""
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
        new=AsyncMock(return_value=MagicMock(success=True, message="ok", intent_data={})),
    )


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


def _reminder_todos():
    from datetime import datetime, timezone

    from services.domain.models import Todo

    return [
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


@pytest.fixture
def todo_boundary(monkeypatch):
    """TodoManagementService boundary: list deterministic; complete/delete
    EXPLOSIVE until a test arms them (nothing may mutate unconfirmed)."""
    from services.todo.todo_management_service import TodoManagementService

    state = {
        "todos": _reminder_todos(),
        "completed": [],
        "deleted": [],
        "allow_complete": False,
        "allow_delete": False,
    }

    async def _list_todos(self, user_id, include_completed=False):
        return list(state["todos"])

    async def _complete(self, todo_id, user_id):
        if not state["allow_complete"]:
            raise AssertionError(
                "todo_service.complete_todo FIRED — a mutation executed on a "
                "turn that must not mutate (#1653 gate breach)"
            )
        state["completed"].append(str(todo_id))
        for t in state["todos"]:
            if t.id == str(todo_id):
                return t
        return None

    async def _delete(self, todo_id, user_id):
        if not state["allow_delete"]:
            raise AssertionError(
                "todo_service.delete_todo FIRED — a destructive mutation "
                "executed without a confirmed yes (#1653/#1190 gate breach)"
            )
        state["deleted"].append(str(todo_id))
        return True

    monkeypatch.setattr(TodoManagementService, "list_todos", _list_todos)
    monkeypatch.setattr(TodoManagementService, "complete_todo", _complete)
    monkeypatch.setattr(TodoManagementService, "delete_todo", _delete)
    return state


def _seed_verb_default(pref_store, value, source="user_verified"):
    pref_store["verified_inferences"] = {
        rc.inference_key("clear"): {
            "value": value,
            "source": source,
            "confidence_at_verification": rc.VERB_CONFIDENCE,
            "verified_at": "2026-09-12T08:00:00+00:00",
        }
    }


async def _arm_verb_question(monkeypatch, service, sid):
    """Turn 1: 'clear my reminders' (classified complete_todo) arms the
    variant-1 verb question."""
    _stub_classification(monkeypatch, service, "clear my reminders", "complete_todo")
    await service.process_intent(message="clear my reminders", session_id=sid, user_id=_USER)
    stored = _pending_offers(service).get(sid)
    assert stored is not None
    assert stored["pending_action"]["kind"] == rc.CLEAR_VERB_QUESTION_KIND
    return stored


def _no_delete_default_stored(pref_store):
    record = (pref_store.get("verified_inferences") or {}).get(rc.inference_key("clear"))
    return record is None or record["value"] != rc.VALUE_DELETE


# ---------------------------------------------------------------------------
# 1. Axes / tier mapping (unit) — the derivation the branch comments claim
# ---------------------------------------------------------------------------


class TestAxesAndTierMapping:
    def test_verb_question_seam_is_read_private_low_ceremony(self):
        axes = declared_axes_for_workflow(rc.CLARIFY_CLEAR_VERB_WORKFLOW)
        assert axes == (EffectClass.READ, Outwardness.PRIVATE)
        assert acceptance_tier(*axes) == AcceptanceTier.LOW_CEREMONY

    def test_correction_window_is_read_private_low_ceremony(self):
        axes = declared_axes_for_workflow(rc.CLEAR_CORRECTION_WORKFLOW)
        assert axes == (EffectClass.READ, Outwardness.PRIVATE)
        assert acceptance_tier(*axes) == AcceptanceTier.LOW_CEREMONY

    def test_delete_claim_target_is_destructive_named_object(self):
        """The claim's crispness bar derives from its TARGET action's axes —
        clear_reminders_delete is DESTRUCTIVE×PRIVATE → NAMED_OBJECT, which
        is why the delete claim takes the anchored #1650 treatment."""
        axes = declared_axes_for_workflow(rc.CLEAR_DELETE_WORKFLOW)
        assert axes == (EffectClass.DESTRUCTIVE, Outwardness.PRIVATE)
        assert acceptance_tier(*axes) == AcceptanceTier.NAMED_OBJECT


# ---------------------------------------------------------------------------
# 2. THE filed defect — a prose aside must not become a sticky verb default
# ---------------------------------------------------------------------------


class TestFiledDefect:
    pytestmark = pytest.mark.asyncio

    async def test_pm_aside_does_not_store_delete_default_or_arm_confirm(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """THE repro, verbatim from the issue's parent incident: with the
        verb QUESTION armed, PM's one-line aside (under the #1631 floor,
        so only anchoring can catch it) mentions 'delete' mid-sentence.
        RED pre-fix: the unanchored claim stored value=delete (wrong,
        sticky) and armed the V3 delete confirm."""
        assert len(PM_ASIDE) < 160 and "\n" not in PM_ASIDE
        sid = "e2e-1653-aside"
        await _arm_verb_question(monkeypatch, live_service, sid)
        p_classify, p_floor = _stub_fallthrough_routing(live_service, PM_ASIDE)
        with p_classify, p_floor:
            result = await live_service.process_intent(
                message=PM_ASIDE, session_id=sid, user_id=_USER
            )
        assert _no_delete_default_stored(pref_store), (
            "#1653: the aside was claimed as a verb answer — a wrong, sticky "
            "'clear'=delete default was stored"
        )
        stored = _pending_offers(live_service).get(sid)
        if stored is not None:
            assert stored["workflow_type"] != CONFIRM_PENDING_ACTION_WORKFLOW, (
                "#1653: the aside armed the V3 delete confirm — one crisp "
                "'yes' from deleting a batch PM never asked to delete"
            )
        assert variant_three_question(2) not in (result.message or "")
        assert todo_boundary["completed"] == [] and todo_boundary["deleted"] == []

    async def test_multiline_prose_mentioning_delete_never_claims(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """Contract axis (c) at this seam: prose by shape (multi-line) never
        claims a verb answer, whatever words it contains."""
        sid = "e2e-1653-prose-delete"
        await _arm_verb_question(monkeypatch, live_service, sid)
        prose = (
            "A few thoughts on this.\n"
            "I'm not sure whether delete is ever the right default here —\n"
            "let me think about it and get back to you."
        )
        p_classify, p_floor = _stub_fallthrough_routing(live_service, prose)
        with p_classify, p_floor:
            await live_service.process_intent(message=prose, session_id=sid, user_id=_USER)
        assert _no_delete_default_stored(pref_store)
        stored = _pending_offers(live_service).get(sid)
        if stored is not None:
            assert stored["workflow_type"] != CONFIRM_PENDING_ACTION_WORKFLOW
        assert todo_boundary["deleted"] == []

    async def test_long_prose_mentioning_done_never_stores_complete(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """The complete claim's target is LOW-tier (WRITE×PRIVATE), so
        word-level detection stands — but the prose floor still gates it
        (axis (c) applies at every tier). RED pre-fix: 'done' anywhere in
        long prose stored value=complete and tried to complete the batch
        (the explosive boundary is the tell)."""
        sid = "e2e-1653-prose-done"
        await _arm_verb_question(monkeypatch, live_service, sid)
        prose = (
            "I keep going back and forth on whether we are actually done "
            "with the vendor thread or whether there is still a follow-up "
            "owed — either way don't touch these until I've checked my notes."
        )
        assert len(prose) >= 160 and "\n" not in prose  # prose by LENGTH
        p_classify, p_floor = _stub_fallthrough_routing(live_service, prose)
        with p_classify, p_floor:
            await live_service.process_intent(message=prose, session_id=sid, user_id=_USER)
        record = (pref_store.get("verified_inferences") or {}).get(rc.inference_key("clear"))
        assert record is None, "#1653: long prose mentioning 'done' was claimed as a verb answer"
        assert todo_boundary["completed"] == []


# ---------------------------------------------------------------------------
# 3. State questions — never a claim; the arm survives silently (§5a, READ)
# ---------------------------------------------------------------------------


class TestStateQuestionSurvival:
    pytestmark = pytest.mark.asyncio

    @pytest.mark.parametrize(
        "question",
        [
            "delete them?",
            "are you going to delete them?",
            "what happens if you delete them?",
        ],
    )
    async def test_delete_question_stores_nothing_and_survives(
        self, live_service, monkeypatch, pref_store, todo_boundary, question
    ):
        """Contract axis (a): an interrogative turn is a state query, not a
        verb answer. RED pre-fix: 'delete' inside a question stored the
        default and armed the confirm. GREEN: nothing stored, the verb
        question survives (silent §5a re-arm via the generic READ branch),
        normal processing answers."""
        sid = f"e2e-1653-q-{abs(hash(question)) % 10000}"
        await _arm_verb_question(monkeypatch, live_service, sid)
        p_classify, p_floor = _stub_fallthrough_routing(live_service, question)
        with p_classify, p_floor:
            await live_service.process_intent(message=question, session_id=sid, user_id=_USER)
        assert _no_delete_default_stored(pref_store), question
        stored = _pending_offers(live_service).get(sid)
        assert stored is not None, (
            "#1739 §5a: a state question must re-arm the verb question, not "
            "abandon it via the off-intent pop"
        )
        assert stored["pending_action"]["kind"] == rc.CLEAR_VERB_QUESTION_KIND
        assert todo_boundary["deleted"] == [] and todo_boundary["completed"] == []

    async def test_survived_arm_still_binds_the_next_crisp_answer(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """The survived arm is a live ask: after the question turn, a crisp
        'delete them' stores the mapping and routes to the REAL confirm."""
        sid = "e2e-1653-q-then-answer"
        await _arm_verb_question(monkeypatch, live_service, sid)
        p_classify, p_floor = _stub_fallthrough_routing(live_service, "delete them?")
        with p_classify, p_floor:
            await live_service.process_intent(message="delete them?", session_id=sid, user_id=_USER)
        result = await live_service.process_intent(
            message="delete them", session_id=sid, user_id=_USER
        )
        assert result.message.startswith(variant_three_question(2))
        record = pref_store["verified_inferences"][rc.inference_key("clear")]
        assert record["value"] == rc.VALUE_DELETE
        stored = _pending_offers(live_service).get(sid)
        assert stored["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW
        assert todo_boundary["deleted"] == []  # still gated behind the yes


# ---------------------------------------------------------------------------
# 4. Crisp answers still bind (the anchored bar must not cost real answers)
# ---------------------------------------------------------------------------


class TestCrispAnswersStillBind:
    pytestmark = pytest.mark.asyncio

    @pytest.mark.parametrize(
        "answer",
        [
            "delete them",
            "yes, delete them",
            "no, delete them",
            "actually, delete them",
            "please delete them",
            "remove them",
            "get rid of them",
            "I want you to delete them",
        ],
    )
    async def test_crisp_delete_answers_store_and_route_to_confirm(
        self, live_service, monkeypatch, pref_store, todo_boundary, answer
    ):
        """The anchored claim (lead-ins tolerated, delete verb at the head)
        keeps every crisp answer shape working — including accept/decline
        lead-ins ('yes, delete them' / 'no, delete them'), which is why the
        claims run BEFORE generic accept/decline at this seam."""
        sid = f"e2e-1653-crisp-{abs(hash(answer)) % 10000}"
        await _arm_verb_question(monkeypatch, live_service, sid)
        result = await live_service.process_intent(message=answer, session_id=sid, user_id=_USER)
        assert result.message.startswith(variant_three_question(2)), answer
        record = pref_store["verified_inferences"][rc.inference_key("clear")]
        assert record["value"] == rc.VALUE_DELETE, answer
        stored = _pending_offers(live_service).get(sid)
        assert stored["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW
        assert todo_boundary["deleted"] == []  # explosive until confirmed

    async def test_mark_done_answer_still_completes(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        sid = "e2e-1653-done"
        await _arm_verb_question(monkeypatch, live_service, sid)
        todo_boundary["allow_complete"] = True
        result = await live_service.process_intent(
            message="mark them done", session_id=sid, user_id=_USER
        )
        record = pref_store["verified_inferences"][rc.inference_key("clear")]
        assert record["value"] == rc.VALUE_COMPLETE
        assert len(todo_boundary["completed"]) == 2
        assert "Marked 2 reminders done" in result.message

    async def test_negated_delete_never_stores(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        sid = "e2e-1653-negated"
        await _arm_verb_question(monkeypatch, live_service, sid)
        p_classify, p_floor = _stub_fallthrough_routing(live_service, "no, don't delete them")
        with p_classify, p_floor:
            await live_service.process_intent(
                message="no, don't delete them", session_id=sid, user_id=_USER
            )
        assert _no_delete_default_stored(pref_store)
        assert todo_boundary["deleted"] == []


# ---------------------------------------------------------------------------
# 5. The correction window gets the same axis-(a) gate
# ---------------------------------------------------------------------------


class TestCorrectionWindowQuestionGate:
    pytestmark = pytest.mark.asyncio

    async def test_delete_question_does_not_claim_the_correction_window(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """'delete them?' inside the one-turn correction window is a state
        query — RED pre-fix it matched the anchored claim (head-anchored
        'delete' + terminal '?') and armed the delete confirm off a
        question. GREEN: no confirm arms; the window survives silently."""
        sid = "e2e-1653-corr-q"
        _seed_verb_default(pref_store, rc.VALUE_COMPLETE)
        _stub_classification(monkeypatch, live_service, "clear my reminders", "complete_todo")
        todo_boundary["allow_complete"] = True
        await live_service.process_intent(
            message="clear my reminders", session_id=sid, user_id=_USER
        )
        stored = _pending_offers(live_service).get(sid)
        assert stored["pending_action"]["kind"] == rc.CLEAR_CORRECTION_KIND
        p_classify, p_floor = _stub_fallthrough_routing(live_service, "delete them?")
        with p_classify, p_floor:
            await live_service.process_intent(message="delete them?", session_id=sid, user_id=_USER)
        stored = _pending_offers(live_service).get(sid)
        assert stored is not None
        assert stored["workflow_type"] != CONFIRM_PENDING_ACTION_WORKFLOW, (
            "#1653: a question-shaped turn armed the delete confirm from the " "correction window"
        )
        assert stored["pending_action"]["kind"] == rc.CLEAR_CORRECTION_KIND
        assert todo_boundary["deleted"] == []
        # The stored default did not flip either.
        record = pref_store["verified_inferences"][rc.inference_key("clear")]
        assert record["value"] == rc.VALUE_COMPLETE


# ---------------------------------------------------------------------------
# 6. Residue 2, pinned as DELIBERATE: echo-answers at the armed delete
#    confirm never fire (PM-visible behavior note on the issue)
# ---------------------------------------------------------------------------


class TestEchoAnswerAtDeleteConfirmStaysSafe:
    pytestmark = pytest.mark.asyncio

    async def test_echo_answer_does_not_fire_the_armed_delete(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """'yes, delete them' against the armed V3 confirm is NOT crisp
        full-message affirmative vocabulary (NAMED_OBJECT bar), so nothing
        fires: the pop stands and normal processing answers. Deliberate
        (issue #1653 note 2): the safe direction. If live use shows verb
        echoes are common, verb-echo forms matching the ARMED action's verb
        may join the crisp set — evidence-gated, not this change."""
        sid = "e2e-1653-echo"
        await _arm_verb_question(monkeypatch, live_service, sid)
        await live_service.process_intent(message="delete them", session_id=sid, user_id=_USER)
        stored = _pending_offers(live_service).get(sid)
        assert stored["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW
        echo = "yes, delete them"
        p_classify, p_floor = _stub_fallthrough_routing(live_service, echo)
        with p_classify, p_floor:
            await live_service.process_intent(message=echo, session_id=sid, user_id=_USER)
        # The explosive boundary (allow_delete False) proves nothing fired;
        # the popped confirm cannot fire later either.
        assert todo_boundary["deleted"] == []
        stored = _pending_offers(live_service).get(sid)
        if stored is not None:
            assert stored["workflow_type"] != CONFIRM_PENDING_ACTION_WORKFLOW
