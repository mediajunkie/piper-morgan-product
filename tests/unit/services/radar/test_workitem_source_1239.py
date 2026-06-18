"""#1239 RADAR-WORKITEM-SOURCE — WorkItemEntitySource (TDD).

Covers: GitHub-issue dicts → WorkItem RadarEntities (observed; lifecycle from the
issue's REAL state + labels — no fabrication; honest meta with #number; ref = issue
url); url/untitled/empty fallbacks; and Conversation + WorkItem composing
attention-first. Mirrors test_document_source_1238.py.

The single-bound-user→repo scoping (Arch's beta path, m-40 layer-then-migrate) lives
in the route provider (test_radar.py); this file tests the pure source mapping with a
fake provider, exactly as the Document source is tested.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from services.radar import (
    ConversationEntitySource,
    EntityType,
    Provenance,
    RadarFeed,
    WorkItemEntitySource,
)


class _FakeWorkItems:
    def __init__(self, rows):
        self._rows = rows

    async def list_for_user(self, user_id):
        return self._rows


class _FakeHistory:
    def __init__(self, summaries):
        self._summaries = summaries

    async def list_summaries(self, user_id):
        return self._summaries


def _issue(**kw):
    base = {
        "number": 1,
        "title": "Fix the thing",
        "state": "open",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "uri": "https://github.com/o/r/issues/1",
        "labels": [],
    }
    base.update(kw)
    return base


# --- WorkItemEntitySource mapping ---


async def test_workitem_source_maps_issue_as_observed():
    e = (await WorkItemEntitySource(_FakeWorkItems([_issue()])).fetch("u1"))[0]
    assert e.entity_type == EntityType.WORK_ITEM
    assert e.title == "Fix the thing"
    assert e.provenance == Provenance.OBSERVED  # the user's real work item
    assert e.lifecycle_state == "open"
    assert e.ref == "https://github.com/o/r/issues/1"
    assert "#1" in e.meta  # honest issue-number context


async def test_workitem_lifecycle_from_state_and_labels():
    """Lifecycle is derived from the issue's REAL state + labels (honest provenance),
    not fabricated. open / in-review / blocked / closed."""
    blocked = (await WorkItemEntitySource(_FakeWorkItems([_issue(labels=["blocked"])])).fetch("u"))[0]
    review = (await WorkItemEntitySource(_FakeWorkItems([_issue(labels=["in review"])])).fetch("u"))[0]
    closed = (await WorkItemEntitySource(_FakeWorkItems([_issue(state="closed")])).fetch("u"))[0]
    plain = (await WorkItemEntitySource(_FakeWorkItems([_issue()])).fetch("u"))[0]
    assert blocked.lifecycle_state == "blocked"
    assert review.lifecycle_state == "in-review"
    assert closed.lifecycle_state == "closed"
    assert plain.lifecycle_state == "open"


async def test_workitem_url_fallback_untitled_and_empty():
    # ref falls back to html_url when the uri key is absent (shape varies by adapter path)
    e = (
        await WorkItemEntitySource(
            _FakeWorkItems([{"number": 5, "title": None, "state": "open", "html_url": "https://x/5"}])
        ).fetch("u")
    )[0]
    assert e.title == "(untitled work item)"
    assert e.ref == "https://x/5"
    assert "#5" in e.meta
    # empty provider → no entities (honest empty, not a fabricated card)
    assert await WorkItemEntitySource(_FakeWorkItems([])).fetch("u") == []


# --- multi-source compose (Conversation + WorkItem, attention-first) ---


async def test_workitem_composes_attention_first():
    now_iso = datetime.now(timezone.utc).isoformat()
    older_iso = (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()
    conv = ConversationEntitySource(
        _FakeHistory(
            [{"conversation_id": "c1", "title": "chat", "last_activity": older_iso, "turn_count": 2}]
        )
    )
    work = WorkItemEntitySource(_FakeWorkItems([_issue(updated_at=now_iso, title="hot issue")]))
    view = await RadarFeed([conv, work]).assemble("u1")
    assert view.state == "populated"
    types = {e.entity_type for e in view.entities}
    assert {EntityType.CONVERSATION, EntityType.WORK_ITEM} <= types
    # the more-recently-updated work item sorts ahead of the older conversation
    assert view.entities[0].entity_type == EntityType.WORK_ITEM
    assert view.entities[0].title == "hot issue"
