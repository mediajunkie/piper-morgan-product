"""
Integration tests for multi-substantive intent orchestration.

Issue #764: GLUE-MULTIINTENT — Multi-Intent Handling Enhancements
Phase 3: IntentService Integration

Tests verify the full routing path from classify_multiple through
orchestrator to aggregated response. Also verifies no regression
in existing greeting+substantive handling.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.orchestrator import IntentOrchestrator
from services.intent_service.pre_classifier import MultiIntentResult
from services.shared_types import IntentCategory


def _make_intent(category: IntentCategory, action: str) -> Intent:
    """Helper to create test intents."""
    return Intent(category=category, action=action, confidence=1.0)


@pytest.fixture
def mock_engine():
    """Mock OrchestrationEngine."""
    engine = MagicMock()
    return engine


@pytest.fixture
def mock_classifier():
    """Mock IntentClassifier with classify_multiple."""
    classifier = MagicMock()
    classifier.classify_multiple = AsyncMock()
    classifier.classify = AsyncMock()
    return classifier


@pytest.fixture
def mock_canonical_handlers():
    """Mock CanonicalHandlers."""
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
    """IntentService with mocked dependencies."""
    service = IntentService(
        intent_classifier=mock_classifier,
    )
    # Replace real canonical handlers with mock to avoid DB calls
    service.canonical_handlers = mock_canonical_handlers
    service.intent_orchestrator = IntentOrchestrator(canonical_handlers=mock_canonical_handlers)
    return service


class TestMultiSubstantiveRouting:
    """Tests that multi-substantive intents route through orchestrator."""

    @pytest.mark.asyncio
    async def test_two_substantive_intents_orchestrated(self, intent_service, mock_classifier):
        """Two substantive intents → orchestrator path."""
        calendar_intent = _make_intent(IntentCategory.QUERY, "meeting_time")
        status_intent = _make_intent(IntentCategory.STATUS, "get_project_status")

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[calendar_intent, status_intent],
            original_message="Check calendar and sprint status",
            is_multi_intent=True,
        )

        # Mock the orchestrator's execute_plan to return a response
        with patch.object(
            intent_service.intent_orchestrator,
            "execute_plan",
            new_callable=AsyncMock,
        ) as mock_execute:
            from services.intent_service.orchestrator import (
                IntentExecutionResult,
                OrchestratedResponse,
            )

            mock_execute.return_value = OrchestratedResponse(
                results=[
                    IntentExecutionResult(
                        intent=calendar_intent,
                        response="Your next meeting is at 2pm.",
                        intent_data={"category": "query", "action": "meeting_time"},
                        success=True,
                    ),
                    IntentExecutionResult(
                        intent=status_intent,
                        response="Sprint is on track.",
                        intent_data={"category": "status", "action": "get_project_status"},
                        success=True,
                    ),
                ],
                aggregated_message="Your next meeting is at 2pm. As for project status, sprint is on track.",
            )

            result = await intent_service.process_intent(
                message="Check calendar and sprint status",
                session_id="sess1",
                user_id=None,
            )

            assert result.success
            assert result.multi_intent_orchestrated
            assert "2pm" in result.message
            assert "track" in result.message
            mock_execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_three_substantive_intents(self, intent_service, mock_classifier):
        """Three substantive intents all orchestrated."""
        intents = [
            _make_intent(IntentCategory.QUERY, "meeting_time"),
            _make_intent(IntentCategory.STATUS, "get_project_status"),
            _make_intent(IntentCategory.PRIORITY, "get_top_priority"),
        ]

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=intents,
            original_message="Calendar, status, and priorities",
            is_multi_intent=True,
        )

        with patch.object(
            intent_service.intent_orchestrator,
            "execute_plan",
            new_callable=AsyncMock,
        ) as mock_execute:
            from services.intent_service.orchestrator import (
                IntentExecutionResult,
                OrchestratedResponse,
            )

            mock_execute.return_value = OrchestratedResponse(
                results=[
                    IntentExecutionResult(intent=i, response=f"Result for {i.action}", success=True)
                    for i in intents
                ],
                aggregated_message="Result for all three.",
            )

            result = await intent_service.process_intent(
                message="Calendar, status, and priorities",
                session_id="sess1",
                user_id=None,
            )

            assert result.multi_intent_orchestrated
            assert len(result.secondary_intents) == 2

    @pytest.mark.asyncio
    async def test_greeting_plus_two_substantive(self, intent_service, mock_classifier):
        """Greeting + 2 substantive → orchestrator (not greeting-only path)."""
        intents = [
            _make_intent(IntentCategory.CONVERSATION, "greeting"),
            _make_intent(IntentCategory.QUERY, "meeting_time"),
            _make_intent(IntentCategory.STATUS, "get_project_status"),
        ]

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=intents,
            original_message="Hi! Calendar and status please",
            is_multi_intent=True,
        )

        with patch.object(
            intent_service.intent_orchestrator,
            "execute_plan",
            new_callable=AsyncMock,
        ) as mock_execute:
            from services.intent_service.orchestrator import (
                IntentExecutionResult,
                OrchestratedResponse,
            )

            mock_execute.return_value = OrchestratedResponse(
                results=[
                    IntentExecutionResult(intent=i, response=f"Result for {i.action}", success=True)
                    for i in intents
                ],
                aggregated_message="Hi there! Calendar and status results.",
                greeting_prefix=True,
            )

            result = await intent_service.process_intent(
                message="Hi! Calendar and status please",
                session_id="sess1",
                user_id=None,
            )

            assert result.multi_intent_orchestrated
            assert result.multi_intent_greeting


class TestGreetingSubstantivePreserved:
    """Verify existing greeting+single-substantive handling is NOT broken."""

    @pytest.mark.asyncio
    async def test_greeting_plus_one_substantive_not_orchestrated(
        self, intent_service, mock_classifier
    ):
        """Greeting + 1 substantive → existing path (NOT orchestrator)."""
        intents = [
            _make_intent(IntentCategory.CONVERSATION, "greeting"),
            _make_intent(IntentCategory.QUERY, "meeting_time"),
        ]

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=intents,
            original_message="Hi! What's on my agenda?",
            is_multi_intent=True,
        )

        # The existing greeting+substantive path sets context flags
        # and continues to canonical handler. We test that orchestrator
        # is NOT called.
        with patch.object(
            intent_service.intent_orchestrator,
            "execute_plan",
            new_callable=AsyncMock,
        ) as mock_execute:
            # Set up canonical handler for this specific test
            mock_canonical_handlers = intent_service.canonical_handlers
            mock_canonical_handlers.handle.return_value = {
                "message": "Your next meeting is at 2pm.",
                "intent": {"category": "query", "action": "meeting_time"},
            }

            result = await intent_service.process_intent(
                message="Hi! What's on my agenda?",
                session_id="sess1",
                user_id=None,
            )

            # Orchestrator should NOT have been called
            mock_execute.assert_not_called()
            # Should have greeting prefix from existing path
            assert result.multi_intent_greeting
            assert not result.multi_intent_orchestrated
            assert "Hi there!" in result.message


class TestSingleIntentPreserved:
    """Verify single-intent flow is unchanged."""

    @pytest.mark.asyncio
    async def test_single_intent_not_orchestrated(self, intent_service, mock_classifier):
        """Single intent → existing canonical path."""
        intent = _make_intent(IntentCategory.QUERY, "meeting_time")

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="What's on my calendar?",
            is_multi_intent=False,
        )

        with patch.object(
            intent_service.intent_orchestrator,
            "execute_plan",
            new_callable=AsyncMock,
        ) as mock_execute:
            intent_service.canonical_handlers.handle.return_value = {
                "message": "Your next meeting is at 2pm.",
                "intent": {"category": "query", "action": "meeting_time"},
            }

            result = await intent_service.process_intent(
                message="What's on my calendar?",
                session_id="sess1",
                user_id=None,
            )

            mock_execute.assert_not_called()
            assert not result.multi_intent_orchestrated


class TestOrchestrationFallback:
    """Verify graceful fallback when orchestration fails."""

    @pytest.mark.asyncio
    async def test_orchestration_failure_falls_back(self, intent_service, mock_classifier):
        """Orchestration failure → process primary intent only."""
        intents = [
            _make_intent(IntentCategory.QUERY, "meeting_time"),
            _make_intent(IntentCategory.STATUS, "get_project_status"),
        ]

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=intents,
            original_message="Calendar and status",
            is_multi_intent=True,
        )

        with patch.object(
            intent_service.intent_orchestrator,
            "execute_plan",
            new_callable=AsyncMock,
            side_effect=RuntimeError("Orchestration failed"),
        ):
            intent_service.canonical_handlers.handle.return_value = {
                "message": "Your next meeting is at 2pm.",
                "intent": {"category": "query", "action": "meeting_time"},
            }

            result = await intent_service.process_intent(
                message="Calendar and status",
                session_id="sess1",
                user_id=None,
            )

            # Should have fallen back to primary intent processing
            assert result.success
            assert "2pm" in result.message
            # Should NOT be marked as orchestrated
            assert not result.multi_intent_orchestrated


class TestIntentProcessingResultField:
    """Verify new field exists and defaults correctly."""

    def test_multi_intent_orchestrated_default_false(self):
        result = IntentProcessingResult(
            success=True,
            message="test",
            intent_data={},
        )
        assert result.multi_intent_orchestrated is False

    def test_multi_intent_orchestrated_set_true(self):
        result = IntentProcessingResult(
            success=True,
            message="test",
            intent_data={},
            multi_intent_orchestrated=True,
        )
        assert result.multi_intent_orchestrated is True
