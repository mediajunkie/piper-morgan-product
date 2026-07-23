"""
Comprehensive integration tests for todo functionality.

Tests the full stack: API → Service → Repository → Database
Verifies polymorphic inheritance works end-to-end.
"""

from uuid import UUID, uuid4

import pytest

from services.domain.models import Todo
from services.domain.primitives import Item
from services.item_service import ItemService
from services.todo_service import TodoService


class TestTodoFullStack:
    """End-to-end tests for todo functionality."""

    @pytest.fixture
    def service(self):
        """Create TodoService instance."""
        return TodoService()

    @pytest.fixture
    def list_id(self):
        """Create test list."""
        return uuid4()

    @pytest.fixture(autouse=True)
    async def todo_owner(self, request):
        """#1452: todo_items.owner_id is a NOT NULL FK to users since
        #484/#1312 — every create_todo needs a real user row. Create one per
        test and cascade it away fully."""
        import uuid as _uuid

        from services.database.models import User
        from services.database.session_factory import AsyncSessionFactory
        from tests.conftest import delete_test_user_fully

        uid = str(_uuid.uuid4())
        async with AsyncSessionFactory.session_scope_fresh() as session:
            session.add(
                User(
                    id=uid,
                    username=f"todofs-{uid[:8]}",
                    email=f"todofs-{uid[:8]}@example.com",
                    password_hash="x",
                    is_active=True,
                    is_verified=True,
                )
            )
            await session.commit()

        request.instance.owner_id = uid
        yield uid

        async with AsyncSessionFactory.session_scope_fresh() as session:
            await delete_test_user_fully(session, uid)
            await session.commit()

    async def test_complete_todo_lifecycle(self, service, list_id):
        """Test complete todo lifecycle: create, update, complete, delete.

        This verifies:
        - Todo creation via service
        - Todo extends Item (polymorphism)
        - Update operations work
        - Todo-specific operations (complete)
        - Generic operations (delete)
        """
        # 1. Create todo
        todo = await service.create_todo(
            owner_id=self.owner_id,
            text="Integration test todo", list_id=list_id, priority="high"
        )

        # Verify creation
        assert isinstance(todo, Todo)
        assert isinstance(todo, Item)  # Polymorphism
        assert todo.text == "Integration test todo"
        assert todo.priority == "high"
        assert todo.completed is False

        # 2. Update text (generic operation)
        updated = await service.update_item_text(UUID(todo.id), "Updated integration test")

        assert updated.text == "Updated integration test"
        assert updated.title == "Updated integration test"  # Backward compat

        # 3. Complete todo (todo-specific operation)
        completed = await service.complete_todo(UUID(todo.id))

        assert completed.completed is True
        assert completed.status == "completed"
        assert completed.completed_at is not None

        # 4. Reopen todo
        reopened = await service.reopen_todo(UUID(todo.id))

        assert reopened.completed is False
        assert reopened.status == "pending"
        assert reopened.completed_at is None

        # 5. Delete todo (generic operation)
        deleted = await service.delete_item(UUID(todo.id))

        assert deleted is True

        # 6. Verify deletion
        retrieved = await service.get_item(UUID(todo.id), Todo)
        assert retrieved is None

    async def test_polymorphic_operations(self, service, list_id):
        """Test that generic operations work on todos.

        Verifies polymorphic inheritance:
        - ItemService operations work on Todo
        - TodoService inherits ItemService operations
        """
        # Create multiple todos
        todo1 = await service.create_todo(owner_id=self.owner_id, text="First todo", list_id=list_id, priority="high")

        todo2 = await service.create_todo(owner_id=self.owner_id, text="Second todo", list_id=list_id, priority="medium")

        todo3 = await service.create_todo(owner_id=self.owner_id, text="Third todo", list_id=list_id, priority="low")

        # Test reordering (generic operation)
        reordered = await service.reorder_items(
            list_id, [UUID(todo3.id), UUID(todo1.id), UUID(todo2.id)]
        )

        assert len(reordered) == 3
        assert reordered[0].text == "Third todo"
        assert reordered[1].text == "First todo"
        assert reordered[2].text == "Second todo"

        # Test get_items_in_list (generic with type filter)
        todos = await service.get_items_in_list(list_id, item_type="todo")

        assert len(todos) == 3
        assert all(isinstance(t, Item) for t in todos)  # All are Items (polymorphism)

    async def test_backward_compatibility(self, service, list_id):
        """Test that title property works (backward compatibility).

        Verifies:
        - todo.text works (new way)
        - todo.title works (old way)
        - Both reference same value
        """
        todo = await service.create_todo(owner_id=self.owner_id, text="Test backward compatibility", list_id=list_id)

        # New way
        assert todo.text == "Test backward compatibility"

        # Old way (backward compatibility)
        assert todo.title == "Test backward compatibility"

        # Both reference same value
        assert todo.title == todo.text

    async def test_priority_operations(self, service, list_id):
        """Test todo-specific priority operations."""
        todo = await service.create_todo(owner_id=self.owner_id, text="Priority test", list_id=list_id, priority="low")

        # Change priority
        updated = await service.set_priority(UUID(todo.id), "urgent")

        assert updated.priority == "urgent"

        # Verify persistence
        retrieved = await service.get_item(UUID(todo.id), Todo)
        assert retrieved.priority == "urgent"

    async def test_database_polymorphic_queries(self, service, list_id):
        """Test that polymorphic database queries work.

        Verifies:
        - Can query via TodoDB
        - Can query via ItemDB with type filter
        - Both return same todos
        """
        # Create todos
        todo1 = await service.create_todo(owner_id=self.owner_id, text="DB test 1", list_id=list_id)
        todo2 = await service.create_todo(owner_id=self.owner_id, text="DB test 2", list_id=list_id)

        # Query via specific service
        todos_specific = await service.get_todos_in_list(list_id)

        # Query via generic service with type filter
        todos_generic = await service.get_items_in_list(list_id, item_type="todo")

        # Should return same number of todos
        assert len(todos_specific) == len(todos_generic)
        assert len(todos_specific) >= 2

        # All should be instances of Item (polymorphism)
        assert all(isinstance(t, Item) for t in todos_specific)
        assert all(isinstance(t, Item) for t in todos_generic)


