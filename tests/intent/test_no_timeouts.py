"""
Verify no timeout errors occur for previously problematic queries.
Tests that Phase 1 QUERY fallback and Phase 2 classifier improvements work together.
"""

import pytest

from services.intent.intent_service import IntentService


class TestNoTimeoutErrors:
    """Verify QUERY fallback prevents timeout errors"""

    @pytest.fixture
    def intent_service(self):
        return IntentService()

    # Previously problematic queries (would timeout before Phase 1)
    PROBLEMATIC_QUERIES = [
        "show my calendar",
        "what is my status",
        "list priorities",
        "what's on my schedule",
        "current work status",
        "my top priorities",
        "what am I working on",
        "calendar for today",
        "show me my tasks",
        "what should I focus on",
    ]

    @pytest.mark.asyncio
    async def test_no_workflow_timeout_errors(self, intent_service):
        """All queries should complete without 'No workflow type found' errors"""
        errors = []

        for query in self.PROBLEMATIC_QUERIES:
            try:
                result = await intent_service.process_intent(query, session_id="test_no_timeout")

                # Should complete successfully (either correct classification or fallback)
                assert result is not None, f"Query '{query}' returned None"

                # Should not contain timeout/workflow error messages
                if result.message and "No workflow type found" in result.message:
                    errors.append(f"{query} → 'No workflow type found' error")
                elif result.message and "timeout" in result.message.lower():
                    errors.append(f"{query} → timeout error")

            except Exception as e:
                errors.append(f"{query} → Exception: {str(e)}")

        # Report any errors found
        if errors:
            error_report = "\n".join(errors)
            pytest.fail(f"Found timeout/workflow errors:\n{error_report}")

        print(f"\n✅ All {len(self.PROBLEMATIC_QUERIES)} queries completed without timeout errors")

    @pytest.mark.asyncio
    async def test_query_fallback_handles_misclassifications(self, intent_service):
        """QUERY category should never cause 'No workflow type found' errors"""

        # Force a QUERY classification (generic question)
        query = "what is the meaning of life"

        result = await intent_service.process_intent(query, session_id="test_query_fallback")

        # Should complete (either via GENERATE_REPORT or other fallback)
        assert result is not None
        assert "No workflow type found" not in (result.message or "")

        print(f"\n✅ QUERY fallback working: '{query}' handled gracefully")
