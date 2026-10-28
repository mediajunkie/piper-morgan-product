"""#2173 (CXO 10-25, class 3): with no saved GitHub username, the standup and Radar
showed every open issue in the default repo as the person's own work ("You're working
on X", "X hasn't moved in 3 days"). Web on alpha 73e050aae5: unassigned #30 "testing"
on an account signed in as @dinp-machine.

Now "assigned to me" defaults to the signed-in login. A saved username still wins. A
login that can't be read is a failed source with CXO's line, never show-all.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import GITHUB_ASSIGNEE_UNRESOLVED_LINE, degraded_disclosure
from services.integrations.github.read_failed import GitHubReadFailed
from services.mcp.consumer.connector import DegradationReason
from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter as _A
from services.radar.feed_factory import WorkItemProvider, WorkItemReadKind, WorkItemScopeReason

SVC = "services.integrations.integration_status_service.IntegrationStatusService"
ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
HANDLE_READER = "services.integrations.github.repo_resolver.read_user_github_handle"


def _router(issues):
    router = MagicMock()
    router.initialize = AsyncMock()
    router.get_open_issues = AsyncMock(return_value=issues)
    router.close = AsyncMock()
    return router


def _issue(num, assignees):
    return {"number": num, "title": f"#{num}", "state": "open", "assignees": assignees}


ISSUES = [_issue(1, ["dinp-machine"]), _issue(7, ["dinp-machine"]), _issue(30, [])]


async def _gather(saved, login, **kw):
    with (
        patch(
            f"{SVC}.get_status",
            new=AsyncMock(return_value={"configured": True, "check_failed": False}),
        ),
        patch(ROUTER, return_value=_router(ISSUES)),
        patch(HANDLE_READER, new=AsyncMock(return_value=saved)),
        patch.object(_A, "account_login", login),
    ):
        return await WorkItemProvider().gather_for_user("u1", **kw)


@pytest.mark.asyncio
async def test_no_saved_username_scopes_to_the_signed_in_login():
    login = AsyncMock(return_value="dinp-machine")
    outcome = await _gather(None, login)
    assert outcome.kind == WorkItemReadKind.ITEMS
    assert [i["number"] for i in outcome.items] == [1, 7]  # #30, unassigned, is gone
    login.assert_awaited_once()


@pytest.mark.asyncio
async def test_a_saved_username_wins_and_the_login_is_not_read():
    login = AsyncMock(return_value="dinp-machine")
    outcome = await _gather("someone-else", login)
    assert outcome.kind == WorkItemReadKind.VERIFIED_EMPTY
    login.assert_not_awaited()


@pytest.mark.asyncio
async def test_an_unreadable_login_fails_the_source_never_shows_all():
    login = AsyncMock(side_effect=GitHubReadFailed("no login", None, detail="login_unresolved"))
    outcome = await _gather(None, login)
    assert outcome.failed
    assert outcome.items == ()
    assert outcome.reason is WorkItemScopeReason.ASSIGNEE_UNRESOLVED


@pytest.mark.asyncio
async def test_a_credential_failure_in_the_login_read_keeps_its_reason():
    login = AsyncMock(side_effect=GitHubReadFailed("stale", DegradationReason.STALE_TOKEN))
    outcome = await _gather(None, login)
    assert outcome.failed and outcome.reason is DegradationReason.STALE_TOKEN


@pytest.mark.asyncio
async def test_the_unscoped_first_contact_read_needs_no_login():
    login = AsyncMock(side_effect=AssertionError("must not be read"))
    outcome = await _gather(None, login, include_unassigned=True)
    assert [i["number"] for i in outcome.items] == [1, 7, 30]


def test_the_failed_source_line_is_cxos_words():
    details = [{"label": "your GitHub", "reason": "assignee_unresolved", "connector": "GitHub"}]
    for empty in (False, True):
        assert degraded_disclosure([], "chat", empty=empty, details=details) == (
            GITHUB_ASSIGNEE_UNRESOLVED_LINE
        )
    assert GITHUB_ASSIGNEE_UNRESOLVED_LINE == (
        "I couldn't tell which GitHub issues are assigned to you, so this summary doesn't "
        "include GitHub. Try again in a moment; if it keeps failing, tell us."
    )


def test_with_another_failure_it_joins_the_one_sentence():
    details = [
        {"label": "your GitHub", "reason": "assignee_unresolved", "connector": "GitHub"},
        {"label": "your calendar", "reason": None, "connector": None},
    ]
    line = degraded_disclosure([], "chat", empty=False, details=details)
    assert line == (
        "I couldn't reach your calendar just now, and I couldn't tell which GitHub issues "
        "are assigned to you, so what's below is incomplete."
    )


@pytest.mark.asyncio
async def test_account_login_reads_get_user_with_the_accounts_credential():
    adapter = _A.__new__(_A)
    with (
        patch.object(
            _A,
            "_grant_headers_or_raise",
            AsyncMock(return_value={"Authorization": "Bearer fake-token-login"}),
        ),
        patch(
            "services.integrations.github.token_validator.verify_github_token",
            new=AsyncMock(return_value={"authenticated": True, "username": "dinp-machine"}),
        ) as verify,
    ):
        assert await adapter.account_login("u1") == "dinp-machine"
    verify.assert_awaited_once_with("fake-token-login")


@pytest.mark.asyncio
async def test_account_login_raises_when_get_user_gives_no_login():
    adapter = _A.__new__(_A)
    with (
        patch.object(
            _A,
            "_grant_headers_or_raise",
            AsyncMock(return_value={"Authorization": "Bearer fake-token-login"}),
        ),
        patch(
            "services.integrations.github.token_validator.verify_github_token",
            new=AsyncMock(return_value={"authenticated": False, "username": None}),
        ),
        pytest.raises(GitHubReadFailed),
    ):
        await adapter.account_login("u1")
