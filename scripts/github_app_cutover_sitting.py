#!/usr/bin/env python3
"""github_app_cutover_sitting.py: the GitHub App cutover sitting as ONE command (#2343).

For the person who holds the App's values (xian). Run it from a checkout, on a machine
where ``fly`` is signed in:

    venv/bin/python scripts/github_app_cutover_sitting.py

It asks for the App's client ID and client secret (hidden) and its slug, does every
step itself, stops at the first failure, and prints one block to paste on issue 2342.

What it does, in order (canonical-ops-recipes.md section 11, steps 3 and 4):

1. Checks, before asking for anything: ``fly`` is signed in; beta's ``/health`` reads
   healthy; the build beta serves contains ``scripts/github_app_cutover.py``; the MCP
   app serves a build with the fix that keeps a grant record from being sent as a
   bearer (recipe 11, step 2a); and a dry run of the cutover works in the main app's
   container. Nothing has changed yet.
2. Asks for the three values. The client ID and secret are typed hidden.
3. Asks GitHub whether the client ID and secret belong together, with a sign-in code
   that cannot exist. GitHub answers ``bad_verification_code`` for a real pair. Any
   other answer stops the run before anything is set.
4. Asks for a typed ``yes``.
5. Sets ``GITHUB_APP_SLUG`` on the MCP app, then the three values on the main app.
   Values go to ``fly secrets import`` on its standard input, never on a command line.
   The MCP app goes first because the slug alone changes nothing there, and once the
   main app has its values the cutover must follow.
6. Waits until beta has restarted and reads healthy.
7. Runs the cutover dry run in the main app's container and shows the counts.
8. Asks for a typed ``yes``, runs the cutover with ``--apply``, then the dry run again,
   which must find no classic grant.
9. Prints the block: each step's result and time, and the three cutover outputs.

If it stops after step 5 set the main app's values, App mode is on and the cutover
has not run: a classic token is refused by the main app and is still valid at GitHub.
Run it again with ``--cutover-only``, which asks for no value and starts at step 6.

Secrets: read with ``getpass`` only. Never in argv (so ``ps`` cannot see them), never
written to a file, never logged. Anything this run holds is replaced with ``[hidden]``
in whatever it prints.

No seat can run this against the hosts; the unit tests pin its rules and xian's first
run is the served check.

Concept: docs/internal/architecture/adrs/adr-081-github-identity-one-app-whose-token-serves-a-request.md
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import re
import subprocess  # noqa: S404 - runs flyctl and git with fixed argv
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
MAIN_APP = "piper-morgan"
MCP_APP = "piper-morgan-mcp"
HEALTH_URL = "https://beta.pipermorgan.ai/health"
MCP_HEALTH_URL = "https://mcp.pipermorgan.ai/health"
#: The fix that stops the MCP app sending a stored grant record as a bearer. An MCP
#: build without it would forward a reconnected person's refresh token (PA, 2026-11-12).
MCP_NEEDS_COMMIT = "7e32d63f688109cb1e6ad642d515f9f7269fb2b3"
TOKEN_URL = "https://github.com/login/oauth/access_token"  # noqa: S105 - an endpoint
CUTOVER_IN_IMAGE = "/app/scripts/github_app_cutover.py"
CUTOVER_IN_REPO = "scripts/github_app_cutover.py"
BLOCK_START = "===== paste this block on issue 2342 ====="
BLOCK_END = "===== end of block ====="
HALF_STATE = (
    "App mode is ON on the main app and the cutover has NOT finished. A classic token is "
    "refused by the main app and is still valid at GitHub.\n"
    "Run this again to finish, with no values to type:\n"
    "    venv/bin/python scripts/github_app_cutover_sitting.py --cutover-only"
)

#: A value goes to ``fly secrets import`` as one NAME=VALUE line, so it can hold no
#: white space. The slug is the last part of the App's public page address.
_NO_SPACE = re.compile(r"^\S+$")
_SLUG = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
_FOUND = re.compile(r"classic grants found\s+(\d+)\s*$", re.MULTILINE)

#: (argv, standard input or None) -> (exit code, output). The seam the tests replace.
Runner = Callable[[List[str], Optional[str]], Tuple[int, str]]


class Stop(Exception):
    """A step failed. The message is what to print; nothing after it runs."""


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(argv: List[str], stdin: Optional[str] = None, timeout: float = 600.0) -> Tuple[int, str]:
    """Run a fixed command. A value reaches it only through ``stdin``."""
    env = dict(os.environ, FLY_NO_UPDATE_CHECK="1")
    try:
        # ``input`` and ``stdin`` cannot both be given. With no value to pass, the
        # child gets an empty standard input so it can never wait on the terminal.
        feed = {"input": stdin} if stdin is not None else {"stdin": subprocess.DEVNULL}
        done = subprocess.run(  # noqa: S603 - fixed argv, no secret in it
            argv,
            capture_output=True,
            text=True,
            env=env,
            cwd=str(ROOT),
            timeout=timeout,
            **feed,
        )
    except FileNotFoundError:
        return 127, f"{argv[0]}: not found on PATH"
    except subprocess.TimeoutExpired:
        return 124, f"{' '.join(argv[:3])}: no answer in {timeout:.0f} s"
    return done.returncode, (done.stdout or "") + (done.stderr or "")


def scrub(text: str, held: List[str]) -> str:
    """No value this run holds can appear in what is printed."""
    for value in sorted((v for v in held if v), key=len, reverse=True):
        text = text.replace(value, "[hidden]")
    return text


def read_health(url: str = HEALTH_URL) -> Dict[str, object]:
    req = urllib.request.Request(  # noqa: S310 - fixed https endpoint
        url, headers={"User-Agent": "cutover-sitting"}
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:  # noqa: S310
            body = json.loads(resp.read().decode() or "{}")
    except (urllib.error.URLError, ValueError, OSError):
        return {}
    return body if isinstance(body, dict) else {}


def ask_github(client_id: str, client_secret: str) -> str:
    """GitHub's error code for a sign-in code that cannot exist. Carries no secret."""
    data = urllib.parse.urlencode(
        {"client_id": client_id, "client_secret": client_secret, "code": "not-a-real-code"}
    ).encode()
    req = urllib.request.Request(  # noqa: S310 - fixed https endpoint
        TOKEN_URL,
        data=data,
        headers={"Accept": "application/json", "User-Agent": "cutover-sitting"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
            body = json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}"
    except (urllib.error.URLError, ValueError, OSError) as e:
        return f"no answer ({type(e).__name__})"
    if isinstance(body, dict) and "access_token" in body:
        return "unexpected: a token was issued"
    return str(body.get("error") or "no error code") if isinstance(body, dict) else "no error code"


def cutover_argv(apply: bool) -> List[str]:
    """The container command. It carries no value: the script reads the environment."""
    command = f"python {CUTOVER_IN_IMAGE}" + (" --apply" if apply else "")
    return ["fly", "ssh", "console", "-a", MAIN_APP, "-C", command]


def import_argv(app: str) -> List[str]:
    return ["fly", "secrets", "import", "-a", app]


def classic_found(output: str) -> Optional[int]:
    m = _FOUND.search(output)
    return int(m.group(1)) if m else None


def ask_values(
    hidden: Callable[[str], str] = getpass.getpass, shown: Callable[[str], str] = input
) -> Dict[str, str]:
    """Ask for each value once. The client ID and secret are hidden; the slug is public."""
    out: Dict[str, str] = {}
    for key, label in (
        ("client_id", "GitHub App client ID"),
        ("client_secret", "GitHub App client secret"),
    ):
        value = hidden(f"{label} (input hidden): ").strip()
        if not value:
            value = hidden(f"{label} is needed (input hidden): ").strip()
        if not value:
            raise Stop(f"no {label.lower()} given")
        if not _NO_SPACE.match(value):
            raise Stop(f"the {label.lower()} has white space in it; nothing was set")
        out[key] = value
    slug = shown("GitHub App slug (the last part of github.com/apps/<slug>): ").strip().lower()
    if not _SLUG.match(slug):
        raise Stop("the slug must be lower-case letters, digits and hyphens; nothing was set")
    out["slug"] = slug
    return out


class Sitting:
    """The steps, with every outside call behind a seam the tests replace."""

    def __init__(
        self,
        runner: Runner = run,
        health: Callable[[], Dict[str, object]] = read_health,
        mcp_health: Callable[[], Dict[str, object]] = lambda: read_health(MCP_HEALTH_URL),
        github: Callable[[str, str], str] = ask_github,
        confirm: Callable[[str], str] = input,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
        out: Callable[[str], None] = print,
    ) -> None:
        self.runner = runner
        self.health = health
        self.mcp_health = mcp_health
        self.github = github
        self.confirm = confirm
        self.sleep = sleep
        self.clock = clock
        self.out = out
        self.held: List[str] = []
        self.lines: List[str] = []
        self.main_set = False
        self.finished = False

    def note(self, line: str) -> None:
        """One line for the block, stamped, and shown as the run goes."""
        stamped = f"{now()}  {line}"
        self.lines.append(stamped)
        self.out(scrub(stamped, self.held))

    def call(self, argv: List[str], stdin: Optional[str] = None) -> Tuple[int, str]:
        code, output = self.runner(argv, stdin)
        return code, scrub(output, self.held)

    # --- step 1: checks that change nothing -------------------------------------
    def preflight(self, cutover_only: bool = False) -> None:
        code, output = self.call(["fly", "auth", "whoami"])
        if code != 0:
            raise Stop("`fly` is not signed in (or not installed). Run `fly auth login` first.")
        self.note("fly is signed in                         PASS")

        body = self.health()
        sha = str(body.get("git_sha") or "")
        if body.get("status") != "healthy" or not sha:
            raise Stop("beta's /health did not read healthy with a build sha; nothing was set")
        self.runner(["git", "fetch", "--quiet", "origin", "main"], None)
        code, _ = self.call(["git", "cat-file", "-e", f"{sha}:{CUTOVER_IN_REPO}"])
        if code != 0:
            raise Stop(
                f"the build beta serves ({sha[:10]}) does not contain {CUTOVER_IN_REPO}, or "
                "this checkout does not have that commit. Promote first (recipe 11, step 2)."
            )
        self.note(f"beta serves {sha[:10]}, with the cutover script   PASS")

        mcp_sha = str(self.mcp_health().get("git_sha") or "")
        code = 1
        if mcp_sha:
            code, _ = self.call(["git", "merge-base", "--is-ancestor", MCP_NEEDS_COMMIT, mcp_sha])
        if code == 0:
            self.note(f"MCP app serves {mcp_sha[:10]}, with the bearer fix   PASS")
        elif cutover_only:
            # The values are already set, so finishing the cutover is still right.
            self.note(
                f"MCP app serves {mcp_sha[:10] or 'an unread build'}, WITHOUT the bearer fix   "
                "WARNING: deploy it now (recipe 11, step 2a)"
            )
        else:
            raise Stop(
                f"the MCP app serves {mcp_sha[:10] or 'a build this could not read'}, which does "
                "not have the fix that keeps a grant record from being sent as a bearer. "
                "Deploy the MCP app from main first (recipe 11, step 2a). Nothing was set."
            )

    def cutover(self, apply: bool, label: str) -> str:
        code, output = self.call(cutover_argv(apply))
        if code != 0 or "github app cutover:" not in output:
            tail = "\n".join(output.strip().splitlines()[-6:])
            raise Stop(f"{label} did not run (exit {code}).\n{tail}")
        kept = [
            line
            for line in output.splitlines()
            if line.startswith("github app cutover:") or line.startswith("  ")
        ]
        self.note(f"{label}:")
        for line in kept:
            self.lines.append(line)
            self.out(line)
        return output

    # --- steps 3 to 5 -------------------------------------------------------------
    def check_pair(self, values: Dict[str, str]) -> None:
        answer = self.github(values["client_id"], values["client_secret"])
        if answer != "bad_verification_code":
            raise Stop(
                f"GitHub did not accept the client ID and secret as a pair (it said: {answer}). "
                "Nothing was set."
            )
        self.note("GitHub accepts the client ID and secret   PASS")

    def set_values(self, values: Dict[str, str]) -> None:
        slug_line = f"GITHUB_APP_SLUG={values['slug']}\n"
        code, output = self.call(import_argv(MCP_APP), slug_line)
        if code != 0:
            tail = "\n".join(output.strip().splitlines()[-4:])
            raise Stop(f"setting the slug on {MCP_APP} failed; the main app is unchanged.\n{tail}")
        self.note(f"slug set on {MCP_APP}              PASS")

        main_lines = (
            f"GITHUB_APP_CLIENT_ID={values['client_id']}\n"
            f"GITHUB_APP_CLIENT_SECRET={values['client_secret']}\n" + slug_line
        )
        # From here a failure may have set them; treat the main app as changed.
        self.main_set = True
        code, output = self.call(import_argv(MAIN_APP), main_lines)
        if code != 0:
            tail = "\n".join(output.strip().splitlines()[-4:])
            raise Stop(f"setting the values on {MAIN_APP} failed or half-finished.\n{tail}")
        self.note(f"three values set on {MAIN_APP}          PASS")

    # --- step 6 -------------------------------------------------------------------
    def wait_for_restart(self, since: float, limit_s: float = 420.0) -> None:
        """Healthy, and up for less time than has passed since the values were set."""
        while self.clock() - since < limit_s:
            body = self.health()
            services = body.get("services") if isinstance(body.get("services"), dict) else {}
            uptime = services.get("uptime_seconds") if isinstance(services, dict) else None
            if (
                body.get("status") == "healthy"
                and isinstance(uptime, (int, float))
                and uptime <= self.clock() - since
            ):
                self.note(f"beta restarted and reads healthy (up {int(uptime)} s)   PASS")
                return
            self.sleep(10)
        raise Stop(f"beta did not restart and read healthy within {limit_s:.0f} s")

    # --- the whole run ------------------------------------------------------------
    def run_all(self, cutover_only: bool, ask: Callable[[], Dict[str, str]] = ask_values) -> None:
        self.preflight(cutover_only)
        if cutover_only:
            self.main_set = True
            self.note("--cutover-only: no value asked for or set")
        else:
            self.cutover(False, "dry run before anything is set")
            values = ask()
            self.held += [values["client_id"], values["client_secret"]]
            self.check_pair(values)
            self.out("")
            self.out(f"This turns GitHub App mode ON for {MAIN_APP} (beta). The cutover follows.")
            if self.confirm("Type yes to set the values: ").strip().lower() != "yes":
                raise Stop("not confirmed; nothing was set")
            since = self.clock()
            self.set_values(values)
            self.wait_for_restart(since)

        first = self.cutover(False, "dry run")
        found = classic_found(first)
        if found is None:
            raise Stop("the dry run printed no count of classic grants")
        self.out("")
        self.out(
            f"--apply revokes and deletes {found} classic GitHub token(s) and marks those "
            "connections stale. Each person reconnects once. It cannot be undone."
        )
        if self.confirm("Type yes to apply: ").strip().lower() != "yes":
            raise Stop("not confirmed; the cutover was not applied")
        self.cutover(True, "apply")
        last = self.cutover(False, "dry run after")
        left = classic_found(last)
        if left != 0:
            raise Stop(f"the dry run after still finds classic grants ({left})")
        self.note("no classic grant left                    PASS")
        self.finished = True


def main(argv: Optional[List[str]] = None, sitting: Optional[Sitting] = None) -> int:
    p = argparse.ArgumentParser(description="The GitHub App cutover sitting as one command (#2343)")
    p.add_argument(
        "--cutover-only",
        action="store_true",
        help="the values are already set: ask for nothing, wait for nothing, run the cutover",
    )
    ns = p.parse_args(argv)
    s = sitting or Sitting()
    code = 0
    try:
        s.run_all(ns.cutover_only)
    except Stop as e:
        s.note(f"STOPPED: {e}")
        code = 1
    except KeyboardInterrupt:
        s.note("STOPPED: interrupted")
        code = 1

    s.out("")
    s.out(BLOCK_START)
    s.out(scrub("\n".join(s.lines), s.held))
    s.out("RESULT: " + ("DONE" if s.finished else "NOT FINISHED"))
    s.out(BLOCK_END)
    if s.main_set and not s.finished:
        s.out("")
        s.out(HALF_STATE)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
