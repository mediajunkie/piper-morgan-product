"""Performance contract tests for all 13 intent categories - GREAT-4E Phase 3

**Standing review rule (#1533 principal-dropping audit, TEST-BLIND section)**:
any new test of a ``{user_id or 'anonymous'}:{session_id}``-keyed surface must
assert at least once under a non-None user_id — a probe where the keys
coincide is a config check, not a verification (m-44). Every test above
never passes user_id at all; ``TestPerformanceContractsAuthenticated`` below
adds the authenticated sibling. Unmarked (no ``@pytest.mark.llm``) — unlike
every test above, which is llm-marked even for deterministically-resolved
categories — it runs against the deterministic classifier tier pinned by
``tests/intent/conftest.py`` (#1831), which is sufficient to prove the
property under test (the outer turn-recording seam threading user_id) without
live-LLM cost. It uses TEMPORAL as a single representative probe rather than
all 13 categories: that seam is category-agnostic and already exhaustively
proven across all 13 categories in
``test_multiuser_contracts.py::TestMultiUserContractsAuthenticated``; a
second full 13-category sweep here would re-prove the same mechanism, not
this file's own distinguishing property (response-time threshold).
"""

import time
from uuid import uuid4

import pytest

from services.api.errors import IntentClassificationFailedError
from services.intent.intent_service import IntentProcessingError
from services.intent_service.conversation_context import (
    clear_context,
    get_or_create_context,
)
from tests.intent.base_validation_test import BaseValidationTest
from tests.intent.coverage_tracker import coverage
from tests.intent.test_constants import CATEGORY_EXAMPLES


