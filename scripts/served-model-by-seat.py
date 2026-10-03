#!/usr/bin/env python3
"""Last model each cohort seat was actually SERVED, from the raw transcript ledger.

The Desktop UI and session-log headers show what was REQUESTED; only the
transcript's assistant-message `model` field shows what Anthropic served.
A switch takes effect at a seat's NEXT turn, so "last served" before that turn
says nothing about whether the switch worked -- this prints the time of the
last turn so you can tell "not yet measured" from "did not take"
(Exec's 2026-10-03 retraction: read idle seats as failed switches).

Usage: scripts/served-model-by-seat.py [--since HH:MM]   (local time, today)
"""

import datetime
import glob
import json
import os
import sys

ROOT = os.path.expanduser("~/.claude-pm/projects")
since = None
if "--since" in sys.argv:
    h, m = sys.argv[sys.argv.index("--since") + 1].split(":")
    since = (
        datetime.datetime.now()
        .astimezone()
        .replace(hour=int(h), minute=int(m), second=0, microsecond=0)
    )


def served(path):
    size = os.path.getsize(path)
    with open(path, "rb") as fh:
        fh.seek(max(0, size - 3_000_000))
        lines = fh.read().decode("utf-8", "ignore").splitlines()
    out = []
    for line in lines:
        if '"model"' not in line:
            continue
        try:
            o = json.loads(line)
        except ValueError:
            continue
        m = (o.get("message") or {}).get("model")
        t = o.get("timestamp")
        if m and t and m != "<synthetic>":
            out.append((datetime.datetime.fromisoformat(t.replace("Z", "+00:00")).astimezone(), m))
    return out


print(
    f"{'seat':6} {'last turn':9} {'last served':18} "
    + ("turns since / models since" if since else "")
)
for d in sorted(glob.glob(os.path.join(ROOT, "*piper-morgan-worktrees-*"))):
    seat = d.rsplit("worktrees-", 1)[1]
    files = sorted(glob.glob(os.path.join(d, "*.jsonl")), key=os.path.getmtime)
    rows = served(files[-1]) if files else []
    if not rows:
        print(f"{seat:6} (no served turns found)")
        continue
    t, m = rows[-1]
    extra = ""
    if since:
        after = [r for r in rows if r[0] >= since]
        extra = (
            f"{len(after)}  " + ",".join(sorted({r[1] for r in after}))
            if after
            else "0  (no turn since: UNMEASURED, not failed)"
        )
    print(f"{seat:6} {t.strftime('%a %H:%M'):9} {m:18} {extra}")
