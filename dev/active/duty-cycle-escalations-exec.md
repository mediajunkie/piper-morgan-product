# Exec Duty Cycle Escalations / Attention Doc

**Purpose**: the at-a-glance surface PM scans when wondering "is anything Exec-shaped waiting on me?" Single canonical place where Exec-cycle outputs surface PM-decision-needed items, blockers, or open coordination questions.

**Format**: append-only chronological. Each entry timestamped + state-marked. Lead with the most time-sensitive.

**Per v0.6 design** § "three architectural decisions" — this file IS the attention doc (reframed escalations file, no new doc).

> Reconciled 2026-06-12 ~10:10 AM PT (new-Exec first fire; the May 28 active entries were resolved or stale — moved to Closed).

---

## Active escalations

**1. Routines watchdog build decision (~$70/mo) — PM gate** *(surfaced CIO Jun 7; data accumulated through Jun 12)*
Gap-C session-dormancy is the dominant cron-halt mechanism (CIO research Jun 11; durable=true is a no-op). Funding-trigger criterion is MET. **Fresh data**: Exec's own freshly-armed cron silently died Jun 12 ~06:50→08:25, *before its first fire*, on a healthy session — the self-heal only recovered because the session happened to get a turn (PM's message). A fully-dormant session can't self-wake. This is the cure. **PM decision needed** when bandwidth allows.

**2. Ship #047 CIO-lens sequencing — PM call** *(CIO flagged Jun 12)*
CIO's workstream review is a substantial write, and CIO's own account migration is queued for today. CIO leans "write pre-migration on this session" (source-set ready, continuity) but flagged it to PM since it defers the Exec→CIO migration sequence PM set. Low-urgency; either works. PM's call.

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
