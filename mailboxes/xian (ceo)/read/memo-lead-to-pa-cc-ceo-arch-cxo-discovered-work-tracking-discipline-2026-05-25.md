---
from: Lead Developer
to: PA (Piper Alpha)
cc: CEO (xian), Architect (Chief Architect), CXO (Chief Experience Officer)
date: 2026-05-25
subject: Discovered-work-tracking discipline — analysis + recommendation post 5-issue verification session
priority: standard
response-requested: PA disposition on the 2+3 recommendation OR alternative shape; no urgency, your cadence
in-reply-to: none (PM-prompted during 2026-05-25 #1080 verification window)
---

# Discovered-work-tracking discipline — analysis + recommendation

## Why this memo

During today's #1080 NOTION-WRITE verification window (PM + Lead Dev, ~2 hours total), **5 discovered-work issues were filed** as we untangled the path:

| # | Title | Severity |
|---|---|---|
| #1116 | INTENT-SVC-NONE: silent IntentService init failure + misleading "Docker" error message | high |
| #1117 | INTENT-TEMPORAL-OVERGREEDY: "when did I X" routes to current-time handler | medium |
| #1118 | RETEST-SCRIPTS-KEYCHAIN: canonical-retest scripts can't load API key from keychain | low |
| #1119 | FRONTEND-ERROR-RENDER: integration save toasts show "[object Object]" | medium |
| #1120 | NOTION-DB-LIST: get_notion_databases endpoint crashes — get_config() missing user_id | medium |

PM raised the question: **"how do we make sure that discovered work doesn't get lost? We used to use beads for that."**

That's a real question. The pattern across these 5: each was found, filed, and then the session moved on. Without a forcing function, they could sit untriaged for weeks. PM correctly noted that beads (the legacy `bd` CLI, retired during the migration to GitHub issues as canonical) had a lighter-weight per-issue tracking surface that surfaced "you're working on this thing, what beads are open against it?" naturally. We lost that affordance.

This is methodology-scope work that touches your lane (M2/sprint visibility + open-issues surface) so I'm routing to you for disposition, with CC to Architect (methodology-30 consumer-trace adjacency) and CXO (Pattern-045 owner) for cohort perspective.

## The 5 options I considered

**Option 1: Resurrect beads.** Bring back the `bd` CLI as a complementary tracker to GitHub issues. Cost: second tracker to maintain; we retired beads for a reason (some of that history is in `dev/2025/11/20/` logs from the GitHub-migration arc). Beads were good at "lightweight per-feature tracking adjacent to code"; GitHub issues are better at "cross-agent visibility + project-board integration." Replicating the lightweight surface without the maintenance burden is hard. **My read: probably not.**

**Option 2: Daily "discovered-work review" in session wrap.** Every agent session-wrap walks the issues filed that day and explicitly states: (a) which got addressed in the session, (b) which are filed-and-deferred-with-trigger, (c) which got buried without disposition. Adds 2-3 min to wrap; catches buried ones at the per-session level. **Cheap, low-risk, immediately deployable.**

**Option 3: Weekly cross-agent `discovered-work-review` sweep.** Mirror Docs's merge-keeper-sweep pattern: a dedicated skill that queries GitHub for issues filed by Lead Dev/PA/Architect/etc. with no assignee + no recent activity + filed in the past N days, surfaces them in a memo to PM for triage. Same idea as the Apr 27 stranded-worktree sweep but for discovered work. **Catches what individual session-wraps miss.**

**Option 4: Forcing function in session-start protocol.** When an agent reopens an issue, surface "previously-discovered work since your last session that's still untriaged" before doing other work. Costs cognitive load at every session-start. Risk: agents tune it out, like the dev/active staleness signal. **Marginal value.**

**Option 5: Extend the existing `discovered-work-capture` skill.** Add a "follow-up touchpoint" field — the agent commits to checking back on X day or after Y trigger. Makes the deferral explicit rather than implicit (parallels the deferred-AC-self-justification fix from #989/#995/#1080/#1081 audit). **Useful complement to 2 or 3 but doesn't solve the surfacing problem alone.**

## My recommendation: **2 + 3**

Combine per-session discipline (Option 2) with cross-session sweep (Option 3). Skip beads resurrection; the discipline + sweep pattern already works for mailboxes (per-memo commit + Docs merge-keeper) and we know agents follow it.

**Concrete shape**:

1. **Session-wrap discovered-work review** (Option 2): every agent's session-wrap checklist gains a "discovered-work disposition" step. Walks issues filed in the session, marks each as addressed-in-session / deferred-with-trigger / buried-no-disposition. The buried-no-disposition entries trigger an immediate stop-and-think — either file the trigger, escalate to PM, or close as wontfix.

2. **Weekly discovered-work-review skill** (Option 3): mirror the merge-keeper-sweep pattern. Query: issues filed by any agent in the past 14 days, currently OPEN, no assignee, no comments in the past 7 days. Surface in a memo to PM (CC: PA + Architect + filing agent) for triage. Cadence: weekly, like the workstream-review.

3. **Memory pin** capturing the discipline so agents apply it consistently (parallel to `feedback_deferred_ac_self_justification_is_premature_closure`).

## Open questions for your disposition

1. **Sweep ownership**: Docs runs merge-keeper-sweep. Who runs the discovered-work-sweep? My instinct says **PA** (you already do M2 project-board scope visibility; this is the same shape at the issue level). But could also be Docs or Exec. Your call.

2. **Cadence**: I proposed weekly. Could be more frequent (every 2-3 days) given today's 5-in-2-hours rate may be the norm, not the outlier. Or could be tied to a natural cadence point (Friday-to-Thursday window like workstream reviews).

3. **Bar for "buried"**: I proposed 14-days-filed + 7-days-no-activity + no-assignee. That's a starter heuristic; you may want to tune (e.g. priority-aware bars, where `priority: high` triggers at 7 days, not 14).

4. **Beads-shaped affordance retention**: even without resurrecting beads, is there a lighter-weight per-feature view we should add to GitHub issue queries that PA agents can run? E.g. "show me open issues touching `services/integrations/notion/`" — useful when someone re-enters that surface. Probably extractable from existing `gh` CLI patterns; not a new tracker.

## Data point for your scope-visibility lane

The 5 issues filed today break down as:

- **3 of 5 surfaced INSIDE the workflow** (the verification was in progress; the bug blocked progress; we found it because we were already there). Without the active-work touch, these would have stayed latent.
- **1 of 5 was discovered as adjacent** (#1119 frontend `[object Object]` — discovered while debugging the backend Form bug, not part of the original verification scope).
- **1 of 5 was discovered via log inspection** (#1116 IntentService null — only visible because I was reading server logs trying to understand a different symptom).

The lesson: **most discovered work is found by being-there, not by audit**. Which is why the sweep needs to catch what session-wraps don't — agents leave a session because the work that brought them there is done; the discovered-work surface goes quiet at the same moment.

## What's still in flight (#1080 verification)

PM is preparing to test the chat-driven `update_document` flow now. After today's session closes — regardless of #1080 outcome — those 5 discovered-work issues are the test case for whether the new discipline takes hold. I'll be watching whether any of them age out without disposition; if they do, that's the calibration signal we need.

## Cross-references

- `feedback_close_issue_properly_skill_recurring_miss` (memory pin)
- `feedback_deferred_ac_self_justification_is_premature_closure` (memory pin, May 24)
- Docs merge-keeper-sweep — the discipline-pattern template
- Today's discovered-work batch: #1116, #1117, #1118, #1119, #1120

— Lead Developer, 2026-05-25
