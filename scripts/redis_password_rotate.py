#!/usr/bin/env python3
"""redis_password_rotate.py: rotate the hosted Redis password as ONE command (#2335).

For the person who can run ``fly`` (xian). Run it in Terminal, from a clean worktree,
on a machine where ``fly`` is signed in. It refuses at once without a real terminal:

    python3 scripts/redis_password_rotate.py

Nobody types or sees the password. The command reads the new address from Fly itself
and hands it to the apps on standard input.

What it does, in order:

1. Checks that change nothing: ``fly`` is signed in; beta's ``/health`` reads healthy;
   which Fly Redis database to rotate (``fly redis list``; ``--redis NAME`` if there is
   more than one); which apps hold ``REDIS_URL`` (``fly secrets list``, names only) out
   of the main app and the MCP app; and that ``fly redis status`` gives an address this
   command can read. If it cannot read one, it stops here, before the reset.
2. Asks for a typed ``yes``. From the reset until the main app restarts (about a
   minute), every page on beta answers 503 "capacity_check_unavailable", because the
   usage cap needs Redis and refuses without it.
3. ``fly redis reset NAME``. The old password stops working at once.
4. Reads the address again from ``fly redis status NAME``. Whether its password
   differs from the one before decides whether the reset happened, whatever
   ``fly redis reset`` exited with. If it did not change, nothing was changed.
5. Sets ``REDIS_URL`` on each app that held it, through ``fly secrets import`` on
   standard input.
6. Waits until beta has restarted and reads healthy, then asks a page the usage cap
   guards and expects anything but that 503.
7. Prints one block: names, times and results. No address, no password.

If it stops after the reset, the apps still hold the old address and beta answers 503.
Run it again with ``--after-reset``: it skips the reset and starts at step 4.

Staging has its own Redis database and is not touched unless you name it:
``--redis NAME --apps piper-morgan-staging --health-url https://piper-morgan-staging.fly.dev/health``.

Not run against the hosts by any seat. What ``fly redis reset`` and ``fly redis status``
print is not in Fly's published pages; step 1 exists so that a surprise there stops the
run before anything changes.

Concept: docs/internal/operations/canonical-ops-recipes.md (section 12)
"""

from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))

from github_app_cutover_sitting import (  # noqa: E402 - sibling script, after the path line
    Runner,
    Stop,
    has_terminal,
    now,
    read_health,
    run,
    scrub,
)

MAIN_APP = "piper-morgan"
MCP_APP = "piper-morgan-mcp"
HEALTH_URL = "https://beta.pipermorgan.ai/health"
MCP_HEALTH_URL = "https://mcp.pipermorgan.ai/health"
SECRET_NAME = "REDIS_URL"
BLOCK_START = "===== paste this block on issue 2335 ====="
BLOCK_END = "===== end of block ====="
HALF_STATE = (
    "The Redis password was reset, or may have been, and an app may still hold the old "
    "address. If so, beta answers 503 on every page until it has the new one.\n"
    "Run this again to finish (it skips the reset):\n"
    "    python3 scripts/redis_password_rotate.py --after-reset"
)

NO_TERMINAL = (
    "stopped before anything ran: this command handles a password and asks for a typed "
    "yes, so it needs a real terminal.\n"
    "Run it in Terminal.app, not through Claude Code's ! prefix and not through a pipe."
)

_URL = re.compile(r"rediss?://[^\s\"'<>|]+")
_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


def find_urls(text: str) -> List[str]:
    """Every distinct Redis address in a command's output that carries a password."""
    found: List[str] = []
    for candidate in _URL.findall(text):
        try:
            parts = urlsplit(candidate)
        except ValueError:
            continue
        if parts.password and parts.hostname and candidate not in found:
            found.append(candidate)
    return found


def find_url(text: str) -> Optional[str]:
    """The one such address, or None when there is none or more than one."""
    found = find_urls(text)
    return found[0] if len(found) == 1 else None


def password_of(url: str) -> str:
    return urlsplit(url).password or ""


def redis_names(listing: str) -> List[str]:
    """Database names from ``fly redis list``: the first word of each row under the header."""
    names: List[str] = []
    for line in listing.splitlines():
        word = line.strip().split()[0] if line.strip() else ""
        if not word or word.upper() == "NAME" or not _NAME.match(word):
            continue
        names.append(word)
    return names


