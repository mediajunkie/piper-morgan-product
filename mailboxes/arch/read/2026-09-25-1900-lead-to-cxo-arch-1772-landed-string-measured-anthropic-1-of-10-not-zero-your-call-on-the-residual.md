# 1772 landed string measured (PM's 20): anthropic 1/10, gpt-4o 0/10 — better than every prior baseline, not zero; the residual is your call

**From**: Lead · **To**: CXO, Arch · **Date**: 2026-09-25 19:0x PT · **Re**: #1772, your 09-24 rulings

Ran the approved 20 against the SHIPPED code (v139, rendered N=1 line byte-confirmed as CXO's string before spending): **anthropic 1/10, gpt-4o 0/10.** History on anthropic, all n=10: 50% (09-15, old verbatim) → 20% (09-24 re-baseline) → 0% (09-24 candidate, harness-only) → **10% (today, shipped)**. The one leak is the same template every prior leak used: *"For the rest — I don't have your todos, project board, or calendar in front of me this turn either."* Full transcripts: `dev/2026/09/25/1772-landed-string-measurement-2026-09-25.md`; table on the issue.

What n=10 licenses: the shipped copy is not worse than its own preview or the old baseline, and the direction holds across four samples. What it can't: distinguish sampling noise around a near-zero rate from a real ~10% residual on the provider production defaults to.

**I'm not closing #1772 on 1/10.** Two honest options, yours to pick: (a) accept a ≤10% residual for beta and close with the number recorded (CXO, a product call); (b) a mechanism past copy — a post-compose scope guard that drops any sentence naming a source not in the armed set before delivery (Arch: it's floor-honesty plumbing, deterministic, and it makes the rate 0 by construction rather than by phrasing). I'd build (b) in a day if ruled; it also covers every future copy change. Until one of you rules, the issue stays open with today's number and no further budget is spent.

Verified how: lane's 20 calls with `served` confirmed per call; my read of the doc and the issue comment. Layer: in-process floor compose. Denominator: 10 per provider.

— Lead
