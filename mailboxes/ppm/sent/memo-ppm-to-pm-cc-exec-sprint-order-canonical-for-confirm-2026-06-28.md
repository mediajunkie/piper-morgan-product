---
from: ppm
to: xian (ceo)
cc: exec
subject: Canonical sprint-order list — for quick confirm
date: 2026-06-28
---

PM — you asked (via Exec) for a canonical sprint-order list as the authoritative reference for "what's the order?" Here it is.

**Location**: `docs/internal/planning/sprint-order.md`

## Sequence summary

**Completed**: M0, M1, M2, M3, RECONNECT WS-1, D1

**Active**: RECONNECT WS-2 (Lead Dev lane)

**Queued in order**:
1. M3-Quality (8 open) — concurrent with WS-2
2. M3-Health (10 issues)
3. M3-Security (9 issues)
4. → M4 starts after both WS-2 closes AND M3 sprints complete
5. M5

**Milestones**: beta Aug 1, production Oct 30, then fast-follow → dot-release → enterprise (all TBD)

## One open question

The Exec relay says "[3 M3 child sprints] → RECONNECT WS-2 → M4. Not concurrent." I've represented this as M3 running concurrent with WS-2 in Lead Dev's lane (since WS-2 is already active), with M4 gated on both closing. If you meant M3 finishes before WS-2 work resumes (WS-2 on hold while cohort does M3), the doc needs a small correction — just let me know.

## Also applied this fire

- Roadmap v18.2 updated in-place: D1 marked CLOSED (June 20, was framed as future), sprint sequence corrected, M3-Quality count corrected (12→8 open), dot-release/enterprise milestones added to timeline.
- #1326 filed: introduce-person standalone M4 issue (per your direction via Exec).
- M3-Quality/Health/Security sprint assignments cleared to PA (product-model review done; one #1175 source-type note forwarded to Lead Dev for awareness).

— PPM, 2026-06-28
