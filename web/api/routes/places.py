"""Places API (#684 / #1192(d) / #1195).

Backs the home page's "What I'm seeing" panel (`templates/home.html` +
`templates/components/place_window.html`). The frontend shipped under #684 with
its fetch stubbed ("TODO: Wire to /api/v1/places endpoint when available") and
`PlaceService` was built but never routed (#1195 audit) — so the panel
permanently showed "No external sources connected yet" even with GitHub
connected (PM-observed, 2026-06-12). This module is the missing last mile.

Returns the user's trust-visible Places (GitHub issue-tracking, Calendar) in
the exact JSON shape `PlaceWindow.render` consumes. Sources that aren't
connected or fail simply don't appear — the panel's empty state is then
honest ("nothing connected") rather than fabricated.
"""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import UUID

import structlog
from fastapi import APIRouter, Depends

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims

router = APIRouter(prefix="/api/v1/places", tags=["places"])
logger = structlog.get_logger(__name__)


def _place_to_payload(place) -> Dict[str, Any]:
    """Serialize a Place to the shape place_window.html's renderer expects."""
    return {
        "id": place.id,
        "place_type": place.place_type.value,
        "name": place.name,
        "confidence": place.confidence.value,
        "summary": place.summary,
        "source_url": place.source_url,
        "hardness": place.hardness.value,
        "staleness": place.get_staleness_indicator(),
        "details": place.details,
    }


@router.get("")
@router.get("/")
async def list_places(current_user: JWTClaims = Depends(get_current_user)) -> Dict[str, Any]:
    """The user's trust-visible Places (federated external-source windows).

    Each integration degrades independently: an unconnected/failing source
    yields no Place (PlaceService returns None for it) rather than an error —
    the panel only ever claims what was actually observed (#1196 discipline).
    """
    user_id = str(current_user.sub)

    # Resolve trust stage (gates which Places are visible, per #684 hardness map).
    from services.repositories.user_trust_profile_repository import (
        UserTrustProfileRepository,
    )
    from services.shared_types import TrustStage
    from services.trust import TrustComputationService

    trust_stage = TrustStage.NEW
    try:
        from services.database.session_factory import AsyncSessionFactory

        async with AsyncSessionFactory.session_scope_fresh() as session:
            trust_service = TrustComputationService(UserTrustProfileRepository(session))
            trust_stage = await trust_service.get_trust_stage(UUID(user_id))
    except Exception as e:
        logger.warning("places_trust_lookup_failed", error=str(e))

    # GitHub source — only offered to the service if the user has a configured
    # token (keychain-first per #1192); otherwise no github Place at all.
    # The candidate is tracked separately from github_router so the finally
    # below closes it even when it doesn't graduate to a source (#1279).
    github_router = None
    gh_candidate = None
    try:
        from services.integrations.github.github_integration_router import (
            GitHubIntegrationRouter,
        )

        gh_candidate = GitHubIntegrationRouter()
        await gh_candidate.initialize(user_id=user_id)
        if gh_candidate.config_service.is_configured(user_id):
            github_router = gh_candidate
    except Exception as e:
        logger.warning("places_github_init_failed", error=str(e))

    # Calendar source — gated on a real authenticate() (not mere construction):
    # an unconfigured calendar must yield NO Place, not a "couldn't reach your
    # calendar" card implying a connection that never existed (#1196 class).
    calendar_service = None
    try:
        from services.integrations.calendar.calendar_integration_router import (
            CalendarIntegrationRouter,
        )

        candidate = CalendarIntegrationRouter()
        if await candidate.authenticate():
            calendar_service = candidate
    except Exception as e:
        logger.debug("places_calendar_unavailable", error=str(e))

    from services.place.place_service import PlaceService

    try:
        service = PlaceService(github_router=github_router, calendar_service=calendar_service)
        places = await service.get_visible_places(trust_stage)

        payload: List[Dict[str, Any]] = [_place_to_payload(p) for p in places]
        logger.info(
            "places_listed",
            user_id=user_id,
            trust_stage=trust_stage.name,
            count=len(payload),
            github=bool(github_router),
            calendar=bool(calendar_service),
        )
        return {"places": payload, "trust_stage": trust_stage.value}
    finally:
        # #1279: this route constructs a fresh router per request; close its
        # aiohttp session (router.close() is idempotent + never raises).
        if gh_candidate is not None:
            await gh_candidate.close()
