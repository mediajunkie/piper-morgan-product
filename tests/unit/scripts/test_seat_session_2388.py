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


def test_the_second_account_is_listed_with_its_closed_row(ss):
    """Was "holds nothing" until xian's Step F.4 connect (2026-11-26). HOST's rulings
    01M8CPKEAQ and 01M8CPMDJ9, Arch's 01M8CPMSV9: GitHub as the one machine login, at most
    one OAuth connector, and nothing else."""
    assert sorted(ss.ACCOUNTS) == ["seat-github-1", "seat-tester-1", "web-seed-1386"]
    second = ss.ACCOUNTS["seat-github-1"]
    assert second.credential_file == "seat-github-1-credentials.txt"
    assert dict(second.integrations) == {
        "github": frozenset(
            {
                ("connected", True, None),
                ("healthy", True, None),
                ("failed", True, None),
                ss.GITHUB_DEAD_ROW,
            }
        )
    }
    assert second.github_login == "atswimtwobirds"
    assert second.max_oauth_connectors == 1
    # HOST 01M8CT906X, xian via Exec 01M8CTPKT8 (2026-11-26): the test workspace's
    # Anthropic key and no other provider's.
    assert second.provider_keys == frozenset({"anthropic"})
    assert second.connectors is False


def test_no_other_account_gained_a_login_or_a_connector(ss):
    for name, account in ss.ACCOUNTS.items():
        if name != "seat-github-1":
            assert account.github_login is None, name
            assert account.max_oauth_connectors == 0, name


# --- seat-github-1's row (HOST 01M8CPKEAQ, 01M8CPMDJ9; Arch 01M8CPMSV9; 2026-11-26) ---

SEAT_GH = "seat-github-1"
MACHINE = "atswimtwobirds"
CARD_FULL = f"Connected as {MACHINE}. Not the right account? Disconnect, then connect again."
CARD_SHORT = f"Connected as {MACHINE}."


def _seat_gh_host(ss, github=None, oauth=(), manual=(), keys=b"[]", admin=403):
    rows = [{"name": n, "status": "not_configured"} for n in ("notion", "slack", "calendar")]
    rows.append({"name": "github", **(github or {"status": "not_configured"})})
    return StubHost(
        ss,
        **{
            "/api/v1/auth/me": ss.Reply(200, json.dumps({"username": SEAT_GH}).encode()),
            "/api/v1/admin/account-flags": ss.Reply(admin, b""),
            "/api/v1/keys/list": ss.Reply(200, keys),
            "/api/v1/integrations/health": ss.Reply(
                200, json.dumps({"integrations": rows}).encode()
            ),
            "/api/v1/settings/mcp-connections": ss.Reply(
                200,
                json.dumps(
                    {"oauth_connections": list(oauth), "manual_tokens": list(manual)}
                ).encode(),
            ),
        },
    )


def _check_seat_gh(ss, host):
    return ss.check_holds_nothing_real(SEAT_GH, {"auth_token": ("made-up", None)}, host)


def _live(status="connected", message=CARD_FULL, **over):
    return {"status": status, "can_test": True, "action": None, "status_message": message, **over}


def test_the_helpers_two_card_lines_are_the_apps_own(ss):
    """The coupling test (HOST's addition, Arch's shape): the helper is stdlib-only and
    carries copies; a copy change in the app fails HERE, never in a sitting."""
    from web.api.routes import integrations

    assert ss.GITHUB_CARD_CONNECTED_AS == integrations._GITHUB_CARD_CONNECTED_AS
    assert ss.GITHUB_CARD_CONNECTED_AS_ONLY == integrations._GITHUB_CARD_CONNECTED_AS_ONLY
    assert ss._github_card_lines(MACHINE) == frozenset(
        {
            integrations._GITHUB_CARD_CONNECTED_AS.format(login=MACHINE),
            integrations._GITHUB_CARD_CONNECTED_AS_ONLY.format(login=MACHINE),
        }
    )
    assert ss._github_card_lines(MACHINE) == frozenset({CARD_FULL, CARD_SHORT})


def test_the_helper_does_not_import_the_app():
    source = (ROOT / "scripts" / "seat_session.py").read_text()
    for line in source.splitlines():
        stripped = line.strip()
        if stripped.startswith(("import ", "from ")):
            assert not stripped.startswith(
                ("from web", "import web", "from services", "import services")
            ), line


@pytest.mark.parametrize(
    "status, message",
    [
        ("connected", CARD_FULL),  # CIO's read of 2026-11-26: github: connected/True/none
        ("healthy", CARD_FULL),
        ("failed", CARD_SHORT),
        ("connected", CARD_SHORT),
    ],
)
def test_github_connected_as_the_machine_account_passes(ss, status, message):
    _check_seat_gh(ss, _seat_gh_host(ss, github=_live(status, message)))


def test_the_dead_github_row_passes_for_the_seat_too(ss):
    dead = {"status": "degraded", "can_test": False, "action": "reconnect"}
    _check_seat_gh(ss, _seat_gh_host(ss, github=dead))


def test_holding_nothing_still_passes(ss):
    _check_seat_gh(ss, _seat_gh_host(ss))


