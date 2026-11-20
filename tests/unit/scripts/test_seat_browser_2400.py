"""seat_browser.py, its hook in seat_session.py, and seat-browser-mcp.sh (ADR-084 D3 browser
half, issue 2400).

No browser is started and nothing calls beta. The cookie value is built from parts, and
every output is searched for it. The DevTools client is run against a small WebSocket
server in this file.
"""

import base64
import hashlib
import importlib.util
import json
import socket
import struct
import subprocess
import sys
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
ACCOUNT = "web-seed-1386"
VALUE = "-".join(["made", "up", "cookie", "71c2"])
NOW = 1_800_000_000
BINARY = "/Users/xian/.claude-pm/chrome-for-testing.app/Contents/MacOS/Google Chrome for Testing"


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
def mods(tmp_path, monkeypatch):
    ss = _load("seat_session")
    _load("seat_read")
    sb = _load("seat_browser")
    monkeypatch.setattr(ss, "shared_dir", lambda: tmp_path)
    return ss, sb


@pytest.fixture
def conf(tmp_path):
    path = tmp_path / "conf"
    path.write_text("# seat port\nweb 9333  # first\nlead 9334\n")
    return path


def _save(ss, tmp_path, expires=NOW + 3600, **over):
    row = {
        "name": ss.AUTH_COOKIE,
        "value": VALUE,
        "domain": "beta.pipermorgan.ai",
        "path": "/",
        "expires": expires,
        "httpOnly": True,
        "secure": True,
        "sameSite": "Lax",
    }
    row.update(over)
    state = {"account": ACCOUNT, "host": ss.HOST, "saved_at": NOW, "cookies": [row], "origins": []}
    path = ss.session_path(ACCOUNT)
    path.write_text(json.dumps(state))
    path.chmod(0o600)
    return path


class StubBrowser:
    """Keeps what Storage.setCookies gives it, like a browser would."""

    def __init__(self, set_error=False, drop=False, http_only=True, change_value=False):
        self.calls, self.held = [], []
        self.set_error, self.drop, self.http_only, self.change = (
            set_error,
            drop,
            http_only,
            change_value,
        )

    def connect(self, seat, port):
        self.seat, self.port = seat, port
        return self.call

    def call(self, method, params):
        self.calls.append((method, params))
        if method == "Storage.setCookies":
            if self.set_error:
                return {"id": 1, "error": {"message": f"bad cookie {VALUE}"}}
            if not self.drop:
                for cookie in params["cookies"]:
                    kept = dict(cookie, httpOnly=self.http_only)
                    if self.change:
                        kept["value"] = "another"
                    self.held.append(kept)
            return {"id": 1, "result": {}}
        return {"id": 2, "result": {"cookies": self.held}}


def test_place_sends_one_httponly_cookie_and_prints_one_line(mods, conf, tmp_path):
    ss, sb = mods
    _save(ss, tmp_path)
    browser = StubBrowser()
    line = sb.place(ACCOUNT, seat="web", now=NOW, connect=browser.connect, conf=conf)
    assert line == f"{ACCOUNT} placed in seat browser web, expires 2027-01-15T09:00:00Z"
    assert VALUE not in line
    assert (browser.seat, browser.port) == ("web", 9333)
    method, params = browser.calls[0]
    assert method == "Storage.setCookies"
    assert params["cookies"] == [
        {
            "name": "auth_token",
            "value": VALUE,
            "domain": "beta.pipermorgan.ai",
            "path": "/",
            "expires": NOW + 3600,
            "httpOnly": True,
            "secure": True,
            "sameSite": "Lax",
        }
    ]


@pytest.mark.parametrize(
    "browser_kwargs, reason",
    [
        ({"set_error": True}, "did not take the session"),
        ({"drop": True}, "does not hold the session as placed"),
        ({"http_only": False}, "does not hold the session as placed"),
        ({"change_value": True}, "does not hold the session as placed"),
    ],
)
def test_place_refuses_when_the_browser_does_not_hold_it_as_placed(
    mods, conf, tmp_path, browser_kwargs, reason
):
    ss, sb = mods
    _save(ss, tmp_path)
    with pytest.raises(ss.Refused) as refusal:
        sb.place(
            ACCOUNT, seat="web", now=NOW, connect=StubBrowser(**browser_kwargs).connect, conf=conf
        )
    assert reason in str(refusal.value)
    assert VALUE not in str(refusal.value)


