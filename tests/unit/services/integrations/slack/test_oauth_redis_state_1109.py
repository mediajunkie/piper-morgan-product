"""Tests for #1109 (RECONNECT WS-7): Slack OAuth state store → Redis.

The OAuth nonce store moved from a class-level in-process dict to Redis so it is
multi-process safe. State is stored at key ``slack:oauth:state:{nonce}`` as JSON,
with a Redis TTL derived from the state's ``expires_at`` (the 15-minute window).
Redis TTL replaces the old manual ``cleanup_expired_states`` housekeeping.

The store-touching methods are now async (``redis.asyncio`` requires ``await``):
``generate_authorization_url``, ``_verify_oauth_state`` / ``verify_oauth_state``,
``handle_oauth_callback`` (already async), and ``get_oauth_status``.

These tests use an in-memory fake Redis (``_FakeRedis``) patched in via
``RedisFactory.redis_scope`` — ``fakeredis`` is not installed in this env, and the
fake captures exactly the surface the handler uses (setex/get/getdel/scan_iter).
"""

import base64
import json
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

from services.integrations.slack.config_service import SlackConfigService
from services.integrations.slack.oauth_handler import (
    OAUTH_STATE_KEY_PREFIX,
    SlackOAuthHandler,
)


# ---------------------------------------------------------------------------
# Fake Redis: a minimal in-memory stand-in for the surface the handler uses.
# Stores values as bytes (RedisFactory uses decode_responses=False) and tracks
# a coarse TTL so an "expired" key can be simulated by setting a past TTL.
# ---------------------------------------------------------------------------
class _FakeRedis:
    def __init__(self):
        # key -> (value_bytes, expires_at_monotonic_or_None)
        self.store: dict[str, bytes] = {}
        self.ttls: dict[str, int] = {}
        self.closed = False

    async def setex(self, key, ttl_seconds, value):
        if isinstance(value, str):
            value = value.encode()
        self.store[key] = value
        self.ttls[key] = int(ttl_seconds)
        return True

    async def get(self, key):
        return self.store.get(key)

    async def getdel(self, key):
        self.ttls.pop(key, None)
        return self.store.pop(key, None)

    async def scan_iter(self, match=None):
        # naive glob: only the trailing "*" form the handler uses
        prefix = match[:-1] if match and match.endswith("*") else match
        for k in list(self.store.keys()):
            if prefix is None or k.startswith(prefix):
                yield k

    async def close(self):
        self.closed = True


@pytest.fixture
def fake_redis():
    return _FakeRedis()


@pytest.fixture
def patched_redis(fake_redis):
    """Patch RedisFactory.redis_scope to yield the shared fake client."""

    @asynccontextmanager
    async def _scope():
        yield fake_redis

    with patch(
        "services.integrations.slack.oauth_handler.RedisFactory.redis_scope",
        side_effect=_scope,
    ):
        yield fake_redis


@pytest.fixture
def handler():
    # config_service.get_config(user_id=...) must return an object with a
    # redirect_uri attribute (the handler reads config.redirect_uri).
    config_service = MagicMock(spec=SlackConfigService)
    config = MagicMock()
    config.redirect_uri = "http://localhost:8001/api/v1/settings/integrations/slack/callback"
    config_service.get_config.return_value = config
    return SlackOAuthHandler(config_service=config_service)


def _decode_state(state: str) -> dict:
    padded = state + "=" * (4 - len(state) % 4)
    return json.loads(base64.urlsafe_b64decode(padded))


# ---------------------------------------------------------------------------
# Storage: store -> retrieve round-trip
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_generate_stores_nonce_in_redis_with_ttl(handler, patched_redis):
    """generate_authorization_url writes the nonce to Redis under the prefixed
    key with a positive TTL (the ~15-minute expiry window)."""
    auth_url, state = await handler.generate_authorization_url(user_id="u-1")

    nonce = _decode_state(state)["nonce"]
    key = f"{OAUTH_STATE_KEY_PREFIX}{nonce}"

    assert key in patched_redis.store, "nonce must be stored under the prefixed key"
    # TTL derived from expires_at - now (15 min); allow slack for execution time
    assert 60 < patched_redis.ttls[key] <= 15 * 60

    # The nonce IS the key; the stored payload mirrors the prior in-process
    # shape (user_id / expires_at / redirect_uri / scopes), without a redundant
    # nonce field.
    stored = json.loads(patched_redis.store[key])
    assert stored["user_id"] == "u-1"
    assert "expires_at" in stored


@pytest.mark.asyncio
async def test_store_retrieve_roundtrips_state_data(handler, patched_redis):
    """The redirect_uri / scopes stored on /connect survive the round-trip and
    are recoverable by the verify path."""
    await handler.generate_authorization_url(
        user_id="u-2", redirect_uri="https://example.test/cb"
    )
    # exactly one key stored
    (key,) = list(patched_redis.store.keys())
    stored = json.loads(patched_redis.store[key])
    assert stored["redirect_uri"] == "https://example.test/cb"


# ---------------------------------------------------------------------------
# Validation: valid nonce passes, missing nonce rejected
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_verify_valid_nonce_returns_user_id(handler, patched_redis):
    _, state = await handler.generate_authorization_url(user_id="u-3")
    is_valid, user_id = await handler.verify_oauth_state(state)
    assert is_valid is True
    assert user_id == "u-3"


