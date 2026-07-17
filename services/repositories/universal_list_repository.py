"""
Universal List Repository implementation for PM-081
Chief Architect's universal composition over specialization principle
"""

import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import UUID

import structlog
from sqlalchemy import and_, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import services.domain.models as domain
from services.database.models import ListDB, ListItemDB, TodoDB
from services.database.repositories import BaseRepository

logger = structlog.get_logger()


class UniversalListRepository(BaseRepository):
    """Repository for Universal List operations supporting ANY item type"""

    model = ListDB

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_list(self, list_obj: domain.List) -> domain.List:
        """Create a new universal list"""
        db_list = ListDB.from_domain(list_obj)
        self.session.add(db_list)
        await self.session.flush()
        await self.session.refresh(db_list)
        return db_list.to_domain()

    async def get_list_by_id(
        self, list_id: str, owner_id: str, is_admin: bool = False
    ) -> Optional[domain.List]:
        """Get universal list by ID - verify ownership (admin bypass in SEC-RBAC Phase 3)

        Args:
            list_id: The list ID to retrieve
            owner_id: REQUIRED - the owner ID for multi-tenancy isolation
            is_admin: If True, bypasses ownership check

        Raises:
            ValueError: If owner_id is None or empty (SEC-MULTITENANCY Phase 4)
        """
        if not owner_id:
            raise ValueError("owner_id is required for multi-tenancy isolation")

        filters = [ListDB.id == list_id]
        if not is_admin:  # Only check ownership if not admin
            filters.append(ListDB.owner_id == owner_id)

        result = await self.session.execute(select(ListDB).where(and_(*filters)))
        db_list = result.scalar_one_or_none()
        return db_list.to_domain() if db_list else None

    async def get_list_for_read(self, list_id: str, user_id: str) -> Optional[domain.List]:
        """Get list for reading - allows both owner AND shared users to access (SEC-RBAC Phase 2)

        Args:
            list_id: The list ID to retrieve
            user_id: REQUIRED - the user ID requesting access

        Raises:
            ValueError: If user_id is None or empty (SEC-MULTITENANCY Phase 4)
        """
        if not user_id:
            raise ValueError("user_id is required for multi-tenancy isolation")

        # Always get the list first
        # global-ok: D6 fetch-then-check — owner/shared_with on instance; shared_with JSON not WHERE-able
        result = await self.session.execute(select(ListDB).where(ListDB.id == list_id))
        db_list = result.scalar_one_or_none()

        if not db_list:
            return None

        # Convert to domain to check access
        domain_list = db_list.to_domain()

        # User can access if:
        # 1. User is owner
        # 2. User is in shared_with array (any role allows read)
        if domain_list.owner_id == user_id or domain_list.user_can_read(user_id):
            return domain_list

        return None

    async def get_lists_by_owner(
        self,
        owner_id: str,
        item_type: Optional[str] = None,
        include_archived: bool = False,
        list_type: Optional[str] = None,
    ) -> List[domain.List]:
        """Get lists for an owner with optional filtering"""
        query = select(ListDB).where(ListDB.owner_id == owner_id)

        if item_type:
            query = query.where(ListDB.item_type == item_type)

        if not include_archived:
            query = query.where(ListDB.is_archived == False)

        if list_type:
            query = query.where(ListDB.list_type == list_type)

        query = query.order_by(ListDB.is_default.desc(), ListDB.name)

        result = await self.session.execute(query)
        db_lists = result.scalars().all()
        return [db_list.to_domain() for db_list in db_lists]

    async def get_max_item_added_at(self, list_id: str):
        """Return the most-recent `ListItem.added_at` for items in the list,
        or `None` if the list has no items.

        Used by the staleness signal (#714) to compute the effective
        last-touched timestamp of a list. Cheap single-row aggregate query
        per list. At alpha scale, the per-list call from the lists endpoint
        is sub-second; Post-MVP optimization could denormalize a
        `last_item_activity_at` column on ListDB and update on item-add to
        avoid the per-list query.
        """
        result = await self.session.execute(
            select(func.max(ListItemDB.added_at)).where(ListItemDB.list_id == list_id)
        )
        return result.scalar_one_or_none()

    async def get_default_list(self, owner_id: str, item_type: str) -> Optional[domain.List]:
        """Get user's default list for a specific item type"""
        result = await self.session.execute(
            select(ListDB).where(
                and_(
                    ListDB.owner_id == owner_id,
                    ListDB.item_type == item_type,
                    ListDB.is_default == True,
                    ListDB.is_archived == False,
                )
            )
        )
        db_list = result.scalar_one_or_none()
        return db_list.to_domain() if db_list else None

    async def get_shared_lists(
        self, user_id: UUID, item_type: Optional[str] = None
    ) -> List[domain.List]:
        """Get lists shared with a user (SEC-RBAC Phase 2)"""
        # For Phase 2, shared_with is now an array of {user_id, role} objects
        query = select(ListDB).where(
            and_(
                # Check if shared_with array contains an object with matching user_id
                ListDB.shared_with.op("@>")(
                    func.jsonb_build_array(func.jsonb_build_object("user_id", user_id))
                ),
                ListDB.is_archived == False,
            )
        )

        if item_type:
            query = query.where(ListDB.item_type == item_type)

        query = query.order_by(ListDB.name)

        result = await self.session.execute(query)
        db_lists = result.scalars().all()
        return [db_list.to_domain() for db_list in db_lists]

    async def update_list(
        self, list_id: str, updates: Dict, owner_id: str, is_admin: bool = False
    ) -> Optional[domain.List]:
        """Update universal list - verify ownership (admin bypass in SEC-RBAC Phase 3)

        Args:
            list_id: The list ID to update
            updates: Dictionary of fields to update
            owner_id: REQUIRED - the owner ID for multi-tenancy isolation
            is_admin: If True, bypasses ownership check

        Raises:
            ValueError: If owner_id is None or empty (SEC-MULTITENANCY Phase 4)
        """
        if not owner_id:
            raise ValueError("owner_id is required for multi-tenancy isolation")

        updates["updated_at"] = datetime.now()

        filters = [ListDB.id == list_id]
        if not is_admin:  # Only check ownership if not admin
            filters.append(ListDB.owner_id == owner_id)

        result = await self.session.execute(
            update(ListDB).where(and_(*filters)).values(**updates).returning(ListDB)
        )
        db_list = result.scalar_one_or_none()
        return db_list.to_domain() if db_list else None

    async def update_item_counts(self, list_id: str, owner_id: str, is_admin: bool = False) -> None:
        """Update cached item counts - verify ownership (admin bypass in SEC-RBAC Phase 3)

        Args:
            list_id: The list ID to update counts for
            owner_id: REQUIRED - the owner ID for multi-tenancy isolation
            is_admin: If True, bypasses ownership check

        Raises:
            ValueError: If owner_id is None or empty (SEC-MULTITENANCY Phase 4)
        """
        if not owner_id:
            raise ValueError("owner_id is required for multi-tenancy isolation")

        # Get total count through list items
        total_result = await self.session.execute(
            select(func.count(ListItemDB.id)).where(ListItemDB.list_id == list_id)
        )
        total_count = total_result.scalar() or 0

        # Get completed count (for todos only - other item types may have different logic)
        list_obj = await self.get_list_by_id(list_id, owner_id, is_admin)
        completed_count = 0

        if list_obj and list_obj.item_type == "todo":
            completed_result = await self.session.execute(
                select(func.count(ListItemDB.id))
                .select_from(ListItemDB)
                .join(TodoDB, ListItemDB.item_id == TodoDB.id)
                .where(and_(ListItemDB.list_id == list_id, TodoDB.status == "completed"))
            )
            completed_count = completed_result.scalar() or 0

        # Update the list with new counts (with ownership verification if provided)
        filters = [ListDB.id == list_id]
        if not is_admin:  # Only check ownership if not admin
            filters.append(ListDB.owner_id == owner_id)

        await self.session.execute(
            update(ListDB)
            .where(and_(*filters))
            .values(
                item_count=total_count, completed_count=completed_count, updated_at=datetime.now()
            )
        )

    async def delete_list(self, list_id: str, owner_id: str, is_admin: bool = False) -> bool:
        """Delete a list - verify ownership (admin bypass in SEC-RBAC Phase 3, cascades to items)

        Args:
            list_id: The list ID to delete
            owner_id: REQUIRED - the owner ID for multi-tenancy isolation
            is_admin: If True, bypasses ownership check

        Raises:
            ValueError: If owner_id is None or empty (SEC-MULTITENANCY Phase 4)
        """
        if not owner_id:
            raise ValueError("owner_id is required for multi-tenancy isolation")

        filters = [ListDB.id == list_id]
        if not is_admin:  # Only check ownership if not admin
            filters.append(ListDB.owner_id == owner_id)

        result = await self.session.execute(select(ListDB).where(and_(*filters)))
        db_list = result.scalar_one_or_none()

        if db_list:
            await self.session.delete(db_list)
            return True
        return False

    async def search_lists_by_name(
        self, owner_id: str, query: str, item_type: Optional[str] = None
    ) -> List[domain.List]:
        """Search lists by name (case-insensitive)"""
        search_query = select(ListDB).where(
            and_(
                ListDB.owner_id == owner_id,
                ListDB.name.ilike(f"%{query}%"),
                ListDB.is_archived == False,
            )
        )

        if item_type:
            search_query = search_query.where(ListDB.item_type == item_type)

        search_query = search_query.order_by(ListDB.name)

        result = await self.session.execute(search_query)
        db_lists = result.scalars().all()
        return [db_list.to_domain() for db_list in db_lists]

    async def share_list(
        self, list_id: str, owner_id: str, user_id_to_share: str, role: domain.ShareRole = None
    ) -> Optional[domain.List]:
        """Share a list with another user at specified role (SEC-RBAC Phase 2)

        Args:
            list_id: ID of list to share
            owner_id: User making the share request (must be owner or admin)
            user_id_to_share: User to share with
            role: ShareRole (viewer, editor, admin) - defaults to viewer if None

        Returns:
            Updated List with new shared_with entry, or None if not found/not owner
        """
        # Default role if not specified
        if role is None:
            role = domain.ShareRole.VIEWER

        # First verify the caller is the owner
        result = await self.session.execute(
            select(ListDB).where(and_(ListDB.id == list_id, ListDB.owner_id == owner_id))
        )
        db_list = result.scalar_one_or_none()

        if not db_list:
            return None  # Not found or not owner

        # Prevent owner from sharing with themselves (no-op)
        if user_id_to_share == owner_id:
            return db_list.to_domain()

        # Convert to domain object to work with SharePermission objects
        domain_list = db_list.to_domain()

        # Check if user already shared with - update role if exists, otherwise add new share
        permission = domain.SharePermission(user_id=user_id_to_share, role=role)
        existing_index = None

        for idx, perm in enumerate(domain_list.shared_with):
            if perm.user_id == user_id_to_share:
                existing_index = idx
                break

        if existing_index is not None:
            # Update existing permission
            domain_list.shared_with[existing_index] = permission
        else:
            # Add new permission
            domain_list.shared_with.append(permission)

        # Convert back to JSONB format for database storage
        shared_with_jsonb = [perm.to_dict() for perm in domain_list.shared_with]

        # Update database
        await self.session.execute(
            update(ListDB)
            .where(ListDB.id == list_id)
            .values(shared_with=shared_with_jsonb, updated_at=datetime.now())
        )

        # Refresh and return updated list
        await self.session.refresh(db_list)
        return db_list.to_domain()

    async def unshare_list(
        self, list_id: str, owner_id: str, user_id_to_unshare: str
    ) -> Optional[domain.List]:
        """Remove sharing access - owner only operation (SEC-RBAC Phase 2)"""
        # First verify the caller is the owner
        result = await self.session.execute(
            select(ListDB).where(and_(ListDB.id == list_id, ListDB.owner_id == owner_id))
        )
        db_list = result.scalar_one_or_none()

        if not db_list:
            return None  # Not found or not owner

        # Convert to domain object to work with SharePermission objects
        domain_list = db_list.to_domain()

        # Remove user from shared_with array
        domain_list.shared_with = [
            perm for perm in domain_list.shared_with if perm.user_id != user_id_to_unshare
        ]

        # Convert back to JSONB format for database storage
        shared_with_jsonb = [perm.to_dict() for perm in domain_list.shared_with]

        # Update database
        await self.session.execute(
            update(ListDB)
            .where(ListDB.id == list_id)
            .values(shared_with=shared_with_jsonb, updated_at=datetime.now())
        )

        # Refresh and return updated list
        await self.session.refresh(db_list)
        return db_list.to_domain()

    async def get_lists_shared_with_me(self, user_id: str) -> List[domain.List]:
        """Get lists that are shared with this user (excluding owned lists) (SEC-RBAC Phase 2)"""
        # For Phase 2, shared_with is now an array of {user_id, role} objects
        # Check if any element in the array has a matching user_id
        # Using SQL: @> operator with JSONB search for array containing object with user_id
        query = select(ListDB).where(
            and_(
                # Check if shared_with array contains an object with matching user_id
                # Using JSONB containment: shared_with @> '[{"user_id": "value"}]'
                ListDB.shared_with.op("@>")(
                    func.jsonb_build_array(func.jsonb_build_object("user_id", user_id))
                ),
                ListDB.owner_id != user_id,  # Not owned by this user
                ListDB.is_archived == False,
            )
        )

        query = query.order_by(ListDB.name)

        result = await self.session.execute(query)
        db_lists = result.scalars().all()
        return [db_list.to_domain() for db_list in db_lists]

    async def update_share_role(
        self, list_id: str, requesting_user_id: str, target_user_id: str, new_role: domain.ShareRole
    ) -> bool:
        """Update a user's role for a shared list (owner or admin only)

        Args:
            list_id: ID of list to modify sharing for
            requesting_user_id: User making the request (must be owner or admin)
            target_user_id: User whose role to update
            new_role: New role (viewer, editor, admin)

        Returns:
            True if update successful, False if not found or unauthorized
        """
        # Verify requestor is owner
        result = await self.session.execute(
            select(ListDB).where(and_(ListDB.id == list_id, ListDB.owner_id == requesting_user_id))
        )
        db_list = result.scalar_one_or_none()

        if not db_list:
            return False  # Not found or not owner

        # Convert to domain object to work with SharePermission objects
        domain_list = db_list.to_domain()

        # Find and update the permission
        found = False
        for perm in domain_list.shared_with:
            if perm.user_id == target_user_id:
                perm.role = new_role
                found = True
                break

        if not found:
            return False  # User not in shared_with

        # Convert back to JSONB format for database storage
        shared_with_jsonb = [perm.to_dict() for perm in domain_list.shared_with]

        # Update database
        await self.session.execute(
            update(ListDB)
            .where(ListDB.id == list_id)
            .values(shared_with=shared_with_jsonb, updated_at=datetime.now())
        )

        return True

    async def get_user_role(self, list_id: str, user_id: str) -> Optional[str]:
        """Get user's role for a list

        Returns:
            'owner' if user is owner
            Role string ('viewer', 'editor', 'admin') if shared with user
            None if user has no access
        """
        # Get the list
        # global-ok: D6 fetch-then-check — owner/shared_with on instance; shared_with JSON not WHERE-able
        result = await self.session.execute(select(ListDB).where(ListDB.id == list_id))
        db_list = result.scalar_one_or_none()

        if not db_list:
            return None

        # Check if owner
        if db_list.owner_id == user_id:
            return "owner"

        # Convert to domain object to search shared_with
        domain_list = db_list.to_domain()

        for perm in domain_list.shared_with:
            if perm.user_id == user_id:
                return perm.role.value

        return None


