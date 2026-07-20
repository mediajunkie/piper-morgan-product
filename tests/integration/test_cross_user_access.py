"""
Cross-user access prevention tests for SEC-RBAC Phase 3.

Tests verify that User A cannot access User B's resources,
and that admin users CAN bypass ownership checks.

Issue: #357 (SEC-RBAC: Implement RBAC)
ADR: ADR-044 (Lightweight RBAC)
Phase: 3 - System-wide admin role testing
"""

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlalchemy import text

from services.domain import models as domain
from services.repositories.file_repository import FileRepository
from services.repositories.todo_repository import TodoRepository
from services.repositories.universal_list_repository import UniversalListRepository


async def create_test_user_in_session(
    session, user_id: str, username: str = None, email: str = None
):
    """Helper to create a test user in a specific session."""
    if username is None:
        username = f"test_user_{user_id[:8]}"
    if email is None:
        email = f"{username}@example.com"

    await session.execute(
        text(
            """
            INSERT INTO users (id, username, email, password_hash, is_active, is_verified,
                               created_at, updated_at, role, is_alpha)
            VALUES (:id, :username, :email, '', true, false, :created_at, :updated_at, 'user', true)
            ON CONFLICT (id) DO NOTHING
        """
        ),
        {
            "id": user_id,
            "username": username,
            "email": email,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        },
    )
    await session.flush()


