"""
List Management API Routes (Issue #357: SEC-RBAC Phase 1.3)

Provides list CRUD endpoints with ownership validation:
- Create, read, update, delete lists
- List filtering by owner
- User-isolated list access
"""

from typing import List, Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.database.models import ItemDB, ListDB
from services.database.session_factory import AsyncSessionFactory
from services.domain import models as domain
from services.domain.primitives import Item
from web.api.dependencies import get_list_repository

router = APIRouter(prefix="/api/v1/lists", tags=["lists"])
logger = structlog.get_logger(__name__)


# Pydantic models for sharing operations
class ShareListRequest(BaseModel):
    """Request model for sharing a list with a user (SEC-RBAC Phase 2)"""

    user_id: str
    role: str = "viewer"  # Default to viewer (read-only) - can be viewer, editor, admin


class SharePermissionResponse(BaseModel):
    """Response model for individual share permissions"""

    user_id: str
    role: str


class ShareListResponse(BaseModel):
    """Response model for sharing operations (SEC-RBAC Phase 2)"""

    id: str
    name: str
    owner_id: str
    shared_with: List[SharePermissionResponse]
    message: str


class UpdateRoleRequest(BaseModel):
    """Request model for updating a user's role (SEC-RBAC Phase 2)"""

    role: str  # viewer, editor, admin


class UserRoleResponse(BaseModel):
    """Response model for user's role on a resource (SEC-RBAC Phase 2)"""

    role: str  # owner, admin, editor, viewer, or null
    message: str


class SharedListsResponse(BaseModel):
    """Response model for shared lists"""

    lists: List[dict]
    count: int


class CreateListRequest(BaseModel):
    """Request model for creating a list (Issue #468)"""

    name: str
    description: Optional[str] = None


@router.post("")
async def create_list(
    request: CreateListRequest,
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> dict:
    """
    Create a new list with ownership validation (SEC-RBAC).

    Args:
        request: CreateListRequest with name and optional description
        current_user: Current authenticated user
        list_repo: List repository (injected)

    Returns:
        Created list with ID and metadata

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
                detail="List name is required",
            )

        # Create list with ownership
        new_list = domain.List(
            name=request.name,
            description=request.description or "",
            owner_id=current_user.sub,
        )

        created_list = await list_repo.create_list(new_list)

        logger.info(
            "list_created",
            user_id=current_user.sub,
            list_id=created_list.id,
            name=request.name,
        )

        return {
            "id": created_list.id,
            "name": created_list.name,
            "description": created_list.description,
            "owner_id": created_list.owner_id,
            "created_at": created_list.created_at.isoformat() if created_list.created_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "list_create_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create list",
        )


@router.get("/{list_id}")
async def get_list(
    list_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> dict:
    """
    Get list by ID with ownership validation (SEC-RBAC).

    Only returns list if current user is the owner.

    Args:
        list_id: List ID to retrieve
        current_user: Current authenticated user
        list_repo: List repository (injected)

    Returns:
        List metadata (if owned by current user)

    Raises:
        HTTPException 404: List not found or not owned by current user
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        list_obj = await list_repo.get_list_by_id(list_id, owner_id=current_user.sub)

        if not list_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"List not found: {list_id}",
            )

        logger.info(
            "list_retrieved",
            user_id=current_user.sub,
            list_id=list_id,
        )

        return {
            "id": list_obj.id,
            "name": list_obj.name,
            "description": list_obj.description,
            "owner_id": list_obj.owner_id,
            "created_at": list_obj.created_at.isoformat() if list_obj.created_at else None,
            "updated_at": list_obj.updated_at.isoformat() if list_obj.updated_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "list_get_error",
            user_id=current_user.sub,
            list_id=list_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve list",
        )


