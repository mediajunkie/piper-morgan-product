"""#1652 — offer-flag gap: the #1591 invitation + mode read-back arm the
one-slot #846 store with no ``*_pending`` intent_data flag.

Found during #1651 (2026-08-18): on the rail-dispatched ``get_standup`` path
the handler's result funnels through ``_apply_soft_offer``, whose no-clobber
guard is flag-keyed — #1651's new bound todo offer carries
``standup_todo_offer_pending``, but the two OLDER #1591 arms (the interview
invitation — both its after-report and empty-lead sites — and the
low-confidence mode read-back) carry nothing, so a soft workflow offer can
overwrite the just-armed ask in the same one-slot store.

Fix under test, both halves:

1. **Arm side (the filed gap)**: the three arm sites stamp
   ``standup_interview_invitation_pending`` / ``verify_inference_read_back_pending``
   onto the result's intent_data, and ``_apply_soft_offer`` lists both flags.
2. **Consume side (#1739 acceptance-contract adoption, epic 3)**: the
   ``verify_inference`` and ``standup_interview`` kinds consult THE predicate
   (``acceptance.evaluate_acceptance``) at their REGISTRY-DECLARED axes
   (WRITE×PRIVATE → LOW_CEREMONY) with the arm-site's stored ask threaded
   (#1665). Arm survival is the LOW-tier SILENT form (contract doc §5a,
   docs/internal/design/acceptance-contract-user-facing-2026-09-10.md):
   a state question re-arms the offer and normal processing answers — the
   legacy detector's off-intent pop no longer silently costs the user the
   pending ask.

Layer honesty (m-43): the end-to-end classes drive the REAL
``IntentService.process_intent`` mocked ONLY at the LLM boundary (explosive;
the rail turns stub ``classify_multiple`` with a QUERY-category
``get_standup`` emission — the exact rail-dispatched shape the issue names),
the standup assembler boundary, the todo SERVICE boundary (empty in-memory
double: no overdue todo, so the #1651 offer never outranks the #1591 asks),
and the users.preferences seam (in-memory double, the #1510 idiom). The
soft-offer clobber is simulated by stubbing the DETECTOR and the throttle
gate open — the guard under test sits between them and the store.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service import standup_preferences as sp
from services.intent_service import verified_inference as vi
from services.intent_service.acceptance import (
    AcceptanceTier,
    acceptance_tier,
    declared_axes_for_workflow,
)
from services.intent_service.classifier import IntentClassifier
from services.intent_service.soft_invocation import SoftInvocationResult, WorkflowOffer
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import EffectClass, IntentCategory, Outwardness

_USER = "3f7b8a52-1652-4b00-9e00-000000001652"
PROSE = "Here's your derived standup."

# A message with NO deterministic claim anywhere in the chain (no "standup"
# token, no imperative verb head) — the classification stub below is the only
# thing that can route it, which is exactly the rail-dispatched shape.
RAIL_MESSAGE = "how did today go for me"


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM. Every turn in
    these tests must resolve deterministically (the stubbed classification,
    the standup claim, or the pending-offer seam)."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1652 turns must resolve deterministically"
        )


@pytest.fixture(autouse=True)
def _clean_transient_state():
    sp._MODE_CHOICES.clear()
    vi._SESSION_DECLINES.clear()
    yield
    sp._MODE_CHOICES.clear()
    vi._SESSION_DECLINES.clear()


@pytest.fixture
def mem_prefs(monkeypatch):
    """In-memory users.preferences double at the ONE persistence seam (the
    #1510 idiom) — get_meta_mode / get_verified_inference / the read-back
    acceptance store all resolve here."""
    store: dict = {_USER: {}}

    async def _load(user_id):
        return dict(store.get(str(user_id), {}))

    async def _save(user_id, key, value):
        if str(user_id) not in store:
            return False
        store[str(user_id)][key] = value
        return True

    from services.intent_service import collaboration_gate

    monkeypatch.setattr(collaboration_gate, "_load_preferences", _load)
    monkeypatch.setattr(collaboration_gate, "_save_preference", _save)
    return store


class _EmptyTodoService:
    """No overdue todos → the #1651 bound offer never arms, so the #1591 mode
    asks are what the turn arms (the seams under test)."""

    async def list_todos(self, user_id, include_completed=False, **kwargs):
        return []


@pytest.fixture
def service(mem_prefs):
    register_default_workflows()
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            clf = IntentClassifier(llm_service=_ExplosiveLLM())
            svc = IntentService(intent_classifier=clf)
    svc.todo_handlers.todo_service = _EmptyTodoService()
    return svc


def _pending(service, sid):
    return service.workflow_offer_service._pending_offers.get(sid)


def _summary(empty: bool = False):
    summary = MagicMock()
    summary.is_empty.return_value = empty
    summary.to_prose.return_value = PROSE
    summary.to_dict.return_value = {"sections": []}
    return summary


def _stub_rail_classification(monkeypatch, service, message):
    """The rail-dispatched shape the issue names: the classifier emits
    ``get_standup`` under a QUERY category (not floor-routed, not canonical
    → the #1124 rail check dispatches it and the result funnels through
    ``_apply_soft_offer`` — the seam under test)."""
    intent = Intent(
        category=IntentCategory.QUERY,
        action="get_standup",
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


def _open_soft_offer_conditions(service):
    """Make the soft-offer path WANT to clobber: the detector reports an
    offer and the throttle gate is open. What stands between them and the
    one-slot store is exactly the ``_pending_flags`` guard under test."""
    service.soft_invocation_detector.detect = MagicMock(
        return_value=SoftInvocationResult(
            has_offer=True,
            offer=WorkflowOffer(
                workflow_type="meeting",
                offer_message="I could help set up a meeting. Want me to find a time?",
                decline_message="No worries.",
                confidence=0.9,
            ),
        )
    )
    service.workflow_offer_service.should_offer = MagicMock(return_value=(True, "gate-open"))


async def _rail_standup_turn(monkeypatch, service, sid, message=RAIL_MESSAGE, empty=False):
    _stub_rail_classification(monkeypatch, service, message)
    with patch(
        "services.standup.assembler.build_user_standup_summary",
        new=AsyncMock(return_value=_summary(empty=empty)),
    ):
        return await service.process_intent(message=message, session_id=sid, user_id=_USER)


async def _claimed_standup_turn(service, sid, message="give me my standup"):
    """The deterministic ``_is_standup_query`` claim path — used for arming
    when the consume side (not the funnel) is under test."""
    with patch(
        "services.standup.assembler.build_user_standup_summary",
        new=AsyncMock(return_value=_summary()),
    ):
        return await service.process_intent(message=message, session_id=sid, user_id=_USER)


def _stub_fallthrough_routing(service, message):
    """After a state question re-arms silently, normal processing answers the
    turn — its routing is not under test. The #1651 idiom: classification
    returns a low-confidence UNKNOWN fallback and the floor door is patched."""
    fallback = Intent(
        category=IntentCategory.UNKNOWN,
        action="unknown",
        confidence=0.2,
        original_message=message,
        context={"original_message": message},
    )
    from services.intent_service.pre_classifier import MultiIntentResult

    return patch.object(
        service.intent_classifier,
        "classify_multiple",
        new=AsyncMock(return_value=MultiIntentResult(intents=[fallback], original_message=message)),
    ), patch.object(
        service,
        "_handle_unknown_intent",
        new=AsyncMock(return_value=MagicMock(success=True, message="ok", intent_data={})),
    )


# ---------------------------------------------------------------------------
# 1. The filed gap — the rail funnel must not clobber the #1591 arms
# ---------------------------------------------------------------------------


class TestArmFlagsSurviveTheSoftOfferFunnel:
    pytestmark = pytest.mark.asyncio

    async def test_invitation_arm_carries_flag_and_survives_the_funnel(self, service, monkeypatch):
        """The after-report invitation arm: rail-dispatched get_standup, first
        report, no signal → the invitation arms; the soft-offer path wants the
        slot; the flag must keep the invitation in the store."""
        sid = "e2e-1652-invite"
        _open_soft_offer_conditions(service)
        result = await _rail_standup_turn(monkeypatch, service, sid)
        assert result.message.startswith(f"Good morning! {PROSE}")
        assert sp.INVITE_AFTER_REPORT in result.message
        assert result.intent_data.get("standup_interview_invitation_pending") is True
        stored = _pending(service, sid)
        assert stored is not None, (
            "#1652: the soft-offer funnel clobbered (or dropped) the just-armed "
            "#1591 invitation in the one-slot store"
        )
        assert stored["workflow_type"] == sp.STANDUP_INTERVIEW_WORKFLOW
        assert stored["pending_action"]["kind"] == sp.INVITE_KIND
        # #1665: the rendered ask rides the record (the input-adequacy half
        # the consume-side adoption depends on).
        assert stored["question"] == sp.INVITE_AFTER_REPORT

    async def test_read_back_arm_carries_flag_and_survives_the_funnel(self, service, monkeypatch):
        """The mode read-back arm: a repeated report choice → the rail's
        low-confidence read-back arms; same funnel, same guard."""
        sp.record_mode_choice(_USER, sp.MODE_REPORT)
        sp.record_mode_choice(_USER, sp.MODE_REPORT)
        sid = "e2e-1652-readback"
        _open_soft_offer_conditions(service)
        result = await _rail_standup_turn(monkeypatch, service, sid)
        assert "Did I get that right?" in result.message
        assert result.intent_data.get("verify_inference_read_back_pending") is True
        stored = _pending(service, sid)
        assert stored is not None, (
            "#1652: the soft-offer funnel clobbered (or dropped) the just-armed "
            "#1591 mode read-back in the one-slot store"
        )
        assert stored["workflow_type"] == vi.VERIFY_INFERENCE_WORKFLOW
        assert stored["pending_action"]["kind"] == vi.VERIFY_INFERENCE_KIND
        assert stored["pending_action"]["inference_key"] == sp.STANDUP_MODE_KEY

    async def test_empty_lead_invitation_carries_flag_and_survives(self, service, monkeypatch):
        """The THIRD arm site (found while fixing the filed two): PPM's
        empty-lead invitation arms in the empty branch — same funnel on the
        rail path, same missing flag before #1652."""
        sid = "e2e-1652-empty"
        _open_soft_offer_conditions(service)
        result = await _rail_standup_turn(monkeypatch, service, sid, empty=True)
        assert result.message == sp.INVITE_EMPTY_LEAD
        assert result.intent_data.get("standup_interview_invitation_pending") is True
        stored = _pending(service, sid)
        assert stored is not None
        assert stored["workflow_type"] == sp.STANDUP_INTERVIEW_WORKFLOW
        assert stored["question"] == sp.INVITE_EMPTY_LEAD

    async def test_guard_holds_per_flag_at_the_apply_seam(self, service):
        """Unit pin on the ``_pending_flags`` guard itself: each new flag
        short-circuits ``_apply_soft_offer`` BEFORE detection — message
        unmodified, nothing stored."""
        _open_soft_offer_conditions(service)
        for flag in (
            "standup_interview_invitation_pending",
            "verify_inference_read_back_pending",
        ):
            result = IntentProcessingResult(
                success=True,
                message="report text",
                intent_data={"category": "status", "action": "get_standup", flag: True},
            )
            out = service._apply_soft_offer(result, "any message", f"sid-guard-{flag}")
            assert out.message == "report text", flag
            assert _pending(service, f"sid-guard-{flag}") is None, flag
            service.soft_invocation_detector.detect.assert_not_called()


# ---------------------------------------------------------------------------
# 2. #1739 adoption at the two seams — verdicts at the declared axes
# ---------------------------------------------------------------------------


class TestAcceptanceContractAdoption:
    pytestmark = pytest.mark.asyncio

    def test_declared_axes_derive_the_low_ceremony_tier(self):
        """The adoption's axis mapping, pinned: both workflows are registered
        WRITE×PRIVATE (#1557 — looked up, never inferred from names), and
        WRITE×PRIVATE derives LOW_CEREMONY (contract axis (d): only
        DESTRUCTIVE and OUTWARD WRITEs take the NAMED_OBJECT bar)."""
        register_default_workflows()
        for wf in (vi.VERIFY_INFERENCE_WORKFLOW, sp.STANDUP_INTERVIEW_WORKFLOW):
            axes = declared_axes_for_workflow(wf)
            assert axes == (EffectClass.WRITE, Outwardness.PRIVATE), wf
            assert acceptance_tier(*axes) == AcceptanceTier.LOW_CEREMONY, wf

    async def test_state_question_survives_the_invitation_arm(self, service):
        """PM's #1617 shape against the INVITATION: "are we done with that
        standup?" is a state query, not a failed acceptance — the arm
        survives SILENTLY (LOW tier, §5a) and normal processing answers.
        Pre-#1652 the legacy detector returned None and the pop abandoned
        the invitation."""
        sid = "e2e-1652-state-q-invite"
        service._start_standup_conversation = AsyncMock()
        await _claimed_standup_turn(service, sid)
        assert _pending(service, sid) is not None
        question = "are we done with that standup?"
        p_classify, p_floor = _stub_fallthrough_routing(service, question)
        with p_classify, p_floor:
            await service.process_intent(message=question, session_id=sid, user_id=_USER)
        # Nothing fired, nothing declined, and the arm SURVIVED the question.
        service._start_standup_conversation.assert_not_called()
        stored = _pending(service, sid)
        assert stored is not None, (
            "#1739 adoption: a state question must re-arm the invitation, not "
            "abandon it via the off-intent pop"
        )
        assert stored["workflow_type"] == sp.STANDUP_INTERVIEW_WORKFLOW
        assert vi.was_declined(sid, sp.INVITE_DECLINE_KEY) is False

    async def test_state_question_then_yes_starts_the_interview(self, service):
        """The survived arm is still a live ask: the next "yes" binds to it
        and starts the EXISTING interview (one interview, three doors)."""
        sid = "e2e-1652-state-q-yes"
        sentinel = IntentProcessingResult(
            success=True,
            message="interview started",
            intent_data={"category": "execution", "action": "standup_started"},
        )
        service._start_standup_conversation = AsyncMock(return_value=sentinel)
        await _claimed_standup_turn(service, sid)
        question = "are we done with that standup?"
        p_classify, p_floor = _stub_fallthrough_routing(service, question)
        with p_classify, p_floor:
            await service.process_intent(message=question, session_id=sid, user_id=_USER)
        result = await service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert result.message == "interview started"
        service._start_standup_conversation.assert_awaited_once_with(_USER, sid)
        assert _pending(service, sid) is None  # consumed

    async def test_state_question_survives_the_read_back_then_yes_stores(self, service, mem_prefs):
        """Same contract at the read-back seam: a question about state
        neither accepts (no store write) nor drops the arm; the follow-up
        "yes" then stores source=user_verified through the same workflow."""
        sp.record_mode_choice(_USER, sp.MODE_REPORT)
        sp.record_mode_choice(_USER, sp.MODE_REPORT)
        sid = "e2e-1652-state-q-rb"
        await _claimed_standup_turn(service, sid)
        stored = _pending(service, sid)
        assert stored is not None
        assert stored["workflow_type"] == vi.VERIFY_INFERENCE_WORKFLOW
        question = "did you save that preference already?"
        p_classify, p_floor = _stub_fallthrough_routing(service, question)
        with p_classify, p_floor:
            await service.process_intent(message=question, session_id=sid, user_id=_USER)
        # The question turn stored NOTHING (it was not read as an accept)…
        assert vi.VERIFIED_INFERENCES_PREF_KEY not in mem_prefs[_USER]
        # …and the arm survived.
        survived = _pending(service, sid)
        assert survived is not None
        assert survived["workflow_type"] == vi.VERIFY_INFERENCE_WORKFLOW
        # The follow-up "yes" binds to the survived ask and stores.
        result = await service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert result.intent_data["verified"] is True
        record = mem_prefs[_USER][vi.VERIFIED_INFERENCES_PREF_KEY][sp.STANDUP_MODE_KEY]
        assert record["value"] == sp.MODE_REPORT
        assert record["source"] == vi.SOURCE_USER_VERIFIED

    async def test_decline_still_declines_through_the_predicate(self, service, mem_prefs):
        """DECLINE verdict parity: "no thanks" after a survived state question
        still cancels honestly with the offer's own decline copy and the
        session anti-nag memo — the adoption changed the judge, not the
        decline semantics."""
        sid = "e2e-1652-decline"
        service._start_standup_conversation = AsyncMock()
        await _claimed_standup_turn(service, sid)
        question = "are we done with that standup?"
        p_classify, p_floor = _stub_fallthrough_routing(service, question)
        with p_classify, p_floor:
            await service.process_intent(message=question, session_id=sid, user_id=_USER)
        result = await service.process_intent(message="no thanks", session_id=sid, user_id=_USER)
        assert result.message == sp.INVITE_DECLINE_MESSAGE
        service._start_standup_conversation.assert_not_called()
        assert vi.was_declined(sid, sp.INVITE_DECLINE_KEY) is True
        assert mem_prefs[_USER] == {}

    async def test_prose_reply_neither_accepts_nor_survives_1631(self, service):
        """PASS parity with the legacy seam: a long prose turn is an aside —
        it neither accepts nor steals, and the pop's off-intent abandonment
        stands (LOW-tier survival is for STATE QUESTIONS, not for every
        non-answer)."""
        sid = "e2e-1652-prose"
        service._start_standup_conversation = AsyncMock()
        await _claimed_standup_turn(service, sid)
        prose = (
            "Yes and no — the mornings have been a mixed bag lately, and "
            "before we make the interview a habit I want to see how the team "
            "run-through lands this week, so let me get back to you on the "
            "guided version once things settle down a bit."
        )
        assert len(prose) >= 160
        p_classify, p_floor = _stub_fallthrough_routing(service, prose)
        with p_classify, p_floor:
            await service.process_intent(message=prose, session_id=sid, user_id=_USER)
        service._start_standup_conversation.assert_not_called()
        assert _pending(service, sid) is None  # popped, gone — off-intent
        assert vi.was_declined(sid, sp.INVITE_DECLINE_KEY) is False
