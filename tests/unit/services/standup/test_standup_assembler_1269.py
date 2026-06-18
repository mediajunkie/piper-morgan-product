"""#1269 — StandupAssembler + StandupSummary.to_prose(): the morning standup reconceived
as a DERIVED view over the live entity catalog (the same EntitySources Radar consumes),
not a bespoke data pipeline. Tests the real partitioning (entities → StandupSummary slots)
with FAKE EntitySources — we control the emitted RadarEntities directly rather than mocking
internals (the #490 wiring-test lesson).

The reconciled slot mapping (Phase-0 finding — the sources emit coarse recency/label
lifecycles + an `attention` epoch, NOT PPM's DONE/RATIFIED vocab):
  Yesterday  = Conversation `active` + Document `new` + WorkItem `closed`   (moved recently)
  Today      = WorkItem `open`/`in-review` (fresh) + Document `recent`       (on my plate)
  Watch      = WorkItem `blocked` (first) + WorkItem `open`/`in-review` stale (>stale_days)
Dropped (in no slot): idle/dormant conversations, stale documents.

The third slot is "Watch" not "Blockers" (CXO #1269): Piper-inferred potential blockers,
confidence-calibrated — confirmed-blocked surface first, staleness signals follow.
"""

from __future__ import annotations

from services.domain.models import StandupItem, StandupSummary
from services.radar.models import EntityType, Provenance, RadarEntity
from services.standup.assembler import StandupAssembler

NOW = 1_000_000_000.0
H = 3600.0
D = 86400.0


def _ent(etype, title, lifecycle, attention, provenance=Provenance.OBSERVED):
    return RadarEntity(
        entity_type=etype,
        title=title,
        lifecycle_state=lifecycle,
        provenance=provenance,
        meta="",
        attention=attention,
        ref=None,
    )


class _FakeSource:
    def __init__(self, entities):
        self._entities = entities

    async def fetch(self, user_id):
        return list(self._entities)


class _BoomSource:
    async def fetch(self, user_id):
        raise RuntimeError("source down")


# --- the canonical mixed fixture, split across three sources ---


def _sources():
    conv = _FakeSource(
        [
            _ent(EntityType.CONVERSATION, "talked perf", "active", NOW - 12 * H),  # → Yesterday
            _ent(EntityType.CONVERSATION, "old thread", "dormant", NOW - 30 * D),  # → dropped
        ]
    )
    doc = _FakeSource(
        [
            _ent(EntityType.DOCUMENT, "spec draft", "new", NOW - 6 * H),  # → Yesterday
            _ent(EntityType.DOCUMENT, "design doc", "recent", NOW - 2 * D),  # → Today
            _ent(EntityType.DOCUMENT, "ancient", "stale", NOW - 40 * D),  # → dropped
        ]
    )
    wi = _FakeSource(
        [
            _ent(EntityType.WORK_ITEM, "open-fresh", "open", NOW - 12 * H),  # → Today
            _ent(EntityType.WORK_ITEM, "review-fresh", "in-review", NOW - 2 * D),  # → Today
            _ent(EntityType.WORK_ITEM, "open-stale", "open", NOW - 5 * D),  # → Watch (stale)
            _ent(EntityType.WORK_ITEM, "blocked-now", "blocked", NOW - 1 * H),  # → Watch (blocked)
            _ent(EntityType.WORK_ITEM, "done-y", "closed", NOW - 12 * H),  # → Yesterday
            _ent(EntityType.WORK_ITEM, "ex", "blocked", 0.0, Provenance.EXAMPLE),  # → excluded
        ]
    )
    return [conv, doc, wi]


def _displays(items):
    return {it.display for it in items}


class TestStandupAssemblerSlotMapping:
    async def test_yesterday_is_recent_movement(self):
        summary = await StandupAssembler(_sources(), now_epoch=NOW).assemble("u1")
        assert isinstance(summary, StandupSummary)
        assert _displays(summary.yesterday) == {"talked perf", "spec draft", "done-y"}

    async def test_today_is_open_plate(self):
        summary = await StandupAssembler(_sources(), now_epoch=NOW).assemble("u1")
        assert _displays(summary.today) == {"open-fresh", "review-fresh", "design doc"}

    async def test_watch_is_blocked_or_stale(self):
        summary = await StandupAssembler(_sources(), now_epoch=NOW).assemble("u1")
        assert _displays(summary.watch) == {"blocked-now", "open-stale"}

    async def test_idle_and_stale_and_example_are_dropped(self):
        summary = await StandupAssembler(_sources(), now_epoch=NOW).assemble("u1")
        everything = (
            _displays(summary.yesterday) | _displays(summary.today) | _displays(summary.watch)
        )
        assert "old thread" not in everything  # dormant conversation
        assert "ancient" not in everything  # stale document
        assert "ex" not in everything  # EXAMPLE provenance (honest-provenance filter)

    async def test_items_are_standupitems_with_provenance_source_and_lifecycle(self):
        summary = await StandupAssembler(_sources(), now_epoch=NOW).assemble("u1")
        all_items = summary.yesterday + summary.today + summary.watch
        assert all(isinstance(it, StandupItem) for it in all_items)
        # source tags the derived origin so the surface can tell derived-from-observed
        # items apart from captured/commit items.
        by_display = {it.display: it for it in all_items}
        assert by_display["talked perf"].source == "radar:conversation"
        assert by_display["spec draft"].source == "radar:document"
        assert by_display["open-fresh"].source == "radar:work_item"
        # coarse lifecycle label carried through verbatim
        assert by_display["open-fresh"].lifecycle_state == "open"
        assert by_display["blocked-now"].lifecycle_state == "blocked"


