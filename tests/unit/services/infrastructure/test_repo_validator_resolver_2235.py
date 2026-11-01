"""#2235: repo validation authenticates through the connector's one credential resolver.

Lead's finding (10-30, building #2230): ``validate_github_repo_for_account`` took its
token from the account's PAT only (``GitHubMCPSpatialAdapter.account_pat``), skipping
``resolve_credential`` (#1965: the BOUND OAuth binding first, the PAT second). So an
account connected only by "Connect with GitHub" was never validated: every repo read
"not checked", in the wizard, the canonical handlers, the repositories route and the
#2230 chat setter. A second credential path beside the resolver, the shape ADR-081's
"one credential resolver per connector" forbids.

Built: ``_account_authorization`` asks ``GitHubMCPSpatialAdapter._grant_headers_or_raise``
(the resolver's Authorization, ``Bearer <grant or PAT>``) and ``validate_github_repo``
sends those headers. "Not checked" keeps a stated reason: ``no_account``,
``no_credential`` (neither leg), ``credential_failed`` (a leg failed: stale token,
unreachable store, missing grant), ``error``; a failed read is never "not found" (#2151).

LAYER: the validator with the resolver seam patched (the resolver's legs have their own
pins) and aiohttp mocked; the served line (an OAuth-only account validates a repo it can
see: the #2230 setter writes, the wizard reports the repo) is PA's after the promotion.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.infrastructure import github_repo_validator as grv
from services.integrations.github.read_failed import GitHubReadFailed
from services.mcp.consumer.connector import DegradationReason
from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

ROOT = Path(__file__).resolve().parents[4]
_USER = "5a2c9d10-0810-4b00-9e00-00000000aaaa"
HEADERS = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter._grant_headers_or_raise"
SESSION = "services.infrastructure.github_repo_validator.aiohttp.ClientSession"


def _aiohttp(status: int, body: dict | None = None):
    """The nested aiohttp context managers, recording the GET's kwargs."""
    response = MagicMock()
    response.status = status
    response.json = AsyncMock(return_value=body or {})
    get_cm = MagicMock()
    get_cm.__aenter__ = AsyncMock(return_value=response)
    get_cm.__aexit__ = AsyncMock(return_value=False)
    session = MagicMock()
    session.get.return_value = get_cm
    session_cm = MagicMock()
    session_cm.__aenter__ = AsyncMock(return_value=session)
    session_cm.__aexit__ = AsyncMock(return_value=False)
    return session_cm, session


def _sent_headers(session) -> dict:
    return session.get.call_args.kwargs["headers"]


@pytest.mark.asyncio
class TestBothLegsValidate:
    async def test_oauth_only_account_validates_a_repo_it_can_see(self):
        """The issue's case: no PAT, a BOUND OAuth grant. Before #2235: not checked."""
        cm, session = _aiohttp(
            200,
            {
                "description": "d",
                "language": "Python",
                "visibility": "private",
                "default_branch": "main",
            },
        )
        with (
            patch(HEADERS, AsyncMock(return_value={"Authorization": "Bearer gho_oauth_grant"})),
            patch(SESSION, return_value=cm),
        ):
            result = await grv.validate_github_repo_for_account("owner/repo", _USER)
        assert (result.validated, result.exists, result.accessible) == (True, True, True)
        assert result.visibility == "private" and result.status_code == 200
        assert _sent_headers(session)["Authorization"] == "Bearer gho_oauth_grant"

    async def test_oauth_only_account_404_is_a_checked_not_found(self):
        cm, session = _aiohttp(404)
        with (
            patch(HEADERS, AsyncMock(return_value={"Authorization": "Bearer gho_oauth_grant"})),
            patch(SESSION, return_value=cm),
        ):
            result = await grv.validate_github_repo_for_account("owner/missing", _USER)
        assert (result.validated, result.exists) == (True, False)
        assert result.status_code == 404 and result.not_checked_reason is None
        assert _sent_headers(session)["Authorization"] == "Bearer gho_oauth_grant"

    async def test_pat_account_validates_with_the_pat_leg(self):
        cm, session = _aiohttp(200, {"default_branch": "main"})
        with (
            patch(HEADERS, AsyncMock(return_value={"Authorization": "Bearer ghp_account_pat"})),
            patch(SESSION, return_value=cm),
        ):
            result = await grv.validate_github_repo_for_account("owner/repo", _USER)
        assert result.validated is True and result.exists is True
        assert _sent_headers(session)["Authorization"] == "Bearer ghp_account_pat"
        assert _sent_headers(session)["Accept"] == "application/vnd.github.v3+json"


