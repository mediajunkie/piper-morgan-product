"""
Tests for soft offer accept/decline cycle.

Issue #824: Close the offer accept/decline loop — detect_offer_response
is now called when a pending offer exists, routing to acceptance or
decline handling before normal intent classification.

Tests verify:
- Accepting a pending offer returns workflow start message
- Declining a pending offer returns graceful acknowledgment
- Non-accept/decline message with pending offer continues normal processing
- No pending offer → normal processing (no interference)
- Pending offer clears after any response (accept, decline, or ignore)
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.orchestrator import IntentOrchestrator
from services.intent_service.pre_classifier import MultiIntentResult
from services.shared_types import IntentCategory


def _make_intent(category: IntentCategory, action: str) -> Intent:
    return Intent(category=category, action=action, confidence=1.0)


@pytest.fixture
def mock_engine():
    return MagicMock()


@pytest.fixture
def mock_classifier():
    classifier = MagicMock()
    classifier.classify_multiple = AsyncMock()
    classifier.classify = AsyncMock()
    return classifier


@pytest.fixture
def mock_canonical_handlers():
    handlers = MagicMock()
    handlers.can_handle = MagicMock(return_value=True)
    handlers.handle = AsyncMock(
        return_value={
            "message": "Default response.",
            "intent": {"category": "query", "action": "test"},
            "requires_clarification": False,
        }
    )
    return handlers


@pytest.fixture
def intent_service(mock_engine, mock_classifier, mock_canonical_handlers):
    # ADR-059: Register default workflows so dispatcher has entries
    from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY
    from services.intent_service.workflow_entries import register_default_workflows

    WORKFLOW_REGISTRY.clear()
    register_default_workflows()

    service = IntentService(
        intent_classifier=mock_classifier,
    )
    service.canonical_handlers = mock_canonical_handlers
    service.intent_orchestrator = IntentOrchestrator(canonical_handlers=mock_canonical_handlers)

    yield service

    # Clean up registry
    WORKFLOW_REGISTRY.clear()


class TestOfferAcceptance:
    """User accepts a pending soft offer."""

    @pytest.mark.asyncio
    async def test_yes_accepts_meeting_offer(self, intent_service, mock_classifier):
        """'Yes please' with pending meeting offer → dispatched via workflow registry."""
        # Mock slot filling on the intent_service so the meeting workflow entry point works
        mock_slot_response = MagicMock()
        mock_slot_response.message = "When would you like to meet?"
        mock_slot_response.filled_slots = {}
        mock_slot_response.template_name = "meeting"
        intent_service.slot_filling_adapter.manager.start_filling = AsyncMock(
            return_value=mock_slot_response
        )

        # Simulate a pending offer from previous turn
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_accept",
            {
                "workflow_type": "meeting",
                "offer_message": "Want me to help set up a meeting?",
                "decline_message": "No worries, just let me know if you change your mind.",
            },
        )

        result = await intent_service.process_intent(
            message="Yes please",
            session_id="sess_accept",
            user_id=None,
        )

        assert result.success
        # ADR-059: Meeting now dispatched via workflow registry
        assert result.intent_data["category"] == "soft_offer_accepted"
        assert result.intent_data["action"] == "meeting"
        assert result.intent_data["context"]["slot_filling_active"] is True

    @pytest.mark.asyncio
    async def test_sure_accepts_unregistered_workflow_routes_to_floor(
        self, intent_service, mock_classifier
    ):
        """ADR-059: 'Sure!' with unregistered workflow type → routes to floor."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_accept2",
            {
                "workflow_type": "status_check",
                "offer_message": "Want me to pull up the status?",
                "decline_message": "No worries.",
            },
        )

        result = await intent_service.process_intent(
            message="Sure!",
            session_id="sess_accept2",
            user_id=None,
        )

        # ADR-059: Unregistered workflow types route to floor (not dead-end acceptance)
        assert result.success
        # Floor routing produces an "unknown" category, not "soft_offer_accepted"
        assert result.intent_data["category"] == "unknown"

    @pytest.mark.asyncio
    async def test_go_ahead_accepts_unregistered_routes_to_floor(
        self, intent_service, mock_classifier
    ):
        """ADR-059: 'Go ahead' with unregistered workflow → routes to floor."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_go",
            {
                "workflow_type": "priority_check",
                "offer_message": "Want me to check priorities?",
                "decline_message": "No worries.",
            },
        )

        result = await intent_service.process_intent(
            message="Go ahead",
            session_id="sess_go",
            user_id=None,
        )

        # ADR-059: Unregistered workflow types route to floor
        assert result.success

    @pytest.mark.asyncio
    async def test_classifier_not_called_on_accept(self, intent_service, mock_classifier):
        """Accepting an offer should NOT trigger classification."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_no_classify",
            {
                "workflow_type": "meeting",
                "offer_message": "Want me to set up a meeting?",
                "decline_message": "No worries.",
            },
        )

        await intent_service.process_intent(
            message="Yes",
            session_id="sess_no_classify",
            user_id=None,
        )

        # Classifier should never be called
        mock_classifier.classify_multiple.assert_not_awaited()


