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
FLOORED = "/api/v1/admin/floored-actions"


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
def shared(ss, tmp_path, monkeypatch):
    monkeypatch.setattr(ss, "shared_dir", lambda: tmp_path)
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
    assert {c["name"] for c in state["cookies"]} == {
        "auth_token"
    }  # the refresh cookie is never kept
    assert REFRESH not in saved.read_text()
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
        ("/api/v1/keys/list", (200, [{"provider": "openai"}]), "holds a provider key"),
        (
            "/api/v1/keys/list",
            (200, [{"provider": "anthropic"}, {"provider": "gemini"}]),
            "holds a provider key",
        ),
        ("/api/v1/keys/list", (200, [{"key": "x"}]), "holds a provider key"),
        ("/api/v1/keys/list", (500, []), "provider-key check could not be read"),
        ("/api/v1/keys/list", (200, {"keys": []}), "provider-key check could not be read"),
        (
            "/api/v1/integrations/health",
            (200, {"integrations": [{"name": "github", "status": "connected"}]}),
            "has a connection",
        ),
        ("/api/v1/integrations/health", (200, {}), "connection check could not be read"),
        (
            "/api/v1/integrations/health",
            (200, {"integrations": [{"name": "github", "status": "unknown"}]}),
            "connection check could not be read",
        ),
        (
            "/api/v1/integrations/health",
            (200, {"integrations": [{"name": "slack", "status": "failed"}]}),
            "has a connection",
        ),
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
    assert ACCESS in headers["Cookie"] and REFRESH not in headers["Cookie"]
    assert path == "/api/v1/admin/floored-actions?days=30"


@pytest.mark.parametrize(
    "path",
    [
        "/api/v1/auth/me",
        "/api/v1/auth/refresh",
        "/API/v1/AUTH/login",
        "/auth/login",
        "/api/v1/keys/list",
        "/api/v1/settings/mcp-connections",
        "/api/v1/admin/account-flags?username=x",
        "/api/v1/admin/floored-actions/",
        "/",
    ],
)
def test_read_refuses_every_path_off_the_closed_list(ss, sr, shared, path):
    _saved(ss, shared)
    host = StubHost(ss)
    with pytest.raises(ss.Refused, match="not on the list"):
        sr.read(ACCOUNT, path, host, now=1_800_000_100)
    assert host.calls == []


@pytest.mark.parametrize(
    "path",
    [
        "https://evil.example/x",
        "//evil.example/x",
        "api/v1/admin/floored-actions",
        "/api/v1/x/../admin/floored-actions",
        "/api/v1//admin/floored-actions",
        "/./api/v1/admin/floored-actions/..",
        "/api/v1/admin/%66loored-actions",
        "/api/v1/admin/floored-actions#frag",
        "/api/v1/admin/floored-actions?days=30;x=1",
        "/api/v1/admin/floored-actions?next=//evil.example",
        "/api/v1/admin/floored-actions?u=a@b",
    ],
)
def test_read_refuses_a_path_that_is_not_in_a_plain_form(ss, sr, shared, path):
    _saved(ss, shared)
    host = StubHost(ss)
    with pytest.raises(ss.Refused, match="plain form"):
        sr.read(ACCOUNT, path, host, now=1_800_000_100)
    assert host.calls == []


def test_read_does_not_print_a_body_that_echoes_a_cookie(ss, sr, shared, capsys):
    _saved(ss, shared)
    host = StubHost(ss, **{FLOORED: ss.Reply(200, f"token={ACCESS}".encode())})
    sr.read.__defaults__ = (host, 1_800_000_100)
    code, text = _run_main(sr, ["--account", ACCOUNT, FLOORED], capsys)
    assert code == 2 and "not printed" in text
    for secret in SECRETS:
        assert secret not in text


def test_read_refuses_an_expired_session(ss, sr, shared):
    _saved(ss, shared)
    with pytest.raises(ss.Refused, match="expired"):
        sr.read(ACCOUNT, FLOORED, StubHost(ss), now=1_800_000_000 + 86401)


