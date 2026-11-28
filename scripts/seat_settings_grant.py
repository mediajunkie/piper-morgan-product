#!/usr/bin/env python3
"""seat_settings_grant.py: xian's one-time grants to a seat, through Claude Code's own settings (ADR-084).

Run by xian in Terminal, never by a seat (auto mode refuses a seat a settings edit, and that is
right). It edits one file, the seat's git-ignored ``.claude/settings.local.json``:

    scripts/seat_settings_grant.py grant-key --seat lead --name PIPER_SEAT_ANTHROPIC_KEY   # all of Step A

The single steps, for a repair or a second seat:

    scripts/seat_settings_grant.py fleet-deny
    scripts/seat_settings_grant.py prepare   --seat lead
    scripts/seat_settings_grant.py add-key   --seat lead --name PIPER_SEAT_ANTHROPIC_KEY
    scripts/seat_settings_grant.py add-allow --seat web  --rule 'Bash(venv/bin/python scripts/seat_session.py --account seat-plain)'
    scripts/seat_settings_grant.py show      --seat lead
    scripts/seat_settings_grant.py remove-key --seat lead --name PIPER_SEAT_ANTHROPIC_KEY

``add-key`` asks for the value at a hidden prompt. The value is never an argument, never printed
and never logged; the script prints its length and the first 8 characters of its SHA-256 so two
people can agree it is the same key without either seeing it. It then sets the file to mode 0600
and adds a Read deny for the file to itself, so the seat's Read tool can't open it (ADR-084 D2).

``prepare`` does the mode and the deny with no key, so the seat can try to Read the file and be
refused before anything real is in it. The deny is honoured for a file inside the seat's own
worktree (tested 2026-11-15 with a dummy ``.env`` against the fleet's ``Read(**/.env)``); the same
form did NOT stop a Read of a file outside the worktree, so it does not protect one seat's file
from another seat. ``fleet-deny`` adds home-path denies to the settings file all PM seats
share, to close that: the two worktree paths (form tested at Step A, 2026-11-20, three Reads refused)
since 2026-11-22, the ``~/.piper-shared`` credential, token and secret names (refusals read 11-26), and
since 2026-11-27, Bash denies for every ``fly`` and ``flyctl`` command (ADR-084: no seat runs ``fly``;
form untested until a seat's ``fly version`` is refused). Running it
again adds only the rules not yet there, keeps the first ``.before-fleet-deny`` copy, and writes a
copy of its own (``.before-fleet-deny.<YYYYMMDD-HHMMSS>``), so the undo it prints reverts that run only.

A seat checks that the key reached its session with no file read at all:

    scripts/seat_settings_grant.py check-env --name PIPER_SEAT_ANTHROPIC_KEY

Nothing here removes or loosens a deny. ``fleet-deny`` removes only the exact allows in
``RETIRED_ALLOWS``, each one already dead under a fleet deny. ``add-allow`` adds one exact ``Bash(...)`` rule and refuses a
wildcard or any other tool. ``check-env`` reads ``PIPER_SEAT_`` names only.

Owner:   CIO
Review:  2026-12-29 (with the methodology audit), or when ADR-084 is accepted or dropped
Concept: docs/internal/operations/adr-084-one-time-steps.md
"""

from __future__ import annotations

import argparse
import getpass
import hashlib
import json
import os
import re
import shutil
import stat
import sys
import tempfile
import time
from pathlib import Path

WORKTREES = Path.home() / "Development" / "piper-morgan-worktrees"
SELF_DENY = "Read(**/.claude/settings.local.json)"
SHARED_SETTINGS = Path.home() / ".claude-pm" / "settings.json"
# The self-deny covers a seat's own file only: a ``**/`` deny is not applied outside the seat's
# worktree (probe, 2026-11-15). These two name the paths from the home folder, in the one settings
# file every PM seat shares, so no seat's Read tool opens another seat's settings file or .env
# (Arch's ruling, 2026-11-15). A deny stops the Read tool; a file read by a command a seat runs is
# still the classifier's to judge.
# The ~/.piper-shared names below were each seat's own deny until 2026-11-22, when Web's seat read a
# file inside its own browser profile folder (`seat-browser-credential-profile-web`) and was not
# refused, while CIO's seat was refused on the same file. A deny that lives only in a seat's own
# git-ignored settings is missing from any seat nobody set it in. Here they cover every PM seat.
# They match a file or a folder by name, and the `/**` forms cover what is inside a matched folder.

