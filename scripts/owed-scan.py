#!/usr/bin/env python3
"""owed-scan.py — find open obligations that never reached a dated, tracked row (#1967, Agent 360 v0.5).

The gap: an agent writes "I owe X to Y" in a session log and it never becomes a standing-items row, so
aging-standing-items.sh (which reads those rows) can't see it. A prose rule to "add a dated row" didn't
take (Exec's v0.4 recommendation, unapplied by its own proposer). This scans for ONE determinate marker
instead of free text, because a free-text scan flags "owed item closed" as open and trains people to skip it.

THE MARKER (HOST's proposal, CIO's amendments, 2026-10-09) — one line per open obligation, in a session log,
typically inside the wake's `Drain:` line or right under it:

    OWED[key: <slug>; to: <role-or-person>; by: <YYYY-MM-DD | trigger: <named event>>]: <what, one line>
    OWED-CLOSED[key: <slug>]: <how it closed>

  * key: a short slug, unique per owner (e.g. `mail4-lead-flip`). Matching is by key, never by subject text.
  * by: a date, or `trigger:` plus a named event. "no rush" can't be written in the field (CLAUDE.md's named-trigger rule).
  * The owner is the role in the log's filename (`...-{role}-code-log.md`).

ROW DATES: the row also carries a Filed date in aging-standing-items.sh's form; that script judges the row's
AGE, this one only whether the row EXISTS and whether `by:` (the due date) has passed (Exec's amendment).
PILOT: HOST and Exec, 10-09 to 10-16, then cohort-wide unless false flags say otherwise.

FLAGS (per open OWED, i.e. no later OWED-CLOSED with the same key by the same owner):
  NO-ROW    the owner's dev/active/{role}-standing-items.md or -carry-forward.md has no line containing `key: <slug>`
  OVERDUE   `by:` is a date in the past
  BAD-BY    `by:` is neither a YYYY-MM-DD date nor `trigger: ...`
Free-text "owed" is ignored on purpose, and so is a marker inside inline code (`OWED[...]`, an example). Window: logs from the last --days (default 14).

Always prints its denominator. Exit 0 = no flags; 1 = flags; 3 = nothing scanned (no logs in the window).
Cost: one pass over ~14 days of logs. Benefit: none yet: measuring. Review: 2026-11-20. Owner: CIO (script), HOST (convention).
"""

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

OWED = re.compile(r"(?<!`)OWED\[([^\]]*)\]:\s*(.*)")  # (?<!`): a quoted example is not a marker
CLOSED = re.compile(r"(?<!`)OWED-CLOSED\[([^\]]*)\]")
LOGNAME = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{4}-([a-z0-9]+)-code(?:-[a-z0-9-]+)?-log\.md$")


def fields(s):
    out = {}
    for part in s.split(";"):
        k, _, v = part.partition(":")
        if k.strip():
            out[k.strip().lower()] = v.strip()
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--today", help="YYYY-MM-DD, for tests")
    a = ap.parse_args()
    root = Path(a.root)
    today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
    since = today - dt.timedelta(days=a.days)

    logs = []
    for f in sorted((root / "dev").glob("20[0-9][0-9]/[0-9][0-9]/[0-9][0-9]/*-log.md")):
        m = LOGNAME.match(f.name)
        if not m:
            continue
        try:
            day = dt.date.fromisoformat(f.name[:10])
        except ValueError:
            continue
        if day >= since:
            logs.append((day, f, m.group(1)))
    if not logs:
        print(f"owed-scan: NOT MEASURED — no session logs since {since}")
        return 3

    opened, closed = {}, set()
    for day, f, role in logs:
        for ln in f.read_text(errors="ignore").splitlines():
            for c in CLOSED.finditer(ln):
                k = fields(c.group(1)).get("key")
                if k:
                    closed.add((role, k))
            m = OWED.search(ln.replace("OWED-CLOSED[", "\0"))  # don't read a close as an open
            if m:
                fd = fields(m.group(1))
                key = fd.get("key") or f"(no key) {m.group(2)[:30]}"
                opened[(role, key)] = dict(
                    fd, what=m.group(2).strip(), log=str(f.relative_to(root)), day=day
                )

    flags, open_n = [], 0
    for (role, key), o in sorted(opened.items()):
        if (role, key) in closed:
            continue
        open_n += 1
        by = o.get("by", "")
        rows = ""
        for name in (f"{role}-standing-items.md", f"{role}-carry-forward.md"):
            p = root / "dev" / "active" / name
            if p.exists():
                rows += p.read_text(errors="ignore")
        if not o.get("key") or f"key: {key}" not in rows:
            flags.append(("NO-ROW", role, key, o))
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", by):
            if dt.date.fromisoformat(by) < today:
                flags.append(("OVERDUE", role, key, o))
        elif not by.startswith("trigger:") or len(by) <= len("trigger:") + 1:
            flags.append(("BAD-BY", role, key, o))

    print(
        f"owed-scan · {len(logs)} session logs since {since} · {len(opened)} OWED markers, "
        f"{len(opened) - open_n} closed, {open_n} open · {len(flags)} flags"
    )
    for kind, role, key, o in flags:
        print(
            f"  {kind:8} {role:<6} key={key}  to={o.get('to', '?')} by={o.get('by', '?')}  ({o['log']})  {o['what'][:70]}"
        )
    return 1 if flags else 0


if __name__ == "__main__":
    sys.exit(main())
