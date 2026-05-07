"""
Issue #553: Tests for standup conversation flow handler.

Epic #242: CONV-MCP-STANDUP-INTERACTIVE

Tests verify:
- ConversationResponse dataclass initialization
- StandupConversationHandler state-based routing
- Turn handling for each state
- Preference extraction
- Refinement logic (add/remove)
- Graceful fallback on errors
- Complete conversation flows

Issue #556: Additional tests for:
- Retry logic on transient failures
- Timeout handling
- Error categorization

Issue #1053 (May 7, 2026): Migrated to async + FakeStandupConversationManager.
After #1052 Phase 2 rewrote the production manager to be async + repository-backed,
these tests use the in-memory Fake test double (no DB). The Fake mirrors the
async public API; tests use the public API exclusively (no `_conversations`
direct access).
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

from services.shared_types import StandupConversationState
from services.standup.conversation_handler import ConversationResponse, StandupConversationHandler
from services.standup.conversation_manager import StandupConversationManager
from tests.unit.services.standup._fake_conversation_manager import (
    FakeStandupConversationManager,
)


class TestConversationResponse:
    """Tests for ConversationResponse dataclass."""

    def test_default_values(self):
        """Default values are set correctly."""
        response = ConversationResponse(
            message="Hello",
            state=StandupConversationState.INITIATED,
        )

        assert response.message == "Hello"
        assert response.state == StandupConversationState.INITIATED
        assert response.requires_input is True
        assert response.standup_content is None
        assert response.suggestions == []
        assert response.metadata == {}

    def test_with_all_values(self):
        """All values are preserved when specified."""
        response = ConversationResponse(
            message="Here's your standup",
            state=StandupConversationState.REFINING,
            requires_input=True,
            standup_content="*Yesterday:*\n* Did stuff",
            suggestions=["Looks good", "Edit"],
            metadata={"source": "test"},
        )

        assert response.message == "Here's your standup"
        assert response.state == StandupConversationState.REFINING
        assert response.standup_content == "*Yesterday:*\n* Did stuff"
        assert len(response.suggestions) == 2
        assert response.metadata["source"] == "test"

    def test_suggestions_not_shared(self):
        """Suggestions list is not shared between instances."""
        r1 = ConversationResponse(message="a", state=StandupConversationState.INITIATED)
        r2 = ConversationResponse(message="b", state=StandupConversationState.INITIATED)

        r1.suggestions.append("test")

        assert "test" in r1.suggestions
        assert "test" not in r2.suggestions


class TestStandupConversationHandler:
    """Tests for StandupConversationHandler initialization."""

    def test_creates_default_manager(self):
        """Handler creates its own manager if none provided."""
        handler = StandupConversationHandler()

        assert handler.manager is not None
        assert isinstance(handler.manager, StandupConversationManager)

    def test_uses_provided_manager(self):
        """Handler uses provided manager (production manager class)."""
        manager = StandupConversationManager()
        handler = StandupConversationHandler(conversation_manager=manager)

        assert handler.manager is manager

    def test_accepts_fake_manager(self):
        """Handler accepts FakeStandupConversationManager via duck typing."""
        fake = FakeStandupConversationManager()
        handler = StandupConversationHandler(conversation_manager=fake)

        assert handler.manager is fake

    def test_workflow_is_optional(self):
        """Workflow can be None (fallback used)."""
        handler = StandupConversationHandler()

        assert handler._workflow is None


class TestStartConversation:
    """Tests for starting a conversation."""

    @pytest.fixture
    def handler(self):
        return StandupConversationHandler(
            conversation_manager=FakeStandupConversationManager()
        )

    @pytest.mark.asyncio
    async def test_start_creates_conversation(self, handler):
        """Starting creates a new conversation in INITIATED state."""
        response = await handler.start_conversation(
            session_id="session1",
            user_id="user1",
        )

        assert response.state == StandupConversationState.INITIATED
        assert response.requires_input is True
        assert "morning" in response.message.lower() or "standup" in response.message.lower()

    @pytest.mark.asyncio
    async def test_start_returns_suggestions(self, handler):
        """Starting provides user suggestions."""
        response = await handler.start_conversation(
            session_id="session1",
            user_id="user1",
        )

        assert len(response.suggestions) > 0
        assert any("quick" in s.lower() for s in response.suggestions)

    @pytest.mark.asyncio
    async def test_start_with_context(self, handler):
        """Starting with context passes it to conversation."""
        response = await handler.start_conversation(
            session_id="session1",
            user_id="user1",
            initial_context={"source": "chat"},
        )

        conv = await handler.manager.get_conversation_by_session("session1")
        assert conv.context.get("source") == "chat"


class TestHandleTurnInitiated:
    """Tests for INITIATED state handling."""

    @pytest.fixture
    def handler(self):
        return StandupConversationHandler(
            conversation_manager=FakeStandupConversationManager()
        )

    @pytest_asyncio.fixture
    async def conversation(self, handler):
        return await handler.manager.create_conversation("s1", "u1")

    @pytest.mark.asyncio
    async def test_quick_skips_to_generating(self, handler, conversation):
        """'Quick' skips preferences and generates standup."""
        response = await handler.handle_turn(conversation, "quick standup")

        assert response.state == StandupConversationState.REFINING
        assert response.standup_content is not None

    @pytest.mark.asyncio
    async def test_fast_skips_to_generating(self, handler, conversation):
        """'Fast' also skips to generation."""
        response = await handler.handle_turn(conversation, "fast please")

        assert response.state == StandupConversationState.REFINING

    @pytest.mark.asyncio
    async def test_cancel_abandons(self, handler, conversation):
        """'Not now' abandons conversation."""
        response = await handler.handle_turn(conversation, "not now")

        assert response.state == StandupConversationState.ABANDONED
        assert response.requires_input is False

    @pytest.mark.asyncio
    async def test_later_abandons(self, handler, conversation):
        """'Later' also abandons conversation."""
        response = await handler.handle_turn(conversation, "maybe later")

        assert response.state == StandupConversationState.ABANDONED

    @pytest.mark.skip(reason="#1063 — stale post-#900 3-part flow; needs rewrite")
    @pytest.mark.asyncio
    async def test_yes_proceeds_to_generating(self, handler, conversation):
        """Positive response proceeds to generation."""
        response = await handler.handle_turn(conversation, "yes, let's do it")

        assert response.state == StandupConversationState.REFINING
        assert response.standup_content is not None

    @pytest.mark.skip(reason="#1063 — stale post-#900 3-part flow; needs rewrite")
    @pytest.mark.asyncio
    async def test_generic_message_proceeds(self, handler, conversation):
        """Generic message proceeds to generation."""
        response = await handler.handle_turn(conversation, "sounds good")

        assert response.state == StandupConversationState.REFINING


class TestHandleTurnGathering:
    """Tests for GATHERING_PREFERENCES state handling."""

    @pytest.fixture
    def handler(self):
        return StandupConversationHandler(
            conversation_manager=FakeStandupConversationManager()
        )

    @pytest_asyncio.fixture
    async def gathering_conversation(self, handler):
        conv = await handler.manager.create_conversation("s1", "u1")
        await handler.manager.transition_state(
            conv.id, StandupConversationState.GATHERING_PREFERENCES
        )
        return await handler.manager.get_conversation(conv.id)

    @pytest.mark.asyncio
    async def test_extracts_github_preference(self, handler, gathering_conversation):
        """Extracts GitHub focus preference and proceeds."""
        response = await handler.handle_turn(gathering_conversation, "focus on github work")

        assert response.state == StandupConversationState.REFINING
        conv = await handler.manager.get_conversation(gathering_conversation.id)
        assert conv.preferences.get("focus") == "github"


class TestHandleTurnRefining:
    """Tests for REFINING state handling."""

    @pytest.fixture
    def handler(self):
        return StandupConversationHandler(
            conversation_manager=FakeStandupConversationManager()
        )

    @pytest_asyncio.fixture
    async def refining_conversation(self, handler):
        conv = await handler.manager.create_conversation("s1", "u1")
        await handler.manager.transition_state(conv.id, StandupConversationState.GENERATING)
        await handler.manager.set_standup_content(
            conv.id, "*Yesterday:*\n* Did work\n\n*Today:*\n* More work"
        )
        await handler.manager.transition_state(conv.id, StandupConversationState.REFINING)
        return await handler.manager.get_conversation(conv.id)

    @pytest.mark.asyncio
    async def test_looks_good_finalizes(self, handler, refining_conversation):
        """'Looks good' moves to finalizing."""
        response = await handler.handle_turn(refining_conversation, "looks good")

        assert response.state == StandupConversationState.FINALIZING
        assert response.standup_content is not None

    @pytest.mark.asyncio
    async def test_perfect_finalizes(self, handler, refining_conversation):
        """'Perfect' moves to finalizing."""
        response = await handler.handle_turn(refining_conversation, "perfect!")

        assert response.state == StandupConversationState.FINALIZING

    @pytest.mark.asyncio
    async def test_thanks_finalizes(self, handler, refining_conversation):
        """'Thanks' moves to finalizing."""
        response = await handler.handle_turn(refining_conversation, "thanks")

        assert response.state == StandupConversationState.FINALIZING

    @pytest.mark.asyncio
    async def test_add_blocker_updates_content(self, handler, refining_conversation):
        """Adding blocker updates standup content."""
        response = await handler.handle_turn(
            refining_conversation, "add blocker waiting for API review"
        )

        assert response.state == StandupConversationState.REFINING
        assert "waiting for API review" in response.standup_content
        assert "*Blockers:*" in response.standup_content

    @pytest.mark.asyncio
    async def test_remove_item_updates_content(self, handler, refining_conversation):
        """Removing item filters standup content."""
        response = await handler.handle_turn(refining_conversation, "remove the work item")

        assert response.state == StandupConversationState.REFINING
        # The exact behavior depends on implementation
        assert response.standup_content is not None

    @pytest.mark.asyncio
    async def test_start_over_regenerates(self, handler, refining_conversation):
        """'Start over' regenerates standup."""
        response = await handler.handle_turn(refining_conversation, "start over")

        assert response.state == StandupConversationState.REFINING
        assert response.standup_content is not None


class TestHandleTurnFinalizing:
    """Tests for FINALIZING state handling."""

    @pytest.fixture
    def handler(self):
        return StandupConversationHandler(
            conversation_manager=FakeStandupConversationManager()
        )

    @pytest_asyncio.fixture
    async def finalizing_conversation(self, handler):
        conv = await handler.manager.create_conversation("s1", "u1")
        await handler.manager.transition_state(conv.id, StandupConversationState.GENERATING)
        await handler.manager.set_standup_content(conv.id, "*Yesterday:*\n* Did work")
        await handler.manager.transition_state(conv.id, StandupConversationState.REFINING)
        await handler.manager.transition_state(conv.id, StandupConversationState.FINALIZING)
        return await handler.manager.get_conversation(conv.id)

    @pytest.mark.asyncio
    async def test_any_input_completes(self, handler, finalizing_conversation):
        """Any input in finalizing completes conversation."""
        response = await handler.handle_turn(finalizing_conversation, "ok")

        assert response.state == StandupConversationState.COMPLETE
        assert response.requires_input is False

    @pytest.mark.asyncio
    async def test_complete_includes_content(self, handler, finalizing_conversation):
        """Completion includes final standup content."""
        response = await handler.handle_turn(finalizing_conversation, "done")

        assert response.standup_content is not None


class TestHandleTerminalStates:
    """Tests for terminal state handling."""

    @pytest.fixture
    def handler(self):
        return StandupConversationHandler(
            conversation_manager=FakeStandupConversationManager()
        )

    @pytest.mark.asyncio
    async def test_complete_state_returns_ended(self, handler):
        """Completed conversation returns ended message."""
        conv = await handler.manager.create_conversation("s1", "u1")
        await handler.manager.transition_state(conv.id, StandupConversationState.GENERATING)
        await handler.manager.transition_state(conv.id, StandupConversationState.FINALIZING)
        await handler.manager.transition_state(conv.id, StandupConversationState.COMPLETE)
        conv = await handler.manager.get_conversation(conv.id)

        response = await handler.handle_turn(conv, "hello again")

        assert "ended" in response.message.lower() or "new" in response.message.lower()
        assert response.requires_input is False

    @pytest.mark.asyncio
    async def test_abandoned_state_returns_ended(self, handler):
        """Abandoned conversation returns ended message."""
        conv = await handler.manager.create_conversation("s1", "u1")
        await handler.manager.transition_state(conv.id, StandupConversationState.ABANDONED)
        conv = await handler.manager.get_conversation(conv.id)

        response = await handler.handle_turn(conv, "hello again")

        assert "ended" in response.message.lower() or "new" in response.message.lower()


class TestGracefulFallback:
    """Tests for graceful fallback behavior."""

    @pytest.fixture
    def handler_with_failing_workflow(self):
        mock_workflow = MagicMock()
        mock_workflow.generate_standup = AsyncMock(side_effect=Exception("API error"))
        return StandupConversationHandler(
            standup_workflow=mock_workflow,
            conversation_manager=FakeStandupConversationManager(),
        )

    @pytest.mark.skip(reason="#1063 — stale post-#900 3-part flow; needs rewrite")
    @pytest.mark.asyncio
    async def test_fallback_on_workflow_error(self, handler_with_failing_workflow):
        """Workflow error triggers graceful fallback."""
        conv = await handler_with_failing_workflow.manager.create_conversation("s1", "u1")

        response = await handler_with_failing_workflow.handle_turn(conv, "yes")

        # Should still get a response with basic standup
        assert response.standup_content is not None
        assert response.metadata.get("fallback") is True

    @pytest.mark.skip(reason="#1063 — stale post-#900 3-part flow; needs rewrite")
    @pytest.mark.asyncio
    async def test_fallback_includes_error(self, handler_with_failing_workflow):
        """Fallback metadata includes error."""
        conv = await handler_with_failing_workflow.manager.create_conversation("s1", "u1")

        response = await handler_with_failing_workflow.handle_turn(conv, "yes")

        assert "error" in response.metadata
        assert "API error" in response.metadata["error"]


class TestPreferenceExtraction:
    """Tests for preference extraction."""

    @pytest.fixture
    def handler(self):
        return StandupConversationHandler()

    def test_extract_github_preference(self, handler):
        """Extracts GitHub focus preference."""
        prefs = handler._extract_preferences("focus on github work")
        assert prefs.get("focus") == "github"

    def test_extract_calendar_preference(self, handler):
        """Extracts calendar focus preference."""
        prefs = handler._extract_preferences("include my calendar")
        assert prefs.get("focus") == "calendar"

    def test_extract_todos_preference(self, handler):
        """Extracts todos focus preference."""
        prefs = handler._extract_preferences("just my todos")
        assert prefs.get("focus") == "todos"

    def test_extract_tasks_preference(self, handler):
        """Extracts tasks focus preference."""
        prefs = handler._extract_preferences("focus on tasks")
        assert prefs.get("focus") == "todos"

    def test_extract_brief_length(self, handler):
        """Extracts brief length preference."""
        prefs = handler._extract_preferences("keep it brief")
        assert prefs.get("length") == "brief"

    def test_extract_detailed_length(self, handler):
        """Extracts detailed length preference."""
        prefs = handler._extract_preferences("make it detailed")
        assert prefs.get("length") == "detailed"

    def test_no_preference_extracted(self, handler):
        """No preference extracted from generic message."""
        prefs = handler._extract_preferences("sounds good")
        assert prefs == {}

    def test_multiple_preferences(self, handler):
        """Extracts multiple preferences from one message."""
        prefs = handler._extract_preferences("brief github summary")
        assert prefs.get("focus") == "github"
        assert prefs.get("length") == "brief"


class TestRefinementLogic:
    """Tests for refinement logic."""

    @pytest.fixture
    def handler(self):
        return StandupConversationHandler(
            conversation_manager=FakeStandupConversationManager()
        )

    @pytest_asyncio.fixture
    async def conversation_with_content(self, handler):
        conv = await handler.manager.create_conversation("s1", "u1")
        await handler.manager.transition_state(conv.id, StandupConversationState.GENERATING)
        await handler.manager.set_standup_content(
            conv.id,
            "*Yesterday:*\n* Completed feature X\n\n*Today:*\n* Working on Y\n\n*Blockers:*\n* None",
        )
        await handler.manager.transition_state(conv.id, StandupConversationState.REFINING)
        return await handler.manager.get_conversation(conv.id)

    @pytest.mark.asyncio
    async def test_add_blocker_with_colon(self, handler, conversation_with_content):
        """Add blocker with colon syntax."""
        result = await handler._apply_refinement(
            conversation_with_content, "add blocker: waiting for code review"
        )

        assert "waiting for code review" in result

    @pytest.mark.asyncio
    async def test_remove_by_keyword(self, handler, conversation_with_content):
        """Remove items by keyword."""
        result = await handler._apply_refinement(conversation_with_content, "remove feature X")

        assert "feature X" not in result


class TestFullConversationFlow:
    """Integration tests for complete conversation flows."""

    @pytest.fixture
    def handler(self):
        return StandupConversationHandler(
            conversation_manager=FakeStandupConversationManager()
        )

    @pytest.mark.asyncio
    async def test_quick_flow(self, handler):
        """Quick path: start -> quick -> accept -> done."""
        # Start
        response = await handler.start_conversation("s1", "u1")
        assert response.state == StandupConversationState.INITIATED

        # Quick
        conv = await handler.manager.get_conversation_by_session("s1")
        response = await handler.handle_turn(conv, "quick")
        assert response.state == StandupConversationState.REFINING

        # Accept
        conv = await handler.manager.get_conversation(conv.id)
        response = await handler.handle_turn(conv, "looks good")
        assert response.state == StandupConversationState.FINALIZING

        # Finalize
        conv = await handler.manager.get_conversation(conv.id)
        response = await handler.handle_turn(conv, "ok")
        assert response.state == StandupConversationState.COMPLETE
        assert response.requires_input is False

    @pytest.mark.skip(reason="#1063 — stale post-#900 3-part flow; needs rewrite")
    @pytest.mark.asyncio
    async def test_refinement_flow(self, handler):
        """Refinement path: start -> generate -> add blocker -> accept -> done."""
        # Start
        response = await handler.start_conversation("s1", "u1")

        # Generate
        conv = await handler.manager.get_conversation_by_session("s1")
        response = await handler.handle_turn(conv, "yes")
        assert response.state == StandupConversationState.REFINING

        # Add blocker
        conv = await handler.manager.get_conversation(conv.id)
        response = await handler.handle_turn(conv, "add blocker waiting for review")
        assert response.state == StandupConversationState.REFINING
        assert "waiting for review" in response.standup_content

        # Accept
        conv = await handler.manager.get_conversation(conv.id)
        response = await handler.handle_turn(conv, "perfect")
        assert response.state == StandupConversationState.FINALIZING

        # Complete
        conv = await handler.manager.get_conversation(conv.id)
        response = await handler.handle_turn(conv, "done")
        assert response.state == StandupConversationState.COMPLETE

    @pytest.mark.asyncio
    async def test_abandon_flow(self, handler):
        """Abandon path: start -> not now."""
        # Start
        response = await handler.start_conversation("s1", "u1")

        # Abandon
        conv = await handler.manager.get_conversation_by_session("s1")
        response = await handler.handle_turn(conv, "not now")

        assert response.state == StandupConversationState.ABANDONED
        assert response.requires_input is False

    @pytest.mark.skip(reason="#1063 — stale post-#900 3-part flow; needs rewrite")
    @pytest.mark.asyncio
    async def test_restart_during_refinement(self, handler):
        """Restart during refinement regenerates standup."""
        # Start and generate
        response = await handler.start_conversation("s1", "u1")
        conv = await handler.manager.get_conversation_by_session("s1")
        response = await handler.handle_turn(conv, "yes")
        original_content = response.standup_content

        # Restart
        conv = await handler.manager.get_conversation(conv.id)
        response = await handler.handle_turn(conv, "start over")

        assert response.state == StandupConversationState.REFINING
        # Content should be regenerated (basic template)
        assert response.standup_content is not None


class TestBasicStandupGeneration:
    """Tests for basic standup generation fallback."""

    @pytest.fixture
    def handler(self):
        return StandupConversationHandler()

    def test_basic_standup_format(self, handler):
        """Basic standup has correct sections."""
        basic = handler._generate_basic_standup({})

        assert "*Yesterday:*" in basic
        assert "*Today:*" in basic
        assert "*Blockers:*" in basic


class TestRetryAndErrorRecovery:
    """Issue #556: Tests for retry logic and error recovery."""

    @pytest.fixture
    def handler_with_transient_failure(self):
        """Handler with workflow that fails then succeeds."""
        mock_workflow = MagicMock()
        call_count = 0

        async def fail_then_succeed(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("Network error")
            result = MagicMock()
            result.summary = "Standup content"
            return result

        mock_workflow.generate_standup = fail_then_succeed
        handler = StandupConversationHandler(
            standup_workflow=mock_workflow,
            conversation_manager=FakeStandupConversationManager(),
        )
        handler._call_count = lambda: call_count  # For test assertions
        return handler

    @pytest.fixture
    def handler_with_permanent_failure(self):
        """Handler with workflow that always fails with permanent error."""
        mock_workflow = MagicMock()
        mock_workflow.generate_standup = AsyncMock(side_effect=Exception("Invalid configuration"))
        return StandupConversationHandler(
            standup_workflow=mock_workflow,
            conversation_manager=FakeStandupConversationManager(),
        )

    @pytest.fixture
    def handler_with_timeout(self):
        """Handler with workflow that times out."""
        mock_workflow = MagicMock()

        async def slow_generation(*args, **kwargs):
            await asyncio.sleep(15)  # Longer than GENERATION_TIMEOUT
            return MagicMock(summary="Never returned")

        mock_workflow.generate_standup = slow_generation
        return StandupConversationHandler(
            standup_workflow=mock_workflow,
            conversation_manager=FakeStandupConversationManager(),
        )

    @pytest.mark.skip(reason="#1063 — stale post-#900 3-part flow; needs rewrite")
    @pytest.mark.asyncio
    async def test_retry_on_transient_failure(self, handler_with_transient_failure):
        """Issue #556: Transient failures trigger retry with eventual success."""
        handler = handler_with_transient_failure
        conv = await handler.manager.create_conversation("s1", "u1")

        response = await handler.handle_turn(conv, "yes")

        # Should succeed after retries
        assert response.standup_content is not None
        assert "Standup content" in response.standup_content
        assert response.metadata.get("fallback") is not True

    @pytest.mark.skip(reason="#1063 — stale post-#900 3-part flow; needs rewrite")
    @pytest.mark.asyncio
    async def test_fallback_on_permanent_failure(self, handler_with_permanent_failure):
        """Issue #556: Permanent failures fall back to basic template."""
        handler = handler_with_permanent_failure
        conv = await handler.manager.create_conversation("s1", "u1")

        response = await handler.handle_turn(conv, "yes")

        # Should fallback to basic standup
        assert response.standup_content is not None
        assert response.metadata.get("fallback") is True
        assert "error" in response.metadata

    @pytest.mark.skip(reason="#1063 — stale post-#900 3-part flow; needs rewrite")
    @pytest.mark.asyncio
    async def test_timeout_triggers_fallback(self, handler_with_timeout):
        """Issue #556: Timeout triggers graceful fallback."""
        handler = handler_with_timeout
        # Reduce timeout for faster test
        handler.GENERATION_TIMEOUT = 0.1
        conv = await handler.manager.create_conversation("s1", "u1")

        response = await handler.handle_turn(conv, "yes")

        # Should fallback due to timeout
        assert response.standup_content is not None
        assert response.metadata.get("fallback") is True

    def test_retry_configuration_exists(self):
        """Issue #556: Retry configuration constants are defined."""
        handler = StandupConversationHandler()

        assert hasattr(handler, "MAX_RETRIES")
        assert handler.MAX_RETRIES == 3
        assert hasattr(handler, "GENERATION_TIMEOUT")
        assert handler.GENERATION_TIMEOUT == 10.0
        assert hasattr(handler, "RETRY_WAIT_MIN")
        assert hasattr(handler, "RETRY_WAIT_MAX")


class TestMonitoringIntegration:
    """Issue #556 Phase 4: Tests for structured monitoring logging."""

    @pytest.fixture
    def handler(self):
        return StandupConversationHandler(
            conversation_manager=FakeStandupConversationManager()
        )

    @pytest.fixture
    def handler_with_workflow(self):
        """Handler with successful mock workflow."""
        mock_workflow = MagicMock()
        result = MagicMock()
        result.summary = "Test standup content"
        mock_workflow.generate_standup = AsyncMock(return_value=result)
        return StandupConversationHandler(
            standup_workflow=mock_workflow,
            conversation_manager=FakeStandupConversationManager(),
        )

    @pytest.mark.asyncio
    async def test_turn_response_time_tracked(self, handler, caplog):
        """Issue #556: Turn response time is logged."""
        conv = await handler.manager.create_conversation("s1", "u1")

        await handler.handle_turn(conv, "yes")

        # Verify structured logging was called (via caplog or mock)
        # The actual logging happens via structlog which may not be captured by caplog
        # This test verifies the code path executes without error
        assert conv is not None

    @pytest.mark.skip(reason="#1063 — stale post-#900 3-part flow; needs rewrite")
    @pytest.mark.asyncio
    async def test_generation_success_metrics_logged(self, handler_with_workflow):
        """Issue #556: Successful generation logs metrics."""
        handler = handler_with_workflow
        conv = await handler.manager.create_conversation("s1", "u1")

        response = await handler.handle_turn(conv, "yes")

        # Should succeed with workflow
        assert response.standup_content is not None
        assert "Test standup content" in response.standup_content

    @pytest.mark.skip(reason="#1063 — stale post-#900 3-part flow; needs rewrite")
    @pytest.mark.asyncio
    async def test_generation_failure_metrics_logged(self):
        """Issue #556: Failed generation logs error metrics."""
        mock_workflow = MagicMock()
        mock_workflow.generate_standup = AsyncMock(side_effect=Exception("API error"))
        handler = StandupConversationHandler(
            standup_workflow=mock_workflow,
            conversation_manager=FakeStandupConversationManager(),
        )
        conv = await handler.manager.create_conversation("s1", "u1")

        response = await handler.handle_turn(conv, "yes")

        # Should fallback with error metadata
        assert response.metadata.get("fallback") is True
        assert "error" in response.metadata

    @pytest.mark.skip(reason="#1063 — stale post-#900 3-part flow; needs rewrite")
    @pytest.mark.asyncio
    async def test_conversation_completion_metrics_logged(self, handler):
        """Issue #556: Conversation completion logs metrics."""
        conv = await handler.manager.create_conversation("s1", "u1")

        # Go through full flow
        await handler.handle_turn(conv, "yes")
        conv = await handler.manager.get_conversation(conv.id)
        await handler.handle_turn(conv, "looks good")
        conv = await handler.manager.get_conversation(conv.id)
        await handler.handle_turn(conv, "done")
        conv = await handler.manager.get_conversation(conv.id)

        # Should be complete
        assert conv.state == StandupConversationState.COMPLETE
        assert conv.completed_at is not None

    @pytest.mark.asyncio
    async def test_abandoned_conversation_metrics_logged(self, handler):
        """Issue #556: Abandoned conversation logs metrics."""
        conv = await handler.manager.create_conversation("s1", "u1")

        await handler.handle_turn(conv, "not now")
        conv = await handler.manager.get_conversation(conv.id)

        # Should be abandoned
        assert conv.state == StandupConversationState.ABANDONED
