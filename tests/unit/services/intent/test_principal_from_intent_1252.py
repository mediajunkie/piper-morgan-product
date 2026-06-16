"""#1252 P6/D4 — `_principal_from_intent` sanctioned-accessor tests.

Consolidates the 8 scattered `intent.context.get("user_id") if intent.context
else None` reads in intent_service.py into one accessor. These tests pin the
behaviour-preserving contract (same result the scattered ternary produced) so
the consolidation can't silently drift.
"""

from __future__ import annotations

from types import SimpleNamespace

from services.intent.intent_service import _principal_from_intent


def _intent(context):
    return SimpleNamespace(context=context)


def test_returns_principal_when_present():
    assert _principal_from_intent(_intent({"user_id": "u-123"})) == "u-123"


def test_returns_none_when_context_is_none():
    # The principal-less system/internal call — legitimately None.
    assert _principal_from_intent(_intent(None)) is None


def test_returns_none_when_context_empty():
    assert _principal_from_intent(_intent({})) is None


def test_returns_none_when_user_id_absent():
    assert _principal_from_intent(_intent({"other": "x"})) is None


def test_matches_legacy_ternary_for_all_cases():
    """Behaviour-preserving vs. the old `ctx.get('user_id') if ctx else None`."""
    for ctx in (None, {}, {"user_id": "a"}, {"other": "y"}, {"user_id": ""}):
        intent = _intent(ctx)
        legacy = intent.context.get("user_id") if intent.context else None
        assert _principal_from_intent(intent) == legacy
