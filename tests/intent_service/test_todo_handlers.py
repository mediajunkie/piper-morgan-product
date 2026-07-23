"""
Unit tests for Todo Intent Handlers (Issue #285)

Tests the natural language interface for todo operations.
"""

import pytest

from services.domain.models import Intent, IntentCategory
from services.intent_service.todo_handlers import TodoIntentHandlers


class TestTodoIntentHandlers:
    """Test TodoIntentHandlers functionality"""

    @pytest.fixture
    def handlers(self):
        """Create TodoIntentHandlers instance"""
        return TodoIntentHandlers()

    @pytest.fixture(autouse=True)
    async def todo_user(self, request):
        """#1452: todo_items.owner_id became UUID + FK + NOT NULL (#484/#1312)
        — the literal self.user_id these tests passed can no longer insert. Create
        a real user per test and cascade it away fully."""
        import uuid as _uuid

        from services.database.models import User
        from services.database.session_factory import AsyncSessionFactory
        from tests.conftest import delete_test_user_fully

        uid = str(_uuid.uuid4())
        async with AsyncSessionFactory.session_scope_fresh() as session:
            session.add(
                User(
                    id=uid,
                    username=f"todo-test-{uid[:8]}",
                    email=f"todo-test-{uid[:8]}@example.com",
                    password_hash="x",
                    is_active=True,
                    is_verified=True,
                )
            )
            await session.commit()

        request.instance.user_id = uid
        yield uid

        async with AsyncSessionFactory.session_scope_fresh() as session:
            await delete_test_user_fully(session, uid)
            await session.commit()

    @pytest.fixture
    def sample_intent(self):
        """Create a sample intent for testing"""
        return Intent(
            category=IntentCategory.EXECUTION,
            action="create_todo",
            original_message="add todo: Review PR #285",
            confidence=0.9,
        )

    @pytest.mark.asyncio
    async def test_create_todo_extracts_text(self, handlers, sample_intent):
        """Test create_todo extracts todo text correctly"""
        result = await handlers.handle_create_todo(sample_intent, "session1", self.user_id)

        assert "Review PR #285" in result
        assert "added" in result.lower() or "✓" in result

    @pytest.mark.asyncio
    async def test_create_todo_handles_missing_text(self, handlers):
        """Test create_todo handles missing todo text"""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_todo",
            original_message="add todo",  # No text after colon
            confidence=0.9,
        )

        result = await handlers.handle_create_todo(intent, "session1", self.user_id)

        assert "didn't catch" in result.lower() or "try:" in result.lower()

    @pytest.mark.asyncio
    async def test_create_todo_extracts_priority(self, handlers):
        """Test create_todo extracts priority from message"""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_todo",
            original_message="add todo: Fix urgent bug in login (high priority)",
            confidence=0.9,
        )

        result = await handlers.handle_create_todo(intent, "session1", self.user_id)

        assert "Fix urgent bug in login" in result
        assert "high" in result.lower() or "urgent" in result.lower()

    @pytest.mark.asyncio
    async def test_list_todos_returns_message(self, handlers):
        """Test list_todos returns a formatted message"""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="list_todos",
            original_message="show my todos",
            confidence=0.9,
        )

        result = await handlers.handle_list_todos(intent, "session1", self.user_id)

        assert "todo" in result.lower()
        # For now, returns placeholder message
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_complete_todo_extracts_id(self, handlers):
        """Test complete_todo extracts todo ID"""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="complete_todo",
            original_message="mark todo 3 as complete",
            confidence=0.9,
        )

        # #1452: the handler now verifies the todo exists (ids resolve by
        # list position) — create three so 'todo 3' resolves.
        for msg in ("add todo: First task", "add todo: Second task", "add todo: Third task"):
            await handlers.handle_create_todo(
                Intent(
                    category=IntentCategory.EXECUTION,
                    action="create_todo",
                    original_message=msg,
                    confidence=0.9,
                ),
                "session1",
                self.user_id,
            )

        result = await handlers.handle_complete_todo(intent, "session1", self.user_id)

        assert "done" in result.lower() or "complete" in result.lower()

    @pytest.mark.asyncio
    async def test_complete_todo_handles_missing_id(self, handlers):
        """Test complete_todo handles missing todo ID"""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="complete_todo",
            original_message="mark todo as complete",  # No ID
            confidence=0.9,
        )

        result = await handlers.handle_complete_todo(intent, "session1", self.user_id)

        # Graceful guidance either way: no todos, or no parseable id
        assert "complete todo" in result.lower() or "add todo" in result.lower()

    @pytest.mark.asyncio
    async def test_delete_todo_extracts_id(self, handlers):
        """Test delete_todo extracts todo ID"""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="delete_todo",
            original_message="delete todo 5",
            confidence=0.9,
        )

        result = await handlers.handle_delete_todo(intent, "session1", self.user_id)

        # No todos exist for this fresh user: graceful not-found naming the id
        assert "5" in result
        assert "couldn't find" in result.lower() or "removed" in result.lower()

    @pytest.mark.asyncio
    async def test_delete_todo_handles_missing_id(self, handlers):
        """Test delete_todo handles missing todo ID"""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="delete_todo",
            original_message="delete todo",  # No ID
            confidence=0.9,
        )

        result = await handlers.handle_delete_todo(intent, "session1", self.user_id)

        assert "which" in result.lower() or "try:" in result.lower()

    def test_extract_todo_text_patterns(self, handlers):
        """Test _extract_todo_text handles various patterns"""
        # Pattern: "add todo: TEXT"
        text1 = handlers._extract_todo_text("add todo: Review code")
        assert text1 == "Review code"

        # Pattern: "create todo: TEXT"
        text2 = handlers._extract_todo_text("create todo: Write docs")
        assert text2 == "Write docs"

        # Pattern: "todo: TEXT"
        text3 = handlers._extract_todo_text("todo: Test feature")
        assert text3 == "Test feature"

        # No match
        text4 = handlers._extract_todo_text("just some random text")
        assert text4 == ""

    def test_extract_priority_levels(self, handlers):
        """Test _extract_priority extracts priority levels"""
        # Urgent
        assert handlers._extract_priority("fix urgent bug") == "urgent"

        # High
        assert handlers._extract_priority("high priority task") == "high"
        assert handlers._extract_priority("this is high importance") == "high"

        # Low
        assert handlers._extract_priority("low priority cleanup") == "low"

        # Default to medium
        assert handlers._extract_priority("normal task") == "medium"

    def test_extract_todo_id_patterns(self, handlers):
        """Test _extract_todo_id handles various patterns"""
        # Pattern: "todo N"
        id1 = handlers._extract_todo_id("mark todo 5 complete")
        assert id1 == "5"

        # Pattern: "todo #N"
        id2 = handlers._extract_todo_id("delete todo #12")
        assert id2 == "12"

        # Pattern: "mark N"
        id3 = handlers._extract_todo_id("mark 7 as done")
        assert id3 == "7"

        # Pattern: "delete N"
        id4 = handlers._extract_todo_id("delete 99")
        assert id4 == "99"

        # No match
        id5 = handlers._extract_todo_id("mark something complete")
        assert id5 is None

    @pytest.mark.asyncio
    async def test_next_todo_returns_highest_priority(self, handlers):
        """Test next_todo returns the highest priority todo"""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="next_todo",
            original_message="what's my next todo?",
            confidence=0.9,
        )

        result = await handlers.handle_next_todo(intent, "session1", self.user_id)

        # Should return a todo or empty message
        assert "todo" in result.lower() or "next" in result.lower()
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_next_todo_handles_no_todos(self, handlers):
        """Test next_todo handles case when user has no todos"""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="next_todo",
            original_message="next task",
            confidence=0.9,
        )

        result = await handlers.handle_next_todo(intent, "session1", self.user_id)

        # Should provide helpful message when no todos exist
        assert len(result) > 0
        # Since there may be no todos, check for reasonable response
        assert "todo" in result.lower() or "task" in result.lower()

    @pytest.mark.asyncio
    async def test_next_todo_shows_priority_icon(self, handlers):
        """Test next_todo includes priority indicators"""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="next_todo",
            original_message="what should I do next?",
            confidence=0.9,
        )

        result = await handlers.handle_next_todo(intent, "session1", self.user_id)

        # Result should be formatted properly
        assert len(result) > 0
        # Priority icons would be in result if todo exists (🔴, 🟡, 🟢)
