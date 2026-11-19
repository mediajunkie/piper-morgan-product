#!/usr/bin/env python3
"""restore_drill_2157.py — #2157's restore drill as one command (HOST's design v2, 11-12;
Arch accepted it with the allowlist as written and a throwaway Redis, 11-12).

xian runs it, in Terminal (canonical-ops-recipes section 10: hidden prompts, no secret in
argv, helpers stopped on every path, one block to paste, refuses without a terminal):

    python3 scripts/restore_drill_2157.py --org <fly org slug>

What it does:
1. Refuses without a terminal. Reads what exists (no change): the production database's
   volume, its newest snapshot and that snapshot's age, the image beta serves. Prints the
   copy's name and that the copy holds everyone's data; you type the name to go on.
2. Asks, hidden: the master key, read from its recorded backup location (that is what
   proves the backup works; never from production's secrets), and R's password. R's
   sign-in name is asked shown.
3. Creates, on a new private network of its own (never staging, never production's):
   a Postgres app from that snapshot, a throwaway Redis app (Arch: the usage cap fails
   closed without Redis; it is never switched off), and the copy app running beta's
   image. The copy gets exactly five secrets, through stdin: its database address, the
   master key, a fresh JWT secret, the Redis address, ``PIPER_CREDENTIAL_STORE=db``. No
   GitHub App, Slack, Calendar, email or MCP values, so nothing on the copy can refresh
   or spend a real person's grant.
4. Proof 1: R signs in on the copy (through ``fly proxy``; the copy has no public
   address) and a signed-in request answers. Prints the time from the start.
5. Proof 2: one stored key decrypts under the typed master key, inside the copy
   (``verify_stored_credential_decrypt.py --own-database-in-drill-copy``).
6. Proof 3 is NOT RUN: it replays the deletion record, which #2158 hasn't built. Proof 4
   (who held the restore and where its log is) is a statement xian writes.
7. Proof 5, on every path, failures and Ctrl-C included: lists each created app's volume
   snapshots (expected none: a run is shorter than Fly's daily snapshot), destroys the
   three apps, then lists apps and shows all three absent. ``--keep`` skips the destroy
   and prints the names to destroy by hand.
8. Prints one block for issue 2157. RESULT says DONE only when every proof passed and the
   listing was empty; while proof 3 isn't built the best is PROOFS 1, 2, 5 PASSED.

Not verified from a seat (no seat runs ``fly`` against the org): the ``fly image show``
JSON shape, that a flex cluster made from a snapshot takes the new superuser password the
create prints, that the copy reaches its database at ``<name>.flycast:5432`` and Redis at
``<name>.internal:6379``, and that beta's image boots with no ChromaDB or GitHub MCP. Each
shows up as a stopped step with its reason, and the copy is destroyed.

Concept: docs/internal/operations/restore-drill-2157-lead-half-fly-lines-DRAFT-2026-11-04.md
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import re
import secrets
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DB = "piper-morgan-db"
SOURCE_APP = "piper-morgan"
LOCAL_PORT = 18001
BLOCK_START = "===== paste this block on issue 2157 ====="
BLOCK_END = "===== end of block ====="
NO_TERMINAL = (
    "run this in a real terminal (Terminal.app), not through Claude Code's ! prefix: "
    "it asks for the master key with a hidden prompt"
)
DRILL_COPY_ENV = "PIPER_RESTORE_DRILL_COPY"  # the decrypt script's drill-copy switch
PROOF_2 = "python /app/scripts/verify_stored_credential_decrypt.py --own-database-in-drill-copy"
REDIS_IMAGE = "redis:7.2-alpine"
_PASSWORD = re.compile(r"^\s*Password:\s*(\S+)\s*$", re.MULTILINE)
_NO_SPACE = re.compile(r"^\S+$")

#: (argv, standard input or None) -> (exit code, output). The seam the tests replace.
Runner = Callable[[List[str], Optional[str]], Tuple[int, str]]
#: (method, url, form or None, bearer or None) -> (status, parsed JSON or {}).
Http = Callable[[str, str, Optional[Dict[str, str]], Optional[str]], Tuple[int, Dict]]


class Stop(Exception):
    """A step failed. The message is what to print; the cleanup still runs."""


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(argv: List[str], stdin: Optional[str] = None, timeout: float = 900.0) -> Tuple[int, str]:
    """Run a fixed command. A value reaches it only through ``stdin``."""
    env = dict(os.environ, FLY_NO_UPDATE_CHECK="1")
    feed = {"input": stdin} if stdin is not None else {"stdin": subprocess.DEVNULL}
    try:
        done = subprocess.run(  # noqa: S603 - fixed argv, no secret in it
            argv, capture_output=True, text=True, env=env, cwd=str(ROOT), timeout=timeout, **feed
        )
    except FileNotFoundError:
        return 127, f"{argv[0]}: not found on PATH"
    except subprocess.TimeoutExpired:
        return 124, f"{' '.join(argv[:3])}: no answer in {timeout:.0f} s"
    return done.returncode, (done.stdout or "") + (done.stderr or "")


def http(method: str, url: str, form=None, bearer=None) -> Tuple[int, Dict]:
    """One request to the copy through the local proxy. Never prints the body."""
    data = urllib.parse.urlencode(form).encode() if form is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    if bearer:
        req.add_header("Authorization", f"Bearer {bearer}")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:  # noqa: S310 - localhost
            body = resp.read()
            status = resp.status
    except urllib.error.HTTPError as e:
        return e.code, {}
    except (urllib.error.URLError, OSError):
        return 0, {}
    try:
        return status, json.loads(body or b"{}")
    except ValueError:
        return status, {}


class Proxy:
    """``fly proxy`` as a helper process: started for proof 1, stopped on every path."""

    def __init__(self, app: str, port: int = LOCAL_PORT) -> None:
        self.app, self.port = app, port
        self.proc: Optional[subprocess.Popen] = None

    def start(self) -> None:
        self.proc = subprocess.Popen(  # noqa: S603 - fixed argv
            ["fly", "proxy", f"{self.port}:8001", "-a", self.app],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=dict(os.environ, FLY_NO_UPDATE_CHECK="1"),
        )

    def stop(self) -> None:
        if self.proc is not None and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        self.proc = None


def scrub(text: str, held: List[str]) -> str:
    """No value this run holds can appear in what is printed."""
    for value in sorted((v for v in held if v), key=len, reverse=True):
        text = text.replace(value, "[hidden]")
    return text


def names(stamp: str) -> Dict[str, str]:
    """The copy's three apps and its network, all new, all named for this run."""
    base = f"pm-restore-drill-{stamp}"
    return {"app": base, "db": f"{base}-db", "redis": f"{base}-redis", "network": base}


