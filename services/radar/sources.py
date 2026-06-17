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
