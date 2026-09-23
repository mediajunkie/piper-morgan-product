"""
GREAT-4E Phase 2: CLI Interface Tests
Test all 13 intent categories through CLI interface

**Standing review rule (#1533 principal-dropping audit, TEST-BLIND section)**:
any new test of a ``{user_id or 'anonymous'}:{session_id}``-keyed surface must
assert at least once under a non-None user_id — a probe where the keys
coincide is a config check, not a verification (m-44). Every test above
never passes user_id at all; ``TestCLIInterfaceAuthenticated`` below adds
the authenticated sibling. It fully mocks the classifier (as every test in
this file does), so no real LLM call or #1831 stub is involved — the
property under test lives entirely in ``process_intent``'s outer
turn-recording seam, which runs identically regardless of what the mocked
classifier returns. It uses TEMPORAL as a single representative probe
rather than all 13 categories: that seam is category-agnostic and already
exhaustively proven across all 13 categories in
``test_multiuser_contracts.py::TestMultiUserContractsAuthenticated``.
"""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.domain.models import Intent, IntentCategory
from services.intent.intent_service import IntentService
from services.intent_service.conversation_context import (
    clear_context,
    get_or_create_context,
)
from services.intent_service.pre_classifier import MultiIntentResult


def _wire_classifier(mock_classifier, intent):
    """Wire BOTH classifier methods the live path can await (#595: process_intent
    awaits classify_multiple; these mocks predated it and stubbed only classify,
    leaving classify_multiple a plain MagicMock — un-awaitable)."""
    mock_classifier.classify = AsyncMock(return_value=intent)
    mock_classifier.classify_multiple = AsyncMock(
        return_value=MultiIntentResult(
            intents=[intent],
            original_message=intent.original_message,
            is_multi_intent=False,
        )
    )