@pytest.mark.parametrize(
    "message",
    [
        "Connected as mediajunkie. Not the right account? Disconnect, then connect again.",
        "Connected as mediajunkie.",
        "Connected.",  # the card's no-login form: it cannot say whose account it is
        f"Connected as {MACHINE}",  # no full stop: not one of the two forms
        f"Connected as {MACHINE}. And more.",
        f"x Connected as {MACHINE}.",
        f"Connected as {MACHINE}-admin.",
        f"Connected as {MACHINE.upper()}.",
        "",
        None,
        42,
        [CARD_FULL],  # unhashable: must refuse, not raise TypeError
        {"line": CARD_FULL},
        True,
    ],
)
def test_any_other_login_or_card_line_refuses(ss, message):
    with pytest.raises(ss.Refused, match="not the named login"):
        _check_seat_gh(ss, _seat_gh_host(ss, github=_live(message=message)))


def test_a_live_row_with_no_status_message_at_all_refuses(ss):
    row = {"status": "connected", "can_test": True, "action": None}
    with pytest.raises(ss.Refused, match="not the named login"):
        _check_seat_gh(ss, _seat_gh_host(ss, github=row))


@pytest.mark.parametrize(
    "row",
    [
        # A stored personal token that still works (the stale-grant card with Test).
        {
            "status": "degraded",
            "can_test": True,
            "action": "reconnect",
            "status_message": CARD_FULL,
        },
        # The own-token card after a passing Test says a different thing, but the row is
        # healthy/True/none, the same triple as a live grant: only the line tells them apart.
        {
            "status": "healthy",
            "can_test": True,
            "action": None,
            "status_message": "Connected with your personal token.",
        },
        {"status": "unhealthy", "can_test": True, "action": None, "status_message": CARD_FULL},
        {"status": "connected", "can_test": False, "action": None, "status_message": CARD_FULL},
        {
            "status": "connected",
            "can_test": True,
            "action": "test_only",
            "status_message": CARD_FULL,
        },
        {"status": "connected", "action": None, "status_message": CARD_FULL},  # can_test missing
    ],
    ids=[
        "token-still-works",
        "own-token-healthy",
        "unhealthy",
        "no-test",
        "test-only",
        "can_test-missing",
    ],
)
def test_every_other_github_state_still_refuses(ss, row):
    with pytest.raises(ss.Refused):
        _check_seat_gh(ss, _seat_gh_host(ss, github=row))


def test_a_live_github_row_still_refuses_on_every_other_account(ss, shared):
    """The pin is per account: web-seed-1386 and seat-tester-1 have no login and no live
    rows on their list, so the machine account's own card refuses there."""
    host = StubHost(ss, **_health(ss, **_live()))
    with pytest.raises(ss.Refused, match="has a connection"):
        ss.run(ACCOUNT, host, now=1_800_000_000)


def test_a_login_without_live_rows_on_the_list_does_nothing(ss, monkeypatch):
    """Belt and braces: the login alone opens nothing; the row must be listed too."""
    monkeypatch.setitem(
        ss.ACCOUNTS,
        SEAT_GH,
        ss.Account(credential_file="seat-github-1-credentials.txt", github_login=MACHINE),
    )
    with pytest.raises(ss.Refused, match="has a connection"):
        _check_seat_gh(ss, _seat_gh_host(ss, github=_live()))


def test_live_rows_without_a_login_refuse(ss, monkeypatch):
    monkeypatch.setitem(
        ss.ACCOUNTS,
        SEAT_GH,
        ss.Account(
            credential_file="seat-github-1-credentials.txt",
            integrations={"github": ss.GITHUB_LIVE_ROWS},
        ),
    )
    with pytest.raises(ss.Refused, match="not the named login"):
        _check_seat_gh(ss, _seat_gh_host(ss, github=_live()))


def test_another_integration_still_refuses_on_the_seat(ss):
    rows = [
        {"name": "github", **_live()},
        {
            "name": "slack",
            "status": "connected",
            "can_test": True,
            "action": None,
            "status_message": CARD_FULL,
        },
    ]
    host = _seat_gh_host(ss)
    host.replies["/api/v1/integrations/health"] = ss.Reply(
        200, json.dumps({"integrations": rows}).encode()
    )
    with pytest.raises(ss.Refused, match="has a connection"):
        _check_seat_gh(ss, host)


# The connector allowance: at most one OAuth connection, no manual token (HOST 01M8CPMDJ9).

ONE_CONNECTOR = {
    "client_id": "made-up-client",
    "client_name": "whatever the client sent",
    "active": True,
}


def test_one_oauth_connector_passes_whatever_its_name(ss):
    _check_seat_gh(ss, _seat_gh_host(ss, github=_live(), oauth=[ONE_CONNECTOR]))


def test_a_second_oauth_connector_refuses(ss):
    two = [ONE_CONNECTOR, {**ONE_CONNECTOR, "client_id": "another"}]
    with pytest.raises(ss.Refused, match="has a connector"):
        _check_seat_gh(ss, _seat_gh_host(ss, github=_live(), oauth=two))


def test_an_inactive_connector_still_counts(ss):
    two = [ONE_CONNECTOR, {**ONE_CONNECTOR, "client_id": "another", "active": False}]
    with pytest.raises(ss.Refused, match="has a connector"):
        _check_seat_gh(ss, _seat_gh_host(ss, oauth=two))


@pytest.mark.parametrize("oauth", [[], [ONE_CONNECTOR]])
def test_a_manual_token_always_refuses(ss, oauth):
    with pytest.raises(ss.Refused, match="has a connector"):
        _check_seat_gh(ss, _seat_gh_host(ss, oauth=oauth, manual=[{"label": "x"}]))


