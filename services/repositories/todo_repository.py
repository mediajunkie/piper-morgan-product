"""
TodoRepository implementation for PM-081 Todo Management System
Following established repository patterns with AsyncSessionFactory
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from uuid import UUID

import structlog
from sqlalchemy import and_, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import services.domain.models as domain
from services.database.models import ItemDB, ListMembershipDB, TodoDB, TodoListDB
from services.database.repositories import BaseRepository
from services.shared_types import ListType, OrderingStrategy, TodoPriority, TodoStatus

logger = structlog.get_logger()


class TodoListRepository(BaseRepository):
    """Repository for TodoList operations with strategic query optimization"""

    model = TodoListDB

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_list(self, todo_list: domain.TodoList) -> domain.TodoList:
        """Create a new todo list"""
        db_list = TodoListDB.from_domain(todo_list)
        self.session.add(db_list)
        await self.session.flush()
        await self.session.refresh(db_list)
        return db_list.to_domain()

    async def get_list_by_id(
        self, list_id: str, owner_id: str, is_admin: bool = False
    ) -> Optional[domain.TodoList]:
        """Get todo list by ID - verify ownership (SEC-RBAC Phase 3: admins bypass ownership check)

        Args:
            list_id: The list ID to retrieve
            owner_id: REQUIRED - the owner ID for multi-tenancy isolation
            is_admin: If True, bypasses ownership check

        Raises:
            ValueError: If owner_id is None or empty (SEC-MULTITENANCY Phase 4)
        """
        if not owner_id:
            raise ValueError("owner_id is required for multi-tenancy isolation")

        filters = [TodoListDB.id == list_id]
        if not is_admin:
            filters.append(TodoListDB.owner_id == owner_id)

        result = await self.session.execute(select(TodoListDB).where(and_(*filters)))
        db_list = result.scalar_one_or_none()
        return db_list.to_domain() if db_list else None

    async def get_lists_by_owner(
        self, owner_id: str, include_archived: bool = False, list_type: Optional[ListType] = None
    ) -> List[domain.TodoList]:
        """Get todo lists for a user with optional filtering"""
        query = select(TodoListDB).where(TodoListDB.owner_id == owner_id)

        if not include_archived:
            query = query.where(TodoListDB.is_archived == False)

        if list_type:
            query = query.where(TodoListDB.list_type == list_type)

        query = query.order_by(TodoListDB.is_default.desc(), TodoListDB.name)

        result = await self.session.execute(query)
        db_lists = result.scalars().all()
        return [db_list.to_domain() for db_list in db_lists]

    async def get_default_list(self, owner_id: str) -> Optional[domain.TodoList]:
        """Get user's default todo list"""
        result = await self.session.execute(
            select(TodoListDB).where(
                and_(
                    TodoListDB.owner_id == owner_id,
                    TodoListDB.is_default == True,
                    TodoListDB.is_archived == False,
                )
            )
        )
        db_list = result.scalar_one_or_none()
        return db_list.to_domain() if db_list else None

    async def get_shared_lists(self, user_id: UUID) -> List[domain.TodoList]:
        """Get lists shared with a user"""
        # Using JSON array containment for shared_with check
        result = await self.session.execute(
            select(TodoListDB)
            .where(
                and_(TodoListDB.shared_with.contains([user_id]), TodoListDB.is_archived == False)
            )
            .order_by(TodoListDB.name)
        )
        db_lists = result.scalars().all()
        return [db_list.to_domain() for db_list in db_lists]

    async def update_list(
        self, list_id: str, updates: Dict, owner_id: str, is_admin: bool = False
    ) -> Optional[domain.TodoList]:
        """Update todo list - verify ownership (SEC-RBAC Phase 3: admins bypass ownership check)

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

        filters = [TodoListDB.id == list_id]
        if not is_admin:
            filters.append(TodoListDB.owner_id == owner_id)

        result = await self.session.execute(
            update(TodoListDB).where(and_(*filters)).values(**updates).returning(TodoListDB)
        )
        db_list = result.scalar_one_or_none()
        return db_list.to_domain() if db_list else None

    async def update_todo_counts(self, list_id: str, owner_id: str, is_admin: bool = False) -> None:
        """Update cached todo counts for a list - verify ownership (SEC-RBAC Phase 3: admins bypass ownership check)

        Args:
            list_id: The list ID to update counts for
            owner_id: REQUIRED - the owner ID for multi-tenancy isolation
            is_admin: If True, bypasses ownership check

        Raises:
            ValueError: If owner_id is None or empty (SEC-MULTITENANCY Phase 4)
        """
        if not owner_id:
            raise ValueError("owner_id is required for multi-tenancy isolation")

        # Get current counts through list memberships
        total_result = await self.session.execute(
            select(func.count(ListMembershipDB.id)).where(ListMembershipDB.list_id == list_id)
        )
        total_count = total_result.scalar() or 0

        completed_result = await self.session.execute(
            select(func.count(ListMembershipDB.id))
            .select_from(ListMembershipDB)
            .join(TodoDB, ListMembershipDB.todo_id == TodoDB.id)
            .where(and_(ListMembershipDB.list_id == list_id, TodoDB.status == TodoStatus.COMPLETED))
        )
        completed_count = completed_result.scalar() or 0

        # Update the list with new counts (with ownership verification if provided)
        filters = [TodoListDB.id == list_id]
        if not is_admin:
            filters.append(TodoListDB.owner_id == owner_id)

        await self.session.execute(
            update(TodoListDB)
            .where(and_(*filters))
            .values(
                todo_count=total_count, completed_count=completed_count, updated_at=datetime.now()
            )
        )

    async def delete_list(self, list_id: str, owner_id: str, is_admin: bool = False) -> bool:
        """Delete a todo list - verify ownership (SEC-RBAC Phase 3: admins bypass ownership check)

        Args:
            list_id: The list ID to delete
            owner_id: REQUIRED - the owner ID for multi-tenancy isolation
            is_admin: If True, bypasses ownership check

        Raises:
            ValueError: If owner_id is None or empty (SEC-MULTITENANCY Phase 4)
        """
        if not owner_id:
            raise ValueError("owner_id is required for multi-tenancy isolation")

        filters = [TodoListDB.id == list_id]
        if not is_admin:
            filters.append(TodoListDB.owner_id == owner_id)

        result = await self.session.execute(select(TodoListDB).where(and_(*filters)))
        db_list = result.scalar_one_or_none()

        if db_list:
            await self.session.delete(db_list)
            return True
        return False

    async def search_lists_by_name(self, owner_id: str, query: str) -> List[domain.TodoList]:
        """Search lists by name (case-insensitive)

        Args:
            owner_id: REQUIRED - the owner ID for multi-tenancy isolation
            query: Search query string

        Raises:
            ValueError: If owner_id is None or empty (SEC-MULTITENANCY Phase 4)
        """
        if not owner_id:
            raise ValueError("owner_id is required for multi-tenancy isolation")

        result = await self.session.execute(
            select(TodoListDB)
            .where(
                and_(
                    TodoListDB.owner_id == owner_id,
                    TodoListDB.name.ilike(f"%{query}%"),
                    TodoListDB.is_archived == False,
                )
            )
            .order_by(TodoListDB.name)
        )
        db_lists = result.scalars().all()
        return [db_list.to_domain() for db_list in db_lists]


class TodoRepository(BaseRepository):
    """Repository for Todo operations with comprehensive indexing support"""

    model = TodoDB

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_todo(self, todo: domain.Todo) -> domain.Todo:
        """Create a new todo"""
        db_todo = TodoDB.from_domain(todo)
        self.session.add(db_todo)
        await self.session.flush()
        await self.session.refresh(db_todo)
        return db_todo.to_domain()

    async def get_todo_by_id(
        self, todo_id: str, owner_id: str, is_admin: bool = False
    ) -> Optional[domain.Todo]:
        """Get todo by ID with optional subtask loading (admin bypass in SEC-RBAC Phase 3)

        Args:
            todo_id: The todo ID to retrieve
            owner_id: REQUIRED - the owner ID for multi-tenancy isolation
            is_admin: If True, bypasses ownership check

        Raises:
            ValueError: If owner_id is None or empty (SEC-MULTITENANCY Phase 4)
        """
        if not owner_id:
            raise ValueError("owner_id is required for multi-tenancy isolation")

        filters = [TodoDB.id == todo_id]
        if not is_admin:  # Only check ownership if not admin
            filters.append(TodoDB.owner_id == owner_id)

        result = await self.session.execute(
            select(TodoDB).options(selectinload(TodoDB.children)).where(and_(*filters))
        )
        db_todo = result.scalar_one_or_none()
        return db_todo.to_domain() if db_todo else None

    async def get_todos_by_owner(
        self,
        owner_id: str,
        status: Optional[TodoStatus] = None,
        priority: Optional[TodoPriority] = None,
        context: Optional[str] = None,
        project_id: Optional[str] = None,
        limit: int = 100,
    ) -> List[domain.Todo]:
        """Get todos for owner with comprehensive filtering"""
        query = select(TodoDB).where(TodoDB.owner_id == owner_id)

        if status:
            query = query.where(TodoDB.status == status)
        if priority:
            query = query.where(TodoDB.priority == priority)
        if context:
            query = query.where(TodoDB.context == context)
        if project_id:
            query = query.where(TodoDB.project_id == project_id)

        query = query.order_by(
            TodoDB.priority.desc(), TodoDB.due_date.asc().nulls_last(), TodoDB.created_at.desc()
        ).limit(limit)

        result = await self.session.execute(query)
        db_todos = result.scalars().all()
        return [db_todo.to_domain() for db_todo in db_todos]

    async def get_assigned_todos(
        self, assigned_to: str, status: Optional[TodoStatus] = None
    ) -> List[domain.Todo]:
        """Get todos assigned to a user"""
        query = select(TodoDB).where(TodoDB.assigned_to == assigned_to)

        if status:
            query = query.where(TodoDB.status == status)

        query = query.order_by(TodoDB.priority.desc(), TodoDB.due_date.asc().nulls_last())

        result = await self.session.execute(query)
        db_todos = result.scalars().all()
        return [db_todo.to_domain() for db_todo in db_todos]

    async def get_due_todos(
        self, owner_id: str, due_before: Optional[datetime] = None, include_overdue: bool = True
    ) -> List[domain.Todo]:
        """Get todos by due date with overdue support"""
        query = select(TodoDB).where(
            and_(
                TodoDB.owner_id == owner_id,
                TodoDB.status != TodoStatus.COMPLETED,
                TodoDB.due_date.is_not(None),
            )
        )

        if due_before:
            query = query.where(TodoDB.due_date <= due_before)
        elif include_overdue:
            query = query.where(TodoDB.due_date <= datetime.now())

        query = query.order_by(TodoDB.due_date.asc())

        result = await self.session.execute(query)
        db_todos = result.scalars().all()
        return [db_todo.to_domain() for db_todo in db_todos]

    async def get_subtodos(self, parent_id: str) -> List[domain.Todo]:
        """Get subtodos for a parent todo"""
        result = await self.session.execute(
            select(TodoDB)
            .where(TodoDB.parent_id == parent_id)
            .order_by(TodoDB.position.asc(), TodoDB.created_at.asc())
        )
        db_todos = result.scalars().all()
        return [db_todo.to_domain() for db_todo in db_todos]

    async def get_root_todos(self, owner_id: str) -> List[domain.Todo]:
        """Get all root-level todos (no parent)"""
        result = await self.session.execute(
            select(TodoDB)
            .where(and_(TodoDB.owner_id == owner_id, TodoDB.parent_id.is_(None)))
            .order_by(TodoDB.created_at.desc())
        )
        db_todos = result.scalars().all()
        return [db_todo.to_domain() for db_todo in db_todos]

    async def search_todos(
        self,
        owner_id: str,
        query: str,
        context: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> List[domain.Todo]:
        """Search todos by text/description with optional context filtering"""
        search_query = select(TodoDB).where(
            and_(
                TodoDB.owner_id == owner_id,
                or_(TodoDB.text.ilike(f"%{query}%"), TodoDB.description.ilike(f"%{query}%")),
            )
        )

        if context:
            search_query = search_query.where(TodoDB.context == context)
        if project_id:
            search_query = search_query.where(TodoDB.project_id == project_id)

        search_query = search_query.order_by(TodoDB.updated_at.desc())

        result = await self.session.execute(search_query)
        db_todos = result.scalars().all()
        return [db_todo.to_domain() for db_todo in db_todos]

    async def get_todos_by_knowledge_node(self, knowledge_node_id: str) -> List[domain.Todo]:
        """Get todos linked to a Knowledge Graph node"""
        result = await self.session.execute(
            select(TodoDB).where(TodoDB.knowledge_node_id == knowledge_node_id)
        )
        db_todos = result.scalars().all()
        return [db_todo.to_domain() for db_todo in db_todos]

    async def get_related_todos(self, todo_id: str) -> List[domain.Todo]:
        """Get todos related to a specific todo via related_todos field"""
        # First get the todo to access its related_todos list
        todo = await self.get_todo_by_id(todo_id)
        if not todo or not todo.related_todos:
            return []

        result = await self.session.execute(select(TodoDB).where(TodoDB.id.in_(todo.related_todos)))
        db_todos = result.scalars().all()
        return [db_todo.to_domain() for db_todo in db_todos]

    async def update_todo(
        self, todo_id: str, updates: Dict, owner_id: str, is_admin: bool = False
    ) -> Optional[domain.Todo]:
        """Update todo with optimistic field updates (admin bypass in SEC-RBAC Phase 3)

        Args:
            todo_id: The todo ID to update
            updates: Dictionary of fields to update
            owner_id: REQUIRED - the owner ID for multi-tenancy isolation
            is_admin: If True, bypasses ownership check

        Raises:
            ValueError: If owner_id is None or empty (SEC-MULTITENANCY Phase 4)
        """
        if not owner_id:
            raise ValueError("owner_id is required for multi-tenancy isolation")

        # Separate inherited fields (from ItemDB) from child-specific fields (from TodoDB)
        # updated_at lives on parent ItemDB; including it in child_updates causes
        # SQLAlchemy CompileError "Unconsumed column names: updated_at"
        inherited_fields = {"text", "position", "list_id", "created_at", "updated_at"}
        child_updates = {k: v for k, v in updates.items() if k not in inherited_fields}
        parent_updates = {k: v for k, v in updates.items() if k in inherited_fields}

        filters = [TodoDB.id == todo_id]
        if not is_admin:  # Only check ownership if not admin
            filters.append(TodoDB.owner_id == owner_id)

        # Always update updated_at on parent table (ItemDB)
        parent_updates["updated_at"] = datetime.now()

        # Build query to fetch the todo first
        select_stmt = select(TodoDB).where(and_(*filters))
        result = await self.session.execute(select_stmt)
        db_todo = result.scalar_one_or_none()

        if not db_todo:
            return None

        # Update parent (ItemDB) fields if any exist
        if parent_updates:
            parent_stmt = update(ItemDB).where(ItemDB.id == todo_id).values(**parent_updates)
            await self.session.execute(parent_stmt)

        # Update child (TodoDB) fields if any exist
        if child_updates:
            child_stmt = update(TodoDB).where(TodoDB.id == todo_id).values(**child_updates)
            await self.session.execute(child_stmt)

        # Refresh the todo to get updated values
        if parent_updates or child_updates:
            result = await self.session.execute(select_stmt)
            db_todo = result.scalar_one_or_none()

        return db_todo.to_domain() if db_todo else None

    async def complete_todo(
        self, todo_id: str, owner_id: str, completion_notes: str = "", is_admin: bool = False
    ) -> Optional[domain.Todo]:
        """Complete a todo with timestamp and notes

        Args:
            todo_id: The todo ID to complete
            owner_id: REQUIRED - the owner ID for multi-tenancy isolation
            completion_notes: Optional notes about completion
            is_admin: If True, bypasses ownership check

        Raises:
            ValueError: If owner_id is None or empty (SEC-MULTITENANCY Phase 4)
        """
        if not owner_id:
            raise ValueError("owner_id is required for multi-tenancy isolation")

        updates = {
            "status": TodoStatus.COMPLETED.value,
            "completed": True,  # Boolean field used by list_todos filter
            "completed_at": datetime.now(),
            "completion_notes": completion_notes,
            "updated_at": datetime.now(),
        }
        return await self.update_todo(todo_id, updates, owner_id=owner_id, is_admin=is_admin)

    async def reopen_todo(
        self, todo_id: str, owner_id: str, is_admin: bool = False
    ) -> Optional[domain.Todo]:
        """Reopen a completed todo

        Args:
            todo_id: The todo ID to reopen
            owner_id: REQUIRED - the owner ID for multi-tenancy isolation
            is_admin: If True, bypasses ownership check

        Raises:
            ValueError: If owner_id is None or empty (SEC-MULTITENANCY Phase 4)
        """
        if not owner_id:
            raise ValueError("owner_id is required for multi-tenancy isolation")

        updates = {
            "status": TodoStatus.PENDING.value,
            "completed": False,  # Boolean field used by list_todos filter
            "completed_at": None,
            "updated_at": datetime.now(),
        }
        return await self.update_todo(todo_id, updates, owner_id=owner_id, is_admin=is_admin)

    async def delete_todo(self, todo_id: str, owner_id: str, is_admin: bool = False) -> bool:
        """Delete a todo (admin bypass in SEC-RBAC Phase 3, cascades to subtodos and memberships)

        Args:
            todo_id: The todo ID to delete
            owner_id: REQUIRED - the owner ID for multi-tenancy isolation
            is_admin: If True, bypasses ownership check

        Raises:
            ValueError: If owner_id is None or empty (SEC-MULTITENANCY Phase 4)
        """
        if not owner_id:
            raise ValueError("owner_id is required for multi-tenancy isolation")

        filters = [TodoDB.id == todo_id]
        if not is_admin:  # Only check ownership if not admin
            filters.append(TodoDB.owner_id == owner_id)

        result = await self.session.execute(select(TodoDB).where(and_(*filters)))
        db_todo = result.scalar_one_or_none()

        if db_todo:
            await self.session.delete(db_todo)
            return True
        return False

    async def get_completion_stats(self, owner_id: str, days: int = 30) -> Dict[str, int]:
        """Get completion statistics for a user over specified days"""
        cutoff_date = datetime.now() - timedelta(days=days)

        # Total todos created in period
        total_result = await self.session.execute(
            select(func.count(TodoDB.id)).where(
                and_(TodoDB.owner_id == owner_id, TodoDB.created_at >= cutoff_date)
            )
        )
        total_created = total_result.scalar() or 0

        # Completed todos in period
        completed_result = await self.session.execute(
            select(func.count(TodoDB.id)).where(
                and_(
                    TodoDB.owner_id == owner_id,
                    TodoDB.status == TodoStatus.COMPLETED,
                    TodoDB.completed_at >= cutoff_date,
                )
            )
        )
        completed_count = completed_result.scalar() or 0

        # Currently active todos
        active_result = await self.session.execute(
            select(func.count(TodoDB.id)).where(
                and_(
                    TodoDB.owner_id == owner_id,
                    TodoDB.status.in_([TodoStatus.PENDING, TodoStatus.IN_PROGRESS]),
                )
            )
        )
        active_count = active_result.scalar() or 0

        return {
            "total_created": total_created,
            "completed": completed_count,
            "active": active_count,
            "completion_rate": (completed_count / total_created * 100) if total_created > 0 else 0,
        }

    async def share_todo(
        self, todo_id: str, owner_id: str, user_id_to_share: str, role: domain.ShareRole = None
    ) -> Optional[domain.Todo]:
        """Share a todo with another user at specified role - owner only operation (SEC-RBAC Phase 2)"""
        # Default role if not specified
        if role is None:
            role = domain.ShareRole.VIEWER

        # First verify the caller is the owner
        result = await self.session.execute(
            select(TodoDB).where(and_(TodoDB.id == todo_id, TodoDB.owner_id == owner_id))
        )
        db_todo = result.scalar_one_or_none()

        if not db_todo:
            return None  # Not found or not owner

        # Prevent owner from sharing with themselves (no-op)
        if user_id_to_share == owner_id:
            return db_todo.to_domain()

        # Convert to domain object to work with SharePermission objects
        domain_todo = db_todo.to_domain()

        # Check if user already shared with - update role if exists, otherwise add new share
        permission = domain.SharePermission(user_id=user_id_to_share, role=role)
        existing_index = None

        for idx, perm in enumerate(domain_todo.shared_with):
            if perm.user_id == user_id_to_share:
                existing_index = idx
                break

        if existing_index is not None:
            # Update existing permission
            domain_todo.shared_with[existing_index] = permission
        else:
            # Add new permission
            domain_todo.shared_with.append(permission)

        # Convert back to JSONB format for database storage
        shared_with_jsonb = [perm.to_dict() for perm in domain_todo.shared_with]

        # Update database
        await self.session.execute(
            update(TodoDB)
            .where(TodoDB.id == todo_id)
            .values(shared_with=shared_with_jsonb, updated_at=datetime.now())
        )

        # Refresh and return updated todo
        await self.session.refresh(db_todo)
        return db_todo.to_domain()

    async def unshare_todo(
        self, todo_id: str, owner_id: str, user_id_to_unshare: str
    ) -> Optional[domain.Todo]:
        """Remove sharing access from a todo - owner only operation (SEC-RBAC Phase 2)"""
        # First verify the caller is the owner
        result = await self.session.execute(
            select(TodoDB).where(and_(TodoDB.id == todo_id, TodoDB.owner_id == owner_id))
        )
        db_todo = result.scalar_one_or_none()

        if not db_todo:
            return None  # Not found or not owner

        # Convert to domain object to work with SharePermission objects
        domain_todo = db_todo.to_domain()

        # Remove user from shared_with array
        domain_todo.shared_with = [
            perm for perm in domain_todo.shared_with if perm.user_id != user_id_to_unshare
        ]

        # Convert back to JSONB format for database storage
        shared_with_jsonb = [perm.to_dict() for perm in domain_todo.shared_with]

        # Update database
        await self.session.execute(
            update(TodoDB)
            .where(TodoDB.id == todo_id)
            .values(shared_with=shared_with_jsonb, updated_at=datetime.now())
        )

        # Refresh and return updated todo
        await self.session.refresh(db_todo)
        return db_todo.to_domain()

    async def get_todos_shared_with_me(self, user_id: str) -> List[domain.Todo]:
        """Get todos that are shared with this user (excluding owned todos - SEC-RBAC Phase 1.4)"""
        # Use PostgreSQL's contains operator to check if user is in shared_with array
        query = select(TodoDB).where(
            and_(
                TodoDB.shared_with.contains([user_id]),  # User is in shared_with array
                TodoDB.owner_id != user_id,  # Not owned by this user
            )
        )

        query = query.order_by(TodoDB.created_at.desc())

        result = await self.session.execute(query)
        db_todos = result.scalars().all()
        return [db_todo.to_domain() for db_todo in db_todos]

    async def update_share_role(
        self, todo_id: str, requesting_user_id: str, target_user_id: str, new_role: domain.ShareRole
    ) -> bool:
        """Update a user's role for a shared todo (owner or admin only)"""
        # Verify requestor is owner
        result = await self.session.execute(
            select(TodoDB).where(and_(TodoDB.id == todo_id, TodoDB.owner_id == requesting_user_id))
        )
        db_todo = result.scalar_one_or_none()

        if not db_todo:
            return False  # Not found or not owner

        # Convert to domain object to work with SharePermission objects
        domain_todo = db_todo.to_domain()

        # Find and update the permission
        found = False
        for perm in domain_todo.shared_with:
            if perm.user_id == target_user_id:
                perm.role = new_role
                found = True
                break

        if not found:
            return False  # User not in shared_with

        # Convert back to JSONB format for database storage
        shared_with_jsonb = [perm.to_dict() for perm in domain_todo.shared_with]

        # Update database
        await self.session.execute(
            update(TodoDB)
            .where(TodoDB.id == todo_id)
            .values(shared_with=shared_with_jsonb, updated_at=datetime.now())
        )

        return True

    async def get_user_role(self, todo_id: str, user_id: str) -> Optional[str]:
        """Get user's role for a todo"""
        # Get the todo
        result = await self.session.execute(select(TodoDB).where(TodoDB.id == todo_id))
        db_todo = result.scalar_one_or_none()

        if not db_todo:
            return None

        # Check if owner
        if db_todo.owner_id == user_id:
            return "owner"

        # Convert to domain object to search shared_with
        domain_todo = db_todo.to_domain()

        for perm in domain_todo.shared_with:
            if perm.user_id == user_id:
                return perm.role.value

        return None