def newest_snapshot(listing: List[Dict]) -> Optional[Dict]:
    """The newest snapshot in a ``fly volumes snapshots list --json`` listing."""
    dated = [s for s in listing if s.get("id") and (s.get("created_at") or s.get("CreatedAt"))]
    return max(dated, key=lambda s: s.get("created_at") or s.get("CreatedAt"), default=None)


def image_ref(shown) -> Optional[str]:
    """Beta's image from ``fly image show --json``: one object, or one per machine (all
    must agree). Unverified shape from a seat; None stops the run before anything is made."""
    items = shown if isinstance(shown, list) else [shown]
    refs = set()
    for item in items:
        if not isinstance(item, dict):
            return None
        reg, repo = item.get("Registry"), item.get("Repository")
        pin = item.get("Digest") and f"@{item['Digest']}" or item.get("Tag") and f":{item['Tag']}"
        if not (reg and repo and pin):
            return None
        refs.add(f"{reg}/{repo}{pin}")
    return refs.pop() if len(refs) == 1 else None


def secrets_stdin(values: Dict[str, str]) -> str:
    """``fly secrets import`` input: NAME=VALUE lines. A value with white space would split."""
    for name, value in values.items():
        if not _NO_SPACE.match(value or ""):
            raise Stop(f"{name} is empty or holds white space; nothing was set")
    return "".join(f"{k}={v}\n" for k, v in values.items())


def ask_values(
    hidden: Callable[[str], str] = getpass.getpass, shown: Callable[[str], str] = input
) -> Tuple[str, str, str]:
    key = hidden("ENCRYPTION_MASTER_KEY, from its recorded backup location (hidden): ").strip()
    who = shown("R's sign-in name (shown): ").strip()
    password = hidden("R's password (hidden): ")
    if not key or not who or not password:
        raise Stop("a value was empty; nothing was created")
    return key, who, password


