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
