"""read_portfolio (list_repos, search_projects): LIVE proof of Arch's release
condition (2026-10-04): with read_portfolio in the flag, a router-named
list_repos reaches the rail adapter on the main path and returns the repo
list answer, NOT the portfolio help menu (the regression the "rail owns every
rail key" change, 25f1abc010, was built to prevent).

Marked ``llm``: real app + DB + served router. Asserts the Inversion dispatched
list_repos (route=inversion, the op named), and that the reply is the list
handler's answer (action list_repos), not portfolio_help.
"""

from __future__ import annotations

import os
from uuid import uuid4

import pytest

from services.intent_service import inversion_live

pytestmark = pytest.mark.llm

FLAG = (
    "read_status,read_referent,read_synthesis,create_todo,create_reminder,"
    "read_strategic,read_temporal,delete_todo,read_floor,read_portfolio"
)

TURNS = {
    "which repositories are linked to my projects?": "list_repos",
    "show me the repos connected to my projects": "list_repos",
}


@pytest.mark.skipif(
    not os.environ.get("PIPER_E2E_LIVE_HEADER_KEY"),
    reason="live probe: set PIPER_E2E_LIVE_HEADER_KEY (operator spend, deliberate)",
)
async def test_list_repos_dispatches_through_the_rail_not_the_help_menu(
    e2e_client, e2e_byoc_auth, monkeypatch, caplog
):
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
        print(f"\n[{msg}] decision: {[d[:220] for d in decision][:1]}")
        print(f"[{msg}] action={action!r} reply: {reply[:260].replace(chr(10), ' ⏎ ')}")
        assert (
            decision and '"route": "inversion"' in decision[0]
        ), f"{msg}: not routed by the Inversion"
        assert f'"operation": "{op}"' in decision[0], f"{msg}: expected {op}"
        assert action != "portfolio_help", f"{msg}: fell into the portfolio help menu"
        assert "I can help you manage your projects" not in reply, f"{msg}: help-menu copy"
