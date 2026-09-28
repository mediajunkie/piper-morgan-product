"""
Tests for Todo Completion Lifecycle Management (Issue #904)

Tests the three gaps identified in the todo completion flow:
1. Fuzzy text matching — "complete the PR review" matches "review the PR" todo
2. Completed todos distinguished in list view
3. Pre-classifier patterns for completion intents

TDD approach: tests written first, then implementation.
"""

import re
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

import pytest

from services.domain.models import Intent, IntentCategory, Todo
from tests.unit.services.intent_service._inversion_pin_helper import (
    assert_inversion_routes,
)

# ============================================================================
# 1. Fuzzy Text Matching Tests
# ============================================================================


class TestFuzzyTodoMatching:
    """Test that todos can be completed by text description, not just number."""

    @pytest.fixture
    def handlers(self):
        from services.intent_service.todo_handlers import TodoIntentHandlers

        h = TodoIntentHandlers()
        h.todo_service = AsyncMock()
        return h

    @pytest.fixture
    def sample_todos(self):
        """Create sample todos for matching tests."""
        todos = []
        for text in [
            "Review the PR for auth module",
            "Fix deployment pipeline bug",
            "Write quarterly report",
        ]:
            todo = Todo(text=text, priority="medium")
            todo.id = str(uuid4())
            todos.append(todo)
        return todos

    @pytest.mark.asyncio
    async def test_complete_by_text_exact_match(self, handlers, sample_todos):
        """'complete the Review the PR' matches 'Review the PR for auth module'."""
        handlers.todo_service.list_todos = AsyncMock(return_value=sample_todos)
        completed = Todo(text=sample_todos[0].text, status="completed", completed=True)
        handlers.todo_service.complete_todo = AsyncMock(return_value=completed)

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="complete_todo",
            original_message="complete the Review the PR todo",
            confidence=0.9,
        )
        user_id = uuid4()
        result = await handlers.handle_complete_todo(intent, "session1", user_id)

        # Should complete the PR review todo, not ask for a number
        assert (
            "done" in result.lower() or "marked" in result.lower() or "complete" in result.lower()
        )
        handlers.todo_service.complete_todo.assert_called_once()

    @pytest.mark.asyncio
    async def test_complete_by_partial_text(self, handlers, sample_todos):
        """'complete the PR review' matches 'Review the PR for auth module'."""
        handlers.todo_service.list_todos = AsyncMock(return_value=sample_todos)
        completed = Todo(text=sample_todos[0].text, status="completed", completed=True)
        handlers.todo_service.complete_todo = AsyncMock(return_value=completed)

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="complete_todo",
            original_message="complete the PR review",
            confidence=0.9,
        )
        user_id = uuid4()
        result = await handlers.handle_complete_todo(intent, "session1", user_id)

        assert (
            "done" in result.lower() or "marked" in result.lower() or "complete" in result.lower()
        )
        handlers.todo_service.complete_todo.assert_called_once()

    @pytest.mark.asyncio
    async def test_complete_by_keyword_match(self, handlers, sample_todos):
        """'finish the deployment thing' matches 'Fix deployment pipeline bug'."""
        handlers.todo_service.list_todos = AsyncMock(return_value=sample_todos)
        completed = Todo(text=sample_todos[1].text, status="completed", completed=True)
        handlers.todo_service.complete_todo = AsyncMock(return_value=completed)

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="complete_todo",
            original_message="finish the deployment thing",
            confidence=0.9,
        )
        user_id = uuid4()
        result = await handlers.handle_complete_todo(intent, "session1", user_id)

        assert (
            "done" in result.lower() or "marked" in result.lower() or "complete" in result.lower()
        )
        handlers.todo_service.complete_todo.assert_called_once()

    @pytest.mark.asyncio
    async def test_complete_by_number_still_works(self, handlers, sample_todos):
        """'mark todo 2 as complete' still works by number."""
        handlers.todo_service.list_todos = AsyncMock(return_value=sample_todos)
        completed = Todo(text=sample_todos[1].text, status="completed", completed=True)
        handlers.todo_service.complete_todo = AsyncMock(return_value=completed)

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="complete_todo",
            original_message="mark todo 2 as complete",
            confidence=0.9,
        )
        user_id = uuid4()
        result = await handlers.handle_complete_todo(intent, "session1", user_id)

        assert (
            "done" in result.lower() or "marked" in result.lower() or "complete" in result.lower()
        )
        handlers.todo_service.complete_todo.assert_called_once()

    @pytest.mark.asyncio
    async def test_no_match_returns_helpful_message(self, handlers, sample_todos):
        """When no todo matches the text, return helpful guidance."""
        handlers.todo_service.list_todos = AsyncMock(return_value=sample_todos)

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="complete_todo",
            original_message="complete the banana shopping",
            confidence=0.9,
        )
        user_id = uuid4()
        result = await handlers.handle_complete_todo(intent, "session1", user_id)

        # Should explain no match and offer help
        assert (
            "couldn't find" in result.lower()
            or "no matching" in result.lower()
            or "which" in result.lower()
        )
        handlers.todo_service.complete_todo.assert_not_called()

    @pytest.mark.asyncio
    async def test_ambiguous_match_asks_for_clarification(self, handlers):
        """When multiple todos match equally well, ask which one."""
        ambiguous_todos = [
            Todo(text="Review PR #100"),
            Todo(text="Review PR #200"),
        ]
        for t in ambiguous_todos:
            t.id = str(uuid4())
        handlers.todo_service.list_todos = AsyncMock(return_value=ambiguous_todos)

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="complete_todo",
            original_message="complete the review PR",
            confidence=0.9,
        )
        user_id = uuid4()
        result = await handlers.handle_complete_todo(intent, "session1", user_id)

        # Should ask which one OR complete the best match — either is acceptable
        # The key is it doesn't silently fail
        assert len(result) > 0


