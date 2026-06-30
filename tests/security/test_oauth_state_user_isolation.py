"""
Tests for OAuth state user isolation (Issue #734: SEC-MULTITENANCY).

TDD: Write failing tests FIRST for OAuth state encoding/decoding.

The OAuth state parameter must:
1. Encode user_id to identify who initiated the flow
2. Include a nonce for CSRF protection
3. Optionally include return_url for post-auth redirect
4. Be tamper-resistant (base64 encoded JSON)

State Format:
    state = base64_encode(json.dumps({
        "user_id": "uuid-string",
        "nonce": "random-token",
        "return_url": "/optional/path"  # optional
    }))
"""

import base64
import json
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from unittest.mock import MagicMock, patch

import pytest

from contextlib import asynccontextmanager, contextmanager


# ---------------------------------------------------------------------------
# Issue #1109: the Slack OAuth nonce store moved to Redis, so the Slack-handler
# tests below exercise async, Redis-backed methods. fakeredis is not installed
# in this env, so we patch RedisFactory.redis_scope with a tiny in-memory fake
# that captures exactly the surface the handler uses (setex/get/getdel).
# ---------------------------------------------------------------------------
class _FakeRedis:
    def __init__(self):
        self.store: Dict[str, bytes] = {}

    async def setex(self, key, ttl_seconds, value):
        self.store[key] = value.encode() if isinstance(value, str) else value
        return True

    async def get(self, key):
        return self.store.get(key)

    async def getdel(self, key):
        return self.store.pop(key, None)

    async def close(self):
        pass


@contextmanager
def _patched_slack_oauth_redis():
    """Patch the Slack OAuth handler's RedisFactory.redis_scope with a shared
    in-memory fake for the duration of the block."""
    fake = _FakeRedis()

    @asynccontextmanager
    async def _scope():
        yield fake

    with patch(
        "services.integrations.slack.oauth_handler.RedisFactory.redis_scope",
        side_effect=_scope,
    ):
        yield fake


class TestOAuthStateEncoding:
    """Tests for OAuth state encoding with user_id."""

    def test_generate_state_includes_user_id(self):
        """State must include user_id in encoded payload."""
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        handler = GoogleCalendarOAuthHandler()
        user_id = "test-user-123"

        # Generate authorization URL with user_id
        auth_url, state = handler.generate_authorization_url(user_id=user_id)

        # Decode state and verify user_id is present
        state_data = _decode_oauth_state(state)
        assert state_data is not None, "State should be valid JSON"
        assert "user_id" in state_data, "State must include user_id"
        assert state_data["user_id"] == user_id, "user_id must match input"

    def test_generate_state_includes_nonce(self):
        """State must include a CSRF nonce."""
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        handler = GoogleCalendarOAuthHandler()
        user_id = "test-user-456"

        auth_url, state = handler.generate_authorization_url(user_id=user_id)

        state_data = _decode_oauth_state(state)
        assert "nonce" in state_data, "State must include nonce"
        assert len(state_data["nonce"]) >= 16, "Nonce must be sufficiently random"

    def test_generate_state_optionally_includes_return_url(self):
        """State can optionally include return_url."""
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        handler = GoogleCalendarOAuthHandler()
        user_id = "test-user-789"
        return_url = "/settings/integrations"

        auth_url, state = handler.generate_authorization_url(user_id=user_id, return_url=return_url)

        state_data = _decode_oauth_state(state)
        assert "return_url" in state_data, "State should include return_url when provided"
        assert state_data["return_url"] == return_url

    def test_state_without_user_id_rejected(self):
        """Generating state without user_id should raise an error."""
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        handler = GoogleCalendarOAuthHandler()

        # Calling without user_id should raise ValueError
        with pytest.raises((ValueError, TypeError)):
            handler.generate_authorization_url()  # No user_id

    async def test_slack_generate_state_includes_user_id(self):
        """Slack handler must also include user_id in state.

        Issue #1109: generate_authorization_url is async (Redis-backed nonce
        store); Redis is patched with an in-memory fake to keep this hermetic.
        """
        from services.integrations.slack.config_service import SlackConfigService
        from services.integrations.slack.oauth_handler import SlackOAuthHandler

        config_service = SlackConfigService()
        handler = SlackOAuthHandler(config_service=config_service)
        user_id = "slack-user-123"

        with _patched_slack_oauth_redis():
            auth_url, state = await handler.generate_authorization_url(user_id=user_id)

        state_data = _decode_oauth_state(state)
        assert state_data is not None, "State should be valid JSON"
        assert "user_id" in state_data, "State must include user_id"
        assert state_data["user_id"] == user_id


