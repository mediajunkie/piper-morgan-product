"""#2174's check script: the token comes only from the environment, the call list is the
one Piper makes, and nothing about the token is printed."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
import github_app_token_check as chk  # noqa: E402


def test_refuses_without_the_env_token(capsys, monkeypatch):
    monkeypatch.delenv(chk.TOKEN_ENV, raising=False)
    assert (
        chk.main(
            ["--repo", "o/r", "--mcp-url", "http://x/mcp", "--uninstalled-private-repo", "o/p"]
        )
        == 2
    )
    assert "refusing" in capsys.readouterr().out


def test_refuses_a_malformed_repo(monkeypatch, capsys):
    monkeypatch.setenv(chk.TOKEN_ENV, "t")
    assert (
        chk.main(
            [
                "--repo",
                "justaname",
                "--mcp-url",
                "http://x/mcp",
                "--uninstalled-private-repo",
                "o/p",
            ]
        )
        == 2
    )


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


def test_writes_refuse_any_repo_but_the_test_one(monkeypatch, capsys):
    """Arch 20:21: a mistyped repo can't take a write."""
    monkeypatch.setenv(chk.TOKEN_ENV, "t")
    code = chk.main(
        [
            "--repo",
            "someone/real-repo",
            "--mcp-url",
            "http://x/mcp",
            "--writes",
            "--uninstalled-private-repo",
            "o/p",
        ]
    )
    assert code == 2 and "refusing" in capsys.readouterr().out


def test_the_narrowing_row_passes_only_when_github_refuses(monkeypatch):
    import asyncio

    class _R:
        def __init__(self, s):
            self.status = s

        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

    class _S:
        def __init__(self, s):
            self.s = s

        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

        def get(self, url):
            return _R(self.s)

    for status, want in [(404, "PASS"), (403, "PASS"), (200, "FAIL readable (200)")]:
        monkeypatch.setattr("aiohttp.ClientSession", lambda headers=None, _s=status: _S(_s))
        assert asyncio.run(chk.run_narrowing("t", "o/p"))[0][1] == want


def _reply(text):
    from types import SimpleNamespace

    return SimpleNamespace(content=[SimpleNamespace(text=text)], isError=False)


def test_the_issue_number_comes_from_the_url_when_the_reply_has_none():
    """#2174 (xian 11-07 16:23): the create reply carried no 'number'; #43 was made."""
    from scripts.github_app_token_check import _first_issue_number

    url = "https://github.com/dinp-machine/piper-test-activity/issues/43"
    assert _first_issue_number(_reply('{"id": 1, "html_url": "' + url + '"}')) == 43
    assert _first_issue_number(_reply('{"id": 1, "url": "' + url + '"}')) == 43
    assert _first_issue_number(_reply("created " + url)) == 43
    assert _first_issue_number(_reply('{"number": 7}')) == 7
    assert _first_issue_number(_reply('{"id": 1}')) is None


def test_issue_needs_writes(monkeypatch, capsys):
    from scripts import github_app_token_check as m

    monkeypatch.setenv(m.TOKEN_ENV, "x")
    rc = m.main(
        [
            "--repo",
            m.WRITES_ALLOWED_REPO,
            "--mcp-url",
            "http://x",
            "--uninstalled-private-repo",
            "a/b",
            "--issue",
            "43",
        ]
    )
    assert rc == 2
    assert "--issue needs --writes" in capsys.readouterr().out
