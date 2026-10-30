#!/usr/bin/env python3
"""stamp_check.py — catch a guessed clock time in a memo's `date:` or a session-log heading.

xian, 2026-10-16 (Ship #065 week review, via Exec): "Yes, date-check seems sound." 7 of 10 roles wrote
guessed times in the week of 10-09, and every one had to be corrected. Writing the rule down (duty-cycle-tick
v1.50) wasn't enough, so the tool checks instead. The clock is `America/Los_Angeles` now.

  stamp_check.py --stamp-now PATH... replace a front-matter `date: now` with the clock (mail-send calls this first)
  stamp_check.py --mail PATH...    memos about to be sent (scripts/mail-send.sh calls this)
  stamp_check.py --log-staged      session-log headings in `git diff --cached` (check-branch.sh calls this)

Mail mode looks only at memos that are new: a file whose exact content is already on origin/main (a move
to read/, a triage of someone else's memo) is skipped. For each new memo's front-matter `date:`:
  BLOCK  a time ahead of now by even a minute (since 10-30; it was 5), or an `HH:Mx` form more than
         10 minutes from now
  WARN   an `HH:Mx` or `~HH:MM` form near now (v1.50 bans both; write the minute), a time more than
         30 minutes behind now (drafted earlier? say so), or a date-only stamp that isn't today
`MAIL_STAMP_CHECK=warn` turns every BLOCK into a WARN, for a memo deliberately stamped another time.
Log mode only warns. It looks at added lines in staged `dev/YYYY/MM/DD/*-log.md` files that are `#`
headings carrying a time, and only for today's log: it flags an estimated form or a time ahead of now, not
one behind (a heading can fairly carry the time a wake began). It also reads today's `*(Role, date time`
attributions on added lines of BRIEFING-CURRENT-STATE.md (10-17: the briefing held 7 `HH:Mx` stamps, two
of them CIO's, because it passed through neither mail-send nor a log heading), and today-dated lines added
to decisions.log, both the leading stamp and any `HH:Mx` inside the line (10-19: "recorded by Exec 10:0x").
Stamp-now mode (xian 10-30 via Exec, "make it easier to do such things without having to remember"): a memo
may say `date: now` (or `date: now PT`), and every such file in one call gets the same clock reading, so the
sent mirror and every recipient copy match. A time nobody types can't be a guess.
Exit 0 = nothing blocking; 1 = a BLOCK (mail mode only). Owner: CIO. Review: 2026-12-08.
"""

import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

PT = ZoneInfo("America/Los_Angeles")
AHEAD = timedelta(0)  # 10-30: a legitimate stamp is never in the future (Exec's rec 3, xian's yes)
BEHIND = timedelta(minutes=30)
MX = re.compile(r"\b(\d{1,2}):(\d)[xX]\b")
NEAR = timedelta(minutes=10)
CLOCK = re.compile(r"\b(\d{1,2}):(\d{2})\b")
DAY = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
BRIEFING = "docs/briefing/BRIEFING-CURRENT-STATE.md"
BRIEF_STAMP = re.compile(r"\(\w[\w ]*, (\d{4}-\d{2}-\d{2}) (~?\d{1,2}:\d[\dxX])")
DECISIONS = "docs/internal/architecture/decisions/decisions.log"


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True)


def judge(stamp: str, now: datetime, default_day: str):
    """Return (level, reason) for one stamp, or None if it's fine."""
    d = DAY.search(stamp)
    day = d.group(1) if d else default_day
    rest = stamp[d.end() :] if d else stamp
    m = MX.search(rest)
    if m:
        lo = datetime.strptime(
            f"{day} {int(m.group(1)):02d}:{m.group(2)}0", "%Y-%m-%d %H:%M"
        ).replace(tzinfo=PT)
        hi = lo + timedelta(minutes=9)
        if lo - NEAR <= now <= hi + NEAR:
            return (
                "WARN",
                f"'{stamp.strip()}' is an estimated form (duty-cycle-tick v1.50); write the minute from date",
            )
        return (
            "BLOCK",
            f"'{stamp.strip()}' is an estimated time more than 10 min from now ({now:%H:%M})",
        )
    estimated = "~" in rest
    c = CLOCK.search(rest)
    if not c:
        if d and day != now.strftime("%Y-%m-%d"):
            return "WARN", f"dated {day}, today is {now:%Y-%m-%d}"
        return None
    when = datetime.strptime(f"{day} {int(c.group(1)):02d}:{c.group(2)}", "%Y-%m-%d %H:%M").replace(
        tzinfo=PT
    )
    if when - now > AHEAD:
        return (
            "BLOCK",
            f"{when:%Y-%m-%d %H:%M} is {int((when - now).total_seconds() // 60)} min ahead of now ({now:%H:%M})",
        )
    if now - when > BEHIND:
        return (
            "WARN",
            f"{when:%Y-%m-%d %H:%M} is {int((now - when).total_seconds() // 60)} min behind now ({now:%H:%M})",
        )
    if estimated:
        return (
            "WARN",
            f"'{stamp.strip()}' is an estimated form (duty-cycle-tick v1.50); write the minute from date",
        )
    return None


