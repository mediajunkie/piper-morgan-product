"""#953 CONTEXT-PERSIST — Phase 1: ConversationContext (de)serialization.

Verifies the persistable-state round-trip for the restart-fragile slice
(last_offer + floor flags). Pure, no DB. The async persist/hydrate
wiring at the floor seam is the companion increment.

(#1863, 2026-09-23, Rule-0 rip: lens_stack was dropped from the persistable
slice — it had no writer anywhere in production. The legacy-key-ignored
behavior for old DB rows that still carry a lens_stack/current_lens key is
pinned separately in test_layer4_hydration_ignores_legacy_lens_keys_1863.py.)

(#1784, 2026-09-24, Lead ruling option 1: ``pending_list_remainder`` joined
the slice as a TOMBSTONE only — kind/shown/held_total/source_total_display/
armed_at, never the item ``lines``. The restart-crossing behavior this buys
(a hydrated tombstone reaching the §5b-i ``render_moved`` turn through the
real ``IntentService`` consume seam, never a fabricated cash) is exercised
end-to-end in ``TestRestartCrossingTombstone`` in
test_cashable_list_remainder_1762.py — this file stays scoped to the pure
writer/reader round-trip, per the layer split the class docstrings above
already draw.)
"""

import json

from services.intent_service.conversation_context import (
    ConversationContext,
    LastOffer,
)
from services.intent_service.list_remainder import compose_capped_list


class TestPersistableStateRoundTrip:
    def test_round_trip_full_state(self):
        ctx = ConversationContext()
        ctx.last_offer = LastOffer(
            offer_type="contextual",
            continuation_hint="explain how project context works",
            offer_text="Would you like me to explain more?",
        )
        ctx.last_response_was_floor = True
        ctx.last_floor_category = "temporal"

        state = ctx.to_persistable_state()
        restored = ConversationContext()
        restored.apply_persisted_state(state)

        assert restored.last_offer is not None
        assert restored.last_offer.offer_type == "contextual"
        assert restored.last_offer.continuation_hint == "explain how project context works"
        assert restored.last_offer.offer_text == "Would you like me to explain more?"
        assert restored.last_response_was_floor is True
        assert restored.last_floor_category == "temporal"

    def test_round_trip_empty_offer(self):
        ctx = ConversationContext()
        ctx.last_offer = None
        state = ctx.to_persistable_state()
        restored = ConversationContext()
        restored.apply_persisted_state(state)
        assert restored.last_offer is None

    def test_state_is_json_safe(self):
        import json

        ctx = ConversationContext()
        ctx.last_offer = LastOffer(offer_type="contextual", continuation_hint="x")
        # Must serialize to JSON without custom encoders (it rides a JSONB column).
        dumped = json.dumps(ctx.to_persistable_state())
        assert "contextual" in dumped

    def test_excludes_turns_and_provenance(self):
        """The persistable slice is ONLY offer/floor state — turns + provenance
        persist elsewhere (ConversationTurnDB), so they must not leak in."""
        ctx = ConversationContext()
        state = ctx.to_persistable_state()
        assert set(state.keys()) == {
            "last_offer",
            "last_response_was_floor",
            "last_floor_category",
            # #1688: the FTUX interview's bound answer — session-scoped (the
            # slice is keyed by THIS session; surviving a mid-session restart
            # is not cross-session recall, which is #1705's).
            "ftux_interview_answer",
            # #1784: the #1762 list-remainder TOMBSTONE (never the items).
            "pending_list_remainder",
        }