@pytest.mark.asyncio
class TestCrossUserListAccess:
    """Test that users cannot access other users' lists"""

    async def test_user_a_cannot_read_user_b_list(self, async_transaction):
        """User A cannot read User B's list"""
        user_a_id = str(uuid4())
        user_b_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, user_a_id)
            await create_test_user_in_session(session, user_b_id)
            list_repo = UniversalListRepository(session)

            # Create list as User B using domain model
            list_b = domain.List(name="User B's Private List", owner_id=user_b_id, item_type="todo")
            list_b = await list_repo.create_list(list_b)

            # Try to read as User A (should return None with ownership check)
            result = await list_repo.get_list_by_id(list_b.id, owner_id=user_a_id, is_admin=False)

            assert result is None, "User A should NOT be able to read User B's list"

    async def test_user_a_cannot_update_user_b_list(self, async_transaction):
        """User A cannot update User B's list"""
        user_a_id = str(uuid4())
        user_b_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, user_a_id)
            await create_test_user_in_session(session, user_b_id)
            list_repo = UniversalListRepository(session)

            # Create list as User B using domain model
            list_b = domain.List(name="User B's List", owner_id=user_b_id, item_type="todo")
            list_b = await list_repo.create_list(list_b)

            # Try to update as User A (should return None)
            result = await list_repo.update_list(
                list_b.id, updates={"name": "Hacked by User A"}, owner_id=user_a_id, is_admin=False
            )

            assert result is None, "User A should NOT be able to update User B's list"

    async def test_user_a_cannot_delete_user_b_list(self, async_transaction):
        """User A cannot delete User B's list"""
        user_a_id = str(uuid4())
        user_b_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, user_a_id)
            await create_test_user_in_session(session, user_b_id)
            list_repo = UniversalListRepository(session)

            # Create list as User B using domain model
            list_b = domain.List(name="User B's List", owner_id=user_b_id, item_type="todo")
            list_b = await list_repo.create_list(list_b)

            # Try to delete as User A (should return False)
            result = await list_repo.delete_list(list_b.id, owner_id=user_a_id, is_admin=False)

            assert result is False, "User A should NOT be able to delete User B's list"

    async def test_owner_can_read_own_list(self, async_transaction):
        """Owner CAN read their own list"""
        user_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, user_id)
            list_repo = UniversalListRepository(session)

            # Create list as owner using domain model
            my_list = domain.List(name="My List", owner_id=user_id, item_type="todo")
            my_list = await list_repo.create_list(my_list)

            # Read as owner (should succeed)
            result = await list_repo.get_list_by_id(my_list.id, owner_id=user_id, is_admin=False)

            assert result is not None, "Owner should be able to read their own list"
            assert result.id == my_list.id
            assert result.owner_id == user_id

    async def test_owner_can_update_own_list(self, async_transaction):
        """Owner CAN update their own list"""
        user_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, user_id)
            list_repo = UniversalListRepository(session)

            # Create list using domain model
            my_list = domain.List(name="My List", owner_id=user_id, item_type="todo")
            my_list = await list_repo.create_list(my_list)

            # Update as owner (should succeed)
            result = await list_repo.update_list(
                my_list.id, updates={"name": "Updated by owner"}, owner_id=user_id, is_admin=False
            )

            assert result is not None, "Owner should be able to update their own list"
            assert result.name == "Updated by owner"

    async def test_owner_can_delete_own_list(self, async_transaction):
        """Owner CAN delete their own list"""
        user_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, user_id)
            list_repo = UniversalListRepository(session)

            # Create list using domain model
            my_list = domain.List(name="My List", owner_id=user_id, item_type="todo")
            my_list = await list_repo.create_list(my_list)

            # Delete as owner (should succeed)
            result = await list_repo.delete_list(my_list.id, owner_id=user_id, is_admin=False)

            assert result is True, "Owner should be able to delete their own list"

    async def test_admin_can_read_any_list(self, async_transaction):
        """Admin CAN read any user's list"""
        user_b_id = str(uuid4())
        admin_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, user_b_id)
            await create_test_user_in_session(session, admin_id)
            list_repo = UniversalListRepository(session)

            # Create list as User B using domain model
            list_b = domain.List(name="User B's List", owner_id=user_b_id, item_type="todo")
            list_b = await list_repo.create_list(list_b)

            # Read as admin (should succeed with admin bypass)
            result = await list_repo.get_list_by_id(
                list_b.id,
                owner_id=admin_id,
                is_admin=True,  # Admin bypass
            )

            assert result is not None, "Admin should be able to read any user's list"
            assert result.id == list_b.id
            assert result.owner_id == user_b_id

    async def test_admin_can_update_any_list(self, async_transaction):
        """Admin CAN update any user's list"""
        user_b_id = str(uuid4())
        admin_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, user_b_id)
            await create_test_user_in_session(session, admin_id)
            list_repo = UniversalListRepository(session)

            # Create list as User B using domain model
            list_b = domain.List(name="User B's List", owner_id=user_b_id, item_type="todo")
            list_b = await list_repo.create_list(list_b)

            # Update as admin (should succeed)
            result = await list_repo.update_list(
                list_b.id,
                updates={"name": "Updated by admin"},
                owner_id=admin_id,
                is_admin=True,  # Admin bypass
            )

            assert result is not None, "Admin should be able to update any list"
            assert result.name == "Updated by admin"

    async def test_admin_can_delete_any_list(self, async_transaction):
        """Admin CAN delete any user's list"""
        user_b_id = str(uuid4())
        admin_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, user_b_id)
            await create_test_user_in_session(session, admin_id)
            list_repo = UniversalListRepository(session)

            # Create list as User B using domain model
            list_b = domain.List(name="User B's List", owner_id=user_b_id, item_type="todo")
            list_b = await list_repo.create_list(list_b)

            # Delete as admin (should succeed)
            result = await list_repo.delete_list(
                list_b.id,
                owner_id=admin_id,
                is_admin=True,  # Admin bypass
            )

            assert result is True, "Admin should be able to delete any list"


