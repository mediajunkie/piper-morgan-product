# Inversion Phase-1 shadow score — CONSTRAINED ROUTER vs Phase-0 baseline
Run: 2026-10-01 05:07Z · corpus: inversion_corpus_phase0.yaml (46 rows) · scripts/inversion_phase1_shadow_score.py
Served (#1620 — resolved, post-fallback, per row): openai:gpt-4o-mini (46/46)

LAYER (m-43): **router only, context-free** — one constrained Haiku-class call per row (46 LLM calls incl. repair retries; 0 ERROR, 0 REFUSED), grammar derived from the live registry at run time (64 canonical operations, 83 input-side aliases collapsed, + NONE/CLARIFY). The production chain was NOT executed in this run; the baseline column is Phase-0's FULL-CHAIN production decision (inversion-phase0-baseline-full-2026-08-12.md). Context-dependent rows (the 1529 offer/flow family) ran WITHOUT session state — their answers are informational for Phase 2, not its measured shape.

## Per-category vs baseline (denominators stated — m-44)

| category | rows | asserted | router match | baseline match | Δ | REVIEW | gate |
|---|---|---|---|---|---|---|---|
| QUERY | 46 | 46 | 32 | 12/13 | +20 | 0 | no regression |
| **TOTAL** | 46 | 46 | 32 | 36/39 | -4 | 0 | (aggregate is NOT the gate) |

Gate reading (Arch condition 1 as amended 08-09 08:3x, PPM): **no category may regress; the aggregate is never the gate** (the M2 precedent: 72.1% aggregate passed while a category was broken). CONVERSATION / DISCOVERY / PROVENANCE / TRUST / ANALYSIS have REVIEW-only denominators in Phase 0 and remain **ungateable** here — same as Phase 0 stated; growing asserted expectations there is outstanding Phase-0 work, not a Phase-1 scoring artifact.

⚠️ **m-44: the table above compares two different denominators** (this run's 116-row corpus vs the baseline's 93-row corpus) — its `Δ`/`gate` cells are INFORMATIONAL ONLY from this run forward. The shared-subset table below, scored on rows asserted in BOTH corpora, is the actual gate.

## Shared-subset score vs 2026-08-12 baseline (m-44 fix — THIS is the gate)

Matching rule: phrase normalized (strip + collapse whitespace + casefold), exact match required; on a miss, fall back to an unambiguous ≥20-char prefix match in either direction (markdown row-detail tables truncate long phrases with no ellipsis, at different fixed lengths in different docs). Only rows asserted (non-REVIEW) on BOTH sides are scored here; the per-category table above compares two different denominators and is informational only from this point forward.

| category | shared asserted | router match | baseline match | gate |
|---|---|---|---|---|

**Denominator deltas (m-44)** — rows in the 08-12 baseline no longer asserted in the current corpus (dropped), and rows asserted now that the baseline never saw (added). Neither is scored above; both are why the totals table's Δ column is informational, not the gate.

Dropped (baseline-asserted, not in current corpus):
- [EXECUTION] create a ticket for the login bug
- [EXECUTION] close issue 42
- [EXECUTION] comment on issue 42: looks good
- [EXECUTION] set my default repo to acme/widgets
- [EXECUTION] update the project plan doc with the new dates
- [EXECUTION] give me a project status report
- [GUIDANCE] how do I create a ticket?
- [IDENTITY] who am I?
- [IDENTITY] what's my role?
- [MEMORY] what have you learned about my workstyle?
- [PORTFOLIO] list my projects
- [PORTFOLIO] list my archived projects
- [PORTFOLIO] what projects have I archived?
- [PORTFOLIO] what projects do I have?
- [PORTFOLIO] Archive my project Test.
- [PORTFOLIO] Archive my project "Test"
- [PORTFOLIO] Archive the project called Test
- [PRIORITY] what should I focus on today?
- [PRIORITY] what are my top priorities?
- [QUERY] analyze the file I uploaded
- [QUERY] show my open issues
- [QUERY] show my open pull requests
- [QUERY] any stale PRs?
- [QUERY] what needs my attention?
- [QUERY] what changed since yesterday?
- [QUERY] how productive was I this week?
- [QUERY] what is my default repo?
- [QUERY] can we connect my github?
- [QUERY] connect my slack
- [QUERY] link mediajunkie/test-piper-morgan to the project
- [QUERY] help me set up github
- [STATUS] give me my standup
- [STATUS] what am I working on?
- [SYNTHESIS] summarize the document
- [SYNTHESIS] write a short update for the CEO on where we are
- [TEMPORAL] what's on my calendar today?
- [TEMPORAL] when is my next meeting?
- [TEMPORAL] what time is it?
- [TEMPORAL] remind me at 9:41 today to check in with the lead developer

Added (current-asserted, not in the 08-12 baseline):
- [QUERY] what is on my calendar
- [QUERY] show me my calendar today
- [QUERY] calendar today please
- [QUERY] what meetings today
- [QUERY] do i have any meetings
- [QUERY] do i have meetings
- [QUERY] what meetings do i have
- [QUERY] what meetings are coming up
- [QUERY] what's my schedule today
- [QUERY] today's schedule please
- [QUERY] what's the schedule for today
- [QUERY] what's my agenda today
- [QUERY] what's my agenda tomorrow
- [QUERY] what's my agenda this week
- [QUERY] what's my agenda next week
- [QUERY] show me my agenda
- [QUERY] show me calendar for tomorrow
- [QUERY] tomorrow's calendar please
- [QUERY] how many meetings do I have tomorrow
- [QUERY] what's the schedule tomorrow
- [QUERY] tomorrow's schedule please
- [QUERY] what's happening tomorrow
- [QUERY] show calendar this week
- [QUERY] show calendar next week
- [QUERY] what's the schedule this week
- [QUERY] what's the schedule next week
- [QUERY] how many meetings this week
- [QUERY] how many meetings next week
- [QUERY] how much time in meetings do I have
- [QUERY] how much time do I spend sitting in meetings
- [QUERY] time spent in meetings is high lately
- [QUERY] what's my meeting time today
- [QUERY] let's review my recurring meetings
- [QUERY] audit my standing meetings
- [QUERY] recurring meetings keep piling up
- [QUERY] show me my week
- [QUERY] what's the week ahead look like
- [QUERY] show the week calendar
- [QUERY] check my calendar for conflicts
- [QUERY] is my calendar showing any conflict
- [QUERY] does my calendar overlap with hers
- [QUERY] is there a conflict on my calendar
- [QUERY] find time for a 1:1 with sarah
- [QUERY] find some time for a sync
- [QUERY] schedule a quick call
- [QUERY] book a slot with the team

## Exhibit A (PM 2026-08-08 live transcript) + Arch's demanded row

Selection rule: corpus `source` containing one of ('exhibit-a', 'issue-1559', 'issue-1492') → 0 rows (the 8 Exhibit-A failures), plus the demanded row `"what reminders do I have?"` (probe-row-11, REVIEW — the sharpest test of the thesis: the LLM classifier misrouted it until the pre-classifier claimed it).

| phrase | expected | router route @conf | verdict | source |
|---|---|---|---|---|

## REVIEW rows — the router's answers as data (informational, unscored)

These 54 rows are the Inversion's question book (36 probe-DISAGREEs by construction + PM's live failures). Nothing here is scored; the router's answer is recorded so the questions accumulate evidence.

