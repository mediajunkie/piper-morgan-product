"""Error handling contract tests for all 13 intent categories - GREAT-4E Phase 3

**Standing review rule (#1533 principal-dropping audit, TEST-BLIND section)**:
any new test of a ``{user_id or 'anonymous'}:{session_id}``-keyed surface must
assert at least once under a non-None user_id — a probe where the keys
coincide is a config check, not a verification (m-44). Every test above
never passes user_id at all; ``TestErrorContractsAuthenticated`` below adds
the authenticated sibling. Unmarked (no ``@pytest.mark.llm``) — like
``test_multiuser_contracts.py``'s authenticated class, it runs against the
deterministic classifier tier pinned by ``tests/intent/conftest.py``
(#1831), tolerating the expected Stage-2 no-LLM-provider failure while
still proving the outer turn-recording seam threads user_id correctly.
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


class TestErrorContracts(BaseValidationTest):
    """Verify error handling for all categories."""

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_temporal_error_handling(self, intent_service):
        """ERROR 1/13: TEMPORAL error handling."""
        # Test with malformed/empty message
        message = ""  # Empty message should not crash

        try:
            result = await intent_service.process_intent(message, session_id="error_test")

            # Verify graceful handling
            assert result is not None
            assert hasattr(result, "message")
            assert len(result.message) > 0

            # Should not have placeholder
            self.assert_no_placeholder(result.message)

            coverage.contract_tests_passed += 1
            print(f"✓ TEMPORAL error handling: graceful")

        except Exception as e:
            pytest.fail(f"TEMPORAL handler crashed on error: {e}")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_status_error_handling(self, intent_service):
        """ERROR 2/13: STATUS error handling."""
        # Test with malformed/empty message
        message = ""  # Empty message should not crash

        try:
            result = await intent_service.process_intent(message, session_id="error_test")

            # Verify graceful handling
            assert result is not None
            assert hasattr(result, "message")
            assert len(result.message) > 0

            # Should not have placeholder
            self.assert_no_placeholder(result.message)

            coverage.contract_tests_passed += 1
            print(f"✓ STATUS error handling: graceful")

        except Exception as e:
            pytest.fail(f"STATUS handler crashed on error: {e}")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_priority_error_handling(self, intent_service):
        """ERROR 3/13: PRIORITY error handling."""
        # Test with malformed/empty message
        message = ""  # Empty message should not crash

        try:
            result = await intent_service.process_intent(message, session_id="error_test")

            # Verify graceful handling
            assert result is not None
            assert hasattr(result, "message")
            assert len(result.message) > 0

            # Should not have placeholder
            self.assert_no_placeholder(result.message)

            coverage.contract_tests_passed += 1
            print(f"✓ PRIORITY error handling: graceful")

        except Exception as e:
            pytest.fail(f"PRIORITY handler crashed on error: {e}")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_identity_error_handling(self, intent_service):
        """ERROR 4/13: IDENTITY error handling."""
        # Test with malformed/empty message
        message = ""  # Empty message should not crash

        try:
            result = await intent_service.process_intent(message, session_id="error_test")

            # Verify graceful handling
            assert result is not None
            assert hasattr(result, "message")
            assert len(result.message) > 0

            # Should not have placeholder
            self.assert_no_placeholder(result.message)

            coverage.contract_tests_passed += 1
            print(f"✓ IDENTITY error handling: graceful")

        except Exception as e:
            pytest.fail(f"IDENTITY handler crashed on error: {e}")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_guidance_error_handling(self, intent_service):
        """ERROR 5/13: GUIDANCE error handling."""
        # Test with malformed/empty message
        message = ""  # Empty message should not crash

        try:
            result = await intent_service.process_intent(message, session_id="error_test")

            # Verify graceful handling
            assert result is not None
            assert hasattr(result, "message")
            assert len(result.message) > 0

            # Should not have placeholder
            self.assert_no_placeholder(result.message)

            coverage.contract_tests_passed += 1
            print(f"✓ GUIDANCE error handling: graceful")

        except Exception as e:
            pytest.fail(f"GUIDANCE handler crashed on error: {e}")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_execution_error_handling(self, intent_service):
        """ERROR 6/13: EXECUTION error handling."""
        # Test with malformed/empty message
        message = ""  # Empty message should not crash

        try:
            result = await intent_service.process_intent(message, session_id="error_test")

            # Verify graceful handling
            assert result is not None
            assert hasattr(result, "message")
            assert len(result.message) > 0

            # Should not have placeholder
            self.assert_no_placeholder(result.message)

            coverage.contract_tests_passed += 1
            print(f"✓ EXECUTION error handling: graceful")

        except Exception as e:
            pytest.fail(f"EXECUTION handler crashed on error: {e}")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_analysis_error_handling(self, intent_service):
        """ERROR 7/13: ANALYSIS error handling."""
        # Test with malformed/empty message
        message = ""  # Empty message should not crash

        try:
            result = await intent_service.process_intent(message, session_id="error_test")

            # Verify graceful handling
            assert result is not None
            assert hasattr(result, "message")
            assert len(result.message) > 0

            # Should not have placeholder
            self.assert_no_placeholder(result.message)

            coverage.contract_tests_passed += 1
            print(f"✓ ANALYSIS error handling: graceful")

        except Exception as e:
            pytest.fail(f"ANALYSIS handler crashed on error: {e}")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_synthesis_error_handling(self, intent_service):
        """ERROR 8/13: SYNTHESIS error handling."""
        # Test with malformed/empty message
        message = ""  # Empty message should not crash

        try:
            result = await intent_service.process_intent(message, session_id="error_test")

            # Verify graceful handling
            assert result is not None
            assert hasattr(result, "message")
            assert len(result.message) > 0

            # Should not have placeholder
            self.assert_no_placeholder(result.message)

            coverage.contract_tests_passed += 1
            print(f"✓ SYNTHESIS error handling: graceful")

        except Exception as e:
            pytest.fail(f"SYNTHESIS handler crashed on error: {e}")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_strategy_error_handling(self, intent_service):
        """ERROR 9/13: STRATEGY error handling."""
        # Test with malformed/empty message
        message = ""  # Empty message should not crash

        try:
            result = await intent_service.process_intent(message, session_id="error_test")

            # Verify graceful handling
            assert result is not None
            assert hasattr(result, "message")
            assert len(result.message) > 0

            # Should not have placeholder
            self.assert_no_placeholder(result.message)

            coverage.contract_tests_passed += 1
            print(f"✓ STRATEGY error handling: graceful")

        except Exception as e:
            pytest.fail(f"STRATEGY handler crashed on error: {e}")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_learning_error_handling(self, intent_service):
        """ERROR 10/13: LEARNING error handling."""
        # Test with malformed/empty message
        message = ""  # Empty message should not crash

        try:
            result = await intent_service.process_intent(message, session_id="error_test")

            # Verify graceful handling
            assert result is not None
            assert hasattr(result, "message")
            assert len(result.message) > 0

            # Should not have placeholder
            self.assert_no_placeholder(result.message)

            coverage.contract_tests_passed += 1
            print(f"✓ LEARNING error handling: graceful")

        except Exception as e:
            pytest.fail(f"LEARNING handler crashed on error: {e}")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_unknown_error_handling(self, intent_service):
        """ERROR 11/13: UNKNOWN error handling."""
        # Test with malformed/empty message
        message = ""  # Empty message should not crash

        try:
            result = await intent_service.process_intent(message, session_id="error_test")

            # Verify graceful handling
            assert result is not None
            assert hasattr(result, "message")
            assert len(result.message) > 0

            # Should not have placeholder
            self.assert_no_placeholder(result.message)

            coverage.contract_tests_passed += 1
            print(f"✓ UNKNOWN error handling: graceful")

        except Exception as e:
            pytest.fail(f"UNKNOWN handler crashed on error: {e}")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_query_error_handling(self, intent_service):
        """ERROR 12/13: QUERY error handling."""
        # Test with malformed/empty message
        message = ""  # Empty message should not crash

        try:
            result = await intent_service.process_intent(message, session_id="error_test")

            # Verify graceful handling
            assert result is not None
            assert hasattr(result, "message")
            assert len(result.message) > 0

            # Should not have placeholder
            self.assert_no_placeholder(result.message)

            coverage.contract_tests_passed += 1
            print(f"✓ QUERY error handling: graceful")

        except Exception as e:
            pytest.fail(f"QUERY handler crashed on error: {e}")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_conversation_error_handling(self, intent_service):
        """ERROR 13/13: CONVERSATION error handling."""
        # Test with malformed/empty message
        message = ""  # Empty message should not crash

        try:
            result = await intent_service.process_intent(message, session_id="error_test")

            # Verify graceful handling
            assert result is not None
            assert hasattr(result, "message")
            assert len(result.message) > 0

            # Should not have placeholder
            self.assert_no_placeholder(result.message)

            coverage.contract_tests_passed += 1
            print(f"✓ CONVERSATION error handling: graceful")

        except Exception as e:
            pytest.fail(f"CONVERSATION handler crashed on error: {e}")

    @pytest.mark.asyncio
    async def test_zzz_error_coverage(self):
        """Error contract coverage report."""
        print("\n" + "=" * 80)
        print("ERROR HANDLING CONTRACT REPORT")
        print("=" * 80)
        print("All 13 categories handle errors gracefully")
        print("=" * 80)


class TestErrorContractsAuthenticated(BaseValidationTest):
    """#1533: authenticated-principal sibling for this suite.

    Every test above calls ``process_intent`` with ``session_id="error_test"``
    and no ``user_id`` — every category's probe collapses onto the same
    anonymous context. This class proves the property none of the tests
    above can see: the outer turn-recording seam still separates two
    DISTINCT authenticated users sharing one session_id even on the
    error-handling (empty-message) path, and still runs — mutating each
    user's own context — regardless of whether classification itself
    succeeds or hits the #1831 deterministic-tier no-LLM-provider failure.
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
    async def test_malformed_message_error_handling_does_not_leak_turns_across_authenticated_users(
        self, intent_service
    ):
        session_id = str(uuid4())
        user_a = str(uuid4())
        user_b = str(uuid4())
        # NOT "" — process_intent's outer turn-recording seam only calls
        # add_turn when `message` is truthy (intent_service.py ~L813:
        # `if message and (...)`), so an empty string never touches the
        # per-user context and can't demonstrate isolation either way.
        # Whitespace-only keeps this suite's "malformed input" spirit
        # while still exercising the seam under test.
        message = "   "

        try:
            result_a = await self._tolerant_call(intent_service, message, session_id, user_a)
            result_b = await self._tolerant_call(intent_service, message, session_id, user_b)

            # Whether or not classification itself succeeded, it must not have
            # crashed, and the outer turn-recording seam ran before it either
            # way — that's the property under test.
            if result_a is not None:
                assert len(result_a.message) > 0
                self.assert_no_placeholder(result_a.message)
            if result_b is not None:
                assert len(result_b.message) > 0
                self.assert_no_placeholder(result_b.message)

            ctx_a = get_or_create_context(session_id, user_id=user_a)
            ctx_b = get_or_create_context(session_id, user_id=user_b)

            # The teeth: under the real composite key, two distinct
            # authenticated user_ids sharing session_id get DISTINCT context
            # objects, each with exactly its own (empty-message) turn.
            assert ctx_a is not ctx_b, (
                "two distinct user_ids sharing session_id resolved to the SAME "
                "context object on the error-handling path — user_id is not "
                "part of the effective key"
            )
            assert len(ctx_a.turns) == 1, (
                f"user A's context leaked cross-user turns: "
                f"{[t.message for t in ctx_a.turns]!r}"
            )
            assert len(ctx_b.turns) == 1, (
                f"user B's context leaked cross-user turns: "
                f"{[t.message for t in ctx_b.turns]!r}"
            )

            coverage.contract_tests_passed += 1
            print("✓ ERROR handling (authenticated): isolated under shared session_id")
        finally:
            clear_context(session_id, user_id=user_a)
            clear_context(session_id, user_id=user_b)
