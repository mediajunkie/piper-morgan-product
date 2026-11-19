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
Log mode refuses since 2026-11-18 (xian's yes to CIO's 11-13 clock-rule proposal, relayed by Comms):
see `review_added` for what it refuses and what it only warns on. Before that it only warned. It looks at added lines in staged `dev/YYYY/MM/DD/*-log.md` files that are `#`
headings carrying a time, and only for today's log: it flags an estimated form or a time ahead of now, not
one behind (a heading can fairly carry the time a wake began). It also reads today's `*(Role, date time`
attributions on added lines of BRIEFING-CURRENT-STATE.md (10-17: the briefing held 7 `HH:Mx` stamps, two
of them CIO's, because it passed through neither mail-send nor a log heading), and today-dated lines added
to decisions.log, both the leading stamp and any `HH:Mx` inside the line (10-19: "recorded by Exec 10:0x").
Since 11-03 it also warns on an `HH:Mx` form in any added line of today's log, and of a
`dev/active/<role>-standing-items.md` or `-carry-forward.md`.
Stamp-now mode (xian 10-30 via Exec, "make it easier to do such things without having to remember"): a memo
may say `date: now` (or `date: now PT`), and every such file in one call gets the same clock reading, so the
sent mirror and every recipient copy match. A time nobody types can't be a guess.
Exit 0 = nothing blocking; 1 = a BLOCK (mail mode) or a refusal (log mode, one line in piper-stamp-refusals.log
under the git common dir); 3 = log mode could not run. Owner: CIO. Review: 2026-12-08.
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
# 11-13: a short `MM-DD` right before a time ("11-11 22:11 to 11-12 06:21") dates that time too. Without it,
# a heading naming yesterday's time read as today's and as ahead of the clock (Lead dbbc7ff3, CIO's backtest).
SHORT_DAY = re.compile(r"(?<![\d-])(\d{2})-(\d{2})(?=\s+\d{1,2}:\d)")
BRIEFING = "docs/briefing/BRIEFING-CURRENT-STATE.md"
BRIEF_STAMP = re.compile(r"\(\w[\w ]*, (\d{4}-\d{2}-\d{2}) (~?\d{1,2}:\d[\dxX])")
DECISIONS = "docs/internal/architecture/decisions/decisions.log"
TRACKERS = re.compile(r"dev/active/[a-z]+-(standing-items|carry-forward)\.md$")


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True)


def judge(stamp: str, now: datetime, default_day: str):
    """Return (level, reason) for one stamp, or None if it's fine."""
    d = DAY.search(stamp)
    if not d:
        sd = SHORT_DAY.search(stamp)
        if sd and 1 <= int(sd.group(1)) <= 12:
            d = sd
            day = f"{now.year}-{sd.group(1)}-{sd.group(2)}"
    if d is not None and d.re is DAY:
        day = d.group(1)
    elif d is None:
        day = default_day
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
    """Read the staged added lines and judge them. Exit 1 if anything is refused."""
    files = git("diff", "--cached", "--name-only").stdout.split()
    added = {}
    for f in files:
        if not (LOG_NAME.match(f) or TRACKERS.match(f) or f in (BRIEFING, DECISIONS)):
            continue
        added[f] = [
            line[1:]
            for line in git("diff", "--cached", "-U0", "--", f).stdout.splitlines()
            if line.startswith("+") and not line.startswith("+++")
        ]
    findings = review_added(added, now)
    for level, f, why in findings:
        print(
            f"stamp-check {level}: {f}: {why}",
            file=sys.stderr if level == "REFUSED" else sys.stdout,
        )
    if any(level == "REFUSED" for level, _, _ in findings):
        record_refusal(findings, now)
        print(
            "stamp-check: commit refused (clock rule, xian 2026-11-18). Read `date` and write the minute; "
            '`scripts/log-entry.sh "title"` writes a heading with the clock. A time you are quoting goes '
            "in backticks.",
            file=sys.stderr,
        )
        return 1
    return 0


def record_refusal(findings, now) -> None:
    """One line per refused commit in `piper-stamp-refusals.log` under the git common dir, so the rule's
    refusal rate can be counted (a refused commit leaves nothing in git). Never fails the check."""
    try:
        common = git("rev-parse", "--git-common-dir").stdout.strip()
        if not common:
            return
        top = git("rev-parse", "--show-toplevel").stdout.strip()
        refused = [f for level, f, _ in findings if level == "REFUSED"]
        line = (
            f"ts={now:%Y-%m-%dT%H:%M%z} worktree={top} refused={len(refused)} "
            f"files={','.join(sorted(set(refused)))}\n"
        )
        with open(os.path.join(common, "piper-stamp-refusals.log"), "a", encoding="utf-8") as out:
            out.write(line)
    except Exception:
        pass


LOG_NAME = re.compile(r"dev/\d{4}/\d{2}/\d{2}/(\d{4}-\d{2}-\d{2})-.*-log\.md$")


def unquoted(line: str) -> str:
    """The line without its backtick spans: the escape for a time quoted from someone else."""
    return re.sub(r"`[^`]*`", "", line)


def review_added(added, now):
    """Judge added lines per staged file. Returns (level, file, why) rows, level REFUSED or WARN.

    Refused (xian's yes 2026-11-18, CIO's 11-13 proposal): a heading in today's log with a time
    ahead of the clock, or with an estimated form (`HH:Mx` or `~HH:MM`); an `HH:Mx` on any added
    line of today's log, a role's standing-items or carry-forward file, the briefing or
    decisions.log. Backticks are the only escape. Still a warning: a briefing attribution or a
    decisions.log stamp ahead of the clock."""
    today = now.strftime("%Y-%m-%d")
    out = []
    for f, lines in added.items():
        m = LOG_NAME.match(f)
        todays_log = bool(m) and m.group(1) == today
        checked = todays_log or bool(TRACKERS.match(f)) or f in (BRIEFING, DECISIONS)
        for raw in lines:
            line = unquoted(raw)
            if todays_log and line.startswith("#"):
                v = judge(line, now, today)
                if v and "behind" not in v[1] and "dated" not in v[1]:
                    out.append(("REFUSED", f, f"heading '{raw.strip()[:70]}': {v[1]}"))
                    continue
            if checked:
                for est in body_estimates(line):
                    out.append(("REFUSED", f, f"'{est}' is an estimated minute; write the minute"))
            if f == BRIEFING:
                for stamp in briefing_stamps(line, today):
                    v = judge(stamp, now, today)
                    if v and "ahead" in v[1]:
                        out.append(("WARN", f, f"'{stamp}': {v[1]}"))
            if f == DECISIONS:
                for stamp in decision_stamps(line, today):
                    v = judge(stamp, now, today)
                    if v and "ahead" in v[1]:
                        out.append(("WARN", f, f"'{stamp}': {v[1]}"))
    return out


def body_estimates(line: str):
    """`HH:Mx` forms on an added body line (11-03: CIO wrote "10:2x" in a standing-items row and "10:0x"
    in a log line; log mode had read headings only). Quoted relays warn too: the remedy is the same."""
    return [m.group(0) for m in MX.finditer(line)]


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
        try:
            return log_staged(now)
        except Exception as error:  # a broken check never blocks a commit (exit 3, not 1)
            print(
                f"stamp-check: could not run ({type(error).__name__}); not checked", file=sys.stderr
            )
            return 3
    print(__doc__.split("\n\n")[2], file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
