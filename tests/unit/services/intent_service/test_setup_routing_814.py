"""
Tests for Issue #814: Explicit setup requests should trigger interactive onboarding.

Verifies:
- "Help me set up a project" with 0 projects → starts interactive onboarding
- "Help me set up a project" with N>0 projects → state-aware response (Option C)
- "Help me get started" routes to GUIDANCE, not DISCOVERY
- Integration setup includes continuity language (Option B)
- Formality-aware response variants
- Greeting-triggered onboarding still works (regression)
"""

import re
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.canonical_handlers import CanonicalHandlers
from services.shared_types import IntentCategory as IntentCategoryEnum


@pytest.fixture
def canonical_handlers():
    """Fixture to create CanonicalHandlers instance."""
    return CanonicalHandlers()


def _make_intent(message: str):
    """Create an Intent-like object for testing."""
    from services.domain.models import Intent

    return Intent(
        category=IntentCategoryEnum.GUIDANCE,
        action="get_contextual_guidance",
        confidence=1.0,
        context={"original_message": message},
        original_message=message,
    )


class TestProjectSetupZeroProjects:
    """Issue #814: When user has 0 projects, explicit setup triggers onboarding."""

    @pytest.mark.asyncio
    async def test_zero_projects_returns_guidance(self, canonical_handlers):
        """ADR-059: With 0 projects, returns static guidance (onboarding on ice)."""
        intent = _make_intent("help me set up a project")

        mock_user_context = MagicMock()
        mock_user_context.projects = []

        with patch(
            "services.intent_service.canonical_handlers.user_context_service.get_user_context",
            new_callable=AsyncMock,
            return_value=mock_user_context,
        ):
            result = await canonical_handlers._handle_project_setup_request(
                intent, "sess-1", "user-1"
            )

        # ADR-059: Returns static guidance instead of launching onboarding
        assert result["intent"]["action"] == "provide_setup_guidance"

    @pytest.mark.asyncio
    async def test_no_user_id_falls_back_to_static(self, canonical_handlers):
        """Without user_id, falls back to static guidance."""
        intent = _make_intent("help me set up a project")

        result = await canonical_handlers._handle_project_setup_request(
            intent, "sess-1", user_id=None
        )

        assert result["intent"]["action"] == "provide_setup_guidance"
        assert "Settings" in result["message"] or "settings" in result["message"].lower()

    @pytest.mark.asyncio
    async def test_onboarding_failure_falls_back_to_static(self, canonical_handlers):
        """If onboarding start fails, falls back to static guidance."""
        intent = _make_intent("help me set up a project")

        mock_user_context = MagicMock()
        mock_user_context.projects = []

        with (
            patch(
                "services.intent_service.canonical_handlers.user_context_service.get_user_context",
                new_callable=AsyncMock,
                return_value=mock_user_context,
            ),
            patch(
                "services.conversation.conversation_handler._get_onboarding_components",
                side_effect=Exception("Onboarding unavailable"),
            ),
        ):
            result = await canonical_handlers._handle_project_setup_request(
                intent, "sess-1", "user-1"
            )

        assert result["intent"]["action"] == "provide_setup_guidance"
        assert "onboarding_session" not in result


