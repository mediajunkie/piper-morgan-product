#!/usr/bin/env python3
"""ADR-084 D3, Step F0 (issue 2389): create one seat account on beta from an invite
code xian minted, with a password no seat or person ever sees.

xian's part, once: mint one invite code and leave two lines in a file under
``~/.piper-shared``, mode 0600::

    invite: <the code>
    email: <the address for the account>

The file is ``<account>-invite-token.txt``, a name the fleet's Read denies match. He
can write it with ``--write-invite``, which asks for the code at a hidden prompt and
for the email, refuses without a terminal, and writes the file at mode 0600; nothing
he types is echoed, put in argv or printed. A seat then runs this script under one
exact-command allow. The script reads the file itself; no seat does.

What it does, in order:
1. Refuses a name that is not on ``seat_session.ACCOUNTS``, an account whose
   credential file already exists, and an invite file that is missing, readable by
   others, or without both lines.
2. Generates a password in this process and sends one sign-up call to the fixed host.
3. Only when the host has answered that the account exists: writes the credential
   file (``username:`` and ``password:``, mode 0600, the name on the account's row),
   then deletes the invite file, whose code is now spent.

HOST's conditions (2026-11-16), all enforced here:
- One code, one account, one file. The invite file is kept unless the code was spent.
- A fixed account list in code and one fixed host. No ``--host`` option exists.
- No value is printed: not the code, the email, the password, a response body or an
  exception's text. Output is the account name and "created", or a fixed reason.
- It sets no flag, stores no provider key, and keeps no cookie from the reply.

Usage:
    scripts/seat_account_create.py --account seat-github-1 --write-invite   (xian, in Terminal)
    scripts/seat_account_create.py --account seat-github-1                  (a seat)

Concept: docs/internal/operations/adr-084-one-time-steps.md
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import secrets
import stat
import sys
import tempfile
import urllib.parse
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

import seat_session  # noqa: E402
from seat_session import Refused, Reply, Transport  # noqa: E402

INVITE_KEY = "invite"
EMAIL_KEY = "email"
PASSWORD_BYTES = 32  # token_urlsafe(32) is 43 characters


def invite_path(account: str) -> Path:
    return seat_session.shared_dir() / f"{account}-invite-token.txt"


def credential_path(account: str) -> Path:
    return seat_session.shared_dir() / seat_session.ACCOUNTS[account].credential_file


def read_invite(path: Path) -> Tuple[str, str]:
    """The invite code and the email from xian's two-line file. Names which line is
    missing and never anything from the file."""
    try:
        mode = stat.S_IMODE(path.stat().st_mode)
        text = path.read_text(encoding="utf-8")
    except OSError:
        raise Refused("the invite file is not there or not readable") from None
    if mode & 0o077:
        raise Refused("the invite file is not mode 0600")
    found: Dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        positions = [line.index(sep) for sep in (":", "=") if sep in line]
        if positions:
            at = min(positions)
            found.setdefault(line[:at].strip().lower(), line[at + 1 :].strip().strip("'\""))
    if not found.get(INVITE_KEY):
        raise Refused(f"the invite file has no '{INVITE_KEY}' line")
    if not found.get(EMAIL_KEY):
        raise Refused(f"the invite file has no '{EMAIL_KEY}' line")
    return found[INVITE_KEY], found[EMAIL_KEY]


def _created(reply: Reply) -> bool:
    if reply.status != 200:
        return False
    try:
        return json.loads(reply.body.decode("utf-8")).get("success") is True
    except Exception:
        return False


def _signs_in(account: str, password: str, send: Transport) -> bool:
    """Does the host already know this account with this password? Used only when the
    sign-up call's outcome is unknown, so a created account is never left without its
    credential file."""
    form = urllib.parse.urlencode({"username": account, "password": password}).encode()
    try:
        reply = send(
            "POST",
            "/api/v1/auth/login",
            form,
            {"Content-Type": "application/x-www-form-urlencoded"},
        )
    except Exception:
        return False
    return reply.status == 200


def sign_up(account: str, email: str, password: str, invite: str, send: Transport) -> None:
    """One sign-up call. Returns only when the account exists on the host."""
    body = json.dumps(
        {
            "username": account,
            "email": email,
            "password": password,
            "password_confirm": password,
            "invite_token": invite,
        }
    ).encode()
    try:
        reply = send(
            "POST", "/api/v1/setup/create-user", body, {"Content-Type": "application/json"}
        )
    except Exception:
        reply = None
    if reply is not None and _created(reply):
        return
    if reply is not None and reply.status == 400:
        # The app refuses inside one transaction, so the code is not spent.
        raise Refused(
            "the host refused the sign-up (400): the name or email is taken, or the invite "
            "code is wrong or already used. The invite file is kept."
        )
    if reply is not None and reply.status == 422:
        raise Refused(
            "the host refused the sign-up (422): a field is not in the form it accepts. "
            "The invite file is kept."
        )
    # No answer, a server error, or an answer that could not be read: the account may
    # or may not exist. Ask the host by signing in with the password only this process holds.
    if _signs_in(account, password, send):
        return
    raise Refused(
        "the sign-up did not complete and the account does not sign in. "
        "The invite file is kept; the code may or may not be spent."
    )


def write_credentials(account: str, password: str) -> None:
    """``username:`` and ``password:``, mode 0600, through a temporary file."""
    target = credential_path(account)
    try:
        target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        fd, temp = tempfile.mkstemp(dir=str(target.parent), prefix=".credential-")
        try:
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(f"username: {account}\npassword: {password}\n")
            os.replace(temp, target)
        except BaseException:
            try:
                os.unlink(temp)
            except OSError:
                pass
            raise
    except OSError:
        raise Refused(
            "the account was created but its credential file could not be written. "
            "The invite code is spent; the account needs a password reset."
        ) from None
    if "credential" not in target.name or stat.S_IMODE(target.stat().st_mode) != 0o600:
        raise Refused("the credential file's name or mode is not what the Read denies cover")


def write_invite(
    account: str,
    ask_hidden: Optional[Callable[[str], str]] = None,
    ask: Optional[Callable[[str], str]] = None,
    is_terminal: Optional[Callable[[], bool]] = None,
) -> str:
    """xian's half: put the code and the email in the invite file from two prompts.
    A seat cannot use this: it refuses without a terminal."""
    ask_hidden = ask_hidden or getpass.getpass
    ask = ask or input
    is_terminal = is_terminal or (lambda: sys.stdin.isatty() and sys.stdout.isatty())
    if account not in seat_session.ACCOUNTS:
        raise Refused("that account is not on the list")
    if not is_terminal():
        raise Refused("--write-invite needs a terminal: the code is typed at a hidden prompt")
    if credential_path(account).exists():
        raise Refused("that account already has a credential file; it was created before")
    target = invite_path(account)
    if target.exists():
        raise Refused("an invite file for that account is already there")
    invite = ask_hidden("Invite code (hidden): ").strip()
    email = ask("Email address for the account: ").strip()
    if not invite or not email or "\n" in invite or "\n" in email:
        raise Refused("the code and the email are both needed, one line each")
    try:
        target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        fd, temp = tempfile.mkstemp(dir=str(target.parent), prefix=".invite-token-")
        try:
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(f"{INVITE_KEY}: {invite}\n{EMAIL_KEY}: {email}\n")
            os.replace(temp, target)
        except BaseException:
            try:
                os.unlink(temp)
            except OSError:
                pass
            raise
    except OSError:
        raise Refused("the invite file could not be written") from None
    return f"{account} invite file written"


def run(account: str, send: Optional[Transport] = None) -> str:
    # Resolved at call time, so a test that replaces the transport can never fall
    # through to the real host.
    send = send or seat_session.http_transport
    if account not in seat_session.ACCOUNTS:
        raise Refused("that account is not on the list")
    if credential_path(account).exists():
        raise Refused("that account already has a credential file; it was created before")
    invite_file = invite_path(account)
    invite, email = read_invite(invite_file)
    password = secrets.token_urlsafe(PASSWORD_BYTES)
    sign_up(account, email, password, invite, send)
    write_credentials(account, password)
    try:
        invite_file.unlink()
    except OSError:
        raise Refused(
            "the account was created and its credential file written, but the spent "
            "invite file could not be deleted"
        ) from None
    return f"{account} created"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Create one seat account on beta.")
    parser.add_argument("--account", required=True)
    parser.add_argument(
        "--write-invite",
        action="store_true",
        help="xian's half, in Terminal: type the code (hidden) and the email into the invite file",
    )
    args = parser.parse_args(argv)
    try:
        print(write_invite(args.account) if args.write_invite else run(args.account))
        return 0
    except Refused as refusal:
        print(f"seat_account_create: refused: {refusal}", file=sys.stderr)
        return 2
    except Exception as error:  # never print an exception's own text
        print(f"seat_account_create: refused: unexpected {type(error).__name__}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