@pytest.mark.asyncio
class TestCrossUserTodoAccess:
    """Test that users cannot access other users' todos"""

    async def test_user_a_cannot_read_user_b_todo(self, async_transaction):
        """User A cannot read User B's todo"""
        user_a_id = str(uuid4())
        user_b_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, user_a_id)
            await create_test_user_in_session(session, user_b_id)
            todo_repo = TodoRepository(session)

            # Create todo as User B using domain model
            todo_b = domain.Todo(text="User B's Private Todo", owner_id=user_b_id)
            todo_b = await todo_repo.create_todo(todo_b)

            # Try to read as User A (should return None)
            result = await todo_repo.get_todo_by_id(todo_b.id, owner_id=user_a_id, is_admin=False)

            assert result is None, "User A should NOT be able to read User B's todo"

    async def test_user_a_cannot_update_user_b_todo(self, async_transaction):
        """User A cannot update User B's todo"""
        user_a_id = str(uuid4())
        user_b_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, user_a_id)
            await create_test_user_in_session(session, user_b_id)
            todo_repo = TodoRepository(session)

            # Create todo as User B using domain model
            todo_b = domain.Todo(text="User B's Todo", owner_id=user_b_id)
            todo_b = await todo_repo.create_todo(todo_b)

            # Try to update as User A (should return None)
            result = await todo_repo.update_todo(
                todo_b.id, updates={"text": "Hacked by User A"}, owner_id=user_a_id, is_admin=False
            )

            assert result is None, "User A should NOT be able to update User B's todo"

    async def test_user_a_cannot_delete_user_b_todo(self, async_transaction):
        """User A cannot delete User B's todo"""
        user_a_id = str(uuid4())
        user_b_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, user_a_id)
            await create_test_user_in_session(session, user_b_id)
            todo_repo = TodoRepository(session)

            # Create todo as User B using domain model
            todo_b = domain.Todo(text="User B's Todo", owner_id=user_b_id)
            todo_b = await todo_repo.create_todo(todo_b)

            # Try to delete as User A (should return False)
            result = await todo_repo.delete_todo(todo_b.id, owner_id=user_a_id, is_admin=False)

            assert result is False, "User A should NOT be able to delete User B's todo"

    async def test_owner_can_read_own_todo(self, async_transaction):
        """Owner CAN read their own todo"""
        user_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, user_id)
            todo_repo = TodoRepository(session)

            # Create todo using domain model
            my_todo = domain.Todo(text="My Todo", owner_id=user_id)
            my_todo = await todo_repo.create_todo(my_todo)

            # Read as owner (should succeed)
            result = await todo_repo.get_todo_by_id(my_todo.id, owner_id=user_id, is_admin=False)

            assert result is not None, "Owner should be able to read their own todo"
            assert result.id == my_todo.id
            assert result.owner_id == user_id

    async def test_owner_can_update_own_todo(self, async_transaction):
        """Owner CAN update their own todo"""
        user_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, user_id)
            todo_repo = TodoRepository(session)

            # Create todo using domain model
            my_todo = domain.Todo(text="My Todo", owner_id=user_id)
            my_todo = await todo_repo.create_todo(my_todo)

            # Update as owner (should succeed)
            result = await todo_repo.update_todo(
                my_todo.id, updates={"text": "Updated by owner"}, owner_id=user_id, is_admin=False
            )

            assert result is not None, "Owner should be able to update their own todo"
            assert result.text == "Updated by owner"

    async def test_owner_can_delete_own_todo(self, async_transaction):
        """Owner CAN delete their own todo"""
        user_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, user_id)
            todo_repo = TodoRepository(session)

            # Create todo using domain model
            my_todo = domain.Todo(text="My Todo", owner_id=user_id)
            my_todo = await todo_repo.create_todo(my_todo)

            # Delete as owner (should succeed)
            result = await todo_repo.delete_todo(my_todo.id, owner_id=user_id, is_admin=False)

            assert result is True, "Owner should be able to delete their own todo"

    async def test_admin_can_read_any_todo(self, async_transaction):
        """Admin CAN read any user's todo"""
        user_b_id = str(uuid4())
        admin_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, user_b_id)
            await create_test_user_in_session(session, admin_id)
            todo_repo = TodoRepository(session)

            # Create todo as User B using domain model
            todo_b = domain.Todo(text="User B's Todo", owner_id=user_b_id)
            todo_b = await todo_repo.create_todo(todo_b)

            # Read as admin (should succeed)
            result = await todo_repo.get_todo_by_id(
                todo_b.id,
                owner_id=admin_id,
                is_admin=True,  # Admin bypass
            )

            assert result is not None, "Admin should be able to read any user's todo"
            assert result.id == todo_b.id
            assert result.owner_id == user_b_id

    async def test_admin_can_update_any_todo(self, async_transaction):
        """Admin CAN update any user's todo"""
        user_b_id = str(uuid4())
        admin_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, user_b_id)
            await create_test_user_in_session(session, admin_id)
            todo_repo = TodoRepository(session)

            # Create todo as User B using domain model
            todo_b = domain.Todo(text="User B's Todo", owner_id=user_b_id)
            todo_b = await todo_repo.create_todo(todo_b)

            # Update as admin (should succeed)
            result = await todo_repo.update_todo(
                todo_b.id,
                updates={"text": "Updated by admin"},
                owner_id=admin_id,
                is_admin=True,  # Admin bypass
            )

            assert result is not None, "Admin should be able to update any todo"
            assert result.text == "Updated by admin"

    async def test_admin_can_delete_any_todo(self, async_transaction):
        """Admin CAN delete any user's todo"""
        user_b_id = str(uuid4())
        admin_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, user_b_id)
            await create_test_user_in_session(session, admin_id)
            todo_repo = TodoRepository(session)

            # Create todo as User B using domain model
            todo_b = domain.Todo(text="User B's Todo", owner_id=user_b_id)
            todo_b = await todo_repo.create_todo(todo_b)

            # Delete as admin (should succeed)
            result = await todo_repo.delete_todo(
                todo_b.id,
                owner_id=admin_id,
                is_admin=True,  # Admin bypass
            )

            assert result is True, "Admin should be able to delete any todo"


