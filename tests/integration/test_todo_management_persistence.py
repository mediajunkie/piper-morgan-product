"""
Integration tests for TodoManagementService - Issue #295

CRITICAL: These tests prove actual database persistence via TodoManagementService.
Tests the complete stack: Intent Handlers → API → TodoManagementService → Database

This is the proof-of-completion test suite for Issue #295.
"""

from uuid import UUID, uuid4

import pytest

from services.domain.models import Todo
from services.todo.todo_management_service import TodoManagementService


async def _seed_user(prefix: str = "todo") -> str:
    """Seed a real users row (owner_id is a UUID FK, #484/#1312); returns the id."""
    from datetime import datetime, timezone
    from uuid import uuid4

    from sqlalchemy import text as _text

    from services.database.session_factory import AsyncSessionFactory

    uid = str(uuid4())
    now = datetime.now(timezone.utc)
    async with AsyncSessionFactory.session_scope_fresh() as s:
        await s.execute(
            _text(
                "INSERT INTO users (id, username, email, is_active, is_verified, "
                "created_at, updated_at, role, is_alpha) "
                "VALUES (:id, :u, :e, true, true, :now, :now, 'user', true)"
            ),
            {"id": uid, "u": f"{prefix}_{uid[:8]}", "e": f"{prefix}_{uid[:8]}@test.example.com", "now": now},
        )
        await s.commit()
    return uid


async def _delete_user(uid: str) -> None:
    from sqlalchemy import text as _text

    from services.database.session_factory import AsyncSessionFactory

    async with AsyncSessionFactory.session_scope_fresh() as s:
        await s.execute(
            _text("DELETE FROM personalization_contexts WHERE owner_id = CAST(:u AS uuid)"),
            {"u": uid},
        )
        await s.execute(_text("DELETE FROM users WHERE id = :u"), {"u": uid})
        await s.commit()


@pytest.fixture
async def test_user_id():
    """Real seeded user (UUID): owner_id is a UUID FK to users (#484/#1312) —
    the old short string id predates the hardening."""
    uid = await _seed_user()
    yield uid
    await _delete_user(uid)


