"""
Insight Journal API Routes (#1031 MUX-INSIGHT-PASSIVE).

Backs the Insight Journal page (`templates/insights.html`) with real
list / correct / confirm / why / delete / reset-all endpoints. The page
itself was built under #424 (closed Jan 2026); the JS dispatches custom
events that this module's endpoints consume.

Per #1031 PM audit dispositions May 3:
- Q1 soft delete (default `exclude_deleted=True` on list)
- Q2 free-text correction (POST /correct accepts text)
- Q3 "why" returns text response (not structured)
- Q4 server-rendered trust_stage in the UI route (separate concern; here
  we just expose stage if the frontend needs it via the journal listing
  response)
- Q6 (post-MVP topic-mapping deferred to #1037)
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.database.repositories import InsightRepository
from services.database.session_factory import AsyncSessionFactory


router = APIRouter(prefix="/api/v1/insights", tags=["insights"])
logger = structlog.get_logger(__name__)


class CorrectRequest(BaseModel):
    """Request shape for POST /api/v1/insights/{id}/correct.

    Per #1031 Q2 (free-text correction).
    """

    correction_text: str


def _insight_to_payload(insight) -> Dict[str, Any]:
    """Serialize a SurfaceableInsight to the JSON shape templates/insights.html
    expects.

    Maps domain fields → frontend fields per the existing JS at
    `templates/insights.html:540-573`:
    - id
    - expression / text  (frontend reads either)
    - confidence
    - topic (post-MVP — #1037; left null for now)
    - source_count (defaults to 1; #1037 will populate from underlying objects)
    - created_at
    """
    learning = insight.learning
    expression = ""
    confidence = 0.0
    if learning is not None:
        expression = learning.expression or learning.description or ""
        confidence = learning.confidence

    return {
        "id": insight.id,
        "expression": expression,
        "text": expression,  # template reads either field
        "confidence": confidence,
        "topic": None,  # #1037 post-MVP — topic mapping deferred
        "source_count": 1,
        "created_at": insight.created_at.isoformat() if insight.created_at else None,
        "user_response": insight.user_response,
        "user_correction": insight.user_correction,
    }


@router.get("")
async def list_insights(
    current_user: JWTClaims = Depends(get_current_user),
) -> Dict[str, Any]:
    """List the current user's non-deleted insights, newest first.

    Backs the Insight Journal page initial load. Soft-deleted insights
    are excluded by default (Q1 disposition).
    """
    try:
        async with AsyncSessionFactory.session_scope() as session:
            repo = InsightRepository(session)
            insights = await repo.list_for_user(user_id=current_user.sub)
        payload = [_insight_to_payload(i) for i in insights]
        logger.info(
            "insights_listed",
            user_id=current_user.sub,
            count=len(payload),
        )
        return {"insights": payload, "count": len(payload)}
    except Exception as e:
        logger.error("insights_list_error", user_id=current_user.sub, error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list insights",
        )


@router.post("/{insight_id}/correct")
async def correct_insight(
    insight_id: str,
    body: CorrectRequest,
    current_user: JWTClaims = Depends(get_current_user),
) -> Dict[str, Any]:
    """Record the user's correction text on an insight (#1031 Q2).

    Auth-scoped: cross-user correct attempts return 404.
    """
    try:
        async with AsyncSessionFactory.session_scope() as session:
            repo = InsightRepository(session)
            updated = await repo.update_user_correction(
                insight_id=insight_id,
                user_id=current_user.sub,
                correction_text=body.correction_text,
            )
        if updated is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Insight not found",
            )
        logger.info(
            "insight_corrected",
            user_id=current_user.sub,
            insight_id=insight_id,
        )
        return {"ok": True, "insight": _insight_to_payload(updated)}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "insight_correct_error",
            user_id=current_user.sub,
            insight_id=insight_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to record correction",
        )


@router.post("/{insight_id}/confirm")
async def confirm_insight(
    insight_id: str,
    current_user: JWTClaims = Depends(get_current_user),
) -> Dict[str, Any]:
    """Mark an insight as user-confirmed ("That's right" affordance).

    Reuses the existing `mark_surfaced` pathway with response="engaged"
    so the journal records the affirmation.
    """
    try:
        async with AsyncSessionFactory.session_scope() as session:
            repo = InsightRepository(session)
            # Defense-in-depth ownership check: fetch first, verify user.
            insight = await repo.get(insight_id)
            if insight is None or insight.user_id != current_user.sub:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Insight not found",
                )
            await repo.mark_surfaced(insight_id, response="engaged")
        logger.info(
            "insight_confirmed",
            user_id=current_user.sub,
            insight_id=insight_id,
        )
        return {"ok": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "insight_confirm_error",
            user_id=current_user.sub,
            insight_id=insight_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to confirm insight",
        )


@router.post("/{insight_id}/why")
async def why_insight(
    insight_id: str,
    current_user: JWTClaims = Depends(get_current_user),
) -> Dict[str, Any]:
    """Return a short text explanation of why this insight surfaced (#1031 Q3).

    Per Q3 Option A: text response, not structured. Pulls source-count from
    the insight's metadata; future refinement will cite specific objects.
    """
    try:
        async with AsyncSessionFactory.session_scope() as session:
            repo = InsightRepository(session)
            insight = await repo.get(insight_id)
            if insight is None or insight.user_id != current_user.sub:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Insight not found",
                )
            # Source count: the insight derives from object_id (one COMPOSTED
            # object); future work counts derived_from + connected_insights.
            source_count = 1
            if insight.learning and getattr(insight.learning, "pattern", None):
                source_count = max(source_count, len(insight.learning.pattern.occurrences or []))
        explanation = (
            f"I noticed this from {source_count} observation"
            + ("" if source_count == 1 else "s")
            + "."
        )
        logger.info(
            "insight_why_returned",
            user_id=current_user.sub,
            insight_id=insight_id,
            source_count=source_count,
        )
        return {"explanation": explanation}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "insight_why_error",
            user_id=current_user.sub,
            insight_id=insight_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to return explanation",
        )


@router.delete("/{insight_id}")
async def delete_insight(
    insight_id: str,
    current_user: JWTClaims = Depends(get_current_user),
) -> Dict[str, bool]:
    """Soft-delete an insight (#1031 Q1).

    Auth-scoped. Cross-user delete returns 404 (no information leak about
    other users' insights).
    """
    try:
        async with AsyncSessionFactory.session_scope() as session:
            repo = InsightRepository(session)
            ok = await repo.soft_delete(insight_id=insight_id, user_id=current_user.sub)
        if not ok:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Insight not found",
            )
        logger.info(
            "insight_deleted",
            user_id=current_user.sub,
            insight_id=insight_id,
        )
        return {"ok": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "insight_delete_error",
            user_id=current_user.sub,
            insight_id=insight_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete insight",
        )


@router.delete("", status_code=status.HTTP_200_OK)
async def reset_all_insights(
    current_user: JWTClaims = Depends(get_current_user),
) -> Dict[str, int]:
    """Reset-all: soft-delete all of the user's insights (#1031 Q1).

    Per-user only (no cross-user effect). Returns count of insights
    soft-deleted in this call.
    """
    try:
        async with AsyncSessionFactory.session_scope() as session:
            repo = InsightRepository(session)
            count = await repo.soft_delete_all(user_id=current_user.sub)
        logger.info(
            "insights_reset",
            user_id=current_user.sub,
            count=count,
        )
        return {"deleted": count}
    except Exception as e:
        logger.error(
            "insights_reset_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset insights",
        )
