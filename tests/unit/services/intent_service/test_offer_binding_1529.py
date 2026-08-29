"""
Issue #1529 OFFER-BINDING: "Yes please" must bind to the offer that was
actually made — never to a dormant flow-starter.

PM's 2026-08-08 T6 transcript, verbatim: Piper offered "Would you like me to
list your archived projects?" (a #852 contextual offer). PM answered "Yes
please". The standup interview started.

Mechanism (diagnosed): #1394 fixed the last_offer split-brain, so the
contextual offer IS now found and bound — but `_check_pending_resume_offer`
(#889) ran on every turn where ANY suspended standup existed in the durable
repo and claimed bare affirmatives ("yes please" is in its accept set)
WITHOUT ever checking that a resume offer had been made. It returned before
classification could consume the bound hint. Post-1394 the hijack therefore
persisted: these tests pin the ordering fix.

Contract:
- An affirmative that just bound to a contextual offer is NOT available to
  the resume check (a pending offer wins over any flow-starter).
- Bare affirmatives resume a suspended flow ONLY when the resume offer was
  made on the previous turn (recorded as last_offer offer_type
  "process_resume" by the greeting reentry check).
- Explicit "resume"/"continue" commands work at any time.
- "end standup" against a suspended standup abandons it deterministically —
  no classifier involved (#1529 part 3).
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.conversation_context import (
    LastOffer,
    get_or_create_context,
)
from services.intent_service.orchestrator import IntentOrchestrator
from services.intent_service.pre_classifier import MultiIntentResult
from services.process.registry import ProcessType, SuspendedInfo
from services.shared_types import IntentCategory

# PM's verbatim transcript lines (2026-08-08 T6)
PM_YES_PLEASE = "Yes please"
PM_END_STANDUP = "end standup"

ARCHIVED_OFFER_HINT = "list archived projects"


def _make_multi_result(action: str = "test") -> MultiIntentResult:
    intent = Intent(category=IntentCategory.CONVERSATION, action=action, confidence=1.0)
    return MultiIntentResult(intents=[intent], original_message="test", is_multi_intent=False)


def _suspended_standup() -> SuspendedInfo:
    return SuspendedInfo(
        process_type=ProcessType.STANDUP,
        suspended_at=datetime.now(timezone.utc),
        description="Your standup was paused. Want to pick it up?",
    )


@pytest.fixture
def mock_classifier():
    classifier = MagicMock()
    classifier.classify_multiple = AsyncMock(return_value=_make_multi_result())
    classifier.classify = AsyncMock()
    return classifier


@pytest.fixture
def mock_canonical_handlers():
    handlers = MagicMock()
    handlers.can_handle = MagicMock(return_value=True)
    handlers.handle = AsyncMock(
        return_value={
            "message": "Here are your archived projects: CoVa.",
            "intent": {"category": "conversation", "action": "test"},
            "requires_clarification": False,
        }
    )
    return handlers


@pytest.fixture
def service(mock_classifier, mock_canonical_handlers):
    svc = IntentService(intent_classifier=mock_classifier)
    svc.canonical_handlers = mock_canonical_handlers
    svc.intent_orchestrator = IntentOrchestrator(canonical_handlers=mock_canonical_handlers)
    return svc


def _patched_pipeline(service, suspended=None):
    """Patch the flow seams around the offer-binding pipeline segment:
    - no ACTIVE guided process (the hijack was a SUSPENDED one),
    - the process registry reports `suspended`,
    - resume/abandon are sentinel AsyncMocks so a claim is observable.
    """
    mock_registry = MagicMock()
    mock_registry.check_suspended_processes = AsyncMock(return_value=suspended)

    resume_sentinel = IntentProcessingResult(
        success=True, message="RESUMED", intent_data={"action": "standup_conversation_resumed"}
    )
    abandon_sentinel = IntentProcessingResult(
        success=True, message="ABANDONED", intent_data={"action": "suspended_session_declined"}
    )

    return (
        patch.object(
            service, "_check_active_guided_process", new=AsyncMock(return_value=(None, None))
        ),
        patch("services.intent.intent_service.get_process_registry", return_value=mock_registry),
        patch.object(
            service,
            "_resume_suspended_standup",
            new=AsyncMock(return_value=resume_sentinel),
        ),
        patch.object(
            service,
            "_abandon_suspended_standup",
            new=AsyncMock(return_value=abandon_sentinel),
        ),
    )


class TestYesPleaseBindsToPendingOffer:
    """The verbatim hijack turn, replayed."""

    @pytest.mark.asyncio
    async def test_yes_please_after_archived_offer_does_not_resume_standup(self, service):
        """PM verbatim: contextual offer pending + suspended standup in repo.
        'Yes please' must bind to the offer — the standup may NOT claim it."""
        session_id = str(uuid4())
        user_id = str(uuid4())

        # The previous turn's offer (written by the canonical seam, #852/#1394)
        ctx = get_or_create_context(session_id, user_id=user_id)
        ctx.last_offer = LastOffer(
            offer_type="contextual",
            continuation_hint=ARCHIVED_OFFER_HINT,
            offer_text="Would you like me to list your archived projects?",
        )

        p1, p2, p3, p4 = _patched_pipeline(service, suspended=_suspended_standup())
        with p1, p2, p3 as mock_resume, p4:
            result = await service._process_intent_internal(
                message=PM_YES_PLEASE, session_id=session_id, user_id=user_id
            )

        # The flow-starter did NOT claim the affirmative
        mock_resume.assert_not_called()
        assert (result.intent_data or {}).get("action") != "standup_conversation_resumed"

        # The affirmative reached classification WITH the bound offer hint
        service.intent_classifier.classify_multiple.assert_called_once()
        _, kwargs = service.intent_classifier.classify_multiple.call_args
        assert kwargs.get("context", {}).get("contextual_continuation_hint") == ARCHIVED_OFFER_HINT

    @pytest.mark.asyncio
    async def test_bare_yes_with_no_pending_offer_does_not_resume(self, service):
        """No offer of any kind was made; a suspended standup exists.
        Bare 'yes please' binds to nothing — it must NOT resume the flow."""
        session_id = str(uuid4())
        user_id = str(uuid4())

        p1, p2, p3, p4 = _patched_pipeline(service, suspended=_suspended_standup())
        with p1, p2, p3 as mock_resume, p4:
            result = await service._process_intent_internal(
                message=PM_YES_PLEASE, session_id=session_id, user_id=user_id
            )

        mock_resume.assert_not_called()
        assert (result.intent_data or {}).get("action") != "standup_conversation_resumed"
        service.intent_classifier.classify_multiple.assert_called_once()


class TestResumeOfferStillWorksWhenActuallyMade:
    """The legitimate #889 path survives, now correctly bound."""

    @pytest.mark.asyncio
    async def test_yes_after_real_resume_offer_resumes(self, service):
        """Greeting reentry made the offer last turn (recorded as
        process_resume last_offer) → bare 'yes' resumes."""
        session_id = str(uuid4())
        user_id = str(uuid4())

        ctx = get_or_create_context(session_id, user_id=user_id)
        ctx.last_offer = LastOffer(
            offer_type="process_resume",
            continuation_hint="resume standup",
            offer_text="Welcome back! Your standup was paused.",
        )

        p1, p2, p3, p4 = _patched_pipeline(service, suspended=_suspended_standup())
        with p1, p2, p3 as mock_resume, p4:
            result = await service._process_intent_internal(
                message="yes", session_id=session_id, user_id=user_id
            )

        mock_resume.assert_called_once()
        assert result.message == "RESUMED"
        service.intent_classifier.classify_multiple.assert_not_called()

    @pytest.mark.asyncio
    async def test_explicit_resume_works_without_pending_offer(self, service):
        """'resume' names the flow unambiguously — honored anytime."""
        session_id = str(uuid4())
        user_id = str(uuid4())

        p1, p2, p3, p4 = _patched_pipeline(service, suspended=_suspended_standup())
        with p1, p2, p3 as mock_resume, p4:
            result = await service._process_intent_internal(
                message="resume", session_id=session_id, user_id=user_id
            )

        mock_resume.assert_called_once()
        assert result.message == "RESUMED"

    @pytest.mark.asyncio
    async def test_no_after_real_resume_offer_abandons(self, service):
        session_id = str(uuid4())
        user_id = str(uuid4())

        ctx = get_or_create_context(session_id, user_id=user_id)
        ctx.last_offer = LastOffer(
            offer_type="process_resume",
            continuation_hint="resume standup",
        )

        p1, p2, p3, p4 = _patched_pipeline(service, suspended=_suspended_standup())
        with p1, p2, p3, p4 as mock_abandon:
            result = await service._process_intent_internal(
                message="no", session_id=session_id, user_id=user_id
            )

        mock_abandon.assert_called_once()
        assert result.message == "ABANDONED"


