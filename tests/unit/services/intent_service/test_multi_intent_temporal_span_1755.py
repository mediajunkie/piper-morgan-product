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
    result = PreClassifier.detect_multiple_intents("what time is it? also connect my github")
    assert _resolved(result) == [
        (IntentCategory.GUIDANCE, "get_contextual_guidance"),
    ], f"resolved {_resolved(result)} — TEMPORAL_PATTERNS is deleted, it should never claim"
    connect = result.intents[0]
    assert connect.context.get("setup_target") == "github"
    assert not result.is_multi_intent


def test_disjoint_temporal_survives_connect_claim_reordered_1755():
    """Same shape, connect ask FIRST in the message text.

    #1595 Phase 3 fourth deletion: same update as the test above — the
    temporal half ("check my schedule") no longer claims at all."""
    result = PreClassifier.detect_multiple_intents("connect my slack and check my schedule")
    assert _resolved(result) == [
        (IntentCategory.GUIDANCE, "get_contextual_guidance"),
    ], f"resolved {_resolved(result)} — TEMPORAL_PATTERNS is deleted, it should never claim"
    connect = result.intents[0]
    assert connect.context.get("setup_target") == "slack"
    assert not result.is_multi_intent


# ---------------------------------------------------------------------------
# The #1471 phantom must NOT return: temporal words CONTAINED WITHIN the
# connect span stay suppressed (span overlap, not disjoint).
# ---------------------------------------------------------------------------


def test_connect_only_when_temporal_words_inside_connect_span_1755():
    """'connect my calendar' — the temporal `\\bmy calendar\\b` pattern
    matches entirely INSIDE the connect match's span ('connect my
    calendar'). This is the original #1471 phantom shape: connect-only,
    exactly as before this fix."""
    result = PreClassifier.detect_multiple_intents("connect my calendar")
    assert _resolved(result) == [(IntentCategory.GUIDANCE, "get_contextual_guidance")]
    assert result.intents[0].context.get("setup_target") == "calendar"
    assert not result.is_multi_intent


def test_connect_only_when_temporal_words_inside_connect_span_with_greeting_1755():
    """Same containment shape, paired with a greeting — TEMPORAL must not
    reappear beside GUIDANCE (the #1471 parity pin's exact shape,
    reconfirmed under the new span-aware rule)."""
    result = PreClassifier.detect_multiple_intents("hi piper, connect my calendar")
    categories = {i.category for i in result.intents}
    assert IntentCategory.TEMPORAL not in categories
    assert IntentCategory.GUIDANCE in categories
    assert IntentCategory.CONVERSATION in categories


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
    result = PreClassifier.detect_multiple_intents("connect my slack and check my schedule")
    assert _resolved(result) == [
        (IntentCategory.GUIDANCE, "get_contextual_guidance"),
    ]


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
    from services.intent_service.classifier import IntentClassifier

    result = await IntentClassifier().classify_multiple("what time is it? also connect my github")
    assert _resolved(result) == [
        (IntentCategory.GUIDANCE, "get_contextual_guidance"),
    ]
