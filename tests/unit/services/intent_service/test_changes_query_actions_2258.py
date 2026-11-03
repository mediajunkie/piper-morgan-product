"""#2258 — the "what changed" Actions block names actions; it never prints an event_type.

Alpha (2026-11-02, #1680's rows): the block grouped audit rows by ``event_type`` and
printed "consequential: 2". CXO's words (18:59): name each action by what it was, from
the row's own message; when no row has a usable message, one plain sentence with the
count ("Piper made 2 changes for you."). Same no-LLM, no-database harness as #2140.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest

from tests.unit.services.intent_service.test_changes_query_fail_closed_2140 import (  # noqa: F401
    _intent,
    _run,
    intent_service,
)

_NEVER = ("consequential", "event_type", "auth")


def _audit(message, minutes_ago=5, event_type="consequential", action="github_create_issue"):
    row = MagicMock()
    row.action = action
    row.event_type = event_type
    row.message = message
    row.created_at = datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)
    return row


def _assert_no_internal_labels(message):
    for word in _NEVER:
        assert word not in message.lower(), f"{word!r} leaked into the reply: {message!r}"


@pytest.mark.asyncio
async def test_two_rows_with_messages_render_two_named_lines(intent_service):
    rows = [
        _audit("Comment on issue #38", 2),
        _audit("Create issue in owner/repo", 9, event_type="auth", action="auth_login"),
    ]
    result, _ = await _run(intent_service, _intent(), rows, [], [])
    assert result.success is True
    assert "**Actions** (2):" in result.message
    assert "  - Comment on issue #38" in result.message
    assert "  - Create issue in owner/repo" in result.message
    assert "more" not in result.message
    _assert_no_internal_labels(result.message)


@pytest.mark.asyncio
@pytest.mark.parametrize("missing", [None, "", "   "])
async def test_rows_without_messages_render_the_plain_count(intent_service, missing):
    rows = [_audit(missing), _audit(missing, event_type="auth", action="auth_login")]
    result, _ = await _run(intent_service, _intent(), rows, [], [])
    assert result.message.endswith("Piper made 2 changes for you.")
    assert "**Actions**" not in result.message
    _assert_no_internal_labels(result.message)


@pytest.mark.asyncio
async def test_one_row_without_message_is_singular(intent_service):
    result, _ = await _run(intent_service, _intent(), [_audit(None)], [], [])
    assert result.message.endswith("Piper made 1 change for you.")
    _assert_no_internal_labels(result.message)


@pytest.mark.asyncio
async def test_mixed_rows_list_the_named_and_count_the_rest(intent_service):
    rows = [_audit("Comment on issue #38", 1), _audit(None, 2), _audit("", 3)]
    result, _ = await _run(intent_service, _intent(), rows, [], [])
    assert "**Actions** (3):" in result.message
    assert "  - Comment on issue #38" in result.message
    assert "  - and 2 more" in result.message
    _assert_no_internal_labels(result.message)


@pytest.mark.asyncio
async def test_more_than_five_named_lists_the_five_most_recent(intent_service):
    rows = [_audit(f"Comment on issue #{n}", n) for n in range(1, 8)]
    result, _ = await _run(intent_service, _intent(), rows, [], [])
    assert "**Actions** (7):" in result.message
    for n in range(1, 6):
        assert f"  - Comment on issue #{n}\n" in result.message + "\n"
    assert "#6" not in result.message and "#7" not in result.message
    assert "  - and 2 more" in result.message
    _assert_no_internal_labels(result.message)


@pytest.mark.asyncio
async def test_failed_read_beside_actions_still_named(intent_service):
    """#2140's fail-closed line stays beside the rows the other reads found."""
    result, _ = await _run(
        intent_service, _intent(), [_audit("Comment on issue #38")], RuntimeError("todo"), []
    )
    assert "  - Comment on issue #38" in result.message
    assert result.message.endswith(
        "I couldn't read your Piper tasks just now, so the list above doesn't include it. "
        "Try again in a moment; if it keeps failing, tell us."
    )
    _assert_no_internal_labels(result.message)
