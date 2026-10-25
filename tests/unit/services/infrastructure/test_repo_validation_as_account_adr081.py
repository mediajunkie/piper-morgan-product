"""ADR-081 D1 (Arch 10-24 18:45): a repo link or check is validated as the requesting
account, with its own credential, never the deployment's env token (which can see repos
the account can't, so "exists" could be claimed for a repo the account can't reach).
No credential, or one that couldn't be read, is ``validated=False``: "not checked".

LAYER: unit. The validator with the HTTP client and the resolver's PAT legs stubbed; the
five callers by source scan.
DENOMINATOR: the no-token path with the env set, the account's token passed through, a
failed read, a principal-less call, and 5 of 5 callers.
"""

import ast
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.infrastructure import github_repo_validator as grv
from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

ROOT = Path(__file__).resolve().parents[4]
_USER = "5a2c9d10-0810-4b00-9e00-00000000aaaa"
CALLERS = {
    "services/conversation/conversation_handler.py": 1,
    "services/intent_service/canonical_handlers.py": 2,
    "web/api/routes/repositories.py": 1,
    "web/api/routes/setup.py": 1,
}


def _no_http():
    return patch.object(grv.aiohttp, "ClientSession", side_effect=AssertionError("no call"))


@pytest.mark.asyncio
class TestValidatesAsTheAccount:
    async def test_no_token_is_not_checked_even_with_the_env_token_set(self, monkeypatch):
        monkeypatch.setenv("GITHUB_TOKEN", "fake-token-deployment")
        with _no_http():
            result = await grv.validate_github_repo("owner/repo")
        assert (result.validated, result.error) == (False, None)

    async def test_the_accounts_own_token_is_the_one_sent(self):
        seen = {}

        async def _validate(full_name, token=None):
            seen["token"] = token
            return grv.RepoValidationResult(validated=True, exists=True, accessible=True)

        with (
            patch.object(
                GitHubMCPSpatialAdapter, "_user_pat_at_rest", AsyncMock(return_value=None)
            ),
            patch.object(
                GitHubMCPSpatialAdapter, "_user_pat", MagicMock(return_value="fake-token-account")
            ),
            patch.object(grv, "validate_github_repo", _validate),
        ):
            await grv.validate_github_repo_for_account("owner/repo", _USER)
        assert seen == {"token": "fake-token-account"}

    async def test_a_failed_read_is_not_checked(self, monkeypatch):
        monkeypatch.setenv("GITHUB_TOKEN", "fake-token-deployment")
        with (
            patch.object(
                GitHubMCPSpatialAdapter,
                "_user_pat_at_rest",
                AsyncMock(side_effect=RuntimeError("store down")),
            ),
            _no_http(),
        ):
            result = await grv.validate_github_repo_for_account("owner/repo", _USER)
        assert (result.validated, result.exists) == (False, False)

    async def test_no_account_is_not_checked(self, monkeypatch):
        monkeypatch.setenv("GITHUB_TOKEN", "fake-token-deployment")
        with _no_http():
            result = await grv.validate_github_repo_for_account("owner/repo", None)
        assert result.validated is False


def _calls(path: Path, name: str) -> int:
    tree = ast.parse(path.read_text())
    return sum(
        1
        for n in ast.walk(tree)
        if isinstance(n, ast.Call) and getattr(n.func, "id", getattr(n.func, "attr", None)) == name
    )


def test_every_caller_validates_as_the_account():
    found = {}
    for base in ("services", "web"):
        for path in (ROOT / base).rglob("*.py"):
            rel = path.relative_to(ROOT).as_posix()
            if rel == "services/infrastructure/github_repo_validator.py":
                continue
            assert _calls(path, "validate_github_repo") == 0, (
                f"{rel} calls validate_github_repo directly; use "
                "validate_github_repo_for_account (ADR-081 D1)"
            )
            n = _calls(path, "validate_github_repo_for_account")
            if n:
                found[rel] = n
    assert found == CALLERS