def test_read_refuses_without_a_saved_session(ss, sr, shared):
    with pytest.raises(ss.Refused, match="no saved session"):
        sr.read(ACCOUNT, FLOORED, StubHost(ss))


def test_read_refuses_a_name_not_on_the_list(ss, sr, shared):
    with pytest.raises(ss.Refused, match="not on the list"):
        sr.read("xian", FLOORED, StubHost(ss))


def test_read_reports_a_non_200_as_a_status_only(ss, sr, shared, capsys):
    _saved(ss, shared)
    host = StubHost(ss, **{FLOORED: ss.Reply(404, ACCESS.encode())})
    sr.read.__defaults__ = (host, 1_800_000_100)
    code, text = _run_main(sr, ["--account", ACCOUNT, FLOORED], capsys)
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


def test_the_key_check_asks_for_inactive_keys_too(ss, shared):
    host = StubHost(ss)
    ss.run(ACCOUNT, host)
    assert any(path == "/api/v1/keys/list?active_only=false" for _, path, _, _ in host.calls)


def test_expiry_is_capped_in_code_whatever_the_host_says(ss, shared):
    host = StubHost(ss)
    host.replies["/api/v1/auth/login"] = ss.Reply(
        200, b"{}", (f"auth_token={ACCESS}; HttpOnly; Max-Age=99999999; Path=/",)
    )
    ss.run(ACCOUNT, host, now=1_800_000_000)
    state = json.loads((shared / f"{ACCOUNT}.session-token.json").read_text())
    assert state["cookies"][0]["expires"] == 1_800_000_000 + 86400
    assert ss.MAX_SESSION_SECONDS == 86400


def test_no_environment_value_moves_the_shared_folder(monkeypatch, tmp_path):
    monkeypatch.setenv("PIPER_SHARED", str(tmp_path))
    fresh = _load("seat_session")
    assert fresh.shared_dir() == Path.home() / ".piper-shared"


def test_a_line_splits_on_whichever_separator_comes_first(ss, shared):
    (shared / CRED).write_text(f"username={ACCOUNT}\npassword=ab:cd\n")
    (shared / CRED).chmod(0o600)
    assert ss.read_credentials(shared / CRED) == (ACCOUNT, "ab:cd")
    (shared / CRED).write_text(f"username: {ACCOUNT}\npassword: ab=cd\n")
    assert ss.read_credentials(shared / CRED) == (ACCOUNT, "ab=cd")


# --- the GitHub dead-row exception (HOST 01M7JVMNWK, Lead 01M7JVJBHT) ------


def _health(ss, **github):
    rows = [{"name": n, "status": "not_configured"} for n in ("notion", "slack", "calendar")]
    rows.append({"name": "github", **github})
    return {
        "/api/v1/integrations/health": ss.Reply(200, json.dumps({"integrations": rows}).encode())
    }


def test_the_dead_github_row_passes_for_web_seed_1386(ss, shared):
    host = StubHost(ss, **_health(ss, status="degraded", can_test=False, action="reconnect"))
    assert ss.run(ACCOUNT, host, now=1_800_000_000).startswith(ACCOUNT)


@pytest.mark.parametrize(
    "row",
    [
        {
            "status": "degraded",
            "can_test": True,
            "action": "reconnect",
        },  # a stored token still works
        {"status": "degraded", "can_test": False, "action": None},
        {"status": "degraded", "can_test": False},  # action missing
        {"status": "degraded", "action": "reconnect"},  # can_test missing
        {"status": "degraded", "can_test": 0, "action": "reconnect"},  # not a boolean
        {"status": "failed", "can_test": False, "action": "reconnect"},
        {"status": "failed", "can_test": True, "action": None},
        {"status": "connected", "can_test": True, "action": None},
        {"status": "healthy", "can_test": True, "action": None},
    ],
)
def test_every_other_github_state_refuses(ss, shared, row):
    host = StubHost(ss, **_health(ss, **row))
    with pytest.raises(ss.Refused, match="has a connection"):
        ss.run(ACCOUNT, host)
    assert not (shared / f"{ACCOUNT}.session-token.json").exists()