class TestProjectSetupExistingProjects:
    """Issue #814: When user has N>0 projects, return state-aware response (Option C)."""

    @pytest.mark.asyncio
    async def test_existing_projects_shows_count(self, canonical_handlers):
        """With existing projects, response acknowledges project count."""
        intent = _make_intent("set up my projects")

        mock_user_context = MagicMock()
        mock_user_context.projects = ["Alpha", "Beta", "Gamma"]

        with patch(
            "services.intent_service.canonical_handlers.user_context_service.get_user_context",
            new_callable=AsyncMock,
            return_value=mock_user_context,
        ):
            result = await canonical_handlers._handle_project_setup_request(
                intent, "sess-1", "user-1"
            )

        assert "3 projects" in result["message"]
        assert result["intent"]["context"]["project_count"] == 3

    @pytest.mark.asyncio
    async def test_existing_projects_lists_names(self, canonical_handlers):
        """Response includes project names."""
        intent = _make_intent("set up my projects")

        mock_user_context = MagicMock()
        mock_user_context.projects = ["Alpha", "Beta"]

        with patch(
            "services.intent_service.canonical_handlers.user_context_service.get_user_context",
            new_callable=AsyncMock,
            return_value=mock_user_context,
        ):
            result = await canonical_handlers._handle_project_setup_request(
                intent, "sess-1", "user-1"
            )

        assert "Alpha" in result["message"]
        assert "Beta" in result["message"]

    @pytest.mark.asyncio
    async def test_existing_projects_offers_add_or_review(self, canonical_handlers):
        """Response offers to add more or review existing."""
        intent = _make_intent("set up my projects")

        mock_user_context = MagicMock()
        mock_user_context.projects = ["Alpha"]

        with patch(
            "services.intent_service.canonical_handlers.user_context_service.get_user_context",
            new_callable=AsyncMock,
            return_value=mock_user_context,
        ):
            result = await canonical_handlers._handle_project_setup_request(
                intent, "sess-1", "user-1"
            )

        msg = result["message"].lower()
        assert "add" in msg or "another" in msg
        assert "review" in msg or "existing" in msg
        assert "offer_hint" in result

    @pytest.mark.asyncio
    async def test_existing_projects_does_not_start_onboarding(self, canonical_handlers):
        """N>0 projects should NOT trigger onboarding."""
        intent = _make_intent("set up my projects")

        mock_user_context = MagicMock()
        mock_user_context.projects = ["Alpha", "Beta"]

        with patch(
            "services.intent_service.canonical_handlers.user_context_service.get_user_context",
            new_callable=AsyncMock,
            return_value=mock_user_context,
        ):
            result = await canonical_handlers._handle_project_setup_request(
                intent, "sess-1", "user-1"
            )

        assert "onboarding_session" not in result
        assert result["intent"]["action"] == "provide_setup_guidance"

    @pytest.mark.asyncio
    async def test_truncates_long_project_list(self, canonical_handlers):
        """More than 5 projects shows '... and N more'."""
        intent = _make_intent("set up my projects")

        mock_user_context = MagicMock()
        mock_user_context.projects = [f"Project-{i}" for i in range(7)]

        with patch(
            "services.intent_service.canonical_handlers.user_context_service.get_user_context",
            new_callable=AsyncMock,
            return_value=mock_user_context,
        ):
            result = await canonical_handlers._handle_project_setup_request(
                intent, "sess-1", "user-1"
            )

        assert "... and 2 more" in result["message"]


class TestProjectSetupFormality:
    """Issue #814 + #838: Formality-aware responses."""

    @pytest.mark.asyncio
    async def test_warm_formality_uses_casual_language(self, canonical_handlers):
        """Warm formality uses casual language."""
        intent = _make_intent("set up my projects")

        mock_user_context = MagicMock()
        mock_user_context.projects = ["Alpha"]

        with (
            patch(
                "services.intent_service.canonical_handlers.user_context_service.get_user_context",
                new_callable=AsyncMock,
                return_value=mock_user_context,
            ),
            patch(
                "services.personality.formality.DEFAULT_WARMTH",
                0.8,
            ),
        ):
            result = await canonical_handlers._handle_project_setup_request(
                intent, "sess-1", "user-1"
            )

        assert "You've already got" in result["message"]

    @pytest.mark.asyncio
    async def test_professional_formality_uses_formal_language(self, canonical_handlers):
        """Professional formality uses formal language."""
        intent = _make_intent("set up my projects")

        mock_user_context = MagicMock()
        mock_user_context.projects = ["Alpha"]

        with (
            patch(
                "services.intent_service.canonical_handlers.user_context_service.get_user_context",
                new_callable=AsyncMock,
                return_value=mock_user_context,
            ),
            patch(
                "services.personality.formality.DEFAULT_WARMTH",
                0.2,
            ),
        ):
            result = await canonical_handlers._handle_project_setup_request(
                intent, "sess-1", "user-1"
            )

        assert "You currently have" in result["message"]

    @pytest.mark.asyncio
    async def test_balanced_formality_uses_neutral_language(self, canonical_handlers):
        """Balanced formality uses neutral language."""
        intent = _make_intent("set up my projects")

        mock_user_context = MagicMock()
        mock_user_context.projects = ["Alpha"]

        with (
            patch(
                "services.intent_service.canonical_handlers.user_context_service.get_user_context",
                new_callable=AsyncMock,
                return_value=mock_user_context,
            ),
            patch(
                "services.personality.formality.DEFAULT_WARMTH",
                0.5,
            ),
        ):
            result = await canonical_handlers._handle_project_setup_request(
                intent, "sess-1", "user-1"
            )

        assert "You have" in result["message"]
        assert "in your portfolio" in result["message"]


