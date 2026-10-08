"""
Issue #490: End-to-end integration tests for portfolio onboarding.

Epic: FTUX (First Time User Experience)
Phase 3: Handler Integration & Persistence

Tests the full flow:
1. User with no projects greets → onboarding prompt
2. User provides project info → project extracted
3. User confirms → project persisted
4. Subsequent greetings → normal (no onboarding)
"""

import pytest

# ADR-059: Onboarding on ice
pytestmark = pytest.mark.skip(reason="ADR-059: onboarding on ice")


from unittest.mock import patch

import pytest

from services.conversation.conversation_handler import ConversationHandler
from services.domain.models import Intent
from services.shared_types import IntentCategory, PortfolioOnboardingState


@pytest.fixture
def conversation_handler():
    """Create a ConversationHandler for testing."""
    return ConversationHandler()


class TestPortfolioOnboardingE2E:
    """End-to-end tests for portfolio onboarding flow."""

    # #1886: test_greeting_triggers_onboarding_for_new_user and
    # test_existing_user_gets_normal_greeting deleted. Both existed only to
    # exercise ConversationHandler._check_portfolio_onboarding (Rule-0
    # deleted — its own, only, production call site in _respond_to_greeting
    # was already commented out under ADR-059: "Portfolio onboarding offer
    # disabled"). There is no live behavior left for either test to cover —
    # a new/existing user's greeting takes the same normal-greeting path
    # regardless of project count, since nothing calls the onboarding-offer
    # check at all. See #1886 session log.

    @pytest.mark.asyncio
    async def test_onboarding_turn_routing(self, conversation_handler):
        """
        Issue #490: Subsequent messages during onboarding should be routed.

        Tests that after onboarding starts, user messages are routed to
        the onboarding handler (not normal intent processing).
        """
        from services.onboarding import PortfolioOnboardingHandler, PortfolioOnboardingManager

        # Create a real onboarding session
        manager = PortfolioOnboardingManager()
        session = manager.create_session("test-session-123", "test-user-123")
        manager.transition_state(session.id, PortfolioOnboardingState.GATHERING_PROJECTS)

        # Create intent with user response to onboarding
        project_intent = Intent(
            category=IntentCategory.CONVERSATION,
            action="chitchat",  # Would normally be chitchat
            confidence=0.5,
            context={
                "user_id": "test-user-123",
                "original_message": "I'm building an app called HealthTrack",
            },
        )

        # Mock the onboarding components to use our test session
        with patch(
            "services.conversation.conversation_handler._get_onboarding_components"
        ) as mock_get_components:
            handler = PortfolioOnboardingHandler(manager)
            mock_get_components.return_value = (manager, handler)

            response = await conversation_handler.respond(
                project_intent, session_id="test-session-123"
            )

            # Should be routed to onboarding handler
            assert response["intent"]["action"] == "portfolio_onboarding"
            assert "healthtrack" in response["message"].lower()

    @pytest.mark.asyncio
    async def test_full_onboarding_flow_with_persistence(self, conversation_handler):
        """
        Issue #490: Complete onboarding flow from greeting to project saved.

        Full flow test:
        1. User greets → onboarding prompt
        2. User accepts → asks for project
        3. User provides project → confirms
        4. User confirms → project persisted
        """
        from services.onboarding import PortfolioOnboardingHandler, PortfolioOnboardingManager

        manager = PortfolioOnboardingManager()
        handler = PortfolioOnboardingHandler(manager)

        # Step 1: Start onboarding. #1886: PortfolioOnboardingHandler.
        # start_onboarding was Rule-0 deleted (zero production callers) —
        # the session is created directly via the manager, exactly what
        # start_onboarding itself did minus the deleted wrapper.
        session = manager.create_session("test-session-123", "test-user-123")
        assert session.state == PortfolioOnboardingState.INITIATED
        onboarding_id = session.id

        # Step 2: User accepts
        response = handler.handle_turn(onboarding_id, "Yes, please!")
        assert response.state == PortfolioOnboardingState.GATHERING_PROJECTS

        # Step 3: User provides project info
        response = handler.handle_turn(
            onboarding_id, "I'm building a mobile app called HealthTrack"
        )
        assert response.state == PortfolioOnboardingState.GATHERING_PROJECTS
        assert "healthtrack" in response.message.lower()

        # Step 4: User says done
        response = handler.handle_turn(onboarding_id, "That's all for now")
        assert response.state == PortfolioOnboardingState.CONFIRMING

        # Step 5: User confirms
        response = handler.handle_turn(onboarding_id, "Yes, save it")
        assert response.state == PortfolioOnboardingState.COMPLETE
        assert response.is_complete is True
        assert response.captured_projects is not None
        assert len(response.captured_projects) == 1
        assert response.captured_projects[0]["name"] == "HealthTrack"

    @pytest.mark.asyncio
    async def test_decline_flow_does_not_persist(self, conversation_handler):
        """
        Issue #490: Declining onboarding should not create projects.
        """
        from services.onboarding import PortfolioOnboardingHandler, PortfolioOnboardingManager

        manager = PortfolioOnboardingManager()
        handler = PortfolioOnboardingHandler(manager)

        # Start onboarding. #1886: start_onboarding Rule-0 deleted — create
        # the session directly via the manager instead.
        onboarding_id = manager.create_session("test-session-123", "test-user-123").id

        # User declines
        response = handler.handle_turn(onboarding_id, "No thanks")
        assert response.state == PortfolioOnboardingState.DECLINED
        assert response.is_complete is True
        assert response.captured_projects is None


class TestOnboardingPersistence:
    """Tests for project persistence during onboarding."""

    @pytest.mark.asyncio
    async def test_persist_handles_empty_projects(self):
        """
        Issue #490: Empty project list should not cause errors.

        This tests the guard clause that prevents unnecessary database
        operations when there are no projects to persist.
        """
        handler = ConversationHandler()

        # Should not raise any errors - empty list returns early
        await handler._persist_onboarding_projects("test-user-123", [])
        # None also returns early
        await handler._persist_onboarding_projects("test-user-123", None)

    @pytest.mark.asyncio
    async def test_persist_method_exists_and_is_async(self):
        """
        Issue #490: Verify persistence method is properly defined.
        """
        handler = ConversationHandler()

        # Verify the method exists and is coroutine
        import inspect

        assert hasattr(handler, "_persist_onboarding_projects")
        assert inspect.iscoroutinefunction(handler._persist_onboarding_projects)

    @pytest.mark.asyncio
    async def test_persist_gracefully_handles_db_errors(self):
        """
        Issue #490: Verify persistence handles database errors gracefully.

        The method catches exceptions and logs them rather than crashing.
        """
        handler = ConversationHandler()

        captured_projects = [
            {"name": "TestProject", "description": "Test"},
        ]

        # This will fail because no real database is connected,
        # but should not raise an exception (it logs the error instead)
        # The method catches all exceptions and logs them
        await handler._persist_onboarding_projects("test-user-123", captured_projects)
        # If we get here without an exception, the error handling works
