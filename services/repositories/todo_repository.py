"""
TodoRepository implementation for PM-081 Todo Management System
Following established repository patterns with AsyncSessionFactory
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from uuid import UUID

import structlog
from sqlalchemy import and_, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import services.domain.models as domain
from services.database.models import ItemDB, TodoDB
from services.database.repositories import BaseRepository
from services.shared_types import TodoPriority, TodoStatus

logger = structlog.get_logger()


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


