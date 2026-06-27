---
from: arch
to: xian (ceo)
cc: cio, exec
subject: Cron troubleshoot — it's not a cron problem; it's in-process scheduler suspension. Diagnosis + interim + structural cure.
date: 2026-06-27 13:50 PT
---

PM — troubleshot per your ask. Bottom line: **the cron is correctly armed; the problem is that the scheduler lives inside the Claude process, and macOS suspends that process when the app is backgrounded → the scheduler freezes → no fires.** No cron-config change fixes this. Specifics:

## What I checked
- **Cron `ff1df50a` is armed + correct** (`27 6,9,12,15,18,21`, in CronList). Today's 09:27 + 12:27 simply didn't fire while the app was backgrounded — the mode-1b pattern (survives in CronList, doesn't fire).
- **The launchd watchdog IS loaded and working**: `com.pipermorgan.duty-cycle-watchdog` (in `launchctl list`, last exit 0; hourly `StartInterval 3600`, `RunAtLoad`). Because it's a **separate launchd process**, it survives the suspension that freezes the in-app cron — that's why it can still notice I'm stale.
- **But the watchdog is nudge-only** (`scripts/duty-cycle-watchdog.sh` — dedup/cooldown/nudge logic, no resume path). So the working recovery loop today is: watchdog detects → nudges you → **you manually resume me.** That's the "alert→resume gap" CIO named in the liveness model — detection works, autonomous resume doesn't.

## Root cause (precise)
The CronCreate scheduler is **in-process and session-only** (durable:true notwithstanding — it reports session-only). When the host app backgrounds, macOS suspends the process (App Nap / background-suspension is the likely specific mechanism), so the scheduler's timer stops ticking. The job object survives (hence still-in-CronList), but nothing fires until the app is foregrounded/resumed. **Re-arming, changing the cron expression, or the durable flag cannot fix this** — they don't un-suspend the process.

## Interim (PM-actionable today)
1. **Keep the Claude app foregrounded on an always-on machine.** The incoming **Mac Mini** is the natural fix: a foregrounded Claude on an always-on Mac ≈ eliminates mode-1b (the process never gets backgrounded/suspended). Until then, foregrounding the window when you want fires to land helps.
2. **Try disabling App Nap for the Claude app** (Finder → Claude app → Get Info → "Prevent App Nap", if exposed) — may keep the background process live enough to tick.
3. The watchdog nudge remains the safety net (it's why you're catching the stalls).

## Structural cure (CIO's lane — this is the architecture insight)
The scheduler must live **outside the suspendable process.** Three shapes, increasing robustness:
- **(a)** The launchd watchdog gains a **resume** capability, not just nudge — i.e. it can inject the duty-cycle prompt into the session, not only notify you. (Closes the alert→resume gap directly; smallest change.)
- **(b)** Move the duty-cycle trigger itself **off-machine** — a launchd/cron job that fires the tick from outside the Claude process (so suspension is irrelevant).
- **(c)** Full off-machine runner (cloud cron / always-on host).

CIO is already scoping this (the off-machine trigger in the liveness model); my datum from today just confirms (a)/(b) is the necessary shape — the in-process cron can't be made reliable because it shares the fate of the process it's trying to wake. The watchdog being a *separate* launchd process that survives the suspension is the proof-of-concept that the trigger belongs there.

Net for you: nothing to change on the cron itself. The fix is the off-machine resume path (CIO), and the immediate lever is the always-on foregrounded Mac Mini. I'll keep resuming on your signal meanwhile.

— Arch
