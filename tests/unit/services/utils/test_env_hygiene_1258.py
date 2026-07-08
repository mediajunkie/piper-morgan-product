"""#1258 — strip present-but-empty Anthropic vars before dotenv."""

import os

from services.utils.env_hygiene import ANTHROPIC_ENV_VARS, strip_empty_anthropic_vars


def test_strips_only_empty_vars(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")           # Claude Code's empty export
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://gw.example")  # legit non-empty
    monkeypatch.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)        # absent
    monkeypatch.setenv("ANTHROPIC_CUSTOM_HEADERS", "")
    stripped = strip_empty_anthropic_vars()
    assert set(stripped) == {"ANTHROPIC_API_KEY", "ANTHROPIC_CUSTOM_HEADERS"}
    assert "ANTHROPIC_API_KEY" not in os.environ          # dotenv can now fill it
    assert os.environ["ANTHROPIC_BASE_URL"] == "https://gw.example"  # untouched
    assert "ANTHROPIC_AUTH_TOKEN" not in os.environ       # absent stays absent


def test_noop_when_nothing_empty(monkeypatch):
    for var in ANTHROPIC_ENV_VARS:
        monkeypatch.delenv(var, raising=False)
    assert strip_empty_anthropic_vars() == []


# --- #1324: prod dev-password guard ---


def test_prod_with_dev_default_password_warns(monkeypatch, caplog):
    import logging

    from services.utils.env_hygiene import warn_if_prod_uses_dev_password

    monkeypatch.setenv("PIPER_ENVIRONMENT", "production")
    monkeypatch.setenv("POSTGRES_PASSWORD", "dev_changeme_in_production")
    with caplog.at_level(logging.CRITICAL):
        assert warn_if_prod_uses_dev_password() is True
    assert "dev default in a production environment" in caplog.text


def test_prod_with_real_password_is_quiet(monkeypatch):
    from services.utils.env_hygiene import warn_if_prod_uses_dev_password

    monkeypatch.setenv("PIPER_ENVIRONMENT", "production")
    monkeypatch.setenv("POSTGRES_PASSWORD", "a-real-secret")
    assert warn_if_prod_uses_dev_password() is False


def test_non_prod_never_warns(monkeypatch):
    from services.utils.env_hygiene import warn_if_prod_uses_dev_password

    monkeypatch.delenv("PIPER_ENVIRONMENT", raising=False)
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.setenv("POSTGRES_PASSWORD", "dev_changeme_in_production")
    assert warn_if_prod_uses_dev_password() is False
