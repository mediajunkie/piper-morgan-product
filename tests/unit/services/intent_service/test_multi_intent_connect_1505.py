"""#1505: the multi-intent path drops integration-connect asks paired with anything.

Found during the #1471 blast-radius probe (2026-08-07): ``detect_multiple_intents``
had no INTEGRATION_CONNECT pattern group, so an integration-connect ask riding
with any other matched group was silently dropped on the multi path —
'hi piper, connect my github' resolved to ``[(conversation, greeting)]`` and the
user got a greeting back. Because ``classify_multiple`` returns any non-empty
detection result, the LLM never saw the message either: the drop was total.

Calendar was the ONLY covered integration, and only via the #1471 TEMPORAL
substitution special-case (the temporal `\\bmy calendar\\b` pattern happened to
match the same words). github/slack/notion — and calendar phrasings that dodge
the temporal patterns, like 'link my google calendar' — were invisible.

The fix (per the issue's fix shape): a general INTEGRATION_CONNECT group in the
``pattern_groups`` table, checked BEFORE TEMPORAL, guarded by the shared
``_integration_connect_match`` (so the #862 repo-lane and #1471 event-write
blockers hold on this path too); the #1471 substitution special-case retires in
favor of the group + the existing GUIDANCE dedupe + a TEMPORAL suppression that
preserves the substitution era's behavior byte-for-byte on calendar collisions.

This is PLUMBING parity, not a new surface-1 claim: the single-intent path
(``pre_classify``) has claimed every one of these phrasings since #1417/#1471.
No new extraction regex — ``INTEGRATION_CONNECT_PATTERNS`` is reused as-is
(TestExtractionPatternRatchet ceilings untouched).

#1595 Phase 3, thirty-first deletion (2026-10-29, issue 2195):
INTEGRATION_CONNECT_PATTERNS is now `[]` (tombstoned). The pattern-groups
entry and its blocker-guarded branch survive but can never claim. The #1505
defect (a connect ask silently DROPPED beside a greeting) cannot recur by a
different route: the greeting now declines when a substantive clause rides
with it (#1416 on the multi path, #1924), so the multi path returns an EMPTY
result, ``classify_multiple`` falls through, and the whole message reaches the
Inversion router, which routes the connect ask to get_contextual_guidance
(corpus: 'hi piper, connect my github' REVIEW-agrees @0.8). The pins below are
converted to that two-part fact (surface 1 claims nothing, the stubbed router
routes to guidance), not deleted.
"""

import pytest

from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory
from tests.unit.services.intent_service._inversion_pin_helper import (
    assert_inversion_routes,
)


async def _routes_to_guidance(monkeypatch, message: str):
    return await assert_inversion_routes(
        monkeypatch,
        message,
        live_categories="read_canonical",
        expected_action="get_contextual_guidance",
    )


def _resolved(result):
    return [(i.category, i.action) for i in result.intents]


# ---------------------------------------------------------------------------
# The defect: greeting + connect keeps BOTH parts, for every integration —
# not just the calendar special case. RED before the #1505 fix.
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "message",
    [
        "hi piper, connect my github",  # issue verbatim
        "hi piper, connect my slack",
        "hi piper, connect my notion",
        # calendar phrasing that dodges TEMPORAL's `\bmy calendar\b`, so the
        # #1471 substitution never covered it — dropped until #1505
        "hey, link my google calendar",
    ],
)
async def test_greeting_plus_connect_keeps_both_parts_1505(message, monkeypatch):
    """Thirty-first deletion: the connect ask is never dropped — surface 1
    claims NOTHING (not a greeting-only result that would swallow the ask),
    and the router routes the whole message to guidance, with the #1460
    original_message field populated."""
    result = PreClassifier.detect_multiple_intents(message)
    assert _resolved(result) == [], (
        f"{message!r} resolved {_resolved(result)} — a non-empty surface-1 "
        "result without the connect ask would drop it (#1505)"
    )
    assert not result.is_multi_intent
    routed = await _routes_to_guidance(monkeypatch, message)
    assert routed.original_message == message  # #1460 field discipline


def test_pattern_lists_name_the_connect_claim_1505():
    """Pre-claim shadow probe threading: lists stay aligned with intents.
    Thirty-first deletion: no list claims the connect ask now, so both are
    empty (INTEGRATION_CONNECT_PATTERNS can never be named)."""
    result = PreClassifier.detect_multiple_intents("hi piper, connect my github")
    assert len(result.pattern_lists) == len(result.intents)
    assert "INTEGRATION_CONNECT_PATTERNS" not in result.pattern_lists
    assert result.pattern_lists == []


