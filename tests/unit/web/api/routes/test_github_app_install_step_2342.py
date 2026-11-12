"""#2342 requirement 2 (ADR-081 D3): the install step.

A person who has authorized the GitHub App but installed it on no repository gets a
named state and CXO's words (2026-11-11 19:08; connector line 2026-11-12 07:19), never an
empty list. CXO's conditions: a working install link, a Refresh that really re-reads,
and the line never shown once a repository is installed. A failed installation read is
never reported as "not installed".

Layer: unit (the installation read against a fake HTTP session, the adapter, the route
function called directly, and the template's source). Nothing here calls GitHub, and no
page is rendered in a browser.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from services.integrations.github.repo_resolver import UnresolvedRepoError
from services.mcp.consumer import github_adapter as gh_mod
from services.mcp.consumer import github_app_grant as grant_mod
from services.mcp.consumer import github_app_install as install_mod
from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import GitHubCredential, GitHubMCPSpatialAdapter
from services.mcp.consumer.github_app_install import (
    DETAIL_APP_NOT_INSTALLED,
    InstallationReadFailed,
    InstalledRepositories,
)
from web.api.routes import settings_integrations as routes

_OWNER = "11111111-1111-1111-1111-111111111111"
_TEMPLATE = Path(__file__).resolve().parents[5] / "templates" / "settings_github.html"


@pytest.fixture
def app_on(monkeypatch):
    monkeypatch.setenv(grant_mod.ENV_APP_CLIENT_ID, "app-client-id")
    monkeypatch.setenv(grant_mod.ENV_APP_CLIENT_SECRET, "app-client-secret")
    monkeypatch.setenv(grant_mod.ENV_APP_SLUG, "piper-example")


@pytest.fixture
def app_off(monkeypatch):
    for name in (grant_mod.ENV_APP_CLIENT_ID, grant_mod.ENV_APP_CLIENT_SECRET):
        monkeypatch.delenv(name, raising=False)


# ── the installation read ───────────────────────────────────────────────────────────


class _Resp:
    def __init__(self, status, body):
        self.status, self._body = status, body

    async def json(self, content_type=None):
        return self._body

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False


class _HTTP:
    """Stands in for ``aiohttp.ClientSession``; answers by URL and page."""

    def __init__(self, routes_, raise_on=None):
        self.routes, self.calls, self.raise_on = routes_, [], raise_on

    def __call__(self, *a, **k):
        return self

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    def get(self, url, headers=None, params=None):
        self.calls.append((url, dict(params or {}), dict(headers or {})))
        if self.raise_on and self.raise_on in url:
            raise ConnectionResetError()
        key = (url.split("api.github.com")[1], (params or {}).get("page", 1))
        return self.routes[key]


def _repo(n, owner="octo"):
    return {"id": n, "name": f"r{n}", "full_name": f"{owner}/r{n}", "description": None}


@pytest.mark.asyncio
class TestInstallationRead:
    async def _read(self, monkeypatch, http, **kwargs):
        monkeypatch.setattr(install_mod.aiohttp, "ClientSession", http)
        return await install_mod.list_installed_repositories("bearer-value", **kwargs)

    async def test_no_installation_is_installed_nowhere(self, monkeypatch):
        http = _HTTP(
            {("/user/installations", 1): _Resp(200, {"total_count": 0, "installations": []})}
        )
        result = await self._read(monkeypatch, http)
        assert result.installations == 0 and result.installed_nowhere
        assert http.calls[0][2]["Authorization"] == "Bearer bearer-value"

    async def test_an_installation_covering_no_repository_is_installed_nowhere(self, monkeypatch):
        http = _HTTP(
            {
                ("/user/installations", 1): _Resp(200, {"installations": [{"id": 7}]}),
                ("/user/installations/7/repositories", 1): _Resp(200, {"repositories": []}),
            }
        )
        result = await self._read(monkeypatch, http)
        assert result.installations == 1 and result.installed_nowhere

    async def test_repositories_across_installations_are_normalized_and_deduplicated(
        self, monkeypatch
    ):
        http = _HTTP(
            {
                ("/user/installations", 1): _Resp(200, {"installations": [{"id": 7}, {"id": 8}]}),
                ("/user/installations/7/repositories", 1): _Resp(
                    200, {"repositories": [_repo(1), _repo(2)]}
                ),
                ("/user/installations/8/repositories", 1): _Resp(
                    200, {"repositories": [_repo(2), _repo(3, "org")]}
                ),
            }
        )
        result = await self._read(monkeypatch, http)
        assert [r["full_name"] for r in result.repositories] == ["octo/r1", "octo/r2", "org/r3"]
        assert result.repositories[0] == {
            "id": 1,
            "name": "r1",
            "full_name": "octo/r1",
            "description": "",
        }
        assert not result.installed_nowhere

    async def test_a_second_page_is_read(self, monkeypatch):
        first = [_repo(n) for n in range(100)]
        http = _HTTP(
            {
                ("/user/installations", 1): _Resp(200, {"installations": [{"id": 7}]}),
                ("/user/installations/7/repositories", 1): _Resp(200, {"repositories": first}),
                ("/user/installations/7/repositories", 2): _Resp(
                    200, {"repositories": [_repo(100)]}
                ),
            }
        )
        result = await self._read(monkeypatch, http)
        assert len(result.repositories) == 101  # pagination is followed to the end

    async def test_the_installation_listing_is_paginated_too(self, monkeypatch):
        first = [{"id": n} for n in range(100)]
        routes_ = {
            ("/user/installations", 1): _Resp(200, {"installations": first}),
            ("/user/installations", 2): _Resp(200, {"installations": [{"id": 100}]}),
        }
        for n in range(101):
            routes_[(f"/user/installations/{n}/repositories", 1)] = _Resp(
                200, {"repositories": [_repo(n)]}
            )
        result = await self._read(monkeypatch, _HTTP(routes_))
        assert result.installations == 101 and len(result.repositories) == 101

    async def test_a_partial_read_is_a_failed_read(self, monkeypatch):
        # Arch 2026-11-12 07:35: never part of a list as if it were complete.
        http = _HTTP(
            {
                ("/user/installations", 1): _Resp(200, {"installations": [{"id": 7}, {"id": 8}]}),
                ("/user/installations/7/repositories", 1): _Resp(200, {"repositories": [_repo(1)]}),
                ("/user/installations/8/repositories", 1): _Resp(502, {}),
            }
        )
        with pytest.raises(InstallationReadFailed):
            await self._read(monkeypatch, http)

    async def test_an_installation_without_an_id_fails_the_read(self, monkeypatch):
        http = _HTTP({("/user/installations", 1): _Resp(200, {"installations": [{"slug": "x"}]})})
        with pytest.raises(InstallationReadFailed):
            await self._read(monkeypatch, http)

    @pytest.mark.parametrize("status", [401, 403, 404, 500, 502])
    async def test_a_refused_read_raises_and_is_never_not_installed(self, monkeypatch, status):
        http = _HTTP({("/user/installations", 1): _Resp(status, {"message": "no"})})
        with pytest.raises(InstallationReadFailed) as exc:
            await self._read(monkeypatch, http)
        assert exc.value.status == status

    async def test_a_failure_on_the_repository_read_raises_too(self, monkeypatch):
        http = _HTTP(
            {
                ("/user/installations", 1): _Resp(200, {"installations": [{"id": 7}]}),
                ("/user/installations/7/repositories", 1): _Resp(503, {}),
            }
        )
        with pytest.raises(InstallationReadFailed):
            await self._read(monkeypatch, http)

    async def test_a_connection_failure_raises(self, monkeypatch):
        http = _HTTP({}, raise_on="/user/installations")
        with pytest.raises(InstallationReadFailed) as exc:
            await self._read(monkeypatch, http)
        assert "bearer-value" not in str(exc.value)


# ── the adapter ─────────────────────────────────────────────────────────────────────


def _oauth():
    return GitHubCredential(
        owner_id=_OWNER, mcp_server_ref="github", token="access-live", leg="oauth"
    )


@pytest.mark.asyncio
class TestAdapterInstalledRepositories:
    async def test_outside_app_mode_the_question_does_not_apply(self, app_off):
        adapter = GitHubMCPSpatialAdapter()
        adapter.resolve_credential = AsyncMock(side_effect=AssertionError("not consulted"))
        assert await adapter.app_installed_repositories(_OWNER) is None

    @pytest.mark.parametrize(
        "credential",
        [
            GitHubCredential(owner_id=_OWNER, mcp_server_ref="github", token="pat", leg="pat"),
            DegradationResponse(reason=DegradationReason.STALE_TOKEN, user_message="x"),
            DegradationResponse(reason=DegradationReason.CONNECT_REQUIRED, user_message="x"),
        ],
    )
    async def test_an_account_not_served_by_an_app_grant_is_not_asked(
        self, app_on, monkeypatch, credential
    ):
        adapter = GitHubMCPSpatialAdapter()
        adapter.resolve_credential = AsyncMock(return_value=credential)
        read = AsyncMock(side_effect=AssertionError("no installation read"))
        monkeypatch.setattr(gh_mod, "list_installed_repositories", read)
        assert await adapter.app_installed_repositories(_OWNER) is None

    async def test_the_app_grant_reads_installations_with_its_own_token(self, app_on, monkeypatch):
        adapter = GitHubMCPSpatialAdapter()
        adapter.resolve_credential = AsyncMock(return_value=_oauth())
        found = InstalledRepositories(installations=1, repositories=[_repo(1)])
        read = AsyncMock(return_value=found)
        monkeypatch.setattr(gh_mod, "list_installed_repositories", read)
        assert await adapter.app_installed_repositories(_OWNER) is found
        read.assert_awaited_once_with("access-live")


@pytest.mark.asyncio
class TestChatAsksToInstallNotWhichRepo:
    """CXO: when a GitHub turn needs a repository and the App is installed nowhere, the
    reply is the install line. If the read fails, "Which repo?" stays."""

    async def _unresolved(self, monkeypatch, adapter):
        monkeypatch.setattr(
            gh_mod, "resolve_repo", AsyncMock(side_effect=UnresolvedRepoError("none"))
        )
        return await adapter._resolve_or_degrade(_OWNER)

    async def test_installed_nowhere_gives_the_install_line(self, app_on, monkeypatch):
        adapter = GitHubMCPSpatialAdapter()
        adapter.app_installed_repositories = AsyncMock(
            return_value=InstalledRepositories(installations=0)
        )
        result = await self._unresolved(monkeypatch, adapter)
        assert result.reason is DegradationReason.REPO_UNRESOLVED
        assert result.detail == DETAIL_APP_NOT_INSTALLED
        assert result.user_message == gh_mod.GITHUB_APP_NOT_INSTALLED_REPLY
        assert gh_mod.github_degrade_reply(result) == gh_mod.GITHUB_APP_NOT_INSTALLED_REPLY
        assert (
            gh_mod.github_connector_reply(result) == gh_mod.GITHUB_CONNECTOR_APP_NOT_INSTALLED_REPLY
        )

    async def test_with_no_install_link_the_chat_line_says_it_is_on_our_side(
        self, app_on, monkeypatch
    ):
        monkeypatch.delenv(grant_mod.ENV_APP_SLUG)
        adapter = GitHubMCPSpatialAdapter()
        adapter.app_installed_repositories = AsyncMock(
            return_value=InstalledRepositories(installations=0)
        )
        result = await self._unresolved(monkeypatch, adapter)
        assert result.detail == install_mod.DETAIL_APP_INSTALL_LINK_MISSING
        assert result.user_message == (
            "You're connected to GitHub, but I can't point you to where the Piper GitHub "
            "app gets installed just now. This is on our side, so please tell us."
        )
        assert gh_mod.github_connector_reply(result) == result.user_message
        assert "Settings" not in result.user_message

    @pytest.mark.parametrize(
        "answer",
        [
            InstalledRepositories(installations=1, repositories=[_repo(1)]),
            None,  # not an App grant
            InstallationReadFailed(502),
            RuntimeError("anything else"),
        ],
    )
    async def test_otherwise_which_repo_stays(self, app_on, monkeypatch, answer):
        adapter = GitHubMCPSpatialAdapter()
        if isinstance(answer, Exception):
            adapter.app_installed_repositories = AsyncMock(side_effect=answer)
        else:
            adapter.app_installed_repositories = AsyncMock(return_value=answer)
        result = await self._unresolved(monkeypatch, adapter)
        assert result.reason is DegradationReason.REPO_UNRESOLVED and result.detail is None
        assert result.user_message.startswith("Which repo?")


@pytest.mark.asyncio
class TestAnEmptyUserWideReadIsNotNoIssues:
    """Requirement 2 on the user-wide reads (PA 07:31): the connector's GitHub resource
    and "my open issues" never resolve a repository, so for a person who installed the
    App nowhere an empty result must be the install step's state, not "no issues"."""

    @staticmethod
    def _adapter(monkeypatch, payload, installed):
        import contextlib

        adapter = GitHubMCPSpatialAdapter()
        adapter.resolve_credential = AsyncMock(return_value=_oauth())

        class _Client:
            async def call_tool(self, tool, args):
                return payload

        @contextlib.asynccontextmanager
        async def _ctx(binding):
            yield _Client()

        adapter._mcp_client_ctx = _ctx
        monkeypatch.setattr(GitHubMCPSpatialAdapter, "_tool_text", classmethod(lambda cls, r: r))
        if isinstance(installed, Exception):
            read = AsyncMock(side_effect=installed)
        else:
            read = AsyncMock(return_value=installed)
        monkeypatch.setattr(gh_mod, "list_installed_repositories", read)
        return adapter, read

    async def test_empty_and_installed_nowhere_is_the_install_state(self, app_on, monkeypatch):
        adapter, read = self._adapter(
            monkeypatch, '{"total_count":0,"items":[]}', InstalledRepositories(installations=0)
        )
        result = await adapter.list_open_issues(_OWNER)
        assert result.issues is None
        assert result.degradation.detail == DETAIL_APP_NOT_INSTALLED
        assert (
            gh_mod.github_connector_reply(result.degradation)
            == gh_mod.GITHUB_CONNECTOR_APP_NOT_INSTALLED_REPLY
        )
        read.assert_awaited_once_with("access-live")  # the credential already in hand

    async def test_empty_with_the_app_installed_somewhere_is_an_honest_empty(
        self, app_on, monkeypatch
    ):
        adapter, _ = self._adapter(
            monkeypatch,
            '{"total_count":0,"items":[]}',
            InstalledRepositories(installations=1, repositories=[_repo(1)]),
        )
        result = await adapter.list_open_issues(_OWNER)
        assert result.issues == [] and result.degradation is None

    async def test_empty_with_a_failed_installation_read_stays_an_empty_result(
        self, app_on, monkeypatch
    ):
        adapter, _ = self._adapter(
            monkeypatch, '{"total_count":0,"items":[]}', InstallationReadFailed(502)
        )
        result = await adapter.list_open_issues(_OWNER)
        assert result.issues == [] and result.degradation is None

    async def test_a_non_empty_result_never_asks_about_installations(self, app_on, monkeypatch):
        payload = '{"total_count":1,"items":[{"number":1,"title":"t","html_url":"u"}]}'
        adapter, read = self._adapter(monkeypatch, payload, AssertionError("no installation read"))
        result = await adapter.list_open_issues(_OWNER)
        assert result.degradation is None and len(result.issues) == 1
        read.assert_not_awaited()

    async def test_classic_mode_never_asks_about_installations(self, app_off, monkeypatch):
        adapter, read = self._adapter(
            monkeypatch, '{"total_count":0,"items":[]}', AssertionError("no installation read")
        )
        result = await adapter.list_open_issues(_OWNER)
        assert result.issues == [] and result.degradation is None
        read.assert_not_awaited()

    async def test_a_personal_token_never_asks_about_installations(self, app_on, monkeypatch):
        adapter, read = self._adapter(
            monkeypatch, '{"total_count":0,"items":[]}', AssertionError("no installation read")
        )
        adapter.resolve_credential = AsyncMock(
            return_value=GitHubCredential(
                owner_id=_OWNER, mcp_server_ref="github", token="pat", leg="pat"
            )
        )
        result = await adapter.list_open_issues(_OWNER)
        assert result.issues == [] and result.degradation is None
        read.assert_not_awaited()


