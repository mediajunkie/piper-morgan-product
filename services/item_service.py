"""
Universal Item Service

Provides operations that work on any item type (Todo, Shopping, Reading, etc.).
Specific services (TodoService) extend this for type-specific operations.

Design Philosophy:
- Generic operations live here (create, update, delete, reorder)
- Type-specific operations live in subclasses (complete, purchase, finish)
- Polymorphic queries handled transparently
"""

from typing import List, Optional, Type
from uuid import UUID

from sqlalchemy import func, select

from services.database.models import ItemDB
from services.database.session_factory import AsyncSessionFactory
from services.domain.primitives import Item


class ItemService:
    """Universal service for all item operations.

    This base class provides operations that work on ANY item type.
    Subclasses (TodoService, ShoppingService) add type-specific operations.

    Examples:
        >>> # Generic operation (works on any item)
        >>> service = ItemService()
        >>> item = await service.create_item(
        ...     text="Generic item",
        ...     list_id=some_list_id
        ... )

        >>> # Todo-specific operation (TodoService only)
        >>> todo_service = TodoService()
        >>> await todo_service.complete_todo(todo_id)
    """

    async def create_item(
        self,
        text: str,
        list_id: UUID,
        position: Optional[int] = None,
        item_class: Type[Item] = Item,
        **kwargs,
    ) -> Item:
        """Create any type of item.

        This is a universal operation that works for todos, shopping items, etc.

        Args:
            text: The item text (universal property)
            list_id: Which list contains this item
            position: Position in list (auto-assigned if not provided)
            item_class: Type of item to create (Item, Todo, etc.)
            **kwargs: Type-specific fields (priority, quantity, etc.)

        Returns:
            Created item

        Examples:
            >>> # Create generic item
            >>> item = await service.create_item(
            ...     text="Buy milk",
            ...     list_id=list_id
            ... )

            >>> # Create todo (from TodoService)
            >>> todo = await service.create_item(
            ...     text="Review PR",
            ...     list_id=list_id,
            ...     item_class=Todo,
            ...     priority="high"
            ... )
        """
        async with AsyncSessionFactory.session_scope() as session:
            # Determine position if not provided
            if position is None:
                position = await self._get_next_position(session, list_id)

            # Create domain object
            item = item_class(text=text, list_id=str(list_id), position=position, **kwargs)

            # Convert to database model
            db_model_class = self._get_db_model_class(item_class)
            item_db = db_model_class.from_domain(item)

            # Save to database
            session.add(item_db)
            await session.commit()
            await session.refresh(item_db)

            # Convert back to domain
            return item_db.to_domain()

    async def get_item(self, item_id: UUID, item_class: Type[Item] = Item) -> Optional[Item]:
        """Get item by ID.

        Universal operation - retrieves any item type.

        Args:
            item_id: ID of item to retrieve
            item_class: Expected type (Item, Todo, etc.)

        Returns:
            Item if found, None otherwise
        """
        async with AsyncSessionFactory.session_scope() as session:
            db_model_class = self._get_db_model_class(item_class)

            result = await session.execute(
                select(db_model_class).where(db_model_class.id == str(item_id))
            )
            item_db = result.scalar_one_or_none()

            if not item_db:
                return None

            return item_db.to_domain()

    async def update_item_text(self, item_id: UUID, new_text: str) -> Optional[Item]:
        """Update item text.

        Universal operation - works on any item type.

        Args:
            item_id: ID of item to update
            new_text: New text for the item

        Returns:
            Updated item
        """
        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(select(ItemDB).where(ItemDB.id == str(item_id)))
            item_db = result.scalar_one_or_none()

            if not item_db:
                return None

            item_db.text = new_text
            await session.commit()
            await session.refresh(item_db)

            return item_db.to_domain()

    async def reorder_items(self, list_id: UUID, item_ids: List[UUID]) -> List[Item]:
        """Reorder items in a list.

        Universal operation - works on any item types in the list.

        Args:
            list_id: List containing the items
            item_ids: Item IDs in desired order

        Returns:
            Reordered items
        """
        from sqlalchemy.orm import selectin_polymorphic

        async with AsyncSessionFactory.session_scope() as session:
            # Update positions
            for position, item_id in enumerate(item_ids):
                result = await session.execute(
                    select(ItemDB).where(ItemDB.id == str(item_id), ItemDB.list_id == str(list_id))
                )
                item_db = result.scalar_one_or_none()

                if item_db:
                    item_db.position = position

            await session.commit()

            # Return reordered items. selectin_polymorphic eager-loads the
            # joined-inheritance subclass tables — to_domain() on a TodoDB row
            # otherwise lazy-loads todo_items synchronously, which the async
            # session forbids (MissingGreenlet).
            result = await session.execute(
                select(ItemDB)
                .options(selectin_polymorphic(ItemDB, ItemDB.__mapper__.polymorphic_map.values()))
                .where(ItemDB.list_id == str(list_id))
                .order_by(ItemDB.position)
            )
            items_db = result.scalars().all()

            return [item_db.to_domain() for item_db in items_db]

    async def delete_item(self, item_id: UUID) -> bool:
        """Delete item.

        Universal operation - deletes any item type.

        Args:
            item_id: ID of item to delete

        Returns:
            True if deleted, False if not found
        """
        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(select(ItemDB).where(ItemDB.id == str(item_id)))
            item_db = result.scalar_one_or_none()

            if not item_db:
                return False

            await session.delete(item_db)
            await session.commit()

            return True

    async def get_items_in_list(self, list_id: UUID, item_type: Optional[str] = None) -> List[Item]:
        """Get all items in a list.

        Universal operation - can filter by item type.

        Args:
            list_id: List to get items from
            item_type: Optional filter ('todo', 'shopping', etc.)

        Returns:
            List of items
        """
        from sqlalchemy.orm import selectin_polymorphic

        async with AsyncSessionFactory.session_scope() as session:
            # Eager-load subclass tables (see reorder_items note — same
            # MissingGreenlet hazard on to_domain()).
            query = (
                select(ItemDB)
                .options(selectin_polymorphic(ItemDB, ItemDB.__mapper__.polymorphic_map.values()))
                .where(ItemDB.list_id == str(list_id))
            )

            if item_type:
                query = query.where(ItemDB.item_type == item_type)

            query = query.order_by(ItemDB.position)

            result = await session.execute(query)
            items_db = result.scalars().all()

            return [item_db.to_domain() for item_db in items_db]

    # Helper methods

    async def _get_next_position(self, session, list_id: UUID) -> int:
        """Get next position for item in list."""
        result = await session.execute(
            select(func.max(ItemDB.position)).where(ItemDB.list_id == str(list_id))
        )
        max_position = result.scalar()

        # Explicitly check for None - don't use `or` because 0 is falsy!
        return (max_position + 1) if max_position is not None else 0

    def _get_db_model_class(self, item_class: Type[Item]):
        """Map domain class to database model class."""
        from services.database.models import TodoDB
        from services.domain.models import Todo

        if item_class == Todo:
            return TodoDB
        # Add other mappings as needed
        return ItemDB
