"""#2174's check script: the token comes only from the environment, the call list is the
one Piper makes, and nothing about the token is printed."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
import github_app_token_check as chk  # noqa: E402


def test_refuses_without_the_env_token(capsys, monkeypatch):
    monkeypatch.delenv(chk.TOKEN_ENV, raising=False)
    assert chk.main(["--repo", "o/r", "--mcp-url", "http://x/mcp"]) == 2
    assert "refusing" in capsys.readouterr().out


def test_refuses_a_malformed_repo(monkeypatch, capsys):
    monkeypatch.setenv(chk.TOKEN_ENV, "t")
    assert chk.main(["--repo", "justaname", "--mcp-url", "http://x/mcp"]) == 2


def test_the_read_tools_are_the_ones_the_adapter_calls():
    src = (
        Path(__file__).resolve().parents[3] / "services/mcp/consumer/github_adapter.py"
    ).read_text()
    for name, _ in chk.read_tools("o", "r"):
        assert f'"{name}"' in src, name


def test_no_token_on_the_command_line():
    import argparse

    p = argparse.ArgumentParser()
    # the script defines no --token flag at all
    src = Path(chk.__file__).read_text()
    assert "--token" not in src
    assert p  # placeholder so the test has a body beyond the read