@pytest.mark.asyncio
async def test_verify_missing_nonce_rejected(handler, patched_redis):
    """A state whose nonce is absent from Redis (never stored / already popped /
    TTL-expired) is rejected."""
    # Build a well-formed state but never store the nonce.
    state_data = {"user_id": "u-4", "nonce": "never-stored-nonce"}
    state = (
        base64.urlsafe_b64encode(json.dumps(state_data).encode()).decode().rstrip("=")
    )
    is_valid, user_id = await handler.verify_oauth_state(state)
    assert is_valid is False
    assert user_id is None


@pytest.mark.asyncio
async def test_verify_is_non_destructive(handler, patched_redis):
    """verify_oauth_state must NOT remove the key (the callback's getdel does the
    single-use pop). Two verifies in a row both succeed."""
    _, state = await handler.generate_authorization_url(user_id="u-5")
    assert (await handler.verify_oauth_state(state))[0] is True
    assert (await handler.verify_oauth_state(state))[0] is True
    assert len(patched_redis.store) == 1


@pytest.mark.asyncio
async def test_verify_expired_state_rejected(handler, patched_redis):
    """A nonce whose stored expires_at is in the past is rejected (defensive
    expiry check; Redis TTL would normally have removed it already)."""
    _, state = await handler.generate_authorization_url(user_id="u-6")
    (key,) = list(patched_redis.store.keys())
    stored = json.loads(patched_redis.store[key])
    stored["expires_at"] = (datetime.utcnow() - timedelta(minutes=1)).isoformat()
    patched_redis.store[key] = json.dumps(stored).encode()

    is_valid, user_id = await handler.verify_oauth_state(state)
    assert is_valid is False
    assert user_id is None


@pytest.mark.asyncio
async def test_verify_user_id_tamper_rejected(handler, patched_redis):
    """If the state's user_id doesn't match the stored user_id, reject (tamper)."""
    _, state = await handler.generate_authorization_url(user_id="real-user")
    # Forge a state reusing the real nonce but a different user_id.
    nonce = _decode_state(state)["nonce"]
    forged = {"user_id": "attacker", "nonce": nonce}
    forged_state = (
        base64.urlsafe_b64encode(json.dumps(forged).encode()).decode().rstrip("=")
    )
    is_valid, user_id = await handler.verify_oauth_state(forged_state)
    assert is_valid is False


# ---------------------------------------------------------------------------
# Single-use pop: the callback removes the nonce (getdel)
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_connect_to_callback_flow_validates_and_pops(handler, patched_redis):
    """End-to-end: /connect stores nonce; a successful /callback validates it,
    pops it (single-use), and a second callback with the same state fails."""
    _, state = await handler.generate_authorization_url(user_id="flow-user")
    assert len(patched_redis.store) == 1

    # Mock the token exchange + spatial init + storage so we isolate state logic.
    token_data = {
        "ok": True,
        "access_token": "xoxb-test",
        "team": {"id": "T1", "name": "WS", "domain": "ws"},
        "authed_user": {"id": "U1"},
        "bot_user_id": "B1",
        "app_id": "A1",
    }
    with patch.object(
        handler, "_exchange_code_for_tokens", return_value=token_data
    ), patch.object(handler, "_store_workspace_tokens", return_value=None):
        result = await handler.handle_oauth_callback(code="c", state=state)

    assert result["success"] is True
    assert result["user_id"] == "flow-user"
    # nonce removed (single-use)
    assert len(patched_redis.store) == 0

    # Replaying the same state now fails (nonce gone).
    with patch.object(handler, "_exchange_code_for_tokens", return_value=token_data):
        with pytest.raises(Exception):
            await handler.handle_oauth_callback(code="c", state=state)


@pytest.mark.asyncio
async def test_callback_error_path_pops_nonce(handler, patched_redis):
    """If token exchange fails, the nonce is still cleaned up (no leak)."""
    _, state = await handler.generate_authorization_url(user_id="err-user")
    assert len(patched_redis.store) == 1

    with patch.object(
        handler, "_exchange_code_for_tokens", side_effect=RuntimeError("boom")
    ):
        with pytest.raises(Exception):
            await handler.handle_oauth_callback(code="c", state=state)

    # nonce cleaned up on the error path
    assert len(patched_redis.store) == 0


# ---------------------------------------------------------------------------
# get_oauth_status is async and counts live entries via SCAN
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_get_oauth_status_counts_active_flows(handler, patched_redis):
    await handler.generate_authorization_url(user_id="s-1")
    await handler.generate_authorization_url(user_id="s-2")

    status = await handler.get_oauth_status()
    assert status["handler_status"] == "operational"
    assert status["active_oauth_flows"] == 2
    assert status["total_state_entries"] == 2


# ---------------------------------------------------------------------------
# The manual cleanup method is gone (TTL replaces it).
# ---------------------------------------------------------------------------
def test_cleanup_expired_states_removed(handler):
    """Redis TTL auto-expires entries; the manual housekeeping method is removed."""
    assert not hasattr(handler, "cleanup_expired_states"), (
        "cleanup_expired_states should be removed — Redis TTL handles expiry"
    )