_EMPTY = '{"total_count":0,"items":[]}'
_USER_WIDE_READS = {
    "issues": (lambda a: a.list_open_issues(_OWNER), lambda r: r.issues),
    "pull requests": (lambda a: a.list_open_prs(_OWNER), lambda r: r.issues),
    "repositories": (lambda a: a.search_user_repositories(_OWNER), lambda r: r.repositories),
}


@pytest.mark.asyncio
@pytest.mark.parametrize("read_name", sorted(_USER_WIDE_READS))
class TestEachUserWideReadInEachOutcome:
    """Arch 2026-11-12 07:48: the three reads that resolve no repository (``assignee:@me``
    issues, ``author:@me`` pull requests, ``user:@me`` repositories), each in the three
    outcomes of the installation read that an empty result triggers."""

    async def _run(self, monkeypatch, read_name, installed):
        adapter, read = TestAnEmptyUserWideReadIsNotNoIssues._adapter(
            monkeypatch, _EMPTY, installed
        )
        call, items = _USER_WIDE_READS[read_name]
        result = await call(adapter)
        return result, items(result), read

    async def test_installed_nowhere_degrades_with_the_install_detail(
        self, app_on, monkeypatch, read_name
    ):
        result, items, _ = await self._run(
            monkeypatch, read_name, InstalledRepositories(installations=0)
        )
        assert items is None
        assert result.degradation.reason is DegradationReason.REPO_UNRESOLVED
        assert result.degradation.detail == DETAIL_APP_NOT_INSTALLED

    async def test_installed_nowhere_with_no_slug_degrades_with_the_link_missing_detail(
        self, app_on, monkeypatch, read_name
    ):
        monkeypatch.delenv(grant_mod.ENV_APP_SLUG)
        result, items, _ = await self._run(
            monkeypatch, read_name, InstalledRepositories(installations=0)
        )
        assert items is None
        assert result.degradation.detail == install_mod.DETAIL_APP_INSTALL_LINK_MISSING

    async def test_installed_somewhere_the_empty_result_is_true(
        self, app_on, monkeypatch, read_name
    ):
        result, items, read = await self._run(
            monkeypatch,
            read_name,
            InstalledRepositories(installations=1, repositories=[_repo(1)]),
        )
        assert items == [] and result.degradation is None
        read.assert_awaited_once()

    async def test_a_failed_installation_read_leaves_the_empty_result(
        self, app_on, monkeypatch, read_name
    ):
        result, items, _ = await self._run(monkeypatch, read_name, InstallationReadFailed(503))
        assert items == [] and result.degradation is None


