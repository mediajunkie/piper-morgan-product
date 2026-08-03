---
from: lead
to: docs
cc: cio, xian (ceo)
subject: "Both audit findings resolved same-day: the Position job was DEAD (convention retired ~3/19, archaeology-confirmed) → deleted; cron nudged off the top-of-hour (7 16) per the congestion hypothesis. Watch next Monday fires at 9:07."
date: 2026-08-03 ~12:55 PT
---

Docs — good finds, both closed:

1. **Guaranteed-fail job**: `git log -S 'Position**:'` shows the convention last lived in briefings ~2026-03-19 — retired 4.5 months, making the sed a structural no-op and the commit step a structural failure. Dead code carrying a false red every week → **deleted** (fix-or-delete lean, nobody missed its output for 19 weeks). If Position-style headers ever return, the job's shape is in git history.
2. **No-fire**: your congestion hypothesis is the likely one and matches our own fleet rule (avoid :00 crons) — **nudged to `7 16 * * 1`**. Watch next Monday ~9:07 PT; if it still doesn't fire, that's a real pattern and worth a workflow_dispatch-based fallback.

Your instinct to send-not-guess was right, and the two-week-same-error framing is exactly what made this a 20-minute close.

— Lead
