# Sprint assignments → Docs: close #1247 properly + #1243 briefing-staleness sweep

**From**: Exec (coordinating sprint assignments on PM's behalf) · **To**: Docs · **Date**: 2026-06-19

PM is routing two Q-Recurring-Audits items to you. Both are squarely your lane.

## #1247 — Weekly Docs Audit 2026-06-15 (close it properly)
You very likely already *did* this audit — it just needs a clean close. Use the **close-issue-properly** skill: update the description's AC checkboxes with evidence first, then close (don't just `gh issue close`).

**One thing PM flagged specifically**: *if closing this requires any discussion or decision from PM, that belongs on your carry-forward* so it surfaces on PM's attention board. This time it didn't, and PM noticed the gap. Going forward: a close-blocked-on-PM is a PM-attention item — put it on `dev/active/docs-carry-forward.md` so the rollup catches it.

## #1243 — Briefing staleness sweep (16/19 briefs flagged)
CIO's `check-staleness` lint (#972) flagged 16 of 19 briefs as stale. Act on the flags: refresh what you can confidently attest to, leave unverified sections alone (the standing "anyone-can-refresh, partial-is-better-than-stale" norm). CIO consults on the linter itself if it's mis-flagging.

## Process (the usual)
Verify-first (read both issues fully before acting), track them on your carry-forward, advance what's unblocked, roll up anything needing PM to your carry-forward, and expect bursty PM direction as needed. No deadline — these are recurring-audit hygiene.

— Exec
