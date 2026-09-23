"""
Test DIRECT interface for all 13 intent categories - GREAT-4E Phase 1

**Standing review rule (#1533 principal-dropping audit, TEST-BLIND section)**:
any new test of a ``{user_id or 'anonymous'}:{session_id}``-keyed surface must
assert at least once under a non-None user_id — a probe where the keys
coincide is a config check, not a verification (m-44). Every test above
never passes user_id at all; ``TestDirectInterfaceAuthenticated`` below adds
the authenticated sibling. It inherits this module's ``pytestmark = pytest.
mark.llm`` (the live tier, per the module docstring above), so unlike the
contracts-file siblings it does NOT go through the #1831 deterministic stub
— though TEMPORAL, the single representative category it uses, resolves at
Stage 1 (deterministic pre-classifier) and so doesn't actually reach the
LLM in practice either way. The property under test — does the outer
turn-recording seam thread ``user_id`` correctly — is category-agnostic and
already exhaustively proven across all 13 categories in
``test_multiuser_contracts.py::TestMultiUserContractsAuthenticated``.
"""

import time
from uuid import uuid4

import pytest

from services.intent_service.conversation_context import (
    clear_context,
    get_or_create_context,
)
from tests.intent.base_validation_test import BaseValidationTest
from tests.intent.coverage_tracker import coverage
from tests.intent.test_constants import CATEGORY_EXAMPLES

# #1452 wave 16: DIRECT-interface validation runs live process_intent with a
# latency assert; categories that fall past the pre-classifier hit the real
# LLM (that's the suite's point) — keyed llm lane, not the keyless CI sweep.
pytestmark = pytest.mark.llm


class TestDirectInterface(BaseValidationTest):
    """Test all 13 categories through DIRECT interface."""

    @pytest.mark.asyncio
    async def test_temporal_direct(self, intent_service):
        """DIRECT 1/13: TEMPORAL category."""
        message = CATEGORY_EXAMPLES["TEMPORAL"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="test_temporal")
        duration_ms = (time.time() - start) * 1000

        # Verify no placeholder
        self.assert_no_placeholder(result.message)

        # Verify handler executed (not error)
        assert result.success is not None
        assert len(result.message) > 0

        # Verify performance
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.categories_tested.add("TEMPORAL")
        coverage.interfaces_tested.add("direct")
        coverage.interface_tests_passed += 1

        print(f"✓ TEMPORAL: {duration_ms:.1f}ms")

    @pytest.mark.asyncio
    async def test_status_direct(self, intent_service):
        """DIRECT 2/13: STATUS category."""
        message = CATEGORY_EXAMPLES["STATUS"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="test_status")
        duration_ms = (time.time() - start) * 1000

        self.assert_no_placeholder(result.message)
        assert result.success is not None
        self.assert_performance(duration_ms)

        coverage.categories_tested.add("STATUS")
        coverage.interface_tests_passed += 1

        print(f"✓ STATUS: {duration_ms:.1f}ms")

    @pytest.mark.asyncio
    async def test_priority_direct(self, intent_service):
        """DIRECT 3/13: PRIORITY category."""
        message = CATEGORY_EXAMPLES["PRIORITY"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="test_priority")
        duration_ms = (time.time() - start) * 1000

        self.assert_no_placeholder(result.message)
        assert result.success is not None
        self.assert_performance(duration_ms)

        coverage.categories_tested.add("PRIORITY")
        coverage.interface_tests_passed += 1

        print(f"✓ PRIORITY: {duration_ms:.1f}ms")

    @pytest.mark.asyncio
    async def test_identity_direct(self, intent_service):
        """DIRECT 4/13: IDENTITY category."""
        message = CATEGORY_EXAMPLES["IDENTITY"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="test_identity")
        duration_ms = (time.time() - start) * 1000

        self.assert_no_placeholder(result.message)
        assert result.success is not None
        self.assert_performance(duration_ms)

        coverage.categories_tested.add("IDENTITY")
        coverage.interface_tests_passed += 1

        print(f"✓ IDENTITY: {duration_ms:.1f}ms")

    @pytest.mark.asyncio
    async def test_guidance_direct(self, intent_service):
        """DIRECT 5/13: GUIDANCE category."""
        message = CATEGORY_EXAMPLES["GUIDANCE"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="test_guidance")
        duration_ms = (time.time() - start) * 1000

        self.assert_no_placeholder(result.message)
        assert result.success is not None
        self.assert_performance(duration_ms)

        coverage.categories_tested.add("GUIDANCE")
        coverage.interface_tests_passed += 1

        print(f"✓ GUIDANCE: {duration_ms:.1f}ms")

    @pytest.mark.asyncio
    async def test_execution_direct(self, intent_service):
        """DIRECT 6/13: EXECUTION category."""
        message = CATEGORY_EXAMPLES["EXECUTION"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="test_execution")
        duration_ms = (time.time() - start) * 1000

        self.assert_no_placeholder(result.message)
        assert result.success is not None
        self.assert_performance(duration_ms)

        coverage.categories_tested.add("EXECUTION")
        coverage.interface_tests_passed += 1

        print(f"✓ EXECUTION: {duration_ms:.1f}ms")

    @pytest.mark.asyncio
    async def test_analysis_direct(self, intent_service):
        """DIRECT 7/13: ANALYSIS category."""
        message = CATEGORY_EXAMPLES["ANALYSIS"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="test_analysis")
        duration_ms = (time.time() - start) * 1000

        self.assert_no_placeholder(result.message)
        assert result.success is not None
        self.assert_performance(duration_ms)

        coverage.categories_tested.add("ANALYSIS")
        coverage.interface_tests_passed += 1

        print(f"✓ ANALYSIS: {duration_ms:.1f}ms")

    @pytest.mark.asyncio
    async def test_synthesis_direct(self, intent_service):
        """DIRECT 8/13: SYNTHESIS category."""
        message = CATEGORY_EXAMPLES["SYNTHESIS"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="test_synthesis")
        duration_ms = (time.time() - start) * 1000

        self.assert_no_placeholder(result.message)
        assert result.success is not None
        self.assert_performance(duration_ms)

        coverage.categories_tested.add("SYNTHESIS")
        coverage.interface_tests_passed += 1

        print(f"✓ SYNTHESIS: {duration_ms:.1f}ms")

    @pytest.mark.asyncio
    async def test_strategy_direct(self, intent_service):
        """DIRECT 9/13: STRATEGY category."""
        message = CATEGORY_EXAMPLES["STRATEGY"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="test_strategy")
        duration_ms = (time.time() - start) * 1000

        self.assert_no_placeholder(result.message)
        assert result.success is not None
        self.assert_performance(duration_ms)

        coverage.categories_tested.add("STRATEGY")
        coverage.interface_tests_passed += 1

        print(f"✓ STRATEGY: {duration_ms:.1f}ms")

    @pytest.mark.asyncio
    async def test_learning_direct(self, intent_service):
        """DIRECT 10/13: LEARNING category."""
        message = CATEGORY_EXAMPLES["LEARNING"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="test_learning")
        duration_ms = (time.time() - start) * 1000

        self.assert_no_placeholder(result.message)
        assert result.success is not None
        self.assert_performance(duration_ms)

        coverage.categories_tested.add("LEARNING")
        coverage.interface_tests_passed += 1

        print(f"✓ LEARNING: {duration_ms:.1f}ms")

    @pytest.mark.asyncio
    async def test_unknown_direct(self, intent_service):
        """DIRECT 11/13: UNKNOWN category."""
        message = CATEGORY_EXAMPLES["UNKNOWN"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="test_unknown")
        duration_ms = (time.time() - start) * 1000

        self.assert_no_placeholder(result.message)
        assert result.success is not None
        self.assert_performance(duration_ms)

        coverage.categories_tested.add("UNKNOWN")
        coverage.interface_tests_passed += 1

        print(f"✓ UNKNOWN: {duration_ms:.1f}ms")

    @pytest.mark.asyncio
    async def test_query_direct(self, intent_service):
        """DIRECT 12/13: QUERY category."""
        message = CATEGORY_EXAMPLES["QUERY"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="test_query")
        duration_ms = (time.time() - start) * 1000

        self.assert_no_placeholder(result.message)
        assert result.success is not None
        self.assert_performance(duration_ms)

        coverage.categories_tested.add("QUERY")
        coverage.interface_tests_passed += 1

        print(f"✓ QUERY: {duration_ms:.1f}ms")

    @pytest.mark.asyncio
    async def test_conversation_direct(self, intent_service):
        """DIRECT 13/13: CONVERSATION category."""
        message = CATEGORY_EXAMPLES["CONVERSATION"]

        start = time.time()
        result = await intent_service.process_intent(message, session_id="test_conversation")
        duration_ms = (time.time() - start) * 1000

        self.assert_no_placeholder(result.message)
        assert result.success is not None
        self.assert_performance(duration_ms)

        coverage.categories_tested.add("CONVERSATION")
        coverage.interface_tests_passed += 1

        print(f"✓ CONVERSATION: {duration_ms:.1f}ms")

    @pytest.mark.asyncio
    async def test_zzz_coverage_report(self):
        """Generate coverage report after all direct tests."""
        print("\n" + "=" * 80)
        print(coverage.report())
        print("=" * 80)

        # Verify we tested all 13 categories through direct interface
        assert (
            len(coverage.categories_tested) == 13
        ), f"Only tested {len(coverage.categories_tested)}/13 categories"

        assert "direct" in coverage.interfaces_tested

        # Should have 13 direct interface tests passing
        assert coverage.interface_tests_passed >= 13


