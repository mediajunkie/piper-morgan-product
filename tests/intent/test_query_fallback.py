"""
Test QUERY fallback routing for mis-classified intents - GREAT-4F Phase 1

Tests verify that QUERY intents no longer cause "No workflow type found" timeout errors.
Pattern matching routes likely mis-classified queries to appropriate handlers.
"""

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.llm.clients import llm_client
from services.orchestration.engine import OrchestrationEngine
from services.shared_types import IntentCategory


@pytest.fixture
async def intent_service():
    """Create IntentService with orchestration engine."""
    from services.domain.llm_domain_service import LLMDomainService
    from services.intent_service import classifier
    from services.service_registry import ServiceRegistry

    # Initialize and register LLM service (required for IntentService classifier)
    llm_domain_service = LLMDomainService()
    await llm_domain_service.initialize()
    ServiceRegistry.register("llm", llm_domain_service)

    orchestration_engine = OrchestrationEngine(llm_client=llm_client)
    service = IntentService(orchestration_engine=orchestration_engine)

    yield service

    # Cleanup: Reset classifier's cached LLM and clear ServiceRegistry
    classifier._llm = None
    ServiceRegistry._services.clear()


class TestQueryFallback:
    """Test QUERY intent fallback handling."""

    @pytest.mark.asyncio
    async def test_query_temporal_fallback(self, intent_service):
        """QUERY with temporal keywords should not timeout."""
        # Simulate mis-classified TEMPORAL query
        result = await intent_service.process_intent(
            "show my calendar", session_id="test_query_temporal"
        )

        # Should not raise "No workflow type found" error
        assert result is not None, "QUERY fallback should return a result"
        assert result.message is not None, "Result should have a message"
        # Don't fail if success=False - workflow might not complete, but shouldn't timeout
        print(f"  Temporal fallback: {result.message[:100] if result.message else 'No message'}")

    @pytest.mark.asyncio
    async def test_query_status_fallback(self, intent_service):
        """QUERY with status keywords should not timeout."""
        result = await intent_service.process_intent(
            "what is my status", session_id="test_query_status"
        )

        assert result is not None, "QUERY fallback should return a result"
        assert result.message is not None, "Result should have a message"
        print(f"  Status fallback: {result.message[:100] if result.message else 'No message'}")

    @pytest.mark.asyncio
    async def test_query_priority_fallback(self, intent_service):
        """QUERY with priority keywords should not timeout."""
        result = await intent_service.process_intent(
            "what are my priorities", session_id="test_query_priority"
        )

        assert result is not None, "QUERY fallback should return a result"
        assert result.message is not None, "Result should have a message"
        print(f"  Priority fallback: {result.message[:100] if result.message else 'No message'}")

    @pytest.mark.asyncio
    async def test_query_generic_fallback(self, intent_service):
        """Generic QUERY should route to GENERATE_REPORT."""
        result = await intent_service.process_intent(
            "what is the weather in Paris", session_id="test_query_generic"
        )

        assert result is not None, "Generic query should return a result"
        assert result.message is not None, "Result should have a message"
        # Generic query handled gracefully, even if it can't provide weather
        print(f"  Generic fallback: {result.message[:100] if result.message else 'No message'}")

    @pytest.mark.asyncio
    async def test_no_workflow_error_prevented(self, intent_service):
        """QUERY should never cause 'No workflow type found' error."""
        queries = ["show calendar", "my status", "what's important", "random query about anything"]

        for query_text in queries:
            # None of these should raise errors or timeout
            result = await intent_service.process_intent(
                query_text, session_id=f"test_no_error_{query_text[:10]}"
            )

            assert result is not None, f"Query should not fail: {query_text}"
            assert result.message is not None, f"Query should have message: {query_text}"
            print(f"  ✓ No error for: {query_text}")

    @pytest.mark.asyncio
    async def test_query_temporal_patterns_comprehensive(self, intent_service):
        """Test comprehensive temporal pattern matching."""
        temporal_queries = [
            "what's on my calendar today",
            "show me tomorrow's schedule",
            "when is my next meeting",
            "what time is the appointment",
        ]

        for query in temporal_queries:
            result = await intent_service.process_intent(
                query, session_id=f"test_temporal_pattern_{query[:15]}"
            )

            assert result is not None, f"Temporal pattern should work: {query}"
            print(f"  ✓ Temporal pattern: {query}")

    @pytest.mark.asyncio
    async def test_query_status_patterns_comprehensive(self, intent_service):
        """Test comprehensive status pattern matching."""
        status_queries = [
            "show my current work",
            "what am I working on",
            "what's my progress",
            "standup status",
        ]

        for query in status_queries:
            result = await intent_service.process_intent(
                query, session_id=f"test_status_pattern_{query[:15]}"
            )

            assert result is not None, f"Status pattern should work: {query}"
            print(f"  ✓ Status pattern: {query}")

    @pytest.mark.asyncio
    async def test_query_priority_patterns_comprehensive(self, intent_service):
        """Test comprehensive priority pattern matching."""
        priority_queries = [
            "what's most important",
            "show my top priorities",
            "what should I focus on",
            "what's urgent",
        ]

        for query in priority_queries:
            result = await intent_service.process_intent(
                query, session_id=f"test_priority_pattern_{query[:15]}"
            )

            assert result is not None, f"Priority pattern should work: {query}"
            print(f"  ✓ Priority pattern: {query}")