# ---------------------------------------------------------------------------
# #1471 parity: the calendar collision family behaves byte-for-byte as the
# substitution era did. GREEN before and after — these guard the retirement.
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_calendar_pairing_parity_1471(monkeypatch):
    """Thirty-first deletion: no TEMPORAL phantom (the #1471 property); the
    multi path claims nothing and the router routes guidance."""
    result = PreClassifier.detect_multiple_intents("hi piper, connect my calendar")
    categories = {i.category for i in result.intents}
    assert IntentCategory.TEMPORAL not in categories
    assert _resolved(result) == []
    await _routes_to_guidance(monkeypatch, "hi piper, connect my calendar")


@pytest.mark.asyncio
async def test_single_calendar_connect_parity_1471(monkeypatch):
    result = PreClassifier.detect_multiple_intents("connect my calendar")
    assert _resolved(result) == []
    await _routes_to_guidance(monkeypatch, "connect my calendar")


def test_guidance_dedupe_survives_retirement_1471():
    """'help me set up my calendar' once matched the #487 GUIDANCE patterns
    AND the connect group — exactly one guidance intent came out (the 1471
    dedupe). Thirty-first deletion: both lists are `[]`; surface 1 produces
    no guidance intent, so no duplicate is possible."""
    result = PreClassifier.detect_multiple_intents("help me set up my calendar")
    guidance = [
        i
        for i in result.intents
        if i.category == IntentCategory.GUIDANCE and i.action == "get_contextual_guidance"
    ]
    assert len(guidance) <= 1
    assert guidance == []


# ---------------------------------------------------------------------------
# The single-ask shape now claims on the multi path too (same destination the
# single path has resolved to since #1417 — one fewer fall-through hop).
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_single_connect_ask_claims_on_multi_path_1505(monkeypatch):
    """Thirty-first deletion: both entry surfaces decline identically (parity
    kept), and the router routes the ask to guidance."""
    result = PreClassifier.detect_multiple_intents("connect my github")
    assert _resolved(result) == []
    assert not result.is_multi_intent
    assert PreClassifier.pre_classify("connect my github") is None
    await _routes_to_guidance(monkeypatch, "connect my github")


# ---------------------------------------------------------------------------
# Blockers hold on the multi path: repo lane (#862) and event-writes (#1471)
# never flip into setup guidance, greeting or no greeting.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "message",
    [
        "hi piper, add a meeting to my calendar",  # event-write blocker (#1471)
        "add an event to my calendar",
        "hi piper, connect my repo to the project",  # repo-lane blocker (#862)
        "connect the mediajunkie/piper-morgan-product repo",
    ],
)
def test_blockers_hold_on_multi_path_1505(message):
    result = PreClassifier.detect_multiple_intents(message)
    hijacked = [
        i
        for i in result.intents
        if i.action == "get_contextual_guidance" and i.context.get("setup_target")
    ]
    assert not hijacked, f"blocked shape reached the connect lane on the multi path: {message!r}"


# ---------------------------------------------------------------------------
# TEMPORAL survives when no connect ask rides along (the suppression is
# conditional on a connect claim, not a blanket skip).
# ---------------------------------------------------------------------------


def test_temporal_still_claims_without_connect_1505():
    """#1595 Phase 3 fourth deletion (2026-10-01): TEMPORAL_PATTERNS is now
    `[]` — "what time is it" no longer claims at surface 1 with or without a
    connect ask riding along (the property this test originally pinned, that
    the #1471 suppression is conditional on a connect claim rather than a
    blanket skip, has nothing left to condition on). Only the greeting half
    survives now; see test_multi_intent_temporal_span_1755.py's identically
    updated sibling for the fuller #1755 span-aware-suppression context."""
    result = PreClassifier.detect_multiple_intents("hi piper, what time is it")
    # #1924 (2026-10-03): the greeting-only remainder no longer claims a
    # message that asks something (#1416 rule on the multi path) — it
    # declines to full classification instead of swallowing the question.
    assert (IntentCategory.TEMPORAL, "get_current_time") not in _resolved(result)
    assert _resolved(result) == []


# ---------------------------------------------------------------------------
# E2E through the real classifier entry: classify_multiple returns both parts
# (this is the dominant chat entry — the drop was invisible to the LLM lane
# because any non-empty detection result returns immediately).
# ---------------------------------------------------------------------------


async def test_classify_multiple_returns_both_parts_1505(monkeypatch):
    """Thirty-first deletion: classify_multiple's surface-1 leg
    (detect_multiple_intents) returns empty, so it never short-circuits with a
    greeting-only result; the LLM leg it falls to is not exercised here (no
    LLM in unit tests). The served answer is the router's (stubbed here)."""
    result = PreClassifier.detect_multiple_intents("hi piper, connect my github")
    assert _resolved(result) == []
    await _routes_to_guidance(monkeypatch, "hi piper, connect my github")
