"""Issue 2461 (CXO, 2026-11-27): the create-issue subject question says how to get a
todo, always.

Served on beta ``f4dff30500`` (seat-github-1, GitHub connected): "add a task to the
Launch project: book the venue" reached the create-issue route and was answered with
"What should the issue be about? ... and I'll create it." The reply never said "todo".
The never-connected reply to the same sentence already ended "If you meant a todo, say
"add a todo: …" and I'll add it." The two now agree.

The sentence is said whenever the question is asked; nothing reads the person's words
to decide it, and it does not change the route (issues 2425 and 2461). The question
stays in the handler, where the unarmed-ask census already lists it.

Layer: unit, through the real handler with no title anywhere in the turn.
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.write_confirm_words import (
    ISSUE_NOT_WORKING_TODO_HINT,
    ISSUE_TODO_HINT,
)
from services.shared_types import IntentCategory

ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"

EXPECTED = (
    "What should the issue be about? Give me a subject — "
    'e.g. "create an issue in owner/repo about flaky login tests" or a quoted title '
    "— and I'll create it. "
    'If you meant a todo, say "add a todo: …" and I\'ll add it.'
)


async def _ask(message: str):
    """The create-issue handler on a CONNECTED account (the 1543 tests' setup), with a
    message that carries no subject the slot-fill can take."""
    intent = Intent(
        original_message=message,
        category=IntentCategory.EXECUTION,
        action="create_issue",
        confidence=0.92,
        context={},
    )
    with (
        patch(f"{ROUTER}.initialize", new=AsyncMock()),
        patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
        patch(f"{ROUTER}.create_issue", new=AsyncMock()) as write,
    ):
        result = await IntentService()._handle_create_issue(intent, "wf-2461", "session-2461")
    write.assert_not_awaited()
    return result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "message",
    [
        # No subject, with a repository named (with none, the handler asks which
        # repository first, and that question is not this one).
        "create an issue in mediajunkie/test-piper-morgan",  # the 1543 no-subject shape
        "open an issue in mediajunkie/test-piper-morgan",
    ],
)
async def test_the_subject_question_ends_with_the_way_out_to_a_todo(message):
    result = await _ask(message)
    assert result.clarification_type == "issue_title_required"
    assert result.message == EXPECTED
    assert result.requires_clarification is True


@pytest.mark.asyncio
async def test_the_served_sentence_does_not_get_a_reply_without_the_word_todo():
    """Beta, 2026-11-27: "add a task to the Launch project: book the venue" on a
    connected account was answered with the subject question and no way out. Whatever
    this handler now says to that sentence, a subject question carries the exit."""
    result = await _ask("add a task to the Launch project: book the venue")
    if result.clarification_type == "issue_title_required":
        assert result.message == EXPECTED


def test_it_is_the_sentence_the_never_connected_reply_ends_with():
    assert EXPECTED.endswith(ISSUE_TODO_HINT)
    assert ISSUE_NOT_WORKING_TODO_HINT.endswith(ISSUE_TODO_HINT)
