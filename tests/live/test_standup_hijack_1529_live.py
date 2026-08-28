"""#1597 backlog item / #1529 — the standup-hijack sequence, replayed against a RUNNING server.

WHAT THIS VERIFIES (m-43 — name the layer): real-turn HTTP. PM's 2026-08-08
T6 hijack (nine attempts to execute one restore) is replayed with PM's
verbatim lines through POST /api/v1/intent against a real server process —
the layer the #1529 closure itself flagged as not yet re-run ("Verification
is unit-level; the nine-attempt live sequence has not been replayed against a
running server (see #1597)").

FIDELITY NOTE (honest scope): the replay is deterministic end-to-end — every
message in it is claimed by the pre-classifier, the guided-process seam, or
the #888/#1529 escape tiers, so no LLM credential is needed. Two deliberate
divergences from PM's original session, both in SETUP not in the defects
under test:
  1. PM's standup was left suspended by earlier session history; here the
     suspended state is produced with `/standup` + the #888 exact-match
     escape "cancel" (which suspends — same durable state, known path).
  2. PM had a real archived project (CoVa); the throwaway user has none, so
     "restore CoVa" takes the not-found branch — which mints EXACTLY the
     offer from PM's transcript ("Would you like me to list your archived
     projects?"), the offer whose "Yes please" was hijacked.

The three pinned defects, each replayed in its own session:
  1. offer-binding — "Yes please" after a contextual offer, with a suspended
     standup lurking, must bind to the OFFER (list archived projects), never
     resume the standup interview.
  2. refusal escape — the verbatim "i am not doing the standup right now.
     restore CoVa" mid-interview must END the flow (honest exit copy), never
     be transcribed into standup content.
  3. exit-phrase routing — "end standup" mid-interview must end the standup,
     never misroute to todo-complete ("Which todo would you like to
     complete?").

Issue: #1597 (item 4: #1529)
"""

import pytest
from sqlalchemy import text

# PM's verbatim transcript lines (2026-08-08 T6)
PM_YES_PLEASE = "Yes please"
PM_RESTORE = "restore CoVa"
PM_REFUSAL = "i am not doing the standup right now. restore CoVa"
PM_END_STANDUP = "end standup"

# The misroute copy #1529 documents ('end standup' → todo-complete lane)
TODO_MISROUTE = "Which todo would you like to complete?"

# Markers of the standup interview claiming/transcribing a turn
_INTERVIEW_MARKERS = ("yesterday", "Blockers", "blockers", "standup report")


async def _standup_states(db, session_id):
    rows = (
        await db.execute(
            text(
                "SELECT state, current_standup FROM standup_conversations "
                "WHERE session_id = :sid"
            ),
            {"sid": session_id},
        )
    ).fetchall()
    return rows


