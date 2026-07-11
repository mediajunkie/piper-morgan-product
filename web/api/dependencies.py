"""
Dependency injection providers for FastAPI routes.

Provides reusable dependency injection functions for repositories and services
used across multiple endpoints. Following FastAPI best practices with Depends().

Issue #469: Fixed to use AsyncSessionFactory instead of non-existent request.state.db.
The original implementation expected middleware to set request.state.db, but that
middleware was never created. Now uses async generators with session_scope_fresh()
for proper session lifecycle management.

Issue #322: Added get_container() for ServiceContainer dependency injection.
This is part of the ARCH-FIX-SINGLETON work to remove the singleton pattern
and enable horizontal scaling with multiple uvicorn workers.
"""

from typing import TYPE_CHECKING, AsyncGenerator

from fastapi import HTTPException, Request

if TYPE_CHECKING:
    from services.container import ServiceContainer

from services.database.repositories import (
    ConversationRepository,
    ProjectIntegrationRepository,
    ProjectRepository,
    RepositoryRepository,
    WorkItemRepository,
)
from services.database.session_factory import AsyncSessionFactory
from services.feedback.feedback_service import FeedbackService
from services.knowledge.knowledge_graph_service import KnowledgeGraphService
from services.repositories.file_repository import FileRepository
from services.repositories.todo_repository import TodoRepository
from services.repositories.universal_list_repository import (
    UniversalListItemRepository,
    UniversalListRepository,
)

# =============================================================================
# ServiceContainer Dependency (Issue #322: ARCH-FIX-SINGLETON)
# =============================================================================


def get_container(request: Request) -> "ServiceContainer":
    """Get ServiceContainer from application state.

    This is the standard dependency injection path for accessing the
    ServiceContainer in FastAPI routes. The container is created during
    application startup (web/startup.py) and stored in app.state.

    Usage in routes:
        from fastapi import Depends
        from web.api.dependencies import get_container

        @router.get("/example")
        async def example_route(
            container: ServiceContainer = Depends(get_container)
        ):
            service = container.get_service("my_service")
            ...

    Args:
        request: FastAPI Request object (injected automatically)

    Returns:
        ServiceContainer: The application's service container

    Raises:
        HTTPException: 503 if container not initialized (startup incomplete)

    Issue #322: Part of ARCH-FIX-SINGLETON to enable horizontal scaling.
    The container is application-scoped (one per uvicorn worker), not a
    process-wide singleton, allowing multiple workers to run independently.
    """
    if not hasattr(request.app.state, "service_container"):
        raise HTTPException(
            status_code=503,
            detail="ServiceContainer not initialized. Application startup may be incomplete.",
        )

    container = request.app.state.service_container

    if container is None:
        raise HTTPException(
            status_code=503,
            detail="ServiceContainer is None. Application startup may have failed.",
        )

    return container


# =============================================================================
# Repository Dependencies (Issue #469, #470)
# =============================================================================


async def get_file_repository() -> AsyncGenerator[FileRepository, None]:
    """Dependency injection for FileRepository.

    Provides FileRepository with database session for file operations.
    Uses AsyncSessionFactory.session_scope_fresh() for event loop safety.

    Issue #469: Fixed to use session factory instead of request.state.db.
    Issue #470: Added commit after yield to persist changes.
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        yield FileRepository(session)
        # Commit changes after successful route execution
        await session.commit()


async def get_list_repository() -> AsyncGenerator[UniversalListRepository, None]:
    """Dependency injection for UniversalListRepository.

    Provides UniversalListRepository with database session for list operations.
    Uses AsyncSessionFactory.session_scope_fresh() for event loop safety.

    Issue #469: Fixed to use session factory instead of request.state.db.
    Issue #470: Added commit after yield to persist changes.
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        yield UniversalListRepository(session)
        # Commit changes after successful route execution
        await session.commit()


