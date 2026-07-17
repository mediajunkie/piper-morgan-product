"""
Todo Management API Routes (Issue #357: SEC-RBAC Phase 1.3)

Provides todo CRUD endpoints with ownership validation:
- Create, read, update, delete todos
- Todo filtering by owner
- User-isolated todo access
"""

from typing import List, Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.domain import models as domain
from web.api.dependencies import get_todo_repository

router = APIRouter(prefix="/api/v1/todos", tags=["todos"])
logger = structlog.get_logger(__name__)


# Pydantic models for sharing operations
class ShareTodoRequest(BaseModel):
    """Request model for sharing a todo with a user (SEC-RBAC Phase 2)"""

    user_id: str
    role: str = "viewer"  # Default to viewer (read-only) - can be viewer, editor, admin


class TodoSharePermissionResponse(BaseModel):
    """Response model for individual todo share permissions"""

    user_id: str
    role: str


class ShareTodoResponse(BaseModel):
    """Response model for sharing operations (SEC-RBAC Phase 2)"""

    id: str
    title: str
    owner_id: str
    shared_with: List[TodoSharePermissionResponse]
    message: str


class UpdateTodoRoleRequest(BaseModel):
    """Request model for updating a user's role on a todo (SEC-RBAC Phase 2)"""

    role: str  # viewer, editor, admin


class TodoUserRoleResponse(BaseModel):
    """Response model for user's role on a todo (SEC-RBAC Phase 2)"""

    role: str  # owner, admin, editor, viewer, or null
    message: str


class SharedTodosResponse(BaseModel):
    """Response model for shared todos"""

    todos: List[dict]
    count: int


class CreateTodoRequest(BaseModel):
    """Request model for creating a todo (Issue #468)"""

    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    priority: Optional[str] = "medium"


@router.post("")
async def create_todo(
    request: CreateTodoRequest,
    current_user: JWTClaims = Depends(get_current_user),
    todo_repo=Depends(get_todo_repository),
) -> dict:
    """
    Create a new todo with ownership validation (SEC-RBAC).

    Args:
        request: CreateTodoRequest with title and optional fields
        current_user: Current authenticated user
        todo_repo: Todo repository (injected)

    Returns:
        Created todo with ID and metadata

    Raises:
        HTTPException 400: Invalid input
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    Issue #468: Accept JSON body instead of query params
    """
    try:
        if not request.title or not request.title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Todo title is required",
            )

        # Create todo with ownership
        # Note: Todo domain model uses 'text' not 'title' (title is a property)
        new_todo = domain.Todo(
            text=request.title,
            description=request.description or "",
            status=request.status or "pending",
            priority=request.priority or "medium",
            owner_id=current_user.sub,
        )

        created_todo = await todo_repo.create_todo(new_todo)

        logger.info(
            "todo_created",
            user_id=current_user.sub,
            todo_id=created_todo.id,
            title=request.title,
        )

        return {
            "id": created_todo.id,
            "title": created_todo.title,
            "description": created_todo.description,
            "status": created_todo.status,
            "priority": created_todo.priority,
            "owner_id": created_todo.owner_id,
            "created_at": created_todo.created_at.isoformat() if created_todo.created_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "todo_create_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create todo",
        )