def test_the_dead_row_exception_is_for_github_only(ss, shared):
    rows = [
        {"name": "slack", "status": "degraded", "can_test": False, "action": "reconnect"},
        {"name": "github", "status": "not_configured"},
    ]
    host = StubHost(
        ss,
        **{
            "/api/v1/integrations/health": ss.Reply(
                200, json.dumps({"integrations": rows}).encode()
            )
        },
    )
    with pytest.raises(ss.Refused, match="has a connection"):
        ss.run(ACCOUNT, host)


def test_the_exception_table_is_exactly_what_host_read(ss):
    assert ss.GITHUB_DEAD_ROW == ("degraded", False, "reconnect")
    assert dict(ss.ACCOUNTS[ACCOUNT].integrations) == {"github": frozenset({ss.GITHUB_DEAD_ROW})}
    assert ss.ACCOUNTS[ACCOUNT].connectors is False


# --- the Anthropic key exception (HOST 01M7JT4WFC, Arch 01M7JV4RQX) ---------


def test_an_anthropic_key_passes_for_web_seed_1386_and_nothing_else_does(ss, shared):
    assert ss.ACCOUNTS[ACCOUNT].provider_keys == frozenset({"anthropic"})
    keys = [
        {"provider": "anthropic", "is_active": True},
        {"provider": "anthropic", "is_active": False},
    ]
    host = StubHost(ss, **{"/api/v1/keys/list": ss.Reply(200, json.dumps(keys).encode())})
    assert ss.run(ACCOUNT, host, now=1_800_000_000).startswith(ACCOUNT)


def test_the_key_exception_names_its_workspace_and_cap(ss):
    source = (ROOT / "scripts" / "seat_session.py").read_text()
    assert "piper-morgan-test" in source and "$40" in source


def test_the_second_account_is_listed_and_holds_nothing(ss):
    assert sorted(ss.ACCOUNTS) == ["seat-github-1", "web-seed-1386"]
    second = ss.ACCOUNTS["seat-github-1"]
    assert second.credential_file == "seat-github-1-credentials.txt"
    assert not second.integrations and not second.provider_keys and second.connectors is False


# --- seat_read.py --redirect-uri (issue 2282 step 5; HOST's four conditions, 11-16) ---

GH_CONNECT = "/api/v1/settings/integrations/github/connect"
CAL_CONNECT = "/api/v1/settings/integrations/calendar/connect"
# Shaped as both handlers mint it: base64 of a made-up user id and nonce, over 100
# characters in one unbroken run.
STATE = (
    __import__("base64")
    .urlsafe_b64encode(
        json.dumps(
            {"user_id": "00000000-0000-4000-8000-000000000000", "nonce": "made-up-nonce-0123456789"}
        ).encode()
    )
    .decode()
    .rstrip("=")
    .lower()
)
SHORT_STATE = "made-up-short-state-1"  # under the length bound: only the comparison catches it
CALLBACK = "https://beta.example.invalid/api/v1/settings/integrations/github/callback"


def _connect_reply(ss, redirect=CALLBACK, extra="", **over):
    from urllib.parse import urlencode

    query = urlencode({"client_id": "made-up-id", "redirect_uri": redirect, "state": STATE})
    payload = {"auth_url": f"https://provider.example.invalid/authorize?{query}{extra}"}
    payload["state"] = STATE
    payload.update(over)
    return ss.Reply(200, json.dumps(payload).encode())