| phrase | category | router route @conf | rationale | source |
|---|---|---|---|---|

## Row detail (asserted rows)

| phrase | category | expected | router route @conf | verdict | note |
|---|---|---|---|---|---|
| what is on my calendar | QUERY | action:meeting_time | `NONE` @1.0 | MISMATCH | NONE |
| show me my calendar today | QUERY | action:meeting_time | `meeting_time` @0.9 | MATCH |  |
| calendar today please | QUERY | action:meeting_time | `meeting_time` @0.9 | MATCH |  |
| what meetings today | QUERY | action:meeting_time | `meeting_time` @1.0 | MATCH |  |
| do i have any meetings | QUERY | action:meeting_time | `meeting_time` @0.9 | MATCH |  |
| do i have meetings | QUERY | action:meeting_time | `meeting_time` @0.9 | MATCH |  |
| what meetings do i have | QUERY | action:meeting_time | `meeting_time` @0.9 | MATCH |  |
| what meetings are coming up | QUERY | action:meeting_time | `meeting_time` @0.9 | MATCH |  |
| what's my schedule today | QUERY | action:meeting_time | `meeting_time` @1.0 | MATCH |  |
| today's schedule please | QUERY | action:meeting_time | `meeting_time` @0.9 | MATCH |  |
| what's the schedule for today | QUERY | action:meeting_time | `meeting_time` @0.9 | MATCH |  |
| what's my agenda today | QUERY | action:meeting_time | `meeting_time` @1.0 | MATCH |  |
| what's my agenda tomorrow | QUERY | action:meeting_time | `meeting_time` @1.0 | MATCH |  |
| what's my agenda this week | QUERY | action:meeting_time | `week_calendar` @1.0 | MISMATCH |  |
| what's my agenda next week | QUERY | action:meeting_time | `week_calendar` @1.0 | MISMATCH |  |
| show me my agenda | QUERY | action:meeting_time | `NONE` @1.0 | MISMATCH | NONE |
| show me calendar for tomorrow | QUERY | action:meeting_time | `meeting_time` @0.9 | MATCH |  |
| tomorrow's calendar please | QUERY | action:meeting_time | `meeting_time` @1.0 | MATCH |  |
| how many meetings do I have tomorrow | QUERY | action:meeting_time | `meeting_time` @1.0 | MATCH |  |
| what's the schedule tomorrow | QUERY | action:meeting_time | `meeting_time` @1.0 | MATCH |  |
| tomorrow's schedule please | QUERY | action:meeting_time | `meeting_time` @1.0 | MATCH |  |
| what's happening tomorrow | QUERY | action:week_calendar | `meeting_time` @0.9 | MISMATCH |  |
| show calendar this week | QUERY | action:week_calendar | `week_calendar` @1.0 | MATCH |  |
| show calendar next week | QUERY | action:week_calendar | `week_calendar` @1.0 | MATCH |  |
| what's the schedule this week | QUERY | action:week_calendar | `week_calendar` @1.0 | MATCH |  |
| what's the schedule next week | QUERY | action:week_calendar | `week_calendar` @1.0 | MATCH |  |
| how many meetings this week | QUERY | action:week_calendar | `week_calendar` @0.9 | MATCH |  |
| how many meetings next week | QUERY | action:week_calendar | `week_calendar` @0.9 | MATCH |  |
| how much time in meetings do I have | QUERY | action:meeting_time | `meeting_time` @1.0 | MATCH |  |
| how much time do I spend sitting in meetings | QUERY | action:meeting_time | `meeting_time` @0.9 | MATCH |  |
| time spent in meetings is high lately | QUERY | action:meeting_time | `NONE` @1.0 | MISMATCH | NONE |
| what's my meeting time today | QUERY | action:meeting_time | `meeting_time` @1.0 | MATCH |  |
| let's review my recurring meetings | QUERY | action:recurring_meetings | `recurring_meetings` @1.0 | MATCH |  |
| audit my standing meetings | QUERY | action:recurring_meetings | `recurring_meetings` @0.9 | MATCH |  |
| recurring meetings keep piling up | QUERY | action:recurring_meetings | `recurring_meetings` @0.9 | MATCH |  |
| show me my week | QUERY | action:week_calendar | `week_calendar` @1.0 | MATCH |  |
| what's the week ahead look like | QUERY | action:week_calendar | `week_calendar` @1.0 | MATCH |  |
| show the week calendar | QUERY | action:week_calendar | `week_calendar` @1.0 | MATCH |  |
| check my calendar for conflicts | QUERY | action:week_calendar | `NONE` @1.0 | MISMATCH | NONE |
| is my calendar showing any conflict | QUERY | action:week_calendar | `NONE` @1.0 | MISMATCH | NONE |
| does my calendar overlap with hers | QUERY | action:week_calendar | `NONE` @0.9 | MISMATCH | NONE |
| is there a conflict on my calendar | QUERY | action:week_calendar | `meeting_time` @0.9 | MISMATCH |  |
| find time for a 1:1 with sarah | QUERY | action:week_calendar | `NONE` @1.0 | MISMATCH | NONE |
| find some time for a sync | QUERY | action:week_calendar | `NONE` @1.0 | MISMATCH | NONE |
| schedule a quick call | QUERY | action:week_calendar | `NONE` @0.0 | MISMATCH | NONE |
| book a slot with the team | QUERY | action:week_calendar | `NONE` @1.0 | MISMATCH | NONE |