class TestStandupAssemblerWatch:
    async def test_blocked_surfaces_before_stale(self):
        # CXO #1269: confirmed-blocked first (higher confidence), then staleness signals.
        summary = await StandupAssembler(_sources(), now_epoch=NOW).assemble("u1")
        assert [it.display for it in summary.watch] == ["blocked-now", "open-stale"]

    async def test_stale_item_carries_age_in_meta_blocked_does_not(self):
        summary = await StandupAssembler(_sources(), now_epoch=NOW).assemble("u1")
        by = {it.display: it for it in summary.watch}
        assert by["open-stale"].meta == "hasn't moved in 5 days"  # NOW-5d
        assert by["blocked-now"].meta == ""  # lifecycle says "blocked"; no fabricated age


class TestStandupAssemblerOrderingAndResilience:
    async def test_within_slot_attention_first(self):
        # Today holds open-fresh (NOW-12h), review-fresh (NOW-2d), design doc (NOW-2d):
        # most-recent attention sorts first.
        summary = await StandupAssembler(_sources(), now_epoch=NOW).assemble("u1")
        assert summary.today[0].display == "open-fresh"

    async def test_per_source_isolation_a_failing_source_never_blanks_the_standup(self):
        conv, doc, wi = _sources()
        summary = await StandupAssembler([conv, _BoomSource(), wi], now_epoch=NOW).assemble("u1")
        # conv + wi still populate; the boom source just contributes nothing.
        assert "talked perf" in _displays(summary.yesterday)
        assert "open-fresh" in _displays(summary.today)
        assert "blocked-now" in _displays(summary.watch)

    async def test_empty_sources_yield_empty_summary_not_fabrication(self):
        summary = await StandupAssembler([_FakeSource([])], now_epoch=NOW).assemble("u1")
        assert summary.is_empty()
        assert summary.yesterday == [] and summary.today == [] and summary.watch == []

    async def test_open_item_with_unknown_recency_is_today_not_stale_watch(self):
        # attention<=0 means the source had no timestamp — DON'T fabricate a "stalled"
        # signal from missing data; treat as on-plate (Today).
        wi = _FakeSource([_ent(EntityType.WORK_ITEM, "no-ts", "open", 0.0)])
        summary = await StandupAssembler([wi], now_epoch=NOW).assemble("u1")
        assert "no-ts" in _displays(summary.today)
        assert "no-ts" not in _displays(summary.watch)

    async def test_stale_threshold_is_configurable(self):
        # An open item 2 days old is Today by default (3d) but Watch at stale_days=1.
        wi = _FakeSource([_ent(EntityType.WORK_ITEM, "two-day", "open", NOW - 2 * D)])
        default_summary = await StandupAssembler([wi], now_epoch=NOW).assemble("u1")
        assert "two-day" in _displays(default_summary.today)
        tight_summary = await StandupAssembler([wi], now_epoch=NOW, stale_days=1).assemble("u1")
        assert "two-day" in _displays(tight_summary.watch)


# --- P3: StandupSummary.to_prose() — honest spoken-standup narrative (tested directly) ---


def _si(display, lifecycle, source="radar:work_item", meta=""):
    return StandupItem(display=display, source=source, lifecycle_state=lifecycle, meta=meta)


class TestStandupSummaryProse:
    def test_empty_summary_is_honest_not_fabricated(self):
        prose = StandupSummary().to_prose()
        assert "Nothing to show yet" in prose
        # no fabricated slot content / fallback copy
        assert "Yesterday" not in prose

    def test_yesterday_uses_verbs_and_actual_things_not_counts(self):
        s = StandupSummary(
            yesterday=[
                _si("auth PR", "closed"),
                _si("API spec", "new", source="radar:document"),
                _si("perf chat", "active", source="radar:conversation"),
            ]
        )
        prose = s.to_prose()
        assert "**Yesterday**" in prose
        assert "closed" in prose and "auth PR" in prose
        assert "updated" in prose and "API spec" in prose
        assert "discussed" in prose and "perf chat" in prose
        assert "3 items" not in prose  # the actual things, not a count

    def test_today_is_working_on(self):
        prose = StandupSummary(today=[_si("onboarding flow", "open")]).to_prose()
        assert "**Today**" in prose
        assert "working on" in prose and "onboarding flow" in prose

    def test_watch_blocked_first_then_stale_with_age(self):
        s = StandupSummary(
            watch=[
                _si("billing", "blocked"),
                _si("search", "open", meta="hasn't moved in 5 days"),
            ]
        )
        prose = s.to_prose()
        assert "**Watch**" in prose
        assert "billing" in prose and "is blocked" in prose
        assert "search" in prose and "hasn't moved in 5 days" in prose
        assert prose.index("billing") < prose.index("search")  # blocked rendered first

    def test_per_slot_empty_messages_are_honest(self):
        # yesterday populated, today + watch empty → CXO's honest per-slot messages.
        prose = StandupSummary(yesterday=[_si("done-y", "closed")]).to_prose()
        assert "Nothing in progress right now." in prose  # today empty
        assert "Nothing flagged as stuck." in prose  # watch empty (CXO verbatim)
        assert "No completions yesterday" not in prose  # yesterday is NOT empty
