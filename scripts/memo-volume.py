#!/usr/bin/env python3
"""Memos per day and words per memo, by sending seat (R16's week of measurement, xian 2026-11-03).
Usage: memo-volume.py SINCE UNTIL     dates YYYY-MM-DD, Pacific, UNTIL exclusive
v3: every memo file a non-merge commit on origin/main added under mailboxes/<role>/inbox/, counted
once per filename (cc copies share it), sender from its `from:` line (else the filename),
words from its body.
v4: every non-canary message in the mail repo (mail4.py's REPO) whose sent_at is in the window.
Exit codes: 0 measured; 3 could not measure v4 (the v3 table still prints, marked partial).
Concept: dev/2026/11/03/methodology-audit-2026-11-03.md
"""

import collections
import datetime as dt
import importlib.util
import statistics
import subprocess
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

PT = ZoneInfo("America/Los_Angeles")


def seat(frm):
    return str(frm or "?").strip().split()[0].strip("\"'").lower()


def body_words(text):
    if text.startswith("---\n"):
        text = text[4:].partition("\n---\n")[2]
    return len(text.split())


def v3(since, until):
    log = subprocess.run(
        [
            "git",
            "log",
            "origin/main",
            "--no-merges",
            "--diff-filter=A",
            "--name-only",
            f"--since={since.isoformat()}",
            f"--until={until.isoformat()}",
            "--format=@@%H %ct",
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    seen, out, sha, day = set(), [], None, None
    for line in log.splitlines():
        if line.startswith("@@"):
            sha, ts = line[2:].split()
            day = dt.datetime.fromtimestamp(int(ts), PT).date()
            continue
        parts = line.split("/")
        if (
            len(parts) != 4
            or parts[0] != "mailboxes"
            or parts[2] != "inbox"
            or not line.endswith(".md")
        ):
            continue
        if parts[3] == "MANIFEST.md" or parts[3] in seen:
            continue
        seen.add(parts[3])
        text = subprocess.run(
            ["git", "show", f"{sha}:{line}"], capture_output=True, text=True
        ).stdout
        # A memo with no front matter (Docs' day-closed nudges) is named "<sender>-to-<recipient>-..."
        frm = parts[3].split("-to-")[0].split("-")[-1]
        frm = next((ln[5:] for ln in text.splitlines()[:12] if ln.startswith("from:")), frm)
        out.append((seat(frm), day, body_words(text)))
    return out


def v4(since, until):
    spec = importlib.util.spec_from_file_location("mail4", Path(__file__).with_name("mail4.py"))
    m4 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m4)
    out = []
    for m in m4.all_messages(m4.fetch_tip()):
        if m.get("type") == "canary" or not m.get("sent_at"):
            continue
        t = dt.datetime.fromisoformat(str(m["sent_at"])).astimezone(PT)
        if since <= t < until:
            out.append((seat(m.get("from")), t.date(), len(m["_body"].split())))
    return out


def report(name, rows, days):
    print(f"\n{name}: {len(rows)} memos over {days} days")
    by = collections.defaultdict(list)
    for s, _, w in rows:
        by[s].append(w)
    print(f"  {'seat':<8}{'memos':>6}{'per day':>9}{'median words':>14}{'total words':>13}")
    for s, ws in sorted(by.items(), key=lambda kv: -len(kv[1])):
        print(
            f"  {s:<8}{len(ws):>6}{len(ws) / days:>9.1f}{statistics.median(ws):>14.0f}{sum(ws):>13}"
        )
    perday = collections.Counter(d for _, d, _ in rows)
    print("  by day: " + ", ".join(f"{d:%m-%d} {n}" for d, n in sorted(perday.items())))


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    since, until = (dt.datetime.fromisoformat(a).replace(tzinfo=PT) for a in sys.argv[1:])
    days = (until - since).days
    subprocess.run(["git", "fetch", "-q", "origin", "main"], check=True)
    report("v3 (mailboxes/)", v3(since, until), days)
    try:
        report("v4 (mail repo)", v4(since, until), days)
    except Exception as e:  # mail4 raises Unmeasured on a missing clone or a failed fetch
        print(f"\nv4: UNMEASURED ({e}); the v3 table above is partial")
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