def test_one_connector_still_refuses_on_the_other_accounts(ss, shared):
    host = StubHost(
        ss,
        **{
            "/api/v1/settings/mcp-connections": ss.Reply(
                200,
                json.dumps({"oauth_connections": [ONE_CONNECTOR], "manual_tokens": []}).encode(),
            )
        },
    )
    with pytest.raises(ss.Refused, match="has a connector"):
        ss.run(ACCOUNT, host, now=1_800_000_000)


# The other bounds are untouched for the seat.


def test_an_admin_seat_still_refuses(ss):
    with pytest.raises(ss.Refused, match="is an admin"):
        _check_seat_gh(ss, _seat_gh_host(ss, github=_live(), admin=200))


def test_the_seats_own_anthropic_key_passes(ss):
    """HOST 01M8CT906X (2026-11-26): without a model key chat refuses every turn, so no
    GitHub-connected chat reply could be read on this account."""
    keys = json.dumps([{"provider": "anthropic"}]).encode()
    _check_seat_gh(ss, _seat_gh_host(ss, github=_live(), keys=keys))


@pytest.mark.parametrize(
    "rows",
    [
        [{"provider": "openai"}],
        [{"provider": "anthropic"}, {"provider": "openai"}],
        [{"provider": "gemini"}],
        [{"provider": None}],
        ["anthropic"],
    ],
    ids=["openai", "anthropic and openai", "gemini", "no provider named", "not a row"],
)
def test_any_other_providers_key_on_the_seat_still_refuses(ss, rows):
    keys = json.dumps(rows).encode()
    with pytest.raises(ss.Refused, match="holds a provider key"):
        _check_seat_gh(ss, _seat_gh_host(ss, github=_live(), keys=keys))


def test_the_key_changes_no_other_bound_on_the_seat(ss):
    """With the key on file: another login, a second connector, a manual token and an
    admin flag each still refuse."""
    keys = json.dumps([{"provider": "anthropic"}]).encode()
    with pytest.raises(ss.Refused, match="not the named login"):
        _check_seat_gh(
            ss, _seat_gh_host(ss, github=_live(message="Connected as mediajunkie."), keys=keys)
        )
    two = [ONE_CONNECTOR, {**ONE_CONNECTOR, "client_id": "another"}]
    with pytest.raises(ss.Refused, match="has a connector"):
        _check_seat_gh(ss, _seat_gh_host(ss, github=_live(), keys=keys, oauth=two))
    with pytest.raises(ss.Refused, match="has a connector"):
        _check_seat_gh(ss, _seat_gh_host(ss, github=_live(), keys=keys, manual=[{"label": "x"}]))
    with pytest.raises(ss.Refused, match="is an admin"):
        _check_seat_gh(ss, _seat_gh_host(ss, github=_live(), keys=keys, admin=200))


def test_the_named_login_refusal_prints_no_server_text(ss, capsys, monkeypatch, tmp_path):
    """The refusal is fixed words: the card's line, whatever it says, never reaches the
    screen."""
    try:
        _check_seat_gh(ss, _seat_gh_host(ss, github=_live(message="Connected as someone-else.")))
    except ss.Refused as refused:
        assert str(refused) == "the account's GitHub connection is not the named login"
        assert "someone-else" not in str(refused)
    else:
        raise AssertionError("expected a refusal")


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
    assert sorted(sr.REDIRECT_URI_ROUTES) == ["calendar", "github", "setup-calendar"]


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
    # The /setup start mints a state every time and has no host-switch page (issue 2282).
    assert set(sr.SWITCH_PAGES) == set(sr.REDIRECT_URI_ROUTES) - {"setup-calendar"}


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


def test_revoke_failed_says_a_grant_may_remain(ss, shared):
    reply = ss.Reply(200, json.dumps({"success": True, "outcome": "revoke_failed"}).encode())
    line = ss.disconnect(ACCOUNT, "calendar", CalendarHost(ss, disconnect_reply=reply))
    assert line == (
        f"{ACCOUNT}: calendar disconnected (outcome revoke_failed; a grant may remain listed "
        "at Google); the holds-nothing checks now pass"
    )


# -- the printed expiry is the token's own, when that is sooner (Web's finding, 11-22) --


def _jwt_shaped(claims) -> str:
    """A three-part value with a readable payload, built at run time; it signs nothing."""
    import base64

    def part(obj) -> str:
        return base64.urlsafe_b64encode(json.dumps(obj).encode()).decode().rstrip("=")

    return ".".join([part({"alg": "none"}), part(claims), "sig"])


def test_expiry_is_the_tokens_own_when_it_is_sooner_than_the_cookie(ss, shared, capsys):
    now = 1_800_000_000
    token = _jwt_shaped({"sub": "x", "exp": now + 1800})
    host = StubHost(ss)
    host.replies["/api/v1/auth/login"] = ss.Reply(
        200, b"{}", (f"auth_token={token}; HttpOnly; Max-Age=86400; Path=/",)
    )
    line = ss.run(ACCOUNT, host, now=now)
    state = json.loads((shared / f"{ACCOUNT}.session-token.json").read_text())
    assert state["cookies"][0]["expires"] == now + 1800
    assert line.endswith("2027-01-15T08:30:00Z")
    assert token not in line


def test_a_token_that_outlives_the_cookie_or_the_cap_changes_nothing(ss, shared):
    now = 1_800_000_000
    token = _jwt_shaped({"exp": now + 10 * 86400})
    host = StubHost(ss)
    host.replies["/api/v1/auth/login"] = ss.Reply(
        200, b"{}", (f"auth_token={token}; HttpOnly; Max-Age=99999999; Path=/",)
    )
    ss.run(ACCOUNT, host, now=now)
    state = json.loads((shared / f"{ACCOUNT}.session-token.json").read_text())
    assert state["cookies"][0]["expires"] == now + 86400


