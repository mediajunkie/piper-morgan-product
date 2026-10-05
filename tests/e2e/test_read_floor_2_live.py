"""read_floor_2: LIVE proof that its members dispatch through the rail when the group is
in the flag (deployed to alpha as Fly v169, 12 tokens, 2026-10-05). Marked
llm: real app + DB + served router. Asserts the Inversion dispatched the op
(route=inversion, the op named) and the reply is not a template/help menu.
"""

from __future__ import annotations

import os
from uuid import uuid4

import pytest

from services.intent_service import inversion_live

pytestmark = pytest.mark.llm

FLAG = "read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal,delete_todo,read_floor,read_floor_2,read_canonical,read_portfolio"

TURNS = {
    "who are you?": "get_identity",
    "did I finish the report yesterday?": "check_completion_status",
    "what does the standup feature do?": "get_feature_info",
    "write a stakeholder update for the board": "write_stakeholder_update",
}


@pytest.mark.skipif(
    not os.environ.get("PIPER_E2E_LIVE_HEADER_KEY"),
    reason="live probe: set PIPER_E2E_LIVE_HEADER_KEY (operator spend, deliberate)",
)
async def test_members_dispatch_through_the_rail(e2e_client, e2e_byoc_auth, monkeypatch, caplog):
    monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, FLAG)
    caplog.set_level("INFO")
    for msg, op in TURNS.items():
        caplog.clear()
        r = await e2e_client.post(
            "/api/v1/intent", json={"message": msg, "session_id": str(uuid4())}, **e2e_byoc_auth
        )
        assert r.status_code == 200, r.text[:300]
        body = r.json()
        reply = body.get("message") or ""
        action = ((body.get("intent") or {}).get("action")) or ""
        events = [x.getMessage() for x in caplog.records]
        decision = [e for e in events if "inversion_live_decision" in e]
        print(f"\n[{msg}] decision: {[d[:200] for d in decision][:1]}")
        print(f"[{msg}] action={action!r} reply: {reply[:240].replace(chr(10), ' ⏎ ')}")
        assert (
            decision and '"route": "inversion"' in decision[0]
        ), f"{msg}: not routed by the Inversion"
        assert f'"operation": "{op}"' in decision[0], f"{msg}: expected {op}"
        assert "I can help you manage your projects" not in reply, f"{msg}: help-menu copy"
