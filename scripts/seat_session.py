#!/usr/bin/env python3
"""ADR-084 D3 (issue 2388): sign a seeded test account in to beta and save its session.

A seat holds a session, never a password. This helper reads the account's credential
file itself, signs in, checks that the account holds nothing real, and saves the
access cookie in one file under ``~/.piper-shared``. A session lasts 30 minutes, the
access token's life (the refresh cookie is never kept), so a longer sitting re-runs the
helper. It prints the account name and the session's expiry, and nothing else. ``scripts/seat_read.py`` reads the saved
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
    scripts/seat_session.py --account web-seed-1386 --disconnect calendar
        (clears that connector through the app's own route, re-runs bound 2, saves nothing;
        its own exact allow, added by xian; see ``disconnect``)
    scripts/seat_session.py --account seat-tester-1 --save-key anthropic
        (saves the test workspace's key on that account through the app's own route, once;
        prints no value; its own exact allow, added by xian; see ``save_key``)

In a seat that has a seat browser (issue 2400) it then prints a second line,
``<account> placed in seat browser <seat>, expires <time>``; see ``place_in_seat_browser``.

Concept: docs/internal/architecture/adrs/adr-084-seat-resources-are-separate-granted-once-and-bounded.md
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import stat
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
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


IntegrationRow = Tuple[str, bool, Optional[str]]

# The one dead state of a GitHub row (Lead's read of ``_github_card``, 11-16): the grant is
# stale or revoked and nothing else serves. ``can_test`` True with the same status is a
# stored personal token that still works, which is live and refuses.
GITHUB_DEAD_ROW: IntegrationRow = ("degraded", False, "reconnect")


@dataclass(frozen=True)
class Account:
    """What one seeded account may hold. Empty means nothing."""

    credential_file: str  # under the shared folder; its name must match a Read deny
    # Integration name -> the exact rows it may show besides ``not_configured``. A row is
    # (status, can_test, action) and all three must match (HOST, 11-16: a predicate, not a
    # set of status names, because one status can be both a dead row and a live one).
    integrations: Mapping[str, FrozenSet[IntegrationRow]] = field(default_factory=dict)
    provider_keys: FrozenSet[str] = frozenset()  # providers allowed to hold a test key
    connectors: bool = False  # may an MCP connector or manual token exist


# Bound 1. A change to this table is a diff HOST reads.
ACCOUNTS: Dict[str, Account] = {
    "web-seed-1386": Account(
        credential_file="web-seed-1386-credentials-2026-10-20.txt",
        # Carried over from 10-20: its OAuth connection was revoked in the 11-12 cutover.
        # Only that dead row passes; any live GitHub state refuses (HOST 01M7JVMNWK).
        integrations={"github": frozenset({GITHUB_DEAD_ROW})},
        # Carried over from 10-20: an Anthropic key from the `piper-morgan-test` workspace,
        # by the record (unverified on the console). The bound is that workspace's $40
        # monthly limit, xian's setting; it is a seat workspace for keys stored on seat
        # accounts (ADR-084 D2; HOST 01M7JT4WFC, Arch 01M7JV4RQX). This row only stops the
        # helper refusing the account. xian answered both questions on 11-17 (decisions.log
        # 13:36 to 14:04): nothing of his uses the workspace, and seats may spend through the
        # key up to its $40 limit. So a seat may take chat turns on it within D2's terms,
        # logging its planned turns before a sitting (Exec 01M7XNQ0MJ). If the console shows
        # another workspace, this comes out.
        provider_keys=frozenset({"anthropic"}),
    ),
    # The second seat account (issue 2389; name agreed by HOST and Lead, 11-16). It holds
    # nothing until its own exceptions are added as diffs HOST reads.
    "seat-github-1": Account(credential_file="seat-github-1-credentials.txt"),
    # The third seat account (HOST 01M827TK7G and 01M828H4AT, CIO 01M82852KZ, 11-22): an
    # account shaped like a new tester's, for served rows that need nothing on file (2406's
    # row first). It may hold an Anthropic key from the `piper-morgan-test` workspace and
    # nothing else: no GitHub, no other provider, no connector. It shares that workspace's
    # $40 monthly limit with `web-seed-1386` (Arch 01M828NS6F, condition 5), so one
    # account's sitting can stop the other's.
    "seat-tester-1": Account(
        credential_file="seat-tester-1-credentials.txt",
        provider_keys=frozenset({"anthropic"}),
    ),
}

USER_KEYS = ("username", "user", "email", "login")
PASSWORD_KEYS = ("password", "pass")


class Refused(Exception):
    """A fixed reason. Its text is safe to print: it never carries server text. The one
    addition is the connection refusal's row, spelled only in words from the fixed lists
    below (``_row_words``); anything else prints as ``other``."""


# The words the health route can emit (web/api/routes/integrations.py, read 11-20 with Lead's
# list in 01M7X815YJ). A refusal names the row in these words so the owner can tell which
# connection without anyone reading beta as the account (Exec 01M7X7QX7P, 11-20). A value
# outside a list prints "other", so no server string reaches the screen.
_KNOWN_INTEGRATIONS = frozenset({"github", "slack", "calendar", "notion"})
_KNOWN_STATUSES = frozenset(
    {"not_configured", "degraded", "connected", "healthy", "failed", "unhealthy", "unknown"}
)
_KNOWN_ACTIONS = frozenset({"reconnect", "test_only"})


def _row_words(name: object, shown: Tuple[object, object, object]) -> str:
    """``github: degraded/True/reconnect``, from fixed words only."""
    status, can_test, action = shown

    def pick(value: object, known: FrozenSet[str]) -> str:
        return value if isinstance(value, str) and value in known else "other"

    test_word = "True" if can_test is True else "False" if can_test is False else "missing"
    action_word = "none" if action is None else pick(action, _KNOWN_ACTIONS)
    return (
        f"{pick(name, _KNOWN_INTEGRATIONS)}: {pick(status, _KNOWN_STATUSES)}/{test_word}/"
        f"{action_word}"
    )


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
        if state == "not_configured":
            continue
        shown = (state, row.get("can_test"), row.get("action"))
        permitted = allowed.integrations.get(name, frozenset())
        # ``is`` on can_test: a missing or non-boolean value never matches False.
        if not any(
            shown[0] == status and shown[1] is can_test and shown[2] == action
            for status, can_test, action in permitted
        ):
            raise Refused(f"the account has a connection ({_row_words(name, shown)})")

    connectors = get("/api/v1/settings/mcp-connections")
    if connectors.status != 200:
        raise Refused("the connector check could not be read")
    body = _json(connectors)
    oauth, manual = body.get("oauth_connections"), body.get("manual_tokens")
    if not isinstance(oauth, list) or not isinstance(manual, list):
        raise Refused("the connector check could not be read")
    if (oauth or manual) and not allowed.connectors:
        raise Refused("the account has a connector")


def token_expiry(value: str) -> Optional[int]:
    """The ``exp`` claim of an access token, or None when the value is not a readable JWT.

    The cookie's Max-Age says how long the browser keeps the cookie; the host stops
    accepting the token at its own ``exp``, which is much sooner (Web, 11-22: a session
    printed as 24 hours lapsed inside one sitting). Only the number is read. The claim is
    not verified here, because the host verifies it on every request.
    """
    parts = value.split(".")
    if len(parts) != 3:
        return None
    try:
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + "=" * (-len(parts[1]) % 4)))
        exp = payload.get("exp") if isinstance(payload, dict) else None
    except Exception:
        return None
    if isinstance(exp, bool) or not isinstance(exp, (int, float)):
        return None
    return int(exp)


def save_session(account: str, cookies: Mapping[str, Tuple[str, Optional[int]]], now: float) -> int:
    """Write the session as a browser storage state, mode 0600, atomically.
    Returns the access cookie's expiry (epoch seconds): the soonest of the cookie's
    Max-Age, the token's own ``exp`` and the 24-hour cap."""
    domain = urllib.parse.urlparse(HOST).hostname
    rows = []
    for name, (value, max_age) in cookies.items():
        rows.append(
            {
                "name": name,
                "value": value,
                "domain": domain,
                "path": "/",
                "expires": min(
                    int(
                        now
                        + min(
                            max_age if max_age is not None else MAX_SESSION_SECONDS,
                            MAX_SESSION_SECONDS,
                        )
                    ),
                    token_expiry(value) or sys.maxsize,
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


# One-shot disconnect (Exec 01M7X9RFAM, 11-20; HOST reads it, condition 4). A connector the
# account must not hold is cleared through the app's own route, so no person signs in as a
# seat account to click (ADR-084 D6). A closed list of connectors; this mode never saves or
# places a session, and it prints only fixed words.
DISCONNECTABLE: Tuple[str, ...] = ("calendar",)
_DISCONNECT_OUTCOMES = frozenset({"cleared", "revoke_failed"})


def disconnect(account: str, connector: str, send: Transport = http_transport) -> str:
    """Sign in, confirm the account and that it is not an admin, clear ``connector`` through
    its disconnect route if the health check shows it, then run bound 2 in full. Returns a
    fixed-word line. Refuses as ``run`` does; never saves a session."""
    if account not in ACCOUNTS:
        raise Refused("that account is not on the list")
    if connector not in DISCONNECTABLE:
        raise Refused("that connector is not on the disconnect list")
    user, password = read_credentials(shared_dir() / ACCOUNTS[account].credential_file)
    cookies = sign_in(account, user, password, send)
    header = {"Cookie": "; ".join(f"{name}={value}" for name, (value, _) in cookies.items())}

    me = send("GET", "/api/v1/auth/me", None, header)
    if me.status != 200 or _json(me).get("username") != account:
        raise Refused("the session is not the named account")
    admin = send(
        "GET",
        "/api/v1/admin/account-flags?" + urllib.parse.urlencode({"username": account}),
        None,
        header,
    )
    if admin.status == 200:
        raise Refused("the account is an admin")
    if admin.status != 403:
        raise Refused("the admin check could not be read")

    health = send("GET", "/api/v1/integrations/health", None, header)
    rows = _json(health).get("integrations") if health.status == 200 else None
    if not isinstance(rows, list):
        raise Refused("the connection check could not be read")
    states = [r.get("status") for r in rows if isinstance(r, dict) and r.get("name") == connector]
    if states == ["not_configured"]:
        before = "was not connected"
    elif len(states) != 1:
        raise Refused("the connection check could not be read")
    else:
        reply = send("POST", f"/api/v1/settings/integrations/{connector}/disconnect", b"", header)
        if reply.status == 503:  # the route's "incomplete" answer; the transport drops its body
            raise Refused(f"the {connector} disconnect did not complete (outcome incomplete)")
        body = _json(reply) if reply.status == 200 else {}
        outcome = body.get("outcome") if isinstance(body, dict) else None
        if outcome not in _DISCONNECT_OUTCOMES:
            raise Refused("the disconnect reply could not be read")
        # HOST 01M7XAG08P: revoke_failed must not read as complete success.
        tail = "; a grant may remain listed at Google" if outcome == "revoke_failed" else ""
        before = f"disconnected (outcome {outcome}{tail})"

    check_holds_nothing_real(account, cookies, send)
    return f"{account}: {connector} {before}; the holds-nothing checks now pass"


# One-shot key save (HOST 01M827TK7G, Arch 01M828NS6F on ADR-084 D2, 11-22). A seat account
# that is to answer chat turns needs a model key, and no person should paste one (D6). The
# helper reads ONE fixed key file itself and sends it to the app's own key-save route as the
# account, so no seat ever holds the value: it is never in a command, an argument, an
# environment variable or any output. The file is the `piper-morgan-test` workspace's spare
# key by Web's record; xian confirms that on his console before the first chat turn (Arch's
# condition 1). A closed list: one provider, one file. This mode never saves a session.
SAVABLE_KEYS: Mapping[str, str] = {"anthropic": "web-credential-anthropic-test-2026-10-15.txt"}
# A standard API key only (Arch 01M82BT11P): the looser ``sk-ant-`` would also match an
# admin key, an organisation-level credential that must never be sent to beta as a
# user's key. Any ``sk-ant-`` value that is not an API key refuses the file.
_KEY_SHAPE = re.compile(r"sk-ant-api[A-Za-z0-9_\-]{20,}")
_ANY_ANTHROPIC_SHAPE = re.compile(r"sk-ant-[A-Za-z0-9_\-]{8,}")


def read_key_file(path: Path) -> str:
    """The one Anthropic key in the file. Refuses anything but a regular file, mode 0600,
    owned by this user, holding exactly one key-shaped value. The file's layout is not
    assumed (a bare key or a ``name: value`` line both work); nothing from it is printed."""
    try:
        info = os.lstat(path)
        if not stat.S_ISREG(info.st_mode):
            raise Refused("the key file is not a regular file")
        if stat.S_IMODE(info.st_mode) & 0o077:
            raise Refused("the key file is not mode 0600")
        if info.st_uid != os.getuid():
            raise Refused("the key file is not owned by this user")
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        raise Refused("the key file is not readable") from None
    found = set(_KEY_SHAPE.findall(text))
    if set(_ANY_ANTHROPIC_SHAPE.findall(text)) - found:
        raise Refused("the key file holds a value that is not a standard API key")
    if len(found) != 1:
        raise Refused("the key file does not hold exactly one key")
    return found.pop()


def _key_rows(provider: str, header: Mapping[str, str], send: Transport) -> list:
    keys = send("GET", "/api/v1/keys/list?active_only=false", None, header)
    listed = _json(keys) if keys.status == 200 else None
    if not isinstance(listed, list):
        raise Refused("the provider-key check could not be read")
    return [row for row in listed if isinstance(row, dict) and row.get("provider") == provider]


class KeyNotValidated(Refused):
    """The key was stored but the provider did not accept it. Its own exit code, so
    nobody books a sitting on a dead key."""


def save_key(account: str, provider: str, send: Transport = http_transport) -> str:
    """Sign in, run bound 2, refuse if the account already has a key for ``provider``, send
    the fixed file's key to ``POST /api/v1/keys/store`` as the account, read back that a key
    is on file, and run bound 2 again. Returns a fixed-word line. From the host's replies
    only a status class is ever printed. Refuses as ``run`` does; never saves a session.

    ``validated: no`` (exit 5) means the key is stored but the provider did not accept it.
    A second run then refuses, because a key is on file. Recovery is a remove mode through
    the app's own delete route, which is not built here: it is a separate diff HOST reads."""
    if account not in ACCOUNTS:
        raise Refused("that account is not on the list")
    if provider not in SAVABLE_KEYS:
        raise Refused("that provider is not on the key list")
    if provider not in ACCOUNTS[account].provider_keys:
        raise Refused("that account may not hold that provider's key")
    key = read_key_file(shared_dir() / SAVABLE_KEYS[provider])
    user, password = read_credentials(shared_dir() / ACCOUNTS[account].credential_file)
    cookies = sign_in(account, user, password, send)
    header = {"Cookie": "; ".join(f"{name}={value}" for name, (value, _) in cookies.items())}

    check_holds_nothing_real(account, cookies, send)
    if _key_rows(provider, header, send):  # a second run must not replace a key silently
        raise Refused("the account already has a key for that provider")

    body = json.dumps({"provider": provider, "api_key": key, "validate": True}).encode()
    reply = send("POST", "/api/v1/keys/store", body, {**header, "Content-Type": "application/json"})
    if not 200 <= reply.status < 300:
        raise Refused(f"the key save was not accepted (status {reply.status // 100}xx)")

    rows = _key_rows(provider, header, send)
    if not rows:
        raise Refused("the key save was accepted but no key is on file")
    check_holds_nothing_real(account, cookies, send)
    # The store route keeps a key the provider refused and still answers 2xx (#485), so
    # "on file" alone can be true for a dead key (Arch 01M82BT11P, HOST 01M82C816F). Only
    # the list row's boolean is read; ``True`` and nothing else counts as validated.
    if not all(row.get("is_validated") is True for row in rows):
        raise KeyNotValidated(f"{account}: key saved; key on file: yes; validated: no")
    return f"{account}: key saved; key on file: yes; validated: yes"


def run(account: str, send: Transport = http_transport, now: Optional[float] = None) -> str:
    if account not in ACCOUNTS:
        raise Refused("that account is not on the list")
    user, password = read_credentials(shared_dir() / ACCOUNTS[account].credential_file)
    cookies = sign_in(account, user, password, send)
    check_holds_nothing_real(account, cookies, send)
    expires = save_session(account, cookies, time.time() if now is None else now)
    stamp = datetime.fromtimestamp(expires, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"{account} session saved, expires {stamp}"


def place_in_seat_browser(account: str) -> int:
    """ADR-084 D3 browser half (issue 2400): when the seat this runs in has a seat browser
    (a row in ``scripts/seat-browser.conf``), put the session just saved into it, so the
    seat's browser tool reads pages signed in. A seat with no row gets nothing more than
    before. A failure here leaves the saved session in place and exits 4 with a fixed
    reason; ``scripts/seat_browser.py`` holds the bounds."""
    try:
        scripts = str(Path(__file__).resolve().parent)
        if scripts not in sys.path:
            sys.path.insert(0, scripts)
        import seat_browser

        if seat_browser.this_seat() not in seat_browser.seats():
            return 0
        try:
            print(seat_browser.place(account))
            return 0
        except (
            seat_browser.Refused
        ) as refusal:  # that module's own class when this file is __main__
            print(
                f"seat_session: session saved, not placed in the seat browser: {refusal}",
                file=sys.stderr,
            )
            return 4
    except Exception as error:  # never print an exception's own text
        print(
            "seat_session: session saved, not placed in the seat browser: "
            f"unexpected {type(error).__name__}",
            file=sys.stderr,
        )
        return 4


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Sign a seeded test account in to beta and save its session."
    )
    parser.add_argument("--account", required=True)
    parser.add_argument(
        "--disconnect",
        choices=DISCONNECTABLE,
        help="clear this connector on the account through the app's route, re-check, save nothing",
    )
    parser.add_argument(
        "--save-key",
        choices=tuple(SAVABLE_KEYS),
        help="save the test workspace's key for this provider on the account, once; saves no session",
    )
    args = parser.parse_args(argv)
    if args.disconnect and args.save_key:
        print("seat_session: refused: one mode at a time", file=sys.stderr)
        return 2
    if args.save_key:
        try:
            print(save_key(args.account, args.save_key))
        except KeyNotValidated as outcome:  # fixed words, on stdout like a result
            print(outcome)
            return 5
        except Refused as refusal:
            print(f"seat_session: refused: {refusal}", file=sys.stderr)
            return 2
        except Exception as error:  # never print an exception's own text
            print(f"seat_session: refused: unexpected {type(error).__name__}", file=sys.stderr)
            return 3
        return 0
    if args.disconnect:
        try:
            print(disconnect(args.account, args.disconnect))
        except Refused as refusal:
            print(f"seat_session: refused: {refusal}", file=sys.stderr)
            return 2
        except Exception as error:  # never print an exception's own text
            print(f"seat_session: refused: unexpected {type(error).__name__}", file=sys.stderr)
            return 3
        return 0
    try:
        print(run(args.account))
    except Refused as refusal:
        print(f"seat_session: refused: {refusal}", file=sys.stderr)
        return 2
    except Exception as error:  # never print an exception's own text: it may carry a URL or a body
        print(f"seat_session: refused: unexpected {type(error).__name__}", file=sys.stderr)
        return 3
    return place_in_seat_browser(args.account)


if __name__ == "__main__":
    sys.exit(main())
