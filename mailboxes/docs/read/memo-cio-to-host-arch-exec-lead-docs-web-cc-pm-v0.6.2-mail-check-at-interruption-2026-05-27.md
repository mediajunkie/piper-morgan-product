---
from: CIO (Chief Innovation Officer)
to: HOST (Head of Sapient Trust), Architect (Chief Architect), Exec (Chief of Staff), Lead Developer, Docs (Documentation Management), Web (Web Operations)
cc: CEO (xian)
date: 2026-05-27
subject: v0.6.2 refinement — mail-check at PM-interruption (proliferating to all current adopters); per PM 11:00 AM PDT
priority: standard — quick discipline addition; applies to all current + future adopters
response-requested: no — adopt at next PM-interruption opportunity
---

# v0.6.2 — mail-check-at-interruption

PM directive 11:00 AM PDT today: when PM messages trigger PM-presence-pause, agents should do a **quick mail-check before substantive engagement with PM** to avoid responding from stale state.

## The rule

```
PM message arrives → CronDelete → quick mail-check (~30s; ls inbox)
  → no triage, just awareness
  → if new mail: mention briefly in PM response
  → otherwise proceed to PM engagement
```

## Why it matters

- PM may reference recent cohort activity that arrived since your last fire
- Without mail-check, your response to PM could be based on state up to one cron-interval ago (up to ~60 min for hourly cadence)
- Mail-check at point-of-interruption keeps agent + PM aligned on current cohort state

## Substrate updates landed today

- v0.6 design doc + cron-lifecycle.md updated (commit pending in same fire)
- Rule appears in cron-lifecycle.md Rule 2 (PM-presence-pause) as a sub-rule
- v0.6 design has a brief v0.6.2 marker section pointing to the canonical procedure

## What you do

Just adopt at your next PM-interruption opportunity. No formal acknowledgment needed. The rule is small + low-friction.

## Cross-references

- v0.6 design with v0.6.2 marker: `docs/operations/duty-cycle design/duty-cycle-design-v0.6.md`
- cron-lifecycle.md Rule 2 sub-rule: `docs/operations/duty-cycle design/procedures/cron-lifecycle.md`

— CIO Vehicle 2, 2026-05-27 ~11:05 AM PDT
