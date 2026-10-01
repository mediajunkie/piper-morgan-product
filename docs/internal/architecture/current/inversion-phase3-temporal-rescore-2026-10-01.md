# Inversion Phase-1 shadow score — CONSTRAINED ROUTER vs Phase-0 baseline
Run: 2026-10-01 14:32Z · corpus: inversion_corpus_phase0.yaml (69 rows) · scripts/inversion_phase1_shadow_score.py
Served (#1620 — resolved, post-fallback, per row): anthropic:claude-haiku-4-5 (69/69)

LAYER (m-43): **router only, context-free** — one constrained Haiku-class call per row (70 LLM calls incl. repair retries; 0 ERROR, 0 REFUSED), grammar derived from the live registry at run time (64 canonical operations, 83 input-side aliases collapsed, + NONE/CLARIFY). The production chain was NOT executed in this run; the baseline column is Phase-0's FULL-CHAIN production decision (inversion-phase0-baseline-full-2026-08-12.md). Context-dependent rows (the 1529 offer/flow family) ran WITHOUT session state — their answers are informational for Phase 2, not its measured shape.

## Per-category vs baseline (denominators stated — m-44)

| category | rows | asserted | router match | baseline match | Δ | REVIEW | gate |
|---|---|---|---|---|---|---|---|
| TEMPORAL | 69 | 65 | 55 | 4/4 | +51 | 4 | no regression |
| **TOTAL** | 69 | 65 | 55 | 36/39 | +19 | 4 | (aggregate is NOT the gate) |

Gate reading (Arch condition 1 as amended 08-09 08:3x, PPM): **no category may regress; the aggregate is never the gate** (the M2 precedent: 72.1% aggregate passed while a category was broken). CONVERSATION / DISCOVERY / PROVENANCE / TRUST / ANALYSIS have REVIEW-only denominators in Phase 0 and remain **ungateable** here — same as Phase 0 stated; growing asserted expectations there is outstanding Phase-0 work, not a Phase-1 scoring artifact.

⚠️ **m-44: the table above compares two different denominators** (this run's 116-row corpus vs the baseline's 93-row corpus) — its `Δ`/`gate` cells are INFORMATIONAL ONLY from this run forward. The shared-subset table below, scored on rows asserted in BOTH corpora, is the actual gate.

## Shared-subset score vs 2026-08-12 baseline (m-44 fix — THIS is the gate)

Matching rule: phrase normalized (strip + collapse whitespace + casefold), exact match required; on a miss, fall back to an unambiguous ≥20-char prefix match in either direction (markdown row-detail tables truncate long phrases with no ellipsis, at different fixed lengths in different docs). Only rows asserted (non-REVIEW) on BOTH sides are scored here; the per-category table above compares two different denominators and is informational only from this point forward.

| category | shared asserted | router match | baseline match | gate |
|---|---|---|---|---|
| TEMPORAL | 4 | 4/4 | 4/4 | no regression |

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

Added (current-asserted, not in the 08-12 baseline):
- [TEMPORAL] remind me at 3pm tomorrow to review the PR
- [TEMPORAL] Remind me tomorrow at 3pm to review the PR
- [TEMPORAL] delete my hydrate reminder
- [TEMPORAL] remind me
- [TEMPORAL] add a reminder: test the safe clarification
- [TEMPORAL] please remind me: ask Lead how to test "outwardness disclosure" today
- [TEMPORAL] set a reminder for the dentist appointment
- [TEMPORAL] create a reminder to call the plumber
- [TEMPORAL] don't let me forget to submit the report
- [TEMPORAL] I need to remember to submit my timesheet
- [TEMPORAL] what are my reminders
- [TEMPORAL] show reminders
- [TEMPORAL] do I have any reminders
- [TEMPORAL] what's the time
- [TEMPORAL] current time please
- [TEMPORAL] give me the time now
- [TEMPORAL] tell me the time
- [TEMPORAL] what day is it
- [TEMPORAL] what's the date
- [TEMPORAL] current date please
- [TEMPORAL] today's date please
- [TEMPORAL] what's today
- [TEMPORAL] give me the date and time
- [TEMPORAL] what day of the week is it
- [TEMPORAL] tell me the date
- [TEMPORAL] what date is it
- [TEMPORAL] remind me today's day
- [TEMPORAL] pull up my calendar
- [TEMPORAL] show the team calendar
- [TEMPORAL] pull up my schedule
- [TEMPORAL] show the team schedule
- [TEMPORAL] calendar check for today
- [TEMPORAL] schedule check for today
- [TEMPORAL] walk me through my appointments
- [TEMPORAL] show all appointments
- [TEMPORAL] walk me through my meetings
- [TEMPORAL] what are the upcoming meetings
- [TEMPORAL] when is my team meeting
- [TEMPORAL] when am i in a meeting
- [TEMPORAL] meeting check for today
- [TEMPORAL] meeting check for tomorrow
- [TEMPORAL] walk me through my events
- [TEMPORAL] show all events
- [TEMPORAL] what are the upcoming events
- [TEMPORAL] events check for today
- [TEMPORAL] events check for tomorrow
- [TEMPORAL] when's the next event
- [TEMPORAL] what did I work on today
- [TEMPORAL] what happened in the meeting yesterday
- [TEMPORAL] did I finish the report yesterday
- [TEMPORAL] a lot happened yesterday
- [TEMPORAL] when was the last time I worked on this
- [TEMPORAL] how long have I been working on this
- [TEMPORAL] this week's priorities, remind me
- [TEMPORAL] next week's priorities, remind me
- [TEMPORAL] this month's numbers, remind me
- [TEMPORAL] when am i free
- [TEMPORAL] when's my next free slot
- [TEMPORAL] what's my available time
- [TEMPORAL] when do I have free time
- [TEMPORAL] what are my open slots

## Exhibit A (PM 2026-08-08 live transcript) + Arch's demanded row

Selection rule: corpus `source` containing one of ('exhibit-a', 'issue-1559', 'issue-1492') → 3 rows (the 8 Exhibit-A failures), plus the demanded row `"what reminders do I have?"` (probe-row-11, REVIEW — the sharpest test of the thesis: the LLM classifier misrouted it until the pre-classifier claimed it).

| phrase | expected | router route @conf | verdict | source |
|---|---|---|---|---|
| remind me at 3pm tomorrow to review the PR | action:create_reminder | `create_reminder` @0.95 | MATCH | issue-1559 (turn-1 PM verbatim, #1517 T4 2026-08 |
| remind me at 9:41 today to check in with the lead develope | action:create_reminder | `create_reminder` @0.95 | MATCH | issue-1559 (adjacency gap: 'remind me at <time>  |
| Remind me tomorrow at 3pm to review the PR | action:create_reminder | `create_reminder` @0.95 | MATCH | issue-1490 (PM 8/7 original verbatim: date-then- |
| what reminders do I have? | REVIEW | `list_reminders_query` @0.99 | REVIEW (informational) | probe-row-11 |

## REVIEW rows — the router's answers as data (informational, unscored)

These 54 rows are the Inversion's question book (36 probe-DISAGREEs by construction + PM's live failures). Nothing here is scored; the router's answer is recorded so the questions accumulate evidence.

| phrase | category | router route @conf | rationale | source |
|---|---|---|---|---|
| what reminders do I have? | TEMPORAL | `list_reminders_query` @0.99 | User asks for their reminders list | probe-row-11 |
| delete my reminders | TEMPORAL | `CLARIFY` @0.4 | Delete all reminders, or specific ones? Need clarification o | issue-1527 (greedy portfolio delete patt |
| what time is it? also connect my github | TEMPORAL | `PLAN[get_current_time→get_contextual_guidance]` |  | issue-1755 (found during the 1505 fix, 2 |
| please clear the reminders except for "Review the PR" - | TEMPORAL | `PLAN[list_reminders_query→set_default_repo]` |  | issue-1606 (PM live 2026-08-12: request  |

## Row detail (asserted rows)

| phrase | category | expected | router route @conf | verdict | note |
|---|---|---|---|---|---|
| what's on my calendar today? | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| when is my next meeting? | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| what time is it? | TEMPORAL | category:TEMPORAL | `get_current_time` @0.99 | MATCH |  |
| remind me at 3pm tomorrow to review the PR | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| remind me at 9:41 today to check in with the lead devel | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| Remind me tomorrow at 3pm to review the PR | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| delete my hydrate reminder | TEMPORAL | action:delete_todo | `NONE` @0.85 | MISMATCH | NONE |
| remind me | TEMPORAL | action:create_reminder | `CLARIFY` @0.95 | MISMATCH | CLARIFY |
| add a reminder: test the safe clarification | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| please remind me: ask Lead how to test "outwardness dis | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| set a reminder for the dentist appointment | TEMPORAL | action:create_reminder | `create_reminder` @0.85 | MATCH |  |
| create a reminder to call the plumber | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| don't let me forget to submit the report | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| I need to remember to submit my timesheet | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| what are my reminders | TEMPORAL | action:list_reminders_query | `list_reminders_query` @0.99 | MATCH |  |
| show reminders | TEMPORAL | action:list_reminders_query | `list_reminders_query` @0.95 | MATCH |  |
| do I have any reminders | TEMPORAL | action:list_reminders_query | `list_reminders_query` @0.95 | MATCH |  |
| what's the time | TEMPORAL | action:get_current_time | `get_current_time` @0.99 | MATCH |  |
| current time please | TEMPORAL | action:get_current_time | `get_current_time` @0.99 | MATCH |  |
| give me the time now | TEMPORAL | action:get_current_time | `get_current_time` @0.99 | MATCH |  |
| tell me the time | TEMPORAL | action:get_current_time | `get_current_time` @0.99 | MATCH |  |
| what day is it | TEMPORAL | action:get_current_time | `get_current_time` @0.95 | MATCH |  |
| what's the date | TEMPORAL | action:get_current_time | `get_current_time` @0.95 | MATCH |  |
| current date please | TEMPORAL | action:get_current_time | `get_current_time` @0.95 | MATCH |  |
| today's date please | TEMPORAL | action:get_current_time | `get_current_time` @0.95 | MATCH |  |
| what's today | TEMPORAL | action:get_current_time | `get_current_time` @0.95 | MATCH |  |
| give me the date and time | TEMPORAL | action:get_current_time | `get_current_time` @0.95 | MATCH |  |
| what day of the week is it | TEMPORAL | action:get_current_time | `get_current_time` @0.95 | MATCH |  |
| tell me the date | TEMPORAL | action:get_current_time | `get_current_time` @0.95 | MATCH |  |
| what date is it | TEMPORAL | action:get_current_time | `get_current_time` @0.95 | MATCH |  |
| remind me today's day | TEMPORAL | action:get_current_time | `get_current_time` @0.85 | MATCH |  |
| pull up my calendar | TEMPORAL | action:week_calendar | `CLARIFY` @0.6 | MISMATCH | CLARIFY |
| show the team calendar | TEMPORAL | floor | `NONE` @0.85 | MATCH | NONE |
| pull up my schedule | TEMPORAL | action:week_calendar | `week_calendar` @0.75 | MATCH |  |
| show the team schedule | TEMPORAL | floor | `CLARIFY` @0.4 | MATCH | CLARIFY |
| calendar check for today | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| schedule check for today | TEMPORAL | action:meeting_time | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| walk me through my appointments | TEMPORAL | action:week_calendar | `week_calendar` @0.75 | MATCH |  |
| show all appointments | TEMPORAL | action:week_calendar | `week_calendar` @0.7 | MATCH |  |
| walk me through my meetings | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| what are the upcoming meetings | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| when is my team meeting | TEMPORAL | action:meeting_time | `meeting_time` @0.85 | MATCH |  |
| when am i in a meeting | TEMPORAL | action:meeting_time | `meeting_time` @0.85 | MATCH |  |
| meeting check for today | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| meeting check for tomorrow | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| walk me through my events | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| show all events | TEMPORAL | action:week_calendar | `CLARIFY` @0.5 | MISMATCH | CLARIFY |
| what are the upcoming events | TEMPORAL | action:week_calendar | `week_calendar` @0.75 | MATCH |  |
| events check for today | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| events check for tomorrow | TEMPORAL | action:meeting_time | `meeting_time` @0.85 | MATCH |  |
| when's the next event | TEMPORAL | action:meeting_time | `meeting_time` @0.85 | MATCH |  |
| what did I work on today | TEMPORAL | action:session_activity_query | `session_activity_query` @0.92 | MATCH |  |
| what happened in the meeting yesterday | TEMPORAL | floor | `NONE` @0.95 | MATCH | NONE |
| did I finish the report yesterday | TEMPORAL | action:check_completion_status | `check_completion_status` @0.92 | MATCH |  |
| a lot happened yesterday | TEMPORAL | action:changes_query | `changes_query` @0.92 | MATCH |  |
| when was the last time I worked on this | TEMPORAL | floor | `CLARIFY` @0.5 | MATCH | CLARIFY |
| how long have I been working on this | TEMPORAL | floor | `CLARIFY` @0.3 | MATCH | CLARIFY |
| this week's priorities, remind me | TEMPORAL | floor | `PLAN[get_top_priority→create_reminder]` | MISMATCH | PLAN |
| next week's priorities, remind me | TEMPORAL | floor | `PLAN[get_top_priority→create_reminder]` | MISMATCH | PLAN |
| this month's numbers, remind me | TEMPORAL | floor | `PLAN[generate_report→create_reminder]` | MISMATCH | PLAN |
| when am i free | TEMPORAL | action:week_calendar | `week_calendar` @0.72 | MATCH |  |
| when's my next free slot | TEMPORAL | action:meeting_time | `CLARIFY` @0.5 | MISMATCH | CLARIFY |
| what's my available time | TEMPORAL | action:week_calendar | `CLARIFY` @0.6 | MISMATCH | CLARIFY |
| when do I have free time | TEMPORAL | action:week_calendar | `week_calendar` @0.72 | MATCH |  |
| what are my open slots | TEMPORAL | action:week_calendar | `week_calendar` @0.72 | MATCH |  |
