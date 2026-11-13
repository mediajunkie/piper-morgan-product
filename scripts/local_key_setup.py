#!/usr/bin/env python3
"""Put an LLM provider key into a local Piper Morgan install, at a hidden prompt.

For someone running Piper on their own machine. Run it in a terminal, from the
repository folder, after the Docker services are up and the database is migrated:

    python scripts/local_key_setup.py              # asks which provider, then the key
    python scripts/local_key_setup.py anthropic    # asks for the key only
    python scripts/local_key_setup.py --list       # which providers have a key stored
    python scripts/local_key_setup.py --remove anthropic

What it does:

1. Makes sure the local settings file (``.env``, git-ignored) holds the three values a
   local install needs, and creates any that are missing: a database encryption key
   (``ENCRYPTION_MASTER_KEY``), a sign-in secret (``JWT_SECRET_KEY``) and
   ``PIPER_CREDENTIAL_STORE=db``. A value already there is never replaced.
2. Asks for the provider key with the input hidden.
3. Stores it encrypted in the local database (the ``secure_credentials`` table), reads
   it back and compares.

What it never does: read or write the operating system's keychain, take a key on the
command line, read a key from an environment variable, print a key, or contact the
provider. The server checks the key against the provider when it starts.

Keep ``.env``. The encryption key in it is the only thing that can read the stored
provider keys; if it is lost, run this again to enter them again.

Concept: docs/internal/operations/canonical-ops-recipes.md (section 13)
"""

from __future__ import annotations

import argparse
import base64
import getpass
import os
import re
import secrets
import stat
import sys
from pathlib import Path
from typing import Callable, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# The providers the app reads a server-wide key for (KeychainService.list_stored_keys).
PROVIDERS = ("anthropic", "openai", "gemini", "perplexity")

STORE_VAR = "PIPER_CREDENTIAL_STORE"
MASTER_VAR = "ENCRYPTION_MASTER_KEY"
SCOPED_VAR = "ENCRYPTION_SCOPED_SUBKEYS"
JWT_VAR = "JWT_SECRET_KEY"

NO_TERMINAL = (
    "stopped before anything ran: this command asks for a key at a hidden prompt and "
    "needs a real terminal.\n"
    "Run it in a terminal window, not through a pipe or another program."
)

DB_HELP = (
    "The local database did not answer, or it has not been set up yet.\n"
    "From the repository folder run:\n"
    "    docker compose up -d\n"
    "    alembic upgrade head\n"
    "then run this command again."
)

_NO_SPACE = re.compile(r"^\S+$")


class Stop(Exception):
    """A plain-language reason the run ended; nothing after it runs."""


def has_terminal() -> bool:
    """True when standard input is a terminal, so a hidden prompt cannot echo."""
    try:
        return bool(sys.stdin.isatty())
    except (AttributeError, ValueError):
        return False


def read_settings(path: Path) -> Dict[str, str]:
    """The names and values in the settings file; empty when there is no file."""
    if not path.exists():
        return {}
    from dotenv import dotenv_values

    return {k: v for k, v in dotenv_values(path).items() if v}


def new_master_key() -> str:
    return base64.b64encode(secrets.token_bytes(32)).decode()


def new_jwt_secret() -> str:
    return secrets.token_urlsafe(32)


def ensure_settings(path: Path, environ: Dict[str, str]) -> List[str]:
    """Make the settings file and this process agree on the three local values.

    Returns one plain line per thing done, never a value. A value already in the file
    is kept. A value only in the environment is used and not written. ``environ`` is
    updated so the store built afterwards sees what the server will see.
    """
    notes: List[str] = []
    in_file = read_settings(path)

    if environ.get(SCOPED_VAR) or in_file.get(SCOPED_VAR):
        raise Stop(
            f"{SCOPED_VAR} is set. That is the hosted layout, not a local install; "
            "this command does not handle it."
        )
    for source, where in ((in_file, f"{path.name}"), (environ, "your environment")):
        store = (source.get(STORE_VAR) or "").strip().lower()
        if store and store != "db":
            raise Stop(
                f"{STORE_VAR}={store} is set in {where}. This command only writes the "
                "database store. Remove that setting, or keep it and use "
                "`python main.py keys add <provider>` instead."
            )

    additions: Dict[str, str] = {}
    for name, make, label in (
        (MASTER_VAR, new_master_key, "database encryption key"),
        (JWT_VAR, new_jwt_secret, "sign-in secret"),
    ):
        if in_file.get(name):
            environ[name] = in_file[name]
            notes.append(f"{label}: already in {path.name}, kept")
        elif environ.get(name):
            notes.append(
                f"{label}: taken from your environment, not written to {path.name}. "
                "The server needs the same value when it starts."
            )
        else:
            additions[name] = make()
            environ[name] = additions[name]
            notes.append(f"{label}: created and saved in {path.name}")
    if not in_file.get(STORE_VAR):
        additions[STORE_VAR] = "db"
        notes.append(f"{STORE_VAR}=db saved in {path.name}")
    environ[STORE_VAR] = "db"

    if additions:
        created = not path.exists()
        existing = "" if created else path.read_text()
        lead = "" if (not existing or existing.endswith("\n")) else "\n"
        body = "".join(f"{name}={value}\n" for name, value in additions.items())
        # Opened owner-only from the first byte when the file is new.
        flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT
        fd = os.open(path, flags, stat.S_IRUSR | stat.S_IWUSR)
        with os.fdopen(fd, "a") as fh:
            fh.write(lead + body)
        # CIO (2026-11-12): a file that was already there (copied from the example, say)
        # is usually readable by others, and it now holds the encryption key.
        loose = stat.S_IMODE(path.stat().st_mode) & (stat.S_IRWXG | stat.S_IRWXO)
        if created or loose:
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
        if loose and not created:
            notes.append(f"{path.name} was readable by other accounts; it is now owner-only")
    return notes


