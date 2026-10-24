"""#1524 (Class 3 must-close): GitHub list reads answered "none" for a read that never
happened. Served instance: PA's #1386 run, Q25 "What's the next milestone?" → "You don't
have any open milestones right now." while the seeded repo had "Beta launch" open.

Cause: the milestone and label handlers built their router with no principal (so the repo
could not resolve and the read had no grant), and the router and adapter returned [] for an
unresolved repo or a failed read. Now the routers read as the principal, an unresolved repo
or a read that did not happen raises, and the handlers say which.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.integrations.github.github_integration_router import GitHubIntegrationRouter
from services.integrations.github.read_failed import GitHubReadFailed, repo_unresolved
from services.intent.intent_service import IntentService
from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import GitHubCredential, GitHubMCPSpatialAdapter
from services.shared_types import IntentCategory

_NATIVE = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
GRANT = "services.mcp.consumer.github_adapter.ConnectorGrantStore.get"
SESSION = "services.mcp.consumer.github_adapter.AsyncSessionFactory.session_scope"
WHICH_REPO = (
    "I couldn't tell which repository you mean. Name one (e.g. `owner/name`), "
    "link a repo to your project, or set a default repo."
)


@pytest.fixture
def intent_service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


def _intent(action, msg):
    return Intent(
        category=IntentCategory.QUERY,
        action=action,
        context={"original_message": msg, "user_id": "u-1"},
    )


def _router(**reads):
    r = MagicMock()
    r.initialize = AsyncMock()
    for name, value in reads.items():
        setattr(
            r,
            name,
            AsyncMock(side_effect=value)
            if isinstance(value, Exception)
            else AsyncMock(return_value=value),
        )
    return r


# --- handlers --------------------------------------------------------------------


@pytest.mark.asyncio
async def test_q25_an_unresolved_repo_says_so_never_says_no_milestones(intent_service):
    r = _router(list_milestones_via_mcp=repo_unresolved())
    with patch(_NATIVE, return_value=r):
        res = await intent_service._handle_list_milestones_query(
            _intent("list_milestones_query", "What's the next milestone?"), "wf"
        )
    assert res.success is False
    assert res.message == WHICH_REPO
    assert "don't have any open milestones" not in res.message
    assert "?" not in res.message  # an imperative: no unarmed question (#1730 Gap-2)
    r.initialize.assert_awaited_once_with(user_id="u-1")  # reads as the principal


@pytest.mark.asyncio
async def test_a_failed_milestone_read_names_the_repo_and_says_it_failed(intent_service):
    from services.mcp.consumer.connector import DegradationReason

    # #2151 (Arch 10-24): a connected account's failed credential (was: no_credential,
    # which now means never connected — see the next test).
    r = _router(
        list_milestones_via_mcp=GitHubReadFailed(
            "x", DegradationReason.STALE_TOKEN, repo="octo/seeded", detail="stale_token"
        )
    )
    with patch(_NATIVE, return_value=r):
        res = await intent_service._handle_list_milestones_query(
            _intent("list_milestones_query", "What's the next milestone?"), "wf"
        )
    assert res.success is False
    assert res.message == (
        "I couldn't read octo/seeded with this account's GitHub connection, so I can't list "
        "its milestones yet."
    )
    assert res.intent_data["context"] == {"read_failed": "stale_token", "detail": "stale_token"}


@pytest.mark.asyncio
async def test_a_never_connected_account_gets_the_not_connected_line(intent_service):
    r = _router(
        list_milestones_via_mcp=GitHubReadFailed(
            "x", None, repo="octo/seeded", detail="no_credential"
        )
    )
    with patch(_NATIVE, return_value=r):
        res = await intent_service._handle_list_milestones_query(
            _intent("list_milestones_query", "What's the next milestone?"), "wf"
        )
    assert res.message == (
        "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can list "
        "its milestones."
    )
    assert "couldn't" not in res.message


@pytest.mark.asyncio
async def test_a_real_empty_answer_still_says_none(intent_service):
    r = _router(list_milestones_via_mcp=[])
    with patch(_NATIVE, return_value=r):
        res = await intent_service._handle_list_milestones_query(
            _intent("list_milestones_query", "What's the next milestone?"), "wf"
        )
    assert res.success is True
    assert res.message == "You don't have any open milestones right now."


@pytest.mark.asyncio
async def test_labels_read_as_the_principal_and_say_a_failed_read(intent_service):
    r = _router(
        list_labels_via_mcp=GitHubReadFailed(
            "x", DegradationReason.UNREACHABLE, repo="octo/seeded", detail="no_response"
        )
    )
    with patch(_NATIVE, return_value=r):
        res = await intent_service._handle_list_labels_query(
            _intent("list_labels_query", "show labels"), "wf"
        )
    r.initialize.assert_awaited_once_with(user_id="u-1")
    assert res.success is False
    assert "couldn't read octo/seeded" in res.message and "labels" in res.message


# --- router ----------------------------------------------------------------------


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method",
    [
        "list_milestones_via_mcp",
        "list_releases_via_mcp",
        "list_labels_via_mcp",
        "list_branches_via_mcp",
    ],
)
async def test_router_unresolved_repo_raises_instead_of_returning_empty(method):
    router = GitHubIntegrationRouter()
    router._initialized = True
    router.mcp_adapter = MagicMock()
    router._resolve_default_repo = AsyncMock(return_value=None)
    with pytest.raises(GitHubReadFailed) as ei:
        await getattr(router, method)()
    assert ei.value.reason is DegradationReason.REPO_UNRESOLVED


@pytest.mark.asyncio
async def test_router_passes_the_principal_to_the_adapter():
    router = GitHubIntegrationRouter()
    router._initialized = True
    router._user_id = "u-1"
    router.mcp_adapter = MagicMock()
    router.mcp_adapter.list_milestones = AsyncMock(return_value=[{"title": "Beta launch"}])
    router._resolve_default_repo = AsyncMock(return_value=("octo", "seeded"))
    out = await router.list_milestones_via_mcp()
    assert out == [{"title": "Beta launch"}]
    assert router.mcp_adapter.list_milestones.await_args.kwargs["user_id"] == "u-1"


@pytest.mark.asyncio
async def test_router_without_an_adapter_is_a_failed_read():
    router = GitHubIntegrationRouter()
    router._initialized = True
    router.mcp_adapter = None
    with pytest.raises(GitHubReadFailed) as ei:
        await router.list_labels_via_mcp(owner="o", repo="r")
    assert ei.value.reason is None and ei.value.detail == "no_adapter"


# --- adapter ---------------------------------------------------------------------


class _Scope:
    async def __aenter__(self):
        return object()

    async def __aexit__(self, *a):
        return False


@pytest.mark.asyncio
async def test_adapter_reads_milestones_with_the_principals_grant():
    a = GitHubMCPSpatialAdapter()
    a.resolve_credential = AsyncMock(
        return_value=GitHubCredential(
            owner_id="u-1", mcp_server_ref="github", token=None, leg="oauth"
        )
    )
    a._call_github_api_list = AsyncMock(return_value=[{"title": "Beta launch", "number": 1}])
    with (
        patch(GRANT, new=AsyncMock(return_value="gho_test")),
        patch(SESSION, return_value=_Scope()),
    ):
        out = await a.list_milestones("seeded", "octo", user_id="u-1")
    assert out and out[0]["title"] == "Beta launch"
    assert a._call_github_api_list.await_args.kwargs["headers"] == {
        "Authorization": "Bearer gho_test"
    }


@pytest.mark.asyncio
async def test_adapter_without_a_credential_is_a_failed_read_and_does_not_read():
    a = GitHubMCPSpatialAdapter()
    a.resolve_credential = AsyncMock(
        return_value=DegradationResponse(
            reason=DegradationReason.CONNECT_REQUIRED, user_message="connect"
        )
    )
    a._call_github_api_list = AsyncMock(return_value=[])
    with pytest.raises(GitHubReadFailed) as ei:
        await a.list_labels("seeded", "octo", user_id="u-1")
    assert (
        ei.value.reason is None
        and ei.value.detail == "no_credential"
        and ei.value.repo == "octo/seeded"
    )
    a._call_github_api_list.assert_not_awaited()
