"""#953 CONTEXT-PERSIST — Phase 1: ConversationContext (de)serialization.

Verifies the persistable-state round-trip for the restart-fragile slice
(last_offer + floor flags). Pure, no DB. The async persist/hydrate
wiring at the floor seam is the companion increment.

(#1863, 2026-09-23, Rule-0 rip: lens_stack was dropped from the persistable
slice — it had no writer anywhere in production. The legacy-key-ignored
behavior for old DB rows that still carry a lens_stack/current_lens key is
pinned separately in test_layer4_hydration_ignores_legacy_lens_keys_1863.py.)
"""

from services.intent_service.conversation_context import (
    ConversationContext,
    LastOffer,
)


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
        }


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
