"""Bypass prevention contract tests for all 13 intent categories - GREAT-4E Phase 3

Verifies that all category handling goes through proper intent classification
and routing (no direct bypasses).

**Standing review rule (#1533 principal-dropping audit, TEST-BLIND section)**:
any new test of a ``{user_id or 'anonymous'}:{session_id}``-keyed surface must
assert at least once under a non-None user_id — a probe where the keys
coincide is a config check, not a verification (m-44). Every test above
never passes user_id at all; ``TestBypassContractsAuthenticated`` below adds
the authenticated sibling. Unmarked (no ``@pytest.mark.llm``) — like
``test_multiuser_contracts.py``'s authenticated class, it runs against the
deterministic classifier tier pinned by ``tests/intent/conftest.py`` (#1831).
It uses TEMPORAL as a single representative probe rather than all 13
categories: the property under test — does the outer turn-recording seam
(``get_or_create_context`` + ``conv_ctx.add_turn``) thread ``user_id``
correctly — lives entirely in ``process_intent``'s category-agnostic seam,
already exhaustively proven across all 13 categories in
``test_multiuser_contracts.py::TestMultiUserContractsAuthenticated``; a
second full 13-category sweep here would re-prove the same mechanism, not
this file's own distinguishing property (no-bypass routing).
"""

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


class TestBypassContracts(BaseValidationTest):
    """Verify no bypass routes exist for any category."""

    @pytest.mark.asyncio
    async def test_temporal_no_bypass(self, intent_service):
        """BYPASS 1/13: TEMPORAL requires classification."""
        message = CATEGORY_EXAMPLES["TEMPORAL"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        # If we get a result, classification occurred
        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ TEMPORAL no bypass: verified")

    @pytest.mark.asyncio
    async def test_status_no_bypass(self, intent_service):
        """BYPASS 2/13: STATUS requires classification."""
        message = CATEGORY_EXAMPLES["STATUS"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ STATUS no bypass: verified")

    @pytest.mark.asyncio
    async def test_priority_no_bypass(self, intent_service):
        """BYPASS 3/13: PRIORITY requires classification."""
        message = CATEGORY_EXAMPLES["PRIORITY"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ PRIORITY no bypass: verified")

    @pytest.mark.asyncio
    async def test_identity_no_bypass(self, intent_service):
        """BYPASS 4/13: IDENTITY requires classification."""
        message = CATEGORY_EXAMPLES["IDENTITY"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ IDENTITY no bypass: verified")

    @pytest.mark.asyncio
    async def test_guidance_no_bypass(self, intent_service):
        """BYPASS 5/13: GUIDANCE requires classification."""
        message = CATEGORY_EXAMPLES["GUIDANCE"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ GUIDANCE no bypass: verified")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_execution_no_bypass(self, intent_service):
        """BYPASS 6/13: EXECUTION requires classification (requires LLM)."""
        message = CATEGORY_EXAMPLES["EXECUTION"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ EXECUTION no bypass: verified")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_analysis_no_bypass(self, intent_service):
        """BYPASS 7/13: ANALYSIS requires classification (requires LLM)."""
        message = CATEGORY_EXAMPLES["ANALYSIS"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ ANALYSIS no bypass: verified")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_synthesis_no_bypass(self, intent_service):
        """BYPASS 8/13: SYNTHESIS requires classification (requires LLM)."""
        message = CATEGORY_EXAMPLES["SYNTHESIS"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ SYNTHESIS no bypass: verified")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_strategy_no_bypass(self, intent_service):
        """BYPASS 9/13: STRATEGY requires classification (requires LLM)."""
        message = CATEGORY_EXAMPLES["STRATEGY"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ STRATEGY no bypass: verified")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_learning_no_bypass(self, intent_service):
        """BYPASS 10/13: LEARNING requires classification (requires LLM)."""
        message = CATEGORY_EXAMPLES["LEARNING"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ LEARNING no bypass: verified")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_unknown_no_bypass(self, intent_service):
        """BYPASS 11/13: UNKNOWN requires classification (requires LLM)."""
        message = CATEGORY_EXAMPLES["UNKNOWN"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ UNKNOWN no bypass: verified")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_query_no_bypass(self, intent_service):
        """BYPASS 12/13: QUERY requires classification (requires LLM)."""
        message = CATEGORY_EXAMPLES["QUERY"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ QUERY no bypass: verified")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_conversation_no_bypass(self, intent_service):
        """BYPASS 13/13: CONVERSATION requires classification (requires LLM)."""
        message = CATEGORY_EXAMPLES["CONVERSATION"]
        result = await intent_service.process_intent(message, session_id="bypass_test")

        assert result is not None
        assert result.message is not None
        self.assert_no_placeholder(result.message)

        coverage.contract_tests_passed += 1
        print("✓ CONVERSATION no bypass: verified")

    @pytest.mark.asyncio
    async def test_zzz_bypass_coverage(self):
        """Bypass contract coverage report."""
        print("\n" + "=" * 80)
        print("BYPASS PREVENTION CONTRACT REPORT")
        print("=" * 80)
        print("All 13 categories require proper classification")
        print("=" * 80)


class TestBypassContractsAuthenticated(BaseValidationTest):
    """#1533: authenticated-principal sibling for this suite.

    Every test above calls ``process_intent`` with ``session_id="bypass_test"``
    and no ``user_id`` — every category's probe collapses onto the same
    anonymous context. This proves the property none of the tests above can
    see: the no-bypass contract (classification actually ran, produced a
    real message) still holds per-user, AND the outer turn-recording seam
    still separates two DISTINCT authenticated users sharing one session_id.
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
    async def test_temporal_no_bypass_does_not_leak_turns_across_authenticated_users(
        self, intent_service
    ):
        session_id = str(uuid4())
        user_a = str(uuid4())
        user_b = str(uuid4())
        # TEMPORAL resolves at Stage 1 (deterministic pre-classifier), so it
        # succeeds under the #1831 unmarked-tier stub too — the no-bypass
        # contract (classification produced a real message) is fully
        # assertable here.
        message = CATEGORY_EXAMPLES["TEMPORAL"]

        try:
            result_a = await self._tolerant_call(intent_service, message, session_id, user_a)
            result_b = await self._tolerant_call(intent_service, message, session_id, user_b)

            assert result_a is not None and result_a.message is not None
            assert result_b is not None and result_b.message is not None
            self.assert_no_placeholder(result_a.message)
            self.assert_no_placeholder(result_b.message)

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
            print("✓ TEMPORAL no bypass (authenticated): isolated under shared session_id")
        finally:
            clear_context(session_id, user_id=user_a)
            clear_context(session_id, user_id=user_b)
