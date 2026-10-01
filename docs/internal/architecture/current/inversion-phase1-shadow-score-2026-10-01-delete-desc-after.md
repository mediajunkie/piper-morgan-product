# Inversion Phase-1 shadow score — CONSTRAINED ROUTER vs Phase-0 baseline
Run: 2026-10-01 17:28Z · corpus: inversion_corpus_phase0.yaml (283 rows) · scripts/inversion_phase1_shadow_score.py
Served (#1620 — resolved, post-fallback, per row): anthropic:claude-haiku-4-5 (283/283)

LAYER (m-43): **router only, context-free** — one constrained Haiku-class call per row (283 LLM calls incl. repair retries; 0 ERROR, 0 REFUSED), grammar derived from the live registry at run time (64 canonical operations, 83 input-side aliases collapsed, + NONE/CLARIFY). The production chain was NOT executed in this run; the baseline column is Phase-0's FULL-CHAIN production decision (inversion-phase0-baseline-full-2026-08-12.md). Context-dependent rows (the 1529 offer/flow family) ran WITHOUT session state — their answers are informational for Phase 2, not its measured shape.

## Per-category vs baseline (denominators stated — m-44)

| category | rows | asserted | router match | baseline match | Δ | REVIEW | gate |
|---|---|---|---|---|---|---|---|
| QUERY | 85 | 67 | 60 | 12/13 | +48 | 18 | no regression |
| TEMPORAL | 69 | 65 | 58 | 4/4 | +54 | 4 | no regression |
| PRIORITY | 41 | 40 | 31 | 2/2 | +29 | 1 | no regression |
| GUIDANCE | 26 | 21 | 16 | 1/1 | +15 | 5 | no regression |
| EXECUTION | 18 | 8 | 7 | 5/6 | +2 | 10 | no regression |
| PORTFOLIO | 16 | 14 | 11 | 6/7 | +5 | 2 | no regression |
| STATUS | 8 | 4 | 3 | 1/4 | +2 | 4 | no regression |
| CONVERSATION | 5 | 0 | 0 | 0/0 | — | 5 | **UNGATEABLE** (REVIEW-only denominator) |
| SYNTHESIS | 4 | 2 | 2 | 2/2 | +0 | 2 | no regression |
| IDENTITY | 3 | 2 | 2 | 2/2 | +0 | 1 | no regression |
| MEMORY | 3 | 1 | 1 | 1/1 | +0 | 2 | no regression |
| DISCOVERY | 2 | 0 | 0 | 0/0 | — | 2 | **UNGATEABLE** (REVIEW-only denominator) |
| PROVENANCE | 1 | 0 | 0 | 0/0 | — | 1 | **UNGATEABLE** (REVIEW-only denominator) |
| TRUST | 1 | 0 | 0 | 0/0 | — | 1 | **UNGATEABLE** (REVIEW-only denominator) |
| ANALYSIS | 1 | 0 | 0 | 0/0 | — | 1 | **UNGATEABLE** (REVIEW-only denominator) |
| **TOTAL** | 283 | 224 | 191 | 36/39 | +155 | 59 | (aggregate is NOT the gate) |

Gate reading (Arch condition 1 as amended 08-09 08:3x, PPM): **no category may regress; the aggregate is never the gate** (the M2 precedent: 72.1% aggregate passed while a category was broken). CONVERSATION / DISCOVERY / PROVENANCE / TRUST / ANALYSIS have REVIEW-only denominators in Phase 0 and remain **ungateable** here — same as Phase 0 stated; growing asserted expectations there is outstanding Phase-0 work, not a Phase-1 scoring artifact.

⚠️ **m-44: the table above compares two different denominators** (this run's 116-row corpus vs the baseline's 93-row corpus) — its `Δ`/`gate` cells are INFORMATIONAL ONLY from this run forward. The shared-subset table below, scored on rows asserted in BOTH corpora, is the actual gate.

## Shared-subset score vs 2026-08-12 baseline (m-44 fix — THIS is the gate)

Matching rule: phrase normalized (strip + collapse whitespace + casefold), exact match required; on a miss, fall back to an unambiguous ≥20-char prefix match in either direction (markdown row-detail tables truncate long phrases with no ellipsis, at different fixed lengths in different docs). Only rows asserted (non-REVIEW) on BOTH sides are scored here; the per-category table above compares two different denominators and is informational only from this point forward.

| category | shared asserted | router match | baseline match | gate |
|---|---|---|---|---|
| QUERY | 12 | 11/12 | 12/12 | **REGRESSION** |
| PORTFOLIO | 7 | 6/7 | 6/7 | no regression |
| EXECUTION | 6 | 5/6 | 5/6 | no regression |
| TEMPORAL | 4 | 4/4 | 4/4 | no regression |
| STATUS | 2 | 1/2 | 1/2 | no regression |
| PRIORITY | 2 | 2/2 | 2/2 | no regression |
| IDENTITY | 2 | 2/2 | 2/2 | no regression |
| SYNTHESIS | 2 | 2/2 | 2/2 | no regression |
| GUIDANCE | 1 | 1/1 | 1/1 | no regression |
| MEMORY | 1 | 1/1 | 1/1 | no regression |

**Named regressions** (baseline matched, router did not — the specific rows behind each REGRESSION cell above):
- [PORTFOLIO] `list my archived projects`
- [QUERY] `analyze the file I uploaded`
- [STATUS] `what am I working on?`

**Denominator deltas (m-44)** — rows in the 08-12 baseline no longer asserted in the current corpus (dropped), and rows asserted now that the baseline never saw (added). Neither is scored above; both are why the totals table's Δ column is informational, not the gate.

Dropped (baseline-asserted, not in current corpus):
- none

Added (current-asserted, not in the 08-12 baseline):
- [EXECUTION] change the status of issue #108 to Done
- [EXECUTION] add todo buy oat milk
- [GUIDANCE] where should I focus this week
- [GUIDANCE] I could use some guidance on this
- [GUIDANCE] do you have a recommendation
- [GUIDANCE] what's your advice here
- [GUIDANCE] ok that's merged, what now?
- [GUIDANCE] what are the next steps
- [GUIDANCE] what should I do about this bug
- [GUIDANCE] advise me on this decision
- [GUIDANCE] what's the process for filing a bug
- [GUIDANCE] can you help me setup the integration
- [GUIDANCE] can you help me configure the connector
- [GUIDANCE] I need to setup my projects
- [GUIDANCE] how do I configure my projects
- [GUIDANCE] how do I setup the connector
- [GUIDANCE] how do I configure the connector
- [GUIDANCE] just getting started here
- [GUIDANCE] can you help me set up the integration
- [GUIDANCE] I want to set up my projects
- [GUIDANCE] how do I set up the connector
- [GUIDANCE] I'd like to set up my portfolio
- [PORTFOLIO] restore CoVa
- [PORTFOLIO] Please list my archived projects
- [PORTFOLIO] what are my projects?
- [PORTFOLIO] list my archive projects
- [PORTFOLIO] Archive my Test project, please.
- [PORTFOLIO] Archive my project called "Test" please
- [PORTFOLIO] archive CoVa
- [PRIORITY] what's my top priority
- [PRIORITY] this is top priority for the team
- [PRIORITY] this is the highest priority item
- [PRIORITY] mark this as priority one
- [PRIORITY] show priorities for this sprint
- [PRIORITY] list priorities for the team
- [PRIORITY] what are my current priorities
- [PRIORITY] what are the key priorities this quarter
- [PRIORITY] what's most important right now
- [PRIORITY] what matters most this week
- [PRIORITY] what are the key tasks for this sprint
- [PRIORITY] what are the key items on my plate
- [PRIORITY] should i focus on the bug first
- [PRIORITY] what could I focus on
- [PRIORITY] where should my focus be today
- [PRIORITY] what are my focus areas this sprint
- [PRIORITY] let's focus on today's priorities
- [PRIORITY] what's my focus this week
- [PRIORITY] not sure what to focus next
- [PRIORITY] what's urgent right now
- [PRIORITY] what are my urgent tasks
- [PRIORITY] what are my urgent items
- [PRIORITY] what's my urgent work today
- [PRIORITY] what's the most urgent thing
- [PRIORITY] what needs my focus today
- [PRIORITY] what requires attention right now
- [PRIORITY] what's critical right now
- [PRIORITY] what are my critical tasks
- [PRIORITY] what are my critical items
- [PRIORITY] what's my critical work today
- [PRIORITY] what's the most critical thing
- [PRIORITY] what should I do first
- [PRIORITY] what should I tackle next
- [PRIORITY] what's next for me
- [PRIORITY] what should I review first
- [PRIORITY] which project should get my focus today
- [PRIORITY] which task should get my focus next
- [PRIORITY] not sure what to do about this
- [QUERY] show me all project plans
- [QUERY] show todos
- [QUERY] list my todos
- [QUERY] what are my todos
- [QUERY] show me completed todos
- [QUERY] show all todos
- [QUERY] next todo
- [QUERY] what should I do next
- [QUERY] what do I have next to do
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
- [STATUS] do a standup
- [STATUS] let's do a standup
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

Selection rule: corpus `source` containing one of ('exhibit-a', 'issue-1559', 'issue-1492') → 16 rows (the 8 Exhibit-A failures), plus the demanded row `"what reminders do I have?"` (probe-row-11, REVIEW — the sharpest test of the thesis: the LLM classifier misrouted it until the pre-classifier claimed it).

| phrase | expected | router route @conf | verdict | source |
|---|---|---|---|---|
| Yes please | REVIEW | `CLARIFY` @0.95 | REVIEW (informational) | exhibit-a/1529 (test_offer_binding_1529.py PM_YE |
| end standup | REVIEW | `NONE` @0.85 | REVIEW (informational) | exhibit-a/1529 (test_offer_binding_1529.py PM_EN |
| i am not doing the standup right now. restore CoVa | REVIEW | `manage_portfolio` @0.95 | REVIEW (informational) | exhibit-a/1529 (test_flow_escape_1529.py PM_REFU |
| restore CoVa | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH | exhibit-a/1529 (PM live 2026-08-08 13:22, v38 —  |
| Please list my archived projects | action:manage_portfolio | `list_archived_projects` @0.99 | MISMATCH | exhibit-a/1529 (PM live 2026-08-08 13:22, v38 —  |
| what projects do I have? | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH | exhibit-a/1530 (chat omitted active CoVa; wrong  |
| what are my projects? | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH | exhibit-a/1530 (PM live 2026-08-08 13:19, v38 —  |
| remind me at 3pm tomorrow to review the PR | action:create_reminder | `create_reminder` @0.95 | MATCH | issue-1559 (turn-1 PM verbatim, #1517 T4 2026-08 |
| remind me at 9:41 today to check in with the lead develope | action:create_reminder | `create_reminder` @0.99 | MATCH | issue-1559 (adjacency gap: 'remind me at <time>  |
| Remind me tomorrow at 3pm to review the PR | action:create_reminder | `create_reminder` @0.99 | MATCH | issue-1490 (PM 8/7 original verbatim: date-then- |
| Archive my project Test. | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH | issue-1492 (trailing punctuation breaks extracti |
| Archive my project "Test" | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH | issue-1492 (quoted name breaks extraction) |
| Archive the project called Test | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH | issue-1492 ('called X' phrasing breaks extractio |
| Archive my Test project, please. | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH | issue-1492 (PM 8/7 EXACT verbatim: adjective-pos |
| Archive my project called "Test" please | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH | issue-1492 (PM 8/7 EXACT verbatim: quoted 'calle |
| archive CoVa | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH | issue-1492 comment (PM live T6, 2026-08-08 13:19 |
| what reminders do I have? | REVIEW | `list_reminders_query` @0.99 | REVIEW (informational) | probe-row-11 |

## REVIEW rows — the router's answers as data (informational, unscored)

These 54 rows are the Inversion's question book (36 probe-DISAGREEs by construction + PM's live failures). Nothing here is scored; the router's answer is recorded so the questions accumulate evidence.

| phrase | category | router route @conf | rationale | source |
|---|---|---|---|---|
| can you clarify what you meant? | QUERY | `NONE` @0.95 | User asks for clarification of prior assistant statement; co | corpus-1283 |
| show me my archived projects | QUERY | `list_archived_projects` @0.99 | User explicitly requests to view archived projects. | corpus-1283 + issue-1579 (PORTFOLIO list |
| what have you learned about my work style? | MEMORY | `pull_insights` @0.95 | User explicitly asks what the assistant has learned about th | probe-row-2 |
| connect my github | GUIDANCE | `get_contextual_guidance` @0.95 | User requests setup/configuration of GitHub integration | probe-row-3 |
| connect my notion | GUIDANCE | `get_contextual_guidance` @0.95 | User requests setup/configuration of Notion integration; des | probe-row-4 |
| link my google calendar | GUIDANCE | `get_contextual_guidance` @0.95 | User requests to connect/configure Google Calendar integrati | probe-row-6 |
| add a repo to my portfolio | PORTFOLIO | `manage_repos` @0.95 | User wants to link a GitHub repository to their project port | probe-row-7 |
| show me my todos | QUERY | `list_todos_query` @0.99 | User explicitly requests to see their todo list | probe-row-8 |
| connect my calendar | GUIDANCE | `get_contextual_guidance` @0.95 | User requests calendar integration setup; onboarding/configu | probe-row-10 |
| what reminders do I have? | TEMPORAL | `list_reminders_query` @0.99 | User asks for their reminders list | probe-row-11 |
| hello | CONVERSATION | `greeting` @0.99 | User sent a simple greeting. | probe-row-12 |
| goodbye | CONVERSATION | `farewell` @1.0 | User said goodbye; farewell operation applies. | probe-row-13 |
| thank you! | CONVERSATION | `thanks` @1.0 | Message is only an expression of gratitude | probe-row-14 |
| what can you do? | DISCOVERY | `get_capabilities` @1.0 | Direct what-can-you-do question about assistant capabilities | probe-row-15 |
| why did you suggest that? | PROVENANCE | `explain_suggestion` @0.95 | User asks for provenance of a prior suggestion. | probe-row-16 |
| why can't you create issues? | TRUST | `NONE` @0.95 | User asking about assistant capability limits; conversationa | probe-row-17 |
| what do you remember about me? | MEMORY | `get_memory` @0.95 | Direct question about stored user context and memory. | probe-row-18 |
| what's my default repo? | QUERY | `get_default_repo` @0.99 | Direct question about default repository setting | probe-row-19 |
| set my default repo to mediajunkie/piper-morgan-product | EXECUTION | `set_default_repo` @0.99 | User explicitly requests setting default repo to a named rep | probe-row-20 |
| write a short update for the CEO on the beta | SYNTHESIS | `write_stakeholder_update` @0.95 | User explicitly requests a stakeholder update for a named au | probe-row-21 |
| update the roadmap doc with the new dates | EXECUTION | `update_document` @0.85 | User requests document update with specific content (new dat | probe-row-22 |
| tell me more about the github integration | QUERY | `get_feature_info` @0.99 | User explicitly asks for details about a specific Piper feat | probe-row-23 |
| who are you? | IDENTITY | `get_identity` @0.99 | Direct who-are-you question about the assistant's identity a | probe-row-24 |
| show my recurring meetings | QUERY | `recurring_meetings` @0.99 | User explicitly requests recurring meetings list | probe-row-28 |
| what's my week look like? | QUERY | `week_calendar` @0.95 | User asking for calendar overview of the week ahead | probe-row-29 |
| what's the next milestone? | STATUS | `list_milestones` @0.85 | User asks for the next milestone; list_milestones retrieves  | probe-row-30 |
| what branch are we on? | QUERY | `local_git_status_query` @0.95 | User asking current branch status in local git repository | probe-row-31 |
| what did we ship this week? | QUERY | `shipped_this_week` @0.95 | Direct query about shipped items this week | probe-row-32 |
| show stale prs | QUERY | `stale_prs` @0.95 | User explicitly requests stale PRs list | probe-row-33 |
| close issue #123 | EXECUTION | `close_issue` @0.99 | User explicitly requests closing issue #123 | probe-row-34 |
| reopen issue #123 | EXECUTION | `reopen_issue` @0.99 | User explicitly requests reopening a specific issue by numbe | probe-row-35 |
| comment on issue #123 | EXECUTION | `comment_issue` @0.9 | User asks to comment on a specific issue; operation identifi | probe-row-36 |
| how many open issues do we have? | QUERY | `list_issues` @0.95 | User asks for count of open issues; list_issues handles issu | probe-row-37 |
| show my prs | QUERY | `list_prs` @0.95 | User explicitly requests to see their pull requests. | probe-row-38 |
| show issue #123 | QUERY | `review_issue` @0.95 | User requests to view/show a specific issue by number. | probe-row-39 |
| show milestones | QUERY | `list_milestones` @0.95 | User requests a list of milestones | probe-row-40 |
| what did we create this session? | QUERY | `session_activity_query` @0.95 | User asking for session activity recall—what was created in  | probe-row-41 |
| what's my productivity? | QUERY | `productivity` @0.95 | Direct productivity query asking for productivity metrics/ov | probe-row-42 |
| remind me to review the roadmap tomorrow | EXECUTION | `create_reminder` @0.95 | User explicitly requests a reminder for a specific task at a | probe-row-43 |
| complete todo 3 | EXECUTION | `complete_todo` @0.95 | User explicitly requests marking todo 3 as done. | probe-row-44 |
| show all my todos | QUERY | `list_todos_query` @0.99 | User explicitly requests to see all their todos. | probe-row-45 |
| what's my next todo? | QUERY | `list_todos_query` @0.95 | User asking for their next todo item from their list | probe-row-46 |
| when did I complete the onboarding project? | STATUS | `check_completion_status` @0.95 | User asks when past work (onboarding project) was completed. | probe-row-47 |
| how do I get started? | GUIDANCE | `get_contextual_guidance` @0.85 | Getting-started question; user seeks onboarding or next-step | probe-row-49 |
| what's blocking the milestone? | ANALYSIS | `analyze_blockers` @0.95 | Direct match to analyze_blockers example; user asks what is  | probe-row-50 |
| what are my priorities? | PRIORITY | `get_top_priority` @0.95 | User asking for prioritized work items or what to focus on f | probe-row-52 |
| Yes please | CONVERSATION | `CLARIFY` @0.95 | User affirmed without prior context; unclear what they're ag | exhibit-a/1529 (test_offer_binding_1529. |
| end standup | CONVERSATION | `NONE` @0.85 | Standup session control is conversational; no catalog operat | exhibit-a/1529 (test_offer_binding_1529. |
| i am not doing the standup right now. restore CoVa | PORTFOLIO | `manage_portfolio` @0.95 | User declines standup, requests project restore. | exhibit-a/1529 (test_flow_escape_1529.py |
| delete my reminders | TEMPORAL | `delete_todo` @0.95 | User explicitly requests deletion of all reminders; destruct | issue-1527 (greedy portfolio delete patt |
| hi piper, connect my github | EXECUTION | `get_contextual_guidance` @0.95 | User requests setup/configuration of GitHub integration | issue-1505 (multi-intent path drops the  |
| what time is it? also connect my github | TEMPORAL | `PLAN[get_current_time→get_contextual_guidance]` |  | issue-1755 (found during the 1505 fix, 2 |
| please clear the reminders except for "Review the PR" - | TEMPORAL | `PLAN[delete_todo→get_contextual_guidance]` |  | issue-1606 (PM live 2026-08-12: request  |
| are you able to set my default repo for me conversation | DISCOVERY | `get_capabilities` @0.85 | User asking about assistant's capability to perform a specif | issue-1606 (interrogative parsed as impe |
| use the interview from now on | STATUS | `CLARIFY` @0.4 | Ambiguous: set default document, enable a feature, or config | issue-1606 comment 2026-08-13 (PM 3:27-3 |
| use the standup interview format by default from now on | STATUS | `NONE` @0.95 | User preference/configuration request; no catalog operation  | issue-1606 comment 2026-08-13 (floor imp |
| please mark issue #108 in the mediajunkie/test-piper-mo | EXECUTION | `close_issue` @0.95 | User explicitly asks to mark issue complete; close_issue is  | issue-1606 comment 2026-08-13 (cross-dom |
| please mark 1, 2, 4, and 5 done | EXECUTION | `complete_todo` @0.95 | User explicitly requests marking multiple todos as done | PM live 2026-08-12 (#1603 session; multi |
| Create a doc from this conversation | SYNTHESIS | `NONE` @0.85 | User asks to create a doc from conversation; no catalog oper | issue-1674 (canonical Q36 mode-4 drift,  |

## Row detail (asserted rows)

| phrase | category | expected | router route @conf | verdict | note |
|---|---|---|---|---|---|
| give me my standup | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| what's on my calendar today? | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| when is my next meeting? | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| what am I working on? | STATUS | category:STATUS | `attention_query` @0.85 | MISMATCH |  |
| what should I focus on today? | PRIORITY | action:attention_query | `attention_query` @0.92 | MATCH |  |
| what are my top priorities? | PRIORITY | category:PRIORITY | `get_top_priority` @0.95 | MATCH |  |
| who am I? | IDENTITY | action:get_identity | `get_identity` @0.3 | MATCH |  |
| what's my role? | IDENTITY | category:IDENTITY | `get_identity` @0.95 | MATCH |  |
| how do I create a ticket? | GUIDANCE | category:GUIDANCE | `get_contextual_guidance` @0.95 | MATCH |  |
| create a ticket for the login bug | EXECUTION | action:create_issue | `create_issue` @0.85 | MATCH |  |
| analyze the file I uploaded | QUERY | action:analyze_data | `analyze_document` @0.95 | MISMATCH |  |
| summarize the document | SYNTHESIS | action:summarize_document | `summarize_document` @0.95 | MATCH |  |
| what time is it? | TEMPORAL | category:TEMPORAL | `get_current_time` @1.0 | MATCH |  |
| show my open issues | QUERY | action:list_issues_query | `list_issues` @0.95 | MATCH |  |
| show my open pull requests | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| any stale PRs? | QUERY | action:stale_prs_query | `stale_prs` @0.95 | MATCH |  |
| what needs my attention? | QUERY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what changed since yesterday? | QUERY | action:changes_query | `changes_query` @0.95 | MATCH |  |
| how productive was I this week? | QUERY | action:productivity_query | `productivity` @0.95 | MATCH |  |
| list my projects | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.99 | MATCH |  |
| close issue 42 | EXECUTION | action:close_issue_query | `close_issue` @0.95 | MATCH |  |
| comment on issue 42: looks good | EXECUTION | action:comment_issue_query | `comment_issue` @0.95 | MATCH |  |
| what have you learned about my workstyle? | MEMORY | action:pull_insights | `pull_insights` @0.95 | MATCH |  |
| set my default repo to acme/widgets | EXECUTION | action:set_default_repo | `set_default_repo` @0.99 | MATCH |  |
| what is my default repo? | QUERY | action:get_default_repo | `get_default_repo` @0.99 | MATCH |  |
| write a short update for the CEO on where we are | SYNTHESIS | action:write_stakeholder_update | `write_stakeholder_update` @0.95 | MATCH |  |
| update the project plan doc with the new dates | EXECUTION | action:update_document_query | `update_document` @0.85 | MATCH |  |
| give me a project status report | EXECUTION | action:update_issue | `get_project_status` @0.95 | MISMATCH |  |
| can we connect my github? | QUERY | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| connect my slack | QUERY | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| link mediajunkie/test-piper-morgan to the project | QUERY | action:manage_repos | `manage_repos` @0.95 | MATCH |  |
| help me set up github | QUERY | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| list my archived projects | PORTFOLIO | action:manage_portfolio | `list_archived_projects` @0.99 | MISMATCH |  |
| what projects have I archived? | PORTFOLIO | action:list_archived_projects | `list_archived_projects` @0.99 | MATCH |  |
| show me all project plans | QUERY | action:search_documents | `manage_portfolio` @0.85 | MISMATCH |  |
| do a standup | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| let's do a standup | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| restore CoVa | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| Please list my archived projects | PORTFOLIO | action:manage_portfolio | `list_archived_projects` @0.99 | MISMATCH |  |
| what projects do I have? | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| what are my projects? | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| remind me at 3pm tomorrow to review the PR | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| remind me at 9:41 today to check in with the lead devel | TEMPORAL | action:create_reminder | `create_reminder` @0.99 | MATCH |  |
| Remind me tomorrow at 3pm to review the PR | TEMPORAL | action:create_reminder | `create_reminder` @0.99 | MATCH |  |
| list my archive projects | PORTFOLIO | action:manage_portfolio | `list_archived_projects` @0.95 | MISMATCH |  |
| Archive my project Test. | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| Archive my project "Test" | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| Archive the project called Test | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| Archive my Test project, please. | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| Archive my project called "Test" please | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| archive CoVa | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| delete my hydrate reminder | TEMPORAL | action:delete_todo | `delete_todo` @0.95 | MATCH |  |
| remind me | TEMPORAL | action:create_reminder | `CLARIFY` @0.95 | MISMATCH | CLARIFY |
| change the status of issue #108 to Done | EXECUTION | action:update_issue | `update_issue` @0.95 | MATCH |  |
| add a reminder: test the safe clarification | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| please remind me: ask Lead how to test "outwardness dis | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| add todo buy oat milk | EXECUTION | action:create_todo | `create_todo` @0.99 | MATCH |  |
| set a reminder for the dentist appointment | TEMPORAL | action:create_reminder | `create_reminder` @0.7 | MATCH |  |
| create a reminder to call the plumber | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| don't let me forget to submit the report | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| I need to remember to submit my timesheet | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| what are my reminders | TEMPORAL | action:list_reminders_query | `list_reminders_query` @0.95 | MATCH |  |
| show reminders | TEMPORAL | action:list_reminders_query | `list_reminders_query` @0.95 | MATCH |  |
| do I have any reminders | TEMPORAL | action:list_reminders_query | `list_reminders_query` @0.95 | MATCH |  |
| show todos | QUERY | action:list_todos_query | `list_todos_query` @0.95 | MATCH |  |
| list my todos | QUERY | action:list_todos_query | `list_todos_query` @0.99 | MATCH |  |
| what are my todos | QUERY | action:list_todos_query | `list_todos_query` @0.99 | MATCH |  |
| show me completed todos | QUERY | action:list_todos_query | `list_todos_query` @0.95 | MATCH |  |
| show all todos | QUERY | action:list_todos_query | `list_todos_query` @0.95 | MATCH |  |
| next todo | QUERY | action:list_todos_query | `list_todos_query` @0.95 | MATCH |  |
| what should I do next | QUERY | action:get_top_priority | `get_top_priority` @0.85 | MATCH |  |
| what do I have next to do | QUERY | action:get_top_priority | `list_todos_query` @0.95 | MISMATCH |  |
| where should I focus this week | GUIDANCE | action:get_top_priority | `get_top_priority` @0.85 | MATCH |  |
| I could use some guidance on this | GUIDANCE | action:get_contextual_guidance | `CLARIFY` @0.3 | MISMATCH | CLARIFY |
| do you have a recommendation | GUIDANCE | action:get_contextual_guidance | `CLARIFY` @0.5 | MISMATCH | CLARIFY |
| what's your advice here | GUIDANCE | action:get_contextual_guidance | `CLARIFY` @0.3 | MISMATCH | CLARIFY |
| ok that's merged, what now? | GUIDANCE | action:get_contextual_guidance | `NONE` @0.85 | MISMATCH | NONE |
| what are the next steps | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.85 | MATCH |  |
| what should I do about this bug | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.85 | MATCH |  |
| advise me on this decision | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.85 | MATCH |  |
| what's the process for filing a bug | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| can you help me setup the integration | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.85 | MATCH |  |
| can you help me configure the connector | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.85 | MATCH |  |
| I need to setup my projects | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| how do I configure my projects | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| how do I setup the connector | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.85 | MATCH |  |
| how do I configure the connector | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.85 | MATCH |  |
| just getting started here | GUIDANCE | action:greeting | `NONE` @0.95 | MISMATCH | NONE |
| can you help me set up the integration | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.85 | MATCH |  |
| I want to set up my projects | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| how do I set up the connector | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.85 | MATCH |  |
| I'd like to set up my portfolio | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| what's my top priority | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| this is top priority for the team | PRIORITY | action:get_top_priority | `NONE` @0.85 | MISMATCH | NONE |
| this is the highest priority item | PRIORITY | action:get_top_priority | `NONE` @0.95 | MISMATCH | NONE |
| mark this as priority one | PRIORITY | action:prioritize | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| show priorities for this sprint | PRIORITY | floor | `get_top_priority` @0.85 | MISMATCH | OPERATION |
| list priorities for the team | PRIORITY | floor | `NONE` @0.85 | MATCH | NONE |
| what are my current priorities | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| what are the key priorities this quarter | PRIORITY | action:get_top_priority | `get_top_priority` @0.75 | MATCH |  |
| what's most important right now | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| what matters most this week | PRIORITY | action:get_top_priority | `attention_query` @0.85 | MISMATCH |  |
| what are the key tasks for this sprint | PRIORITY | floor | `get_top_priority` @0.85 | MISMATCH | OPERATION |
| what are the key items on my plate | PRIORITY | action:attention_query | `attention_query` @0.92 | MATCH |  |
| should i focus on the bug first | PRIORITY | action:get_top_priority | `get_top_priority` @0.75 | MATCH |  |
| what could I focus on | PRIORITY | action:get_top_priority | `get_top_priority` @0.85 | MATCH |  |
| where should my focus be today | PRIORITY | action:attention_query | `attention_query` @0.92 | MATCH |  |
| what are my focus areas this sprint | PRIORITY | action:get_top_priority | `get_contextual_guidance` @0.75 | MISMATCH |  |
| let's focus on today's priorities | PRIORITY | action:get_top_priority | `get_top_priority` @0.85 | MATCH |  |
| what's my focus this week | PRIORITY | action:get_top_priority | `week_calendar` @0.72 | MISMATCH |  |
| not sure what to focus next | PRIORITY | action:get_top_priority | `get_top_priority` @0.85 | MATCH |  |
| what's urgent right now | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what are my urgent tasks | PRIORITY | action:attention_query | `attention_query` @0.92 | MATCH |  |
| what are my urgent items | PRIORITY | action:attention_query | `attention_query` @0.92 | MATCH |  |
| what's my urgent work today | PRIORITY | action:attention_query | `attention_query` @0.92 | MATCH |  |
| what's the most urgent thing | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| what needs my focus today | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what requires attention right now | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what's critical right now | PRIORITY | action:attention_query | `attention_query` @0.92 | MATCH |  |
| what are my critical tasks | PRIORITY | action:attention_query | `attention_query` @0.85 | MATCH |  |
| what are my critical items | PRIORITY | action:attention_query | `attention_query` @0.92 | MATCH |  |
| what's my critical work today | PRIORITY | action:attention_query | `attention_query` @0.85 | MATCH |  |
| what's the most critical thing | PRIORITY | action:get_top_priority | `get_top_priority` @0.85 | MATCH |  |
| what should I do first | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| what should I tackle next | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| what's next for me | PRIORITY | action:get_top_priority | `get_top_priority` @0.85 | MATCH |  |
| what should I review first | PRIORITY | action:get_top_priority | `get_top_priority` @0.85 | MATCH |  |
| which project should get my focus today | PRIORITY | action:get_top_priority | `get_top_priority` @0.92 | MATCH |  |
| which task should get my focus next | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| not sure what to do about this | PRIORITY | action:get_contextual_guidance | `CLARIFY` @0.85 | MISMATCH | CLARIFY |
| what is on my calendar | QUERY | action:meeting_time | `week_calendar` @0.85 | MISMATCH |  |
| show me my calendar today | QUERY | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| calendar today please | QUERY | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| what meetings today | QUERY | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| do i have any meetings | QUERY | action:meeting_time | `meeting_time` @0.85 | MATCH |  |
| do i have meetings | QUERY | action:meeting_time | `meeting_time` @0.85 | MATCH |  |
| what meetings do i have | QUERY | action:meeting_time | `meeting_time` @0.7 | MATCH |  |
| what meetings are coming up | QUERY | action:meeting_time | `week_calendar` @0.85 | MISMATCH |  |
| what's my schedule today | QUERY | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| today's schedule please | QUERY | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| what's the schedule for today | QUERY | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| what's my agenda today | QUERY | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| what's my agenda tomorrow | QUERY | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| what's my agenda this week | QUERY | action:week_calendar | `week_calendar` @0.95 | MATCH |  |
| what's my agenda next week | QUERY | action:week_calendar | `week_calendar` @0.95 | MATCH |  |
| show me my agenda | QUERY | action:meeting_time | `meeting_time` @0.85 | MATCH |  |
| show me calendar for tomorrow | QUERY | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| tomorrow's calendar please | QUERY | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| how many meetings do I have tomorrow | QUERY | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| what's the schedule tomorrow | QUERY | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| tomorrow's schedule please | QUERY | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| what's happening tomorrow | QUERY | action:meeting_time | `meeting_time` @0.85 | MATCH |  |
| show calendar this week | QUERY | action:week_calendar | `week_calendar` @0.95 | MATCH |  |
| show calendar next week | QUERY | action:week_calendar | `week_calendar` @0.95 | MATCH |  |
| what's the schedule this week | QUERY | action:week_calendar | `week_calendar` @0.95 | MATCH |  |
| what's the schedule next week | QUERY | action:week_calendar | `week_calendar` @0.95 | MATCH |  |
| how many meetings this week | QUERY | action:week_calendar | `week_calendar` @0.95 | MATCH |  |
| how many meetings next week | QUERY | action:week_calendar | `week_calendar` @0.95 | MATCH |  |
| how much time in meetings do I have | QUERY | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| how much time do I spend sitting in meetings | QUERY | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| time spent in meetings is high lately | QUERY | floor | `NONE` @0.95 | MATCH | NONE |
| what's my meeting time today | QUERY | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| let's review my recurring meetings | QUERY | action:recurring_meetings | `recurring_meetings` @0.95 | MATCH |  |
| audit my standing meetings | QUERY | action:recurring_meetings | `recurring_meetings` @0.92 | MATCH |  |
| recurring meetings keep piling up | QUERY | floor | `NONE` @0.85 | MATCH | NONE |
| show me my week | QUERY | action:week_calendar | `week_calendar` @0.95 | MATCH |  |
| what's the week ahead look like | QUERY | action:week_calendar | `week_calendar` @0.95 | MATCH |  |
| show the week calendar | QUERY | action:week_calendar | `week_calendar` @0.95 | MATCH |  |
| check my calendar for conflicts | QUERY | floor | `NONE` @0.85 | MATCH | NONE |
| is my calendar showing any conflict | QUERY | floor | `week_calendar` @0.72 | MISMATCH | OPERATION |
| does my calendar overlap with hers | QUERY | floor | `CLARIFY` @0.4 | MATCH | CLARIFY |
| is there a conflict on my calendar | QUERY | floor | `week_calendar` @0.7 | MISMATCH | OPERATION |
| find time for a 1:1 with sarah | QUERY | floor | `NONE` @0.85 | MATCH | NONE |
| find some time for a sync | QUERY | floor | `NONE` @0.85 | MATCH | NONE |
| schedule a quick call | QUERY | floor | `NONE` @0.95 | MATCH | NONE |
| book a slot with the team | QUERY | floor | `NONE` @0.95 | MATCH | NONE |
| what's the time | TEMPORAL | action:get_current_time | `get_current_time` @0.99 | MATCH |  |
| current time please | TEMPORAL | action:get_current_time | `get_current_time` @0.99 | MATCH |  |
| give me the time now | TEMPORAL | action:get_current_time | `get_current_time` @1.0 | MATCH |  |
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
| pull up my calendar | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| show the team calendar | TEMPORAL | floor | `NONE` @0.85 | MATCH | NONE |
| pull up my schedule | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| show the team schedule | TEMPORAL | floor | `CLARIFY` @0.4 | MATCH | CLARIFY |
| calendar check for today | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| schedule check for today | TEMPORAL | action:meeting_time | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| walk me through my appointments | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| show all appointments | TEMPORAL | action:week_calendar | `week_calendar` @0.75 | MATCH |  |
| walk me through my meetings | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| what are the upcoming meetings | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| when is my team meeting | TEMPORAL | action:meeting_time | `meeting_time` @0.72 | MATCH |  |
| when am i in a meeting | TEMPORAL | action:meeting_time | `meeting_time` @0.85 | MATCH |  |
| meeting check for today | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| meeting check for tomorrow | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| walk me through my events | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| show all events | TEMPORAL | action:week_calendar | `CLARIFY` @0.6 | MISMATCH | CLARIFY |
| what are the upcoming events | TEMPORAL | action:week_calendar | `week_calendar` @0.75 | MATCH |  |
| events check for today | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| events check for tomorrow | TEMPORAL | action:meeting_time | `meeting_time` @0.92 | MATCH |  |
| when's the next event | TEMPORAL | action:meeting_time | `meeting_time` @0.85 | MATCH |  |
| what did I work on today | TEMPORAL | action:session_activity_query | `session_activity_query` @0.95 | MATCH |  |
| what happened in the meeting yesterday | TEMPORAL | floor | `NONE` @0.95 | MATCH | NONE |
| did I finish the report yesterday | TEMPORAL | action:check_completion_status | `check_completion_status` @0.92 | MATCH |  |
| a lot happened yesterday | TEMPORAL | action:changes_query | `changes_query` @0.92 | MATCH |  |
| when was the last time I worked on this | TEMPORAL | floor | `CLARIFY` @0.5 | MATCH | CLARIFY |
| how long have I been working on this | TEMPORAL | floor | `CLARIFY` @0.4 | MATCH | CLARIFY |
| this week's priorities, remind me | TEMPORAL | plan | `PLAN[get_top_priority→create_reminder]` | MATCH | PLAN[get_top_priority→create_reminder] |
| next week's priorities, remind me | TEMPORAL | plan | `PLAN[get_top_priority→create_reminder]` | MATCH | PLAN[get_top_priority→create_reminder] |
| this month's numbers, remind me | TEMPORAL | plan | `PLAN[generate_report→create_reminder]` | MATCH | PLAN[generate_report→create_reminder] |
| when am i free | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| when's my next free slot | TEMPORAL | action:meeting_time | `week_calendar` @0.72 | MISMATCH |  |
| what's my available time | TEMPORAL | action:week_calendar | `CLARIFY` @0.6 | MISMATCH | CLARIFY |
| when do I have free time | TEMPORAL | action:week_calendar | `CLARIFY` @0.6 | MISMATCH | CLARIFY |
| what are my open slots | TEMPORAL | action:week_calendar | `NONE` @0.85 | MISMATCH | NONE |