class ListMembershipRepository(BaseRepository):
    """Repository for ListMembership operations managing many-to-many relationships"""

    model = ListMembershipDB

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_membership(self, membership: domain.ListMembership) -> domain.ListMembership:
        """Create a list membership"""
        db_membership = ListMembershipDB.from_domain(membership)
        self.session.add(db_membership)
        await self.session.flush()
        await self.session.refresh(db_membership)
        return db_membership.to_domain()

    async def get_membership_by_id(self, membership_id: str) -> Optional[domain.ListMembership]:
        """Get membership by ID"""
        result = await self.session.execute(
            select(ListMembershipDB).where(ListMembershipDB.id == membership_id)
        )
        db_membership = result.scalar_one_or_none()
        return db_membership.to_domain() if db_membership else None

    async def get_membership(self, list_id: str, todo_id: str) -> Optional[domain.ListMembership]:
        """Get specific list-todo membership"""
        result = await self.session.execute(
            select(ListMembershipDB).where(
                and_(ListMembershipDB.list_id == list_id, ListMembershipDB.todo_id == todo_id)
            )
        )
        db_membership = result.scalar_one_or_none()
        return db_membership.to_domain() if db_membership else None

    async def get_todos_in_list(
        self, list_id: str, ordering_strategy: OrderingStrategy = OrderingStrategy.MANUAL
    ) -> List[domain.Todo]:
        """Get todos in a list with specified ordering"""

        # Build the base query joining memberships with todos
        query = (
            select(TodoDB)
            .join(ListMembershipDB, TodoDB.id == ListMembershipDB.todo_id)
            .where(ListMembershipDB.list_id == list_id)
        )

        # Apply ordering based on strategy
        if ordering_strategy == OrderingStrategy.MANUAL:
            query = query.order_by(ListMembershipDB.position.asc())
        elif ordering_strategy == OrderingStrategy.PRIORITY:
            query = query.order_by(TodoDB.priority.desc(), ListMembershipDB.position.asc())
        elif ordering_strategy == OrderingStrategy.DUE_DATE:
            query = query.order_by(
                TodoDB.due_date.asc().nulls_last(), ListMembershipDB.position.asc()
            )
        elif ordering_strategy == OrderingStrategy.CREATED_DATE:
            query = query.order_by(TodoDB.created_at.desc())
        elif ordering_strategy == OrderingStrategy.ALPHABETICAL:
            query = query.order_by(TodoDB.text.asc())
        elif ordering_strategy == OrderingStrategy.STATUS:
            query = query.order_by(TodoDB.status.asc(), ListMembershipDB.position.asc())

        result = await self.session.execute(query)
        db_todos = result.scalars().all()
        return [db_todo.to_domain() for db_todo in db_todos]

    async def get_lists_for_todo(self, todo_id: str) -> List[domain.TodoList]:
        """Get all lists containing a specific todo"""
        result = await self.session.execute(
            select(TodoListDB)
            .join(ListMembershipDB, TodoListDB.id == ListMembershipDB.list_id)
            .where(ListMembershipDB.todo_id == todo_id)
            .order_by(TodoListDB.name)
        )
        db_lists = result.scalars().all()
        return [db_list.to_domain() for db_list in db_lists]

    async def add_todo_to_list(
        self, list_id: str, todo_id: str, added_by: str, position: Optional[int] = None
    ) -> domain.ListMembership:
        """Add a todo to a list with automatic position assignment"""

        # If no position specified, add at end
        if position is None:
            max_position_result = await self.session.execute(
                select(func.max(ListMembershipDB.position)).where(
                    ListMembershipDB.list_id == list_id
                )
            )
            max_position = max_position_result.scalar() or 0
            position = max_position + 1

        membership = domain.ListMembership(
            list_id=list_id,
            todo_id=todo_id,
            position=position,
            added_by=added_by,
            added_at=datetime.now(),
        )

        return await self.create_membership(membership)

    async def remove_todo_from_list(self, list_id: str, todo_id: str) -> bool:
        """Remove a todo from a list"""
        result = await self.session.execute(
            select(ListMembershipDB).where(
                and_(ListMembershipDB.list_id == list_id, ListMembershipDB.todo_id == todo_id)
            )
        )
        db_membership = result.scalar_one_or_none()

        if db_membership:
            await self.session.delete(db_membership)
            return True
        return False

    async def reorder_todos_in_list(
        self, list_id: str, todo_positions: List[tuple[str, int]]
    ) -> bool:
        """Reorder todos in a list by updating positions"""
        try:
            for todo_id, new_position in todo_positions:
                await self.session.execute(
                    update(ListMembershipDB)
                    .where(
                        and_(
                            ListMembershipDB.list_id == list_id, ListMembershipDB.todo_id == todo_id
                        )
                    )
                    .values(position=new_position)
                )
            return True
        except Exception as e:
            logger.error("Failed to reorder todos", list_id=list_id, error=str(e))
            return False

    async def get_membership_count(self, list_id: str) -> int:
        """Get count of todos in a list"""
        result = await self.session.execute(
            select(func.count(ListMembershipDB.id)).where(ListMembershipDB.list_id == list_id)
        )
        return result.scalar() or 0

    async def delete_memberships_for_todo(self, todo_id: str) -> int:
        """Delete all list memberships for a todo (used when deleting todo)"""
        result = await self.session.execute(
            select(ListMembershipDB).where(ListMembershipDB.todo_id == todo_id)
        )
        memberships = result.scalars().all()

        count = len(memberships)
        for membership in memberships:
            await self.session.delete(membership)

        return count

    async def delete_memberships_for_list(self, list_id: str) -> int:
        """Delete all memberships for a list (used when deleting list)"""
        result = await self.session.execute(
            select(ListMembershipDB).where(ListMembershipDB.list_id == list_id)
        )
        memberships = result.scalars().all()

        count = len(memberships)
        for membership in memberships:
            await self.session.delete(membership)

        return count


