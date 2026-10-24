"""#2151 GH-NONSTRICT (Arch 10-23 21:28): the GitHub floor gathers' reads fail loudly.

f57a31faf8 armed ``open_issues_source_failed`` at the gather, but the read under it
(``get_open_issues`` non-strict → ``list_github_issues_direct``) caught every error
and returned [], so a 401 or a timeout still read as zero issues. These pins fail
the read at the adapter (below the old swallow point), through a real
``GitHubIntegrationRouter.get_open_issues``, and assert the gather's flag:

- a failed read (stale token, unreachable) arms the flag;
- CONNECT_REQUIRED is NOT PERFORMED: no flag and no absence claim;
- the non-strict direct read is never called;
- on the empty path, a broken repo resolver is a failed read, not "no repo".
"""

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations.github.github_integration_router import GitHubIntegrationRouter
from services.integrations.github.repo_resolver import UnresolvedRepoError
from services.intent_service.context_assembler import ContextAssembler
from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import GitHubIssuesResult

UID = "00000000-0000-0000-0000-000000002151"


class _NoOpCache:
    async def get_or_compute(self, key, ttl_seconds, compute_fn):
        return await compute_fn()


@pytest.fixture(autouse=True)
def _patch_context_cache(monkeypatch):
    monkeypatch.setattr(
        "services.intent_service.context_assembler.ContextCache",
        lambda *args, **kwargs: _NoOpCache(),
    )


def _router(result: GitHubIssuesResult) -> GitHubIntegrationRouter:
    """A real router (its get_open_issues and _open_issues_via_connector run) whose
    adapter returns ``result`` from the connector read."""
    router = GitHubIntegrationRouter.__new__(GitHubIntegrationRouter)
    router._initialized = True
    router._user_id = UID
    adapter = MagicMock()
    adapter.list_open_issues = AsyncMock(return_value=result)
    adapter.list_github_issues_direct = AsyncMock(return_value=[])
    router.mcp_adapter = adapter
    router.spatial_github = None
    router._resolve_default_repo = AsyncMock(return_value=("o", "r"))
    return router


def _degraded(reason: DegradationReason) -> GitHubIssuesResult:
    return GitHubIssuesResult(
        degradation=DegradationResponse(reason=reason, user_message="fake degrade")
    )


async def _gather(router, resolve_repo=None):
    patches = [
        patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        )
    ]
    if resolve_repo is not None:
        patches.append(
            patch("services.integrations.github.repo_resolver.resolve_repo", new=resolve_repo)
        )
    for p in patches:
        p.start()
    try:
        return await ContextAssembler()._gather_high_priority_issues_context(UID)
    finally:
        for p in patches:
            p.stop()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "reason",
    [DegradationReason.STALE_TOKEN, DegradationReason.UNREACHABLE, DegradationReason.MISCONFIGURED],
)
async def test_a_failed_read_arms_the_flag(reason):
    router = _router(_degraded(reason))
    out = await _gather(router)
    assert out == {"open_issues_source_failed": True}
    router.mcp_adapter.list_open_issues.assert_awaited_once()
    # The non-strict direct read (the old swallow point) is never taken.
    assert router.mcp_adapter.list_github_issues_direct.await_count == 0


@pytest.mark.asyncio
async def test_not_connected_is_not_performed_not_failed():
    router = _router(_degraded(DegradationReason.CONNECT_REQUIRED))
    out = await _gather(router)
    assert out == {}
    assert "open_issues_source_failed" not in out
    assert "open_issue_count" not in out


@pytest.mark.asyncio
async def test_a_read_that_raises_at_the_adapter_arms_the_flag():
    router = _router(GitHubIssuesResult(issues=[]))
    router.mcp_adapter.list_open_issues = AsyncMock(side_effect=TimeoutError("fake timeout"))
    out = await _gather(router)
    assert out == {"open_issues_source_failed": True}


@pytest.mark.asyncio
async def test_issues_read_through_the_connector():
    item = {
        "number": 7,
        "title": "Fake issue",
        "state": "open",
        "labels": [],
        "html_url": "https://github.test/7",
        "updated_at": "2026-10-23",
    }
    out = await _gather(_router(GitHubIssuesResult(issues=[item], total=1)))
    assert out["open_issue_count"] == 1
    assert out["high_priority_issues"][0]["number"] == 7
    assert "open_issues_source_failed" not in out


@pytest.mark.asyncio
async def test_empty_with_a_broken_resolver_is_a_failed_read_not_no_repo():
    out = await _gather(
        _router(GitHubIssuesResult(issues=[], total=0)),
        resolve_repo=AsyncMock(side_effect=RuntimeError("fake resolver failure")),
    )
    assert out == {"open_issues_source_failed": True}
    assert "github_repo_unconfigured" not in out


