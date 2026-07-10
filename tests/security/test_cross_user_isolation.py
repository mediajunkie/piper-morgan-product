"""
Cross-User Isolation Tests for SEC-MULTITENANCY Phase 4

TDD tests verifying that:
1. User A's data is not visible to User B
2. Repository methods reject None owner_id
3. Repository methods reject empty string owner_id

GitHub Issue: #734
Created: 2026-01-30
"""

from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest

# Test UUIDs from conftest.py
TEST_USER_A = UUID("11111111-1111-1111-1111-111111111111")
TEST_USER_B = UUID("22222222-2222-2222-2222-222222222222")
TEST_LIST_ID = UUID("33333333-3333-3333-3333-333333333333")
TEST_TODO_ID = UUID("44444444-4444-4444-4444-444444444444")


class TestOwnerIdValidation:
    """Test that repository methods reject invalid owner_id values"""

    @pytest.mark.asyncio
    async def test_list_repository_rejects_none_owner_id(self, db_session):
        """get_list_by_id should raise ValueError when owner_id is None"""
        from services.repositories.universal_list_repository import UniversalListRepository

        repo = UniversalListRepository(db_session)

        with pytest.raises(ValueError, match="owner_id is required"):
            await repo.get_list_by_id(str(TEST_LIST_ID), owner_id=None)

    @pytest.mark.asyncio
    async def test_list_repository_rejects_empty_owner_id(self, db_session):
        """get_list_by_id should raise ValueError when owner_id is empty string"""
        from services.repositories.universal_list_repository import UniversalListRepository

        repo = UniversalListRepository(db_session)

        with pytest.raises(ValueError, match="owner_id is required"):
            await repo.get_list_by_id(str(TEST_LIST_ID), owner_id="")

    @pytest.mark.asyncio
    async def test_todo_repository_rejects_none_owner_id(self, db_session):
        """get_todo_by_id should raise ValueError when owner_id is None"""
        from services.repositories.todo_repository import TodoRepository

        repo = TodoRepository(db_session)

        with pytest.raises(ValueError, match="owner_id is required"):
            await repo.get_todo_by_id(str(TEST_TODO_ID), owner_id=None)

    @pytest.mark.asyncio
    async def test_todo_repository_rejects_empty_owner_id(self, db_session):
        """get_todo_by_id should raise ValueError when owner_id is empty string"""
        from services.repositories.todo_repository import TodoRepository

        repo = TodoRepository(db_session)

        with pytest.raises(ValueError, match="owner_id is required"):
            await repo.get_todo_by_id(str(TEST_TODO_ID), owner_id="")

    @pytest.mark.asyncio
    async def test_list_for_read_rejects_none_user_id(self, db_session):
        """get_list_for_read should raise ValueError when user_id is None"""
        from services.repositories.universal_list_repository import UniversalListRepository

        repo = UniversalListRepository(db_session)

        with pytest.raises(ValueError, match="user_id is required"):
            await repo.get_list_for_read(str(TEST_LIST_ID), user_id=None)

    @pytest.mark.asyncio
    async def test_list_for_read_rejects_empty_user_id(self, db_session):
        """get_list_for_read should raise ValueError when user_id is empty string"""
        from services.repositories.universal_list_repository import UniversalListRepository

        repo = UniversalListRepository(db_session)

        with pytest.raises(ValueError, match="user_id is required"):
            await repo.get_list_for_read(str(TEST_LIST_ID), user_id="")


class TestUpdateMethodValidation:
    """Test that update methods reject invalid owner_id"""

    @pytest.mark.asyncio
    async def test_update_list_rejects_none_owner_id(self, db_session):
        """update_list should raise ValueError when owner_id is None"""
        from services.repositories.universal_list_repository import UniversalListRepository

        repo = UniversalListRepository(db_session)

        with pytest.raises(ValueError, match="owner_id is required"):
            await repo.update_list(str(TEST_LIST_ID), {"name": "Updated"}, owner_id=None)

    @pytest.mark.asyncio
    async def test_update_todo_rejects_none_owner_id(self, db_session):
        """update_todo should raise ValueError when owner_id is None"""
        from services.repositories.todo_repository import TodoRepository

        repo = TodoRepository(db_session)

        with pytest.raises(ValueError, match="owner_id is required"):
            await repo.update_todo(str(TEST_TODO_ID), {"text": "Updated"}, owner_id=None)


class TestDeleteMethodValidation:
    """Test that delete methods reject invalid owner_id"""

    @pytest.mark.asyncio
    async def test_delete_list_rejects_none_owner_id(self, db_session):
        """delete_list should raise ValueError when owner_id is None"""
        from services.repositories.universal_list_repository import UniversalListRepository

        repo = UniversalListRepository(db_session)

        with pytest.raises(ValueError, match="owner_id is required"):
            await repo.delete_list(str(TEST_LIST_ID), owner_id=None)


class TestTodoRepositoryMethodValidation:
    """Test additional TodoRepository methods reject invalid owner_id"""

    @pytest.mark.asyncio
    async def test_complete_todo_rejects_none_owner_id(self, db_session):
        """complete_todo should raise ValueError when owner_id is None"""
        from services.repositories.todo_repository import TodoRepository

        repo = TodoRepository(db_session)

        with pytest.raises(ValueError, match="owner_id is required"):
            await repo.complete_todo(str(TEST_TODO_ID), owner_id=None)


