"""#1943 (Arch's (a), step 5): the SERVED answer for PM's 2026-10-05 sentence.

PM live, alpha v169: "Mark the first three complete and leave the fourth one
pending." completed ONE and said "Left the other one as is." The gate for
the fix is not ``route=inversion`` (yesterday's lesson — a route-level probe
proved nothing about the answer); it is the reply the user reads:

  turn 1 → the enumerating confirm, nothing changed:
           'Complete "A", "B" and "C"? Leaving "D". (yes/no)'
  turn 2 ("yes") → 'Marked 3 reminders done: …' + 'Left "D" as is.'

Marked ``llm``: real app + DB + the served router (local flag includes
``complete_todo``, which alpha's flag does not yet — the flip is PM's hand).
Seeds four due reminders through the REAL write path
(TodoManagementService.create_todo, the call handle_create_reminder makes),
under the authenticated principal, and removes them after.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import pytest

from services.intent_service import inversion_live

pytestmark = pytest.mark.llm

FLAG = (
    "read_status,read_referent,read_synthesis,create_todo,create_reminder,"
    "read_strategic,read_temporal,delete_todo,read_floor,read_floor_2,"
    "read_canonical,read_portfolio,complete_todo"
)
SEED = ["check the test card again", "check the test card again", "review the pr", "revise the pr"]
PM_SENTENCE = "Mark the first three complete and leave the fourth one pending."


async def _seed_due_reminders(user_id: str):
    from services.todo.todo_management_service import TodoManagementService

    svc = TodoManagementService()
    now = datetime.now(timezone.utc)
    made = []
    for i, text in enumerate(SEED):
        when = now - timedelta(hours=len(SEED) - i)  # oldest first, all in the past
        t = await svc.create_todo(
            user_id=UUID(user_id), text=text, priority="medium", reminder_date=when, due_date=when
        )
        assert t is not None and t.id, "seed failed to persist"
        made.append(t)
    return svc, made


@pytest.mark.skipif(
    not os.environ.get("PIPER_E2E_LIVE_HEADER_KEY"),
    reason="live probe: set PIPER_E2E_LIVE_HEADER_KEY (operator spend, deliberate)",
)
async def test_pm_first_three_served_answer_enumerates_then_completes_exactly_those(
    e2e_client, e2e_byoc_auth, e2e_test_user, monkeypatch, caplog
):
    monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, FLAG)
    caplog.set_level("INFO")
    user_id = e2e_test_user[0]
    svc, seeded = await _seed_due_reminders(user_id)
    session_id = str(uuid4())
    try:
        # ── turn 1: the ask ──────────────────────────────────────────────
        caplog.clear()
        r = await e2e_client.post(
            "/api/v1/intent",
            json={"message": PM_SENTENCE, "session_id": session_id},
            **e2e_byoc_auth,
        )
        assert r.status_code == 200, r.text[:300]
        body = r.json()
        reply = body.get("message") or ""
        decision = [
            x.getMessage() for x in caplog.records if "inversion_live_decision" in x.getMessage()
        ]
        print(f"\n[turn 1] decision: {[d[:240] for d in decision][:1]}")
        print(f"[turn 1] reply: {reply.replace(chr(10), ' ⏎ ')[:400]}")
        assert (
            decision and '"route": "inversion"' in decision[0]
        ), "turn 1 not served by the Inversion"
        assert (
            '"operation": "complete_todo"' in decision[0]
        ), "turn 1 did not route to complete_todo"
        # the SERVED answer, not the route:
        assert reply.startswith(
            'Complete "check the test card again", "check the test card again" and "review the pr"?'
        ), reply
        assert 'Leaving "revise the pr".' in reply, reply
        # the app appends its first-turn personalization notice after the
        # answer; the ASK is the first line
        assert reply.splitlines()[0].rstrip().endswith("(yes/no)"), reply
        assert body.get("requires_clarification") is True
        # nothing changed yet
        still_open = [
            t
            for t in await svc.list_todos(user_id=UUID(user_id), include_completed=False)
            if t.text in SEED
        ]
        assert len(still_open) == 4, [t.text for t in still_open]

        # ── turn 2: yes ─────────────────────────────────────────────────
        r2 = await e2e_client.post(
            "/api/v1/intent", json={"message": "yes", "session_id": session_id}, **e2e_byoc_auth
        )
        assert r2.status_code == 200, r2.text[:300]
        reply2 = r2.json().get("message") or ""
        print(f"[turn 2] reply: {reply2.replace(chr(10), ' ⏎ ')[:400]}")
        assert reply2.startswith("Marked 3 reminders done:"), reply2
        assert "review the pr" in reply2 and reply2.count("check the test card again") == 2, reply2
        assert 'Left "revise the pr" as is.' in reply2, reply2

        remaining = [
            t
            for t in await svc.list_todos(user_id=UUID(user_id), include_completed=False)
            if t.text in SEED
        ]
        assert [t.text for t in remaining] == ["revise the pr"], [t.text for t in remaining]
    finally:
        for t in seeded:
            try:
                await svc.delete_todo(todo_id=UUID(t.id), user_id=UUID(user_id))
            except Exception:  # cleanup is best-effort; the user fixture removes the rest
                pass
