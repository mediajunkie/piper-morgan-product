"""
Tests for process adapters (ADR-049: Two-Tier Intent Architecture).

These tests verify that the adapters correctly wrap the existing
onboarding and standup managers.

Issue #427: MUX-IMPLEMENT-CONVERSE-MODEL
Issue #687: ADR-049 Implementation

Issue #1053 (May 7, 2026): TestStandupProcessAdapter migrated to async +
FakeStandupConversationManager. After #1052 Phase 2 rewrote the production
manager to be async + repository-backed, the adapter's calls to
manager.get_conversation_by_session / transition_state / get_suspended_for_user
are awaited. The Fake mirrors the async API in-memory; tests use it instead
of MagicMock for the manager-shaped argument.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.process.adapters import (
    OnboardingProcessAdapter,
    StandupProcessAdapter,
    register_default_processes,
)
from services.process.registry import GuidedProcess, ProcessCheckResult, ProcessType
from services.shared_types import StandupConversationState
from tests.unit.services.standup._fake_conversation_manager import (
    FakeStandupConversationManager,
)


@pytest.mark.skip(reason="ADR-059: onboarding on ice")
class TestOnboardingProcessAdapter:
    """Tests for OnboardingProcessAdapter."""

    def test_implements_protocol(self):
        """Adapter implements GuidedProcess protocol."""
        adapter = OnboardingProcessAdapter()
        assert isinstance(adapter, GuidedProcess)

    def test_process_type(self):
        """Returns ONBOARDING process type."""
        adapter = OnboardingProcessAdapter()
        assert adapter.process_type == ProcessType.ONBOARDING

    @pytest.mark.asyncio
    async def test_check_active_no_session(self):
        """Returns False when no active session."""
        adapter = OnboardingProcessAdapter()

        mock_manager = MagicMock()
        mock_manager.get_session_by_user.return_value = None
        mock_manager.get_session_by_session_id.return_value = None

        with patch.object(adapter, "_get_components", return_value=(mock_manager, None)):
            result = await adapter.check_active("user1", "session1")

        assert result is False

    @pytest.mark.asyncio
    async def test_check_active_terminal_state(self):
        """Returns False for terminal state sessions."""
        from services.shared_types import PortfolioOnboardingState

        adapter = OnboardingProcessAdapter()

        mock_session = MagicMock()
        mock_session.state = PortfolioOnboardingState.COMPLETE

        mock_manager = MagicMock()
        mock_manager.get_session_by_user.return_value = mock_session

        with patch.object(adapter, "_get_components", return_value=(mock_manager, None)):
            result = await adapter.check_active("user1", "session1")

        assert result is False

    @pytest.mark.asyncio
    async def test_check_active_active_session(self):
        """Returns True for active session."""
        from services.shared_types import PortfolioOnboardingState

        adapter = OnboardingProcessAdapter()

        mock_session = MagicMock()
        mock_session.state = PortfolioOnboardingState.GATHERING_PROJECTS

        mock_manager = MagicMock()
        mock_manager.get_session_by_user.return_value = mock_session

        with patch.object(adapter, "_get_components", return_value=(mock_manager, None)):
            result = await adapter.check_active("user1", "session1")

        assert result is True

    @pytest.mark.asyncio
    async def test_check_active_fallback_to_session_id(self):
        """Falls back to session_id when user_id lookup fails."""
        from services.shared_types import PortfolioOnboardingState

        adapter = OnboardingProcessAdapter()

        mock_session = MagicMock()
        mock_session.state = PortfolioOnboardingState.GATHERING_PROJECTS

        mock_manager = MagicMock()
        mock_manager.get_session_by_user.return_value = None
        mock_manager.get_session_by_session_id.return_value = mock_session

        with patch.object(adapter, "_get_components", return_value=(mock_manager, None)):
            result = await adapter.check_active("user1", "session1")

        assert result is True
        mock_manager.get_session_by_session_id.assert_called_once_with("session1")

    @pytest.mark.asyncio
    async def test_handle_message_returns_result(self):
        """handle_message returns ProcessCheckResult with response."""
        from services.shared_types import PortfolioOnboardingState

        adapter = OnboardingProcessAdapter()

        mock_session = MagicMock()
        mock_session.id = "onboard-123"
        mock_session.state = PortfolioOnboardingState.GATHERING_PROJECTS

        mock_response = MagicMock()
        mock_response.message = "Tell me about your project"
        mock_response.state = PortfolioOnboardingState.GATHERING_PROJECTS

        mock_manager = MagicMock()
        mock_manager.get_session_by_user.return_value = mock_session

        mock_handler = MagicMock()
        mock_handler.handle_turn.return_value = mock_response

        with patch.object(adapter, "_get_components", return_value=(mock_manager, mock_handler)):
            result = await adapter.handle_message("user1", "session1", "My project is Piper")

        assert result.handled is True
        assert result.process_type == ProcessType.ONBOARDING
        assert result.response_message == "Tell me about your project"
        assert result.intent_data["action"] == "portfolio_onboarding"
        assert result.intent_data["context"]["bypassed_classification"] is True


class TestStandupProcessAdapter:
    """Tests for StandupProcessAdapter."""

    def test_implements_protocol(self):
        """Adapter implements GuidedProcess protocol."""
        adapter = StandupProcessAdapter()
        assert isinstance(adapter, GuidedProcess)

    def test_process_type(self):
        """Returns STANDUP process type."""
        adapter = StandupProcessAdapter()
        assert adapter.process_type == ProcessType.STANDUP

    @pytest.mark.asyncio
    async def test_check_active_no_conversation(self):
        """Returns False when no active conversation."""
        adapter = StandupProcessAdapter()

        # Fake with no conversations registered → get_conversation_by_session returns None
        manager = FakeStandupConversationManager()

        with patch.object(adapter, "_get_components", return_value=(manager, None)):
            result = await adapter.check_active("user1", "session1")

        assert result is False

    @pytest.mark.asyncio
    async def test_check_active_terminal_state(self):
        """Returns False for terminal state conversations."""
        adapter = StandupProcessAdapter()

        # Fake with a COMPLETE conv on session1 → default lookup excludes terminal
        manager = FakeStandupConversationManager()
        conv = await manager.create_conversation("session1", "user1")
        await manager.transition_state(conv.id, StandupConversationState.GENERATING)
        await manager.transition_state(conv.id, StandupConversationState.FINALIZING)
        await manager.transition_state(conv.id, StandupConversationState.COMPLETE)

        with patch.object(adapter, "_get_components", return_value=(manager, None)):
            result = await adapter.check_active("user1", "session1")

        assert result is False

    @pytest.mark.asyncio
    async def test_check_active_active_conversation(self):
        """Returns True for active conversation."""
        adapter = StandupProcessAdapter()

        # Fake with a non-terminal conv on session1 → default lookup returns it
        manager = FakeStandupConversationManager()
        conv = await manager.create_conversation("session1", "user1")
        await manager.transition_state(conv.id, StandupConversationState.GENERATING)

        with patch.object(adapter, "_get_components", return_value=(manager, None)):
            result = await adapter.check_active("user1", "session1")

        assert result is True

    @pytest.mark.asyncio
    async def test_handle_message_returns_result(self):
        """handle_message returns ProcessCheckResult with response."""
        adapter = StandupProcessAdapter()

        # Fake with an active conv that handle_turn will operate on
        manager = FakeStandupConversationManager()
        conv = await manager.create_conversation("session1", "user1")
        await manager.transition_state(conv.id, StandupConversationState.GENERATING)

        mock_response = MagicMock()
        mock_response.message = "Here's your standup..."
        mock_response.state = StandupConversationState.GENERATING

        mock_handler = AsyncMock()
        mock_handler.handle_turn.return_value = mock_response

        with patch.object(adapter, "_get_components", return_value=(manager, mock_handler)):
            result = await adapter.handle_message("user1", "session1", "Make it shorter")

        assert result.handled is True
        assert result.process_type == ProcessType.STANDUP
        assert result.response_message == "Here's your standup..."
        assert result.intent_data["action"] == "standup_conversation_turn"
        assert result.intent_data["context"]["bypassed_classification"] is True


class TestRegisterDefaultProcesses:
    """Tests for register_default_processes."""

    def test_registers_standup_process(self):
        """ADR-059: Only standup registered (onboarding on ice)."""
        from services.process.registry import ProcessRegistry

        # Reset singleton
        ProcessRegistry.reset_instance()

        try:
            # Mock the components to avoid importing actual managers
            with patch(
                "services.process.adapters.StandupProcessAdapter._get_components",
                return_value=(MagicMock(), MagicMock()),
            ):
                register_default_processes()

            from services.process import get_process_registry

            registry = get_process_registry()

            # ADR-059: Onboarding no longer registered
            assert ProcessType.ONBOARDING not in registry.registered_types
            assert ProcessType.STANDUP in registry.registered_types
        finally:
            ProcessRegistry.reset_instance()
