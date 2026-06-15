"""#1236 — /api/v1/radar route. Tests the real wiring (route → _build_feed →
ConversationEntitySource → RadarFeed → response), mocking only the external
UserHistoryService (per the #490 wiring-test lesson — don't mock internals).
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from web.api.routes.radar import get_radar


def _summary(cid, title, last_activity, turns=2):
    return SimpleNamespace(
        conversation_id=cid, title=title, last_activity=last_activity,
        turn_count=turns, topics=[], preview="...", is_private=False,
    )


class _FakeHistoryService:
    def __init__(self, conversations):
        self._conversations = conversations

    async def get_history(self, user_id, page, page_size, include_private):
        return SimpleNamespace(
            conversations=self._conversations, total_count=len(self._conversations),
            page=page, page_size=page_size, has_more=False,
        )


_USER = SimpleNamespace(sub="user-1")


async def test_radar_populated_is_attention_first_and_observed():
    now = datetime.now(timezone.utc)
    older = now - timedelta(days=400)
    svc = _FakeHistoryService([_summary("c1", "old chat", older),
                               _summary("c2", "new chat", now)])
    view = await get_radar(current_user=_USER, service=svc)

    assert view.state == "populated"
    # attention-first: most-recent last_activity at the top
    assert [e.title for e in view.entities] == ["new chat", "old chat"]
    assert all(e.entity_type == "Conversation" for e in view.entities)
    assert all(e.provenance == "observed" for e in view.entities)
    assert view.entities[0].ref == "c2"


async def test_radar_empty_returns_one_example():
    view = await get_radar(current_user=_USER, service=_FakeHistoryService([]))
    assert view.state == "empty"
    assert len(view.entities) == 1
    assert view.entities[0].provenance == "example"


async def test_radar_lifecycle_derived_from_recency():
    now = datetime.now(timezone.utc)
    svc = _FakeHistoryService([_summary("c1", "fresh", now)])
    view = await get_radar(current_user=_USER, service=svc)
    assert view.entities[0].lifecycle_state == "active"  # recent → active