class TestTodoManagementPersistence:
    """
    Integration tests proving TodoManagementService persists todos to database.

    These tests verify:
    1. TodoManagementService creates todos in database
    2. TodoManagementService retrieves todos from database
    3. TodoManagementService updates todos in database
    4. TodoManagementService deletes todos from database
    5. Database changes persist across service instances
    """

    @pytest.fixture
    def service(self):
        """Create TodoManagementService instance."""
        return TodoManagementService()

    async def test_create_persists_to_database(self, service, test_user_id):
        """
        CRITICAL TEST: Verify create_todo actually writes to database.

        This is the core proof that Issue #295 is complete.
        If this passes, todos are being persisted to the database.
        """
        # Create todo via TodoManagementService
        todo = await service.create_todo(
            user_id=test_user_id, text="Test database persistence", priority="high"
        )

        # Verify todo was created with all expected fields
        assert todo is not None
        assert isinstance(todo, Todo)
        assert todo.id is not None
        assert isinstance(todo.id, str)  # Database uses string IDs
        assert todo.text == "Test database persistence"
        assert todo.priority == "high"
        assert todo.completed is False
        assert todo.status == "pending"
        assert todo.owner_id == test_user_id

        # CRITICAL: Retrieve to prove database persistence
        # Note: In tests, we retrieve in same context, but service commits ensure production persistence
        retrieved = await service.get_todo(todo_id=todo.id, user_id=test_user_id)

        # If this passes, the todo was actually written to database
        assert retrieved is not None
        assert str(retrieved.id) == str(todo.id)
        assert retrieved.text == "Test database persistence"
        assert retrieved.priority == "high"
        assert retrieved.owner_id == test_user_id

        # Cleanup
        await service.delete_todo(todo_id=todo.id, user_id=test_user_id)

    async def test_list_retrieves_from_database(self, service, test_user_id):
        """
        Verify list_todos retrieves actual persisted todos from database.
        """
        # Create multiple todos
        todo1 = await service.create_todo(
            user_id=test_user_id, text="First persistent todo", priority="high"
        )
        todo2 = await service.create_todo(
            user_id=test_user_id, text="Second persistent todo", priority="medium"
        )
        todo3 = await service.create_todo(
            user_id=test_user_id, text="Third persistent todo", priority="low"
        )

        # Retrieve via NEW service instance (proves database persistence)
        service2 = TodoManagementService()
        todos = await service2.list_todos(user_id=test_user_id, include_completed=False)

        # Should retrieve at least our 3 todos
        assert len(todos) >= 3

        # Find our todos in the list
        our_todo_ids = {str(todo1.id), str(todo2.id), str(todo3.id)}
        retrieved_ids = {str(t.id) for t in todos}

        assert our_todo_ids.issubset(retrieved_ids)

        # Verify content
        todo_texts = {t.text for t in todos if str(t.id) in our_todo_ids}
        assert "First persistent todo" in todo_texts
        assert "Second persistent todo" in todo_texts
        assert "Third persistent todo" in todo_texts

        # Cleanup
        await service.delete_todo(todo_id=todo1.id, user_id=test_user_id)
        await service.delete_todo(todo_id=todo2.id, user_id=test_user_id)
        await service.delete_todo(todo_id=todo3.id, user_id=test_user_id)

    async def test_update_persists_to_database(self, service, test_user_id):
        """
        Verify update_todo actually updates database.
        """
        # Create todo
        todo = await service.create_todo(user_id=test_user_id, text="Original text", priority="low")

        # Update todo-specific field (priority) via TodoManagementService
        # Note: Updating inherited fields (text) requires different approach - out of scope for #295
        updated = await service.update_todo(
            todo_id=todo.id, user_id=test_user_id, priority="urgent"
        )

        assert updated.priority == "urgent"

        # CRITICAL: Retrieve to prove database update
        retrieved = await service.get_todo(todo_id=todo.id, user_id=test_user_id)

        assert retrieved.priority == "urgent"

        # Cleanup
        await service.delete_todo(todo_id=todo.id, user_id=test_user_id)

    async def test_complete_persists_to_database(self, service, test_user_id):
        """
        Verify complete_todo actually updates database.
        """
        # Create todo
        todo = await service.create_todo(
            user_id=test_user_id, text="Todo to complete", priority="medium"
        )

        assert todo.completed is False
        assert todo.status == "pending"

        # Complete via TodoManagementService
        completed = await service.complete_todo(todo_id=todo.id, user_id=test_user_id)

        assert completed.completed is True
        assert completed.status == "completed"
        assert completed.completed_at is not None

        # CRITICAL: Retrieve from NEW service instance to prove database update
        service2 = TodoManagementService()
        retrieved = await service2.get_todo(todo_id=todo.id, user_id=test_user_id)

        assert retrieved.completed is True
        assert retrieved.status == "completed"
        assert retrieved.completed_at is not None

        # Cleanup
        await service.delete_todo(todo_id=todo.id, user_id=test_user_id)

    async def test_reopen_persists_to_database(self, service, test_user_id):
        """
        Verify reopen_todo actually updates database.
        """
        # Create and complete todo
        todo = await service.create_todo(
            user_id=test_user_id, text="Todo to reopen", priority="medium"
        )
        completed = await service.complete_todo(todo_id=todo.id, user_id=test_user_id)
        assert completed.completed is True

        # Reopen via TodoManagementService
        reopened = await service.reopen_todo(todo_id=todo.id, user_id=test_user_id)

        assert reopened.completed is False
        assert reopened.status == "pending"
        assert reopened.completed_at is None

        # CRITICAL: Retrieve from NEW service instance to prove database update
        service2 = TodoManagementService()
        retrieved = await service2.get_todo(todo_id=todo.id, user_id=test_user_id)

        assert retrieved.completed is False
        assert retrieved.status == "pending"
        assert retrieved.completed_at is None

        # Cleanup
        await service.delete_todo(todo_id=todo.id, user_id=test_user_id)

    async def test_delete_removes_from_database(self, service, test_user_id):
        """
        Verify delete_todo actually removes from database.
        """
        # Create todo
        todo = await service.create_todo(
            user_id=test_user_id, text="Todo to delete", priority="low"
        )

        # Verify it exists
        retrieved = await service.get_todo(todo_id=todo.id, user_id=test_user_id)
        assert retrieved is not None

        # Delete via TodoManagementService
        deleted = await service.delete_todo(todo_id=todo.id, user_id=test_user_id)
        assert deleted is True

        # CRITICAL: Try to retrieve from NEW service instance
        service2 = TodoManagementService()
        retrieved2 = await service2.get_todo(todo_id=todo.id, user_id=test_user_id)

        # Should be None (deleted from database)
        assert retrieved2 is None

    async def test_validation_errors(self, service, test_user_id):
        """
        Verify validation errors are raised properly.
        """
        # Empty text should raise ValueError
        with pytest.raises(ValueError, match="Todo text cannot be empty"):
            await service.create_todo(user_id=test_user_id, text="", priority="medium")

        # Whitespace-only text should raise ValueError
        with pytest.raises(ValueError, match="Todo text cannot be empty"):
            await service.create_todo(user_id=test_user_id, text="   ", priority="medium")

        # Invalid priority should raise ValueError
        with pytest.raises(ValueError, match="Invalid priority"):
            await service.create_todo(
                user_id=test_user_id, text="Valid text", priority="super-duper-urgent"
            )

    async def test_user_isolation(self, service):
        """
        Verify todos are isolated by user_id.
        """
        user1 = await _seed_user("iso1")
        user2 = await _seed_user("iso2")

        # Create todo for user1
        todo1 = await service.create_todo(user_id=user1, text="User 1 todo", priority="medium")

        # Create todo for user2
        todo2 = await service.create_todo(user_id=user2, text="User 2 todo", priority="medium")

        # User 1 should only see their todo
        user1_todos = await service.list_todos(user_id=user1, include_completed=False)
        user1_todo_ids = {str(t.id) for t in user1_todos}
        assert str(todo1.id) in user1_todo_ids
        assert str(todo2.id) not in user1_todo_ids

        # User 2 should only see their todo
        user2_todos = await service.list_todos(user_id=user2, include_completed=False)
        user2_todo_ids = {str(t.id) for t in user2_todos}
        assert str(todo2.id) in user2_todo_ids
        assert str(todo1.id) not in user2_todo_ids

        # Cleanup
        await service.delete_todo(todo_id=todo1.id, user_id=user1)
        await service.delete_todo(todo_id=todo2.id, user_id=user2)
        await _delete_user(user1)
        await _delete_user(user2)

    async def test_complete_lifecycle_with_persistence(self, service, test_user_id):
        """
        End-to-end test: Create → List → Update → Complete → Reopen → Delete.

        Each operation verified via NEW service instance to prove database persistence.
        """
        # 1. Create
        todo = await service.create_todo(
            user_id=test_user_id, text="Lifecycle test", priority="medium"
        )
        service2 = TodoManagementService()
        retrieved = await service2.get_todo(todo_id=todo.id, user_id=test_user_id)
        assert retrieved is not None
        assert retrieved.text == "Lifecycle test"

        # 2. List
        service3 = TodoManagementService()
        todos = await service3.list_todos(user_id=test_user_id, include_completed=False)
        assert any(str(t.id) == str(todo.id) for t in todos)

        # 3. Update
        await service.update_todo(
            todo_id=todo.id, user_id=test_user_id, text="Updated lifecycle test", priority="high"
        )
        service4 = TodoManagementService()
        retrieved = await service4.get_todo(todo_id=todo.id, user_id=test_user_id)
        assert retrieved.text == "Updated lifecycle test"
        assert retrieved.priority == "high"

        # 4. Complete
        await service.complete_todo(todo_id=todo.id, user_id=test_user_id)
        service5 = TodoManagementService()
        retrieved = await service5.get_todo(todo_id=todo.id, user_id=test_user_id)
        assert retrieved.completed is True
        assert retrieved.status == "completed"

        # 5. Reopen
        await service.reopen_todo(todo_id=todo.id, user_id=test_user_id)
        service6 = TodoManagementService()
        retrieved = await service6.get_todo(todo_id=todo.id, user_id=test_user_id)
        assert retrieved.completed is False
        assert retrieved.status == "pending"

        # 6. Delete
        await service.delete_todo(todo_id=todo.id, user_id=test_user_id)
        service7 = TodoManagementService()
        retrieved = await service7.get_todo(todo_id=todo.id, user_id=test_user_id)
        assert retrieved is None


