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
            intent.action == "get_contextual_guidance"
            and intent.context.get("setup_target")
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