class TestEndStandupAgainstSuspendedFlow:
    """#1529 part 3: 'end standup' is consumed deterministically — never
    reaches a classifier to be misrouted (the todo-complete misroute)."""

    @pytest.mark.asyncio
    async def test_end_standup_abandons_suspended_flow_without_classification(self, service):
        session_id = str(uuid4())
        user_id = str(uuid4())

        p1, p2, p3, p4 = _patched_pipeline(service, suspended=_suspended_standup())
        with p1, p2, p3 as mock_resume, p4 as mock_abandon:
            result = await service._process_intent_internal(
                message=PM_END_STANDUP, session_id=session_id, user_id=user_id
            )

        mock_abandon.assert_called_once()
        mock_resume.assert_not_called()
        assert result.message == "ABANDONED"
        service.intent_classifier.classify_multiple.assert_not_called()


class TestGreetingReentryRecordsOffer:
    """The reentry check writes the one-turn process_resume offer record."""

    @pytest.mark.asyncio
    async def test_reentry_offer_recorded_as_last_offer(self):
        from services.conversation.conversation_handler import ConversationHandler

        session_id = str(uuid4())
        user_id = str(uuid4())

        mock_registry = MagicMock()
        mock_registry.check_suspended_processes = AsyncMock(return_value=_suspended_standup())

        handler = ConversationHandler()
        with patch("services.process.registry.get_process_registry", return_value=mock_registry):
            offer = await handler._check_suspended_session_reentry(user_id, session_id=session_id)

        assert offer is not None
        assert offer["intent"]["action"] == "suspended_session_reentry"

        ctx = get_or_create_context(session_id, user_id=user_id)
        assert ctx.last_offer is not None
        assert ctx.last_offer.offer_type == "process_resume"
        assert ctx.last_offer.continuation_hint == "resume standup"