@router.get("/{todo_id}")
async def get_todo(
    todo_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    todo_repo=Depends(get_todo_repository),
) -> dict:
    """
    Get todo by ID with ownership validation (SEC-RBAC).

    Only returns todo if current user is the owner.

    Args:
        todo_id: Todo ID to retrieve
        current_user: Current authenticated user
        todo_repo: Todo repository (injected)

    Returns:
        Todo metadata (if owned by current user)

    Raises:
        HTTPException 404: Todo not found or not owned by current user
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        todo_obj = await todo_repo.get_todo_by_id(todo_id, owner_id=current_user.sub)

        if not todo_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo not found: {todo_id}",
            )

        logger.info(
            "todo_retrieved",
            user_id=current_user.sub,
            todo_id=todo_id,
        )

        return {
            "id": todo_obj.id,
            "title": todo_obj.title,
            "description": todo_obj.description,
            "status": todo_obj.status,
            "priority": todo_obj.priority,
            "owner_id": todo_obj.owner_id,
            "created_at": todo_obj.created_at.isoformat() if todo_obj.created_at else None,
            "updated_at": todo_obj.updated_at.isoformat() if todo_obj.updated_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "todo_get_error",
            user_id=current_user.sub,
            todo_id=todo_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve todo",
        )


@router.get("")
async def list_todos(
    current_user: JWTClaims = Depends(get_current_user),
    todo_repo=Depends(get_todo_repository),
) -> dict:
    """
    List all todos owned by current user (SEC-RBAC).

    Returns:
        List of todos owned by current user

    Raises:
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        todos = await todo_repo.get_todos_by_owner(current_user.sub)

        logger.info(
            "todos_retrieved",
            user_id=current_user.sub,
            count=len(todos),
        )

        return {
            "todos": [
                {
                    "id": t.id,
                    "text": t.title,  # Frontend expects 'text' field
                    "status": t.status,
                    "priority": t.priority,
                    "owner_id": t.owner_id,
                    "created_at": t.created_at.isoformat() if t.created_at else None,
                    # MUX Lifecycle (#708) - include when present for UI indicator
                    "lifecycle_state": t.lifecycle_state.value if t.lifecycle_state else None,
                }
                for t in todos
            ],
            "count": len(todos),
        }

    except Exception as e:
        logger.error(
            "todos_get_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve todos",
        )


@router.put("/{todo_id}")
async def update_todo(
    todo_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    # #1436 B5: renamed (public API preserved via alias) — a param literally
    # named `status` shadowed the starlette `status` module, so every
    # 404/400/500 branch in this function raised AttributeError instead of the
    # intended HTTPException.
    todo_status: Optional[str] = Query(None, alias="status"),
    priority: Optional[str] = None,
    current_user: JWTClaims = Depends(get_current_user),
    todo_repo=Depends(get_todo_repository),
) -> dict:
    """
    Update todo with ownership validation (SEC-RBAC).

    Only allows updating if current user is the owner.

    Args:
        todo_id: Todo ID to update
        title: New todo title (optional)
        description: New todo description (optional)
        todo_status: New todo status (optional; query param name stays `status`)
        priority: New todo priority (optional)
        current_user: Current authenticated user
        todo_repo: Todo repository (injected)

    Returns:
        Updated todo

    Raises:
        HTTPException 404: Todo not found or not owned by current user
        HTTPException 400: Invalid input
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        # Verify ownership
        todo_obj = await todo_repo.get_todo_by_id(todo_id, owner_id=current_user.sub)

        if not todo_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo not found: {todo_id}",
            )

        # Update fields
        if title is not None:
            if not title.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Todo title cannot be empty",
                )
            todo_obj.title = title

        if description is not None:
            todo_obj.description = description

        if todo_status is not None:
            todo_obj.status = todo_status

        if priority is not None:
            todo_obj.priority = priority

        updated = await todo_repo.update_todo(todo_obj)

        logger.info(
            "todo_updated",
            user_id=current_user.sub,
            todo_id=todo_id,
        )

        return {
            "id": updated.id,
            "title": updated.title,
            "status": updated.status,
            "priority": updated.priority,
            "owner_id": updated.owner_id,
            "updated_at": updated.updated_at.isoformat() if updated.updated_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "todo_update_error",
            user_id=current_user.sub,
            todo_id=todo_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update todo",
        )


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    todo_repo=Depends(get_todo_repository),
) -> dict:
    """
    Delete todo with ownership validation (SEC-RBAC).

    Only allows deleting if current user is the owner.

    Args:
        todo_id: Todo ID to delete
        current_user: Current authenticated user
        todo_repo: Todo repository (injected)

    Returns:
        Success message

    Raises:
        HTTPException 404: Todo not found or not owned by current user
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        # Verify ownership before deleting
        todo_obj = await todo_repo.get_todo_by_id(todo_id, owner_id=current_user.sub)

        if not todo_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo not found: {todo_id}",
            )

        await todo_repo.delete_todo(todo_id, owner_id=current_user.sub)

        logger.info(
            "todo_deleted",
            user_id=current_user.sub,
            todo_id=todo_id,
        )

        return {
            "status": "deleted",
            "todo_id": todo_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "todo_delete_error",
            user_id=current_user.sub,
            todo_id=todo_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete todo",
        )


