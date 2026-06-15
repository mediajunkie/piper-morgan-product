# Exec Duty Cycle Escalations / Attention Doc

**Purpose**: the at-a-glance surface PM scans when wondering "is anything Exec-shaped waiting on me?" Single canonical place where Exec-cycle outputs surface PM-decision-needed items, blockers, or open coordination questions.

**Format**: append-only chronological. Each entry timestamped + state-marked. Lead with the most time-sensitive.

**Per v0.6 design** § "three architectural decisions" — this file IS the attention doc (reframed escalations file, no new doc).

> Reconciled 2026-06-12 ~10:10 AM PT (new-Exec first fire; the May 28 active entries were resolved or stale — moved to Closed).

---

## Active escalations

**1. [RESOLVED Jun 13 — NOT a PM decision] Gap-C dormancy cure = scheduled-tasks (not a $70/mo build)** *(was framed as a PM funding-gate; superseded — caught stale by PM 6/14 + live-state verification)*
The "Routines watchdog ~$70/mo" was the *candidate* cure under PM funding consideration. **CIO proved the real cure is scheduled-tasks** — disk-persistent, surviving the session-resumes that kill CronCreate-based crons. CIO's Gap-C scheduled-task pilot SUCCEEDED Jun 13 (`e0de384e7`, full autonomous commit/push loop); CIO is operationalizing the recurring conversion cohort-wide. **No PM funding decision needed** — scheduled-tasks are a deployed platform capability (in PM's Max plan; CIO already experimenting). **EXEC ACTION (open, operational not PM-gated): migrate the Exec duty-cycle cron from CronCreate (session-only — died ~29.5h 6/13→14) to scheduled-tasks**, adopting CIO's proven pattern. This is the fix for Exec's own dormancy.

**2. [RESOLVED Jun 12] Ship #047 CIO-lens sequencing** — moot: CIO filed their #047 lens (wrote pre-migration); the Ship is now drafted v0.1 + in the Comms pipeline. No PM action. (Drops at next reconcile.)

**3. dev/active/ cleanup — awareness, no PM action** *(carried from May 28; still true)*
dev/active/ is well over the ~15-file cleanup-skill threshold (cohort cycle-logs + delta-* + trackers). A solo exec sweep would violate commit-only-own-files. Candidate for cross-role cleanup-coordination or a per-agent self-cleanup norm tied to the duty-cycle STOP ritual. Flagging for awareness.

---

## Closed entries

**[CLOSED Jun 12] Worktree-vs-main operating model — RESOLVED, no do-over** *(surfaced Exec bootstrap Jun 12)*
CIO confirmed the ephemeral worktree IS the canonical Option-B pattern (Desktop "worktree-on" cohort standard since 6/2); dedicated `claude/exec-cycle` was older Model A, not required. Exec corrected to genuine Option B (non-mailbox in worktree → push-to-ref; mailbox via bridge). The variant-preservation finding stands as m-41 instance #2 (separate methodology track, CIO-driven). No PM action needed.

**[CLOSED Jun 12] BRIEFING-CURRENT-STATE / XPOLL staleness** *(was active May 28)*
Both now fresh: BRIEFING last updated Jun 10 (within 7-day window); XPOLL current.md Jun 12. The May 28 escalation (31/29 days stale) is resolved.

**[CLOSED May 28] v0.7 worktree-as-cycle-default — PM RATIFIED**
PM ratified ~7:53 AM May 28 ("worktree decision ratified. do not register on main") + Rule-2-Model-A. Superseded by the Jun 12 Option-B clarification above (the cohort moved to ephemeral worktrees). No PM action needed — closed.

---

## Notes on shape

- **What goes here**: items requiring PM decision/awareness that Exec surfaced during a fire (cohort-coordination questions, cross-role blockers Exec can't resolve, PM-decision-queue items accumulating).
- **What does NOT go here**: routine mail triage (inbox MANIFEST), Ship-cycle work (workstream memos + Ship draft), cycle-operational-state (cycle log).
- **Update cadence**: each fire's Mail/Task Loop drain may produce 0+ entries; STOP drain may close some.
- **Surface convention**: lead with the most-time-sensitive; PM should read the top entry and act within 60s.
