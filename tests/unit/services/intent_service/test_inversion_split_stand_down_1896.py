"""#1896 — the live consult stands down on a turn surface 1 would SPLIT.

A live route replaces the whole classify_multiple block, so a two-part
message answered by one routed operation silently dropped its other half
(found by the #1595 unit-4 design probe, 2026-09-25, the day every read wave
went live). Layer: the consult module with the deterministic router stub —
no LLM; the split probe is the real PreClassifier.

#1595 Phase 3 (second deletion, 2026-09-27): the original SPLIT_TURN
("what are my todos and what time is it") used TODO_QUERY_PATTERNS to
claim its first half — that list's literals are now deleted, so the turn
no longer splits into 2 intents at surface 1 (it degrades to a single
temporal claim, defeating the point of this module — the guard needs a
GENUINE two-claim split to prove stand-down against). Swapped for "give me
my standup and what time is it" (STATUS_PATTERNS + TEMPORAL_PATTERNS,
unaffected by that deletion) — same shape, same point: a real split still
stands the consult down before any router call.

#1595 Phase 3 (fourth deletion, 2026-10-01): TEMPORAL_PATTERNS is now ALSO
`[]` — the "give me my standup and what time is it" swap above degrades
the SAME way the original did (a single STATUS claim, no split). Swapped
AGAIN, to "give me my standup and what should i do next" (STATUS_PATTERNS +
PRIORITY_PATTERNS, both unaffected by any of the five deletions to date) —
confirmed directly (detect_multiple_intents still returns exactly 2
intents for it), same idiom as the first two deletions' "give me my
standup" conversions elsewhere in this test family.

#1595 Phase 3 (sixth deletion, 2026-10-02): PRIORITY_PATTERNS is now ALSO
`[]` — the "give me my standup and what should i do next" swap above
degrades the SAME way, a third time (a single STATUS claim, no split).
Swapped AGAIN, to "give me my standup and what branch are we on"
(STATUS_PATTERNS + LOCAL_GIT_STATUS_PATTERNS, neither scheduled for
deletion — STATUS_PATTERNS/GUIDANCE_PATTERNS deliberately avoided for the
SECOND half specifically, both being the next two lists scheduled for
deletion in this epic) — confirmed directly (detect_multiple_intents still
returns exactly 2 intents: local_git_status_query + get_project_status),
same idiom as the first three deletions' "give me my standup" conversions
elsewhere in this test family.

#1595 Phase 3 (seventh deletion, 2026-10-02, PARTIAL): STATUS_PATTERNS'
own \bmy standup\b literal is gone (52 of 56 deleted — STATUS_PATTERNS now
keeps only \bcurrent work\b, \bproject overview\b, \bproject landscape\b,
\bnext milestone\b). This is the FIRST time this test family has had to
survive its OWN first-half list surviving a deletion but losing the
specific literal it used — STATUS_PATTERNS itself is NOT scheduled for
further deletion (it's done, partially), so this swap should be durable.
Swapped the STATUS half from "give me my standup" to "can you summarize my
current work" (matches the surviving \bcurrent work\b literal) in BOTH
SPLIT_TURN and SINGLE_TURN below — confirmed directly (detect_multiple_intents
returns exactly 2 intents for the split turn, 1 for the single turn), same
idiom as the first four deletions' conversions above.
"""

import pytest

from services.intent_service import inversion_live
from services.intent_service.pre_classifier import PreClassifier

SPLIT_TURN = "can you summarize my current work and what branch are we on"
SINGLE_TURN = "can you summarize my current work"


def test_the_probe_shape_is_real():
    # Denominator: the exact phrasing the guard exists for is split by surface 1
    # (2 intents) and its single-topic sibling is not.
    assert len(PreClassifier.detect_multiple_intents(SPLIT_TURN).intents) == 2
    assert len(PreClassifier.detect_multiple_intents(SINGLE_TURN).intents) <= 1


@pytest.mark.asyncio
async def test_split_turn_stands_down_before_any_router_call(monkeypatch):
    monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, "read_status")
    calls = []

    async def _never(*a, **k):  # the router must not be consulted at all
        calls.append(1)
        raise AssertionError("router consulted on a split turn")

    from services.intent_service import inversion_router as ir

    monkeypatch.setattr(ir, "route", _never)  # the real router entry the consult awaits
    decisions = []
    monkeypatch.setattr(
        inversion_live, "_log_decision", lambda *a, **k: decisions.append(k), raising=True
    )
    out = await inversion_live.consult_inversion_live(
        SPLIT_TURN, session_id="s-1896", user_id="u-1896", intent_service=None
    )
    assert out is None
    assert not calls
    assert decisions and decisions[-1]["reason"] == "multi_intent_split_stand_down"
    assert decisions[-1]["sibling_count"] == 2


@pytest.mark.asyncio
async def test_default_empty_stays_dark_no_probe(monkeypatch):
    monkeypatch.delenv(inversion_live.LIVE_CATEGORIES_ENV, raising=False)
    probed = []
    monkeypatch.setattr(
        PreClassifier,
        "detect_multiple_intents",
        staticmethod(lambda m: probed.append(m) or None),
    )
    out = await inversion_live.consult_inversion_live(
        SPLIT_TURN, session_id="s", user_id="u", intent_service=None
    )
    assert out is None
    assert probed == []  # zero work when the flag is empty — the pinned invariant
