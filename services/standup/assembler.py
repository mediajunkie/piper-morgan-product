"""StandupAssembler (#1269) — derive a StandupSummary from the live entity catalog.

The morning standup is a CONSUMER of the Radar EntitySources (PPM's "derive, don't
maintain"), NOT a parallel data pipeline. It calls the SAME sources that
``services.radar.feed_factory.build_entity_sources()`` wires for Radar, then partitions
the emitted ``RadarEntity`` objects into the standup's three slots by their coarse
lifecycle label + ``attention`` recency. Every EntitySource improvement (a new source, a
richer lifecycle) flows into the standup for free.

Phase-0 reconcile (the sources emit coarse recency/label lifecycles + an ``attention``
epoch, NOT PPM's DONE/RATIFIED/IN_PROGRESS vocab — see ``dev/2026/06/18/1269-standup-gameplan.md``):

    Yesterday = Conversation `active` + Document `new` + WorkItem `closed`   (moved recently)
    Today     = WorkItem `open`/`in-review` (fresh) + Document `recent`       (on my plate)
    Blockers  = WorkItem `blocked` + WorkItem `open`/`in-review` gone stale   (> stale_days)

Idle/dormant conversations and stale documents fall into no slot (not "what moved" nor
"on my plate"). EXAMPLE / SEED provenance is filtered out (honest-provenance, #1214/#1216)
— only OBSERVED entities are derived. NB the WorkItem source is open-only
(``get_open_issues``), so `closed` won't appear live in beta; the rule is kept correct for
when a recently-closed pull lands (#706/post-MVP).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

import structlog

from services.domain.models import StandupItem, StandupSummary
from services.radar.models import EntityType, Provenance, RadarEntity
from services.radar.sources import EntitySource

logger = structlog.get_logger(__name__)

_DEFAULT_STALE_DAYS = 3
_SECONDS_PER_DAY = 86400.0

# entity_type → the StandupItem.source tag marking a derived-from-observed item, so the
# surface can distinguish these from user-captured / commit-sourced items.
_SOURCE_TAG = {
    EntityType.CONVERSATION: "radar:conversation",
    EntityType.DOCUMENT: "radar:document",
    EntityType.WORK_ITEM: "radar:work_item",
    EntityType.PERSON: "radar:person",
}

# per-slot presentation hint for standup.html (honest + minimal).
_YESTERDAY_ICON = "✅"
_TODAY_ICON = "🎯"
_BLOCKER_ICON = "⚠️"


class StandupAssembler:
    """Derives a ``StandupSummary`` from a list of EntitySources (the SAME wiring Radar
    uses via ``build_entity_sources()``). Pure derivation — reads no DB directly; the
    sources own all I/O and their own per-source graceful-empty behavior.
    """

    def __init__(
        self,
        sources: list[EntitySource],
        now_epoch: Optional[float] = None,
        stale_days: int = _DEFAULT_STALE_DAYS,
    ):
        self._sources = sources
        self._now = now_epoch  # injectable for deterministic tests; None → wall clock
        self._stale_secs = stale_days * _SECONDS_PER_DAY

    def _now_epoch(self) -> float:
        return self._now if self._now is not None else datetime.now(timezone.utc).timestamp()

    async def assemble(self, user_id: str) -> StandupSummary:
        gathered: list[RadarEntity] = []
        for source in self._sources:
            # Per-source isolation (mirror RadarFeed.assemble): a failing/slow source must
            # NEVER blank the standup — skip it, surface the rest.
            try:
                gathered.extend(await source.fetch(user_id))
            except Exception:
                logger.warning("standup_source_failed", source=type(source).__name__, exc_info=True)

        observed = [e for e in gathered if e.provenance == Provenance.OBSERVED]
        # Attention-first within each slot: iterate most-recent-first so appends preserve
        # recency order (Today ordering uses recency for now; attention-scoring is post-MVP).
        observed.sort(key=lambda e: e.attention, reverse=True)

        now = self._now_epoch()
        summary = StandupSummary()
        for e in observed:
            slot = self._classify(e, now)
            if slot == "yesterday":
                summary.yesterday.append(self._item(e, _YESTERDAY_ICON))
            elif slot == "today":
                summary.today.append(self._item(e, _TODAY_ICON))
            elif slot == "blockers":
                summary.blockers.append(self._item(e, _BLOCKER_ICON))
        return summary

    def _classify(self, e: RadarEntity, now: float) -> Optional[str]:
        """Map one entity to a slot name (or None to drop), per the Phase-0 reconcile."""
        et = e.entity_type
        ls = (e.lifecycle_state or "").lower()

        if et == EntityType.CONVERSATION:
            # Only recently-active conversations are "what moved"; idle/dormant drop.
            return "yesterday" if ls == "active" else None

        if et == EntityType.DOCUMENT:
            if ls == "new":  # touched <24h → moved recently
                return "yesterday"
            if ls == "recent":  # touched <7d, still warm → on my plate
                return "today"
            return None  # stale → drop

        if et == EntityType.WORK_ITEM:
            if ls == "closed":
                return "yesterday"
            if ls == "blocked":
                return "blockers"
            if ls in ("open", "in-review"):
                return "blockers" if self._is_stale(e.attention, now) else "today"
            return None

        # PERSON (and any future type) is not a standup slot — PPM: people emerge as
        # context, they aren't listed directly.
        return None

    def _is_stale(self, attention: float, now: float) -> bool:
        """An open/in-review item is "stalled" only if it has a real timestamp older than
        the threshold. ``attention <= 0`` means the source had no timestamp — treat as
        unknown recency, NOT stale (don't fabricate a stalled blocker from missing data)."""
        return attention > 0 and (now - attention) > self._stale_secs

    def _item(self, e: RadarEntity, icon: str) -> StandupItem:
        return StandupItem(
            display=e.title,
            source=_SOURCE_TAG.get(e.entity_type, "radar"),
            lifecycle_state=e.lifecycle_state,
            icon=icon,
        )
