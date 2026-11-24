"""
Feedback API Routes (Issue #357: SEC-RBAC Phase 1.3)

Provides feedback CRUD endpoints with ownership validation:
- Submit feedback
- Retrieve feedback
- List user feedback
"""

from typing import Any, Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from services.api.errors import UserFacingHTTPException
from services.auth.auth_middleware import get_current_user, require_admin
from services.auth.jwt_service import JWTClaims
from web.api.dependencies import get_feedback_service

router = APIRouter(prefix="/api/v1/feedback", tags=["feedback"])
logger = structlog.get_logger(__name__)

# Issue 2432 (CXO, comment 7144095698): reworded, marked.
FEEDBACK_NEEDED_LINE = "Write your feedback first."

# #2096 (Arch, 2026-10-19): the text travels in a bounded JSON body, never the
# query string (a query string lands in access logs; a tester's words must not).
FEEDBACK_MAX_CHARS = 4000


class FeedbackSubmission(BaseModel):
    content: str = Field(..., max_length=FEEDBACK_MAX_CHARS)
    feedback_type: Optional[str] = "general"
    page_path: Optional[str] = Field(default=None, max_length=255)


@router.post("")
async def submit_feedback(
    submission: FeedbackSubmission,
    current_user: JWTClaims = Depends(get_current_user),
    feedback_service=Depends(get_feedback_service),
) -> dict:
    """
    Submit feedback with ownership validation (SEC-RBAC).

    Args:
        submission: JSON body — content (bounded), feedback_type (general, bug,
            feature_request, tester, …), page_path (#2096, the page it was sent from)
        current_user: Current authenticated user
        feedback_service: Feedback service (injected)

    Returns:
        Created feedback with ID

    Raises:
        HTTPException 400: Invalid input
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    content = submission.content
    feedback_type = submission.feedback_type
    page_path = submission.page_path
    try:
        if not content or not content.strip():
            raise UserFacingHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=FEEDBACK_NEEDED_LINE
            )

        # #1436 B15: this route constructed a nonexistent domain.Feedback and
        # called a nonexistent submit_feedback() — every submission 500'd. The
        # real service API is capture_feedback(session_id, feedback_type,
        # comment, ...) -> feedback_id (services/feedback/feedback_service.py).
        from uuid import UUID as _UUID

        # #2096: the Send feedback page passes the path it was opened from; the
        # page and time are attached by code, never asked of the person. Only a
        # path on this site is kept (never an outside URL).
        _path = (page_path or "").strip()[:255]
        # Arch (#2096 validation): "//evil.example/x" starts with "/" and is a
        # protocol-relative outside URL; only a single leading slash is a path here.
        _ctx = (
            {"page_path": _path}
            if _path.startswith("/") and not _path.startswith(("//", "/\\"))
            else None
        )
        feedback_id = await feedback_service.capture_feedback(
            session_id=f"api-{current_user.sub}",
            feedback_type=feedback_type or "general",
            comment=content,
            context=_ctx,
            user_id=_UUID(str(current_user.sub)),
            source="ui" if _ctx is not None else "api",
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

        feedback_list = await feedback_service.list_feedback(user_id=_UUID(str(current_user.sub)))

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


# #2096: the admin read of what testers sent through the Send feedback page.
# Its own router under /api/v1/admin so the path never collides with
# GET /api/v1/feedback/{feedback_id} above. require_admin is the same live,
# fail-closed gate every admin route uses (#1598 / #2081).
admin_router = APIRouter(prefix="/api/v1/admin", tags=["feedback"])


@admin_router.get("/feedback")
async def list_all_feedback(
    admin: JWTClaims = Depends(require_admin),
    feedback_service=Depends(get_feedback_service),
    limit: int = 200,
) -> dict:
    """Every tester's Send-feedback rows, newest first (feedback_type 'tester')."""
    rows = await feedback_service.list_feedback(feedback_type="tester", limit=min(limit, 500))
    out = []
    for fb in rows:
        ctx: Any = getattr(fb, "context", None) or {}
        created: Any = getattr(fb, "created_at", None)
        out.append(
            {
                "id": str(getattr(fb, "id", "")),
                "user_id": str(getattr(fb, "user_id", "") or ""),
                "body": getattr(fb, "comment", ""),
                "page_path": ctx.get("page_path") if isinstance(ctx, dict) else None,
                "created_at": created.isoformat()
                if created is not None and hasattr(created, "isoformat")
                else created,
            }
        )
    return {"feedback": out, "count": len(out)}
