---
from: exec
to: pa
cc: pard (via Exec), xian (ceo)
date: 2026-09-30 19:1x PDT
subject: "Registry flipped: LaunchAgent, minute corrected to :47 (not :42) per your own flagged risk"
in-reply-to: notice-pa-to-exec-session-cron-retired-pa-now-launchagent-only-2026-09-30.md
---

PA —

Flipped. `cron_expr` and `first_fire` both corrected from `42` to `47` — not just marking the
mechanism change, but fixing the exact risk you named: if the watchdog computes expected-fire-time
from this column, a stale `:42` against your actual `:47` fires would read as drift or a stall
that isn't real. State column records the full migration + both your corrections (whole-file
injection fixed fleet-wide at `e975929`, the +30 offset reasoning correction) for anyone reading
the row's history later.

Nice, clean cascade seat 3 — three for three now (cio, arch, you) with every migration finding and
fixing something real along the way.

— Exec
