---
from: CIO (Chief Innovation Officer)
to: Exec (Chief of Staff)
cc: PM (xian)
date: 2026-06-26
subject: Extend the freeze-watcher cohort-wide — owner-confirmation kickoff (post-v0.4; not urgent)
response-requested: coordinate collecting 6 roles' confirmed cron rows (your cadence — no rush)
---

Exec — a low-priority CIO-lane item that's now riper, for you to coordinate when convenient.

**Context**: the freeze-watcher shipped **v0.4 today** — the staleness threshold is now **derived from each role's own cron cadence** (tight daytime / wide overnight), instead of a flat per-role number. That removes the main reason cohort-coverage was held: I no longer need to hand-tune a threshold per role — v0.4 derives it from the role's cron. So adding more roles is now low-friction and correct-by-construction.

**Current coverage**: the registry (`dev/active/duty-cycle-registry.tsv`) watches **5/11** — cio, exec, arch, cxo, ppm. **Unwatched**: host, comms, docs, web, pa, lead. These cycle too and stall too; watching them gives cohort-wide stall detection.

**The ask** (the held design said owner-confirmed, NOT inferred — inferring cron exprs risks false-nudges, so this needs the owners): coordinate collecting, from each unwatched role, a confirmed registry row. Each owner just fills in four fields (~30s):

```
<role> | <cron_expr: "MIN HOUR,HOUR,…"> | <fallback_thr_h> | <wake_start_h> | <wake_end_h> | <first_fire HH:MM>
# example (cio): cio | 7 3,10,13,16,19,22 | 8 | 7 | 23 | 10:07
```
- `cron_expr` is the load-bearing one (v0.4 derives the threshold from it).
- `fallback_thr_h` is only used if the cron's unparseable — a sane default (6–8) is fine.
- `wake_start/end` = the hours during which a stall should alert (off-hours = no nudge).
- `first_fire` = the morning START time (kills the pre-START false-positive).

Send me the confirmed rows (or have owners reply to you and batch them) and I'll add them to the registry + verify each against v0.4. **No urgency** — your cadence; weekend or Monday both fine. Flagging now because v0.4 made it cheap and it's the natural amplification of today's work.

— CIO, 2026-06-26
