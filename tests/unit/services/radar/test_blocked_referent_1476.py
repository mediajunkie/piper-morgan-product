"""#1476 — a "blocked" Radar card must carry a findable referent, or say honestly
that it can't.

Alpha-tester finding (Jake, 2026-07-25): the first thing he saw was a card saying
something was blocked; he searched the UI for the blocked thing, failed, and read
it as breakage. HOST's requirement, carried in the issue: *a surfaced signal must
be traceable to its subject; an unresolvable alert is an invitation to imagine the
failure.*

Three rules under test:
1. The empty-state teaching card may not masquerade as a live "blocked" status —
   it must be unmistakably an example (state chip not "blocked"; copy says it is
   not a real item).
2. An OBSERVED blocked work item renders its referent in the meta line: the
   blocker's name when a label carries one, else honest copy pointing at the
   issue (which the card's ref opens).
3. An OBSERVED blocked entity with NO ref at all (nothing findable to open) is
   suppressed from the view and logged — never rendered as a ghost.
"""

from __future__ import annotations

from datetime import datetime, timezone

from services.radar import (
    EntityType,
    Provenance,
    RadarEntity,
    RadarFeed,
    WorkItemEntitySource,
)
from services.radar.feed import _example_entity


class _FakeSource:
    def __init__(self, entities):
        self._entities = entities

    async def fetch(self, user_id):
        return self._entities


class _FakeWorkItems:
    def __init__(self, rows):
        self._rows = rows

    async def list_for_user(self, user_id):
        return self._rows


def _issue(**kw):
    base = {
        "number": 42,
        "title": "Ship the flow",
        "state": "open",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "uri": "https://github.com/o/r/issues/42",
        "labels": [],
    }
    base.update(kw)
    return base


def _blocked_entity(ref):
    return RadarEntity(
        entity_type=EntityType.WORK_ITEM,
        title="Blocked thing",
        lifecycle_state="blocked",
        provenance=Provenance.OBSERVED,
        attention=5.0,
        ref=ref,
    )


# --- Rule 1: the example card must not read as a live blocked status ---


def test_example_card_does_not_claim_blocked_state():
    e = _example_entity()
    # The state chip is what the tester read as "something is blocked" — the
    # example's chip must not be a live lifecycle claim.
    assert e.lifecycle_state != "blocked"
    assert e.provenance == Provenance.EXAMPLE


def test_example_card_copy_says_it_is_not_real():
    e = _example_entity()
    text = (e.title + " " + e.meta).lower()
    assert "example" in text
    assert "not a real" in text  # explicit: nothing of yours is blocked


# --- Rule 2: an observed blocked work item renders its referent ---


async def test_blocked_workitem_with_named_blocker_label_renders_the_name():
    rows = [_issue(labels=["blocked-by: auth-service migration"])]
    e = (await WorkItemEntitySource(_FakeWorkItems(rows)).fetch("u1"))[0]
    assert e.lifecycle_state == "blocked"
    assert "blocked by auth-service migration" in e.meta


async def test_blocked_workitem_with_bare_label_says_cause_not_named():
    rows = [_issue(labels=["blocked"])]
    e = (await WorkItemEntitySource(_FakeWorkItems(rows)).fetch("u1"))[0]
    assert e.lifecycle_state == "blocked"
    # Honest fallback: no ghost blocker named — the card says the cause isn't
    # recorded and points at the issue the card opens.
    assert "cause not named" in e.meta
    assert "issue" in e.meta


async def test_non_blocked_workitem_meta_untouched():
    e = (await WorkItemEntitySource(_FakeWorkItems([_issue()])).fetch("u1"))[0]
    assert "blocked" not in e.meta


# --- Rule 3: blocked-with-no-ref is suppressed and logged ---


async def test_feed_suppresses_observed_blocked_entity_without_ref():
    ok = _blocked_entity(ref="https://github.com/o/r/issues/1")
    ghost = _blocked_entity(ref=None)
    view = await RadarFeed([_FakeSource([ok, ghost])]).assemble("u1")
    assert view.state == "populated"
    assert ok in view.entities
    assert ghost not in view.entities


async def test_feed_keeps_nonblocked_entities_without_ref():
    # Only BLOCKED cards demand a findable referent; a plain active card without
    # a ref (e.g. informational) is not a ghost alert.
    plain = RadarEntity(
        entity_type=EntityType.WORK_ITEM,
        title="Plain",
        lifecycle_state="open",
        provenance=Provenance.OBSERVED,
        attention=1.0,
        ref=None,
    )
    view = await RadarFeed([_FakeSource([plain])]).assemble("u1")
    assert plain in view.entities


async def test_feed_all_blocked_ghosts_suppressed_yields_empty_state():
    ghost = _blocked_entity(ref=None)
    view = await RadarFeed([_FakeSource([ghost])]).assemble("u1")
    # With every observed entity suppressed, the honest view is the empty state
    # (with its clearly-labeled example), not a populated view of ghosts.
    assert view.state == "empty"
    assert all(e.provenance == Provenance.EXAMPLE for e in view.entities)
