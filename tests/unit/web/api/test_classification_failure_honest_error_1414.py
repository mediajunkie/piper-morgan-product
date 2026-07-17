"""#1414: a classification-path LLM failure surfaces the honest key message.

The gap (PM's Scenario-A incident): #1404 wired the humanizer into the
degradation path, but a turn failing at INTENT CLASSIFICATION raises
``IntentClassificationFailedError`` — which stringifies to just
"API Error [INTENT_CLASSIFICATION_FAILED]". That matched no humanizer pattern,
so every LLM-backed turn showed the generic "Something unexpected happened.
Please try again in a moment." while the real cause (a quota-dead key) was
trapped in ``details["original_error"]``.

Pinned here: the degradation extractor unwraps the wrapper and produces the
actionable #1404 messages on the classification path.
"""

from services.api.errors import IntentClassificationFailedError
from web.api.routes.intent import _extract_degradation_message

QUOTA_ERROR = (
    "All configured LLM providers failed. Details: openai: Error code: 429 - "
    "insufficient_quota: You exceeded your current quota"
)


def test_quota_failure_is_actionable_not_generic():
    err = IntentClassificationFailedError(details={"original_error": QUOTA_ERROR})
    msg = _extract_degradation_message(err)
    assert "Something unexpected happened" not in msg
    assert "quota" in msg.lower() or "key" in msg.lower()
    assert "settings" in msg.lower()  # points at the fix surface (#1404 recovery)


def test_invalid_key_failure_is_actionable():
    err = IntentClassificationFailedError(
        details={"original_error": "anthropic: invalid_api_key — authentication failed"}
    )
    msg = _extract_degradation_message(err)
    assert "Something unexpected happened" not in msg
    assert "key" in msg.lower()


def test_wrapper_without_details_still_degrades_gracefully():
    err = IntentClassificationFailedError()
    msg = _extract_degradation_message(err)
    assert isinstance(msg, str) and len(msg) > 10


def test_unwrapped_exceptions_unchanged():
    msg = _extract_degradation_message(Exception("database connection refused"))
    assert "Database service is temporarily unavailable" in msg