class Drill:
    """The steps, with every outside call behind a seam the tests replace."""

    def __init__(
        self,
        org: str,
        region: str = "sjc",
        keep: bool = False,
        runner: Runner = run,
        request: Http = http,
        proxy_factory: Callable[[str], Proxy] = Proxy,
        values: Callable[[], Tuple[str, str, str]] = ask_values,
        confirm: Callable[[str], str] = input,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
        out: Callable[[str], None] = print,
        stamp: Optional[str] = None,
    ) -> None:
        self.org, self.region, self.keep = org, region, keep
        self.runner, self.request, self.proxy_factory = runner, request, proxy_factory
        self.values, self.confirm = values, confirm
        self.sleep, self.clock, self.out = sleep, clock, out
        self.n = names(stamp or datetime.now(timezone.utc).strftime("%Y%m%d-%H%M"))
        self.held: List[str] = []
        self.lines: List[str] = []
        self.attempted: List[str] = []  # apps this run tried to make; cleanup covers them all
        self.proxy: Optional[Proxy] = None
        self.passed: Dict[str, bool] = {}
        self.listing_clean = False

    def note(self, line: str) -> None:
        stamped = f"{now()}  {line}"
        self.lines.append(stamped)
        self.out(scrub(stamped, self.held))

    def call(self, argv: List[str], stdin: Optional[str] = None) -> Tuple[int, str]:
        code, output = self.runner(argv, stdin)
        return code, scrub(output, self.held)

    def must(self, argv: List[str], what: str, stdin: Optional[str] = None) -> str:
        code, output = self.call(argv, stdin)
        if code != 0:
            tail = output.strip().splitlines()[-1:] if output.strip() else ["(no output)"]
            raise Stop(f"{what} failed (exit {code}): {tail[0][:200]}")
        return output

    def json_of(self, argv: List[str], what: str):
        output = self.must(argv, what)
        try:
            return json.loads(output)
        except ValueError:
            raise Stop(f"{what}: the output was not JSON") from None

    # --- step 1: reads that change nothing ------------------------------------------
    def preflight(self) -> Dict[str, str]:
        who = self.must(["fly", "auth", "whoami"], "fly auth whoami").strip().splitlines()
        self.note(f"fly signed in as: {who[-1] if who else '(unknown)'}")
        vols = self.json_of(["fly", "volumes", "list", "-a", SOURCE_DB, "--json"], "volumes")
        if not isinstance(vols, list) or len(vols) != 1:
            raise Stop(f"{SOURCE_DB} has {len(vols) if isinstance(vols, list) else '?'} volumes")
        vol = vols[0]
        snaps = self.json_of(
            ["fly", "volumes", "snapshots", "list", vol["id"], "-a", SOURCE_DB, "--json"],
            "snapshots",
        )
        snap = newest_snapshot(snaps if isinstance(snaps, list) else [])
        if snap is None:
            raise Stop(f"no snapshot listed for {vol['id']}")
        made = snap.get("created_at") or snap.get("CreatedAt")
        self.note(f"source volume {vol['id']} ({vol.get('size_gb')} GB)")
        self.note(f"newest snapshot {snap['id']} created {made} (the loss window starts here)")
        image = image_ref(
            self.json_of(["fly", "image", "show", "-a", SOURCE_APP, "--json"], "image")
        )
        if image is None:
            raise Stop("couldn't read one image for beta from `fly image show --json`")
        self.note(f"copy runs beta's image {image}")
        apps = self.json_of(["fly", "apps", "list", "--json"], "apps list")
        taken = {a.get("Name") or a.get("name") for a in apps if isinstance(a, dict)}
        clash = [n for k, n in self.n.items() if k != "network" and n in taken]
        if clash:
            raise Stop(f"an app named {clash[0]} already exists; nothing was created")
        return {"snapshot": snap["id"], "size": str(vol.get("size_gb") or 1), "image": image}

    # --- step 2: the copy, on its own network ---------------------------------------
    def create(self, src: Dict[str, str], key: str) -> None:
        n, org, region = self.n, self.org, self.region
        self.attempted.append(n["db"])
        made = self.must(
            ["fly", "postgres", "create", "--name", n["db"], "--org", org, "--region", region,
             "--network", n["network"], "--snapshot-id", src["snapshot"],
             "--initial-cluster-size", "1", "--vm-size", "shared-cpu-1x",
             "--volume-size", src["size"]],
            "postgres create from the snapshot",
        )  # fmt: skip
        found = _PASSWORD.search(made)
        if not found:
            raise Stop("the create printed no superuser password; the copy can't be reached")
        db_password = found.group(1)
        self.held.append(db_password)
        self.note(f"created {n['db']} from {src['snapshot']} on network {n['network']}")

        self.attempted.append(n["redis"])
        self.must(
            ["fly", "apps", "create", n["redis"], "--org", org, "--network", n["network"]],
            "redis app create",
        )
        self.must(
            ["fly", "machine", "run", REDIS_IMAGE, "redis-server", "--bind", "::",
             "--protected-mode", "no", "-a", n["redis"], "--region", region,
             "--vm-size", "shared-cpu-1x"],
            "redis machine run",
        )  # fmt: skip
        self.note(f"created {n['redis']} (throwaway Redis, no outside address)")

        self.attempted.append(n["app"])
        self.must(
            ["fly", "apps", "create", n["app"], "--org", org, "--network", n["network"]],
            "copy app create",
        )
        jwt = secrets.token_urlsafe(48)
        self.held.append(jwt)
        allow = {
            "DATABASE_URL": (
                f"postgres://postgres:{db_password}@{n['db']}.flycast:5432/piper_morgan"
                "?sslmode=disable"
            ),
            "ENCRYPTION_MASTER_KEY": key,
            "JWT_SECRET_KEY": jwt,
            "REDIS_URL": f"redis://{n['redis']}.internal:6379/0",
            "PIPER_CREDENTIAL_STORE": "db",
        }
        self.held.append(allow["DATABASE_URL"])
        self.must(
            ["fly", "secrets", "import", "-a", n["app"], "--stage"],
            "secrets import",
            stdin=secrets_stdin(allow),
        )
        self.note("copy secrets set (names only): " + ", ".join(allow))
        env = {
            "PIPER_ENVIRONMENT": "production",
            "PIPER_HOST": "0.0.0.0",  # noqa: S104 - inside the copy's machine
            "PORT": "8001",
            "PYTHONPATH": "/app",
            "LOG_LEVEL": "WARNING",
            "AUTH_ENABLED": "true",
            "ENABLE_ETHICS_ENFORCEMENT": "true",
            DRILL_COPY_ENV: "yes",
        }
        argv = ["fly", "machine", "run", src["image"], "-a", n["app"], "--region", region,
                "--vm-size", "shared-cpu-1x", "--vm-memory", "1024", "--restart", "no"]  # fmt: skip
        for k, v in env.items():
            argv += ["-e", f"{k}={v}"]
        self.must(argv, "copy machine run")
        self.note(f"created {n['app']} (beta's image; no public address)")

    # --- the proofs ------------------------------------------------------------------
    def proof_1(self, who: str, password: str, started: float, wait_s: float = 600) -> None:
        base = f"http://127.0.0.1:{LOCAL_PORT}"
        self.proxy = self.proxy_factory(self.n["app"])
        self.proxy.start()
        deadline = self.clock() + wait_s
        status: int = 0
        while self.clock() < deadline:
            status, body = self.request("GET", f"{base}/health", None, None)
            if status == 200:
                break
            self.sleep(10)
        if status != 200:
            self.passed["1"] = False
            raise Stop(f"the copy's /health didn't answer 200 within {wait_s:.0f} s")
        status, body = self.request(
            "POST", f"{base}/api/v1/auth/login", {"username": who, "password": password}, None
        )
        token = body.get("token") if status == 200 else None
        if token:
            self.held.append(token)
        me, _ = self.request("GET", f"{base}/api/v1/auth/me", None, token) if token else (0, {})
        self.passed["1"] = me == 200
        elapsed = self.clock() - started
        self.note(
            f"PROOF 1 {'PASS' if me == 200 else 'FAIL'}: sign-in {status}, signed-in request "
            f"{me}; {elapsed / 60:.1f} min from the start of the create"
        )

    def proof_2(self) -> None:
        code, output = self.call(["fly", "ssh", "console", "-a", self.n["app"], "-C", PROOF_2])
        words = [w for w in output.split() if w == "ok" or w.startswith("fail:")]
        word = words[-1] if words else f"no word (exit {code}; image may predate the drill flag)"
        self.passed["2"] = word == "ok"
        self.note(f"PROOF 2 {'PASS' if word == 'ok' else 'FAIL'}: stored key decrypts: {word}")

    # --- proof 5: always ---------------------------------------------------------------
    def cleanup(self) -> None:
        if self.proxy is not None:
            self.proxy.stop()
        made = list(dict.fromkeys(self.attempted))
        if not made:
            return
        if self.keep:
            self.note("--keep: NOT destroyed. Destroy by hand today: " + ", ".join(made))
            self.out(f"REMINDER: {', '.join(made)} hold a copy of everyone's data.")
            return
        for app in made:
            code, output = self.call(["fly", "volumes", "list", "-a", app, "--json"])
            vols = _loads(output) if code == 0 else []
            count = 0
            for vol in vols if isinstance(vols, list) else []:
                c, o = self.call(["fly", "volumes", "snapshots", "list", vol.get("id", ""),
                                  "-a", app, "--json"])  # fmt: skip
                listed = _loads(o) if c == 0 else []
                count += len(listed) if isinstance(listed, list) else 0
            code, _ = self.call(["fly", "apps", "destroy", app, "--yes"])
            self.note(f"destroy {app}: exit {code}; its volume snapshots before: {count}")
        code, output = self.call(["fly", "apps", "list", "--json"])
        listed = _loads(output) if code == 0 else None
        if not isinstance(listed, list):
            self.note("PROOF 5 FAIL: the app listing couldn't be read; check by hand")
            return
        left = [a for a in made if a in {x.get("Name") or x.get("name") for x in listed}]
        self.listing_clean = not left
        self.passed["5"] = not left
        self.note(
            "PROOF 5 PASS: apps listing shows none of " + ", ".join(made)
            if not left
            else "PROOF 5 FAIL: still listed: " + ", ".join(left)
        )

    def run_all(self) -> None:
        src = self.preflight()
        self.out("")
        self.out(f"The copy will be {self.n['app']} (+ -db, -redis). It holds EVERYONE's data.")
        typed = self.confirm(f"Type {self.n['app']} to go on: ").strip()
        if typed != self.n["app"]:
            raise Stop("the name didn't match; nothing was created")
        key, who, password = self.values()
        self.held += [key, password]
        started = self.clock()
        self.note("drill started")
        try:
            self.create(src, key)
            self.proof_1(who, password, started)
            self.proof_2()
            self.note("PROOF 3 NOT RUN: the deletion record (#2158) isn't built")
            self.note("PROOF 4: xian's statement (who held the restore, where its log is)")
        finally:
            self.cleanup()

    def result(self) -> str:
        if all(self.passed.get(k) for k in ("1", "2", "3", "5")) and self.listing_clean:
            return "DONE"
        if all(self.passed.get(k) for k in ("1", "2", "5")):
            return "PROOFS 1, 2, 5 PASSED; proof 3 waits on #2158, proof 4 is xian's"
        return "NOT FINISHED"


