"""#2341: ADR-081 D3's refresh check as one command with hidden prompts.

Every "secret" in this file is a made-up string, not a credential.
"""

import argparse
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
_spec = importlib.util.spec_from_file_location(
    "github_app_refresh_check", ROOT / "scripts" / "github_app_refresh_check.py"
)
rc = importlib.util.module_from_spec(_spec)
sys.modules["github_app_refresh_check"] = rc
_spec.loader.exec_module(rc)

FAKE = {
    "client_id": "fake-client-id",
    "client_secret": "fake-client-secret",
    "refresh_token": "fake-old-refresh",
    "old_token": "fake-old-access",
}
NEW_ACCESS = "fake-new-access"
NEW_REFRESH = "fake-new-refresh"


def _ns(**kw):
    base = dict(
        repo=rc.DEFAULT_REPO, uninstalled_private_repo="o/private", issue=43, mcp_url="http://x/mcp"
    )
    base.update(kw)
    return argparse.Namespace(**base)


def _good_post(url, fields):
    assert url == rc.TOKEN_URL
    assert fields["grant_type"] == "refresh_token"
    return 200, {
        "access_token": NEW_ACCESS,
        "refresh_token": NEW_REFRESH,
        "expires_in": 28800,
        "refresh_token_expires_in": 15897600,
    }


def test_secrets_are_asked_hidden_and_once_each():
    asked = []
    answers = iter(FAKE.values())

    def ask(prompt):
        asked.append(prompt)
        return next(answers)

    assert rc.ask_secrets(ask) == FAKE
    assert len(asked) == 4
    assert all("input hidden" in a for a in asked)


def test_a_missing_required_secret_stops_the_run():
    with pytest.raises(SystemExit):
        rc.ask_secrets(lambda prompt: "")


def test_the_old_token_may_be_skipped():
    answers = iter(["a", "b", "c", ""])
    assert rc.ask_secrets(lambda p: next(answers))["old_token"] == ""
    assert "SKIPPED" in rc.old_token_line("")


def test_the_only_prompt_function_is_getpass():
    src = (ROOT / "scripts" / "github_app_refresh_check.py").read_text()
    assert "ask: Callable[[str], str] = getpass.getpass" in src
    # input() appears once: the yes/no about showing the new refresh token.
    assert src.count("input(") == 1


def test_a_good_refresh_reports_lifetimes_and_no_secret():
    reply, line = rc.refresh(FAKE, _good_post)
    assert reply["access_token"] == NEW_ACCESS
    assert "PASS" in line and "8 h" in line and "184 days" in line
    for secret in (*FAKE.values(), NEW_ACCESS, NEW_REFRESH):
        assert secret not in line


def test_a_failed_refresh_prints_githubs_error_code_only():
    reply, line = rc.refresh(FAKE, lambda u, f: (200, {"error": "bad_refresh_token"}))
    assert reply is None
    assert line.endswith("FAIL bad_refresh_token")
    for secret in FAKE.values():
        assert secret not in line


def test_the_old_token_line_passes_only_on_401():
    assert "PASS (HTTP 401" in rc.old_token_line("fake-old-access", lambda u, t: 401)
    assert "FAIL (HTTP 200" in rc.old_token_line("fake-old-access", lambda u, t: 200)


def test_no_secret_reaches_the_checks_command_line():
    argv = rc.check_argv(_ns(), "http://localhost:8082/mcp")
    joined = " ".join(argv)
    for secret in (*FAKE.values(), NEW_ACCESS, NEW_REFRESH):
        assert secret not in joined
    assert argv[-3:] == ["--writes", "--issue", "43"]
    assert "--writes" not in rc.check_argv(_ns(issue=None), "http://x/mcp")


