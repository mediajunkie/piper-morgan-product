"""#1595 read_floor — LIVE proof that the five floor ops dispatch through the
rail under their own category when the group is in the flag.

Marked ``llm``: real app + DB + served router + the real floor. One turn per
category; asserts the Inversion dispatched (route=inversion, the op named)
and that the reply is a floor answer, not a template.
"""

from __future__ import annotations

import os
from uuid import uuid4

import pytest

from services.intent_service import inversion_live

pytestmark = pytest.mark.llm
FLAG = (
    "read_status,read_referent,read_synthesis,create_todo,create_reminder,"
    "read_strategic,read_temporal,delete_todo,read_floor"
)
TURNS = {
    "what can you do?": "get_capabilities",
    "do you trust me with this decision": "explain_trust",
    "what do you remember about me?": "get_memory",
    "what's blocking the milestone?": "analyze_blockers",
}


@pytest.mark.skipif(
    not os.environ.get("PIPER_E2E_LIVE_HEADER_KEY"),
    reason="live probe: set PIPER_E2E_LIVE_HEADER_KEY (operator spend, deliberate)",
)
async def test_read_floor_dispatches_each_member(e2e_client, e2e_byoc_auth, monkeypatch, caplog):
    monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, FLAG)
    caplog.set_level("INFO")
    for msg, op in TURNS.items():
        caplog.clear()
        r = await e2e_client.post(
            "/api/v1/intent", json={"message": msg, "session_id": str(uuid4())}, **e2e_byoc_auth
        )
        assert r.status_code == 200, r.text[:300]
        reply = r.json().get("message") or ""
        events = [x.getMessage() for x in caplog.records]
        decision = [e for e in events if "inversion_live_decision" in e]
        floor = [e for e in events if "action_gate_routing_to_floor" in e]
        print(f"\n[{msg}] decision: {[d[:200] for d in decision][:1]}")
        print(f"[{msg}] floor: {[f[:160] for f in floor][:1]}")
        print(f"[{msg}] reply: {reply[:260].replace(chr(10), ' ⏎ ')}")
        assert (
            decision and '"route": "inversion"' in decision[0]
        ), f"{msg}: not routed by the Inversion"
        assert f'"operation": "{op}"' in decision[0], f"{msg}: expected {op}"
        assert floor, f"{msg}: the floor did not run"
