"""
API routes for Repository CRUD and Project-Repository linking.

Issue #866: Repository as first-class domain entity with M2M Project relationship.
"""

from typing import Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import update as sa_update

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.database.models import RepositoryDB
from services.domain import models as domain
from services.infrastructure.github_repo_validator import (
    apply_validation_metadata,
    validate_github_repo_for_account,
)
from web.api.dependencies import get_project_repository, get_repository_repository

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v1/repositories", tags=["repositories"])

VALID_PROVIDERS = {"github", "gitlab", "bitbucket"}


# -- Pydantic models --


class CreateRepositoryRequest(BaseModel):
    provider: str = "github"
    full_name: str  # "owner/repo"
    display_name: Optional[str] = None
    url: Optional[str] = None


class LinkRepositoryRequest(BaseModel):
    is_primary: bool = False


# -- Repository CRUD --


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_repository(
    req: CreateRepositoryRequest,
    current_user: JWTClaims = Depends(get_current_user),
    repo_repo=Depends(get_repository_repository),
):
    """Register a new code repository for the current user."""
    # Validate provider
    if req.provider not in VALID_PROVIDERS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid provider '{req.provider}'. Must be one of: {', '.join(sorted(VALID_PROVIDERS))}",
        )

    # Validate full_name format
    full_name = req.full_name.strip()
    if "/" not in full_name:
        raise HTTPException(
            status_code=400,
            detail="Repository full_name must be in owner/repo format",
        )

    # Check for duplicate
    existing = await repo_repo.get_by_full_name(
        full_name=full_name, provider=req.provider, owner_id=current_user.sub
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Repository '{full_name}' ({req.provider}) already registered",
        )

    # Derive display_name and url
    display_name = req.display_name or full_name.split("/")[-1]
    url = req.url or ""
    if not url and req.provider == "github":
        url = f"https://github.com/{full_name}"

    # Issue #867: Soft-validate via GitHub API (GitHub provider only)
    validation_warning = None
    if req.provider == "github":
        validation = await validate_github_repo_for_account(full_name, current_user.sub)
        if validation.validated and not validation.exists:
            validation_warning = validation.error
            logger.warning(
                "repo_api_validation_warning", full_name=full_name, error=validation.error
            )

    repo = domain.Repository(
        owner_id=current_user.sub,
        provider=req.provider,
        full_name=full_name,
        display_name=display_name,
        url=url,
    )
    if req.provider == "github":
        apply_validation_metadata(repo, validation)

    created = await repo_repo.create_repository(repo)
    result = created.to_dict()
    if validation_warning:
        result["validation_warning"] = validation_warning
    return result


@router.get("")
async def list_repositories(
    provider: Optional[str] = None,
    current_user: JWTClaims = Depends(get_current_user),
    repo_repo=Depends(get_repository_repository),
):
    """List the current user's registered repositories."""
    repos = await repo_repo.list_by_owner(owner_id=current_user.sub, provider=provider)
    return {"repositories": [r.to_dict() for r in repos]}


@router.get("/{repo_id}")
async def get_repository(
    repo_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    repo_repo=Depends(get_repository_repository),
):
    """Get a single repository by ID."""
    repo = await repo_repo.get_by_id(repo_id, owner_id=current_user.sub)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    return repo.to_dict()


@router.delete("/{repo_id}")
async def deactivate_repository(
    repo_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    repo_repo=Depends(get_repository_repository),
):
    """Deactivate a repository (soft delete)."""
    repo = await repo_repo.get_by_id(repo_id, owner_id=current_user.sub)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    await repo_repo.session.execute(
        sa_update(RepositoryDB).where(RepositoryDB.id == repo_id).values(is_active=False)
    )
    await repo_repo.session.flush()

    return {"message": f"Repository '{repo.full_name}' deactivated"}


# -- Project-Repository linking --


@router.post("/{repo_id}/projects/{project_id}", status_code=status.HTTP_201_CREATED)
async def link_repository_to_project(
    repo_id: str,
    project_id: str,
    req: LinkRepositoryRequest = LinkRepositoryRequest(),
    current_user: JWTClaims = Depends(get_current_user),
    repo_repo=Depends(get_repository_repository),
    project_repo=Depends(get_project_repository),
):
    """Link a repository to a project."""
    # Verify repository exists and belongs to user
    repo = await repo_repo.get_by_id(repo_id, owner_id=current_user.sub)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    # Verify project exists and belongs to user
    project = await project_repo.get_by_id(project_id, owner_id=current_user.sub)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check for existing link
    existing_links = await repo_repo.get_project_links(repo_id)
    for link in existing_links:
        if link.project_id == project_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Repository already linked to this project",
            )

    link = await repo_repo.link_to_project(
        repository_id=repo_id,
        project_id=project_id,
        linked_by=current_user.sub,
        is_primary=req.is_primary,
    )
    return link.to_dict()


@router.delete("/{repo_id}/projects/{project_id}")
async def unlink_repository_from_project(
    repo_id: str,
    project_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    repo_repo=Depends(get_repository_repository),
    project_repo=Depends(get_project_repository),
):
    """Unlink a repository from a project."""
    # Verify repository exists and belongs to user
    repo = await repo_repo.get_by_id(repo_id, owner_id=current_user.sub)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    # Verify project exists and belongs to user
    project = await project_repo.get_by_id(project_id, owner_id=current_user.sub)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    removed = await repo_repo.unlink_from_project(repo_id, project_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Link not found")

    return {"message": f"Repository '{repo.full_name}' unlinked from project '{project.name}'"}


@router.get("/{repo_id}/projects")
async def list_projects_for_repository(
    repo_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    repo_repo=Depends(get_repository_repository),
    project_repo=Depends(get_project_repository),
):
    """List all projects linked to a repository."""
    # Verify repository exists and belongs to user
    repo = await repo_repo.get_by_id(repo_id, owner_id=current_user.sub)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    links = await repo_repo.get_project_links(repo_id)
    projects = []
    for link in links:
        project = await project_repo.get_by_id(link.project_id, owner_id=current_user.sub)
        if project:
            projects.append(
                {
                    "project_id": project.id,
                    "project_name": project.name,
                    "is_primary": link.is_primary,
                    "linked_at": link.linked_at.isoformat(),
                }
            )

    return {"repository_id": repo_id, "projects": projects}