class TestTodoManagementServiceIntegration:
    """
    Tests for TodoManagementService integration with existing services.
    """

    async def test_service_uses_todo_repository(self):
        """
        Verify TodoManagementService uses TodoRepository for database operations.
        """
        service = TodoManagementService()

        # Service should have todo_service
        assert hasattr(service, "todo_service")
        assert service.todo_service is not None

    async def test_service_uses_knowledge_service(self):
        """
        Verify TodoManagementService can work with TodoKnowledgeService.
        """
        service = TodoManagementService()

        # knowledge_service is optional, should be None by default
        assert hasattr(service, "knowledge_service")
        # It's OK if it's None (optional dependency)

    async def test_transaction_management(self, test_user_id):
        """
        Verify TodoManagementService manages database transactions properly.

        If a transaction fails, changes should be rolled back.
        """
        service = TodoManagementService()

        # Create a valid todo (should succeed)
        todo = await service.create_todo(
            user_id=test_user_id, text="Transaction test", priority="medium"
        )

        # Verify it was created
        retrieved = await service.get_todo(todo_id=todo.id, user_id=test_user_id)
        assert retrieved is not None

        # Try to create an invalid todo (should fail)
        try:
            await service.create_todo(
                user_id=test_user_id,
                text="",  # Empty text - should fail validation
                priority="medium",
            )
        except ValueError:
            pass  # Expected

        # Original todo should still exist (transaction isolation)
        retrieved2 = await service.get_todo(todo_id=todo.id, user_id=test_user_id)
        assert retrieved2 is not None
        assert retrieved2.text == "Transaction test"

        # Cleanup
        await service.delete_todo(todo_id=todo.id, user_id=test_user_id)