@pytest.mark.parametrize(
    "value",
    ["plain-value", "a.b", "a.!!!.c", "a.e30.c", "a.eyJleHAiOiAidG9tb3Jyb3cifQ.c", "a.WzFd.c"],
)
def test_an_unreadable_token_falls_back_to_the_cookie_and_the_cap(ss, value):
    assert ss.token_expiry(value) is None


# --- seat-tester-1 and --save-key anthropic (HOST 01M827TK7G, Arch 01M828NS6F, 11-22) ---

TESTER = "seat-tester-1"
TESTER_CRED = "seat-tester-1-credentials.txt"
KEY_FILE = "web-credential-anthropic-test-2026-10-15.txt"
# Key-shaped, built at run time so no key-shaped literal sits in the repo; it opens nothing.
FAKE_KEY = "sk-" + "ant-" + "api03-made-up-0123456789-abcdefghij"
FAKE_ADMIN_KEY = "sk-" + "ant-" + "admin01-made-up-0123456789-abcdefghij"
SAVE_SECRETS = SECRETS + (FAKE_KEY,)


def test_the_third_account_may_hold_an_anthropic_key_and_nothing_else(ss):
    third = ss.ACCOUNTS[TESTER]
    assert third.credential_file == TESTER_CRED and "credential" in third.credential_file
    assert third.provider_keys == frozenset({"anthropic"})
    assert not third.integrations and third.connectors is False
    # Every account's key list is the one provider, never more (the GitHub seat gained
    # it on 2026-11-26, HOST 01M8CT906X).
    for name, account in ss.ACCOUNTS.items():
        assert account.provider_keys <= frozenset({"anthropic"}), name


def test_the_key_list_is_one_provider_and_one_file_under_the_fleet_deny(ss):
    assert dict(ss.SAVABLE_KEYS) == {"anthropic": KEY_FILE}
    assert "credential" in KEY_FILE


@pytest.fixture
def tester(ss, shared):
    cred = shared / TESTER_CRED
    cred.write_text(f"username: {TESTER}\npassword: {PASSWORD}\n")
    cred.chmod(0o600)
    key = shared / KEY_FILE
    key.write_text(f"# the test workspace's spare key\nANTHROPIC_API_KEY={FAKE_KEY}\n")
    key.chmod(0o600)
    return shared


class KeyHost(StubHost):
    """Beta for a new account: no key until the store call, then one Anthropic key. The
    store's reply body echoes the key, to prove nothing from a body is ever printed."""

    def __init__(self, ss, store_status=201, lands=True, validated=True, **over):
        super().__init__(ss, **over)
        self.ss, self.store_status, self.lands, self.stored = ss, store_status, lands, False
        self.validated = validated
        self.replies["/api/v1/auth/me"] = ss.Reply(200, json.dumps({"username": TESTER}).encode())

    def __call__(self, method, path, data, headers):
        self.calls.append((method, path, data, dict(headers)))
        bare = path.split("?")[0]
        if bare == "/api/v1/keys/store":
            if 200 <= self.store_status < 300 and self.lands:
                self.stored = True
            return self.ss.Reply(self.store_status, f"echo {FAKE_KEY}".encode())
        if bare == "/api/v1/keys/list" and self.stored:
            row = {"provider": "anthropic", "is_validated": self.validated}
            return self.ss.Reply(200, json.dumps([row]).encode())
        return self.replies[bare]


def test_save_key_sends_the_files_key_once_and_prints_fixed_words(ss, tester):
    host = KeyHost(ss)
    line = ss.save_key(TESTER, "anthropic", host)
    assert line == f"{TESTER}: key saved; key on file: yes; validated: yes"
    stores = [c for c in host.calls if c[1] == "/api/v1/keys/store"]
    assert len(stores) == 1
    method, _, data, headers = stores[0]
    assert method == "POST" and headers["Content-Type"] == "application/json"
    assert json.loads(data) == {"provider": "anthropic", "api_key": FAKE_KEY, "validate": True}
    # the key is in that one body and nowhere else: no path, no header, no other body
    for _, path, other_data, other_headers in host.calls:
        assert FAKE_KEY not in path and FAKE_KEY not in json.dumps(other_headers)
        if path != "/api/v1/keys/store":
            assert other_data is None or FAKE_KEY.encode() not in other_data
    assert not (tester / f"{TESTER}.session-token.json").exists()  # saves no session


def test_save_key_runs_bound_2_before_and_after_the_store(ss, tester):
    host = KeyHost(ss)
    ss.save_key(TESTER, "anthropic", host)
    paths = [c[1].split("?")[0] for c in host.calls]
    store = paths.index("/api/v1/keys/store")
    for check in ("/api/v1/admin/account-flags", "/api/v1/integrations/health"):
        positions = [i for i, p in enumerate(paths) if p == check]
        assert len(positions) == 2 and positions[0] < store < positions[1], check


def test_save_key_refuses_when_a_key_is_already_there_and_sends_nothing(ss, tester):
    host = KeyHost(ss)
    host.stored = True
    with pytest.raises(ss.Refused, match="already has a key"):
        ss.save_key(TESTER, "anthropic", host)
    assert not [c for c in host.calls if c[1] == "/api/v1/keys/store"]


