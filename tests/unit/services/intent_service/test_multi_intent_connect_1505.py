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
"""

import pytest

from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory


def _resolved(result):
    return [(i.category, i.action) for i in result.intents]


# ---------------------------------------------------------------------------
# The defect: greeting + connect keeps BOTH parts, for every integration —
# not just the calendar special case. RED before the #1505 fix.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "message,target",
    [
        ("hi piper, connect my github", "github"),  # issue verbatim
        ("hi piper, connect my slack", "slack"),
        ("hi piper, connect my notion", "notion"),
        # calendar phrasing that dodges TEMPORAL's `\bmy calendar\b`, so the
        # #1471 substitution never covered it — dropped until #1505
        ("hey, link my google calendar", "google calendar"),
    ],
)
def test_greeting_plus_connect_keeps_both_parts_1505(message, target):
    result = PreClassifier.detect_multiple_intents(message)
    assert _resolved(result) == [
        (IntentCategory.CONVERSATION, "greeting"),
        (IntentCategory.GUIDANCE, "get_contextual_guidance"),
    ], f"{message!r} resolved {_resolved(result)} — connect ask dropped (#1505)"
    connect = result.intents[1]
    assert connect.context.get("setup_target") == target
    assert connect.original_message == message  # #1460 field discipline
    assert result.is_multi_intent
    assert result.has_greeting
    # primary_intent must be the substantive part, so the greeting+substantive
    # lane in process_intent dispatches the guidance handler
    assert result.primary_intent is connect


def test_pattern_lists_name_the_connect_claim_1505():
    """Pre-claim shadow probe threading: the connect intent's claiming list is
    reported by name, aligned post-subsumption (the 2026-09-02 probe contract)."""
    result = PreClassifier.detect_multiple_intents("hi piper, connect my github")
    assert len(result.pattern_lists) == len(result.intents)
    by_action = dict(zip([i.action for i in result.intents], result.pattern_lists))
    assert by_action["get_contextual_guidance"] == "INTEGRATION_CONNECT_PATTERNS"


# ---------------------------------------------------------------------------
# #1471 parity: the calendar collision family behaves byte-for-byte as the
# substitution era did. GREEN before and after — these guard the retirement.
# ---------------------------------------------------------------------------


def test_calendar_pairing_parity_1471():
    result = PreClassifier.detect_multiple_intents("hi piper, connect my calendar")
    categories = {i.category for i in result.intents}
    assert IntentCategory.TEMPORAL not in categories
    assert IntentCategory.GUIDANCE in categories
    assert IntentCategory.CONVERSATION in categories


def test_single_calendar_connect_parity_1471():
    result = PreClassifier.detect_multiple_intents("connect my calendar")
    assert _resolved(result) == [(IntentCategory.GUIDANCE, "get_contextual_guidance")]
    assert result.intents[0].context.get("setup_target") == "calendar"


def test_guidance_dedupe_survives_retirement_1471():
    """'help me set up my calendar' matches the #487 GUIDANCE patterns AND the
    connect group — exactly one guidance intent comes out (the 1471 dedupe)."""
    result = PreClassifier.detect_multiple_intents("help me set up my calendar")
    guidance = [
        i
        for i in result.intents
        if i.category == IntentCategory.GUIDANCE and i.action == "get_contextual_guidance"
    ]
    assert len(guidance) == 1


# ---------------------------------------------------------------------------
# The single-ask shape now claims on the multi path too (same destination the
# single path has resolved to since #1417 — one fewer fall-through hop).
# ---------------------------------------------------------------------------


def test_single_connect_ask_claims_on_multi_path_1505():
    result = PreClassifier.detect_multiple_intents("connect my github")
    assert _resolved(result) == [(IntentCategory.GUIDANCE, "get_contextual_guidance")]
    assert result.intents[0].context.get("setup_target") == "github"
    assert not result.is_multi_intent
    # the single path resolves identically (pre-existing #1417 behavior)
    single = PreClassifier.pre_classify("connect my github")
    assert single is not None
    assert (single.category, single.action) == _resolved(result)[0]
    assert single.context.get("setup_target") == "github"


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
    result = PreClassifier.detect_multiple_intents("hi piper, what time is it")
    assert (IntentCategory.CONVERSATION, "greeting") in _resolved(result)
    assert (IntentCategory.TEMPORAL, "get_current_time") in _resolved(result)


# ---------------------------------------------------------------------------
# E2E through the real classifier entry: classify_multiple returns both parts
# (this is the dominant chat entry — the drop was invisible to the LLM lane
# because any non-empty detection result returns immediately).
# ---------------------------------------------------------------------------


async def test_classify_multiple_returns_both_parts_1505():
    from services.intent_service.classifier import IntentClassifier

    result = await IntentClassifier().classify_multiple("hi piper, connect my github")
    assert _resolved(result) == [
        (IntentCategory.CONVERSATION, "greeting"),
        (IntentCategory.GUIDANCE, "get_contextual_guidance"),
    ]
    assert result.primary_intent.context.get("setup_target") == "github"
