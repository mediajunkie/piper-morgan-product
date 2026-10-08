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
from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import (
    GitHubCredential,
    GitHubIssuesResult,
    GitHubMCPSpatialAdapter,
    GitHubReadFailed,
)
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
    r._user_id = "u1"
    r.mcp_adapter = adapter
    r.spatial_github = None
    r._resolve_default_repo = AsyncMock(return_value=("o", "r"))
    return r


async def test_router_strict_propagates_the_resolver_degrade():
    """#1965 (b): the strict read goes through the connector; a degrade raises
    with the RESOLVER's reason (not one inferred from an HTTP status)."""
    a = _adapter(None)
    a.list_open_issues = AsyncMock(
        return_value=GitHubIssuesResult(
            degradation=DegradationResponse(
                reason=DegradationReason.CONNECT_REQUIRED, user_message="Connect GitHub."
            )
        )
    )
    with pytest.raises(GitHubReadFailed) as exc:
        await _router(a).get_open_issues(limit=5, strict=True)
    assert exc.value.reason is DegradationReason.CONNECT_REQUIRED


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
    adapter = _adapter(None)
    adapter.list_open_issues = AsyncMock(
        return_value=GitHubIssuesResult(
            degradation=DegradationResponse(
                reason=DegradationReason.UNREACHABLE, user_message="down"
            )
        )
    )
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
    a = _adapter(None)
    a.list_open_issues = AsyncMock(
        return_value=GitHubIssuesResult(
            degradation=DegradationResponse(
                reason=DegradationReason.STALE_TOKEN, user_message="Re-authorize."
            )
        )
    )
    router = _router(a)
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


# --- #1965 (b): the one credential resolver (Arch's ruling, PA's order) ------

_AD = "services.mcp.consumer.github_adapter"


class _Binding:
    def __init__(self, status, owner_id="u1", ref="github"):
        self.status, self.owner_id, self.mcp_server_ref = status, owner_id, ref


def _binding_store(binding):
    repo = MagicMock()
    repo.get = AsyncMock(return_value=binding)

    class _Scope:
        async def __aenter__(self):
            return MagicMock()

        async def __aexit__(self, *a):
            return False

    return (
        patch(f"{_AD}.ConnectorBindingRepository", return_value=repo),
        patch(f"{_AD}.AsyncSessionFactory.session_scope", return_value=_Scope()),
    )


async def _resolve(binding, pat):
    a = _adapter(None)
    p1, p2 = _binding_store(binding)
    with p1, p2, patch.object(GitHubMCPSpatialAdapter, "_user_pat", return_value=pat):
        return await a.resolve_credential("u1")


async def test_bound_binding_is_the_oauth_leg():
    v = await _resolve(_Binding("bound"), pat="ghp_user_own")
    assert isinstance(v, GitHubCredential) and v.leg == "oauth"
    assert v.token is None  # the grant is read lazily at connect, as before


async def test_pat_only_user_gets_the_pat_leg_not_connect_required():
    """PA's regression guard: a PAT-connected user with NO binding row."""
    v = await _resolve(None, pat="ghp_user_own")
    assert isinstance(v, GitHubCredential)
    assert (v.leg, v.token, v.mcp_server_ref) == ("pat", "ghp_user_own", "github")
    assert v.stale_oauth_reason is None


async def test_no_binding_no_pat_is_connect_required():
    v = await _resolve(None, pat=None)
    assert isinstance(v, DegradationResponse)
    assert v.reason is DegradationReason.CONNECT_REQUIRED


async def test_stale_oauth_plus_working_pat_serves_on_the_pat_and_reports_the_stale_leg():
    v = await _resolve(_Binding("stale"), pat="ghp_user_own")
    assert isinstance(v, GitHubCredential) and v.leg == "pat"
    assert v.stale_oauth_reason is DegradationReason.STALE_TOKEN


async def test_stale_oauth_without_pat_degrades_with_its_reason():
    v = await _resolve(_Binding("stale"), pat=None)
    assert isinstance(v, DegradationResponse)
    assert v.reason is DegradationReason.STALE_TOKEN


@pytest.mark.parametrize("uid", ["system", "", None])
def test_never_the_system_or_env_token_for_the_pat_leg(uid):
    with patch(
        "services.integrations.github.config_service.GitHubConfigService.get_authentication_token",
        return_value="ENV_SYSTEM_TOKEN",
    ):
        assert GitHubMCPSpatialAdapter._user_pat(uid) is None


async def test_pat_leg_rides_the_authorization_header():
    a = _adapter(None)
    seen = {}

    class _CM:
        async def __aenter__(self):
            return MagicMock()

        async def __aexit__(self, *x):
            return False

    def _connect(url, headers=None):
        seen["url"], seen["headers"] = url, headers
        return _CM()

    cred = GitHubCredential(owner_id="u1", mcp_server_ref="github", token="ghp_x", leg="pat")
    with (
        patch(f"{_AD}.MCPClient.connect_http", side_effect=_connect),
        patch(
            "services.connectors.server_ref_resolver.resolve_server_ref",
            return_value="http://ghmcp:8082/",
        ),
    ):
        async with a._mcp_client_ctx(cred):
            pass
    assert seen["headers"] == {"Authorization": "Bearer ghp_x"}
    assert seen["url"] == "http://ghmcp:8082/"


async def test_router_connector_read_normalizes_items_and_drops_prs():
    a = _adapter(None)
    a.list_open_issues = AsyncMock(
        return_value=GitHubIssuesResult(
            issues=[
                {
                    "number": 7,
                    "title": "Fix login",
                    "state": "open",
                    "html_url": "https://github.com/o/r/issues/7",
                    "labels": [{"name": "bug"}],
                    "assignees": [{"login": "alice"}],
                    "user": {"login": "bob"},
                    "updated_at": "2026-10-08T00:00:00Z",
                },
                {"number": 8, "title": "a PR", "state": "open", "pull_request": {}},
            ],
            total=2,
        )
    )
    out = await _router(a).get_open_issues(limit=5, strict=True)
    assert [i["number"] for i in out] == [7]
    assert out[0]["labels"] == ["bug"] and out[0]["assignees"] == ["alice"]
    assert out[0]["uri"] == "https://github.com/o/r/issues/7"
    assert a.list_open_issues.await_args.kwargs["repository"] == "o/r"
