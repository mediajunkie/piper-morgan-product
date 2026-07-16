"""#1415: LLM provider SELECTION resolves per-user, consent fails CLOSED.

The incident (2026-07-16): provider selection read GLOBAL keychain slots, so
one tester's setup pinned the whole instance to a quota-dead provider and a
second user's per-user key was un-selectable — every turn 429'd. And the #946
consent filter failed OPEN on any keychain error (census F1), silently routing
messages to de-authorized providers.

Pinned here:
  - the resolution chains (per-user -> server -> env -> first), stateless
  - THE INCIDENT SCENARIO: global slots pinned to a dead provider, the acting
    user's own choice wins anyway
  - consent fail-CLOSED (server-default only, never all-configured)
  - resilience never overrides consent (fallback set is consent-filtered)
  - identity threads from LLMClient.complete() into selection
"""

from typing import Dict, Optional
from unittest.mock import AsyncMock, patch

import pytest

from services.llm.provider_selection import (
    resolve_authorized_providers,
    resolve_default_provider,
)


class FakeKeychain:
    """Dict-backed stand-in honoring the (provider, username) slot shape."""

    def __init__(self, slots: Optional[Dict[tuple, str]] = None, raise_on: str = ""):
        self.slots = slots or {}
        self.raise_on = raise_on

    def get_api_key(self, provider: str, username: Optional[str] = None) -> Optional[str]:
        if self.raise_on and provider == self.raise_on:
            raise RuntimeError("keychain unavailable")
        return self.slots.get((provider, username))


AVAILABLE = ["anthropic", "openai"]


# ---------------------------------------------------------------------------
# resolve_default_provider — the selection chain
# ---------------------------------------------------------------------------


class TestDefaultProviderChain:
    def test_two_users_get_their_own_choices(self):
        kc = FakeKeychain(
            {
                ("default_llm_provider", "user-a"): "anthropic",
                ("default_llm_provider", "user-b"): "openai",
                ("default_llm_provider", None): "openai",  # global pin must not matter
            }
        )
        assert resolve_default_provider("user-a", AVAILABLE, keychain=kc) == "anthropic"
        assert resolve_default_provider("user-b", AVAILABLE, keychain=kc) == "openai"

    def test_incident_scenario_user_choice_beats_global_pin(self):
        """2026-07-16: global slot pinned to (dead) openai by another tester's
        setup; the acting user's own per-user choice must win."""
        kc = FakeKeychain(
            {
                ("default_llm_provider", None): "openai",
                ("default_llm_provider", "dinp"): "anthropic",
            }
        )
        assert resolve_default_provider("dinp", AVAILABLE, keychain=kc) == "anthropic"

    def test_no_user_choice_falls_to_global_then_env_then_first(self):
        kc_global = FakeKeychain({("default_llm_provider", None): "openai"})
        assert resolve_default_provider("user-x", AVAILABLE, keychain=kc_global) == "openai"

        kc_empty = FakeKeychain()
        assert (
            resolve_default_provider("user-x", AVAILABLE, env_default="openai", keychain=kc_empty)
            == "openai"
        )
        assert resolve_default_provider("user-x", AVAILABLE, keychain=kc_empty) == "anthropic"

    def test_unavailable_user_choice_falls_through_never_locks_out(self):
        """PM: selection must never lock a user out — a stored choice pointing
        at an unavailable provider degrades to the next step, not a hard fail."""
        kc = FakeKeychain({("default_llm_provider", "user-a"): "gemini"})  # not in AVAILABLE
        assert resolve_default_provider("user-a", AVAILABLE, keychain=kc) == "anthropic"

    def test_empty_available_returns_none(self):
        assert resolve_default_provider("user-a", [], keychain=FakeKeychain()) is None

    def test_keychain_error_degrades_to_env_default(self):
        kc = FakeKeychain(raise_on="default_llm_provider")
        assert (
            resolve_default_provider("user-a", AVAILABLE, env_default="openai", keychain=kc)
            == "openai"
        )


# ---------------------------------------------------------------------------
# resolve_authorized_providers — consent (#946) with F1 fail-closed
# ---------------------------------------------------------------------------


