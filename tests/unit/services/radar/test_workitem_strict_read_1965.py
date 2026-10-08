"""#1965 — the Radar/standup GitHub work-items read must tell FAILED from EMPTY.

Before: ``GitHubMCPSpatialAdapter._call_github_api`` returned ``None`` on no
session / 401 / 403 / any non-200 / any exception, ``list_github_issues_direct``
turned that into ``[]``, and ``WorkItemProvider.gather_for_user`` recorded
VERIFIED_EMPTY — so #1587/#1889's "I couldn't reach your GitHub work items"
disclosure could never fire for a real GitHub failure (including an
OAuth-connected user whose adapter has no token at all).

After: a ``strict=True`` read raises ``GitHubReadFailed``; the work-items gather
uses it; every other caller keeps the lenient ``None`` / ``[]`` contract.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations.github.github_integration_router import GitHubIntegrationRouter
from services.mcp.consumer.connector import DegradationReason
from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter, GitHubReadFailed
from services.radar.feed_factory import WorkItemProvider, WorkItemReadKind
from services.radar.sources import EntitySourceReadFailed, WorkItemEntitySource

SVC = "services.integrations.integration_status_service.IntegrationStatusService"
HANDLE_READER = "services.integrations.github.repo_resolver.read_user_github_handle"


class _Resp:
    def __init__(self, status, payload):
        self.status = status
        self._payload = payload

    async def json(self):
        return self._payload

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False


class _Session:
    def __init__(self, status=200, payload=None, boom=False):
        self._status, self._payload, self._boom = status, payload, boom

    def get(self, url, params=None):
        if self._boom:
            raise OSError("connection reset")
        return _Resp(self._status, self._payload)


def _adapter(session=None):
    a = GitHubMCPSpatialAdapter.__new__(GitHubMCPSpatialAdapter)
    a._github_api_base = "https://api.github.com"
    a._session = session
    a.token_counter = MagicMock()

    async def _wrap(name, coro, input_data=None):
        return await coro

    a.token_counter.wrap_mcp_call = _wrap
    a._store_github_context = AsyncMock()
    return a


_ISSUE = {"number": 1, "title": "t", "state": "open", "labels": [], "assignees": [], "user": {}}


# --- adapter ---------------------------------------------------------------


@pytest.mark.parametrize(
    "session",
    [None, _Session(status=401), _Session(status=404), _Session(status=500), _Session(boom=True)],
    ids=["no-session", "401", "404", "500", "transport"],
)
async def test_strict_list_raises_on_every_failure(session):
    with pytest.raises(GitHubReadFailed):
        await _adapter(session).list_github_issues_direct("r", "o", strict=True)


@pytest.mark.parametrize(
    "session",
    [None, _Session(status=401), _Session(status=404), _Session(boom=True)],
    ids=["no-session", "401", "404", "transport"],
)
async def test_lenient_list_is_unchanged_empty_on_failure(session):
    assert await _adapter(session).list_github_issues_direct("r", "o") == []


async def test_strict_list_returns_issues_on_200():
    out = await _adapter(_Session(payload=[_ISSUE])).list_github_issues_direct(
        "r", "o", strict=True
    )
    assert [i["number"] for i in out] == [1]


async def test_strict_empty_array_is_empty_not_failure():
    assert (
        await _adapter(_Session(payload=[])).list_github_issues_direct("r", "o", strict=True) == []
    )


async def test_strict_non_array_payload_raises():
    with pytest.raises(GitHubReadFailed):
        await _adapter(_Session(payload={"message": "x"})).list_github_issues_direct(
            "r", "o", strict=True
        )


# --- router ----------------------------------------------------------------


def _router(adapter):
    r = GitHubIntegrationRouter.__new__(GitHubIntegrationRouter)
    r._initialized = True
    r.mcp_adapter = adapter
    r.spatial_github = None
    r._resolve_default_repo = AsyncMock(return_value=("o", "r"))
    return r


async def test_router_strict_propagates_failure():
    with pytest.raises(GitHubReadFailed):
        await _router(_adapter(None)).get_open_issues(limit=5, strict=True)


async def test_router_lenient_still_empty_on_failure():
    assert await _router(_adapter(None)).get_open_issues(limit=5) == []


async def test_router_strict_unresolved_repo_is_empty_not_failure():
    r = _router(_adapter(None))
    r._resolve_default_repo = AsyncMock(return_value=None)
    assert await r.get_open_issues(limit=5, strict=True) == []


# --- provider (the #1587 three-valued read) --------------------------------


async def test_provider_asks_for_the_strict_read():
    router = MagicMock()
    router.initialize = AsyncMock()
    router.get_open_issues = AsyncMock(return_value=[])
    router.close = AsyncMock()
    with (
        patch(f"{SVC}.is_configured", AsyncMock(return_value=True)),
        patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ),
        patch(HANDLE_READER, AsyncMock(return_value=None)),
    ):
        await WorkItemProvider().gather_for_user("u1")
    assert router.get_open_issues.await_args.kwargs.get("strict") is True


async def test_provider_end_to_end_no_token_is_source_failed_not_empty():
    """The alpha shape: GitHub reported configured (binding-first #1547) but the
    router's adapter has no usable token. Real router + real adapter code path;
    only the status check, initialize and repo resolution are stubbed."""
    adapter = _adapter(None)  # no session == no token configured
    router = _router(adapter)
    router.initialize = AsyncMock()
    router.close = AsyncMock()
    with (
        patch(f"{SVC}.is_configured", AsyncMock(return_value=True)),
        patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ),
        patch(HANDLE_READER, AsyncMock(return_value=None)),
    ):
        outcome = await WorkItemProvider().gather_for_user("u1")
    assert outcome.kind is WorkItemReadKind.SOURCE_FAILED


# --- Arch's ruling: the failure carries the connector DegradationReason -------


@pytest.mark.parametrize(
    "session,reason",
    [
        (_Session(status=401), DegradationReason.STALE_TOKEN),
        (_Session(status=404), DegradationReason.RESOURCE_NOT_FOUND),
        (_Session(status=500), DegradationReason.UNREACHABLE),
        (_Session(status=403), DegradationReason.UNREACHABLE),
        (_Session(boom=True), DegradationReason.UNREACHABLE),
        # CXO's rule: no session is NOT "not connected" on this path before (b).
        (None, None),
    ],
    ids=["401", "404", "500", "403", "transport", "no-session-unclassified"],
)
async def test_strict_failure_carries_the_reason(session, reason):
    with pytest.raises(GitHubReadFailed) as exc:
        await _adapter(session).list_github_issues_direct("r", "o", strict=True)
    assert exc.value.reason is reason


async def test_reason_reaches_the_outcome_and_the_source_error():
    router = _router(_adapter(_Session(status=401)))
    router.initialize = AsyncMock()
    router.close = AsyncMock()
    with (
        patch(f"{SVC}.is_configured", AsyncMock(return_value=True)),
        patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ),
        patch(HANDLE_READER, AsyncMock(return_value=None)),
    ):
        provider = WorkItemProvider()
        outcome = await provider.gather_for_user("u1")
        assert outcome.kind is WorkItemReadKind.SOURCE_FAILED
        assert outcome.reason is DegradationReason.STALE_TOKEN
        with pytest.raises(EntitySourceReadFailed) as exc:
            await WorkItemEntitySource(provider).fetch("u1")
    assert exc.value.reason is DegradationReason.STALE_TOKEN