@pytest.mark.asyncio
class TestConnectorResourceEndToEnd:
    """Arch 07:48, PA 07:44: through ``_read_github_issues``, the connector's only GitHub
    surface, a person who installed the App nowhere reads CXO's connector install line."""

    async def _payload(self, monkeypatch, installed):
        import json as _json

        from services.mcp.server import resources

        adapter, _ = TestAnEmptyUserWideReadIsNotNoIssues._adapter(monkeypatch, _EMPTY, installed)
        monkeypatch.setattr(resources, "GitHubMCPSpatialAdapter", lambda: adapter)
        monkeypatch.setattr(resources, "current_user_id", lambda: _OWNER)
        return _json.loads(await resources._read_github_issues())

    async def test_installed_nowhere_reads_the_connector_install_line(self, app_on, monkeypatch):
        payload = await self._payload(monkeypatch, InstalledRepositories(installations=0))
        assert payload["available"] is False
        assert payload["message"] == gh_mod.GITHUB_CONNECTOR_APP_NOT_INSTALLED_REPLY
        assert "in the Piper Morgan app" in payload["message"]

    async def test_no_slug_reads_the_on_our_side_line(self, app_on, monkeypatch):
        monkeypatch.delenv(grant_mod.ENV_APP_SLUG)
        payload = await self._payload(monkeypatch, InstalledRepositories(installations=0))
        assert payload["message"] == gh_mod.GITHUB_APP_INSTALL_LINK_MISSING_REPLY

    async def test_installed_somewhere_reads_an_honest_empty_list(self, app_on, monkeypatch):
        payload = await self._payload(
            monkeypatch, InstalledRepositories(installations=1, repositories=[_repo(1)])
        )
        assert payload["available"] is True and payload["issues"] == [] and payload["total"] == 0

    async def test_a_failed_installation_read_reads_the_empty_list_as_today(
        self, app_on, monkeypatch
    ):
        payload = await self._payload(monkeypatch, InstallationReadFailed(None, "timeout"))
        assert payload["available"] is True and payload["issues"] == []


