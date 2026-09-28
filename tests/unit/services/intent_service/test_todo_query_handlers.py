"""
Unit tests for Todo Query Handlers (Issue #518 - Queries #56 and #57)

Tests the canonical query handlers for:
- Query #56: "Show my todos" - list todos
- Query #57: "What's my next todo?" - next todo recommendation
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import pytest

from services.domain.models import Intent, IntentCategory
from services.intent_service.todo_handlers import TodoIntentHandlers


class TestTodoQueryHandlers:
    """Test todo query handlers for canonical queries"""

    @pytest.fixture
    def handlers(self):
        """Create TodoIntentHandlers instance"""
        return TodoIntentHandlers()

    @pytest.fixture
    def mock_todo_service(self):
        """Create a mock TodoManagementService"""
        mock_service = MagicMock()
        mock_service.list_todos = AsyncMock(return_value=[])
        return mock_service

    # Query #56: "Show my todos" Tests
    @pytest.mark.asyncio
    async def test_list_todos_returns_formatted_list(self, handlers, mock_todo_service):
        """Test list_todos returns a formatted todo list with mock data"""
        # Create mock todos
        mock_todo_1 = MagicMock()
        mock_todo_1.text = "Review PR #285"
        mock_todo_1.completed = False
        mock_todo_1.priority = "high"

        mock_todo_2 = MagicMock()
        mock_todo_2.text = "Write documentation"
        mock_todo_2.completed = False
        mock_todo_2.priority = "medium"

        mock_todo_service.list_todos.return_value = [mock_todo_1, mock_todo_2]
        handlers.todo_service = mock_todo_service

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="list_todos",
            original_message="show my todos",
            confidence=0.9,
        )

        result = await handlers.handle_list_todos(
            intent, "session1", UUID("12345678-1234-5678-1234-567812345678")
        )

        # Verify result contains todo text
        assert "Review PR #285" in result
        assert "Write documentation" in result
        # Grammar-conscious formatting uses natural language (Issue #621, #633-638)
        assert "2 things" in result or "2 items" in result or "two" in result.lower()

    @pytest.mark.asyncio
    async def test_list_todos_handles_no_todos(self, handlers, mock_todo_service):
        """Test list_todos gracefully handles empty todo list"""
        mock_todo_service.list_todos.return_value = []
        handlers.todo_service = mock_todo_service

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="list_todos",
            original_message="show my todos",
            confidence=0.9,
        )

        result = await handlers.handle_list_todos(
            intent, "session1", UUID("12345678-1234-5678-1234-567812345678")
        )

        # Verify helpful message when no todos (grammar-conscious formatting)
        assert (
            "empty" in result.lower()
            or "no todos" in result.lower()
            or "don't have" in result.lower()
        )
        assert "add todo" in result.lower()

    # Query #57: "What's my next todo?" Tests
    @pytest.mark.asyncio
    async def test_next_todo_returns_highest_priority(self, handlers, mock_todo_service):
        """Test next_todo returns the highest priority todo (first in sorted list)"""
        # Create mock todos (already sorted by priority in service)
        mock_high_priority = MagicMock()
        mock_high_priority.text = "Fix critical bug"
        mock_high_priority.priority = "urgent"
        mock_high_priority.due_date = None
        mock_high_priority.context = None

        mock_low_priority = MagicMock()
        mock_low_priority.text = "Update readme"
        mock_low_priority.priority = "low"
        mock_low_priority.due_date = None
        mock_low_priority.context = None

        mock_todo_service.list_todos.return_value = [mock_high_priority, mock_low_priority]
        handlers.todo_service = mock_todo_service

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="next_todo",
            original_message="what's my next todo?",
            confidence=0.9,
        )

        result = await handlers.handle_next_todo(
            intent, "session1", UUID("12345678-1234-5678-1234-567812345678")
        )

        # Verify it returns the high priority todo, not the low priority one
        assert "Fix critical bug" in result
        assert "Update readme" not in result
        # Grammar-conscious formatting may use different phrasing (Issue #633-638)
        assert (
            "next" in result.lower() or "suggest" in result.lower() or "tackling" in result.lower()
        )

    @pytest.mark.asyncio
    async def test_next_todo_handles_no_todos(self, handlers, mock_todo_service):
        """Test next_todo gracefully handles empty todo list"""
        mock_todo_service.list_todos.return_value = []
        handlers.todo_service = mock_todo_service

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="next_todo",
            original_message="next task",
            confidence=0.9,
        )

        result = await handlers.handle_next_todo(
            intent, "session1", UUID("12345678-1234-5678-1234-567812345678")
        )

        # Verify helpful message when no todos (grammar-conscious formatting - Issue #633-638)
        assert "empty" in result.lower() or "no" in result.lower() or "nothing" in result.lower()
        assert "add todo" in result.lower()

    @pytest.mark.asyncio
    async def test_next_todo_includes_priority_icon(self, handlers, mock_todo_service):
        """Test next_todo includes priority icon in response"""
        # Test urgent priority
        mock_urgent = MagicMock()
        mock_urgent.text = "Critical task"
        mock_urgent.priority = "urgent"
        mock_urgent.due_date = None
        mock_urgent.context = None

        mock_todo_service.list_todos.return_value = [mock_urgent]
        handlers.todo_service = mock_todo_service

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="next_todo",
            original_message="what should I do next?",
            confidence=0.9,
        )

        result = await handlers.handle_next_todo(
            intent, "session1", UUID("12345678-1234-5678-1234-567812345678")
        )

        # Verify urgent priority is indicated (Issue #633-638 may use text instead of emoji)
        assert "Critical task" in result
        assert "urgent" in result.lower() or "🔴" in result

    @pytest.mark.asyncio
    async def test_next_todo_includes_due_date(self, handlers, mock_todo_service):
        """Test next_todo includes due date when present"""
        from datetime import datetime

        mock_todo = MagicMock()
        mock_todo.text = "Submit report"
        mock_todo.priority = "high"
        mock_todo.due_date = datetime(2025, 12, 31)
        mock_todo.context = None

        mock_todo_service.list_todos.return_value = [mock_todo]
        handlers.todo_service = mock_todo_service

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="next_todo",
            original_message="next task",
            confidence=0.9,
        )

        result = await handlers.handle_next_todo(
            intent, "session1", UUID("12345678-1234-5678-1234-567812345678")
        )

        # Verify due date is included (Issue #633-638 may use natural language for dates)
        assert "Submit report" in result
        # Accept "Due:" format or natural language like "due on December 31"
        assert "Due:" in result or "due" in result.lower()
        assert "2025-12-31" in result or "December 31" in result or "dec" in result.lower()

    @pytest.mark.asyncio
    async def test_next_todo_includes_context(self, handlers, mock_todo_service):
        """Test next_todo includes context when present"""
        mock_todo = MagicMock()
        mock_todo.text = "Review code"
        mock_todo.priority = "medium"
        mock_todo.due_date = None
        mock_todo.context = "PR #518 - Todo query handlers"

        mock_todo_service.list_todos.return_value = [mock_todo]
        handlers.todo_service = mock_todo_service

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="next_todo",
            original_message="what's next?",
            confidence=0.9,
        )

        result = await handlers.handle_next_todo(
            intent, "session1", UUID("12345678-1234-5678-1234-567812345678")
        )

        # Verify task is in result (Issue #633-638 grammar-conscious formatting may omit context label)
        assert "Review code" in result
        # Context may be omitted in natural language response or included with "Context:" label
        # The key verification is that the todo task itself is present


class TestPreClassifierRoutingIntegration:
    """Test full routing path from pre-classifier to handlers (Issue #521)

    #1595 Phase 3 (second deletion, 2026-09-27): TODO_QUERY_PATTERNS'
    literals were deleted (scripts/inversion_phase3_deleted_patterns.json)
    — surface 1 no longer claims these phrases. Every test below is a
    two-part pin: (a) surface 1 declines (the honest new fact), and (b) the
    Inversion routes it to the correct destination, deterministically (a
    stubbed router, never a live LLM call) — mirroring the conversion done
    for REMINDER_PATTERNS/REMINDER_QUERY_PATTERNS in
    test_reminder_query_preclassifier_1521.py. "what should I do next" is
    the one phrase ruled to a DIFFERENT destination (get_top_priority,
    CXO/PPM concurring, docs/internal/architecture/current/
    inversion-phase3-todo-query-rescore-2026-09-27.md) — every other
    variant routes to list_todos_query (the alias action names the old
    literals used to emit, e.g. next_todo_query/list_completed_todos, no
    longer surface anywhere; the corpus's own canonical destination is what
    the router names)."""

    @pytest.mark.asyncio
    async def test_list_todos_query_routes_to_query_category(self, monkeypatch):
        """Test 'show my todos' routes to QUERY category"""
        from services.intent_service.pre_classifier import PreClassifier
        from services.shared_types import IntentCategory
        from tests.unit.services.intent_service._inversion_pin_helper import (
            assert_inversion_routes,
        )

        result = PreClassifier.pre_classify("show my todos")
        assert result is None, (
            f"TODO_QUERY_PATTERNS is deleted — pre-classifier should no "
            f"longer claim 'show my todos' (got {result!r})"
        )
        routed = await assert_inversion_routes(
            monkeypatch,
            "show my todos",
            live_categories="read_status,create_reminder",
            expected_action="list_todos_query",
        )
        assert routed.category == IntentCategory.QUERY

    @pytest.mark.asyncio
    async def test_list_todos_query_variants(self, monkeypatch):
        """Test list todos query pattern variants all route correctly"""
        from services.intent_service.pre_classifier import PreClassifier
        from services.shared_types import IntentCategory
        from tests.unit.services.intent_service._inversion_pin_helper import (
            assert_inversion_routes,
        )

        test_cases = [
            "show my todos",
            "list my todos",
            "what are my todos",
        ]

        for query in test_cases:
            result = PreClassifier.pre_classify(query)
            assert result is None, f"pre-classifier should no longer claim: {query}"
            routed = await assert_inversion_routes(
                monkeypatch,
                query,
                live_categories="read_status,create_reminder",
                expected_action="list_todos_query",
            )
            assert routed.category == IntentCategory.QUERY, f"Wrong category for: {query}"

    @pytest.mark.asyncio
    async def test_next_todo_query_routes_to_query_category(self, monkeypatch):
        """Test "what's my next todo" routes to QUERY category
        (list_todos_query is the canonical destination — the pre-#1595
        alias action name next_todo_query no longer surfaces anywhere)."""
        from services.intent_service.pre_classifier import PreClassifier
        from services.shared_types import IntentCategory
        from tests.unit.services.intent_service._inversion_pin_helper import (
            assert_inversion_routes,
        )

        result = PreClassifier.pre_classify("what's my next todo")
        assert result is None, (
            f"TODO_QUERY_PATTERNS is deleted — pre-classifier should no "
            f'longer claim "what\'s my next todo" (got {result!r})'
        )
        routed = await assert_inversion_routes(
            monkeypatch,
            "what's my next todo",
            live_categories="read_status,create_reminder",
            expected_action="list_todos_query",
        )
        assert routed.category == IntentCategory.QUERY

    @pytest.mark.asyncio
    async def test_next_todo_query_variants(self, monkeypatch):
        """Test next todo query pattern variants all route correctly.

        "what should I do next" is ruled DIFFERENTLY, AND — a genuine
        sibling-reabsorption finding from this deletion, named not hidden
        (docs/internal/architecture/current/intent-routing-stack.md §Phase
        3, "Second deletion") — it is NOT unclaimed at surface 1 at all:
        PRIORITY_PATTERNS already carries an identical literal
        (r"\\bwhat should i do next\\b", pre-existing since 2026-03-22,
        commit 33f3a43ad42), previously shadowed by TODO_QUERY_PATTERNS'
        earlier position in pre_classify's if-chain. Once TODO_QUERY_
        PATTERNS emptied, PRIORITY_PATTERNS claims this phrase directly —
        and agrees with the ruled destination (get_top_priority), so no
        inversion consult is needed or exercised for this one phrase."""
        from services.intent_service.pre_classifier import PreClassifier
        from services.shared_types import IntentCategory
        from tests.unit.services.intent_service._inversion_pin_helper import (
            assert_inversion_routes,
        )

        result = PreClassifier.pre_classify("what should I do next")
        assert result is not None and result.action == "get_top_priority", (
            f"PRIORITY_PATTERNS should claim this phrase directly (sibling "
            f"reabsorption) — got {result!r}"
        )
        assert result.category == IntentCategory.PRIORITY

        test_cases = {
            "what's my next todo": ("list_todos_query", IntentCategory.QUERY),
            "next todo": ("list_todos_query", IntentCategory.QUERY),
        }

        for query, (expected_action, expected_category) in test_cases.items():
            result = PreClassifier.pre_classify(query)
            assert result is None, f"pre-classifier should no longer claim: {query}"
            routed = await assert_inversion_routes(
                monkeypatch,
                query,
                live_categories="read_status,read_strategic,create_reminder",
                expected_action=expected_action,
            )
            assert routed.category == expected_category, f"Wrong category for: {query}"
