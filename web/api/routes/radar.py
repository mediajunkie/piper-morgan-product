"""Radar API (#1236 / #1090) — the Layer-2 entities-surfacing feed.

GET /api/v1/radar → the current user's RadarView (attention-first, observed-only
entities, or the empty-state teaching example). The JS Radar surface (history-sidebar
slot now; F2 page-shell aside later) renders this response. The domain lives in
`services/radar/`; this route only wires the live ConversationEntitySource (#1021
user-history) into RadarFeed and serializes — WorkItem/Person/Document sources slot
into `_build_feed` as PPM lands the entity catalog (#706), no surface change.
"""
from __future__ import annotations

from typing import List, Optional

import structlog
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.knowledge_graph.document_service import get_document_service
from services.memory.user_history import UserHistoryService
from services.radar import ConversationEntitySource, DocumentEntitySource, RadarFeed
from web.api.dependencies import get_user_history_service

router = APIRouter(prefix="/api/v1/radar", tags=["radar"])
logger = structlog.get_logger(__name__)

# v1: how many conversations the conversation source pulls as candidate entities.
_CONVERSATION_FETCH = 25


class RadarEntityResponse(BaseModel):
    entity_type: str
    title: str
    lifecycle_state: str
    provenance: str
    meta: str
    ref: Optional[str] = None


class RadarViewResponse(BaseModel):
    state: str  # "populated" | "empty"
    entities: List[RadarEntityResponse]


class _ConversationHistoryProvider:
    """Adapts UserHistoryService → the `list_summaries(user_id)` shape
    ConversationEntitySource expects (#1021 summary fields; last_activity as ISO str)."""

    def __init__(self, service: UserHistoryService):
        self._service = service

    async def list_summaries(self, user_id: str) -> list[dict]:
        page = await self._service.get_history(
            user_id=user_id, page=1, page_size=_CONVERSATION_FETCH, include_private=False
        )
        return [
            {
                "conversation_id": c.conversation_id,
                "title": c.title,
                "last_activity": c.last_activity.isoformat() if c.last_activity else None,
                "turn_count": c.turn_count,
                "topics": list(c.topics or []),
                "preview": c.preview or "",
            }
            for c in page.conversations
        ]


def _build_feed(service: UserHistoryService) -> RadarFeed:
    """Live entity sources: Conversations (#1021) + Documents (#1238). WorkItem/Person
    register here as PPM lands the entity catalog (#706); no surface change when they do.
    Per-source isolation in RadarFeed means a failing source never blanks the feed."""
    return RadarFeed(
        [
            ConversationEntitySource(_ConversationHistoryProvider(service)),
            DocumentEntitySource(get_document_service()),
        ]
    )


@router.get("", response_model=RadarViewResponse)
async def get_radar(
    current_user: JWTClaims = Depends(get_current_user),
    service: UserHistoryService = Depends(get_user_history_service),
) -> RadarViewResponse:
    """The user's Radar — observed entities attention-first, or the empty-state example."""
    view = await _build_feed(service).assemble(str(current_user.sub))
    return RadarViewResponse(
        state=view.state,
        entities=[
            RadarEntityResponse(
                entity_type=e.entity_type.value,
                title=e.title,
                lifecycle_state=e.lifecycle_state,
                provenance=e.provenance.value,
                meta=e.meta,
                ref=e.ref,
            )
            for e in view.entities
        ],
    )