class TestPendingListRemainderTombstoneRoundTrip:
    """#1784: the tombstone half of the #1762 remainder. Persist ONLY
    kind/shown/held_total/source_total_display/armed_at — never ``lines``."""

    def _armed_remainder(self, held=50, source_total=179):
        lines = [f"\n- item {i}" for i in range(held)]
        return compose_capped_list(
            lines=lines, cap=5, kind="open issues", source_total=source_total
        ).remainder

    def test_round_trip_carries_the_tombstone_fields(self):
        ctx = ConversationContext()
        remainder = self._armed_remainder()
        ctx.pending_list_remainder = remainder

        state = ctx.to_persistable_state()
        restored = ConversationContext()
        restored.apply_persisted_state(state)

        tomb = restored.pending_list_remainder
        assert tomb is not None
        assert tomb.kind == remainder.kind
        assert tomb.shown == remainder.shown
        assert tomb.held_total == remainder.held_total
        assert tomb.source_total_display == remainder.source_total_display
        assert tomb.armed_at == remainder.armed_at

    def test_round_trip_never_carries_the_item_lines(self):
        """The whole point of the tombstone: the items themselves never ride
        the JSONB column, however many were held."""
        ctx = ConversationContext()
        ctx.pending_list_remainder = self._armed_remainder(held=340, source_total=340)

        state = ctx.to_persistable_state()
        assert "lines" not in state["pending_list_remainder"]
        dumped = json.dumps(state["pending_list_remainder"])
        assert "item " not in dumped

        restored = ConversationContext()
        restored.apply_persisted_state(state)
        assert restored.pending_list_remainder.lines == ()

    def test_the_persisted_tombstone_is_size_bounded_regardless_of_held_total(self):
        """Bounded independent of how many items were hidden — the size pin
        (#1784)."""
        ctx = ConversationContext()
        ctx.pending_list_remainder = self._armed_remainder(held=5000, source_total=5000)
        dumped = json.dumps(ctx.to_persistable_state()["pending_list_remainder"])
        assert len(dumped) < 500

    def test_round_trip_empty_remainder(self):
        ctx = ConversationContext()
        ctx.pending_list_remainder = None
        state = ctx.to_persistable_state()
        restored = ConversationContext()
        restored.pending_list_remainder = self._armed_remainder()  # pre-existing state
        restored.apply_persisted_state(state)
        assert restored.pending_list_remainder is None

    def test_state_is_json_safe(self):
        ctx = ConversationContext()
        ctx.pending_list_remainder = self._armed_remainder()
        # Must serialize without a custom encoder (JSONB column) — the
        # datetime is stored as an isoformat string, not a raw datetime.
        dumped = json.dumps(ctx.to_persistable_state())
        assert "open issues" in dumped

    def test_malformed_tombstone_missing_kind_is_ignored(self):
        """Mirrors ``test_malformed_offer_ignored``: a persisted dict that
        cannot honestly be called a tombstone (no ``kind``) leaves the
        default rather than hydrating a half-built ``ListRemainder``."""
        ctx = ConversationContext()
        ctx.apply_persisted_state({"pending_list_remainder": {"shown": 5}})
        assert ctx.pending_list_remainder is None

    def test_malformed_armed_at_fails_toward_stale_not_fresh(self):
        ctx = ConversationContext()
        ctx.apply_persisted_state(
            {"pending_list_remainder": {"kind": "open issues", "armed_at": "not-a-timestamp"}}
        )
        tomb = ctx.pending_list_remainder
        assert tomb is not None
        assert tomb.is_stale()

    def test_a_hydrated_tombstone_can_only_reach_render_moved_never_render_cash(self):
        """The structural guarantee, pinned directly against the dataclass
        rather than through the intent-service seam (that end-to-end path is
        TestRestartCrossingTombstone in test_cashable_list_remainder_1762.py):
        an empty ``lines`` tuple is exactly the condition
        ``_check_pending_list_remainder`` already uses to route to
        ``render_moved`` — a tombstone can never satisfy ``remainder.lines``
        being non-empty, so it can never reach ``render_cash``."""
        ctx = ConversationContext()
        ctx.pending_list_remainder = self._armed_remainder()
        state = ctx.to_persistable_state()
        restored = ConversationContext()
        restored.apply_persisted_state(state)
        assert not restored.pending_list_remainder.lines


class TestApplyPersistedStateBackwardCompatible:
    def test_none_is_noop(self):
        ctx = ConversationContext()
        ctx.last_floor_category = "preexisting"
        ctx.apply_persisted_state(None)  # legacy row → no persisted state
        assert ctx.last_floor_category == "preexisting"  # unchanged

    def test_empty_dict_is_noop(self):
        ctx = ConversationContext()
        ctx.last_response_was_floor = True
        ctx.apply_persisted_state({})
        assert ctx.last_response_was_floor is True

    def test_partial_legacy_state_leaves_missing_fields_default(self):
        """A persisted dict missing newer keys must not clobber defaults."""
        ctx = ConversationContext()
        ctx.apply_persisted_state({"last_floor_category": "temporal"})  # only one key
        assert ctx.last_floor_category == "temporal"
        assert ctx.last_offer is None  # default preserved
        assert ctx.last_response_was_floor is False  # default preserved

    def test_malformed_offer_ignored(self):
        ctx = ConversationContext()
        ctx.apply_persisted_state({"last_offer": {"junk": "no hint"}})
        assert ctx.last_offer is None  # no continuation_hint → not hydrated