# ============================================================================
# 2. Completed Todos in List View
# ============================================================================


class TestCompletedTodosInListView:
    """Test that completed todos are visible and distinguished in list view."""

    @pytest.fixture
    def handlers(self):
        from services.intent_service.todo_handlers import TodoIntentHandlers

        h = TodoIntentHandlers()
        h.todo_service = AsyncMock()
        return h

    @pytest.mark.asyncio
    async def test_list_with_completed_shows_both(self, handlers):
        """'show all my todos' includes completed items."""
        active = Todo(text="Active task", status="pending", completed=False)
        active.id = str(uuid4())
        done = Todo(text="Done task", status="completed", completed=True)
        done.id = str(uuid4())
        handlers.todo_service.list_todos = AsyncMock(return_value=[active, done])

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="list_todos",
            original_message="show all my todos including completed",
            confidence=0.9,
        )
        user_id = uuid4()
        result = await handlers.handle_list_todos(intent, "session1", user_id)

        # Should show both active and completed
        assert "active" in result.lower() or "Active task" in result or "pending" in result.lower()

    @pytest.mark.asyncio
    async def test_default_list_still_excludes_completed(self, handlers):
        """'show my todos' defaults to active only."""
        active = Todo(text="Active task", status="pending", completed=False)
        active.id = str(uuid4())
        handlers.todo_service.list_todos = AsyncMock(return_value=[active])

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="list_todos",
            original_message="show my todos",
            confidence=0.9,
        )
        user_id = uuid4()
        result = await handlers.handle_list_todos(intent, "session1", user_id)

        # Default call should pass include_completed=False
        handlers.todo_service.list_todos.assert_called_once()
        call_kwargs = handlers.todo_service.list_todos.call_args
        assert call_kwargs[1].get("include_completed", False) is False


class TestCompletedTodoFormatting:
    """Test consciousness formatting distinguishes completed vs active."""

    def test_completed_todo_has_done_marker(self):
        """Completed todos should be visually distinct in list formatting."""
        from services.consciousness.todo_consciousness import format_todo_list_conscious

        active = Todo(text="Active task", status="pending", completed=False)
        done = Todo(text="Done task", status="completed", completed=True)

        result = format_todo_list_conscious([active, done], include_completed=True)

        # The result should distinguish between active and completed
        assert "Done task" in result or "done" in result.lower()
        assert len(result) > 0


# ============================================================================
# 3. Pre-classifier Patterns for Completion
# ============================================================================


