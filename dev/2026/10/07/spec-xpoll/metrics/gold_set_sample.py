#!/usr/bin/env python3 -I
"""Gold-set scaffold: 100 published, confidentiality-clear insights, stratified by quarter, seeded.
Writes gold-set-scaffold.md (table for Janus to pre-label and xian to confirm) and gold_set_ids.json."""
import json, random, collections, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
rows = [json.loads(l) for l in open(os.path.join(HERE, "insights.jsonl"))]
pool = [r for r in rows if r.get("published") and r.get("confidentiality") == "clear" and r.get("era") == "unified"]
def q(d): y, m = d[:4], int(d[5:7]); return "%s-Q%d" % (y, (m - 1) // 3 + 1)
by_q = collections.defaultdict(list)
for r in pool: by_q[q(r["brief_date"])].append(r)
N = 100
quarters = sorted(by_q)
# proportional allocation, min 8 per quarter where available
alloc = {k: min(len(v), max(8, round(N * len(v) / len(pool)))) for k, v in by_q.items()}
while sum(alloc.values()) > N:
    k = max(alloc, key=lambda k: alloc[k] - 8 if alloc[k] > 8 else -1); alloc[k] -= 1
while sum(alloc.values()) < N:
    k = max(alloc, key=lambda k: len(by_q[k]) - alloc[k]); alloc[k] += 1
assert all(alloc[k] <= len(by_q[k]) for k in alloc) and sum(alloc.values()) == N
rng = random.Random(20261008)
chosen = []
for k in quarters:
    c = sorted(by_q[k], key=lambda r: r["id"]); rng.shuffle(c); chosen += c[:alloc[k]]
chosen.sort(key=lambda r: r["id"])
assert len(chosen) == N, len(chosen)
json.dump([r["id"] for r in chosen], open(os.path.join(HERE, "gold_set_ids.json"), "w"), indent=0)
L = []
L.append("# Gold set scaffold — 100 insights for topic labelling (decision g: Janus pre-labels, xian confirms)\n")
L.append("Generated 2026-10-08 by `gold_set_sample.py` (seed 20261008) from `insights.jsonl`: published unified briefs only, confidentiality `clear` only, stratified by quarter. Pool: %d of 632 insights. Per quarter: %s.\n" % (len(pool), ", ".join("%s %d" % (k, alloc[k]) for k in quarters)))
L.append("""## Codebook (frozen 2026-10-08 per Janus C3) — one primary topic per insight

| # | Topic | Assign when the insight is mainly about… |
|---|---|---|
| 1 | agent coordination & process | how agents/roles hand off, schedule, message, decide, or govern their own work; duty cycles; mailboxes; session discipline |
| 2 | verification & testing | proving something works or didn't: tests, evals, checks, evidence standards, "verified how", false-clear failure modes |
| 3 | tooling & infrastructure | the machinery: CI, deploys, hosts, git mechanics, scripts, hooks, keys, environments, model/harness behaviour |
| 4 | documentation & knowledge | docs, briefings, logs, memory, glossaries, knowledge capture and retrieval — **including the sweep's own meta-insights about briefs, publishing and delivery** (the old "publishing & process meta" label folds here) |
| 5 | product & user-facing | what a user sees or does: features, UX, onboarding, surfaces (web/MCP/plugin), positioning, beta/launch |
| 6 | governance & security | rules, permissions, confidentiality, credentials, data boundaries, approvals, trust and oversight |

Secondary tag: free text, optional, your words (e.g. "worktrees", "ratchet tests", "Letters").

## How to fill it in
- **Janus**: put a topic number 1–6 in `Janus` for every row; add a tag if one jumps out. Same session it lands is perfect.
- **xian**: in `xian`, write **ok** to confirm, a **number** to correct, or **?** if it could be either (those rows drop out of the gold set rather than being forced). Rows you correct count double in the accuracy report.
- The "first line" is the insight heading only; open the brief (`src/internal/briefs/<date>-brief.md`, heading number in the id) when the heading is not enough.

## The 100

| # | id | brief date | first line | Janus | tag | xian |
|---|---|---|---|---|---|---|
""")
for i, r in enumerate(chosen, 1):
    head = (r.get("heading") or "").replace("|", "\\|").strip()
    L.append("| %d | `%s` | %s | %s |  |  |  |" % (i, r["id"], r["brief_date"], head))
open(os.path.join(HERE, "gold-set-scaffold.md"), "w").write("\n".join(L) + "\n")
print("pool", len(pool), "chosen", len(chosen), "quarters", dict(sorted(alloc.items())))
