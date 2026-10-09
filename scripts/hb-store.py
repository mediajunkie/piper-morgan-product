#!/usr/bin/env python3
"""hb-store.py — reader for the non-git heartbeat store (R3 step 1), plus the git-vs-store parity check.

R3 step 1 (PM-approved 2026-10-04; built 2026-10-08, CIO) moves heartbeats out of git. During the parity
window scripts/duty-cycle-heartbeat.sh writes BOTH: the old git rows/markers (dev/heartbeats/, read by the
freeze checks) and a local store (default ~/.local/state/piper-heartbeats, override PIPER_HB_STORE):
  <store>/YYYY-MM-DD/<role>.tsv     ts, role, fire, source (fire|hook), epoch      (one row per invocation)
  <store>/last-invoked/<role>.txt   ts, fire, source, epoch                        (latest invocation)
The git write stops only after this reader agrees with the git reader on 11/11 roles for 3 consecutive
days (docs/internal/operations/r3-metric.md). Exec runs the parity test; this script is the instrument.

  hb-store.py latest [--role R] [--epoch]   newest store signal per role (or one role's epoch)
  hb-store.py day --role R [--day YYYY-MM-DD]  that day's store rows for a role
  hb-store.py parity [--tolerance-min 10]   per registry role: git newest signal vs store newest signal

Parity semantics (Exec's trap, 10-08: the freeze check uses COMMIT time, not the row's timestamp): the git
side is the newest COMMIT time on origin/main touching dev/heartbeats/*/<role>.tsv or
dev/heartbeats/last-invoked/<role>.txt, the same thing duty-cycle-freeze-check.sh reads. The store side is
the newest store epoch. A role AGREES when the store's newest signal is no older than git's minus the
tolerance (the store records every invocation, git only some, so store >= git is the healthy shape). It
DISAGREES when git shows a signal the store lacks, e.g. a seat still running the pre-store writer.
Always prints its denominator; exit 0 = all roles agree, 1 = some disagree, 3 = could not measure.

Single-host assumption: every seat and the watchdog run on Amber, so one local directory is the store.
Cost: a few local file reads; parity adds ~2 git log calls per role. Benefit: none yet: measuring.
Review: 2026-11-05. Owner: CIO.
"""

import argparse
import datetime as dt
import os
import subprocess
import sys
from pathlib import Path

STORE = Path(os.environ.get("PIPER_HB_STORE", str(Path.home() / ".local/state/piper-heartbeats")))
REGISTRY = "dev/active/duty-cycle-registry.tsv"


def registry_roles():
    r = subprocess.run(
        ["git", "show", f"origin/main:{REGISTRY}"], capture_output=True, text=True, check=False
    )
    if r.returncode != 0:
        return None
    roles = []
    for line in r.stdout.splitlines():
        if not line or line.startswith("#"):
            continue
        role = line.split("\t", 1)[0]
        if role != "role":
            roles.append(role)
    return roles


def store_rows(role, day=None):
    days = [STORE / day] if day else sorted(p for p in STORE.glob("20??-??-??") if p.is_dir())
    out = []
    for d in days:
        f = d / f"{role}.tsv"
        if f.exists():
            for line in f.read_text().splitlines():
                parts = line.split("\t")
                if len(parts) >= 5 and parts[4].isdigit():
                    out.append(parts)
    return out


def store_latest(role):
    best = None
    li = STORE / "last-invoked" / f"{role}.txt"
    if li.exists():
        parts = li.read_text().strip().split("\t")
        if len(parts) >= 4 and parts[3].isdigit():
            best = int(parts[3])
    # Recent days only: the newest signal is in the last few files.
    for d in sorted((p for p in STORE.glob("20??-??-??") if p.is_dir()), reverse=True)[:3]:
        for parts in store_rows(role, d.name):
            ep = int(parts[4])
            best = ep if best is None or ep > best else best
    return best


def git_latest(role):
    r = subprocess.run(
        [
            "git",
            "log",
            "origin/main",
            "-1",
            "--format=%ct",
            "--",
            f"dev/heartbeats/*/{role}.tsv",
            f"dev/heartbeats/last-invoked/{role}.txt",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    s = r.stdout.strip()
    return int(s) if r.returncode == 0 and s.isdigit() else None


def fmt(ep):
    if ep is None:
        return "—"
    return dt.datetime.fromtimestamp(ep).strftime("%m-%d %H:%M")


def cmd_latest(a):
    roles = [a.role] if a.role else (registry_roles() or [])
    if a.epoch and a.role:
        ep = store_latest(a.role)
        print(ep if ep is not None else "NONE")
        return 0 if ep is not None else 1
    print(f"hb-store latest · store {STORE} · {len(roles)} roles")
    for r in roles:
        print(f"  {r:<6} {fmt(store_latest(r))}")
    return 0


def cmd_day(a):
    day = a.day or dt.date.today().isoformat()
    rows = store_rows(a.role, day)
    print(f"hb-store day · {a.role} · {day} · {len(rows)} rows")
    for p in rows:
        print("  " + "\t".join(p[:4]))
    return 0


def cmd_parity(a):
    if not STORE.exists():
        print(f"hb-store parity: NOT MEASURED — no store at {STORE}")
        return 3
    subprocess.run(["git", "fetch", "-q", "origin", "main"], check=False)
    roles = registry_roles()
    if not roles:
        print(f"hb-store parity: NOT MEASURED — {REGISTRY} unreadable on origin/main")
        return 3
    tol = a.tolerance_min * 60
    agree, rows = 0, []
    for r in roles:
        g, s = git_latest(r), store_latest(r)
        if g is None and s is None:
            verdict = "no signal either side"
            ok = True
        elif s is None:
            verdict, ok = "DISAGREE: git has signals, store has none", False
        elif g is None:
            verdict, ok = "store only (git silent)", True
        elif s >= g - tol:
            verdict, ok = "agree", True
        else:
            verdict, ok = f"DISAGREE: store {int((g - s) / 60)} min behind git", False
        agree += ok
        rows.append(f"  {r:<6} git {fmt(g)}  store {fmt(s)}  {verdict}")
    print(
        f"hb-store parity · {agree}/{len(roles)} roles agree (tolerance {a.tolerance_min} min) · "
        f"git = newest commit time on origin/main; store = {STORE}"
    )
    print("\n".join(rows))
    return 0 if agree == len(roles) else 1


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    lt = sub.add_parser("latest")
    lt.add_argument("--role")
    lt.add_argument("--epoch", action="store_true")
    d = sub.add_parser("day")
    d.add_argument("--role", required=True)
    d.add_argument("--day")
    pa = sub.add_parser("parity")
    pa.add_argument("--tolerance-min", type=int, default=10)
    a = p.parse_args()
    return {"latest": cmd_latest, "day": cmd_day, "parity": cmd_parity}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