class TestDirectInterfaceAuthenticated(BaseValidationTest):
    """#1533: authenticated-principal sibling for this suite.

    Every test above calls ``process_intent`` with a distinct per-category
    session_id and no ``user_id`` — every probe resolves to the anonymous
    half of the composite key. This proves the property none of the tests
    above can see: the DIRECT-interface contract (success, no placeholder,
    <threshold latency) still holds per-user, AND the outer turn-recording
    seam still separates two DISTINCT authenticated users sharing one
    session_id.
    """

    @pytest.mark.asyncio
    async def test_temporal_direct_does_not_leak_turns_across_authenticated_users(
        self, intent_service
    ):
        session_id = str(uuid4())
        user_a = str(uuid4())
        user_b = str(uuid4())
        message = CATEGORY_EXAMPLES["TEMPORAL"]

        try:
            start_a = time.time()
            result_a = await intent_service.process_intent(
                message, session_id=session_id, user_id=user_a
            )
            duration_a_ms = (time.time() - start_a) * 1000

            start_b = time.time()
            result_b = await intent_service.process_intent(
                message, session_id=session_id, user_id=user_b
            )
            duration_b_ms = (time.time() - start_b) * 1000

            self.assert_no_placeholder(result_a.message)
            self.assert_no_placeholder(result_b.message)
            assert result_a.success is not None
            assert result_b.success is not None
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

            coverage.categories_tested.add("TEMPORAL")
            coverage.interfaces_tested.add("direct")
            coverage.interface_tests_passed += 1

            print(
                f"✓ TEMPORAL (authenticated): {duration_a_ms:.1f}ms / "
                f"{duration_b_ms:.1f}ms, isolated"
            )
        finally:
            clear_context(session_id, user_id=user_a)
            clear_context(session_id, user_id=user_b)
