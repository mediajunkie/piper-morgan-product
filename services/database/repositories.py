"""
Database Repositories
Handles CRUD operations for domain entities
"""

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import structlog
from sqlalchemy import String, and_, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import services.domain.models as domain
from services.shared_types import ConversationLifecycleState, EdgeType, IntegrationType, NodeType

from .connection import db
from .models import (
    EthicsAuditLogDB,
    Feature,
    InsightDB,
    Intent,
    KnowledgeEdgeDB,
    KnowledgeNodeDB,
    Product,
    ProjectDB,
    ProjectIntegrationDB,
    ProjectRepositoryLinkDB,
    RepositoryDB,
    Task,
    Workflow,
    WorkItem,
)
from .session_factory import AsyncSessionFactory

logger = structlog.get_logger()


# #1089 Phase 0 increment 4: repository-layer safety-net flag-word list.
# Architect Q3 disposition 2026-05-17 — "trivially-detectable flag word"
# for the defense-in-depth check in `KnowledgeGraphRepository.create_node`.
# Deliberately narrow (low false-positive rate on legitimate PUBLIC-level
# writes). Service layer's full `BoundaryEnforcer` is the primary gate;
# this list catches BYPASSES where a future service writes directly to
# the repo without going through `KnowledgeGraphService.create_node`.
# Expansion requires explicit policy review (each addition can affect
# legitimate writes touching the new pattern).
_REPO_SAFETY_NET_PATTERNS: tuple[str, ...] = ("harass", "bully")


# Issue #1021: heuristic topic extraction for the UserHistoryRepository
# Layer 3 surface. Per PM disposition Q2=b: deterministic, no LLM cost,
# upgradable later. Aggregates intents + named entities across turns and
# dedupes while preserving first-mention order.
_GENERIC_INTENTS = {
    "general_query",
    "general",
    "small_talk",
    "greeting",
    "thanks",
    "unknown",
    "chitchat",
}


def _extract_topics_heuristic(turns: List[Any], max_topics: int = 5) -> List[str]:
    """Build a list of up to `max_topics` topic strings from turn rows.

    Accepts either ConversationTurnDB rows or domain.ConversationTurn
    objects — both expose `intent` and `entities` attributes with
    compatible shapes. Entities are expected to be a list of strings
    (per domain.ConversationTurn) but tolerates dict-shaped JSONB rows
    by reading `name`/`value`/`text` keys.
    """
    topics: List[str] = []
    seen: set = set()

    def _add(candidate: Optional[str]) -> bool:
        if not candidate:
            return False
        cleaned = candidate.replace("_", " ").strip().lower()
        if not cleaned or cleaned in seen:
            return False
        seen.add(cleaned)
        topics.append(cleaned)
        return len(topics) >= max_topics

    for t in turns:
        intent = getattr(t, "intent", None)
        if intent and intent.lower() not in _GENERIC_INTENTS:
            if _add(intent):
                return topics

        entities = getattr(t, "entities", None) or []
        for ent in entities:
            if isinstance(ent, str):
                if _add(ent):
                    return topics
            elif isinstance(ent, dict):
                value = ent.get("name") or ent.get("value") or ent.get("text")
                if isinstance(value, str) and _add(value):
                    return topics
    return topics


def _build_preview(user_message: Optional[str], max_len: int = 280) -> str:
    """Truncate the first user message to a single-line preview."""
    if not user_message:
        return ""
    text = user_message.strip().replace("\n", " ").replace("\r", " ")
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


class BaseRepository:
    """Base repository with common CRUD operations"""

    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> Any:
        """Create a new entity"""
        if "id" not in kwargs:
            kwargs["id"] = str(uuid.uuid4())

        entity = self.model(**kwargs)
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def get_by_id(self, id: str) -> Optional[Any]:
        """Get entity by ID"""
        result = await self.session.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    # Keep legacy get method for backwards compatibility
    async def get(self, id: str) -> Optional[Any]:
        """Get entity by ID (legacy method)"""
        return await self.get_by_id(id)

    async def list(self, limit: int = 100) -> List[Any]:
        """List all entities"""
        result = await self.session.execute(select(self.model).limit(limit))
        return result.scalars().all()

    async def update(self, id: str, **kwargs) -> Optional[Any]:
        """Update an entity"""
        entity = await self.get_by_id(id)
        if not entity:
            return None

        for key, value in kwargs.items():
            setattr(entity, key, value)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def delete(self, id: str) -> bool:
        """Delete an entity"""
        entity = await self.get_by_id(id)
        if not entity:
            return False

        self.session.delete(entity)
        await self.session.flush()
        return True


class ProductRepository(BaseRepository):
    model = Product


class FeatureRepository(BaseRepository):
    model = Feature


class WorkItemRepository(BaseRepository):
    model = WorkItem

    async def create_from_workflow(self, workflow_data: Dict[str, Any]) -> WorkItem:
        """Create work item from workflow context"""
        return await self.create(
            title=workflow_data.get("title", "Untitled"),
            description=workflow_data.get("requirements", ""),
            status="open",
            external_refs={},
        )


class WorkflowRepository(BaseRepository):
    model = Workflow

    async def create_from_domain(self, domain_workflow) -> Workflow:
        """Create DB workflow from domain workflow"""
        workflow = Workflow(
            id=domain_workflow.id,
            type=domain_workflow.type,
            status=domain_workflow.status,
            input_data={},  # Domain model has context instead
            output_data=(domain_workflow.result.__dict__ if domain_workflow.result else None),
            context=domain_workflow.context,
            created_at=domain_workflow.created_at,
        )
        self.session.add(workflow)
        await self.session.flush()
        await self.session.refresh(workflow)
        return workflow

    async def update_status(self, workflow_id: str, status, output_data=None, error=None):
        """Update workflow status"""
        updates = {"status": status}
        if output_data:
            updates["output_data"] = output_data
        if error:
            updates["error"] = error
        if status.value == "completed":
            updates["completed_at"] = datetime.now(timezone.utc)
        elif status.value == "running":
            updates["started_at"] = datetime.now(timezone.utc)

        return await self.update(workflow_id, **updates)

    async def find_by_id(self, workflow_id: str) -> Optional[domain.Workflow]:
        """Find workflow by ID and return domain model (for API compatibility)"""
        # Use selectinload to eagerly load the intent relationship
        result = await self.session.execute(
            select(Workflow)
            .options(selectinload(Workflow.intent))
            .where(Workflow.id == workflow_id)
        )
        db_workflow = result.scalar_one_or_none()
        return db_workflow.to_domain() if db_workflow else None


class TaskRepository(BaseRepository):
    model = Task

    async def create_from_domain(self, workflow_id: str, domain_task) -> Task:
        """Create DB task from domain task"""
        return await self.create(
            id=domain_task.id,
            workflow_id=workflow_id,
            type=domain_task.type,
            status=domain_task.status,
            input_data={},  # Domain task has no input_data
        )


