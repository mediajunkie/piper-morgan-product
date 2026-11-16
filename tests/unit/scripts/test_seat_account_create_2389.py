"""#2389 (ADR-084 D3, Step F0): the seat account create script.

Every value here is made up. The stand-in host records what it is sent; nothing leaves
the test process, and the shared folder is a temporary one.
"""

import json
import stat
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[3] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import seat_account_create as create  # noqa: E402
import seat_session  # noqa: E402
from seat_session import Refused, Reply  # noqa: E402

ACCOUNT = "seat-github-1"
INVITE = "MADE-UP-INVITE-CODE-0001"
EMAIL = "made-up-address@example.invalid"


class Host:
    """A stand-in for beta. ``outcome`` decides what the sign-up call answers."""

    def __init__(self, outcome="created"):
        self.outcome = outcome
        self.calls = []
        self.password = None
        self.exists = False

    def __call__(self, method, path, data, headers):
        self.calls.append((method, path))
        if path == "/api/v1/setup/create-user":
            sent = json.loads(data.decode())
            self.password = sent["password"]
            self.sent = sent
            if self.outcome == "created":
                self.exists = True
                return Reply(200, json.dumps({"success": True, "user_id": "x"}).encode(), ("c=1",))
            if self.outcome == "refused":
                return Reply(400, b"", ())
            if self.outcome == "invalid":
                return Reply(422, b"", ())
            if self.outcome == "created-but-no-answer":
                self.exists = True
                raise TimeoutError("the reply never arrived, with a secret in its text")
            if self.outcome == "down":
                return Reply(503, b"", ())
        if path == "/api/v1/auth/login":
            return Reply(200 if self.exists else 401, b"", ())
        raise AssertionError(f"unexpected request {method} {path}")


@pytest.fixture(autouse=True)
def _the_account_row(monkeypatch):
    """The real row for this name is CIO's diff, read by HOST. Until it is on main the
    tests supply the row the design agreed: this credential file, nothing allowed."""
    monkeypatch.setitem(
        seat_session.ACCOUNTS,
        ACCOUNT,
        seat_session.Account(credential_file="seat-github-1-credentials.txt"),
    )