# No seat runs `fly` (ADR-084 line 22; production reads and secret changes are xian's). Until
# 2026-11-27 nothing on a seat enforced it: PA's seat ran `fly releases` and `fly status` against the
# MCP app while `fly secrets list` was refused (HOST 01M8FZGA3P, Exec 01M8G038V2). These deny every
# `fly` and `flyctl` command a seat types, by the bare name, the Homebrew path (`command -v` on Amber,
# 11-27: /opt/homebrew/bin/fly and flyctl; there is no ~/.fly/bin), the `env` and `command`
# prefixes, and a leading `FLY_…=` assignment (the shape a token would arrive in, HOST 01M8G0GFRB). A deny matches what a seat types, not what a script runs inside it
# (Pard, 10-13): Pard's cycle-check arm and the GitHub Actions jobs are not affected. Not covered:
# an assignment to any other variable (`X=1 fly ...`), or a path other than Homebrew's; those are the
# classifier's. There
# is no `*/fly *` form: a leading `*` matches inside any command, so a grep or a log heredoc that
# mentions `bin/fly ` would be refused.
FLY_DENIES = tuple(
    f"Bash({form})"
    for name in ("fly", "flyctl")
    for form in (
        name,
        f"{name} *",
        f"/opt/homebrew/bin/{name}",
        f"/opt/homebrew/bin/{name} *",
        f"env {name} *",
        f"env * {name} *",
        f"command {name} *",
        f"FLY_* {name} *",
    )
)
FLEET_DENIES = (
    "Read(~/Development/piper-morgan-worktrees/*/.claude/settings.local.json)",
    "Read(~/Development/piper-morgan-worktrees/*/.env)",
    "Read(~/.piper-shared/*credential*)",
    "Read(~/.piper-shared/*credential*/**)",
    "Read(~/.piper-shared/*token*)",
    "Read(~/.piper-shared/*token*/**)",
    "Read(~/.piper-shared/*secret*)",
    "Read(~/.piper-shared/*secret*/**)",
    *FLY_DENIES,
)
# Allows in the shared file that a fleet deny has made dead, removed by ``fleet-deny`` so the file
# does not carry a grant nobody can use (Arch 01M8G0QQYT, 2026-11-27). Exact strings only: removing
# one can only take access away. The live-set read below let every PM seat print a production
# secret's value; ADR-084 makes that xian's, and Arch's rulings read the deletion gate's mirror
# (`CURRENT_LIVE_CATEGORIES`) instead.
RETIRED_ALLOWS = (
    "Bash(fly ssh console -a piper-morgan -C 'printenv PIPER_INVERSION_LIVE_CATEGORIES')",
)
NAME_RE = re.compile(r"^PIPER_SEAT_[A-Z0-9_]+$")
SEAT_RE = re.compile(r"^[a-z][a-z0-9-]*$")


def fingerprint(value: str) -> str:
    """Length and a short hash: enough to compare two copies, useless for recovering the value."""
    return f"{len(value)} chars, sha256 {hashlib.sha256(value.encode()).hexdigest()[:8]}"


def settings_path(seat: str, root: Path) -> Path:
    if not SEAT_RE.match(seat):
        raise SystemExit(f"seat name {seat!r} is not a plain role slug")
    path = root / seat / ".claude" / "settings.local.json"
    if not path.parent.is_dir():
        raise SystemExit(f"no .claude folder at {path.parent}; is {seat!r} a seat on this machine?")
    return path


def load(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path} is not valid JSON ({exc}); nothing was changed") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"{path} does not hold a JSON object; nothing was changed")
    return data