class TestConsentFilter:
    CONFIGURED = ["anthropic", "openai", "gemini"]

    def test_per_user_list_wins_over_global(self):
        kc = FakeKeychain(
            {
                ("authorized_llm_providers", "user-a"): "anthropic",
                ("authorized_llm_providers", None): "openai,gemini",
            }
        )
        assert resolve_authorized_providers("user-a", self.CONFIGURED, "openai", kc) == [
            "anthropic"
        ]

    def test_global_list_applies_when_no_user_list(self):
        kc = FakeKeychain({("authorized_llm_providers", None): "openai"})
        assert resolve_authorized_providers("user-a", self.CONFIGURED, "openai", kc) == ["openai"]

    def test_legacy_no_lists_returns_all_configured(self):
        assert (
            resolve_authorized_providers("user-a", self.CONFIGURED, "openai", FakeKeychain())
            == self.CONFIGURED
        )

    def test_f1_read_error_fails_closed_to_server_default_only(self):
        """Census F1: the old code failed OPEN to all configured providers on a
        consent-read error — silently disabling the #946 boundary. Now: the
        server-default provider only."""
        kc = FakeKeychain(raise_on="authorized_llm_providers")
        assert resolve_authorized_providers("user-a", self.CONFIGURED, "openai", kc) == ["openai"]
        # and never the full set
        assert resolve_authorized_providers("user-a", self.CONFIGURED, "openai", kc) != (
            self.CONFIGURED
        )

    def test_f1_fail_closed_with_unconfigured_default_is_empty(self):
        kc = FakeKeychain(raise_on="authorized_llm_providers")
        assert resolve_authorized_providers("user-a", self.CONFIGURED, "mistral", kc) == []


# ---------------------------------------------------------------------------
# LLMClient identity threading + consent-filtered failure fallback
# ---------------------------------------------------------------------------


class _StubConfigService:
    """Per-user-aware stub: returns what a real (resolver-backed) service would."""

    def __init__(self):
        self.default_by_user = {"user-a": "anthropic", "user-b": "openai"}
        self.authorized_by_user = {"user-a": ["anthropic"], "user-b": ["openai", "anthropic"]}
        self.seen_user_ids = []

    def get_default_provider(self, user_id=None):
        self.seen_user_ids.append(user_id)
        return self.default_by_user.get(user_id, "openai")

    def get_configured_providers(self, user_id=None):
        return self.authorized_by_user.get(user_id, ["openai", "anthropic", "gemini"])


def _make_client(config_service):
    from services.llm.clients import LLMClient

    client = LLMClient.__new__(LLMClient)  # skip heavyweight __init__ (builds SDKs)
    client._config_service = config_service
    client._output_filter = None
    client.anthropic_client = object()
    client.openai_client = object()
    client.gemini_client = None
    return client


@pytest.mark.asyncio
async def test_selection_uses_the_acting_users_provider():
    cfg = _StubConfigService()
    client = _make_client(cfg)
    calls = []

    async def fake_call(provider, *a, **k):
        calls.append(provider.value)
        return "ok"

    with patch.object(type(client), "_call_provider", new=AsyncMock(side_effect=fake_call)):
        await client._complete_raw("conversation", "hi", user_id="user-a")
        await client._complete_raw("conversation", "hi", user_id="user-b")

    assert calls == ["anthropic", "openai"]
    assert cfg.seen_user_ids == ["user-a", "user-b"]


@pytest.mark.asyncio
async def test_failure_fallback_respects_user_consent():
    """user-a authorized ONLY anthropic. When anthropic fails, the client must
    NOT fall back to openai (configured on the server, de-authorized by the
    user) — resilience never overrides #946."""
    cfg = _StubConfigService()
    client = _make_client(cfg)
    attempted = []

    async def fake_call(provider, *a, **k):
        attempted.append(provider.value)
        raise RuntimeError("provider down")

    with patch.object(type(client), "_call_provider", new=AsyncMock(side_effect=fake_call)):
        with pytest.raises(RuntimeError, match="All configured LLM providers failed"):
            await client._complete_raw("conversation", "hi", user_id="user-a")

    assert attempted == ["anthropic"]  # openai never attempted


@pytest.mark.asyncio
async def test_failure_fallback_uses_authorized_alternate():
    """user-b authorized both: openai primary fails -> anthropic serves."""
    cfg = _StubConfigService()
    client = _make_client(cfg)
    attempted = []

    async def fake_call(provider, *a, **k):
        attempted.append(provider.value)
        if provider.value == "openai":
            raise RuntimeError("quota dead")
        return "served-by-fallback"

    with patch.object(type(client), "_call_provider", new=AsyncMock(side_effect=fake_call)):
        out = await client._complete_raw("conversation", "hi", user_id="user-b")

    assert out == "served-by-fallback"
    assert attempted[0] == "openai" and "anthropic" in attempted


@pytest.mark.asyncio
async def test_public_complete_threads_user_id_to_selection():
    cfg = _StubConfigService()
    client = _make_client(cfg)

    with patch.object(
        type(client), "_call_provider", new=AsyncMock(return_value="ok")
    ):
        await client.complete("conversation", "hi", user_id="user-a")

    assert cfg.seen_user_ids == ["user-a"]