@router.post("/{todo_id}/share")
async def share_todo(
    todo_id: str,
    request: ShareTodoRequest,
    current_user: JWTClaims = Depends(get_current_user),
    todo_repo=Depends(get_todo_repository),
) -> ShareTodoResponse:
    """
    Share a todo with another user at specified role (owner only - SEC-RBAC Phase 2).

    Owner explicitly specifies role when sharing:
    - viewer: Read-only access
    - editor: Can modify content
    - admin: Can share with others (but not delete)

    Args:
        todo_id: ID of the todo to share
        request: ShareTodoRequest with user_id and role
        current_user: Current authenticated user (must be owner)
        todo_repo: Todo repository (injected)

    Returns:
        Updated todo with shared_with array of {user_id, role} objects

    Raises:
        HTTPException 400: Invalid user_id or role
        HTTPException 404: Todo not found or user not owner
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

        # Share todo (owner-only operation)
        shared_todo = await todo_repo.share_todo(
            todo_id, current_user.sub, request.user_id, share_role
        )

        if not shared_todo:
            logger.warning(
                "todo_share_unauthorized",
                user_id=current_user.sub,
                todo_id=todo_id,
                target_user=request.user_id,
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or you don't have permission to share it",
            )

        logger.info(
            "todo_shared",
            owner_id=current_user.sub,
            todo_id=todo_id,
            shared_with_user=request.user_id,
            role=request.role,
        )

        # Convert shared_with SharePermission objects to response format
        shared_with_response = [
            TodoSharePermissionResponse(user_id=perm.user_id, role=perm.role.value)
            for perm in shared_todo.shared_with
        ]

        return ShareTodoResponse(
            id=shared_todo.id,
            title=shared_todo.title,
            owner_id=shared_todo.owner_id,
            shared_with=shared_with_response,
            message=f"Todo shared with user {request.user_id} as {request.role}",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "todo_share_error",
            user_id=current_user.sub,
            todo_id=todo_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to share todo",
        )


@router.delete("/{todo_id}/share/{user_id}")
async def unshare_todo(
    todo_id: str,
    user_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    todo_repo=Depends(get_todo_repository),
) -> dict:
    """
    Remove sharing access from a todo (owner only - SEC-RBAC Phase 1.4).

    Revokes read access for the specified user.

    Args:
        todo_id: ID of the todo to unshare
        user_id: ID of user to remove from shared_with
        current_user: Current authenticated user (must be owner)
        todo_repo: Todo repository (injected)

    Returns:
        Success status

    Raises:
        HTTPException 404: Todo not found or user not owner
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.4 Shared Resource Access
    """
    try:
        # Unshare todo (owner-only operation)
        unshared_todo = await todo_repo.unshare_todo(todo_id, current_user.sub, user_id)

        if not unshared_todo:
            logger.warning(
                "todo_unshare_unauthorized",
                user_id=current_user.sub,
                todo_id=todo_id,
                unshare_from_user=user_id,
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or you don't have permission to unshare it",
            )

        logger.info(
            "todo_unshared",
            owner_id=current_user.sub,
            todo_id=todo_id,
            unshared_from_user=user_id,
        )

        return {
            "success": True,
            "message": f"User {user_id} no longer has access to this todo",
            "todo_id": todo_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "todo_unshare_error",
            user_id=current_user.sub,
            todo_id=todo_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to unshare todo",
        )


@router.put("/{todo_id}/share/{user_id}")
async def update_todo_share_role(
    todo_id: str,
    user_id: str,
    request: UpdateTodoRoleRequest,
    current_user: JWTClaims = Depends(get_current_user),
    todo_repo=Depends(get_todo_repository),
) -> dict:
    """
    Update a user's role for a shared todo (owner only - SEC-RBAC Phase 2).

    Changes the role of an already-shared user (viewer, editor, admin).

    Args:
        todo_id: ID of the todo
        user_id: ID of user whose role to update
        request: UpdateTodoRoleRequest with new role
        current_user: Current authenticated user (must be owner)
        todo_repo: Todo repository (injected)

    Returns:
        Success status with updated role

    Raises:
        HTTPException 400: Invalid role
        HTTPException 404: Todo not found or user not owner or user not shared with
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
        success = await todo_repo.update_share_role(todo_id, current_user.sub, user_id, share_role)

        if not success:
            logger.warning(
                "todo_update_role_failed",
                user_id=current_user.sub,
                todo_id=todo_id,
                target_user=user_id,
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found, you don't have permission, or user is not shared with this todo",
            )

        logger.info(
            "todo_share_role_updated",
            owner_id=current_user.sub,
            todo_id=todo_id,
            target_user=user_id,
            new_role=request.role,
        )

        return {
            "success": True,
            "message": f"Updated user {user_id} role to {request.role}",
            "todo_id": todo_id,
            "user_id": user_id,
            "role": request.role,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "todo_update_role_error",
            user_id=current_user.sub,
            todo_id=todo_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update share role",
        )


