"""
Test graceful error handling in canonical handlers.
Ensures service failures provide helpful fallback responses instead of crashes.
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.domain.models import Intent
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.shared_types import IntentCategory


@pytest.fixture
def handlers():
    return CanonicalHandlers()


@pytest.mark.asyncio
async def test_temporal_query_calendar_unavailable(handlers):
    """Temporal query should work even if calendar fails."""

    # Mock calendar service to fail
    with patch(
        "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter"
    ) as mock_calendar:
        mock_calendar.return_value.get_temporal_summary = AsyncMock(
            side_effect=Exception("Calendar service unavailable")
        )

        intent = Intent(
            original_message="What day is it?",
            category=IntentCategory.TEMPORAL,
            action="provide_date",
            confidence=1.0,
        )

        response = await handlers._handle_temporal_query(intent, "test_session")

        # Should still return date/time
        assert "Today is" in response["message"]
        # Check calendar service status in context
        calendar_context = response["intent"]["context"].get("calendar_context", {})
        assert calendar_context.get("calendar_service") == "unavailable"
        assert calendar_context.get("fallback_used") is True
        assert "calendar" in response["message"].lower()


@pytest.mark.asyncio
async def test_status_query_missing_config(handlers):
    """Status query should handle missing PIPER.md gracefully."""

    # Mock user context service to fail
    with patch(
        "services.user_context_service.user_context_service.get_user_context"
    ) as mock_context:
        mock_context.side_effect = FileNotFoundError("PIPER.md not found")

        intent = Intent(
            original_message="What am I working on?",
            category=IntentCategory.STATUS,
            action="provide_status",
            confidence=1.0,
        )

        response = await handlers._handle_status_query(intent, "test_session")

        # Should provide helpful error message
        assert "configuration" in response["message"].lower()
        assert (
            "setting it up" in response["message"].lower() or "setup" in response["message"].lower()
        )
        assert response["error"] == "config_unavailable"
        assert response["action_required"] == "setup_piper_config"


@pytest.mark.asyncio
async def test_status_query_empty_projects(handlers):
    """Status query should handle empty projects list."""

    # Mock user context with no projects
    from services.user_context_service import UserContext

    empty_context = UserContext(user_id="test_user", projects=[], priorities=["Complete testing"])

    with patch(
        "services.user_context_service.user_context_service.get_user_context"
    ) as mock_context:
        mock_context.return_value = empty_context

        intent = Intent(
            original_message="What am I working on?",
            category=IntentCategory.STATUS,
            action="provide_status",
            confidence=1.0,
        )

        response = await handlers._handle_status_query(intent, "test_session")

        # Should provide helpful message
        assert "configure" in response["message"].lower() or "set up" in response["message"].lower()
        assert response.get("action_required") == "configure_projects"


@pytest.mark.asyncio
async def test_priority_query_missing_config(handlers):
    """Priority query should handle missing PIPER.md gracefully."""

    # Mock user context service to fail
    with patch(
        "services.user_context_service.user_context_service.get_user_context"
    ) as mock_context:
        mock_context.side_effect = Exception("Configuration unavailable")

        intent = Intent(
            original_message="What's my top priority?",
            category=IntentCategory.PRIORITY,
            action="provide_priority",
            confidence=1.0,
        )

        response = await handlers._handle_priority_query(intent, "test_session")

        # Should provide helpful error message
        assert "configuration" in response["message"].lower()
        assert (
            "setting it up" in response["message"].lower() or "setup" in response["message"].lower()
        )
        assert response["error"] == "config_unavailable"
        assert response["action_required"] == "setup_piper_config"


@pytest.mark.asyncio
async def test_priority_query_empty_priorities(handlers):
    """Priority query should handle empty priorities list."""

    # Mock user context with no priorities
    from services.user_context_service import UserContext

    empty_context = UserContext(user_id="test_user", projects=["Test Project"], priorities=[])

    with patch(
        "services.user_context_service.user_context_service.get_user_context"
    ) as mock_context:
        mock_context.return_value = empty_context

        intent = Intent(
            original_message="What's my top priority?",
            category=IntentCategory.PRIORITY,
            action="provide_priority",
            confidence=1.0,
        )

        response = await handlers._handle_priority_query(intent, "test_session")

        # Should provide helpful message
        assert "configure" in response["message"].lower() or "set up" in response["message"].lower()
        assert response.get("action_required") == "configure_priorities"


@pytest.mark.asyncio
async def test_guidance_without_user_context(handlers):
    """Guidance should work with generic advice if context unavailable."""

    # Mock context to fail
    with patch(
        "services.user_context_service.user_context_service.get_user_context"
    ) as mock_context:
        mock_context.side_effect = Exception("Context unavailable")

        intent = Intent(
            original_message="What should I focus on?",
            category=IntentCategory.GUIDANCE,
            action="provide_guidance",
            confidence=1.0,
        )

        response = await handlers._handle_guidance_query(intent, "test_session")

        # Should still provide guidance (time-based)
        assert len(response["message"]) > 20
        assert response["fallback_guidance"] is True
        assert response["personalized"] is False


@pytest.mark.asyncio
async def test_guidance_with_partial_context(handlers):
    """Guidance should work with partial user context."""

    # Mock user context with only organization, no projects/priorities
    from services.user_context_service import UserContext

    partial_context = UserContext(
        user_id="test_user", organization="Test Org", projects=[], priorities=[]
    )

    with patch(
        "services.user_context_service.user_context_service.get_user_context"
    ) as mock_context:
        mock_context.return_value = partial_context

        intent = Intent(
            original_message="What should I focus on?",
            category=IntentCategory.GUIDANCE,
            action="provide_guidance",
            confidence=1.0,
        )

        response = await handlers._handle_guidance_query(intent, "test_session")

        # Should provide guidance with organization context
        assert "Test Org" in response["message"]
        assert response["personalized"] is True
        assert response["fallback_guidance"] is False


# Spatial context test removed - Intent class doesn't have spatial_context field yet


@pytest.mark.asyncio
async def test_all_handlers_graceful_degradation(handlers):
    """All handlers should degrade gracefully when services fail."""

    # Mock all services to fail
    with (
        patch(
            "services.user_context_service.user_context_service.get_user_context"
        ) as mock_context,
        patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter"
        ) as mock_calendar,
    ):
        mock_context.side_effect = Exception("All services down")
        mock_calendar.return_value.get_temporal_summary = AsyncMock(
            side_effect=Exception("Calendar service unavailable")
        )

        test_cases = [
            (IntentCategory.TEMPORAL, "What day is it?", "provide_date"),
            (IntentCategory.STATUS, "What am I working on?", "provide_status"),
            (IntentCategory.PRIORITY, "What's my top priority?", "provide_priority"),
            (IntentCategory.GUIDANCE, "What should I focus on?", "provide_guidance"),
        ]

        for category, text, action in test_cases:
            intent = Intent(original_message=text, category=category, action=action, confidence=1.0)

            # Should not crash
            if category == IntentCategory.TEMPORAL:
                response = await handlers._handle_temporal_query(intent, "test_session")
            elif category == IntentCategory.STATUS:
                response = await handlers._handle_status_query(intent, "test_session")
            elif category == IntentCategory.PRIORITY:
                response = await handlers._handle_priority_query(intent, "test_session")
            elif category == IntentCategory.GUIDANCE:
                response = await handlers._handle_guidance_query(intent, "test_session")

            # Should have a message
            assert "message" in response
            assert len(response["message"]) > 10

            # Should indicate fallback/error state appropriately
            if category == IntentCategory.TEMPORAL:
                calendar_context = response["intent"]["context"].get("calendar_context", {})
                assert calendar_context.get("fallback_used") is True
            elif category in [IntentCategory.STATUS, IntentCategory.PRIORITY]:
                assert response.get("error") == "config_unavailable"
            elif category == IntentCategory.GUIDANCE:
                assert response.get("fallback_guidance") is True