class TestRepliesArePickedByDetail:
    """Arch 2026-11-12 07:35: ``detail`` is a closed set of named constants and every
    surface picks its line by it, never by reading a message."""

    @pytest.mark.parametrize(
        "detail,web,connector",
        [
            (
                install_mod.DETAIL_APP_NOT_INSTALLED,
                gh_mod.GITHUB_APP_NOT_INSTALLED_REPLY,
                gh_mod.GITHUB_CONNECTOR_APP_NOT_INSTALLED_REPLY,
            ),
            (
                install_mod.DETAIL_APP_INSTALL_LINK_MISSING,
                gh_mod.GITHUB_APP_INSTALL_LINK_MISSING_REPLY,
                gh_mod.GITHUB_APP_INSTALL_LINK_MISSING_REPLY,
            ),
        ],
    )
    def test_each_install_detail_picks_its_line_whatever_the_message_says(
        self, detail, web, connector
    ):
        degraded = DegradationResponse(
            reason=DegradationReason.REPO_UNRESOLVED,
            user_message="a message nobody should read the state from",
            detail=detail,
        )
        assert gh_mod.github_degrade_reply(degraded) == web
        assert gh_mod.github_connector_reply(degraded) == connector

    def test_the_details_are_three_named_constants(self):
        assert {
            grant_mod.REASON_CUTOVER,
            install_mod.DETAIL_APP_NOT_INSTALLED,
            install_mod.DETAIL_APP_INSTALL_LINK_MISSING,
        } == {"cutover", "app_not_installed", "app_install_link_missing"}

    def test_the_install_line_is_not_a_clarifying_question(self):
        # The get-issue handler arms a "which repo?" follow-up on REPO_UNRESOLVED; the
        # install step's statement must not arm it. A source pin: no handler-level
        # fixture exists for that branch.
        source = (
            Path(__file__).resolve().parents[5] / "services" / "intent" / "intent_service.py"
        ).read_text(encoding="utf-8")
        branch = source[
            source.index("requires_clarification=(\n                        connector_result") :
        ]
        assert 'and not getattr(_deg, "detail", None)' in branch[:500]


