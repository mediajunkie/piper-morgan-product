"""
Project Query Service - CQRS-lite pattern for read-only project operations
"""

from typing import List, Optional

from services.database.repositories import ProjectRepository
from services.domain.models import Project


class ProjectQueryService:
    """Query service for read-only project operations"""

    def __init__(self, project_repository: ProjectRepository):
        self.repo = project_repository

    async def list_active_projects(self) -> List[Project]:
        """List all active projects"""
        return await self.repo.list_active_projects()

    async def get_project_by_id(self, project_id: str) -> Optional[Project]:
        """Get a specific project by ID"""
        return await self.repo.get_by_id(project_id)

    async def get_default_project(self, owner_id: Optional[str]) -> Optional[Project]:
        """Get the acting user's default project (#1421: owner-scoped, fail-closed)."""
        return await self.repo.get_default_project(owner_id)

    async def find_project_by_name(self, name: str) -> Optional[Project]:
        """Find a project by name"""
        return await self.repo.find_by_name(name)

    async def count_active_projects(self) -> int:
        """Count active projects"""
        return await self.repo.count_active_projects()

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
