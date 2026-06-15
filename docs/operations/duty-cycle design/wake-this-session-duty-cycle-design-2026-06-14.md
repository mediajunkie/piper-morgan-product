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

---

## ✅ PM decisions (2026-06-14) — chosen scope: simplest / never-silently-freeze
PM: *"start with the simplest thing that could work (never silently freeze) — if we get good at that, we can try harder things."*
- **Scope**: NOT full self-pacing (layer 1) yet. The bar is: the cycle **never freezes silently** — failures become **loud** (PM alerted) and recover ASAP on the next session load / machine restart.
- **Environment (PM)**: the app *tends* to be open + powered while PM is away (a watcher can usually run), with exceptions. **No cloud** → the system only works while the app is running with machine access; no 24/7 expectation. **On machine wake/restart → resume ASAP.**
- **Alert channel (PM)**: **PushNotification + Slack** (belt-and-suspenders).

### The simplest concrete mechanism
1. **Heartbeat = the role's routine commits to `main`** (push-to-main-routinely is now a standing order). A live cycle commits regularly; a frozen one stops. No new heartbeat file. Check implemented: `scripts/duty-cycle-freeze-check.sh` (per-role last-tagged-commit staleness during waking hours → emits `STALE <role> <hours>h`).
2. **Persistent notify-only watcher** — survives resume; during waking hours runs the check; on STALE → PushNotification + Slack. **Does ZERO work** (reads + pings only). The one safe kind of background job: a smoke detector, never a worker. (The rejected design had the background job *do work* as a forked persona — that's the line we don't cross.)
3. **Resume-ASAP on restart** — handled by the duty-cycle **START self-heal**: when a session loads (incl. after app/machine restart) the agent re-arms its in-session cron. Honest limit: this needs *a session to load* (bash hooks can't manage crons), so realistic recovery = "as soon as a session is next active after restart," not instantaneous.

### Implementation — recommending the zero-agent path
The watcher must survive resume → either **(A)** a notify-only scheduled-task (fresh agent that does nothing but read+ping) or **(B)** a pure **launchd** OS-script (no Claude agent at all). **Recommend (B)** — it honors "no fresh sessions" completely, and **Slack itself pushes to PM's phone** (phone-reach without Claude PushNotification), with a macOS desktop notification as the second belt. Cost: a launchd plist + the check script + Slack-send via the keychain bot token. Fall back to (A) only if PM specifically wants Claude push-to-phone. **Building (B) next.**

---

## ✅ Implementation — SHIPPED 2026-06-15 (desktop belt live; Slack belt pending PM webhook)
Built (B), the zero-agent launchd path. **Loaded + tested.**
- **Freeze-check**: `scripts/duty-cycle-freeze-check.sh` — per-role last-commit staleness (CIO-only; cohort extension needs active→silent detection, see caveat above).
- **Watcher**: `scripts/duty-cycle-watchdog.sh` — runs the check; on STALE → macOS desktop notification (always) + Slack (if a webhook is configured). **Zero Claude agents**; touches no repo state but its own audit log (`dev/active/duty-cycle-watchdog.log`).
- **launchd**: `scripts/launchd/com.pipermorgan.duty-cycle-watchdog.plist` (version-controlled; installed to `~/Library/LaunchAgents/`). `StartInterval` 3600 (hourly) + `RunAtLoad` → **fires on login/wake** = "resume ASAP after the machine wakes," natively. Loaded + verified (`launchctl list | grep pipermorgan`). Tested: a forced-stale run fired the desktop notification + logged `ALERT: STALE cio 0h`.
- **Enable the Slack belt (phone-reach)**: create a Slack incoming-webhook URL and write it to `~/.piper-watchdog-slack-webhook`. The watcher picks it up automatically — Slack's own app then pushes the alert to PM's phone (no bot-token/user-id wiring; the bot token is user-scoped per ADR-058, so the webhook is the clean no-agent path).
- **Next**: (1) PM drops the Slack webhook → phone belt active. (2) Cohort extension: active→silent transition detection so it watches all roles without false-flagging quiet/unmigrated ones. (3) Later "try harder things": `ScheduleWakeup` self-pacing (verify resume-survival first).
