"""#1417 (Arch-ratified 2026-07-16): "connect my github" reaches the guidance lane.

Before: integration-connect utterances were mode-4 category-luck — the LLM
usually emitted EXECUTION + a free-form action, landing on the generic
unwired-write decline ("still on the way") while the OAuth flow, the settings
page, AND a purpose-built chat answer (_format_integration_setup_guidance) all
existed. Now surface 1 routes them deterministically to the EXISTING registry
canonical GUIDANCE/get_contextual_guidance (no new action; pure reachability).

Coverage shape per Arch's ruling: positive rows, the COLLISION guard (repo
slug / "repo" word stays in the #862 repo-link lane), and the REGRESSION row
("help me set up github" unchanged via the older #487 patterns).
"""

import pytest

from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory


def _classify(msg: str):
    return PreClassifier.pre_classify(msg)


# ---------------------------------------------------------------------------
# Positive: natural connect phrasings route deterministically
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "message,target",
    [
        ("can we connect my github?", "github"),
        ("connect my github", "github"),
        ("Connect GitHub", "github"),
        ("connect my slack", "slack"),
        ("set up notion", "notion"),
        ("setup notion for me", "notion"),
        ("hook up google calendar", "google calendar"),
        ("can you integrate slack with this?", "slack"),
        ("link my github account", "github"),
        ("enable the calendar integration", "calendar"),
    ],
)
def test_integration_connect_routes_to_guidance(message, target):
    intent = _classify(message)
    assert intent is not None, f"pre-classifier missed: {message!r}"
    assert intent.category == IntentCategory.GUIDANCE
    assert intent.action == "get_contextual_guidance"
    assert intent.context.get("setup_target") == target


# ---------------------------------------------------------------------------
# Collision guard (the load-bearing one): repo-slug / "repo" stays link_repo
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "message",
    [
        "connect the mediajunkie/piper-morgan-product repo",
        "connect my repo to the project",
        "link mediajunkie/test-piper-morgan",
        "add my github repo to the portfolio",
        "connect repository acme/widgets",
    ],
)
def test_repo_phrasings_never_hijacked(message):
    intent = _classify(message)
    if intent is not None:
        assert not (
            intent.action == "get_contextual_guidance" and intent.context.get("setup_target")
        ), f"repo-lane message hijacked into integration setup: {message!r}"


def test_slug_link_still_reaches_repo_management():
    intent = _classify("link mediajunkie/test-piper-morgan to the project")
    assert intent is not None
    assert intent.action == "manage_repos"


# ---------------------------------------------------------------------------
# Regression: the older #487 setup phrasings are unchanged
# ---------------------------------------------------------------------------


def test_help_me_set_up_github_unchanged():
    intent = _classify("help me set up github")
    assert intent is not None
    assert intent.category == IntentCategory.GUIDANCE
    assert intent.action == "get_contextual_guidance"


# ---------------------------------------------------------------------------
# Negative: no integration noun, no hijack
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "message",
    ["connect the dots for me", "add a todo to buy milk", "can you connect?"],
)
def test_no_integration_noun_no_match(message):
    intent = _classify(message)
    if intent is not None:
        assert intent.context.get("setup_target") is None


# ---------------------------------------------------------------------------
# #1471: temporal-calendar collision — connect verbs OUT-RANK the temporal
# calendar-noun patterns. "connect my calendar" matched `\bmy calendar\b` in
# TEMPORAL_PATTERNS (checked earlier than the #1417 lane) and answered with
# the current time; only pattern-avoiding phrasings ("link my google
# calendar") reached setup guidance. Fixed by precedence (pre_classify) and
# substitution (detect_multiple_intents), sharing _integration_connect_match.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "message,target",
    [
        ("connect my calendar", "calendar"),
        ("can you connect my calendar?", "calendar"),
        ("link my calendar", "calendar"),
        ("set up my calendar", "calendar"),
        ("add my google calendar", "google calendar"),
    ],
)
def test_connect_calendar_beats_temporal_1471(message, target):
    intent = _classify(message)
    assert intent is not None, f"pre-classifier missed: {message!r}"
    assert intent.category == IntentCategory.GUIDANCE, (
        f"{message!r} routed to {intent.category} — the temporal calendar "
        f"pattern is winning over integration-connect again (#1471)"
    )
    assert intent.action == "get_contextual_guidance"
    assert intent.context.get("setup_target") == target


