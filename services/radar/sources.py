"""Radar entity sources — #1236.

An EntitySource turns some backing store into RadarEntities. ConversationEntitySource
wraps the #1021 user-history (the only live entity type today); WorkItem / Person /
Document sources register here as PPM lands the entity catalog (#706) — the surface
does not change when they do. That is the point of this seam.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Protocol, runtime_checkable

from .models import EntityType, Provenance, RadarEntity


@runtime_checkable
class EntitySource(Protocol):
    async def fetch(self, user_id: str) -> list[RadarEntity]: ...


def _parse_ts(value: Any) -> float:
    """ISO timestamp (str, optionally 'Z') → epoch seconds; 0.0 if missing/unparseable."""
    if not value:
        return 0.0
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).timestamp()
    except (ValueError, TypeError):
        return 0.0


def _derive_conversation_lifecycle(last_activity_epoch: float) -> str:
    """v1 coarse lifecycle from recency — #1021 has no lifecycle field for conversations.
    Richer lifecycle arrives with PPM's entity model (#706)."""
    if last_activity_epoch <= 0:
        return "idle"
    age_h = (datetime.now(timezone.utc).timestamp() - last_activity_epoch) / 3600.0
    if age_h < 24:
        return "active"
    if age_h < 24 * 7:
        return "idle"
    return "dormant"


def _get(summary: Any, key: str, default: Any = None) -> Any:
    return summary.get(key, default) if isinstance(summary, dict) else getattr(summary, key, default)


class ConversationEntitySource:
    """Maps #1021 conversation summaries → Conversation RadarEntities.

    All conversations are OBSERVED — they are the user's real conversations (the
    seed/example provenance distinction applies to derived surfaces like insights,
    not to a user's own chats).
    """

    def __init__(self, history_provider: Any):
        # history_provider: object exposing `async list_summaries(user_id) -> list[summary]`,
        # each summary carrying #1021 ConversationSummaryResponse fields.
        self._history = history_provider

    async def fetch(self, user_id: str) -> list[RadarEntity]:
        summaries = await self._history.list_summaries(user_id)
        entities: list[RadarEntity] = []
        for s in summaries or []:
            last_activity = _get(s, "last_activity")
            attention = _parse_ts(last_activity)
            turn_count = _get(s, "turn_count", 0) or 0
            meta_bits: list[str] = []
            if last_activity:
                meta_bits.append(f"last activity {last_activity}")
            meta_bits.append(f"{turn_count} turn{'' if turn_count == 1 else 's'}")
            entities.append(
                RadarEntity(
                    entity_type=EntityType.CONVERSATION,
                    title=_get(s, "title") or "(untitled)",
                    lifecycle_state=_derive_conversation_lifecycle(attention),
                    provenance=Provenance.OBSERVED,
                    meta=" · ".join(meta_bits),
                    attention=attention,
                    ref=_get(s, "conversation_id"),
                )
            )
        return entities


def _derive_document_lifecycle(last_touch_epoch: float) -> str:
    """v1 coarse lifecycle from recency — the documents table carries timestamps, not a
    workflow-status field. Richer lifecycle arrives with PPM's entity model (#706)."""
    if last_touch_epoch <= 0:
        return "stale"
    age_h = (datetime.now(timezone.utc).timestamp() - last_touch_epoch) / 3600.0
    if age_h < 24:
        return "new"
    if age_h < 24 * 7:
        return "recent"
    return "stale"


class DocumentEntitySource:
    """Maps the user's documents (#1238) → Document RadarEntities.

    Wraps ``DocumentService.list_for_user`` (owner-scoped — the user's OWN docs; the
    global PM knowledge base is shared reasoning-context for the reads, not personal-radar
    items). All listed documents are OBSERVED (they are the user's real uploaded docs);
    lifecycle is derived from real timestamps (no fabrication — honest provenance).
    """

    def __init__(self, document_service: Any):
        # document_service: object exposing `async list_for_user(user_id) -> list[dict]`
        # with keys: chromadb_base_id, title, source, created_at, updated_at.
        self._docs = document_service

    async def fetch(self, user_id: str) -> list[RadarEntity]:
        rows = await self._docs.list_for_user(user_id)
        entities: list[RadarEntity] = []
        for r in rows or []:
            last_touch = _get(r, "updated_at") or _get(r, "created_at")
            attention = _parse_ts(last_touch)
            meta_bits: list[str] = []
            source = _get(r, "source")
            if source:
                meta_bits.append(str(source).rsplit("/", 1)[-1])  # filename
            if last_touch:
                meta_bits.append(f"updated {last_touch}")
            entities.append(
                RadarEntity(
                    entity_type=EntityType.DOCUMENT,
                    title=_get(r, "title") or "(untitled document)",
                    lifecycle_state=_derive_document_lifecycle(attention),
                    provenance=Provenance.OBSERVED,
                    meta=" · ".join(meta_bits),
                    attention=attention,
                    ref=_get(r, "chromadb_base_id"),
                )
            )
        return entities


