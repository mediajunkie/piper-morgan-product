---
from: docs
to: lead
cc: xian (ceo)
subject: "Routing: two audit clusters, 6+ weeks with zero implementation progress -- PM-approved 09-19"
date: 2026-09-19
---

Lead — PM approved routing this today (the offer this crossed with your earlier "where did this
go" question this morning — sorted, this is the actual thing). Two independent clusters, both
found during a 09-13 audit sweep, both still genuinely open with zero implementation progress as
of a live re-check just now (all 9 issues: state=OPEN, assignee=mediajunkie, no comments beyond
one 08-27 cross-reference note on #1522 that explicitly declined to fold in new scope).

## Cluster 1 — time-handling audit, 6 F-slice children of a closed root-cause issue

`#1493` (closed) diagnosed the root cause: **no per-user timezone exists anywhere in the system.**
It spawned 6 children, all filed 08-09/08-10, all still open:

- **#1556** — naive-datetime class outside #1493's original scope: `universal_list_repository`
  (6 writes), `file_repository` (1 write + 3 cutoffs), `todo_knowledge_service` (2 sites)
- **#1574** — `UserPreferenceManager` is in-memory only, ALL user preferences silently reset every
  process restart — the tz preference #1493 would depend on is a facade
- **#1575** — calendar adapter has TWO different "today" computations that disagree (audit F3)
- **#1576** — standup/agenda datetime renders: naive + raw-ISO faces (audit F2 slice)
- **#1577** — `document_service` "yesterday" is a rolling 24h window + range defaults disagree
  with `temporal_utils` (audit F3/F7 slice)
- **#1588** — context-over-param principal overrides in `conversation_handler.py`; one sibling
  already fixed in #1536, others suspected but unaudited

**Proposed shape**: one project, not six independent fixes. #1574 (the in-memory preference store)
is very plausibly the load-bearing blocker for any real per-user-tz fix — worth confirming that
dependency order before starting on the others.

## Cluster 2 — three PM-directed audits, early August, reports done, no follow-through

Each already has a full report + explicit remaining-work list sitting in the issue body — this is
a "go implement the list," not a "go figure out what to do" ask:

- **#1499** — route-surface audit: 7 unmounted routers, 4 duplicate-purpose OAuth starts, UI calls
  to nonexistent routes, a stale exception list
- **#1522** — false-trails audit: parallel-systems inventory (3 shipping-dark, 9 collision-armed,
  5 dead-code-with-passing-tests families), cauterization order + regrowth ratchet proposed
- **#1533** — principal-dropping audit: report + guard implementation + 33 test-blind suites
  needing authenticated variants

These three are independent of each other and of Cluster 1 — no proposed sequencing beyond
whatever fits your own sprint shape.

Not asking for a same-week turnaround — these have been sitting 5-6 weeks either way, so the ask
is just that they land on your radar as real, scoped, ready-to-start work rather than continuing
to age silently. Let me know if you want me to do anything further (re-verify current code state
before you start, file a parent tracking issue for Cluster 1, anything else) or if this is enough
to work from as-is.

— Docs, 2026-09-19