@pytest.mark.parametrize(
    "account, provider, reason",
    [
        ("xian", "anthropic", "not on the list"),
        (TESTER, "openai", "not on the key list"),
        ("seat-github-1", "openai", "not on the key list"),
    ],
)
def test_save_key_refuses_off_the_lists_before_any_file_or_call(
    ss, tester, account, provider, reason
):
    host = KeyHost(ss)
    with pytest.raises(ss.Refused, match=reason):
        ss.save_key(account, provider, host)
    assert host.calls == []


def test_save_key_refuses_an_account_whose_row_allows_no_key(ss, tester, monkeypatch):
    """Every real account's row now allows the one key, so this bound is exercised on a
    row that allows none (it was read on seat-github-1 until 2026-11-26)."""
    monkeypatch.setitem(
        ss.ACCOUNTS, "keyless-for-the-test", ss.Account(credential_file="x-credentials.txt")
    )
    host = KeyHost(ss)
    with pytest.raises(ss.Refused, match="may not hold"):
        ss.save_key("keyless-for-the-test", "anthropic", host)
    assert host.calls == []


def test_save_key_refuses_an_account_with_something_real_on_it(ss, tester):
    host = KeyHost(ss, **{"/api/v1/admin/account-flags": None})
    host.replies["/api/v1/admin/account-flags"] = ss.Reply(200, b"{}")
    with pytest.raises(ss.Refused, match="is an admin"):
        ss.save_key(TESTER, "anthropic", host)
    assert not [c for c in host.calls if c[1] == "/api/v1/keys/store"]


@pytest.mark.parametrize("status, word", [(400, "4xx"), (401, "4xx"), (500, "5xx"), (302, "3xx")])
def test_a_refused_store_prints_the_status_class_only(ss, tester, capsys, status, word):
    host = KeyHost(ss, store_status=status)
    ss.save_key.__defaults__ = (host,)
    code, text = _run_main(ss, ["--account", TESTER, "--save-key", "anthropic"], capsys)
    assert code == 2
    assert f"refused: the key save was not accepted (status {word})" in text
    for secret in SAVE_SECRETS:
        assert secret not in text


def test_an_accepted_store_with_no_key_on_file_refuses(ss, tester):
    with pytest.raises(ss.Refused, match="no key is on file"):
        ss.save_key(TESTER, "anthropic", KeyHost(ss, lands=False))


def test_save_key_through_main_prints_one_line_and_no_secret(ss, tester, capsys):
    ss.save_key.__defaults__ = (KeyHost(ss),)
    code, text = _run_main(ss, ["--account", TESTER, "--save-key", "anthropic"], capsys)
    assert code == 0
    assert text.strip() == f"{TESTER}: key saved; key on file: yes; validated: yes"
    for secret in SAVE_SECRETS:
        assert secret not in text


def test_save_key_unexpected_error_prints_class_name_only(ss, tester, capsys):
    def boom(method, path, data, headers):
        raise RuntimeError(f"leaky {FAKE_KEY} {PASSWORD}")

    ss.save_key.__defaults__ = (boom,)
    code, text = _run_main(ss, ["--account", TESTER, "--save-key", "anthropic"], capsys)
    assert code == 3 and "unexpected RuntimeError" in text
    for secret in SAVE_SECRETS:
        assert secret not in text


def test_main_takes_one_mode_and_only_listed_providers(ss, tester, capsys):
    code, text = _run_main(
        ss, ["--account", ACCOUNT, "--save-key", "anthropic", "--disconnect", "calendar"], capsys
    )
    assert code == 2 and "one mode at a time" in text
    with pytest.raises(SystemExit):
        ss.main(["--account", TESTER, "--save-key", "openai"])
    with pytest.raises(SystemExit):  # the key is never an argument
        ss.main(["--account", TESTER, "--save-key", "anthropic", "--key", FAKE_KEY])


def _key_file_cases():
    two = f"{FAKE_KEY}\n{FAKE_KEY}x\n"
    return [
        ("others can read it", lambda p: (p.write_text(FAKE_KEY), p.chmod(0o644)), "not mode 0600"),
        ("empty", lambda p: (p.write_text(""), p.chmod(0o600)), "exactly one key"),
        ("two keys", lambda p: (p.write_text(two), p.chmod(0o600)), "exactly one key"),
        ("no key shape", lambda p: (p.write_text("hello"), p.chmod(0o600)), "exactly one key"),
        ("missing", lambda p: p.unlink(), "not readable"),
    ]


@pytest.mark.parametrize("name, spoil, reason", _key_file_cases(), ids=lambda v: str(v)[:20])
def test_save_key_refuses_a_key_file_it_should_not_trust(ss, tester, capsys, name, spoil, reason):
    spoil(tester / KEY_FILE)
    host = KeyHost(ss)
    ss.save_key.__defaults__ = (host,)
    code, text = _run_main(ss, ["--account", TESTER, "--save-key", "anthropic"], capsys)
    assert code == 2 and reason in text
    assert host.calls == []
    assert FAKE_KEY not in text


def test_save_key_refuses_a_link_in_place_of_the_key_file(ss, tester):
    real = tester / "elsewhere.txt"
    real.write_text(FAKE_KEY)
    real.chmod(0o600)
    (tester / KEY_FILE).unlink()
    (tester / KEY_FILE).symlink_to(real)
    with pytest.raises(ss.Refused, match="not a regular file"):
        ss.save_key(TESTER, "anthropic", KeyHost(ss))


def test_the_same_key_written_twice_is_one_key(ss, tester):
    (tester / KEY_FILE).write_text(f"key: {FAKE_KEY}\n# again: {FAKE_KEY}\n")
    assert ss.read_key_file(tester / KEY_FILE) == FAKE_KEY


