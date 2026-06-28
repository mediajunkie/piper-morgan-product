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
