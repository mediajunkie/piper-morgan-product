"""seat_session.py and seat_read.py (ADR-084 D3, issue 2388): HOST's bounds, against a stub host.

Nothing here calls beta. The password and both cookie values are dummies, and every
output is searched for them.
"""

import importlib.util
import json
import stat
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
ACCOUNT = "web-seed-1386"
PASSWORD = "dummy-password-not-real-9f3a"
ACCESS = "dummy-access-cookie-value-71c2"
REFRESH = "dummy-refresh-cookie-value-55d0"
SECRETS = (PASSWORD, ACCESS, REFRESH)
CRED = "web-seed-1386-credentials-2026-10-20.txt"


def _load(name):
    scripts = str(ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def ss():
    return _load("seat_session")


@pytest.fixture
def sr(ss):
    return _load("seat_read")


@pytest.fixture
def shared(tmp_path, monkeypatch):
    monkeypatch.setenv("PIPER_SHARED", str(tmp_path))
    cred = tmp_path / CRED
    cred.write_text(f"username: {ACCOUNT}\npassword: {PASSWORD}\n")
    cred.chmod(0o600)
    return tmp_path


class StubHost:
    """Answers like beta for an account that holds nothing, unless told otherwise."""

    def __init__(self, ss, **over):
        self.ss = ss
        self.calls = []
        self.replies = {
            "/api/v1/auth/login": ss.Reply(
                200,
                json.dumps({"token": ACCESS, "username": ACCOUNT}).encode(),
                (
                    f"auth_token={ACCESS}; HttpOnly; Max-Age=86400; Path=/; SameSite=lax; Secure",
                    f"refresh_token={REFRESH}; HttpOnly; Max-Age=604800; Path=/; SameSite=lax; Secure",
                ),
            ),
            "/api/v1/auth/me": ss.Reply(200, json.dumps({"username": ACCOUNT}).encode()),
            "/api/v1/admin/account-flags": ss.Reply(403, b""),
            "/api/v1/keys/list": ss.Reply(200, b"[]"),
            "/api/v1/integrations/health": ss.Reply(
                200,
                json.dumps(
                    {
                        "integrations": [
                            {"name": n, "status": "not_configured"}
                            for n in ("notion", "slack", "github", "calendar")
                        ]
                    }
                ).encode(),
            ),
            "/api/v1/settings/mcp-connections": ss.Reply(
                200, json.dumps({"oauth_connections": [], "manual_tokens": []}).encode()
            ),
        }
        self.replies.update(over)

    def __call__(self, method, path, data, headers):
        self.calls.append((method, path, data, dict(headers)))
        return self.replies[path.split("?")[0]]


def _run_main(mod, argv, capsys):
    code = mod.main(argv)
    out = capsys.readouterr()
    return code, out.out + out.err


def test_saves_and_prints_name_and_expiry_only(ss, shared):
    line = ss.run(ACCOUNT, StubHost(ss), now=1_800_000_000)
    assert line == f"{ACCOUNT} session saved, expires 2027-01-16T08:00:00Z"
    for secret in SECRETS:
        assert secret not in line
    saved = shared / f"{ACCOUNT}.session-token.json"
    assert stat.S_IMODE(saved.stat().st_mode) == 0o600
    state = json.loads(saved.read_text())
    assert {c["name"] for c in state["cookies"]} == {"auth_token", "refresh_token"}
    assert state["host"] == ss.HOST and state["account"] == ACCOUNT


def test_session_file_name_matches_the_fleet_deny(ss):
    assert "token" in ss.session_path(ACCOUNT).name
    assert all("credential" in a.credential_file for a in ss.ACCOUNTS.values())


def test_refuses_a_name_not_on_the_list(ss, shared, capsys):
    host = StubHost(ss)
    with pytest.raises(ss.Refused, match="not on the list"):
        ss.run("xian", host)
    assert host.calls == []


def test_host_is_fixed_and_is_beta(ss):
    assert ss.HOST == "https://beta.pipermorgan.ai"
    with pytest.raises(SystemExit):  # no --host option exists
        ss.main(["--account", ACCOUNT, "--host", "https://example.invalid"])


def test_password_goes_in_the_form_body_only(ss, shared):
    host = StubHost(ss)
    ss.run(ACCOUNT, host)
    method, path, data, headers = host.calls[0]
    assert (method, path) == ("POST", "/api/v1/auth/login")
    assert PASSWORD.encode() in data
    for _, later_path, later_data, later_headers in host.calls[1:]:
        assert later_data is None
        assert PASSWORD not in later_path and PASSWORD not in json.dumps(later_headers)


def test_forced_failed_sign_in_prints_no_secret(ss, shared, capsys):
    host = StubHost(ss)
    host.replies["/api/v1/auth/login"] = ss.Reply(401, PASSWORD.encode(), (f"auth_token={ACCESS}",))
    ss.run.__defaults__ = (host, None)
    code, text = _run_main(ss, ["--account", ACCOUNT], capsys)
    assert code == 2
    assert "refused: sign-in was refused by the host" in text
    for secret in SECRETS:
        assert secret not in text
    assert not (shared / f"{ACCOUNT}.session-token.json").exists()


def test_unexpected_error_prints_class_name_only(ss, shared, capsys):
    def boom(method, path, data, headers):
        raise RuntimeError(f"leaky {PASSWORD} {ACCESS}")

    ss.run.__defaults__ = (boom, None)
    code, text = _run_main(ss, ["--account", ACCOUNT], capsys)
    assert code == 3 and "unexpected RuntimeError" in text
    for secret in SECRETS:
        assert secret not in text


@pytest.mark.parametrize(
    "path, reply, reason",
    [
        ("/api/v1/auth/me", (200, {"username": "someone-else"}), "not the named account"),
        ("/api/v1/admin/account-flags", (200, {"found": True}), "is an admin"),
        ("/api/v1/admin/account-flags", (503, {}), "admin check could not be read"),
        ("/api/v1/keys/list", (200, [{"provider": "anthropic"}]), "holds a provider key"),
        ("/api/v1/keys/list", (500, []), "provider-key check could not be read"),
        ("/api/v1/keys/list", (200, {"keys": []}), "provider-key check could not be read"),
        (
            "/api/v1/integrations/health",
            (200, {"integrations": [{"name": "github", "status": "connected"}]}),
            "has a connection",
        ),
        ("/api/v1/integrations/health", (200, {}), "connection check could not be read"),
        (
            "/api/v1/settings/mcp-connections",
            (200, {"oauth_connections": [{"client_id": "x"}], "manual_tokens": []}),
            "has a connector",
        ),
        (
            "/api/v1/settings/mcp-connections",
            (200, {"oauth_connections": [], "manual_tokens": [{"id": 1}]}),
            "has a connector",
        ),
        (
            "/api/v1/settings/mcp-connections",
            (200, {"oauth_connections": []}),
            "connector check could not be read",
        ),
    ],
)
def test_refuses_to_save_when_the_account_holds_something_or_a_check_fails(
    ss, shared, path, reply, reason
):
    status, body = reply
    host = StubHost(ss, **{path: ss.Reply(status, json.dumps(body).encode())})
    with pytest.raises(ss.Refused, match=reason):
        ss.run(ACCOUNT, host)
    assert not (shared / f"{ACCOUNT}.session-token.json").exists()


def test_unreadable_check_body_refuses(ss, shared):
    host = StubHost(ss, **{"/api/v1/keys/list": ss.Reply(200, b"<html>")})
    with pytest.raises(ss.Refused, match="unreadable"):
        ss.run(ACCOUNT, host)


def test_refuses_a_credential_file_others_can_read(ss, shared):
    (shared / CRED).chmod(0o644)
    host = StubHost(ss)
    with pytest.raises(ss.Refused, match="not mode 0600"):
        ss.run(ACCOUNT, host)
    assert host.calls == []


def test_reads_key_equals_value_and_email_key(ss, shared):
    (shared / CRED).write_text(f"# note\nemail={ACCOUNT}\npassword='{PASSWORD}'\n")
    (shared / CRED).chmod(0o600)
    assert ss.read_credentials(shared / CRED) == (ACCOUNT, PASSWORD)


def test_missing_credential_file_refuses_without_a_path(ss, shared, capsys):
    (shared / CRED).unlink()
    ss.run.__defaults__ = (StubHost(ss), None)
    code, text = _run_main(ss, ["--account", ACCOUNT], capsys)
    assert code == 2 and "credential file not readable" in text
    assert str(shared) not in text


# --- seat_read.py -----------------------------------------------------------


def _saved(ss, shared):
    ss.run(ACCOUNT, StubHost(ss), now=1_800_000_000)


def test_read_sends_the_cookies_and_returns_the_body(ss, sr, shared):
    _saved(ss, shared)
    host = StubHost(ss, **{"/api/v1/admin/floored-actions": ss.Reply(200, b'{"rows": []}')})
    body = sr.read(ACCOUNT, "/api/v1/admin/floored-actions?days=30", host, now=1_800_000_100)
    assert body == '{"rows": []}'
    method, path, data, headers = host.calls[0]
    assert method == "GET" and data is None
    assert ACCESS in headers["Cookie"]


@pytest.mark.parametrize(
    "path", ["/api/v1/auth/me", "/api/v1/auth/refresh", "/API/v1/AUTH/login", "/auth/login"]
)
def test_read_refuses_the_sign_in_routes(ss, sr, shared, path):
    _saved(ss, shared)
    host = StubHost(ss)
    with pytest.raises(ss.Refused, match="sign-in routes"):
        sr.read(ACCOUNT, path, host, now=1_800_000_100)
    assert host.calls == []


@pytest.mark.parametrize("path", ["https://evil.example/x", "//evil.example/x", "api/v1/x"])
def test_read_refuses_anything_that_is_not_a_path_on_the_host(ss, sr, shared, path):
    _saved(ss, shared)
    host = StubHost(ss)
    with pytest.raises(ss.Refused, match="one slash"):
        sr.read(ACCOUNT, path, host, now=1_800_000_100)
    assert host.calls == []


def test_read_does_not_print_a_body_that_echoes_a_cookie(ss, sr, shared, capsys):
    _saved(ss, shared)
    host = StubHost(ss, **{"/api/v1/echo": ss.Reply(200, f"token={REFRESH}".encode())})
    sr.read.__defaults__ = (host, 1_800_000_100)
    code, text = _run_main(sr, ["--account", ACCOUNT, "/api/v1/echo"], capsys)
    assert code == 2 and "not printed" in text
    for secret in SECRETS:
        assert secret not in text


def test_read_refuses_an_expired_session(ss, sr, shared):
    _saved(ss, shared)
    with pytest.raises(ss.Refused, match="expired"):
        sr.read(ACCOUNT, "/api/v1/x", StubHost(ss), now=1_800_000_000 + 86401)


def test_read_refuses_without_a_saved_session(ss, sr, shared):
    with pytest.raises(ss.Refused, match="no saved session"):
        sr.read(ACCOUNT, "/api/v1/x", StubHost(ss))


def test_read_refuses_a_name_not_on_the_list(ss, sr, shared):
    with pytest.raises(ss.Refused, match="not on the list"):
        sr.read("xian", "/api/v1/x", StubHost(ss))


def test_read_reports_a_non_200_as_a_status_only(ss, sr, shared, capsys):
    _saved(ss, shared)
    host = StubHost(ss, **{"/api/v1/gone": ss.Reply(404, ACCESS.encode())})
    sr.read.__defaults__ = (host, 1_800_000_100)
    code, text = _run_main(sr, ["--account", ACCOUNT, "/api/v1/gone"], capsys)
    assert code == 2 and "answered 404" in text and ACCESS not in text


def test_neither_script_follows_a_redirect(ss):
    import inspect

    source = inspect.getsource(ss.http_transport)
    assert "NoRedirect" in source and "return None" in source


@pytest.mark.parametrize(
    "text, reason",
    [
        (
            f"name: {ACCOUNT}\npassword: {PASSWORD}\n",
            "no sign-in name key; expected one of username, user, email, login",
        ),
        (
            f"username: {ACCOUNT}\nsecret: {PASSWORD}\n",
            "no password key; expected one of password, pass",
        ),
    ],
)
def test_a_key_name_mismatch_names_the_expected_key_and_nothing_from_the_file(
    ss, shared, capsys, text, reason
):
    (shared / CRED).write_text(text)
    (shared / CRED).chmod(0o600)
    ss.run.__defaults__ = (StubHost(ss), None)
    code, out = _run_main(ss, ["--account", ACCOUNT], capsys)
    assert code == 2 and reason in out
    assert PASSWORD not in out and "secret" not in out and "name:" not in out