def test_connect_calendar_multi_intent_path_1471():
    """The dominant chat path is classify_multiple → detect_multiple_intents,
    where TEMPORAL_PATTERNS matched before any connect handling existed —
    the #1471 misroute lived here even after pre_classify was fixed."""
    result = PreClassifier.detect_multiple_intents("connect my calendar")
    resolved = [(i.category, i.action) for i in result.intents]
    assert resolved == [
        (IntentCategory.GUIDANCE, "get_contextual_guidance")
    ], f"multi-intent path resolved {resolved} (#1471)"
    intent = result.intents[0]
    assert intent.original_message == "connect my calendar"  # #1460 field
    assert intent.context.get("setup_target") == "calendar"


def test_multi_intent_substitution_keeps_other_parts_1471():
    """Substitution, not suppression: a greeting riding with the connect ask
    survives, and the temporal phantom does not."""
    result = PreClassifier.detect_multiple_intents("hi piper, connect my calendar")
    categories = {i.category for i in result.intents}
    assert IntentCategory.TEMPORAL not in categories
    assert IntentCategory.GUIDANCE in categories


def test_no_duplicate_guidance_when_both_lanes_match_1471():
    """'help me set up my calendar' matches the #487 GUIDANCE patterns AND the
    connect substitution — exactly one guidance intent must come out."""
    result = PreClassifier.detect_multiple_intents("help me set up my calendar")
    guidance = [
        i
        for i in result.intents
        if i.category == IntentCategory.GUIDANCE and i.action == "get_contextual_guidance"
    ]
    assert len(guidance) == 1, f"expected 1 guidance intent, got {len(guidance)}"


@pytest.mark.parametrize(
    "message",
    [
        "show my calendar",
        "what time is it",
        "my appointments",
    ],
)
def test_temporal_queries_unchanged_1471(message):
    intent = _classify(message)
    assert intent is not None
    assert intent.category == IntentCategory.TEMPORAL
    assert intent.action == "get_current_time"


@pytest.mark.parametrize(
    "message",
    [
        "add a meeting to my calendar",
        "add an event to my calendar",
        "set up a meeting on my calendar",
    ],
)
def test_calendar_event_writes_stay_out_of_connect_lane_1471(message):
    """Event-write nouns are blocked from the connect lane (#1471 blocker):
    these keep their pre-#1471 routing instead of flipping to setup guidance."""
    intent = _classify(message)
    if intent is not None:
        assert not (
            intent.action == "get_contextual_guidance" and intent.context.get("setup_target")
        ), f"event-write ask hijacked into integration setup: {message!r}"


# ---------------------------------------------------------------------------
# The handoff bug found via this issue: the classifier's Stage-1 return left
# Intent.original_message EMPTY (only context carried it), so the GUIDANCE
# canonical gate (_detect_setup_request reads the FIELD) never fired for ANY
# pre-classified setup request — they all floored (#1332/#1220 completion).
# ---------------------------------------------------------------------------


async def test_classifier_handoff_populates_original_message_field():
    from services.intent_service.classifier import IntentClassifier

    classifier = IntentClassifier()
    msg = "can we connect my github?"
    intent = await classifier.classify(msg, use_cache=False)
    assert intent.action == "get_contextual_guidance"
    assert intent.original_message == msg  # the FIELD, not just context


async def test_setup_gate_fires_end_to_end_on_the_classified_intent():
    from services.intent_service.canonical_handlers import CanonicalHandlers
    from services.intent_service.classifier import IntentClassifier

    intent = await IntentClassifier().classify("can we connect my github?", use_cache=False)
    assert CanonicalHandlers()._detect_setup_request(intent) == "integrations"