def save(path: Path, data: dict, mode: int = stat.S_IRUSR | stat.S_IWUSR) -> None:
    """Write whole, at ``mode`` (0600 unless told), by rename, so a failure leaves the old file."""
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".settings.", suffix=".tmp")
    try:
        os.fchmod(fd, mode)
        with os.fdopen(fd, "w") as handle:
            json.dump(data, handle, indent=2)
            handle.write("\n")
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    os.chmod(path, mode)


def fleet_deny(path: Path) -> list[str]:
    """Add the home-path denies to the shared settings file. Additive: nothing else is changed."""
    return fleet_deny_run(path)[0]


def fleet_deny_run(path: Path) -> tuple[list[str], Path | None]:
    """``fleet_deny``, also returning the copy that undoes this run alone (None when nothing was added)."""
    added, _retired, backup = fleet_deny_change(path)
    return added, backup


def fleet_deny_change(path: Path) -> tuple[list[str], list[str], Path | None]:
    """Add the fleet denies and drop the retired allows. Returns (added, retired, undo copy)."""
    if not path.exists():
        raise SystemExit(f"{path} does not exist; nothing was changed")
    data = load(path)
    perms = data.setdefault("permissions", {})
    deny = perms.setdefault("deny", [])
    added = [rule for rule in FLEET_DENIES if rule not in deny]
    retired = [rule for rule in perms.get("allow", []) if rule in RETIRED_ALLOWS]
    backup = None
    if added or retired:
        # Arch, 2026-11-15: this rewrites the one file every seat's session depends on, so keep the
        # file as it was beside it. The undo is then one `mv`. An earlier copy is never overwritten:
        # the first one is the true "before". Arch, 2026-11-22: a later run keeps its own copy too,
        # so the undo it prints reverts that run only, not Step A's denies or edits made since.
        backup = path.with_name(path.name + ".before-fleet-deny")
        if backup.exists():
            stamp = time.strftime("%Y%m%d-%H%M%S")
            backup = path.with_name(f"{path.name}.before-fleet-deny.{stamp}")
            n = 1
            while backup.exists():
                n += 1
                backup = path.with_name(f"{path.name}.before-fleet-deny.{stamp}-{n}")
        shutil.copy2(path, backup)
        deny.extend(added)
        if retired:
            perms["allow"] = [rule for rule in perms["allow"] if rule not in RETIRED_ALLOWS]
        save(path, data, mode=stat.S_IMODE(path.stat().st_mode))  # the shared file keeps its mode
    return added, retired, backup


def add_key(data: dict, name: str, value: str) -> dict:
    if not NAME_RE.match(name):
        raise SystemExit(
            f"{name!r} is not a PIPER_SEAT_ name; a seat key never uses a provider's own variable name"
        )
    if not value or value != value.strip() or any(ch.isspace() for ch in value):
        raise SystemExit("the value is empty or has whitespace in it; nothing was changed")
    data.setdefault("env", {})[name] = value
    deny = data.setdefault("permissions", {}).setdefault("deny", [])
    if SELF_DENY not in deny:
        deny.append(SELF_DENY)
    return data


def remove_key(data: dict, name: str) -> bool:
    env = data.get("env") or {}
    if name not in env:
        return False
    del env[name]
    if not env:
        data.pop("env", None)
    return True


def add_allow(data: dict, rule: str) -> bool:
    if not re.match(r"^Bash\(.+\)$", rule):
        raise SystemExit(
            "this script adds exact Bash(command) allows only, for example Bash(scripts/foo.py --account bar); any other grant is a hand edit by xian"
        )
    if "*" in rule:
        raise SystemExit("this script adds exact rules only; a rule with * in it is refused")
    allow = data.setdefault("permissions", {}).setdefault("allow", [])
    if rule in allow:
        return False
    allow.append(rule)
    return True


