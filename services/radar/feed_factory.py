"""Shared EntitySource wiring (#1269) — build the live Radar entity sources in ONE place.

Both the Radar route (`web/api/routes/radar.py`) and the morning-standup skill
(`StandupAssembler`, #1269) consume these sources. The standup is a *consumer* of the
entity catalog, not a parallel data pipeline (PPM's "derive, don't maintain") — so the
source wiring must not be duplicated. This lives in the service layer (not the web
route, where it predated the standup consumer) so `services/standup/` can reuse it
without importing from `web/`.

Providers moved here verbatim from `web/api/routes/radar.py` (#1239 behavior preserved).
"""

from __future__ import annotations

from typing import Optional

import structlog

from services.knowledge_graph.document_service import get_document_service
from services.memory.user_history import UserHistoryService
from services.radar import (
    ConversationEntitySource,
    DocumentEntitySource,
    EntitySource,
    PlaceEntitySource,
    WorkItemEntitySource,
)

logger = structlog.get_logger(__name__)

# v1: how many candidate entities each source pulls.
CONVERSATION_FETCH = 25
WORKITEM_FETCH = 25


class ConversationHistoryProvider:
    """Adapts UserHistoryService → the ``list_summaries(user_id)`` shape
    ConversationEntitySource expects (#1021 summary fields; last_activity as ISO str)."""

    def __init__(self, service: UserHistoryService):
        self._service = service

    async def list_summaries(self, user_id: str) -> list[dict]:
        page = await self._service.get_history(
            user_id=user_id, page=1, page_size=CONVERSATION_FETCH, include_private=False
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


def filter_issues_by_assignee(issues: list, handle: Optional[str]) -> list:
    """#6: keep only issues assigned to ``handle`` (case-insensitive) — "what's on MY
    plate". No handle → all issues (opt-in; absent config preserves show-all)."""
    items = list(issues or [])
    if not handle:
        return items
    h = handle.lower()
    return [i for i in items if h in [str(a).lower() for a in (i.get("assignees") or [])]]


class WorkItemProvider:
    """Resolves the SINGLE bound user's configured repo and lists their open GitHub work
    items — Arch's #1239 beta path (user-default / ``PIPER_DEFAULT_REPO`` via the GitHub
    router's stashed user_id), scoped to "assigned to me" when a handle is configured (#6).
    Returns [] when GitHub isn't configured or no repo resolves (graceful — checks
    ``is_configured`` BEFORE ``initialize`` so an unconfigured user opens no session)."""

    async def list_for_user(self, user_id: str) -> list[dict]:
        try:
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )
            from services.integrations.github.repo_resolver import (
                read_user_github_handle,
            )

            router = GitHubIntegrationRouter()
            if not router.config_service.is_configured(user_id):
                return []
            try:
                await router.initialize(user_id=user_id)
                handle = await read_user_github_handle(user_id)  # WS-1 P4: now async (DB-backed read)
                issues = await router.get_open_issues(limit=100 if handle else WORKITEM_FETCH)
                return filter_issues_by_assignee(issues, handle)[:WORKITEM_FETCH]
            finally:
                await router.close()  # #1279: fresh router per call — release its aiohttp session
        except Exception as e:  # never let a github hiccup blank Radar/standup
            logger.warning("radar_workitem_source_failed", error=str(e))
            return []


class PlaceProvider:
    """Resolves the user's connected external surfaces (GitHub issue-tracking + Calendar)
    into Places — #1236 home-module consolidation. Mirrors the /api/v1/places route's
    construction (trust lookup → per-user github/calendar → ``PlaceService.get_visible_places``)
    so the Radar surfaces the same trust-visible Places the home "what I'm seeing" module did,
    serialized to the dict shape PlaceEntitySource consumes. Returns [] on any failure
    (graceful — a place hiccup never blanks Radar/standup)."""

    async def list_for_user(self, user_id: str) -> list[dict]:
        try:
            from uuid import UUID

            from services.place.place_service import PlaceService
            from services.shared_types import TrustStage

            # Trust stage gates which Places are visible (#684 hardness map); default NEW on failure.
            trust_stage = TrustStage.NEW
            try:
                from services.database.session_factory import AsyncSessionFactory
                from services.repositories.user_trust_profile_repository import (
                    UserTrustProfileRepository,
                )
                from services.trust import TrustComputationService

                async with AsyncSessionFactory.session_scope_fresh() as session:
                    trust_stage = await TrustComputationService(
                        UserTrustProfileRepository(session)
                    ).get_trust_stage(UUID(user_id))
            except Exception as e:
                logger.warning("radar_place_trust_lookup_failed", error=str(e))

            # GitHub source — only if the user has a configured token (keychain-first #1192).
            # Candidate tracked separately so the finally below closes it even
            # when it doesn't graduate to a source (#1279).
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
                logger.warning("radar_place_github_init_failed", error=str(e))

            # Calendar source — gated on a real authenticate() (#1196: no fabricated card).
            calendar_service = None
            try:
                from services.integrations.calendar.calendar_integration_router import (
                    CalendarIntegrationRouter,
                )

                candidate = CalendarIntegrationRouter()
                if await candidate.authenticate():
                    calendar_service = candidate
            except Exception as e:
                logger.debug("radar_place_calendar_unavailable", error=str(e))

            try:
                service = PlaceService(
                    github_router=github_router, calendar_service=calendar_service
                )
                places = await service.get_visible_places(trust_stage)
                return [
                    {
                        "id": p.id,
                        "name": p.name,
                        "summary": p.summary,
                        "source_url": p.source_url,
                        "last_fetched": p.last_fetched.isoformat() if p.last_fetched else None,
                    }
                    for p in places
                ]
            finally:
                if gh_candidate is not None:
                    await gh_candidate.close()  # #1279: release the per-call aiohttp session
        except Exception as e:  # never let a place hiccup blank Radar/standup
            logger.warning("radar_place_source_failed", error=str(e))
            return []


def build_entity_sources(user_history_service: UserHistoryService) -> list[EntitySource]:
    """The live Radar entity sources — Conversations (#1021) + Documents (#1238) +
    WorkItems (#1239) + Places (#1236, the retired home "what I'm seeing" module). The
    single wiring both the Radar feed and the standup consume. Person (#1240) is deferred
    to 1.0 (no beta source); it registers here when it lands."""
    return [
        ConversationEntitySource(ConversationHistoryProvider(user_history_service)),
        DocumentEntitySource(get_document_service()),
        WorkItemEntitySource(WorkItemProvider()),
        PlaceEntitySource(PlaceProvider()),
    ]