@pytest.mark.asyncio
async def test_empty_with_no_repo_is_unconfigured():
    out = await _gather(
        _router(GitHubIssuesResult(issues=[], total=0)),
        resolve_repo=AsyncMock(side_effect=UnresolvedRepoError("no repo")),
    )
    assert out.get("github_repo_unconfigured") is True
    assert "open_issues_source_failed" not in out


@pytest.mark.asyncio
async def test_empty_with_a_repo_is_genuinely_none():
    out = await _gather(
        _router(GitHubIssuesResult(issues=[], total=0)),
        resolve_repo=AsyncMock(return_value=MagicMock(full_name="o/r")),
    )
    assert out == {}


# ── Blocked items: the same read, the same contract (10-24) ──


async def _gather_blocked(router):
    with patch(
        "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
        return_value=router,
    ):
        return await ContextAssembler()._gather_blocked_items_context(UID)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "reason",
    [DegradationReason.STALE_TOKEN, DegradationReason.UNREACHABLE, DegradationReason.MISCONFIGURED],
)
async def test_blocked_a_failed_read_arms_the_flag(reason):
    router = _router(_degraded(reason))
    out = await _gather_blocked(router)
    assert out == {"blocked_items_source_failed": True}
    assert router.mcp_adapter.list_github_issues_direct.await_count == 0


@pytest.mark.asyncio
async def test_blocked_a_read_that_raises_at_the_adapter_arms_the_flag():
    router = _router(GitHubIssuesResult(issues=[]))
    router.mcp_adapter.list_open_issues = AsyncMock(side_effect=TimeoutError("fake timeout"))
    assert await _gather_blocked(router) == {"blocked_items_source_failed": True}


@pytest.mark.asyncio
async def test_blocked_not_connected_is_not_performed():
    out = await _gather_blocked(_router(_degraded(DegradationReason.CONNECT_REQUIRED)))
    assert out == {}


@pytest.mark.asyncio
async def test_blocked_items_read_through_the_connector():
    item = {
        "number": 9,
        "title": "Fake blocked",
        "state": "open",
        "labels": [{"name": "status: blocked"}],
        "html_url": "https://github.test/9",
        "updated_at": "2026-10-24",
    }
    out = await _gather_blocked(_router(GitHubIssuesResult(issues=[item], total=1)))
    assert out["blocked_count"] == 1
    assert out["blocked_items"][0]["number"] == 9


# ── Milestones (10-24): the read already raised (#1524); the compute stopped swallowing ──


@asynccontextmanager
async def _fake_scope():
    yield MagicMock()


def _resolver_for(headers):
    """#2151 (Arch 10-24): inject at ``resolve_credential``, below
    ``_grant_headers_or_raise``. A headers dict is a PAT-leg credential whose token
    renders as that Authorization; None is the never-connected degrade."""
    from services.mcp.consumer.github_adapter import GitHubCredential

    if headers is None:
        return AsyncMock(
            return_value=DegradationResponse(
                reason=DegradationReason.CONNECT_REQUIRED, user_message="fake connect"
            )
        )
    token = headers["Authorization"].removeprefix("Bearer ")
    return AsyncMock(
        return_value=GitHubCredential(owner_id=UID, mcp_server_ref="github", token=token, leg="pat")
    )


def _milestones_router(*, headers, api):
    """A real router and the real adapter's ``list_milestones``; the failure is injected
    at the adapter's credential lookup and API call (the bottom of the read)."""
    from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

    adapter = GitHubMCPSpatialAdapter.__new__(GitHubMCPSpatialAdapter)
    adapter.resolve_credential = _resolver_for(headers)
    adapter._call_github_api_list = api
    router = GitHubIntegrationRouter.__new__(GitHubIntegrationRouter)
    router._initialized = True
    router._user_id = UID
    router.mcp_adapter = adapter
    router.spatial_github = None
    router._resolve_default_repo = AsyncMock(return_value=("o", "r"))
    return router


async def _gather_milestones(router):
    with patch(
        "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
        return_value=router,
    ):
        return await ContextAssembler()._gather_active_milestones_context(UID)


@pytest.mark.asyncio
async def test_milestones_no_response_arms_the_flag():
    router = _milestones_router(headers={"Authorization": "fake"}, api=AsyncMock(return_value=None))
    assert await _gather_milestones(router) == {"milestones_source_failed": True}


@pytest.mark.asyncio
async def test_milestones_api_error_arms_the_flag():
    router = _milestones_router(
        headers={"Authorization": "fake"}, api=AsyncMock(side_effect=TimeoutError("fake"))
    )
    assert await _gather_milestones(router) == {"milestones_source_failed": True}


