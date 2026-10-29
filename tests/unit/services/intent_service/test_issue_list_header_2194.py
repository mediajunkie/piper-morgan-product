"""#2194 — the issue-list header states the scope the read used (CXO 2026-10-29 08:51).

One composer (``services/intent_service/issue_list_header.py``) builds the scope
words from the applied qualifiers. "across all your repositories" only on the
unscoped assignee read; a milestone read keeps "assigned to you" (the assignee
term stays on the query) and names the milestone's repo; a named repo read has
neither; label is spelled "labelled"; singular for 1.
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.issue_list_header import (
    compose_count_header,
    compose_empty_line,
    compose_scope,
    repo_of_item,
    shared_repo,
)
from services.mcp.consumer.github_adapter import GitHubIssuesResult
from services.shared_types import IntentCategory

_CONN = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_open_issues"
REPO = "mediajunkie/piper-morgan-product"


def _item(n, repo=REPO, *, api=True, html=True):
    d = {"number": n, "title": f"Issue {n}", "labels": []}
    if api and repo:
        d["repository_url"] = f"https://api.github.com/repos/{repo}"
    if html and repo:
        d["html_url"] = f"https://github.com/{repo}/issues/{n}"
    return d


@pytest.fixture
def svc():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            s = IntentService()
    s._user_default_repo_or_none = AsyncMock(return_value=None)
    return s


def _intent(message, args=None, **ctx):
    context = {"original_message": message, **ctx}
    if args is not None:
        context["inversion_args"] = args
    return Intent(
        category=IntentCategory.QUERY,
        action="list_issues_query",
        original_message=message,
        context=context,
    )


async def _run(svc, intent, issues, total):
    stub = AsyncMock(return_value=GitHubIssuesResult(issues=issues, total=total))
    with patch(_CONN, new=stub):
        res = await svc._handle_list_issues_query(intent, "wf")
    return stub, res


# ── the pure composer ──


def test_repo_from_each_item_field():
    assert repo_of_item(_item(1, html=False)) == REPO
    assert repo_of_item(_item(1, api=False)) == REPO
    assert repo_of_item({"repository": {"full_name": "o/r"}}) == "o/r"
    assert repo_of_item({"number": 1}) is None


def test_shared_repo_only_when_every_item_agrees():
    assert shared_repo([_item(1), _item(2)]) == REPO
    assert shared_repo([_item(1), _item(2, "other/repo")]) is None
    assert shared_repo([_item(1), {"number": 2}]) is None
    assert shared_repo([]) is None


def test_scope_order_and_words():
    assert compose_scope(named_repo=None, assignee_scoped=True) == (
        " assigned to you across all your repositories"
    )
    assert compose_scope(named_repo=REPO, assignee_scoped=False) == f" in {REPO}"
    assert compose_scope(
        named_repo=None, assignee_scoped=True, milestone="MVP", milestone_repo=REPO
    ) == (f' assigned to you in {REPO} in milestone "MVP"')
    assert compose_scope(named_repo=None, assignee_scoped=True, label="bug") == (
        ' assigned to you across all your repositories labelled "bug"'
    )
    assert compose_scope(named_repo=REPO, assignee_scoped=False, milestone="MVP", label="bug") == (
        f' in {REPO} in milestone "MVP" labelled "bug"'
    )


def test_count_header_singular_and_closed():
    assert compose_count_header(total=1, state_word="open", scope=f" in {REPO}") == (
        f"You have **1 open issue** in {REPO}."
    )
    assert compose_count_header(total=2, state_word="closed", scope="") == (
        "You have **2 closed issues**."
    )


def test_empty_lines_follow_the_scope_rule():
    assert compose_empty_line(
        state_word="open",
        named_repo=None,
        assignee_scoped=True,
        milestone="MVP",
        milestone_repo=REPO,
    ) == (f'You have no open issues assigned to you in {REPO} in milestone "MVP".')
    assert compose_empty_line(
        state_word="open", named_repo=REPO, assignee_scoped=False, label="bug"
    ) == (f'No open issues in {REPO} labelled "bug" right now.')


# ── through the handler ──


@pytest.mark.asyncio
async def test_milestone_read_names_the_items_repo_and_keeps_assigned_to_you(svc):
    stub, res = await _run(
        svc,
        _intent("show my open issues in the MVP milestone", {"milestone": "MVP"}),
        [_item(2184), _item(1595), _item(1386)],
        3,
    )
    assert stub.await_args.kwargs == {"limit": 50, "repository": None, "milestone": "MVP"}
    assert res.message.startswith(
        f'You have **3 open issues** assigned to you in {REPO} in milestone "MVP".'
    )
    assert "across all your repositories" not in res.message
    svc._user_default_repo_or_none.assert_not_awaited()


@pytest.mark.asyncio
async def test_milestone_read_over_several_repos_names_none_and_does_not_guess(svc):
    _, res = await _run(
        svc,
        _intent("show my open issues in the MVP milestone", {"milestone": "MVP"}),
        [_item(1), _item(2, "other/repo")],
        2,
    )
    assert res.message.startswith('You have **2 open issues** assigned to you in milestone "MVP".')
    svc._user_default_repo_or_none.assert_not_awaited()


@pytest.mark.asyncio
async def test_milestone_read_without_item_repos_uses_the_default_repo(svc):
    svc._user_default_repo_or_none = AsyncMock(return_value=REPO)
    _, res = await _run(
        svc,
        _intent("show my open issues in the MVP milestone", {"milestone": "MVP"}),
        [{"number": 1, "title": "x", "labels": []}],
        1,
    )
    assert res.message.startswith(
        f'You have **1 open issue** assigned to you in {REPO} in milestone "MVP".'
    )


@pytest.mark.asyncio
async def test_empty_milestone_read_names_milestone_and_known_repo(svc):
    svc._user_default_repo_or_none = AsyncMock(return_value=REPO)
    _, res = await _run(
        svc,
        _intent("show my open issues in the MVP milestone", {"milestone": "MVP"}),
        [],
        0,
    )
    assert res.message == f'You have no open issues assigned to you in {REPO} in milestone "MVP".'


@pytest.mark.asyncio
async def test_named_repo_read_has_neither_assigned_nor_across(svc):
    _, res = await _run(svc, _intent(f"show open issues in {REPO}"), [_item(1), _item(2)], 2)
    assert res.message.startswith(f"You have **2 open issues** in {REPO}.")
    assert "assigned to you" not in res.message
    assert "across all your repositories" not in res.message


@pytest.mark.asyncio
async def test_unscoped_read_says_across_all_your_repositories(svc):
    _, res = await _run(svc, _intent("show my open issues"), [_item(1)] * 3, 260)
    assert res.message.startswith(
        "You have **260 open issues** assigned to you across all your repositories."
    )


@pytest.mark.asyncio
async def test_label_is_spelled_labelled(svc):
    _, res = await _run(
        svc,
        _intent("open bugs labeled needs-triage", {"label": "needs-triage"}),
        [_item(1)],
        1,
    )
    assert res.message.startswith(
        'You have **1 open issue** assigned to you across all your repositories labelled "needs-triage".'
    )
    assert 'labeled "' not in res.message


@pytest.mark.asyncio
async def test_pick_bound_read_is_repo_wide_and_names_repo_then_milestone(svc):
    """#2184's pick binds the listed repo: the read is repo-wide (no assignee
    term), so the header names the repo and the milestone, not "assigned to you"."""
    stub, res = await _run(
        svc,
        _intent(
            "MVP",
            list_scope_milestone="MVP",
            list_scope_repository=REPO,
            milestone_pick_bound=True,
        ),
        [_item(2184), _item(1595), _item(1386)],
        3,
    )
    assert stub.await_args.kwargs["repository"] == REPO
    assert res.message.startswith(f'You have **3 open issues** in {REPO} in milestone "MVP".')
