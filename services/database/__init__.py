"""
Database Service
Handles data persistence and retrieval

#1797 (2026-09-22): the five dead persistence twins (Product/Feature/Intent/
Stakeholder/Task DB classes) and their dead repository subgraph
(Product/Feature/TaskRepository, RepositoryFactory) are DELETED — zero live
consumers (census in the issue + the deleting commit). Their tables (all empty,
create_all residue, never migration-managed) are dropped by m1797drop.
"""

from .connection import Base, db
from .models import (
    ProjectDB,
    ProjectIntegrationDB,
    ProjectRepositoryLinkDB,
    RepositoryDB,
    Workflow,
    WorkItem,
)
from .repositories import (
    ProjectIntegrationRepository,
    ProjectRepository,
    RepositoryRepository,
    WorkflowRepository,
    WorkItemRepository,
)

__all__ = [
    # Connection
    "db",
    "Base",
    # Models
    "WorkItem",
    "Workflow",
    "ProjectDB",
    "ProjectIntegrationDB",
    "RepositoryDB",
    "ProjectRepositoryLinkDB",
    # Repositories
    "WorkItemRepository",
    "WorkflowRepository",
    "ProjectRepository",
    "ProjectIntegrationRepository",
    "RepositoryRepository",
]
