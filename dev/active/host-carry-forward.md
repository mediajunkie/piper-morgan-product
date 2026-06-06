# HOST Carry-Forward — ephemeral session state

**Purpose**: read-at-fire-time carry-forward for the `duty-cycle-tick` skill (v1.1, state-based dispatch). Holds the *genuinely transient* "where am I right now" state that used to be frozen into the fat cron prompt. The skill reads this at START / each fire and **rewrites it at the end of every substantive fire**. Durable owed/queued items live in `host-standing-items.md` (the Task List); this file is only the ephemeral state. See `.claude/skills/duty-cycle-tick/SKILL.md`.

**Launch model + shape**: Model A worktree-cycle in `claude/host-cycle`; **LOW-FREQUENCY every-3-hour variant** (`37 */3 * * *`). Overnight = quiet-holds (no 2am WATCH); new-day START fires at the first MORNING fire (~06:37). v1.1 routes by STATE (new-day = no session-log-today), so the low-freq shape dispatches correctly.

**Last updated**: 2026-06-06 ~13:10 PT (migrating to thin prompt, day 6/6)

---

## Active with PM
- *(nothing live right now — Saturday quiet)*

## Co-dogfooding / in-flight
- **Thin-prompt PoC adoption**: HOST on thin cron (`c85076d3`) + this carry-forward, co-dogfooding the **low-freq path** of `duty-cycle-tick` v1.1. **First thin-prompt fire (16:07) PASSED** ✅ — thin prompt → Skill(duty-cycle-tick) loaded, state-dispatch routed correctly (session-log-exists + daytime → WORK PARTS, NOT misrouted to START), carry-forward read from file cleanly. Remaining verification: 18:37/21:37 daytime fires, then the **overnight crossing** (the real low-freq test, since v1.1 hasn't cleared an overnight on any cron). Revert to fat prompt if anything misroutes.

## Parked / awaiting others
- **gbrain co-signed memo (CIO+HOST → PM)**: HOST owes the agent-experience findings pass (thin-job lived-friction half DONE via this adoption + the Dream-cycle propose-and-diff constraint). Next gbrain target: dream-cycle propose-and-diff read (CIO waiting). Findings: `gbrain-host-agent-experience-findings.md`.
- **Dashboard welfare-criteria v0.2**: HOST owns (m-39); v0.1 starter done; pair w/ CIO when it fits.

## Watch (trigger-bound)
- **CIO cohort-rollout memo** for duty-cycle-tick (post-CIO-overnight-clear) — will bundle the Rule-2 keep-armed-default change. HOST already has both pieces.
- **v0.3 360 synthesis** (~Jun 12): full set 9/9; extraction durable (`agent-360-v0.3-synthesis-working-2026-06-04.md`); TODO 7 v0.2 §7 diffs → memo → PM-collaborative step.
- cron-shape Day-7 report (~Jun 10): HOST low-freq variant — 4 clean overnight crossings + the v1.1 dispatch fix is the headline.

## Cron
- THIN prompt LIVE: job `c85076d3` (migrated 6/6 ~13:10). Keep-armed-default (Rule 2, PM-ratified 6/6): stays armed through PM conversation; a pending PM question does NOT delete it or block other work. Only positive CronDelete is Rule 1 (substantive fire).