@router.get("/{todo_id}/my-role")
async def get_todo_my_role(
    todo_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    todo_repo=Depends(get_todo_repository),
) -> TodoUserRoleResponse:
    """
    Get current user's role for a todo (SEC-RBAC Phase 2).

    Returns the role of the current user for the specified todo:
    - 'owner': User owns the todo
    - 'admin': User can share and modify
    - 'editor': User can modify content
    - 'viewer': User can read only
    - None: User has no access (404)

    Args:
        todo_id: ID of the todo
        current_user: Current authenticated user
        todo_repo: Todo repository (injected)

    Returns:
        Current user's role for the todo

    Raises:
        HTTPException 404: Todo not found or user has no access
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 2 Role-Based Permissions
    """
    try:
        # Get user's role
        role = await todo_repo.get_user_role(todo_id, current_user.sub)

        if not role:
            logger.info(
                "todo_no_access",
                user_id=current_user.sub,
                todo_id=todo_id,
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or you don't have access to it",
            )

        logger.info(
            "todo_role_retrieved",
            user_id=current_user.sub,
            todo_id=todo_id,
            role=role,
        )

        return TodoUserRoleResponse(role=role, message=f"You have {role} access to this todo")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "todo_get_role_error",
            user_id=current_user.sub,
            todo_id=todo_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user role",
        )


@router.get("/shared-with-me")
async def get_shared_todos(
    current_user: JWTClaims = Depends(get_current_user),
    todo_repo=Depends(get_todo_repository),
) -> SharedTodosResponse:
    """
    Get todos shared with the current user (SEC-RBAC Phase 1.4).

    Returns all todos where the current user is in the shared_with array.
    Does not include todos owned by the current user (see GET / for owned todos).

    Args:
        current_user: Current authenticated user
        todo_repo: Todo repository (injected)

    Returns:
        List of todos shared with this user

    Raises:
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.4 Shared Resource Access
    """
    try:
        shared_todos = await todo_repo.get_todos_shared_with_me(current_user.sub)

        logger.info(
            "shared_todos_retrieved",
            user_id=current_user.sub,
            count=len(shared_todos),
        )

        return SharedTodosResponse(
            todos=[
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "owner_id": t.owner_id,
                    "status": t.status,
                    "created_at": t.created_at.isoformat() if t.created_at else None,
                }
                for t in shared_todos
            ],
            count=len(shared_todos),
        )

    except Exception as e:
        logger.error(
            "shared_todos_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve shared todos",
        )