def test_place_refuses_an_account_or_a_seat_not_on_its_list(mods, conf, tmp_path):
    ss, sb = mods
    _save(ss, tmp_path)
    browser = StubBrowser()
    with pytest.raises(ss.Refused, match="not on the list"):
        sb.place("xian", seat="web", now=NOW, connect=browser.connect, conf=conf)
    with pytest.raises(ss.Refused, match="has no seat browser"):
        sb.place(ACCOUNT, seat="cio", now=NOW, connect=browser.connect, conf=conf)
    assert browser.calls == []


def test_place_refuses_an_expired_a_missing_or_a_loose_session_and_sends_nothing(
    mods, conf, tmp_path
):
    ss, sb = mods
    browser = StubBrowser()
    with pytest.raises(ss.Refused, match="no saved session"):
        sb.place(ACCOUNT, seat="web", now=NOW, connect=browser.connect, conf=conf)
    _save(ss, tmp_path, expires=NOW - 1)
    with pytest.raises(ss.Refused, match="expired"):
        sb.place(ACCOUNT, seat="web", now=NOW, connect=browser.connect, conf=conf)
    _save(ss, tmp_path).chmod(0o644)
    with pytest.raises(ss.Refused, match="0600"):
        sb.place(ACCOUNT, seat="web", now=NOW, connect=browser.connect, conf=conf)
    _save(ss, tmp_path, domain="example.com")
    with pytest.raises(ss.Refused, match="expected form"):
        sb.place(ACCOUNT, seat="web", now=NOW, connect=browser.connect, conf=conf)
    assert browser.calls == []


# --- which browser is on the port ---------------------------------------------------------


def _identity(sb, tmp_path, command=None, fields=None, version=None, mode=0o700, make=True):
    folder = sb.profile_dir("web")
    if make:
        folder.mkdir(mode=0o700, exist_ok=True)
        folder.chmod(mode)
    if command is None:
        command = (
            f"{BINARY} --headless=new --remote-debugging-port=9333 "
            f"--user-data-dir={folder} --use-mock-keychain"
        )
    if version is None:
        version = {"webSocketDebuggerUrl": "ws://127.0.0.1:9333/devtools/browser/ab12-cd34"}
    return sb.browser_socket_path(
        "web",
        9333,
        get_json=lambda port, path: version,
        listener=lambda port: ["p4242", "f53", "n127.0.0.1:9333"] if fields is None else fields,
        command_line=lambda pid: command,
    )


def test_the_seat_browser_is_recognised_by_its_process(mods, tmp_path):
    _, sb = mods
    assert _identity(sb, tmp_path) == "/devtools/browser/ab12-cd34"
    assert sb.profile_dir("web").name == "seat-browser-credential-profile-web"  # under a Read deny