@router.get("")
async def list_lists(
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> dict:
    """
    List all lists owned by current user (SEC-RBAC).

    Returns:
        List of lists owned by current user

    Raises:
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        lists = await list_repo.get_lists_by_owner(current_user.sub)

        # #714: compute staleness per list. Per-list aggregate query is
        # acceptable at alpha scale; Post-MVP optimization is denormalizing
        # `last_item_activity_at` on ListDB and updating it on item-add.
        from services.lists.staleness import compute_staleness

        list_payloads = []
        for list_item in lists:
            max_item_ts = await list_repo.get_max_item_added_at(list_item.id)
            item_ts_values = [max_item_ts] if max_item_ts is not None else []
            staleness = compute_staleness(
                list_updated_at=list_item.updated_at,
                item_added_at_values=item_ts_values,
            )
            list_payloads.append(
                {
                    "id": list_item.id,
                    "name": list_item.name,
                    "description": list_item.description,
                    "owner_id": list_item.owner_id,
                    "created_at": (
                        list_item.created_at.isoformat() if list_item.created_at else None
                    ),
                    "updated_at": (
                        list_item.updated_at.isoformat() if list_item.updated_at else None
                    ),
                    "staleness": staleness.to_dict(),
                }
            )

        logger.info(
            "lists_retrieved",
            user_id=current_user.sub,
            count=len(lists),
            stale_count=sum(1 for p in list_payloads if p["staleness"]["is_stale"]),
        )

        return {
            "lists": list_payloads,
            "count": len(lists),
        }

    except Exception as e:
        logger.error(
            "lists_get_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve lists",
        )


@router.put("/{list_id}")
async def update_list(
    list_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> dict:
    """
    Update list with ownership validation (SEC-RBAC).

    Only allows updating if current user is the owner.

    Args:
        list_id: List ID to update
        name: New list name (optional)
        description: New list description (optional)
        current_user: Current authenticated user
        list_repo: List repository (injected)

    Returns:
        Updated list

    Raises:
        HTTPException 404: List not found or not owned by current user
        HTTPException 400: Invalid input
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        # Verify ownership
        list_obj = await list_repo.get_list_by_id(list_id, owner_id=current_user.sub)

        if not list_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"List not found: {list_id}",
            )

        # Update fields
        if name is not None:
            if not name.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="List name cannot be empty",
                )
            list_obj.name = name

        if description is not None:
            list_obj.description = description

        updated = await list_repo.update_list(list_obj)

        logger.info(
            "list_updated",
            user_id=current_user.sub,
            list_id=list_id,
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
            "list_update_error",
            user_id=current_user.sub,
            list_id=list_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update list",
        )


