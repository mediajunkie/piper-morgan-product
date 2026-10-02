"""#1606 / #1595 unit 4b — LIVE end-to-end proof (Arch's condition 5(a)) that
PM's two-part turn — a reminder clear PLUS a capability QUESTION — is served
as a plan whose second element the FLOOR answers.

Marked ``llm``: spends real router + floor calls through the REAL app (ASGI,
real DB at 5433, real intent service, real Inversion with alpha's live flag).
Deselected by every spend-free sweep; runs only when an operator sets
``PIPER_E2E_LIVE_HEADER_KEY`` (an Anthropic key on the BYOC header rung — the
same provider alpha's router uses).

What 5(a) demands, verbatim from the ruling: the delete arms its confirm, the
capability answer is present, and nothing says the delete happened. Seeding:
two reminders are created through the same API first, so the delete half has
something to arm; create_reminder is on the live write allowlist.
"""

from __future__ import annotations

import os
from uuid import uuid4

import pytest

from services.intent_service import inversion_live

pytestmark = pytest.mark.llm

ALPHA_FLAG = (
    "read_status,read_referent,read_synthesis,create_todo,create_reminder,"
    "read_strategic,read_temporal,delete_todo"
)
TURN = (
    'please clear the reminders except for "Review the PR" - also, are you able '
    "to set my default repo for me conversationally?"
)
SEED = [
    "remind me tomorrow at 9am to Review the PR",
    "remind me tomorrow at 10am to hydrate",
]


@pytest.mark.skipif(
    not os.environ.get("PIPER_E2E_LIVE_HEADER_KEY"),
    reason="live probe: set PIPER_E2E_LIVE_HEADER_KEY (operator spend, deliberate)",
)
async def test_two_part_turn_floor_element_live(e2e_client, e2e_byoc_auth, monkeypatch, caplog):
    monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, ALPHA_FLAG)
    caplog.set_level("INFO")
    sid = str(uuid4())
    for seed in SEED:
        r = await e2e_client.post(
            "/api/v1/intent", json={"message": seed, "session_id": sid}, **e2e_byoc_auth
        )
        assert r.status_code == 200, r.text[:300]
        print("seed reply:", (r.json().get("message") or r.json().get("response") or "")[:160])
    caplog.clear()

    resp = await e2e_client.post(
        "/api/v1/intent", json={"message": TURN, "session_id": sid}, **e2e_byoc_auth
    )
    assert resp.status_code == 200, resp.text[:300]
    body = resp.json()
    text = body.get("message") or body.get("response") or ""
    events = [r.getMessage() for r in caplog.records]
    dispatched = [e for e in events if "inversion_multi_intent_dispatched" in e]
    declined = [e for e in events if "inversion_multi_intent_declined" in e]
    decisions = [e for e in events if "inversion_live_decision" in e]
    print("\n=== LIVE 1606 PROBE ===")
    print("decision:", [e[:400] for e in decisions][:2])
    print("dispatched:", [e[:400] for e in dispatched][:2])
    print("declined:", declined[:3])
    floor_calls = [e[:300] for e in events if "action_gate_routing_to_floor" in e]
    print("floor saw:", floor_calls[:1])
    print("reply:", text.replace("\n", " ⏎ "))
    assert dispatched, "expected the rail to dispatch a plan with a floor element; see events"
    assert not declined
    assert '"plan_floor_elements": 1' in dispatched[0]
    low = text.lower()
    assert "default repo" in low, "the capability answer must be present"
    # The delete half reached its own carrier (the #1605 clear-verb either/or
    # with the exception note) — its text follows the capability answer.
    assert "mark it done" in low or "(yes/no)" in low, "the delete half must arm, not vanish"
    assert low.index("default repo") < low.index(
        "mark it done" if "mark it done" in low else "(yes/no)"
    )
    assert "deleted" not in low and "cleared" not in low.replace(
        "clear the", ""
    ), "nothing may say the delete happened before the confirm"
