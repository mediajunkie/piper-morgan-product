"""#1387 — the plaintext-write fallback is dev-only, ENFORCED.

Arch's #1278 boundary-check found: with ENCRYPTION_MASTER_KEY unset, the
encrypted column types logged one warning and wrote PLAINTEXT ("non-prod
fallback" that nothing restricted to non-prod). Reads were fail-closed;
writes were not. A host cutover booting before the secret is set would
silently write tester PII as plaintext — discovered by audit, not runtime.

Contract pinned: production + no key = FATAL write; dev/test + no key =
fallback preserved (keyless local runs still work).
"""

import pytest

from services.security.encrypted_types import EncryptedJSON, EncryptedString


def _keyless(monkeypatch, env: str | None):
    monkeypatch.delenv("ENCRYPTION_MASTER_KEY", raising=False)
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    if env is None:
        monkeypatch.delenv("PIPER_ENVIRONMENT", raising=False)
    else:
        monkeypatch.setenv("PIPER_ENVIRONMENT", env)


class TestProdFatal:
    def test_encrypted_string_write_raises_in_production(self, monkeypatch):
        _keyless(monkeypatch, "production")
        t = EncryptedString(context="test.col")
        with pytest.raises(RuntimeError, match="refusing to write plaintext"):
            t.process_bind_param("tester PII", dialect=None)

    def test_encrypted_json_write_raises_in_production(self, monkeypatch):
        _keyless(monkeypatch, "production")
        t = EncryptedJSON(context="test.col")
        with pytest.raises(RuntimeError, match="#1387"):
            t.process_bind_param({"private": "thing"}, dialect=None)

    def test_environment_var_spelling_also_fatal(self, monkeypatch):
        """The guard honors ENVIRONMENT too (both spellings exist in the repo)."""
        monkeypatch.delenv("ENCRYPTION_MASTER_KEY", raising=False)
        monkeypatch.delenv("PIPER_ENVIRONMENT", raising=False)
        monkeypatch.setenv("ENVIRONMENT", "production")
        with pytest.raises(RuntimeError):
            EncryptedString(context="t.c").process_bind_param("x", dialect=None)


class TestDevFallbackPreserved:
    def test_dev_keyless_write_still_passes_through(self, monkeypatch):
        _keyless(monkeypatch, "development")
        assert (
            EncryptedString(context="t.c").process_bind_param("v", dialect=None) == "v"
        )

    def test_no_env_at_all_keeps_fallback(self, monkeypatch):
        """Unset environment (plain local runs) is NOT treated as production."""
        _keyless(monkeypatch, None)
        assert (
            EncryptedJSON(context="t.c").process_bind_param({"a": 1}, dialect=None)
            == {"a": 1}
        )


class TestWithKeyUnaffected:
    def test_production_with_key_encrypts_normally(self, monkeypatch):
        monkeypatch.setenv("PIPER_ENVIRONMENT", "production")
        monkeypatch.setenv("ENCRYPTION_MASTER_KEY", "Y2ktdGVzdC1vbmx5LTEzODItbmV2ZXItcHJvZCEhMzI=")
        out = EncryptedString(context="t.c").process_bind_param("v", dialect=None)
        assert out.startswith("PMENC1:")  # encrypted, not plaintext
