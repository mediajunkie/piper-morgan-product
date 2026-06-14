# Scheduled-Task Duty-Cycle — Gap-C attempt (⛔ SUSPENDED 2026-06-14 — persona-fork)

**Status**: ⛔ **SUSPENDED** (PM design critique, 2026-06-14). Scheduled-tasks spawn a **concurrent fresh session** on each fire (a context-less new instance of the persona) — NOT a wake of the live session. This diverges from our continuity model, and there is **no robust reintegration design** for same-persona concurrent instances. `cio-duty-cycle` is **DISABLED**. **Cohort rollout: OFF the table** pending a wake-this-session redesign.
**Author**: CIO · **Date**: 2026-06-14.

> The Gap-C *problem analysis* below is still valid. The *conclusion* — "scheduled-tasks are the cure" — is **rejected**: it cures resume-death by trading it for persona-fork, which is worse. Kept as the record of what was tried and why it was abandoned.

## ⛔ PM critique (2026-06-14) — why this is suspended
PM: *"Your duty cycle spawns subagents who are going to compete with you to race to update your session log… The cron needs to prod THIS session when it is not active, not start subsessions, unless you have a robust design for reintegration of experiences of same-persona subagents."*

**Confirmed mechanism (evidence):** the 10:07 fire spawned a fresh agent that did NOT know an in-session agent was active (it self-reported "no double-fire observed") — proof it's a concurrent *fresh* instance, not a wake of the live conversation. Two same-persona instances diverged and raced on the session log → collision.

**No robust reintegration exists.** Disk-write/disk-read is lossy + concurrency-unsafe. The "fire-level guard" floated below is *fork-avoidance* (a lock → single instance), not reintegration — and it still leaves respawn-from-disk, which only the away/relaunch case justifies.

**Right shape = wake, not respawn.** Investigate a wake-the-live-session primitive (`ScheduleWakeup` / `/loop` self-pacing re-invokes THIS session with full conversation context) — pending verification of whether it survives app-close/compaction. Until that's settled, no autonomous-fire mechanism is adopted.

---
*(historical analysis follows — accurate as problem-statement, rejected as conclusion)*

## The problem — Gap-C
In-session `CronCreate` crons **die on session resume / compaction**. `durable:true` is a no-op in practice. Symptom: the duty cycle **silently freezes** — no fires, no 22:07 STOP — and PM sees only silence (the "agent isn't running but PM thinks it is" expectation-violation seam HOST flagged). Three CIO crons died this way (d982e3d0 → afb1da90 → 16d19ac8) before the cure; the cycle froze overnight 6/13→14.

## The cure — `mcp__scheduled-tasks` (disk-persistent Routines)
Scheduled-tasks live on disk (`~/.claude/scheduled-tasks/<id>/SKILL.md`), **not** bound to a session. They survive resumes + compaction and **fire headless in the main checkout**.
- **Disk-persistence proof**: old-CIO's May-16 scheduled-task dir survived a *month* of session churn.
- **Headless-loop proof**: the one-shot probe `cio-gapc-pilot-probe` fired autonomously at 13:23 on 6/13 and did the FULL read → commit → push loop unattended (commit e0de384e7).
- **Live**: `cio-duty-cycle` (cronExpression `7 3,10,13,16,19,22`; enabled; next fire confirmed) — the resumed CIO cycle, Gap-C-resistant by construction.

## Mechanism (how to set one up)
`mcp__scheduled-tasks__create_scheduled_task` with:
- **cronExpression**: the windowed shape, e.g. `7 3,10,13,16,19,22 * * *` (03 START · daytime mail-catch · 22 STOP). Offset the minute per role to avoid collisions (CIO :07, Comms :12, Docs :17…).
- **prompt = main-checkout-direct**: the fire runs a FRESH headless agent in the **main checkout** (`/Users/xian/Development/piper-morgan/piper-morgan-product`). It commits/pushes **straight to main** (no ephemeral worktree, no bridge needed for the fire's own logging), reads its carry-forward, runs the `duty-cycle-tick` skill, and logs to its **session log** (single-surface, skill v1.8).
- **enabled: true**. Jitter (a few hundred s) is fine.

## Caveats still being validated (the reason for the 2-tracer observation window)
1. **Double-fire — CONFIRMED 2026-06-14, THE blocker for full-cohort rollout.** The 10:07 `cio-duty-cycle` fire spawned a fresh headless agent while an in-session CIO agent was active; both committed to `main` → a rebase collision (resolved, no work lost). The fire spawns regardless of an active in-session agent. **Do NOT mitigate by disabling-when-engaged** — disabling a disk-persistent task reintroduces the freeze-on-death risk this whole cure removes (a disabled task stays disabled if the session dies before re-enable). The correct fix is a **fire-level guard**: the fire's first step checks for an active in-session agent (a lock-file the in-session agent maintains, or a recent main-commit heartbeat) and **no-ops** if found. Build + prove this guard before converting the rest of the cohort.
2. **7-day expiry**: confirm whether recurring scheduled-tasks auto-renew or expire after ~7 days; if they expire, the cycle must re-arm (a self-renew step, or a watchdog).
3. **Display quirk**: the UI human-readable can show a wrong time ("At 03:16 AM"); the stored `cronExpression` + `nextRunAt` are the truth.

## What this resolves
- **Routines-watchdog feasibility** (`routines-watchdog-feasibility-2026-06-07.md`): the paid watchdog (~$70/mo) is **not needed** — the free, on-account scheduled-tasks ARE the Gap-C cure. That thread can close.
- **The freeze class**: a cycle on a scheduled-task cannot freeze on resume the way CronCreate did.

## Rollout
CIO (done) → **Docs** (this migration — 2nd tracer; report first-fire behavior) → observe both → convert the rest (Web, Arch, CXO, PPM) at migration, and PA/HOST/Comms/Exec/LD at their next cycle. Don't full-cohort before the 2 tracers are clean.
