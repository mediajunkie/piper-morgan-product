"""#2271 (PA's served repro on 0d4938cf23; Arch 11-06 10:49): "link repo owner/name to
<project>" in a fresh session reached the generic "I didn't recognize that" decline,
because the legacy classifier emitted EXECUTION/link_repository, which was no rail key.

The fix is the #1527 alias discipline: ``link_repository`` is a rail alias of the
link_repo entry and inherits every gate. These drive the REAL ``process_intent`` and
classifier chain with only the LLM boundary pinned, and record the handler call rather
than touching the database.
"""

import json

import pytest

from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.unwired_writes import GENERIC_UNWIRED_WRITE_DECLINE
from services.intent_service.workflow_dispatcher import get_action_workflows
from services.intent_service.workflow_entries import register_default_workflows

_USER = "3f7b8a52-2271-4b00-9e00-000000002271"
_PHRASE = "link repo dinp-machine/piper-test-activity to Piper Test Activity"


# The legacy classifier's invented spellings seen on alpha (#2271): 10:49, 11:26, 15:59.
_LINK_ALIASES = ("link_repository", "link_repository_to_project", "link_repo_to_project")


class _PinnedEmissionLLM:
    def __init__(self, action="link_repository"):
        self._action = action

    async def complete(self, task_type=None, **kwargs):
        if task_type != "intent_classification":
            raise AssertionError(f"LLM boundary touched for task_type={task_type!r}")
        return json.dumps(
            {
                "category": "execution",
                "action": self._action,
                "confidence": 0.9,
                "reasoning": "link a repository to a project",
            }
        )


@pytest.mark.parametrize("alias", _LINK_ALIASES)
def test_link_repository_is_the_link_repo_entry(alias):
    register_default_workflows()
    wf = get_action_workflows()
    assert wf[alias] is wf["link_repo"]


@pytest.mark.asyncio
@pytest.mark.parametrize("alias", _LINK_ALIASES)
async def test_the_emission_reaches_the_link_handler_not_the_decline(monkeypatch, alias):
    from services.intent_service.canonical_handlers import CanonicalHandlers

    seen = []

    async def _link(self, intent, session_id, user_id=None):
        seen.append(intent.context.get("original_message"))
        return {
            "message": "Linked dinp-machine/piper-test-activity to Piper Test Activity.",
            "intent": {"category": "portfolio", "action": "link_repo", "confidence": 1.0},
            "requires_clarification": False,
        }

    monkeypatch.setattr(CanonicalHandlers, "_handle_link_repo", _link)
    register_default_workflows()
    service = IntentService(
        intent_classifier=IntentClassifier(llm_service=_PinnedEmissionLLM(alias))
    )
    result = await service.process_intent(
        message=_PHRASE, session_id=f"e2e-2271-{alias}", user_id=_USER
    )
    assert seen == [_PHRASE]
    assert result.message != GENERIC_UNWIRED_WRITE_DECLINE
    assert "didn't recognize" not in result.message
