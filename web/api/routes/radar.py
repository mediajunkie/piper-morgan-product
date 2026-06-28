"""Radar API (#1236 / #1090) — the Layer-2 entities-surfacing feed.

GET /api/v1/radar → the current user's RadarView (attention-first, observed-only
entities, or the empty-state teaching example). The JS Radar surface (history-sidebar
slot now; F2 page-shell aside later) renders this response. The domain lives in
`services/radar/`; this route only wires the live ConversationEntitySource (#1021
user-history), Documents (#1238), and WorkItems (#1239) into RadarFeed and serializes
— Person slots into `_build_feed` as PPM lands the entity catalog (#706), no surface
change.
"""

from __future__ import annotations

from typing import List, Optional

import structlog
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.memory.user_history import UserHistoryService
from services.radar import RadarFeed
from services.radar.feed_factory import build_entity_sources
from web.api.dependencies import get_user_history_service

router = APIRouter(prefix="/api/v1/radar", tags=["radar"])
logger = structlog.get_logger(__name__)


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


def _build_feed(service: UserHistoryService) -> RadarFeed:
    """The live Radar feed over the shared EntitySource wiring (#1269 `feed_factory`) —
    the SAME sources the standup consumes (no duplicate pipeline). Per-source isolation in
    RadarFeed means a failing source never blanks the feed."""
    return RadarFeed(build_entity_sources(service))


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
