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
unaffected by the deletion) — same shape, same point: a real split still
stands the consult down before any router call.
"""

import pytest

from services.intent_service import inversion_live
from services.intent_service.pre_classifier import PreClassifier

SPLIT_TURN = "give me my standup and what time is it"
SINGLE_TURN = "give me my standup"


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
