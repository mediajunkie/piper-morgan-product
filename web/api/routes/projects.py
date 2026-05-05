"""
Project Management API Routes (Issue #357: SEC-RBAC Phase 1.3)

Provides project CRUD endpoints with ownership validation:
- Create, read, update, delete projects
- Project filtering by owner
- User-isolated project access
"""

from typing import Any, Dict, Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.domain import models as domain
from services.shared_types import IntegrationType
from web.api.dependencies import get_project_integration_repository, get_project_repository

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])
logger = structlog.get_logger(__name__)


# Request/Response Models (SEC-RBAC Phase 3)


class ShareProjectRequest(BaseModel):
    """Request model for sharing a project with a user (SEC-RBAC Phase 3)"""

    user_id: str
    role: str = "viewer"  # Default to viewer (read-only) - can be viewer, editor, admin


class UpdateShareRoleRequest(BaseModel):
    """Request model for updating a user's role in a shared project"""

    role: str  # viewer, editor, admin


class CreateProjectRequest(BaseModel):
    """Request model for creating a project (Issue #468)"""

    name: str
    description: Optional[str] = None


class CreateIntegrationRequest(BaseModel):
    """Request model for creating a project integration (Issue #859)"""

    type: str  # IntegrationType value: "github", "jira", "linear", "slack"
    name: str
    config: Dict[str, Any]


class UpdateIntegrationRequest(BaseModel):
    """Request model for updating a project integration (Issue #859)"""

    name: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


@router.post("")
async def create_project(
    request: CreateProjectRequest,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
) -> dict:
    """
    Create a new project with ownership validation (SEC-RBAC).

    Args:
        request: CreateProjectRequest with name and optional description
        current_user: Current authenticated user
        project_repo: Project repository (injected)

    Returns:
        Created project with ID and metadata

    Raises:
        HTTPException 400: Invalid input
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    Issue #468: Accept JSON body instead of query params
    """
    try:
        if not request.name or not request.name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project name is required",
            )

        # Create project with ownership using kwargs (BaseRepository.create signature)
        created_project = await project_repo.create(
            name=request.name,
            description=request.description or "",
            owner_id=current_user.sub,
        )

        logger.info(
            "project_created",
            user_id=current_user.sub,
            project_id=created_project.id,
            name=request.name,
        )

        return {
            "id": created_project.id,
            "name": created_project.name,
            "description": created_project.description,
            "owner_id": created_project.owner_id,
            "created_at": (
                created_project.created_at.isoformat() if created_project.created_at else None
            ),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "project_create_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create project",
        )


