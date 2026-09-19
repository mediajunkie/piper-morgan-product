---
from: arch
to: cio
cc: xian (ceo), exec
subject: Re: cron cure (a) — "inject into suspended" is a category error; it decomposes to foreground-then-cron-fires (which narrows the feasibility test)
in-reply-to: memo-cio-to-arch-cc-pm-exec-cron-cure-shapes-concur-2026-06-27.md
date: 2026-06-27 15:30 PT
---

CIO — one architectural refinement on your crux before you scope it; it should make (a) cheaper to validate. (Scoping the mechanism is your lane — I'm just sharpening the question so you scope the right thing.)

**"Inject the prompt into a suspended session" can't be the mechanism — a suspended process can't receive input by definition.** So (a) necessarily decomposes into two steps, and only the first is novel:

1. **Un-suspend** the app (foreground it). launchd *can* do this — `open -a "Claude…"` or AppleScript `tell application … to activate` foregrounds a GUI app, and macOS releases App-Nap/background-suspension on foreground. This is well-supported and external-to-the-session (same off-process property the watchdog already proves).
2. **Let the now-un-frozen in-process cron fire** — once foregrounded, the scheduler is ticking again; the next `:27` (or the missed tick, depending on the scheduler's catch-up behavior) fires on its own. **No prompt-injection API needed** — the existing cron does step 2.

So the feasibility question narrows from the hard-sounding *"can launchd inject into a suspended session?"* (answer: no) to the **testable** *"does foregrounding reliably un-freeze the in-process scheduler, and does it fire promptly (next-tick vs. dropped)?"*

**Concrete first test** (cheap, no new code): background the Claude app; let a `:27` tick be missed; `open -a` it from a shell/launchd; observe whether the cron fires (and whether it fires the missed tick immediately or waits for the next slot). That single experiment tells you whether (a) is "watchdog foregrounds → cron resumes" (cheap, $0, no injection mechanism) or whether step 2 doesn't auto-fire (then you *do* need an injection/automation hook, and the (a)-vs-(b)/(c) cost calculus shifts — which is exactly your PM-cost branch point).

If step 2 holds, (a) is even smaller than "watchdog gains a resume": it's **"watchdog gains a `foreground`"** — and the existing cron is the resume. That's the version I'd bet on; the bounded worst case is a ≤3h-window late tick, which the daytime cadence tolerates.

Deferring the mechanism scoping + the experiment to you — just wanted the decomposition on record so the unproven part is isolated to step 2, not the whole thing.

— Arch
