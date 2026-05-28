# Exec Duty Cycle Escalations / Attention Doc

**Purpose**: the at-a-glance surface PM scans when wondering "is anything Exec-shaped waiting on me?" Single canonical place where Exec-cycle outputs surface PM-decision-needed items, blockers, or open coordination questions.

**Format**: append-only chronological. Each entry timestamped + state-marked.

**Per v0.6 design** § "three architectural decisions" — this file IS the attention doc (reframed escalations file, no new doc).

---

## Active escalations

**1. dev/active/ at 63 files — cleanup-skill threshold is ~15** *(surfaced Fire 0, May 28; low priority)*
Mostly other agents' cycle-logs + delta-* + tracker files. A solo exec sweep would violate commit-only-own-files. Candidate for a cross-role cleanup coordination (cleanup-dev-active skill is cross-role) or a per-agent self-cleanup norm tied to the duty-cycle STOP ritual. No PM action needed; flagging for awareness.

**2. BRIEFING-CURRENT-STATE.md 31 days stale; XPOLL brief 29 days** *(surfaced Fire 0, May 28; Docs/PA lanes)*
Both past the 7-day freshness threshold the session-start hook flags. Docs lane for BRIEFING; PA/cross lane for XPOLL. Not exec-fixable but worth surfacing so it doesn't sit silent indefinitely — the hook has been flagging it daily without resolution.

---

## Closed entries

*(empty)*

---

## Notes on shape

- **What goes here**: items requiring PM decision/awareness that Exec surfaced during a fire (mail-routing decisions, cohort-coordination questions, cross-role blockers Exec can't resolve, PM-decision-queue items accumulating)
- **What does NOT go here**: routine mail triage (that lives in inbox MANIFEST), Ship-cycle work (lives in workstream memos + Ship draft), cycle-operational-state (lives in cycle log)
- **Update cadence**: each fire's Mail Loop drain or Task Loop drain may produce 0+ entries here. End-of-day drain may close some.
- **Surface convention**: lead with the most-time-sensitive item; PM should be able to read the top entry and act within 60s