@router.get("/{project_id}")
async def get_project(
    project_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
) -> dict:
    """
    Get project by ID with ownership validation (SEC-RBAC).

    Only returns project if current user is the owner.

    Args:
        project_id: Project ID to retrieve
        current_user: Current authenticated user
        project_repo: Project repository (injected)

    Returns:
        Project metadata (if owned by current user)

    Raises:
        HTTPException 404: Project not found or not owned by current user
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        project_obj = await project_repo.get_by_id(project_id, owner_id=current_user.sub)

        if not project_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project not found: {project_id}",
            )

        logger.info(
            "project_retrieved",
            user_id=current_user.sub,
            project_id=project_id,
        )

        return {
            "id": project_obj.id,
            "name": project_obj.name,
            "description": project_obj.description,
            "owner_id": project_obj.owner_id,
            "created_at": project_obj.created_at.isoformat() if project_obj.created_at else None,
            "updated_at": project_obj.updated_at.isoformat() if project_obj.updated_at else None,
            # MUX Lifecycle (#711) - include when present for UI indicator
            "lifecycle_state": (
                getattr(project_obj, "lifecycle_state", None).value
                if getattr(project_obj, "lifecycle_state", None)
                else None
            ),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "project_get_error",
            user_id=current_user.sub,
            project_id=project_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve project",
        )


@router.get("")
async def list_projects(
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
) -> dict:
    """
    List all projects owned by current user (SEC-RBAC).

    Issue #672: Now falls back to user preferences if projects table is empty,
    matching chat handler behavior for data source consistency.

    Returns:
        List of projects owned by current user

    Raises:
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    Issue #672: MUX-WIRE-PROJECTS-PAGE data consistency fix
    """
    try:
        # Primary source: projects table
        projects = await project_repo.list_active_projects(owner_id=current_user.sub)

        # Issue #672: Fallback to user preferences if projects table is empty
        # This matches chat handler behavior in canonical_handlers.py
        from_preferences = False
        if not projects:
            from uuid import UUID

            from services.user_context_service import user_context_service

            try:
                user_id = UUID(current_user.sub)
                user_context = await user_context_service.get_user_context(
                    session_id="web-projects-page",
                    user_id=user_id,
                )
                if user_context and user_context.projects:
                    # Convert preference-based projects to display format
                    # These don't have IDs since they're from preferences
                    from_preferences = True
                    projects = [
                        type(
                            "PreferenceProject",
                            (),
                            {
                                "id": f"pref-{i}",
                                "name": p if isinstance(p, str) else p,
                                "description": "From user preferences (not yet migrated to projects table)",
                                "owner_id": current_user.sub,
                                "created_at": None,
                            },
                        )()
                        for i, p in enumerate(user_context.projects)
                    ]
                    logger.info(
                        "projects_from_preferences",
                        user_id=current_user.sub,
                        count=len(projects),
                    )
            except Exception as fallback_error:
                logger.warning(
                    "projects_preferences_fallback_failed",
                    user_id=current_user.sub,
                    error=str(fallback_error),
                )

        logger.info(
            "projects_retrieved",
            user_id=current_user.sub,
            count=len(projects),
            from_preferences=from_preferences,
        )

        return {
            "projects": [
                {
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                    "owner_id": p.owner_id,
                    "created_at": p.created_at.isoformat() if p.created_at else None,
                    # MUX Lifecycle (#709) - include when present for UI indicator
                    # getattr handles PreferenceProject objects which lack this field
                    "lifecycle_state": (
                        getattr(p, "lifecycle_state", None).value
                        if getattr(p, "lifecycle_state", None)
                        else None
                    ),
                    # #869 Phase 3: status counts for the Settings → Projects
                    # overview list. ProjectRepository.list_active_projects
                    # already eagerly loads both collections via selectinload,
                    # so this is free. PreferenceProject lacks them — fall to 0.
                    "repo_count": len(getattr(p, "repositories", []) or []),
                    "integration_count": len(getattr(p, "integrations", []) or []),
                }
                for p in projects
            ],
            "count": len(projects),
            "source": "preferences" if from_preferences else "database",
        }

    except Exception as e:
        logger.error(
            "projects_get_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve projects",
        )


@router.get("/{project_id}/work-items")
async def get_project_work_items(
    project_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
) -> dict:
    """
    Get work items associated with a project (#711 MUX-PROJECT-DETAIL-VIEW).

    Returns work items where project_id matches, with lifecycle_state for MUX UI.

    Args:
        project_id: Project ID to get work items for
        current_user: Current authenticated user
        project_repo: Project repository (injected)

    Returns:
        List of work items with lifecycle_state

    Raises:
        HTTPException 404: Project not found or not owned by current user
        HTTPException 500: Server error
    """
    from sqlalchemy import select

    from services.database.models import WorkItem as WorkItemDB
    from services.database.session_factory import AsyncSessionFactory

    try:
        # First verify project exists and user owns it (SEC-RBAC)
        project_obj = await project_repo.get_by_id(project_id, owner_id=current_user.sub)

        if not project_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project not found: {project_id}",
            )

        # Query work items for this project
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(
                select(WorkItemDB).where(WorkItemDB.project_id == project_id)
            )
            db_work_items = result.scalars().all()

            # Convert to domain objects to get lifecycle_state mapping
            work_items = [wi.to_domain() for wi in db_work_items]

        logger.info(
            "project_work_items_retrieved",
            user_id=current_user.sub,
            project_id=project_id,
            count=len(work_items),
        )

        return {
            "work_items": [
                {
                    "id": w.id,
                    "title": w.title,
                    "description": w.description,
                    "type": w.type,
                    "status": w.status,
                    "priority": w.priority,
                    "assignee": w.assignee,
                    "created_at": w.created_at.isoformat() if w.created_at else None,
                    # MUX Lifecycle (#711) - include when present for UI indicator
                    "lifecycle_state": w.lifecycle_state.value if w.lifecycle_state else None,
                }
                for w in work_items
            ],
            "count": len(work_items),
            "project_id": project_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "project_work_items_error",
            user_id=current_user.sub,
            project_id=project_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve project work items",
        )


@router.put("/{project_id}")
async def update_project(
    project_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
) -> dict:
    """
    Update project with ownership validation (SEC-RBAC).

    Only allows updating if current user is the owner.

    Args:
        project_id: Project ID to update
        name: New project name (optional)
        description: New project description (optional)
        current_user: Current authenticated user
        project_repo: Project repository (injected)

    Returns:
        Updated project

    Raises:
        HTTPException 404: Project not found or not owned by current user
        HTTPException 400: Invalid input
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        # Verify ownership
        project_obj = await project_repo.get_by_id(project_id, owner_id=current_user.sub)

        if not project_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project not found: {project_id}",
            )

        # Build update kwargs
        update_kwargs = {}
        if name is not None:
            if not name.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Project name cannot be empty",
                )
            update_kwargs["name"] = name

        if description is not None:
            update_kwargs["description"] = description

        # Update using BaseRepository.update(id, **kwargs) signature
        updated = await project_repo.update(project_id, **update_kwargs)

        logger.info(
            "project_updated",
            user_id=current_user.sub,
            project_id=project_id,
        )

        return {
            "id": updated.id,
            "name": updated.name,
            "description": updated.description,
            "owner_id": updated.owner_id,
            "updated_at": updated.updated_at.isoformat() if updated.updated_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "project_update_error",
            user_id=current_user.sub,
            project_id=project_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update project",
        )


