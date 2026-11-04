"""Tests for universal ItemService."""

from uuid import UUID, uuid4

import pytest
import pytest_asyncio

from services.domain.primitives import Item
from services.item_service import ItemService


class TestItemService:
    """Tests for ItemService base class."""

    @pytest.fixture
    def service(self):
        """Create service instance."""
        return ItemService()

    @pytest_asyncio.fixture
    async def test_owner_id(self) -> str:
        """Create a test user (lists.owner_id is NOT NULL and a FK to users)."""
        from datetime import datetime, timezone

        from sqlalchemy import text

        from services.database.session_factory import AsyncSessionFactory

        user_id = str(uuid4())
        async with AsyncSessionFactory.session_scope() as session:
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
                    "username": f"test_user_{user_id[:8]}",
                    "email": f"test_{user_id[:8]}@example.com",
                    "created_at": datetime.now(timezone.utc),
                    "updated_at": datetime.now(timezone.utc),
                },
            )
            await session.commit()
        yield user_id
        # #2254: leave nothing behind: the user's items, lists and row, in the
        # helper's FK order (base items have no owner column; see tests/conftest.py).
        from tests.conftest import delete_test_user_fully

        async with AsyncSessionFactory.session_scope() as session:
            await delete_test_user_fully(session, user_id)

    @pytest_asyncio.fixture
    async def list_id(self, test_owner_id) -> UUID:
        """Create a real list. 2014 (s2014items): items.list_id is a FK to lists.id, so an
        invented uuid4() is rejected once the DB is at head — CI's smoke set caught this
        on the 10-15 landing (14 failures)."""
        from services.database.session_factory import AsyncSessionFactory
        from services.domain import models as domain
        from services.repositories.universal_list_repository import UniversalListRepository

        async with AsyncSessionFactory.session_scope() as session:
            created = await UniversalListRepository(session).create_list(
                domain.List(name="item-service-test", owner_id=test_owner_id, item_type="item")
            )
            await session.commit()
        return UUID(created.id)

    @pytest.mark.smoke
    async def test_create_item(self, service, list_id):
        """Can create generic item."""
        item = await service.create_item(text="Test item", list_id=list_id)

        assert isinstance(item, Item)
        assert item.text == "Test item"
        assert item.list_id == str(list_id)
        assert item.position == 0

    @pytest.mark.smoke
    async def test_get_item(self, service, list_id):
        """Can retrieve item by ID."""
        # Create item
        created = await service.create_item(text="Retrieve me", list_id=list_id)

        # Retrieve it
        retrieved = await service.get_item(UUID(created.id))

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.text == "Retrieve me"

    @pytest.mark.smoke
    async def test_update_item_text(self, service, list_id):
        """Can update item text."""
        item = await service.create_item(text="Original", list_id=list_id)

        updated = await service.update_item_text(UUID(item.id), "Updated")

        assert updated.text == "Updated"

    @pytest.mark.smoke
    async def test_reorder_items(self, service, list_id):
        """Can reorder items in list."""
        # Create 3 items
        item1 = await service.create_item(text="First", list_id=list_id)
        item2 = await service.create_item(text="Second", list_id=list_id)
        item3 = await service.create_item(text="Third", list_id=list_id)

        # Reorder: 3, 1, 2
        reordered = await service.reorder_items(
            list_id, [UUID(item3.id), UUID(item1.id), UUID(item2.id)]
        )

        assert reordered[0].text == "Third"
        assert reordered[1].text == "First"
        assert reordered[2].text == "Second"

    @pytest.mark.smoke
    async def test_delete_item(self, service, list_id):
        """Can delete item."""
        item = await service.create_item(text="Delete me", list_id=list_id)

        deleted = await service.delete_item(UUID(item.id))
        assert deleted is True

        # Verify deleted
        retrieved = await service.get_item(UUID(item.id))
        assert retrieved is None

    @pytest.mark.smoke
    async def test_get_items_in_list(self, service, list_id):
        """Can get all items in a list."""
        # Create multiple items
        await service.create_item(text="Item 1", list_id=list_id)
        await service.create_item(text="Item 2", list_id=list_id)
        await service.create_item(text="Item 3", list_id=list_id)

        # Retrieve all
        items = await service.get_items_in_list(list_id)

        assert len(items) == 3
        assert items[0].text == "Item 1"
        assert items[1].text == "Item 2"
        assert items[2].text == "Item 3"

    @pytest.mark.smoke
    async def test_position_auto_assignment(self, service, list_id):
        """Items are auto-assigned sequential positions."""
        item1 = await service.create_item(text="First", list_id=list_id)
        item2 = await service.create_item(text="Second", list_id=list_id)
        item3 = await service.create_item(text="Third", list_id=list_id)

        assert item1.position == 0
        assert item2.position == 1
        assert item3.position == 2
