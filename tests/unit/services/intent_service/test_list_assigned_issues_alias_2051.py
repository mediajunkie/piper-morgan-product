"""#2051: ``list_assigned_issues`` is an alias of the list-issues read.

Web's served run of 6bb955919d (2026-10-16 08:10, 0 issues assigned):
``what issues are assigned to me?`` → the classifier's own action name
``list_assigned_issues`` had no rail key, the turn fell to the floor, and
the reply was "Let me pull that up…" with nothing pulled.

Fix (Lead's read on the issue): register ``list_assigned_issues`` as an
ALIAS on the ``list_issues`` / ``list_issues_query`` entry. The read runs:
0 assigned → the #2040 scope line; some → the capped list.

Layer: the REAL rail dispatcher (``dispatch_workflow``) with the action name
``list_assigned_issues`` → the REAL ``_handle_list_issues_query``, the
GitHub adapter stubbed at its method and the default-repo store stubbed.
Not a served run.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.inversion_router import (
    build_routing_prompt,
    derive_routing_grammar,
)
from services.intent_service.workflow_dispatcher import (
    dispatch_workflow,
    get_action_workflows,
    wired_chat_actions,
)
from services.intent_service.workflow_entries import register_default_workflows
from services.mcp.consumer.github_adapter import GitHubIssuesResult
from services.shared_types import IntentCategory

_USER = "6b3d2e40-2051-4b00-9e00-000000002051"
_REPO = "dinp-machine/piper-test-activity"
_ADAPTER = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_open_issues"
_DEFAULT_REPO = "services.integrations.github.repo_resolver.get_user_default_repo"
PHRASE = "what issues are assigned to me?"


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name}); this read is deterministic")


def _issue(n):
    return {"number": n, "title": f"test issue {n}", "labels": []}


def _adapter(assigned, repo_total):
    async def list_open_issues(_self, user_id, *, limit=50, repository=None):
        if repository is None:
            return GitHubIssuesResult(issues=list(assigned), total=len(assigned))
        page = [_issue(n) for n in range(repo_total, 0, -1)][:limit]
        return GitHubIssuesResult(issues=page, total=repo_total)

    return list_open_issues


async def _dispatch(assigned=(), repo_total=0, session_id="sess-2051"):
    register_default_workflows()
    svc = IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))
    intent = Intent(
        category=IntentCategory.QUERY,
        action="list_assigned_issues",
        confidence=0.9,
        original_message=PHRASE,
        context={"original_message": PHRASE, "user_id": _USER},
    )
    with (
        patch(_ADAPTER, new=_adapter(assigned, repo_total)),
        patch(_DEFAULT_REPO, new=AsyncMock(return_value=_REPO)),
    ):
        return await dispatch_workflow(
            workflow_type="list_assigned_issues",
            session_id=session_id,
            user_id=_USER,
            context={"intent": intent, "workflow_id": "wf-2051", "intent_service": svc},
        )


class TestAliasRegistration:
    def test_alias_shares_the_list_issues_entry(self):
        register_default_workflows()
        wf = get_action_workflows()
        assert "list_assigned_issues" in wf
        assert wf["list_assigned_issues"] is wf["list_issues_query"] is wf["list_issues"]

    def test_router_grammar_maps_it_to_the_one_operation(self):
        grammar = derive_routing_grammar()
        assert grammar.alias_to_canonical["list_assigned_issues"] == "list_issues"
        names = [op.name for op in grammar.operations]
        assert "list_assigned_issues" not in names  # collapsed, not a new op

    def test_catalog_text_does_not_name_the_alias(self):
        # Aliases are not rendered: the router's prompt text is unchanged by
        # this registration (measured: byte-identical prompt, 2026-10-17).
        prompt = build_routing_prompt("x", derive_routing_grammar())
        assert "list_assigned_issues" not in prompt

    def test_wired_actions_name_the_entry_once(self):
        register_default_workflows()
        assert "list_assigned_issues" not in wired_chat_actions()


class TestTheReadRuns:
    pytestmark = pytest.mark.asyncio

    async def test_zero_assigned_answers_with_the_2040_scope_line(self):
        result = await _dispatch(assigned=(), repo_total=7)
        assert result is not None and result.success
        assert result.message == (
            "You have no open issues assigned to you. "
            f"There are 7 open issues in {_REPO}. "
            f"Say 'show open issues in {_REPO}' to see them."
        )
        assert "pull that up" not in result.message.lower()
        assert result.intent_data["context"]["scope"] == "assigned_to_you"

    async def test_nine_assigned_is_the_capped_list(self):
        result = await _dispatch(assigned=[_issue(n) for n in range(9, 0, -1)], repo_total=0)
        assert result is not None and result.success
        assert result.message.startswith(
            "You have **9 open issues** assigned to you across all your repositories."
        )
        assert result.message.count("\n- **#") == 5
        assert "That's 5 of 9 — say the word and I'll pull the rest." in result.message
        assert result.intent_data["list_remainder_offer_pending"] is True
