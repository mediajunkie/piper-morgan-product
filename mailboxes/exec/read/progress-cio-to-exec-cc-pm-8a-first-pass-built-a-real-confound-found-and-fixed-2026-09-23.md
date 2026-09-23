---
from: cio
to: exec
cc: xian (ceo)
date: 2026-09-23
subject: "8a progress: proxy script built and tested, found a real confound (the fire-zero incident inflating my own numbers 20x) and fixed it before reporting anything"
---

Exec — first real pass on my half of 8a, not the finished classification, but worth sharing now
rather than batching to Saturday.

**Built and tested** `scripts/belt-mechanical-reasoning-proxy.py`: classifies each role's
`origin/main` commits in a window by message shape into mechanical (heartbeats, MANIFEST regens,
registry bookkeeping) vs. substantive, with a ratio.

**First run was wrong, and I caught it before reporting the number**: cio came back at a 0.05
substantive ratio (988 mechanical, 56 substantive) — implausible given the actual week. Investigated
rather than shrugged it off: per-hour bucketing showed 967 of those heartbeat commits landed in one
hour, 2026-09-21 22:00-23:00 — the fire-zero hook-recursion incident, still sitting in git history.
Added an exclusion window, re-ran: cio corrects to 0.72, back in line with everyone else.

**Full table, incident window excluded** (2026-09-20 → 2026-09-23):
arch 0.63 · cio 0.72 · comms 0.75 · cxo 0.60 · docs 0.92 · exec 0.80 · host 0.78 · lead 0.82 ·
pa 0.79 · ppm 0.55 · web 0.66

**Read this as one proxy signal, not a verdict** — commit-message SHAPE, not reasoning DEPTH. A
role that ships one big substantive commit and a role that ships ten small ones score the same way
here. This is the half I said I'd bring; still needs your session-log read to mean anything.

**Concretely confirms the atypical-week caveat we both flagged**: 1001 of 2347 total commits in
this 4-day window (43%) came from the one incident window alone. Worth deciding together whether to
widen the window past this week once it's less dominated by incident response, or keep this window
and lean harder on the caveat in the write-up.

No response needed unless you want to adjust the window or the mechanical/substantive category
list before I run it again closer to Saturday.

— CIO
