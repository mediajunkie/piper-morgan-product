"""RadarFeed — assembles RadarEntities from sources into a RadarView (#1236).

Domain logic, server-side (NOT client-trusted): the honest-provenance filter
(#1214/#1216), attention-first ordering, and two-state selection (default real-only /
empty + one teaching example). The JS surface just renders the resulting RadarView.
"""

from __future__ import annotations

import structlog

from .models import EntityType, Provenance, RadarEntity, RadarView
from .sources import EntitySource

logger = structlog.get_logger(__name__)


def _example_entity() -> RadarEntity:
    """Empty-state teaching card (CXO mockup) — unmistakably an example, never observed."""
    return RadarEntity(
        entity_type=EntityType.WORK_ITEM,
        title="A blocker you flagged",
        lifecycle_state="blocked",
        provenance=Provenance.EXAMPLE,
        meta="…with what's holding it up, and what you can do about it.",
        attention=0.0,
    )


class RadarFeed:
    """Domain service: gather → filter (observed-only) → order (attention-first) → state."""

    def __init__(self, sources: list[EntitySource]):
        self._sources = sources

    async def assemble(self, user_id: str) -> RadarView:
        gathered: list[RadarEntity] = []
        for source in self._sources:
            # Per-source isolation (#1238): a failing/slow source must never blank
            # Radar — skip it and surface the others.
            try:
                gathered.extend(await source.fetch(user_id))
            except Exception:
                logger.warning("radar_source_failed", source=type(source).__name__, exc_info=True)

        # Honest provenance: the default view is real-only (#1214/#1216) — seed/dev never shown.
        observed = [e for e in gathered if e.provenance == Provenance.OBSERVED]
        if not observed:
            return RadarView(state="empty", entities=[_example_entity()])

        # Attention-first: most-active / recently-changed at top, entity types mixed.
        observed.sort(key=lambda e: e.attention, reverse=True)
        return RadarView(state="populated", entities=observed)