class UniversalListItemRepository(BaseRepository):
    """Repository for Universal ListItem operations managing polymorphic relationships"""

    model = ListItemDB

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_item(self, item: domain.ListItem) -> domain.ListItem:
        """Create a list item relationship"""
        db_item = ListItemDB.from_domain(item)
        self.session.add(db_item)
        await self.session.flush()
        await self.session.refresh(db_item)
        return db_item.to_domain()

    async def get_item_by_id(self, item_id: str) -> Optional[domain.ListItem]:
        """Get list item by ID"""
        result = await self.session.execute(select(ListItemDB).where(ListItemDB.id == item_id))
        db_item = result.scalar_one_or_none()
        return db_item.to_domain() if db_item else None

    async def get_list_item(self, list_id: str, item_id: str) -> Optional[domain.ListItem]:
        """Get specific list-item relationship"""
        result = await self.session.execute(
            select(ListItemDB).where(
                and_(ListItemDB.list_id == list_id, ListItemDB.item_id == item_id)
            )
        )
        db_item = result.scalar_one_or_none()
        return db_item.to_domain() if db_item else None

    async def get_items_in_list(
        self, list_id: str, item_type: Optional[str] = None
    ) -> List[domain.ListItem]:
        """Get all items in a list with optional type filtering"""
        query = select(ListItemDB).where(ListItemDB.list_id == list_id)

        if item_type:
            query = query.where(ListItemDB.item_type == item_type)

        query = query.order_by(ListItemDB.position.asc())

        result = await self.session.execute(query)
        db_items = result.scalars().all()
        return [db_item.to_domain() for db_item in db_items]

    async def get_lists_for_item(self, item_id: str, item_type: str) -> List[domain.List]:
        """Get all lists containing a specific item"""
        result = await self.session.execute(
            select(ListDB)
            .join(ListItemDB, ListDB.id == ListItemDB.list_id)
            .where(and_(ListItemDB.item_id == item_id, ListItemDB.item_type == item_type))
            .order_by(ListDB.name)
        )
        db_lists = result.scalars().all()
        return [db_list.to_domain() for db_list in db_lists]

    async def add_item_to_list(
        self,
        list_id: str,
        item_id: str,
        item_type: str,
        added_by: str,
        position: Optional[int] = None,
    ) -> domain.ListItem:
        """Add an item to a list with automatic position assignment"""

        # If no position specified, add at end
        if position is None:
            max_position_result = await self.session.execute(
                select(func.max(ListItemDB.position)).where(ListItemDB.list_id == list_id)
            )
            max_position = max_position_result.scalar() or 0
            position = max_position + 1

        item = domain.ListItem(
            list_id=list_id,
            item_id=item_id,
            item_type=item_type,
            position=position,
            added_by=added_by,
            added_at=datetime.now(),
        )

        return await self.create_item(item)

    async def remove_item_from_list(self, list_id: str, item_id: str) -> bool:
        """Remove an item from a list"""
        result = await self.session.execute(
            select(ListItemDB).where(
                and_(ListItemDB.list_id == list_id, ListItemDB.item_id == item_id)
            )
        )
        db_item = result.scalar_one_or_none()

        if db_item:
            await self.session.delete(db_item)
            return True
        return False

    async def reorder_items_in_list(
        self, list_id: str, item_positions: List[tuple[str, int]]
    ) -> bool:
        """Reorder items in a list by updating positions"""
        try:
            for item_id, new_position in item_positions:
                await self.session.execute(
                    update(ListItemDB)
                    .where(and_(ListItemDB.list_id == list_id, ListItemDB.item_id == item_id))
                    .values(position=new_position)
                )
            return True
        except Exception as e:
            logger.error("Failed to reorder items", list_id=list_id, error=str(e))
            return False

    async def get_item_count(self, list_id: str, item_type: Optional[str] = None) -> int:
        """Get count of items in a list"""
        query = select(func.count(ListItemDB.id)).where(ListItemDB.list_id == list_id)

        if item_type:
            query = query.where(ListItemDB.item_type == item_type)

        result = await self.session.execute(query)
        return result.scalar() or 0

    async def delete_items_for_list(self, list_id: str) -> int:
        """Delete all items for a list (used when deleting list)"""
        result = await self.session.execute(select(ListItemDB).where(ListItemDB.list_id == list_id))
        items = result.scalars().all()

        count = len(items)
        for item in items:
            await self.session.delete(item)

        return count

    async def delete_items_by_item_id(self, item_id: str, item_type: str) -> int:
        """Delete all list memberships for an item (used when deleting the item)"""
        result = await self.session.execute(
            select(ListItemDB).where(
                and_(ListItemDB.item_id == item_id, ListItemDB.item_type == item_type)
            )
        )
        items = result.scalars().all()

        count = len(items)
        for item in items:
            await self.session.delete(item)

        return count


