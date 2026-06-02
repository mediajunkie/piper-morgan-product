"""
Tests for Issue #1030 R4 turn_provenance sidecar on ConversationContext.

Step 3 of R4 implementation. Covers:
- turn_provenance dict accepts entries keyed by turn id
- _prune_old_turns drops provenance entries in lockstep with turns (count + age)
- get_turn_provenance / get_last_turn_provenance / get_previous_assistant_turn
- Empty-state behavior (no provenance for any turn)
"""

from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from services.intent_service.conversation_context import (
    ConversationContext,
    ConversationTurn,
)


def _ctx_with_turns(n: int) -> ConversationContext:
    """ConversationContext factory: n turns added."""
    ctx = ConversationContext()
    for i in range(n):
        ctx.add_turn(message=f"message {i}")
    return ctx


class TestTurnProvenanceSidecar:
    """The sidecar accepts entries and prunes in lockstep with turns."""

    def test_default_provenance_is_empty(self):
        ctx = ConversationContext()
        assert ctx.turn_provenance == {}

    def test_can_attach_provenance_to_turn(self):
        ctx = _ctx_with_turns(1)
        turn = ctx.turns[0]
        ctx.turn_provenance[turn.id] = {
            "calendar": {"source": "GoogleCalendar", "fetch_timestamp": "now"}
        }
        assert ctx.get_turn_provenance(turn.id) is not None
        assert ctx.get_turn_provenance(turn.id)["calendar"]["source"] == "GoogleCalendar"

    def test_get_turn_provenance_returns_none_when_missing(self):
        ctx = _ctx_with_turns(1)
        unknown_id = uuid4()
        assert ctx.get_turn_provenance(unknown_id) is None

    def test_prune_drops_provenance_when_turn_pruned_by_count(self):
        """Add 15 turns + provenance to all; assert prune keeps 10 of each."""
        ctx = ConversationContext()
        ctx.max_turns = 10
        for i in range(15):
            turn = ctx.add_turn(message=f"message {i}")
            ctx.turn_provenance[turn.id] = {"index": i}
            # Re-prune in case add_turn already pruned this iteration
            ctx._prune_old_turns()

        assert len(ctx.turns) == 10, "Turns must be pruned to max_turns"
        assert len(ctx.turn_provenance) == 10, (
            "Provenance must be pruned to match turns count"
        )
        # The provenance keys must all be in the remaining turns
        remaining_ids = {t.id for t in ctx.turns}
        provenance_keys = set(ctx.turn_provenance.keys())
        assert provenance_keys == remaining_ids, (
            "Provenance keys must match remaining turn ids exactly"
        )

    def test_prune_drops_provenance_when_turn_pruned_by_age(self):
        """Mark all turns as stale (>30 min old); assert provenance fully cleared."""
        ctx = ConversationContext()
        for i in range(3):
            turn = ctx.add_turn(message=f"message {i}")
            ctx.turn_provenance[turn.id] = {"index": i}
        # Backdate all turns to >30min ago
        stale_time = datetime.now() - timedelta(minutes=45)
        for t in ctx.turns:
            t.timestamp = stale_time
        ctx._prune_old_turns()
        assert ctx.turns == []
        assert ctx.turn_provenance == {}

    def test_provenance_unaffected_when_no_pruning_needed(self):
        ctx = ConversationContext()
        ctx.max_turns = 10
        for i in range(5):
            turn = ctx.add_turn(message=f"message {i}")
            ctx.turn_provenance[turn.id] = {"index": i}
        assert len(ctx.turn_provenance) == 5


class TestProvenanceLookupHelpers:
    """get_last_turn_provenance + get_previous_assistant_turn semantics."""

    def test_get_last_turn_provenance_returns_most_recent(self):
        ctx = ConversationContext()
        t1 = ctx.add_turn(message="first")
        t2 = ctx.add_turn(message="second")
        t3 = ctx.add_turn(message="third")
        ctx.turn_provenance[t1.id] = {"marker": "first"}
        ctx.turn_provenance[t3.id] = {"marker": "third"}
        # t2 has no provenance
        last = ctx.get_last_turn_provenance()
        assert last is not None
        assert last["marker"] == "third"

    def test_get_last_turn_provenance_skips_turns_without_provenance(self):
        ctx = ConversationContext()
        t1 = ctx.add_turn(message="first")
        t2 = ctx.add_turn(message="second")  # no provenance
        ctx.turn_provenance[t1.id] = {"marker": "first"}
        last = ctx.get_last_turn_provenance()
        assert last is not None
        assert last["marker"] == "first"

    def test_get_last_turn_provenance_returns_none_when_no_provenance(self):
        ctx = _ctx_with_turns(3)
        # No provenance attached
        assert ctx.get_last_turn_provenance() is None

    def test_get_previous_assistant_turn_requires_response_and_provenance(self):
        ctx = ConversationContext()
        t1 = ctx.add_turn(message="user-only")  # no response, no provenance
        t2 = ctx.add_turn(message="user msg")
        t2.response = "piper response"  # response set but no provenance
        t3 = ctx.add_turn(message="another")
        t3.response = "piper response 2"
        ctx.turn_provenance[t3.id] = {"calendar": {"source": "GoogleCalendar"}}

        prev = ctx.get_previous_assistant_turn()
        assert prev is not None
        assert prev.id == t3.id  # most recent with BOTH response and provenance

    def test_get_previous_assistant_turn_returns_none_when_no_match(self):
        ctx = ConversationContext()
        ctx.add_turn(message="user")
        # No response set, no provenance
        assert ctx.get_previous_assistant_turn() is None
