#!/usr/bin/env python3
"""R3 step-0 baseline: lines added to coordination vs product paths on origin/main.
Usage: r3-coordination-baseline.py SINCE UNTIL [--exclude-hour 'YYYY-MM-DD HH:MM' 'YYYY-MM-DD HH:MM']
Classes agreed with CIO 2026-10-04. Metric is lines added (git numstat), non-merge commits, Pacific time."""
import subprocess, sys, collections, datetime as dt
from zoneinfo import ZoneInfo
PT = ZoneInfo("America/Los_Angeles")
COORD_PREFIX = ("mailboxes/", "dev/", "docs/internal/operations/", "scripts/git-hooks/",
                ".claude/hooks/", ".claude/skills/duty-cycle-tick/")
COORD_SCRIPTS = ("scripts/duty-cycle-", "scripts/mail-send.sh", "scripts/regenerate-mailbox-manifests.py",
                 "scripts/archive-mailbox-read.py", "scripts/sprint-truth.py", "scripts/check-unboarded-pm-items.sh")
CODE_PREFIX = ("services/", "web/", "tests/", "alembic/", "config/", "cli/", "main.py", "mcp/")
def cls(p):
    if p.startswith(COORD_PREFIX) or p.startswith(COORD_SCRIPTS): return "coord"
    if p.startswith(CODE_PREFIX): return "product_code"
    return "product_other"
since, until = sys.argv[1], sys.argv[2]
ex = None
if "--exclude-hour" in sys.argv:
    i = sys.argv.index("--exclude-hour")
    f = lambda s: dt.datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=PT)
    ex = (f(sys.argv[i+1]), f(sys.argv[i+2]))
out = subprocess.run(["git","log","origin/main","--no-merges",f"--since={since}",f"--until={until}",
    "--numstat","--format=@@%H\t%ct\t%s"],capture_output=True,text=True,check=True).stdout
tot = collections.defaultdict(lambda: collections.defaultdict(int))
commits = collections.defaultdict(lambda: collections.defaultdict(int))
cur = None; skip = False
for line in out.splitlines():
    if line.startswith("@@"):
        h, ct, subj = line[2:].split("\t", 2)
        t = dt.datetime.fromtimestamp(int(ct), PT)
        skip = bool(ex and ex[0] <= t < ex[1])
        wk = (t - dt.timedelta(days=t.weekday())).strftime("%m-%d")
        cur = None if skip else wk
        if cur: tot[cur]["commits"] += 1
        continue
    if not line or cur is None: continue
    a, d, p = line.split("\t", 2)
    if a == "-": continue
    tot[cur][cls(p)] += int(a)
print(f"range {since}..{until}  excl={'none' if not ex else ex[0].strftime('%m-%d %H:%M')+'-'+ex[1].strftime('%H:%M')+' PT'}")
print(f"{'week(Mon)':10} {'commits':>8} {'coord':>10} {'prod_code':>10} {'prod_other':>11} {'coord:code':>11}")
T = collections.defaultdict(int)
for wk in sorted(tot):
    r = tot[wk]
    for k in ("commits","coord","product_code","product_other"): T[k] += r[k]
    print(f"{wk:10} {r['commits']:>8} {r['coord']:>10} {r['product_code']:>10} {r['product_other']:>11} {r['coord']/max(r['product_code'],1):>11.1f}")
print(f"{'TOTAL':10} {T['commits']:>8} {T['coord']:>10} {T['product_code']:>10} {T['product_other']:>11} {T['coord']/max(T['product_code'],1):>11.1f}")
