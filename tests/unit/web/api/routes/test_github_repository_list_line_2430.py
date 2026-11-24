"""Issue 2430: the GitHub settings page's repository list says CXO's reconnect line for a
stale grant, instead of "Try refreshing the page".

CXO's words (mail 01M878T7RJ); Arch's mechanism (mail 01M8786G87): a separate picker,
``github_degrade_fixed_line``, whose every ``return`` is an UPPER_CASE constant or None;
the 502 site raises it user-facing when it names a line; the guard of issue 2428 holds
the picker on a closed list and reads its body (tests for that live in
``tests/unit/web/test_setup_lines_reach_the_page_2428.py``).

LAYER: the route mounted on a small app with the app's REAL ``HTTPException`` handler
(taken from ``web.app``), the connector result stubbed, the signed-in user overridden;
the client's JSON is read. The adapter's list read with the installation read faked (no
network). The page's script is read as source; nothing is rendered here.
DENOMINATOR: every ``DegradationReason`` crossed with no detail and each of the five
named ``detail`` constants (42 cases) for the picker-against-chat pin.
NOT COVERED: a render of the page (CXO reads two local renders, on the issue).
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from services.auth.auth_middleware import get_current_user
from services.mcp.consumer import github_adapter as gh_mod
from services.mcp.consumer import github_app_grant as grant_mod
from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import (
    GITHUB_REPOSITORY_LIST_RECONNECT_LINE,
    GitHubCredential,
    GitHubMCPSpatialAdapter,
    GitHubReposResult,
    github_degrade_fixed_line,
    github_degrade_reply,
)
from services.mcp.consumer.github_app_grant import REASON_CUTOVER
from services.mcp.consumer.github_app_install import (
    DETAIL_APP_INSTALL_LINK_MISSING,
    DETAIL_APP_NOT_INSTALLED,
    DETAIL_APP_NOT_ON_REPOSITORY,
    DETAIL_APP_TOO_MANY_REPOSITORIES,
    InstalledRepositories,
)
from web.api.routes import settings_integrations as routes

ROOT = Path(__file__).resolve().parents[5]
TEMPLATE = ROOT / "templates" / "settings_github.html"
GENERIC = "Something went wrong on my end. I've logged the details for debugging."
CXO_RECONNECT = (
    "GitHub needs reconnecting, so I can't load your repositories. Use Reconnect with "
    "GitHub on this page."
)
_ADAPTER = "web.api.routes.settings_integrations.GitHubMCPSpatialAdapter"
_OWNER = "11111111-1111-1111-1111-111111111111"


def _real_handler():
    from web.app import app as real_app  # the handler is registered on the module-level app

    return real_app.exception_handlers[HTTPException]


def _get_list(degradation):
    instance = MagicMock()
    instance.search_user_repositories = AsyncMock(
        return_value=GitHubReposResult(degradation=degradation)
    )
    app = FastAPI()
    app.add_exception_handler(HTTPException, _real_handler())
    app.include_router(routes.router)
    user = MagicMock()
    user.sub = _OWNER
    app.dependency_overrides[get_current_user] = lambda: user
    with patch(_ADAPTER, MagicMock(return_value=instance)):
        return TestClient(app).get("/api/v1/settings/integrations/github/repositories")


class TestTheLine:
    def test_the_constant_carries_cxos_words(self):
        assert GITHUB_REPOSITORY_LIST_RECONNECT_LINE == CXO_RECONNECT

    def test_the_too_many_line_was_not_built(self):
        names = [n for n in vars(gh_mod) if n.isupper() and "LIST" in n]
        assert not [n for n in names if "TOO_MANY" in n], names


class TestThroughTheRealHandler:
    @pytest.mark.parametrize("detail", [None, REASON_CUTOVER], ids=["plain", "cutover"])
    def test_a_stale_degrade_says_the_reconnect_line(self, detail):
        reply = _get_list(
            DegradationResponse(
                reason=DegradationReason.STALE_TOKEN,
                user_message="an open-text message nobody should read",
                detail=detail,
            )
        )
        assert reply.status_code == 502
        assert reply.json() == {"message": CXO_RECONNECT, "detail": CXO_RECONNECT}

    @pytest.mark.parametrize(
        "reason",
        [
            DegradationReason.UNREACHABLE,
            DegradationReason.MISCONFIGURED,
            DegradationReason.REPO_UNRESOLVED,
        ],
    )
    def test_an_unnamed_reason_says_the_generic_line(self, reason):
        reply = _get_list(DegradationResponse(reason=reason, user_message="msg: /srv/secret"))
        assert reply.status_code == 502
        assert reply.json() == {"message": GENERIC, "detail": GENERIC}
        assert "secret" not in reply.text


class TestTheListReadCannotSayTooMany:
    """The brief's question: can a repository-list read reach the 502 with
    ``DETAIL_APP_TOO_MANY_REPOSITORIES``? No. The list read on an App grant pages the
    installation read to the end and returns every repository; the too-many degrade is
    set in one place, ``_installed_search_queries``, which only the issue and pull-request
    searches call. Shown both ways: by behaviour, and by where the detail is set."""

    @staticmethod
    def _names(count):
        return [f"octo-org-with-a-long-name/repository-number-{i:04d}" for i in range(count)]

    @staticmethod
    def _adapter(monkeypatch, names):
        installed = InstalledRepositories(
            installations=1,
            repositories=[
                {"id": i, "name": n.split("/")[1], "full_name": n} for i, n in enumerate(names)
            ],
        )
        monkeypatch.setenv(grant_mod.ENV_APP_SLUG, "piper-example")
        monkeypatch.setattr(
            gh_mod, "list_installed_repositories", AsyncMock(return_value=installed)
        )
        credential = GitHubCredential(
            owner_id=_OWNER, mcp_server_ref="github", token="t", leg="oauth", app_grant=True
        )
        adapter = GitHubMCPSpatialAdapter()
        adapter._bound_binding_or_degrade = AsyncMock(return_value=credential)
        adapter.resolve_credential = AsyncMock(return_value=credential)
        return adapter

    async def test_a_set_too_large_to_search_is_listed_whole(self, monkeypatch):
        names = self._names(400)
        assert len(gh_mod._repo_qualifier_chunks(names)) > gh_mod._INSTALLED_SEARCH_MAX_QUERIES
        adapter = self._adapter(monkeypatch, names)

        listed = await adapter.search_user_repositories(_OWNER, limit=100)
        assert listed.degradation is None
        assert [r["full_name"] for r in listed.repositories] == names

        # Control: the same set does produce the reason on a search, so the size is real.
        searched = await adapter.list_open_issues(_OWNER)
        assert searched.degradation.detail == DETAIL_APP_TOO_MANY_REPOSITORIES

    def test_the_detail_is_set_only_by_the_search_path(self):
        tree = ast.parse((ROOT / "services/mcp/consumer/github_adapter.py").read_text())
        setters, callers = [], []
        for func in ast.walk(tree):
            if not isinstance(func, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for node in ast.walk(func):
                if (
                    isinstance(node, ast.keyword)
                    and node.arg == "detail"
                    and isinstance(node.value, ast.Name)
                    and node.value.id == "DETAIL_APP_TOO_MANY_REPOSITORIES"
                ):
                    setters.append(func.name)
                if (
                    isinstance(node, ast.Attribute)
                    and node.attr == "_installed_search_queries"
                    and isinstance(node.ctx, ast.Load)
                ):
                    callers.append(func.name)
        assert setters == ["_installed_search_queries"]
        assert callers == ["_search_via_connector"]
        list_read = next(
            f
            for f in ast.walk(tree)
            if isinstance(f, ast.AsyncFunctionDef) and f.name == "search_user_repositories"
        )
        assert "_search_via_connector" not in ast.unparse(list_read)


# What the chat function and the page's picker return, side by side, for every reason
# crossed with no detail and each named detail. A new branch in one without the other
# changes a row. "USER_MESSAGE" is the degrade's own open text (chat only).
_DETAILS = {
    None: "None",
    REASON_CUTOVER: "REASON_CUTOVER",
    DETAIL_APP_NOT_INSTALLED: "DETAIL_APP_NOT_INSTALLED",
    DETAIL_APP_INSTALL_LINK_MISSING: "DETAIL_APP_INSTALL_LINK_MISSING",
    DETAIL_APP_NOT_ON_REPOSITORY: "DETAIL_APP_NOT_ON_REPOSITORY",
    DETAIL_APP_TOO_MANY_REPOSITORIES: "DETAIL_APP_TOO_MANY_REPOSITORIES",
}
_BY_DETAIL = {
    "DETAIL_APP_NOT_INSTALLED": "GITHUB_APP_NOT_INSTALLED_REPLY",
    "DETAIL_APP_INSTALL_LINK_MISSING": "GITHUB_APP_INSTALL_LINK_MISSING_REPLY",
    "DETAIL_APP_NOT_ON_REPOSITORY": "GITHUB_APP_NOT_ON_REPOSITORY_REPLY",
    "DETAIL_APP_TOO_MANY_REPOSITORIES": "GITHUB_APP_TOO_MANY_REPOSITORIES_REPLY",
}
_TABLE = {}
for _reason in DegradationReason:
    for _detail_name in _DETAILS.values():
        _TABLE[(_reason.name, _detail_name)] = (_BY_DETAIL.get(_detail_name, "USER_MESSAGE"), None)
_TABLE[("STALE_TOKEN", "None")] = (
    "GITHUB_STALE_TOKEN_REPLY",
    "GITHUB_REPOSITORY_LIST_RECONNECT_LINE",
)
_TABLE[("STALE_TOKEN", "REASON_CUTOVER")] = (
    "GITHUB_CUTOVER_STALE_REPLY",
    "GITHUB_REPOSITORY_LIST_RECONNECT_LINE",
)


class TestThePickerBesideTheChatFunction:
    def test_the_table_covers_every_reason_and_detail(self):
        assert len(_TABLE) == len(DegradationReason) * len(_DETAILS) == 42

    @pytest.mark.parametrize("reason", list(DegradationReason), ids=lambda r: r.name)
    @pytest.mark.parametrize("detail", list(_DETAILS), ids=lambda d: _DETAILS[d])
    def test_both_functions_return_the_recorded_line(self, reason, detail):
        names = {v: k for k, v in vars(gh_mod).items() if k.isupper() and isinstance(v, str)}
        degraded = DegradationResponse(reason=reason, user_message="USER_MESSAGE", detail=detail)
        chat = github_degrade_reply(degraded)
        picked = github_degrade_fixed_line(degraded)
        got = (
            "USER_MESSAGE" if chat == "USER_MESSAGE" else names[chat],
            None if picked is None else names[picked],
        )
        assert got == _TABLE[(reason.name, _DETAILS[detail])]


class TestThePage:
    SOURCE = TEMPLATE.read_text(encoding="utf-8")

    def _function(self, name):
        start = self.SOURCE.index(f"async function {name}(")
        end = self.SOURCE.index("\n      }\n", start)
        return self.SOURCE[start:end]

    def test_the_pages_named_lines_equal_the_python_constants(self):
        match = re.search(
            r"const GITHUB_REPOSITORY_LIST_NAMED_LINES = \[(.*?)\];", self.SOURCE, re.S
        )
        assert match
        lines = json.loads(f"[{match.group(1).strip().rstrip(',')}]")
        assert lines == [GITHUB_REPOSITORY_LIST_RECONNECT_LINE]
        assert GENERIC not in lines

    def test_a_502_branch_comes_before_the_generic_throw(self):
        body = self._function("loadRepositoryList")
        branch = body.index("response.status === 502")
        assert body.index("response.status === 503") < branch
        assert branch < body.index("throw new Error('Failed to load repositories')")

    def test_the_branch_shows_only_a_named_line_as_text_with_save_off_and_no_toast(self):
        body = self._function("loadRepositoryList")
        branch = body[
            body.index("response.status === 502") : body.index(
                "throw new Error('Failed to load repositories')"
            )
        ]
        assert "GITHUB_REPOSITORY_LIST_NAMED_LINES.includes(detail)" in branch
        assert "typeof detail === 'string'" in branch
        assert "prefsLoadFailed = true" in branch
        assert "named.className = 'repository-list-empty'" in branch
        assert "named.textContent = detail" in branch
        assert "innerHTML = detail" not in branch and "${detail}" not in branch
        assert "Toast" not in branch
        assert "return;" in branch

    def test_everything_else_keeps_todays_words_and_toast(self):
        body = self._function("loadRepositoryList")
        catch = body[body.index("} catch (error) {") :]
        assert "I couldn\\'t load your repositories. Try refreshing the page." in catch
        assert "Toast.show('error', 'Error', 'Failed to load GitHub repositories')" in catch
        assert "prefsLoadFailed = true" in catch


class TestSaveDoesNotLookLiveAfterAFailedList:
    """CXO 2026-11-24 (mail 01M87C1V2D): a button that looks live and silently does nothing
    is a control that lies. Both failed-list paths disable Save; Refresh List stays live.
    LAYER: the page's source. The rendered state is on the issue."""

    PAGE = (Path(__file__).resolve().parents[5] / "templates" / "settings_github.html").read_text(
        encoding="utf-8"
    )

    def test_one_helper_disables_the_save_button(self):
        helper = self.PAGE[self.PAGE.index("function disableSaveAfterFailedList()") :][:260]
        assert "getElementById('save-github-prefs-btn')" in helper
        assert "btn.disabled = true" in helper
        assert "refresh" not in helper.lower()

    def test_both_failed_list_paths_call_it(self):
        load = self.PAGE[self.PAGE.index("async function loadRepositoryList()") :]
        load = load[: load.index("function renderRepositoryList(")]
        assert load.count("disableSaveAfterFailedList();") == 2
        named = load[load.index("github-repository-list-named-line") :]
        assert named.index("disableSaveAfterFailedList();") < named.index("return;")
        catch = load[load.index("} catch (error) {") :]
        assert "disableSaveAfterFailedList();" in catch