# Backward compatibility wrappers
class TodoListRepository:
    """Backward compatibility wrapper for TodoList operations"""

    def __init__(self, session: AsyncSession):
        self.universal_repo = UniversalListRepository(session)

    async def create_list(self, todo_list: domain.TodoList) -> domain.TodoList:
        """Create a todo list using universal pattern"""
        # Convert TodoList to universal List
        universal_list = domain.List(
            id=todo_list.id,
            name=todo_list.name,
            description=todo_list.description,
            item_type="todo",
            list_type=(
                todo_list.list_type.value
                if hasattr(todo_list.list_type, "value")
                else todo_list.list_type
            ),
            ordering_strategy=(
                todo_list.ordering_strategy.value
                if hasattr(todo_list.ordering_strategy, "value")
                else todo_list.ordering_strategy
            ),
            color=todo_list.color,
            emoji=todo_list.emoji,
            is_archived=todo_list.is_archived,
            is_default=todo_list.is_default,
            metadata=todo_list.metadata,
            tags=todo_list.tags,
            created_at=todo_list.created_at,
            updated_at=todo_list.updated_at,
            owner_id=todo_list.owner_id,
            shared_with=todo_list.shared_with,
        )

        result = await self.universal_repo.create_list(universal_list)

        # Convert back to TodoList for compatibility
        return domain.TodoList(**result.to_dict())

    async def get_list_by_id(
        self, list_id: str, owner_id: str, is_admin: bool = False
    ) -> Optional[domain.TodoList]:
        """Get todo list by ID - verify ownership

        Args:
            list_id: The list ID to retrieve
            owner_id: REQUIRED - the owner ID for multi-tenancy isolation
            is_admin: If True, bypasses ownership check

        Raises:
            ValueError: If owner_id is None or empty (SEC-MULTITENANCY Phase 4)
        """
        result = await self.universal_repo.get_list_by_id(
            list_id, owner_id=owner_id, is_admin=is_admin
        )
        if result and result.item_type == "todo":
            return domain.TodoList(**result.to_dict())
        return None

    async def get_list_for_read(self, list_id: str, user_id: str) -> Optional[domain.TodoList]:
        """Get todo list for reading - allows both owner AND shared users to access

        Args:
            list_id: The list ID to retrieve
            user_id: REQUIRED - the user ID requesting access

        Raises:
            ValueError: If user_id is None or empty (SEC-MULTITENANCY Phase 4)
        """
        result = await self.universal_repo.get_list_for_read(list_id, user_id=user_id)
        if result and result.item_type == "todo":
            return domain.TodoList(**result.to_dict())
        return None

    async def get_lists_by_owner(
        self, owner_id: str, include_archived: bool = False, list_type: Optional[str] = None
    ) -> List[domain.TodoList]:
        """Get todo lists for a user"""
        results = await self.universal_repo.get_lists_by_owner(
            owner_id=owner_id,
            item_type="todo",
            include_archived=include_archived,
            list_type=list_type,
        )
        return [domain.TodoList(**r.to_dict()) for r in results]

    async def get_default_list(self, owner_id: str) -> Optional[domain.TodoList]:
        """Get user's default todo list"""
        result = await self.universal_repo.get_default_list(owner_id, "todo")
        if result:
            return domain.TodoList(**result.to_dict())
        return None

    async def share_list(
        self, list_id: str, owner_id: str, user_id_to_share: str, role: domain.ShareRole = None
    ) -> Optional[domain.TodoList]:
        """Share a todo list with another user at specified role - owner only operation (SEC-RBAC Phase 2)"""
        result = await self.universal_repo.share_list(list_id, owner_id, user_id_to_share, role)
        if result and result.item_type == "todo":
            return domain.TodoList(**result.to_dict())
        return None

    async def unshare_list(
        self, list_id: str, owner_id: str, user_id_to_unshare: str
    ) -> Optional[domain.TodoList]:
        """Remove sharing access from a todo list - owner only operation"""
        result = await self.universal_repo.unshare_list(list_id, owner_id, user_id_to_unshare)
        if result and result.item_type == "todo":
            return domain.TodoList(**result.to_dict())
        return None

    async def get_lists_shared_with_me(self, user_id: str) -> List[domain.TodoList]:
        """Get todo lists that are shared with this user"""
        results = await self.universal_repo.get_lists_shared_with_me(user_id)
        return [domain.TodoList(**r.to_dict()) for r in results if r.item_type == "todo"]

    async def update_share_role(
        self, list_id: str, requesting_user_id: str, target_user_id: str, new_role: domain.ShareRole
    ) -> bool:
        """Update a user's role for a shared todo list (owner only)"""
        return await self.universal_repo.update_share_role(
            list_id, requesting_user_id, target_user_id, new_role
        )

    async def get_user_role(self, list_id: str, user_id: str) -> Optional[str]:
        """Get user's role for a todo list"""
        return await self.universal_repo.get_user_role(list_id, user_id)

    async def update_todo_counts(self, list_id: str) -> None:
        """Update cached todo counts for a list"""
        await self.universal_repo.update_item_counts(list_id)