# PM-009: Project Repository for multi-project support
class ProjectRepository(BaseRepository):
    """Repository for Project operations"""

    model = ProjectDB

    async def get_by_id(
        self,
        project_id: str,
        owner_id: Optional[str] = None,
        is_admin: bool = False,
    ) -> Optional[domain.Project]:
        """Get project by ID with integrations - optionally verify ownership (admin bypass in SEC-RBAC Phase 3)"""
        filters = [ProjectDB.id == project_id]
        if owner_id and not is_admin:  # Only check ownership if not admin
            filters.append(ProjectDB.owner_id == owner_id)

        result = await self.session.execute(
            select(ProjectDB)
            .options(
                selectinload(ProjectDB.integrations),
                selectinload(ProjectDB.repository_links).selectinload(
                    ProjectRepositoryLinkDB.repository
                ),
            )
            .where(and_(*filters))
        )
        db_project = result.scalar_one_or_none()
        if db_project:
            return db_project.to_domain()
        return None

    async def get_default_project(self, owner_id: Optional[str]) -> Optional[domain.Project]:
        """Return the OWNER's default project, or None.

        #1421: owner_id is a required argument (fail-closed). The old zero-arg
        form selected the single process-global is_default row — one user's
        default became every user's project context (cross-tenant read). No
        principal -> no default, never another tenant's; callers with no
        principal must handle None honestly.
        """
        if not owner_id:
            logger.warning("get_default_project called without owner_id — fail-closed None")
            return None
        result = await self.session.execute(
            select(ProjectDB)
            .options(
                selectinload(ProjectDB.integrations),
                selectinload(ProjectDB.repository_links).selectinload(
                    ProjectRepositoryLinkDB.repository
                ),
            )
            .where(
                ProjectDB.owner_id == owner_id,
                ProjectDB.is_default == True,
                ProjectDB.is_archived == False,
            )
            .order_by(ProjectDB.created_at)
        )
        db_project = result.scalars().first()
        return db_project.to_domain() if db_project else None

    async def list_active_projects(
        self,
        owner_id: Optional[str] = None,
        is_admin: bool = False,
    ) -> List[domain.Project]:
        """List active projects - optionally filter by owner (admin bypass in SEC-RBAC Phase 3)"""
        filters = [ProjectDB.is_archived == False]
        if owner_id and not is_admin:  # Only check ownership if not admin
            filters.append(ProjectDB.owner_id == owner_id)

        result = await self.session.execute(
            select(ProjectDB)
            .options(
                selectinload(ProjectDB.integrations),
                selectinload(ProjectDB.repository_links).selectinload(
                    ProjectRepositoryLinkDB.repository
                ),
            )
            .where(and_(*filters))
            .order_by(ProjectDB.name)
        )
        return [db_project.to_domain() for db_project in result.scalars().all()]

    async def count_active_projects(
        self,
        owner_id: Optional[str] = None,
        is_admin: bool = False,
    ) -> int:
        """Count active projects - optionally filter by owner (admin bypass in SEC-RBAC Phase 3)"""
        filters = [ProjectDB.is_archived == False]
        if owner_id and not is_admin:  # Only check ownership if not admin
            filters.append(ProjectDB.owner_id == owner_id)

        result = await self.session.execute(select(func.count(ProjectDB.id)).where(and_(*filters)))
        return result.scalar() or 0

    async def find_by_name(
        self,
        name: str,
        owner_id: Optional[str] = None,
        is_admin: bool = False,
    ) -> Optional[domain.Project]:
        """Find project by name - optionally filter by owner (admin bypass in SEC-RBAC Phase 3)"""
        filters = [
            func.lower(ProjectDB.name) == name.lower(),
            ProjectDB.is_archived == False,
        ]
        if owner_id and not is_admin:  # Only check ownership if not admin
            filters.append(ProjectDB.owner_id == owner_id)

        result = await self.session.execute(
            select(ProjectDB)
            .options(
                selectinload(ProjectDB.integrations),
                selectinload(ProjectDB.repository_links).selectinload(
                    ProjectRepositoryLinkDB.repository
                ),
            )
            .where(and_(*filters))
        )
        db_project = result.scalar_one_or_none()
        return db_project.to_domain() if db_project else None

    async def search_projects(
        self,
        query: str,
        owner_id: Optional[str] = None,
        include_archived: bool = False,
        limit: int = 20,
    ) -> List[domain.Project]:
        """
        Search projects by name (partial match, case-insensitive).

        Part of #567 MUX-INTERACT-CONV-SEARCH.

        Args:
            query: Search query (matches against project name)
            owner_id: Filter to this user's projects
            include_archived: Whether to include archived projects
            limit: Maximum results to return

        Returns:
            List of matching projects, ordered by name
        """
        filters = [
            ProjectDB.name.ilike(f"%{query}%"),
        ]

        if not include_archived:
            filters.append(ProjectDB.is_archived == False)

        if owner_id:
            filters.append(ProjectDB.owner_id == owner_id)

        result = await self.session.execute(
            select(ProjectDB)
            .options(
                selectinload(ProjectDB.integrations),
                selectinload(ProjectDB.repository_links).selectinload(
                    ProjectRepositoryLinkDB.repository
                ),
            )
            .where(and_(*filters))
            .order_by(ProjectDB.name)
            .limit(limit)
        )
        db_projects = result.scalars().all()
        return [db_project.to_domain() for db_project in db_projects]

    async def create_default_project(self) -> domain.Project:
        logger.info("Creating default project")
        project = domain.Project(
            id=str(uuid.uuid4()),
            name="Piper Morgan Test",
            description="Default project for Piper Morgan development and testing",
            is_default=True,
            is_archived=False,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db_project = ProjectDB.from_domain(project)
        self.session.add(db_project)
        await self.session.commit()
        await self.session.refresh(db_project)
        return db_project.to_domain()

    async def get_project_with_integrations(
        self,
        project_id: str,
        owner_id: Optional[str] = None,
        is_admin: bool = False,
    ) -> Optional[domain.Project]:
        """Get project with integrations - optionally verify ownership (admin bypass in SEC-RBAC Phase 3)"""
        filters = [ProjectDB.id == project_id, ProjectDB.is_archived == False]
        if owner_id and not is_admin:  # Only check ownership if not admin
            filters.append(ProjectDB.owner_id == owner_id)

        result = await self.session.execute(
            select(ProjectDB)
            .where(and_(*filters))
            .options(
                selectinload(ProjectDB.integrations),
                selectinload(ProjectDB.repository_links).selectinload(
                    ProjectRepositoryLinkDB.repository
                ),
            )
        )
        db_project = result.scalar_one_or_none()
        return db_project.to_domain() if db_project else None

    async def share_project(
        self,
        project_id: str,
        owner_id: str,
        user_to_share_with: str,
        role: domain.ShareRole = None,
    ) -> Optional[domain.Project]:
        """Share a project with another user at specified role (SEC-RBAC Phase 3)

        Args:
            project_id: ID of project to share
            owner_id: User making the share request (must be owner)
            user_to_share_with: User to share with
            role: ShareRole (viewer, editor, admin) - defaults to viewer if None

        Returns:
            Updated Project with new shared_with entry, or None if not found/not owner
        """
        # Default role if not specified
        if role is None:
            role = domain.ShareRole.VIEWER

        # Verify the caller is the owner
        result = await self.session.execute(
            select(ProjectDB)
            .options(
                selectinload(ProjectDB.integrations),
                selectinload(ProjectDB.repository_links).selectinload(
                    ProjectRepositoryLinkDB.repository
                ),
            )
            .where(and_(ProjectDB.id == project_id, ProjectDB.owner_id == owner_id))
        )
        db_project = result.scalar_one_or_none()

        if not db_project:
            return None  # Not found or not owner

        # Prevent owner from sharing with themselves (no-op)
        if user_to_share_with == owner_id:
            return db_project.to_domain()

        # Convert to domain object to work with SharePermission objects
        domain_project = db_project.to_domain()

        # Check if user already shared with - update role if exists, otherwise add new share
        permission = domain.SharePermission(user_id=user_to_share_with, role=role)
        existing_index = None

        for idx, perm in enumerate(domain_project.shared_with):
            if perm.user_id == user_to_share_with:
                existing_index = idx
                break

        if existing_index is not None:
            # Update existing permission
            domain_project.shared_with[existing_index] = permission
        else:
            # Add new permission
            domain_project.shared_with.append(permission)

        # Convert back to JSONB format for database storage
        shared_with_jsonb = [perm.to_dict() for perm in domain_project.shared_with]

        # Update database
        await self.session.execute(
            update(ProjectDB)
            .where(ProjectDB.id == project_id)
            .values(shared_with=shared_with_jsonb, updated_at=datetime.now())
        )

        # Refresh and return updated project
        await self.session.refresh(db_project)
        return db_project.to_domain()

    async def unshare_project(self, project_id: str, owner_id: str, user_to_unshare: str) -> bool:
        """Remove user from project sharing (SEC-RBAC Phase 3)

        Args:
            project_id: ID of project
            owner_id: User making the unshare request (must be owner)
            user_to_unshare: User to remove from sharing

        Returns:
            True if user was unshared, False if not found/not owner
        """
        # Verify the caller is the owner
        result = await self.session.execute(
            select(ProjectDB)
            .options(
                selectinload(ProjectDB.integrations),
                selectinload(ProjectDB.repository_links).selectinload(
                    ProjectRepositoryLinkDB.repository
                ),
            )
            .where(and_(ProjectDB.id == project_id, ProjectDB.owner_id == owner_id))
        )
        db_project = result.scalar_one_or_none()

        if not db_project:
            return False  # Not found or not owner

        # Convert to domain object
        domain_project = db_project.to_domain()

        # Remove user from shared_with
        initial_length = len(domain_project.shared_with)
        domain_project.shared_with = [
            perm for perm in domain_project.shared_with if perm.user_id != user_to_unshare
        ]

        # If nothing changed, return False
        if len(domain_project.shared_with) == initial_length:
            return False

        # Convert back to JSONB format
        shared_with_jsonb = [perm.to_dict() for perm in domain_project.shared_with]

        # Update database
        await self.session.execute(
            update(ProjectDB)
            .where(ProjectDB.id == project_id)
            .values(shared_with=shared_with_jsonb, updated_at=datetime.now())
        )

        return True

    async def update_share_role(
        self,
        project_id: str,
        owner_id: str,
        target_user_id: str,
        new_role: domain.ShareRole,
    ) -> bool:
        """Update sharing role for a user (SEC-RBAC Phase 3)

        Args:
            project_id: ID of project
            owner_id: User making the request (must be owner)
            target_user_id: User whose role to update
            new_role: New ShareRole (viewer, editor, admin)

        Returns:
            True if role was updated, False if not found/not owner/user not shared
        """
        # Verify the caller is the owner
        result = await self.session.execute(
            select(ProjectDB)
            .options(
                selectinload(ProjectDB.integrations),
                selectinload(ProjectDB.repository_links).selectinload(
                    ProjectRepositoryLinkDB.repository
                ),
            )
            .where(and_(ProjectDB.id == project_id, ProjectDB.owner_id == owner_id))
        )
        db_project = result.scalar_one_or_none()

        if not db_project:
            return False  # Not found or not owner

        # Convert to domain object
        domain_project = db_project.to_domain()

        # Find and update the user's role
        updated = False
        for perm in domain_project.shared_with:
            if perm.user_id == target_user_id:
                perm.role = new_role
                updated = True
                break

        if not updated:
            return False  # User not in shared_with list

        # Convert back to JSONB format
        shared_with_jsonb = [perm.to_dict() for perm in domain_project.shared_with]

        # Update database
        await self.session.execute(
            update(ProjectDB)
            .where(ProjectDB.id == project_id)
            .values(shared_with=shared_with_jsonb, updated_at=datetime.now())
        )

        return True

    async def get_user_role(self, project_id: str, user_id: str) -> Optional[domain.ShareRole]:
        """Get user's role for a project (owner/viewer/editor/admin) (SEC-RBAC Phase 3)

        Args:
            project_id: ID of project
            user_id: User ID to check

        Returns:
            ShareRole if user has access (owner or in shared_with), None otherwise
        """
        result = await self.session.execute(select(ProjectDB).where(ProjectDB.id == project_id))
        db_project = result.scalar_one_or_none()

        if not db_project:
            return None

        # Check if user is owner
        if db_project.owner_id == user_id:
            return domain.ShareRole.ADMIN  # Owner is treated as admin role

        # Check shared_with
        if db_project.shared_with:
            for perm_dict in db_project.shared_with:
                if perm_dict["user_id"] == user_id:
                    return domain.ShareRole(perm_dict["role"])

        return None  # User has no access


class ProjectIntegrationRepository(BaseRepository):
    """Repository for ProjectIntegration operations"""

    model = ProjectIntegrationDB

    async def get_by_project_and_type(
        self, project_id: str, integration_type: IntegrationType, owner_id: Optional[str] = None
    ) -> Optional[domain.ProjectIntegration]:
        """Get integration by project and type - optionally verify project ownership"""
        filters = [
            ProjectIntegrationDB.project_id == project_id,
            ProjectIntegrationDB.type == integration_type,
            ProjectIntegrationDB.is_active == True,
        ]

        # If owner_id provided, join with projects to verify ownership
        if owner_id:
            from .models import ProjectDB

            result = await self.session.execute(
                select(ProjectIntegrationDB)
                .where(and_(*filters))
                .join(ProjectDB, ProjectIntegrationDB.project_id == ProjectDB.id)
                .where(ProjectDB.owner_id == owner_id)
            )
        else:
            result = await self.session.execute(select(ProjectIntegrationDB).where(and_(*filters)))

        db_integration = result.scalar_one_or_none()
        return db_integration.to_domain() if db_integration else None

    async def list_by_project(
        self, project_id: str, active_only: bool = True, owner_id: Optional[str] = None
    ) -> List[domain.ProjectIntegration]:
        """List integrations by project - optionally verify project ownership"""
        query = select(ProjectIntegrationDB).where(ProjectIntegrationDB.project_id == project_id)
        if active_only:
            query = query.where(ProjectIntegrationDB.is_active == True)

        # If owner_id provided, join with projects to verify ownership
        if owner_id:
            from .models import ProjectDB

            query = query.join(ProjectDB, ProjectIntegrationDB.project_id == ProjectDB.id).where(
                ProjectDB.owner_id == owner_id
            )

        result = await self.session.execute(query.order_by(ProjectIntegrationDB.type))
        return [db_integration.to_domain() for db_integration in result.scalars().all()]


class RepositoryRepository(BaseRepository):
    """Repository for Repository (code repo) operations.

    Issue #866: Repository as first-class domain entity.
    """

    model = RepositoryDB

    async def create_repository(self, repo: domain.Repository) -> domain.Repository:
        """Create a new repository."""
        db_repo = RepositoryDB.from_domain(repo)
        self.session.add(db_repo)
        await self.session.flush()
        await self.session.refresh(db_repo)
        return db_repo.to_domain()

    async def get_by_id(
        self, repo_id: str, owner_id: Optional[str] = None
    ) -> Optional[domain.Repository]:
        """Get repository by ID, optionally verifying ownership."""
        filters = [RepositoryDB.id == repo_id]
        if owner_id:
            filters.append(RepositoryDB.owner_id == owner_id)
        result = await self.session.execute(select(RepositoryDB).where(and_(*filters)))
        db_repo = result.scalar_one_or_none()
        return db_repo.to_domain() if db_repo else None

    async def get_by_full_name(
        self, full_name: str, provider: str = "github", owner_id: Optional[str] = None
    ) -> Optional[domain.Repository]:
        """Get repository by provider + full_name, optionally scoped to owner."""
        filters = [
            RepositoryDB.full_name == full_name,
            RepositoryDB.provider == provider,
        ]
        if owner_id:
            filters.append(RepositoryDB.owner_id == owner_id)
        result = await self.session.execute(select(RepositoryDB).where(and_(*filters)))
        db_repo = result.scalar_one_or_none()
        return db_repo.to_domain() if db_repo else None

    async def list_by_owner(
        self, owner_id: str, provider: Optional[str] = None, active_only: bool = True
    ) -> List[domain.Repository]:
        """List all repositories owned by a user."""
        filters: List = [RepositoryDB.owner_id == owner_id]
        if provider:
            filters.append(RepositoryDB.provider == provider)
        if active_only:
            filters.append(RepositoryDB.is_active == True)
        result = await self.session.execute(
            select(RepositoryDB).where(and_(*filters)).order_by(RepositoryDB.full_name)
        )
        return [db.to_domain() for db in result.scalars().all()]

    async def list_by_project(self, project_id: str) -> List[domain.Repository]:
        """Get all repositories linked to a project."""
        result = await self.session.execute(
            select(RepositoryDB)
            .join(ProjectRepositoryLinkDB, RepositoryDB.id == ProjectRepositoryLinkDB.repository_id)
            .where(ProjectRepositoryLinkDB.project_id == project_id)
            .order_by(RepositoryDB.full_name)
        )
        return [db.to_domain() for db in result.scalars().all()]

    async def link_to_project(
        self,
        repository_id: str,
        project_id: str,
        linked_by: str,
        is_primary: bool = False,
    ) -> domain.ProjectRepositoryLink:
        """Create a project-repository link."""
        link = ProjectRepositoryLinkDB(
            id=str(uuid.uuid4()),
            project_id=project_id,
            repository_id=repository_id,
            is_primary=is_primary,
            linked_by=linked_by,
        )
        self.session.add(link)
        await self.session.flush()
        await self.session.refresh(link)
        return link.to_domain()

    async def unlink_from_project(self, repository_id: str, project_id: str) -> bool:
        """Remove a project-repository link."""
        result = await self.session.execute(
            select(ProjectRepositoryLinkDB).where(
                and_(
                    ProjectRepositoryLinkDB.repository_id == repository_id,
                    ProjectRepositoryLinkDB.project_id == project_id,
                )
            )
        )
        link = result.scalar_one_or_none()
        if link:
            await self.session.delete(link)
            await self.session.flush()
            return True
        return False

    async def get_project_links(self, repository_id: str) -> List[domain.ProjectRepositoryLink]:
        """Get all projects linked to a repository."""
        result = await self.session.execute(
            select(ProjectRepositoryLinkDB)
            .where(ProjectRepositoryLinkDB.repository_id == repository_id)
            .order_by(ProjectRepositoryLinkDB.linked_at)
        )
        return [link.to_domain() for link in result.scalars().all()]


class KnowledgeGraphRepository(BaseRepository):
    """Repository for knowledge graph operations"""

    model = KnowledgeNodeDB  # Default to nodes, but we'll handle both

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    # Node operations
    async def create_node(self, node: domain.KnowledgeNode) -> domain.KnowledgeNode:
        """Create a knowledge node (with #1089 repository safety-net check).

        See `_privacy_safety_check` for the defensive contract — raises
        PrivacyFilterRejectedError if a direct repo write attempts to
        store content with trivially-detectable flag words AND lacks
        the `is_filtered` flag from the service-layer write path.
        """
        self._privacy_safety_check(node)
        db_node = KnowledgeNodeDB.from_domain(node)
        return await self.create(**db_node.__dict__)

    def _privacy_safety_check(self, node: domain.KnowledgeNode) -> None:
        """#1089 Phase 0 increment 4: repository-layer defensive check.

        Architect Q3 disposition 2026-05-17: the service layer
        (`KnowledgeGraphService.create_node`) is the primary gate; this
        repo-layer check is a defense-in-depth safety net. Intended to
        catch FUTURE BYPASSES — a new service writing directly to
        `KnowledgeGraphRepository` without going through the service
        layer's full BoundaryEnforcer check would otherwise be able to
        land flagged content unfiltered.

        Mechanism:
        - If `metadata.is_filtered is True`, the service layer's write
          path already redacted the content (and recorded the filter
          event). Trust that flag and skip — no double-checking.
        - Otherwise, scan `name + description` against the slim
          `_REPO_SAFETY_NET_PATTERNS` list (deliberately narrow per the
          "trivially-detectable" framing). On match: raise +
          structured-log.

        Deliberately narrow: the patterns list is short by design so
        false positives on legitimate PUBLIC-level content stay low.
        Expansion is via amendment to `_REPO_SAFETY_NET_PATTERNS` with
        explicit policy review.

        Raises:
            PrivacyFilterRejectedError: a trivial flag word was found
                in content that wasn't pre-filtered by the service
                layer. `filter_reason` is HARASSMENT_PATTERN_MATCHED
                (the current safety-net patterns are harassment-leaning).
        """
        # Lazy local import to avoid pulling the ethics module into the
        # database-layer import graph at module load.
        from services.ethics.privacy_types import (
            FilterReason,
            PrivacyFilterRejectedError,
        )

        if node.metadata.get("is_filtered") is True:
            return  # service-layer write path already filtered this

        content_lower = f"{node.name} {node.description}".lower()
        for pattern in _REPO_SAFETY_NET_PATTERNS:
            if pattern in content_lower:
                # Structured log for ops observability + audit. Truncate
                # node name to limit log-cardinality risk.
                logger.warning(
                    "repo_privacy_safety_net_fired",
                    pattern=pattern,
                    node_name_truncated=node.name[:50],
                    node_type=node.node_type.value if node.node_type else "unknown",
                )
                raise PrivacyFilterRejectedError(
                    FilterReason.HARASSMENT_PATTERN_MATCHED,
                    message=(
                        "Repository safety net rejected node creation: "
                        f"trivial flag word '{pattern}' in content without "
                        "is_filtered flag (write should go through "
                        "KnowledgeGraphService.create_node so the service-"
                        "layer BoundaryEnforcer can vet content)"
                    ),
                )

    async def get_node_by_id(
        self, node_id: str, owner_id: Optional[str] = None
    ) -> Optional[domain.KnowledgeNode]:
        """Get node by ID - optionally verify ownership"""
        filters = [KnowledgeNodeDB.id == node_id]
        if owner_id:
            filters.append(KnowledgeNodeDB.owner_id == owner_id)

        result = await self.session.execute(select(KnowledgeNodeDB).where(and_(*filters)))
        db_node = result.scalar_one_or_none()
        return db_node.to_domain() if db_node else None

    async def get_nodes_by_session(
        self, session_id: str, limit: int = 100
    ) -> List[domain.KnowledgeNode]:
        """Get nodes for an owner (parameter named session_id for backward compatibility)"""
        result = await self.session.execute(
            select(KnowledgeNodeDB).where(KnowledgeNodeDB.owner_id == session_id).limit(limit)
        )
        db_nodes = result.scalars().all()
        return [db_node.to_domain() for db_node in db_nodes]

    async def get_nodes_by_type(
        self, node_type: NodeType, session_id: Optional[str] = None, limit: int = 100
    ) -> List[domain.KnowledgeNode]:
        """Get nodes by type, optionally filtered by owner (parameter named session_id for backward compatibility)"""
        # Convert enum to string for comparison (ADR-041: String columns, enum at domain boundary)
        node_type_value = node_type.value if isinstance(node_type, NodeType) else node_type
        query = select(KnowledgeNodeDB).where(KnowledgeNodeDB.node_type == node_type_value)
        if session_id:
            query = query.where(KnowledgeNodeDB.owner_id == session_id)
        query = query.limit(limit)

        result = await self.session.execute(query)
        db_nodes = result.scalars().all()
        return [db_node.to_domain() for db_node in db_nodes]

    # Edge operations
    async def create_edge(self, edge: domain.KnowledgeEdge) -> domain.KnowledgeEdge:
        """Create a knowledge edge"""
        db_edge = KnowledgeEdgeDB.from_domain(edge)
        return await self.create(**db_edge.__dict__)

    async def get_edge_by_id(
        self, edge_id: str, owner_id: Optional[str] = None
    ) -> Optional[domain.KnowledgeEdge]:
        """Get edge by ID - optionally verify ownership"""
        filters = [KnowledgeEdgeDB.id == edge_id]
        if owner_id:
            filters.append(KnowledgeEdgeDB.owner_id == owner_id)

        result = await self.session.execute(select(KnowledgeEdgeDB).where(and_(*filters)))
        db_edge = result.scalar_one_or_none()
        return db_edge.to_domain() if db_edge else None

    async def get_edges_by_session(
        self, session_id: str, limit: int = 100
    ) -> List[domain.KnowledgeEdge]:
        """Get edges for an owner (parameter named session_id for backward compatibility)"""
        result = await self.session.execute(
            select(KnowledgeEdgeDB).where(KnowledgeEdgeDB.owner_id == session_id).limit(limit)
        )
        db_edges = result.scalars().all()
        return [db_edge.to_domain() for db_edge in db_edges]

    # Graph-specific operations
    async def find_neighbors(
        self,
        node_id: str,
        edge_type: Optional[EdgeType] = None,
        direction: str = "both",
        owner_id: Optional[str] = None,
    ) -> List[domain.KnowledgeNode]:
        """Find neighboring nodes - optionally verify ownership of root node"""
        # Verify ownership of the root node if owner_id provided
        if owner_id:
            root_node = await self.get_node_by_id(node_id, owner_id)
            if not root_node:
                return []  # Node not found or doesn't belong to owner

        if direction == "outgoing":
            query = select(KnowledgeEdgeDB).where(KnowledgeEdgeDB.source_node_id == node_id)
        elif direction == "incoming":
            query = select(KnowledgeEdgeDB).where(KnowledgeEdgeDB.target_node_id == node_id)
        else:  # both
            query = select(KnowledgeEdgeDB).where(
                or_(
                    KnowledgeEdgeDB.source_node_id == node_id,
                    KnowledgeEdgeDB.target_node_id == node_id,
                )
            )

        if edge_type:
            # Convert enum to string for comparison (ADR-041: String columns, enum at domain boundary)
            edge_type_value = edge_type.value if isinstance(edge_type, EdgeType) else edge_type
            query = query.where(KnowledgeEdgeDB.edge_type == edge_type_value)

        result = await self.session.execute(query)
        edges = result.scalars().all()

        # Get unique neighbor node IDs
        neighbor_ids = set()
        for edge in edges:
            if edge.source_node_id == node_id:
                neighbor_ids.add(edge.target_node_id)
            else:
                neighbor_ids.add(edge.source_node_id)

        # Fetch neighbor nodes
        if neighbor_ids:
            result = await self.session.execute(
                select(KnowledgeNodeDB).where(KnowledgeNodeDB.id.in_(neighbor_ids))
            )
            db_nodes = result.scalars().all()
            return [db_node.to_domain() for db_node in db_nodes]

        return []

    async def get_subgraph(
        self, node_ids: List[str], max_depth: int = 2, owner_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get a subgraph around specified nodes - optionally verify ownership"""
        nodes = {}
        edges = []
        visited_nodes = set()
        nodes_to_visit = set(node_ids)

        # If owner_id provided, verify all starting nodes belong to owner
        if owner_id:
            result = await self.session.execute(
                select(KnowledgeNodeDB.id).where(
                    and_(KnowledgeNodeDB.id.in_(node_ids), KnowledgeNodeDB.owner_id == owner_id)
                )
            )
            valid_node_ids = set(row[0] for row in result.fetchall())
            nodes_to_visit = nodes_to_visit.intersection(valid_node_ids)

            if not nodes_to_visit:
                # No valid starting nodes
                return {"nodes": [], "edges": [], "depth": max_depth}

        for depth in range(max_depth):
            if not nodes_to_visit:
                break

            # Get nodes at current depth
            result = await self.session.execute(
                select(KnowledgeNodeDB).where(KnowledgeNodeDB.id.in_(nodes_to_visit))
            )
            db_nodes = result.scalars().all()

            # Add nodes to result
            for db_node in db_nodes:
                nodes[db_node.id] = db_node.to_domain()
                visited_nodes.add(db_node.id)

            # Find edges connecting to these nodes
            result = await self.session.execute(
                select(KnowledgeEdgeDB).where(
                    or_(
                        KnowledgeEdgeDB.source_node_id.in_(nodes_to_visit),
                        KnowledgeEdgeDB.target_node_id.in_(nodes_to_visit),
                    )
                )
            )
            db_edges = result.scalars().all()

            # Add edges to result and collect next level nodes
            next_level_nodes = set()
            for db_edge in db_edges:
                edges.append(db_edge.to_domain())
                if (
                    db_edge.source_node_id in nodes_to_visit
                    and db_edge.target_node_id not in visited_nodes
                ):
                    next_level_nodes.add(db_edge.target_node_id)
                elif (
                    db_edge.target_node_id in nodes_to_visit
                    and db_edge.source_node_id not in visited_nodes
                ):
                    next_level_nodes.add(db_edge.source_node_id)

            nodes_to_visit = next_level_nodes

        return {"nodes": list(nodes.values()), "edges": edges, "depth": max_depth}

    async def find_paths(
        self, source_id: str, target_id: str, max_paths: int = 5, owner_id: Optional[str] = None
    ) -> List[List[domain.KnowledgeNode]]:
        """Find paths between two nodes - optionally verify ownership"""
        # This is a simplified path finding - in production you'd want a more sophisticated algorithm
        paths = []

        # Get direct connections
        result = await self.session.execute(
            select(KnowledgeEdgeDB).where(
                and_(
                    KnowledgeEdgeDB.source_node_id == source_id,
                    KnowledgeEdgeDB.target_node_id == target_id,
                )
            )
        )
        direct_edges = result.scalars().all()

        if direct_edges:
            # Direct path exists - verify ownership if required
            source_node = await self.get_node_by_id(source_id, owner_id)
            target_node = await self.get_node_by_id(target_id, owner_id)
            if source_node and target_node:
                paths.append([source_node, target_node])

        # For simplicity, we'll limit to direct connections for now
        # A full implementation would use recursive CTEs or graph algorithms
        return paths[:max_paths]

    # Bulk operations
    async def create_nodes_bulk(
        self, nodes: List[domain.KnowledgeNode]
    ) -> List[domain.KnowledgeNode]:
        """Create multiple nodes efficiently"""
        db_nodes = [KnowledgeNodeDB.from_domain(node) for node in nodes]
        self.session.add_all(db_nodes)
        await self.session.flush()

        # Refresh to get generated IDs
        for db_node in db_nodes:
            await self.session.refresh(db_node)

        return [db_node.to_domain() for db_node in db_nodes]

    async def create_edges_bulk(
        self, edges: List[domain.KnowledgeEdge]
    ) -> List[domain.KnowledgeEdge]:
        """Create multiple edges efficiently"""
        db_edges = [KnowledgeEdgeDB.from_domain(edge) for edge in edges]
        self.session.add_all(db_edges)
        await self.session.flush()

        # Refresh to get generated IDs
        for db_edge in db_edges:
            await self.session.refresh(db_edge)

        return [db_edge.to_domain() for db_edge in db_edges]

    # #1010 (May 2026): `*_with_privacy_check` placeholder methods removed.
    # They were no-op pass-throughs with `# Future:` comments claiming privacy
    # filtering that the implementation never provided — Pattern-067 +
    # Pattern-045 in the same file. KG-internal privacy filtering as a real
    # feature is tracked in the #1010 follow-up (designed-feature shape, not
    # aspirational stubs).


# PM-034 Phase 3: Conversation Repository for ConversationManager
# Issue #563: Implemented actual persistence (was stubbed)
class ConversationRepository(BaseRepository):
    """Repository for conversation turn operations"""

    model = None  # Uses ConversationTurnDB directly via from_domain/to_domain

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_conversation_turns(
        self,
        conversation_id: str,
        limit: int = 100,
        is_admin: bool = False,
        most_recent: bool = False,
    ) -> List[domain.ConversationTurn]:
        """Get conversation turns for a conversation ID.

        Args:
            conversation_id: The conversation to fetch turns for
            limit: Maximum number of turns to return (default 100)
            is_admin: SEC-RBAC Phase 3 - admins can access any conversation
            most_recent: When True, return the most-recent ``limit`` turns
                (still ordered chronologically by turn_number). When False
                (default), return the FIRST ``limit`` turns. Issue #1223: the
                recent-context read path needs the newest turns, not the oldest
                — a plain ``ORDER BY turn_number ASC LIMIT n`` returns turns
                1..n, which for a conversation longer than ``limit`` is the
                wrong (oldest) window. The default is preserved so existing
                callers (e.g. the conversations API) are unaffected.

        Returns:
            List of ConversationTurn domain objects, ordered chronologically
            by turn_number (ascending).
        """
        from services.database.models import ConversationTurnDB

        if most_recent:
            # #1223: take the newest `limit` turns by turn_number DESC, then
            # restore chronological order for callers (which slice/iterate
            # ascending). DESC+limit keeps the query bounded.
            stmt = (
                select(ConversationTurnDB)
                .where(ConversationTurnDB.conversation_id == conversation_id)
                .order_by(ConversationTurnDB.turn_number.desc())
                .limit(limit)
            )
            result = await self.session.execute(stmt)
            db_turns = list(reversed(result.scalars().all()))
        else:
            stmt = (
                select(ConversationTurnDB)
                .where(ConversationTurnDB.conversation_id == conversation_id)
                .order_by(ConversationTurnDB.turn_number)
                .limit(limit)
            )
            result = await self.session.execute(stmt)
            db_turns = result.scalars().all()

        return [t.to_domain() for t in db_turns]

    async def save_turn(
        self, turn: domain.ConversationTurn, is_admin: bool = False, user_id: Optional[str] = None
    ) -> None:
        """Save conversation turn to database.

        Args:
            turn: The ConversationTurn domain object to persist
            is_admin: SEC-RBAC Phase 3 - admins can save turns for any conversation
            user_id: Optional user ID to associate with conversation (Issue #563)
        """
        from services.database.models import ConversationDB, ConversationTurnDB

        # Issue #563: Ensure conversation exists before saving turn (FK constraint)
        await self.ensure_conversation_exists(turn.conversation_id, user_id)

        # Check if turn already exists (upsert logic)
        existing = await self.session.get(ConversationTurnDB, turn.id)

        if existing:
            # Update existing turn
            existing.user_message = turn.user_message
            existing.assistant_response = turn.assistant_response
            existing.intent = turn.intent
            existing.entities = turn.entities
            existing.references = turn.references
            existing.context_used = turn.context_used
            existing.turn_metadata = turn.metadata
            existing.processing_time = turn.processing_time
            existing.completed_at = turn.completed_at
            logger.debug(f"ConversationTurn updated: {turn.id}")
        else:
            # Create new turn
            db_turn = ConversationTurnDB.from_domain(turn)
            self.session.add(db_turn)
            logger.debug(f"ConversationTurn created: {turn.id}")

            # Issue #598: Auto-title conversation on first turn
            if turn.turn_number == 1 and turn.user_message:
                db_conv = await self.session.get(ConversationDB, turn.conversation_id)
                if db_conv and db_conv.title == "New conversation":
                    new_title = self.generate_title_from_message(turn.user_message)
                    db_conv.title = new_title
                    logger.debug(
                        f"Auto-titled conversation: {turn.conversation_id} -> {new_title[:30]}..."
                    )

        # Issue #726: Update last_activity_at so sidebar ordering works correctly
        db_conv = await self.session.get(ConversationDB, turn.conversation_id)
        if db_conv:
            from datetime import datetime

            db_conv.last_activity_at = datetime.now(timezone.utc)
            logger.debug(f"Updated last_activity_at for conversation: {turn.conversation_id}")

            # Issue #1021 Q3=c: preview set on first turn (refresh on archive).
            if turn.turn_number == 1 and turn.user_message and not db_conv.preview:
                db_conv.preview = _build_preview(turn.user_message)

            # Issue #1021 Q2=b: incremental topic accumulation at turn-save.
            # Merge new candidates from this turn into existing topics (max 5).
            existing_topics = list(db_conv.topics or [])
            new_topics = _extract_topics_heuristic([turn])
            merged: List[str] = []
            seen: set = set()
            for t in existing_topics + new_topics:
                key = t.lower().strip()
                if key and key not in seen:
                    seen.add(key)
                    merged.append(t)
                    if len(merged) >= 5:
                        break
            if merged != existing_topics:
                db_conv.topics = merged

            # Issue #1021: maintain denormalized turn_count for UserHistoryRepository.
            # Increment on new-turn path; idempotent recount on update path.
            if existing:
                count_stmt = select(func.count(ConversationTurnDB.id)).where(
                    ConversationTurnDB.conversation_id == turn.conversation_id
                )
                db_conv.turn_count = (await self.session.execute(count_stmt)).scalar() or 0
            else:
                db_conv.turn_count = (db_conv.turn_count or 0) + 1

        await self.session.commit()
        logger.info(f"ConversationTurn saved to database: {turn.id}")

    async def get_next_turn_number(self, conversation_id: str, is_admin: bool = False) -> int:
        """Get next turn number for conversation.

        Args:
            conversation_id: The conversation to get next turn number for
            is_admin: SEC-RBAC Phase 3 - admins can get next turn for any conversation

        Returns:
            The next sequential turn number (max existing + 1, or 1 if no turns)
        """
        from services.database.models import ConversationTurnDB

        stmt = select(func.max(ConversationTurnDB.turn_number)).where(
            ConversationTurnDB.conversation_id == conversation_id
        )

        result = await self.session.execute(stmt)
        max_turn = result.scalar()

        return (max_turn or 0) + 1

    async def get_most_recent_turn_provenance(
        self, conversation_id: str
    ) -> Optional[Dict[str, Any]]:
        """Issue #1030 R4 Step 11: DB-backed fallback for provenance lookup.

        Used by ProvenanceHandler when the in-memory sidecar has expired
        (turn aged out of the 30-min/10-turn window) or the process restarted.
        Returns the provenance dict from the most recent turn for this
        conversation (by turn_number desc) that has provenance in its metadata.

        Returns None if:
        - No turns exist for this conversation
        - No turn has provenance attached (legacy turns pre-R4)
        - DB query fails (caller fails-graceful)
        """
        from services.database.models import ConversationTurnDB

        # Walk turns newest-first, return first with provenance
        # (turn_metadata is the column; .turn_metadata is the attribute)
        stmt = (
            select(ConversationTurnDB)
            .where(ConversationTurnDB.conversation_id == conversation_id)
            .order_by(ConversationTurnDB.turn_number.desc())
            .limit(10)  # bounded scan; most recent within last 10 will have provenance if any
        )
        result = await self.session.execute(stmt)
        rows = result.scalars().all()
        for row in rows:
            md = row.turn_metadata or {}
            if isinstance(md, dict) and "provenance" in md and md["provenance"]:
                return md["provenance"]
        return None

    async def ensure_conversation_exists(
        self, conversation_id: str, user_id: Optional[str] = None
    ) -> None:
        """
        Ensure a conversation exists, creating it if necessary.

        This is needed because conversation_turns has a FK to conversations.
        Issue #563: Called before saving turns to handle new sessions.
        Issue #715: Sets lifecycle_state=ACTIVE on creation.

        Args:
            conversation_id: The conversation/session ID
            user_id: Optional user ID to associate with conversation
        """
        from services.database.models import ConversationDB

        # Check if conversation exists
        existing = await self.session.get(ConversationDB, conversation_id)
        if existing:
            return

        # Issue #840: Refuse to create conversation without valid user_id.
        # Conversations with user_id="unknown" become permanently invisible
        # in list_for_user() — better to skip creation (turn save will fail
        # on FK constraint) than create an orphaned record.
        if not user_id:
            logger.error(
                "ensure_conversation_exists_refused_no_user_id",
                conversation_id=conversation_id,
                reason="Cannot create conversation without user_id — would be invisible in sidebar",
            )
            return

        conversation = ConversationDB(
            id=conversation_id,
            user_id=user_id,
            session_id=conversation_id,
            title="Conversation",
            context={},
            is_active=True,
            lifecycle_state=ConversationLifecycleState.ACTIVE.value,
        )

        self.session.add(conversation)
        await self.session.commit()
        logger.debug(f"Created conversation: {conversation_id}")

    async def get_latest_for_user(self, user_id: str) -> Optional[domain.Conversation]:
        """
        Get the most recent active conversation for a user.

        Issue #563: Used for "Continue where you left off" prompt.
        Issue #715: Filters by lifecycle_state instead of is_active.

        Args:
            user_id: The user ID to find conversations for

        Returns:
            The most recent ACTIVE Conversation domain object, or None
        """
        from services.database.models import ConversationDB

        stmt = (
            select(ConversationDB)
            .where(ConversationDB.user_id == user_id)
            .where(ConversationDB.lifecycle_state == ConversationLifecycleState.ACTIVE.value)
            .order_by(ConversationDB.created_at.desc())
            .limit(1)
        )

        result = await self.session.execute(stmt)
        db_conv = result.scalar_one_or_none()

        if db_conv:
            return db_conv.to_domain()
        return None

    # Issue #565: Additional methods for conversation sidebar

    async def list_for_user(
        self,
        user_id: str,
        limit: int = 50,
        offset: int = 0,
        state: Optional[ConversationLifecycleState] = None,
    ) -> List[domain.Conversation]:
        """
        List conversations for a user, ordered by most recent first.

        Issue #565: Used for conversation history sidebar.
        Issue #715: Filters by lifecycle_state instead of is_active.

        Args:
            user_id: The user ID to find conversations for
            limit: Maximum number of conversations to return (default 50)
            offset: Number of conversations to skip for pagination
            state: Filter by lifecycle state (default: ACTIVE only)

        Returns:
            List of Conversation domain objects, newest first
        """
        from services.database.models import ConversationDB

        filter_state = state or ConversationLifecycleState.ACTIVE

        # Issue #587: Sort by last_activity_at (most recently active first)
        # Use COALESCE to fall back to created_at for conversations with no activity yet
        stmt = (
            select(ConversationDB)
            .where(ConversationDB.user_id == user_id)
            .where(ConversationDB.lifecycle_state == filter_state.value)
            .order_by(
                func.coalesce(ConversationDB.last_activity_at, ConversationDB.created_at).desc()
            )
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(stmt)
        db_convs = result.scalars().all()

        return [c.to_domain() for c in db_convs]

    async def search_for_user(
        self,
        user_id: str,
        query: str,
        limit: int = 50,
        offset: int = 0,
        states: Optional[List[ConversationLifecycleState]] = None,
    ) -> List[domain.Conversation]:
        """
        Search conversations by title for a user.

        Issue #786: GLUE-HISTORY-DIFF - History sidebar search.
        Issue #715: Filters by lifecycle_state. Defaults to ACTIVE + ARCHIVED
        (search should find archived conversations per spec #858 Section 5).

        Args:
            user_id: The user ID to search conversations for
            query: Search string to match against title (case-insensitive)
            limit: Maximum number of conversations to return (default 50)
            offset: Number of conversations to skip for pagination
            states: Lifecycle states to include (default: ACTIVE + ARCHIVED)

        Returns:
            List of Conversation domain objects matching the search, newest first
        """
        from services.database.models import ConversationDB

        # Search spans ACTIVE + ARCHIVED by default (spec #858 Section 5)
        filter_states = states or [
            ConversationLifecycleState.ACTIVE,
            ConversationLifecycleState.ARCHIVED,
        ]
        state_values = [s.value for s in filter_states]

        # Case-insensitive search on title using ILIKE
        search_pattern = f"%{query}%"
        stmt = (
            select(ConversationDB)
            .where(ConversationDB.user_id == user_id)
            .where(ConversationDB.lifecycle_state.in_(state_values))
            .where(ConversationDB.title.ilike(search_pattern))
            .order_by(
                func.coalesce(ConversationDB.last_activity_at, ConversationDB.created_at).desc()
            )
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(stmt)
        db_convs = result.scalars().all()

        return [c.to_domain() for c in db_convs]

    async def get_by_id(
        self, conversation_id: str, user_id: Optional[str] = None
    ) -> Optional[domain.Conversation]:
        """
        Get a specific conversation by ID.

        Issue #565: Used when switching conversations in sidebar.

        Args:
            conversation_id: The conversation ID to fetch

        Returns:
            Conversation domain object, or None if not found
        """
        from services.database.models import ConversationDB

        # D3 (ADR-071 #1252): scope at the data layer when the principal is
        # provided (the routes pass current_user.sub). When omitted, returns
        # unscoped + WARNs — an m-40 shim until all callers thread the principal.
        # The method itself was the (a,3) leak: fetch-by-PK with no owner filter.
        if user_id is None:
            logger.warning(
                "conversation_get_by_id_without_principal",
                conversation_id=str(conversation_id),
            )
            db_conv = await self.session.get(ConversationDB, conversation_id)
        else:
            stmt = select(ConversationDB).where(
                ConversationDB.id == conversation_id,
                ConversationDB.user_id == str(user_id),
            )
            db_conv = (await self.session.execute(stmt)).scalar_one_or_none()

        if db_conv:
            return db_conv.to_domain()
        return None

    async def create(self, user_id: str, title: Optional[str] = None) -> domain.Conversation:
        """
        Create a new conversation for a user.

        Issue #565: Used when clicking "New Chat" in sidebar.
        Issue #715: Sets lifecycle_state=ACTIVE on creation.

        Args:
            user_id: The user ID to create conversation for
            title: Optional title (defaults to "New conversation")

        Returns:
            The newly created Conversation domain object
        """
        import uuid

        from services.database.models import ConversationDB

        conversation_id = str(uuid.uuid4())

        conversation = ConversationDB(
            id=conversation_id,
            user_id=user_id,
            session_id=conversation_id,
            title=title or "New conversation",
            context={},
            is_active=True,
            lifecycle_state=ConversationLifecycleState.ACTIVE.value,
        )

        self.session.add(conversation)
        await self.session.commit()
        await self.session.refresh(conversation)

        logger.debug(f"Created new conversation: {conversation_id} for user: {user_id}")

        return conversation.to_domain()

    async def get_turn_count(self, conversation_id: str) -> int:
        """
        Get the number of turns in a conversation.

        Issue #565: Used for conversation list display.

        Args:
            conversation_id: The conversation to count turns for

        Returns:
            Number of turns in the conversation
        """
        from services.database.models import ConversationTurnDB

        stmt = select(func.count(ConversationTurnDB.id)).where(
            ConversationTurnDB.conversation_id == conversation_id
        )

        result = await self.session.execute(stmt)
        return result.scalar() or 0

    # ---- Layer-4 context-state persistence (#953 CONTEXT-PERSIST) ----
    # Persists the restart-fragile slice of the in-memory ConversationContext
    # (lens_stack + last_offer + floor flags — see
    # ConversationContext.to_persistable_state) into the existing
    # ConversationDB.context JSONB column, namespaced under "layer4_state" so it
    # never collides with any other use of the column. The async persist/hydrate
    # WIRING at the floor seam is the companion increment; these are the storage
    # primitives it builds on.
    _LAYER4_KEY = "layer4_state"

    async def save_context_state(self, conversation_id: str, state: dict) -> bool:
        """Persist the Layer-4 context slice for a conversation. Returns True on
        write, False if the conversation row doesn't exist (caller may
        ensure_conversation_exists first). JSONB is reassigned wholesale because
        SQLAlchemy doesn't track in-place dict mutation. #953."""
        from services.database.models import ConversationDB

        db_conv = await self.session.get(ConversationDB, conversation_id)
        if db_conv is None:
            return False
        # Copy-and-reassign so the ORM detects the change.
        merged = dict(db_conv.context or {})
        merged[self._LAYER4_KEY] = state
        db_conv.context = merged
        await self.session.commit()
        return True

    async def load_context_state(self, conversation_id: str) -> Optional[dict]:
        """Load the persisted Layer-4 context slice, or None if the conversation
        doesn't exist or has no persisted state (backward-compatible: a row that
        predates #953 simply returns None). #953."""
        from services.database.models import ConversationDB

        db_conv = await self.session.get(ConversationDB, conversation_id)
        if db_conv is None:
            return None
        return (db_conv.context or {}).get(self._LAYER4_KEY)

    async def update_title(self, conversation_id: str, title: str) -> None:
        """
        Update conversation title.

        Issue #598: Used to auto-generate title from first user message.

        Args:
            conversation_id: The conversation to update
            title: The new title
        """
        from services.database.models import ConversationDB

        db_conv = await self.session.get(ConversationDB, conversation_id)
        if db_conv:
            db_conv.title = title
            await self.session.commit()
            logger.debug(f"Updated conversation title: {conversation_id} -> {title[:30]}...")

    @staticmethod
    def generate_title_from_message(message: str, max_length: int = 50) -> str:
        """
        Generate a conversation title from a user message.

        Issue #598: Auto-title conversations based on first user message.

        Args:
            message: The user message to derive title from
            max_length: Maximum title length (default 50)

        Returns:
            A cleaned, truncated title string
        """
        import re

        if not message:
            return "New conversation"

        # Strip markdown formatting
        cleaned = re.sub(r"\*\*|__|\*|_|`|##+\s*", "", message)
        # Strip URLs
        cleaned = re.sub(r"https?://\S+", "", cleaned)
        # Strip excessive whitespace
        cleaned = " ".join(cleaned.split())
        # Trim leading/trailing whitespace
        cleaned = cleaned.strip()

        if not cleaned:
            return "New conversation"

        # Truncate with ellipsis if too long
        if len(cleaned) > max_length:
            # Try to break at word boundary
            truncated = cleaned[:max_length].rsplit(" ", 1)[0]
            if len(truncated) < max_length * 0.7:  # If we lost too much, just hard truncate
                truncated = cleaned[: max_length - 3]
            return truncated + "..."

        return cleaned

    # --- Lifecycle state transitions (Issue #715, spec #858) ---

    async def archive_conversation(self, conversation_id: str) -> Optional[domain.Conversation]:
        """
        Archive a conversation (ACTIVE → ARCHIVED).

        Issue #715: Sets lifecycle_state=ARCHIVED, records archived_at timestamp.
        Spec #858 Section 2: ACTIVE → ARCHIVED transition.

        Args:
            conversation_id: The conversation ID to archive

        Returns:
            Updated Conversation domain object, or None if not found/not ACTIVE
        """
        from services.database.models import ConversationDB

        db_conv = await self.session.get(ConversationDB, conversation_id)
        if not db_conv or db_conv.lifecycle_state != ConversationLifecycleState.ACTIVE.value:
            return None

        db_conv.lifecycle_state = ConversationLifecycleState.ARCHIVED.value
        db_conv.archived_at = datetime.now(timezone.utc)

        # Issue #1021 Q3=c: refresh preview + topics from the full turn set
        # on archive transition. Catches conversations that pivoted mid-flow
        # or were created before the user-history columns existed.
        from services.database.models import ConversationTurnDB

        turn_stmt = (
            select(ConversationTurnDB)
            .where(ConversationTurnDB.conversation_id == conversation_id)
            .order_by(ConversationTurnDB.turn_number)
        )
        all_turns = (await self.session.execute(turn_stmt)).scalars().all()
        if all_turns:
            db_conv.turn_count = len(all_turns)
            db_conv.preview = _build_preview(all_turns[0].user_message)
            db_conv.topics = _extract_topics_heuristic(all_turns)

        await self.session.commit()
        await self.session.refresh(db_conv)

        logger.info(
            "conversation_archived",
            conversation_id=conversation_id,
            turn_count=db_conv.turn_count,
            topic_count=len(db_conv.topics or []),
        )
        return db_conv.to_domain()

    async def delete_conversation(self, conversation_id: str) -> Optional[domain.Conversation]:
        """
        Soft-delete a conversation (ACTIVE or ARCHIVED → DELETED).

        Issue #715: Sets lifecycle_state=DELETED, records deleted_at timestamp.
        Spec #858 Section 2: Terminal state, no return path.

        Args:
            conversation_id: The conversation ID to soft-delete

        Returns:
            Updated Conversation domain object, or None if not found/already deleted
        """
        from services.database.models import ConversationDB

        db_conv = await self.session.get(ConversationDB, conversation_id)
        if not db_conv or db_conv.lifecycle_state == ConversationLifecycleState.DELETED.value:
            return None

        db_conv.lifecycle_state = ConversationLifecycleState.DELETED.value
        db_conv.deleted_at = datetime.now(timezone.utc)
        db_conv.is_active = False  # Keep is_active in sync during deprecation period
        await self.session.commit()
        await self.session.refresh(db_conv)

        logger.info("conversation_deleted", conversation_id=conversation_id)
        return db_conv.to_domain()

    async def reactivate_conversation(self, conversation_id: str) -> Optional[domain.Conversation]:
        """
        Reactivate an archived conversation (ARCHIVED → ACTIVE).

        Issue #715: Sets lifecycle_state=ACTIVE, clears archived_at.
        Spec #858 Section 2: Only ARCHIVED → ACTIVE is valid (not DELETED/COMPOSTED).

        Args:
            conversation_id: The conversation ID to reactivate

        Returns:
            Updated Conversation domain object, or None if not found/not ARCHIVED
        """
        from services.database.models import ConversationDB

        db_conv = await self.session.get(ConversationDB, conversation_id)
        if not db_conv or db_conv.lifecycle_state != ConversationLifecycleState.ARCHIVED.value:
            return None

        db_conv.lifecycle_state = ConversationLifecycleState.ACTIVE.value
        db_conv.archived_at = None
        await self.session.commit()
        await self.session.refresh(db_conv)

        logger.info("conversation_reactivated", conversation_id=conversation_id)
        return db_conv.to_domain()


class DBUserHistoryRepository:
    """Postgres-backed implementation of UserHistoryRepository (Issue #1021).

    Implements the UserHistoryRepository ABC defined in
    `services/memory/user_history.py`. Projects ConversationDB +
    ConversationTurnDB into ConversationSummary / ConversationDetail
    shapes for the Layer 3 history surface.

    Per #1021 PM disposition Q1=γ: extends ConversationDB rather than
    standing up a parallel summary table. The `topics`, `preview`,
    `is_private`, and `turn_count` columns landed in migration
    `a1021userhist`.

    Excludes DELETED conversations from all reads (user soft-deleted).
    Surfaces ACTIVE + ARCHIVED. Private conversations are returned only
    when `include_private=True` for `get_conversations`; never surfaced
    in `search_conversations` (per InMemory impl's contract).
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_conversations(
        self,
        user_id: str,
        offset: int,
        limit: int,
        include_private: bool,
    ) -> tuple[list, int]:
        """Paginated list of ConversationSummary for a user.

        Ordered by last_activity_at DESC (COALESCE → created_at).
        Excludes DELETED. Filters private unless include_private.
        Returns (page, total_count).
        """
        from services.database.models import ConversationDB
        from services.memory.user_history import ConversationSummary

        visible_states = [
            ConversationLifecycleState.ACTIVE.value,
            ConversationLifecycleState.ARCHIVED.value,
        ]

        base_filters = [
            ConversationDB.user_id == user_id,
            ConversationDB.lifecycle_state.in_(visible_states),
        ]
        if not include_private:
            base_filters.append(ConversationDB.is_private.is_(False))

        count_stmt = select(func.count(ConversationDB.id)).where(and_(*base_filters))
        total = (await self.session.execute(count_stmt)).scalar() or 0

        page_stmt = (
            select(ConversationDB)
            .where(and_(*base_filters))
            .order_by(
                func.coalesce(ConversationDB.last_activity_at, ConversationDB.created_at).desc()
            )
            .offset(offset)
            .limit(limit)
        )
        db_convs = (await self.session.execute(page_stmt)).scalars().all()

        summaries = [self._to_summary(c) for c in db_convs]
        return summaries, total

    async def search_conversations(
        self,
        user_id: str,
        query: str,
        limit: int,
    ) -> list:
        """Search across title, preview, and topics.

        Excludes private + DELETED. Title matches sort first, then by
        recency. Topic search uses JSONB containment via the GIN index
        (idx_conversations_topics_gin).
        """
        from services.database.models import ConversationDB
        from services.memory.user_history import ConversationSummary

        query_lower = query.lower()
        ilike_pattern = f"%{query}%"

        visible_states = [
            ConversationLifecycleState.ACTIVE.value,
            ConversationLifecycleState.ARCHIVED.value,
        ]

        # Topic match uses JSONB path query: topics @> '["query"]' style won't
        # match case-insensitive, so we use the @? JSON path operator with
        # like_regex. Simpler portable approach: cast topics to text and ILIKE.
        # Loses GIN index for topic-only matches but keeps the title+preview
        # path fast; topic-only matches fall back to seq scan, acceptable for
        # conversation-history scale (typically < 10k rows per user).
        stmt = (
            select(ConversationDB)
            .where(ConversationDB.user_id == user_id)
            .where(ConversationDB.lifecycle_state.in_(visible_states))
            .where(ConversationDB.is_private.is_(False))
            .where(
                or_(
                    ConversationDB.title.ilike(ilike_pattern),
                    ConversationDB.preview.ilike(ilike_pattern),
                    func.cast(ConversationDB.topics, String).ilike(ilike_pattern),
                )
            )
            .order_by(
                # Title matches first (rank by title-match bit), then recency.
                func.lower(ConversationDB.title).ilike(ilike_pattern).desc(),
                func.coalesce(ConversationDB.last_activity_at, ConversationDB.created_at).desc(),
            )
            .limit(limit)
        )

        db_convs = (await self.session.execute(stmt)).scalars().all()
        return [self._to_summary(c) for c in db_convs]

    async def set_private(
        self,
        user_id: str,
        conversation_id: str,
        is_private: bool,
    ) -> bool:
        """Flip privacy flag on a conversation. Returns True if updated."""
        from services.database.models import ConversationDB

        db_conv = await self.session.get(ConversationDB, conversation_id)
        if not db_conv or db_conv.user_id != user_id:
            return False

        db_conv.is_private = is_private
        await self.session.commit()
        logger.info(
            "conversation_privacy_set",
            conversation_id=conversation_id,
            user_id=user_id,
            is_private=is_private,
        )
        return True

    async def get_detail(
        self,
        user_id: str,
        conversation_id: str,
    ) -> Optional[Any]:
        """Full conversation with all turns. Verifies user ownership."""
        from services.database.models import ConversationDB, ConversationTurnDB
        from services.memory.user_history import ConversationDetail

        db_conv = await self.session.get(ConversationDB, conversation_id)
        if not db_conv or db_conv.user_id != user_id:
            return None
        if db_conv.lifecycle_state == ConversationLifecycleState.DELETED.value:
            return None

        turn_stmt = (
            select(ConversationTurnDB)
            .where(ConversationTurnDB.conversation_id == conversation_id)
            .order_by(ConversationTurnDB.turn_number)
        )
        db_turns = (await self.session.execute(turn_stmt)).scalars().all()

        turns = []
        for t in db_turns:
            if t.user_message:
                turns.append(
                    {
                        "role": "user",
                        "content": t.user_message,
                        "timestamp": t.created_at.isoformat() if t.created_at else None,
                    }
                )
            if t.assistant_response:
                turns.append(
                    {
                        "role": "assistant",
                        "content": t.assistant_response,
                        "timestamp": t.completed_at.isoformat() if t.completed_at else None,
                    }
                )

        return ConversationDetail(
            conversation_id=db_conv.id,
            title=db_conv.title,
            started_at=db_conv.created_at,
            last_activity=db_conv.last_activity_at or db_conv.created_at,
            is_private=bool(db_conv.is_private),
            topics=list(db_conv.topics or []),
            turns=turns,
        )

    @staticmethod
    def _to_summary(db_conv) -> Any:
        from services.memory.user_history import ConversationSummary

        return ConversationSummary(
            conversation_id=db_conv.id,
            title=db_conv.title or "",
            started_at=db_conv.created_at,
            last_activity=db_conv.last_activity_at or db_conv.created_at,
            turn_count=int(db_conv.turn_count or 0),
            topics=list(db_conv.topics or []),
            preview=db_conv.preview or "",
            is_private=bool(db_conv.is_private),
        )


class EthicsAuditRepository:
    """Repository for ethics-decision audit log persistence (Issue #1018).

    Replaces the in-memory list at `services/ethics/audit_transparency.py`.
    Used by both the write path (`audit_transparency.log_ethics_decision`)
    and the read path (`services/api/transparency.py` endpoints).

    Architectural notes from Phase 1 design + Architect's Apr 30 ratification:
    - Write path opens its own session via `AsyncSessionFactory()` (NOT
      plumbed through the request transaction). This is deliberate: an
      audit-write failure must NOT roll back the ethics decision. Joining
      the request transaction would couple ethics enforcement to request
      shape and make audit failures user-visible. Better to lose a single
      audit entry than the decision itself.
    - Read path queries indexed columns: `(session_id)`, `(user_id, timestamp)`,
      `(event_type, timestamp)`, `(timestamp)` — see migration
      `alembic/versions/a1018_add_ethics_audit_log.py`.
    - Retention: scheduled cleanup via `EthicsAuditCleanupJob` (sibling of
      `BlacklistCleanupJob`); 90-day TTL preserved.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, entry) -> None:
        """Persist a domain `AuditLogEntry` via DB.

        Caller is responsible for transaction lifecycle (commit/rollback).
        For per-call sessions opened in `audit_transparency.log_ethics_decision`,
        a fresh `AsyncSessionFactory()` context manager handles commit.
        """
        db_entry = EthicsAuditLogDB.from_domain(entry)
        self.session.add(db_entry)
        await self.session.flush()

    async def find_by_session(self, session_id: str, limit: int = 50) -> List:
        """Recent entries for a given session, newest first.

        Returns list of domain `AuditLogEntry` (NOT DB rows). Limit caps
        the number of entries returned per the existing transparency
        endpoint behavior.
        """
        result = await self.session.execute(
            select(EthicsAuditLogDB)
            .where(EthicsAuditLogDB.session_id == session_id)
            .order_by(EthicsAuditLogDB.timestamp.desc())
            .limit(limit)
        )
        return [row.to_domain() for row in result.scalars().all()]

    async def find_by_user(self, user_id, limit: int = 50) -> List:
        """Recent entries for a given user, newest first."""
        result = await self.session.execute(
            select(EthicsAuditLogDB)
            .where(EthicsAuditLogDB.user_id == user_id)
            .order_by(EthicsAuditLogDB.timestamp.desc())
            .limit(limit)
        )
        return [row.to_domain() for row in result.scalars().all()]

    async def summarize_recent(self, days: int = 30) -> Dict[str, Any]:
        """Aggregate stats over recent entries (matches the existing
        `audit_transparency.get_system_audit_summary` response shape).

        Returns counts per event_type + per boundary_type (the latter from
        details JSON). Uses indexed `(event_type, timestamp)` for the time
        filter.
        """
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)

        # Total entries in window + per-event-type counts
        type_counts = await self.session.execute(
            select(
                EthicsAuditLogDB.event_type,
                func.count(EthicsAuditLogDB.entry_id).label("count"),
            )
            .where(EthicsAuditLogDB.timestamp >= cutoff)
            .group_by(EthicsAuditLogDB.event_type)
        )
        events_by_type: Dict[str, int] = {row[0]: row[1] for row in type_counts}
        total_entries = sum(events_by_type.values())

        # Boundary-type breakdown — pulled from JSONB details field for
        # event_type='ethics_decision' rows. Keep this fetch bounded so
        # we don't pull the full window into memory if it grows large;
        # the legacy in-memory implementation iterated the full list, so
        # this matches established behavior at small scale.
        recent_decisions = await self.session.execute(
            select(EthicsAuditLogDB)
            .where(
                EthicsAuditLogDB.timestamp >= cutoff,
                EthicsAuditLogDB.event_type == "ethics_decision",
            )
            .order_by(EthicsAuditLogDB.timestamp.desc())
        )
        boundary_breakdown: Dict[str, int] = {}
        for row in recent_decisions.scalars().all():
            details = row.details or {}
            bt = details.get("boundary_type")
            if bt:
                boundary_breakdown[bt] = boundary_breakdown.get(bt, 0) + 1

        return {
            "period_days": days,
            "total_entries": total_entries,
            "events_by_type": events_by_type,
            "boundary_breakdown": boundary_breakdown,
        }

    async def delete_older_than(self, cutoff: datetime) -> int:
        """Retention sweep: delete entries with `timestamp < cutoff`.

        Returns count deleted. Called by `EthicsAuditCleanupJob` on the
        24-hour cadence; can also be invoked synchronously by the manual
        `POST /transparency/cleanup` endpoint.
        """
        from sqlalchemy import delete as sa_delete

        result = await self.session.execute(
            sa_delete(EthicsAuditLogDB).where(EthicsAuditLogDB.timestamp < cutoff)
        )
        return result.rowcount or 0

    async def count(self) -> int:
        """Total row count (used by /transparency/stats)."""
        result = await self.session.execute(select(func.count(EthicsAuditLogDB.entry_id)))
        return result.scalar_one() or 0


class InsightRepository:
    """Repository for SurfaceableInsight persistence (Issue #1035).

    Replaces the in-memory dict at `services/mux/composting_pipeline.py
    InsightJournal._insights`. Used by the composting pipeline (write path)
    and the four insight-surfacing modes (#1030 Pull, #1031 Passive,
    #1032 Push, #1033 COMPOSTED-experience) on the read path.

    Architectural notes from #1035 audit walkthrough (May 3) + #1018 pattern lift:
    - Write path opens its own session via `AsyncSessionFactory.session_scope()`
      (NOT plumbed through the request transaction). Same rationale as
      EthicsAuditRepository: an insight-write failure must not roll back the
      composting cycle.
    - Read path queries indexed columns: `(user_id, created_at)`,
      `(user_id, surfaced_count)`, `(object_id)`, `(user_id)`. See migration
      `alembic/versions/a1035_add_insights_table.py`.
    - User-scoped from day one (PM directive: "anything else is a false economy").
    - `clear()` is per-user only (no system-wide wipe per audit Q6).
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, insight) -> None:
        """Persist a `SurfaceableInsight` via DB.

        Caller is responsible for transaction lifecycle. For per-call sessions
        opened in InsightJournal, AsyncSessionFactory.session_scope() handles
        commit.
        """
        db_row = InsightDB.from_domain(insight)
        self.session.add(db_row)
        await self.session.flush()

    async def get(self, insight_id: str):
        """Fetch a single insight by id; returns SurfaceableInsight or None."""
        result = await self.session.execute(select(InsightDB).where(InsightDB.id == insight_id))
        row = result.scalar_one_or_none()
        return row.to_domain() if row else None

    async def list_for_user(
        self,
        user_id: str,
        limit: Optional[int] = None,
        exclude_deleted: bool = True,
    ) -> List:
        """All non-deleted insights for a user, newest first.

        Used by the Insight Journal page (#1031 Passive mode) for browse-on-
        demand listing.

        Per #1031 Q1 (May 3): soft-delete semantics — `exclude_deleted=True`
        is the default; deleted insights are hidden from the journal page.
        Pass `exclude_deleted=False` for admin/diagnostic use cases.
        """
        filters = [InsightDB.user_id == user_id]
        if exclude_deleted:
            filters.append(InsightDB.is_deleted == False)
        stmt = select(InsightDB).where(and_(*filters)).order_by(InsightDB.created_at.desc())
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self.session.execute(stmt)
        return [row.to_domain() for row in result.scalars().all()]

    async def update_user_correction(self, insight_id: str, user_id: str, correction_text: str):
        """Record the user's free-text correction for an insight (#1031 Q2).

        Verifies user owns the insight (auth-scoping defense in depth).
        Returns updated SurfaceableInsight or None if not found / not owned.
        """
        result = await self.session.execute(
            select(InsightDB).where(
                and_(
                    InsightDB.id == insight_id,
                    InsightDB.user_id == user_id,
                )
            )
        )
        row = result.scalar_one_or_none()
        if row is None:
            return None
        row.user_correction = correction_text
        row.user_response = "corrected"
        await self.session.flush()
        return row.to_domain()

    async def soft_delete(self, insight_id: str, user_id: str) -> bool:
        """Per-insight soft delete (#1031 Q1).

        Sets `is_deleted=True`. Verifies user owns the insight. Returns
        True if deletion happened (insight existed + was owned), False
        otherwise.
        """
        result = await self.session.execute(
            select(InsightDB).where(
                and_(
                    InsightDB.id == insight_id,
                    InsightDB.user_id == user_id,
                )
            )
        )
        row = result.scalar_one_or_none()
        if row is None:
            return False
        row.is_deleted = True
        await self.session.flush()
        return True

    async def soft_delete_all(self, user_id: str) -> int:
        """Per-user reset-all (#1031 Q1).

        Sets `is_deleted=True` for all of the user's not-yet-deleted insights.
        Used by the Insight Journal "Reset all learnings" affordance.
        Returns count of insights soft-deleted in this call.
        """
        from sqlalchemy import update as sa_update

        # Count first (only those not already deleted)
        count_result = await self.session.execute(
            select(func.count(InsightDB.id)).where(
                and_(
                    InsightDB.user_id == user_id,
                    InsightDB.is_deleted == False,
                )
            )
        )
        affected = count_result.scalar() or 0

        await self.session.execute(
            sa_update(InsightDB)
            .where(
                and_(
                    InsightDB.user_id == user_id,
                    InsightDB.is_deleted == False,
                )
            )
            .values(is_deleted=True)
        )
        await self.session.flush()
        return affected

    async def get_for_object(self, object_id: str, user_id: Optional[str] = None) -> List:
        """All insights derived from a particular composted object.

        #1252 (a,3): when ``user_id`` is provided the result is scoped to that
        owner at the data layer — two users with insights on the same object
        never see each other's (the fetch-by-object cross-owner leak closed).
        Omitting it (the m-40 shim) returns every insight for the object and
        logs a WARNING, so pre-existing callers keep working until they thread
        the principal.
        """
        stmt = select(InsightDB).where(InsightDB.object_id == object_id)
        if user_id is None:
            logger.warning("insight_get_for_object_without_principal", object_id=object_id)
        else:
            stmt = stmt.where(InsightDB.user_id == user_id)
        result = await self.session.execute(stmt)
        return [row.to_domain() for row in result.scalars().all()]

    async def get_unsurfaced(
        self,
        user_id: str,
        min_confidence: float = 0.75,
        trust_stage: int = 3,
        limit: int = 10,
    ) -> List:
        """Insights eligible for Push surfacing (#1032).

        Returns insights where:
        - user_id matches
        - surfaced_count == 0 (never surfaced)
        - min_trust_stage <= trust_stage (trust gate)
        - learning.confidence >= min_confidence (quality gate)

        Caller (#1032) layers additional gates: Stage 3+ hard gate,
        right-moment, anti-spam, mute. This method is the candidate-set
        retrieval; gates are applied above.

        Sorted by confidence desc; cooldown (`is_surfaceable`) is applied
        in Python because last_surfaced + 24h-cooldown logic is currently
        on the dataclass not the SQL layer (lift later if perf demands).
        """
        result = await self.session.execute(
            select(InsightDB)
            .where(
                InsightDB.user_id == user_id,
                InsightDB.surfaced_count == 0,
                InsightDB.min_trust_stage <= trust_stage,
                # #1031: exclude soft-deleted from Push retrieval
                InsightDB.is_deleted == False,
            )
            .order_by(InsightDB.created_at.desc())
        )
        rows = result.scalars().all()

        # Apply confidence + surfaceability filters in Python (relevance
        # scoring elsewhere; this is candidate retrieval).
        candidates = []
        for row in rows:
            insight = row.to_domain()
            if insight.learning and insight.learning.confidence < min_confidence:
                continue
            if not insight.is_surfaceable(trust_stage):
                continue
            candidates.append(insight)
            if len(candidates) >= limit:
                break

        # Sort by attention then confidence (matches existing in-memory shape)
        candidates.sort(
            key=lambda i: (
                i.requires_attention,
                i.learning.confidence if i.learning else 0,
            ),
            reverse=True,
        )
        return candidates[:limit]

    async def get_for_context(
        self,
        user_id: str,
        context_entities: Optional[List[str]] = None,
        context_topics: Optional[List[str]] = None,
        trust_stage: int = 1,
        limit: int = 5,
    ) -> List:
        """Insights relevant to the current context (Pull mode #1030).

        Pulls all user insights matching the trust gate, then scores
        relevance in Python (entity overlap + topic overlap + context_tags
        overlap with insight metadata). Acceptable at MVP scale; if perf
        demands, migrate scoring to SQL.

        Mirrors the existing `InsightJournal.get_for_context` logic so the
        DB-backed implementation is a drop-in.
        """
        context_entities = context_entities or []
        context_topics = context_topics or []
        entity_set = set(context_entities)
        topic_set = set(context_topics)

        # All candidate insights for this user that pass trust gate
        result = await self.session.execute(
            select(InsightDB).where(
                InsightDB.user_id == user_id,
                InsightDB.min_trust_stage <= trust_stage,
                # #1031: exclude soft-deleted from Pull retrieval
                InsightDB.is_deleted == False,
            )
        )
        rows = result.scalars().all()

        scored = []
        for row in rows:
            insight = row.to_domain()
            if not insight.is_surfaceable(trust_stage):
                continue

            relevance = 0
            if insight.learning:
                for entity in insight.learning.applies_to_entities:
                    if entity in entity_set:
                        relevance += 2
                for tag in insight.learning.topic_tags:
                    if tag in topic_set:
                        relevance += 1
            for tag in insight.context_tags:
                if tag in entity_set or tag in topic_set:
                    relevance += 1

            if relevance > 0:
                scored.append((relevance, insight))

        scored.sort(
            key=lambda x: (
                x[0],
                x[1].learning.confidence if x[1].learning else 0,
            ),
            reverse=True,
        )
        return [s[1] for s in scored[:limit]]

    async def mark_surfaced(self, insight_id: str, response: str):
        """Record that an insight was surfaced + the user's response.

        Increments `surfaced_count`, sets `last_surfaced=now()`,
        sets `user_response`. Returns updated SurfaceableInsight or None.
        """
        result = await self.session.execute(select(InsightDB).where(InsightDB.id == insight_id))
        row = result.scalar_one_or_none()
        if row is None:
            return None

        row.surfaced_count = (row.surfaced_count or 0) + 1
        row.last_surfaced = datetime.now(timezone.utc)
        row.user_response = response
        await self.session.flush()
        return row.to_domain()

    async def count(self, user_id: Optional[str] = None) -> int:
        """Row count, optionally scoped to a single user."""
        stmt = select(func.count(InsightDB.id))
        if user_id is not None:
            stmt = stmt.where(InsightDB.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one() or 0

    async def clear(self, user_id: str) -> int:
        """Per-user clear (#1035 Q6 resolution).

        Deletes all insights belonging to `user_id`. Returns count deleted.
        Used by the Insight Journal "Reset all learnings" affordance (#1031).
        """
        from sqlalchemy import delete as sa_delete

        result = await self.session.execute(
            sa_delete(InsightDB).where(InsightDB.user_id == user_id)
        )
        return result.rowcount or 0


class StandupConversationRepository:
    """Repository for StandupConversation persistence (Issue #1052, PRE-900).

    Replaces the in-memory module-level singleton dict at
    `services/conversation/conversation_handler.py:42-43`. Used by
    `StandupConversationManager` (write + read path) so partial captures
    survive server restarts — required for #900 Phase 4.

    Architectural notes (matches #1018/#1035 pattern):
    - Write path opens its own session via `AsyncSessionFactory.session_scope()`
      (NOT plumbed through the request transaction). A standup-state-write
      failure must not roll back the user's request.
    - User-scoped from day one (PM directive May 3).
    - Active-conversation lookup uses index on (user_id, state).
    """

    # Terminal states — conversations in these states are not "active"
    _TERMINAL_STATES = ("complete", "abandoned")

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, conversation) -> None:
        """Persist a `StandupConversation` row.

        Caller owns the transaction. For per-call sessions opened in
        StandupConversationManager, AsyncSessionFactory.session_scope()
        handles commit.
        """
        from services.database.models import StandupConversationDB

        db_row = StandupConversationDB.from_domain(conversation)
        self.session.add(db_row)
        await self.session.flush()

    async def get_by_id(self, conversation_id: str):
        """Fetch a conversation by id; returns StandupConversation or None."""
        from services.database.models import StandupConversationDB

        result = await self.session.execute(
            select(StandupConversationDB).where(StandupConversationDB.id == conversation_id)
        )
        row = result.scalar_one_or_none()
        return row.to_domain() if row else None

    async def get_by_session_id(self, session_id: str):
        """Fetch most-recent conversation for a session id; returns
        StandupConversation or None.

        Multiple standups per session are possible over time; this returns
        the latest by created_at (matches the singleton-dict semantics where
        only one was held).
        """
        from services.database.models import StandupConversationDB

        result = await self.session.execute(
            select(StandupConversationDB)
            .where(StandupConversationDB.session_id == session_id)
            .order_by(StandupConversationDB.created_at.desc())
            .limit(1)
        )
        row = result.scalar_one_or_none()
        return row.to_domain() if row else None

    async def get_active_for_user(self, user_id: str) -> List:
        """All non-terminal conversations for a user, newest first.

        Used to surface SUSPENDED standups for resume per #900 Phase 4.
        """
        from services.database.models import StandupConversationDB

        result = await self.session.execute(
            select(StandupConversationDB)
            .where(
                and_(
                    StandupConversationDB.user_id == user_id,
                    ~StandupConversationDB.state.in_(self._TERMINAL_STATES),
                )
            )
            .order_by(StandupConversationDB.created_at.desc())
        )
        return [row.to_domain() for row in result.scalars().all()]

    async def update(self, conversation) -> None:
        """Replace the persisted row with the in-memory state.

        Uses the row's existing id; raises ValueError if not found. The
        persistence shape is full-replace rather than field-by-field patch
        because StandupConversation aggregates state (turns, preferences,
        context) that's mutated atomically by the manager.
        """
        from datetime import datetime, timezone

        from services.database.models import StandupConversationDB

        result = await self.session.execute(
            select(StandupConversationDB).where(StandupConversationDB.id == conversation.id)
        )
        row = result.scalar_one_or_none()
        if row is None:
            raise ValueError(f"StandupConversation {conversation.id!r} not found for update")

        row.session_id = conversation.session_id
        row.user_id = conversation.user_id
        row.state = conversation.state.value if conversation.state else None
        row.previous_state = (
            conversation.previous_state.value if conversation.previous_state else None
        )
        row.preferences = conversation.preferences or {}
        row.current_standup = conversation.current_standup
        row.standup_versions = conversation.standup_versions or []
        row.turns = [t.to_dict() for t in (conversation.turns or [])]
        row.context = conversation.context or {}
        row.partial_capture = (
            conversation.partial_capture.to_dict()
            if conversation.partial_capture
            else {"yesterday": [], "today": [], "blockers": []}
        )
        row.completed_at = conversation.completed_at
        # #1079: tz-aware UTC to match the timestamptz column and the manager's
        # tz-aware writes; naive here is interpreted per DB session tz and feeds
        # naive-vs-aware subtraction crashes in timeout/duration math.
        row.updated_at = datetime.now(timezone.utc)
        await self.session.flush()

    async def delete(self, conversation_id: str) -> bool:
        """Hard-delete a conversation. Returns True if a row was removed."""
        from sqlalchemy import delete as sa_delete

        from services.database.models import StandupConversationDB

        result = await self.session.execute(
            sa_delete(StandupConversationDB).where(StandupConversationDB.id == conversation_id)
        )
        return bool(result.rowcount)

    async def count_for_user(self, user_id: str) -> int:
        """Count conversations for a user (diagnostics)."""
        from services.database.models import StandupConversationDB

        result = await self.session.execute(
            select(func.count())
            .select_from(StandupConversationDB)
            .where(StandupConversationDB.user_id == user_id)
        )
        return int(result.scalar() or 0)

    async def delete_stale(self, max_age_minutes: int) -> int:
        """Delete non-COMPLETE conversations older than max_age_minutes.

        Returns the count of deleted rows. Used by
        StandupConversationManager.cleanup_expired().
        """
        from sqlalchemy import delete as sa_delete

        from services.database.models import StandupConversationDB

        cutoff = datetime.now() - timedelta(minutes=max_age_minutes)
        result = await self.session.execute(
            sa_delete(StandupConversationDB).where(
                and_(
                    StandupConversationDB.updated_at < cutoff,
                    StandupConversationDB.state != "complete",
                )
            )
        )
        return result.rowcount or 0


class ArtifactRepository(BaseRepository):
    """Read/write persistence for Artifacts (#952). Owner-scoped CRUD with
    is_admin bypass (the #470 pattern); mirrors InsightRepository/FileRepository.
    Persists via ArtifactDB.from_domain (JSON-safe) and returns domain Artifacts."""

    async def add(self, artifact: domain.Artifact) -> domain.Artifact:
        from services.database.models import ArtifactDB

        self.session.add(ArtifactDB.from_domain(artifact))
        await self.session.commit()
        return artifact

    async def get_by_id(
        self,
        artifact_id: str,
        owner_id: Optional[str] = None,
        is_admin: bool = False,
    ) -> Optional[domain.Artifact]:
        from services.database.models import ArtifactDB

        # D3 (ADR-071 #1252): filter at the data layer (in the SELECT), not
        # post-hoc in Python — a missed/incorrect post-hoc check is the leak
        # vector D3 closes. Behavior preserved: owner-scoped unless admin or an
        # explicit unscoped/internal fetch (owner_id=None, used by existence/
        # round-trip checks). Tightening the None path to *require* a principal
        # belongs with the D5 guard + the broad caller migration (P5/P6), not
        # this query-level move. All production callers already pass owner_id.
        stmt = select(ArtifactDB).where(ArtifactDB.id == artifact_id)
        if owner_id is not None and not is_admin:
            stmt = stmt.where(ArtifactDB.owner_id == str(owner_id))
        row = (await self.session.execute(stmt)).scalar_one_or_none()
        return row.to_domain() if row else None

    async def list_for_owner(
        self,
        owner_id: str,
        source_type: Optional[str] = None,
        limit: int = 50,
    ) -> List[domain.Artifact]:
        from services.database.models import ArtifactDB

        stmt = select(ArtifactDB).where(ArtifactDB.owner_id == owner_id)
        if source_type:
            stmt = stmt.where(ArtifactDB.source_type == source_type)
        stmt = stmt.order_by(ArtifactDB.created_at.desc()).limit(limit)
        result = await self.session.execute(stmt)
        return [row.to_domain() for row in result.scalars().all()]

    async def delete(
        self,
        artifact_id: str,
        owner_id: Optional[str] = None,
        is_admin: bool = False,
    ) -> bool:
        from services.database.models import ArtifactDB

        row = await self.session.get(ArtifactDB, artifact_id)
        if row is None:
            return False
        if owner_id and not is_admin and str(row.owner_id) != str(owner_id):
            return False  # not the owner → refuse (no cross-owner delete)
        await self.session.delete(row)
        await self.session.commit()
        return True

    async def update_title(
        self,
        artifact_id: str,
        new_title: str,
        owner_id: Optional[str] = None,
        is_admin: bool = False,
    ) -> Optional[domain.Artifact]:
        """Rename an artifact (#1184) — updates ``payload['title']`` (where the
        title rides; the projected /files filename derives from it). Owner-scoped
        (#470); cross-owner → None (no cross-owner rename, no existence leak —
        the #1241 (a,3) discipline)."""
        from sqlalchemy.orm.attributes import flag_modified

        from services.database.models import ArtifactDB

        row = await self.session.get(ArtifactDB, artifact_id)
        if row is None:
            return None
        if owner_id and not is_admin and str(row.owner_id) != str(owner_id):
            return None
        payload = dict(row.payload or {})
        payload["title"] = new_title
        row.payload = payload
        flag_modified(row, "payload")  # JSON column: ensure the reassignment flushes
        await self.session.commit()
        return row.to_domain()


class SessionActivityRepository(BaseRepository):
    """ADR-078 D1/D1a (#1394) — owner-scoped persistence for the session-activity
    ledger (external creations: issue #107, docs). Written by ONE central observer
    (OQ-3); read by B4 recall now and B3 antecedent resolution later.

    D1a (the non-negotiable, HOST trust-lens): the reader keys on ``owner_id`` BY
    CONSTRUCTION. ``list_for_session`` REQUIRES ``owner_id`` (not Optional, no admin
    bypass, no unscoped path) and always filters ``owner_id AND conversation_id`` —
    so a second user's activity can never be returned. This is deliberately stricter
    than ``ArtifactRepository.get_by_id`` (which keeps an ``owner_id=None`` internal
    path): a ledger read feeds resolution context, so an unscoped read here IS the
    cross-user leak (#1366 / ADR-071 class). Cross-user resolution is not expressible.
    """

    async def record(
        self,
        *,
        owner_id: str,
        conversation_id: str,
        action_type: str,
        target_ref: str,
        turn_id: Optional[str] = None,
        target_title: Optional[str] = None,
    ) -> domain.SessionActivity:
        """Write one ledger row (the observer's single call). owner_id is required."""
        from services.database.models import SessionActivityDB

        row = SessionActivityDB(
            id=str(uuid.uuid4()),
            owner_id=str(owner_id),
            conversation_id=str(conversation_id),
            action_type=action_type,
            target_ref=target_ref,
            turn_id=turn_id,
            target_title=target_title,
        )
        self.session.add(row)
        await self.session.commit()
        return row.to_domain()

    async def list_for_session(
        self,
        owner_id: str,
        conversation_id: str,
        limit: int = 50,
    ) -> List[domain.SessionActivity]:
        """D1a owner-scoped reader — ``owner_id`` AND ``conversation_id`` are ALWAYS
        in the WHERE. There is no owner_id=None / admin path by design; a second
        user's rows are unreturnable. Newest first."""
        from services.database.models import SessionActivityDB

        stmt = (
            select(SessionActivityDB)
            .where(
                SessionActivityDB.owner_id == str(owner_id),
                SessionActivityDB.conversation_id == str(conversation_id),
            )
            .order_by(SessionActivityDB.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return [row.to_domain() for row in result.scalars().all()]


# Repository factory
class RepositoryFactory:
    """Creates repositories with session
    NOTE: The caller is responsible for closing the returned session (repos["session"]) after use, ideally in a finally block.
    """

    @staticmethod
    async def get_repositories():
        """Get all repositories with a new session
        DEPRECATED: Use AsyncSessionFactory.session_scope() directly for better resource management.
        This method is maintained for backward compatibility only.
        """
        session = await AsyncSessionFactory.create_session()
        return {
            "products": ProductRepository(session),
            "features": FeatureRepository(session),
            "work_items": WorkItemRepository(session),
            "workflows": WorkflowRepository(session),
            "tasks": TaskRepository(session),
            "projects": ProjectRepository(session),  # PM-009: Add project repository
            "project_integrations": ProjectIntegrationRepository(
                session
            ),  # PM-009: Add integration repository
            "knowledge_graph": KnowledgeGraphRepository(
                session
            ),  # PM-040: Add knowledge graph repository
            "session": session,
        }
