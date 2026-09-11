"""#1711 — bounded-timeout guard around keyring calls in KeychainService.

The bug: on macOS, SecItemCopyMatching blocks INDEFINITELY (0% CPU, GUI
permission dialog nobody headless can see) when the keychain item exists but
the requesting python binary differs from the ACL'd one (rebuilt venv, second
checkout). Server startup froze silently at "Validating LLM providers...".

The fix under test: every raw keyring call runs in a worker thread with a
bounded join (default 5s, PIPER_KEYCHAIN_TIMEOUT_SECONDS configurable). On
timeout: a LOUD actionable error (phrases literal-pinned below), reads fail
through to the env-var fallback (resolution order unchanged), and the hang is
memoized process-wide so later calls short-circuit instead of re-paying the
timeout or parking more stuck threads.
"""

import threading
import time
from unittest.mock import patch

import pytest

from services.config.llm_config_service import LLMConfigService
from services.infrastructure import keychain_service as keychain_module
from services.infrastructure.keychain_service import (
    DEFAULT_KEYCHAIN_TIMEOUT_SECONDS,
    KEYCHAIN_HANG_GUIDANCE,
    KEYCHAIN_TIMEOUT_ENV_VAR,
    KeychainService,
    KeychainTimeoutError,
    _keychain_timeout_seconds,
    _reset_keychain_hang_for_tests,
)

# Simulated ACL hang: a keyring backend call that blocks until released.
# An Event (set at teardown) rather than a bare sleep, so abandoned daemon
# workers exit promptly instead of lingering for the sleep duration.
_release = threading.Event()


def _hanging_keyring_call(*args, **kwargs):
    """Stands in for SecItemCopyMatching waiting on the permission dialog."""
    _release.wait(30)
    return None


@pytest.fixture(autouse=True)
def _isolate(monkeypatch):
    """Fresh hang-memo + fast timeout + FORCED keychain store, per test.

    PIPER_CREDENTIAL_STORE=keychain (not merely unset): the code under test is
    the #1711 timeout guard around raw keyring calls, which only exists on the
    OS-keyring path. On CI's ubuntu runners keyring resolves to the fail
    backend, so an unforced KeychainService routes to the #1382 DB store (or
    the no-secure-store refusal) and never reaches `_keyring_call` — the
    patched hanging keyring function is never invoked and the write test
    reported "DID NOT RAISE". Forcing `keychain` exercises the guard
    identically under both backends; on macOS it changes nothing (that is the
    auto-selected path already).
    """
    _reset_keychain_hang_for_tests()
    _release.clear()
    monkeypatch.setenv("PIPER_CREDENTIAL_STORE", "keychain")
    monkeypatch.setenv(KEYCHAIN_TIMEOUT_ENV_VAR, "0.2")
    yield
    _release.set()  # release any abandoned worker threads
    _reset_keychain_hang_for_tests()


@pytest.fixture
def service(_isolate):
    # Depends on _isolate explicitly: the forced-store env var must be set
    # BEFORE construction (store selection happens in __init__).
    return KeychainService(service_name="piper-test-1711")


class TestHangDetection:
    def test_hung_read_returns_none_within_bounded_time(self, service):
        """The startup killer: a hung get_password no longer blocks forever."""
        with patch("keyring.get_password", _hanging_keyring_call):
            start = time.monotonic()
            result = service.get_api_key("anthropic")
            elapsed = time.monotonic() - start

        assert result is None  # truthfully empty from this store
        assert elapsed < 2.0  # bounded (0.2s timeout + slack), not indefinite

    def test_timeout_error_names_the_actual_fix(self, service):
        """LOUD + actionable: the error names every escape hatch (pinned)."""
        with patch("keyring.get_password", _hanging_keyring_call):
            with pytest.raises(KeychainTimeoutError) as exc_info:
                service._keyring_call("get_password", _hanging_keyring_call, "svc", "name")

        message = str(exc_info.value)
        assert "macOS Keychain is waiting for a permission dialog for this python binary" in message
        assert "'Always Allow'" in message
        assert "PIPER_CREDENTIAL_STORE=db" in message
        assert "previously-authorized environment" in message
        # And the guidance constant itself carries the same phrases (it is
        # what the structured log's `fix=` field emits).
        assert "'Always Allow'" in KEYCHAIN_HANG_GUIDANCE
        assert "PIPER_CREDENTIAL_STORE=db" in KEYCHAIN_HANG_GUIDANCE

    def test_hang_is_memoized_process_wide(self, service):
        """Second read short-circuits: no second timeout wait, no new thread."""
        with patch("keyring.get_password", _hanging_keyring_call):
            assert service.get_api_key("anthropic") is None  # pays the timeout

            before = threading.active_count()
            start = time.monotonic()
            assert service.get_api_key("openai") is None
            elapsed = time.monotonic() - start
            after = threading.active_count()

        assert elapsed < 0.05  # immediate, did not re-pay the 0.2s timeout
        assert after <= before  # no additional stuck worker parked

        # And the memo is process-wide, not per-instance: a DIFFERENT
        # KeychainService (startup constructs several) also short-circuits.
        other = KeychainService(service_name="piper-test-1711-other")
        start = time.monotonic()
        assert other.get_api_key("anthropic") is None
        assert time.monotonic() - start < 0.05

    def test_hung_write_raises_with_guidance(self, service):
        """store_api_key surfaces the timeout loudly instead of hanging."""
        with patch("keyring.set_password", _hanging_keyring_call):
            with pytest.raises(RuntimeError) as exc_info:
                service.store_api_key("anthropic", "sk-test")
        assert "PIPER_CREDENTIAL_STORE=db" in str(exc_info.value)

    def test_hung_delete_returns_false(self, service):
        with patch("keyring.delete_password", _hanging_keyring_call):
            assert service.delete_api_key("anthropic") is False


