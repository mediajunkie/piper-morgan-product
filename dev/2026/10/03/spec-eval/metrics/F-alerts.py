#!/usr/bin/env python3
"""F-alerts.py — classify duty-cycle-watchdog alert memos in PM's mailbox against git activity. Read-only.
For each alert: roles listed as STALE with their claimed age; compare with last commit (any author) whose subject
starts with the role slug (`role(`, `role:`, `<class>(role)`), before the detection time. Timezone: alert times are
PDT (UTC-7) per watchdog; git %at is epoch.
  claimed-stale-but-committed  = a role commit exists within the role's threshold before detection (alert contradicted by git)
  silent-per-git               = no role commit within threshold (consistent with stall OR a compliant quiet hold)
  recovered_within_3h          = role commit within 3h after detection.
"""
import os, re, subprocess, datetime as dt, collections
R = "/home/user/piper-morgan-product"; SNAP = "a191856164351cf59ba033d7dbc4a34f036c6122"
log = subprocess.run(["git", "log", "--no-merges", "--format=%at\t%s", SNAP, "--since=2026-06-01"], cwd=R, capture_output=True, text=True).stdout
ev = collections.defaultdict(list)
for line in log.splitlines():
    t, s = line.split("\t", 1)
    m = re.match(r"([a-z-]+)(\(([a-z-]+)\))?[:( ]", s)
    if not m: continue
    for slug in {m.group(1), m.group(3)}:
        if slug: ev[slug].append(int(t))
for k in ev: ev[k].sort()
box = os.path.join(R, "mailboxes/xian (ceo)")
rows = []
for sub in ("inbox", "read"):
    for f in sorted(os.listdir(os.path.join(box, sub))):
        if not f.startswith("alert"): continue
        txt = open(os.path.join(box, sub, f), errors="replace").read()
        m = re.search(r"Detected\*\*: (\d{4}-\d\d-\d\d \d\d:\d\d)", txt)
        if not m: rows.append((f, None, [])); continue
        det = dt.datetime.strptime(m.group(1), "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone(dt.timedelta(hours=-7)))
        stale = re.findall(r"STALE (\w+) (\d+)h \((?:dyn-)?threshold (\d+)h", txt.split("all currently stale")[0] if "all currently stale" in txt else txt)
        rows.append((f, det, stale))
cnt = collections.Counter(); per = []
for f, det, stale in rows:
    if det is None: cnt["unparsed"] += 1; continue
    ts = det.timestamp()
    for role, age, thr in stale:
        prior = [t for t in ev.get(role, []) if t <= ts]
        gap_h = (ts - prior[-1]) / 3600 if prior else None
        after = [t for t in ev.get(role, []) if ts < t <= ts + 3 * 3600]
        cls = "claimed-stale-but-committed" if gap_h is not None and gap_h < int(thr) else "silent-per-git"
        cnt[cls] += 1; cnt["recovered_within_3h"] += bool(after)
        per.append((f, role, age, thr, None if gap_h is None else round(gap_h, 1), cls, bool(after)))
print(f"alert memos: {len(rows)}; role-alerts: {len(per)}")
print(dict(cnt))
bym = collections.Counter((p[0][len('alert-duty-cycle-stall-'):][:7], p[5]) for p in per)
for k in sorted(bym): print(" ", k, bym[k])
print("\nsample rows (file, role, claimed_age_h, threshold_h, git_gap_h, class, recovered<3h):")
for p in per[:: max(1, len(per)//25)]: print(" ", p)