@pytest.mark.parametrize(
    "kwargs, reason",
    [
        ({"make": False}, "profile folder does not exist"),
        ({"mode": 0o755}, "not mode 0700"),
        ({"fields": []}, "not answering"),
        ({"fields": ["p1", "n*:9333"]}, "127.0.0.1 only"),
        ({"fields": ["p1", "n127.0.0.1:9333", "p2", "n127.0.0.1:9333"]}, "127.0.0.1 only"),
        ({"fields": ["p1", "n127.0.0.1:9333", "n[::1]:9333"]}, "127.0.0.1 only"),
        (
            {"command": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome --x"},
            "not the cohort's test browser",
        ),
        (
            {"command": f"{BINARY} --user-data-dir=/Users/xian/elsewhere --use-mock-keychain"},
            "not on this seat's profile folder",
        ),
        ({"version": {"webSocketDebuggerUrl": "ws://10.0.0.5:9333/devtools/browser/x"}}, "form"),
        (
            {"version": {"webSocketDebuggerUrl": "ws://127.0.0.1:9333/devtools/browser/a/../b"}},
            "form",
        ),
        ({"version": {}}, "form"),
    ],
)
def test_any_other_browser_on_the_port_is_refused(mods, tmp_path, kwargs, reason):
    ss, sb = mods
    with pytest.raises(ss.Refused) as refusal:
        _identity(sb, tmp_path, **kwargs)
    assert reason in str(refusal.value)


def test_a_browser_without_the_fake_keychain_or_with_wildcard_origins_is_refused(mods, tmp_path):
    ss, sb = mods
    folder = sb.profile_dir("web")
    base = f"{BINARY} --remote-debugging-port=9333 --user-data-dir={folder}"
    with pytest.raises(ss.Refused, match="--use-mock-keychain"):
        _identity(sb, tmp_path, command=base)
    with pytest.raises(ss.Refused, match="--remote-allow-origins"):
        _identity(sb, tmp_path, command=base + " --use-mock-keychain --remote-allow-origins=*")


# --- the conf, the one place a port is written ---------------------------------------------


def test_the_tracked_conf_parses_and_names_only_served_read_seats(mods):
    _, sb = mods
    assert sb.seats() == {"web": 9333}


@pytest.mark.parametrize(
    "text", ["web\n", "web 80\n", "web 9333 extra\n", "web 9333\nweb 9334\n", "a 9333\nb 9333\n"]
)
def test_a_conf_row_that_cannot_be_read_refuses(mods, tmp_path, text):
    ss, sb = mods
    path = tmp_path / "bad"
    path.write_text(text)
    with pytest.raises(ss.Refused):
        sb.seats(path)


def test_where_prints_the_port_and_the_folder_for_the_launch_wrapper(mods, conf, tmp_path):
    _, sb = mods
    assert (
        sb.where("web", conf)
        == f"port 9333\nprofile {tmp_path}/seat-browser-credential-profile-web"
    )


def test_main_prints_a_fixed_reason_and_never_an_exceptions_text(mods, capsys, monkeypatch):
    _, sb = mods

    def boom(*args, **kwargs):
        raise RuntimeError(f"cookie {VALUE}")

    monkeypatch.setattr(sb, "place", boom)
    assert sb.main(["--account", ACCOUNT]) == 3
    out = capsys.readouterr()
    assert VALUE not in out.out + out.err and "RuntimeError" in out.err


# --- the hook in seat_session.py --------------------------------------------------------------


def test_a_seat_with_no_seat_browser_gets_nothing_more(mods, capsys, monkeypatch):
    ss, sb = mods
    monkeypatch.setattr(sb, "this_seat", lambda: "cio")
    monkeypatch.setattr(sb, "place", lambda *a, **k: pytest.fail("must not place"))
    assert ss.place_in_seat_browser(ACCOUNT) == 0
    out = capsys.readouterr()
    assert out.out == "" and out.err == ""


def test_a_seat_with_a_seat_browser_gets_the_second_line(mods, capsys, monkeypatch):
    ss, sb = mods
    monkeypatch.setattr(sb, "this_seat", lambda: "web")
    monkeypatch.setattr(
        sb, "place", lambda account: f"{account} placed in seat browser web, expires X"
    )
    assert ss.place_in_seat_browser(ACCOUNT) == 0
    assert capsys.readouterr().out.strip() == f"{ACCOUNT} placed in seat browser web, expires X"


def test_a_failed_placement_exits_4_with_a_fixed_reason(mods, capsys, monkeypatch):
    ss, sb = mods
    monkeypatch.setattr(sb, "this_seat", lambda: "web")

    def refuse(account):
        raise sb.Refused("the seat browser is not answering on its port")

    monkeypatch.setattr(sb, "place", refuse)
    assert ss.place_in_seat_browser(ACCOUNT) == 4
    assert "session saved, not placed" in capsys.readouterr().err

    def boom(account):
        raise ValueError(VALUE)

    monkeypatch.setattr(sb, "place", boom)
    assert ss.place_in_seat_browser(ACCOUNT) == 4
    err = capsys.readouterr().err
    assert VALUE not in err and "ValueError" in err


# --- the DevTools client against a real socket -------------------------------------------------


def _frame(payload: bytes, opcode=0x1, fin=True) -> bytes:
    head = bytes([(0x80 if fin else 0) | opcode])
    if len(payload) < 126:
        return head + bytes([len(payload)]) + payload
    return head + bytes([126]) + struct.pack("!H", len(payload)) + payload


def _serve(server, seen):
    conn, _ = server.accept()
    with conn:
        head = b""
        while b"\r\n\r\n" not in head:
            head += conn.recv(1024)
        key = [
            l.split(b": ")[1] for l in head.split(b"\r\n") if l.startswith(b"Sec-WebSocket-Key")
        ][0]
        accept = base64.b64encode(
            hashlib.sha1(key + b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11").digest()
        )
        conn.sendall(
            b"HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
            b"Sec-WebSocket-Accept: " + accept + b"\r\n\r\n"
        )
        seen["headers"] = head.decode()
        for _ in range(2):
            while True:  # the client's pong to our ping arrives first on the second round
                first, second = conn.recv(2)
                size = second & 0x7F
                if size == 126:
                    (size,) = struct.unpack("!H", conn.recv(2))
                mask = conn.recv(4)
                data = b""
                while len(data) < size:
                    data += conn.recv(size - len(data))
                if first & 0x0F == 0xA:
                    seen["pongs"] = seen.get("pongs", 0) + 1
                    continue
                break
            message = json.loads(bytes(b ^ mask[i % 4] for i, b in enumerate(data)))
            seen.setdefault("masked", []).append(bool(second & 0x80))
            seen.setdefault("methods", []).append(message["method"])
            conn.sendall(_frame(b'{"method": "Some.event"}'))  # an event first: skipped
            conn.sendall(_frame(b"", opcode=0x9))  # a ping: answered, not returned
            reply = json.dumps({"id": message["id"], "result": {"echo": "x" * 300}}).encode()
            conn.sendall(_frame(reply[:100], fin=False) + _frame(reply[100:], opcode=0x0))


def test_the_devtools_client_speaks_websocket_on_loopback(mods):
    _, sb = mods
    server = socket.socket()
    server.bind(("127.0.0.1", 0))
    server.listen(1)
    port = server.getsockname()[1]
    seen = {}
    thread = threading.Thread(target=_serve, args=(server, seen), daemon=True)
    thread.start()
    client = sb.DevTools(port, "/devtools/browser/abc")
    first = client.call("Storage.setCookies", {"cookies": []})
    second = client.call("Storage.getCookies", {})
    client.close()
    thread.join(timeout=5)
    server.close()
    assert first["id"] == 1 and second["id"] == 2 and len(second["result"]["echo"]) == 300
    assert seen["methods"] == ["Storage.setCookies", "Storage.getCookies"]
    assert seen["masked"] == [True, True]  # a client must mask its frames
    assert seen["pongs"] == 1  # the first ping was answered before the second call
    assert f"Host: 127.0.0.1:{port}" in seen["headers"] and "Origin" not in seen["headers"]


# --- the browser tool's launcher ---------------------------------------------------------------


def _launcher(tmp_path, seat, conf_text):
    top = tmp_path / seat
    (top / "scripts").mkdir(parents=True)
    for name in ("seat-browser-mcp.sh", "seat_browser.py", "seat_session.py", "seat_read.py"):
        (top / "scripts" / name).write_text((ROOT / "scripts" / name).read_text())
    script = top / "scripts" / "seat-browser-mcp.sh"
    (top / "scripts" / "seat-browser.conf").write_text(conf_text)
    done = subprocess.run(["bash", str(script), "--print"], capture_output=True, text=True)
    return done.returncode, done.stdout.split("\n"), done.stderr


def test_a_seat_without_a_row_starts_what_mcp_json_started_before(tmp_path):
    code, lines, err = _launcher(tmp_path, "cio", "web 9333\n")
    # The exact command .mcp.json ran before it called the launcher (switched 2026-11-20).
    before = [
        "npx",
        "chrome-devtools-mcp@1.10.1",
        "--executablePath=/Users/xian/.claude-pm/chrome-for-testing.app/Contents/MacOS/"
        "Google Chrome for Testing",
        "--isolated",
        "--viewport=1280x720",
    ]
    assert [line for line in lines if line] == before
    assert code == 0 and "--isolated" in lines and err == ""
    assert not any(line.startswith("--browserUrl") for line in lines)


def test_a_seat_whose_browser_is_down_falls_back_and_says_so(tmp_path):
    server = socket.socket()
    server.bind(("127.0.0.1", 0))
    port = server.getsockname()[1]
    server.close()  # nothing listens on this port now
    code, lines, err = _launcher(tmp_path, "web", f"web {port}\n")
    assert code == 0 and "--isolated" in lines
    assert not any(line.startswith("--browserUrl") for line in lines)
    assert "not attaching for 'web'" in err and "refused" in err


def test_the_launcher_never_attaches_to_another_browser_on_the_port(tmp_path):
    """Arch, 2026-11-16: something answers /json/version on the seat's port like a browser
    would, but it is not the seat's own browser. The tool must get the throwaway."""
    import http.server

    class Answers(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            body = b'{"webSocketDebuggerUrl": "ws://127.0.0.1:1/devtools/browser/abc"}'
            self.send_response(200)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = http.server.HTTPServer(("127.0.0.1", 0), Answers)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        code, lines, err = _launcher(tmp_path, "web", f"web {server.server_address[1]}\n")
    finally:
        server.shutdown()
        server.server_close()
    assert code == 0 and "--isolated" in lines
    assert not any(line.startswith("--browserUrl") for line in lines)
    assert "not attaching for 'web'" in err and "refused" in err


def test_check_makes_the_placement_proof_and_sends_nothing(mods, conf, tmp_path, monkeypatch):
    ss, sb = mods
    seen = []
    monkeypatch.setattr(sb, "browser_socket_path", lambda seat, port: seen.append((seat, port)))
    assert sb.check("web", conf) == "port 9333"
    assert seen == [("web", 9333)]
    with pytest.raises(ss.Refused, match="has no seat browser"):
        sb.check("cio", conf)

    def refuse(seat, port):
        raise ss.Refused("the browser on that port is not on this seat's profile folder")

    monkeypatch.setattr(sb, "browser_socket_path", refuse)
    with pytest.raises(ss.Refused, match="profile folder"):
        sb.check("web", conf)


def test_the_launcher_reads_the_port_from_the_helper_and_pins_the_tool():
    text = (ROOT / "scripts" / "seat-browser-mcp.sh").read_text()
    assert "seat-browser.conf" in text and "9333" not in text
    assert "chrome-devtools-mcp@1.10.1" in text
    assert 'seat_browser.py" --check "$seat"' in text
    assert "curl" not in text  # an answering port is not proof of whose browser it is
    assert "--remote-allow-origins" not in text.replace("# ", "")


@pytest.mark.parametrize(
    "helper_prints, helper_exit, attaches",
    [
        ("port 9444", 0, True),
        ("port 9444", 2, False),  # a refusal is a refusal whatever it printed
        ("port 9444 --executablePath=/bin/sh", 0, False),  # only 'port <digits>' is taken
        ("", 0, False),
    ],
)
def test_the_launcher_attaches_only_on_the_helpers_plain_yes(
    tmp_path, helper_prints, helper_exit, attaches
):
    top = tmp_path / "web"
    (top / "scripts").mkdir(parents=True)
    script = top / "scripts" / "seat-browser-mcp.sh"
    script.write_text((ROOT / "scripts" / "seat-browser-mcp.sh").read_text())
    (top / "scripts" / "seat-browser.conf").write_text("web 9333\n")
    (top / "scripts" / "seat_browser.py").write_text(
        f"import sys\nprint({helper_prints!r})\nsys.exit({helper_exit})\n"
    )
    done = subprocess.run(["bash", str(script), "--print"], capture_output=True, text=True)
    lines = done.stdout.split("\n")
    assert done.returncode == 0
    if attaches:
        assert lines[:4] == [
            "npx",
            "chrome-devtools-mcp@1.10.1",
            "--browserUrl",
            "http://127.0.0.1:9444",
        ]
        assert "--isolated" not in lines and done.stderr == ""
    else:
        assert "--isolated" in lines and not any(l.startswith("--browserUrl") for l in lines)
        assert "not attaching for 'web'" in done.stderr


def test_mcp_json_calls_the_launcher():
    """ADR-084 one-time steps, item 5 (CIO, 2026-11-20): every seat's browser tool starts
    through the launcher, which decides attach or throwaway."""
    current = json.loads((ROOT / ".mcp.json").read_text())["mcpServers"]["chrome-devtools"]
    assert current == {"command": "bash", "args": ["scripts/seat-browser-mcp.sh"]}
