"""#2070: the consent line names the project the portfolio write targets.

#2304 reworded it (CXO 11-06): the check asks the entry's own question
('Archive the project "Bar"? (yes/no)', the existing confirm wording), and a turn
whose args name no project, or an entry with no words, gets CXO's "not sure"
statement with nothing armed. Was: "...asking me to archive project Bar, ..." /
"...asking me to archive project, ..." / "...asking me to list repos, ...".
"""

import pytest

from services.domain.models import Intent
from services.intent_service import consent_gate as cg
from services.intent_service.workflow_dispatcher import get_action_workflows
from services.intent_service.workflow_entries import register_default_workflows
from services.intent_service.write_confirm_words import (
    NOT_SURE_STATEMENT,
    WriteAskRequest,
    resolve_write_ask,
)
from services.shared_types import IntentCategory


def _intent(action, message):
    return Intent(
        category=IntentCategory.EXECUTION,
        action=action,
        confidence=0.9,
        original_message=message,
        context={"original_message": message},
    )


async def _ask(action, message):
    register_default_workflows()
    entry = get_action_workflows()[action]
    return await resolve_write_ask(
        entry, WriteAskRequest(intent=_intent(action, message), message=message)
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "action,message,expected",
    [
        ("archive_project", "I would like to archive project Bar", 'Archive the project "Bar"?'),
        ("archive_project", "archive project Bar", 'Archive the project "Bar"?'),
        ("restore_project", "I would like to restore project Bar", 'Restore the project "Bar"?'),
    ],
)
async def test_consent_line_names_the_project(action, message, expected):
    ask = await _ask(action, message)
    offer = cg.build_consent_check_offer(_intent(action, message), ask.words)
    assert offer.question.startswith(f"{expected} (yes/no)")
    assert '"Bar"' in offer.offer["decline_message"]


@pytest.mark.asyncio
async def test_no_name_says_not_sure_and_arms_nothing():
    ask = await _ask("archive_project", "archive")
    assert ask.words is None
    assert ask.reply == NOT_SURE_STATEMENT
    assert ask.armed is False


@pytest.mark.asyncio
async def test_an_entry_with_no_words_says_not_sure():
    # list_repos is READ (never asked); stands in for any entry without write_ask.
    ask = await _ask("list_repos", "list repos")
    assert ask.reply == NOT_SURE_STATEMENT