@router.delete("/{project_id}")
async def delete_project(
    project_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
) -> dict:
    """
    Delete project with ownership validation (SEC-RBAC).

    Only allows deleting if current user is the owner.

    Args:
        project_id: Project ID to delete
        current_user: Current authenticated user
        project_repo: Project repository (injected)

    Returns:
        Success message

    Raises:
        HTTPException 404: Project not found or not owned by current user
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        # Verify ownership before deleting
        project_obj = await project_repo.get_by_id(project_id, owner_id=current_user.sub)

        if not project_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project not found: {project_id}",
            )

        await project_repo.delete(project_id)

        logger.info(
            "project_deleted",
            user_id=current_user.sub,
            project_id=project_id,
        )

        return {
            "status": "deleted",
            "project_id": project_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "project_delete_error",
            user_id=current_user.sub,
            project_id=project_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete project",
        )


# Share/Unshare Endpoints (SEC-RBAC Phase 3)


@router.post("/{project_id}/share")
async def share_project(
    project_id: str,
    request: ShareProjectRequest,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
) -> dict:
    """
    Share a project with another user at specified role (SEC-RBAC Phase 3).

    Args:
        project_id: ID of project to share
        request: ShareProjectRequest with user_id and role
        current_user: Current authenticated user (must be project owner)
        project_repo: Project repository (injected)

    Returns:
        Updated project with shared_with information

    Raises:
        HTTPException 403: User is not the project owner
        HTTPException 404: Project not found
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 3 Endpoints
    """
    try:
        # Validate role
        valid_roles = ["viewer", "editor", "admin"]
        role = request.role.lower() if request.role else "viewer"
        if role not in valid_roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}",
            )

        # Convert string role to ShareRole enum
        share_role = domain.ShareRole(role)

        # Share the project
        updated_project = await project_repo.share_project(
            project_id=project_id,
            owner_id=current_user.sub,
            user_to_share_with=request.user_id,
            role=share_role,
        )

        if not updated_project:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be the project owner to share it",
            )

        logger.info(
            "project_shared",
            project_id=project_id,
            owner_id=current_user.sub,
            shared_with=request.user_id,
            role=role,
        )

        return {
            "status": "shared",
            "project_id": project_id,
            "shared_with": request.user_id,
            "role": role,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "project_share_error",
            project_id=project_id,
            owner_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to share project",
        )


@router.delete("/{project_id}/share/{user_id}")
async def unshare_project(
    project_id: str,
    user_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
) -> dict:
    """
    Remove user from project sharing (SEC-RBAC Phase 3).

    Args:
        project_id: ID of project
        user_id: User ID to remove from sharing
        current_user: Current authenticated user (must be project owner)
        project_repo: Project repository (injected)

    Returns:
        Status confirmation

    Raises:
        HTTPException 403: User is not the project owner
        HTTPException 404: Project not found or user not in shared_with
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 3 Endpoints
    """
    try:
        success = await project_repo.unshare_project(
            project_id=project_id, owner_id=current_user.sub, user_to_unshare=user_id
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be the project owner or user is not currently shared",
            )

        logger.info(
            "project_unshared",
            project_id=project_id,
            owner_id=current_user.sub,
            unshared_from=user_id,
        )

        return {
            "status": "unshared",
            "project_id": project_id,
            "removed_user": user_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "project_unshare_error",
            project_id=project_id,
            owner_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to unshare project",
        )


@router.put("/{project_id}/share/{user_id}")
async def update_project_share(
    project_id: str,
    user_id: str,
    request: UpdateShareRoleRequest,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
) -> dict:
    """
    Update user's sharing role for a project (SEC-RBAC Phase 3).

    Args:
        project_id: ID of project
        user_id: User ID to update
        request: UpdateShareRoleRequest with new role
        current_user: Current authenticated user (must be project owner)
        project_repo: Project repository (injected)

    Returns:
        Updated share information

    Raises:
        HTTPException 400: Invalid role
        HTTPException 403: User is not the project owner
        HTTPException 404: Project or user not found
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 3 Endpoints
    """
    try:
        # Validate role
        valid_roles = ["viewer", "editor", "admin"]
        role = request.role.lower() if request.role else "viewer"
        if role not in valid_roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}",
            )

        # Convert string role to ShareRole enum
        share_role = domain.ShareRole(role)

        # Update the role
        success = await project_repo.update_share_role(
            project_id=project_id,
            owner_id=current_user.sub,
            target_user_id=user_id,
            new_role=share_role,
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be the project owner or user is not currently shared",
            )

        logger.info(
            "project_share_role_updated",
            project_id=project_id,
            owner_id=current_user.sub,
            user_id=user_id,
            new_role=role,
        )

        return {
            "status": "role_updated",
            "project_id": project_id,
            "user_id": user_id,
            "new_role": role,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "project_share_role_error",
            project_id=project_id,
            owner_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update sharing role",
        )


@router.get("/{project_id}/my-role")
async def get_my_project_role(
    project_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
) -> dict:
    """
    Get current user's role for a project (SEC-RBAC Phase 3).

    Args:
        project_id: ID of project
        current_user: Current authenticated user
        project_repo: Project repository (injected)

    Returns:
        User's role (owner/admin/editor/viewer) or None if no access

    Issue #357: SEC-RBAC Phase 3 Endpoints
    """
    try:
        role = await project_repo.get_user_role(project_id=project_id, user_id=current_user.sub)

        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found or you do not have access",
            )

        logger.info(
            "get_project_role",
            project_id=project_id,
            user_id=current_user.sub,
            role=role.value,
        )

        return {
            "project_id": project_id,
            "user_id": current_user.sub,
            "role": role.value,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "get_project_role_error",
            project_id=project_id,
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get project role",
        )


# --- Project Repository Endpoints (Issue #866) ---


@router.get("/{project_id}/repositories")
async def list_project_repositories(
    project_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
) -> dict:
    """List repositories linked to a project."""
    project = await project_repo.get_by_id(project_id, owner_id=current_user.sub)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return {
        "project_id": project_id,
        "repositories": [repo.to_dict() for repo in project.repositories],
    }


# --- Project Integration Endpoints (Issue #859) ---


@router.get("/{project_id}/integrations")
async def list_project_integrations(
    project_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
    integration_repo=Depends(get_project_integration_repository),
) -> dict:
    """
    List all integrations for a project.

    Issue #859: Project integration CRUD API.
    """
    try:
        project = await project_repo.get_by_id(project_id, owner_id=current_user.sub)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project not found: {project_id}",
            )

        integrations = await integration_repo.list_by_project(
            project_id=project_id, owner_id=current_user.sub
        )

        logger.info(
            "list_project_integrations",
            user_id=current_user.sub,
            project_id=project_id,
            count=len(integrations),
        )

        return {
            "project_id": project_id,
            "integrations": [
                {
                    "id": i.id,
                    "type": i.type.value,
                    "name": i.name,
                    "config": i.config,
                    "is_active": i.is_active,
                    "created_at": i.created_at.isoformat() if i.created_at else None,
                }
                for i in integrations
            ],
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "list_integrations_error",
            user_id=current_user.sub,
            project_id=project_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list integrations",
        )


@router.post("/{project_id}/integrations", status_code=status.HTTP_201_CREATED)
async def create_project_integration(
    project_id: str,
    request: CreateIntegrationRequest,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
    integration_repo=Depends(get_project_integration_repository),
) -> dict:
    """
    Create a new integration for a project.

    Validates integration type and config before creating.

    Issue #859: Project integration CRUD API.
    """
    try:
        project = await project_repo.get_by_id(project_id, owner_id=current_user.sub)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project not found: {project_id}",
            )

        # Validate integration type
        try:
            integration_type = IntegrationType(request.type)
        except ValueError:
            valid_types = [t.value for t in IntegrationType]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid integration type '{request.type}'. Valid types: {valid_types}",
            )

        # Validate config using domain model
        integration = domain.ProjectIntegration(
            type=integration_type,
            name=request.name,
            config=request.config,
            project_id=project_id,
        )
        if not integration.validate_config():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid config for {integration_type.value} integration",
            )

        # Check for duplicate type
        existing = await integration_repo.get_by_project_and_type(
            project_id=project_id,
            integration_type=integration_type,
            owner_id=current_user.sub,
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Integration of type '{integration_type.value}' already exists for this project",
            )

        created = await integration_repo.create(
            id=integration.id,
            project_id=project_id,
            type=integration_type,
            name=request.name,
            config=request.config,
        )

        logger.info(
            "integration_created",
            user_id=current_user.sub,
            project_id=project_id,
            integration_id=created.id,
            type=integration_type.value,
        )

        return {
            "id": created.id,
            "project_id": project_id,
            "type": integration_type.value,
            "name": request.name,
            "config": request.config,
            "is_active": True,
            "created_at": created.created_at.isoformat() if created.created_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "create_integration_error",
            user_id=current_user.sub,
            project_id=project_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create integration",
        )


@router.get("/{project_id}/integrations/{integration_id}")
async def get_project_integration(
    project_id: str,
    integration_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
    integration_repo=Depends(get_project_integration_repository),
) -> dict:
    """
    Get a specific integration for a project.

    Issue #859: Project integration CRUD API.
    """
    try:
        project = await project_repo.get_by_id(project_id, owner_id=current_user.sub)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project not found: {project_id}",
            )

        db_integration = await integration_repo.get_by_id(integration_id)
        if not db_integration or db_integration.project_id != project_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Integration not found: {integration_id}",
            )

        integration = db_integration.to_domain()

        logger.info(
            "integration_retrieved",
            user_id=current_user.sub,
            project_id=project_id,
            integration_id=integration_id,
        )

        return {
            "id": integration.id,
            "project_id": project_id,
            "type": integration.type.value,
            "name": integration.name,
            "config": integration.config,
            "is_active": integration.is_active,
            "created_at": integration.created_at.isoformat() if integration.created_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "get_integration_error",
            user_id=current_user.sub,
            project_id=project_id,
            integration_id=integration_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve integration",
        )


@router.put("/{project_id}/integrations/{integration_id}")
async def update_project_integration(
    project_id: str,
    integration_id: str,
    request: UpdateIntegrationRequest,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
    integration_repo=Depends(get_project_integration_repository),
) -> dict:
    """
    Update an integration for a project.

    Issue #859: Project integration CRUD API.
    """
    try:
        project = await project_repo.get_by_id(project_id, owner_id=current_user.sub)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project not found: {project_id}",
            )

        db_integration = await integration_repo.get_by_id(integration_id)
        if not db_integration or db_integration.project_id != project_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Integration not found: {integration_id}",
            )

        # Build update kwargs
        update_kwargs = {}
        if request.name is not None:
            update_kwargs["name"] = request.name
        if request.config is not None:
            # Validate new config against integration type
            test_integration = domain.ProjectIntegration(
                type=db_integration.type,
                config=request.config,
            )
            if not test_integration.validate_config():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid config for {db_integration.type.value} integration",
                )
            update_kwargs["config"] = request.config
        if request.is_active is not None:
            update_kwargs["is_active"] = request.is_active

        if not update_kwargs:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update",
            )

        updated = await integration_repo.update(integration_id, **update_kwargs)

        logger.info(
            "integration_updated",
            user_id=current_user.sub,
            project_id=project_id,
            integration_id=integration_id,
            fields=list(update_kwargs.keys()),
        )

        return {
            "id": updated.id,
            "project_id": project_id,
            "type": updated.type.value,
            "name": updated.name,
            "config": updated.config,
            "is_active": updated.is_active,
            "created_at": updated.created_at.isoformat() if updated.created_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "update_integration_error",
            user_id=current_user.sub,
            project_id=project_id,
            integration_id=integration_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update integration",
        )


@router.delete("/{project_id}/integrations/{integration_id}")
async def delete_project_integration(
    project_id: str,
    integration_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    project_repo=Depends(get_project_repository),
    integration_repo=Depends(get_project_integration_repository),
) -> dict:
    """
    Delete an integration from a project.

    Issue #859: Project integration CRUD API.
    """
    try:
        project = await project_repo.get_by_id(project_id, owner_id=current_user.sub)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project not found: {project_id}",
            )

        db_integration = await integration_repo.get_by_id(integration_id)
        if not db_integration or db_integration.project_id != project_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Integration not found: {integration_id}",
            )

        await integration_repo.delete(integration_id)

        logger.info(
            "integration_deleted",
            user_id=current_user.sub,
            project_id=project_id,
            integration_id=integration_id,
        )

        return {"deleted": True, "integration_id": integration_id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "delete_integration_error",
            user_id=current_user.sub,
            project_id=project_id,
            integration_id=integration_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete integration",
        )