def test_redirect_uri_prints_the_host_and_path_and_nothing_else(ss, sr, shared):
    _saved(ss, shared)
    host = StubHost(ss, **{GH_CONNECT: _connect_reply(ss)})
    line = sr.read_redirect_uri(ACCOUNT, "github", host, now=1_800_000_100)
    assert line == (
        "github redirect_uri: https://beta.example.invalid/api/v1/settings/integrations/github/callback"
    )
    assert STATE not in line and "made-up-id" not in line and "?" not in line
    for secret in SECRETS:
        assert secret not in line
    assert [(c[0], c[1], c[2]) for c in host.calls] == [("GET", GH_CONNECT, None)]  # one request


def test_redirect_uri_drops_a_query_on_the_redirect_itself(ss, sr, shared):
    _saved(ss, shared)
    host = StubHost(ss, **{CAL_CONNECT: _connect_reply(ss, redirect=CALLBACK + "?next=" + STATE)})
    line = sr.read_redirect_uri(ACCOUNT, "calendar", host, now=1_800_000_100)
    assert line.endswith("/github/callback") and STATE not in line


def test_redirect_uri_reports_a_host_switch_by_host_and_path(ss, sr, shared):
    _saved(ss, shared)
    reply = ss.Reply(
        200,
        json.dumps(
            {
                "switch_host_url": f"https://other.example.invalid/settings/integrations/github?s={STATE}"
            }
        ).encode(),
    )
    host = StubHost(ss, **{GH_CONNECT: reply})
    line = sr.read_redirect_uri(ACCOUNT, "github", host, now=1_800_000_100)
    assert line == "github: start on https://other.example.invalid/settings/integrations/github"


@pytest.mark.parametrize(
    "reply_kwargs,reason",
    [
        ({"redirect": "https://beta.example.invalid/cb/" + STATE}, "too long"),
        ({"redirect": "javascript:alert(1)"}, "plain form"),
        ({"redirect": "https://user:pw@beta.example.invalid/cb"}, "plain form"),
        ({"redirect": "https://beta.example.invalid/cb%2Fx"}, "plain form"),
        ({"extra": "&redirect_uri=https%3A%2F%2Fsecond.example.invalid%2Fcb"}, "exactly one"),
        ({"auth_url": None}, "expected form"),
    ],
)
def test_redirect_uri_refuses_and_names_no_value(ss, sr, shared, reply_kwargs, reason):
    _saved(ss, shared)
    host = StubHost(ss, **{GH_CONNECT: _connect_reply(ss, **reply_kwargs)})
    with pytest.raises(ss.Refused, match=reason) as refusal:
        sr.read_redirect_uri(ACCOUNT, "github", host, now=1_800_000_100)
    assert STATE not in str(refusal.value)


def test_redirect_uri_refuses_a_state_in_the_path_when_the_reply_sends_no_state_key(ss, sr, shared):
    # Arch 2026-11-16 18:43: the state is also read from the sign-in address.
    _saved(ss, shared)
    reply = _connect_reply(ss, redirect="https://beta.example.invalid/cb/" + STATE)
    payload = json.loads(reply.body)
    del payload["state"]
    host = StubHost(ss, **{GH_CONNECT: ss.Reply(200, json.dumps(payload).encode())})
    with pytest.raises(ss.Refused, match="too long") as refusal:
        sr.read_redirect_uri(ACCOUNT, "github", host, now=1_800_000_100)
    assert STATE not in str(refusal.value)


def test_redirect_uri_compares_a_short_state_the_length_rule_would_pass(ss, sr, shared):
    """The comparison, on its own: a state under the length bound, in the path."""
    from urllib.parse import urlencode

    _saved(ss, shared)
    redirect = "https://beta.example.invalid/cb/" + SHORT_STATE
    for payload in (
        {
            "auth_url": "https://p.example.invalid/a?" + urlencode({"redirect_uri": redirect}),
            "state": SHORT_STATE,
        },
        {
            "auth_url": "https://p.example.invalid/a?"
            + urlencode({"redirect_uri": redirect, "state": SHORT_STATE})
        },
    ):
        host = StubHost(ss, **{GH_CONNECT: ss.Reply(200, json.dumps(payload).encode())})
        with pytest.raises(ss.Refused, match="state value") as refusal:
            sr.read_redirect_uri(ACCOUNT, "github", host, now=1_800_000_100)
        assert SHORT_STATE not in str(refusal.value)


