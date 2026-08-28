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


def _coming_soon_entity() -> RadarEntity:
    """#1635 ambient-presence false door — CXO's copy VERBATIM (design memo 2026-08-27),
    per PM's Radar-card decision. Two binding rules, both structural here:

    Rule 1 — never outranks real held state, never stands alone: appended AFTER the
    attention sort (unconditionally last, never pinned, never attention-ordered) and
    only in the populated branch — zero real entities → suppressed entirely (the
    empty-state/FTUX path owns the empty moment; a placeholder faking fullness would
    be display-side fabrication).

    Rule 2 — copy claims the FUTURE, never the present: "not watching anything yet"
    is load-bearing self-honesty against the fabrication class. EXAMPLE provenance
    drives the existing dashed `radar-card--example` style in the JS renderers, so
    the card is visually distinct from real held state. No ref → not clickable.
    """
    return RadarEntity(
        entity_type=EntityType.COMING_SOON,
        title="Piper will be able to watch for changes and bring you what matters",
        lifecycle_state="preview",
        provenance=Provenance.EXAMPLE,
        meta="Coming soon — not watching anything yet. Briefings when something "
        "needs you, not notification noise.",
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
        # #1625: pinned entities (due reminders) lock ABOVE the attention ordering —
        # PM's ruling gives the persistent surface ownership of reminder persistence.
        observed.sort(key=lambda e: (not e.pinned, -e.attention))
        # #1635: ambient-presence coming-soon placeholder — appended after the sort so
        # it is unconditionally LAST (below every real entity), and only on this branch
        # (zero real entities → the empty state above renders, placeholder suppressed).
        return RadarView(state="populated", entities=observed + [_coming_soon_entity()])
