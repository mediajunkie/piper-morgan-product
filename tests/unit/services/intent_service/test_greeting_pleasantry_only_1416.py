"""#1416: the canned pleasantry short-circuits only claim pleasantry-ONLY messages.

The bug (PM, Scenario A turn 1): "Hi, I just got access to this and am excited
to try it. How do I address you?" matched ``\\bhi\\b``, the greeting
short-circuit fired at confidence 1.0, and the canned "Hello!" swallowed the
actual question. Farewell and thanks had the identical over-claim shape.

The contract pinned here (B3-N2/#1417's conservative over-resolution
discipline): a deterministic fast-path may only claim what it fully
understands. Pleasantry + substantive residue -> fall through to full
classification, where the floor greets AND answers.
"""

import pytest

from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory


def _classify(msg: str):
    return PreClassifier.pre_classify(msg)


# ---------------------------------------------------------------------------
# Pure pleasantries: canned fast-path unchanged (cheap, deterministic)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "message,action",
    [
        ("hi", "greeting"),
        ("Hi!", "greeting"),
        ("hey there", "greeting"),
        ("good morning", "greeting"),
        ("hello piper", "greeting"),
        ("hi, how are you?", "greeting"),
        ("hey, what's up?", "greeting"),
        ("bye", "farewell"),
        ("goodbye, thanks again!", "farewell"),
        ("thanks!", "thanks"),
        ("thank you so much", "thanks"),
    ],
)
def test_pure_pleasantries_stay_canned(message, action):
    intent = _classify(message)
    assert intent is not None, f"pleasantry no longer claimed: {message!r}"
    assert intent.category == IntentCategory.CONVERSATION
    assert intent.action == action


# ---------------------------------------------------------------------------
# Pleasantry + substance: NEVER swallowed by the canned path
# ---------------------------------------------------------------------------

THE_INCIDENT = "Hi, I just got access to this and am excited to try it. How do I address you?"


@pytest.mark.parametrize(
    "message",
    [
        THE_INCIDENT,
        "hi, can you show me my open issues?",
        "hello — what should I focus on today?",
        "thanks! now add a todo to review the PR",
        "bye, but first close issue 42",
        "good morning, what's on my agenda?",
    ],
)
def test_pleasantry_plus_substance_is_not_swallowed(message):
    intent = _classify(message)
    if intent is not None:
        assert not (
            intent.category == IntentCategory.CONVERSATION
            and intent.action in ("greeting", "farewell", "thanks")
        ), f"canned pleasantry swallowed a substantive message: {message!r} -> {intent.action}"


def test_the_incident_message_falls_through_to_full_classification():
    """The exact Scenario-A turn-1 message: no other deterministic pattern
    claims it, so it reaches the LLM classifier (which routes the whole
    message — greeting AND question — to the floor)."""
    assert _classify(THE_INCIDENT) is None


# ---------------------------------------------------------------------------
# Substance detection isn't fooled by filler
# ---------------------------------------------------------------------------


def test_agenda_phrasing_still_reaches_agenda_not_greeting():
    intent = _classify("good morning, what's on the agenda for today?")
    assert intent is not None
    assert intent.action != "greeting"


# ---------------------------------------------------------------------------
# The second layer: even when the LLM classifier labels a compound message
# "greeting", the canonical gate must send it to the floor (greet AND answer),
# reserving the canned/consciousness greeting for pure pleasantries.
# ---------------------------------------------------------------------------


def _gate(message: str) -> bool:
    from services.domain.models import Intent
    from services.intent.intent_service import IntentService
    from services.shared_types import IntentCategory as IC

    svc = IntentService.__new__(IntentService)  # branch under test reads no self state
    intent = Intent(
        category=IC.CONVERSATION,
        action="greeting",
        confidence=0.9,
        original_message=message,
        context={"original_message": message},
    )
    return svc._requires_canonical_handler(intent)


def test_gate_pure_greeting_stays_canonical():
    assert _gate("hi there!") is True


def test_gate_compound_greeting_goes_to_floor():
    assert _gate(THE_INCIDENT) is False


def test_gate_greeting_with_task_goes_to_floor():
    assert _gate("hey, can you list my open PRs?") is False
