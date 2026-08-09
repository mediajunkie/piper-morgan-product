"""
Project Query Service - CQRS-lite pattern for read-only project operations
"""

from typing import List, Optional

import structlog

from services.database.repositories import ProjectRepository
from services.domain.models import Project

logger = structlog.get_logger()


class ProjectQueryService:
    """Query service for read-only project operations.

    #1501: every project read here is owner-scoped and fail-closed, mirroring
    #1421's get_default_project. The old zero-principal forms passed no owner
    to the repository, so its optional owner filter never engaged — one
    tenant's name lookup matched another tenant's project, and list/count
    returned global data (cross-tenant read, live in beta). No principal now
    means empty ([]/None/0), never global; callers with no principal in scope
    must handle the empty result honestly, not invent one. Admin surfaces that
    legitimately need unscoped reads use ProjectRepository's is_admin bypass
    directly (SEC-RBAC Phase 3), not this service.
    """

    def __init__(self, project_repository: ProjectRepository):
        self.repo = project_repository

    async def list_active_projects(self, owner_id: Optional[str]) -> List[Project]:
        """List the OWNER's active projects (#1501: owner-scoped, fail-closed)."""
        if not owner_id:
            logger.warning("list_active_projects called without owner_id — fail-closed []")
            return []
        return await self.repo.list_active_projects(owner_id=owner_id)

    async def get_project_by_id(self, project_id: str) -> Optional[Project]:
        """Get a specific project by ID"""
        return await self.repo.get_by_id(project_id)

    async def get_default_project(self, owner_id: Optional[str]) -> Optional[Project]:
        """Get the acting user's default project (#1421: owner-scoped, fail-closed)."""
        return await self.repo.get_default_project(owner_id)

    async def find_project_by_name(self, name: str, owner_id: Optional[str]) -> Optional[Project]:
        """Find the OWNER's project by name (#1501: owner-scoped, fail-closed)."""
        if not owner_id:
            logger.warning("find_project_by_name called without owner_id — fail-closed None")
            return None
        return await self.repo.find_by_name(name, owner_id=owner_id)

    async def count_active_projects(self, owner_id: Optional[str]) -> int:
        """Count the OWNER's active projects (#1501: owner-scoped, fail-closed)."""
        if not owner_id:
            logger.warning("count_active_projects called without owner_id — fail-closed 0")
            return 0
        return await self.repo.count_active_projects(owner_id=owner_id)

    async def get_project_details(self, project_id: str) -> Optional[dict]:
        """Get detailed project information including integrations"""
        project = await self.repo.get_by_id(project_id)
        if not project:
            return None

        # Return detailed project information
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "is_default": project.is_default,
            "is_archived": project.is_archived,
            "created_at": project.created_at.isoformat(),
            "updated_at": project.updated_at.isoformat(),
            "integrations": [
                {
                    "id": integration.id,
                    "type": integration.type.value,
                    "name": integration.name,
                    "config": integration.config,
                    "is_active": integration.is_active,
                    "created_at": integration.created_at.isoformat(),
                }
                for integration in project.integrations
            ],
            "total_integrations": len(project.integrations),
            "active_integrations": len([i for i in project.integrations if i.is_active]),
        }