class TestCrossUserIsolation:
    """
    Integration tests verifying data isolation between users.

    These tests require database setup with actual data.
    Mark as integration tests that need real database.
    """

    async def _create_test_users(self, db_session):
        """Create test users for isolation tests"""
        from services.database.models import User

        # Create User A if not exists
        user_a = User(
            id=TEST_USER_A,
            username="test_user_a",
            email="user_a@test.com",
            is_active=True,
        )
        # Create User B if not exists
        user_b = User(
            id=TEST_USER_B,
            username="test_user_b",
            email="user_b@test.com",
            is_active=True,
        )
        db_session.add_all([user_a, user_b])
        try:
            await db_session.commit()
        except Exception:
            # Users might already exist - rollback and continue
            await db_session.rollback()

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_user_a_list_not_visible_to_user_b(self, db_session):
        """
        Lists owned by User A should not be returned when querying as User B.

        This tests the core multi-tenancy isolation requirement.
        """
        import services.domain.models as domain
        from services.database.models import ListDB
        from services.repositories.universal_list_repository import UniversalListRepository

        # Create test users first
        await self._create_test_users(db_session)

        repo = UniversalListRepository(db_session)

        # Create a list owned by User A
        user_a_list = ListDB(
            id=str(TEST_LIST_ID),
            owner_id=str(TEST_USER_A),
            name="User A Private List",
            item_type="todo",
            list_type="standard",
        )
        db_session.add(user_a_list)
        await db_session.commit()

        # User A should be able to access their own list
        result_a = await repo.get_list_by_id(str(TEST_LIST_ID), owner_id=str(TEST_USER_A))
        assert result_a is not None, "User A should see their own list"
        assert result_a.name == "User A Private List"

        # User B should NOT be able to access User A's list
        result_b = await repo.get_list_by_id(str(TEST_LIST_ID), owner_id=str(TEST_USER_B))
        assert result_b is None, "User B should NOT see User A's list"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_user_a_todos_not_visible_to_user_b(self, db_session):
        """
        Todos owned by User A should not be returned when querying as User B.
        """
        from services.database.models import TodoDB
        from services.repositories.todo_repository import TodoRepository

        # Create test users first
        await self._create_test_users(db_session)

        repo = TodoRepository(db_session)

        # Create a todo owned by User A
        user_a_todo = TodoDB(
            id=str(TEST_TODO_ID),
            owner_id=str(TEST_USER_A),
            text="User A Private Todo",
        )
        db_session.add(user_a_todo)
        await db_session.commit()

        # User A should be able to access their own todo
        result_a = await repo.get_todo_by_id(str(TEST_TODO_ID), owner_id=str(TEST_USER_A))
        assert result_a is not None, "User A should see their own todo"
        assert result_a.text == "User A Private Todo"

        # User B should NOT be able to access User A's todo
        result_b = await repo.get_todo_by_id(str(TEST_TODO_ID), owner_id=str(TEST_USER_B))
        assert result_b is None, "User B should NOT see User A's todo"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_lists_by_owner_returns_only_owned_lists(self, db_session):
        """
        get_lists_by_owner should only return lists for the specified owner.
        """
        from uuid import uuid4

        from services.database.models import ListDB
        from services.repositories.universal_list_repository import UniversalListRepository

        # Create test users first
        await self._create_test_users(db_session)

        repo = UniversalListRepository(db_session)

        # Create lists for both users
        list_a = ListDB(
            id=str(uuid4()),
            owner_id=str(TEST_USER_A),
            name="User A List",
            item_type="todo",
            list_type="standard",
        )
        list_b = ListDB(
            id=str(uuid4()),
            owner_id=str(TEST_USER_B),
            name="User B List",
            item_type="todo",
            list_type="standard",
        )
        db_session.add_all([list_a, list_b])
        await db_session.commit()

        # Get lists for User A
        user_a_lists = await repo.get_lists_by_owner(str(TEST_USER_A))

        # Should only contain User A's list
        list_names = [lst.name for lst in user_a_lists]
        assert "User A List" in list_names, "User A should see their own list"
        assert "User B List" not in list_names, "User A should NOT see User B's list"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_todos_by_owner_returns_only_owned_todos(self, db_session):
        """
        get_todos_by_owner should only return todos for the specified owner.
        """
        from uuid import uuid4

        from services.database.models import TodoDB
        from services.repositories.todo_repository import TodoRepository

        # Create test users first
        await self._create_test_users(db_session)

        repo = TodoRepository(db_session)

        # Create todos for both users
        todo_a = TodoDB(
            id=str(uuid4()),
            owner_id=str(TEST_USER_A),
            text="User A Todo",
        )
        todo_b = TodoDB(
            id=str(uuid4()),
            owner_id=str(TEST_USER_B),
            text="User B Todo",
        )
        db_session.add_all([todo_a, todo_b])
        await db_session.commit()

        # Get todos for User A
        user_a_todos = await repo.get_todos_by_owner(str(TEST_USER_A))

        # Should only contain User A's todo
        todo_texts = [t.text for t in user_a_todos]
        assert "User A Todo" in todo_texts, "User A should see their own todo"
        assert "User B Todo" not in todo_texts, "User A should NOT see User B's todo"
