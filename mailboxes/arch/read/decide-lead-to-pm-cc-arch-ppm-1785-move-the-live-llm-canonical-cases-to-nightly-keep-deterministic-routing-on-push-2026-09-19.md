---
from: lead
to: xian (ceo)
cc: arch, ppm
subject: "#1785 DECISION NEEDED (cheap one): the push-time canonical job spends your real key ~20×/day — recommend splitting: deterministic routing stays on push, the 28 live-LLM cases join the nightly. One-line workflow change either way."
date: 2026-09-19
---

PM — #1785 (epic 1) was filed with "not decided unilaterally," so here's the decision memo.
Two facts verified this fire, then a recommendation.

## The facts (workflow source, read directly)

- `.github/workflows/e2e-aaxt.yml` job `canonical-regression` runs on every push touching
  conversation code (~20 runs/day per #1785's own measurement) and injects
  `secrets.ANTHROPIC_API_KEY` / `OPENAI_API_KEY` — **your real keys**. The job's own comments
  document **28 live-LLM `test_floor_response_no_template` cases** running to completion at
  5–13s each; the rest of its selection (`TestCanonicalRouting or
  TestCanonicalResponseStructure`) is deterministic and free.
- This spend is invisible to per-account attribution today — it bills whichever account the
  repo secrets belong to, which is exactly the blind spot the usage-per-account capture
  (written this morning) exists to close. CI's rows would come from you or Dispatch, not any
  seat.

## Recommendation: split, don't move wholesale

Keep the **deterministic** routing/structure asserts on push (they're the cheap regression
net that catches misroutes at the moment they land — that's earning its keep), and move only
the **live-LLM floor cases** to the AAXT nightly schedule, which already exists in the same
workflow for exactly this cost profile (~$0.50/run tier). Push-time coverage loses nothing
deterministic; live-response quality checking drops from ~20×/day to 1×/day. Implementation
is a `-k` filter change plus adding the live cases to the nightly job's selection — one
commit, reversible, no new infrastructure.

Alternative if you'd rather not split: move the whole job to nightly (simplest), accepting
that routing regressions surface next morning instead of at push time. I wouldn't — the
deterministic half is free and fast.

**Say "split" or "wholesale" (or "leave it") and I'll ship it in the epic-1 lane.** No
urgency beyond it being the last undecided item in epic 1 besides the standing-red closeouts
in flight.

**Verified how**: e2e-aaxt.yml read directly this fire (secrets injection at :241-242, the
28-case count and 25-min timeout rationale in the job's own comments at :146-151); run
cadence from #1785's filing. NOT independently re-measured: the ~20 runs/day figure or
per-case latency — both from #1785's own account.

— Lead, 2026-09-19
