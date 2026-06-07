"""Tests for #1124 Phase 3: verb-boundary observability.

`IntentService._observe_action_verb` emits a structured `action_verb_unregistered`
canonicalization-backlog signal for any classified action with no registered Verb,
and emits nothing for registered ones. Observability only — routing is unchanged
(enforce-floor waits for Phase 4 per Arch 2026-06-07).

The helper is pure (logger + get_verb), so it's tested via an unbound call with a
mock `self` — no full IntentService construction needed.
"""

from unittest.mock import MagicMock

from services.intent.intent_service import IntentService


def _intent(category_value, action):
    intent = MagicMock()
    intent.action = action
    intent.category = MagicMock()
    intent.category.value = category_value
    return intent


def test_unregistered_action_emits_backlog_signal():
    """An action with no Verb (e.g. the 'summarize' alias) is emitted as the signal."""
    me = MagicMock()
    IntentService._observe_action_verb(me, _intent("QUERY", "summarize"), "summarize the repo")

    me.logger.info.assert_called_once()
    args, kwargs = me.logger.info.call_args
    assert args[0] == "action_verb_unregistered"
    assert kwargs["signal"] == "canonicalization_backlog"
    assert kwargs["action"] == "summarize"
    assert kwargs["category"] == "QUERY"
    assert kwargs["sample"] == "summarize the repo"


def test_registered_verb_action_emits_nothing():
    """'greeting' maps to Verb.GREET → registered → no backlog signal."""
    me = MagicMock()
    IntentService._observe_action_verb(me, _intent("CONVERSATION", "greeting"), "hi there")
    me.logger.info.assert_not_called()


def test_sample_is_truncated_to_80_chars():
    me = MagicMock()
    long_msg = "x" * 200
    IntentService._observe_action_verb(me, _intent("QUERY", "search_documents"), long_msg)
    _, kwargs = me.logger.info.call_args
    assert len(kwargs["sample"]) == 80


def test_observability_never_raises():
    """A failure in the hook must not propagate (classification must not break)."""
    me = MagicMock()
    bad = MagicMock()
    type(bad).action = property(lambda self: (_ for _ in ()).throw(RuntimeError("boom")))
    # Should swallow and fall to logger.debug, not raise.
    IntentService._observe_action_verb(me, bad, "msg")
    me.logger.debug.assert_called_once()