def choose_provider(given: Optional[str], shown: Callable[[str], str] = input) -> str:
    name = (given or "").strip().lower()
    if not name:
        name = shown(f"Which provider ({', '.join(PROVIDERS)}): ").strip().lower()
    if name not in PROVIDERS:
        raise Stop(f"unknown provider. Choose one of: {', '.join(PROVIDERS)}")
    return name


def ask_key(provider: str, hidden: Callable[[str], str] = getpass.getpass) -> str:
    """One hidden prompt, asked again once if empty. Never echoed, never returned padded."""
    value = hidden(f"{provider} API key (input hidden): ").strip()
    if not value:
        value = hidden(f"{provider} API key is needed (input hidden): ").strip()
    if not value:
        raise Stop("no key given; nothing was stored")
    if not _NO_SPACE.match(value):
        raise Stop("the key has white space in it; nothing was stored")
    return value


def quiet_logs() -> None:
    """Warnings and errors only: the app's info lines are noise at a prompt."""
    import logging

    import structlog

    logging.basicConfig(level=logging.WARNING)
    structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.WARNING))


def open_store():
    """The app's own credential seam, on the database store."""
    from services.infrastructure.keychain_service import KeychainService

    service = KeychainService()
    if getattr(service, "_db_store", None) is None:
        raise Stop(
            "the database credential store could not be opened; nothing was stored. "
            f"Check that {MASTER_VAR} in .env is the value this install was set up with."
        )
    return service


def check_database(service) -> None:
    """Stop with the two setup commands when the table cannot be read.

    The app's own read returns "no key" when the database is down, which would show
    as an empty list here; this asks the store directly so the cause is named.
    """
    try:
        service._db_store.list_names()
    except Exception as exc:
        raise Stop(f"{DB_HELP}\n({type(exc).__name__})") from None


def stored_providers(service) -> List[str]:
    return [p for p in PROVIDERS if service.get_api_key(p) is not None]


def store_key(service, provider: str, key: str) -> None:
    """Store, then read back and compare. The key is never in a message."""
    try:
        service.store_api_key(provider, key)
    except Exception as exc:
        # The app's message can carry the database's own text; give the type only.
        cause = type(exc.__cause__ or exc).__name__
        raise Stop(f"the key was not stored.\n{DB_HELP}\n({cause})") from None
    if service.get_api_key(provider) != key:
        raise Stop(
            "the key was stored but did not read back the same. Run this command again; "
            "if it repeats, the database encryption key in .env has changed."
        )


def main(
    argv: Optional[List[str]] = None,
    *,
    terminal: Callable[[], bool] = has_terminal,
    hidden: Callable[[str], str] = getpass.getpass,
    shown: Callable[[str], str] = input,
    settings_path: Optional[Path] = None,
    environ: Optional[Dict[str, str]] = None,
    store_factory: Callable[[], object] = open_store,
    out: Callable[[str], None] = print,
) -> int:
    p = argparse.ArgumentParser(
        description="Store an LLM provider key for a local install, at a hidden prompt."
    )
    p.add_argument("provider", nargs="?", help=f"one of: {', '.join(PROVIDERS)}")
    p.add_argument("--list", action="store_true", help="show which providers have a key stored")
    p.add_argument("--remove", metavar="PROVIDER", help="delete the stored key for a provider")
    ns = p.parse_args(argv)
    if ns.provider and ns.provider.strip().lower() not in PROVIDERS:
        # Anything else in that position may be a pasted key: say nothing about it.
        out(f"unknown provider. Choose one of: {', '.join(PROVIDERS)}")
        out("A key is never given on the command line; you are asked for it, hidden.")
        return 2

    asking = not ns.list and not ns.remove
    if asking and not terminal():
        out(NO_TERMINAL)
        return 2

    path = settings_path or (ROOT / ".env")
    env = os.environ if environ is None else environ
    try:
        for note in ensure_settings(path, env):
            out(note)
        quiet_logs()
        service = store_factory()
        check_database(service)

        if ns.list:
            have = stored_providers(service)
            out("stored: " + (", ".join(have) if have else "none"))
            return 0
        if ns.remove:
            provider = choose_provider(ns.remove)
            gone = service.delete_api_key(provider)
            out(f"{provider}: " + ("removed" if gone else "no stored key to remove"))
            return 0

        provider = choose_provider(ns.provider, shown)
        replacing = provider in stored_providers(service)
        key = ask_key(provider, hidden)
        store_key(service, provider, key)
        out(f"{provider}: key {'replaced' if replacing else 'stored'}, read back and matched")
        out("Next: start Piper (python main.py) and open the setup page it names.")
        out(
            'On the "Connect Your AI" step choose this provider and press "Use Keychain": '
            "on a local install that button means the key stored here."
        )
        return 0
    except Stop as stop:
        out(f"STOPPED: {stop}")
        return 1
    except (KeyboardInterrupt, EOFError):
        out("\nSTOPPED: cancelled; nothing more was done")
        return 1
    except Exception as exc:  # never a traceback that could carry a value
        out(f"STOPPED: unexpected {type(exc).__name__}; nothing more was done")
        return 1


if __name__ == "__main__":
    sys.exit(main())