@router.delete("/{list_id}")
async def delete_list(
    list_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> dict:
    """
    Delete list with ownership validation (SEC-RBAC).

    Only allows deleting if current user is the owner.

    Args:
        list_id: List ID to delete
        current_user: Current authenticated user
        list_repo: List repository (injected)

    Returns:
        Success message

    Raises:
        HTTPException 404: List not found or not owned by current user
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        # Verify ownership before deleting
        list_obj = await list_repo.get_list_by_id(list_id, owner_id=current_user.sub)

        if not list_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"List not found: {list_id}",
            )

        await list_repo.delete_list(list_id, owner_id=current_user.sub)

        logger.info(
            "list_deleted",
            user_id=current_user.sub,
            list_id=list_id,
        )

        return {
            "status": "deleted",
            "list_id": list_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "list_delete_error",
            user_id=current_user.sub,
            list_id=list_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete list",
        )


@router.post("/{list_id}/share")
async def share_list(
    list_id: str,
    request: ShareListRequest,
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> ShareListResponse:
    """
    Share a list with another user at specified role (owner only - SEC-RBAC Phase 2).

    Owner explicitly specifies role when sharing:
    - viewer: Read-only access
    - editor: Can modify content
    - admin: Can share with others (but not delete)

    Args:
        list_id: ID of the list to share
        request: ShareListRequest with user_id and role
        current_user: Current authenticated user (must be owner)
        list_repo: List repository (injected)

    Returns:
        Updated list with shared_with array of {user_id, role} objects

    Raises:
        HTTPException 400: Invalid user_id or role
        HTTPException 404: List not found or user not owner
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 2 Role-Based Permissions
    """
    try:
        if not request.user_id or not request.user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user_id is required",
            )

        # Validate role
        valid_roles = ["viewer", "editor", "admin"]
        if request.role not in valid_roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"role must be one of {valid_roles}",
            )

        # Convert string role to ShareRole enum
        share_role = domain.ShareRole(request.role)

        # Share list (owner-only operation)
        shared_list = await list_repo.share_list(
            list_id, current_user.sub, request.user_id, share_role
        )

        if not shared_list:
            logger.warning(
                "list_share_unauthorized",
                user_id=current_user.sub,
                list_id=list_id,
                target_user=request.user_id,
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="List not found or you don't have permission to share it",
            )

        logger.info(
            "list_shared",
            owner_id=current_user.sub,
            list_id=list_id,
            shared_with_user=request.user_id,
            role=request.role,
        )

        # Convert shared_with SharePermission objects to response format
        shared_with_response = [
            SharePermissionResponse(user_id=perm.user_id, role=perm.role.value)
            for perm in shared_list.shared_with
        ]

        return ShareListResponse(
            id=shared_list.id,
            name=shared_list.name,
            owner_id=shared_list.owner_id,
            shared_with=shared_with_response,
            message=f"List shared with user {request.user_id} as {request.role}",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "list_share_error",
            user_id=current_user.sub,
            list_id=list_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to share list",
        )


@router.delete("/{list_id}/share/{user_id}")
async def unshare_list(
    list_id: str,
    user_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> dict:
    """
    Remove sharing access from a list (owner only - SEC-RBAC Phase 1.4).

    Revokes read access for the specified user.

    Args:
        list_id: ID of the list to unshare
        user_id: ID of user to remove from shared_with
        current_user: Current authenticated user (must be owner)
        list_repo: List repository (injected)

    Returns:
        Success status

    Raises:
        HTTPException 404: List not found or user not owner
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.4 Shared Resource Access
    """
    try:
        # Unshare list (owner-only operation)
        unshared_list = await list_repo.unshare_list(list_id, current_user.sub, user_id)

        if not unshared_list:
            logger.warning(
                "list_unshare_unauthorized",
                user_id=current_user.sub,
                list_id=list_id,
                unshare_from_user=user_id,
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="List not found or you don't have permission to unshare it",
            )

        logger.info(
            "list_unshared",
            owner_id=current_user.sub,
            list_id=list_id,
            unshared_from_user=user_id,
        )

        return {
            "success": True,
            "message": f"User {user_id} no longer has access to this list",
            "list_id": list_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "list_unshare_error",
            user_id=current_user.sub,
            list_id=list_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to unshare list",
        )


@router.put("/{list_id}/share/{user_id}")
async def update_share_role(
    list_id: str,
    user_id: str,
    request: UpdateRoleRequest,
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> dict:
    """
    Update a user's role for a shared list (owner only - SEC-RBAC Phase 2).

    Changes the role of an already-shared user (viewer, editor, admin).

    Args:
        list_id: ID of the list
        user_id: ID of user whose role to update
        request: UpdateRoleRequest with new role
        current_user: Current authenticated user (must be owner)
        list_repo: List repository (injected)

    Returns:
        Success status with updated role

    Raises:
        HTTPException 400: Invalid role
        HTTPException 404: List not found or user not owner or user not shared with
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 2 Role-Based Permissions
    """
    try:
        # Validate role
        valid_roles = ["viewer", "editor", "admin"]
        if request.role not in valid_roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"role must be one of {valid_roles}",
            )

        # Convert string role to ShareRole enum
        share_role = domain.ShareRole(request.role)

        # Update role
        success = await list_repo.update_share_role(list_id, current_user.sub, user_id, share_role)

        if not success:
            logger.warning(
                "list_update_role_failed",
                user_id=current_user.sub,
                list_id=list_id,
                target_user=user_id,
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="List not found, you don't have permission, or user is not shared with this list",
            )

        logger.info(
            "list_share_role_updated",
            owner_id=current_user.sub,
            list_id=list_id,
            target_user=user_id,
            new_role=request.role,
        )

        return {
            "success": True,
            "message": f"Updated user {user_id} role to {request.role}",
            "list_id": list_id,
            "user_id": user_id,
            "role": request.role,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "list_update_role_error",
            user_id=current_user.sub,
            list_id=list_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update share role",
        )


@router.get("/{list_id}/my-role")
async def get_my_role(
    list_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> UserRoleResponse:
    """
    Get current user's role for a list (SEC-RBAC Phase 2).

    Returns the role of the current user for the specified list:
    - 'owner': User owns the list
    - 'admin': User can share and modify
    - 'editor': User can modify content
    - 'viewer': User can read only
    - None: User has no access (404)

    Args:
        list_id: ID of the list
        current_user: Current authenticated user
        list_repo: List repository (injected)

    Returns:
        Current user's role for the list

    Raises:
        HTTPException 404: List not found or user has no access
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 2 Role-Based Permissions
    """
    try:
        # Get user's role
        role = await list_repo.get_user_role(list_id, current_user.sub)

        if not role:
            logger.info(
                "list_no_access",
                user_id=current_user.sub,
                list_id=list_id,
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="List not found or you don't have access to it",
            )

        logger.info(
            "list_role_retrieved",
            user_id=current_user.sub,
            list_id=list_id,
            role=role,
        )

        return UserRoleResponse(role=role, message=f"You have {role} access to this list")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "list_get_role_error",
            user_id=current_user.sub,
            list_id=list_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user role",
        )


@router.get("/shared-with-me")
async def get_shared_lists(
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> SharedListsResponse:
    """
    Get lists shared with the current user (SEC-RBAC Phase 1.4).

    Returns all lists where the current user is in the shared_with array.
    Does not include lists owned by the current user (see GET / for owned lists).

    Args:
        current_user: Current authenticated user
        list_repo: List repository (injected)

    Returns:
        List of lists shared with this user

    Raises:
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.4 Shared Resource Access
    """
    try:
        shared_lists = await list_repo.get_lists_shared_with_me(current_user.sub)

        logger.info(
            "shared_lists_retrieved",
            user_id=current_user.sub,
            count=len(shared_lists),
        )

        return SharedListsResponse(
            lists=[
                {
                    "id": shared_list.id,
                    "name": shared_list.name,
                    "description": shared_list.description,
                    "owner_id": shared_list.owner_id,
                    "created_at": (
                        shared_list.created_at.isoformat() if shared_list.created_at else None
                    ),
                }
                for shared_list in shared_lists
            ],
            count=len(shared_lists),
        )

    except Exception as e:
        logger.error(
            "shared_lists_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve shared lists",
        )


# =============================================================================
# Item Management Endpoints (Issue #474: MUX-TECH-LISTS)
# =============================================================================


class CreateItemRequest(BaseModel):
    """Request model for creating an item in a list"""

    text: str


class UpdateItemRequest(BaseModel):
    """Request model for updating an item"""

    text: str


class ItemResponse(BaseModel):
    """Response model for item data"""

    id: str
    text: str
    position: int
    list_id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@router.post("/{list_id}/items")
async def add_item_to_list(
    list_id: str,
    request: CreateItemRequest,
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> ItemResponse:
    """
    Add an item to a list with ownership validation.

    Only allows adding items to lists owned by the current user.

    Args:
        list_id: ID of the list to add item to
        request: CreateItemRequest with item text
        current_user: Current authenticated user
        list_repo: List repository (injected)

    Returns:
        Created item with ID and metadata

    Raises:
        HTTPException 400: Invalid input
        HTTPException 404: List not found or not owned by user
        HTTPException 500: Server error

    Issue #474: MUX-TECH-LISTS Item Management
    """
    try:
        if not request.text or not request.text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item text is required",
            )

        # Verify list ownership
        list_obj = await list_repo.get_list_by_id(list_id, owner_id=current_user.sub)
        if not list_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"List not found: {list_id}",
            )

        # Get max position for new item
        async with AsyncSessionFactory.session_scope_fresh() as session:
            from sqlalchemy import func

            max_pos_result = await session.execute(
                select(func.max(ItemDB.position)).where(ItemDB.list_id == list_id)
            )
            max_position = max_pos_result.scalar() or -1
            new_position = max_position + 1

            # Create domain item
            item = Item(
                text=request.text.strip(),
                position=new_position,
                list_id=list_id,
            )

            # Save to database
            db_item = ItemDB.from_domain(item)
            session.add(db_item)
            await session.commit()
            await session.refresh(db_item)

            logger.info(
                "item_added_to_list",
                user_id=current_user.sub,
                list_id=list_id,
                item_id=db_item.id,
            )

            return ItemResponse(
                id=db_item.id,
                text=db_item.text,
                position=db_item.position,
                list_id=db_item.list_id,
                created_at=db_item.created_at.isoformat() if db_item.created_at else None,
                updated_at=db_item.updated_at.isoformat() if db_item.updated_at else None,
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "item_add_error",
            user_id=current_user.sub,
            list_id=list_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add item to list",
        )


@router.get("/{list_id}/items")
async def get_items_in_list(
    list_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> dict:
    """
    Get all items in a list with ownership validation.

    Only returns items for lists owned by the current user.

    Args:
        list_id: ID of the list
        current_user: Current authenticated user
        list_repo: List repository (injected)

    Returns:
        List of items in the list

    Raises:
        HTTPException 404: List not found or not owned by user
        HTTPException 500: Server error

    Issue #474: MUX-TECH-LISTS Item Management
    """
    try:
        # Verify list ownership
        list_obj = await list_repo.get_list_by_id(list_id, owner_id=current_user.sub)
        if not list_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"List not found: {list_id}",
            )

        # Get items
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(
                select(ItemDB).where(ItemDB.list_id == list_id).order_by(ItemDB.position.asc())
            )
            db_items = result.scalars().all()

            logger.info(
                "items_retrieved",
                user_id=current_user.sub,
                list_id=list_id,
                count=len(db_items),
            )

            return {
                "items": [
                    {
                        "id": item.id,
                        "text": item.text,
                        "position": item.position,
                        "list_id": item.list_id,
                        "created_at": item.created_at.isoformat() if item.created_at else None,
                        "updated_at": item.updated_at.isoformat() if item.updated_at else None,
                    }
                    for item in db_items
                ],
                "count": len(db_items),
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "items_get_error",
            user_id=current_user.sub,
            list_id=list_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve items",
        )


@router.put("/{list_id}/items/{item_id}")
async def update_item(
    list_id: str,
    item_id: str,
    request: UpdateItemRequest,
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> ItemResponse:
    """
    Update an item in a list with ownership validation.

    Only allows updating items in lists owned by the current user.

    Args:
        list_id: ID of the list containing the item
        item_id: ID of the item to update
        request: UpdateItemRequest with new text
        current_user: Current authenticated user
        list_repo: List repository (injected)

    Returns:
        Updated item

    Raises:
        HTTPException 400: Invalid input
        HTTPException 404: List or item not found
        HTTPException 500: Server error

    Issue #474: MUX-TECH-LISTS Item Management
    """
    try:
        if not request.text or not request.text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item text is required",
            )

        # Verify list ownership
        list_obj = await list_repo.get_list_by_id(list_id, owner_id=current_user.sub)
        if not list_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"List not found: {list_id}",
            )

        # Update item
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(
                select(ItemDB).where(
                    ItemDB.id == item_id,
                    ItemDB.list_id == list_id,
                )
            )
            db_item = result.scalar_one_or_none()

            if not db_item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Item not found: {item_id}",
                )

            db_item.text = request.text.strip()
            await session.commit()
            await session.refresh(db_item)

            logger.info(
                "item_updated",
                user_id=current_user.sub,
                list_id=list_id,
                item_id=item_id,
            )

            return ItemResponse(
                id=db_item.id,
                text=db_item.text,
                position=db_item.position,
                list_id=db_item.list_id,
                created_at=db_item.created_at.isoformat() if db_item.created_at else None,
                updated_at=db_item.updated_at.isoformat() if db_item.updated_at else None,
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "item_update_error",
            user_id=current_user.sub,
            list_id=list_id,
            item_id=item_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update item",
        )


@router.delete("/{list_id}/items/{item_id}")
async def delete_item(
    list_id: str,
    item_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    list_repo=Depends(get_list_repository),
) -> dict:
    """
    Delete an item from a list with ownership validation.

    Only allows deleting items from lists owned by the current user.

    Args:
        list_id: ID of the list containing the item
        item_id: ID of the item to delete
        current_user: Current authenticated user
        list_repo: List repository (injected)

    Returns:
        Success status

    Raises:
        HTTPException 404: List or item not found
        HTTPException 500: Server error

    Issue #474: MUX-TECH-LISTS Item Management
    """
    try:
        # Verify list ownership
        list_obj = await list_repo.get_list_by_id(list_id, owner_id=current_user.sub)
        if not list_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"List not found: {list_id}",
            )

        # Delete item
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(
                select(ItemDB).where(
                    ItemDB.id == item_id,
                    ItemDB.list_id == list_id,
                )
            )
            db_item = result.scalar_one_or_none()

            if not db_item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Item not found: {item_id}",
                )

            await session.delete(db_item)
            await session.commit()

            logger.info(
                "item_deleted",
                user_id=current_user.sub,
                list_id=list_id,
                item_id=item_id,
            )

            return {
                "status": "deleted",
                "item_id": item_id,
                "list_id": list_id,
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "item_delete_error",
            user_id=current_user.sub,
            list_id=list_id,
            item_id=item_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item",
        )
