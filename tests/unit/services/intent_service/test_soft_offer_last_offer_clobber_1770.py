"""#1770 — a STATE_QUESTION-survived arm on the ``last_offer`` rail must not
be clobbered by a same-turn soft contextual offer: the #1753 defect shape at
the SECOND one-slot arm store.

The filed gap (found by the #1769 lane, stated as the in-branch honest
boundary at the resume seam's §5a survival): the cohort has TWO one-slot arm
rails — the #846 pending-offer store (guarded since #1753) and the
#852/#1529 one-turn ``ConversationContext.last_offer`` rail, where the #1769
resume-offer survival silently re-arms. Nothing guarded the second one. On a
survival turn there are two clobber vectors:

1. REPLACES — the canonical ``offer_hint`` write (#852 tracking, the rail's
   only other same-turn write site) overwrites the survived
   ``process_resume`` arm with a ``contextual`` one.
2. HIDES — ``_apply_soft_offer`` arms the #846 store with a soft workflow
   offer; next turn the #846 pop runs BEFORE the ``last_offer`` pop, so the
   soft offer steals the user's answer to the survived resume ask.

Mitigating floor (from the issue): the suspended process persists durably
and re-offers at the next greeting — the failure is a lost turn of arm
continuity, not a lost flow. It is still the exact failure the survival
ruling exists to prevent.

Fix under test: the #1753 guard in ``_apply_soft_offer`` now peeks BOTH
stores (one block, one skip log naming the store), and the ``offer_hint``
write is first-arm-wins. The soundness argument is the same for the rail as
for the store: ``process_intent`` always-clears ``last_offer`` at turn start
(the #852 one-turn invariant, before classification and before every
``_apply_soft_offer`` call site), so any non-None value at either guard site
was armed — or survival-re-armed — THIS turn. A stale prior-turn arm cannot
reach the guards; the no-over-block class pins that.

Layer honesty (m-43): the e2e classes drive the REAL
``IntentService.process_intent`` mocked only at the LLM boundary (explosive),
the process registry (suspended standup present; active check inert), and —
for the clobber halves — the soft-offer DETECTOR + throttle stubbed OPEN
(the #1652/#1753 idiom: what stands between them and the one-slot stores is
exactly the guard under test). The guard-unit and no-over-block classes pin
``_apply_soft_offer`` directly.
"""

from datetime import datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.conversation_context import get_or_create_context
from services.intent_service.soft_invocation import SoftInvocationResult, WorkflowOffer
from services.intent_service.workflow_entries import register_default_workflows
from services.process.registry import ProcessType, SuspendedInfo
from services.shared_types import IntentCategory

_USER = "5a2c9d10-1770-4b00-9e00-000000001770"  # valid UUID: survives principal parsing

RESUME_ASK = "Welcome back! Your standup was paused. Would you like to continue, or start fresh?"

# The clobberer is a DIFFERENT ask than the survived arm, so a replaced /
# hidden arm is unambiguous in the asserts.
_CLOBBER_ASK = "I could help you set up a project structure. Want that?"

_HINT_ASK = "Want more detail on either project?"


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM. Every turn in
    these tests must resolve deterministically."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1770 turns must resolve deterministically"
        )


@pytest.fixture
def live_service():
    register_default_workflows()
    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