def test_the_docstring_says_thirty_minutes(ss):
    source = (ROOT / "scripts" / "seat_session.py").read_text()
    assert "30 minutes" in source and "24 hours at most" not in source


# --- Arch 01M82BT11P and HOST 01M82C816F (11-22): the validated word; API keys only ---


@pytest.mark.parametrize("validated", [False, None, "true", 1])
def test_a_key_the_provider_did_not_accept_says_validated_no_and_exits_5(
    ss, tester, capsys, validated
):
    """The store keeps a refused key and still answers 2xx, so only the list row's
    boolean ``True`` counts. Anything else is "no" and a non-zero exit."""
    ss.save_key.__defaults__ = (KeyHost(ss, validated=validated),)
    code, text = _run_main(ss, ["--account", TESTER, "--save-key", "anthropic"], capsys)
    assert code == 5
    assert text.strip() == f"{TESTER}: key saved; key on file: yes; validated: no"
    for secret in SAVE_SECRETS:
        assert secret not in text


def test_a_second_run_after_validated_no_refuses_because_a_key_is_on_file(ss, tester):
    host = KeyHost(ss, validated=False)
    with pytest.raises(ss.KeyNotValidated):
        ss.save_key(TESTER, "anthropic", host)
    with pytest.raises(ss.Refused, match="already has a key"):
        ss.save_key(TESTER, "anthropic", host)
    assert len([c for c in host.calls if c[1] == "/api/v1/keys/store"]) == 1


@pytest.mark.parametrize(
    "content",
    [
        FAKE_ADMIN_KEY,
        f"{FAKE_KEY}\n{FAKE_ADMIN_KEY}\n",
        "sk-" + "ant-" + "oat01-made-up-0123456789",
    ],
    ids=["admin only", "api and admin", "another kind"],
)
def test_a_file_with_anything_but_a_standard_api_key_is_refused(ss, tester, content):
    (tester / KEY_FILE).write_text(content)
    host = KeyHost(ss)
    with pytest.raises(ss.Refused, match="not a standard API key"):
        ss.save_key(TESTER, "anthropic", host)
    assert host.calls == []


# --- Arch 01M8CN4PR6 (2026-11-26): a closed list of two prefixes, api and usr ---

FAKE_USR_KEY = "sk-" + "ant-" + "usr-1made-up-0123456789-abcdefghijklmnop"


def test_the_accepted_prefixes_are_a_closed_list_of_two(ss):
    assert ss.PERSON_KEY_PREFIXES == ("sk-ant-api", "sk-ant-usr")
    # The shape is generated from the tuple, so the two cannot drift apart.
    for prefix in ss.PERSON_KEY_PREFIXES:
        assert ss._KEY_SHAPE.fullmatch(prefix + "-" + "a" * 30)
    source = (ROOT / "scripts" / "seat_session.py").read_text()
    assert source.count('"sk-ant-usr"') == 1 and source.count('"sk-ant-api"') == 1


@pytest.mark.parametrize("key", [FAKE_KEY, FAKE_USR_KEY], ids=["api", "usr"])
def test_a_file_with_one_person_key_of_either_form_is_read(ss, tester, key):
    (tester / KEY_FILE).write_text(f"ANTHROPIC_API_KEY={key}\n")
    assert ss.read_key_file(tester / KEY_FILE) == key


def test_a_usr_key_is_sent_whole_and_saved(ss, tester):
    (tester / KEY_FILE).write_text(FAKE_USR_KEY + "\n")
    host = KeyHost(ss)
    ss.save_key(TESTER, "anthropic", host)
    stored = [c for c in host.calls if c[1] == "/api/v1/keys/store"]
    assert len(stored) == 1
    assert json.loads(stored[0][2])["api_key"] == FAKE_USR_KEY


@pytest.mark.parametrize(
    "content, reason",
    [
        ("sk-" + "ant-" + "admin01-made-up-0123456789-abcdefghij", "not a standard API key"),
        (f"{FAKE_USR_KEY}\n# shown as sk-" + "ant-" + "usr-1Xv…RgAA\n", "not a standard API key"),
        (f"{FAKE_KEY}\n# shown as sk-" + "ant-" + "api03…\n", "not a standard API key"),
        (f"{FAKE_USR_KEY}\n{FAKE_USR_KEY}x\n", "exactly one key"),
        (f"{FAKE_USR_KEY}\n{FAKE_KEY}\n", "exactly one key"),
        ("sk-" + "ant-" + "usr-short", "not a standard API key"),
    ],
    ids=[
        "admin",
        "usr plus a masked form",
        "api plus a masked form",
        "two usr keys",
        "one usr and one api",
        "a short usr string",
    ],
)
def test_everything_else_still_refuses_the_file_before_any_request(ss, tester, content, reason):
    (tester / KEY_FILE).write_text(content)
    host = KeyHost(ss)
    with pytest.raises(ss.Refused, match=reason):
        ss.save_key(TESTER, "anthropic", host)
    assert host.calls == []


def test_a_usr_key_the_provider_refuses_still_exits_non_zero(ss, tester, capsys):
    """Arch's condition 2: the validated word stays, so a usr key beta's validator
    rejects never looks saved."""
    (tester / KEY_FILE).write_text(FAKE_USR_KEY + "\n")
    ss.save_key.__defaults__ = (KeyHost(ss, validated=False),)
    code, text = _run_main(ss, ["--account", TESTER, "--save-key", "anthropic"], capsys)
    assert code == 5
    assert text.strip() == f"{TESTER}: key saved; key on file: yes; validated: no"
    assert FAKE_USR_KEY not in text


