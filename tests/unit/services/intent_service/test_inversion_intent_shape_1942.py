"""1942 — a router-served Intent hands handlers the SAME message shape the
classifier path does.

PM live, alpha v169 (2026-10-05): "get issue 101" → "I couldn't find an
issue number in your request." The handler (_handle_review_issue_query, live
via read_referent) reads ONLY intent.context["original_message"]; the
Inversion live path built its Intent with the top-level field alone, so the
handler was handed an empty message. 1898 patched one handler for the same
gap; this pins the source: the served Intent carries the message in BOTH
places (Issue #744's duality), so no context-only reader can see nothing.

Layer: the Intent consult_inversion_live returns, with the router stubbed —
not the handler, not the live deploy.
"""

from types import SimpleNamespace

import pytest

from services.intent_service import inversion_live
from services.intent_service.inversion_router import RoutingDecision
from services.intent_service.workflow_entries import register_default_workflows

pytestmark = pytest.mark.asyncio


def _svc():
    register_default_workflows()
    return SimpleNamespace(intent_classifier=None)


def _stub_route(monkeypatch, *, operation, confidence=0.95, args=None):
    from services.intent_service import inversion_router as ir

    async def _route(message, session_state=None, **kwargs):
        return RoutingDecision(
            outcome="operation", operation=operation, confidence=confidence, args=args or {}
        )

    monkeypatch.setattr(ir, "route", _route)


async def test_served_intent_carries_the_message_in_context_too(monkeypatch):
    monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, "read_referent")
    _stub_route(monkeypatch, operation="review_issue_query")
    intent = await inversion_live.consult_inversion_live(
        "get issue 101", session_id="s1", user_id="u1", intent_service=_svc()
    )
    assert intent is not None, "flip did not apply — the pin measured nothing"
    assert intent.original_message == "get issue 101"
    assert intent.context.get("original_message") == "get issue 101"
    # the existing markers are untouched
    assert intent.context.get("inversion_live") is True
    assert "inversion_args" in intent.context


async def test_context_only_reader_sees_the_number(monkeypatch):
    """The shape the failing handler actually reads: a context-only lookup
    must now find the issue number a user typed, with or without '#'."""
    import re

    monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, "read_referent")
    _stub_route(monkeypatch, operation="review_issue_query")
    for message in ("get issue 101", "get issue #101"):
        intent = await inversion_live.consult_inversion_live(
            message, session_id="s1", user_id="u1", intent_service=_svc()
        )
        assert intent is not None
        match = re.search(r"#?(\d+)", intent.context.get("original_message", ""))
        assert match and match.group(1) == "101", message
