"""#1597 backlog item / #1518 — conversation_turns.intent is non-null after a REAL chat turn.

WHAT THIS VERIFIES (m-43 — name the layer): real-turn HTTP + persistence.
The #1518 fix wired the resolved intent label through
IntentService._save_conversation_turn → ConversationManager → repository, and
its own text says the proof must be "a post-cut spot-check that
conversation_turns.intent is non-null after a REAL chat turn" — because the
dev DB's non-null rows were all test-seed shapes written straight to the
repository (bare "question"/"statement" at microsecond intervals), which is
exactly the layer that CANNOT prove the live write path. This test drives the
turn through POST /api/v1/intent against a real server process and then reads
the very rows that turn persisted.

The turns are deterministic (pre-classified reminder path) so this never
depends on LLM credentials. #1518's own fix commit states the persisted shape:
"category:action" or bare category, lowercase.

Issue: #1597 (item 1: #1518)
"""

import re

import pytest
from sqlalchemy import text

# The #1518 commit's stated shape: lowercase "category:action" or bare category.
_INTENT_LABEL_RE = re.compile(r"^[a-z_]+(:[a-z_]+)?$")


@pytest.mark.live
class TestIntentRecordedLive:
    async def test_real_turns_persist_non_null_intent(self, turn_driver, live_db_session):
        """Two real turns (a create and a clarify); EVERY persisted turn row
        for the session must carry a non-null, fix-shaped intent label."""
        session_id = turn_driver.new_session()

        body1 = turn_driver.turn(
            "Remind me to run the live verification suite tomorrow at 10am",
            session_id=session_id,
        )
        assert "Reminder saved" in body1.get("message", ""), (
            f"Turn 1 did not take the deterministic reminder path: "
            f"{body1.get('message', '')[:300]!r}"
        )

        body2 = turn_driver.turn(
            "Remind me to stretch at 25:99",
            session_id=session_id,
        )
        assert "couldn't work out" in body2.get("message", ""), (
            f"Turn 2 did not take the deterministic clarify path: "
            f"{body2.get('message', '')[:300]!r}"
        )

        rows = (
            await live_db_session.execute(
                text(
                    "SELECT id, intent, user_message FROM conversation_turns "
                    "WHERE conversation_id = :sid ORDER BY created_at"
                ),
                {"sid": session_id},
            )
        ).fetchall()

        assert len(rows) >= 2, (
            f"Expected at least 2 persisted turns for session {session_id}, "
            f"found {len(rows)} — the live write path did not persist the turns "
            "this test just drove."
        )

        # THE #1518 claim, measured at the row (m-44: the fix commit is a
        # claim; the column value after a live turn is the measurement):
        for row in rows:
            turn_id, intent, user_message = row
            assert intent is not None and intent != "", (
                f"conversation_turns.intent is NULL/empty on a LIVE turn "
                f"(turn id={turn_id}, user_message={str(user_message)[:80]!r}) — "
                "this is the exact defect #1518 claims to have fixed."
            )
            assert _INTENT_LABEL_RE.match(intent), (
                f"conversation_turns.intent={intent!r} does not match the "
                "#1518 fix's stated shape (lowercase 'category:action' or "
                "bare category) — looks like a test-seed shape, not the "
                "live derivation."
            )

        # Evidence for the issue record: print the actual persisted labels.
        print(
            "\n#1518 live evidence — persisted intent labels for session "
            f"{session_id}: {[(str(r[2])[:50], r[1]) for r in rows]}"
        )
