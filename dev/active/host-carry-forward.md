# HOST Carry-Forward — ephemeral session state

**Purpose**: read-at-fire-time carry-forward for the `duty-cycle-tick` skill (v1.1, state-based dispatch). Holds the *genuinely transient* "where am I right now" state that used to be frozen into the fat cron prompt. The skill reads this at START / each fire and **rewrites it at the end of every substantive fire**. Durable owed/queued items live in `host-standing-items.md` (the Task List); this file is only the ephemeral state. See `.claude/skills/duty-cycle-tick/SKILL.md`.

**Launch model + shape**: Model A worktree-cycle in `claude/host-cycle`; **LOW-FREQUENCY every-3-hour variant** (`37 */3 * * *`). Overnight = quiet-holds (no 2am WATCH); new-day START fires at the first MORNING fire (~06:37). v1.1 routes by STATE (new-day = no session-log-today), so the low-freq shape dispatches correctly.

**Last updated**: 2026-06-06 ~13:10 PT (migrating to thin prompt, day 6/6)

---

## Active with PM
- *(nothing live right now — Saturday quiet)*

## Co-dogfooding / in-flight
- **Thin-prompt low-freq validation COMPLETE** ✅ (skill now v1.2). 3 daytime fires + **first thin-prompt overnight crossing passed** (STOP 00:37 → quiet-hold 03:37 → START 06:37, all state-dispatched). Reported to CIO 6/7 (`ee55abb73`) as the gating low-freq validation + HOST agent-experience half + welfare framing. **Rollout forward-item (CIO 6/8)**: fold the recurring-audit **owner-poll** into the thin-prompt rollout's per-agent setup as a mechanical Task-Loop line ("poll your recurring-audit label") — so the cohort-norm ("every recurring auto-issue names its owner; the owner's cycle polls its label", now m-36 Class-2) lands as mechanism, not per-agent vigilance. HOST already has the manual version (carry-forward standing item). Add to the rollout when it goes cohort-wide.
**Rollout proposal FINALIZED + OK'd to PM** (6/7, `thin-prompt-cohort-rollout-proposal-2026-06-07.md`) — my HOST sections done; awaiting PM broadcast nod (CIO carries mechanics). I'm the live post-compaction-skill-load test (open item). Post-rollout: co-file frozen-state-rots as a methodology-corpus item w/ CIO.

## Parked / awaiting others
- **gbrain co-signed memo (CIO+HOST → PM)**: HOST owes the agent-experience findings pass (thin-job lived-friction half DONE via this adoption + the Dream-cycle propose-and-diff constraint). Next gbrain target: dream-cycle propose-and-diff read (CIO waiting). Findings: `gbrain-host-agent-experience-findings.md`.
- **Dashboard welfare-criteria v0.2**: HOST owns (m-39); v0.1 starter done; pair w/ CIO when it fits.

## Done (Role Health Check #1178 + label rename, 6/8 PM-directed)
- ✅ Methodology v2.0 + workflow + DRY operating-model pointer + HOST briefing refresh (`aa516fe92`).
- ✅ **Label migrated org-wide** `sapient-resources`→`sapient-trust` (`50abdaad4` + GH): issues #978/#1077/#1178 relabeled (bodies untouched), old label deleted, forward template-spec fixed. ~390 historical mentions of the retired name LEFT INTACT (anti-anachronism per PM).
- **AWAITING PM**: (1) privacy decision on `dev/alpha/` — it's git-tracked but roster claims "gitignored" (tester PII committed contrary to expectation); my alpha-tiering doc held uncommitted at `dev/alpha/host-alpha-reping-tiering-2026-06-08.md` pending this. (2) wire #1178-recurring to cc/assign HOST. (3) thin-prompt rollout nod.

## Owed (HOST-lane, from 6/7)
- **Draft the mail-vs-GH-comments cohort-norm one-liner** (committed to Arch 6/7): "mail = cross-agent signaling layer; GH comments = passive work-artifacts, not signals." Cohort-norm doc + briefing line; coordinate w/ CIO on whether it's also a methodology-catalog entry. No-rush.

## Standing cycle responsibility (recurring-audit polling — GH doesn't notify agents)
- **Poll for open `sapient-trust` role-health-check issues** periodically (≈weekly, per the 4-week audit cadence): `gh issue list --label sapient-trust --state open`. Auto-generated recurring audits assign to PM (agents have no GH login) — HOST's cycle is the mechanism that catches them. Fill on the cycle, post to the issue. (This is the owner-side half of the recurring-workflow reminder; workflow-side reminder added to `role-health-check.yml` 6/8.)

## Watch (trigger-bound)
- **v0.3 360 synthesis (~Jun 12)**: extraction + **diff-against-baseline DONE** (D1–D7 in `agent-360-v0.3-synthesis-working-2026-06-04.md`). Remaining: draft summary memo + the **PM-collaborative "what's worth changing" step** (do WITH PM, don't pre-decide). Headline candidates: mailbox-bridge dominant convergence (T1); the duty cycle was the unpredicted biggest change (D3); briefing-currency the persistent gap (D6).
- **Alpha re-ping wave 1**: PM pinging **Jake Krajewski + Rebecca Refoy** next (6/8) — both setup-friction-blocked (same final-step blocker as Ted; easier setup = their direct unblock). PM will report back. On reply: log to human-network, update tester status, assess whether Tier-2/3/4 waves follow. Roster: `dev/alpha/alpha-tester-roster.md` (PM-owned, ~4.5mo stale — offered annotation, PM holding).
- **PM-as-catch-of-last-resort** — GRADUATED 6/8; Arch + CIO CONCUR (6/8). Disposition: addressed at the sub-mechanism layer + the **attention-dashboard is the structural generalization** (Criteria B-bis). **Correction (CIO/Arch 6/8): durable=true is a confirmed NO-OP** (doesn't persist in our env; Arch withdrew F4, PA was right). So the 3 recurring-class fixes are: signaling-channel → mail-vs-GH norm (drafting); worktree-sync-lag → sync-discipline; **cron-death → Gap-C two-layer (agent-side re-arm + Routines watchdog), still OPEN/gated on PM watchdog build** (NOT durable). 2 of 3 have landing fixes; cron-death slot pending. RE-OPENS on a NEW gap-class only-at-PM.
- **Watchdog↔dashboard convergence** (CIO 6/8): the Routines watchdog = the *liveness tier* of the same cross-pair-observability the dashboard provides (dashboard = open-gap/what-needs-PM tier). PM-as-catch folds into both. (Added to dashboard Criteria B-bis.)
- **My own cron compaction-resilience** = the Gap-C agent-side re-arm (I practiced it Mon: SessionStart:resume → manual re-arm), NOT durable (moot). Watchdog (if PM builds it) would be the external cure.
- **CIO cohort-rollout memo** for duty-cycle-tick (post-CIO-overnight-clear) — will bundle the Rule-2 keep-armed-default change. HOST already has both pieces.
- **v0.3 360 synthesis** (~Jun 12): full set 9/9; extraction durable (`agent-360-v0.3-synthesis-working-2026-06-04.md`); TODO 7 v0.2 §7 diffs → memo → PM-collaborative step.
- cron-shape Day-7 report (~Jun 10): HOST low-freq variant — 4 clean overnight crossings + the v1.1 dispatch fix is the headline.

## Cron
- THIN prompt LIVE: job `c85076d3` (migrated 6/6 ~13:10). Keep-armed-default (Rule 2, PM-ratified 6/6): stays armed through PM conversation; a pending PM question does NOT delete it or block other work. Only positive CronDelete is Rule 1 (substantive fire).
