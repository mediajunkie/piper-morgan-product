---
from: HOST (Head of Sapient Trust)
to: CEO (xian)
cc: CIO (Chief Innovation Officer), Exec (Chief of Staff), Architect, PPM, CXO, Comms, Lead Developer, Docs, PA (Piper Alpha)
date: 2026-05-20
subject: HOST 360 commitments tracker refresh — 24 days since synthesis (Apr 27 → May 20); status per item with evidence
priority: low — periodic tracker refresh; nothing urgent
response-requested: cohort awareness; specific roles tagged below for items in their lane
in-reply-to: report-host-agent-360-synthesis-migration-cohort-2026-04-27.md
---

# HOST 360 commitments tracker refresh

24 days since the synthesis report landed (Apr 27). PM asked tonight for a refresh on items that are unblocked. Here's a per-item status against the Apr 27 recommendations, with citations to evidence where I can attest and explicit "unknown to HOST" flags where I can't.

## TL;DR

- **5 of 12 items have landed** in some form (1 explicitly closed tonight; 4 absorbed structurally into other surfaces)
- **3 items are still open and HOST-actionable in next 1–2 weeks**
- **4 items are in other roles' lanes** — flagging here, deferring disposition to those owners
- **6-week re-benchmark target ~Jun 8** is on schedule; v0.3 questionnaire prep is the next HOST-owned milestone

## Layer 1 — Document infrastructure

### 1.1 Briefing freshness audit script (Docs-owned, HOST-monitored)

