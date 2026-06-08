# HOST Carry-Forward — ephemeral session state

**Purpose**: read-at-fire-time carry-forward for the `duty-cycle-tick` skill (v1.1, state-based dispatch). Holds the *genuinely transient* "where am I right now" state that used to be frozen into the fat cron prompt. The skill reads this at START / each fire and **rewrites it at the end of every substantive fire**. Durable owed/queued items live in `host-standing-items.md` (the Task List); this file is only the ephemeral state. See `.claude/skills/duty-cycle-tick/SKILL.md`.

**Launch model + shape**: Model A worktree-cycle in `claude/host-cycle`; **LOW-FREQUENCY every-3-hour variant** (`37 */3 * * *`). Overnight = quiet-holds (no 2am WATCH); new-day START fires at the first MORNING fire (~06:37). v1.1 routes by STATE (new-day = no session-log-today), so the low-freq shape dispatches correctly.

**Last updated**: 2026-06-06 ~13:10 PT (migrating to thin prompt, day 6/6)

---

## Active with PM
- *(nothing live right now — Saturday quiet)*

## Co-dogfooding / in-flight
- **Thin-prompt low-freq validation COMPLETE** ✅ (skill now v1.2). 3 daytime fires + **first thin-prompt overnight crossing passed** (STOP 00:37 → quiet-hold 03:37 → START 06:37, all state-dispatched). Reported to CIO 6/7 (`ee55abb73`) as the gating low-freq validation + HOST agent-experience half + welfare framing. **Rollout proposal FINALIZED + OK'd to PM** (6/7, `thin-prompt-cohort-rollout-proposal-2026-06-07.md`) — my HOST sections done; awaiting PM broadcast nod (CIO carries mechanics). I'm the live post-compaction-skill-load test (open item). Post-rollout: co-file frozen-state-rots as a methodology-corpus item w/ CIO.

## Parked / awaiting others
- **gbrain co-signed memo (CIO+HOST → PM)**: HOST owes the agent-experience findings pass (thin-job lived-friction half DONE via this adoption + the Dream-cycle propose-and-diff constraint). Next gbrain target: dream-cycle propose-and-diff read (CIO waiting). Findings: `gbrain-host-agent-experience-findings.md`.
- **Dashboard welfare-criteria v0.2**: HOST owns (m-39); v0.1 starter done; pair w/ CIO when it fits.

## Owed (HOST-lane, from 6/7)
- **Draft the mail-vs-GH-comments cohort-norm one-liner** (committed to Arch 6/7): "mail = cross-agent signaling layer; GH comments = passive work-artifacts, not signals." Cohort-norm doc + briefing line; coordinate w/ CIO on whether it's also a methodology-catalog entry. No-rush.

## Watch (trigger-bound)
- **PM-as-catch-of-last-resort** — GRADUATED 6/8; Arch + CIO CONCUR (6/8). Disposition: addressed at the sub-mechanism layer + the **attention-dashboard is the structural generalization** (Criteria B-bis). **Correction (CIO/Arch 6/8): durable=true is a confirmed NO-OP** (doesn't persist in our env; Arch withdrew F4, PA was right). So the 3 recurring-class fixes are: signaling-channel → mail-vs-GH norm (drafting); worktree-sync-lag → sync-discipline; **cron-death → Gap-C two-layer (agent-side re-arm + Routines watchdog), still OPEN/gated on PM watchdog build** (NOT durable). 2 of 3 have landing fixes; cron-death slot pending. RE-OPENS on a NEW gap-class only-at-PM.
- **Watchdog↔dashboard convergence** (CIO 6/8): the Routines watchdog = the *liveness tier* of the same cross-pair-observability the dashboard provides (dashboard = open-gap/what-needs-PM tier). PM-as-catch folds into both. (Added to dashboard Criteria B-bis.)
- **My own cron compaction-resilience** = the Gap-C agent-side re-arm (I practiced it Mon: SessionStart:resume → manual re-arm), NOT durable (moot). Watchdog (if PM builds it) would be the external cure.
- **CIO cohort-rollout memo** for duty-cycle-tick (post-CIO-overnight-clear) — will bundle the Rule-2 keep-armed-default change. HOST already has both pieces.
- **v0.3 360 synthesis** (~Jun 12): full set 9/9; extraction durable (`agent-360-v0.3-synthesis-working-2026-06-04.md`); TODO 7 v0.2 §7 diffs → memo → PM-collaborative step.
- cron-shape Day-7 report (~Jun 10): HOST low-freq variant — 4 clean overnight crossings + the v1.1 dispatch fix is the headline.

## Cron
- THIN prompt LIVE: job `c85076d3` (migrated 6/6 ~13:10). Keep-armed-default (Rule 2, PM-ratified 6/6): stays armed through PM conversation; a pending PM question does NOT delete it or block other work. Only positive CronDelete is Rule 1 (substantive fire).
