"""User History API Routes (Issue #1021 Phase 2.7).

User-reachable surface for Layer 3 cross-session memory:
- GET    /api/v1/users/me/history          — paginated history list
- GET    /api/v1/users/me/history/search   — search across title/preview/topics
- GET    /api/v1/users/me/history/{id}     — full conversation detail
- PATCH  /api/v1/users/me/history/{id}/privacy — flip is_private

Backed by DBUserHistoryRepository (a1021userhist migration columns on
the conversations table). Per Q4-revised disposition: ship the API
surface alongside the column + repo so the feature is user-reachable
even before the dedicated UI lands under #1090.
"""

from typing import List, Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.memory.user_history import UserHistoryService
from web.api.dependencies import get_user_history_service

router = APIRouter(prefix="/api/v1/users/me/history", tags=["user-history"])
logger = structlog.get_logger(__name__)


class ConversationSummaryResponse(BaseModel):
    conversation_id: str
    title: str
    started_at: Optional[str]
    last_activity: Optional[str]
    turn_count: int
    topics: List[str]
    preview: str
    is_private: bool


class HistoryPageResponse(BaseModel):
    conversations: List[ConversationSummaryResponse]
    total_count: int
    page: int
    page_size: int
    has_more: bool


class SearchResponse(BaseModel):
    matches: List[ConversationSummaryResponse]


class PrivacyUpdateRequest(BaseModel):
    is_private: bool


class PrivacyUpdateResponse(BaseModel):
    conversation_id: str
    is_private: bool


class ConversationDetailResponse(BaseModel):
    conversation_id: str
    title: str
    started_at: Optional[str]
    last_activity: Optional[str]
    is_private: bool
    topics: List[str]
    turns: List[dict]


def _summary_to_response(summary) -> ConversationSummaryResponse:
    return ConversationSummaryResponse(
        conversation_id=summary.conversation_id,
        title=summary.title,
        started_at=summary.started_at.isoformat() if summary.started_at else None,
        last_activity=summary.last_activity.isoformat() if summary.last_activity else None,
        turn_count=summary.turn_count,
        topics=list(summary.topics or []),
        preview=summary.preview or "",
        is_private=bool(summary.is_private),
    )


@router.get("", response_model=HistoryPageResponse)
async def list_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    include_private: bool = Query(False),
    current_user: JWTClaims = Depends(get_current_user),
    service: UserHistoryService = Depends(get_user_history_service),
) -> HistoryPageResponse:
    """Paginated history of the current user's conversations."""
    history_page = await service.get_history(
        user_id=str(current_user.sub),
        page=page,
        page_size=page_size,
        include_private=include_private,
    )
    return HistoryPageResponse(
        conversations=[_summary_to_response(c) for c in history_page.conversations],
        total_count=history_page.total_count,
        page=history_page.page,
        page_size=history_page.page_size,
        has_more=history_page.has_more,
    )


@router.get("/search", response_model=SearchResponse)
async def search_history(
    q: str = Query(..., min_length=1, max_length=200),
    limit: int = Query(10, ge=1, le=100),
    current_user: JWTClaims = Depends(get_current_user),
    service: UserHistoryService = Depends(get_user_history_service),
) -> SearchResponse:
    """Search across title, preview, and topics. Excludes private + DELETED."""
    matches = await service.search_history(
        user_id=str(current_user.sub),
        query=q,
        limit=limit,
    )
    return SearchResponse(matches=[_summary_to_response(m) for m in matches])


@router.get("/{conversation_id}", response_model=ConversationDetailResponse)
async def get_history_detail(
    conversation_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    service: UserHistoryService = Depends(get_user_history_service),
) -> ConversationDetailResponse:
    """Full conversation detail including all turns."""
    detail = await service.get_conversation_detail(
        user_id=str(current_user.sub),
        conversation_id=conversation_id,
    )
    if not detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    return ConversationDetailResponse(
        conversation_id=detail.conversation_id,
        title=detail.title,
        started_at=detail.started_at.isoformat() if detail.started_at else None,
        last_activity=detail.last_activity.isoformat() if detail.last_activity else None,
        is_private=detail.is_private,
        topics=list(detail.topics or []),
        turns=detail.turns,
    )


@router.patch("/{conversation_id}/privacy", response_model=PrivacyUpdateResponse)
async def set_conversation_privacy(
    conversation_id: str,
    request: PrivacyUpdateRequest,
    current_user: JWTClaims = Depends(get_current_user),
    service: UserHistoryService = Depends(get_user_history_service),
) -> PrivacyUpdateResponse:
    """Flip the is_private flag on a conversation owned by the current user."""
    if request.is_private:
        ok = await service.mark_private(
            user_id=str(current_user.sub),
            conversation_id=conversation_id,
        )
    else:
        ok = await service.unmark_private(
            user_id=str(current_user.sub),
            conversation_id=conversation_id,
        )

    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    logger.info(
        "conversation_privacy_updated",
        user_id=current_user.sub,
        conversation_id=conversation_id,
        is_private=request.is_private,
    )
    return PrivacyUpdateResponse(
        conversation_id=conversation_id,
        is_private=request.is_private,
    )