def show(path: Path, data: dict) -> list[str]:
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else None
    lines = [f"file: {path}", f"mode: {oct(mode) if mode is not None else 'absent'}"]
    for name, value in sorted((data.get("env") or {}).items()):
        shown = (
            fingerprint(value) if name.startswith("PIPER_SEAT_") else "(not a seat key; not read)"
        )
        lines.append(f"env: {name}: {shown}")
    perms = data.get("permissions") or {}
    lines.append(
        f"allow: {len(perms.get('allow', []))} rules; deny: {len(perms.get('deny', []))} rules"
    )
    # The self-deny is added with a seat key (add-key, grant-key, prepare), never by add-allow, so a
    # file that never held a key reads False, and that is correct (Exec 01M8CJW0EX, 2026-11-26: Web's
    # and CIO's files read False while Lead's read True). Say which case it is, so a False doesn't
    # read as a fault.
    if SELF_DENY in perms.get("deny", []):
        lines.append("self-deny present: True")
    elif any(name.startswith("PIPER_SEAT_") for name in (data.get("env") or {})):
        lines.append(
            "self-deny present: False. MISSING: this file holds a seat key; run prepare for this seat"
        )
    else:
        lines.append(
            "self-deny present: False (not needed: no seat key in this file; added with the first key)"
        )
    return lines


def is_terminal() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()