# --- HOST 01M82C816F and 01M82F420Z (11-22): the remove mode, recovery after "validated: no" ---


class DeadKeyHost(KeyHost):
    """Beta for the tester account with a key already on file. ``removes`` False models a
    delete route that answers 2xx and leaves the row."""

    def __init__(self, ss, validated=False, delete_status=200, removes=True, **over):
        super().__init__(ss, validated=validated, **over)
        self.stored, self.delete_status, self.removes = True, delete_status, removes

    def __call__(self, method, path, data, headers):
        if method == "DELETE":
            self.calls.append((method, path, data, dict(headers)))
            if 200 <= self.delete_status < 300 and self.removes:
                self.stored = False
            return self.ss.Reply(self.delete_status, f"echo {FAKE_KEY}".encode())
        return super().__call__(method, path, data, headers)


def _deletes(host):
    return [c for c in host.calls if c[0] == "DELETE"]


@pytest.mark.parametrize("validated", [False, None, "true", 1])
def test_remove_key_clears_a_key_the_provider_did_not_accept(ss, tester, validated):
    host = DeadKeyHost(ss, validated=validated)
    assert ss.remove_key(TESTER, "anthropic", host) == f"{TESTER}: key removed; key on file: no"
    assert [c[1] for c in _deletes(host)] == ["/api/v1/keys/anthropic"]
    assert _deletes(host)[0][2] is None  # nothing is sent in the body
    assert not [c for c in host.calls if c[1] == "/api/v1/keys/store"]
    assert not list(tester.glob("*session*"))  # no session is saved


def test_remove_key_runs_bound_2_before_and_after_the_delete(ss, tester):
    host = DeadKeyHost(ss)
    ss.remove_key(TESTER, "anthropic", host)
    paths = [c[1].split("?")[0] for c in host.calls]
    at = paths.index("/api/v1/keys/anthropic")
    assert "/api/v1/admin/account-flags" in paths[:at]
    assert "/api/v1/admin/account-flags" in paths[at + 1 :]


def test_remove_key_refuses_a_validated_key_and_sends_nothing(ss, tester):
    host = DeadKeyHost(ss, validated=True)
    with pytest.raises(ss.Refused, match="validated; a working key is not removed"):
        ss.remove_key(TESTER, "anthropic", host)
    assert not _deletes(host)


class SeatGitHubKeyHost(DeadKeyHost):
    """Beta for seat-github-1: GitHub live as the machine login, a key already on file."""

    def __init__(self, ss, **over):
        super().__init__(ss, **over)
        self.replies["/api/v1/auth/me"] = ss.Reply(
            200, json.dumps({"username": "seat-github-1"}).encode()
        )
        rows = [{"name": n, "status": "not_configured"} for n in ("notion", "slack", "calendar")]
        rows.append({"name": "github", **_live()})
        self.replies["/api/v1/integrations/health"] = ss.Reply(
            200, json.dumps({"integrations": rows}).encode()
        )


@pytest.fixture
def seat_github(ss, shared):
    cred = shared / "seat-github-1-credentials.txt"
    cred.write_text(f"username: seat-github-1\npassword: {PASSWORD}\n")
    cred.chmod(0o600)
    return shared


def test_remove_key_never_clears_a_working_key_on_seat_github_1(ss, seat_github):
    """HOST 01M8CVHZBJ, Arch 01M8CVHXAG (2026-11-26): the account is on the list for the
    refused-key case only. A key the provider accepted is refused and nothing is sent; it
    leaves the account only by xian's hand."""
    host = SeatGitHubKeyHost(ss, validated=True)
    with pytest.raises(ss.Refused, match="validated; a working key is not removed"):
        ss.remove_key("seat-github-1", "anthropic", host)
    assert not _deletes(host)


@pytest.mark.parametrize("validated", [False, None])
def test_remove_key_clears_a_refused_key_on_seat_github_1(ss, seat_github, validated):
    host = SeatGitHubKeyHost(ss, validated=validated)
    line = ss.remove_key("seat-github-1", "anthropic", host)
    assert line == "seat-github-1: key removed; key on file: no"
    assert len(_deletes(host)) == 1


def test_remove_key_with_no_key_on_file_says_so_and_sends_nothing(ss, tester):
    host = KeyHost(ss)
    assert (
        ss.remove_key(TESTER, "anthropic", host) == f"{TESTER}: no key to remove; key on file: no"
    )
    assert not _deletes(host)


@pytest.mark.parametrize(
    "account, provider",
    [
        (ACCOUNT, "anthropic"),
        ("seat-github-1", "openai"),
        (TESTER, "openai"),
        ("x", "anthropic"),
    ],
)
def test_remove_key_refuses_off_its_closed_list_before_any_call(ss, tester, account, provider):
    """``web-seed-1386`` holds a key other served rows depend on; it is not removable.
    ``seat-github-1`` is on the list for Anthropic only (the refused-key recovery)."""
    host = DeadKeyHost(ss)
    with pytest.raises(ss.Refused):
        ss.remove_key(account, provider, host)
    assert host.calls == []
    # seat-github-1 joined on 2026-11-26 (HOST 01M8CVHZBJ, Arch 01M8CVHXAG), for a key
    # the provider refused only; web-seed-1386 stays off.
    assert ss.KEY_REMOVABLE == {
        TESTER: frozenset({"anthropic"}),
        "seat-github-1": frozenset({"anthropic"}),
    }