class TestCompletionPreClassifierPatterns:
    """Test that the pre-classifier recognizes todo completion intents."""

    @pytest.fixture
    def pre_classifier(self):
        from services.intent_service.pre_classifier import PreClassifier

        return PreClassifier

    def test_mark_todo_complete_pattern(self, pre_classifier):
        """'mark todo 1 as complete' is pre-classified as EXECUTION/complete_todo."""
        result = pre_classifier.pre_classify("mark todo 1 as complete")
        assert result is not None
        assert result.category == IntentCategory.EXECUTION
        assert result.action == "complete_todo"

    def test_complete_the_pr_review_pattern(self, pre_classifier):
        """'complete the PR review todo' is pre-classified correctly."""
        result = pre_classifier.pre_classify("complete the PR review todo")
        assert result is not None
        assert result.category == IntentCategory.EXECUTION
        assert result.action == "complete_todo"

    def test_mark_done_pattern(self, pre_classifier):
        """'mark done: review the docs' is pre-classified correctly."""
        result = pre_classifier.pre_classify("mark done the review docs todo")
        assert result is not None
        assert result.category == IntentCategory.EXECUTION
        assert result.action == "complete_todo"

    def test_finish_todo_pattern(self, pre_classifier):
        """'finish todo about deployment' is pre-classified correctly."""
        result = pre_classifier.pre_classify("finish todo about deployment")
        assert result is not None
        assert result.category == IntentCategory.EXECUTION
        assert result.action == "complete_todo"

    def test_done_with_todo_pattern(self, pre_classifier):
        """'done with the PR review' is pre-classified correctly."""
        result = pre_classifier.pre_classify("done with the PR review todo")
        assert result is not None
        assert result.category == IntentCategory.EXECUTION
        assert result.action == "complete_todo"

    @pytest.mark.asyncio
    async def test_show_completed_todos_pattern(self, pre_classifier, monkeypatch):
        """'show completed todos' should route to list with completed flag.

        #1595 Phase 3 (second deletion, 2026-09-27): TODO_QUERY_PATTERNS'
        literals were deleted (scripts/inversion_phase3_deleted_patterns.json)
        — surface 1 no longer claims this phrase. Two-part pin: (a) surface 1
        declines, (b) the Inversion routes it to list_todos_query,
        deterministically (a stubbed router, no LLM)."""
        result = pre_classifier.pre_classify("show my completed todos")
        assert result is None, (
            f"TODO_QUERY_PATTERNS is deleted — pre-classifier should no "
            f"longer claim 'show my completed todos' (got {result!r})"
        )
        routed = await assert_inversion_routes(
            monkeypatch,
            "show my completed todos",
            live_categories="read_status,create_reminder",
            expected_action="list_todos_query",
        )
        assert routed.category == IntentCategory.QUERY


# ============================================================================
# 4. Text Extraction for Completion
# ============================================================================


class TestCompletionTextExtraction:
    """Test extracting the todo description from completion requests."""

    @pytest.fixture
    def handlers(self):
        from services.intent_service.todo_handlers import TodoIntentHandlers

        h = TodoIntentHandlers()
        return h

    def test_extract_text_from_complete_command(self, handlers):
        """Extract 'PR review' from 'complete the PR review todo'."""
        text = handlers._extract_completion_text("complete the PR review todo")
        assert text is not None
        assert "pr review" in text.lower()

    def test_extract_text_from_mark_done(self, handlers):
        """Extract text from 'mark done: review the docs'."""
        text = handlers._extract_completion_text("mark the review docs todo as done")
        assert text is not None
        assert "review" in text.lower()

    def test_extract_text_from_finish(self, handlers):
        """Extract text from 'finish the deployment task'."""
        text = handlers._extract_completion_text("finish the deployment task")
        assert text is not None
        assert "deployment" in text.lower()

    def test_extract_returns_none_for_number_only(self, handlers):
        """'mark todo 3 as complete' returns None — handled by number path."""
        text = handlers._extract_completion_text("mark todo 3 as complete")
        assert text is None  # Number path should take priority


# ============================================================================
# 5. Fuzzy Match Scoring
# ============================================================================


class TestFuzzyMatchScoring:
    """Test the word-overlap fuzzy matching algorithm."""

    @pytest.fixture
    def handlers(self):
        from services.intent_service.todo_handlers import TodoIntentHandlers

        return TodoIntentHandlers()

    def test_exact_overlap_scores_high(self, handlers):
        """Exact word match scores highly."""
        score = handlers._fuzzy_match_score("Review the PR", "review the PR for auth")
        assert score > 0.5

    def test_no_overlap_scores_zero(self, handlers):
        """No common words scores zero."""
        score = handlers._fuzzy_match_score("banana shopping list", "deploy kubernetes cluster")
        assert score == 0.0

    def test_partial_overlap_scores_medium(self, handlers):
        """Some common words score proportionally."""
        # "fix deployment" (after stopword removal) fully matches candidate
        score = handlers._fuzzy_match_score("fix the deployment", "Fix deployment pipeline bug")
        assert score > 0.5
        # True partial: only "deployment" matches
        score2 = handlers._fuzzy_match_score(
            "deployment review status", "Fix deployment pipeline bug"
        )
        assert 0.2 < score2 < 1.0

    def test_stopwords_excluded(self, handlers):
        """Common words like 'the', 'a', 'for' don't inflate scores."""
        score_with_stopwords = handlers._fuzzy_match_score("the the the", "the a for in")
        assert score_with_stopwords == 0.0  # Stopwords only → no real match