@pytest.mark.asyncio
async def test_milestones_no_credential_is_not_performed():
    api = AsyncMock(return_value=[])
    router = _milestones_router(headers=None, api=api)
    assert await _gather_milestones(router) == {}
    assert api.await_count == 0


@pytest.mark.asyncio
async def test_milestones_no_repo_is_not_performed():
    router = _milestones_router(headers={"Authorization": "fake"}, api=AsyncMock(return_value=[]))
    router._resolve_default_repo = AsyncMock(return_value=None)
    assert await _gather_milestones(router) == {}


@pytest.mark.asyncio
async def test_milestones_read_and_verified_empty():
    m = {"title": "MVP", "number": 1, "due_on": "2026-11-01", "open_issues": 3, "closed_issues": 5}
    router = _milestones_router(headers={"Authorization": "fake"}, api=AsyncMock(return_value=[m]))
    out = await _gather_milestones(router)
    assert out["active_milestone_count"] == 1
    assert out["active_milestones"][0]["title"] == "MVP"
    empty = _milestones_router(headers={"Authorization": "fake"}, api=AsyncMock(return_value=[]))
    assert await _gather_milestones(empty) == {}


# ── Recent activity, GitHub leg (10-24): principal credential, partial read ──


def _activity_router(*, headers, api):
    """A real router and the real adapter's ``list_github_issues_direct``; the failure is
    injected at the adapter's credential lookup and API call."""
    from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

    adapter = GitHubMCPSpatialAdapter.__new__(GitHubMCPSpatialAdapter)
    adapter.resolve_credential = _resolver_for(headers)
    adapter._call_github_api_list = api
    adapter._store_github_context = AsyncMock()
    counter = MagicMock()

    async def _passthrough(_name, coro, input_data=""):
        return await coro

    counter.wrap_mcp_call = _passthrough
    adapter.token_counter = counter
    router = GitHubIntegrationRouter.__new__(GitHubIntegrationRouter)
    router._initialized = True
    router._user_id = UID
    router.mcp_adapter = adapter
    router.spatial_github = None
    router._resolve_default_repo = AsyncMock(return_value=("o", "r"))
    return router


async def _gather_activity(router, *, slack=None):
    assembler = ContextAssembler()
    with (
        patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ),
        patch.object(assembler, "_fetch_calendar_activity_items", new=AsyncMock(return_value=[])),
        patch.object(
            assembler, "_fetch_slack_activity_items", new=AsyncMock(return_value=slack or [])
        ),
        patch.object(assembler, "_fetch_slack_mentions_items", new=AsyncMock(return_value=[])),
    ):
        return await assembler._gather_recent_activity_context(UID)


def _recent_issue():
    from datetime import datetime, timezone

    return {
        "number": 5,
        "title": "Fake recent",
        "state": "open",
        "html_url": "https://github.test/5",
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "labels": [],
        "assignees": [],
    }


@pytest.mark.asyncio
async def test_activity_no_response_arms_the_flag():
    router = _activity_router(headers={"Authorization": "fake"}, api=AsyncMock(return_value=None))
    assert await _gather_activity(router) == {"github_activity_source_failed": True}


@pytest.mark.asyncio
async def test_activity_failure_keeps_the_other_sources_and_names_the_failed_one():
    slack = [{"source": "slack", "title": "fake DM", "updated_at": "2026-10-24T10:00:00Z"}]
    router = _activity_router(
        headers={"Authorization": "fake"}, api=AsyncMock(side_effect=TimeoutError("fake"))
    )
    out = await _gather_activity(router, slack=slack)
    assert out["github_activity_source_failed"] is True
    assert [i["source"] for i in out["recent_activity"]] == ["slack"]


@pytest.mark.asyncio
async def test_activity_no_credential_is_not_performed():
    api = AsyncMock(return_value=[_recent_issue()])
    router = _activity_router(headers=None, api=api)
    assert await _gather_activity(router) == {}
    assert api.await_count == 0


@pytest.mark.asyncio
async def test_activity_reads_with_the_principals_credential():
    api = AsyncMock(return_value=[_recent_issue()])
    router = _activity_router(headers={"Authorization": "fake-grant"}, api=api)
    out = await _gather_activity(router)
    assert out["recent_activity"][0]["number"] == 5
    assert "github_activity_source_failed" not in out
    assert api.await_args.kwargs.get("headers") == {"Authorization": "Bearer fake-grant"}
    router.mcp_adapter.resolve_credential.assert_awaited_once_with(UID)


