"""
Tests for IntentOrchestrator — multi-substantive intent execution.

Issue #764: GLUE-MULTIINTENT — Multi-Intent Handling Enhancements
Phase 1: IntentOrchestrator + ExecutionPlan data model

Tests cover:
- ExecutionPlan creation and properties
- Intent execution through canonical handlers
- Response aggregation with transitions
- Partial failure handling
- Intent cap enforcement
- Greeting prefix handling
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.domain.models import Intent
from services.intent_service.orchestrator import (
    MAX_INTENTS,
    ExecutionPlan,
    ExecutionStrategy,
    IntentExecutionResult,
    IntentOrchestrator,
    OrchestratedResponse,
    _intent_topic_label,
    _lowercase_first,
)
from services.intent_service.pre_classifier import MultiIntentResult
from services.shared_types import IntentCategory


def _make_intent(category: IntentCategory, action: str) -> Intent:
    """Helper to create test intents."""
    return Intent(category=category, action=action, confidence=1.0)


def _make_multi_result(intents: list, message: str = "test") -> MultiIntentResult:
    """Helper to create MultiIntentResult."""
    return MultiIntentResult(
        intents=intents,
        original_message=message,
        is_multi_intent=len(intents) > 1,
    )


@pytest.fixture
def mock_handlers():
    """Mock CanonicalHandlers."""
    handlers = MagicMock()
    handlers.can_handle = MagicMock(return_value=True)
    # 2026-10-04 Arch's split-predicate ruling: _execute_single now gates on
    # claims_category (category-only), not can_handle (rail-aware) — see
    # orchestrator.py's docstring on _execute_single. Default True so every
    # other test in this class (written against can_handle) is unaffected.
    handlers.claims_category = MagicMock(return_value=True)
    handlers.handle = AsyncMock(
        return_value={
            "message": "Here's the result.",
            "intent": {"category": "query", "action": "test"},
            "requires_clarification": False,
        }
    )
    return handlers


@pytest.fixture
def orchestrator(mock_handlers):
    return IntentOrchestrator(canonical_handlers=mock_handlers)


# --- ExecutionPlan Tests ---


class TestExecutionPlan:
    def test_creation(self):
        intent = _make_intent(IntentCategory.QUERY, "meeting_time")
        plan = ExecutionPlan(intents=[intent])
        assert plan.intent_count == 1
        assert plan.strategy == ExecutionStrategy.PARALLEL
        assert not plan.capped

    def test_empty_plan(self):
        plan = ExecutionPlan(intents=[])
        assert plan.intent_count == 0


# --- IntentExecutionResult Tests ---


class TestIntentExecutionResult:
    def test_successful_result(self):
        intent = _make_intent(IntentCategory.QUERY, "meeting_time")
        result = IntentExecutionResult(
            intent=intent, response="Your next meeting is at 2pm.", success=True
        )
        assert result.success

    def test_failed_result(self):
        intent = _make_intent(IntentCategory.STATUS, "get_project_status")
        result = IntentExecutionResult(intent=intent, success=False, error="Handler timeout")
        assert not result.success
        assert result.error == "Handler timeout"


# --- OrchestratedResponse Tests ---


class TestOrchestratedResponse:
    def test_all_successful(self):
        results = [
            IntentExecutionResult(
                intent=_make_intent(IntentCategory.QUERY, "meeting_time"),
                response="Next meeting at 2pm.",
                success=True,
            ),
            IntentExecutionResult(
                intent=_make_intent(IntentCategory.STATUS, "get_project_status"),
                response="Sprint is on track.",
                success=True,
            ),
        ]
        response = OrchestratedResponse(results=results)
        assert len(response.successful_results) > 0
        assert len(response.successful_results) == 2
        assert len(response.failed_results) == 0
        assert not response.has_partial_failure

    def test_partial_failure(self):
        results = [
            IntentExecutionResult(
                intent=_make_intent(IntentCategory.QUERY, "meeting_time"),
                response="Next meeting at 2pm.",
                success=True,
            ),
            IntentExecutionResult(
                intent=_make_intent(IntentCategory.STATUS, "get_project_status"),
                success=False,
                error="Timeout",
            ),
        ]
        response = OrchestratedResponse(results=results, has_partial_failure=True)
        assert len(response.successful_results) > 0  # At least one succeeded
        assert len(response.successful_results) == 1
        assert len(response.failed_results) == 1

    def test_all_failed(self):
        results = [
            IntentExecutionResult(
                intent=_make_intent(IntentCategory.QUERY, "meeting_time"),
                success=False,
                error="Timeout",
            ),
        ]
        response = OrchestratedResponse(results=results)
        assert len(response.successful_results) == 0

    def test_primary_intent_data(self):
        results = [
            IntentExecutionResult(
                intent=_make_intent(IntentCategory.QUERY, "meeting_time"),
                intent_data={"category": "query", "action": "meeting_time"},
                success=True,
            ),
        ]
        response = OrchestratedResponse(results=results)
        assert response.primary_intent_data["action"] == "meeting_time"

    def test_primary_intent_data_empty_on_all_failure(self):
        results = [
            IntentExecutionResult(
                intent=_make_intent(IntentCategory.QUERY, "meeting_time"),
                success=False,
            ),
        ]
        response = OrchestratedResponse(results=results)
        assert response.primary_intent_data == {}


# --- IntentOrchestrator.create_plan Tests ---


class TestCreatePlan:
    def test_two_intents(self, orchestrator):
        intents = [
            _make_intent(IntentCategory.QUERY, "meeting_time"),
            _make_intent(IntentCategory.STATUS, "get_project_status"),
        ]
        multi = _make_multi_result(intents, "calendar and status")
        plan = orchestrator.create_plan(multi)
        assert plan.intent_count == 2
        assert plan.strategy == ExecutionStrategy.PARALLEL
        assert not plan.capped

    def test_with_greeting(self, orchestrator):
        intents = [
            _make_intent(IntentCategory.CONVERSATION, "greeting"),
            _make_intent(IntentCategory.QUERY, "meeting_time"),
            _make_intent(IntentCategory.STATUS, "get_project_status"),
        ]
        multi = _make_multi_result(intents, "Hi! Calendar and status")
        plan = orchestrator.create_plan(multi)
        assert plan.has_greeting
        assert plan.intent_count == 3

    def test_caps_at_max(self, orchestrator):
        intents = [_make_intent(IntentCategory.QUERY, f"action_{i}") for i in range(6)]
        multi = _make_multi_result(intents)
        plan = orchestrator.create_plan(multi)
        assert plan.intent_count == MAX_INTENTS
        assert plan.capped

    def test_single_intent(self, orchestrator):
        intents = [_make_intent(IntentCategory.QUERY, "meeting_time")]
        multi = _make_multi_result(intents)
        multi.is_multi_intent = False
        plan = orchestrator.create_plan(multi)
        assert plan.intent_count == 1
        assert not plan.capped


# --- IntentOrchestrator.execute_plan Tests ---


class TestExecutePlan:
    @pytest.mark.asyncio
    async def test_single_intent_execution(self, orchestrator, mock_handlers):
        mock_handlers.handle.return_value = {
            "message": "Your next meeting is at 2pm.",
            "intent": {"category": "query", "action": "meeting_time"},
        }
        plan = ExecutionPlan(intents=[_make_intent(IntentCategory.QUERY, "meeting_time")])
        response = await orchestrator.execute_plan(plan, "sess1", "user1")
        assert len(response.successful_results) > 0
        assert len(response.results) == 1
        assert "2pm" in response.aggregated_message

    @pytest.mark.asyncio
    async def test_two_intent_execution(self, orchestrator, mock_handlers):
        call_count = 0

        async def multi_handle(intent, session_id, user_id=None):
            nonlocal call_count
            call_count += 1
            if intent.action == "meeting_time":
                return {
                    "message": "Your next meeting is at 2pm.",
                    "intent": {"category": "query", "action": "meeting_time"},
                }
            else:
                return {
                    "message": "Sprint is on track.",
                    "intent": {"category": "status", "action": "get_project_status"},
                }

        mock_handlers.handle = multi_handle
        plan = ExecutionPlan(
            intents=[
                _make_intent(IntentCategory.QUERY, "meeting_time"),
                _make_intent(IntentCategory.STATUS, "get_project_status"),
            ]
        )
        response = await orchestrator.execute_plan(plan, "sess1", "user1")
        assert len(response.successful_results) > 0
        assert len(response.results) == 2
        assert call_count == 2
        assert "2pm" in response.aggregated_message
        assert "track" in response.aggregated_message

    @pytest.mark.asyncio
    async def test_partial_failure(self, orchestrator, mock_handlers):
        call_count = 0

        async def failing_handle(intent, session_id, user_id=None):
            nonlocal call_count
            call_count += 1
            if intent.action == "meeting_time":
                return {
                    "message": "Your next meeting is at 2pm.",
                    "intent": {"category": "query", "action": "meeting_time"},
                }
            else:
                raise RuntimeError("Status service unavailable")

        mock_handlers.handle = failing_handle
        plan = ExecutionPlan(
            intents=[
                _make_intent(IntentCategory.QUERY, "meeting_time"),
                _make_intent(IntentCategory.STATUS, "get_project_status"),
            ]
        )
        response = await orchestrator.execute_plan(plan, "sess1", "user1")
        assert len(response.successful_results) > 0  # Partial success
        assert response.has_partial_failure
        assert len(response.successful_results) == 1
        assert len(response.failed_results) == 1
        assert "2pm" in response.aggregated_message
        assert "wasn't able" in response.aggregated_message

    @pytest.mark.asyncio
    async def test_all_failure(self, orchestrator, mock_handlers):
        mock_handlers.handle = AsyncMock(side_effect=RuntimeError("Everything broken"))
        plan = ExecutionPlan(intents=[_make_intent(IntentCategory.QUERY, "meeting_time")])
        response = await orchestrator.execute_plan(plan, "sess1", "user1")
        assert len(response.successful_results) == 0
        assert "trouble processing" in response.aggregated_message

    @pytest.mark.asyncio
    async def test_unhandleable_intent(self, orchestrator, mock_handlers):
        # claims_category, not can_handle — _execute_single's actual gate
        # (Arch's 2026-10-04 split-predicate ruling).
        mock_handlers.claims_category.return_value = False
        plan = ExecutionPlan(intents=[_make_intent(IntentCategory.QUERY, "meeting_time")])
        response = await orchestrator.execute_plan(plan, "sess1", "user1")
        assert len(response.successful_results) == 0
        assert response.results[0].error

    @pytest.mark.asyncio
    async def test_greeting_prefix_added(self, orchestrator, mock_handlers):
        mock_handlers.handle.return_value = {
            "message": "Your next meeting is at 2pm.",
            "intent": {"category": "query", "action": "meeting_time"},
        }
        plan = ExecutionPlan(
            intents=[
                _make_intent(IntentCategory.CONVERSATION, "greeting"),
                _make_intent(IntentCategory.QUERY, "meeting_time"),
            ],
            has_greeting=True,
        )
        response = await orchestrator.execute_plan(plan, "sess1", "user1")
        assert response.greeting_prefix
        assert response.aggregated_message.startswith("Hi there!")

    @pytest.mark.asyncio
    async def test_duration_tracked(self, orchestrator, mock_handlers):
        plan = ExecutionPlan(intents=[_make_intent(IntentCategory.QUERY, "meeting_time")])
        response = await orchestrator.execute_plan(plan, "sess1", "user1")
        assert response.total_duration_ms >= 0
        assert response.results[0].duration_ms >= 0

    @pytest.mark.asyncio
    async def test_session_and_user_passed(self, orchestrator, mock_handlers):
        plan = ExecutionPlan(intents=[_make_intent(IntentCategory.QUERY, "meeting_time")])
        await orchestrator.execute_plan(plan, "sess-abc", "user-xyz")
        mock_handlers.handle.assert_called_once()
        call_args = mock_handlers.handle.call_args
        assert call_args[0][1] == "sess-abc"  # session_id
        assert call_args[0][2] == "user-xyz"  # user_id


# --- Aggregation Tests ---


class TestAggregation:
    def test_single_result_no_aggregation(self, orchestrator):
        response = OrchestratedResponse(
            results=[
                IntentExecutionResult(
                    intent=_make_intent(IntentCategory.QUERY, "meeting_time"),
                    response="Your next meeting is at 2pm.",
                    success=True,
                )
            ]
        )
        msg = orchestrator._aggregate_messages(response)
        assert msg == "Your next meeting is at 2pm."

    def test_two_results_with_transition(self, orchestrator):
        response = OrchestratedResponse(
            results=[
                IntentExecutionResult(
                    intent=_make_intent(IntentCategory.QUERY, "meeting_time"),
                    response="Your next meeting is at 2pm.",
                    success=True,
                ),
                IntentExecutionResult(
                    intent=_make_intent(IntentCategory.STATUS, "get_project_status"),
                    response="Sprint is on track.",
                    success=True,
                ),
            ]
        )
        msg = orchestrator._aggregate_messages(response)
        assert "2pm" in msg
        assert "track" in msg
        # Should have a transition phrase
        assert any(t in msg for t in ["As for", "Regarding", "On the"])

    def test_greeting_prefix(self, orchestrator):
        response = OrchestratedResponse(
            results=[
                IntentExecutionResult(
                    intent=_make_intent(IntentCategory.QUERY, "meeting_time"),
                    response="Your next meeting is at 2pm.",
                    success=True,
                )
            ],
            greeting_prefix=True,
        )
        msg = orchestrator._aggregate_messages(response)
        assert msg.startswith("Hi there!")

    def test_partial_failure_message(self, orchestrator):
        response = OrchestratedResponse(
            results=[
                IntentExecutionResult(
                    intent=_make_intent(IntentCategory.QUERY, "meeting_time"),
                    response="Your next meeting is at 2pm.",
                    success=True,
                ),
                IntentExecutionResult(
                    intent=_make_intent(IntentCategory.STATUS, "get_project_status"),
                    success=False,
                    error="Timeout",
                ),
            ]
        )
        msg = orchestrator._aggregate_messages(response)
        assert "2pm" in msg
        assert "wasn't able" in msg
        assert "project status" in msg

    def test_all_failed_message(self, orchestrator):
        response = OrchestratedResponse(
            results=[
                IntentExecutionResult(
                    intent=_make_intent(IntentCategory.QUERY, "meeting_time"),
                    success=False,
                )
            ]
        )
        msg = orchestrator._aggregate_messages(response)
        assert "trouble processing" in msg


# --- Helper Function Tests ---


class TestHelpers:
    def test_topic_label_known_actions(self):
        intent = _make_intent(IntentCategory.QUERY, "meeting_time")
        assert _intent_topic_label(intent) == "your calendar"

    def test_topic_label_unknown_action(self):
        intent = _make_intent(IntentCategory.QUERY, "custom_action")
        assert _intent_topic_label(intent) == "custom action"

    def test_lowercase_first_normal(self):
        assert _lowercase_first("Hello world") == "hello world"

    def test_lowercase_first_preserves_i(self):
        assert _lowercase_first("I'm here to help") == "I'm here to help"

    def test_lowercase_first_empty(self):
        assert _lowercase_first("") == ""

    def test_lowercase_first_single_char(self):
        assert _lowercase_first("A") == "a"