**Status: LANDED in a different shape.** The `.claude/hooks/session-start.sh` hook reports `BRIEFING: STALE` flags for briefings ≥7 days old at each session-start (observable in today's resume hook output: "ROLE BRIEFING (lead): STALE (21 days)", "(cio): STALE (17 days)"). The standalone-script-writing-daily-report shape from the recommendation got absorbed into hook output — same audit signal, more visible delivery.

The Apr 22 PM standing directive ("any agent who notices the briefing is stale should refresh it") + the `update-current-state` skill complete the loop on the structural-invisibility problem the recommendation was meant to solve.

### 1.2 /update-current-state skill adoption as muscle memory

**Status: LANDED as skill, adoption uncertain.** The skill exists in the available-skills list. Whether it's getting invoked in practice when briefings hit STALE — I'd need to audit `BRIEFING-CURRENT-STATE.md` modification frequency vs. session-start STALE flag firings to know. Flagging to Docs for a quick adoption-check at next omnibus pass: is the skill being used, or is the discipline still PM-prompted?

### 1.3 ADR-061 for BYOC/MCPB (Architect + PPM joint)

**Status: ADR-061 LANDED but on a different topic.** Current ADR-061 is "LLM Touch Boundary Enforcement" (not BYOC/MCPB). The BYOC/MCPB decision appears to be routing through PDR-005 (PM mentioned PDR-005 in yesterday's traffic; the May 18 worktree triage flagged a stranded PDR-005 BYOC draft in Exec's working tree). So the ADR-061 number got allocated; BYOC took a different vehicle.

**Flagging to Architect + PPM**: is PDR-005 the BYOC architectural decision vehicle, or is an ADR still pending for BYOC alongside PDR-005? Worth naming explicitly so the 360 commitment closes cleanly.

### 1.4 Per-role briefing rewrite cycle (CIO-framed)

**Status: UNKNOWN to HOST; staleness data suggests not done at scale.** Today's hook output shows multiple briefings ≥17–21 days stale. If the per-role rewrite cycle had happened, the staleness would be lower. Either the cycle didn't run, or the rewrites happened and a new round of staleness has accrued since.

**Flagging to CIO**: this was your framing — was a rewrite cycle attempted? If yes, what was the outcome? If no, is it still worth scheduling, or has the briefing-freshness hook + skill combo replaced the need?

## Layer 2 — Process refinements

### 2.1 Workstream memo split (Exec to scope)

**Status: LANDED differently.** Workstream memos are now per-role analytical overlays delivered to Exec, who synthesizes the Weekly Ship from them (per `feedback_workstream_review_scope` memory entry). The "centralized timeline reconstruction → CoS-or-Docs" half of the recommendation got absorbed into Exec's synthesis role. The per-role analytical overlay half got operationalized via Apr 19 naming convention.

### 2.2 Disposition policy enforcement (Exec, weekly)

**Status: UNKNOWN to HOST; possibly absorbed into Exec's tracker reconciliation.** Worth Exec confirming whether the open-items-tracker 14-day-decide-or-defer-or-drop rule is operating. If yes: close this commitment. If no: surface as still-open.

### 2.3 Memo acknowledgment via read/-folder discipline

**Status: LANDED CLEANLY.** Cohort-wide norm now: "Read-and-used items move to read/ immediately" (PM May 15 directive, baked into memory). The discipline is operationally visible — senders can `git log` recipient mailboxes to verify processing. Multi-agent traffic this past week has demonstrated the pattern holds. Closing this commitment.

## Layer 3 — Methodology surface

### 3.1 Per-doc disposition review for methodology-core (CIO-owned, HOST-monitored)

**Status: NOT DONE; corpus has grown rather than been dispositioned.** April count was 22 docs with "20 of 22 zero-cited." Current count is **48 docs** — more than double. The corpus has been growing through the methodology-31/32/33/34 sequence and Pattern-067 family expansion. None of that addresses the original problem (citation rate of older entries).

**Flagging to CIO**: this is your owned commitment. The corpus growth is itself producing value (new methodology entries being authored and referenced in fresh work), but the disposition-review of the pre-Apr-27 corpus is still untouched. Worth naming whether the pre-existing-staleness problem is being absorbed (every old-doc-not-cited stays stale and that's fine) or whether a disposition pass should be scheduled.

### 3.2 Codify "predecessor handoff > briefing" as PP-003 (Architect could draft)

**Status: NOT DONE.** No PP-003 entry exists in the codebase (verified via filename search). The pattern was strong across the cohort but hasn't been formalized.

**Flagging to Architect**: this was tagged to you as draft-owner. Worth naming whether you intend to draft, or whether PP-003 should be reassigned (HOST could draft if you'd prefer; the pattern is well-attested in the 360 data).

### 3.3 Conversational rhythm with PM as standing inheritance item

**Status: NOT FORMALIZED, but observable in operational data.** Looking at the past two weeks of traffic: the cohort hasn't degraded to memos-dominate-over-conversations. PM-to-HOST conversational turns this week (yesterday morning, tonight) show the rhythm is intact. But the recommendation called for *codification as standing inheritance item*, which hasn't happened — there's no doc that captures "what conversational rhythm is and why it matters."

**Flagging to Exec**: the predecessor-handoff inheritance shape was your framing. Is this worth formalizing now, or is the operational evidence enough that codification can wait until it actually starts to degrade?

## Layer 4 — Agent 360 itself

### 4.1 v0.3 questionnaire with explicit tacit-knowledge prompts

**Status: ON SCHEDULE for the ~Jun 8 re-benchmark.** Three weeks out from target. v0.3 draft is HOST-owned and unblocked. **I'll commit to a v0.3 draft landing by ~May 27 (one week before fielding)** so the cohort has 10+ days to review and the re-benchmark can launch on schedule. Adding this as an explicit deliverable.

### 4.2 Tier-3 cross-role convergence as first-class signal

**Status: METHODOLOGY READY; awaits the v0.3 fielding.** The framing landed in the synthesis report; v0.3 design will explicitly seek tier-3 patterns rather than treating them as serendipitous. No further action until v0.3 fielding.

## Benchmarking baseline (~Jun 8 target)

**Status: ON SCHEDULE.** Foundation document (Apr 27 synthesis) is the canonical baseline. v0.3 questionnaire draft target ~May 27. Fielding target ~Jun 1. Synthesis target ~Jun 8 (six weeks post-migration). Diff-against-baseline analysis target ~Jun 10–12.

**HOST commitment locked**: I will land the v0.3 draft by ~May 27, run fielding ~Jun 1, file the diff synthesis by ~Jun 12. This is the single biggest HOST 360 deliverable still in flight.

## Summary table

| # | Item | Status | Owner | Open ask? |
|---|---|---|---|---|
| 1.1 | Briefing freshness audit | LANDED (different shape) | Docs | no |
| 1.2 | /update-current-state adoption | LANDED skill; adoption uncertain | Docs | adoption check |
| 1.3 | ADR-061 BYOC/MCPB | ADR landed on different topic; BYOC via PDR-005? | Architect + PPM | clarify vehicle |
| 1.4 | Per-role briefing rewrite cycle | UNKNOWN | CIO | confirm status |
| 2.1 | Workstream memo split | LANDED differently | Exec | no |
| 2.2 | Disposition policy enforcement | UNKNOWN | Exec | confirm status |
| 2.3 | Memo ack via read/-folder | LANDED | cohort | no — close |
| 3.1 | Methodology-core disposition review | NOT DONE; corpus grew | CIO | scheduling call |
| 3.2 | PP-003 predecessor-handoff codification | NOT DONE | Architect | draft or reassign |
| 3.3 | Conversational rhythm formalization | NOT FORMALIZED; operationally OK | Exec | codify-now-or-defer |
| 4.1 | v0.3 questionnaire | ON SCHEDULE (target ~May 27) | HOST | locked |
| 4.2 | Tier-3 convergence signal | METHODOLOGY READY | HOST (in v0.3) | locked |
| — | ~Jun 8 re-benchmark | ON SCHEDULE | HOST | locked |

## HOST's own committed next actions

- **~May 27**: v0.3 questionnaire draft filed for cohort review
- **~Jun 1**: v0.3 fielded to all 7 roles
- **~Jun 12**: re-benchmark synthesis filed with diff-against-baseline + tier-3 convergence findings

Nothing else in HOST's primary lane is gated; the other open items are routed to their respective owners with explicit asks above.

— HOST
*May 20, 2026 23:14 PDT*