def _loads(text: str):
    try:
        return json.loads(text)
    except ValueError:
        return None


def has_terminal() -> bool:
    try:
        return bool(sys.stdin.isatty())
    except (AttributeError, ValueError):
        return False


def main(
    argv: Optional[List[str]] = None,
    drill: Optional[Drill] = None,
    terminal: Callable[[], bool] = has_terminal,
) -> int:
    p = argparse.ArgumentParser(description="#2157's restore drill as one command")
    p.add_argument("--org", required=True, help="the Fly org slug that owns piper-morgan-db")
    p.add_argument("--region", default="sjc")
    p.add_argument("--keep", action="store_true", help="don't destroy the copy (prints names)")
    ns = p.parse_args(argv)
    # Section 10 rule 8: before any check, so a prompt that might echo is never reached.
    if not terminal():
        print(NO_TERMINAL)
        return 2
    d = drill or Drill(org=ns.org, region=ns.region, keep=ns.keep)
    code = 0
    try:
        d.run_all()
    except Stop as e:
        d.note(f"STOPPED: {e}")
        code = 1
    except KeyboardInterrupt:
        d.note("STOPPED: interrupted")
        code = 1
    except Exception as e:  # noqa: BLE001 - the block must print
        d.note(f"STOPPED: unexpected {type(e).__name__}")  # the type only, never the text
        code = 1
    d.out("")
    d.out(BLOCK_START)
    d.out(scrub("\n".join(d.lines), d.held))
    d.out("RESULT: " + d.result())
    d.out(BLOCK_END)
    return code if d.result() != "NOT FINISHED" or code else 1


if __name__ == "__main__":
    raise SystemExit(main())