@pytest.mark.parametrize("status, word", [(404, "4xx"), (500, "5xx")])
def test_a_refused_removal_prints_the_status_class_only(ss, tester, capsys, status, word):
    ss.remove_key.__defaults__ = (DeadKeyHost(ss, delete_status=status),)
    code, text = _run_main(ss, ["--account", TESTER, "--remove-key", "anthropic"], capsys)
    assert code == 2
    assert text.strip() == (
        f"seat_session: refused: the key removal was not accepted (status {word})"
    )
    for secret in SAVE_SECRETS:
        assert secret not in text


def test_an_accepted_removal_that_leaves_the_key_refuses(ss, tester):
    with pytest.raises(ss.Refused, match="a key is still on file"):
        ss.remove_key(TESTER, "anthropic", DeadKeyHost(ss, removes=False))


def test_remove_key_never_opens_the_key_file(ss, tester):
    (tester / KEY_FILE).unlink()
    assert ss.remove_key(TESTER, "anthropic", DeadKeyHost(ss)).endswith("key on file: no")


def test_remove_key_through_main_prints_one_line_and_no_secret(ss, tester, capsys):
    ss.remove_key.__defaults__ = (DeadKeyHost(ss),)
    code, text = _run_main(ss, ["--account", TESTER, "--remove-key", "anthropic"], capsys)
    assert code == 0
    assert text.strip() == f"{TESTER}: key removed; key on file: no"
    for secret in SAVE_SECRETS:
        assert secret not in text


def test_remove_key_unexpected_error_prints_class_name_only(ss, tester, capsys):
    def boom(*_args, **_kwargs):
        raise RuntimeError(f"body with {FAKE_KEY}")

    ss.remove_key.__defaults__ = (boom,)
    code, text = _run_main(ss, ["--account", TESTER, "--remove-key", "anthropic"], capsys)
    assert code == 3 and text.strip() == "seat_session: refused: unexpected RuntimeError"


def test_remove_key_is_its_own_mode_and_takes_only_listed_providers(ss, tester, capsys):
    for other in (["--save-key", "anthropic"], ["--disconnect", "calendar"]):
        code, text = _run_main(
            ss, ["--account", TESTER, "--remove-key", "anthropic", *other], capsys
        )
        assert code == 2 and "one mode at a time" in text
    with pytest.raises(SystemExit):
        ss.main(["--account", TESTER, "--remove-key", "openai"])


def test_after_a_removal_a_save_can_run_again(ss, tester):
    host = DeadKeyHost(ss)
    ss.remove_key(TESTER, "anthropic", host)
    host.validated = True
    assert ss.save_key(TESTER, "anthropic", host).endswith("validated: yes")


# --- Issue 2282 box 4 (Arch 01M8728HYN, 2026-11-24): the third start, the /setup calendar step ---

SETUP_CAL_START = "/api/v1/setup/calendar/oauth/start"


def test_setup_calendar_prints_the_return_address_and_nothing_else(ss, sr, shared):
    _saved(ss, shared)
    reply = _connect_reply(
        ss, redirect="https://beta.pipermorgan.ai/api/v1/setup/calendar/oauth/callback"
    )
    host = StubHost(ss, **{SETUP_CAL_START: reply})
    line = sr.read_redirect_uri(ACCOUNT, "setup-calendar", host, now=1_800_000_100)
    assert line == (
        "setup-calendar redirect_uri: "
        "https://beta.pipermorgan.ai/api/v1/setup/calendar/oauth/callback"
    )
    assert [(c[0], c[1]) for c in host.calls] == [("GET", SETUP_CAL_START)]


def test_setup_calendar_shows_an_alpha_return_address_as_it_is(ss, sr, shared):
    """The read exists to find this case: the line says alpha if the host names alpha."""
    _saved(ss, shared)
    reply = _connect_reply(
        ss, redirect="https://alpha.pipermorgan.ai/api/v1/setup/calendar/oauth/callback"
    )
    host = StubHost(ss, **{SETUP_CAL_START: reply})
    line = sr.read_redirect_uri(ACCOUNT, "setup-calendar", host, now=1_800_000_100)
    assert line.endswith("https://alpha.pipermorgan.ai/api/v1/setup/calendar/oauth/callback")


def test_setup_calendar_has_no_host_switch_and_refuses_one(ss, sr, shared):
    _saved(ss, shared)
    other = {"switch_host_url": "https://beta.pipermorgan.ai/settings/integrations/calendar"}
    host = StubHost(ss, **{SETUP_CAL_START: _raw_reply(ss, other)})
    with pytest.raises(ss.Refused, match="not the page"):
        sr.read_redirect_uri(ACCOUNT, "setup-calendar", host, now=1_800_000_100)


def test_the_setup_start_can_never_be_read_as_a_body_and_its_callback_fits(ss, sr, shared):
    _saved(ss, shared)
    assert SETUP_CAL_START == sr.REDIRECT_URI_ROUTES["setup-calendar"]
    assert SETUP_CAL_START not in sr.ALLOWED_PATHS
    with pytest.raises(ss.Refused, match="not on the list"):
        sr.read(ACCOUNT, SETUP_CAL_START, StubHost(ss), now=1_800_000_100)
    shown = sr.host_and_path("https://beta.pipermorgan.ai/api/v1/setup/calendar/oauth/callback")
    assert shown == "https://beta.pipermorgan.ai/api/v1/setup/calendar/oauth/callback"