class TestInstallCopy:
    """CXO's words, exactly."""

    def test_the_card_line(self):
        assert gh_mod.GITHUB_APP_NOT_INSTALLED_CARD_LINE == (
            "GitHub is connected, but the Piper GitHub app isn't installed on any of your "
            "repositories yet, so I can't see any. Install it on the ones you want me to "
            "use, then refresh this list."
        )

    def test_the_chat_line(self):
        assert gh_mod.GITHUB_APP_NOT_INSTALLED_REPLY == (
            "You're connected to GitHub, but the Piper GitHub app isn't installed on any of "
            "your repositories yet, so there's nothing for me to read. Install it on the "
            "ones you want in Settings, under Integrations."
        )

    def test_the_connector_line_names_the_piper_morgan_app(self):
        assert gh_mod.GITHUB_CONNECTOR_APP_NOT_INSTALLED_REPLY == (
            "You're connected to GitHub, but the Piper GitHub app isn't installed on any of "
            "your repositories yet, so there's nothing for me to read. Install it on the "
            "ones you want in the Piper Morgan app, in Settings under Integrations."
        )


# ── the Settings route ──────────────────────────────────────────────────────────────


def _user():
    user = MagicMock()
    user.sub = _OWNER
    return user


def _adapter_class(installed=None, error=None):
    instance = MagicMock()
    if error is not None:
        instance.app_installed_repositories = AsyncMock(side_effect=error)
    else:
        instance.app_installed_repositories = AsyncMock(return_value=installed)
    instance.search_user_repositories = AsyncMock(
        side_effect=AssertionError("the user:@me search must not run")
    )
    return MagicMock(return_value=instance), instance