def front_date(text: str):
    if not text.startswith("---"):
        return None
    fm = text.split("---", 2)[1] if text.count("---") >= 2 else ""
    m = re.search(r"^date:[ \t]*(\S.*)$", fm, re.M)
    return m.group(1).strip().strip("\"'") if m else None


NOW_LINE = re.compile(r"^(date:[ \t]*)[\"']?now(?:[ \t]+PT)?[\"']?[ \t]*$", re.M | re.I)


def stamp_now(paths, now) -> int:
    """Write the clock into every front-matter `date: now`. One reading for all files, so copies match."""
    for p in paths:
        if not os.path.isfile(p):
            continue
        text = open(p, encoding="utf-8").read()
        if not text.startswith("---") or text.count("---") < 2:
            continue
        _, fm, rest = text.split("---", 2)
        new_fm, n = NOW_LINE.subn(lambda m: f"{m.group(1)}{now:%Y-%m-%d %H:%M} PT", fm, count=1)
        if n:
            with open(p, "w", encoding="utf-8") as f:
                f.write(f"---{new_fm}---{rest}")
            print(f"stamp-now: {p}: date: {now:%Y-%m-%d %H:%M} PT", file=sys.stderr)
    return 0


def mail(paths, now) -> int:
    on_main = set()
    r = git("ls-tree", "-r", "origin/main", "mailboxes/")
    for line in r.stdout.splitlines():
        on_main.add(line.split()[2])
    soft = os.environ.get("MAIL_STAMP_CHECK") == "warn"
    blocked = 0
    for p in paths:
        if not os.path.isfile(p):
            continue
        blob = git("hash-object", p).stdout.strip()
        if blob in on_main:
            continue
        stamp = front_date(open(p, encoding="utf-8", errors="replace").read())
        if not stamp:
            continue
        v = judge(stamp, now, now.strftime("%Y-%m-%d"))
        if not v:
            continue
        level, why = v
        if level == "BLOCK" and soft:
            level = "WARN"
        print(f"stamp-check {level}: {p}: date: {why}", file=sys.stderr)
        blocked += level == "BLOCK"
    return 1 if blocked else 0


def log_staged(now) -> int:
    today = now.strftime("%Y-%m-%d")
    files = git("diff", "--cached", "--name-only").stdout.split()
    for f in files:
        m = re.match(r"dev/\d{4}/\d{2}/\d{2}/(\d{4}-\d{2}-\d{2})-.*-log\.md$", f)
        if not m or m.group(1) != today:
            continue
        for line in git("diff", "--cached", "-U0", "--", f).stdout.splitlines():
            if not line.startswith("+#"):
                continue
            v = judge(line[1:], now, today)
            if v and "behind" not in v[1] and "dated" not in v[1]:
                print(f"stamp-check WARN: {f}: heading '{line[1:].strip()[:70]}': {v[1]}")
    if BRIEFING in files:
        for line in git("diff", "--cached", "-U0", "--", BRIEFING).stdout.splitlines():
            if not line.startswith("+") or line.startswith("+++"):
                continue
            for stamp in briefing_stamps(line[1:], today):
                v = judge(stamp, now, today)
                if v and "behind" not in v[1] and "dated" not in v[1]:
                    print(f"stamp-check WARN: {BRIEFING}: '{stamp}': {v[1]}")
    if DECISIONS in files:
        for line in git("diff", "--cached", "-U0", "--", DECISIONS).stdout.splitlines():
            if not line.startswith("+") or line.startswith("+++"):
                continue
            for stamp in decision_stamps(line[1:], today):
                v = judge(stamp, now, today)
                if v and "behind" not in v[1] and "dated" not in v[1]:
                    print(f"stamp-check WARN: {DECISIONS}: '{stamp}': {v[1]}")
    return 0


def decision_stamps(line: str, today: str):
    """A today-dated decisions.log line's leading stamp, plus any `HH:Mx` inside it ("recorded by Exec 10:0x")."""
    if not line.startswith(today):
        return []
    head = CLOCK.search(line[: len(today) + 8]) or MX.search(line[: len(today) + 8])
    stamps = [f"{today} {head.group(0)}"] if head else []
    return stamps + [
        f"{today} {m.group(0)}" for m in MX.finditer(line) if not head or m.start() > head.end()
    ]


def briefing_stamps(line: str, today: str):
    """Today's `*(Role, YYYY-MM-DD HH:MM ...` attributions on one briefing line; older ones are left alone."""
    return [f"{d} {t}" for d, t in BRIEF_STAMP.findall(line) if d == today]


def main(argv) -> int:
    now = datetime.now(PT).replace(second=0, microsecond=0)
    if argv[:1] == ["--stamp-now"]:
        return stamp_now(argv[1:], now)
    if argv[:1] == ["--mail"]:
        return mail(argv[1:], now)
    if argv == ["--log-staged"]:
        return log_staged(now)
    print(__doc__.split("\n\n")[2], file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