class TestOfferDecline:
    """User declines a pending soft offer."""

    @pytest.mark.asyncio
    async def test_no_thanks_declines(self, intent_service, mock_classifier):
        """'No thanks' with pending offer → decline message."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_decline",
            {
                "workflow_type": "meeting",
                "offer_message": "Want me to set up a meeting?",
                "decline_message": "No worries, just let me know if you change your mind.",
            },
        )

        result = await intent_service.process_intent(
            message="No thanks",
            session_id="sess_decline",
            user_id=None,
        )

        assert result.success
        assert "no worries" in result.message.lower()
        assert result.intent_data["category"] == "soft_offer_declined"

    @pytest.mark.asyncio
    async def test_not_now_declines(self, intent_service, mock_classifier):
        """'Not now' with pending offer → decline."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_later",
            {
                "workflow_type": "status_check",
                "offer_message": "Want me to check?",
                "decline_message": "No problem, I'll be here if you need me.",
            },
        )

        result = await intent_service.process_intent(
            message="Not now",
            session_id="sess_later",
            user_id=None,
        )

        assert result.success
        assert result.intent_data["category"] == "soft_offer_declined"

    @pytest.mark.asyncio
    async def test_classifier_not_called_on_decline(self, intent_service, mock_classifier):
        """Declining an offer should NOT trigger classification."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_no_classify2",
            {
                "workflow_type": "meeting",
                "offer_message": "Want me to set up a meeting?",
                "decline_message": "No worries.",
            },
        )

        await intent_service.process_intent(
            message="Maybe later",
            session_id="sess_no_classify2",
            user_id=None,
        )

        mock_classifier.classify_multiple.assert_not_awaited()


class TestOfferIgnored:
    """User says something unrelated to the pending offer."""

    @pytest.mark.asyncio
    async def test_new_topic_continues_normally(self, intent_service, mock_classifier):
        """New topic with pending offer → normal processing, offer cleared."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_ignore",
            {
                "workflow_type": "meeting",
                "offer_message": "Want me to set up a meeting?",
                "decline_message": "No worries.",
            },
        )

        # #925: STATUS migrated to floor. Use PORTFOLIO (still canonical)
        # to test that a new topic with a pending offer clears the offer.
        intent = _make_intent(IntentCategory.PORTFOLIO, "portfolio_help")
        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="Tell me about my projects",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "Your project portfolio looks good.",
            "intent": {"category": "portfolio", "action": "portfolio_help"},
        }

        result = await intent_service.process_intent(
            message="Tell me about my projects",
            session_id="sess_ignore",
            user_id=None,
        )

        # Should proceed with normal processing
        assert result.success
        assert "project" in result.message.lower()
        # Classifier WAS called (normal flow)
        mock_classifier.classify_multiple.assert_awaited_once()


class TestNoPendingOffer:
    """No pending offer → normal processing unaffected."""

    @pytest.mark.asyncio
    async def test_yes_without_pending_offer_is_normal(self, intent_service, mock_classifier):
        """'Yes' without a pending offer → normal classification."""
        intent = _make_intent(IntentCategory.CONVERSATION, "affirmation")

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="Yes",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "Great!",
            "intent": {"category": "conversation", "action": "affirmation"},
        }

        result = await intent_service.process_intent(
            message="Yes",
            session_id="sess_no_offer",
            user_id=None,
        )

        # Normal processing — classifier was called
        assert result.success
        mock_classifier.classify_multiple.assert_awaited_once()


class TestPendingOfferClearing:
    """Pending offer clears after any response type."""

    @pytest.mark.asyncio
    async def test_offer_clears_after_accept(self, intent_service, mock_classifier):
        """After acceptance, no pending offer remains."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_clear",
            {
                "workflow_type": "meeting",
                "offer_message": "Want me to set up a meeting?",
                "decline_message": "No worries.",
            },
        )

        await intent_service.process_intent(
            message="Yes",
            session_id="sess_clear",
            user_id=None,
        )

        # Offer should be cleared
        assert (
            intent_service.workflow_offer_service.get_and_clear_pending_offer("sess_clear") is None
        )

    @pytest.mark.asyncio
    async def test_offer_clears_after_ignore(self, intent_service, mock_classifier):
        """After ignoring, no pending offer remains."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_clear2",
            {
                "workflow_type": "meeting",
                "offer_message": "Want me to set up a meeting?",
                "decline_message": "No worries.",
            },
        )

        intent = _make_intent(IntentCategory.STATUS, "get_project_status")
        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="Check status",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "Status report.",
            "intent": {"category": "status", "action": "get_project_status"},
        }

        await intent_service.process_intent(
            message="Check status",
            session_id="sess_clear2",
            user_id=None,
        )

        # Offer should be cleared (get_and_clear was already called)
        assert (
            intent_service.workflow_offer_service.get_and_clear_pending_offer("sess_clear2") is None
        )