_ADAPTER = "web.api.routes.settings_integrations.GitHubMCPSpatialAdapter"
_PREFS = "web.api.routes.settings_integrations._load_github_prefs_db"


@pytest.mark.asyncio
class TestSettingsRepositoryList:
    async def test_installed_nowhere_is_a_named_state_with_the_install_link(self, app_on):
        cls, _ = _adapter_class(InstalledRepositories(installations=0))
        with patch(_ADAPTER, cls):
            result = await routes.get_github_repositories(current_user=_user())
        assert result.repositories == []
        assert result.state == "app_not_installed"
        assert result.message == gh_mod.GITHUB_APP_NOT_INSTALLED_CARD_LINE
        assert result.install_url == "https://github.com/apps/piper-example/installations/new"

    async def test_without_a_slug_the_card_says_it_is_on_our_side_and_never_install_it(
        self, app_on, monkeypatch
    ):
        # CXO 2026-11-12 07:30: never "install it" with no way to.
        monkeypatch.delenv(grant_mod.ENV_APP_SLUG)
        cls, _ = _adapter_class(InstalledRepositories(installations=0))
        with patch(_ADAPTER, cls):
            result = await routes.get_github_repositories(current_user=_user())
        assert result.state == "app_not_installed" and result.install_url is None
        assert result.message == (
            "GitHub is connected, but I can't show you where to install the Piper GitHub "
            "app just now. This is on our side, so please tell us."
        )
        assert "GITHUB_APP_SLUG" not in result.message and "Install it" not in result.message

    async def test_installed_somewhere_is_an_ordinary_list_and_the_line_never_shows(self, app_on):
        installed = InstalledRepositories(
            installations=1,
            repositories=[
                {"id": 1, "name": "r1", "full_name": "octo/r1", "description": ""},
                {"id": 2, "name": "r2", "full_name": "octo/r2", "description": "two"},
            ],
        )
        cls, instance = _adapter_class(installed)
        saved = {"selected_repositories": ["octo/r2", "octo/not-installed-any-more"]}
        with patch(_ADAPTER, cls), patch(_PREFS, new=AsyncMock(return_value=saved)):
            result = await routes.get_github_repositories(current_user=_user())
        assert result.state is None and result.message is None
        assert result.note == (
            "These are the repositories the Piper GitHub app is installed on. To add "
            "another, install the app on it."
        )  # CXO 07:30: only under a non-empty list in App mode
        assert [(r.full_name, r.selected) for r in result.repositories] == [
            ("octo/r1", False),
            ("octo/r2", True),
        ]  # a saved choice the App isn't installed on simply doesn't appear (Arch)
        instance.search_user_repositories.assert_not_awaited()

    @pytest.mark.parametrize("error", [InstallationReadFailed(502), RuntimeError("boom")])
    async def test_a_failed_read_is_an_honest_error_never_the_install_line(self, app_on, error):
        cls, _ = _adapter_class(error=error)
        with patch(_ADAPTER, cls):
            with pytest.raises(HTTPException) as exc:
                await routes.get_github_repositories(current_user=_user())
        assert exc.value.status_code == 502
        assert "installed" not in str(exc.value.detail)

    async def test_an_account_not_on_an_app_grant_keeps_the_search(self, app_on):
        from services.mcp.consumer.github_adapter import GitHubReposResult

        cls, instance = _adapter_class(None)
        instance.search_user_repositories = AsyncMock(
            return_value=GitHubReposResult(
                repositories=[{"id": 9, "name": "p", "full_name": "me/p", "description": ""}]
            )
        )
        with patch(_ADAPTER, cls), patch(_PREFS, new=AsyncMock(return_value={})):
            result = await routes.get_github_repositories(current_user=_user())
        assert [r.full_name for r in result.repositories] == ["me/p"] and result.state is None
        assert result.note is None  # the search path's list carries no App note

    async def test_with_app_mode_off_the_installation_read_is_never_made(self, app_off):
        from services.mcp.consumer.github_adapter import GitHubReposResult

        cls, instance = _adapter_class(error=AssertionError("must not be called"))
        instance.search_user_repositories = AsyncMock(
            return_value=GitHubReposResult(repositories=[])
        )
        with patch(_ADAPTER, cls), patch(_PREFS, new=AsyncMock(return_value={})):
            result = await routes.get_github_repositories(current_user=_user())
        assert result.state is None
        instance.app_installed_repositories.assert_not_awaited()


