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

A second mode, ``--redirect-uri github|calendar`` (issue 2282 step 5; HOST's four
conditions and Exec's yes, 2026-11-16), reads where a connector's sign-in would send the
browser back to, so nobody has to start a sign-in in a browser to see it:
- One GET to that connector's connect-start route, a second closed list by exact path.
  These routes are NOT on the list above, so their reply body can never be printed.
- The route answers with JSON that holds the provider's sign-in address and a state
  value. The state is a bearer for that sign-in attempt. This script prints one line:
  the host and path of the ``redirect_uri`` inside that address. The query string, the
  state and the body are never printed, stored or logged, and a line that contains the
  state or a cookie value is refused.
- No redirect is followed and nothing is sent to the provider.
- One request per run. Each request leaves one unused state in the app's memory. It is
  refused after 15 minutes (``STATE_EXPIRATION = 900`` in both handlers) and is dropped
  when the app restarts; nothing sweeps it sooner, so don't run this in a loop.
- The account needs no connected integration: ``web-seed-1386`` runs it.

Usage:
    scripts/seat_read.py --account web-seed-1386 '/api/v1/admin/floored-actions?days=30'
    scripts/seat_read.py --account web-seed-1386 --redirect-uri github

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

# The connect-start routes ``--redirect-uri`` may call (HOST, 2026-11-16). Kept apart
# from ALLOWED_PATHS on purpose: ``read`` prints a body, and these bodies hold a state.
REDIRECT_URI_ROUTES = {
    "github": "/api/v1/settings/integrations/github/connect",
    "calendar": "/api/v1/settings/integrations/calendar/connect",
}
HOST_OK = re.compile(r"^[A-Za-z0-9.-]+(:[0-9]{1,5})?$")
PATH_OK = re.compile(r"^/[A-Za-z0-9/_.-]*$")


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


def host_and_path(address: object) -> str:
    """``host/path`` of an http(s) address, or a refusal. The query and fragment are
    dropped, never shown."""
    if not isinstance(address, str):
        raise Refused("the reply was not in the expected form")
    parts = urllib.parse.urlsplit(address)
    if (
        parts.scheme not in ("http", "https")
        or not HOST_OK.match(parts.netloc)
        or not PATH_OK.match(parts.path or "/")
    ):
        raise Refused("the address in the reply is not in a plain form")
    return parts.netloc + (parts.path or "/")


def read_redirect_uri(
    account: str,
    connector: str,
    send: Optional[Transport] = None,
    now: Optional[float] = None,
) -> str:
    """One line: where ``connector``'s sign-in would return to (host and path only)."""
    send = send or seat_session.http_transport  # resolved at call time
    if account not in seat_session.ACCOUNTS:
        raise Refused("that account is not on the list")
    route = REDIRECT_URI_ROUTES.get(connector)
    if route is None:
        raise Refused("that connector is not on the list this script reads")
    cookies = load_cookies(account, now)
    header = {"Cookie": "; ".join(f"{name}={value}" for name, value in cookies.items())}
    reply = send("GET", route, None, header)
    if reply.status != 200:
        raise Refused(f"the host answered {reply.status}")
    try:
        payload = json.loads(reply.body.decode("utf-8"))
    except ValueError:
        raise Refused("the reply was not in the expected form") from None
    if not isinstance(payload, dict):
        raise Refused("the reply was not in the expected form")
    if payload.get("switch_host_url"):
        # #2281 (b): the app asks the browser to start the sign-in on another host.
        line = f"{connector}: start on {host_and_path(payload['switch_host_url'])}"
    else:
        address = payload.get("auth_url")
        if not isinstance(address, str):
            raise Refused("the reply was not in the expected form")
        values = urllib.parse.parse_qs(urllib.parse.urlsplit(address).query).get("redirect_uri")
        if not values or len(values) != 1:
            raise Refused("the sign-in address does not carry exactly one redirect_uri")
        line = f"{connector} redirect_uri: {host_and_path(values[0])}"
    state = payload.get("state")
    secrets_seen = [v for v in cookies.values() if v] + ([state] if isinstance(state, str) else [])
    if any(secret and secret in line for secret in secrets_seen):
        raise Refused("the line would contain a session or state value; not printed")
    return line


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="One GET on beta as a seeded test account.")
    parser.add_argument("--account", required=True)
    parser.add_argument("path", nargs="?")
    parser.add_argument(
        "--redirect-uri",
        choices=sorted(REDIRECT_URI_ROUTES),
        help="print where that connector's sign-in returns to (host and path only)",
    )
    args = parser.parse_args(argv)
    try:
        if bool(args.path) == bool(args.redirect_uri):
            raise Refused("give a path or --redirect-uri, one of them")
        if args.redirect_uri:
            print(read_redirect_uri(args.account, args.redirect_uri))
        else:
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