@pytest.mark.parametrize("body", [b"not json", b"[]", b'"text"'])
def test_redirect_uri_refuses_a_reply_in_another_form(ss, sr, shared, body):
    _saved(ss, shared)
    host = StubHost(ss, **{GH_CONNECT: ss.Reply(200, body)})
    with pytest.raises(ss.Refused, match="expected form"):
        sr.read_redirect_uri(ACCOUNT, "github", host, now=1_800_000_100)


def test_redirect_uri_says_only_the_status_when_the_host_refuses(ss, sr, shared):
    _saved(ss, shared)
    host = StubHost(ss, **{GH_CONNECT: ss.Reply(503, f"state={STATE}".encode())})
    with pytest.raises(ss.Refused, match="answered 503") as refusal:
        sr.read_redirect_uri(ACCOUNT, "github", host, now=1_800_000_100)
    assert STATE not in str(refusal.value)


def test_redirect_uri_refuses_a_connector_or_account_off_the_lists(ss, sr, shared):
    _saved(ss, shared)
    host = StubHost(ss)
    with pytest.raises(ss.Refused, match="connector is not on the list"):
        sr.read_redirect_uri(ACCOUNT, "slack", host, now=1_800_000_100)
    with pytest.raises(ss.Refused, match="account is not on the list"):
        sr.read_redirect_uri("someone-else", "github", host, now=1_800_000_100)
    assert host.calls == []


def test_the_connect_routes_can_never_be_read_as_a_body(ss, sr, shared):
    """``read`` prints a body, and these bodies hold a state: the two lists stay apart."""
    _saved(ss, shared)
    assert not (set(sr.REDIRECT_URI_ROUTES.values()) & set(sr.ALLOWED_PATHS))
    host = StubHost(ss, **{GH_CONNECT: _connect_reply(ss)})
    for route in sr.REDIRECT_URI_ROUTES.values():
        with pytest.raises(ss.Refused, match="not on the list"):
            sr.read(ACCOUNT, route, host, now=1_800_000_100)
    assert host.calls == []
    assert sorted(sr.REDIRECT_URI_ROUTES) == ["calendar", "github"]


def test_main_takes_a_path_or_the_option_never_both_or_neither(ss, sr, shared, capsys, monkeypatch):
    _saved(ss, shared)
    host = StubHost(ss, **{GH_CONNECT: _connect_reply(ss)})
    monkeypatch.setattr(ss, "http_transport", host)
    monkeypatch.setattr(sr, "load_cookies", lambda account, now=None: {"auth_token": ACCESS})
    code, text = _run_main(sr, ["--account", ACCOUNT, "--redirect-uri", "github"], capsys)
    assert code == 0
    assert text.strip() == (
        "github redirect_uri: https://beta.example.invalid/api/v1/settings/integrations/github/callback"
    )
    assert len(host.calls) == 1
    code, text = _run_main(sr, ["--account", ACCOUNT], capsys)
    assert code == 2 and "one of them" in text
    code, text = _run_main(sr, ["--account", ACCOUNT, FLOORED, "--redirect-uri", "github"], capsys)
    assert code == 2 and "one of them" in text
    assert len(host.calls) == 1  # neither refusal sent anything


def test_the_two_routes_exist_in_the_app_as_get_routes():
    source = (ROOT / "web" / "api" / "routes" / "settings_integrations.py").read_text()
    assert 'APIRouter(prefix="/api/v1/settings/integrations"' in source
    assert '@router.get("/github/connect")' in source
    assert '@router.get("/calendar/connect")' in source


# CIO's read (2026-11-16 18:49): four replies no handler sends today, each of which
# printed a line containing the state at 9abd173fa8.


