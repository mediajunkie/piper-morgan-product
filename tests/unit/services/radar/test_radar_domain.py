"""#1236 Radar domain — TDD.

Covers: the RadarEntity value object; RadarFeed assembly (provenance filter,
attention-first ordering, two-state selection); ConversationEntitySource mapping
(#1021 summary → Conversation entity, observed, derived lifecycle, honest meta).
"""

from __future__ import annotations

from datetime import datetime, timezone

from services.radar import (
    ConversationEntitySource,
    EntityType,
    Provenance,
    RadarEntity,
    RadarFeed,
)


def _obs(title: str, attention: float) -> RadarEntity:
    return RadarEntity(
        entity_type=EntityType.WORK_ITEM,
        title=title,
        lifecycle_state="active",
        provenance=Provenance.OBSERVED,
        attention=attention,
    )


class _FakeSource:
    def __init__(self, entities):
        self._entities = entities

    async def fetch(self, user_id):
        return self._entities


class _FakeHistory:
    def __init__(self, summaries):
        self._summaries = summaries

    async def list_summaries(self, user_id):
        return self._summaries


def test_radar_entity_is_a_value_object():
    e = RadarEntity(
        EntityType.CONVERSATION,
        "auth migration",
        "active",
        Provenance.OBSERVED,
        meta="1h ago",
        attention=5.0,
        ref="c1",
    )
    assert e.entity_type == EntityType.CONVERSATION
    assert e.title == "auth migration"
    assert e.provenance == Provenance.OBSERVED
    assert e.ref == "c1"


async def test_feed_populated_orders_attention_first():
    feed = RadarFeed([_FakeSource([_obs("low", 1.0), _obs("high", 9.0), _obs("mid", 5.0)])])
    view = await feed.assemble("u1")
    assert view.state == "populated"
    assert [e.title for e in view.entities] == ["high", "mid", "low"]


async def test_feed_filters_non_observed_from_default_view():
    seed = RadarEntity(EntityType.WORK_ITEM, "seed card", "active", Provenance.SEED, attention=99.0)
    feed = RadarFeed([_FakeSource([_obs("real", 1.0), seed])])
    view = await feed.assemble("u1")
    assert view.state == "populated"
    assert [e.title for e in view.entities] == ["real"]
    assert all(e.provenance == Provenance.OBSERVED for e in view.entities)


async def test_feed_empty_when_no_observed_returns_one_example():
    seed = RadarEntity(EntityType.WORK_ITEM, "seed", "active", Provenance.SEED, attention=99.0)
    view = await RadarFeed([_FakeSource([seed])]).assemble("u1")  # nothing observed
    assert view.state == "empty"
    assert len(view.entities) == 1
    assert view.entities[0].provenance == Provenance.EXAMPLE


async def test_feed_empty_when_no_entities_at_all():
    view = await RadarFeed([_FakeSource([])]).assemble("u1")
    assert view.state == "empty"
    assert len(view.entities) == 1
    assert view.entities[0].provenance == Provenance.EXAMPLE


async def test_conversation_source_maps_summary_as_observed():
    now_iso = datetime.now(timezone.utc).isoformat()
    summaries = [
        {
            "conversation_id": "c1",
            "title": "auth migration",
            "last_activity": now_iso,
            "turn_count": 3,
            "topics": [],
            "preview": "...",
        }
    ]
    entities = await ConversationEntitySource(_FakeHistory(summaries)).fetch("u1")
    assert len(entities) == 1
    e = entities[0]
    assert e.entity_type == EntityType.CONVERSATION
    assert e.title == "auth migration"
    assert e.provenance == Provenance.OBSERVED  # a user's real conversation
    assert e.lifecycle_state == "active"  # recent last_activity → active
    assert e.ref == "c1"
    assert "3 turns" in e.meta


async def test_conversation_source_dormant_for_old_activity():
    old_iso = "2020-01-01T00:00:00+00:00"
    summaries = [
        {"conversation_id": "c2", "title": "old", "last_activity": old_iso, "turn_count": 1}
    ]
    e = (await ConversationEntitySource(_FakeHistory(summaries)).fetch("u1"))[0]
    assert e.lifecycle_state == "dormant"
    assert "1 turn" in e.meta and "1 turns" not in e.meta  # singular


async def test_conversation_source_empty_list():
    assert await ConversationEntitySource(_FakeHistory([])).fetch("u1") == []


# --- #1625: due reminders — pinned Reminder entities locked at the top ---


class _FakeReminderProvider:
    def __init__(self, texts):
        self._texts = texts

    async def list_due(self, user_id):
        return self._texts


async def test_feed_pinned_entities_lock_above_attention_order():
    """#1625 PM ruling: pinned (due-reminder) cards sort ABOVE the attention
    ordering, however hot the unpinned cards are."""
    from services.radar import ReminderEntitySource

    pinned_src = ReminderEntitySource(_FakeReminderProvider(["call the vendor"]))
    feed = RadarFeed([_FakeSource([_obs("hot item", 999.0)]), pinned_src])
    view = await feed.assemble("u1")
    assert view.state == "populated"
    assert [e.title for e in view.entities] == ["call the vendor", "hot item"]
    assert view.entities[0].pinned is True
    assert view.entities[1].pinned is False


async def test_reminder_source_maps_due_texts_as_pinned_observed():
    from services.radar import ReminderEntitySource

    entities = await ReminderEntitySource(
        _FakeReminderProvider(["submit the report", "call the vendor"])
    ).fetch("u1")
    assert [e.title for e in entities] == ["submit the report", "call the vendor"]
    for e in entities:
        assert e.entity_type == EntityType.REMINDER
        assert e.provenance == Provenance.OBSERVED  # real user reminders, no fabrication
        assert e.lifecycle_state == "due"
        assert e.pinned is True


async def test_reminder_source_empty_and_failed_lookup_yield_no_cards():
    """A None from the provider (failed lookup) renders NO card — conversational
    #1425 honesty owns failure disclosure; Radar never fabricates."""
    from services.radar import ReminderEntitySource

    assert await ReminderEntitySource(_FakeReminderProvider([])).fetch("u1") == []
    assert await ReminderEntitySource(_FakeReminderProvider(None)).fetch("u1") == []