class TestPatternCollisionFix:
    """Issue #814: Fix 'help me get started' routing collision."""

    def test_help_me_get_started_not_in_discovery_patterns(self):
        """'help me get started' should not be in DISCOVERY_PATTERNS."""
        from services.intent_service.pre_classifier import PreClassifier

        for pattern in PreClassifier.DISCOVERY_PATTERNS:
            assert "help me get started" not in pattern

    def test_help_me_get_started_matches_guidance_patterns(self):
        """'help me get started' should match GUIDANCE_PATTERNS via 'get started'."""
        from services.intent_service.pre_classifier import PreClassifier

        test_message = "help me get started"
        matches_guidance = any(
            re.search(p, test_message, re.IGNORECASE) for p in PreClassifier.GUIDANCE_PATTERNS
        )
        assert matches_guidance

    def test_what_can_you_do_still_routes_to_discovery(self):
        """Regression: 'what can you do?' still routes to DISCOVERY."""
        from services.intent_service.pre_classifier import PreClassifier

        test_message = "what can you do"
        matches_discovery = any(
            re.search(p, test_message, re.IGNORECASE) for p in PreClassifier.DISCOVERY_PATTERNS
        )
        assert matches_discovery


class TestIntegrationSetupContinuity:
    """Issue #814: Integration setup response includes continuity language (Option B)."""

    @pytest.mark.asyncio
    async def test_integration_guidance_has_continuity(self, canonical_handlers):
        """Integration setup guidance includes connection-testing offer.
        (#1547: async + canonical status service.)"""
        from unittest.mock import AsyncMock, patch

        with patch(
            "services.integrations.integration_status_service." "IntegrationStatusService.get_all",
            new=AsyncMock(return_value={}),
        ):
            result = await canonical_handlers._format_integration_setup_guidance(
                user_id="test-user"
            )
        assert "test the connection" in result["message"].lower()


class TestGreetingOnboardingRegression:
    """Issue #814, #888: Greeting-triggered onboarding uses offer-first model."""

    @pytest.mark.asyncio
    async def test_greeting_offers_onboarding_for_zero_projects(self):
        """
        Greeting-based onboarding via ConversationHandler offers (not auto-activates).

        Issue #888: Changed from start_onboarding() to offer_onboarding().
        Session is created in OFFERED state — user must explicitly accept.
        """
        from services.conversation.conversation_handler import ConversationHandler

        handler = ConversationHandler()

        mock_response = MagicMock()
        mock_response.message = (
            "Hey! I'm Piper, your PM assistant. I notice you're new here. "
            "I can walk you through setting up your workspace — want to do "
            "that now, or would you rather just dive in?"
        )
        mock_response.state = MagicMock()
        mock_response.state.value = "offered"
        mock_response.metadata = {"onboarding_id": "onb-456"}

        mock_onboarding_handler = MagicMock()
        mock_onboarding_handler.offer_onboarding.return_value = mock_response

        mock_project_repo = MagicMock()
        mock_project_repo.count_active_projects = AsyncMock(return_value=0)

        with (
            patch(
                "services.conversation.conversation_handler._get_onboarding_components",
                return_value=(MagicMock(), mock_onboarding_handler),
            ),
            patch(
                "services.database.session_factory.AsyncSessionFactory.session_scope",
            ) as mock_scope,
            patch(
                "services.database.repositories.ProjectRepository",
                return_value=mock_project_repo,
            ),
            patch(
                "services.onboarding.first_meeting_detector.FirstMeetingDetector.should_trigger",
                new_callable=AsyncMock,
                return_value=True,
            ),
        ):
            mock_scope.return_value.__aenter__ = AsyncMock()
            mock_scope.return_value.__aexit__ = AsyncMock()

            result = await handler._check_portfolio_onboarding("user-1", "sess-1")

        assert result is not None
        assert result["intent"]["action"] == "portfolio_onboarding_offered"
        assert result["onboarding_session"] == "onb-456"
        assert result["intent"]["context"]["offer_pending"] is True
        mock_onboarding_handler.offer_onboarding.assert_called_once_with("sess-1", "user-1")
