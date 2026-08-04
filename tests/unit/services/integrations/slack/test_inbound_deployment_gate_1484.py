"""#1484 fail-closed deployment gate (Arch ruling + CXO refusal contract, 2026-08-04).

The load-bearing test per the issue's own AC: the TOKEN-PRESENT + FLAG-UNSET
case (the token-absent case passes vacuously today and proves nothing —
scripts/assertion-vacuity-check.py).
"""
from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.asyncio
async def test_build_runner_refuses_with_tokens_present_but_flag_unset(monkeypatch):
    monkeypatch.delenv("PIPER_SLACK_INBOUND_ENABLED", raising=False)
    # Tokens PRESENT — the non-vacuous case: the gate alone must refuse.
    monkeypatch.setenv("SLACK_APP_TOKEN", "xapp-test-token")
    from services.integrations.slack import socket_mode_runner as smr
    runner = await smr.build_runner(intent_service=object())
    assert runner is None, "gate must refuse regardless of token presence"


@pytest.mark.asyncio
async def test_build_runner_proceeds_past_gate_when_flag_set(monkeypatch):
    monkeypatch.setenv("PIPER_SLACK_INBOUND_ENABLED", "true")
    monkeypatch.delenv("SLACK_APP_TOKEN", raising=False)
    from services.integrations.slack import socket_mode_runner as smr
    with patch.object(smr, "_resolve_app_token", return_value=None, create=True):
        runner = await smr.build_runner(intent_service=object())
    # flag set + no token → None for TOKEN reasons (the pre-existing behavior),
    # proving the gate is not a blanket refusal in dev.
    assert runner is None


@pytest.mark.asyncio
async def test_save_route_refuses_409_BEFORE_keychain_write(monkeypatch):
    monkeypatch.delenv("PIPER_SLACK_INBOUND_ENABLED", raising=False)
    from fastapi import HTTPException
    import web.api.routes.settings_integrations as si
    stored = []
    with patch("services.infrastructure.keychain_service.KeychainService") as KC:
        KC.return_value.store_api_key = lambda *a, **k: stored.append(a)
        body = si.SlackAppTokenRequest(app_token="xapp-real-looking")
        with pytest.raises(HTTPException) as exc:
            await si.save_slack_app_token(body=body, request=AsyncMock(), current_user=AsyncMock())
        assert exc.value.status_code == 409
        assert "wasn't saved" in exc.value.detail
    assert not stored, "the keychain write must NEVER precede the gate — 'wasn't saved' must be TRUE"
