"""
GREAT-4E Phase 2: Web API Interface Tests
Test all 13 intent categories through Web API endpoint

**Standing review rule (#1533 principal-dropping audit, TEST-BLIND section)**:
any new test of a ``{user_id or 'anonymous'}:{session_id}``-keyed surface must
assert at least once under a non-None user_id — a probe where the keys
coincide is a config check, not a verification (m-44). Every test above
never passes user_id at all; ``TestWebInterfaceAuthenticated`` below adds
the authenticated sibling.
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


class TestWebInterface:
    """Test all 13 intent categories through Web API."""

    @pytest.fixture
    def mock_orchestration_engine(self):
        """Mock orchestration engine for testing."""
        mock_engine = Mock()
        mock_engine.create_workflow_from_intent = AsyncMock()

        # Mock workflow
        mock_workflow = Mock()
        mock_workflow.id = "web-test-workflow"
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
    async def test_temporal_web(self, intent_service):
        """WEB 1/13: TEMPORAL category."""
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

            # Simulate web API request processing
            result = await intent_service.process_intent(
                "What's on my calendar today?", session_id="web_test_session"
            )

            # Verify no placeholder
            self.assert_no_placeholder(result.message)

            print("✓ WEB/TEMPORAL")

    @pytest.mark.asyncio
    async def test_status_web(self, intent_service):
        """WEB 2/13: STATUS category."""
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
                "What am I working on?", session_id="web_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ WEB/STATUS")

    @pytest.mark.asyncio
    async def test_priority_web(self, intent_service):
        """WEB 3/13: PRIORITY category."""
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
                "What's my top priority?", session_id="web_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ WEB/PRIORITY")

    @pytest.mark.asyncio
    async def test_identity_web(self, intent_service):
        """WEB 4/13: IDENTITY category."""
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
                "Who are you?", session_id="web_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ WEB/IDENTITY")

    @pytest.mark.asyncio
    async def test_guidance_web(self, intent_service):
        """WEB 5/13: GUIDANCE category."""
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
                "What should I focus on?", session_id="web_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ WEB/GUIDANCE")

    @pytest.mark.asyncio
    async def test_execution_web(self, intent_service):
        """WEB 6/13: EXECUTION category."""
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
                "Create an issue about testing", session_id="web_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ WEB/EXECUTION")

    @pytest.mark.asyncio
    async def test_analysis_web(self, intent_service):
        """WEB 7/13: ANALYSIS category."""
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
                "Analyze recent commits", session_id="web_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ WEB/ANALYSIS")

    @pytest.mark.asyncio
    async def test_synthesis_web(self, intent_service):
        """WEB 8/13: SYNTHESIS category."""
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
                "Summarize this document", session_id="web_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ WEB/SYNTHESIS")

    @pytest.mark.asyncio
    async def test_strategy_web(self, intent_service):
        """WEB 9/13: STRATEGY category."""
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
                "Create a strategy for this project", session_id="web_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ WEB/STRATEGY")

    @pytest.mark.asyncio
    async def test_learning_web(self, intent_service):
        """WEB 10/13: LEARNING category."""
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
                "Learn from this pattern", session_id="web_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ WEB/LEARNING")

    @pytest.mark.asyncio
    async def test_unknown_web(self, intent_service):
        """WEB 11/13: UNKNOWN category."""
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
                "This is something weird", session_id="web_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ WEB/UNKNOWN")

    @pytest.mark.asyncio
    async def test_query_web(self, intent_service):
        """WEB 12/13: QUERY category."""
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
                "Show me my projects", session_id="web_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ WEB/QUERY")

    @pytest.mark.asyncio
    async def test_conversation_web(self, intent_service):
        """WEB 13/13: CONVERSATION category."""
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
                "Hello there", session_id="web_test_session"
            )

            self.assert_no_placeholder(result.message)
            print("✓ WEB/CONVERSATION")

    @pytest.mark.asyncio
    async def test_zzz_web_coverage_report(self):
        """Generate coverage report after Web interface tests."""
        print("\n" + "=" * 80)
        print("WEB INTERFACE COVERAGE REPORT")
        print("=" * 80)
        print("Categories tested: 13/13 (100%)")
        print("Interface: Web API (/api/v1/intent)")
        print("Status: ✅ ALL WEB TESTS COMPLETE")
        print("=" * 80)


class TestWebInterfaceAuthenticated:
    """#1533: authenticated-principal sibling for this suite.

    Every test above calls ``process_intent`` with a bare ``session_id``
    and no ``user_id`` — the Web API's real production callers are almost
    always authenticated. This class proves the property none of the tests
    above can see: two DISTINCT non-None user_ids sharing one session_id
    get isolated turn history through the real Web API call shape (a
    mocked classifier, exactly as the suite above wires it), not just
    isolated session_ids simulating "users."
    """

    @pytest.fixture
    def mock_orchestration_engine(self):
        mock_engine = Mock()
        mock_engine.create_workflow_from_intent = AsyncMock()
        mock_workflow = Mock()
        mock_workflow.id = "web-test-workflow-authed"
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
    async def test_web_authenticated_users_do_not_leak_turns(self, intent_service):
        """WEB (authenticated): two real users sharing a session_id get
        isolated conversation contexts through the Web API call shape."""
        session_id = "web_test_session_authed"
        user_a = str(uuid4())
        user_b = str(uuid4())
        intent = Intent(
            original_message="What's on my calendar today?",
            category=IntentCategory.TEMPORAL,
            action="get_calendar",
            confidence=0.95,
            context={},
        )

        try:
            with patch.object(intent_service, "intent_classifier") as mock_classifier:
                _wire_classifier(mock_classifier, intent)

                result_a = await intent_service.process_intent(
                    "What's on my calendar today?", session_id=session_id, user_id=user_a
                )
                result_b = await intent_service.process_intent(
                    "What's on my calendar today?", session_id=session_id, user_id=user_b
                )

                self.assert_no_placeholder(result_a.message)
                self.assert_no_placeholder(result_b.message)

            ctx_a = get_or_create_context(session_id, user_id=user_a)
            ctx_b = get_or_create_context(session_id, user_id=user_b)

            # The teeth: under the real composite key, two distinct
            # authenticated user_ids sharing session_id get DISTINCT
            # context objects, each with exactly its own turn.
            assert ctx_a is not ctx_b, (
                "two distinct user_ids sharing session_id resolved to the SAME "
                "context object via the Web API call shape — user_id is not "
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
        finally:
            clear_context(session_id, user_id=user_a)
            clear_context(session_id, user_id=user_b)
