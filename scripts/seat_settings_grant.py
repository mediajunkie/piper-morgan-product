#!/usr/bin/env python3
"""seat_settings_grant.py: xian's one-time grants to a seat, through Claude Code's own settings (ADR-084).

Run by xian in Terminal, never by a seat (auto mode refuses a seat a settings edit, and that is
right). It edits one file, the seat's git-ignored ``.claude/settings.local.json``:

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
from another seat. ``fleet-deny`` adds two home-path denies to the settings file all PM seats
share, to close that. Their pattern form is untested until the first sitting, which is why both
are tested by a Read before any key exists.

A seat checks that the key reached its session with no file read at all:

    scripts/seat_settings_grant.py check-env --name PIPER_SEAT_ANTHROPIC_KEY

Nothing here removes or loosens a deny. ``add-allow`` adds one exact ``Bash(...)`` rule and refuses a
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
import stat
import sys
import tempfile
from pathlib import Path

WORKTREES = Path.home() / "Development" / "piper-morgan-worktrees"
SELF_DENY = "Read(**/.claude/settings.local.json)"
SHARED_SETTINGS = Path.home() / ".claude-pm" / "settings.json"
# The self-deny covers a seat's own file only: a ``**/`` deny is not applied outside the seat's
# worktree (probe, 2026-11-15). These two name the paths from the home folder, in the one settings
# file every PM seat shares, so no seat's Read tool opens another seat's settings file or .env
# (Arch's ruling, 2026-11-15). A deny stops the Read tool; a file read by a command a seat runs is
# still the classifier's to judge.
FLEET_DENIES = (
    "Read(~/Development/piper-morgan-worktrees/*/.claude/settings.local.json)",
    "Read(~/Development/piper-morgan-worktrees/*/.env)",
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
    if not path.exists():
        raise SystemExit(f"{path} does not exist; nothing was changed")
    data = load(path)
    deny = data.setdefault("permissions", {}).setdefault("deny", [])
    added = [rule for rule in FLEET_DENIES if rule not in deny]
    if added:
        deny.extend(added)
        save(
            path, data, mode=stat.S_IMODE(path.stat().st_mode)
        )  # the shared file keeps its own mode
    return added


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
    lines.append(f"self-deny present: {SELF_DENY in perms.get('deny', [])}")
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=WORKTREES, help=argparse.SUPPRESS)
    sub = parser.add_subparsers(dest="cmd", required=True)
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

    if args.cmd == "fleet-deny":
        added = fleet_deny(args.shared_settings)
        print(f"shared settings: {args.shared_settings}")
        print(
            f"added {len(added)} deny rule(s); {len(FLEET_DENIES) - len(added)} were already there. No allow, env or other rule was changed."
        )
        print(
            "Next: one seat tries to Read ANOTHER seat's settings file by its full path. It should be refused."
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