# Integrated Todo Repository combining all three repositories
class TodoManagementRepository:
    """
    Integrated repository for complete Todo Management System operations
    Provides high-level operations across TodoList, Todo, and ListMembership
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.todo_lists = TodoListRepository(session)
        self.todos = TodoRepository(session)
        self.memberships = ListMembershipRepository(session)

    async def create_todo_in_list(
        self, todo: domain.Todo, list_id: str, added_by: str, owner_id: str
    ) -> tuple[domain.Todo, domain.ListMembership]:
        """Create a todo and add it to a list in one operation

        Args:
            todo: The todo domain object to create
            list_id: The list to add the todo to
            added_by: Who is adding the todo
            owner_id: REQUIRED - the owner ID for multi-tenancy isolation

        Raises:
            ValueError: If owner_id is None or empty (SEC-MULTITENANCY Phase 4)
        """
        if not owner_id:
            raise ValueError("owner_id is required for multi-tenancy isolation")

        # Create the todo
        created_todo = await self.todos.create_todo(todo)

        # Add to list
        membership = await self.memberships.add_todo_to_list(
            list_id=list_id, todo_id=created_todo.id, added_by=added_by
        )

        # Update list counts with owner verification
        await self.todo_lists.update_todo_counts(list_id, owner_id=owner_id)

        return created_todo, membership

    async def delete_todo_from_everywhere(self, todo_id: str, owner_id: str) -> Dict[str, int]:
        """Delete a todo from all lists and remove the todo itself

        Args:
            todo_id: The todo ID to delete
            owner_id: REQUIRED - the owner ID for multi-tenancy isolation

        Raises:
            ValueError: If owner_id is None or empty (SEC-MULTITENANCY Phase 4)
        """
        if not owner_id:
            raise ValueError("owner_id is required for multi-tenancy isolation")

        # Get all lists containing this todo for count updates
        lists_with_todo = await self.memberships.get_lists_for_todo(todo_id)

        # Remove from all lists
        memberships_deleted = await self.memberships.delete_memberships_for_todo(todo_id)

        # Delete the todo itself with owner verification
        todo_deleted = await self.todos.delete_todo(todo_id, owner_id=owner_id)

        # Update counts for affected lists
        for todo_list in lists_with_todo:
            await self.todo_lists.update_todo_counts(todo_list.id, owner_id=owner_id)

        return {
            "todo_deleted": 1 if todo_deleted else 0,
            "memberships_deleted": memberships_deleted,
            "lists_updated": len(lists_with_todo),
        }

    async def complete_todo_in_all_lists(
        self, todo_id: str, owner_id: str, completion_notes: str = ""
    ) -> Optional[domain.Todo]:
        """Complete a todo and update counts in all containing lists

        Args:
            todo_id: The todo ID to complete
            owner_id: REQUIRED - the owner ID for multi-tenancy isolation
            completion_notes: Optional notes about completion

        Raises:
            ValueError: If owner_id is None or empty (SEC-MULTITENANCY Phase 4)
        """
        if not owner_id:
            raise ValueError("owner_id is required for multi-tenancy isolation")

        # Complete the todo with owner verification
        completed_todo = await self.todos.complete_todo(
            todo_id, owner_id=owner_id, completion_notes=completion_notes
        )

        if completed_todo:
            # Get all lists containing this todo
            lists_with_todo = await self.memberships.get_lists_for_todo(todo_id)

            # Update counts for all affected lists
            for todo_list in lists_with_todo:
                await self.todo_lists.update_todo_counts(todo_list.id, owner_id=owner_id)

        return completed_todo

    async def get_user_dashboard(self, user_id: UUID) -> Dict[str, any]:
        """Get comprehensive dashboard data for a user"""
        # Get user's lists
        user_lists = await self.todo_lists.get_lists_by_owner(user_id)

        # Get completion stats
        stats = await self.todos.get_completion_stats(user_id)

        # Get due/overdue todos
        due_todos = await self.todos.get_due_todos(user_id, include_overdue=True)

        # Get assigned todos
        assigned_todos = await self.todos.get_assigned_todos(user_id)

        return {
            "lists": user_lists,
            "stats": stats,
            "due_todos": due_todos,
            "assigned_todos": assigned_todos,
            "overdue_count": len([t for t in due_todos if t.is_overdue()]),
            "due_today_count": len([t for t in due_todos if t.is_due_today()]),
        }