async def get_todo_repository() -> AsyncGenerator[TodoRepository, None]:
    """Dependency injection for TodoRepository.

    Provides TodoRepository with database session for todo CRUD operations.
    Uses AsyncSessionFactory.session_scope_fresh() for event loop safety.

    Issue #469: Fixed to use session factory instead of request.state.db.
    Issue #470: Added commit after yield to persist changes.
    Issue #479: Fixed to return TodoRepository (for Todos), not TodoListRepository (for TodoLists).
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        yield TodoRepository(session)
        # Commit changes after successful route execution
        await session.commit()


async def get_knowledge_graph_service() -> AsyncGenerator[KnowledgeGraphService, None]:
    """Dependency injection for KnowledgeGraphService.

    Provides KnowledgeGraphService with database session for knowledge graph operations.
    Uses AsyncSessionFactory.session_scope_fresh() for event loop safety.

    Issue #469: Fixed to use session factory instead of request.state.db.
    Issue #470: Added commit after yield to persist changes.
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        yield KnowledgeGraphService(session)
        # Commit changes after successful route execution
        await session.commit()


async def get_project_repository() -> AsyncGenerator[ProjectRepository, None]:
    """Dependency injection for ProjectRepository.

    Provides ProjectRepository with database session for project operations.
    Uses AsyncSessionFactory.session_scope_fresh() for event loop safety.

    Issue #469: Fixed to use session factory instead of request.state.db.
    Issue #470: Added commit after yield to persist changes.
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        yield ProjectRepository(session)
        # Commit changes after successful route execution
        await session.commit()


async def get_project_integration_repository() -> (
    AsyncGenerator[ProjectIntegrationRepository, None]
):
    """Dependency injection for ProjectIntegrationRepository.

    Issue #859: Project integration CRUD endpoints.
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        yield ProjectIntegrationRepository(session)
        await session.commit()


async def get_repository_repository() -> AsyncGenerator[RepositoryRepository, None]:
    """Dependency injection for RepositoryRepository.

    Issue #866: Repository as first-class domain entity.
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        yield RepositoryRepository(session)
        await session.commit()


async def get_conversation_repository() -> AsyncGenerator[ConversationRepository, None]:
    """Dependency injection for ConversationRepository.

    Provides ConversationRepository with database session for conversation operations.
    Uses AsyncSessionFactory.session_scope_fresh() for event loop safety.

    Issue #563: Added for "Continue where you left off" feature.
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        yield ConversationRepository(session)
        # Commit changes after successful route execution
        await session.commit()


async def get_user_history_service() -> "AsyncGenerator":
    """Dependency injection for UserHistoryService.

    Provides UserHistoryService backed by DBUserHistoryRepository so chat
    surfaces and API consumers reach the same Postgres-backed Layer 3
    store. Issue #1021 Phase 2.7 — wires the user-reachable surface.
    """
    from services.database.repositories import DBUserHistoryRepository
    from services.memory.user_history import UserHistoryService

    async with AsyncSessionFactory.session_scope_fresh() as session:
        repo = DBUserHistoryRepository(session)
        yield UserHistoryService(repo)
        await session.commit()


async def get_feedback_service() -> AsyncGenerator[FeedbackService, None]:
    """Dependency injection for FeedbackService.

    Provides FeedbackService with database session for feedback operations.
    Uses AsyncSessionFactory.session_scope_fresh() for event loop safety.

    Issue #469: Fixed to use session factory instead of request.state.db.
    Issue #470: Added commit after yield to persist changes.
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        yield FeedbackService(session)
        # Commit changes after successful route execution
        await session.commit()


async def get_list_item_repository() -> AsyncGenerator[UniversalListItemRepository, None]:
    """Dependency injection for UniversalListItemRepository.

    Provides UniversalListItemRepository with database session for list item operations.
    Uses AsyncSessionFactory.session_scope_fresh() for event loop safety.

    Issue #474: Added for list item management (add/edit/delete items).
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        yield UniversalListItemRepository(session)
        # Commit changes after successful route execution
        await session.commit()


async def get_work_item_repository() -> AsyncGenerator[WorkItemRepository, None]:
    """Dependency injection for WorkItemRepository.

    Provides WorkItemRepository with database session for work item operations.
    Uses AsyncSessionFactory.session_scope_fresh() for event loop safety.

    Issue #710: Added for Work Items view with lifecycle indicators.
    """
    async with AsyncSessionFactory.session_scope_fresh() as session:
        yield WorkItemRepository(session)
        # Commit changes after successful route execution
        await session.commit()