class ListMembershipRepository:
    """Backward compatibility wrapper for ListMembership operations"""

    def __init__(self, session: AsyncSession):
        self.universal_repo = UniversalListItemRepository(session)

    async def create_membership(self, membership: domain.ListMembership) -> domain.ListMembership:
        """Create a list membership using universal pattern"""
        # Convert ListMembership to universal ListItem
        universal_item = domain.ListItem(
            id=membership.id,
            list_id=membership.list_id,
            item_id=membership.todo_id,
            item_type="todo",
            position=membership.position,
            added_at=membership.added_at,
            added_by=membership.added_by,
            list_priority=(
                membership.list_priority.value
                if hasattr(membership.list_priority, "value")
                else membership.list_priority
            ),
            list_due_date=membership.list_due_date,
            list_notes=membership.list_notes,
        )

        result = await self.universal_repo.create_item(universal_item)

        # Convert back to ListMembership for compatibility
        return domain.ListMembership(**{**result.to_dict(), "todo_id": result.item_id})

    async def add_todo_to_list(
        self, list_id: str, todo_id: str, added_by: str, position: Optional[int] = None
    ) -> domain.ListMembership:
        """Add a todo to a list"""
        result = await self.universal_repo.add_item_to_list(
            list_id=list_id, item_id=todo_id, item_type="todo", added_by=added_by, position=position
        )

        return domain.ListMembership(**{**result.to_dict(), "todo_id": result.item_id})
