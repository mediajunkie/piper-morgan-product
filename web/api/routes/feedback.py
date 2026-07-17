"""
Feedback API Routes (Issue #357: SEC-RBAC Phase 1.3)

Provides feedback CRUD endpoints with ownership validation:
- Submit feedback
- Retrieve feedback
- List user feedback
"""

from typing import Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from web.api.dependencies import get_feedback_service

router = APIRouter(prefix="/api/v1/feedback", tags=["feedback"])
logger = structlog.get_logger(__name__)


@router.post("")
async def submit_feedback(
    content: str,
    feedback_type: Optional[str] = "general",
    current_user: JWTClaims = Depends(get_current_user),
    feedback_service=Depends(get_feedback_service),
) -> dict:
    """
    Submit feedback with ownership validation (SEC-RBAC).

    Args:
        content: Feedback content
        feedback_type: Type of feedback (general, bug, feature_request, etc.)
        current_user: Current authenticated user
        feedback_service: Feedback service (injected)

    Returns:
        Created feedback with ID

    Raises:
        HTTPException 400: Invalid input
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        if not content or not content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Feedback content is required",
            )

        # #1436 B15: this route constructed a nonexistent domain.Feedback and
        # called a nonexistent submit_feedback() — every submission 500'd. The
        # real service API is capture_feedback(session_id, feedback_type,
        # comment, ...) -> feedback_id (services/feedback/feedback_service.py).
        from uuid import UUID as _UUID

        feedback_id = await feedback_service.capture_feedback(
            session_id=f"api-{current_user.sub}",
            feedback_type=feedback_type or "general",
            comment=content,
            user_id=_UUID(str(current_user.sub)),
            source="api",
        )

        logger.info(
            "feedback_submitted",
            user_id=current_user.sub,
            feedback_id=feedback_id,
            type=feedback_type,
        )

        return {
            "id": feedback_id,
            "content": content,
            "type": feedback_type or "general",
            "user_id": str(current_user.sub),
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "feedback_submit_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit feedback",
        )


@router.get("/{feedback_id}")
async def get_feedback(
    feedback_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    feedback_service=Depends(get_feedback_service),
) -> dict:
    """
    Get feedback by ID with ownership validation (SEC-RBAC).

    Only returns feedback if current user is the creator.

    Args:
        feedback_id: Feedback ID to retrieve
        current_user: Current authenticated user
        feedback_service: Feedback service (injected)

    Returns:
        Feedback details (if owned by current user)

    Raises:
        HTTPException 404: Feedback not found or not owned by current user
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        # #1436 B15: was get_feedback_by_id() — doesn't exist; the real,
        # owner-scoped read is get_feedback(feedback_id, user_id=...) and the
        # domain field is `comment`, not `content`.
        from uuid import UUID as _UUID

        feedback_obj = await feedback_service.get_feedback(
            feedback_id, user_id=_UUID(str(current_user.sub))
        )

        if not feedback_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Feedback not found: {feedback_id}",
            )

        logger.info(
            "feedback_retrieved",
            user_id=current_user.sub,
            feedback_id=feedback_id,
        )

        return {
            "id": feedback_obj.id,
            "content": feedback_obj.comment,
            "type": feedback_obj.feedback_type,
            "user_id": str(feedback_obj.user_id) if feedback_obj.user_id else None,
            "created_at": feedback_obj.created_at.isoformat() if feedback_obj.created_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "feedback_get_error",
            user_id=current_user.sub,
            feedback_id=feedback_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve feedback",
        )


@router.get("")
async def list_feedback(
    current_user: JWTClaims = Depends(get_current_user),
    feedback_service=Depends(get_feedback_service),
) -> dict:
    """
    List all feedback submitted by current user (SEC-RBAC).

    Returns:
        List of feedback items from current user

    Raises:
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        # #1436 B15: was get_feedback_by_user() — doesn't exist; the real read
        # is list_feedback(user_id=...) (WHERE-scoped to the owner) and the
        # domain field is `comment`.
        from uuid import UUID as _UUID

        feedback_list = await feedback_service.list_feedback(
            user_id=_UUID(str(current_user.sub))
        )

        logger.info(
            "feedback_listed",
            user_id=current_user.sub,
            count=len(feedback_list),
        )

        return {
            "feedback": [
                {
                    "id": f.id,
                    "content": f.comment,
                    "type": f.feedback_type,
                    "created_at": f.created_at.isoformat() if f.created_at else None,
                }
                for f in feedback_list
            ],
            "count": len(feedback_list),
        }

    except Exception as e:
        logger.error(
            "feedback_list_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve feedback",
        )