class TestOAuthStateDecoding:
    """Tests for OAuth state decoding and user_id extraction."""

    def test_verify_state_returns_user_id(self):
        """State verification should return extracted user_id."""
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        handler = GoogleCalendarOAuthHandler()
        user_id = "decode-test-user"

        # Generate state
        auth_url, state = handler.generate_authorization_url(user_id=user_id)

        # Verify state - should return tuple (is_valid, user_id)
        is_valid, extracted_user_id = handler.verify_state(state)

        assert is_valid is True, "Valid state should pass verification"
        assert extracted_user_id == user_id, "Extracted user_id must match"

    def test_verify_state_rejects_invalid_state(self):
        """Invalid state should be rejected."""
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        handler = GoogleCalendarOAuthHandler()

        # Random invalid state
        is_valid, extracted_user_id = handler.verify_state("invalid-random-state")

        assert is_valid is False, "Invalid state should fail verification"
        assert extracted_user_id is None, "No user_id should be extracted from invalid state"

    def test_verify_state_rejects_expired_state(self):
        """Expired state should be rejected."""
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        handler = GoogleCalendarOAuthHandler()
        user_id = "expire-test-user"

        # Generate state
        auth_url, state = handler.generate_authorization_url(user_id=user_id)

        # Simulate time passing (mock the state storage to show expired)
        # The implementation stores timestamp, so we'll mock time.time()
        with patch("time.time", return_value=9999999999):  # Far future
            is_valid, extracted_user_id = handler.verify_state(state)

        assert is_valid is False, "Expired state should fail verification"
        assert extracted_user_id is None

    def test_verify_state_rejects_tampered_state(self):
        """Tampered state should be rejected."""
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        handler = GoogleCalendarOAuthHandler()
        user_id = "original-user"

        # Generate valid state
        auth_url, state = handler.generate_authorization_url(user_id=user_id)

        # Tamper with state (decode, modify, re-encode)
        state_data = _decode_oauth_state(state)
        state_data["user_id"] = "attacker-user"  # Change user_id
        tampered_state = _encode_oauth_state(state_data)

        # Tampered state should fail (nonce won't match stored)
        is_valid, extracted_user_id = handler.verify_state(tampered_state)

        assert is_valid is False, "Tampered state should fail verification"

    async def test_slack_verify_state_returns_user_id(self):
        """Slack handler verification should also return user_id.

        Issue #1109: generate/verify are async (Redis-backed nonce store);
        Redis is patched with a shared in-memory fake so the nonce stored on
        generate is visible to verify within the test.
        """
        from services.integrations.slack.config_service import SlackConfigService
        from services.integrations.slack.oauth_handler import SlackOAuthHandler

        config_service = SlackConfigService()
        handler = SlackOAuthHandler(config_service=config_service)
        user_id = "slack-decode-user"

        with _patched_slack_oauth_redis():
            auth_url, state = await handler.generate_authorization_url(user_id=user_id)
            is_valid, extracted_user_id = await handler.verify_oauth_state(state)

        assert is_valid is True
        assert extracted_user_id == user_id


class TestOAuthStateSecurityRequirements:
    """Security requirements for OAuth state handling."""

    def test_state_nonce_is_unique_per_request(self):
        """Each request should generate a unique nonce."""
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        handler = GoogleCalendarOAuthHandler()
        user_id = "same-user"

        # Generate multiple states for same user
        _, state1 = handler.generate_authorization_url(user_id=user_id)
        _, state2 = handler.generate_authorization_url(user_id=user_id)

        state1_data = _decode_oauth_state(state1)
        state2_data = _decode_oauth_state(state2)

        assert state1_data["nonce"] != state2_data["nonce"], "Each request must have unique nonce"

    def test_state_cannot_be_reused(self):
        """State should be consumed after first verification (single-use)."""
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        handler = GoogleCalendarOAuthHandler()
        user_id = "reuse-test-user"

        auth_url, state = handler.generate_authorization_url(user_id=user_id)

        # First verification should succeed
        is_valid1, user_id1 = handler.verify_state(state)
        assert is_valid1 is True

        # Second verification should fail (state consumed)
        is_valid2, user_id2 = handler.verify_state(state)
        assert is_valid2 is False, "State must be single-use"


# Helper functions for testing state encoding/decoding


def _decode_oauth_state(state: str) -> Optional[Dict[str, Any]]:
    """Decode OAuth state from base64 JSON to dict."""
    try:
        # Add padding if needed
        padded = state + "=" * (4 - len(state) % 4)
        decoded = base64.urlsafe_b64decode(padded)
        return json.loads(decoded)
    except (ValueError, json.JSONDecodeError):
        return None


def _encode_oauth_state(data: Dict[str, Any]) -> str:
    """Encode dict to OAuth state (base64 JSON)."""
    json_str = json.dumps(data)
    encoded = base64.urlsafe_b64encode(json_str.encode()).decode()
    return encoded.rstrip("=")
