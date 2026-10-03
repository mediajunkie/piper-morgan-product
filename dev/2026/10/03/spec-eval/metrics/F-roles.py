#!/usr/bin/env python3
"""F-roles.py — per-role cost/value proxies, 4 weeks 2026-09-05..2026-10-03 (snapshot a191856). Read-only.
commits: non-merge commits whose subject's first token or parenthesized scope is the role slug.
classes: mail/log/hb/stop/heartbeat (coordination) vs other. bytes: added-line bytes for those commits (numstat).
memos_sent: files in mailboxes/<role>/sent dated in window; replies_received: other roles' memos whose frontmatter
in-reply-to names a file that is in <role>/sent. pm_cc: sent memos with PM in to/cc.
state files: bytes of dev/active/<role>-carry-forward.md + <role>-standing-items.md + briefing (session-start-ish reads).
"""
import os, re, subprocess, collections, datetime as dt
R = "/home/user/piper-morgan-product"; SNAP = "a191856164351cf59ba033d7dbc4a34f036c6122"
ROLES = "exec arch cxo ppm cio host comms lead pa docs web".split()
since, until = "2026-09-05", "2026-10-04"
out = subprocess.run(["git", "log", "--no-merges", f"--since={since}", f"--until={until}", "--format=@@%s", "--numstat", SNAP],
                     cwd=R, capture_output=True, text=True).stdout
c = collections.defaultdict(collections.Counter)
cur = None
for line in out.splitlines():
    if line.startswith("@@"):
        s = line[2:]; m = re.match(r"([a-z-]+)(\(([a-z-]+)\))?[:( ]", s); cur = None
        if m:
            role = m.group(3) if m.group(3) in ROLES else (m.group(1) if m.group(1) in ROLES else None)
            cls = m.group(1) if m.group(1) in ("mail", "log", "hb", "hb-last-invoked", "stop", "heartbeat") else "work"
            if role: cur = (role, "coord" if cls != "work" else "work"); c[role][cur[1] + "_commits"] += 1
    elif cur and line.strip():
        p = line.split("\t")
        if p[0].isdigit(): c[cur[0]][cur[1] + "_lines_added"] += int(p[0])
B = os.path.join(R, "mailboxes")
def fm(path):
    try: t = open(path, errors="replace").read(4000)
    except Exception: return {}
    m = re.match(r"---\n(.*?)\n---", t, re.S); d = {}
    if m:
        for l in m.group(1).splitlines():
            if ":" in l: k, v = l.split(":", 1); d[k.strip().lower()] = v.strip()
    return d
def indate(f):
    m = re.search(r"(2026-\d\d-\d\d)", f); return m and since <= m.group(1) < until
sentfiles = {r: set(os.listdir(os.path.join(B, r, "sent"))) if os.path.isdir(os.path.join(B, r, "sent")) else set() for r in ROLES}
owner = {f: r for r in ROLES for f in sentfiles[r]}
replies = collections.Counter(); pmcc = collections.Counter(); sent = collections.Counter()
for r in ROLES:
    for f in sentfiles[r]:
        if not indate(f): continue
        sent[r] += 1; d = fm(os.path.join(B, r, "sent", f))
        if re.search(r"xian|ceo|\bpm\b", (d.get("to", "") + " " + d.get("cc", "")).lower()): pmcc[r] += 1
        irt = d.get("in-reply-to", "").strip().strip('"')
        irt = os.path.basename(irt)
        if irt in owner and owner[irt] != r: replies[owner[irt]] += 1
logs = collections.Counter()
for root, _, files in os.walk(os.path.join(R, "dev/2026")):
    for f in files:
        m = re.match(r"(2026-\d\d-\d\d)-\d{4}-([a-z]+)-", f)
        if m and since <= m.group(1) < until and m.group(2) in ROLES: logs[m.group(2)] += 1
def sz(p): p = os.path.join(R, p); return os.path.getsize(p) if os.path.exists(p) else 0
BR = {"exec": "BRIEFING-ESSENTIAL-CHIEF-STAFF.md", "arch": "BRIEFING-ESSENTIAL-ARCHITECT.md", "cxo": "BRIEFING-ESSENTIAL-CXO.md", "ppm": "BRIEFING-ESSENTIAL-PPM.md",
      "cio": "BRIEFING-ESSENTIAL-CIO.md", "host": "BRIEFING-ESSENTIAL-HOST.md", "comms": "BRIEFING-ESSENTIAL-COMMS.md", "lead": "BRIEFING-ESSENTIAL-LEAD-DEV.md",
      "pa": "BRIEFING-piper-alpha.md", "docs": "BRIEFING-ESSENTIAL-DOCS.md", "web": "BRIEFING-ESSENTIAL-WEB.md"}
hdr = "role work_commits coord_commits coord_share work_lines_added coord_lines_added memos_sent memos_pmcc pmcc_share replies_recv replies_per_memo session_logs briefing_KB carryfwd_KB standing_KB portfolio_KB"
print(hdr.replace(" ", "\t"))
for r in ROLES:
    w, k = c[r]["work_commits"], c[r]["coord_commits"]
    print("\t".join(map(str, [r, w, k, f"{k/(w+k):.2f}" if w + k else "-", c[r]["work_lines_added"], c[r]["coord_lines_added"], sent[r], pmcc[r],
          f"{pmcc[r]/sent[r]:.2f}" if sent[r] else "-", replies[r], f"{replies[r]/sent[r]:.2f}" if sent[r] else "-", logs[r],
          round(sz("docs/briefing/" + BR[r]) / 1024), round(sz(f"dev/active/{r}-carry-forward.md") / 1024), round(sz(f"dev/active/{r}-standing-items.md") / 1024),
          round(sz(f"docs/briefing/ROLE-PORTFOLIO-{r.upper()}.md") / 1024)])))
for p in ["CLAUDE.md", "docs/briefing/BRIEFING-CURRENT-STATE.md", "docs/briefs/cross-pollination/current.md", ".claude/skills/duty-cycle-tick/SKILL.md", "dev/active/duty-cycle-registry.tsv"]:
    print(f"shared: {p} {sz(p)/1024:.0f} KB (~{sz(p)/4/1000:.1f}k tokens at chars/4, bytes as chars proxy)")
