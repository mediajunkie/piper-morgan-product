"""StandupAssembler (#1269) — derive a StandupSummary from the live entity catalog.

The morning standup is a CONSUMER of the Radar EntitySources (PPM's "derive, don't
maintain"), NOT a parallel data pipeline. It calls the SAME sources that
``services.radar.feed_factory.build_entity_sources()`` wires for Radar, then partitions
the emitted ``RadarEntity`` objects into the standup's three slots by their coarse
lifecycle label + ``attention`` recency. Every EntitySource improvement (a new source, a
richer lifecycle) flows into the standup for free.

Phase-0 reconcile (the sources emit coarse recency/label lifecycles + an ``attention``
epoch, NOT PPM's DONE/RATIFIED/IN_PROGRESS vocab — see ``dev/2026/06/18/1269-standup-gameplan.md``):

    Yesterday = Document `new` + WorkItem `closed`   (completed work)
    Today     = WorkItem `open`/`in-review` (fresh) + Document `recent`       (on my plate)
    Watch     = WorkItem `blocked` (first) + WorkItem `open`/`in-review` stale (> stale_days)

"Watch" not "Blockers" (CXO #1269 experience design): these are Piper-INFERRED potential
blockers (confidence-calibrated) — confirmed-`blocked` surface first, staleness signals
follow labeled "hasn't moved in N days". Calling them "blockers" would overstate confidence.

Conversations are NOT standup items (a chat isn't an accomplishment/priority/blocker — PM
2026-06-19); stale documents also fall into no slot. EXAMPLE / SEED provenance is filtered
out (honest-provenance, #1214/#1216)
— only OBSERVED entities are derived. NB the WorkItem source is open-only
(``get_open_issues``), so `closed` won't appear live in beta; the rule is kept correct for
when a recently-closed pull lands (#706/post-MVP).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

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
_WATCH_ICON = "⚠️"
_CALENDAR_ICON = "📅"


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
        calendar_provider: Optional[Any] = None,
    ):
        self._sources = sources
        self._now = now_epoch  # injectable for deterministic tests; None → wall clock
        self._stale_secs = stale_days * _SECONDS_PER_DAY
        # Optional calendar pull for the Today slot (CXO's "key differentiator"). DI so
        # tests inject a fake; the real one is StandupCalendarProvider. None → no calendar.
        self._calendar = calendar_provider

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
            elif slot == "watch":
                summary.watch.append(self._watch_item(e, now))
        # Watch ordering (CXO #1269): confirmed-blocked first, then staleness signals.
        # Stable sort preserves the attention-desc order within each group.
        summary.watch.sort(
            key=lambda it: 0 if (it.lifecycle_state or "").lower() == "blocked" else 1
        )
        await self._append_calendar_events(summary, user_id)
        return summary

    def _classify(self, e: RadarEntity, now: float) -> Optional[str]:
        """Map one entity to a slot name (or None to drop), per the Phase-0 reconcile."""
        et = e.entity_type
        ls = (e.lifecycle_state or "").lower()

        if et == EntityType.CONVERSATION:
            # A conversation is a chat the user HAD — not an accomplishment, a priority, or a
            # blocker — so it is NOT a standup item (PM 2026-06-19: an active conversation under
            # Yesterday rendered as "✅ <chat title>", reading as "you completed having a
            # standup"). Conversations live in the Radar + chat history, not the standup.
            return None

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
                return "watch"
            if ls in ("open", "in-review"):
                return "watch" if self._is_stale(e.attention, now) else "today"
            return None

        # PERSON (and any future type) is not a standup slot — PPM: people emerge as
        # context, they aren't listed directly.
        return None

    def _is_stale(self, attention: float, now: float) -> bool:
        """An open/in-review item is "stalled" only if it has a real timestamp older than
        the threshold. ``attention <= 0`` means the source had no timestamp — treat as
        unknown recency, NOT stale (don't fabricate a stalled blocker from missing data)."""
        return attention > 0 and (now - attention) > self._stale_secs

    def _item(self, e: RadarEntity, icon: str, meta: str = "") -> StandupItem:
        return StandupItem(
            display=e.title,
            source=_SOURCE_TAG.get(e.entity_type, "radar"),
            lifecycle_state=e.lifecycle_state,
            icon=icon,
            meta=meta,
        )

    def _watch_item(self, e: RadarEntity, now: float) -> StandupItem:
        """A Watch item carries an honest "why" in meta: confirmed-blocked items get no
        extra detail (the lifecycle label says it); stale open/in-review items get the
        age, so the surface can render "hasn't moved in N days" (CXO #1269). Unknown
        recency (no timestamp) → "recently" rather than a fabricated day-count."""
        if (e.lifecycle_state or "").lower() == "blocked":
            meta = ""
        elif e.attention > 0:
            days = max(1, int((now - e.attention) / _SECONDS_PER_DAY))
            meta = f"hasn't moved in {days} day{'s' if days != 1 else ''}"
        else:
            meta = "hasn't moved recently"
        return self._item(e, _WATCH_ICON, meta=meta)

    async def _append_calendar_events(self, summary: StandupSummary, user_id: str) -> None:
        """Append today's calendar events to the Today slot (CXO: calendar is what makes
        "today" feel real). Per-source isolation: a calendar hiccup never blanks Today."""
        if self._calendar is None:
            return
        try:
            events = await self._calendar.events_today(user_id)
        except Exception:
            logger.warning("standup_calendar_failed", exc_info=True)
            return
        for ev in events or []:
            title = (ev.get("title") or "").strip()
            if not title:
                continue
            summary.today.append(
                StandupItem(
                    display=title,
                    source="calendar",
                    icon=_CALENDAR_ICON,
                    meta=ev.get("time", ""),
                )
            )


class StandupCalendarProvider:
    """Adapts ``CalendarIntegrationRouter.get_todays_events`` → the assembler's
    ``events_today(user_id) -> [{title, time}]`` contract. Graceful-empty (returns ``[]``)
    when the calendar isn't configured / reachable — never raises into the standup. Time is
    formatted from the event's ``start_time`` as-given (the calendar integration owns
    timezone-correctness, #586). DI ``router_factory`` keeps it unit-testable."""

    def __init__(self, router_factory: Optional[Any] = None):
        self._router_factory = router_factory or self._default_router

    @staticmethod
    def _default_router(user_id: str):
        from services.integrations.calendar.calendar_integration_router import (
            CalendarIntegrationRouter,
        )

        return CalendarIntegrationRouter(user_id=user_id)

    async def events_today(self, user_id: str) -> list[dict]:
        try:
            router = self._router_factory(user_id)
            raw = await router.get_todays_events(user_id=user_id)
            return [self._normalize(ev) for ev in (raw or [])]
        except Exception:
            logger.warning("standup_calendar_provider_failed", exc_info=True)
            return []

    @staticmethod
    def _normalize(ev: dict) -> dict:
        title = (ev.get("title") or ev.get("summary") or "Event").strip()
        return {"title": title, "time": StandupCalendarProvider._fmt_time(ev.get("start_time"))}

    @staticmethod
    def _fmt_time(iso: Any) -> str:
        if not iso:
            return ""
        try:
            dt = datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
        except (ValueError, TypeError):
            return ""
        h12 = dt.hour % 12 or 12
        ampm = "am" if dt.hour < 12 else "pm"
        return f"{h12}:{dt.minute:02d}{ampm}" if dt.minute else f"{h12}{ampm}"


def build_standup_assembler(user_history_service, calendar_provider=None) -> StandupAssembler:
    """Wire a live ``StandupAssembler`` over the SAME EntitySources Radar uses
    (``build_entity_sources`` — derive-don't-maintain, one wiring not two) plus the real
    calendar provider. The standup's analog of radar's ``_build_feed``; the surfaces (the
    morning card #1269-P4, the on-demand chat skill #1269-P5) call this rather than
    constructing sources themselves.
    """
    # Lazy import: keep assembler import-light + avoid any future feed_factory↔standup cycle.
    from services.radar.feed_factory import build_entity_sources

    return StandupAssembler(
        build_entity_sources(user_history_service),
        calendar_provider=calendar_provider or StandupCalendarProvider(),
    )


async def build_user_standup_summary(user_id: Optional[str]) -> StandupSummary:
    """The on-demand standup (#1269 P5/P4): assemble a ``StandupSummary`` over a fresh
    DB-backed ``UserHistoryService`` (mirrors ``web.api.dependencies.get_user_history_service``)
    + the live Radar EntitySources + calendar. The chat query path
    (``IntentService._handle_standup_query`` → "give me my standup") and the morning card
    call this; the caller renders ``summary.to_prose()`` / ``summary.to_dict()``.

    ``user_id`` is the authenticated user (``current_user.sub`` — the SAME identity Radar
    scopes by). Anonymous (``None``/empty) → an honest empty summary, no DB session opened.
    """
    if not user_id:
        return StandupSummary()  # anonymous → honest empty (the surface renders "nothing yet")

    # Lazy imports: this is the only place the standup engine touches the DB/session layer;
    # keep it out of the import-light assembler core.
    from services.database.repositories import DBUserHistoryRepository
    from services.database.session_factory import AsyncSessionFactory
    from services.memory.user_history import UserHistoryService

    async with AsyncSessionFactory.session_scope_fresh() as session:
        uhs = UserHistoryService(DBUserHistoryRepository(session))
        return await build_standup_assembler(uhs).assemble(user_id)
