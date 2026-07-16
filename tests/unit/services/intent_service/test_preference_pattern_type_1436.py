"""#1436 B9: preference confirmations must reach the learning loop.

Regression: ``_log_preference_to_learning`` built its pattern with
``PatternType.PREFERENCE`` — a member that does not exist on
``services.learning.query_learning_loop.PatternType`` (that enum has
``USER_PREFERENCE_PATTERN``; the same-named enum in ``services.shared_types``
DOES have ``PREFERENCE``, which is how the bug read as plausible). The
AttributeError was swallowed by the classify hook's broad except
(``classifier.py:317``), so every confirmed preference was silently dropped —
part of the census F13 "Piper permanently stops learning" cluster.

This pins the whole call actually executing and carrying the real enum member.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock

from services.intent_service.preference_handler import PreferenceDetectionHandler
from services.learning.query_learning_loop import PatternType


def _confirmation():
    return SimpleNamespace(
        id="conf-1",
        user_id="user-abc",
        dimension=SimpleNamespace(value="verbosity"),
        new_value="concise",
        previous_value="detailed",
        hint_id="hint-1",
        confirmation_source="chat",
    )


async def test_confirmed_preference_reaches_learning_loop_with_real_enum_member():
    handler = PreferenceDetectionHandler.__new__(PreferenceDetectionHandler)  # method under test is self-contained
    handler.learning_loop = SimpleNamespace(
        _apply_user_preference_pattern=AsyncMock(return_value={"success": True})
    )

    ok = await handler._log_preference_to_learning(_confirmation())

    assert ok is True
    handler.learning_loop._apply_user_preference_pattern.assert_awaited_once()
    pattern = handler.learning_loop._apply_user_preference_pattern.await_args.kwargs["pattern"]
    # The old code raised AttributeError constructing this (PatternType.PREFERENCE
    # doesn't exist) — the await above never happened at all.
    assert pattern.pattern_type is PatternType.USER_PREFERENCE_PATTERN
