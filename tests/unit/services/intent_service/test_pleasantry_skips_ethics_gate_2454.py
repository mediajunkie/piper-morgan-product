"""#2454: what may skip the ethics check, and what may not.

The rule (Arch and CXO, 2026-11-26): the detector is skipped only for a message that is
ONLY a greeting, farewell or thanks plus fixed filler: one that code fully understands
and that carries no content. Everything else is read, including a pleasantry with a
request after it. The detector is a model call on the person's own key, so before this a
bare "hi" cost one.

One predicate decides it, ``PreClassifier.is_pleasantry_only_message``, which cleans
the message exactly as the canned pleasantry path does and calls the predicate that path
uses. The last tests here are the guard on that predicate's lists: adding to them
changes what skips the ethics check, so they fail until Arch and CXO have read the
change.

# principal-blind-by-design: the skip is decided from the message text alone, before any
# principal is consulted, the same as the gate it guards (see test_ethics_denial_flow).
"""

import re
from unittest.mock import AsyncMock, patch

import pytest

from services.ethics.boundary_enforcer_refactored import BoundaryDecision
from services.intent_service.conversational_floor import FloorResponse
from services.intent_service.pre_classifier import PreClassifier
from tests.ethics.probe_set.probe_definitions import ALL_PROBES
from tests.unit.services.intent_service.test_ethics_denial_flow import _make_service

_PROBE_TEXT = {p.probe_id: p.input for p in ALL_PROBES}

# Every form here is a whole message. Drawn from each list the predicate strips.
PLEASANTRIES = [
    "hi",
    "Hi!",
    "hello",
    "hello there",
    "hey",
    "Hey Piper 👋",
    "good morning",
    "Good morning, team!",
    "howdy",
    "greetings",
    "hi, how are you?",
    "hey, how's it going",
    "what's up",
    "nice to meet you",
    "thanks",
    "Thanks!",
    "thank you",
    "thank you so much",
    "thanks a lot",
    "thanks again",
    "thx",
    "ty",
    "much appreciated",
    "bye",
    "goodbye",
    "see you later",
    "farewell",
    "bye everyone",
]

# A pleasantry with anything after it is not a pleasantry.
NOT_PLEASANTRIES = [
    "hi, can you help me with something",
    "thanks, now delete the staging database",
    "hello, what's open in our private repo?",
    "bye for now, but first summarize the notes",
    "thanks for nothing",
    "hi Martin",
    "good morning, draft the release notes",
    "archive project Apollo in my portfolio",
    "show me my repos",
    "why did you suggest that",
]


def _violating() -> BoundaryDecision:
    return BoundaryDecision(
        violation_detected=True,
        boundary_type="harassment",
        explanation="audit-only",
        audit_data={"decision_id": "bd_test_2454"},
        session_id="test_session_2454",
        redirect_context="redirect toward the work",
    )


async def _one_turn(message: str, *, environ: dict):
    """Drive the entry point with the enforcer mocked to DECLINE whatever it is shown.
    Returns (enforcer_mock, result_or_None)."""
    service = _make_service()
    enforcer_mock = AsyncMock(return_value=_violating())
    floor_mock = AsyncMock(return_value=FloorResponse(message="Not that one.", floor_hit=True))
    result = None
    with (
        patch.dict("os.environ", environ),
        patch(
            "services.intent.intent_service.boundary_enforcer_refactored.enforce_boundaries",
            new=enforcer_mock,
        ),
        patch(
            "services.intent_service.conversational_floor.ConversationalFloor.respond",
            new=floor_mock,
        ),
        patch.object(
            service, "_check_active_guided_process", new=AsyncMock(return_value=(None, None, None))
        ),
        patch.object(service, "_check_pending_resume_offer", new=AsyncMock(return_value=None)),
    ):
        try:
            result = await service._process_intent_internal(
                message=message, session_id="test_session_2454", user_id=None
            )
        except Exception:
            # Past the gate the stubbed service has nothing to classify with. The
            # gate's decision is already recorded on the mock by then.
            pass
    return enforcer_mock, result


@pytest.mark.parametrize("message", PLEASANTRIES)
def test_each_form_is_a_pleasantry(message):
    assert PreClassifier.is_pleasantry_only_message(message) is True


@pytest.mark.parametrize("message", NOT_PLEASANTRIES)
def test_a_message_with_anything_else_in_it_is_not(message):
    assert PreClassifier.is_pleasantry_only_message(message) is False


