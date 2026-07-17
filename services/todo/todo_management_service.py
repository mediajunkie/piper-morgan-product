"""
Todo Management Service

Business logic layer for todo operations.
Orchestrates TodoService, TodoRepository, and TodoKnowledgeService.

Architecture:
- Manages transactions (AsyncSessionFactory.session_scope)
- Validates business rules (ownership, permissions)
- Coordinates domain operations via TodoService
- Handles persistence via TodoRepository
- Optional: Knowledge graph integration via TodoKnowledgeService

Examples:
    >>> service = TodoManagementService()
    >>> todo = await service.create_todo(
    ...     user_id="user-123",
    ...     text="Review PR",
    ...     priority="high"
    ... )
    >>> print(f"Created todo {todo.id}: {todo.text}")
"""

from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4

import structlog

from services.database.session_factory import AsyncSessionFactory
from services.domain.models import Todo
from services.repositories.todo_repository import TodoRepository

logger = structlog.get_logger()
from services.todo_service import TodoService

if TYPE_CHECKING:
    from services.todo.todo_knowledge_service import TodoKnowledgeService


class TodoManagementService:
    """Service for managing todo operations with business logic.

    This service provides the business logic layer between handlers/API
    and the repository layer. It:
    - Manages database transactions
    - Validates business rules (ownership, etc.)
    - Coordinates TodoService and TodoRepository
    - Handles errors gracefully
    - Optional: Integrates with knowledge graph

    Architecture Decision (Nov 3, 2025 - Chief Architect):
    - Service layer approach chosen over direct repository access
    - Service manages transactions (not repository)
    - Use TodoRepository (not UniversalList migration)
    """

    def __init__(
        self,
        todo_service: Optional[TodoService] = None,
        knowledge_service: Optional["TodoKnowledgeService"] = None,
    ):
        """Initialize service with dependencies.

        Args:
            todo_service: Optional TodoService (created if not provided)
            knowledge_service: Optional knowledge graph service
        """
        self.todo_service = todo_service or TodoService()
        self.knowledge_service = knowledge_service

    async def create_todo(
        self,
        user_id: UUID,
        text: str,
        priority: str = "medium",
        list_id: Optional[str] = None,
        due_date: Optional[datetime] = None,
        **kwargs,
    ) -> Todo:
        """Create a new todo with database persistence.

        This is the main entry point for creating todos. It:
        1. Validates input
        2. Creates todo in database via repository
        3. Optional: Creates knowledge node
        4. Returns persisted todo

        Args:
            user_id: Owner of the todo
            text: Todo text/title
            priority: Priority level (low, medium, high, urgent)
            list_id: Optional list to add todo to
            due_date: Optional due date
            **kwargs: Additional todo fields

        Returns:
            Created Todo with database ID

        Raises:
            ValueError: If validation fails
            DatabaseError: If persistence fails

        Examples:
            >>> service = TodoManagementService()
            >>> todo = await service.create_todo(
            ...     user_id="user-123",
            ...     text="Review PR",
            ...     priority="high"
            ... )
            >>> assert todo.id is not None  # Has database ID
            >>> assert todo.text == "Review PR"
        """
        # Validate input
        if not text or not text.strip():
            raise ValueError("Todo text cannot be empty")

        if priority not in ["low", "medium", "high", "urgent"]:
            raise ValueError(f"Invalid priority: {priority}")

        # Create todo via service (domain operation)
        async with AsyncSessionFactory.session_scope() as session:
            # Create repository with session
            todo_repo = TodoRepository(session)

            # Create todo domain object
            # Note: Convert UUID to string for database (ItemDB.id is String type)
            todo = Todo(
                id=str(uuid4()),
                text=text.strip(),
                priority=priority,
                owner_id=user_id,
                list_id=list_id,
                due_date=due_date,
                status="pending",
                completed=False,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                **kwargs,
            )

            # Persist to database
            saved_todo = await todo_repo.create_todo(todo)

            # Commit the transaction to persist to database
            await session.commit()

            # Optional: Create knowledge node
            if self.knowledge_service:
                try:
                    # #1436 B8: user_id was missing — the TypeError was swallowed
                    # below (via print!, census F14), so the KG got a node for NO
                    # todo ever created; downstream KG-todo features starved.
                    await self.knowledge_service.create_todo_knowledge_node(
                        saved_todo, str(user_id)
                    )
                except Exception as e:  # silent-ok: KG side-write is best-effort by design — todo creation itself succeeded and says so; failure is WARN-logged (#1436 B8)
                    logger.warning(
                        "todo_knowledge_node_creation_failed",
                        todo_id=saved_todo.id,
                        error=str(e),
                    )

            # #984: Invalidate cached todo lists so the next floor query
            # reflects this new todo immediately.
            from services.intent_service.cache_invalidation import invalidate_user_todos

            await invalidate_user_todos(user_id)

            return saved_todo

    async def list_todos(
        self,
        user_id: UUID,
        list_id: Optional[str] = None,
        status: Optional[str] = None,
        include_completed: bool = False,
    ) -> List[Todo]:
        """List todos for a user.

        Args:
            user_id: Owner ID to filter by
            list_id: Optional list to filter by
            status: Optional status filter
            include_completed: Include completed todos

        Returns:
            List of todos matching filters

        Examples:
            >>> todos = await service.list_todos(user_id="user-123")
            >>> active = await service.list_todos(
            ...     user_id="user-123",
            ...     include_completed=False
            ... )
        """
        async with AsyncSessionFactory.session_scope() as session:
            todo_repo = TodoRepository(session)

            # Get todos by owner
            todos = await todo_repo.get_todos_by_owner(user_id)

            # Filter by list if specified
            if list_id:
                todos = [t for t in todos if t.list_id == list_id]

            # Filter by status if specified
            if status:
                todos = [t for t in todos if t.status == status]

            # Filter completed if requested
            if not include_completed:
                todos = [t for t in todos if not t.completed]

            return todos

    async def get_todo(self, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
        """Get a specific todo by ID.

        Args:
            todo_id: Todo ID
            user_id: REQUIRED - User ID for multi-tenancy isolation

        Returns:
            Todo if found and authorized, None otherwise

        Examples:
            >>> todo = await service.get_todo(todo_id, user_id="user-123")
            >>> if todo:
            ...     print(f"Found: {todo.text}")
        """
        async with AsyncSessionFactory.session_scope() as session:
            todo_repo = TodoRepository(session)

            # SEC-MULTITENANCY Phase 4: Pass owner_id for isolation
            todo = await todo_repo.get_todo_by_id(todo_id, owner_id=str(user_id))

            return todo

    async def complete_todo(self, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
        """Mark a todo as complete.

        Args:
            todo_id: Todo to complete
            user_id: REQUIRED - User completing the todo (for authorization and isolation)

        Returns:
            Completed todo, or None if not found/unauthorized

        Examples:
            >>> completed = await service.complete_todo(todo_id, user_id)
            >>> assert completed.completed is True
        """
        async with AsyncSessionFactory.session_scope() as session:
            todo_repo = TodoRepository(session)

            # SEC-MULTITENANCY Phase 4: Complete with owner_id for isolation
            completed_todo = await todo_repo.complete_todo(todo_id, owner_id=str(user_id))

            if completed_todo:
                # Commit the transaction
                await session.commit()
                # #984: Invalidate cached todo lists so floor reflects state.
                from services.intent_service.cache_invalidation import (
                    invalidate_user_todos,
                )

                await invalidate_user_todos(user_id)

            return completed_todo

    async def reopen_todo(self, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
        """Reopen a completed todo.

        Args:
            todo_id: Todo to reopen
            user_id: REQUIRED - User reopening (for authorization and isolation)

        Returns:
            Reopened todo, or None if not found/unauthorized
        """
        async with AsyncSessionFactory.session_scope() as session:
            todo_repo = TodoRepository(session)

            # SEC-MULTITENANCY Phase 4: Reopen with owner_id for isolation
            reopened_todo = await todo_repo.reopen_todo(todo_id, owner_id=str(user_id))

            if reopened_todo:
                # Commit the transaction
                await session.commit()
                # #984: Invalidate cached todo lists.
                from services.intent_service.cache_invalidation import (
                    invalidate_user_todos,
                )

                await invalidate_user_todos(user_id)

            return reopened_todo

    async def update_todo(self, todo_id: UUID, user_id: UUID, **updates) -> Optional[Todo]:
        """Update todo fields.

        Args:
            todo_id: Todo to update
            user_id: REQUIRED - User updating (for authorization and isolation)
            **updates: Fields to update

        Returns:
            Updated todo, or None if not found/unauthorized

        Examples:
            >>> updated = await service.update_todo(
            ...     todo_id,
            ...     user_id="user-123",
            ...     priority="urgent",
            ...     due_date=tomorrow
            ... )
        """
        async with AsyncSessionFactory.session_scope() as session:
            todo_repo = TodoRepository(session)

            # Prepare updates dict (repository expects dict, not object)
            update_dict = {}
            for key, value in updates.items():
                update_dict[key] = value

            # SEC-MULTITENANCY Phase 4: Update with owner_id for isolation
            updated_todo = await todo_repo.update_todo(
                str(todo_id), update_dict, owner_id=str(user_id)
            )

            if updated_todo:
                # Commit the transaction
                await session.commit()
                # #984: Invalidate cached todo lists.
                from services.intent_service.cache_invalidation import (
                    invalidate_user_todos,
                )

                await invalidate_user_todos(user_id)

            return updated_todo

    async def delete_todo(self, todo_id: UUID, user_id: UUID) -> bool:
        """Delete a todo.

        Args:
            todo_id: Todo to delete
            user_id: REQUIRED - User deleting (for authorization and isolation)

        Returns:
            True if deleted, False if not found/unauthorized

        Examples:
            >>> deleted = await service.delete_todo(todo_id, user_id)
            >>> assert deleted is True
        """
        async with AsyncSessionFactory.session_scope() as session:
            todo_repo = TodoRepository(session)

            # SEC-MULTITENANCY Phase 4: Delete with owner_id for isolation
            deleted = await todo_repo.delete_todo(todo_id, owner_id=str(user_id))

            if deleted:
                # Commit the transaction
                await session.commit()
                # #984: Invalidate cached todo lists.
                from services.intent_service.cache_invalidation import (
                    invalidate_user_todos,
                )

                await invalidate_user_todos(user_id)

            return deleted