def grant_key(seat: str, name: str, root: Path, shared: Path) -> int:
    """Step A of ADR-084 as ONE command (Exec, 2026-11-15): denies first, a wait while seats test
    them, and the key only after xian confirms every Read was refused. Stops at the first failure."""
    if not NAME_RE.match(name):
        raise SystemExit(f"{name!r} is not a PIPER_SEAT_ name; nothing was changed")
    if not is_terminal():
        raise SystemExit(
            "grant-key asks questions and takes a key at a hidden prompt; run it in a terminal. Nothing was changed."
        )
    path = settings_path(seat, root)
    load(path)  # refuse a broken seat file before touching the shared one

    print("1 of 4. The shared settings file (every PM seat reads it).")
    added, backup = fleet_deny_run(shared)
    print(
        f"   added {len(added)} deny rule(s); {len(FLEET_DENIES) - len(added)} were already there."
    )
    if added:
        print(f"   the file as it was is kept at: {backup}")
        print(f"   to undo this step: mv '{backup}' '{shared}'")

    print(f"2 of 4. Seat {seat}'s own settings file.")
    data = load(path)
    deny = data.setdefault("permissions", {}).setdefault("deny", [])
    if SELF_DENY not in deny:
        deny.append(SELF_DENY)
    save(path, data)
    print("   mode 0600; the seat's own Read deny is in place; no key is in the file.")

    print("3 of 4. Three Read tests, with no key anywhere. Tell Exec this line is on your screen:")
    print(f"   WAITING FOR READ TESTS on seat {seat}")
    print(f"   a. {seat} tries to Read its own settings file: {path}")
    print(f"   b. HOST tries to Read that same file by its full path.")
    print("   c. HOST tries to Read a made-up .env that CIO places at the top of the CIO worktree.")
    print("   Each must be REFUSED. If a seat needs a restart to pick up the new rules, do it now;")
    print("   this command will wait.")
    print(
        "   You can also stop here (Return) and run this same line again later; done parts are skipped."
    )
    answer = input(
        "   Type the three results as Exec gives them, in order a b c (for example: refused refused refused): "
    )
    # HOST, 2026-11-15: a bare Return or one word would let it through without anyone reading the
    # results. All three, each exactly "refused", or it stops before the key.
    if answer.strip().lower().split() != ["refused", "refused", "refused"]:
        print("Stopped before any key. The deny rules stay in place (they only add protection).")
        print("Nothing secret was written. Tell Exec what the seats reported.")
        return 2

    print("4 of 4. The key.")
    value = getpass.getpass(f"   {name} for seat {seat} (input hidden): ")
    save(path, add_key(load(path), name, value))
    print(f"   stored {name}: {fingerprint(value)}")
    print(
        f"Done. {seat}'s check, after its next session start: scripts/seat_settings_grant.py check-env --name {name}"
    )
    for line in show(path, load(path)):
        print(line)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=WORKTREES, help=argparse.SUPPRESS)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("grant-key")
    p.add_argument("--seat", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--shared-settings", type=Path, default=SHARED_SETTINGS, help=argparse.SUPPRESS)
    for cmd in ("add-key", "remove-key"):
        p = sub.add_parser(cmd)
        p.add_argument("--seat", required=True)
        p.add_argument("--name", required=True)
    p = sub.add_parser("add-allow")
    p.add_argument("--seat", required=True)
    p.add_argument("--rule", required=True)
    for cmd in ("show", "prepare"):
        p = sub.add_parser(cmd)
        p.add_argument("--seat", required=True)
    p = sub.add_parser("fleet-deny")
    p.add_argument("--shared-settings", type=Path, default=SHARED_SETTINGS, help=argparse.SUPPRESS)
    p = sub.add_parser("check-env")
    p.add_argument("--name", required=True)
    args = parser.parse_args(argv)

    if args.cmd == "check-env":
        if not NAME_RE.match(args.name):
            # Arch, 2026-11-15: a fingerprint of anything else is not this tool's business, and for
            # a short or guessable value it would let someone test guesses.
            raise SystemExit(
                f"{args.name!r} is not a PIPER_SEAT_ name; check-env reads seat keys only"
            )
        value = os.environ.get(args.name, "")
        print(f"{args.name}: {'set, ' + fingerprint(value) if value else 'UNSET in this session'}")
        return 0 if value else 1

    if args.cmd == "grant-key":
        return grant_key(args.seat, args.name, args.root, args.shared_settings)

    if args.cmd == "fleet-deny":
        added, retired, backup = fleet_deny_change(args.shared_settings)
        print(f"shared settings: {args.shared_settings}")
        if backup:
            print(f"the file as it was before this run is kept at: {backup}")
            print(f"to undo: mv '{backup}' '{args.shared_settings}'")
        print(
            f"added {len(added)} deny rule(s); {len(FLEET_DENIES) - len(added)} were already there."
            f" removed {len(retired)} retired allow rule(s). No other allow, env or rule was changed."
        )
        print(
            "Next: one seat tries to Read ANOTHER seat's settings file by its full path, and Web tries to Read"
            " a file inside ~/.piper-shared/seat-browser-credential-profile-web. Both should be refused."
            " For the fly denies: a seat types `fly version`, then `/opt/homebrew/bin/flyctl version`;"
            " both should be refused before they run."
        )
        return 0

    path = settings_path(args.seat, args.root)
    data = load(path)
    if args.cmd == "prepare":
        # Lead, 2026-11-15: put the deny in place and test it BEFORE any key is in the file, so a
        # deny that doesn't hold shows nothing real.
        deny = data.setdefault("permissions", {}).setdefault("deny", [])
        if SELF_DENY not in deny:
            deny.append(SELF_DENY)
        save(path, data)
        print(
            f"seat {args.seat}: file set to mode 0600; Read deny for the file is in place; no key was added."
        )
        print(
            "Next: the seat tries to Read this file with its Read tool. It should be refused. Only then run add-key."
        )
    elif args.cmd == "add-key":
        value = getpass.getpass(f"{args.name} for seat {args.seat} (input hidden): ")
        save(path, add_key(data, args.name, value))
        print(f"stored {args.name}: {fingerprint(value)}")
        print("file set to mode 0600; Read deny for the file added.")
        print(
            f"The seat picks it up at its next session start. Its check: scripts/seat_settings_grant.py check-env --name {args.name}"
        )
    elif args.cmd == "remove-key":
        if remove_key(data, args.name):
            save(path, data)
            print(f"removed {args.name} from seat {args.seat}")
        else:
            print(f"{args.name} was not set for seat {args.seat}; nothing changed")
    elif args.cmd == "add-allow":
        if add_allow(data, args.rule):
            save(path, data)
            print(f"added 1 allow rule for seat {args.seat}")
        else:
            print("that exact rule is already there; nothing changed")
    for line in show(path, load(path)):
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
