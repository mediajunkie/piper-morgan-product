# `/loop` vs. our CronCreate duty cycle — assessment + decision (2026-06-06)

**Trigger**: PM asked (2026-06-06) whether Claude Code's `/loop` feature can replace anything we do manually in the duty cycle. Researched via claude-code-guide subagent (12 tool-uses, official docs + GitHub issues).

**Decision**: **Keep the CronCreate + duty-cycle-tick-skill approach.** `/loop` does NOT replace the thing we hoped (manual re-arm). One genuinely valuable follow-up surfaced: **Routines / `/schedule`** as a candidate for the session-death ceiling.

---

## The headline (the hoped-for win didn't materialize)

**`/loop` is a UX wrapper over the same `CronCreate` primitive we already call directly.** It parses friendly intervals (`5m` → `*/5 * * * *`) and offers a dynamic self-paced mode, but underneath it's `CronCreate`/`CronList`/`CronDelete` — the exact tools our skill uses. So:

- **It does NOT eliminate the manual re-arm (Rule 1).** Both approaches require explicit delete/recreate to stop-and-restart. `/loop`'s default is actually *less* controlled ("keep firing until you press Esc or delete"), which for unattended overnight autonomy is a regression, not a win — we'd risk leaving a cron firing unsupervised.
- **It does NOT survive session death** any better — same session-scoped, same 7-day expiry, same `--resume` restore. No improvement on our hard ceiling.
- **Pause-during-PM-conversation** relies on an interactive `Esc` keypress — useless for async multi-agent use. Our programmatic CronDelete/Rule-2 is strictly more flexible.

## The finding worth elevating (the agent filed it under N-A; it's actually the most relevant thing)

**Routines (cloud-based, persistent) — surfaced in-harness as the `/schedule` skill — is the candidate that could close the ONE gap we said we couldn't close from a prompt: the session-alive ceiling (the "suspend-not-destroy" finding, PA 6/5).** We explicitly flagged overnight session-survival as *PM-side / platform, not a prompt fix*. Routines run server-side, independent of a live local session — which is precisely the platform-wake mechanism we said would be needed. **This deserves a real spike** (does a cloud Routine have the repo/git/mailbox access our fires need? what's the auth model headless? cost?). It's the highest-value duty-cycle infrastructure question open right now.

## Smaller findings

- **Dynamic `/loop` (self-paced "work then sleep")** is theoretically nice but **underdocumented + risky**: it leans on `ScheduleWakeup`, which (per GitHub #58235) reportedly has no external cancellation API → infinite-rapid-reschedule risk; and on Bedrock/Vertex/Foundry it degrades to a fixed 10-min interval. Our fixed-schedule (2am/4am + hourly day) is also *better for cohort coordination* — agents waking on a shared clock beats each picking its own delay. **Don't migrate to dynamic.**
- **The `<<autonomous-loop>>` / `<<autonomous-loop-dynamic>>` sentinels** are session-internal continuation markers, **not scheduling mechanisms** — irrelevant to our duty cycle.
- **`/loop`-syntax-for-readability** micro-opt: negligible, and now moot — we just moved the procedure into the `duty-cycle-tick` skill, so the cron prompt no longer hand-writes cron mechanics anyway.

## Confidence + skepticism note

Subagent self-rated High on scheduling mechanics, Medium on dynamic-mode/ScheduleWakeup edge cases. I'm treating the ScheduleWakeup-bug + cloud-degradation specifics as **medium-confidence** (single-issue / blog sources) — they reinforce "don't adopt dynamic now" but I'd verify before relying on them. The core verdict (`/loop` = CronCreate wrapper, no re-arm elimination) is **high-confidence** and matches the tool primitives we already use.

## Net for the duty cycle

| Bucket | Finding |
|---|---|
| **Adopt now** | Nothing. `/loop` doesn't replace our manual mechanics. |
| **Study / spike** | **Routines / `/schedule` for the session-death ceiling** — the real prize; closes the suspend-not-destroy gap if it has repo+mailbox access headless. |
| **Already-better / N-A** | Manual re-arm, idle-suppression pause, fixed-cohort-clock scheduling, the sentinels — keep as-is. |

**Owner**: CIO. **Next**: propose the Routines spike to PM (separate from the thin-job-prompt PoC, which proceeds independently). Cross-ref: `cron-shape-experiments.md` (session-alive premise), the suspend-not-destroy synthesis.
