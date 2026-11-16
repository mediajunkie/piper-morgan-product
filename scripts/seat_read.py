#!/usr/bin/env python3
"""ADR-084 D3 (issue 2388): one GET on beta as a seeded test account, from its saved session.

The session is saved by ``scripts/seat_session.py``. This script reads it so that no
seat has to. It prints the response body and nothing else.

Bounds:
- The host is ``seat_session.HOST``; the account must be on ``seat_session.ACCOUNTS``.
- GET only, and only a path on the closed list below, matched on the parsed path with
  its query split off. Adding a path is a diff HOST reads. The sign-in routes, the key
  list and the connector list are never on it.
- Redirects are not followed, so the cookies never go to another host.
- If the body contains either cookie's value, nothing is printed.
- A failure prints a fixed reason and the status code, never a header.

Usage:
    scripts/seat_read.py --account web-seed-1386 '/api/v1/admin/floored-actions?days=30'

Concept: docs/internal/operations/adr-084-one-time-steps.md
"""

from __future__ import annotations

import argparse
import json
import re
import stat
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Dict, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

import seat_session  # noqa: E402
from seat_session import Refused, Transport  # noqa: E402

# The closed list (HOST and Lead, 11-16). The ops_reader routes of issue 2390 join it as they land.
ALLOWED_PATHS = frozenset({"/api/v1/admin/floored-actions"})
QUERY_OK = re.compile(r"^[A-Za-z0-9_=&.-]*$")


def checked_path(path: str) -> str:
    """The path as it will be sent, or a refusal. Nothing is normalised: a form that
    would need normalising is refused."""
    if not path.startswith("/") or "%" in path or "//" in path or ".." in path or "#" in path:
        raise Refused("the path is not in a plain form")
    parts = urllib.parse.urlsplit(path)
    if parts.scheme or parts.netloc or parts.fragment or not QUERY_OK.match(parts.query):
        raise Refused("the path is not in a plain form")
    if parts.path not in ALLOWED_PATHS:
        raise Refused("that path is not on the list this script reads")
    return parts.path + ("?" + parts.query if parts.query else "")


def load_cookies(account: str, now: Optional[float] = None) -> Dict[str, str]:
    path = seat_session.session_path(account)
    try:
        mode = stat.S_IMODE(path.stat().st_mode)
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise Refused("no saved session; run seat_session.py for this account") from None
    if mode & 0o077:
        raise Refused("the session file is not mode 0600")
    if state.get("account") != account or state.get("host") != seat_session.HOST:
        raise Refused("the session file is for another account or host")
    current = time.time() if now is None else now
    cookies = {
        row["name"]: row["value"]
        for row in state.get("cookies", [])
        if row.get("expires", 0) > current
    }
    if seat_session.AUTH_COOKIE not in cookies:
        raise Refused("the saved session has expired; run seat_session.py again")
    return cookies


def read(
    account: str,
    path: str,
    send: Transport = seat_session.http_transport,
    now: Optional[float] = None,
) -> str:
    if account not in seat_session.ACCOUNTS:
        raise Refused("that account is not on the list")
    path = checked_path(path)
    cookies = load_cookies(account, now)
    header = {"Cookie": "; ".join(f"{name}={value}" for name, value in cookies.items())}
    reply = send("GET", path, None, header)
    if reply.status != 200:
        raise Refused(f"the host answered {reply.status}")
    body = reply.body.decode("utf-8", errors="replace")
    if any(value and value in body for value in cookies.values()):
        raise Refused("the reply contains a session value; not printed")
    return body


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="One GET on beta as a seeded test account.")
    parser.add_argument("--account", required=True)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    try:
        print(read(args.account, args.path))
        return 0
    except Refused as refusal:
        print(f"seat_read: refused: {refusal}", file=sys.stderr)
        return 2
    except Exception as error:  # never print an exception's own text
        print(f"seat_read: refused: unexpected {type(error).__name__}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