class TestSlotFillingOnAccept:
    """Issue #825: Accepting a meeting offer starts slot filling."""

    @pytest.mark.asyncio
    async def test_meeting_accept_starts_slot_filling(self, intent_service, mock_classifier):
        """'Yes' to meeting offer → slot filling session starts, prompts for slots."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_slot",
            {
                "workflow_type": "meeting",
                "offer_message": "Want me to help set up a meeting?",
                "decline_message": "No worries.",
                "trigger_message": "I need to get the team together Tuesday",
            },
        )

        result = await intent_service.process_intent(
            message="Yes please",
            session_id="sess_slot",
            user_id=None,
        )

        assert result.success
        assert result.intent_data["category"] == "soft_offer_accepted"
        assert result.intent_data["action"] == "meeting"
        # Should have slot filling context
        assert result.intent_data.get("context", {}).get("slot_filling_active") is True
        assert result.intent_data["context"]["template_name"] == "schedule_meeting"

    @pytest.mark.asyncio
    async def test_meeting_accept_has_acceptance_message(self, intent_service, mock_classifier):
        """Acceptance response includes both acceptance message and slot prompt."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_slot2",
            {
                "workflow_type": "meeting",
                "offer_message": "Want me to help set up a meeting?",
                "decline_message": "No worries.",
                "trigger_message": "We should sync up about the project",
            },
        )

        result = await intent_service.process_intent(
            message="Sure!",
            session_id="sess_slot2",
            user_id=None,
        )

        assert result.success
        # Acceptance message ("Great! Let me help set that up.") should be in response
        assert "set that up" in result.message.lower() or "help" in result.message.lower()
        # Slot filling prompt should also be present (asking for missing slots)
        # The exact wording depends on slot prompts, but message should be multi-part
        assert len(result.message) > 40  # More than just the acceptance

    @pytest.mark.asyncio
    async def test_meeting_accept_creates_active_session(self, intent_service, mock_classifier):
        """After accepting meeting offer, slot filling session is active."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_slot3",
            {
                "workflow_type": "meeting",
                "offer_message": "Want me to help set up a meeting?",
                "decline_message": "No worries.",
                "trigger_message": "I need to get the team together",
            },
        )

        await intent_service.process_intent(
            message="Yes",
            session_id="sess_slot3",
            user_id=None,
        )

        # Slot filling adapter should have an active session
        has_session = intent_service.slot_filling_adapter.manager.has_active_session(
            None, "sess_slot3"
        )
        assert has_session

    @pytest.mark.asyncio
    async def test_non_meeting_accept_routes_to_floor(self, intent_service, mock_classifier):
        """ADR-059: Accepting unregistered workflow → routes to floor, no slot filling."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_status",
            {
                "workflow_type": "status_check",
                "offer_message": "Want me to pull up the status?",
                "decline_message": "No problem.",
                "trigger_message": "I'm worried about the deadline",
            },
        )

        result = await intent_service.process_intent(
            message="Yes please",
            session_id="sess_status",
            user_id=None,
        )

        # ADR-059: Unregistered workflow types route to floor
        assert result.success
        assert result.intent_data["category"] == "unknown"

    @pytest.mark.asyncio
    async def test_meeting_accept_without_trigger_still_works(
        self, intent_service, mock_classifier
    ):
        """Meeting offer without trigger_message still starts slot filling."""
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_no_trigger",
            {
                "workflow_type": "meeting",
                "offer_message": "Want me to help set up a meeting?",
                "decline_message": "No worries.",
                # No trigger_message — should default to empty string
            },
        )

        result = await intent_service.process_intent(
            message="Go ahead",
            session_id="sess_no_trigger",
            user_id=None,
        )

        assert result.success
        assert result.intent_data["category"] == "soft_offer_accepted"
        assert result.intent_data.get("context", {}).get("slot_filling_active") is True

    @pytest.mark.asyncio
    async def test_subsequent_turn_handled_by_slot_filling(
        self, intent_service, mock_classifier, mock_canonical_handlers
    ):
        """After accepting meeting offer, next message goes to slot filling."""
        # Turn 1: Set up and accept offer
        intent_service.workflow_offer_service.set_pending_offer(
            "sess_turn2",
            {
                "workflow_type": "meeting",
                "offer_message": "Want me to help set up a meeting?",
                "decline_message": "No worries.",
                "trigger_message": "I need to get the team together",
            },
        )

        await intent_service.process_intent(
            message="Yes",
            session_id="sess_turn2",
            user_id=None,
        )

        # Turn 2: Respond with slot data — should be handled by slot filling,
        # NOT by the classifier
        mock_classifier.classify_multiple.reset_mock()

        result = await intent_service.process_intent(
            message="Tuesday at 2pm with the design team",
            session_id="sess_turn2",
            user_id=None,
        )

        assert result.success
        # Classifier should NOT have been called — slot filling handled it
        mock_classifier.classify_multiple.assert_not_awaited()


