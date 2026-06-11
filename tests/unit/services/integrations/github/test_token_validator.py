"""#1192 slice (c): GitHub PAT validation via GET /user (token_validator).

These mock httpx so no network is hit. They guard the validator that replaced
the orphaned router.test_connection() path (which 500'd every PAT — #541).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations.github.token_validator import verify_github_token


def _mock_async_client(status_code=200, json_data=None, raise_exc=None):
    """Build an httpx.AsyncClient() replacement whose `async with ... as client`
    yields a client whose `await client.get(...)` returns a response (or raises)."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_data if json_data is not None else {}
    client = MagicMock()
    client.get = AsyncMock(side_effect=raise_exc) if raise_exc else AsyncMock(return_value=resp)
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=client)
    cm.__aexit__ = AsyncMock(return_value=None)
    return MagicMock(return_value=cm)


class TestVerifyGithubToken:
    @pytest.mark.asyncio
    async def test_valid_token_returns_username(self):
        with patch("httpx.AsyncClient", _mock_async_client(200, {"login": "mediajunkie"})):
            result = await verify_github_token("ghp_valid")
        assert result == {"authenticated": True, "username": "mediajunkie", "error": None}

    @pytest.mark.asyncio
    async def test_401_is_invalid_token(self):
        with patch("httpx.AsyncClient", _mock_async_client(401)):
            result = await verify_github_token("ghp_expired")
        assert result["authenticated"] is False
        assert "401" in result["error"]

    @pytest.mark.asyncio
    async def test_403_is_rejected(self):
        with patch("httpx.AsyncClient", _mock_async_client(403)):
            result = await verify_github_token("ghp_rate_limited")
        assert result["authenticated"] is False
        assert "403" in result["error"]

    @pytest.mark.asyncio
    async def test_other_status_surfaces_code(self):
        with patch("httpx.AsyncClient", _mock_async_client(500)):
            result = await verify_github_token("ghp_x")
        assert result["authenticated"] is False
        assert "500" in result["error"]

    @pytest.mark.asyncio
    async def test_empty_token_short_circuits_no_network(self):
        # No patch needed — must not touch httpx at all.
        result = await verify_github_token("")
        assert result == {"authenticated": False, "username": None, "error": "No token provided"}

    @pytest.mark.asyncio
    async def test_none_token_short_circuits(self):
        assert (await verify_github_token(None))["authenticated"] is False

    @pytest.mark.asyncio
    async def test_network_error_degrades_gracefully(self):
        with patch("httpx.AsyncClient", _mock_async_client(raise_exc=RuntimeError("DNS fail"))):
            result = await verify_github_token("ghp_valid")
        assert result["authenticated"] is False
        assert "Connection error" in result["error"]