@pytest.mark.asyncio
class TestNotCheckedKeepsItsReason:
    async def test_neither_leg_is_no_credential_and_no_http(self):
        with (
            patch(
                HEADERS,
                AsyncMock(
                    side_effect=GitHubReadFailed(
                        "no credential for this account", None, detail="no_credential"
                    )
                ),
            ),
            patch(SESSION, side_effect=AssertionError("no call")),
        ):
            result = await grv.validate_github_repo_for_account("owner/repo", _USER)
        assert (result.validated, result.exists, result.accessible) == (False, False, False)
        assert result.not_checked_reason == "no_credential"
        assert result.error is None

    @pytest.mark.parametrize(
        "reason, detail",
        [
            (DegradationReason.STALE_TOKEN, "stale_token"),
            (DegradationReason.UNREACHABLE, "unreachable"),
            (DegradationReason.MISCONFIGURED, "grant_missing"),
        ],
    )
    async def test_a_failed_credential_read_is_credential_failed_never_not_found(
        self, reason, detail
    ):
        with (
            patch(
                HEADERS,
                AsyncMock(side_effect=GitHubReadFailed("credential failed", reason, detail=detail)),
            ),
            patch(SESSION, side_effect=AssertionError("no call")),
        ):
            result = await grv.validate_github_repo_for_account("owner/repo", _USER)
        assert result.validated is False
        assert result.not_checked_reason == "credential_failed"
        assert detail in (result.error or "")
        assert result.exists is False and result.accessible is False

    async def test_no_account_is_no_account(self):
        with patch(SESSION, side_effect=AssertionError("no call")):
            result = await grv.validate_github_repo_for_account("owner/repo", None)
        assert result.validated is False and result.not_checked_reason == "no_account"

    async def test_an_unexpected_resolver_fault_is_error_not_not_found(self):
        with (
            patch(HEADERS, AsyncMock(side_effect=RuntimeError("db down"))),
            patch(SESSION, side_effect=AssertionError("no call")),
        ):
            result = await grv.validate_github_repo_for_account("owner/repo", _USER)
        assert result.validated is False and result.not_checked_reason == "error"
        assert result.exists is False

    async def test_the_deployment_env_token_is_never_used_for_an_account(self, monkeypatch):
        monkeypatch.setenv("GITHUB_TOKEN", "fake-token-deployment")
        with (
            patch(
                HEADERS,
                AsyncMock(side_effect=GitHubReadFailed("none", None, detail="no_credential")),
            ),
            patch(SESSION, side_effect=AssertionError("no call")),
        ):
            result = await grv.validate_github_repo_for_account("owner/repo", _USER)
        assert result.validated is False


# ─────────────────────────── the grep pin (acceptance line 2) ────────────────


def _calls(path: Path, name: str) -> int:
    tree = ast.parse(path.read_text())
    return sum(
        1
        for n in ast.walk(tree)
        if isinstance(n, ast.Call) and getattr(n.func, "id", getattr(n.func, "attr", None)) == name
    )


def test_the_validator_reads_no_token_outside_the_resolver():
    """No caller of the validator reads a token outside ``resolve_credential``: the
    validator module itself names neither the PAT reader nor the deployment token for
    the account path, and only the resolver's header builder."""
    src = (ROOT / "services/infrastructure/github_repo_validator.py").read_text()
    assert "_grant_headers_or_raise" in src
    for forbidden in ("account_pat", "_account_github_token", "_user_pat", "get_github_token()"):
        assert forbidden not in src.replace("def get_github_token()", ""), forbidden
    assert re.search(r"validate_github_repo\(full_name, headers=headers\)", src)


def test_every_caller_goes_through_the_account_validator():
    """The ADR-081 pin, restated here so this file holds the whole rule: outside the
    validator module nothing calls ``validate_github_repo`` directly (so nothing can
    pass a token of its own), and nothing calls ``_account_authorization`` either."""
    for base in ("services", "web"):
        for path in (ROOT / base).rglob("*.py"):
            rel = path.relative_to(ROOT).as_posix()
            if rel == "services/infrastructure/github_repo_validator.py":
                continue
            assert _calls(path, "validate_github_repo") == 0, rel
            assert _calls(path, "_account_authorization") == 0, rel
