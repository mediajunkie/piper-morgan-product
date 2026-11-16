#!/usr/bin/env python3
"""ADR-084 D3 (issue 2388): sign a seeded test account in to beta and save its session.

A seat holds a session, never a password. This helper reads the account's credential
file itself, signs in, checks that the account holds nothing real, and saves the
access cookie (24 hours at most) in one file under ``~/.piper-shared``. It prints the account name and
the session's expiry, and nothing else. ``scripts/seat_read.py`` reads the saved
session; no seat does.

HOST's bounds, all enforced here:
1. One fixed host and a fixed list of account names, in code. Anything else is refused.
   Adding a name, or an exception for one, is a diff HOST reads.
2. After sign-in and before saving, it refuses if the account is an admin, holds a
   provider key, or has a connection, beyond what the table below allows for that name.
   A check that cannot be read refuses too.
3. Output is the account name and the expiry. Every failure prints a fixed reason:
   never a response body, a header, or an exception's text.
4. The credential file and the saved session sit under the fleet's Read denies on
   ``~/.piper-shared`` (names matching ``*credential*`` / ``*token*``), mode 0600.
5. The grant is one exact-command allow per account name, added by xian.
6. Revocation is a password rotation plus deleting the session file.

Usage:
    scripts/seat_session.py --account web-seed-1386

Concept: docs/internal/architecture/adrs/adr-084-seat-resources-are-separate-granted-once-and-bounded.md
"""

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from http.cookies import SimpleCookie
from pathlib import Path
from typing import Callable, Dict, FrozenSet, Mapping, Optional, Tuple

HOST = "https://beta.pipermorgan.ai"
AUTH_COOKIE = "auth_token"
TIMEOUT_SECONDS = 30
MAX_SESSION_SECONDS = (
    86400  # HOST and Lead, 11-16: the expiry is capped here, whatever the host says
)


@dataclass(frozen=True)
class Account:
    """What one seeded account may hold. Empty means nothing."""

    credential_file: str  # under the shared folder; its name must match a Read deny
    integrations: FrozenSet[str] = frozenset()  # integration ids allowed to be connected
    provider_keys: FrozenSet[str] = frozenset()  # providers allowed to hold a test key
    connectors: bool = False  # may an MCP connector or manual token exist


# Bound 1. A change to this table is a diff HOST reads.
ACCOUNTS: Dict[str, Account] = {
    "web-seed-1386": Account(credential_file="web-seed-1386-credentials-2026-10-20.txt"),
}

USER_KEYS = ("username", "user", "email", "login")
PASSWORD_KEYS = ("password", "pass")


class Refused(Exception):
    """A fixed reason. Its text is safe to print: it never carries server data."""


@dataclass(frozen=True)
class Reply:
    status: int
    body: bytes
    set_cookies: Tuple[str, ...] = ()


Transport = Callable[[str, str, Optional[bytes], Mapping[str, str]], Reply]


def shared_dir() -> Path:
    """Fixed. No environment value moves where credentials are read from (HOST, 11-16)."""
    return Path.home() / ".piper-shared"


def session_path(account: str) -> Path:
    return shared_dir() / f"{account}.session-token.json"


def http_transport(
    method: str, path: str, data: Optional[bytes], headers: Mapping[str, str]
) -> Reply:
    """One request to the fixed host. Redirects are not followed, so a cookie is never
    sent to another host."""

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs):  # noqa: D401
            return None

    opener = urllib.request.build_opener(NoRedirect)
    request = urllib.request.Request(HOST + path, data=data, method=method, headers=dict(headers))
    try:
        with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
            return Reply(
                response.status,
                response.read(),
                tuple(response.headers.get_all("Set-Cookie") or ()),
            )
    except urllib.error.HTTPError as error:
        return Reply(error.code, b"", ())


def read_credentials(path: Path) -> Tuple[str, str]:
    """The sign-in name and password from a ``key: value`` (or ``key=value``) file.
    Refuses a file that others can read."""
    try:
        mode = stat.S_IMODE(path.stat().st_mode)
        text = path.read_text(encoding="utf-8")
    except OSError:
        raise Refused("credential file not readable") from None
    if mode & 0o077:
        raise Refused("credential file is not mode 0600")
    found: Dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        positions = [line.index(sep) for sep in (":", "=") if sep in line]
        if positions:  # split on whichever separator comes first (Lead, 11-16)
            at = min(positions)
            found.setdefault(line[:at].strip().lower(), line[at + 1 :].strip().strip("'\""))
    user = next((found[k] for k in USER_KEYS if found.get(k)), "")
    password = next((found[k] for k in PASSWORD_KEYS if found.get(k)), "")
    # Lead's point (11-16): say which expected name is missing, and nothing from the file.
    if not user:
        raise Refused(
            "credential file has no sign-in name key; expected one of " + ", ".join(USER_KEYS)
        )
    if not password:
        raise Refused(
            "credential file has no password key; expected one of " + ", ".join(PASSWORD_KEYS)
        )
    return user, password


def _cookies_from(reply: Reply) -> Dict[str, Tuple[str, Optional[int]]]:
    """name -> (value, max-age) for the access cookie in a reply. The refresh cookie
    is dropped here: nothing a seat does needs a 7-day credential (Lead, 11-16)."""
    out: Dict[str, Tuple[str, Optional[int]]] = {}
    for header in reply.set_cookies:
        jar = SimpleCookie()
        try:
            jar.load(header)
        except Exception:
            continue
        for name, morsel in jar.items():
            if name == AUTH_COOKIE and morsel.value:  # the 7-day refresh cookie is never kept
                age = morsel["max-age"]
                out[name] = (morsel.value, int(age) if str(age).isdigit() else None)
    return out