def test_the_new_token_reaches_the_check_through_its_environment(monkeypatch):
    seen = {}

    class _Done:
        returncode = 0
        stdout = "noise\nrest GET /user  PASS\nmcp server  INFO github-mcp-server 1.5.0\n--- 1 calls: 1 pass, 0 fail\n"

    def fake_run(argv, env, capture_output, text, cwd):
        seen["argv"], seen["env"] = argv, env
        return _Done()

    monkeypatch.setattr(rc.subprocess, "run", fake_run)
    code, table = rc.run_check(_ns(), "http://x/mcp", NEW_ACCESS)
    assert code == 0
    assert seen["env"]["GITHUB_CHECK_TOKEN"] == NEW_ACCESS
    assert NEW_ACCESS not in " ".join(seen["argv"])
    assert "noise" not in table
    assert "INFO github-mcp-server 1.5.0" in table and table.endswith("1 pass, 0 fail")


def test_the_proxy_starts_with_the_update_check_off_and_no_secret(monkeypatch):
    seen = {}

    class _Proc:
        def poll(self):
            return None

    def fake_popen(argv, env, stdout, stderr):
        seen["argv"], seen["env"] = argv, env
        return _Proc()

    monkeypatch.setattr(rc.subprocess, "Popen", fake_popen)
    monkeypatch.setattr(rc, "_port_open", lambda port: True)
    rc.start_proxy()
    assert seen["argv"] == ["fly", "proxy", "8082:8082", "-a", "piper-morgan-gh-mcp"]
    assert seen["env"]["FLY_NO_UPDATE_CHECK"] == "1"


def _run_main(
    monkeypatch, capsys, post, check=(0, "rest GET /user  PASS"), answer="n", raises=None
):
    stopped = []
    monkeypatch.setattr(rc, "ask_secrets", lambda: dict(FAKE))
    monkeypatch.setattr(rc, "_post_form", post)
    monkeypatch.setattr(rc, "refresh", lambda s: rc.__dict__["_refresh_orig"](s, post))
    monkeypatch.setattr(
        rc, "old_token_line", lambda t: "old token GET /user          PASS (HTTP 401)"
    )
    monkeypatch.setattr(rc, "start_proxy", lambda: "proxy")
    monkeypatch.setattr(rc, "stop_proxy", lambda p: stopped.append(p))

    def fake_check(ns, url, token):
        if raises:
            raise raises
        return check[0], check[1] + f"\nleak {token} {NEW_REFRESH}"

    monkeypatch.setattr(rc, "run_check", fake_check)
    monkeypatch.setattr("builtins.input", lambda prompt: answer)
    try:
        code = rc.main(["--uninstalled-private-repo", "o/private", "--issue", "43"])
    except RuntimeError:
        code = "raised"
    return code, capsys.readouterr().out, stopped


rc._refresh_orig = rc.refresh


def test_the_block_carries_no_secret_even_if_a_step_echoes_one(monkeypatch, capsys):
    code, out, stopped = _run_main(monkeypatch, capsys, _good_post)
    block = out.split(rc.BLOCK_START)[1].split(rc.BLOCK_END)[0]
    for secret in (*FAKE.values(), NEW_ACCESS, NEW_REFRESH):
        assert secret not in block
    assert "[hidden]" in block and "refresh" in block and "old token GET /user" in block
    assert code == 0
    assert stopped == ["proxy"]
    assert NEW_REFRESH not in out


def test_the_new_refresh_token_is_shown_only_on_yes_and_outside_the_block(monkeypatch, capsys):
    _code, out, _ = _run_main(monkeypatch, capsys, _good_post, answer="y")
    before_end, after_end = out.split(rc.BLOCK_END)
    assert NEW_REFRESH not in before_end
    assert NEW_REFRESH in after_end
    assert NEW_ACCESS not in out


def test_a_failed_refresh_stops_before_the_proxy_and_the_check(monkeypatch, capsys):
    code, out, stopped = _run_main(
        monkeypatch, capsys, lambda u, f: (400, {"error": "bad_refresh_token"})
    )
    assert code == 1
    assert "FAIL bad_refresh_token" in out
    assert stopped == []
    assert "old token" not in out


def test_the_proxy_is_stopped_when_the_check_raises(monkeypatch, capsys):
    code, _out, stopped = _run_main(monkeypatch, capsys, _good_post, raises=RuntimeError("boom"))
    assert code == "raised"
    assert stopped == ["proxy"]
