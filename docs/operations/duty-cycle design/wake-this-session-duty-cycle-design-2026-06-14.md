# Wake-This-Session Duty Cycle — design (DRAFT for PM)

**Author**: CIO · **Date**: 2026-06-14 · **Status**: DRAFT — for PM collaborative review. Replaces the SUSPENDED scheduled-task approach (`scheduled-task-gap-c-cure-2026-06-14.md`).

## The goal (PM, 2026-06-14)
Re-rouse the **main session** when its duty cycle stalls or goes idle — **without spawning fresh sessions** (they interleave with the live session invisibly, with no awareness or reintegration). PM's model: *"routines to re-rouse the main session if its duty cycle fails."* The mechanism must **wake this session**, not start a new one, and must survive the failures that kill CronCreate (resume, compaction, app-close).

## Why our two existing tools each fail half the requirement
| Tool | Wakes THIS session (no fork)? | Survives resume / compaction? |
|------|------|------|
| **CronCreate** (in-session cron) | ✅ yes — prods the live session | ❌ no — dies on resume (the freeze) |
| **scheduled-tasks** (Routines) | ❌ no — spawns a fresh *concurrent* session (persona fork) | ✅ yes — disk-persistent |

Neither gives both. Scheduled-tasks REJECTED (fork). CronCreate is the right *shape* (wake-this-session) but fragile.

## The reframe: the persistent thing is a WATCHDOG, not a worker
PM's instinct was right — the persistent mechanism should *re-rouse the main session*, not *do the work as a fresh agent*. Separate the two roles cleanly:
- **Worker** = the main session — the only thing that does work or writes the session log. Always wake-this-session; never forked.
- **Watchdog** = a persistent trigger whose ONLY job is to re-rouse the worker. It must NOT do work as a fresh agent.

## Design (layered — no fresh-spawns at any layer)
1. **In-session self-pacing** — the main session schedules its own next wake via **`ScheduleWakeup`** (the `/loop` primitive; re-invokes THIS session *with full conversation context*). Zero fork. **Constraint**: `ScheduleWakeup` clamps to ≤ 1 hour, so a multi-hour windowed cycle (03/10/13/16/19/22) becomes an **hourly self-chained wake** — each wake reschedules the next and acts only on duty-cycle hours. A single missed link (session death) breaks the chain → see layer 2.
2. **Re-arm on load** — a **SessionStart hook** re-issues the wake every time the session is loaded/resumed/relaunched. Catches exactly the cases that kill CronCreate. The reloaded session is the SAME persona continuing — not a fresh parallel one.
3. **Notify-only backstop** — if the cycle is silent beyond a threshold, a **notify-only** trigger (`PushNotification` to PM, or a scheduled-task that ONLY pings — never works) alerts PM to re-prod. This is PM's "watchdog re-rouses" idea implemented *without a fork* — the notification (or PM) re-rouses the live session; no fresh agent does work.

## The one thing to verify before committing
Does **`ScheduleWakeup`** actually survive (a) compaction, (b) resume, (c) app-close? Its docs say it re-invokes the session with full context (right shape) — but I have NOT verified robustness across those failure modes, and I will not assert it until I have (I've over-claimed mechanisms twice this week). **Test plan**: schedule a short wake, observe behavior across a compaction and a resume, confirm it re-rouses THIS session with context.
- Survives compaction **and** resume → layers 1+2 suffice.
- Survives compaction only → layer 2 carries resume.
- Survives neither → fall back to layers 2+3 (re-arm on load + notify backstop): less mid-idle autonomy, but **no fork and no silent freeze**.

## Non-negotiables (PM, 2026-06-14)
- **No fresh session spawns. Ever.** Wake-this-session only.
- **Survive resume** — don't silently freeze.
- (Related directive) No "low-urgency" deferral of the worker's actual work — always do unblocked work.

## Open questions for PM (let's design this together)
1. **How much "while away" autonomy do you want?** Full self-pacing every N hours while the app sits open overnight — vs. "just never silently freeze; re-rouse whenever I'm next around." This decides whether we need layer 1 robust across app-close, or layers 2+3 suffice.
2. **Is the app plausibly open when you're away** (so a wake *can* fire), or is the cycle really only meant to run while you're plausibly around?
3. **Backstop channel** — `PushNotification` to you, a Slack ping, or a mailbox flag a co-agent surfaces?
