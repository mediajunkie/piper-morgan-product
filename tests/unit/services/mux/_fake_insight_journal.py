"""
Test double for InsightJournal — in-memory, no DB.

Mirrors the InsightJournal API surface (post-#1035 rewrite) so tests
that use the journal as a *dependency* for testing other classes
(CompostingPipeline, CompostingScheduler, premonition surfacers, etc.)
don't need an AsyncSessionFactory or DB session.

This is explicitly a TEST DOUBLE — never imported from production code.
The naming `FakeInsightJournal` makes the test/prod boundary visible.

Production InsightJournal (`services/mux/composting_pipeline.py`) is
async + repository-backed. Tests that need to verify production behavior
(persistence, transaction-boundary, etc.) use `InsightRepository` against
in-memory SQLite per the #1035 Phase 3 pattern at
`tests/unit/services/test_insight_repository_1035.py`.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from services.mux.composting_pipeline import SurfaceableInsight


class FakeInsightJournal:
    """In-memory test double of InsightJournal.

    Implements the same async API as InsightJournal (post-#1035) using
    in-memory dicts. Suitable for tests that depend on InsightJournal's
    surface behavior but don't exercise persistence semantics.
    """

    def __init__(self):
        self._insights: Dict[str, SurfaceableInsight] = {}
        self._by_user: Dict[str, List[str]] = {}
        self._by_object: Dict[str, List[str]] = {}

    async def add(self, insight: SurfaceableInsight) -> SurfaceableInsight:
        self._insights[insight.id] = insight
        if insight.user_id:
            self._by_user.setdefault(insight.user_id, []).append(insight.id)
        if insight.object_id:
            self._by_object.setdefault(insight.object_id, []).append(insight.id)
        return insight

    async def get(self, insight_id: str) -> Optional[SurfaceableInsight]:
        return self._insights.get(insight_id)

    async def get_unsurfaced(
        self,
        user_id: str,
        min_confidence: float = 0.75,
        trust_stage: int = 3,
        limit: int = 10,
    ) -> List[SurfaceableInsight]:
        if user_id not in self._by_user:
            return []
        candidates: List[SurfaceableInsight] = []
        for iid in self._by_user[user_id]:
            insight = self._insights.get(iid)
            if insight is None:
                continue
            if not insight.is_surfaceable(trust_stage):
                continue
            if insight.learning and insight.learning.confidence < min_confidence:
                continue
            if insight.surfaced_count == 0:
                candidates.append(insight)
            if len(candidates) >= limit:
                break
        candidates.sort(
            key=lambda i: (
                i.requires_attention,
                i.learning.confidence if i.learning else 0,
            ),
            reverse=True,
        )
        return candidates[:limit]

    async def get_for_context(
        self,
        user_id: str,
        context_entities: Optional[List[str]] = None,
        context_topics: Optional[List[str]] = None,
        trust_stage: int = 1,
        limit: int = 5,
    ) -> List[SurfaceableInsight]:
        if user_id not in self._by_user:
            return []
        entity_set = set(context_entities or [])
        topic_set = set(context_topics or [])
        scored = []
        for iid in self._by_user[user_id]:
            insight = self._insights.get(iid)
            if insight is None:
                continue
            if not insight.is_surfaceable(trust_stage):
                continue
            relevance = 0
            if insight.learning:
                for ent in insight.learning.applies_to_entities:
                    if ent in entity_set:
                        relevance += 2
                for tag in insight.learning.topic_tags:
                    if tag in topic_set:
                        relevance += 1
            for tag in insight.context_tags:
                if tag in entity_set or tag in topic_set:
                    relevance += 1
            if relevance > 0:
                scored.append((relevance, insight))
        scored.sort(
            key=lambda x: (x[0], x[1].learning.confidence if x[1].learning else 0),
            reverse=True,
        )
        return [s[1] for s in scored[:limit]]

    async def mark_surfaced(self, insight_id: str, response: str) -> Optional[SurfaceableInsight]:
        insight = self._insights.get(insight_id)
        if insight is None:
            return None
        insight.surfaced_count += 1
        insight.last_surfaced = datetime.now()
        insight.user_response = response
        return insight

    async def get_for_object(
        self, object_id: str, user_id: Optional[str] = None
    ) -> List[SurfaceableInsight]:
        # #1252 (a,3): mirror the real journal — scope by owner when provided.
        if object_id not in self._by_object:
            return []
        return [
            self._insights[iid]
            for iid in self._by_object[object_id]
            if iid in self._insights and (user_id is None or self._insights[iid].user_id == user_id)
        ]

    async def count(self, user_id: Optional[str] = None) -> int:
        if user_id is None:
            return len(self._insights)
        if user_id not in self._by_user:
            return 0
        return len(self._by_user[user_id])

    async def clear(self, user_id: str) -> int:
        if user_id not in self._by_user:
            return 0
        ids_to_remove = list(self._by_user[user_id])
        for iid in ids_to_remove:
            insight = self._insights.pop(iid, None)
            if insight and insight.object_id in self._by_object:
                try:
                    self._by_object[insight.object_id].remove(iid)
                except ValueError:
                    pass
        del self._by_user[user_id]
        return len(ids_to_remove)