def _json(reply: Reply):
    try:
        return json.loads(reply.body.decode("utf-8"))
    except Exception:
        raise Refused("a check returned something unreadable") from None


def sign_in(
    account: str, user: str, password: str, send: Transport
) -> Dict[str, Tuple[str, Optional[int]]]:
    form = urllib.parse.urlencode({"username": user, "password": password}).encode()
    reply = send(
        "POST", "/api/v1/auth/login", form, {"Content-Type": "application/x-www-form-urlencoded"}
    )
    if reply.status in (401, 403):
        raise Refused("sign-in was refused by the host")
    if reply.status != 200:
        raise Refused("sign-in did not return 200")
    cookies = _cookies_from(reply)
    if AUTH_COOKIE not in cookies:
        raise Refused("sign-in returned no session cookie")
    return cookies


def check_holds_nothing_real(
    account: str, cookies: Mapping[str, Tuple[str, Optional[int]]], send: Transport
) -> None:
    """Bound 2. Every read must succeed and show nothing beyond the account's row."""
    allowed = ACCOUNTS[account]
    header = {"Cookie": "; ".join(f"{name}={value}" for name, (value, _) in cookies.items())}

    def get(path: str) -> Reply:
        return send("GET", path, None, header)

    me = get("/api/v1/auth/me")
    if me.status != 200 or _json(me).get("username") != account:
        raise Refused("the session is not the named account")

    admin = get("/api/v1/admin/account-flags?" + urllib.parse.urlencode({"username": account}))
    if admin.status == 200:
        raise Refused("the account is an admin")
    if admin.status != 403:
        raise Refused("the admin check could not be read")

    keys = get("/api/v1/keys/list?active_only=false")  # a deactivated key row counts too
    if keys.status != 200:
        raise Refused("the provider-key check could not be read")
    listed = _json(keys)
    if not isinstance(listed, list):
        raise Refused("the provider-key check could not be read")
    for row in listed:
        provider = row.get("provider") if isinstance(row, dict) else None
        if provider not in allowed.provider_keys:
            raise Refused("the account holds a provider key")

    health = get("/api/v1/integrations/health")
    if health.status != 200:
        raise Refused("the connection check could not be read")
    integrations = _json(health).get("integrations")
    if not isinstance(integrations, list):
        raise Refused("the connection check could not be read")
    for row in integrations:
        name = row.get("name") if isinstance(row, dict) else None
        state = row.get("status") if isinstance(row, dict) else None
        if not name or not state:
            raise Refused("the connection check could not be read")
        if state == "unknown":  # the host could not run its own check
            raise Refused("the connection check could not be read")
        if state != "not_configured" and name not in allowed.integrations:
            raise Refused("the account has a connection")

    connectors = get("/api/v1/settings/mcp-connections")
    if connectors.status != 200:
        raise Refused("the connector check could not be read")
    body = _json(connectors)
    oauth, manual = body.get("oauth_connections"), body.get("manual_tokens")
    if not isinstance(oauth, list) or not isinstance(manual, list):
        raise Refused("the connector check could not be read")
    if (oauth or manual) and not allowed.connectors:
        raise Refused("the account has a connector")


def save_session(account: str, cookies: Mapping[str, Tuple[str, Optional[int]]], now: float) -> int:
    """Write the session as a browser storage state, mode 0600, atomically.
    Returns the access cookie's expiry (epoch seconds)."""
    domain = urllib.parse.urlparse(HOST).hostname
    rows = []
    for name, (value, max_age) in cookies.items():
        rows.append(
            {
                "name": name,
                "value": value,
                "domain": domain,
                "path": "/",
                "expires": int(
                    now
                    + min(
                        max_age if max_age is not None else MAX_SESSION_SECONDS, MAX_SESSION_SECONDS
                    )
                ),
                "httpOnly": True,
                "secure": True,
                "sameSite": "Lax",
            }
        )
    expires = next(r["expires"] for r in rows if r["name"] == AUTH_COOKIE)
    state = {"account": account, "host": HOST, "saved_at": int(now), "cookies": rows, "origins": []}
    target = session_path(account)
    try:
        target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        fd, temp = tempfile.mkstemp(dir=str(target.parent), prefix=".session-token-")
        try:
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(state, handle)
            os.replace(temp, target)
        except BaseException:
            try:
                os.unlink(temp)
            except OSError:
                pass
            raise
    except OSError:
        raise Refused("the session file could not be written") from None
    return expires


def run(account: str, send: Transport = http_transport, now: Optional[float] = None) -> str:
    if account not in ACCOUNTS:
        raise Refused("that account is not on the list")
    user, password = read_credentials(shared_dir() / ACCOUNTS[account].credential_file)
    cookies = sign_in(account, user, password, send)
    check_holds_nothing_real(account, cookies, send)
    expires = save_session(account, cookies, time.time() if now is None else now)
    stamp = datetime.fromtimestamp(expires, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"{account} session saved, expires {stamp}"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Sign a seeded test account in to beta and save its session."
    )
    parser.add_argument("--account", required=True)
    args = parser.parse_args(argv)
    try:
        print(run(args.account))
        return 0
    except Refused as refusal:
        print(f"seat_session: refused: {refusal}", file=sys.stderr)
        return 2
    except Exception as error:  # never print an exception's own text: it may carry a URL or a body
        print(f"seat_session: refused: unexpected {type(error).__name__}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
