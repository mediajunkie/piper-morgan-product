"""Multi-user contract tests for all 13 intent categories - GREAT-4E Phase 3

#1533 (principal-dropping audit, 2026-08-08): the 13 ``test_*_multiuser``
contracts below were the audit's named worst offender — 26 ``process_intent``
calls, zero of which ever passed a non-None ``user_id``. Each contract
differentiates its two calls by ``session_id`` only (``"user1"``/``"user2"``),
so both resolve to the ``anonymous:`` half of the composite registry key
(``f"{user_id or 'anonymous'}:{session_id}"``, #817) — isolation there is
proven by the DIFFERENT session_id, never by the user_id half of the key.
That means this suite could not have caught the #1394 defect class (a
handler drops user_id internally and silently reads/writes the anonymous
context for an authenticated user) even though every one of these tests is
named and printed as a "user isolation" contract.

``TestMultiUserContractsAuthenticated`` below adds one authenticated sibling
per category: two DISTINCT non-None user_ids (uuid4) sharing the SAME
session_id — the shape that actually depends on user_id being threaded
through, since a dropped user_id collapses both principals onto one
composite key. Teeth verified by temporarily forcing the two user_ids equal
(see session log dev/2026/09/23/2026-09-23-*-prog-code-1533-log.md): the
turn-count assertion FAILS (not vacuous) when the ids coincide.

**Standing review rule (audit's TEST-BLIND section)**: any new test of a
``{user_id or 'anonymous'}:{session_id}``-keyed surface must assert at
least once under a non-None user_id — a probe where the keys coincide is a
config check, not a verification (m-44).
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

# Categories whose CATEGORY_EXAMPLES message the deterministic pre-classifier
# (Stage 1, classifier.py) resolves WITHOUT reaching the LLM at all — the
# other 7 fall through to Stage 2 (LLM classification), which the #1831
# unmarked-tier stub deliberately fails with "No LLM providers configured."
# For those 7, process_intent's OUTER turn-recording seam (get_or_create_
# context + add_turn, intent_service.py ~L765-819) still runs and mutates
# the per-user context BEFORE the classifier is reached and raises — so the
# property under test (does the composite key separate the two users?) is
# still provable, we just can't also assert result.success for that half.
_PRE_CLASSIFIED_DETERMINISTICALLY = {
    "TEMPORAL",
    "STATUS",
    "PRIORITY",
    "IDENTITY",
    "GUIDANCE",
    "CONVERSATION",
}


class TestMultiUserContracts(BaseValidationTest):
    """Verify multi-user support for all categories."""

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_temporal_multiuser(self, intent_service):
        """MULTI 1/13: TEMPORAL user isolation."""
        message = CATEGORY_EXAMPLES["TEMPORAL"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ TEMPORAL multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_status_multiuser(self, intent_service):
        """MULTI 2/13: STATUS user isolation."""
        message = CATEGORY_EXAMPLES["STATUS"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ STATUS multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_priority_multiuser(self, intent_service):
        """MULTI 3/13: PRIORITY user isolation."""
        message = CATEGORY_EXAMPLES["PRIORITY"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ PRIORITY multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_identity_multiuser(self, intent_service):
        """MULTI 4/13: IDENTITY user isolation."""
        message = CATEGORY_EXAMPLES["IDENTITY"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ IDENTITY multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_guidance_multiuser(self, intent_service):
        """MULTI 5/13: GUIDANCE user isolation."""
        message = CATEGORY_EXAMPLES["GUIDANCE"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ GUIDANCE multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_execution_multiuser(self, intent_service):
        """MULTI 6/13: EXECUTION user isolation."""
        message = CATEGORY_EXAMPLES["EXECUTION"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ EXECUTION multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_analysis_multiuser(self, intent_service):
        """MULTI 7/13: ANALYSIS user isolation."""
        message = CATEGORY_EXAMPLES["ANALYSIS"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ ANALYSIS multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_synthesis_multiuser(self, intent_service):
        """MULTI 8/13: SYNTHESIS user isolation."""
        message = CATEGORY_EXAMPLES["SYNTHESIS"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ SYNTHESIS multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_strategy_multiuser(self, intent_service):
        """MULTI 9/13: STRATEGY user isolation."""
        message = CATEGORY_EXAMPLES["STRATEGY"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ STRATEGY multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_learning_multiuser(self, intent_service):
        """MULTI 10/13: LEARNING user isolation."""
        message = CATEGORY_EXAMPLES["LEARNING"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ LEARNING multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_unknown_multiuser(self, intent_service):
        """MULTI 11/13: UNKNOWN user isolation."""
        message = CATEGORY_EXAMPLES["UNKNOWN"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ UNKNOWN multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_query_multiuser(self, intent_service):
        """MULTI 12/13: QUERY user isolation."""
        message = CATEGORY_EXAMPLES["QUERY"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ QUERY multi-user: isolated")

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_conversation_multiuser(self, intent_service):
        """MULTI 13/13: CONVERSATION user isolation."""
        message = CATEGORY_EXAMPLES["CONVERSATION"]

        # Process for user 1
        result1 = await intent_service.process_intent(message, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process_intent(message, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        assert result1.message is not None
        assert result2.message is not None

        coverage.contract_tests_passed += 1
        print(f"✓ CONVERSATION multi-user: isolated")

    @pytest.mark.asyncio
    async def test_zzz_multiuser_coverage(self):
        """Multi-user contract coverage report."""
        print("\n" + "=" * 80)
        print("MULTI-USER CONTRACT REPORT")
        print("=" * 80)
        print("All 13 categories support session isolation")
        print("=" * 80)


class TestMultiUserContractsAuthenticated(BaseValidationTest):
    """#1533: authenticated-principal siblings for every category above.

    Unmarked (no ``@pytest.mark.llm``) — these run against the deterministic
    classifier tier pinned by ``tests/intent/conftest.py`` (#1831), not live
    LLM calls. That's deliberate: the property under test lives entirely in
    ``IntentService.process_intent``'s outer turn-recording seam
    (``get_or_create_context`` + ``conv_ctx.add_turn``, intent_service.py
    ~L765-819), which runs identically regardless of which classifier tier
    resolved the category — the deterministic degrade path exercises it
    exactly as well as a real LLM call would, for a fraction of the cost.

    Each test drives two DISTINCT non-None user_ids through the SAME
    session_id — the one shape that depends on user_id actually being part
    of the composite key. If a handler ever drops user_id internally (the
    #1394 defect class), both principals collapse onto the same
    ``anonymous:{session_id}`` (or worse, matching non-anonymous) key and
    each user's turn list would contain the other's turn.
    """

    async def _call_process_intent_tolerant(self, intent_service, message, session_id, user_id):
        """Real process_intent, tolerating ONLY the expected #1831 no-LLM-
        provider failure for categories that fall through to Stage-2
        classification. The outer turn-recording seam already ran (and
        mutated the per-user context we assert on) before that failure —
        see module docstring. Anything else re-raises."""
        try:
            return await intent_service.process_intent(
                message, session_id=session_id, user_id=user_id
            )
        except (IntentProcessingError, IntentClassificationFailedError) as e:
            # #1824: the informative cause lives in .details["original_error"],
            # not str(e) (which is just "Intent processing failed: API Error
            # [INTENT_CLASSIFICATION_FAILED]" for IntentProcessingError, or
            # "API Error [INTENT_CLASSIFICATION_FAILED]" for the classifier's
            # own error) — check both so we don't silently swallow anything
            # other than the specific #1831 no-provider failure.
            details = getattr(e, "details", None) or {}
            cause = str(details.get("original_error", "")) or str(e)
            if "No LLM providers configured" not in cause:
                raise
            return None

    async def _assert_authenticated_users_do_not_leak_turns(self, intent_service, category: str):
        session_id = str(uuid4())
        user_a = str(uuid4())
        user_b = str(uuid4())
        message = CATEGORY_EXAMPLES[category]

        try:
            result_a = await self._call_process_intent_tolerant(
                intent_service, message, session_id, user_a
            )
            result_b = await self._call_process_intent_tolerant(
                intent_service, message, session_id, user_b
            )

            if category in _PRE_CLASSIFIED_DETERMINISTICALLY:
                # Both should succeed (mirrors the original contract's shape).
                assert result_a is not None and result_a.success is not None
                assert result_b is not None and result_b.success is not None
            else:
                # Stage-2 (LLM) categories: classification itself fails
                # deterministically under the #1831 stub — that's the
                # expected, tolerated outcome, not this test's property.
                assert result_a is None and result_b is None, (
                    f"{category}: expected the deterministic-tier no-LLM "
                    "failure for this Stage-2 category, but process_intent "
                    "returned a result — CATEGORY_EXAMPLES or the "
                    "pre-classifier may have changed; update "
                    "_PRE_CLASSIFIED_DETERMINISTICALLY"
                )

            ctx_a = get_or_create_context(session_id, user_id=user_a)
            ctx_b = get_or_create_context(session_id, user_id=user_b)

            # The teeth: under the real composite key, two distinct user_ids
            # sharing one session_id get DISTINCT context objects, and
            # neither one's turn list contains the other's turn. If the
            # user_id half of the key were ever dropped, both principals
            # would resolve to the same context and this would see 2 turns
            # (or the wrong message) instead of 1.
            assert ctx_a is not ctx_b, (
                f"{category}: two distinct user_ids sharing session_id "
                f"{session_id!r} resolved to the SAME context object — "
                "user_id is not part of the effective key"
            )
            assert len(ctx_a.turns) == 1 and ctx_a.turns[0].message == message, (
                f"{category}: user A's context leaked cross-user turns "
                f"under a shared session_id: {[t.message for t in ctx_a.turns]!r}"
            )
            assert len(ctx_b.turns) == 1 and ctx_b.turns[0].message == message, (
                f"{category}: user B's context leaked cross-user turns "
                f"under a shared session_id: {[t.message for t in ctx_b.turns]!r}"
            )

            coverage.contract_tests_passed += 1
            print(f"✓ {category} multi-user (authenticated): isolated under shared session_id")
        finally:
            clear_context(session_id, user_id=user_a)
            clear_context(session_id, user_id=user_b)

    @pytest.mark.asyncio
    async def test_temporal_multiuser_authenticated(self, intent_service):
        """MULTI 1/13 (authenticated): TEMPORAL."""
        await self._assert_authenticated_users_do_not_leak_turns(intent_service, "TEMPORAL")

    @pytest.mark.asyncio
    async def test_status_multiuser_authenticated(self, intent_service):
        """MULTI 2/13 (authenticated): STATUS."""
        await self._assert_authenticated_users_do_not_leak_turns(intent_service, "STATUS")

    @pytest.mark.asyncio
    async def test_priority_multiuser_authenticated(self, intent_service):
        """MULTI 3/13 (authenticated): PRIORITY."""
        await self._assert_authenticated_users_do_not_leak_turns(intent_service, "PRIORITY")

    @pytest.mark.asyncio
    async def test_identity_multiuser_authenticated(self, intent_service):
        """MULTI 4/13 (authenticated): IDENTITY."""
        await self._assert_authenticated_users_do_not_leak_turns(intent_service, "IDENTITY")

    @pytest.mark.asyncio
    async def test_guidance_multiuser_authenticated(self, intent_service):
        """MULTI 5/13 (authenticated): GUIDANCE."""
        await self._assert_authenticated_users_do_not_leak_turns(intent_service, "GUIDANCE")

    @pytest.mark.asyncio
    async def test_execution_multiuser_authenticated(self, intent_service):
        """MULTI 6/13 (authenticated): EXECUTION."""
        await self._assert_authenticated_users_do_not_leak_turns(intent_service, "EXECUTION")

    @pytest.mark.asyncio
    async def test_analysis_multiuser_authenticated(self, intent_service):
        """MULTI 7/13 (authenticated): ANALYSIS."""
        await self._assert_authenticated_users_do_not_leak_turns(intent_service, "ANALYSIS")

    @pytest.mark.asyncio
    async def test_synthesis_multiuser_authenticated(self, intent_service):
        """MULTI 8/13 (authenticated): SYNTHESIS."""
        await self._assert_authenticated_users_do_not_leak_turns(intent_service, "SYNTHESIS")

    @pytest.mark.asyncio
    async def test_strategy_multiuser_authenticated(self, intent_service):
        """MULTI 9/13 (authenticated): STRATEGY."""
        await self._assert_authenticated_users_do_not_leak_turns(intent_service, "STRATEGY")

    @pytest.mark.asyncio
    async def test_learning_multiuser_authenticated(self, intent_service):
        """MULTI 10/13 (authenticated): LEARNING."""
        await self._assert_authenticated_users_do_not_leak_turns(intent_service, "LEARNING")

    @pytest.mark.asyncio
    async def test_unknown_multiuser_authenticated(self, intent_service):
        """MULTI 11/13 (authenticated): UNKNOWN."""
        await self._assert_authenticated_users_do_not_leak_turns(intent_service, "UNKNOWN")

    @pytest.mark.asyncio
    async def test_query_multiuser_authenticated(self, intent_service):
        """MULTI 12/13 (authenticated): QUERY."""
        await self._assert_authenticated_users_do_not_leak_turns(intent_service, "QUERY")

    @pytest.mark.asyncio
    async def test_conversation_multiuser_authenticated(self, intent_service):
        """MULTI 13/13 (authenticated): CONVERSATION."""
        await self._assert_authenticated_users_do_not_leak_turns(intent_service, "CONVERSATION")

    @pytest.mark.asyncio
    async def test_zzz_multiuser_authenticated_coverage(self):
        """Authenticated multi-user contract coverage report."""
        print("\n" + "=" * 80)
        print("MULTI-USER CONTRACT REPORT (authenticated siblings, #1533)")
        print("=" * 80)
        print("All 13 categories verified under two distinct non-None user_ids")
        print("sharing one session_id — the shape that depends on user_id")
        print("actually being part of the composite registry key.")
        print("=" * 80)
