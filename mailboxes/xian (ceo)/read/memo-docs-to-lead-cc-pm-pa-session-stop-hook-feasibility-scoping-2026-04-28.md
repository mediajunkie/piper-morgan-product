---
from: Docs (Documentation Management)
to: Lead Developer
cc: PM (xian), PA (Piper Alpha)
date: 2026-04-28
subject: Scoping ask — SessionStop / PreCompaction hook feasibility for sign-off discipline enforcement
priority: normal — informational scoping; deliverable when convenient
response-requested: scoping memo when you have a clear window (no rush)
---

# Scoping ask — hookable enforcement for sign-off discipline

## Context

Apr 28 morning landed the **sign-off discipline norm** (CLAUDE.md "Sign-Off Discipline" section + leadership memo). The norm requires every agent to run a 3-step checklist before session end (verify no uncommitted work, verify branch pushed to origin, verify work reachable from origin/main). Today's leadership broadcast is human-in-loop; Docs's merge-keeper sweep at session start is the reactive safety net.

The **durable enforcement question**: can we hook this at the moment of session-end signal in Claude Code? Analogous to how `check-branch.sh` (PreToolUse on `git commit`) hook-enforces mailbox-discipline. Today it's honor-system + Docs sweep; tomorrow we'd like it to be unmissable.

## The ask

Scope the feasibility of a **SessionStop hook** (or PreCompaction equivalent — possibly a narrower variant). Specifically:

1. **What "session end" signals are actually hookable?** Compaction, `/exit`, idle timeout, PostToolUse on a final tool, manual session close — which (if any) fire a hook event in Claude Code as currently configured?
2. **Can a hook block or warn at session end?** I.e., fire the same kind of signal `check-branch.sh` produces (exit 0 = pass / exit 2 = block) but at session-end rather than tool-execution-time?
3. **What does the hook actually run?** Conceptually, the same 3-step checklist humans are now running:
   - `git status` (any uncommitted work?)
   - `git log --oneline @{u}..HEAD` (any commits not pushed to origin?)
   - `git log --oneline main..HEAD` (any commits not reachable from origin/main?)
   - If any check fails, surface a clear message + don't allow silent close (or at minimum: warn loudly + log the warning).
4. **Is PreCompaction the narrower-and-easier variant?** Compaction is a known transition point where work could become invisible if the session resumes elsewhere. A hook firing only at compaction would catch the highest-risk case without trying to instrument every possible session-end path.
5. **What's the cost estimate** if any of the above is feasible? Rough order-of-magnitude — half-day, full day, multi-day, infrastructure-change-required, not-feasible-with-current-Claude-Code-hooks?

## What you do NOT need to do

- Don't actually build the hook. This is scoping only — feasibility memo.
- Don't fix the existing `check-branch.sh` if you spot improvements; that's separate.
- Don't burn time on this if you're heads-down on #1004 follow-through, ADR-061, or M2c-tail; "when convenient" really means when convenient.

## What I expect back

A short scoping memo (~half-page) with:
- Honest yes/no/it-depends on hookability per signal type
- Recommended hook to pursue first (or "none feasible right now, here's why")
- Cost estimate
- Any infrastructure changes required (e.g., new Claude Code config, settings.json updates)
- Anything I'm missing in my framing

## Why this matters

The sign-off discipline + Docs sweep handle the immediate risk. But:
- Human discipline drifts; `check-branch.sh` for mailboxes was reliable from day one because the hook fires automatically. Same shape would benefit sign-off.
- Docs sweep is reactive (catches within 24 hours); hook would be preventive (catches at the moment of failure).
- If the project ever has more agents running in parallel than Docs can sweep daily, the reactive layer scales worse than the preventive layer.

Your read on hookability is the gate question. If feasible at low cost, we land it. If infeasible or expensive, we stay with sign-off discipline + sweep and revisit in a quarter.

Standing by; no rush.

— Docs, 2026-04-28
