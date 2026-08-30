"""
#1460: original_message instance fix — dual-surface regression tests.

Instance fix split from #1459 (class issue, Production). Two live paths
(trace on #1459's first comment, 2026-07-30):

1. Setup/onboarding mis-route: ``detect_multiple_intents`` built Intents with
   only ``context["original_message"]`` set (attribute ``""``), returning
   BEFORE the ``classify()``-entry backfill. ``_detect_setup_request`` read
   the attribute only → setup requests silently skipped the #814 interactive
   setup flow (#1417's mis-route resurfaced on the dominant chat path).
2. Dead TEMPORAL gates on multi-intent turns: the orchestrator's
   ``_execute_single`` calls CanonicalHandlers directly (no gate, no
   backfill); all four temporal detectors read the attribute only.

Writer-side cure: ``detect_multiple_intents`` now populates the attribute at
Intent construction. Reader-side belt-and-suspenders: the 6 attribute-only
detector sites use idiom B (``attr or (context or {}).get(...)``). Plus the
2 half-safe Slack sites that fell back to a key nothing ever writes
(``context.get("message")``) now fall back to ``original_message``.

D4 discipline: wiring only — no classifier prompt or pattern changes.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.domain.models import Intent
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory

SETUP_MESSAGE = "help me setup my projects"
MULTI_INTENT_MESSAGE = "What's my schedule today and show my todos"


@pytest.fixture
def handlers():
    return CanonicalHandlers()


def _dict_only_intent(category: IntentCategory, action: str, message: str) -> Intent:
    """Reproduce the pre-fix detect_multiple_intents shape: dict set, attribute ''."""
    return Intent(
        category=category,
        action=action,
        confidence=1.0,
        context={"original_message": message, "multi_intent_detection": True},
    )


# ---------------------------------------------------------------------------
# Writer-side cure: detect_multiple_intents populates BOTH surfaces
# ---------------------------------------------------------------------------


class TestDetectMultipleIntentsWritesBothSurfaces:
    @pytest.mark.parametrize(
        "message",
        [
            SETUP_MESSAGE,
            MULTI_INTENT_MESSAGE,
            "Hi Piper! What's on my agenda?",
        ],
    )
    def test_attribute_populated_at_construction(self, message):
        result = PreClassifier.detect_multiple_intents(message)
        assert result.intents, f"expected at least one pre-classified intent for {message!r}"
        for intent in result.intents:
            # Attribute surface (the one the detectors read)
            assert intent.original_message == message, (
                f"{intent.category}/{intent.action}: original_message attribute not "
                f"populated at construction (got {intent.original_message!r}) — "
                "the detect_multiple path bypasses the classify()-entry backfill, "
                "so the attribute must be set at the writer (#1460)"
            )
            # Dict surface (unchanged — existing readers keep working)
            assert intent.context.get("original_message") == message
            assert intent.context.get("multi_intent_detection") is True


# ---------------------------------------------------------------------------
# Reader-side belt-and-suspenders: the 6 detector sites are two-surface-safe
# (a dict-only Intent — any OTHER unbackfilled writer — still gates correctly)
# ---------------------------------------------------------------------------


class TestDetectorsReadBothSurfaces:
    def test_setup_request_detected_from_dict_only_intent(self, handlers):
        intent = _dict_only_intent(
            IntentCategory.GUIDANCE, "get_contextual_guidance", SETUP_MESSAGE
        )
        assert intent.original_message == ""  # precondition: attribute empty
        assert handlers._detect_setup_request(intent) == "projects"

    def test_agenda_request_detected_from_dict_only_intent(self, handlers):
        intent = _dict_only_intent(
            IntentCategory.TEMPORAL, "get_current_time", MULTI_INTENT_MESSAGE
        )
        assert handlers._detect_agenda_request(intent) is True

    def test_retrospective_request_detected_from_dict_only_intent(self, handlers):
        intent = _dict_only_intent(
            IntentCategory.TEMPORAL, "get_current_time", "What did we accomplish yesterday?"
        )
        assert handlers._detect_retrospective_request(intent) is True

    def test_last_activity_request_detected_from_dict_only_intent(self, handlers):
        intent = _dict_only_intent(
            IntentCategory.TEMPORAL,
            "get_current_time",
            "When was the last time we worked on piper?",
        )
        assert handlers._detect_last_activity_request(intent) == "piper"

    def test_duration_request_detected_from_dict_only_intent(self, handlers):
        intent = _dict_only_intent(
            IntentCategory.TEMPORAL,
            "get_current_time",
            "How long have we been working on piper?",
        )
        assert handlers._detect_duration_request(intent) == "piper"

    def test_priority_recommendation_detected_from_dict_only_intent(self, handlers):
        # 6th site per the #1460 audit: no additional LIVE attribute-only reader
        # exists beyond the 5 named in the #1459 trace; this is the nearest-risk
        # one (PRIORITY is a category detect_multiple_intents emits; today its
        # only callers set the attribute, but it is one wiring change from live).
        intent = _dict_only_intent(
            IntentCategory.PRIORITY, "get_top_priority", "Which project should I focus on?"
        )
        assert handlers._detect_priority_recommendation_request(intent) is True

    def test_detectors_still_negative_on_unrelated_message(self, handlers):
        # Idiom B must not change gating for messages that shouldn't match.
        intent = _dict_only_intent(IntentCategory.TEMPORAL, "get_current_time", "What day is it?")
        assert handlers._detect_agenda_request(intent) is False
        assert handlers._detect_retrospective_request(intent) is False
        assert handlers._detect_last_activity_request(intent) is None
        assert handlers._detect_duration_request(intent) is None
        assert handlers._detect_setup_request(intent) is None
        assert handlers._detect_priority_recommendation_request(intent) is False

    def test_detectors_safe_on_empty_intent(self, handlers):
        # Guard behavior preserved: no message on either surface → no match.
        intent = Intent(category=IntentCategory.TEMPORAL, action="get_current_time", context={})
        assert handlers._detect_agenda_request(intent) is False
        assert handlers._detect_setup_request(intent) is None
        assert handlers._detect_priority_recommendation_request(intent) is False

    def test_attribute_surface_still_wins_when_present(self, handlers):
        # Attribute takes precedence over dict (idiom B ordering).
        intent = Intent(
            category=IntentCategory.TEMPORAL,
            action="get_current_time",
            confidence=1.0,
            original_message="What's my schedule today?",
            context={"original_message": "What day is it?"},
        )
        assert handlers._detect_agenda_request(intent) is True


# ---------------------------------------------------------------------------
# Slack half-safe sites: fallback key corrected (context["message"] was never
# written by anything — the fallback was dead)
# ---------------------------------------------------------------------------


def _execution_intent_dict_only(message: str) -> Intent:
    return Intent(
        category=IntentCategory.EXECUTION,
        action="create_issue",
        confidence=1.0,
        context={"original_message": message},
    )


@pytest.mark.asyncio
async def test_slack_response_handler_dispatches_from_dict_only_intent():
    from services.integrations.slack.response_handler import SlackResponseHandler

    mock_intent_service = MagicMock()
    mock_result = MagicMock()
    mock_result.success = True
    mock_result.message = "done"
    mock_intent_service.process_intent = AsyncMock(return_value=mock_result)

    handler = SlackResponseHandler(
        spatial_adapter=MagicMock(),
        intent_classifier=MagicMock(),
        slack_client=MagicMock(),
        intent_service=mock_intent_service,
    )

    intent = _execution_intent_dict_only("create an issue about flaky tests")
    slack_context = {"user_id": "U123", "channel_id": "C123"}

    result = await handler._process_through_orchestration(intent, slack_context)

    assert result is not None, (
        "dispatch bailed with 'No message available' — the fallback read "
        "context['message'], a key nothing ever writes (#1460)"
    )
    mock_intent_service.process_intent.assert_awaited_once()
    assert (
        mock_intent_service.process_intent.await_args.kwargs["message"]
        == "create an issue about flaky tests"
    )


# NOTE (2026-08-30, census disposal Batch 3): the SimpleSlackResponseHandler
# twin of the test above was excised here with
# services/integrations/slack/simple_response_handler.py (zero production
# callers; the LIVE 1460 surface is response_handler, covered above).
