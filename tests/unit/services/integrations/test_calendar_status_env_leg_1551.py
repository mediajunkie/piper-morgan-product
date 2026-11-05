"""#1551 (Arch 2026-11-04 18:34, the one per-account fix in the unit): the Integrations
status for Google Calendar counted the deployment's env (``GOOGLE_CALENDAR_CREDENTIALS``,
or ``MCP_ENABLED``, which is not a credential at all) as "configured" for a user who has
no token of their own, and calendar is in the beta offered set. The env leg now counts
only for a principal-less call, GitHub's ADR-081 D1 shape in the same function."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from services.integrations import integration_status_service as iss

pytestmark = pytest.mark.asyncio

_NO_KEYCHAIN = patch.object(iss, "_keychain_has", new=AsyncMock(return_value=False))


@pytest.mark.parametrize("env_name", ["GOOGLE_CALENDAR_CREDENTIALS", "MCP_ENABLED"])
async def test_a_user_with_no_token_is_not_configured_whatever_the_host_env(monkeypatch, env_name):
    monkeypatch.setenv(env_name, "set-on-the-host")
    with _NO_KEYCHAIN:
        assert await iss.get_config_status("calendar", "user-b") == ("not_configured", None)


async def test_a_principal_less_call_still_reads_the_host_env(monkeypatch):
    monkeypatch.setenv("GOOGLE_CALENDAR_CREDENTIALS", "set-on-the-host")
    with _NO_KEYCHAIN:
        assert await iss.get_config_status("calendar", None) == ("configured", "env")


async def test_a_user_with_their_own_token_is_configured_via_keychain(monkeypatch):
    monkeypatch.delenv("GOOGLE_CALENDAR_CREDENTIALS", raising=False)
    monkeypatch.delenv("MCP_ENABLED", raising=False)
    with patch.object(iss, "_keychain_has", new=AsyncMock(return_value=True)):
        assert await iss.get_config_status("calendar", "user-b") == ("configured", "keychain")
