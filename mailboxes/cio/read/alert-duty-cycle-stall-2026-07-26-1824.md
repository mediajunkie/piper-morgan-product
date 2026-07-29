---
from: duty-cycle-watchdog (automated)
to: cio
date: 2026-07-26
subject: ⚠️ Piper Morgan: duty-cycle stall — lead
priority: high — automated freeze-watcher nudge; fold into carry-forward for the attention rollup
---

# ⚠️ Piper Morgan: duty-cycle stall — lead

duty-cycle stall (STALE lead 5h (dyn-threshold 5h wake-window-aware; cron '17 6,9,12,15,18,21')). The cron object likely survives; the session needs a prod/resume to wake it.

- **Detected**: 2026-07-26 18:24:10 (freeze-watcher hourly run); thresholds per `dev/active/duty-cycle-registry.tsv`.
- **Newly nudge-worthy**: lead   ·   **all currently stale**: STALE lead 5h (dyn-threshold 5h wake-window-aware; cron '17 6,9,12,15,18,21')
- **Action for PM**: re-prod the listed role's session. If many at once, wake the machine/app — one wake covers it. (PM likely already saw this via the desktop notification or Slack — this memo is the durable copy.)
- **Action for CIO** (reading this first): fold into `dev/active/cio-carry-forward.md`'s PM-attention section if still relevant by the time you see it — Exec's cohort-attention-rollup reads the carry-forward directly, so that's how this reaches PM if the other two belts were missed.

*(Automated nudge — duty-cycle-watchdog.sh. Dedup'd: re-pings ~6h while still stale. The nudge belt PM asked for 2026-06-20; both belts — desktop + this memo. Routed to CIO's inbox, not PM's, since 2026-07-12 (PM retired direct-inbox monitoring) — see the Belt-2 code comment above for the full relay path.)*
