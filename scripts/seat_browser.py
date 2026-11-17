#!/usr/bin/env python3
"""ADR-084 D3 browser half (issue 2400): put a seeded account's saved session into a seat's
own browser, through that browser's debug port.

A seat's browser tool has no call that sets a cookie, and a seat never types one. So this
script reads the session that ``scripts/seat_session.py`` saved and places its access
cookie into the seat browser with the DevTools protocol. The cookie's value goes from the
session file to the browser over a loopback socket. It is never printed, logged or passed
through a tool call. ``seat_session.py`` calls this after it saves a session, when the seat
it runs in has a row in ``scripts/seat-browser.conf``; no grant beyond that helper's own
exact-command allow is needed.

Bounds (D3; HOST reads a change to any of them):
- The account must be on ``seat_session.ACCOUNTS``. The seat must have a row in
  ``scripts/seat-browser.conf``, the one place a seat browser's port is written.
- The browser is spoken to on 127.0.0.1 only, with no proxy.
- It must be the seat browser and nothing else. The profile folder is
  ``~/.piper-shared/seat-browser-credential-profile-<seat>``, mode 0700. Before any
  cookie is sent, the process listening on the port is read (``lsof``, then ``ps``): it
  must be one process, bound to 127.0.0.1 only, the cohort's test browser binary, started
  with ``--user-data-dir`` on that folder and ``--use-mock-keychain`` (so it never asks
  the login keychain for a key), and without ``--remote-allow-origins``. A browser on
  another profile, xian's own Chrome included, is refused.
- Output is one line: the account, the seat and the expiry. Every failure prints a fixed
  reason, never a reply, a header or an exception's text.
- Revocation is deleting the profile folder (and the session file).

Usage:
    scripts/seat_browser.py --account web-seed-1386     # place, for the seat this runs in
    scripts/seat_browser.py --where web                  # print that seat's port and folder
    scripts/seat_browser.py --check web                  # is that seat's own browser up (no cookie sent)

Concept: docs/internal/operations/adr-084-one-time-steps.md
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import socket
import stat
import struct
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

import seat_read  # noqa: E402
import seat_session  # noqa: E402
from seat_session import Refused  # noqa: E402

CONF = Path(__file__).resolve().parent / "seat-browser.conf"
LOOPBACK = "127.0.0.1"
TIMEOUT_SECONDS = 10
MAX_FRAME = 8 * 1024 * 1024
# The cohort's test browser (the same binary .mcp.json names). Never xian's own Chrome.
BROWSER_BINARY = (
    "/Users/xian/.claude-pm/chrome-for-testing.app/Contents/MacOS/Google Chrome for Testing"
)

Call = Callable[[str, dict], dict]  # one DevTools method call: (method, params) -> reply


def seats(conf: Optional[Path] = None) -> Dict[str, int]:
    """seat name -> port, from the one conf file. A row that can't be read refuses."""
    try:
        text = (conf or CONF).read_text(encoding="utf-8")
    except OSError:
        raise Refused("the seat browser list could not be read") from None
    out: Dict[str, int] = {}
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 2 or not parts[1].isdigit() or not 1024 <= int(parts[1]) <= 65535:
            raise Refused("the seat browser list has a row that is not 'seat port'")
        if parts[0] in out or int(parts[1]) in out.values():
            raise Refused("the seat browser list names a seat or a port twice")
        out[parts[0]] = int(parts[1])
    return out


def this_seat() -> str:
    """The seat this checkout belongs to: the worktree folder's name."""
    return Path(__file__).resolve().parent.parent.name


def profile_dir(seat: str) -> Path:
    """Fixed, under the shared folder, with a name the fleet's Read denies match."""
    return seat_session.shared_dir() / f"seat-browser-credential-profile-{seat}"


