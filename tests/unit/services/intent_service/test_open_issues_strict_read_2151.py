"""#2151 GH-NONSTRICT (Arch 10-23 21:28): the open-issues and blocked-items gathers' read is strict.

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