class TestFailThrough:
    def test_resolution_order_proceeds_to_env_var(self, service, monkeypatch):
        """The server comes up keyless-but-honest: a hung keychain read falls
        through to the env-var fallback (documented resolution order), so
        startup validation proceeds instead of freezing."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-env-fallback")
        config = LLMConfigService(keychain_service=service)

        with patch("keyring.get_password", _hanging_keyring_call):
            start = time.monotonic()
            key = config.get_api_key("anthropic")
            elapsed = time.monotonic() - start

        assert key == "sk-env-fallback"
        assert elapsed < 2.0

    def test_no_keys_anywhere_returns_none_not_hang(self, service, monkeypatch):
        """Truly keyless after a hang → None (the /setup wizard funnel),
        never an exception, never a block."""
        for var in (
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "GEMINI_API_KEY",
            "PERPLEXITY_API_KEY",
        ):
            monkeypatch.delenv(var, raising=False)
        config = LLMConfigService(keychain_service=service)

        with patch("keyring.get_password", _hanging_keyring_call):
            assert config.get_api_key("anthropic") is None


class TestFastPathUnchanged:
    def test_fast_read_returns_value(self, service):
        with patch("keyring.get_password", return_value="sk-fast"):
            assert service.get_api_key("anthropic") == "sk-fast"

    def test_fast_missing_key_returns_none(self, service):
        with patch("keyring.get_password", return_value=None):
            assert service.get_api_key("anthropic") is None

    def test_fast_write_and_delete_pass_through(self, service):
        with patch("keyring.set_password", return_value=None) as set_pw:
            service.store_api_key("anthropic", "sk-x")
        set_pw.assert_called_once_with("piper-test-1711", "anthropic_api_key", "sk-x")

        with patch("keyring.delete_password", return_value=None) as del_pw:
            assert service.delete_api_key("anthropic") is True
        del_pw.assert_called_once_with("piper-test-1711", "anthropic_api_key")

    def test_backend_errors_still_propagate(self, service):
        """Real backend exceptions cross the thread boundary unchanged."""
        with patch("keyring.get_password", side_effect=ValueError("backend boom")):
            # get_api_key's existing generic handler converts to None
            assert service.get_api_key("anthropic") is None
        with pytest.raises(ValueError, match="backend boom"):
            service._keyring_call(
                "get_password",
                lambda *a: (_ for _ in ()).throw(ValueError("backend boom")),
                "svc",
                "name",
            )


class TestTimeoutConfig:
    def test_default_when_unset(self, monkeypatch):
        monkeypatch.delenv(KEYCHAIN_TIMEOUT_ENV_VAR, raising=False)
        assert _keychain_timeout_seconds() == DEFAULT_KEYCHAIN_TIMEOUT_SECONDS

    def test_env_var_overrides(self, monkeypatch):
        monkeypatch.setenv(KEYCHAIN_TIMEOUT_ENV_VAR, "12.5")
        assert _keychain_timeout_seconds() == 12.5

    def test_invalid_value_falls_back_to_default(self, monkeypatch):
        monkeypatch.setenv(KEYCHAIN_TIMEOUT_ENV_VAR, "not-a-number")
        assert _keychain_timeout_seconds() == DEFAULT_KEYCHAIN_TIMEOUT_SECONDS

    def test_zero_disables_guard_calls_directly(self, service, monkeypatch):
        """timeout <= 0 → direct call, no worker thread involved."""
        monkeypatch.setenv(KEYCHAIN_TIMEOUT_ENV_VAR, "0")
        with patch.object(keychain_module.threading, "Thread") as thread_cls:
            result = service._keyring_call("get_password", lambda *a: "direct", "s", "n")
        assert result == "direct"
        thread_cls.assert_not_called()
