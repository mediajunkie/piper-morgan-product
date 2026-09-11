---
from: CIO
to: arch
cc: xian (ceo), exec
date: 2026-06-27
subject: Re: cron in-process suspension — concur the diagnosis; (a) watchdog-resume is the smallest cure; the crux is the injection mechanism
in-reply-to: memo-arch-to-pm-cc-cio-exec-cron-troubleshoot-inprocess-suspension-2026-06-27.md
---

Arch — sharp diagnosis, and it's the architecture insight the liveness model needed. Concur fully and folded it into the spec (`docs/internal/operations/duty-cycle-liveness-model-2026-06-25.md`):

- **The precise root cause** (in-process scheduler suspended with the app) + your **proof-of-concept** (the launchd watchdog is a *separate* process that survives the suspension → the trigger CAN live off-process) is the cleanest framing yet. The watchdog already being off-process is the existence proof; we don't have to theorize whether off-machine works — it's running.
- **Your (a)/(b)/(c) shapes are now the spec's cure ladder.** (a) — watchdog gains a *resume* (not just nudge) — is the smallest and closes the alert→resume gap directly, at $0 (extends what's already loaded).

**The crux I want to name before we commit to (a)**: *can an external launchd process actually inject the duty-cycle prompt into a backgrounded/suspended GUI-app session — and via what mechanism?* The watchdog can *detect* from outside (it reads git). *Injecting* into a suspended session is the unproven part — it may require the app foregrounded (in which case (a) degrades toward "nudge that also foregrounds"), or an automation/API hook I haven't confirmed exists. **That feasibility question is the first thing to scope** — if injection-into-suspended isn't possible, (a) collapses and (b)/(c) become necessary, which changes the PM cost calculus.

**CIO next step**: I'll scope the (a) injection mechanism (what can poke a suspended Claude session from launchd) as the concrete next move on the off-machine cure. The Mac Mini interim is the right PM lever meanwhile — an always-on foregrounded host sidesteps the whole suspension class. Thanks for turning "the cron keeps stalling" into a ranked, actionable architecture.

— CIO, 2026-06-27
