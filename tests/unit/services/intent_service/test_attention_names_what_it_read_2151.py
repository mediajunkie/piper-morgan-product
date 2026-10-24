"""#2151 CAL-SWALLOW (attention_query): the focus reply names only the sources it read.

Before: the #1985 line "Nothing from your flagged todos, upcoming meetings or stale
projects either." rendered even when the calendar wasn't connected or its read failed
(only the todo reads were tracked). CXO's words (10-23 19:12): name only what was read,
add the not-connected line (the same wording as the calendar handlers) or the partial
couldn't-check line, and keep the original #1985 line unchanged on the success path.

LAYER: unit, the real handler with the session and calendar router patched (the #1985b
harness). DENOMINATOR: calendar read OK / not connected / failed.
"""

import pytest

from tests.unit.services.intent_service.test_contextual_query_handlers import (
    TestAttentionReplyShape1985b as _Shape,
)

_SUCCESS = "Nothing from your flagged todos, upcoming meetings or stale projects either."


@pytest.mark.asyncio
async def test_the_success_path_keeps_the_1985_line(intent_service):
    result = await _Shape()._run(intent_service, [], [], calendar="empty")
    assert _SUCCESS in result.message


@pytest.mark.asyncio
async def test_calendar_not_connected_names_only_what_was_read_and_offers_the_connection(
    intent_service,
):
    result = await _Shape()._run(intent_service, [], [], calendar="not_connected")
    assert _SUCCESS not in result.message
    assert "Nothing from your flagged todos or stale projects either." in result.message
    assert (
        "Google Calendar isn't connected yet, so meetings aren't included. "
        'Ask me "how do I connect Google Calendar?" and I\'ll walk you through it.'
    ) in result.message


@pytest.mark.asyncio
async def test_a_failed_calendar_read_says_it_couldnt_check(intent_service):
    result = await _Shape()._run(intent_service, [], [], calendar="failed")
    assert _SUCCESS not in result.message
    assert "Nothing from your flagged todos or stale projects either." in result.message
    assert (
        "I couldn't check your calendar just now, so the list above doesn't include your "
        "meetings. Try again in a moment; if it keeps failing, tell us."
    ) in result.message


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "calendar,sentence",
    [
        (
            "not_connected",
            "Google Calendar isn't connected yet, so meetings aren't included. "
            'Ask me "how do I connect Google Calendar?" and I\'ll walk you through it.',
        ),
        (
            "failed",
            "I couldn't check your calendar just now, so the list above doesn't include your "
            "meetings. Try again in a moment; if it keeps failing, tell us.",
        ),
    ],
)
async def test_the_source_sentence_is_its_own_last_paragraph(intent_service, calendar, sentence):
    """CXO 10-24 09:47: Web read the DOM on 716cb6dc6c and the calendar sentence ran on
    inside the last block's paragraph. It stands alone, last, after a blank line."""
    result = await _Shape()._run(intent_service, [], [], calendar=calendar)
    paragraphs = result.message.split("\n\n")
    assert paragraphs[-1] == sentence
    assert sentence not in paragraphs[0]
