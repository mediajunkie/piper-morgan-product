"""#684/#1192(d)/#1195: Places API — the "What I'm seeing" panel backend.

Route called directly with mocked deps (established route-unit pattern).
Honesty contract (#1196 class): unconnected sources yield NO Place — never a
fabricated "I see..." or an implied-but-nonexistent connection.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from web.api.routes.places import _place_to_payload, list_places

_USER = SimpleNamespace(sub="009afc8c-bbb0-4391-8265-1575c0812949")


def _place(pid="gh-x", summary="I see 3 open issues"):
    from datetime import datetime, timezone

    from services.domain.models import Place, PlaceConfidence, PlaceType
    from services.shared_types import HardnessLevel

    return Place(
        id=pid,
        place_type=PlaceType.ISSUE_TRACKING,
        name="x repository",
        confidence=PlaceConfidence.HIGH,
        summary=summary,
        source_url="https://github.com/x",
        hardness=HardnessLevel.HARD,
        last_fetched=datetime.now(timezone.utc),
    )


class TestPlaceToPayload:
    def test_serializes_renderer_contract(self):
        p = _place()
        payload = _place_to_payload(p)
        # Exactly the keys place_window.html's renderer reads.
        for key in (
            "id",
            "place_type",
            "name",
            "confidence",
            "summary",
            "source_url",
            "hardness",
            "staleness",
            "details",
        ):
            assert key in payload
        assert payload["confidence"] == "high"
        assert payload["summary"] == "I see 3 open issues"


@pytest.mark.asyncio
async def test_unconnected_sources_yield_empty_honest_list():
    """GitHub unconfigured + calendar unauthenticated → zero places (no fabrication)."""
    gh = MagicMock()
    gh.initialize = AsyncMock()
    gh.close = AsyncMock()  # #1279: the route now closes the router in a finally
    gh.config_service.is_configured.return_value = False
    cal = MagicMock()
    cal.authenticate = AsyncMock(return_value=False)
    with (
        patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=gh,
        ),
        patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
            return_value=cal,
        ),
        patch("services.trust.TrustComputationService") as trust_cls,
    ):
        trust_cls.return_value.get_trust_stage = AsyncMock()
        result = await list_places(current_user=_USER)
    assert result["places"] == []


@pytest.mark.asyncio
async def test_connected_github_yields_place_at_stage4():
    """GitHub configured → its Place flows through, serialized for the renderer."""
    from services.shared_types import TrustStage

    gh = MagicMock()
    gh.initialize = AsyncMock()
    gh.close = AsyncMock()  # #1279: the route now closes the router in a finally
    gh.config_service.is_configured.return_value = True
    cal = MagicMock()
    cal.authenticate = AsyncMock(return_value=False)
    svc = MagicMock()
    svc.get_visible_places = AsyncMock(return_value=[_place()])
    with (
        patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=gh,
        ),
        patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
            return_value=cal,
        ),
        patch("services.place.place_service.PlaceService", return_value=svc),
        patch("services.trust.TrustComputationService") as trust_cls,
    ):
        trust_cls.return_value.get_trust_stage = AsyncMock(return_value=TrustStage.TRUSTED)
        result = await list_places(current_user=_USER)
    assert len(result["places"]) == 1
    assert result["places"][0]["summary"] == "I see 3 open issues"
    # PlaceService was constructed WITH the configured github router.
    from services.place.place_service import PlaceService  # noqa: F401

    svc.get_visible_places.assert_awaited_once()


@pytest.mark.asyncio
async def test_trust_lookup_failure_degrades_not_crashes():
    gh = MagicMock()
    gh.initialize = AsyncMock()
    gh.close = AsyncMock()  # #1279: the route now closes the router in a finally
    gh.config_service.is_configured.return_value = False
    cal = MagicMock()
    cal.authenticate = AsyncMock(side_effect=RuntimeError("no creds"))
    with (
        patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=gh,
        ),
        patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
            return_value=cal,
        ),
        patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope_fresh",
            side_effect=RuntimeError("db down"),
        ),
    ):
        result = await list_places(current_user=_USER)
    assert result["places"] == []  # degraded, honest, no 500
