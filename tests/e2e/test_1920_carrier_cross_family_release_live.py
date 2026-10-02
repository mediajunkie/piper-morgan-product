"""#1920 — LIVE proof that an armed reminder-pick carrier releases a
cross-family write command instead of re-asking.

Marked ``llm``: real app + DB + the served router. Seeds two reminders, arms
the pick-target carrier with an ambiguous clear ("clear the reminder" — two
candidates, no referent), then sends "close issue #108" mid-pick. Before
#1920 (alpha v164): "Still not sure which one". After: the carrier releases
and the turn is routed normally (GitHub isn't connected on the test user, so
the honest outcome is the close path's own answer — any answer that is NOT
the pick re-ask proves the release).
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


@pytest.mark.skipif(
    not os.environ.get("PIPER_E2E_LIVE_HEADER_KEY"),
    reason="live probe: set PIPER_E2E_LIVE_HEADER_KEY (operator spend, deliberate)",
)
async def test_cross_family_write_releases_the_pick(e2e_client, e2e_byoc_auth, monkeypatch, caplog):
    monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, ALPHA_FLAG)
    caplog.set_level("INFO")
    sid = str(uuid4())

    async def turn(msg):
        r = await e2e_client.post(
            "/api/v1/intent", json={"message": msg, "session_id": sid}, **e2e_byoc_auth
        )
        assert r.status_code == 200, r.text[:300]
        return r.json().get("message") or ""

    for seed in [
        "remind me tomorrow at 9am to Review the PR",
        "remind me tomorrow at 10am to hydrate",
    ]:
        await turn(seed)
    arm = await turn("clear the standup reminder")  # named target matches neither → pick carrier arms
    print("\narm:", arm.replace("\n", " ⏎ ")[:300])
    assert "never mind" in arm.lower(), "the pick prompt must carry the exit copy"
    caplog.clear()
    reply = await turn("close issue #108")
    events = [r.getMessage() for r in caplog.records]
    released = [e[:300] for e in events if "armed_carrier_cross_family_release" in e]
    reasked = [
        e for e in events if "pick_target_reask" in e or "reminder_clear_pick_target_reasked" in e
    ]
    print("released:", released[:1])
    print("reply:", reply.replace("\n", " ⏎ ")[:400])
    assert released, "expected the cross-family release to fire; see events"
    assert "still not sure which one" not in reply.lower()