def _open_soft_offer_conditions(service):
    """Make the soft-offer path WANT to fire (the #1652/#1753 idiom): the
    detector reports an offer on any message and the throttle gate is open.
    What stands between them and the one-slot stores is the guard under
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
    """Shut the gate for turns whose own behavior is under test — otherwise a
    follow-up turn's empty stores legitimately take a fresh offer and muddy
    the asserts."""
    service.workflow_offer_service.should_offer = MagicMock(return_value=(False, "gate-closed"))


def _stub_fallthrough_routing(service, message):
    """After a silent survival re-arm, normal processing answers the turn —
    its routing is not under test (the #1753 idiom): classification returns a
    low-confidence UNKNOWN and the floor door is patched. The patched floor
    result carries NO ``*_pending`` flag — the flag-less composition is the
    filed gap."""
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


def _registry_with_suspended_standup():
    """Patch the registry the resume seam consults: a suspended standup
    exists (so the seam reaches its verdict stage) and the active-process
    check is inert (no guided flow claims the turn)."""
    mock_registry = MagicMock()
    mock_registry.check_suspended_processes = AsyncMock(
        return_value=SuspendedInfo(
            process_type=ProcessType.STANDUP,
            suspended_at=datetime.now(),
            description="Your standup was paused.",
        )
    )
    mock_registry.check_active_processes = AsyncMock(
        return_value=SimpleNamespace(
            handled=False, escaped=False, response_message=None, process_type=None
        )
    )
    p = patch("services.intent.intent_service.get_process_registry")
    return p, mock_registry


def _arm_resume_rail(service, sid):
    """Arm the one-turn process-resume offer the way the arm sites do
    (#1529 greeting reentry / #1769 ``_arm_resume_offer``) — rendered ask on
    the record (#1665)."""
    service._arm_resume_offer(sid, _USER, question=RESUME_ASK)


def _rail(sid, user_id=_USER):
    return get_or_create_context(sid, user_id=user_id).last_offer


# ---------------------------------------------------------------------------
# 1. THE filed gap, HIDES vector: the survived resume arm outlives a turn on
#    which a soft offer fires (e2e, real process_intent)
# ---------------------------------------------------------------------------


class TestSurvivedResumeArmOutlivesSoftOffer:
    pytestmark = pytest.mark.asyncio

    async def test_soft_offer_does_not_hide_the_survived_resume_arm(self, live_service):
        """RED pre-fix: the state question re-arms the resume offer on the
        last_offer rail (§5a), normal processing composes a flag-less result,
        and the open soft-offer path arms the #846 store with project_setup —
        which the NEXT turn's pop consumes FIRST, stealing the user's answer
        to the survived resume ask."""
        sid = "e2e-1770-resume-survival"
        _arm_resume_rail(live_service, sid)
        _open_soft_offer_conditions(live_service)
        question = "what would that involve?"
        p_registry, mock_registry = _registry_with_suspended_standup()
        p_classify, p_floor = _stub_fallthrough_routing(live_service, question)
        with p_registry as registry_fn, p_classify, p_floor:
            registry_fn.return_value = mock_registry
            result = await live_service.process_intent(
                message=question, session_id=sid, user_id=_USER
            )
        assert _pending_offers(live_service).get(sid) is None, (
            "#1770: the soft offer armed the #846 store over a survived "
            "resume arm — next turn's pop would bind the user's answer to "
            "the clobberer, not the resume ask they were answering"
        )
        rail = _rail(sid)
        assert rail is not None, "#1770: the survived arm vanished from the rail"
        assert rail.offer_type == "process_resume"
        assert rail.offer_text == RESUME_ASK
        assert _CLOBBER_ASK not in (result.message or "")

    async def test_survived_arm_still_binds_the_next_continue(self, live_service):
        """The survived arm is a live ask across BOTH hazards: the question
        turn AND the soft-offer application. The next 'continue' resumes the
        SUSPENDED STANDUP, not the clobberer's workflow."""
        sid = "e2e-1770-resume-survival-continue"
        _arm_resume_rail(live_service, sid)
        _open_soft_offer_conditions(live_service)
        question = "what would that involve?"
        p_registry, mock_registry = _registry_with_suspended_standup()
        p_classify, p_floor = _stub_fallthrough_routing(live_service, question)
        with p_registry as registry_fn, p_classify, p_floor:
            registry_fn.return_value = mock_registry
            await live_service.process_intent(message=question, session_id=sid, user_id=_USER)
        _close_soft_offer_conditions(live_service)
        p_registry2, mock_registry2 = _registry_with_suspended_standup()
        with (
            p_registry2 as registry_fn2,
            patch.object(
                live_service,
                "_resume_suspended_standup",
                new=AsyncMock(
                    return_value=IntentProcessingResult(
                        success=True, message="Picking your standup back up.", intent_data={}
                    )
                ),
            ) as resume_mock,
        ):
            registry_fn2.return_value = mock_registry2
            result = await live_service.process_intent(
                message="continue", session_id=sid, user_id=_USER
            )
        resume_mock.assert_called_once()
        assert result.message == "Picking your standup back up."
        assert _CLOBBER_ASK not in (result.message or "")


# ---------------------------------------------------------------------------
# 2. THE filed gap, REPLACES vector: the canonical offer_hint write must not
#    overwrite the survived arm (first-arm-wins on the rail)
# ---------------------------------------------------------------------------


class TestCanonicalOfferHintDoesNotReplaceSurvivedArm:
    pytestmark = pytest.mark.asyncio

    async def test_offer_hint_write_skips_when_an_arm_survived_this_turn(self, live_service):
        """RED pre-fix: the survival turn's answer comes from a canonical
        handler that emits ``offer_hint`` — the #852 tracking write replaced
        the survived ``process_resume`` arm with a ``contextual`` one, so the
        next turn's 'continue' had nothing to bind to."""
        sid = "e2e-1770-hint-replace"
        _arm_resume_rail(live_service, sid)
        _close_soft_offer_conditions(live_service)  # isolate the REPLACES vector
        question = "which projects do I have?"
        canonical_result = {
            "message": "You have 2 projects: Alpha and Beta.",
            "intent": {
                "category": "portfolio",
                "action": "list_projects",
                "confidence": 0.95,
            },
            "offer_hint": {
                "continuation_hint": "tell me more about the projects",
                "offer_text": _HINT_ASK,
            },
        }
        from services.intent_service.pre_classifier import MultiIntentResult

        canonical_intent = Intent(
            category=IntentCategory.PORTFOLIO,
            action="list_projects",
            confidence=0.95,
            original_message=question,
            context={"original_message": question},
        )
        p_registry, mock_registry = _registry_with_suspended_standup()
        with (
            p_registry as registry_fn,
            patch.object(
                live_service.intent_classifier,
                "classify_multiple",
                new=AsyncMock(
                    return_value=MultiIntentResult(
                        intents=[canonical_intent], original_message=question
                    )
                ),
            ),
            patch.object(live_service, "_should_route_to_floor", return_value=False),
            patch.object(live_service.canonical_handlers, "can_handle", return_value=True),
            patch.object(
                live_service.canonical_handlers,
                "handle",
                new=AsyncMock(return_value=canonical_result),
            ),
            patch.object(live_service, "_is_generic_canonical_response", return_value=False),
        ):
            registry_fn.return_value = mock_registry
            await live_service.process_intent(message=question, session_id=sid, user_id=_USER)
        rail = _rail(sid)
        assert rail is not None
        assert rail.offer_type == "process_resume", (
            "#1770: the canonical offer_hint write REPLACED the "
            "STATE_QUESTION-survived resume arm on the one-turn rail — the "
            "question silently cost the user their pending ask"
        )
        assert rail.offer_text == RESUME_ASK

    async def test_offer_hint_still_tracks_on_a_free_turn(self, live_service):
        """No over-block at the write site: with the rail empty, the #852
        contextual tracking write proceeds unchanged."""
        sid = "e2e-1770-hint-free"
        _close_soft_offer_conditions(live_service)
        question = "which projects do I have?"
        canonical_result = {
            "message": "You have 2 projects: Alpha and Beta.",
            "intent": {
                "category": "portfolio",
                "action": "list_projects",
                "confidence": 0.95,
            },
            "offer_hint": {
                "continuation_hint": "tell me more about the projects",
                "offer_text": _HINT_ASK,
            },
        }
        from services.intent_service.pre_classifier import MultiIntentResult

        canonical_intent = Intent(
            category=IntentCategory.PORTFOLIO,
            action="list_projects",
            confidence=0.95,
            original_message=question,
            context={"original_message": question},
        )
        with (
            patch.object(
                live_service.intent_classifier,
                "classify_multiple",
                new=AsyncMock(
                    return_value=MultiIntentResult(
                        intents=[canonical_intent], original_message=question
                    )
                ),
            ),
            patch.object(live_service, "_should_route_to_floor", return_value=False),
            patch.object(live_service.canonical_handlers, "can_handle", return_value=True),
            patch.object(
                live_service.canonical_handlers,
                "handle",
                new=AsyncMock(return_value=canonical_result),
            ),
            patch.object(live_service, "_is_generic_canonical_response", return_value=False),
        ):
            await live_service.process_intent(message=question, session_id=sid, user_id=_USER)
        rail = _rail(sid)
        assert rail is not None, "#852 tracking must still work on free turns"
        assert rail.offer_type == "contextual"
        assert rail.continuation_hint == "tell me more about the projects"


# ---------------------------------------------------------------------------
# 3. Guard unit pin — the RAIL, like the store, short-circuits the apply seam
# ---------------------------------------------------------------------------


class TestRailGuardAtTheApplySeam:
    def test_live_rail_arm_short_circuits_before_detection(self, live_service):
        """A live arm on the last_offer rail with a FLAG-LESS result and an
        EMPTY #846 store (the #1769 survival-turn composition) short-circuits
        ``_apply_soft_offer`` BEFORE detection — message unmodified, both
        stores untouched."""
        sid = "unit-1770-rail-guard"
        _arm_resume_rail(live_service, sid)
        _open_soft_offer_conditions(live_service)
        result = IntentProcessingResult(
            success=True,
            message="the answer to the state question",
            intent_data={"category": "unknown", "action": "unknown"},  # no *_pending flag
        )
        out = live_service._apply_soft_offer(result, "what would that involve?", sid, user_id=_USER)
        assert out.message == "the answer to the state question"
        assert _pending_offers(live_service).get(sid) is None
        rail = _rail(sid)
        assert rail is not None
        assert rail.offer_type == "process_resume"
        live_service.soft_invocation_detector.detect.assert_not_called()

    def test_store_guard_still_holds_no_1753_regression(self, live_service):
        """The #1753 half of the guard remains: a live #846 entry with an
        empty rail still short-circuits before detection."""
        sid = "unit-1770-store-guard"
        live_service.workflow_offer_service.set_pending_offer(
            sid,
            {"workflow_type": "meeting", "question": "Want me to find a time?"},
        )
        _open_soft_offer_conditions(live_service)
        result = IntentProcessingResult(
            success=True,
            message="the answer",
            intent_data={"category": "unknown", "action": "unknown"},
        )
        out = live_service._apply_soft_offer(result, "any message", sid)
        assert out.message == "the answer"
        assert _pending_offers(live_service)[sid]["workflow_type"] == "meeting"
        live_service.soft_invocation_detector.detect.assert_not_called()


# ---------------------------------------------------------------------------
# 4. No over-block — a genuinely expired or absent rail arm never suppresses
#    offers (the staleness-soundness pin)
# ---------------------------------------------------------------------------


class TestNoOverBlock:
    pytestmark = pytest.mark.asyncio

    async def test_expired_prior_turn_arm_does_not_suppress_offers(self, live_service):
        """The soundness pin: a prior-turn resume arm that this turn's PASS
        message lets EXPIRE (the #852 one-turn invariant — popped at turn
        start, not re-armed) must NOT block the soft offer. The guard reads
        post-pop state, so an expired arm is invisible to it."""
        sid = "e2e-1770-expired-arm"
        _arm_resume_rail(live_service, sid)
        _open_soft_offer_conditions(live_service)
        message = "tell me about the roadmap"  # PASS at the seam: not an accept/decline/question
        p_registry, mock_registry = _registry_with_suspended_standup()
        p_classify, p_floor = _stub_fallthrough_routing(live_service, message)
        with p_registry as registry_fn, p_classify, p_floor:
            registry_fn.return_value = mock_registry
            result = await live_service.process_intent(
                message=message, session_id=sid, user_id=_USER
            )
        assert _rail(sid) is None, "a PASS turn expires the one-turn arm (#852)"
        assert _CLOBBER_ASK in (result.message or ""), (
            "#1770 over-block: an EXPIRED prior-turn arm suppressed the soft "
            "offer — the guard must only see arms live THIS turn"
        )
        stored = _pending_offers(live_service).get(sid)
        assert stored is not None
        assert stored["workflow_type"] == "project_setup"

    async def test_absent_rail_and_empty_store_applies_the_offer(self, live_service):
        """Free turn, both stores empty: the offer applies (the #1753
        free-turn pin, re-run through the two-store guard)."""
        sid = "unit-1770-free-turn"
        _open_soft_offer_conditions(live_service)
        result = IntentProcessingResult(
            success=True,
            message="here's your answer",
            intent_data={"category": "unknown", "action": "unknown"},
        )
        out = live_service._apply_soft_offer(result, "set up the project", sid, user_id=_USER)
        assert _CLOBBER_ASK in out.message
        stored = _pending_offers(live_service).get(sid)
        assert stored is not None
        assert stored["workflow_type"] == "project_setup"