class TestServiceLayerArchitecture:
    """Tests for service layer architecture patterns."""

    async def test_service_inheritance(self):
        """Verify TodoService inherits from ItemService."""
        service = TodoService()

        # TodoService should be instance of ItemService
        assert isinstance(service, ItemService)

        # TodoService should have ItemService methods
        assert hasattr(service, "create_item")
        assert hasattr(service, "update_item_text")
        assert hasattr(service, "reorder_items")
        assert hasattr(service, "delete_item")

        # TodoService should have todo-specific methods
        assert hasattr(service, "create_todo")
        assert hasattr(service, "complete_todo")
        assert hasattr(service, "reopen_todo")
        assert hasattr(service, "set_priority")

    async def test_item_service_universal_operations(self):
        """Verify ItemService works with any item type."""
        service = ItemService()

        # Should have universal operations
        assert hasattr(service, "create_item")
        assert hasattr(service, "get_item")
        assert hasattr(service, "update_item_text")
        assert hasattr(service, "reorder_items")
        assert hasattr(service, "delete_item")
        assert hasattr(service, "get_items_in_list")

    async def test_domain_inheritance(self):
        """Verify Todo extends Item in domain model."""
        # Todo should be subclass of Item
        assert issubclass(Todo, Item)

        # Create a todo
        import uuid as _uuid

        todo = Todo(
            text="Test todo",
            position=0,
            priority="medium",
            status="pending",
            completed=False,
            owner_id=str(_uuid.uuid4()),  # pure domain object — no DB row needed
        )

        # Should be instance of both
        assert isinstance(todo, Todo)
        assert isinstance(todo, Item)

        # Should have Item properties
        assert hasattr(todo, "text")
        assert hasattr(todo, "position")
        assert hasattr(todo, "list_id")

        # Should have Todo properties
        assert hasattr(todo, "priority")
        assert hasattr(todo, "status")
        assert hasattr(todo, "completed")

        # Backward compatibility
        assert todo.title == todo.text
