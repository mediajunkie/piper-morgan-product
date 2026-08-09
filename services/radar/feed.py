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
    """Empty-state teaching card — unmistakably an example, never observed.

    #1476: the previous copy ("A blocker you flagged" with a live "blocked" state
    chip) read as a REAL blocked item to a first-time user, who searched the UI
    for the blocked thing, failed, and read it as breakage. HOST's rule: a
    surfaced signal must be traceable to its subject; an unresolvable alert is an
    invitation to imagine the failure. The example must therefore never claim a
    live lifecycle state or name a ghost referent.
    """
    return RadarEntity(
        entity_type=EntityType.WORK_ITEM,
        title="Example — how a blocked item appears",
        lifecycle_state="example",
        provenance=Provenance.EXAMPLE,
        meta="Not a real item — nothing of yours is blocked. When something is, "
        "it shows here with what's holding it up.",
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

        # #1476: a "blocked" card whose referent can't be opened at all (no ref)
        # is a ghost alert — the user can't trace the signal to its subject.
        # Suppress it and log, rather than render an unresolvable "blocked".
        kept: list[RadarEntity] = []
        for e in observed:
            if e.lifecycle_state == "blocked" and not e.ref:
                logger.warning(
                    "radar_blocked_card_suppressed_no_referent",
                    title=e.title,
                    entity_type=str(e.entity_type),
                )
                continue
            kept.append(e)
        observed = kept

        if not observed:
            return RadarView(state="empty", entities=[_example_entity()])

        # Attention-first: most-active / recently-changed at top, entity types mixed.
        observed.sort(key=lambda e: e.attention, reverse=True)
        return RadarView(state="populated", entities=observed)
