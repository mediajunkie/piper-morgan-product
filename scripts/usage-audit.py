#!/usr/bin/env python3
"""Weekly token-usage audit, read from Claude Code's own transcripts.

Every assistant message in ~/.claude-pm/projects/*/*.jsonl carries `message.usage`
with exact input / cache_creation / cache_read / output counts, plus the model and
the cwd. That is a ledger, not an estimate, and it is the only per-seat usage data
we have locally. Built 2026-09-21 (Exec) when the weekly limit hit 62% at 48% through
the week and nobody could say which seat, model, or mechanism was responsible.

Usage:  python3 scripts/usage-audit.py ["YYYY-MM-DD HH:MM" window start, UTC]
        default window start is the 2026-09-18 05:00Z limit reset.

Two honest limits, both load-bearing when reading the output:
  1. Price weighting is NOT applied here -- this reports raw weighted token movement.
     A model-price view changes the ranking completely (Sonnet dominates raw volume;
     Opus dominates cost). Anthropic's actual rate-limit formula is not visible to
     this script, so neither view is authoritative on its own. Report both.
  2. This is the client-side ledger. Anthropic's own metering is the authority.

Deduped by requestId -- retries and re-serialized lines otherwise double-count.
"""

import collections
import datetime as dt
import glob
import json
import os
import sys

_a = sys.argv[1] if len(sys.argv) > 1 else "2026-09-18 05:00"  # default: Thu 22:00 PDT reset
WEEK_START = dt.datetime.strptime(_a, "%Y-%m-%d %H:%M").replace(tzinfo=dt.timezone.utc)


def parse(ts):
    try:
        return dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except:
        return None


# relative cost weights vs 1 input token (standard Anthropic price structure)
W = dict(inp=1.0, cw=1.25, cr=0.1, out=5.0)

rows = []
seen = set()
for f in glob.glob(os.path.expanduser("~/.claude-pm/projects/*/*.jsonl")):
    if os.path.getmtime(f) < WEEK_START.timestamp():
        continue
    for line in open(f, encoding="utf-8", errors="replace"):
        if '"usage"' not in line:
            continue
        try:
            d = json.loads(line)
        except:
            continue
        m = d.get("message") or {}
        u = m.get("usage")
        if not u:
            continue
        t = parse(d.get("timestamp") or "")
        if not t or t < WEEK_START:
            continue
        rid = d.get("requestId") or d.get("uuid")
        if rid in seen:
            continue
        seen.add(rid)
        rows.append(
            dict(
                t=t,
                model=m.get("model") or "?",
                cwd=d.get("cwd") or "",
                side=bool(d.get("isSidechain")),
                inp=u.get("input_tokens", 0),
                cw=u.get("cache_creation_input_tokens", 0),
                cr=u.get("cache_read_input_tokens", 0),
                out=u.get("output_tokens", 0),
            )
        )


def seat(cwd):
    if not cwd:
        return "?"
    if "piper-morgan-worktrees/" in cwd:
        return cwd.split("piper-morgan-worktrees/")[1].split("/")[0]
    return os.path.basename(cwd.rstrip("/")) or "?"


def cost(r):
    return sum(r[k] * W[k] for k in W)


for r in rows:
    r["seat"] = seat(r["cwd"])
    r["c"] = cost(r)
TOT = sum(r["c"] for r in rows)
print(f"records={len(rows)}  window={WEEK_START:%Y-%m-%d %H:%M}Z .. now")
print(f"TOTAL weighted cost-equivalent tokens = {TOT/1e6:.1f}M\n")


def table(title, key, limit=None):
    agg = collections.Counter()
    for r in rows:
        agg[key(r)] += r["c"]
    print(f"── {title} " + "─" * (52 - len(title)))
    items = agg.most_common(limit)
    for k, v in items:
        print(f"  {str(k)[:34]:<34} {v/1e6:>7.1f}M  {100*v/TOT:>5.1f}%")
    print()


table("BY SEAT", lambda r: r["seat"])
table("BY MODEL", lambda r: r["model"])
table("MAIN SESSION vs SUBAGENT", lambda r: "SUBAGENT (sidechain)" if r["side"] else "main session")
table("BY DAY (PDT)", lambda r: (r["t"] - dt.timedelta(hours=7)).strftime("%a %m-%d"))