@pytest.mark.asyncio
class TestCrossUserFileAccess:
    """Test file access control across users with owner_id enforcement"""

    async def test_user_a_cannot_read_user_b_file(self, async_transaction):
        """User A should not be able to read User B's file"""
        user_a_id = str(uuid4())
        user_b_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, user_a_id)
            await create_test_user_in_session(session, user_b_id)
            # Create test users to satisfy FK constraints
            await create_test_user_in_session(session, user_a_id)
            await create_test_user_in_session(session, user_b_id)

            file_repo = FileRepository(session)
            file_b = domain.UploadedFile(
                id=str(uuid4()),
                owner_id=user_b_id,
                filename="user_b_file.txt",
                file_type="text/plain",
                file_size=1024,
                storage_path="/files/user_b_file.txt",
            )
            await file_repo.save_file_metadata(file_b)

            result = await file_repo.get_file_by_id(file_b.id, owner_id=user_a_id, is_admin=False)
            assert result is None  # Cross-user access blocked ✅

    async def test_user_a_cannot_delete_user_b_file(self, async_transaction):
        """User A should not be able to delete User B's file"""
        user_a_id = str(uuid4())
        user_b_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, user_a_id)
            await create_test_user_in_session(session, user_b_id)
            # Create test users to satisfy FK constraints
            await create_test_user_in_session(session, user_a_id)
            await create_test_user_in_session(session, user_b_id)

            file_repo = FileRepository(session)
            file_b = domain.UploadedFile(
                id=str(uuid4()),
                owner_id=user_b_id,
                filename="user_b_file.txt",
                file_type="text/plain",
                file_size=1024,
                storage_path="/files/user_b_file.txt",
            )
            await file_repo.save_file_metadata(file_b)

            deleted = await file_repo.delete_file(file_b.id, owner_id=user_a_id, is_admin=False)
            assert not deleted  # Cross-user delete blocked ✅

    async def test_owner_can_read_own_file(self, async_transaction):
        """Owner should be able to read their own file"""
        owner_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, owner_id)
            # Create test user to satisfy FK constraints
            await create_test_user_in_session(session, owner_id)

            file_repo = FileRepository(session)
            my_file = domain.UploadedFile(
                id=str(uuid4()),
                owner_id=owner_id,
                filename="my_file.txt",
                file_type="text/plain",
                file_size=1024,
                storage_path="/files/my_file.txt",
            )
            await file_repo.save_file_metadata(my_file)

            result = await file_repo.get_file_by_id(my_file.id, owner_id=owner_id, is_admin=False)
            assert result is not None  # Owner access allowed ✅
            assert result.id == my_file.id

    async def test_admin_can_read_any_file(self, async_transaction):
        """Admin should be able to read any file"""
        owner_id = str(uuid4())
        admin_id = str(uuid4())

        async with async_transaction as session:
            # #1312 FK: owner ids must exist in users (fixtures predate the FK)
            await create_test_user_in_session(session, owner_id)
            await create_test_user_in_session(session, admin_id)
            # Create test users to satisfy FK constraints
            await create_test_user_in_session(session, owner_id)
            await create_test_user_in_session(session, admin_id)

            file_repo = FileRepository(session)
            any_file = domain.UploadedFile(
                id=str(uuid4()),
                owner_id=owner_id,
                filename="any_file.txt",
                file_type="text/plain",
                file_size=1024,
                storage_path="/files/any_file.txt",
            )
            await file_repo.save_file_metadata(any_file)

            result = await file_repo.get_file_by_id(any_file.id, owner_id=admin_id, is_admin=True)
            assert result is not None  # Admin bypass allowed ✅
            assert result.id == any_file.id