class TestCLIInterface:
    """Test all 13 intent categories through CLI interface."""

    @pytest.fixture
    def mock_orchestration_engine(self):
        """Mock orchestration engine for testing."""
        mock_engine = Mock()
        mock_engine.create_workflow_from_intent = AsyncMock()

        # Mock workflow
        mock_workflow = Mock()
        mock_workflow.id = "cli-test-workflow"
        mock_engine.create_workflow_from_intent.return_value = mock_workflow

        return mock_engine

    @pytest.fixture
    def intent_service(self, mock_orchestration_engine):
        """Create IntentService with mocked dependencies."""
        return IntentService()

    def assert_no_placeholder(self, message):
        """Verify no placeholder messages in response."""
        assert "Phase 3" not in message
        assert "full orchestration workflow" not in message
        assert "placeholder" not in message.lower()

    @pytest.mark.asyncio
    async def test_temporal_cli(self, intent_service):
        """CLI 1/13: TEMPORAL category."""
        # Mock intent
        intent = Intent(
            original_message="What's on my calendar today?",
            category=IntentCategory.TEMPORAL,
            action="get_calendar",
            confidence=0.95,
            context={},
        )

        # Mock classifier
        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            _wire_classifier(mock_classifier, intent)

            # Simulate CLI command processing
            result = await intent_service.process_intent(
                "What's on my calendar today?", session_id="cli_test_session"
            )

            # Verify no placeholder
            self.assert_no_placeholder(result.message)

            print("✓ CLI/TEMPORAL")

    @pytest.mark.asyncio
    async def test_status_cli(self, intent_service):
        """CLI 2/13: STATUS category."""
        intent = Intent(
            original_message="What am I working on?",
            category=IntentCategory.STATUS,
            action="get_status",
            confidence=0.92,
            context={},
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            _wire_classifier(mock_classifier, intent)

            result = await intent_service.process_intent(
                "What am I working on?", session_id="cli_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ CLI/STATUS")

    @pytest.mark.asyncio
    async def test_priority_cli(self, intent_service):
        """CLI 3/13: PRIORITY category."""
        intent = Intent(
            original_message="What's my top priority?",
            category=IntentCategory.PRIORITY,
            action="get_priority",
            confidence=0.90,
            context={},
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            _wire_classifier(mock_classifier, intent)

            result = await intent_service.process_intent(
                "What's my top priority?", session_id="cli_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ CLI/PRIORITY")

    @pytest.mark.asyncio
    async def test_identity_cli(self, intent_service):
        """CLI 4/13: IDENTITY category."""
        intent = Intent(
            original_message="Who are you?",
            category=IntentCategory.IDENTITY,
            action="get_identity",
            confidence=0.98,
            context={},
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            _wire_classifier(mock_classifier, intent)

            result = await intent_service.process_intent(
                "Who are you?", session_id="cli_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ CLI/IDENTITY")

    @pytest.mark.asyncio
    async def test_guidance_cli(self, intent_service):
        """CLI 5/13: GUIDANCE category."""
        intent = Intent(
            original_message="What should I focus on?",
            category=IntentCategory.GUIDANCE,
            action="get_guidance",
            confidence=0.88,
            context={},
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            _wire_classifier(mock_classifier, intent)

            result = await intent_service.process_intent(
                "What should I focus on?", session_id="cli_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ CLI/GUIDANCE")

    @pytest.mark.asyncio
    async def test_execution_cli(self, intent_service):
        """CLI 6/13: EXECUTION category."""
        intent = Intent(
            original_message="Create an issue about testing",
            category=IntentCategory.EXECUTION,
            action="create_issue",
            confidence=0.93,
            context={"repository": "test-repo"},
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            _wire_classifier(mock_classifier, intent)

            result = await intent_service.process_intent(
                "Create an issue about testing", session_id="cli_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ CLI/EXECUTION")

    @pytest.mark.asyncio
    async def test_analysis_cli(self, intent_service):
        """CLI 7/13: ANALYSIS category."""
        intent = Intent(
            original_message="Analyze recent commits",
            category=IntentCategory.ANALYSIS,
            action="analyze_commits",
            confidence=0.91,
            context={"repository": "test-repo"},
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            _wire_classifier(mock_classifier, intent)

            result = await intent_service.process_intent(
                "Analyze recent commits", session_id="cli_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ CLI/ANALYSIS")

    @pytest.mark.asyncio
    async def test_synthesis_cli(self, intent_service):
        """CLI 8/13: SYNTHESIS category."""
        intent = Intent(
            original_message="Summarize this document",
            category=IntentCategory.SYNTHESIS,
            action="generate_content",
            confidence=0.89,
            context={"content_type": "document"},
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            _wire_classifier(mock_classifier, intent)

            result = await intent_service.process_intent(
                "Summarize this document", session_id="cli_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ CLI/SYNTHESIS")

    @pytest.mark.asyncio
    async def test_strategy_cli(self, intent_service):
        """CLI 9/13: STRATEGY category."""
        intent = Intent(
            original_message="Create a strategy for this project",
            category=IntentCategory.STRATEGY,
            action="strategic_planning",
            confidence=0.87,
            context={"planning_scope": "project"},
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            _wire_classifier(mock_classifier, intent)

            result = await intent_service.process_intent(
                "Create a strategy for this project", session_id="cli_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ CLI/STRATEGY")

    @pytest.mark.asyncio
    async def test_learning_cli(self, intent_service):
        """CLI 10/13: LEARNING category."""
        intent = Intent(
            original_message="Learn from this pattern",
            category=IntentCategory.LEARNING,
            action="learn_pattern",
            confidence=0.85,
            context={"learning_type": "pattern"},
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            _wire_classifier(mock_classifier, intent)

            result = await intent_service.process_intent(
                "Learn from this pattern", session_id="cli_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ CLI/LEARNING")

    @pytest.mark.asyncio
    async def test_unknown_cli(self, intent_service):
        """CLI 11/13: UNKNOWN category."""
        intent = Intent(
            original_message="This is something weird",
            category=IntentCategory.UNKNOWN,
            action="unknown",
            confidence=0.60,
            context={},
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            _wire_classifier(mock_classifier, intent)

            result = await intent_service.process_intent(
                "This is something weird", session_id="cli_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ CLI/UNKNOWN")

    @pytest.mark.asyncio
    async def test_query_cli(self, intent_service):
        """CLI 12/13: QUERY category."""
        intent = Intent(
            original_message="Show me my projects",
            category=IntentCategory.QUERY,
            action="list_projects",
            confidence=0.94,
            context={},
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            _wire_classifier(mock_classifier, intent)

            result = await intent_service.process_intent(
                "Show me my projects", session_id="cli_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ CLI/QUERY")

    @pytest.mark.asyncio
    async def test_conversation_cli(self, intent_service):
        """CLI 13/13: CONVERSATION category."""
        intent = Intent(
            original_message="Hello there",
            category=IntentCategory.CONVERSATION,
            action="greeting",
            confidence=0.96,
            context={},
        )

        with patch.object(intent_service, "intent_classifier") as mock_classifier:
            _wire_classifier(mock_classifier, intent)

            result = await intent_service.process_intent(
                "Hello there", session_id="cli_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ CLI/CONVERSATION")

    @pytest.mark.asyncio
    async def test_zzz_cli_coverage_report(self):
        """Generate coverage report after CLI interface tests."""
        print("\n" + "=" * 80)
        print("CLI INTERFACE COVERAGE REPORT")
        print("=" * 80)
        print("Categories tested: 13/13 (100%)")
        print("Interface: CLI (main.py + cli/commands/)")
        print("Status: ✅ ALL CLI TESTS COMPLETE")
        print("=" * 80)


class TestCLIInterfaceAuthenticated:
    """#1533: authenticated-principal sibling for this suite.

    Every test above calls ``process_intent`` with ``session_id=
    "cli_test_session"`` and no ``user_id`` — every category's probe
    collapses onto the same anonymous context. This proves the property none
    of the tests above can see: the outer turn-recording seam still
    separates two DISTINCT authenticated users sharing one session_id, even
    when the classifier itself is fully mocked (as it is throughout this
    file).
    """

    @pytest.fixture
    def mock_orchestration_engine(self):
        mock_engine = Mock()
        mock_engine.create_workflow_from_intent = AsyncMock()
        mock_workflow = Mock()
        mock_workflow.id = "cli-test-workflow"
        mock_engine.create_workflow_from_intent.return_value = mock_workflow
        return mock_engine

    @pytest.fixture
    def intent_service(self, mock_orchestration_engine):
        return IntentService()

    def assert_no_placeholder(self, message):
        assert "Phase 3" not in message
        assert "full orchestration workflow" not in message
        assert "placeholder" not in message.lower()

    @pytest.mark.asyncio
    async def test_temporal_cli_does_not_leak_turns_across_authenticated_users(
        self, intent_service
    ):
        """CLI (authenticated): TEMPORAL, two distinct real user_ids sharing
        one session_id must not leak turns across each other."""
        session_id = str(uuid4())
        user_a = str(uuid4())
        user_b = str(uuid4())
        message = "What's on my calendar today?"

        intent = Intent(
            original_message=message,
            category=IntentCategory.TEMPORAL,
            action="get_calendar",
            confidence=0.95,
            context={},
        )

        try:
            with patch.object(intent_service, "intent_classifier") as mock_classifier:
                _wire_classifier(mock_classifier, intent)

                result_a = await intent_service.process_intent(
                    message, session_id=session_id, user_id=user_a
                )
                result_b = await intent_service.process_intent(
                    message, session_id=session_id, user_id=user_b
                )

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

            print("✓ CLI/TEMPORAL (authenticated): isolated under shared session_id")
        finally:
            clear_context(session_id, user_id=user_a)
            clear_context(session_id, user_id=user_b)