def _raw_reply(ss, payload):
    return ss.Reply(200, json.dumps(payload).encode())


def _auth_url(redirect, with_state=True):
    from urllib.parse import urlencode

    params = {"client_id": "made-up-id", "redirect_uri": redirect}
    if with_state:
        params["state"] = STATE
    return f"https://provider.example.invalid/authorize?{urlencode(params)}"


@pytest.mark.parametrize(
    "payload",
    [
        # 1. state in the redirect's path, no ``state`` key
        {"auth_url": _auth_url("https://beta.example.invalid/cb/" + STATE)},
        # 2. state as a host label of the redirect, no ``state`` key
        {"auth_url": _auth_url(f"https://{STATE}.example.invalid/cb")},
        # 3. state in the path, ``state`` key present but not a string
        {"auth_url": _auth_url("https://beta.example.invalid/cb/" + STATE), "state": 7},
        # 4. state in the host-switch address's path, no ``state`` key
        {"switch_host_url": "https://other.example.invalid/settings/" + STATE},
        # and the same four with the state nowhere the script could learn it
        {"auth_url": _auth_url("https://beta.example.invalid/cb/" + STATE, with_state=False)},
        {"auth_url": _auth_url(f"https://{STATE}.example.invalid/cb", with_state=False)},
        {"switch_host_url": f"https://{STATE}.example.invalid/settings/integrations/github"},
    ],
    ids=[
        "path",
        "host-label",
        "non-string-key",
        "switch-path",
        "path-unknown",
        "host-unknown",
        "switch-host",
    ],
)
def test_redirect_uri_never_prints_a_state_in_cios_cases(
    ss, sr, shared, capsys, monkeypatch, payload
):
    _saved(ss, shared)
    host = StubHost(ss, **{GH_CONNECT: _raw_reply(ss, payload)})
    with pytest.raises(ss.Refused) as refusal:
        sr.read_redirect_uri(ACCOUNT, "github", host, now=1_800_000_100)
    assert STATE not in str(refusal.value)
    monkeypatch.setattr(ss, "http_transport", host)
    monkeypatch.setattr(sr, "load_cookies", lambda account, now=None: {"auth_token": ACCESS})
    code, text = _run_main(sr, ["--account", ACCOUNT, "--redirect-uri", "github"], capsys)
    assert code == 2 and STATE not in text


def test_redirect_uri_refuses_a_reply_with_no_state_to_compare(ss, sr, shared):
    _saved(ss, shared)
    payload = {"auth_url": _auth_url(CALLBACK, with_state=False)}
    host = StubHost(ss, **{GH_CONNECT: _raw_reply(ss, payload)})
    with pytest.raises(ss.Refused, match="no state to check"):
        sr.read_redirect_uri(ACCOUNT, "github", host, now=1_800_000_100)


def test_redirect_uri_takes_the_state_from_the_address_alone(ss, sr, shared):
    _saved(ss, shared)
    host = StubHost(ss, **{GH_CONNECT: _raw_reply(ss, {"auth_url": _auth_url(CALLBACK)})})
    line = sr.read_redirect_uri(ACCOUNT, "github", host, now=1_800_000_100)
    assert line.endswith("/github/callback") and STATE not in line


def test_the_host_switch_line_is_only_ever_the_apps_own_page(ss, sr, shared):
    _saved(ss, shared)
    other = {"switch_host_url": "https://other.example.invalid/settings/integrations/calendar"}
    host = StubHost(ss, **{GH_CONNECT: _raw_reply(ss, other)})
    with pytest.raises(ss.Refused, match="not the page"):
        sr.read_redirect_uri(ACCOUNT, "github", host, now=1_800_000_100)
    assert set(sr.SWITCH_PAGES) == set(sr.REDIRECT_URI_ROUTES)


