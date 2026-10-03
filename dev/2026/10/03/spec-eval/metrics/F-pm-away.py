#!/usr/bin/env python3
"""F-pm-away.py — weekly PC/coordination commits around the PM-away week (2026-07-11..18, per Lead log
'five quiet days since PM's illness note' and a memo 'week of July 11–18 (PM was away)'). Reads D0 commits.csv."""
import csv, datetime as dt, collections
W = collections.defaultdict(collections.Counter)
for r in csv.DictReader(open(__file__.replace("F-pm-away.py", "commits.csv"))):
    d = dt.datetime.utcfromtimestamp(int(r["epoch"])).date()
    if not (dt.date(2026, 6, 20) <= d < dt.date(2026, 8, 8)): continue
    wk = d - dt.timedelta(days=(d - dt.date(2026, 7, 11)).days % 7)
    if r["merge"] == "1": W[wk]["merge"] += 1; continue
    W[wk]["all"] += 1; W[wk]["pc"] += r["is_pc"] == "1"; W[wk]["pc_lines"] += int(r["pc_lines"] or 0)
    W[wk]["coord"] += bool(r["coord_class"])
print("week_start(Sat)  nonmerge  PC  PC_lines  coord(mail/log/hb/stop)")
for k in sorted(W): print(k, W[k]["all"], W[k]["pc"], W[k]["pc_lines"], W[k]["coord"], "<- PM away" if k == dt.date(2026, 7, 11) else "")