class TestEmbeddedOfferRegistration:
    """Issue #846: Canonical handler responses with embedded offers register as pending."""

    @pytest.mark.asyncio
    async def test_portfolio_offer_registers_as_pending(self, intent_service, mock_classifier):
        """#925: When canonical handler returns action_required, a pending offer is registered.
        Uses PORTFOLIO (still canonical) since PRIORITY migrated to floor."""
        intent_service.canonical_handlers.handle = AsyncMock(
            return_value={
                "message": "You don't have any projects configured yet. "
                "Would you like me to help you set up your project list?",
                "action_required": "configure_projects",
                "intent": {
                    "category": "portfolio",
                    "action": "portfolio_help",
                    "confidence": 1.0,
                },
            }
        )

        portfolio_intent = _make_intent(IntentCategory.PORTFOLIO, "portfolio_help")
        mock_classifier.classify.return_value = portfolio_intent
        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[portfolio_intent],
        )

        await intent_service.process_intent(
            message="Tell me about my projects",
            session_id="sess_embedded",
            user_id=None,
        )

        # A pending offer should now exist
        pending = intent_service.workflow_offer_service.get_and_clear_pending_offer(
            "sess_embedded", user_id=None
        )
        assert pending is not None
        assert pending["workflow_type"] == "project_setup"

    @pytest.mark.asyncio
    async def test_yes_after_priority_offer_is_accepted(self, intent_service, mock_classifier):
        """Issue #846: 'Yes' after portfolio offer should be accepted, not classified as greeting."""
        # #925: Step 1 uses PORTFOLIO (still canonical) since PRIORITY migrated to floor
        intent_service.canonical_handlers.handle = AsyncMock(
            return_value={
                "message": "You don't have any projects configured yet. "
                "Would you like me to help you set up your project list?",
                "action_required": "configure_projects",
                "intent": {
                    "category": "portfolio",
                    "action": "portfolio_help",
                    "confidence": 1.0,
                },
            }
        )

        portfolio_intent = _make_intent(IntentCategory.PORTFOLIO, "portfolio_help")
        mock_classifier.classify.return_value = portfolio_intent
        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[portfolio_intent],
        )

        await intent_service.process_intent(
            message="Tell me about my projects",
            session_id="sess_yes_846",
            user_id=None,
        )

        # Step 2: User responds "yes"
        result = await intent_service.process_intent(
            message="yes",
            session_id="sess_yes_846",
            user_id=None,
        )

        # ADR-059: Should be accepted (not classified as greeting),
        # but priority_check is unregistered → routes to floor
        assert result.success
        # The key assertion: "yes" was NOT classified as a greeting
        assert result.intent_data.get("category") != "conversation"

    @pytest.mark.asyncio
    async def test_project_offer_registers_as_pending(self, intent_service, mock_classifier):
        """#925: Project setup offer via PORTFOLIO (still canonical) registers as pending."""
        intent_service.canonical_handlers.handle = AsyncMock(
            return_value={
                "message": "You don't have any active projects configured yet. "
                "Would you like me to help you set up your project portfolio?",
                "action_required": "configure_projects",
                "intent": {
                    "category": "portfolio",
                    "action": "portfolio_help",
                    "confidence": 1.0,
                },
            }
        )

        portfolio_intent = _make_intent(IntentCategory.PORTFOLIO, "portfolio_help")
        mock_classifier.classify.return_value = portfolio_intent
        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[portfolio_intent],
        )

        await intent_service.process_intent(
            message="What are my projects?",
            session_id="sess_project_846",
            user_id=None,
        )

        pending = intent_service.workflow_offer_service.get_and_clear_pending_offer(
            "sess_project_846", user_id=None
        )
        assert pending is not None
        assert pending["workflow_type"] == "project_setup"
