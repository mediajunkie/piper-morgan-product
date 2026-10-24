"""#2128: 'Issues/PRs Closed: 0' and 'what did we ship' finding nothing while the repo had
closed work (PA's #1386 run on web-seed-1386, Q41 and Q51).

Two faults: the router passed (project, limit) positionally into the adapter's
(repo, owner, ...) since #1042, so every read hit repos/<limit>/<None>/issues and
returned []; and the adapter returned [] for a read that did not happen. Now the
router resolves the repo and calls by keyword, the adapter reads with the account's
own grant and raises GitHubReadFailed when the read did not happen, and the two
handlers say so instead of reporting zero.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations.github.github_integration_router import GitHubIntegrationRouter
from services.integrations.github.read_failed import GitHubReadFailed
from services.intent.intent_service import IntentService
from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import GitHubCredential, GitHubMCPSpatialAdapter

GRANT = "services.mcp.consumer.github_adapter.ConnectorGrantStore.get"
SESSION = "services.mcp.consumer.github_adapter.AsyncSessionFactory.session_scope"


class _Scope:
    async def __aenter__(self):
        return object()

    async def __aexit__(self, *a):
        return False


@pytest.fixture
def intent_service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


# --- the router's call shape (the bug) -------------------------------------------


@pytest.mark.asyncio
async def test_the_router_resolves_the_repo_and_calls_the_adapter_by_keyword():
    router = GitHubIntegrationRouter()
    router._user_id = "u-1"
    router.mcp_adapter = MagicMock()
    router.mcp_adapter.get_closed_issues = AsyncMock(return_value=[{"number": 1}])
    router._resolve_default_repo = AsyncMock(return_value=("octo", "seeded"))
    out = await router.get_closed_issues(limit=50, user_id="u-1")
    assert out == [{"number": 1}]
    kwargs = router.mcp_adapter.get_closed_issues.await_args.kwargs
    assert kwargs == {
        "repo": "seeded",
        "owner": "octo",
        "project": None,
        "limit": 50,
        "user_id": "u-1",
    }
    assert router.mcp_adapter.get_closed_issues.await_args.args == ()


@pytest.mark.asyncio
async def test_an_unresolved_repo_is_a_failed_read_not_an_empty_one():
    router = GitHubIntegrationRouter()
    router.mcp_adapter = MagicMock()
    router.mcp_adapter.get_closed_issues = AsyncMock(return_value=[])
    router._resolve_default_repo = AsyncMock(return_value=None)
    with pytest.raises(GitHubReadFailed) as ei:
        await router.get_closed_issues(limit=50, user_id="u-1")
    assert ei.value.reason is DegradationReason.REPO_UNRESOLVED
    router.mcp_adapter.get_closed_issues.assert_not_awaited()


# --- the adapter's read ------------------------------------------------------------


@pytest.fixture
def adapter():
    a = GitHubMCPSpatialAdapter()
    a._rest_configured = lambda: False
    return a


@pytest.mark.asyncio
async def test_a_principal_reads_with_its_own_grant(adapter):
    adapter.resolve_credential = AsyncMock(
        return_value=GitHubCredential(
            owner_id="u-1", mcp_server_ref="github", token=None, leg="oauth"
        )
    )
    adapter._call_github_api_list = AsyncMock(
        return_value=[{"number": 7, "state": "closed", "labels": [], "user": {}}]
    )
    with (
        patch(GRANT, new=AsyncMock(return_value="gho_test")),
        patch(SESSION, return_value=_Scope()),
    ):
        out = await adapter.get_closed_issues("seeded", "octo", limit=50, user_id="u-1")
    assert [i["number"] for i in out] == [7]
    assert adapter._call_github_api_list.await_args.kwargs["headers"] == {
        "Authorization": "Bearer gho_test"
    }


@pytest.mark.asyncio
async def test_no_credential_is_a_failed_read(adapter):
    adapter.resolve_credential = AsyncMock(
        return_value=DegradationResponse(
            reason=DegradationReason.CONNECT_REQUIRED, user_message="connect GitHub"
        )
    )
    adapter._call_github_api_list = AsyncMock(return_value=[])
    with pytest.raises(GitHubReadFailed) as ei:
        await adapter.get_closed_issues("seeded", "octo", limit=50, user_id="u-1")
    assert (
        ei.value.reason is None
        and ei.value.detail == "no_credential"
        and ei.value.repo == "octo/seeded"
    )
    adapter._call_github_api_list.assert_not_awaited()


@pytest.mark.asyncio
async def test_no_response_is_a_failed_read_and_an_empty_list_is_empty(adapter):
    adapter._call_github_api_list = AsyncMock(return_value=None)
    with pytest.raises(GitHubReadFailed) as ei:
        await adapter.get_closed_issues("seeded", "octo", limit=50)
    assert ei.value.reason is DegradationReason.UNREACHABLE and ei.value.detail == "no_response"
    adapter._call_github_api_list = AsyncMock(return_value=[])
    assert await adapter.get_closed_issues("seeded", "octo", limit=50) == []


@pytest.mark.asyncio
async def test_an_error_during_the_read_is_a_failed_read_with_the_type(adapter):
    adapter._call_github_api_list = AsyncMock(side_effect=TimeoutError("slow"))
    with pytest.raises(GitHubReadFailed) as ei:
        await adapter.get_closed_issues("seeded", "octo", limit=50)
    assert ei.value.reason is DegradationReason.UNREACHABLE and ei.value.detail == "TimeoutError"


# --- the handlers ------------------------------------------------------------------


def _intent(action):
    from services.domain.models import Intent, IntentCategory

    return Intent(
        category=IntentCategory.QUERY,
        action=action,
        confidence=0.9,
        context={"user_id": "u-1", "session_id": "s-1", "original_message": action},
    )


@pytest.mark.asyncio
async def test_shipped_this_week_says_the_read_failed_not_nothing_shipped(intent_service):
    with patch(
        "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
    ) as MockRouter:
        mock_router = MagicMock()
        mock_router.is_available = AsyncMock(return_value=True)
        mock_router.initialize = AsyncMock()
        # #2151 (Arch 10-24): a connected account's failed credential; no_credential now
        # means never connected (the not-connected line).
        mock_router.get_closed_issues = AsyncMock(
            side_effect=GitHubReadFailed(
                "x", DegradationReason.STALE_TOKEN, repo="octo/seeded", detail="stale_token"
            )
        )
        MockRouter.return_value = mock_router
        result = await intent_service._handle_shipped_this_week(_intent("shipped_this_week"), "wf")
    assert result.success is False
    assert result.message == (
        "I couldn't read octo/seeded with this account's GitHub connection, so there's nothing to report yet."
    )
    assert "No closed" not in result.message and "0" not in result.message
    assert mock_router.get_closed_issues.await_args.kwargs.get("user_id") == "u-1"


@pytest.mark.asyncio
async def test_productivity_never_counts_zero_for_a_failed_read(intent_service):
    with (
        patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter,
        patch("services.repositories.todo_repository.TodoRepository") as MockRepo,
        patch("services.intent.intent_service.AsyncSessionFactory.session_scope") as scope,
    ):
        mock_router = MagicMock()
        mock_router.is_available = AsyncMock(return_value=True)
        mock_router.initialize = AsyncMock()
        mock_router.get_closed_issues = AsyncMock(
            side_effect=GitHubReadFailed(
                "x", DegradationReason.UNREACHABLE, repo="octo/seeded", detail="no_response"
            )
        )
        MockRouter.return_value = mock_router
        repo = MagicMock()
        repo.get_completion_stats = AsyncMock(
            return_value={"completed": 2, "total_created": 3, "active": 1, "completion_rate": 66.7}
        )
        MockRepo.return_value = repo
        scope.return_value.__aenter__ = AsyncMock(return_value=MagicMock())
        scope.return_value.__aexit__ = AsyncMock(return_value=False)
        result = await intent_service._handle_productivity_query(
            _intent("productivity"), "wf", "s-1"
        )
    assert "Issues/PRs Closed: 0" not in result.message
    assert "couldn't read this account's GitHub connection" in result.message


# --- 2129 follow-up: a closed PR is labelled a PR (CXO's 2128 nit, served on fc183c41bc) -----


@pytest.mark.asyncio
async def test_the_adapter_keeps_githubs_pull_request_marker_and_url(adapter):
    adapter.resolve_credential = AsyncMock(
        return_value=GitHubCredential(
            owner_id="u-1", mcp_server_ref="github", token=None, leg="oauth"
        )
    )
    adapter._call_github_api_list = AsyncMock(
        return_value=[
            {
                "number": 27,
                "title": "Fix typo in setup notes",
                "state": "closed",
                "labels": [],
                "user": {},
                "html_url": "https://github.com/octo/seeded/pull/27",
                "pull_request": {"url": "https://api.github.com/repos/octo/seeded/pulls/27"},
            },
            {"number": 26, "title": "A bug", "state": "closed", "labels": [], "user": {}},
        ]
    )
    with (
        patch(GRANT, new=AsyncMock(return_value="gho_test")),
        patch(SESSION, return_value=_Scope()),
    ):
        out = await adapter.get_closed_issues("seeded", "octo", limit=50, user_id="u-1")
    assert [(i["number"], i["is_pull_request"]) for i in out] == [(27, True), (26, False)]
    assert out[0]["html_url"] == "https://github.com/octo/seeded/pull/27"


@pytest.mark.asyncio
async def test_shipped_this_week_labels_a_closed_pr_as_a_pr(intent_service):
    closed = datetime.now(timezone.utc) - timedelta(days=1)
    items = [
        {
            "number": 27,
            "title": "Fix typo in setup notes",
            "closed_at": closed.isoformat().replace("+00:00", "Z"),
            "is_pull_request": True,
            "html_url": "https://github.com/octo/seeded/pull/27",
        },
        {
            "number": 26,
            "title": "A bug",
            "closed_at": closed.isoformat().replace("+00:00", "Z"),
            "is_pull_request": False,
        },
    ]
    with patch(
        "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
    ) as MockRouter:
        mock_router = MagicMock()
        mock_router.is_available = AsyncMock(return_value=True)
        mock_router.initialize = AsyncMock()
        mock_router.get_closed_issues = AsyncMock(return_value=items)
        MockRouter.return_value = mock_router
        result = await intent_service._handle_shipped_this_week(_intent("shipped_this_week"), "wf")
    assert "- PR #27: Fix typo in setup notes" in result.message
    assert "Issue #27" not in result.message
    assert "- Issue #26: A bug" in result.message
    assert "https://github.com/octo/seeded/pull/27" in result.message
