"""
Work Items API Routes (Issue #710: MUX-WORKITEMS-VIEW)

Provides work item CRUD endpoints with lifecycle state support.
Following the pattern established by projects.py and todos.py.
"""

from typing import Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from services.api.errors import UserFacingHTTPException
from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.database.repositories import WorkItemRepository
from web.api.dependencies import get_work_item_repository


class CreateWorkItemRequest(BaseModel):
    """Request model for creating a work item"""

    title: str
    description: Optional[str] = None
    type: str = "task"  # bug, feature, task, improvement
    status: str = "open"
    priority: str = "medium"  # low, medium, high, critical
    project_id: Optional[str] = None


router = APIRouter(prefix="/api/v1/work-items", tags=["work-items"])
logger = structlog.get_logger(__name__)

# Issue 2432 (CXO, comment 7144095698): reworded, marked.
WORK_ITEM_TITLE_NEEDED_LINE = "Give the work item a title first."


@router.get("")
async def list_work_items(
    current_user: JWTClaims = Depends(get_current_user),
    work_item_repo: WorkItemRepository = Depends(get_work_item_repository),
) -> dict:
    """
    List all work items.

    Returns work items with lifecycle_state for MUX UI indicators (#710).

    Note: Currently returns all work items. Future enhancement could filter
    by owner/project when ownership model is established.

    Returns:
        List of work items with metadata and lifecycle state

    Raises:
        HTTPException 500: Server error
    """
    try:
        # Get all work items (BaseRepository.list returns DB objects)
        db_work_items = await work_item_repo.list(limit=100)

        # Convert to domain objects to get lifecycle_state mapping
        work_items = [wi.to_domain() for wi in db_work_items]

        logger.info(
            "work_items_retrieved",
            user_id=current_user.sub,
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
                    "labels": w.labels,
                    "assignee": w.assignee,
                    "project_id": w.project_id,
                    "source_system": w.source_system,
                    "external_id": w.external_id,
                    "external_url": w.external_url,
                    "created_at": w.created_at.isoformat() if w.created_at else None,
                    # MUX Lifecycle (#710) - include when present for UI indicator
                    "lifecycle_state": w.lifecycle_state.value if w.lifecycle_state else None,
                }
                for w in work_items
            ],
            "count": len(work_items),
        }

    except Exception as e:
        logger.error(
            "work_items_get_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve work items",
        )


@router.post("")
async def create_work_item(
    request: CreateWorkItemRequest,
    current_user: JWTClaims = Depends(get_current_user),
    work_item_repo: WorkItemRepository = Depends(get_work_item_repository),
) -> dict:
    """
    Create a new work item.

    Args:
        request: CreateWorkItemRequest with title, type, status, priority
        current_user: Current authenticated user
        work_item_repo: Work item repository (injected)

    Returns:
        Created work item with ID

    Raises:
        HTTPException 400: Invalid input
        HTTPException 500: Server error
    """
    try:
        if not request.title or not request.title.strip():
            raise UserFacingHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=WORK_ITEM_TITLE_NEEDED_LINE
            )

        # Create work item using BaseRepository.create
        created_item = await work_item_repo.create(
            title=request.title.strip(),
            description=request.description or "",
            type=request.type,
            status=request.status,
            priority=request.priority,
            project_id=request.project_id,
        )

        logger.info(
            "work_item_created",
            user_id=current_user.sub,
            work_item_id=created_item.id,
            title=request.title,
        )

        return {
            "id": created_item.id,
            "title": created_item.title,
            "description": created_item.description,
            "type": created_item.type,
            "status": created_item.status,
            "priority": created_item.priority,
            "project_id": created_item.project_id,
            "created_at": created_item.created_at.isoformat() if created_item.created_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "work_item_create_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create work item",
        )