# ── the card ────────────────────────────────────────────────────────────────────────


class TestCardSource:
    """A source read of the template, not a render. CXO's conditions on the card: an
    install link, a Refresh that calls the same load, and no Save over the kept choices
    from an empty list."""

    def _source(self) -> str:
        return _TEMPLATE.read_text(encoding="utf-8")

    def test_the_named_state_is_handled_before_the_list_is_rendered(self):
        source = self._source()
        state = source.index("data.state === 'app_not_installed'")
        assert state < source.index("renderRepositoryList(loadedRepositories);", state)
        assert "showAppNotInstalled(listEl, data.message, data.install_url)" in source

    def test_the_line_is_set_as_text_and_the_link_is_the_servers_url(self):
        source = self._source()
        assert "text.textContent = line;" in source
        assert "install.href = installUrl;" in source and "if (installUrl) {" in source

    def test_the_buttons_carry_cxos_labels(self):
        source = self._source()
        assert "install.textContent = 'Install on GitHub';" in source
        assert "refresh.textContent = 'Refresh';" in source

    def test_the_list_note_shows_only_under_a_non_empty_list(self):
        source = self._source()
        assert "if (data.note && loadedRepositories.length > 0) {" in source
        assert "note.textContent = data.note;" in source

    def test_refresh_really_re_reads(self):
        assert "refresh.addEventListener('click', () => loadRepositoryList());" in self._source()

    def test_nothing_is_saved_from_the_not_installed_state(self):
        source = self._source()
        assert "if (appNotInstalled) return;" in source
        shown = source.index("function showAppNotInstalled")
        assert (
            "btn.disabled = true;"
            in source[shown : source.index("async function loadRepositoryList")]
        )
