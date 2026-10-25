"""#1982 — the GitHub PAT dual write (Arch's ruling on the PAT-only gap, 2026-10-11).

Settings → GitHub keeps its keychain write and ALSO stores the PAT through
``UserAPIKeyService.store_user_key(provider="github", validate=False)``, which lands
the row under the GitHub-only HKDF context the MCP app's scoped subkey can read.
Disconnect deletes both copies. The backfill script copies pre-existing PATs.

LAYER (m-43): the helper and the disconnect path with the key service patched (no
DB); the backfill's name parsing on strings. DENOMINATOR: unit level; the route
itself is exercised only through the helper it calls (the route's JWT/Form shape is
unchanged and covered elsewhere).
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.connectors.github_pat_store import (
    GITHUB_PAT_PROVIDER,
    delete_user_pat_at_rest,
    store_user_pat_at_rest,
)

_U = "11111111-2222-3333-4444-555555555555"


class _Scope:
    def __init__(self, session):
        self._s = session

    async def __aenter__(self):
        return self._s

    async def __aexit__(self, *a):
        return False


@pytest.mark.asyncio
async def test_store_writes_the_github_provider_unvalidated():
    svc = MagicMock()
    svc.store_user_key = AsyncMock()
    session = MagicMock()
    factory = MagicMock()
    factory.session_scope_fresh = MagicMock(return_value=_Scope(session))
    with (
        patch("services.security.user_api_key_service.UserAPIKeyService", return_value=svc),
        patch("services.database.session_factory.AsyncSessionFactory", factory),
    ):
        await store_user_pat_at_rest(_U, "ghp_example")
    svc.store_user_key.assert_awaited_once_with(
        session=session,
        user_id=_U,
        provider=GITHUB_PAT_PROVIDER,
        api_key="ghp_example",
        validate=False,
        security_check=False,
    )


@pytest.mark.asyncio
async def test_store_failure_propagates_not_swallowed():
    """A half-save (keychain yes, at-rest no) would show "Connected" on Settings while
    the MCP app cannot serve the PAT; the route must see the failure."""
    svc = MagicMock()
    svc.store_user_key = AsyncMock(side_effect=RuntimeError("db down"))
    factory = MagicMock()
    factory.session_scope_fresh = MagicMock(return_value=_Scope(MagicMock()))
    with (
        patch("services.security.user_api_key_service.UserAPIKeyService", return_value=svc),
        patch("services.database.session_factory.AsyncSessionFactory", factory),
    ):
        with pytest.raises(RuntimeError):
            await store_user_pat_at_rest(_U, "ghp_example")


@pytest.mark.asyncio
async def test_delete_targets_the_github_provider():
    svc = MagicMock()
    svc.delete_user_key = AsyncMock(return_value=True)
    session = MagicMock()
    with patch("services.security.user_api_key_service.UserAPIKeyService", return_value=svc):
        assert await delete_user_pat_at_rest(session, _U) is True
    svc.delete_user_key.assert_awaited_once_with(session, _U, GITHUB_PAT_PROVIDER)


@pytest.mark.asyncio
async def test_disconnect_github_removes_all_three_copies():
    """Arch #1982: a revoke is proven complete. After the dual write the PAT lives in
    three places: the keychain under ``github_token`` (the route's write), the keychain
    under ``github`` (the key service's own copy from store_user_key) and the at-rest
    ``user_api_keys`` row. Disconnect must remove all three. The key service is REAL
    here (only the keychain, the session and the audit logger are doubles), so the
    second keychain delete and the row delete are the service's own behaviour."""
    from types import SimpleNamespace

    from services.connectors.disconnect import disconnect_connector
    from services.infrastructure.keychain_service import SecretProvenance, SecretRead
    from services.mcp.consumer.connector import DegradationReason

    keychain = MagicMock()
    # the helper's own copy goes through the async surface (#2172); the real key
    # service's copy (provider "github") still uses the sync delete_api_key
    keychain.adelete_api_key = AsyncMock(return_value=True)
    keychain.aread_secret = AsyncMock(return_value=SecretRead(SecretProvenance.VERIFIED_ABSENT))
    binding_repo = MagicMock()
    binding_repo.set_status = AsyncMock()
    grant_store = MagicMock()
    grant_store.delete = AsyncMock()
    row = MagicMock()
    row.key_reference = "ref"
    row.created_at = None
    row.last_validated_at = None
    result = MagicMock()
    result.scalar_one_or_none.return_value = row
    session = MagicMock()
    session.execute = AsyncMock(return_value=result)
    session.delete = AsyncMock()
    session.commit = AsyncMock()
    factory = MagicMock()
    factory.session_scope = MagicMock(side_effect=lambda: _Scope(session))
    with (
        patch("services.infrastructure.keychain_service.KeychainService", return_value=keychain),
        # the key service binds the class at import time; patch its own name too, or
        # this test's outcome depends on whether the module was imported earlier
        patch("services.security.user_api_key_service.KeychainService", return_value=keychain),
        patch("services.integrations.github.config_service.GitHubConfigService"),
        patch("services.database.session_factory.AsyncSessionFactory", factory),
        patch(
            "services.connectors.binding_repository.ConnectorBindingRepository",
            return_value=binding_repo,
        ),
        patch(
            "services.mcp.consumer.connector_grant_store.ConnectorGrantStore",
            return_value=grant_store,
        ),
        patch("services.security.user_api_key_service.audit_logger") as audit,
        patch(
            "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.resolve_credential",
            AsyncMock(return_value=SimpleNamespace(reason=DegradationReason.CONNECT_REQUIRED)),
        ),
    ):
        audit.log_api_key_event = AsyncMock()
        outcome = await disconnect_connector(_U, "github")
    assert outcome.cleared, outcome.remaining
    # 1. the route's keychain copy
    keychain.adelete_api_key.assert_any_await("github_token", _U)
    keychain.adelete_api_key.assert_any_await("github", _U)  # helper's read-back of copy 2
    # 2. the key service's own keychain copy (provider "github", user-scoped)
    keychain.delete_api_key.assert_any_call("github", username=_U)
    # 3. the at-rest row
    session.delete.assert_awaited_once_with(row)
    grant_store.delete.assert_awaited_once()


def _load_backfill():
    name = "backfill_github_pat_rows_1982_under_test"
    spec = importlib.util.spec_from_file_location(
        name, Path("scripts/backfill_github_pat_rows_1982.py")
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


class TestBackfillNames:
    def test_parse_user_pat_name(self):
        mod = _load_backfill()
        assert mod.parse_name(f"{_U}_github_token_api_key") == _U

    @pytest.mark.parametrize(
        "name",
        [
            "github_token_api_key",  # system-scoped, not a user row
            f"{_U}_github_api_key",  # the key service's own keychain copy
            f"{_U}_github_client_secret_api_key",
            "not-a-uuid_github_token_api_key",
            f"{_U}_github_token_api_key_extra",
        ],
    )
    def test_other_names_are_not_user_pats(self, name):
        mod = _load_backfill()
        assert mod.parse_name(name) is None

    def test_apply_without_snapshot_is_refused_before_db(self, monkeypatch):
        import base64

        mod = _load_backfill()
        monkeypatch.setenv("ENCRYPTION_MASTER_KEY", base64.b64encode(bytes(32)).decode())
        monkeypatch.delenv("ENCRYPTION_SCOPED_SUBKEYS", raising=False)
        assert mod.main(["--apply"]) == 2


@pytest.mark.asyncio
async def test_store_skips_the_format_validator_for_a_live_verified_token():
    """``validate=False`` does not skip the #268 format/strength/leak validator; the
    dual write must, or a PAT GitHub accepted could be refused after the keychain
    write (a half-save). Pinned at the key service: with security_check=False the
    validator is never consulted."""
    from services.security.user_api_key_service import UserAPIKeyService

    keychain = MagicMock()
    enc = MagicMock()
    enc.encrypt.return_value = "token"
    svc = UserAPIKeyService(keychain_service=keychain, field_encryption_service=enc)
    svc._validator = MagicMock()
    svc._validator.validate_api_key = AsyncMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = None  # no existing row → create branch
    session = MagicMock()
    session.execute = AsyncMock(return_value=result)
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    with patch("services.security.user_api_key_service.audit_logger") as audit:
        audit.log_api_key_event = AsyncMock()
        await svc.store_user_key(
            session, _U, "github", "ghp_short", validate=False, security_check=False
        )
    svc._validator.validate_api_key.assert_not_called()
    enc.encrypt.assert_called_once()
    assert enc.encrypt.call_args.args[1] == "user_api_keys.secret.github"


def test_helper_passes_security_check_false():
    """The helper's call shape is the whole point; keep it honest by reading the source."""
    import inspect

    import services.connectors.github_pat_store as m

    src = inspect.getsource(m.store_user_pat_at_rest)
    assert "validate=False" in src and "security_check=False" in src