def test_the_real_callback_paths_fit_the_length_rule(sr):
    for path in (
        "/api/v1/settings/integrations/github/callback",
        "/api/v1/settings/integrations/calendar/callback",
    ):
        assert (
            sr.host_and_path("https://beta.pipermorgan.ai" + path)
            == "https://beta.pipermorgan.ai" + path
        )
    assert len(STATE) > 3 * sr.MAX_PART  # a minted state is far over the bound


def test_the_line_shows_http_against_https(sr):
    # HOST 2026-11-16 19:03: the scheme is part of what a provider compares.
    assert (
        sr.host_and_path("http://beta.example.invalid/cb?x=1") == "http://beta.example.invalid/cb"
    )
    assert (
        sr.host_and_path("https://beta.example.invalid/cb#f") == "https://beta.example.invalid/cb"
    )


# 11-20 (Exec 01M7X7QX7P): the connection refusal names the row, in fixed words only.
@pytest.mark.parametrize(
    "row, words",
    [
        (
            {"status": "degraded", "can_test": True, "action": "reconnect"},
            "github: degraded/True/reconnect",
        ),
        ({"status": "connected", "can_test": True, "action": None}, "github: connected/True/none"),
        ({"status": "failed", "can_test": True}, "github: failed/True/none"),
        (
            {"status": "degraded", "can_test": 0, "action": "reconnect"},
            "github: degraded/missing/reconnect",
        ),
    ],
)
def test_the_connection_refusal_names_the_row(ss, shared, row, words):
    host = StubHost(ss, **_health(ss, **row))
    with pytest.raises(ss.Refused) as e:
        ss.run(ACCOUNT, host)
    assert str(e.value) == f"the account has a connection ({words})"


def test_server_text_outside_the_lists_prints_as_other(ss, shared):
    odd = "zz-" + PASSWORD
    rows = [{"name": odd, "status": odd, "can_test": True, "action": odd}]
    host = StubHost(
        ss,
        **{
            "/api/v1/integrations/health": ss.Reply(
                200, json.dumps({"integrations": rows}).encode()
            )
        },
    )
    with pytest.raises(ss.Refused) as e:
        ss.run(ACCOUNT, host)
    assert str(e.value) == "the account has a connection (other: other/True/other)"
    assert "zz-" not in str(e.value)


def test_a_slack_row_is_named(ss, shared):
    rows = [{"name": "slack", "status": "healthy", "can_test": True, "action": None}]
    host = StubHost(
        ss,
        **{
            "/api/v1/integrations/health": ss.Reply(
                200, json.dumps({"integrations": rows}).encode()
            )
        },
    )
    with pytest.raises(ss.Refused, match=r"has a connection \(slack: healthy/True/none\)"):
        ss.run(ACCOUNT, host)


# 11-20 (Exec 01M7X9RFAM): one-shot disconnect of a connector the account must not hold.
DISCONNECT = "/api/v1/settings/integrations/calendar/disconnect"


def _health_with(ss, calendar_row):
    rows = [{"name": n, "status": "not_configured"} for n in ("notion", "slack", "github")]
    rows.append({"name": "calendar", **calendar_row})
    return ss.Reply(200, json.dumps({"integrations": rows}).encode())


class CalendarHost(StubHost):
    """Shows a live Calendar row until the disconnect route is called (unless ``sticky``)."""

    def __init__(self, ss, disconnect_reply=None, sticky=False, **over):
        super().__init__(ss, **over)
        self.live = _health_with(ss, {"status": "connected", "can_test": True, "action": None})
        self.gone = _health_with(ss, {"status": "not_configured"})
        self.cleared = False
        self.sticky = sticky
        self.disconnect_reply = disconnect_reply or ss.Reply(
            200, json.dumps({"success": True, "outcome": "cleared", "message": "x"}).encode()
        )

    def __call__(self, method, path, data, headers):
        self.calls.append((method, path, data, dict(headers)))
        if path == DISCONNECT:
            assert method == "POST"
            self.cleared = not self.sticky
            return self.disconnect_reply
        if path == "/api/v1/integrations/health":
            return self.gone if self.cleared else self.live
        return self.replies[path.split("?")[0]]


