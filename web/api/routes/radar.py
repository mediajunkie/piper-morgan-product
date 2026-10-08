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
from services.domain.models import degraded_disclosure, degraded_radar_card
from services.memory.user_history import UserHistoryService
from services.radar import RadarFeed, ReminderEntitySource
from services.radar.feed_factory import DueReminderProvider, build_entity_sources
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
    pinned: bool = False  # #1625: due reminders render in a locked section at top


class RadarViewResponse(BaseModel):
    state: str  # "populated" | "empty"
    entities: List[RadarEntityResponse]
    # #1587: user-facing labels of any source that genuinely FAILED this read
    # (e.g. ["your GitHub work items"]) — empty means no source failed, not
    # that every source was attempted.
    degraded_sources: List[str] = []
    # #1889 / #1963: server-rendered copy for a failed source (CXO 2026-10-08),
    # "" when none failed. ``degraded_title`` heads the empty-Radar card;
    # ``degraded_note`` sits above a populated Radar.
    degraded_title: str = ""
    degraded_sub: str = ""  # #1965 (b): the reason-specific second line of the empty card
    degraded_note: str = ""


def _build_feed(service: UserHistoryService) -> RadarFeed:
    """The live Radar feed over the shared EntitySource wiring (#1269 `feed_factory`) —
    the SAME sources the standup consumes (no duplicate pipeline). Per-source isolation in
    RadarFeed means a failing source never blanks the feed.

    #1625: due reminders join as a RADAR-ONLY source (PM's ruling pins them here;
    the standup's shared wiring is untouched — reminders in the standup would be a
    separate design call, not a side effect of the Radar pin)."""
    return RadarFeed(build_entity_sources(service) + [ReminderEntitySource(DueReminderProvider())])


@router.get("", response_model=RadarViewResponse)
async def get_radar(
    current_user: JWTClaims = Depends(get_current_user),
    service: UserHistoryService = Depends(get_user_history_service),
) -> RadarViewResponse:
    """The user's Radar — observed entities attention-first, or the empty-state example."""
    view = await _build_feed(service).assemble(str(current_user.sub))
    # #1889/#1965 (b): the empty-Radar card copy for a failed source, by reason.
    details = list(getattr(view, "degraded_details", None) or []) or [
        {"label": lb, "reason": None, "connector": None} for lb in view.degraded_sources
    ]
    card = (
        degraded_radar_card(details)
        if view.state == "empty" and view.degraded_sources
        else ("", "")
    )
    return RadarViewResponse(
        state=view.state,
        degraded_sources=view.degraded_sources,
        degraded_title=card[0],
        degraded_sub=card[1],
        degraded_note=(
            degraded_disclosure(view.degraded_sources, "chat", details=view.degraded_details)
            if view.state == "populated"
            else ""
        ),
        entities=[
            RadarEntityResponse(
                entity_type=e.entity_type.value,
                title=e.title,
                lifecycle_state=e.lifecycle_state,
                provenance=e.provenance.value,
                meta=e.meta,
                ref=e.ref,
                pinned=e.pinned,
            )
            for e in view.entities
        ],
    )