@pytest.mark.asyncio
async def test_a_partial_read_is_not_cached():
    """The partial result raises past get_or_compute, so a real cache stores nothing."""
    from services.intent_service.context_cache import ContextCache

    calls = []

    class _MemoryCache(ContextCache):
        """The real get_or_compute over an in-memory get/set."""

        def __init__(self):
            self.store = {}

        async def get(self, key):
            return self.store.get(key)

        async def set(self, key, value, ttl_seconds):
            self.store[key] = value
            return True

    cache = _MemoryCache()

    async def _no_response(*args, **kwargs):
        calls.append(1)
        return None

    router = _activity_router(headers={"Authorization": "fake"}, api=_no_response)
    assembler = ContextAssembler()
    assembler.cache = cache
    with (
        patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ),
        patch.object(assembler, "_fetch_calendar_activity_items", new=AsyncMock(return_value=[])),
        patch.object(assembler, "_fetch_slack_activity_items", new=AsyncMock(return_value=[])),
        patch.object(assembler, "_fetch_slack_mentions_items", new=AsyncMock(return_value=[])),
    ):
        first = await assembler._gather_recent_activity_context(UID)
        second = await assembler._gather_recent_activity_context(UID)
    assert first == second == {"github_activity_source_failed": True}
    assert cache.store == {}
    assert len(calls) == 2


# ── Arch 10-24 07:55: only a never-connected account is "not performed" ──


@pytest.mark.asyncio
async def test_a_stale_binding_is_a_failed_read_not_not_connected():
    router = _activity_router(headers=None, api=AsyncMock(return_value=[_recent_issue()]))
    router.mcp_adapter.resolve_credential = AsyncMock(
        return_value=DegradationResponse(
            reason=DegradationReason.STALE_TOKEN, user_message="fake reconnect"
        )
    )
    assert await _gather_activity(router) == {"github_activity_source_failed": True}


@pytest.mark.asyncio
async def test_a_bound_binding_with_a_missing_grant_is_a_failed_read():
    from services.mcp.consumer.github_adapter import GitHubCredential

    router = _activity_router(headers=None, api=AsyncMock(return_value=[_recent_issue()]))
    router.mcp_adapter.resolve_credential = AsyncMock(
        return_value=GitHubCredential(
            owner_id=UID, mcp_server_ref="github", token=None, leg="oauth"
        )
    )
    store = MagicMock()
    store.get = AsyncMock(return_value=None)
    with (
        patch("services.mcp.consumer.github_adapter.ConnectorGrantStore", return_value=store),
        patch(
            "services.mcp.consumer.github_adapter.AsyncSessionFactory.session_scope",
            new=_fake_scope,
        ),
    ):
        out = await _gather_activity(router)
    assert out == {"github_activity_source_failed": True}


@pytest.mark.asyncio
async def test_the_milestones_read_carries_the_stale_reason():
    from services.integrations.github.read_failed import GitHubReadFailed

    router = _milestones_router(headers=None, api=AsyncMock(return_value=[]))
    router.mcp_adapter.resolve_credential = AsyncMock(
        return_value=DegradationResponse(
            reason=DegradationReason.STALE_TOKEN, user_message="fake reconnect"
        )
    )
    with pytest.raises(GitHubReadFailed) as ei:
        await router.mcp_adapter.list_milestones("r", "o", user_id=UID)
    assert ei.value.reason is DegradationReason.STALE_TOKEN
    assert ei.value.detail != "no_credential"
    assert await _gather_milestones(router) == {"milestones_source_failed": True}


# ── The ACTIVITY handlers' read_failed (9c906e48e4): no_credential is not connected ──


def _activity_intent():
    from services.shared_types import IntentCategory

    intent = MagicMock()
    intent.category = IntentCategory.ANALYSIS
    intent.action = "analyze_commits"
    return intent


def test_a_never_connected_account_gets_the_not_connected_line_not_couldnt_check():
    from services.intent.intent_service import IntentService

    out = IntentService._activity_read_failed_result(
        {"read_failed": [{"error": "no_credential"}]},
        _activity_intent(),
        "your GitHub commits in o/r",
        "what changed in the code",
    )
    assert out.message.startswith("GitHub isn't connected yet. Connect it in Settings")
    assert "couldn't" not in out.message


def test_a_connected_accounts_failed_credential_says_couldnt_check():
    from services.intent.intent_service import IntentService

    out = IntentService._activity_read_failed_result(
        {"read_failed": [{"error": "stale_token"}]},
        _activity_intent(),
        "your GitHub commits in o/r",
        "what changed in the code",
    )
    assert out.message.startswith("I couldn't check your GitHub commits in o/r just now")
