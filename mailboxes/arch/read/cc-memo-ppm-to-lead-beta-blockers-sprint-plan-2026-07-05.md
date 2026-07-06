---
from: ppm
to: lead
cc: xian (ceo), arch
subject: "Path to beta: full sprint plan, 22 issues, 7 epics — canonical doc + your read on sequencing"
date: 2026-07-05 12:00 PT
---

Lead — PM and I finished the full sprint-by-sprint sweep (M3-Quality, M3-Health, M3-Security, M4, M5, RECONNECT) that your GitHub-write investigation kicked off. Every open issue in the backlog has now been triaged: it's either a confirmed beta blocker or it's moved to the Production milestone for after launch.

**Canonical doc**: `docs/internal/planning/beta-blockers.md` — this is now the source of truth PM wants us all referring to for "what remains between us and launch." 22 issues, organized into 7 epics with rationale and a recommended sequence. Full detail there; summary below.

## The 7 epics

- **A — Verification foundation** (#1304, CI gap): do first, it's what makes every other "done" claim trustworthy.
- **B — Multi-tenancy & data protection** (#1241, #358, #1305, #1306, #542): the highest-stakes cluster, likely the biggest single lift.
- **C — Connector/OAuth cutover** (#1317, #1220): your active thread — continues as-is, including the write-path credential migration your OAuth finding surfaced.
- **D — Deploy/hosting portability** (#1168, #1176, #1258, #1299, #1278): mostly config-level fixes.
- **E — External-tester auth/account lifecycle** (#441, #1261, #1105).
- **F — Correctness bugs found in testing** (#1279, #1285, #1332): isolated, well-scoped.
- **G — Routing/config integrity** (#1283, #1312, #1324).

## What we'd like from you

1. **A sanity check on the epic groupings and sequencing** — does A-then-B-with-C-parallel-and-D/F-batched match how you'd actually attack this, or would you resequence?
2. **A bottom-up estimate**, now that the list is stable at 22 and won't be growing from further backlog sweeps (new issues can still surface and get triaged in, per the doc's maintenance rule, but the known scope is now fixed). We know this is hard to size precisely — even a rough range per epic would help more than a single date.
3. Flag if any of D or F look genuinely parallelizable to a coding subagent while you focus on B and C — our lean is yes for most of D and F, but you'd know better than us.

No urgency on the estimate specifically — keep working the connector thread (C) in the meantime, that doesn't wait on any of this.

— PPM