def probe_status(url: str) -> int:
    """The HTTP status of one GET, or 0 when nothing answered."""
    req = urllib.request.Request(  # noqa: S310 - https, built from HEALTH_URL
        url, headers={"User-Agent": "redis-rotate"}
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:  # noqa: S310
            return int(resp.status)
    except urllib.error.HTTPError as e:
        return int(e.code)
    except Exception:  # noqa: BLE001 - any failure to reach it is "no answer"
        return 0


class Rotation:
    """The steps, with every outside call behind a seam the tests replace."""

    def __init__(
        self,
        runner: Runner = run,
        health: Callable[[], Dict[str, object]] = read_health,
        probe: Callable[[str], int] = probe_status,
        mcp_health: Callable[[], Dict[str, object]] = lambda: read_health(MCP_HEALTH_URL),
        confirm: Callable[[str], str] = input,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
        out: Callable[[str], None] = print,
        apps: Tuple[str, ...] = (MAIN_APP, MCP_APP),
        probe_url: str = HEALTH_URL.rsplit("/", 1)[0] + "/login",
    ) -> None:
        self.runner = runner
        self.health = health
        self.probe = probe
        self.mcp_health = mcp_health
        self.confirm = confirm
        self.sleep = sleep
        self.clock = clock
        self.out = out
        self.apps = apps
        self.probe_url = probe_url
        self.held: List[str] = []
        self.lines: List[str] = []
        self.was_reset = False
        self.verified_change = True
        self.finished = False

    def hold(self, url: Optional[str]) -> None:
        if url:
            self.held += [url, password_of(url)]

    def note(self, line: str) -> None:
        stamped = f"{now()}  {line}"
        self.lines.append(stamped)
        self.out(scrub(stamped, self.held))

    def call(self, argv: List[str], stdin: Optional[str] = None) -> Tuple[int, str]:
        """Run a command. Any Redis address in its output is held, then scrubbed."""
        code, output = self.runner(argv, stdin)
        # Every one, not the first (CIO, 2026-11-12): a second address in the output
        # must be scrubbed from a failure tail as surely as the one this run uses.
        for url in find_urls(output):
            self.hold(url)
        return code, output

    def tail(self, output: str, lines: int = 4) -> str:
        return scrub("\n".join(output.strip().splitlines()[-lines:]), self.held)

    # --- step 1 -------------------------------------------------------------------
    def choose_database(self, wanted: Optional[str]) -> str:
        code, listing = self.call(["fly", "redis", "list"])
        if code != 0:
            raise Stop(f"`fly redis list` failed.\n{self.tail(listing)}")
        names = redis_names(listing)
        if wanted:
            if wanted not in names:
                raise Stop(f"no Redis database named {wanted}; Fly lists: {', '.join(names)}")
            return wanted
        if len(names) != 1:
            raise Stop(
                f"Fly lists {len(names)} Redis databases ({', '.join(names) or 'none'}). "
                "Name the one to rotate with --redis NAME. Nothing was changed."
            )
        return names[0]

    def holders(self) -> List[str]:
        found: List[str] = []
        for app in self.apps:
            code, listing = self.call(["fly", "secrets", "list", "-a", app])
            if code != 0:
                raise Stop(f"`fly secrets list -a {app}` failed.\n{self.tail(listing)}")
            holds = any(line.split()[:1] == [SECRET_NAME] for line in listing.splitlines())
            self.note(f"{app}: {'holds' if holds else 'does not hold'} {SECRET_NAME}")
            if holds:
                found.append(app)
        if not found:
            raise Stop(f"no app holds {SECRET_NAME}; there is nothing to rotate here")
        return found

    def read_address(self, name: str, what: str) -> str:
        code, output = self.call(["fly", "redis", "status", name])
        found = find_urls(output)
        if code != 0 or not found:
            raise Stop(
                f"could not read {what} from `fly redis status {name}` (exit {code}; "
                "no address with a password in its output)."
            )
        if len(found) > 1:
            # HOST, 2026-11-12: with two, the order would decide what every app gets.
            raise Stop(
                f"`fly redis status {name}` gave {len(found)} different addresses with a "
                "password; this command will not pick one."
            )
        return found[0]

    def preflight(self, wanted: Optional[str]) -> Tuple[str, List[str]]:
        code, output = self.call(["fly", "auth", "whoami"])
        if code != 0:
            raise Stop("`fly` is not signed in (or not installed). Run `fly auth login` first.")
        self.note("fly is signed in                         PASS")
        body = self.health()
        if body.get("status") != "healthy":
            raise Stop("the app's /health did not read healthy; nothing was changed")
        self.note("the app reads healthy                    PASS")
        name = self.choose_database(wanted)
        self.note(f"Redis database: {name}")
        return name, self.holders()

    # --- steps 3 to 6 -------------------------------------------------------------
    def reset(self, name: str, old: str) -> str:
        """Reset the password and return the new address.

        What changed decides, not the exit code (HOST, CIO 2026-11-12): the address is
        read again and its password compared with the one before. So a reset that
        failed without changing anything is reported as that, never as a reset.
        """
        # Until the address is read again, treat the password as possibly changed.
        self.was_reset = True
        code, output = self.call(["fly", "redis", "reset", name])
        new = self.read_address(name, "the address after the reset")
        if password_of(new) == password_of(old):
            self.was_reset = False
            raise Stop(
                f"`fly redis reset {name}` did not change the password (exit {code}). Nothing "
                "was changed. If it asks a question this command cannot answer, run "
                f"`fly redis reset {name}` yourself in this terminal, then this command with "
                f"--after-reset.\n{self.tail(output)}"
            )
        self.note(f"password reset on {name}: the address now carries a different one   PASS")
        if code != 0:
            self.note(f"NOTE: `fly redis reset` exited {code} although the password changed")
        return new

    def set_address(self, apps: List[str], url: str) -> None:
        for app in apps:
            code, output = self.call(
                ["fly", "secrets", "import", "-a", app], f"{SECRET_NAME}={url}\n"
            )
            if code != 0:
                raise Stop(f"setting {SECRET_NAME} on {app} failed.\n{self.tail(output)}")
            self.note(f"{SECRET_NAME} set on {app}        PASS")

    def wait_and_probe(self, since: float, limit_s: float = 420.0) -> None:
        while self.clock() - since < limit_s:
            body = self.health()
            services = body.get("services")
            uptime = services.get("uptime_seconds") if isinstance(services, dict) else None
            if (
                body.get("status") == "healthy"
                and isinstance(uptime, (int, float))
                and uptime <= self.clock() - since
            ):
                self.note(f"the app restarted and reads healthy (up {int(uptime)} s)   PASS")
                break
            self.sleep(10)
        else:
            raise Stop(f"the app did not restart and read healthy within {limit_s:.0f} s")
        status = self.probe(self.probe_url)
        if status in (0, 503):
            raise Stop(
                f"a page the usage cap guards answered {status or 'nothing'}; "
                "Redis is not answering the app"
            )
        self.note(f"a page the usage cap guards answers {status} (not 503)   PASS")

    # --- the whole run ------------------------------------------------------------
    def run_all(self, wanted: Optional[str], after_reset: bool) -> None:
        name, apps = self.preflight(wanted)
        since = self.clock()
        if after_reset:
            self.was_reset = True
            self.verified_change = False
            self.note(
                "--after-reset: the reset is skipped, so this run cannot check that the "
                "password changed"
            )
            new = self.read_address(name, "the new address")
        else:
            old = self.read_address(name, "the address")
            self.note("Fly gives an address this command can read   PASS")
            self.out("")
            self.out(
                f"This resets the password of Redis database {name} and sets the new address on: "
                f"{', '.join(apps)}."
            )
            self.out(
                "From the reset until the restart (about a minute), every page answers 503. "
                "The old password stops working and cannot be brought back."
            )
            if self.confirm("Type yes to reset: ").strip().lower() != "yes":
                raise Stop("not confirmed; nothing was changed")
            since = self.clock()
            new = self.reset(name, old)
        self.note(f"address scheme: {urlsplit(new).scheme}")
        self.set_address(apps, new)
        self.wait_and_probe(since)
        if MCP_APP in apps:
            if self.mcp_health().get("status") != "healthy":
                raise Stop(f"{MCP_APP} did not read healthy after the new address was set")
            self.note(f"{MCP_APP} reads healthy                 PASS")
        self.note(
            "if the reset emptied Redis, the restart refilled the revoked-token list from "
            "the database (it is seeded at every start)"
        )
        self.finished = True


def main(
    argv: Optional[List[str]] = None,
    rotation: Optional[Rotation] = None,
    terminal: Callable[[], bool] = has_terminal,
) -> int:
    p = argparse.ArgumentParser(description="Rotate the hosted Redis password (#2335)")
    p.add_argument("--redis", default=None, help="the Fly Redis database name, if more than one")
    p.add_argument(
        "--apps",
        nargs="+",
        default=None,
        help=f"the apps to check for {SECRET_NAME} (default: {MAIN_APP} {MCP_APP})",
    )
    p.add_argument("--health-url", default=HEALTH_URL, help="the /health to wait on")
    p.add_argument(
        "--after-reset",
        action="store_true",
        help="the password was already reset: skip the reset, set the new address",
    )
    ns = p.parse_args(argv)
    # Section 10 rule 8: before any check.
    if not terminal():
        print(NO_TERMINAL)
        return 2
    if rotation is None:
        rotation = Rotation(
            health=lambda: read_health(ns.health_url),
            apps=tuple(ns.apps) if ns.apps else (MAIN_APP, MCP_APP),
            probe_url=ns.health_url.rsplit("/", 1)[0] + "/login",
        )
    r = rotation
    code = 0
    try:
        r.run_all(ns.redis, ns.after_reset)
    except Stop as e:
        r.note(f"STOPPED: {e}")
        code = 1
    except KeyboardInterrupt:
        r.note("STOPPED: interrupted")
        code = 1
    except Exception as e:  # noqa: BLE001 - the block and the half-state text must print
        r.note(f"STOPPED: unexpected {type(e).__name__}")
        code = 1

    r.out("")
    r.out(BLOCK_START)
    r.out(scrub("\n".join(r.lines), r.held))
    if r.finished and not r.verified_change:
        r.out("RESULT: DONE (address set; change of password NOT verified by this run)")
    else:
        r.out("RESULT: " + ("DONE" if r.finished else "NOT FINISHED"))
    r.out(BLOCK_END)
    if r.was_reset and not r.finished:
        r.out("")
        r.out(HALF_STATE)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
