"""#1897 / #1595 unit 4b — LIVE end-to-end proof that a two-part turn surface 1
claims only HALF of no longer loses the other half.

Marked ``llm``: it spends one real router call (plus whatever the two reads
cost) through the REAL app (ASGI, real DB at 5433, real intent service, real
Inversion with the flag set to alpha's live value). It is deselected by every
spend-free sweep and runs only when an operator sets
``PIPER_E2E_LIVE_HEADER_KEY`` (an Anthropic key on the BYOC header rung — the
same provider alpha's router uses, so this measures the Haiku-class router the
users get, not the dev scorer's gpt-4o-mini).

Shape under test (verified deterministically before spending anything):
``PreClassifier.pre_classify("what's my next meeting, and are any PRs sitting
idle?")`` claims ONLY ``get_current_time`` and ``detect_multiple_intents`` finds
one intent — i.e. the PR half is invisible to surface 1. Both halves are live
READs (read_temporal + read_status), so a 4b plan is eligible all-or-nothing.
"""

from __future__ import annotations

import os
from uuid import uuid4

import pytest

from services.intent_service import inversion_live
from services.intent_service.pre_classifier import PreClassifier

pytestmark = pytest.mark.llm

ALPHA_FLAG = "read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal"
TURN = "what's my next meeting, and are any PRs sitting idle?"


def test_shape_is_the_1897_shape_before_spending():
    """The #1897 shape as it stands after Phase 3's deletions (2026-10-02):
    surface 1 claims NEITHER half now — TEMPORAL_PATTERNS (which used to claim
    the meeting half as get_current_time) and GITHUB_QUERY_PATTERNS (the PR
    half was never claimed by it either) are both tombstoned. The whole turn
    is the router's: a two-read plan, all-or-nothing. The invariant this pin
    protects is unchanged in spirit — surface 1 must not split or half-claim
    the turn — only its concrete form moved from "claims exactly one half"
    to "claims nothing"."""
    pre = PreClassifier.pre_classify(TURN)
    multi = PreClassifier.detect_multiple_intents(TURN)
    assert pre is None, pre
    assert multi.is_multi_intent is False and [i.action for i in multi.intents] == []


@pytest.mark.skipif(
    not os.environ.get("PIPER_E2E_LIVE_HEADER_KEY"),
    reason="live probe: set PIPER_E2E_LIVE_HEADER_KEY (operator spend, deliberate)",
)
async def test_two_part_turn_dispatches_both_halves_live(
    e2e_client, e2e_byoc_auth, monkeypatch, caplog
):
    monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, ALPHA_FLAG)
    caplog.set_level("INFO")
    resp = await e2e_client.post(
        "/api/v1/intent",
        json={"message": TURN, "session_id": str(uuid4())},
        **e2e_byoc_auth,
    )
    assert resp.status_code == 200, resp.text[:300]
    body = resp.json()
    text = body.get("message") or body.get("response") or ""
    events = [r.getMessage() for r in caplog.records]
    dispatched = [e for e in events if "inversion_multi_intent_dispatched" in e]
    declined = [e for e in events if "inversion_multi_intent_declined" in e]
    print("\n=== LIVE 1897 PROBE ===")
    print(
        "router/plan events:",
        [e[:160] for e in events if "plan" in e.lower() or "inversion_live" in e][:12],
    )
    print("dispatched:", dispatched[:3])
    print("declined:", declined[:3])
    print("reply:", text[:600])
    assert dispatched, "expected the rail to dispatch a plan; see printed events"
    assert not declined
