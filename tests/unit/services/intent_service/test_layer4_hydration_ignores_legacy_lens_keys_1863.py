"""#1863 Rule-0 rip — hydrator pin for the legacy lens_stack/current_lens keys.

The lens surface (ConversationTurn.lens, ConversationContext.current_lens,
ConversationContext.lens_stack — including its #953 persisted slice) had no
writer anywhere in production (Arch-verified GO, 2026-09-23) and was deleted
outright, WITHOUT an alembic migration: lens_stack was a key inside the
``ConversationDB.context`` JSONB blob (under ``layer4_state``), not a column.

Existing DB rows may therefore still carry a ``layer4_state`` dict containing
the legacy ``lens_stack`` key (a list) — and, since #820's soft-invocation
read piggybacked on the same conversational-turn concept, a hypothetical
``current_lens`` key could appear too, even though nothing ever wrote one.
This test pins the behavioral condition Arch's GO required: hydration must
succeed and silently ignore both legacy keys, per the same isinstance-guard
pattern ``apply_persisted_state`` already uses for every other key.
"""

from services.intent_service.conversation_context import ConversationContext


class TestLayer4HydrationIgnoresLegacyLensKeys1863:
    def test_hydration_succeeds_and_ignores_legacy_lens_stack_key(self):
        """A persisted layer4_state dict carrying the legacy lens_stack key
        must hydrate without error, and the key must leave no trace on the
        restored context (there is no lens_stack attribute to set)."""
        legacy_state = {
            "lens_stack": ["issues", "calendar"],
            "last_offer": None,
            "last_response_was_floor": True,
            "last_floor_category": "temporal",
        }

        ctx = ConversationContext()
        ctx.apply_persisted_state(legacy_state)  # must not raise

        assert not hasattr(ctx, "lens_stack")
        # Every other key in the same legacy blob still hydrates correctly —
        # proving the ignore is surgical (just the unknown key), not a
        # silent swallow of the whole dict.
        assert ctx.last_response_was_floor is True
        assert ctx.last_floor_category == "temporal"

    def test_hydration_succeeds_and_ignores_legacy_current_lens_key(self):
        """current_lens was a read-only derived property (never persisted by
        to_persistable_state), but a hand-edited or pre-#1863 row could in
        principle carry it. It must be ignored, not raise."""
        legacy_state = {
            "current_lens": "calendar",
            "last_response_was_floor": False,
        }

        ctx = ConversationContext()
        ctx.apply_persisted_state(legacy_state)  # must not raise

        assert not hasattr(ctx, "current_lens")
        assert ctx.last_response_was_floor is False

    def test_hydration_succeeds_with_both_legacy_keys_and_only_legacy_keys(self):
        """A layer4_state blob that is NOTHING but the two legacy lens keys
        (the oldest possible pre-#953-expansion shape) still hydrates to an
        all-default context, never an exception."""
        ctx = ConversationContext()
        ctx.apply_persisted_state({"lens_stack": [], "current_lens": None})

        assert not hasattr(ctx, "lens_stack")
        assert not hasattr(ctx, "current_lens")
        assert ctx.last_offer is None
        assert ctx.last_response_was_floor is False
        assert ctx.last_floor_category is None