def _derive_workitem_lifecycle(state: Any, labels: Any) -> str:
    """Lifecycle from the work item's REAL state + labels (no fabrication — honest
    provenance). closed → closed; open refined by label → blocked / in-review / open.
    A richer status field arrives with PPM's entity model (#706)."""
    if str(state or "").lower() == "closed":
        return "closed"
    labels_lower = {str(label).lower() for label in (labels or [])}
    if any("block" in label for label in labels_lower):
        return "blocked"
    if any(("review" in label) or ("in progress" in label) or ("in-progress" in label) for label in labels_lower):
        return "in-review"
    return "open"


class WorkItemEntitySource:
    """Maps the bound user's GitHub work items (#1239) → WorkItem RadarEntities.

    Beta path (Arch 2026-06-17, m-40 layer-then-migrate): the route provider scopes to
    the SINGLE bound user's configured repo via the existing repo-resolution (user-default
    / ``PIPER_DEFAULT_REPO``) — NOT the full #1233 multi-identity unification. When #1233
    lands, the user→repo mapping generalizes with no rework (the single-user binding is the
    degenerate case, not a throwaway). All listed issues are OBSERVED (the user's real work
    items); lifecycle is derived from real issue state + labels (no fabrication).
    """

    def __init__(self, work_item_provider: Any):
        # work_item_provider: object exposing `async list_for_user(user_id) -> list[dict]`,
        # each dict carrying GitHub-issue keys: number, title, state, updated_at/created_at,
        # uri|html_url, labels (list[str]).
        self._provider = work_item_provider

    async def fetch(self, user_id: str) -> list[RadarEntity]:
        rows = await self._provider.list_for_user(user_id)
        entities: list[RadarEntity] = []
        for r in rows or []:
            last_touch = _get(r, "updated_at") or _get(r, "created_at")
            attention = _parse_ts(last_touch)
            number = _get(r, "number")
            meta_bits: list[str] = []
            if number is not None:
                meta_bits.append(f"#{number}")
            if last_touch:
                meta_bits.append(f"updated {last_touch}")
            entities.append(
                RadarEntity(
                    entity_type=EntityType.WORK_ITEM,
                    title=_get(r, "title") or "(untitled work item)",
                    lifecycle_state=_derive_workitem_lifecycle(_get(r, "state"), _get(r, "labels")),
                    provenance=Provenance.OBSERVED,
                    meta=" · ".join(meta_bits),
                    attention=attention,
                    ref=_get(r, "uri") or _get(r, "html_url"),
                )
            )
        return entities


class PlaceEntitySource:
    """Maps the user's Places (#684 "what I'm seeing" — connected external surfaces like
    GitHub issue-tracking + Calendar) → WorkItem RadarEntities.

    #1236 home-module consolidation: the home "what i'm seeing" module is retired into the
    Radar. CXO call (2026-06-19): Places map onto the existing ``work_item`` type (no schema
    expansion for beta — a Place is an external surface where work happens; close enough) with
    a fixed ``active`` lifecycle. All Places are OBSERVED — PlaceService only yields real
    connected sources (unconnected/failing ones drop to None upstream), so no fabrication.
    """

    def __init__(self, place_provider: Any):
        # place_provider: object exposing `async list_for_user(user_id) -> list[dict]`
        # with keys: id, name, summary, source_url, last_fetched (ISO str).
        self._provider = place_provider

    async def fetch(self, user_id: str) -> list[RadarEntity]:
        rows = await self._provider.list_for_user(user_id)
        entities: list[RadarEntity] = []
        for r in rows or []:
            attention = _parse_ts(_get(r, "last_fetched"))
            entities.append(
                RadarEntity(
                    entity_type=EntityType.WORK_ITEM,
                    title=_get(r, "name") or "(unnamed place)",
                    lifecycle_state="active",  # CXO: Places render with a fixed active/neutral lifecycle
                    provenance=Provenance.OBSERVED,
                    meta=_get(r, "summary") or "",
                    attention=attention,
                    ref=_get(r, "source_url") or _get(r, "id"),
                )
            )
        return entities
