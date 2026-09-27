"""Shared test helper for #1595 Phase-3 POINTER/pin conversions.

A pattern list's literals were deleted (scripts/inversion_phase3_deleted_
patterns.json) — the phrases it used to claim at surface 1 are now unclaimed
there BY DESIGN. Every regression test that used to pin "surface 1 claims
this phrase" must now pin the TWO-PART fact the deletion procedure actually
guarantees: (a) surface 1 no longer claims it, and (b) the Inversion router
routes it to the same destination, deterministically (a stubbed router call,
NEVER a live LLM).

Import ``assert_inversion_routes`` from any test file doing that conversion.
Not a test module itself (filename doesn't match ``test_*.py`` — pytest.ini
``python_files``), so it is never collected.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Optional

import pytest

from services.intent_service import inversion_live
from services.intent_service.inversion_router import RoutingDecision
from services.intent_service.workflow_entries import register_default_workflows


def stub_router_operation(
    monkeypatch: "pytest.MonkeyPatch",
    operation: Optional[str],
    *,
    confidence: float = 0.95,
    outcome: str = "operation",
) -> None:
    """Monkeypatch inversion_router.route to a deterministic fake — NO LLM
    call, ever. Mirrors the idiom test_inversion_live_1595.py's _stub_route
    uses (a fixed RoutingDecision, regardless of input)."""
    from services.intent_service import inversion_router as ir

    async def _route(message, session_state=None, **kwargs):
        return RoutingDecision(
            outcome=outcome,
            operation=operation if outcome == "operation" else None,
            confidence=confidence,
        )

    monkeypatch.setattr(ir, "route", _route)


async def assert_inversion_routes(
    monkeypatch: "pytest.MonkeyPatch",
    message: str,
    *,
    live_categories: str,
    expected_action: str,
    confidence: float = 0.95,
):
    """Sets PIPER_INVERSION_LIVE_CATEGORIES, stubs the router to
    deterministically return ``expected_action``, and asserts
    ``consult_inversion_live`` returns an Intent with that action for
    ``message``.

    ``session_id``/``user_id`` are both deliberately None: this keeps the
    consult entirely DB-free — ``assemble_session_snapshot``'s
    declared-mode/ledger-head/clear-verb reads are all gated on ``user_id``
    truthy and no-op cleanly when it's None (services/intent_service/
    snapshot_assembly.py); the process-registry probe is in-memory only, no
    storage. This is the routing-plumbing attestation the Phase-3 deletion
    procedure asks for, not a full end-to-end dispatch/handler test (those
    live in the dedicated test_inversion_write_allowlist_*_*.py /
    test_inversion_flip_groups_1667.py files, which DO carry the aiosqlite
    session fixtures because they also exercise session-scoped state).

    Returns the Intent for further assertions.
    """
    monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, live_categories)
    stub_router_operation(monkeypatch, expected_action, confidence=confidence)
    register_default_workflows()  # idempotent
    svc = SimpleNamespace(intent_classifier=None)
    intent = await inversion_live.consult_inversion_live(
        message, session_id=None, user_id=None, intent_service=svc
    )
    assert (
        intent is not None
    ), f"inversion did not route {message!r} (expected {expected_action!r}, live={live_categories!r})"
    assert intent.action == expected_action, (
        f"inversion routed {message!r} to {intent.action!r}, expected "
        f"{expected_action!r} (live={live_categories!r})"
    )
    return intent
