"""
Verify no timeout errors occur for previously problematic queries.
Tests that Phase 1 QUERY fallback and Phase 2 classifier improvements work together.
"""

from uuid import uuid4

import pytest

from services.intent.intent_service import IntentService
from services.intent_service.conversation_context import clear_context, get_or_create_context


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
        """QUERY category should never cause 'No workflow type found' errors.

        1637: this used to send the raw message through the REAL classifier —
        "what is the meaning of life" matches no pre-classifier pattern, so it
        reached the LLM classifier, which in this environment has no
        initialized container and raised INTENT_CLASSIFICATION_FAILED. The
        test was env-dependent, and the failure it produced was the
        classifier's, not the dispatch fallback's — the layer this test
        exists to cover (m-43). Stub classification to hand dispatch a QUERY
        intent directly; what stays under test is that QUERY dispatch
        completes via the fallback rail instead of a workflow-type error.
        """
        from unittest.mock import AsyncMock, patch

        from services.domain.models import Intent
        from services.intent_service.pre_classifier import MultiIntentResult
        from services.shared_types import IntentCategory

        query = "what is the meaning of life"
        query_intent = Intent(
            original_message=query,
            category=IntentCategory.QUERY,
            action=None,
            confidence=0.9,
        )
        multi_result = MultiIntentResult(
            intents=[query_intent], original_message=query, is_multi_intent=False
        )

        with patch.object(
            intent_service.intent_classifier,
            "classify_multiple",
            AsyncMock(return_value=multi_result),
        ):
            result = await intent_service.process_intent(query, session_id="test_query_fallback")

        # Should complete (either via GENERATE_REPORT or other fallback)
        assert result is not None
        assert result.success is True
        assert "No workflow type found" not in (result.message or "")

        print(f"\n✅ QUERY fallback working: '{query}' handled gracefully")


class TestNoTimeoutErrorsAuthenticated:
    """#1533 (principal-dropping audit) — both calls above pass session_id
    only, no user_id at all. If process_intent's outer turn-recording seam
    (get_or_create_context, intent_service.py ~L765-819) ever dropped
    user_id on this QUERY-fallback dispatch path, two authenticated users
    sharing a session_id would collapse onto the same context and this
    file's coverage would not catch it (m-44)."""

    @pytest.fixture
    def intent_service(self):
        return IntentService()

    @pytest.mark.asyncio
    async def test_query_fallback_does_not_leak_turns_across_authenticated_users(
        self, intent_service
    ):
        session_id = str(uuid4())
        user_a = str(uuid4())
        user_b = str(uuid4())

        try:
            result_a = await intent_service.process_intent(
                "show my calendar", session_id=session_id, user_id=user_a
            )
            result_b = await intent_service.process_intent(
                "what is my status", session_id=session_id, user_id=user_b
            )

            assert result_a is not None and result_b is not None

            ctx_a = get_or_create_context(session_id, user_id=user_a)
            ctx_b = get_or_create_context(session_id, user_id=user_b)

            # The teeth: under the real composite key, two distinct user_ids
            # sharing one session_id get DISTINCT contexts. If user_id were
            # ever dropped on the QUERY-fallback dispatch path, both turns
            # would land in the same context.
            assert ctx_a is not ctx_b, (
                "two distinct authenticated users sharing a session_id "
                "collapsed onto the same context on the QUERY-fallback "
                "dispatch path — user_id was dropped"
            )
            assert [t.message for t in ctx_a.turns] == ["show my calendar"]
            assert [t.message for t in ctx_b.turns] == ["what is my status"]
        finally:
            clear_context(session_id, user_a)
            clear_context(session_id, user_b)