@pytest.fixture(autouse=True)
def _no_test_reaches_the_real_host(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("a test reached the real transport")

    monkeypatch.setattr(seat_session, "http_transport", forbidden)


@pytest.fixture
def shared(tmp_path, monkeypatch):
    folder = tmp_path / "shared"
    folder.mkdir(mode=0o700)
    monkeypatch.setattr(seat_session, "shared_dir", lambda: folder)
    return folder


@pytest.fixture
def invite_file(shared):
    path = shared / f"{ACCOUNT}-invite-token.txt"
    path.write_text(f"invite: {INVITE}\nemail: {EMAIL}\n")
    path.chmod(0o600)
    return path


def _leaks(text, host):
    return [v for v in (INVITE, EMAIL, host.password) if v and v in text]


def test_a_good_run_creates_writes_the_credential_file_and_deletes_the_invite(shared, invite_file):
    host = Host()
    line = create.run(ACCOUNT, host)
    assert line == f"{ACCOUNT} created"
    assert host.calls == [("POST", "/api/v1/setup/create-user")]
    assert host.sent["username"] == ACCOUNT and host.sent["invite_token"] == INVITE
    assert host.sent["password"] == host.sent["password_confirm"] and len(host.password) >= 40
    written = shared / seat_session.ACCOUNTS[ACCOUNT].credential_file
    assert written.read_text() == f"username: {ACCOUNT}\npassword: {host.password}\n"
    assert stat.S_IMODE(written.stat().st_mode) == 0o600
    assert not invite_file.exists(), "the spent invite file was kept"
    assert seat_session.read_credentials(written) == (ACCOUNT, host.password)
    assert _leaks(line, host) == []


def test_two_runs_generate_different_passwords(shared, invite_file):
    first = Host()
    create.run(ACCOUNT, first)
    (shared / seat_session.ACCOUNTS[ACCOUNT].credential_file).unlink()
    invite_file.write_text(f"invite: {INVITE}\nemail: {EMAIL}\n")
    invite_file.chmod(0o600)
    second = Host()
    create.run(ACCOUNT, second)
    assert first.password != second.password


def test_a_name_off_the_list_is_refused_before_anything_is_read(shared):
    host = Host()
    with pytest.raises(Refused, match="not on the list"):
        create.run("someone-else", host)
    assert host.calls == []


def test_an_account_that_already_has_a_credential_file_is_refused(shared, invite_file):
    (shared / seat_session.ACCOUNTS[ACCOUNT].credential_file).write_text("x")
    host = Host()
    with pytest.raises(Refused, match="created before"):
        create.run(ACCOUNT, host)
    assert host.calls == [] and invite_file.exists()


def test_a_missing_invite_file_is_refused(shared):
    host = Host()
    with pytest.raises(Refused, match="not there"):
        create.run(ACCOUNT, host)
    assert host.calls == []


def test_an_invite_file_others_can_read_is_refused(shared, invite_file):
    invite_file.chmod(0o644)
    host = Host()
    with pytest.raises(Refused, match="not mode 0600"):
        create.run(ACCOUNT, host)
    assert host.calls == []


@pytest.mark.parametrize(
    "text,missing",
    ((f"email: {EMAIL}\n", "invite"), (f"invite: {INVITE}\n", "email")),
)
def test_a_missing_line_is_named_and_nothing_from_the_file_is_shown(shared, text, missing):
    path = shared / f"{ACCOUNT}-invite-token.txt"
    path.write_text(text)
    path.chmod(0o600)
    with pytest.raises(Refused) as refusal:
        create.run(ACCOUNT, Host())
    assert f"no '{missing}' line" in str(refusal.value)
    assert INVITE not in str(refusal.value) and EMAIL not in str(refusal.value)


@pytest.mark.parametrize("outcome", ("refused", "invalid", "down"))
def test_a_failed_sign_up_keeps_the_invite_file_and_writes_no_credential_file(
    shared, invite_file, outcome
):
    host = Host(outcome)
    with pytest.raises(Refused) as refusal:
        create.run(ACCOUNT, host)
    assert invite_file.exists()
    assert not (shared / seat_session.ACCOUNTS[ACCOUNT].credential_file).exists()
    assert _leaks(str(refusal.value), host) == []
    assert "kept" in str(refusal.value)


def test_an_account_created_with_no_answer_still_gets_its_credential_file(shared, invite_file):
    host = Host("created-but-no-answer")
    assert create.run(ACCOUNT, host) == f"{ACCOUNT} created"
    assert host.calls == [("POST", "/api/v1/setup/create-user"), ("POST", "/api/v1/auth/login")]
    written = shared / seat_session.ACCOUNTS[ACCOUNT].credential_file
    assert host.password in written.read_text()
    assert not invite_file.exists()


def test_main_prints_only_the_name_or_a_fixed_reason(shared, invite_file, monkeypatch, capsys):
    host = Host()
    monkeypatch.setattr(seat_session, "http_transport", host)
    assert create.main(["--account", ACCOUNT]) == 0
    out = capsys.readouterr()
    assert out.out.strip() == f"{ACCOUNT} created" and out.err == ""
    assert _leaks(out.out + out.err, host) == []

    assert create.main(["--account", ACCOUNT]) == 2  # the credential file now exists
    out = capsys.readouterr()
    assert out.out == "" and out.err.startswith("seat_account_create: refused: ")
    assert _leaks(out.err, host) == []


def test_an_unexpected_error_prints_its_class_name_only(shared, invite_file, monkeypatch, capsys):
    def boom(account, send=None):
        raise RuntimeError(f"text with {INVITE} in it")

    monkeypatch.setattr(create, "run", boom)
    assert create.main(["--account", ACCOUNT]) == 3
    err = capsys.readouterr().err
    assert err.strip() == "seat_account_create: refused: unexpected RuntimeError"


def test_there_is_no_host_option_and_no_value_reaches_argv():
    source = (SCRIPTS / "seat_account_create.py").read_text()
    assert "--host" not in source.replace("No ``--host`` option exists", "")
    assert "print(password" not in source and "print(invite" not in source
    assert 'add_argument("--invite' not in source and 'add_argument("--email' not in source


# --- xian's half: --write-invite -----------------------------------------------------


def _typed(code=INVITE, email=EMAIL):
    return {"ask_hidden": lambda prompt: code, "ask": lambda prompt: email}


def test_write_invite_writes_the_two_lines_at_mode_0600_and_the_create_run_reads_them(shared):
    line = create.write_invite(ACCOUNT, is_terminal=lambda: True, **_typed())
    assert line == f"{ACCOUNT} invite file written"
    path = shared / f"{ACCOUNT}-invite-token.txt"
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    assert create.read_invite(path) == (INVITE, EMAIL)
    assert INVITE not in line and EMAIL not in line
    host = Host()
    assert create.run(ACCOUNT, host) == f"{ACCOUNT} created"
    assert host.sent["invite_token"] == INVITE and host.sent["email"] == EMAIL


def test_write_invite_refuses_without_a_terminal_and_asks_nothing(shared):
    asked = []
    with pytest.raises(Refused, match="needs a terminal"):
        create.write_invite(
            ACCOUNT,
            ask_hidden=lambda p: asked.append(p) or INVITE,
            ask=lambda p: asked.append(p) or EMAIL,
            is_terminal=lambda: False,
        )
    assert asked == [] and not (shared / f"{ACCOUNT}-invite-token.txt").exists()


def test_write_invite_refuses_an_existing_file_or_a_made_account(shared, invite_file):
    with pytest.raises(Refused, match="already there"):
        create.write_invite(ACCOUNT, is_terminal=lambda: True, **_typed())
    invite_file.unlink()
    (shared / "seat-github-1-credentials.txt").write_text("x")
    with pytest.raises(Refused, match="created before"):
        create.write_invite(ACCOUNT, is_terminal=lambda: True, **_typed())


@pytest.mark.parametrize("code,email", (("", EMAIL), (INVITE, ""), ("  ", EMAIL)))
def test_write_invite_refuses_an_empty_answer_and_writes_nothing(shared, code, email):
    with pytest.raises(Refused, match="both needed"):
        create.write_invite(ACCOUNT, is_terminal=lambda: True, **_typed(code, email))
    assert not (shared / f"{ACCOUNT}-invite-token.txt").exists()


def test_write_invite_refuses_a_name_off_the_list(shared):
    with pytest.raises(Refused, match="not on the list"):
        create.write_invite("someone-else", is_terminal=lambda: True, **_typed())
