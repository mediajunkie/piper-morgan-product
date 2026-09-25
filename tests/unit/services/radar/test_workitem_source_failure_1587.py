"""#1587 — WorkItemEntitySource honestly propagates a FAILED provider read, and
RadarFeed records it as a degraded source instead of silently dropping it.

Covers the consumer half of #1587: WorkItemEntitySource duck-types onto
``gather_for_user`` when the provider exposes it (the real WorkItemProvider
does) and raises EntitySourceReadFailed on FAILED so RadarFeed/StandupAssembler's
existing per-source isolation can disclose it. Providers that only expose the
older ``list_for_user`` shape (fakes elsewhere in the suite) keep working via
the fallback — this file asserts that fallback explicitly so it's not just an
implicit side effect of other tests passing.
"""

from __future__ import annotations

import pytest

from services.radar import RadarFeed, WorkItemEntitySource
from services.radar.feed_factory import WorkItemOutcome, WorkItemReadKind
from services.radar.sources import EntitySourceReadFailed


class _OutcomeProvider:
    """A fake exposing the honest gather_for_user contract directly."""

    def __init__(self, outcome: WorkItemOutcome):
        self._outcome = outcome

    async def gather_for_user(self, user_id, *, include_unassigned=False):
        return self._outcome


class _LegacyProvider:
    """A fake exposing only the old list_for_user shape — no gather_for_user."""

    def __init__(self, rows):
        self._rows = rows

    async def list_for_user(self, user_id):
        return self._rows


@pytest.mark.asyncio
async def test_failed_outcome_raises_entity_source_read_failed():
    source = WorkItemEntitySource(
        _OutcomeProvider(WorkItemOutcome(kind=WorkItemReadKind.SOURCE_FAILED))
    )
    with pytest.raises(EntitySourceReadFailed):
        await source.fetch("u1")


@pytest.mark.asyncio
async def test_verified_empty_outcome_yields_no_entities_not_an_exception():
    source = WorkItemEntitySource(
        _OutcomeProvider(WorkItemOutcome(kind=WorkItemReadKind.VERIFIED_EMPTY))
    )
    entities = await source.fetch("u1")
    assert entities == []


@pytest.mark.asyncio
async def test_items_outcome_maps_to_entities():
    row = {"number": 1, "title": "Fix it", "state": "open", "labels": [], "uri": "https://x/1"}
    source = WorkItemEntitySource(
        _OutcomeProvider(WorkItemOutcome(kind=WorkItemReadKind.ITEMS, items=(row,)))
    )
    entities = await source.fetch("u1")
    assert len(entities) == 1
    assert entities[0].title == "Fix it"


@pytest.mark.asyncio
async def test_legacy_provider_without_gather_for_user_still_works():
    row = {"number": 2, "title": "Legacy row", "state": "open", "labels": [], "uri": "https://x/2"}
    source = WorkItemEntitySource(_LegacyProvider([row]))
    entities = await source.fetch("u1")
    assert len(entities) == 1
    assert entities[0].title == "Legacy row"


@pytest.mark.asyncio
async def test_radar_feed_records_degraded_source_and_still_shows_others():
    """The core honesty property: a failed WorkItem source must show up in
    RadarView.degraded_sources, and other sources must still render (never a
    blank feed)."""

    class _OkSource:
        async def fetch(self, user_id):
            from services.radar.models import EntityType, Provenance, RadarEntity

            return [
                RadarEntity(
                    entity_type=EntityType.DOCUMENT,
                    title="a doc",
                    lifecycle_state="new",
                    provenance=Provenance.OBSERVED,
                    attention=1.0,
                )
            ]

    failing = WorkItemEntitySource(
        _OutcomeProvider(WorkItemOutcome(kind=WorkItemReadKind.SOURCE_FAILED))
    )
    feed = RadarFeed([_OkSource(), failing])
    view = await feed.assemble("u1")

    assert view.degraded_sources == ["your GitHub work items"]
    assert view.state == "populated"
    assert any(e.title == "a doc" for e in view.entities)


@pytest.mark.asyncio
async def test_radar_feed_empty_view_still_discloses_degraded_source():
    """A failed WorkItem source with NO other entities must not silently
    render as the plain empty-state — the degraded signal must survive even
    on the empty branch (m-44: 'clear' emitted identically whether nothing
    was found or nothing could be read is exactly the false-clear this fixes)."""
    failing = WorkItemEntitySource(
        _OutcomeProvider(WorkItemOutcome(kind=WorkItemReadKind.SOURCE_FAILED))
    )
    feed = RadarFeed([failing])
    view = await feed.assemble("u1")

    assert view.state == "empty"
    assert view.degraded_sources == ["your GitHub work items"]


@pytest.mark.asyncio
async def test_radar_feed_generic_exception_still_isolated_unrecorded():
    """A non-#1587 bug (arbitrary exception from an unrelated source) keeps
    its pre-existing behavior: isolated and logged, but NOT added to
    degraded_sources — that field is scoped to the honest #1587 signal, not a
    general crash reporter (out of scope for this issue)."""

    class _BoomSource:
        async def fetch(self, user_id):
            raise RuntimeError("unrelated bug")

    feed = RadarFeed([_BoomSource()])
    view = await feed.assemble("u1")

    assert view.degraded_sources == []
    assert view.state == "empty"
