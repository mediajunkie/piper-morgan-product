"""#2151 GH-NONSTRICT (rails): the native fallback of list_issues, list_prs and stale_prs.

The fallback ran when the connector said CONNECT_REQUIRED, and read with
``get_open_issues(limit=...)``: lenient (a failed read was []) and on the router's native
PAT (the HOST's token, the #2127 shape), so an account with no GitHub of its own could be
told "You don't have any open issues", or shown the host's. Now it reads
``get_open_items_strict``: as this account (grant, then its own PAT), and a read that didn't
happen raises into #1524's honest lines.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations.github.github_integration_router import GitHubIntegrationRouter
from services.integrations.github.read_failed import GitHubReadFailed
from services.mcp.consumer.connector import DegradationReason

UID = "00000000-0000-0000-0000-00000000215a"


def _router(direct):
    router = GitHubIntegrationRouter.__new__(GitHubIntegrationRouter)
    router._initialized = True
    router._user_id = UID
    router.mcp_adapter = MagicMock()
    router.mcp_adapter.list_github_issues_direct = direct
    router.spatial_github = None
    router._resolve_default_repo = AsyncMock(return_value=("o", "r"))
    return router


@pytest.mark.asyncio
async def test_the_read_is_strict_and_as_this_account():
    items = [
        {"number": 1, "state": "open", "is_pull_request": False},
        {"number": 2, "state": "open", "is_pull_request": True},
        {"number": 3, "state": "closed", "is_pull_request": False},
    ]
    direct = AsyncMock(return_value=items)
    out = await _router(direct).get_open_items_strict(limit=100)
    assert [i["number"] for i in out] == [1, 2]
    direct.assert_awaited_once_with("r", "o", strict=True, user_id=UID, state="open")


@pytest.mark.asyncio
async def test_no_repo_raises_repo_unresolved_never_empty():
    router = _router(AsyncMock(return_value=[]))
    router._resolve_default_repo = AsyncMock(return_value=None)
    router.mcp_adapter._grant_headers_or_raise = AsyncMock(return_value={"Authorization": "x"})
    with pytest.raises(GitHubReadFailed) as ei:
        await router.get_open_items_strict()
    assert ei.value.reason is DegradationReason.REPO_UNRESOLVED


async def _list_issues(intent_service, failure):
    from services.mcp.consumer.connector import DegradationResponse
    from services.mcp.consumer.github_adapter import GitHubIssuesResult

    degraded = GitHubIssuesResult(
        degradation=DegradationResponse(
            reason=DegradationReason.CONNECT_REQUIRED, user_message="fake connect"
        )
    )
    native = MagicMock()
    native.initialize = AsyncMock()
    native.get_open_items_strict = AsyncMock(side_effect=failure)
    with (
        patch(
            "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_open_issues",
            new=AsyncMock(return_value=degraded),
        ),
        patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=native,
        ),
    ):
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        intent = Intent(
            category=IntentCategory.QUERY,
            action="list_issues_query",
            original_message="list my issues",
            context={"original_message": "list my issues", "user_id": UID},
        )
        return await intent_service._handle_list_issues_query(intent, "wf")


@pytest.mark.asyncio
async def test_list_issues_never_connected_says_so(intent_service):
    res = await _list_issues(
        intent_service, GitHubReadFailed("x", None, repo="o/r", detail="no_credential")
    )
    assert res.message.startswith("GitHub isn't connected yet.")
    assert "don't have any open issues" not in res.message


@pytest.mark.asyncio
async def test_list_issues_failed_read_says_it_couldnt_read(intent_service):
    res = await _list_issues(
        intent_service,
        GitHubReadFailed("x", DegradationReason.STALE_TOKEN, repo="o/r", detail="stale_token"),
    )
    assert res.message.startswith("I couldn't read o/r with this account's GitHub connection")


@pytest.mark.asyncio
async def test_no_repo_and_no_credential_is_not_connected_first():
    """Web 10-24 14:09 (web-fresh-test): an account with no GitHub at all also has no repo;
    it must hear "not connected", never "which repository?"."""
    router = _router(AsyncMock(return_value=[]))
    router._resolve_default_repo = AsyncMock(return_value=None)
    router.mcp_adapter._grant_headers_or_raise = AsyncMock(
        side_effect=GitHubReadFailed("x", None, detail="no_credential")
    )
    with pytest.raises(GitHubReadFailed) as ei:
        await router.get_open_items_strict()
    assert ei.value.detail == "no_credential"


@pytest.mark.asyncio
async def test_no_repo_with_a_credential_still_asks_which_repo():
    router = _router(AsyncMock(return_value=[]))
    router._resolve_default_repo = AsyncMock(return_value=None)
    router.mcp_adapter._grant_headers_or_raise = AsyncMock(return_value={"Authorization": "x"})
    with pytest.raises(GitHubReadFailed) as ei:
        await router.get_open_items_strict()
    assert ei.value.reason is DegradationReason.REPO_UNRESOLVED


@pytest.mark.asyncio
async def test_the_read_asks_for_open_items_only_and_says_when_the_window_is_full():
    """Arch 15:29 gap A: state=open, so the 100-item page is a window over open rows."""
    page = [{"number": n, "state": "open", "is_pull_request": False} for n in range(100)]
    direct = AsyncMock(return_value=page)
    router = _router(direct)
    out = await router.get_open_items_strict(limit=100)
    assert len(out) == 100 and router.last_open_window_full is True
    assert direct.await_args.kwargs["state"] == "open"
    router2 = _router(AsyncMock(return_value=page[:7]))
    await router2.get_open_items_strict()
    assert router2.last_open_window_full is False


@pytest.mark.asyncio
async def test_a_full_window_never_states_a_bare_total(intent_service):
    from services.mcp.consumer.connector import DegradationResponse
    from services.mcp.consumer.github_adapter import GitHubIssuesResult

    degraded = GitHubIssuesResult(
        degradation=DegradationResponse(
            reason=DegradationReason.CONNECT_REQUIRED, user_message="fake connect"
        )
    )
    native = MagicMock()
    native.initialize = AsyncMock()
    native.get_open_items_strict = AsyncMock(
        return_value=[
            {
                "number": n,
                "title": f"fake {n}",
                "state": "open",
                "is_pull_request": False,
                "labels": [],
            }
            for n in range(60)
        ]
    )
    native.last_open_window_full = True
    with (
        patch(
            "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_open_issues",
            new=AsyncMock(return_value=degraded),
        ),
        patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=native,
        ),
    ):
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        intent = Intent(
            category=IntentCategory.QUERY,
            action="list_issues_query",
            original_message="list my issues",
            context={"original_message": "list my issues", "user_id": UID},
        )
        res = await intent_service._handle_list_issues_query(intent, "wf")
    assert "You have **60+ open issues**. (counted among your first 100 open issues" in res.message
    assert "there may be more" in res.message


@pytest.mark.asyncio
async def test_a_short_window_never_says_at_least(intent_service):
    from services.mcp.consumer.connector import DegradationResponse
    from services.mcp.consumer.github_adapter import GitHubIssuesResult

    degraded = GitHubIssuesResult(
        degradation=DegradationResponse(
            reason=DegradationReason.CONNECT_REQUIRED, user_message="fake connect"
        )
    )
    native = MagicMock()
    native.initialize = AsyncMock()
    native.get_open_items_strict = AsyncMock(
        return_value=[
            {
                "number": n,
                "title": f"fake {n}",
                "state": "open",
                "is_pull_request": False,
                "labels": [],
            }
            for n in range(7)
        ]
    )
    native.last_open_window_full = False
    with (
        patch(
            "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_open_issues",
            new=AsyncMock(return_value=degraded),
        ),
        patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=native,
        ),
    ):
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        intent = Intent(
            category=IntentCategory.QUERY,
            action="list_issues_query",
            original_message="list my issues",
            context={"original_message": "list my issues", "user_id": UID},
        )
        res = await intent_service._handle_list_issues_query(intent, "wf")
    assert "You have **7 open issues**." in res.message
    assert "at least" not in res.message


@pytest.mark.asyncio
async def test_the_count_is_taken_before_the_display_slice(intent_service):
    """Arch 15:58: 60 issues and 5 PRs (not a full window) read as "60", never "50"."""
    from services.mcp.consumer.connector import DegradationResponse
    from services.mcp.consumer.github_adapter import GitHubIssuesResult

    degraded = GitHubIssuesResult(
        degradation=DegradationResponse(
            reason=DegradationReason.CONNECT_REQUIRED, user_message="fake connect"
        )
    )
    items = [
        {"number": n, "title": f"fake {n}", "state": "open", "is_pull_request": False, "labels": []}
        for n in range(60)
    ] + [
        {"number": 900 + n, "title": "pr", "state": "open", "is_pull_request": True, "labels": []}
        for n in range(5)
    ]
    native = MagicMock()
    native.initialize = AsyncMock()
    native.get_open_items_strict = AsyncMock(return_value=items)
    native.last_open_window_full = False
    with (
        patch(
            "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_open_issues",
            new=AsyncMock(return_value=degraded),
        ),
        patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=native,
        ),
    ):
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        intent = Intent(
            category=IntentCategory.QUERY,
            action="list_issues_query",
            original_message="list my issues",
            context={"original_message": "list my issues", "user_id": UID},
        )
        res = await intent_service._handle_list_issues_query(intent, "wf")
    assert "You have **60 open issues**." in res.message
