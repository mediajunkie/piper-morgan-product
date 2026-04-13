"""
Tests for contextual offer continuation tracking (#852).

When Piper makes a contextual offer ("Would you like me to explain more?")
and the user responds with a bare affirmative ("yes"), the classifier
should receive a continuation hint so it can interpret "yes" correctly.

Bright-line rule (Chief Architect): action_required → WorkflowOfferService.
Contextual offers → ConversationContext.last_offer → classifier hint.

Tests verify:
- LastOffer is stored when canonical handler returns offer_hint
- LastOffer is cleared on next turn (one-turn memory)
- Bare affirmative + last_offer → continuation hint passed to classifier
- Non-affirmative + last_offer → cleared, no hint
- No last_offer + "yes" → normal classification (no regression)
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.conversation_context import (
    ConversationContext,
    LastOffer,
    get_or_create_context,
)
from services.intent_service.orchestrator import IntentOrchestrator
from services.intent_service.pre_classifier import MultiIntentResult
from services.shared_types import IntentCategory


def _make_multi_result(action: str = "test") -> MultiIntentResult:
    """Create a single-intent MultiIntentResult for mock classifier."""
    from services.domain.models import Intent

    intent = Intent(category=IntentCategory.CONVERSATION, action=action, confidence=1.0)
    return MultiIntentResult(intents=[intent], original_message="test", is_multi_intent=False)


@pytest.fixture
def mock_engine():
    return MagicMock()


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
            "message": "Default response.",
            "intent": {"category": "conversation", "action": "test"},
            "requires_clarification": False,
        }
    )
    return handlers


@pytest.fixture
def intent_service(mock_engine, mock_classifier, mock_canonical_handlers):
    service = IntentService(
        orchestration_engine=mock_engine,
        intent_classifier=mock_classifier,
    )
    service.canonical_handlers = mock_canonical_handlers
    service.intent_orchestrator = IntentOrchestrator(canonical_handlers=mock_canonical_handlers)
    return service


# ============================================================================
# LastOffer Data Model Tests
# ============================================================================


class TestLastOfferDataModel:
    """Tests for the LastOffer dataclass and ConversationContext integration."""

    def test_last_offer_creation(self):
        """LastOffer can be created with required fields."""
        offer = LastOffer(
            offer_type="contextual",
            continuation_hint="explain how project context works",
            offer_text="Would you like me to explain more?",
        )
        assert offer.offer_type == "contextual"
        assert offer.continuation_hint == "explain how project context works"
        assert offer.offer_text == "Would you like me to explain more?"

    def test_last_offer_default_offer_text(self):
        """offer_text defaults to empty string."""
        offer = LastOffer(offer_type="contextual", continuation_hint="test hint")
        assert offer.offer_text == ""

    def test_conversation_context_has_last_offer_field(self):
        """ConversationContext has a last_offer field defaulting to None."""
        ctx = ConversationContext()
        assert ctx.last_offer is None

    def test_conversation_context_stores_last_offer(self):
        """last_offer can be set and retrieved on ConversationContext."""
        ctx = ConversationContext()
        ctx.last_offer = LastOffer(
            offer_type="contextual",
            continuation_hint="test",
        )
        assert ctx.last_offer is not None
        assert ctx.last_offer.continuation_hint == "test"

    def test_last_offer_overwritten_by_newer(self):
        """Setting last_offer replaces the previous value."""
        ctx = ConversationContext()
        ctx.last_offer = LastOffer(offer_type="contextual", continuation_hint="first")
        ctx.last_offer = LastOffer(offer_type="contextual", continuation_hint="second")
        assert ctx.last_offer.continuation_hint == "second"


# ============================================================================
# Storage Tests (Step 3: intent_service stores offer_hint)
# ============================================================================


class TestOfferHintStorage:
    """Tests that canonical handler offer_hint is stored as last_offer."""

    @pytest.mark.asyncio
    async def test_offer_hint_stored_from_canonical_handler(
        self, intent_service, mock_canonical_handlers, mock_classifier
    ):
        """When canonical handler returns offer_hint, it's stored as last_offer."""
        mock_canonical_handlers.handle = AsyncMock(
            return_value={
                "message": "Would you like me to explain project context?",
                "intent": {"category": "status", "action": "provide_status"},
                "requires_clarification": False,
                "offer_hint": {
                    "continuation_hint": "explain how project context works",
                    "offer_text": "Would you like me to explain project context?",
                },
            }
        )
        # Issue #925: STATUS migrated to floor. Use PORTFOLIO (still canonical,
        # mutations) to test canonical handler offer_hint storage.
        from services.domain.models import Intent

        status_intent = Intent(
            category=IntentCategory.PORTFOLIO, action="portfolio_help", confidence=1.0
        )
        mock_classifier.classify_multiple = AsyncMock(
            return_value=MultiIntentResult(
                intents=[status_intent], original_message="test", is_multi_intent=False
            )
        )

        session_id = str(uuid4())
        await intent_service.process_intent(
            message="how do I set up projects?",
            session_id=session_id,
            user_id=None,
        )

        ctx = get_or_create_context(session_id)
        assert ctx.last_offer is not None
        assert ctx.last_offer.continuation_hint == "explain how project context works"
        assert ctx.last_offer.offer_type == "contextual"

    @pytest.mark.asyncio
    async def test_no_offer_hint_means_no_last_offer(
        self, intent_service, mock_canonical_handlers, mock_classifier
    ):
        """Normal response without offer_hint → no last_offer."""
        mock_canonical_handlers.handle = AsyncMock(
            return_value={
                "message": "Here's your project status.",
                "intent": {"category": "status", "action": "provide_status"},
                "requires_clarification": False,
            }
        )
        mock_classifier.classify_multiple = AsyncMock(
            return_value=_make_multi_result("provide_status")
        )

        session_id = str(uuid4())
        await intent_service.process_intent(
            message="what's the status of my project?",
            session_id=session_id,
            user_id=None,
        )

        ctx = get_or_create_context(session_id)
        assert ctx.last_offer is None

    @pytest.mark.asyncio
    async def test_action_required_does_not_set_last_offer(
        self, intent_service, mock_canonical_handlers, mock_classifier
    ):
        """action_required responses use WorkflowOfferService, not last_offer."""
        mock_canonical_handlers.handle = AsyncMock(
            return_value={
                "message": "Would you like help setting it up?",
                "intent": {"category": "status", "action": "provide_status"},
                "action_required": "setup_piper_config",
                "requires_clarification": False,
            }
        )
        mock_classifier.classify_multiple = AsyncMock(
            return_value=_make_multi_result("provide_status")
        )

        session_id = str(uuid4())
        await intent_service.process_intent(
            message="show me my config",
            session_id=session_id,
            user_id=None,
        )

        ctx = get_or_create_context(session_id)
        assert ctx.last_offer is None