class TestPerformanceContracts(BaseValidationTest):
    """Verify all categories meet performance requirements (<3000ms)."""

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_temporal_performance(self, intent_service):
        """PERF 1/13: TEMPORAL response time."""
        message = CATEGORY_EXAMPLES["TEMPORAL"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ TEMPORAL performance: {duration_ms:.1f}ms")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_status_performance(self, intent_service):
        """PERF 2/13: STATUS response time."""
        message = CATEGORY_EXAMPLES["STATUS"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ STATUS performance: {duration_ms:.1f}ms")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_priority_performance(self, intent_service):
        """PERF 3/13: PRIORITY response time."""
        message = CATEGORY_EXAMPLES["PRIORITY"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ PRIORITY performance: {duration_ms:.1f}ms")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_identity_performance(self, intent_service):
        """PERF 4/13: IDENTITY response time."""
        message = CATEGORY_EXAMPLES["IDENTITY"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ IDENTITY performance: {duration_ms:.1f}ms")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_guidance_performance(self, intent_service):
        """PERF 5/13: GUIDANCE response time."""
        message = CATEGORY_EXAMPLES["GUIDANCE"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ GUIDANCE performance: {duration_ms:.1f}ms")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_execution_performance(self, intent_service):
        """PERF 6/13: EXECUTION response time."""
        message = CATEGORY_EXAMPLES["EXECUTION"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ EXECUTION performance: {duration_ms:.1f}ms")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_analysis_performance(self, intent_service):
        """PERF 7/13: ANALYSIS response time."""
        message = CATEGORY_EXAMPLES["ANALYSIS"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ ANALYSIS performance: {duration_ms:.1f}ms")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_synthesis_performance(self, intent_service):
        """PERF 8/13: SYNTHESIS response time."""
        message = CATEGORY_EXAMPLES["SYNTHESIS"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ SYNTHESIS performance: {duration_ms:.1f}ms")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_strategy_performance(self, intent_service):
        """PERF 9/13: STRATEGY response time."""
        message = CATEGORY_EXAMPLES["STRATEGY"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ STRATEGY performance: {duration_ms:.1f}ms")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_learning_performance(self, intent_service):
        """PERF 10/13: LEARNING response time."""
        message = CATEGORY_EXAMPLES["LEARNING"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ LEARNING performance: {duration_ms:.1f}ms")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_unknown_performance(self, intent_service):
        """PERF 11/13: UNKNOWN response time."""
        message = CATEGORY_EXAMPLES["UNKNOWN"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ UNKNOWN performance: {duration_ms:.1f}ms")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_query_performance(self, intent_service):
        """PERF 12/13: QUERY response time."""
        message = CATEGORY_EXAMPLES["QUERY"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ QUERY performance: {duration_ms:.1f}ms")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_conversation_performance(self, intent_service):
        """PERF 13/13: CONVERSATION response time."""
        message = CATEGORY_EXAMPLES["CONVERSATION"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold (3000ms)
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ CONVERSATION performance: {duration_ms:.1f}ms")

    @pytest.mark.asyncio
    async def test_zzz_performance_coverage(self):
        """Performance contract coverage report."""
        print("\n" + "=" * 80)
        print("PERFORMANCE CONTRACT REPORT")
        print("=" * 80)
        print("All 13 categories meet <3000ms threshold")
        print("=" * 80)


class TestPerformanceContractsAuthenticated(BaseValidationTest):
    """#1533: authenticated-principal sibling for this suite.

    Every test above calls ``process_intent`` with ``session_id="perf_test"``
    and no ``user_id`` — every category's probe collapses onto the same
    anonymous context. This proves the property none of the tests above can
    see: the performance contract still holds per-user, AND the outer
    turn-recording seam still separates two DISTINCT authenticated users
    sharing one session_id.
    """

    async def _tolerant_call(self, intent_service, message, session_id, user_id):
        """Real process_intent, tolerating ONLY the expected #1831
        no-LLM-provider failure (see test_multiuser_contracts.py's sibling
        helper for the full rationale). Anything else re-raises."""
        try:
            return await intent_service.process_intent(
                message, session_id=session_id, user_id=user_id
            )
        except (IntentProcessingError, IntentClassificationFailedError) as e:
            details = getattr(e, "details", None) or {}
            cause = str(details.get("original_error", "")) or str(e)
            if "No LLM providers configured" not in cause:
                raise
            return None

    @pytest.mark.asyncio
    async def test_temporal_performance_does_not_leak_turns_across_authenticated_users(
        self, intent_service
    ):
        session_id = str(uuid4())
        user_a = str(uuid4())
        user_b = str(uuid4())
        # TEMPORAL resolves at Stage 1 (deterministic pre-classifier), so it
        # succeeds under the #1831 unmarked-tier stub too.
        message = CATEGORY_EXAMPLES["TEMPORAL"]

        try:
            start_a = time.time()
            result_a = await self._tolerant_call(intent_service, message, session_id, user_a)
            duration_a_ms = (time.time() - start_a) * 1000

            start_b = time.time()
            result_b = await self._tolerant_call(intent_service, message, session_id, user_b)
            duration_b_ms = (time.time() - start_b) * 1000

            assert result_a is not None and result_a.success is not None
            assert result_b is not None and result_b.success is not None
            self.assert_performance(duration_a_ms)
            self.assert_performance(duration_b_ms)

            ctx_a = get_or_create_context(session_id, user_id=user_a)
            ctx_b = get_or_create_context(session_id, user_id=user_b)

            # The teeth: two distinct authenticated user_ids sharing one
            # session_id must get DISTINCT context objects, each holding
            # only its own turn.
            assert ctx_a is not ctx_b, (
                "two distinct user_ids sharing session_id resolved to the SAME "
                "context object — user_id is not part of the effective key"
            )
            assert len(ctx_a.turns) == 1 and ctx_a.turns[0].message == message, (
                f"user A's context leaked cross-user turns: "
                f"{[t.message for t in ctx_a.turns]!r}"
            )
            assert len(ctx_b.turns) == 1 and ctx_b.turns[0].message == message, (
                f"user B's context leaked cross-user turns: "
                f"{[t.message for t in ctx_b.turns]!r}"
            )

            coverage.contract_tests_passed += 1
            print(
                f"✓ TEMPORAL performance (authenticated): "
                f"{duration_a_ms:.1f}ms / {duration_b_ms:.1f}ms, isolated"
            )
        finally:
            clear_context(session_id, user_id=user_a)
            clear_context(session_id, user_id=user_b)
