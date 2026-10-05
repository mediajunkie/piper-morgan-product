#!/usr/bin/env python3
"""seat-denial-scan.py: count auto-mode classifier denials per seat (read-only).

Usage: seat-denial-scan.py [HOURS=24]
Scans ~/.claude-pm/projects/*worktrees-<role>/*.jsonl tool_results containing the
classifier-denial sentence. Prints per-seat count, categories, and the denied tool call.
Measures: denials recorded in each seat's own transcripts. Does NOT see denials in
seats whose transcripts live elsewhere (config_dir=default).
"""

import collections
import datetime as dt
import glob
import json
import os
import re
import sys

hours = float(sys.argv[1]) if len(sys.argv) > 1 else 24
cut = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours)
base = os.path.expanduser("~/.claude-pm/projects")
pat = re.compile(r"denied by the Claude Code auto mode classifier\. Reason: \[([^\]]+)\]")
rows = {}
for d in sorted(glob.glob(base + "/*piper-morgan-worktrees-*")):
    role = d.rsplit("worktrees-", 1)[1]
    cnt = collections.Counter()
    ex = []
    files = 0
    for f in glob.glob(d + "/*.jsonl"):
        if dt.datetime.fromtimestamp(os.path.getmtime(f), dt.timezone.utc) < cut:
            continue
        files += 1
        last_use = {}
        for line in open(f, errors="replace"):
            if "tool_use" not in line and "classifier" not in line:
                continue
            try:
                o = json.loads(line)
            except Exception:
                continue
            ts = o.get("timestamp", "")
            c = (o.get("message") or {}).get("content")
            if not isinstance(c, list):
                continue
            for b in c:
                if b.get("type") == "tool_use":
                    last_use[b.get("id")] = b
                elif b.get("type") == "tool_result":
                    s = b.get("content")
                    if isinstance(s, list):
                        s = " ".join(x.get("text", "") for x in s if isinstance(x, dict))
                    m = pat.search(s or "")
                    if m and ts and dt.datetime.fromisoformat(ts.replace("Z", "+00:00")) >= cut:
                        cnt[m.group(1)] += 1
                        u = last_use.get(b.get("tool_use_id"), {})
                        inp = u.get("input", {})
                        tgt = inp.get("file_path") or (inp.get("command") or "")[:90].replace(
                            "\n", " "
                        )
                        ex.append((ts[:19], u.get("name", "?"), tgt))
    rows[role] = (files, cnt, ex)
print(
    f"classifier denials, last {hours:g}h, per seat (denominator: {len(rows)} seats with transcripts in ~/.claude-pm)"
)
for role, (files, cnt, ex) in rows.items():
    print(f"{role:8} files={files:3} denials={sum(cnt.values()):3} {dict(cnt)}")
    for e in ex[:6]:
        print("   ", *e)
