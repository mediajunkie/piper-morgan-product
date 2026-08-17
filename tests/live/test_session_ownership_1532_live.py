"""#1597 backlog item / #1532 — two REAL accounts exchange a session UUID: mutual not-found.

WHAT THIS VERIFIES (m-43 — name the layer): real-turn HTTP, two principals.
The #1532 fix put an ownership check in the chat path (web/api/routes/intent.py:
owner mismatch → HTTP 404 "Conversation not found for this account.", raised
BEFORE process_intent so there is no hydration and no append). Unit + route
coverage was thorough (67 passed), but the issue's own stated live check —
"two accounts exchanging a session UUID, expecting mutual not-found" — had
never been performed. This test performs it: two throwaway users, each with a
real login and a real conversation, each posting the OTHER's session UUID to
POST /api/v1/intent over a real socket.

Also measured at the persistence layer (m-44): the cross-account attempt must
leave the victim's conversation untouched — turn count unchanged, no row
carrying the intruder's message.

Issue: #1597 (item 2: #1532)
"""

import pytest
from sqlalchemy import text


async def _turn_rows(db, session_id):
    return (
        await db.execute(
            text(
                "SELECT user_message FROM conversation_turns "
                "WHERE conversation_id = :sid ORDER BY created_at"
            ),
            {"sid": session_id},
        )
    ).fetchall()


@pytest.mark.live
class TestSessionOwnershipLive:
    async def test_cross_account_session_exchange_is_mutual_not_found(
        self, turn_driver, turn_driver_b, live_db_session
    ):
        user_a = turn_driver.user
        user_b = turn_driver_b.user
        assert user_a.user_id != user_b.user_id

        # --- Each account drives a REAL turn in its own session -----------
        session_a = turn_driver.new_session()
        body_a = turn_driver.turn(
            "Remind me to review the ownership audit tomorrow at 9am",
            session_id=session_a,
        )
        assert "Reminder saved" in body_a.get("message", "")

        session_b = turn_driver_b.new_session()
        body_b = turn_driver_b.turn(
            "Remind me to rotate my keys tomorrow at 11am",
            session_id=session_b,
        )
        assert "Reminder saved" in body_b.get("message", "")

        # Both conversations exist and are owned correctly (precondition —
        # without this the 404s below would prove nothing; m-44).
        for sid, owner in ((session_a, user_a.user_id), (session_b, user_b.user_id)):
            row = (
                await live_db_session.execute(
                    text("SELECT user_id FROM conversations WHERE id = :sid"),
                    {"sid": sid},
                )
            ).fetchone()
            assert row is not None, f"Conversation {sid} was not created"
            assert str(row[0]) == str(owner), (
                f"Precondition failed: conversation {sid} owned by {row[0]!r}, "
                f"expected {owner!r}"
            )

        turns_a_before = await _turn_rows(live_db_session, session_a)
        turns_b_before = await _turn_rows(live_db_session, session_b)

        intruder_msg_b = "What did we talk about earlier in this conversation?"
        intruder_msg_a = "Summarize this conversation for me please"

        # --- THE EXCHANGE: B posts A's session UUID ------------------------
        # NOTE on the expected body: the route raises 404 detail="Conversation
        # not found for this account.", but the app-wide HTTPException handler
        # (web/app.py http_exception_handler) rewrites EVERY 404 body to the
        # generic friendly copy "I couldn't find that. It may have been moved
        # or deleted." — observed live 2026-08-16. The refusal is the 404
        # itself; the generic body is fine (it confirms nothing about the
        # conversation's existence, which is the #1532 intent).
        resp = turn_driver_b.raw_turn(intruder_msg_b, session_id=session_a)
        assert resp.status_code == 404, (
            f"#1532 FAILED LIVE: user B posting user A's session UUID got "
            f"HTTP {resp.status_code}, expected 404. Body: {resp.text[:500]}"
        )
        assert "couldn't find" in resp.text, f"Unexpected refusal body: {resp.text[:300]}"
        # Never confirm existence or ownership to the intruder:
        assert "different" not in resp.text and "principal" not in resp.text

        # --- ...and A posts B's session UUID (the MUTUAL half) -------------
        resp2 = turn_driver.raw_turn(intruder_msg_a, session_id=session_b)
        assert resp2.status_code == 404, (
            f"#1532 FAILED LIVE: user A posting user B's session UUID got "
            f"HTTP {resp2.status_code}, expected 404. Body: {resp2.text[:500]}"
        )
        assert "couldn't find" in resp2.text, f"Unexpected refusal body: {resp2.text[:300]}"

        # --- Persistence unchanged: refusal happened BEFORE append ---------
        turns_a_after = await _turn_rows(live_db_session, session_a)
        turns_b_after = await _turn_rows(live_db_session, session_b)
        assert len(turns_a_after) == len(turns_a_before), (
            f"User A's conversation grew from {len(turns_a_before)} to "
            f"{len(turns_a_after)} turns after B's refused post — the append "
            "was NOT prevented."
        )
        assert len(turns_b_after) == len(turns_b_before), (
            f"User B's conversation grew from {len(turns_b_before)} to "
            f"{len(turns_b_after)} turns after A's refused post."
        )
        all_messages = [str(r[0]) for r in turns_a_after + turns_b_after]
        assert intruder_msg_b not in all_messages
        assert intruder_msg_a not in all_messages

        # --- The REST surface agrees (the contract the chat path now mirrors)
        rest_b = turn_driver_b.get(f"/api/v1/conversations/{session_a}")
        assert rest_b.status_code == 404, (
            f"REST cross-account read of A's conversation by B returned "
            f"{rest_b.status_code}, expected 404: {rest_b.text[:300]}"
        )
        rest_a = turn_driver.get(f"/api/v1/conversations/{session_b}")
        assert rest_a.status_code == 404, (
            f"REST cross-account read of B's conversation by A returned "
            f"{rest_a.status_code}, expected 404: {rest_a.text[:300]}"
        )

        # --- Owners still work: the guard rejects intruders, not owners ----
        body_a2 = turn_driver.turn(
            "Remind me to file the evidence at 4pm tomorrow", session_id=session_a
        )
        assert "Reminder saved" in body_a2.get("message", ""), (
            "Owner's own follow-up turn failed after the exchange — the guard "
            f"is over-broad: {body_a2.get('message', '')[:300]!r}"
        )

        print(
            "\n#1532 live evidence — B→A: HTTP "
            f"{resp.status_code} {resp.text[:120]!r}; A→B: HTTP "
            f"{resp2.status_code} {resp2.text[:120]!r}; "
            f"A turn count {len(turns_a_before)}→{len(turns_a_after)}, "
            f"B turn count {len(turns_b_before)}→{len(turns_b_after)}"
        )