def _posts(host):
    return [c[1] for c in host.calls if c[0] == "POST"]


def test_disconnect_clears_rechecks_and_saves_nothing(ss, shared):
    host = CalendarHost(ss)
    line = ss.disconnect(ACCOUNT, "calendar", host)
    assert line == (
        f"{ACCOUNT}: calendar disconnected (outcome cleared); the holds-nothing checks now pass"
    )
    assert _posts(host) == ["/api/v1/auth/login", DISCONNECT]
    post = next(c for c in host.calls if c[1] == DISCONNECT)
    assert f"auth_token={ACCESS}" in post[3]["Cookie"]
    assert not (shared / f"{ACCOUNT}.session-token.json").exists()
    for secret in SECRETS:
        assert secret not in line


def test_disconnect_when_not_connected_posts_nothing(ss, shared):
    host = CalendarHost(ss)
    host.cleared = True
    line = ss.disconnect(ACCOUNT, "calendar", host)
    assert line == f"{ACCOUNT}: calendar was not connected; the holds-nothing checks now pass"
    assert _posts(host) == ["/api/v1/auth/login"]


def test_disconnect_incomplete_refuses_and_skips_the_recheck(ss, shared):
    host = CalendarHost(ss, disconnect_reply=ss.Reply(503, b""))
    with pytest.raises(ss.Refused, match=r"calendar disconnect did not complete"):
        ss.disconnect(ACCOUNT, "calendar", host)
    assert "/api/v1/keys/list" not in [c[1] for c in host.calls]


def test_disconnect_reply_outside_the_list_never_prints(ss, shared):
    odd = json.dumps({"outcome": "zz-" + PASSWORD}).encode()
    host = CalendarHost(ss, disconnect_reply=ss.Reply(200, odd))
    with pytest.raises(ss.Refused) as e:
        ss.disconnect(ACCOUNT, "calendar", host)
    assert str(e.value) == "the disconnect reply could not be read"


def test_a_route_that_says_cleared_but_leaves_the_row_still_refuses(ss, shared):
    host = CalendarHost(ss, sticky=True)
    with pytest.raises(ss.Refused) as e:
        ss.disconnect(ACCOUNT, "calendar", host)
    assert str(e.value) == "the account has a connection (calendar: connected/True/none)"


def test_disconnect_refuses_an_admin_before_any_post(ss, shared):
    host = CalendarHost(ss, **{"/api/v1/admin/account-flags": ss.Reply(200, b"{}")})
    with pytest.raises(ss.Refused, match="is an admin"):
        ss.disconnect(ACCOUNT, "calendar", host)
    assert _posts(host) == ["/api/v1/auth/login"]


def test_disconnect_list_is_closed(ss, shared):
    assert ss.DISCONNECTABLE == ("calendar",)
    with pytest.raises(ss.Refused, match="not on the disconnect list"):
        ss.disconnect(ACCOUNT, "slack", CalendarHost(ss))
    with pytest.raises(ss.Refused, match="not on the list"):
        ss.disconnect("someone-else", "calendar", CalendarHost(ss))
    with pytest.raises(SystemExit):
        ss.main(["--account", ACCOUNT, "--disconnect", "github"])


def test_main_disconnect_prints_one_line_and_places_nothing(ss, shared, monkeypatch, capsys):
    host = CalendarHost(ss)
    monkeypatch.setattr(ss, "http_transport", host)
    monkeypatch.setattr(ss.disconnect, "__defaults__", (host,))
    placed = []
    monkeypatch.setattr(ss, "place_in_seat_browser", lambda a: placed.append(a) or 0)
    code, out = _run_main(ss, ["--account", ACCOUNT, "--disconnect", "calendar"], capsys)
    assert code == 0
    assert out.strip().endswith("the holds-nothing checks now pass")
    assert placed == []
