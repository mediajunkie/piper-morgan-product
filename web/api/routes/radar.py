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
from services.knowledge_graph.document_service import get_document_service
from services.memory.user_history import UserHistoryService
from services.radar import (
    ConversationEntitySource,
    DocumentEntitySource,
    RadarFeed,
    WorkItemEntitySource,
)
from web.api.dependencies import get_user_history_service

router = APIRouter(prefix="/api/v1/radar", tags=["radar"])
logger = structlog.get_logger(__name__)

# v1: how many conversations the conversation source pulls as candidate entities.
_CONVERSATION_FETCH = 25
# v1: how many open work items the work-item source pulls as candidate entities.
_WORKITEM_FETCH = 25


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


def _filter_issues_by_assignee(issues: list, handle: Optional[str]) -> list:
    """#6: keep only issues assigned to ``handle`` (case-insensitive), so Radar shows
    "what's on MY plate" not every open issue in the repo. No handle → all issues (the
    assignee filter is OPT-IN — absent config preserves the prior show-all behavior).
    Forward-compatible with #1233 (one configured handle now → unified identity later)."""
    items = list(issues or [])
    if not handle:
        return items
    h = handle.lower()
    return [
        i for i in items if h in [str(a).lower() for a in (i.get("assignees") or [])]
    ]


class _WorkItemProvider:
    """Resolves the SINGLE bound user's configured repo and lists their open GitHub
    work items — Arch's beta path (#1239, m-40 layer-then-migrate): reuse the existing
    repo-resolution (user-default / ``PIPER_DEFAULT_REPO`` via the GitHub router's stashed
    user_id), NOT new user-scoping infra and NOT the full #1233 identity unification.

    ``get_open_issues`` auto-resolves the repo from the user_id stashed by ``initialize``
    (the Slack socket-runner's single-bound-user pattern applied to GitHub). If a GitHub
    handle is configured (#6), the issues are scoped to "assigned to me"; otherwise all
    open issues are shown. Returns [] when GitHub isn't configured or no repo resolves —
    graceful empty (RadarFeed's per-source isolation also guards the feed)."""

    async def list_for_user(self, user_id: str) -> list[dict]:
        try:
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )
            from services.integrations.github.repo_resolver import (
                read_user_github_handle,
            )

            router = GitHubIntegrationRouter()
            # Check config BEFORE initialize() — config_service is set at construction,
            # but initialize() opens the adapter's network session. Skipping it for an
            # unconfigured user avoids opening (and leaking) a session for nothing.
            if not router.config_service.is_configured(user_id):
                return []
            # initialize(user_id) stashes the user_id so get_open_issues resolves the
            # user-default repo (→ PIPER_DEFAULT_REPO) — the single-bound-user scope.
            await router.initialize(user_id=user_id)
            # #6: scope to "assigned to me" when a handle is configured. Fetch wider when
            # filtering so assigned issues aren't missed beyond the display cap.
            handle = read_user_github_handle(user_id)
            issues = await router.get_open_issues(limit=100 if handle else _WORKITEM_FETCH)
            return _filter_issues_by_assignee(issues, handle)[:_WORKITEM_FETCH]
        except Exception as e:  # never let a github hiccup blank Radar
            logger.warning("radar_workitem_source_failed", error=str(e))
            return []


def _build_feed(service: UserHistoryService) -> RadarFeed:
    """Live entity sources: Conversations (#1021) + Documents (#1238) + WorkItems (#1239,
    single-bound-user→repo beta scope). Person registers here as PPM lands the entity
    catalog (#706); no surface change when it does. Per-source isolation in RadarFeed means
    a failing source never blanks the feed."""
    return RadarFeed(
        [
            ConversationEntitySource(_ConversationHistoryProvider(service)),
            DocumentEntitySource(get_document_service()),
            WorkItemEntitySource(_WorkItemProvider()),
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
