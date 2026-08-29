"""Worked example (#1621): a formerly-manual verification, scripted at the LIVE layer.

WHAT THIS VERIFIES (m-43 — name the layer): real-turn HTTP. A real server
process (env-stripped launch), a real login (bcrypt + JWT cookie), real
POST /api/v1/intent turns over TCP, real DB rows checked afterward. This is
the surface PM actually touches when typing in the chat box — one layer above
tests/e2e/'s in-process ASGI, two above process_intent unit pins.

WHAT IT DOES NOT VERIFY: the rendered UI (template/JS layer — a curl-shaped
200 with the right body is NOT proof the message displays; see
feedback_ui_fix_requires_template_render_test_not_curl_200).

THE FORMERLY-MANUAL VERIFICATION BEING CONVERTED:
    The reminder create + clarify exchange — the #903/#1490/#1562 family that
    until now was verified by a human typing into the live chat window
    (e.g. the #1562 live checks). Chosen because the whole path is
    deterministic: "remind me to X <time>" is claimed by the pre-classifier
    (surface 1, no LLM), dispatched down the action rail to the todo handler,
    and persisted to todo_items — so this example exercises login, cookie
    auth, intent POST, dispatch, handler, and persistence WITHOUT depending
    on LLM credentials or nondeterministic prose.

RUN IT:
    PIPER_LIVE=1 POSTGRES_PORT=5433 venv/bin/python -m pytest tests/live/ -v \
        -o addopts="--import-mode=importlib"

Issue: #1621
"""

import pytest
from sqlalchemy import text


@pytest.mark.live
class TestReminderLive:
    async def test_reminder_create_then_clarify_live(self, turn_driver, live_db_session):
        """One conversation, two real turns: a create that persists, then an
        unbindable-time clarify that must NOT persist."""
        user = turn_driver.user
        session_id = turn_driver.new_session()

        # --- Turn 1: reminder create (deterministic pre-classified path) ---
        body = turn_driver.turn(
            "Remind me to check the ratchet suite tomorrow at 9am",
            session_id=session_id,
        )
        assert body.get("error") is None, f"Turn returned error: {body.get('error')}"
        message = body.get("message", "")
        assert (
            "Reminder saved" in message
        ), f"Expected the #903 confirmation shape, got: {message[:300]!r}"
        assert (
            "ratchet suite" in message
        ), f"Confirmation should echo the task text, got: {message[:300]!r}"

        # The claim "saved" must be TRUE at the persistence layer, not just in
        # the prose (m-44: the message is a claim; the row is the measurement).
        rows = (
            await live_db_session.execute(
                text(
                    """
                    SELECT i.text, t.reminder_date
                    FROM todo_items t JOIN items i ON i.id = t.id
                    WHERE t.owner_id = CAST(:uid AS uuid)
                      AND t.reminder_date IS NOT NULL
                    """
                ),
                {"uid": user.user_id},
            )
        ).fetchall()
        assert len(rows) == 1, (
            f"Expected exactly 1 persisted reminder for {user.username}, "
            f"found {len(rows)}: {rows!r}"
        )
        saved_text, reminder_date = rows[0]
        assert "ratchet suite" in saved_text
        assert reminder_date is not None

        # --- Turn 2: explicit-but-unbindable time → honest clarify (#1490) ---
        body2 = turn_driver.turn(
            "Remind me to stretch at 25:99",
            session_id=session_id,
        )
        message2 = body2.get("message", "")
        assert "couldn't work out" in message2 and "25:99" in message2, (
            f"Expected the #1490 honest-ask (echoing the unparsed time), "
            f"got: {message2[:300]!r}"
        )

        # The clarify must not have silently saved anything (#1490 invariant:
        # an explicit time is never replaced by a guessed default).
        count_after = (
            await live_db_session.execute(
                text(
                    "SELECT COUNT(*) FROM todo_items "
                    "WHERE owner_id = CAST(:uid AS uuid) AND reminder_date IS NOT NULL"
                ),
                {"uid": user.user_id},
            )
        ).scalar()
        assert (
            count_after == 1
        ), f"Clarify turn must not persist a reminder; count went 1 → {count_after}"

        # Both turns rode the same conversation; the server auto-created it
        # for this session (#731) and owns it to this user.
        conv = (
            await live_db_session.execute(
                text("SELECT user_id FROM conversations WHERE id = :sid"),
                {"sid": session_id},
            )
        ).fetchone()
        assert conv is not None, "Conversation was not auto-created for the session"
        assert (
            conv[0] == user.user_id
        ), f"Conversation owner mismatch: {conv[0]!r} != {user.user_id!r}"

    async def test_login_identity_live(self, turn_driver):
        """The cookie jar really authenticates: /api/v1/auth/me sees the
        throwaway user, through the same client the turns use."""
        resp = turn_driver.get("/api/v1/auth/me")
        assert resp.status_code == 200, f"auth/me failed: {resp.status_code} {resp.text[:300]}"
        body = resp.json()
        assert (
            body.get("username") == turn_driver.user.username
        ), f"auth/me identity mismatch: {body!r}"
