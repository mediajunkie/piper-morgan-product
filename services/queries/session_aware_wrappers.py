"""
Session-aware wrappers for query services that handle database session management.
These wrappers allow QueryRouter to work without requiring pre-initialized repositories.
"""

from typing import Any, List, Optional

from services.database.repositories import ProjectRepository
from services.database.session_factory import AsyncSessionFactory
from services.domain.models import Project
from services.queries.file_queries import FileQueryService
from services.queries.project_queries import ProjectQueryService
from services.repositories.file_repository import FileRepository


class SessionAwareProjectQueryService:
    """Wrapper for ProjectQueryService that handles session management internally."""

    async def list_active_projects(self) -> List[Project]:
        """List all active projects with automatic session management."""
        async with AsyncSessionFactory.session_scope() as session:
            repo = ProjectRepository(session)
            service = ProjectQueryService(repo)
            return await service.list_active_projects()

    async def get_project_by_id(self, project_id: str) -> Optional[Project]:
        """Get a specific project by ID with automatic session management."""
        async with AsyncSessionFactory.session_scope() as session:
            repo = ProjectRepository(session)
            service = ProjectQueryService(repo)
            return await service.get_project_by_id(project_id)

    async def get_default_project(self, owner_id: Optional[str]) -> Optional[Project]:
        """Get the acting user's default project (#1421: owner-scoped, fail-closed)."""
        async with AsyncSessionFactory.session_scope() as session:
            repo = ProjectRepository(session)
            service = ProjectQueryService(repo)
            return await service.get_default_project(owner_id)

    async def find_project_by_name(self, name: str) -> Optional[Project]:
        """Find a project by name with automatic session management."""
        async with AsyncSessionFactory.session_scope() as session:
            repo = ProjectRepository(session)
            service = ProjectQueryService(repo)
            return await service.find_project_by_name(name)

    async def count_active_projects(self) -> int:
        """Count active projects with automatic session management."""
        async with AsyncSessionFactory.session_scope() as session:
            repo = ProjectRepository(session)
            service = ProjectQueryService(repo)
            return await service.count_active_projects()

    async def get_project_details(self, project_id: str) -> Optional[dict]:
        """Get detailed project information with automatic session management."""
        async with AsyncSessionFactory.session_scope() as session:
            repo = ProjectRepository(session)
            service = ProjectQueryService(repo)
            return await service.get_project_details(project_id)


class SessionAwareFileQueryService:
    """Wrapper for FileQueryService that handles session management internally."""

    async def get_file_metadata(self, file_id: str) -> Optional[Any]:
        """Get file metadata with automatic session management."""
        async with AsyncSessionFactory.session_scope() as session:
            repo = FileRepository(session)
            service = FileQueryService(repo)
            return await service.get_file_metadata(file_id)

    async def list_recent_files(self, limit: int = 10) -> List[Any]:
        """List recent files with automatic session management."""
        async with AsyncSessionFactory.session_scope() as session:
            repo = FileRepository(session)
            service = FileQueryService(repo)
            return await service.list_recent_files(limit)

    async def search_files(self, query: str) -> List[Any]:
        """Search files with automatic session management."""
        async with AsyncSessionFactory.session_scope() as session:
            repo = FileRepository(session)
            service = FileQueryService(repo)
            return await service.search_files(query)
