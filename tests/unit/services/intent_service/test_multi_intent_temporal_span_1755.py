"""#1755: the multi-intent path's TEMPORAL-skip was group-level, not span-aware.

`detect_multiple_intents` suppresses a TEMPORAL match whenever an
integration-connect ask ALSO claims in the same message (#1471) — because
'connect my calendar' matches the temporal `\\bmy calendar\\b` pattern on the
SAME words as the connect ask, and without the skip the user would get a
current-time phantom beside the setup guidance.

The #1471/#1505 skip was a BLANKET group-level suppression: any connect claim
dropped the WHOLE TEMPORAL group, including a genuinely separate temporal ask
riding elsewhere in the message — 'what time is it? also connect my github'
resolved to connect-only, silently losing the time question (found during the
#1505 repro probe, 2026-09-12).

The fix is span-aware, not group-level: a TEMPORAL match is suppressed only
when its span OVERLAPS (or is contained in) the integration-connect match's
span; a TEMPORAL match whose span is DISJOINT from the connect span survives.
No new pattern literal — `PreClassifier._temporal_disjoint_from_connect`
reuses `TEMPORAL_PATTERNS` as-is (TestExtractionPatternRatchet-clean; the
`re.finditer` call inside it passes a bare loop-variable pattern, never an
inline literal, so the ratchet's counter does not see it as a new pattern).

The #1471 calendar-collision parity (`test_calendar_pairing_parity_1471` et
al. in test_multi_intent_connect_1505.py) is UNCHANGED by this fix — those
cases have the temporal words CONTAINED WITHIN the connect span, so they hit
the "overlap" branch and stay suppressed, byte-for-byte.

Ordering note (see docstrings below): `pattern_groups` iterates in a FIXED
PRIORITY order, not message-word order.
`INTEGRATION_CONNECT_PATTERNS` sits BEFORE `TEMPORAL_PATTERNS` in that list,
so the connect intent is always appended to `intents` before a surviving
temporal intent — even when the temporal words come first in the actual
message text. This mirrors the pre-existing #1505 convention (e.g. greeting
is appended before connect because GREETING_PATTERNS precedes
INTEGRATION_CONNECT_PATTERNS in the same list) — priority order, not message
position.

#1595 Phase 3 fourth deletion (2026-10-01): TEMPORAL_PATTERNS is now `[]`
(tombstoned). `_temporal_disjoint_from_connect` (the span-aware helper this
file exists to pin) still exists and is still called, but its internal loop
now iterates zero literals, so it is permanently, structurally inert — there
is no TEMPORAL match left to be either suppressed-by-overlap or
survives-by-disjointness, because TEMPORAL never claims at surface 1 at all
any more, span or no span. Every test below is updated to pin the NEW
reality (no TEMPORAL claim ever, regardless of span) rather than deleted —
what remains verifiable and worth keeping is that the CONNECT/GUIDANCE lane's
own behavior is unaffected by TEMPORAL's departure. "What time is it" is now
served live via the Inversion (get_current_time_entry, flip_group
read_temporal) or the LLM classifier fallback, never via this span-aware
surface-1 mechanism.
"""

from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory
from tests.unit.services.intent_service._inversion_pin_helper import (
    assert_inversion_routes,
)


def _resolved(result):
    return [(i.category, i.action) for i in result.intents]


# ---------------------------------------------------------------------------
# The defect: a genuinely disjoint temporal ask survives alongside a connect
# claim. RED before the #1755 fix (temporal was silently dropped).
# ---------------------------------------------------------------------------


def test_disjoint_temporal_survives_connect_claim_1755():
    """Issue #1755 verbatim repro: the time question and the connect ask are
    unrelated parts of the same message.

    #1595 Phase 3 fourth deletion: TEMPORAL_PATTERNS is `[]` — the temporal
    half no longer claims (span-disjointness is moot with zero literals to
    match). Pinned directly: only the connect/GUIDANCE half survives now,
    and it is correctly single-intent (not multi) since there is only one
    surface-1 claim left."""
    # #1977 step 1 (2026-10-11): with TEMPORAL_PATTERNS gone, "what time is it"
    # is an UNCLAIMED leading clause beside the connect claim, so surface 1
    # DECLINES the whole turn rather than letting the connect handler take it
    # and drop the time question. The corpus row (INTEGRATION_CONNECT, expected
    # REVIEW) has the router's answer on file: get_current_time @0.9.
    result = PreClassifier.detect_multiple_intents("what time is it? also connect my github")
    assert (
        _resolved(result) == []
    ), f"resolved {_resolved(result)} — step 1 declines a claim set that leaves a substantive clause"
    assert not result.is_multi_intent


def test_disjoint_temporal_survives_connect_claim_reordered_1755():
    """Same shape, connect ask FIRST in the message text.

    #1595 Phase 3 fourth deletion: same update as the test above — the
    temporal half ("check my schedule") no longer claims at all."""
    # #1977 (residue rule): the connect claim leaves "check my schedule"
    # unclaimed (substantive second clause) -> surface 1 declines the turn
    # so the whole message reaches the router/classifier.
    result = PreClassifier.detect_multiple_intents("connect my slack and check my schedule")
    assert _resolved(result) == []
    assert not result.is_multi_intent