@pytest.mark.asyncio
@pytest.mark.parametrize("message", PLEASANTRIES)
async def test_a_bare_pleasantry_makes_no_detector_call(message):
    """Even with the enforcer set to decline everything, it is never asked."""
    enforcer_mock, result = await _one_turn(message, environ={"ENABLE_ETHICS_ENFORCEMENT": "true"})
    enforcer_mock.assert_not_called()
    assert not (result is not None and (result.intent_data or {}).get("ethics_triggered"))


@pytest.mark.asyncio
@pytest.mark.parametrize("message", NOT_PLEASANTRIES)
async def test_anything_else_reaches_the_detector(message):
    enforcer_mock, _ = await _one_turn(message, environ={"ENABLE_ETHICS_ENFORCEMENT": "true"})
    enforcer_mock.assert_called_once()
    assert enforcer_mock.call_args.kwargs["message"] == message


@pytest.mark.asyncio
@pytest.mark.parametrize("opener", ["thanks", "hi", "Thanks!", "hello there,", "bye, but first:"])
@pytest.mark.parametrize("probe_id", ["h-3", "per-1"])
async def test_a_block_band_request_cannot_ride_a_pleasantry_past_the_detector(opener, probe_id):
    """CXO's pinned negative: a pleasantry followed by a block-band probe's text is
    shown to the detector whole, and its decline stands."""
    message = f"{opener} {_PROBE_TEXT[probe_id]}"
    enforcer_mock, result = await _one_turn(message, environ={"ENABLE_ETHICS_ENFORCEMENT": "true"})
    enforcer_mock.assert_called_once()
    assert enforcer_mock.call_args.kwargs["message"] == message
    assert result is not None
    assert result.intent_data["ethics_triggered"] is True
    assert result.message == "Not that one."


@pytest.mark.asyncio
async def test_the_off_switch_still_skips_everything():
    enforcer_mock, _ = await _one_turn(
        f"hi {_PROBE_TEXT['h-3']}", environ={"ENABLE_ETHICS_ENFORCEMENT": "false"}
    )
    enforcer_mock.assert_not_called()


def test_the_skip_and_the_canned_path_clean_the_message_the_same_way():
    """One cleaning function, used by the pre-classifier's three entry points and by
    the skip, so the two cannot disagree about what the message is."""
    import inspect

    source = inspect.getsource(PreClassifier)
    assert source.count("PreClassifier._clean_for_matching(message)") == 4
    assert source.count("string.punctuation") == 1  # only inside the helper


# --- the guard on what may skip the ethics check ------------------------------------

# Regex syntax a FIXED phrase may use: word boundaries, whitespace runs, an optional
# apostrophe or "s", optional groups and alternations of literal words.
_ALLOWED = re.compile(r"\\b|\\s\+|'\?|s\?|[()|?]|[a-z ]")

_STRIPPED_LISTS = (
    "GREETING_PATTERNS",
    "FAREWELL_PATTERNS",
    "THANKS_PATTERNS",
    "_PLEASANTRY_FILLER_PATTERNS",
)


@pytest.mark.parametrize("list_name", _STRIPPED_LISTS)
def test_every_stripped_pattern_is_a_fixed_phrase(list_name):
    """No wildcard, no character class, no open quantifier: each pattern can only
    remove the words written in it. A catch-all here would let content skip the check."""
    for pattern in getattr(PreClassifier, list_name):
        leftover = _ALLOWED.sub("", pattern)
        assert leftover == "", (
            f"{list_name}: {pattern!r} is not a fixed phrase (unexpected {leftover!r}). "
            "These lists decide what skips the ethics check (#2454)."
        )
        assert pattern.startswith(r"\b") and pattern.endswith(r"\b"), pattern


def test_the_stripped_lists_are_the_ones_arch_and_cxo_read():
    """The exact contents on 2026-11-26. Any addition, removal or edit fails here: it
    changes what skips the ethics check, so Arch and CXO read it, then this is updated
    in the same commit."""
    import hashlib

    blob = "\n".join(
        f"{name}:{pattern}" for name in _STRIPPED_LISTS for pattern in getattr(PreClassifier, name)
    )
    assert sum(len(getattr(PreClassifier, name)) for name in _STRIPPED_LISTS) == 29
    assert (
        hashlib.sha256(blob.encode("utf-8")).hexdigest()
        == "1adc461b8d4ee73f7486db184e9aa24fae9f7f56321773aa0fdf0794e4de1e34"
    ), "the pleasantry lists changed; see this test's docstring"