# ============================================================================
# Consumption Tests (Step 4: bare affirmative + last_offer → hint)
# ============================================================================


class TestContextualOfferContinuation:
    """Tests that bare affirmative + last_offer → continuation hint to classifier."""

    @pytest.mark.asyncio
    async def test_yes_after_offer_passes_hint_to_classifier(
        self, intent_service, mock_classifier, mock_canonical_handlers
    ):
        """'yes' with last_offer → contextual_continuation_hint in classifier context."""
        session_id = str(uuid4())
        ctx = get_or_create_context(session_id)
        ctx.last_offer = LastOffer(
            offer_type="contextual",
            continuation_hint="explain how project context works",
        )

        mock_classifier.classify_multiple = AsyncMock(return_value=_make_multi_result())

        await intent_service.process_intent(
            message="yes",
            session_id=session_id,
            user_id=None,
        )

        # Verify classifier was called with continuation hint in context
        mock_classifier.classify_multiple.assert_called_once()
        call_kwargs = mock_classifier.classify_multiple.call_args
        context_arg = call_kwargs.kwargs.get("context") or (
            call_kwargs.args[1] if len(call_kwargs.args) > 1 else None
        )
        assert context_arg is not None
        assert context_arg["contextual_continuation_hint"] == "explain how project context works"

    @pytest.mark.asyncio
    async def test_sure_after_offer_passes_hint(
        self, intent_service, mock_classifier, mock_canonical_handlers
    ):
        """'sure' is also detected as acceptance."""
        session_id = str(uuid4())
        ctx = get_or_create_context(session_id)
        ctx.last_offer = LastOffer(
            offer_type="contextual",
            continuation_hint="provide integration guidance",
        )

        mock_classifier.classify_multiple = AsyncMock(return_value=_make_multi_result())

        await intent_service.process_intent(
            message="sure",
            session_id=session_id,
            user_id=None,
        )

        call_kwargs = mock_classifier.classify_multiple.call_args
        context_arg = call_kwargs.kwargs.get("context") or (
            call_kwargs.args[1] if len(call_kwargs.args) > 1 else None
        )
        assert context_arg is not None
        assert context_arg["contextual_continuation_hint"] == "provide integration guidance"

    @pytest.mark.asyncio
    async def test_last_offer_cleared_after_acceptance(
        self, intent_service, mock_classifier, mock_canonical_handlers
    ):
        """last_offer is cleared after processing, even on acceptance."""
        session_id = str(uuid4())
        ctx = get_or_create_context(session_id)
        ctx.last_offer = LastOffer(
            offer_type="contextual",
            continuation_hint="test hint",
        )

        mock_classifier.classify_multiple = AsyncMock(return_value=_make_multi_result())

        await intent_service.process_intent(
            message="yes",
            session_id=session_id,
            user_id=None,
        )

        assert ctx.last_offer is None

    @pytest.mark.asyncio
    async def test_no_after_offer_clears_no_hint(
        self, intent_service, mock_classifier, mock_canonical_handlers
    ):
        """'no' with last_offer → cleared, no continuation hint."""
        session_id = str(uuid4())
        ctx = get_or_create_context(session_id)
        ctx.last_offer = LastOffer(
            offer_type="contextual",
            continuation_hint="test hint",
        )

        mock_classifier.classify_multiple = AsyncMock(return_value=_make_multi_result())

        await intent_service.process_intent(
            message="no thanks",
            session_id=session_id,
            user_id=None,
        )

        # last_offer cleared
        assert ctx.last_offer is None

        # Classifier called without continuation hint
        call_kwargs = mock_classifier.classify_multiple.call_args
        context_arg = call_kwargs.kwargs.get("context") or (
            call_kwargs.args[1] if len(call_kwargs.args) > 1 else None
        )
        assert context_arg is None

    @pytest.mark.asyncio
    async def test_new_topic_after_offer_clears(
        self, intent_service, mock_classifier, mock_canonical_handlers
    ):
        """A new topic message clears last_offer, no hint injected."""
        session_id = str(uuid4())
        ctx = get_or_create_context(session_id)
        ctx.last_offer = LastOffer(
            offer_type="contextual",
            continuation_hint="test hint",
        )

        mock_classifier.classify_multiple = AsyncMock(return_value=_make_multi_result())

        await intent_service.process_intent(
            message="what's on my calendar tomorrow?",
            session_id=session_id,
            user_id=None,
        )

        assert ctx.last_offer is None
        call_kwargs = mock_classifier.classify_multiple.call_args
        context_arg = call_kwargs.kwargs.get("context") or (
            call_kwargs.args[1] if len(call_kwargs.args) > 1 else None
        )
        assert context_arg is None

    @pytest.mark.asyncio
    async def test_yes_without_last_offer_is_normal(
        self, intent_service, mock_classifier, mock_canonical_handlers
    ):
        """'yes' with no last_offer → normal classification, no hint."""
        session_id = str(uuid4())
        ctx = get_or_create_context(session_id)
        assert ctx.last_offer is None  # No offer set

        mock_classifier.classify_multiple = AsyncMock(return_value=_make_multi_result())

        await intent_service.process_intent(
            message="yes",
            session_id=session_id,
            user_id=None,
        )

        # Classifier called without continuation hint
        call_kwargs = mock_classifier.classify_multiple.call_args
        context_arg = call_kwargs.kwargs.get("context") or (
            call_kwargs.args[1] if len(call_kwargs.args) > 1 else None
        )
        assert context_arg is None