# ---------------------------------------------------------------------------
# The #1471 phantom must NOT return: temporal words CONTAINED WITHIN the
# connect span stay suppressed (span overlap, not disjoint).
# ---------------------------------------------------------------------------


async def test_connect_only_when_temporal_words_inside_connect_span_1755(monkeypatch):
    """'connect my calendar' — the temporal `\\bmy calendar\\b` pattern
    matches entirely INSIDE the connect match's span ('connect my
    calendar'). This is the original #1471 phantom shape: connect-only,
    exactly as before this fix.

    #1595 Phase 3 thirty-first deletion (2026-10-29): INTEGRATION_CONNECT_
    PATTERNS is `[]` too, so surface 1 claims nothing (no phantom is
    possible) and the router routes the ask to guidance."""
    result = PreClassifier.detect_multiple_intents("connect my calendar")
    assert _resolved(result) == []
    assert not result.is_multi_intent
    await assert_inversion_routes(
        monkeypatch,
        "connect my calendar",
        live_categories="read_canonical",
        expected_action="get_contextual_guidance",
    )


async def test_connect_only_when_temporal_words_inside_connect_span_with_greeting_1755(
    monkeypatch,
):
    """Same containment shape, paired with a greeting — TEMPORAL must not
    reappear (the #1471 parity pin's exact shape). Thirty-first deletion:
    the greeting declines with substantive residue and the connect lane is
    `[]`, so surface 1 claims nothing and the router routes guidance."""
    result = PreClassifier.detect_multiple_intents("hi piper, connect my calendar")
    categories = {i.category for i in result.intents}
    assert IntentCategory.TEMPORAL not in categories
    assert _resolved(result) == []
    await assert_inversion_routes(
        monkeypatch,
        "hi piper, connect my calendar",
        live_categories="read_canonical",
        expected_action="get_contextual_guidance",
    )


# ---------------------------------------------------------------------------
# Disjoint spans within a calendar-flavored message: a connect ask and a
# SEPARATE temporal ask about the calendar, not the same words.
# ---------------------------------------------------------------------------


def test_connect_and_temporal_disjoint_spans_1755():
    """'connect my slack and check my schedule' — the connect span covers
    only 'connect my slack'; a temporal `\\bmy schedule\\b` match would sit
    entirely outside it, IF TEMPORAL_PATTERNS still matched anything.

    #1595 Phase 3 fourth deletion: TEMPORAL_PATTERNS is `[]` — only the
    connect/GUIDANCE half survives now (same update as
    test_disjoint_temporal_survives_connect_claim_reordered_1755 above,
    which uses the identical message)."""
    # #1977 (residue rule): declined -- see the reordered test above.
    result = PreClassifier.detect_multiple_intents("connect my slack and check my schedule")
    assert _resolved(result) == []


# ---------------------------------------------------------------------------
# #1505 parity — TEMPORAL still claims normally with no connect ask at all
# (the suppression is conditional on a connect claim, never a standing
# blocker on TEMPORAL_PATTERNS itself).
# ---------------------------------------------------------------------------


def test_temporal_still_claims_without_connect_1755():
    """#1595 Phase 3 fourth deletion: TEMPORAL_PATTERNS is `[]` — "what time
    is it" no longer claims with or without a connect ask riding along
    (the property this test originally pinned — the suppression is
    conditional, not a blanket skip — has nothing left to condition on).
    Only the greeting half survives now."""
    result = PreClassifier.detect_multiple_intents("hi piper, what time is it")
    # #1924 (2026-10-03): the greeting-only remainder no longer claims a
    # message that asks something (#1416 rule on the multi path) — it
    # declines to full classification instead of swallowing the question.
    assert (IntentCategory.TEMPORAL, "get_current_time") not in _resolved(result)
    assert _resolved(result) == []


# ---------------------------------------------------------------------------
# E2E through the real classifier entry — the dominant chat path.
# ---------------------------------------------------------------------------


async def test_classify_multiple_returns_both_parts_1755():
    """#1595 Phase 3 fourth deletion: TEMPORAL_PATTERNS is `[]` — only the
    connect/GUIDANCE half survives through the real classifier entry now
    (same message, same update as test_disjoint_temporal_survives_connect_
    claim_1755 above, exercised through classify_multiple instead of
    detect_multiple_intents directly)."""
    # #1977 step 1 (2026-10-11): the surface-1 leg of classify_multiple
    # (detect_multiple_intents) now declines this turn (see the test above);
    # the LLM leg it then falls to is not exercised here (no LLM in unit tests).
    # The corpus row carries the served answer (router get_current_time @0.9).
    result = PreClassifier.detect_multiple_intents("what time is it? also connect my github")
    assert _resolved(result) == []
