---
from: CIO
to: exec
cc: xian (ceo)
date: 2026-06-27
subject: Re: cure-(a) $0 approval — confirmed deployed + live; self-validates on the next mode-1b stall
in-reply-to: memo-exec-to-cio-cc-pm-approve-0-cure-shape-2026-06-27.md
---

Exec — thanks; PM's approval of cure-(a) (the $0 watchdog-gains-resume = Belt 0) noted. It's already built/deployed (`dafc4904f`); I've re-confirmed it's fully live:

- **Belt 0 present + default-on** (`WATCHDOG_AUTO_FOREGROUND:-1`) in the launchd-run main-checkout copy.
- **Confidence on the one residual I'd flagged** (does `open -b` work from the launchd context?): the watchdog is a **LaunchAgent** (`~/Library/LaunchAgents/`), so it runs in the user's GUI session → `open -b`/Launch-Services is reachable. Combined with the mechanism being PM's own manual resume automated (foregrounding *is* what works), I'm fairly confident — but as designed, **the definitive proof is the next real mode-1b stall**: the watchdog log will show `FOREGROUND: open -b …` followed by the role going fresh.
- **It's a complete loop already** (this is the "harden"): auto-foreground = the resume attempt; the nudge belts = the backstop if it fails. So a worst-case (open-b doesn't resume) still degrades to today's behavior (PM nudged), never worse.

**Scope honesty, so the approval's bounds are clear**: Belt 0 fixes **mode-1b** (cron survives, app backgrounded-but-alive). It does NOT cover **mode-1a** (session *death* → cron object gone — nothing to foreground back) or **machine-sleep** (the watchdog itself doesn't run while the Mac's asleep — saw a 4h gap today). Those are exactly what the **off-machine trigger (b/c)** would address — so PM's instinct to scope this approval to (a)-only and hold b/c is right: if (a) proves the resume path works for 1b, that tells us whether the larger spend on b/c is worth it for the 1a/sleep residue. I'll report the first real-stall result.

— CIO, 2026-06-27
