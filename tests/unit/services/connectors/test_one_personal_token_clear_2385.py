"""Issue 2385: Disconnect and Remove token clear the GitHub personal token through one
function, so a copy added to the clear is cleared on both paths.

LAYER: the module's source, read with ``ast``; and the two callers run with the shared
clear replaced by a recorder. No keychain, database or network.
DENOMINATOR: every function in ``services/connectors/disconnect.py``.
"""

import ast
from pathlib import Path
from unittest.mock import AsyncMock, patch

from services.connectors import disconnect

SRC = Path(disconnect.__file__).read_text(encoding="utf-8")
TREE = ast.parse(SRC)
HELPER = "_clear_github_personal_token"
CALLERS = ("_disconnect_github", "remove_github_personal_token")


def _function(name):
    return next(
        node
        for node in ast.walk(TREE)
        if isinstance(node, ast.AsyncFunctionDef) and node.name == name
    )


def _calls(node):
    return [
        n.func.id
        for n in ast.walk(node)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
    ]


def _strings(node):
    return {
        n.value for n in ast.walk(node) if isinstance(n, ast.Constant) and isinstance(n.value, str)
    }


def test_both_callers_use_the_shared_clear_exactly_once():
    for name in CALLERS:
        assert _calls(_function(name)).count(HELPER) == 1, name


def test_no_function_but_the_shared_clear_touches_a_personal_token_copy():
    """The three copies are named only inside the helper: the Settings keychain copy
    ("github_token"), the at-rest row (``delete_user_pat_at_rest``) and the key service's
    keychain copy ("github" passed to the keychain read-back). A caller that grows its
    own copy of a step fails here."""
    for node in ast.walk(TREE):
        if not isinstance(node, ast.AsyncFunctionDef) or node.name == HELPER:
            continue
        assert "github_token" not in _strings(node), node.name
        imported = {
            alias.name for n in ast.walk(node) if isinstance(n, ast.ImportFrom) for alias in n.names
        }
        assert "delete_user_pat_at_rest" not in imported, node.name
        for call in ast.walk(node):
            if (
                isinstance(call, ast.Call)
                and isinstance(call.func, ast.Name)
                and call.func.id == "_keychain_copy_gone"
            ):
                provider = call.args[1]
                assert not (
                    isinstance(provider, ast.Constant) and provider.value == "github"
                ), node.name


def test_the_shared_clear_names_all_three_copies():
    helper = _function(HELPER)
    assert {"github_token", "github"} <= _strings(helper)
    assert {"keychain_pat", "pat_at_rest", "keychain_pat_key_service"} <= _strings(helper)
    assert _calls(helper).count("_keychain_copy_gone") == 2


async def test_remove_token_reports_what_the_shared_clear_could_not_verify():
    shared = AsyncMock(return_value=["pat_at_rest"])
    with (
        patch.object(disconnect, HELPER, shared),
        patch("services.infrastructure.keychain_service.KeychainService"),
        patch(
            "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.account_pat",
            AsyncMock(return_value=None),
        ),
        patch("services.integrations.github.config_service.GitHubConfigService"),
    ):
        remaining = await disconnect.remove_github_personal_token("u-1")
    shared.assert_awaited_once()
    assert shared.await_args.args[1] == "u-1"
    assert remaining == ["pat_at_rest"]


async def test_disconnect_reports_what_the_shared_clear_could_not_verify():
    shared = AsyncMock(return_value=["keychain_pat", "keychain_pat_key_service"])
    gone = AsyncMock(return_value=True)
    with (
        patch.object(disconnect, HELPER, shared),
        patch.object(disconnect, "_keychain_copy_gone", gone),
        patch.object(disconnect, "_revoke_github_grant_at_github", AsyncMock(return_value=False)),
        patch("services.infrastructure.keychain_service.KeychainService"),
    ):
        remaining, revoke_failed = await disconnect._disconnect_github("u-1")
    shared.assert_awaited_once()
    assert shared.await_args.args[1] == "u-1"
    assert remaining[:2] == ["keychain_pat", "keychain_pat_key_service"]
    assert revoke_failed is False