def _get_json(port: int, path: str):
    """One GET to the browser's own HTTP endpoint on loopback. No proxy is used."""
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(f"http://{LOOPBACK}:{port}{path}", timeout=TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def _listener(port: int) -> List[str]:
    """What listens on ``port``: lsof's field lines (``p<pid>``, ``n<address>``)."""
    done = subprocess.run(
        ["/usr/sbin/lsof", "-nP", f"-iTCP:{port}", "-sTCP:LISTEN", "-Fpn"],
        capture_output=True,
        text=True,
        timeout=TIMEOUT_SECONDS,
        check=False,
    )
    return done.stdout.split()


def _command_line(pid: str) -> str:
    done = subprocess.run(
        ["/bin/ps", "-ww", "-o", "command=", "-p", pid],
        capture_output=True,
        text=True,
        timeout=TIMEOUT_SECONDS,
        check=False,
    )
    return done.stdout.strip()


def browser_socket_path(
    seat: str, port: int, get_json=_get_json, listener=_listener, command_line=_command_line
) -> str:
    """The browser's DevTools path, after proving that what listens on ``port`` is this
    seat's browser: one process, bound to 127.0.0.1 only, the cohort's test browser, started
    on this seat's profile folder, with the fake keychain and no wildcard origins."""
    folder = profile_dir(seat)
    try:
        mode = stat.S_IMODE(folder.stat().st_mode)
    except OSError:
        raise Refused("the seat browser's profile folder does not exist") from None
    if mode & 0o077:
        raise Refused("the seat browser's profile folder is not mode 0700")
    try:
        fields = listener(port)
        pids = sorted({f[1:] for f in fields if f.startswith("p")})
        addresses = {f[1:] for f in fields if f.startswith("n")}
        command = command_line(pids[0]) if len(pids) == 1 and pids[0].isdigit() else ""
    except (OSError, subprocess.SubprocessError):
        raise Refused("the seat browser's process could not be read") from None
    if not pids:
        raise Refused("the seat browser is not answering on its port")
    if len(pids) != 1 or addresses != {f"{LOOPBACK}:{port}"}:
        raise Refused("the port is not held by one browser on 127.0.0.1 only")
    words = (
        command[len(BROWSER_BINARY) :].split() if command.startswith(BROWSER_BINARY + " ") else None
    )
    if words is None:
        raise Refused("the browser on that port is not the cohort's test browser")
    if f"--user-data-dir={folder}" not in words:
        raise Refused("the browser on that port is not on this seat's profile folder")
    if "--use-mock-keychain" not in words:
        raise Refused("the seat browser was started without --use-mock-keychain")
    if any(word.startswith("--remote-allow-origins") for word in words):
        raise Refused("the seat browser was started with --remote-allow-origins")
    try:
        answered = get_json(port, "/json/version").get("webSocketDebuggerUrl")
    except Exception:
        raise Refused("the seat browser is not answering on its port") from None
    prefix = f"ws://{LOOPBACK}:{port}/devtools/browser/"
    if not isinstance(answered, str) or not answered.startswith(prefix):
        raise Refused("the seat browser's reply was not in the expected form")
    if not all(ch.isalnum() or ch == "-" for ch in answered[len(prefix) :]):
        raise Refused("the seat browser's reply was not in the expected form")
    return answered[len(f"ws://{LOOPBACK}:{port}") :]


class DevTools:
    """A minimal WebSocket client for one browser on loopback (RFC 6455, text frames)."""

    def __init__(self, port: int, path: str):
        self._next = 0
        self._sock = socket.create_connection((LOOPBACK, port), timeout=TIMEOUT_SECONDS)
        key = base64.b64encode(os.urandom(16)).decode("ascii")
        self._sock.sendall(
            (
                f"GET {path} HTTP/1.1\r\nHost: {LOOPBACK}:{port}\r\nUpgrade: websocket\r\n"
                f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\n"
                "Sec-WebSocket-Version: 13\r\n\r\n"
            ).encode("ascii")
        )
        head = b""
        while b"\r\n\r\n" not in head:
            chunk = self._sock.recv(1)
            if not chunk or len(head) > 8192:
                raise OSError("no upgrade")
            head += chunk
        if not head.startswith(b"HTTP/1.1 101"):
            raise OSError("no upgrade")

    def _exact(self, count: int) -> bytes:
        data = b""
        while len(data) < count:
            chunk = self._sock.recv(count - len(data))
            if not chunk:
                raise OSError("closed")
            data += chunk
        return data

    def _send(self, opcode: int, payload: bytes) -> None:
        mask = os.urandom(4)
        size = len(payload)
        if size < 126:
            head = struct.pack("!BB", 0x80 | opcode, 0x80 | size)
        elif size < 65536:
            head = struct.pack("!BBH", 0x80 | opcode, 0x80 | 126, size)
        else:
            head = struct.pack("!BBQ", 0x80 | opcode, 0x80 | 127, size)
        masked = bytes(byte ^ mask[i % 4] for i, byte in enumerate(payload))
        self._sock.sendall(head + mask + masked)

    def _message(self) -> bytes:
        whole = b""
        while True:
            first, second = self._exact(2)
            opcode, size = first & 0x0F, second & 0x7F
            if size == 126:
                (size,) = struct.unpack("!H", self._exact(2))
            elif size == 127:
                (size,) = struct.unpack("!Q", self._exact(8))
            if size > MAX_FRAME or second & 0x80:  # too big, or a masked server frame
                raise OSError("bad frame")
            payload = self._exact(size)
            if opcode == 0x8:
                raise OSError("closed")
            if opcode == 0x9:
                self._send(0xA, payload)
                continue
            if opcode == 0xA:
                continue
            whole += payload
            if first & 0x80:
                return whole

    def call(self, method: str, params: dict) -> dict:
        self._next += 1
        wanted = self._next
        self._send(0x1, json.dumps({"id": wanted, "method": method, "params": params}).encode())
        while True:  # events and other replies are skipped
            message = json.loads(self._message().decode("utf-8"))
            if isinstance(message, dict) and message.get("id") == wanted:
                return message

    def close(self) -> None:
        try:
            self._sock.close()
        except OSError:
            pass


def _session_rows(account: str, now: Optional[float]) -> List[dict]:
    """The unexpired cookie rows of the saved session. ``seat_read.load_cookies`` makes the
    checks (mode 0600, this account, this host, not expired) and refuses otherwise."""
    live = seat_read.load_cookies(account, now)
    try:
        state = json.loads(seat_session.session_path(account).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise Refused("no saved session; run seat_session.py for this account") from None
    return [
        row
        for row in state.get("cookies", [])
        if row.get("name") in live and row.get("value") == live[row["name"]]
    ]


def place(
    account: str,
    seat: Optional[str] = None,
    now: Optional[float] = None,
    connect: Optional[Callable[[str, int], Call]] = None,
    conf: Optional[Path] = None,
) -> str:
    """Place ``account``'s saved access cookie into ``seat``'s browser. One line back."""
    if account not in seat_session.ACCOUNTS:
        raise Refused("that account is not on the list")
    seat = seat or this_seat()
    port = seats(conf).get(seat)
    if port is None:
        raise Refused("this seat has no seat browser")
    rows = _session_rows(account, now)
    domain = urllib.parse.urlparse(seat_session.HOST).hostname
    wanted = [row for row in rows if row.get("name") == seat_session.AUTH_COOKIE]
    if len(wanted) != 1 or wanted[0].get("domain") != domain:
        raise Refused("the saved session is not in the expected form")
    row = wanted[0]
    cookie = {
        "name": row["name"],
        "value": row["value"],
        "domain": domain,
        "path": "/",
        "expires": int(row["expires"]),
        "httpOnly": True,
        "secure": True,
        "sameSite": "Lax",
    }
    client: Optional[DevTools] = None
    try:
        if connect is not None:
            call = connect(seat, port)
        else:
            path = browser_socket_path(seat, port)
            try:
                client = DevTools(port, path)
            except OSError:
                raise Refused("the seat browser is not answering on its port") from None
            call = client.call
        try:
            if call("Storage.setCookies", {"cookies": [cookie]}).get("error"):
                raise Refused("the seat browser did not take the session")
            held = call("Storage.getCookies", {}).get("result", {}).get("cookies", [])
        except (OSError, ValueError):
            raise Refused("the seat browser stopped answering") from None
    finally:
        if client is not None:
            client.close()
    ours = [
        c
        for c in held
        if isinstance(c, dict)
        and c.get("name") == cookie["name"]
        and str(c.get("domain", "")).lstrip(".") == domain
    ]
    if (
        len(ours) != 1
        or ours[0].get("value") != cookie["value"]
        or ours[0].get("httpOnly") is not True
        or ours[0].get("secure") is not True
    ):
        raise Refused("the seat browser does not hold the session as placed")
    stamp = datetime.fromtimestamp(cookie["expires"], tz=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    return f"{account} placed in seat browser {seat}, expires {stamp}"


def where(seat: str, conf: Optional[Path] = None) -> str:
    """Two lines for the LaunchAgent's wrapper: the port and the profile folder."""
    port = seats(conf).get(seat)
    if port is None:
        raise Refused("that seat has no seat browser")
    return f"port {port}\nprofile {profile_dir(seat)}"


def check(seat: str, conf: Optional[Path] = None) -> str:
    """The same proof ``place`` makes before it sends a cookie, with nothing sent. The
    browser tool's launcher asks this before it attaches (Arch, 2026-11-16: the bound
    "a dedicated seat browser, never xian's own Chrome" has to hold at the attach too).
    Returns the port; refuses with the fixed reason otherwise."""
    port = seats(conf).get(seat)
    if port is None:
        raise Refused("that seat has no seat browser")
    browser_socket_path(seat, port)
    return f"port {port}"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Place a saved seat session in a seat browser.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--account", help="place this account's saved session")
    group.add_argument("--where", metavar="SEAT", help="print that seat's port and folder")
    group.add_argument("--check", metavar="SEAT", help="is that seat's own browser on its port")
    args = parser.parse_args(argv)
    try:
        if args.check:
            print(check(args.check))
        else:
            print(where(args.where) if args.where else place(args.account, now=time.time()))
        return 0
    except Refused as refusal:
        print(f"seat_browser: refused: {refusal}", file=sys.stderr)
        return 2
    except Exception as error:  # never print an exception's own text
        print(f"seat_browser: refused: unexpected {type(error).__name__}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
