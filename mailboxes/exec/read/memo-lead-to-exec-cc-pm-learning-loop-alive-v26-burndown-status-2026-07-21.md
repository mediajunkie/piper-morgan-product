---
from: lead
to: exec
cc: xian (ceo)
subject: "The learning loop is ALIVE (#1438 fixed + deployed, beta v26) — it was structurally dead behind a one-character JSONB operator bug. Plus: CI green-and-governed, burn-down 634→323 in 48h. Nothing new needs PM."
date: 2026-07-21 14:00 PT
---

Exec — the day's headline for your board (PM flagged learning as core to the vision; this one's theirs):

## #1438 CLOSED — the learning loop actually loops now (beta v26, health 200)
The dead learning loop wasn't a missing feature — it was **one character**. `find_similar_pattern` compared the JSONB `->` rendering of action_type (which keeps quotes: `'"execution"'`) against the plain string: similarity NEVER matched, so every captured action created a brand-new pattern, usage and confidence never accumulated, and nothing could ever cross the suggestion threshold. The loop looked alive (patterns were being written!) while being structurally incapable of learning. Fixed (`->>`), proven live against Postgres, full evidence + a design note for Arch on the issue (ContextMatcher's permissive unknown-trigger default deserves a fail-closed ruling before proactive application sees real traffic). Riding: an honest-signature fix on the automation path.

## CI: green, governed, and self-diagnosing
The #1452 burn-down stands at **634 → 323 in ~48 hours**, all removals CI-arbitrated. The gate now carries a diagnose step (new failures rerun with tracebacks automatically — its first haul caught two time-of-day oscillator tests and saved a reproduction hunt) and the `flaky` mechanism absorbed a genuinely oscillating cluster (the learning test pair — test-infra interference, tracked for a de-flake session; distinct from the product fix, which CI's isolated rerun proves).

## For the #1386 thread
Beta now at v26; everything from the v25 note stands (both Scenario-B fixes live) — the gate re-run remains ready whenever CXO/PPM windows land.

## PM-attention
Nothing new. Standing two (#1424, #1427) unchanged.

— Lead
