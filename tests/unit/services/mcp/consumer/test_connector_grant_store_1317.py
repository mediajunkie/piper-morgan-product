"""#1317 inc.2 slice B — ConnectorGrantStore over the #358 encrypted user-secret store.

Asserts the grant is stored/retrieved under the (user, "<connector>_mcp_oauth") key with
validate=False (it's an OAuth token, not a vendor API key). The underlying
UserAPIKeyService is mocked (DI) — this is the wiring/convention contract, not the
encryption (which #358 already tests).
"""

from unittest.mock import AsyncMock

import pytest

from services.mcp.consumer.connector_grant_store import ConnectorGrantStore

pytestmark = pytest.mark.asyncio

_ALPHA = "11111111-1111-1111-1111-111111111111"
_SESSION = object()  # opaque session; the mock doesn't use it


class TestConnectorGrantStore:
    async def test_store_uses_connector_provider_and_skips_validation(self):
        svc = AsyncMock()
        await ConnectorGrantStore(service=svc).store(_SESSION, _ALPHA, "github", "gho_tok")
        svc.store_user_key.assert_awaited_once()
        args, kwargs = svc.store_user_key.call_args
        # (session, user_id, provider, api_key) positional; validate kwarg
        assert args[1] == _ALPHA
        assert args[2] == "github_mcp_oauth"
        assert args[3] == "gho_tok"
        assert kwargs.get("validate") is False  # OAuth grant, not a key to validate

    async def test_get_returns_the_grant(self):
        svc = AsyncMock()
        svc.retrieve_user_key.return_value = "gho_stored"
        got = await ConnectorGrantStore(service=svc).get(_SESSION, _ALPHA, "github")
        assert got == "gho_stored"
        args, _ = svc.retrieve_user_key.call_args
        assert args[1] == _ALPHA and args[2] == "github_mcp_oauth"

    async def test_get_missing_is_none(self):
        svc = AsyncMock()
        svc.retrieve_user_key.return_value = None
        assert await ConnectorGrantStore(service=svc).get(_SESSION, _ALPHA, "github") is None

    async def test_provider_key_is_connector_scoped(self):
        # different connectors → distinct provider keys (no cross-connector collision)
        from services.mcp.consumer.connector_grant_store import _provider

        assert _provider("github") == "github_mcp_oauth"
        assert _provider("calendar") == "calendar_mcp_oauth"
        assert _provider("github") != _provider("calendar")

    async def test_delete_revokes_the_grant(self):
        # #1330: delete is the disconnect inverse of store — same connector-scoped key.
        svc = AsyncMock()
        svc.delete_user_key.return_value = True
        ok = await ConnectorGrantStore(service=svc).delete(_SESSION, _ALPHA, "github")
        assert ok is True
        args, _ = svc.delete_user_key.call_args
        assert args[1] == _ALPHA and args[2] == "github_mcp_oauth"

    async def test_delete_missing_is_false(self):
        # nothing stored → idempotent no-op (so disconnect never fails on a missing grant)
        svc = AsyncMock()
        svc.delete_user_key.return_value = False
        assert await ConnectorGrantStore(service=svc).delete(_SESSION, _ALPHA, "github") is False
