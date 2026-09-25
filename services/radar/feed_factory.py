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

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Tuple

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


class WorkItemReadKind(str, Enum):
    """The three-valued read result (#1587). Names borrowed verbatim from the
    GatherOutcome contract's provenance vocabulary (``docs/internal/design/
    gather-outcome-user-facing-contract-2026-09-09.md`` §3) rather than invented —
    ``VERIFIED_EMPTY`` and ``SOURCE_FAILED`` mean exactly what they mean there. No
    typed ``GatherOutcome`` class exists in the repo yet (that epic is still
    copy-contract-only per that doc's §7), so this is a small local outcome type
    scoped to this provider, not an adoption of a shared class."""

    ITEMS = "items"
    VERIFIED_EMPTY = "verified_empty"
    SOURCE_FAILED = "source_failed"


@dataclass(frozen=True)
class WorkItemOutcome:
    """``WorkItemProvider.gather_for_user``'s honest result — distinguishes a read
    that genuinely found nothing from one that FAILED (the m-44 false-clear this
    issue exists to close), so a consumer never mistakes "couldn't check" for
    "you have none"."""

    kind: WorkItemReadKind
    items: Tuple[dict, ...] = ()

    @property
    def failed(self) -> bool:
        return self.kind is WorkItemReadKind.SOURCE_FAILED


class WorkItemProvider:
    """Resolves the SINGLE bound user's configured repo and lists their open GitHub work
    items — Arch's #1239 beta path (user-default / ``PIPER_DEFAULT_REPO`` via the GitHub
    router's stashed user_id), scoped to "assigned to me" when a handle is configured (#6).
    Returns [] when GitHub isn't configured or no repo resolves (graceful — checks the
    canonical status service BEFORE ``initialize`` so an unconfigured user opens no
    session). #1547 (audit F4): the gate is the binding-first IntegrationStatusService —
    the previous PAT-only ``config_service.is_configured`` silently blanked standup/Radar
    work items for OAuth-bound-no-PAT users.

    #1587: ``list_for_user`` is the pre-existing flattened contract, kept as a back-compat
    shim over ``gather_for_user`` — it still collapses a FAILED read to ``[]`` for any
    caller that hasn't migrated. New callers (``WorkItemEntitySource``) should use
    ``gather_for_user`` and treat FAILED honestly instead of silently rendering empty.
    """

    async def gather_for_user(
        self, user_id: str, *, include_unassigned: bool = False
    ) -> WorkItemOutcome:
        """The honest three-valued read (#1587).

        ``include_unassigned``: when True, skips the "assigned to me" filter (#6)
        even when a handle is configured. A brand-new binding often has nothing
        assigned to the user yet, so filtering by default would read as "you have
        no work items" when the repo actually has open issues — the exact failure
        mode #1536's first-contact gather built its own read to avoid (see that
        module's docstring). Default False preserves today's Radar/standup
        behavior unchanged.
        """
        try:
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )
            from services.integrations.github.repo_resolver import (
                read_user_github_handle,
            )
            from services.integrations.integration_status_service import (
                IntegrationStatusService,
            )

            if not await IntegrationStatusService().is_configured(user_id, "github"):
                # No configured GitHub connector -> genuinely nothing to read,
                # not a failed attempt.
                return WorkItemOutcome(kind=WorkItemReadKind.VERIFIED_EMPTY)
            router = GitHubIntegrationRouter()
            try:
                await router.initialize(user_id=user_id)
                handle = await read_user_github_handle(
                    user_id
                )  # WS-1 P4: now async (DB-backed read)
                issues = await router.get_open_issues(limit=100 if handle else WORKITEM_FETCH)
                filtered = (
                    list(issues or [])
                    if include_unassigned
                    else filter_issues_by_assignee(issues, handle)
                )
                items = tuple(filtered[:WORKITEM_FETCH])
                kind = WorkItemReadKind.ITEMS if items else WorkItemReadKind.VERIFIED_EMPTY
                return WorkItemOutcome(kind=kind, items=items)
            finally:
                await router.close()  # #1279: fresh router per call — release its aiohttp session
        except Exception as e:  # never let a github hiccup raise into Radar/standup — the
            # honest FAILED outcome is the signal; callers decide how to render it (#1587)
            logger.warning("radar_workitem_source_failed", error=str(e))
            return WorkItemOutcome(kind=WorkItemReadKind.SOURCE_FAILED)

    async def list_for_user(self, user_id: str) -> list[dict]:
        """Back-compat shim (#1587): flattens ``gather_for_user`` to the old
        list-or-empty contract, including the old FAILED==EMPTY conflation this
        issue exists to fix elsewhere. Preserves the previously-tested behavior
        for any caller not yet migrated to ``gather_for_user``."""
        outcome = await self.gather_for_user(user_id)
        return list(outcome.items)


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

                # #1888: scope the router to the user (as context_assembler and the standup
                # assembler already do) — unscoped, it never takes the per-user keychain
                # path, so a connected user's calendar Places were silently absent.
                candidate = CalendarIntegrationRouter(user_id=user_id)
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


class DueReminderProvider:
    """Resolves the user's due-now/overdue reminders (#1625) — the same
    ``TodoIntentHandlers.get_due_reminders`` read the conversational surfacing
    rider (#1566) consumes, so Radar and conversation can never disagree about
    what is due. Returns [] on any failure or a non-UUID principal (graceful —
    a reminder hiccup never blanks Radar; conversational #1425 honesty owns
    failure disclosure)."""

    async def list_due(self, user_id: str) -> list[str]:
        try:
            from uuid import UUID

            from services.intent_service.todo_handlers import TodoIntentHandlers

            due = await TodoIntentHandlers().get_due_reminders(UUID(user_id))
            return due or []
        except Exception as e:  # never let a reminder hiccup blank Radar
            logger.warning("radar_reminder_source_failed", error=str(e))
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