@pytest.mark.live
class TestStandupHijackReplayLive:
    async def test_offer_binding_yes_please_binds_to_offer_not_standup(
        self, turn_driver, live_db_session
    ):
        """Defect 1: with a suspended standup lurking, 'Yes please' after a
        contextual offer must execute the offer — not resume the interview."""
        session_id = turn_driver.new_session()

        # Setup: a suspended standup in the durable repo (the dormant
        # flow-starter that hijacked PM's affirmative).
        body = turn_driver.turn("/standup", session_id=session_id)
        assert (
            "standup" in body.get("message", "").lower()
        ), f"/standup did not start the interview: {body.get('message', '')[:300]!r}"
        body = turn_driver.turn("cancel", session_id=session_id)
        assert (
            "paused" in body.get("message", "").lower()
        ), f"#888 exact-match escape did not suspend: {body.get('message', '')[:300]!r}"
        states = await _standup_states(live_db_session, session_id)
        assert any(
            s == "suspended" for s, _ in states
        ), f"Setup failed: no suspended standup in DB for session (states={states!r})"

        # PM's transcript, verbatim: restore of a project that isn't found
        # mints the archived-projects offer...
        body = turn_driver.turn(PM_RESTORE, session_id=session_id)
        msg = body.get("message", "")
        # (The handler echoes the captured name lowercased — 'cova' —
        # observed live 2026-08-16; match case-insensitively.)
        assert (
            "couldn't find an archived project" in msg and "cova" in msg.lower()
        ), f"'restore CoVa' did not take the deterministic not-found branch: {msg[:300]!r}"
        assert (
            "Would you like me to list your archived projects?" in msg
        ), f"The contextual offer from PM's transcript was not made: {msg[:300]!r}"

        # ...and THE hijacked line: "Yes please".
        body = turn_driver.turn(PM_YES_PLEASE, session_id=session_id)
        msg = body.get("message", "")

        # The hijack shape, asserted dead: no standup interview resume.
        assert "standup" not in msg.lower(), (
            f"#1529 FAILED LIVE (offer-binding): 'Yes please' reached the "
            f"standup instead of the pending offer: {msg[:300]!r}"
        )
        # The offer's continuation, honored: the archived-projects listing
        # (throwaway user has none — the deterministic empty-list copy).
        assert "archived" in msg.lower(), (
            f"#1529 FAILED LIVE (offer-binding): 'Yes please' did not execute "
            f"the archived-projects offer: {msg[:300]!r}"
        )

        # And the suspended standup was not resurrected by the affirmative.
        states = await _standup_states(live_db_session, session_id)
        assert all(
            s in ("suspended", "abandoned", "complete") for s, _ in states
        ), f"'Yes please' reactivated the standup (states={states!r})"

        print(f"\n#1529 live evidence (offer-binding) — 'Yes please' answered with: {msg[:200]!r}")

    async def test_verbatim_refusal_escapes_and_is_not_transcribed(
        self, turn_driver, live_db_session
    ):
        """Defect 2: PM's verbatim refusal mid-interview ends the flow with
        honest copy; the protest is never composed into standup content."""
        session_id = turn_driver.new_session()

        body = turn_driver.turn("/standup", session_id=session_id)
        assert "standup" in body.get("message", "").lower()

        # One legitimate answer first — mid-gathering, like PM's session.
        body = turn_driver.turn("Worked on the live verification harness", session_id=session_id)

        # THE verbatim hostage line. allow_degraded: the residual
        # ("restore CoVa") flows to normal processing whose availability is
        # not this test's subject — the assertions below are.
        body = turn_driver.turn(PM_REFUSAL, session_id=session_id, allow_degraded=True)
        msg = body.get("message", "")

        # The honest exit copy (the #1529 refusal-prefix contract):
        assert "Okay — no standup. I've ended it." in msg, (
            f"#1529 FAILED LIVE (refusal): the verbatim refusal did not get "
            f"the honest exit copy: {msg[:400]!r}"
        )
        # The hostage shape, asserted dead: the refusal must not be
        # transcribed back as standup content.
        assert "Blockers: i am not doing" not in msg, (
            f"#1529 FAILED LIVE (refusal): the protest was transcribed into "
            f"the standup: {msg[:400]!r}"
        )

        # Persistence: the flow is closed and no standup content carries the
        # protest (m-44: the response copy is a claim; the row is the measure).
        states = await _standup_states(live_db_session, session_id)
        assert states, "Standup conversation row vanished"
        for state, content in states:
            assert state in ("abandoned", "suspended", "complete"), (
                f"#1529 FAILED LIVE (refusal): standup still active "
                f"(state={state!r}) after an explicit refusal"
            )
            assert "not doing the standup" not in (content or ""), (
                f"#1529 FAILED LIVE (refusal): protest transcribed into "
                f"persisted standup content: {content[:300]!r}"
            )

        # The flow no longer claims turns: the follow-up restore gets the
        # deterministic portfolio answer, not an interview question.
        body = turn_driver.turn(PM_RESTORE, session_id=session_id)
        msg2 = body.get("message", "")
        assert "couldn't find an archived project" in msg2, (
            f"#1529 FAILED LIVE (refusal): post-escape turn was not answered "
            f"by normal processing: {msg2[:300]!r}"
        )

        print(f"\n#1529 live evidence (refusal) — refusal answered with: {msg[:200]!r}")

    async def test_end_standup_ends_standup_not_todo_complete(self, turn_driver, live_db_session):
        """Defect 3: 'end standup' mid-interview ends the standup — it must
        never reach a classifier and misroute to the todo-complete lane."""
        session_id = turn_driver.new_session()

        body = turn_driver.turn("/standup", session_id=session_id)
        assert "standup" in body.get("message", "").lower()

        body = turn_driver.turn(PM_END_STANDUP, session_id=session_id)
        msg = body.get("message", "")

        assert TODO_MISROUTE not in msg, (
            f"#1529 FAILED LIVE (exit routing): 'end standup' misrouted to "
            f"todo-complete: {msg[:300]!r}"
        )
        assert "ended the standup" in msg, (
            f"#1529 FAILED LIVE (exit routing): 'end standup' did not return "
            f"the honest exit copy: {msg[:300]!r}"
        )

        states = await _standup_states(live_db_session, session_id)
        assert states and all(
            s in ("abandoned", "complete") for s, _ in states
        ), f"'end standup' left the flow non-terminal (states={states!r})"

        print(f"\n#1529 live evidence (exit) — 'end standup' answered with: {msg[:200]!r}")
