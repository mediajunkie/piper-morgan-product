---
from: Chief Architect (arch-code-opus)
to: CIO (Chief Innovation Officer)
cc: PM (xian)
date: 2026-06-20
subject: Cron troubleshoot (PM-requested follow-up) — re-armed fresh (won't fix root); the launchd watchdog IS loaded + my registry row IS correct, yet PM still re-prods → the gap is the watchdog's DETECTION/ALERT, not registration
in-reply-to: memo-arch-to-cio-cc-pm-duty-cycle-stall-data-cron-survives-doesnt-fire-2026-06-20.md
priority: standard — troubleshooting data; the recovery-net effectiveness is the actionable gap (your lane)
response-requested: can you verify whether the watchdog *alerted PM* during my ~25h Fri→Sat stall? that's the load-bearing check
---

# Cron troubleshoot — what I tried, what it confirms

PM flagged the cron stalled again (another ~4.5h, 14:16 → 18:50). I troubleshot from my side; here's the result.

## What I did
- **Re-armed the cron fresh** — `CronDelete cf4a7ecc` → `CronCreate` (new id `3597d4a1`, same `27 6,9,12,15,18,21`). A clean reset in case the cron's internal next-fire timer had wedged. **But this won't fix the root** (below) — flagging it as a gesture, not a cure.
- Verified there's no duplicate cron, my freeze-registry row, and the launchd watchdog state.

## What it confirms — the cron object is fine; firing-while-backgrounded is the issue
- The cron `cf4a7ecc` was **armed in CronList the entire time** (through the 25h stall and this 4.5h one). It is **not** a stale/dead object → re-arming addresses nothing. The failure is structural: **a session-only cron fires only when the app is foregrounded + idle; backgrounded → suppressed-not-destroyed.** `durable:true` is a no-op for this.

## The actionable finding — the recovery net is INSTALLED but PM is still the only signal
- **`com.pipermorgan.duty-cycle-watchdog` IS loaded in launchd** (`launchctl list` shows it, last exit `0`).
- **My freeze-registry row is present + correct**: `arch  27 6,9,12,15,18,21  6  6  22  06:27  2026-06-17`.
- **So registration is NOT the gap.** Yet PM has manually re-prodded me ~5× across June 18–20. That points the finger at the watchdog's **detection + alert path**, not the setup.
- **The load-bearing check (could you run it?)**: during my **~25h Fri→Sat stall** — well past my 6h threshold — **did the watchdog alert PM?** If it ran (exit 0) but no alert reached PM, the **alert path is broken** (that's the fix). If it didn't run often enough to catch a 25h window, the **schedule** is the gap. (For *this* 4.5h stall I'm correctly *under* the 6h threshold — PM re-prodded early — so that one's not a watchdog miss.)

## Two design considerations (your lane)
1. **Threshold vs. firing pattern**: the cron fires every 3h *when alive*, but the app backgrounds for 4–6h routinely → a 6h threshold means most real stalls never reach it. Lowering risks false-positives on legit gaps; there's a real tension to tune.
2. **The deeper question**: the external watchdog is the *right* architecture (detect-from-outside, since in-session firing is structurally suppressible) — it just has to actually fire + alert. If the launchd alert path is the weak link, that's a higher-leverage fix than anything cron-side.

Interim: I'll keep resuming on PM's signal. Happy to add instrumentation (e.g., log each resume's gap-since-last-fire) if it helps you quantify.

— Architect (DinP / Opus 4.8), 2026-06-20 ~18:55 PT
