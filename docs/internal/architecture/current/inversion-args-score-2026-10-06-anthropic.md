# Inversion Phase-1 shadow score — CONSTRAINED ROUTER vs Phase-0 baseline
Run: 2026-10-06 13:51Z · corpus: inversion_corpus_phase0.yaml (514 rows) · scripts/inversion_phase1_shadow_score.py
Served (#1620 — resolved, post-fallback, per row): anthropic:claude-haiku-4-5 (514/514)

LAYER (m-43): **router only, context-free** — one constrained Haiku-class call per row (514 LLM calls incl. repair retries; 0 ERROR, 0 REFUSED), grammar derived from the live registry at run time (71 canonical operations, 86 input-side aliases collapsed, + NONE/CLARIFY). The production chain was NOT executed in this run; the baseline column is Phase-0's FULL-CHAIN production decision (inversion-phase0-baseline-full-2026-08-12.md). Context-dependent rows (the 1529 offer/flow family) ran WITHOUT session state — their answers are informational for Phase 2, not its measured shape.

## Per-category vs baseline (denominators stated — m-44)

| category | rows | asserted | router match | baseline match | Δ | REVIEW | gate |
|---|---|---|---|---|---|---|---|
| QUERY | 162 | 147 | 138 | 12/13 | +126 | 15 | no regression |
| TEMPORAL | 69 | 66 | 59 | 4/4 | +55 | 3 | no regression |
| STATUS | 54 | 50 | 37 | 1/4 | +36 | 4 | no regression |
| PRIORITY | 44 | 43 | 32 | 2/2 | +30 | 1 | no regression |
| EXECUTION | 40 | 30 | 26 | 5/6 | +21 | 10 | no regression |
| PORTFOLIO | 31 | 29 | 10 | 6/7 | +4 | 2 | no regression |
| GUIDANCE | 26 | 21 | 16 | 1/1 | +15 | 5 | no regression |
| DISCOVERY | 25 | 24 | 23 | 0/0 | +23 | 1 | no regression |
| MEMORY | 23 | 21 | 18 | 1/1 | +17 | 2 | no regression |
| ANALYSIS | 15 | 14 | 10 | 0/0 | +10 | 1 | no regression |
| TRUST | 11 | 10 | 10 | 0/0 | +10 | 1 | no regression |
| CONVERSATION | 5 | 0 | 0 | 0/0 | — | 5 | **UNGATEABLE** (REVIEW-only denominator) |
| SYNTHESIS | 4 | 2 | 2 | 2/2 | +0 | 2 | no regression |
| IDENTITY | 3 | 2 | 2 | 2/2 | +0 | 1 | no regression |
| PROVENANCE | 2 | 1 | 1 | 0/0 | +1 | 1 | no regression |
| **TOTAL** | 514 | 460 | 384 | 36/39 | +348 | 54 | (aggregate is NOT the gate) |

### Target-set assertions (`expected_args`, Arch's (a))

| category | rows asserting args | action AND args right | ARGS_MISMATCH rows |
|---|---|---|---|
| EXECUTION | 13 | 12 | 1 |

ARGS_MISMATCH detail (expected vs served):

- `Mark the first three complete and leave the fourth one pending.` → complete_todo; ARGS exclude: ['4']≠[]

Gate reading (Arch condition 1 as amended 08-09 08:3x, PPM): **no category may regress; the aggregate is never the gate** (the M2 precedent: 72.1% aggregate passed while a category was broken). CONVERSATION / DISCOVERY / PROVENANCE / TRUST / ANALYSIS have REVIEW-only denominators in Phase 0 and remain **ungateable** here — same as Phase 0 stated; growing asserted expectations there is outstanding Phase-0 work, not a Phase-1 scoring artifact.

⚠️ **m-44: the table above compares two different denominators** (this run's 116-row corpus vs the baseline's 93-row corpus) — its `Δ`/`gate` cells are INFORMATIONAL ONLY from this run forward. The shared-subset table below, scored on rows asserted in BOTH corpora, is the actual gate.

## Shared-subset score vs 2026-08-12 baseline (m-44 fix — THIS is the gate)

Matching rule: phrase normalized (strip + collapse whitespace + casefold), exact match required; on a miss, fall back to an unambiguous ≥20-char prefix match in either direction (markdown row-detail tables truncate long phrases with no ellipsis, at different fixed lengths in different docs). Only rows asserted (non-REVIEW) on BOTH sides are scored here; the per-category table above compares two different denominators and is informational only from this point forward.

| category | shared asserted | router match | baseline match | gate |
|---|---|---|---|---|
| QUERY | 12 | 10/12 | 12/12 | **REGRESSION** |
| PORTFOLIO | 7 | 3/7 | 6/7 | **REGRESSION** |
| EXECUTION | 6 | 5/6 | 5/6 | no regression |
| TEMPORAL | 4 | 4/4 | 4/4 | no regression |
| STATUS | 2 | 1/2 | 1/2 | no regression |
| PRIORITY | 2 | 2/2 | 2/2 | no regression |
| IDENTITY | 2 | 2/2 | 2/2 | no regression |
| SYNTHESIS | 2 | 2/2 | 2/2 | no regression |
| GUIDANCE | 1 | 1/1 | 1/1 | no regression |
| MEMORY | 1 | 1/1 | 1/1 | no regression |

**Named regressions** (baseline matched, router did not — the specific rows behind each REGRESSION cell above):
- [PORTFOLIO] `what projects do I have?`
- [PORTFOLIO] `Archive my project Test.`
- [PORTFOLIO] `Archive my project "Test"`
- [PORTFOLIO] `Archive the project called Test`
- [QUERY] `analyze the file I uploaded`
- [QUERY] `link mediajunkie/test-piper-morgan to the project`
- [STATUS] `what am I working on?`

**Denominator deltas (m-44)** — rows in the 08-12 baseline no longer asserted in the current corpus (dropped), and rows asserted now that the baseline never saw (added). Neither is scored above; both are why the totals table's Δ column is informational, not the gate.

Dropped (baseline-asserted, not in current corpus):
- none

Added (current-asserted, not in the 08-12 baseline):
- [ANALYSIS] what is blocking this release
- [ANALYSIS] what tasks are blocking our sprint
- [ANALYSIS] blockers for the release
- [ANALYSIS] what's the main obstacle here
- [ANALYSIS] what's in the way of finishing this
- [ANALYSIS] let's analyze the risk here
- [ANALYSIS] I'd like a risk assessment for this project
- [ANALYSIS] can you run an impact analysis on this change
- [ANALYSIS] what risks does this project have
- [ANALYSIS] what risk do we have in this plan
- [ANALYSIS] please identify the risks in this plan
- [ANALYSIS] risks we should flag before launch
- [ANALYSIS] threats to our timeline this week
- [ANALYSIS] what could threaten this deadline
- [DISCOVERY] are you able to set my default repo for me conversationally?
- [DISCOVERY] what are your capabilities?
- [DISCOVERY] what services can you provide?
- [DISCOVERY] what do you offer as an assistant?
- [DISCOVERY] what features does piper have?
- [DISCOVERY] what can you help me do today?
- [DISCOVERY] show me your capabilities
- [DISCOVERY] give me a menu of services
- [DISCOVERY] can you list your capabilities
- [DISCOVERY] I want to understand your capabilities better
- [DISCOVERY] pull up the capability menu
- [DISCOVERY] open the capabilities menu
- [DISCOVERY] show me the menu
- [DISCOVERY] what are you able to do for my project
- [DISCOVERY] show me the features you offer
- [DISCOVERY] what's available in terms of features
- [DISCOVERY] help
- [DISCOVERY] open the help menu
- [DISCOVERY] can you show help topics
- [DISCOVERY] I need help understanding something
- [DISCOVERY] is there a bottleneck analysis available
- [DISCOVERY] what can't you do here
- [DISCOVERY] what are your limits as an assistant
- [DISCOVERY] what's the capability boundary here
- [EXECUTION] Mark the first three complete and leave the fourth one pending.
- [EXECUTION] Mark the first one complete and leave the second one pending.
- [EXECUTION] I want you to clear 'check the test card again,' and 'review the pr' — mark them done
- [EXECUTION] mark all my reminders done except for 'revise the pr'
- [EXECUTION] mark the first two complete
- [EXECUTION] complete the last one
- [EXECUTION] mark #2 as done
- [EXECUTION] mark todo 3 as complete
- [EXECUTION] mark 1, 2 and 4 done
- [EXECUTION] complete 'review the pr'
- [EXECUTION] finish the second one
- [EXECUTION] I'm done with the first and the third
- [EXECUTION] mark the PR review todo as done
- [EXECUTION] mark everything done except the last one
- [EXECUTION] change the status of issue #108 to Done
- [EXECUTION] add todo buy oat milk
- [EXECUTION] close the completed issue
- [EXECUTION] please close this issue
- [EXECUTION] re-open issue 88
- [EXECUTION] reopen the old issue
- [EXECUTION] re-open the old issue
- [EXECUTION] add comment to issue 99
- [EXECUTION] reply to issue 99
- [EXECUTION] comment on 99
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
- [MEMORY] how well do you know me by now
- [MEMORY] what can you remember about our last conversation
- [MEMORY] do you remember my last project update
- [MEMORY] remember when we shipped the last release?
- [MEMORY] can you show my conversation history
- [MEMORY] our history together has been good
- [MEMORY] let's look at past conversations we've had
- [MEMORY] pull up my previous messages please
- [MEMORY] can I see the conversation log
- [MEMORY] find when I mentioned this bug before
- [MEMORY] search history for that conversation topic
- [MEMORY] what did we discuss in our last session
- [MEMORY] what we discussed yesterday was helpful
- [MEMORY] how long is your memory exactly
- [MEMORY] what do you know about my work habits
- [MEMORY] tell me what you've learned about my habits
- [MEMORY] what insights do you have about my productivity
- [MEMORY] show me what you've learned about my preferences
- [MEMORY] what patterns have you noticed in my work
- [MEMORY] what have you noticed about my habits lately
- [PORTFOLIO] show me my archived projects
- [PORTFOLIO] update my project name to Atlas
- [PORTFOLIO] edit my project description
- [PORTFOLIO] restore CoVa
- [PORTFOLIO] Please list my archived projects
- [PORTFOLIO] what are my projects?
- [PORTFOLIO] list my archive projects
- [PORTFOLIO] Archive my Test project, please.
- [PORTFOLIO] Archive my project called "Test" please
- [PORTFOLIO] archive CoVa
- [PORTFOLIO] link my repository to the project
- [PORTFOLIO] connect my repository to the project
- [PORTFOLIO] connect octocat/hello-world to the project
- [PORTFOLIO] add octocat/hello-world to the project
- [PORTFOLIO] please unlink my repository from this project
- [PORTFOLIO] please remove my repository from this project
- [PORTFOLIO] please disconnect my repository from this project
- [PORTFOLIO] please show my linked repos
- [PORTFOLIO] which repo connected to this project should i check
- [PORTFOLIO] can you show project repositories for this account
- [PORTFOLIO] list my repos on github
- [PORTFOLIO] show all of my repos
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
- [PRIORITY] what's my most important task right now
- [PRIORITY] what is my most important work today
- [PRIORITY] what should I work on next
- [PROVENANCE] why are you always cautious about this suggestion
- [QUERY] show issue #123
- [QUERY] show milestones
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
- [QUERY] what shipped recently
- [QUERY] can you show what has shipped
- [QUERY] what has shipped this past week
- [QUERY] show our stale pull requests
- [QUERY] any old prs lying around
- [QUERY] prs needing review
- [QUERY] review issue 101
- [QUERY] issue 101 details
- [QUERY] get issue 101
- [QUERY] what are my issues
- [QUERY] list the issues please
- [QUERY] show the issues
- [QUERY] what's the issue count
- [QUERY] which issues are assigned to engineering
- [QUERY] show my pull requests
- [QUERY] what are my prs looking like
- [QUERY] where are my pull requests
- [QUERY] list the prs
- [QUERY] list all pull requests from this sprint
- [QUERY] any open prs waiting on me
- [QUERY] any prs assigned to me
- [QUERY] any pull requests assigned to me
- [QUERY] list the milestones for this quarter
- [QUERY] any update on the next milestone
- [QUERY] what milestones do we have
- [QUERY] milestones due this month
- [QUERY] when's the milestone deadline
- [QUERY] any recent releases
- [QUERY] show me the releases
- [QUERY] list our releases
- [QUERY] what version are we on
- [QUERY] what's the current release
- [QUERY] what's our latest release
- [QUERY] what labels do we use
- [QUERY] show me the labels
- [QUERY] list the labels
- [QUERY] what are the issue labels
- [QUERY] labels count please
- [QUERY] all labels please
- [QUERY] show me the active branches
- [QUERY] show which branches exist
- [QUERY] list the branches
- [QUERY] what feature branches do we have
- [QUERY] what are the current branches
- [QUERY] what branches do we have
- [QUERY] what's changed since last week
- [QUERY] show me the changes since last monday
- [QUERY] show me everything that's changed
- [QUERY] any changes since the last deploy
- [QUERY] give me the activity since yesterday's standup
- [QUERY] any updates since this morning
- [QUERY] what needs attention right now
- [QUERY] this project needs my attention today
- [QUERY] show me what needs the most attention
- [QUERY] the items that need attention haven't been touched
- [QUERY] please list the attention items for review
- [QUERY] which repository is my default
- [QUERY] please show my default repository
- [QUERY] my default repository
- [QUERY] what branch am i on right now
- [QUERY] which branch are we on at the moment
- [QUERY] can you tell me the current branch
- [QUERY] what's the working tree status
- [QUERY] are there any uncommitted changes
- [QUERY] do we have a dirty working tree
- [QUERY] are we ahead of origin right now
- [QUERY] are we behind upstream at all
- [QUERY] do we have any unpushed commits
- [QUERY] can you show the local git status
- [QUERY] please run git status for me
- [QUERY] show me my productivity report
- [QUERY] can you share my productivity metrics
- [QUERY] i'd like to check my productivity this week
- [QUERY] what have we created so far
- [QUERY] what did we make earlier
- [QUERY] what did i create this session
- [QUERY] what did we do this session
- [QUERY] what issues did we open during the call
- [STATUS] do a standup
- [STATUS] let's do a standup
- [STATUS] time for my stand-up
- [STATUS] give me my stand up
- [STATUS] give me a standup update
- [STATUS] give me a standup report
- [STATUS] what's my daily standup
- [STATUS] show today's standup
- [STATUS] show me my portfolio
- [STATUS] list my active projects for this quarter
- [STATUS] any upcoming milestones for this project
- [STATUS] what's my current project
- [STATUS] can you summarize my current work
- [STATUS] what are my current projects
- [STATUS] give me a project overview
- [STATUS] what's the project landscape
- [STATUS] what projects am I working on
- [STATUS] tell me what I'm working on
- [STATUS] quick check, working on now?
- [STATUS] what are my active projects
- [STATUS] show my active work
- [STATUS] what's my status
- [STATUS] give me a status update
- [STATUS] what is my status
- [STATUS] what's my work status
- [STATUS] show the current status
- [STATUS] what's the current status
- [STATUS] I need a status report
- [STATUS] what's my progress
- [STATUS] give me a progress update
- [STATUS] I need a progress report
- [STATUS] what's the progress on this
- [STATUS] show today's progress
- [STATUS] what's the current progress
- [STATUS] how's the progress going
- [STATUS] what's the progress looking like
- [STATUS] what are my tasks
- [STATUS] show me my current tasks
- [STATUS] what are my active tasks
- [STATUS] show today's tasks
- [STATUS] list today's tasks
- [STATUS] tasks I'm actively working on
- [STATUS] what tasks do I have
- [STATUS] what's the task status
- [STATUS] what are my assignments
- [STATUS] show me my current assignments
- [STATUS] what's assigned to me
- [STATUS] show today's assignments
- [TEMPORAL] remind me at 3pm tomorrow to review the PR
- [TEMPORAL] Remind me tomorrow at 3pm to review the PR
- [TEMPORAL] delete my hydrate reminder
- [TEMPORAL] remind me
- [TEMPORAL] please clear the reminders except for "Review the PR" - also, are you able to set my default repo for me conversationally?
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
- [TRUST] why won't you create issues for me
- [TRUST] why don't you just do it yourself
- [TRUST] do you trust me with this decision
- [TRUST] how much do you trust my judgment
- [TRUST] what's our relationship like these days
- [TRUST] how do you see our relationship evolving
- [TRUST] how do we work together on this project
- [TRUST] why did you go ahead without asking
- [TRUST] why do you always ask me the same thing
- [TRUST] i didn't ask you to do that

## Exhibit A (PM 2026-08-08 live transcript) + Arch's demanded row

Selection rule: corpus `source` containing one of ('exhibit-a', 'issue-1559', 'issue-1492') → 16 rows (the 8 Exhibit-A failures), plus the demanded row `"what reminders do I have?"` (probe-row-11, REVIEW — the sharpest test of the thesis: the LLM classifier misrouted it until the pre-classifier claimed it).

| phrase | expected | router route @conf | verdict | source |
|---|---|---|---|---|
| Yes please | REVIEW | `CLARIFY` @0.95 | REVIEW (informational) | exhibit-a/1529 (test_offer_binding_1529.py PM_YE |
| end standup | REVIEW | `NONE` @0.85 | REVIEW (informational) | exhibit-a/1529 (test_offer_binding_1529.py PM_EN |
| i am not doing the standup right now. restore CoVa | REVIEW | `restore_project` @0.95 | REVIEW (informational) | exhibit-a/1529 (test_flow_escape_1529.py PM_REFU |
| restore CoVa | action:manage_portfolio | `restore_project` @0.95 | MISMATCH | exhibit-a/1529 (PM live 2026-08-08 13:22, v38 —  |
| Please list my archived projects | action:list_archived_projects | `list_archived_projects` @0.99 | MATCH | exhibit-a/1529 (PM live 2026-08-08 13:22, v38 —  |
| what projects do I have? | action:manage_portfolio | `list_projects` @0.95 | MISMATCH | exhibit-a/1530 (chat omitted active CoVa; wrong  |
| what are my projects? | action:manage_portfolio | `list_projects` @0.95 | MISMATCH | exhibit-a/1530 (PM live 2026-08-08 13:19, v38 —  |
| remind me at 3pm tomorrow to review the PR | action:create_reminder | `create_reminder` @0.99 | MATCH | issue-1559 (turn-1 PM verbatim, #1517 T4 2026-08 |
| remind me at 9:41 today to check in with the lead develope | action:create_reminder | `create_reminder` @0.99 | MATCH | issue-1559 (adjacency gap: 'remind me at <time>  |
| Remind me tomorrow at 3pm to review the PR | action:create_reminder | `create_reminder` @0.99 | MATCH | issue-1490 (PM 8/7 original verbatim: date-then- |
| Archive my project Test. | action:manage_portfolio | `archive_project` @0.99 | MISMATCH | issue-1492 (trailing punctuation breaks extracti |
| Archive my project "Test" | action:manage_portfolio | `archive_project` @0.99 | MISMATCH | issue-1492 (quoted name breaks extraction) |
| Archive the project called Test | action:manage_portfolio | `archive_project` @0.99 | MISMATCH | issue-1492 ('called X' phrasing breaks extractio |
| Archive my Test project, please. | action:manage_portfolio | `archive_project` @0.95 | MISMATCH | issue-1492 (PM 8/7 EXACT verbatim: adjective-pos |
| Archive my project called "Test" please | action:manage_portfolio | `archive_project` @0.99 | MISMATCH | issue-1492 (PM 8/7 EXACT verbatim: quoted 'calle |
| archive CoVa | action:manage_portfolio | `archive_project` @0.95 | MISMATCH | issue-1492 comment (PM live T6, 2026-08-08 13:19 |
| what reminders do I have? | REVIEW | `list_reminders_query` @0.99 | REVIEW (informational) | probe-row-11 |

## REVIEW rows — the router's answers as data (informational, unscored)

These 54 rows are the Inversion's question book (36 probe-DISAGREEs by construction + PM's live failures). Nothing here is scored; the router's answer is recorded so the questions accumulate evidence.

| phrase | category | router route @conf | rationale | source |
|---|---|---|---|---|
| can you clarify what you meant? | QUERY | `CLARIFY` @0.95 | User asks for clarification but no prior suggestion or state | corpus-1283 |
| what have you learned about my work style? | MEMORY | `pull_insights` @0.99 | Direct what-have-you-learned question about work style patte | probe-row-2 |
| connect my github | GUIDANCE | `get_contextual_guidance` @0.95 | User requests GitHub integration setup; guidance on connecti | probe-row-3 |
| connect my notion | GUIDANCE | `get_contextual_guidance` @0.95 | User requests to set up or connect Notion integration — onbo | probe-row-4 |
| link my google calendar | GUIDANCE | `get_contextual_guidance` @0.95 | User requests setup/configuration of a calendar integration  | probe-row-6 |
| add a repo to my portfolio | PORTFOLIO | `CLARIFY` @0.4 | Ambiguous: link repo to existing project, or add new project | probe-row-7 |
| show me my todos | QUERY | `list_todos_query` @0.99 | User explicitly requests to see their todo list | probe-row-8 |
| connect my calendar | GUIDANCE | `get_contextual_guidance` @0.95 | User requests calendar integration setup; guidance operation | probe-row-10 |
| what reminders do I have? | TEMPORAL | `list_reminders_query` @0.99 | Direct request to list reminders | probe-row-11 |
| hello | CONVERSATION | `greeting` @0.99 | User sent a simple greeting | probe-row-12 |
| goodbye | CONVERSATION | `farewell` @1.0 | User is saying goodbye; a pleasantry-only farewell. | probe-row-13 |
| thank you! | CONVERSATION | `thanks` @1.0 | Message is only an expression of gratitude | probe-row-14 |
| what can you do? | DISCOVERY | `get_capabilities` @0.99 | Direct question about assistant capabilities and features | probe-row-15 |
| why did you suggest that? | PROVENANCE | `explain_suggestion` @0.95 | User asking for provenance of a prior suggestion | probe-row-16 |
| why can't you create issues? | TRUST | `explain_trust` @0.92 | User asking why the assistant can't/won't do something — wor | probe-row-17 |
| what do you remember about me? | MEMORY | `get_memory` @0.99 | Direct question about what the assistant remembers about the | probe-row-18 |
| what's my default repo? | QUERY | `get_default_repo` @0.99 | Direct question about default repository setting | probe-row-19 |
| set my default repo to mediajunkie/piper-morgan-product | EXECUTION | `set_default_repo` @0.99 | User explicitly requests setting default repo with owner/rep | probe-row-20 |
| write a short update for the CEO on the beta | SYNTHESIS | `write_stakeholder_update` @0.95 | User explicitly requests a stakeholder update for a named au | probe-row-21 |
| update the roadmap doc with the new dates | EXECUTION | `update_document` @0.85 | User asks to update a document with new content (dates). Slo | probe-row-22 |
| tell me more about the github integration | QUERY | `get_feature_info` @0.99 | User explicitly asks for details about a specific Piper feat | probe-row-23 |
| who are you? | IDENTITY | `get_identity` @0.99 | Direct who-are-you question about the assistant's identity a | probe-row-24 |
| show my recurring meetings | QUERY | `recurring_meetings` @0.95 | User explicitly asks to show recurring meetings | probe-row-28 |
| what's my week look like? | QUERY | `week_calendar` @0.99 | User asking for calendar overview of the week ahead | probe-row-29 |
| what's the next milestone? | STATUS | `list_milestones` @0.92 | User asking for the next upcoming milestone in their project | probe-row-30 |
| what branch are we on? | QUERY | `local_git_status_query` @0.95 | Direct question about current Git branch status | probe-row-31 |
| what did we ship this week? | QUERY | `shipped_this_week` @0.95 | Direct query about shipped releases this week | probe-row-32 |
| show stale prs | QUERY | `stale_prs` @0.95 | User explicitly requests stale PRs report | probe-row-33 |
| close issue #123 | EXECUTION | `close_issue` @0.95 | User explicitly requests closing a specific issue by number. | probe-row-34 |
| reopen issue #123 | EXECUTION | `reopen_issue` @0.95 | User explicitly requests reopening a specific issue by numbe | probe-row-35 |
| comment on issue #123 | EXECUTION | `comment_issue` @0.95 | User asks to comment on a specific issue number. | probe-row-36 |
| how many open issues do we have? | QUERY | `list_issues` @0.95 | User asks for a count of open issues across their repos | probe-row-37 |
| show my prs | QUERY | `list_prs` @0.95 | User asks to show their pull requests | probe-row-38 |
| what did we create this session? | QUERY | `session_activity_query` @0.95 | User asks what was created in the current session only | probe-row-41 |
| what's my productivity? | QUERY | `productivity` @0.95 | Direct productivity query requesting metrics or analysis of  | probe-row-42 |
| remind me to review the roadmap tomorrow | EXECUTION | `create_reminder` @0.95 | User explicitly requests a reminder for a specific task at a | probe-row-43 |
| complete todo 3 | EXECUTION | `complete_todo` @0.99 | User explicitly requests marking todo item 3 as done. | probe-row-44 |
| show all my todos | QUERY | `list_todos_query` @0.99 | User requests a listing of all their todos | probe-row-45 |
| what's my next todo? | QUERY | `list_todos_query` @0.95 | User asking for their next todo item from their todo list | probe-row-46 |
| when did I complete the onboarding project? | STATUS | `check_completion_status` @0.95 | User asks when past work (project completion) was finished. | probe-row-47 |
| how do I get started? | GUIDANCE | `get_contextual_guidance` @0.95 | Getting-started question; user seeks onboarding or initial g | probe-row-49 |
| what's blocking the milestone? | ANALYSIS | `analyze_blockers` @0.95 | Direct question about what is blocking a milestone | probe-row-50 |
| what are my priorities? | PRIORITY | `get_top_priority` @0.95 | User asking what to work on first or prioritize | probe-row-52 |
| Yes please | CONVERSATION | `CLARIFY` @0.95 | Affirmative response without prior context; unclear what is  | exhibit-a/1529 (test_offer_binding_1529. |
| end standup | CONVERSATION | `NONE` @0.85 | Ending standup is conversational; no catalog operation handl | exhibit-a/1529 (test_offer_binding_1529. |
| i am not doing the standup right now. restore CoVa | PORTFOLIO | `restore_project` @0.95 | User declines standup, requests project restoration by name. | exhibit-a/1529 (test_flow_escape_1529.py |
| delete my reminders | TEMPORAL | `delete_todo` @0.95 | User explicitly requests deletion of all reminders — destruc | issue-1527 (greedy portfolio delete patt |
| hi piper, connect my github | EXECUTION | `get_contextual_guidance` @0.95 | User requests GitHub integration setup; guidance on connecti | issue-1505 (multi-intent path drops the  |
| what time is it? also connect my github | TEMPORAL | `PLAN[get_current_time→get_contextual_guidance]` |  | issue-1755 (found during the 1505 fix, 2 |
| use the interview from now on | STATUS | `CLARIFY` @0.4 | Ambiguous: set default document, configure integration, or c | issue-1606 comment 2026-08-13 (PM 3:27-3 |
| use the standup interview format by default from now on | STATUS | `get_contextual_guidance` @0.72 | User requests setup/configuration of a default behavior; gui | issue-1606 comment 2026-08-13 (floor imp |
| please mark issue #108 in the mediajunkie/test-piper-mo | EXECUTION | `close_issue` @0.95 | User requests closing issue #108 in a specific repo | issue-1606 comment 2026-08-13 (cross-dom |
| please mark 1, 2, 4, and 5 done | EXECUTION | `complete_todo` @0.99 | User explicitly requests marking multiple todos as done by o | PM live 2026-08-12 (#1603 session; multi |
| Create a doc from this conversation | SYNTHESIS | `NONE` @0.85 | Document creation from conversation is out of scope; no cata | issue-1674 (canonical Q36 mode-4 drift,  |

## Row detail (asserted rows)

| phrase | category | expected | router route @conf | verdict | note |
|---|---|---|---|---|---|
| give me my standup | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| what's on my calendar today? | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| when is my next meeting? | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| what am I working on? | STATUS | floor | `session_activity_query` @0.7 | MISMATCH | OPERATION |
| what should I focus on today? | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what are my top priorities? | PRIORITY | category:PRIORITY | `get_top_priority` @0.95 | MATCH |  |
| who am I? | IDENTITY | action:get_identity | `get_identity` @0.95 | MATCH |  |
| what's my role? | IDENTITY | category:IDENTITY | `get_identity` @0.95 | MATCH |  |
| how do I create a ticket? | GUIDANCE | category:GUIDANCE | `get_contextual_guidance` @0.95 | MATCH |  |
| create a ticket for the login bug | EXECUTION | action:create_issue | `create_issue` @0.85 | MATCH |  |
| analyze the file I uploaded | QUERY | action:analyze_data | `analyze_document` @0.95 | MISMATCH |  |
| summarize the document | SYNTHESIS | action:summarize_document | `summarize_document` @0.95 | MATCH |  |
| what time is it? | TEMPORAL | category:TEMPORAL | `get_current_time` @0.99 | MATCH |  |
| show my open issues | QUERY | action:list_issues_query | `list_issues` @0.95 | MATCH |  |
| show my open pull requests | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| any stale PRs? | QUERY | action:stale_prs_query | `stale_prs` @0.95 | MATCH |  |
| what needs my attention? | QUERY | action:attention_query | `attention_query` @0.99 | MATCH |  |
| what changed since yesterday? | QUERY | action:changes_query | `changes_query` @0.95 | MATCH |  |
| how productive was I this week? | QUERY | action:productivity_query | `productivity` @0.95 | MATCH |  |
| list my projects | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| close issue 42 | EXECUTION | action:close_issue_query | `close_issue` @0.95 | MATCH |  |
| comment on issue 42: looks good | EXECUTION | action:comment_issue_query | `comment_issue` @0.99 | MATCH |  |
| what have you learned about my workstyle? | MEMORY | action:pull_insights | `pull_insights` @0.99 | MATCH |  |
| set my default repo to acme/widgets | EXECUTION | action:set_default_repo | `set_default_repo` @0.99 | MATCH |  |
| what is my default repo? | QUERY | action:get_default_repo | `get_default_repo` @0.99 | MATCH |  |
| write a short update for the CEO on where we are | SYNTHESIS | action:write_stakeholder_update | `write_stakeholder_update` @0.95 | MATCH |  |
| update the project plan doc with the new dates | EXECUTION | action:update_document_query | `update_document` @0.85 | MATCH |  |
| give me a project status report | EXECUTION | action:generate_report | `get_project_status` @0.95 | MISMATCH |  |
| can we connect my github? | QUERY | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| connect my slack | QUERY | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| link mediajunkie/test-piper-morgan to the project | QUERY | action:manage_repos | `link_repo` @0.72 | MISMATCH |  |
| help me set up github | QUERY | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| show me my archived projects | PORTFOLIO | action:list_archived_projects | `list_archived_projects` @0.99 | MATCH |  |
| list my archived projects | PORTFOLIO | action:list_archived_projects | `list_archived_projects` @0.99 | MATCH |  |
| what projects have I archived? | PORTFOLIO | action:list_archived_projects | `list_archived_projects` @0.95 | MATCH |  |
| show issue #123 | QUERY | action:review_issue_query | `review_issue` @0.99 | MATCH |  |
| show milestones | QUERY | action:list_milestones | `list_milestones` @0.95 | MATCH |  |
| Mark the first three complete and leave the fourth one  | EXECUTION | action:complete_todo | `complete_todo` @0.95 | ARGS_MISMATCH | ARGS exclude: ['4']≠[] |
| Mark the first one complete and leave the second one pe | EXECUTION | action:complete_todo | `complete_todo` @0.95 | MATCH |  |
| I want you to clear 'check the test card again,' and 'r | EXECUTION | action:complete_todo | `complete_todo` @0.95 | MATCH |  |
| mark all my reminders done except for 'revise the pr' | EXECUTION | action:complete_todo | `complete_todo` @0.95 | MATCH |  |
| mark the first two complete | EXECUTION | action:complete_todo | `complete_todo` @0.95 | MATCH |  |
| complete the last one | EXECUTION | action:complete_todo | `complete_todo` @0.95 | MATCH |  |
| mark #2 as done | EXECUTION | action:complete_todo | `complete_todo` @0.95 | MATCH |  |
| mark todo 3 as complete | EXECUTION | action:complete_todo | `complete_todo` @0.99 | MATCH |  |
| mark 1, 2 and 4 done | EXECUTION | action:complete_todo | `complete_todo` @0.99 | MATCH |  |
| complete 'review the pr' | EXECUTION | action:complete_todo | `complete_todo` @0.95 | MATCH |  |
| finish the second one | EXECUTION | action:complete_todo | `CLARIFY` @0.3 | MISMATCH | CLARIFY |
| I'm done with the first and the third | EXECUTION | action:complete_todo | `complete_todo` @0.92 | MATCH |  |
| mark the PR review todo as done | EXECUTION | action:complete_todo | `complete_todo` @0.92 | MATCH |  |
| mark everything done except the last one | EXECUTION | action:complete_todo | `complete_todo` @0.95 | MATCH |  |
| update my project name to Atlas | PORTFOLIO | floor | `CLARIFY` @0.6 | MATCH | CLARIFY |
| edit my project description | PORTFOLIO | floor | `update_document` @0.85 | MISMATCH | OPERATION |
| show me all project plans | QUERY | action:search_documents | `NONE` @0.85 | MISMATCH | NONE |
| do a standup | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| let's do a standup | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| restore CoVa | PORTFOLIO | action:manage_portfolio | `restore_project` @0.95 | MISMATCH |  |
| Please list my archived projects | PORTFOLIO | action:list_archived_projects | `list_archived_projects` @0.99 | MATCH |  |
| what projects do I have? | PORTFOLIO | action:manage_portfolio | `list_projects` @0.95 | MISMATCH |  |
| what are my projects? | PORTFOLIO | action:manage_portfolio | `list_projects` @0.95 | MISMATCH |  |
| remind me at 3pm tomorrow to review the PR | TEMPORAL | action:create_reminder | `create_reminder` @0.99 | MATCH |  |
| remind me at 9:41 today to check in with the lead devel | TEMPORAL | action:create_reminder | `create_reminder` @0.99 | MATCH |  |
| Remind me tomorrow at 3pm to review the PR | TEMPORAL | action:create_reminder | `create_reminder` @0.99 | MATCH |  |
| list my archive projects | PORTFOLIO | action:manage_portfolio | `list_archived_projects` @0.95 | MISMATCH |  |
| Archive my project Test. | PORTFOLIO | action:manage_portfolio | `archive_project` @0.99 | MISMATCH |  |
| Archive my project "Test" | PORTFOLIO | action:manage_portfolio | `archive_project` @0.99 | MISMATCH |  |
| Archive the project called Test | PORTFOLIO | action:manage_portfolio | `archive_project` @0.99 | MISMATCH |  |
| Archive my Test project, please. | PORTFOLIO | action:manage_portfolio | `archive_project` @0.95 | MISMATCH |  |
| Archive my project called "Test" please | PORTFOLIO | action:manage_portfolio | `archive_project` @0.99 | MISMATCH |  |
| archive CoVa | PORTFOLIO | action:manage_portfolio | `archive_project` @0.95 | MISMATCH |  |
| delete my hydrate reminder | TEMPORAL | action:delete_todo | `delete_todo` @0.95 | MATCH |  |
| remind me | TEMPORAL | action:create_reminder | `CLARIFY` @0.95 | MISMATCH | CLARIFY |
| please clear the reminders except for "Review the PR" - | TEMPORAL | plan | `PLAN[delete_todo→get_capabilities]` | MATCH | PLAN[delete_todo→get_capabilities] |
| are you able to set my default repo for me conversation | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| change the status of issue #108 to Done | EXECUTION | action:update_issue | `update_issue` @0.95 | MATCH |  |
| add a reminder: test the safe clarification | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| please remind me: ask Lead how to test "outwardness dis | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| add todo buy oat milk | EXECUTION | action:create_todo | `create_todo` @0.99 | MATCH |  |
| set a reminder for the dentist appointment | TEMPORAL | action:create_reminder | `create_reminder` @0.75 | MATCH |  |
| create a reminder to call the plumber | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| don't let me forget to submit the report | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| I need to remember to submit my timesheet | TEMPORAL | action:create_reminder | `create_todo` @0.95 | MISMATCH |  |
| what are my reminders | TEMPORAL | action:list_reminders_query | `list_reminders_query` @0.99 | MATCH |  |
| show reminders | TEMPORAL | action:list_reminders_query | `list_reminders_query` @0.95 | MATCH |  |
| do I have any reminders | TEMPORAL | action:list_reminders_query | `list_reminders_query` @0.99 | MATCH |  |
| show todos | QUERY | action:list_todos_query | `list_todos_query` @0.99 | MATCH |  |
| list my todos | QUERY | action:list_todos_query | `list_todos_query` @1.0 | MATCH |  |
| what are my todos | QUERY | action:list_todos_query | `list_todos_query` @0.99 | MATCH |  |
| show me completed todos | QUERY | action:list_todos_query | `list_todos_query` @0.92 | MATCH |  |
| show all todos | QUERY | action:list_todos_query | `list_todos_query` @0.95 | MATCH |  |
| next todo | QUERY | action:list_todos_query | `list_todos_query` @0.95 | MATCH |  |
| what should I do next | QUERY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| what do I have next to do | QUERY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| where should I focus this week | GUIDANCE | action:get_top_priority | `get_top_priority` @0.85 | MATCH |  |
| I could use some guidance on this | GUIDANCE | action:get_contextual_guidance | `CLARIFY` @0.5 | MISMATCH | CLARIFY |
| do you have a recommendation | GUIDANCE | action:get_contextual_guidance | `CLARIFY` @0.6 | MISMATCH | CLARIFY |
| what's your advice here | GUIDANCE | action:get_contextual_guidance | `CLARIFY` @0.5 | MISMATCH | CLARIFY |
| ok that's merged, what now? | GUIDANCE | action:get_contextual_guidance | `get_top_priority` @0.85 | MISMATCH |  |
| what are the next steps | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.85 | MATCH |  |
| what should I do about this bug | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.85 | MATCH |  |
| advise me on this decision | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.85 | MATCH |  |
| what's the process for filing a bug | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| can you help me setup the integration | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.92 | MATCH |  |
| can you help me configure the connector | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.85 | MATCH |  |
| I need to setup my projects | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| how do I configure my projects | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| how do I setup the connector | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.85 | MATCH |  |
| how do I configure the connector | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.85 | MATCH |  |
| just getting started here | GUIDANCE | action:greeting | `NONE` @0.95 | MISMATCH | NONE |
| can you help me set up the integration | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| I want to set up my projects | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| how do I set up the connector | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.85 | MATCH |  |
| I'd like to set up my portfolio | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| what's my top priority | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| this is top priority for the team | PRIORITY | action:get_top_priority | `NONE` @0.95 | MATCH | FLOOR-expected: NONE |
| this is the highest priority item | PRIORITY | action:get_top_priority | `NONE` @0.95 | MATCH | FLOOR-expected: NONE |
| mark this as priority one | PRIORITY | action:prioritize | `prioritize` @0.72 | MATCH |  |
| show priorities for this sprint | PRIORITY | floor | `prioritize` @0.85 | MISMATCH | OPERATION |
| list priorities for the team | PRIORITY | floor | `NONE` @0.85 | MATCH | NONE |
| what are my current priorities | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| what are the key priorities this quarter | PRIORITY | action:get_top_priority | `strategic_planning` @0.85 | MISMATCH |  |
| what's most important right now | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| what matters most this week | PRIORITY | action:get_top_priority | `attention_query` @0.85 | MISMATCH |  |
| what are the key tasks for this sprint | PRIORITY | floor | `get_contextual_guidance` @0.72 | MISMATCH | OPERATION |
| what are the key items on my plate | PRIORITY | action:attention_query | `attention_query` @0.92 | MATCH |  |
| should i focus on the bug first | PRIORITY | action:get_top_priority | `get_top_priority` @0.85 | MATCH |  |
| what could I focus on | PRIORITY | action:get_top_priority | `get_top_priority` @0.92 | MATCH |  |
| where should my focus be today | PRIORITY | action:attention_query | `attention_query` @0.92 | MATCH |  |
| what are my focus areas this sprint | PRIORITY | action:get_top_priority | `get_contextual_guidance` @0.72 | MISMATCH |  |
| let's focus on today's priorities | PRIORITY | action:get_top_priority | `attention_query` @0.85 | MISMATCH |  |
| what's my focus this week | PRIORITY | action:get_top_priority | `week_calendar` @0.72 | MISMATCH |  |
| not sure what to focus next | PRIORITY | action:get_top_priority | `get_top_priority` @0.92 | MATCH |  |
| what's urgent right now | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what are my urgent tasks | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what are my urgent items | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what's my urgent work today | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what's the most urgent thing | PRIORITY | action:get_top_priority | `attention_query` @0.95 | MISMATCH |  |
| what needs my focus today | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what requires attention right now | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what's critical right now | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what are my critical tasks | PRIORITY | action:attention_query | `attention_query` @0.92 | MATCH |  |
| what are my critical items | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what's my critical work today | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what's the most critical thing | PRIORITY | action:get_top_priority | `attention_query` @0.92 | MISMATCH |  |
| what should I do first | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| what should I tackle next | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| what's next for me | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| what should I review first | PRIORITY | action:get_top_priority | `get_top_priority` @0.92 | MATCH |  |
| which project should get my focus today | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| which task should get my focus next | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| not sure what to do about this | PRIORITY | action:get_contextual_guidance | `CLARIFY` @0.5 | MISMATCH | CLARIFY |
| what is on my calendar | QUERY | action:meeting_time | `week_calendar` @0.85 | MISMATCH |  |
| show me my calendar today | QUERY | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| calendar today please | QUERY | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| what meetings today | QUERY | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| do i have any meetings | QUERY | action:meeting_time | `meeting_time` @0.85 | MATCH |  |
| do i have meetings | QUERY | action:meeting_time | `meeting_time` @0.85 | MATCH |  |
| what meetings do i have | QUERY | action:meeting_time | `meeting_time` @0.85 | MATCH |  |
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
| how much time do I spend sitting in meetings | QUERY | action:meeting_time | `meeting_time` @0.92 | MATCH |  |
| time spent in meetings is high lately | QUERY | floor | `NONE` @0.95 | MATCH | NONE |
| what's my meeting time today | QUERY | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| let's review my recurring meetings | QUERY | action:recurring_meetings | `recurring_meetings` @0.95 | MATCH |  |
| audit my standing meetings | QUERY | action:recurring_meetings | `recurring_meetings` @0.92 | MATCH |  |
| recurring meetings keep piling up | QUERY | floor | `NONE` @0.85 | MATCH | NONE |
| show me my week | QUERY | action:week_calendar | `week_calendar` @0.95 | MATCH |  |
| what's the week ahead look like | QUERY | action:week_calendar | `week_calendar` @0.99 | MATCH |  |
| show the week calendar | QUERY | action:week_calendar | `week_calendar` @0.95 | MATCH |  |
| check my calendar for conflicts | QUERY | floor | `NONE` @0.85 | MATCH | NONE |
| is my calendar showing any conflict | QUERY | floor | `week_calendar` @0.72 | MISMATCH | OPERATION |
| does my calendar overlap with hers | QUERY | floor | `CLARIFY` @0.3 | MATCH | CLARIFY |
| is there a conflict on my calendar | QUERY | floor | `meeting_time` @0.85 | MISMATCH | OPERATION |
| find time for a 1:1 with sarah | QUERY | floor | `NONE` @0.85 | MATCH | NONE |
| find some time for a sync | QUERY | floor | `NONE` @0.85 | MATCH | NONE |
| schedule a quick call | QUERY | floor | `NONE` @0.95 | MATCH | NONE |
| book a slot with the team | QUERY | floor | `NONE` @0.95 | MATCH | NONE |
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
| pull up my calendar | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| show the team calendar | TEMPORAL | floor | `NONE` @0.85 | MATCH | NONE |
| pull up my schedule | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| show the team schedule | TEMPORAL | floor | `week_calendar` @0.72 | MISMATCH | OPERATION |
| calendar check for today | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| schedule check for today | TEMPORAL | action:meeting_time | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| walk me through my appointments | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| show all appointments | TEMPORAL | action:week_calendar | `week_calendar` @0.72 | MATCH |  |
| walk me through my meetings | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| what are the upcoming meetings | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| when is my team meeting | TEMPORAL | action:meeting_time | `meeting_time` @0.85 | MATCH |  |
| when am i in a meeting | TEMPORAL | action:meeting_time | `meeting_time` @0.85 | MATCH |  |
| meeting check for today | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| meeting check for tomorrow | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| walk me through my events | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| show all events | TEMPORAL | action:week_calendar | `CLARIFY` @0.6 | MISMATCH | CLARIFY |
| what are the upcoming events | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| events check for today | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| events check for tomorrow | TEMPORAL | action:meeting_time | `meeting_time` @0.92 | MATCH |  |
| when's the next event | TEMPORAL | action:meeting_time | `meeting_time` @0.85 | MATCH |  |
| what did I work on today | TEMPORAL | action:session_activity_query | `session_activity_query` @0.95 | MATCH |  |
| what happened in the meeting yesterday | TEMPORAL | floor | `NONE` @0.95 | MATCH | NONE |
| did I finish the report yesterday | TEMPORAL | action:check_completion_status | `check_completion_status` @0.95 | MATCH |  |
| a lot happened yesterday | TEMPORAL | action:changes_query | `changes_query` @0.95 | MATCH |  |
| when was the last time I worked on this | TEMPORAL | floor | `CLARIFY` @0.4 | MATCH | CLARIFY |
| how long have I been working on this | TEMPORAL | floor | `CLARIFY` @0.4 | MATCH | CLARIFY |
| this week's priorities, remind me | TEMPORAL | plan | `PLAN[week_calendar→create_reminder]` | MATCH | PLAN[week_calendar→create_reminder] |
| next week's priorities, remind me | TEMPORAL | plan | `PLAN[get_top_priority→create_reminder]` | MATCH | PLAN[get_top_priority→create_reminder] |
| this month's numbers, remind me | TEMPORAL | plan | `PLAN[generate_report→create_reminder]` | MATCH | PLAN[generate_report→create_reminder] |
| when am i free | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| when's my next free slot | TEMPORAL | floor | `meeting_time` @0.85 | MISMATCH | OPERATION |
| what's my available time | TEMPORAL | floor | `week_calendar` @0.72 | MISMATCH | OPERATION |
| when do I have free time | TEMPORAL | action:week_calendar | `week_calendar` @0.72 | MATCH |  |
| what are my open slots | TEMPORAL | action:week_calendar | `week_calendar` @0.72 | MATCH |  |
| what shipped recently | QUERY | action:shipped_query | `shipped_this_week` @0.92 | MATCH |  |
| can you show what has shipped | QUERY | action:shipped_query | `shipped_this_week` @0.92 | MATCH |  |
| what has shipped this past week | QUERY | action:shipped_query | `shipped_this_week` @0.95 | MATCH |  |
| show our stale pull requests | QUERY | action:stale_prs_query | `stale_prs` @0.95 | MATCH |  |
| any old prs lying around | QUERY | action:stale_prs_query | `stale_prs` @0.95 | MATCH |  |
| prs needing review | QUERY | floor | `list_prs` @0.95 | MISMATCH | OPERATION |
| close the completed issue | EXECUTION | floor | `CLARIFY` @0.4 | MATCH | CLARIFY |
| please close this issue | EXECUTION | action:close_issue_query | `CLARIFY` @0.3 | MISMATCH | CLARIFY |
| re-open issue 88 | EXECUTION | action:reopen_issue_query | `reopen_issue` @0.95 | MATCH |  |
| reopen the old issue | EXECUTION | floor | `CLARIFY` @0.3 | MATCH | CLARIFY |
| re-open the old issue | EXECUTION | floor | `CLARIFY` @0.3 | MATCH | CLARIFY |
| add comment to issue 99 | EXECUTION | action:comment_issue_query | `comment_issue` @0.95 | MATCH |  |
| reply to issue 99 | EXECUTION | action:comment_issue_query | `comment_issue` @0.85 | MATCH |  |
| comment on 99 | EXECUTION | action:comment_issue_query | `comment_issue` @0.95 | MATCH |  |
| review issue 101 | QUERY | action:review_issue_query | `review_issue` @0.99 | MATCH |  |
| issue 101 details | QUERY | action:review_issue_query | `review_issue` @0.95 | MATCH |  |
| get issue 101 | QUERY | action:review_issue_query | `review_issue` @0.95 | MATCH |  |
| what are my issues | QUERY | action:list_issues_query | `list_issues` @0.95 | MATCH |  |
| list the issues please | QUERY | action:list_issues_query | `list_issues` @0.95 | MATCH |  |
| show the issues | QUERY | action:list_issues_query | `list_issues` @0.85 | MATCH |  |
| what's the issue count | QUERY | action:list_issues_query | `list_issues` @0.95 | MATCH |  |
| which issues are assigned to engineering | QUERY | action:list_issues_query | `list_issues` @0.85 | MATCH |  |
| show my pull requests | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| what are my prs looking like | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| where are my pull requests | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| list the prs | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| list all pull requests from this sprint | QUERY | action:list_prs_query | `list_prs` @0.85 | MATCH |  |
| any open prs waiting on me | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| any prs assigned to me | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| any pull requests assigned to me | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| list the milestones for this quarter | QUERY | action:list_milestones_query | `list_milestones` @0.85 | MATCH |  |
| any update on the next milestone | QUERY | action:get_project_status | `analyze_blockers` @0.72 | MISMATCH |  |
| what milestones do we have | QUERY | action:list_milestones_query | `list_milestones` @0.95 | MATCH |  |
| milestones due this month | QUERY | action:list_milestones_query | `list_milestones` @0.92 | MATCH |  |
| when's the milestone deadline | QUERY | floor | `CLARIFY` @0.6 | MATCH | CLARIFY |
| any recent releases | QUERY | action:list_releases_query | `list_releases` @0.95 | MATCH |  |
| show me the releases | QUERY | action:list_releases_query | `list_releases` @0.95 | MATCH |  |
| list our releases | QUERY | action:list_releases_query | `list_releases` @0.95 | MATCH |  |
| what version are we on | QUERY | action:list_releases_query | `list_releases` @0.95 | MATCH |  |
| what's the current release | QUERY | action:list_releases_query | `list_releases` @0.95 | MATCH |  |
| what's our latest release | QUERY | action:list_releases_query | `list_releases` @0.95 | MATCH |  |
| what labels do we use | QUERY | action:list_labels_query | `list_labels` @0.95 | MATCH |  |
| show me the labels | QUERY | action:list_labels_query | `list_labels` @0.95 | MATCH |  |
| list the labels | QUERY | action:list_labels_query | `list_labels` @0.95 | MATCH |  |
| what are the issue labels | QUERY | action:list_labels_query | `list_labels` @0.95 | MATCH |  |
| labels count please | QUERY | action:list_labels_query | `list_labels` @0.85 | MATCH |  |
| all labels please | QUERY | action:list_labels_query | `list_labels` @0.95 | MATCH |  |
| show me the active branches | QUERY | action:list_branches_query | `list_branches` @0.85 | MATCH |  |
| show which branches exist | QUERY | action:list_branches_query | `list_branches` @0.95 | MATCH |  |
| list the branches | QUERY | action:list_branches_query | `list_branches` @0.95 | MATCH |  |
| what feature branches do we have | QUERY | action:list_branches_query | `list_branches` @0.95 | MATCH |  |
| what are the current branches | QUERY | action:list_branches_query | `list_branches` @0.95 | MATCH |  |
| what branches do we have | QUERY | action:list_branches_query | `list_branches` @0.95 | MATCH |  |
| what's my most important task right now | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| what is my most important work today | PRIORITY | action:get_top_priority | `attention_query` @0.92 | MISMATCH |  |
| what should I work on next | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| time for my stand-up | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| give me my stand up | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| give me a standup update | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| give me a standup report | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| what's my daily standup | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| show today's standup | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| show me my portfolio | STATUS | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| list my active projects for this quarter | STATUS | action:manage_portfolio | `list_projects` @0.92 | MISMATCH |  |
| any upcoming milestones for this project | STATUS | action:list_milestones | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| what's my current project | STATUS | action:get_project_status | `NONE` @0.85 | MATCH | FLOOR-expected: NONE |
| can you summarize my current work | STATUS | action:get_project_status | `NONE` @0.85 | MATCH | FLOOR-expected: NONE |
| what are my current projects | STATUS | action:manage_portfolio | `list_projects` @0.95 | MISMATCH |  |
| give me a project overview | STATUS | action:get_project_status | `get_project_status` @0.85 | MATCH |  |
| what's the project landscape | STATUS | action:get_project_status | `list_projects` @0.92 | MISMATCH |  |
| what projects am I working on | STATUS | action:manage_portfolio | `list_projects` @0.95 | MISMATCH |  |
| tell me what I'm working on | STATUS | floor | `session_activity_query` @0.7 | MISMATCH | OPERATION |
| quick check, working on now? | STATUS | action:get_project_status | `session_activity_query` @0.72 | MISMATCH |  |
| what are my active projects | STATUS | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| show my active work | STATUS | floor | `attention_query` @0.85 | MISMATCH | OPERATION |
| what's my status | STATUS | action:get_project_status | `get_project_status` @0.7 | MATCH |  |
| give me a status update | STATUS | action:get_project_status | `get_project_status` @0.85 | MATCH |  |
| what is my status | STATUS | action:get_project_status | `get_project_status` @0.7 | MATCH |  |
| what's my work status | STATUS | action:get_project_status | `get_project_status` @0.85 | MATCH |  |
| show the current status | STATUS | action:get_project_status | `get_project_status` @0.85 | MATCH |  |
| what's the current status | STATUS | action:get_project_status | `CLARIFY` @0.4 | MATCH | FLOOR-expected: CLARIFY |
| I need a status report | STATUS | action:generate_report | `get_project_status` @0.85 | MISMATCH |  |
| what's my progress | STATUS | action:get_project_status | `get_project_status` @0.72 | MATCH |  |
| give me a progress update | STATUS | action:get_project_status | `get_project_status` @0.85 | MATCH |  |
| I need a progress report | STATUS | action:generate_report | `generate_report` @0.85 | MATCH |  |
| what's the progress on this | STATUS | action:get_project_status | `CLARIFY` @0.3 | MATCH | FLOOR-expected: CLARIFY |
| show today's progress | STATUS | action:get_project_status | `session_activity_query` @0.85 | MISMATCH |  |
| what's the current progress | STATUS | action:get_project_status | `get_project_status` @0.72 | MATCH |  |
| how's the progress going | STATUS | action:get_project_status | `get_project_status` @0.85 | MATCH |  |
| what's the progress looking like | STATUS | action:get_project_status | `get_project_status` @0.85 | MATCH |  |
| what are my tasks | STATUS | action:list_todos_query | `list_todos_query` @0.95 | MATCH |  |
| show me my current tasks | STATUS | action:list_todos_query | `list_todos_query` @0.95 | MATCH |  |
| what are my active tasks | STATUS | action:list_todos_query | `list_todos_query` @0.92 | MATCH |  |
| show today's tasks | STATUS | action:list_todos_query | `attention_query` @0.85 | MISMATCH |  |
| list today's tasks | STATUS | action:list_todos_query | `list_todos_query` @0.95 | MATCH |  |
| tasks I'm actively working on | STATUS | action:list_todos_query | `session_activity_query` @0.72 | MISMATCH |  |
| what tasks do I have | STATUS | action:list_todos_query | `list_todos_query` @0.95 | MATCH |  |
| what's the task status | STATUS | action:get_project_status | `get_project_status` @0.85 | MATCH |  |
| what are my assignments | STATUS | floor | `NONE` @0.95 | MATCH | NONE |
| show me my current assignments | STATUS | floor | `NONE` @0.85 | MATCH | NONE |
| what's assigned to me | STATUS | floor | `NONE` @0.95 | MATCH | NONE |
| show today's assignments | STATUS | action:get_project_status | `NONE` @0.85 | MATCH | FLOOR-expected: NONE |
| what are your capabilities? | DISCOVERY | action:get_capabilities | `get_capabilities` @1.0 | MATCH |  |
| what services can you provide? | DISCOVERY | action:get_capabilities | `get_capabilities` @0.99 | MATCH |  |
| what do you offer as an assistant? | DISCOVERY | action:get_capabilities | `get_capabilities` @0.99 | MATCH |  |
| what features does piper have? | DISCOVERY | action:get_capabilities | `get_capabilities` @0.99 | MATCH |  |
| what can you help me do today? | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| show me your capabilities | DISCOVERY | action:get_capabilities | `get_capabilities` @0.99 | MATCH |  |
| give me a menu of services | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| can you list your capabilities | DISCOVERY | action:get_capabilities | `get_capabilities` @0.99 | MATCH |  |
| I want to understand your capabilities better | DISCOVERY | action:get_capabilities | `get_capabilities` @0.99 | MATCH |  |
| pull up the capability menu | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| open the capabilities menu | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| show me the menu | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| what are you able to do for my project | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| show me the features you offer | DISCOVERY | action:get_capabilities | `get_capabilities` @0.99 | MATCH |  |
| what's available in terms of features | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| help | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| open the help menu | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| can you show help topics | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| I need help understanding something | DISCOVERY | action:get_capabilities | `CLARIFY` @0.6 | MISMATCH | CLARIFY |
| what is blocking this release | ANALYSIS | action:analyze_blockers | `analyze_blockers` @0.92 | MATCH |  |
| what tasks are blocking our sprint | ANALYSIS | action:analyze_blockers | `analyze_blockers` @0.95 | MATCH |  |
| blockers for the release | ANALYSIS | action:analyze_blockers | `analyze_blockers` @0.95 | MATCH |  |
| what's the main obstacle here | ANALYSIS | action:analyze_blockers | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| what's in the way of finishing this | ANALYSIS | action:analyze_blockers | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| let's analyze the risk here | ANALYSIS | action:analyze_blockers | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| I'd like a risk assessment for this project | ANALYSIS | action:analyze_blockers | `analyze_blockers` @0.72 | MATCH |  |
| can you run an impact analysis on this change | ANALYSIS | action:analyze_blockers | `NONE` @0.85 | MISMATCH | NONE |
| is there a bottleneck analysis available | DISCOVERY | action:get_capabilities | `get_capabilities` @0.92 | MATCH |  |
| what risks does this project have | ANALYSIS | action:analyze_blockers | `analyze_blockers` @0.85 | MATCH |  |
| what risk do we have in this plan | ANALYSIS | action:analyze_blockers | `analyze_blockers` @0.85 | MATCH |  |
| please identify the risks in this plan | ANALYSIS | action:analyze_blockers | `analyze_blockers` @0.72 | MATCH |  |
| risks we should flag before launch | ANALYSIS | action:analyze_blockers | `analyze_blockers` @0.85 | MATCH |  |
| threats to our timeline this week | ANALYSIS | action:analyze_blockers | `analyze_blockers` @0.92 | MATCH |  |
| what could threaten this deadline | ANALYSIS | action:analyze_blockers | `analyze_blockers` @0.85 | MATCH |  |
| why won't you create issues for me | TRUST | action:explain_trust | `explain_trust` @0.95 | MATCH |  |
| why don't you just do it yourself | TRUST | action:explain_trust | `explain_trust` @0.92 | MATCH |  |
| why are you always cautious about this suggestion | PROVENANCE | action:explain_suggestion | `explain_suggestion` @0.95 | MATCH |  |
| what can't you do here | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| what are your limits as an assistant | DISCOVERY | action:get_capabilities | `get_capabilities` @0.92 | MATCH |  |
| what's the capability boundary here | DISCOVERY | action:get_capabilities | `get_capabilities` @0.92 | MATCH |  |
| how well do you know me by now | MEMORY | action:pull_insights | `pull_insights` @0.92 | MATCH |  |
| do you trust me with this decision | TRUST | action:explain_trust | `explain_trust` @0.95 | MATCH |  |
| how much do you trust my judgment | TRUST | action:explain_trust | `explain_trust` @0.95 | MATCH |  |
| what's our relationship like these days | TRUST | action:explain_trust | `explain_trust` @0.85 | MATCH |  |
| how do you see our relationship evolving | TRUST | action:explain_trust | `explain_trust` @0.85 | MATCH |  |
| how do we work together on this project | TRUST | action:explain_trust | `explain_trust` @0.85 | MATCH |  |
| why did you go ahead without asking | TRUST | action:explain_trust | `explain_trust` @0.95 | MATCH |  |
| why do you always ask me the same thing | TRUST | action:explain_trust | `explain_trust` @0.92 | MATCH |  |
| i didn't ask you to do that | TRUST | action:explain_trust | `explain_trust` @0.85 | MATCH |  |
| what can you remember about our last conversation | MEMORY | action:get_memory | `get_memory` @0.95 | MATCH |  |
| do you remember my last project update | MEMORY | action:get_memory | `get_memory` @0.95 | MATCH |  |
| remember when we shipped the last release? | MEMORY | action:check_completion_status | `check_completion_status` @0.85 | MATCH |  |
| can you show my conversation history | MEMORY | action:get_memory | `get_memory` @0.95 | MATCH |  |
| our history together has been good | MEMORY | action:get_memory | `NONE` @0.95 | MISMATCH | NONE |
| let's look at past conversations we've had | MEMORY | action:get_memory | `get_memory` @0.95 | MATCH |  |
| pull up my previous messages please | MEMORY | action:get_memory | `get_memory` @0.95 | MATCH |  |
| can I see the conversation log | MEMORY | action:get_memory | `get_memory` @0.85 | MATCH |  |
| find when I mentioned this bug before | MEMORY | action:get_memory | `get_memory` @0.85 | MATCH |  |
| search history for that conversation topic | MEMORY | action:get_memory | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| what did we discuss in our last session | MEMORY | action:get_memory | `get_memory` @0.92 | MATCH |  |
| what we discussed yesterday was helpful | MEMORY | action:get_memory | `NONE` @0.95 | MISMATCH | NONE |
| how long is your memory exactly | MEMORY | action:get_memory | `get_memory` @0.92 | MATCH |  |
| link my repository to the project | PORTFOLIO | action:manage_repos | `CLARIFY` @0.3 | MISMATCH | CLARIFY |
| connect my repository to the project | PORTFOLIO | action:manage_repos | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| connect octocat/hello-world to the project | PORTFOLIO | action:manage_repos | `link_repo` @0.85 | MISMATCH |  |
| add octocat/hello-world to the project | PORTFOLIO | action:manage_repos | `link_repo` @0.85 | MISMATCH |  |
| please unlink my repository from this project | PORTFOLIO | action:unlink_repo | `CLARIFY` @0.3 | MISMATCH | CLARIFY |
| please remove my repository from this project | PORTFOLIO | action:unlink_repo | `unlink_repo` @0.75 | MATCH |  |
| please disconnect my repository from this project | PORTFOLIO | action:unlink_repo | `unlink_repo` @0.75 | MATCH |  |
| please show my linked repos | PORTFOLIO | action:manage_repos | `list_repos` @0.95 | MISMATCH |  |
| which repo connected to this project should i check | PORTFOLIO | action:manage_repos | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| can you show project repositories for this account | PORTFOLIO | action:manage_repos | `list_repos` @0.85 | MISMATCH |  |
| list my repos on github | PORTFOLIO | action:list_repos | `list_repos` @0.95 | MATCH |  |
| show all of my repos | PORTFOLIO | action:list_repos | `list_repos` @0.95 | MATCH |  |
| what's changed since last week | QUERY | action:changes_query | `changes_query` @0.95 | MATCH |  |
| show me the changes since last monday | QUERY | action:changes_query | `changes_query` @0.95 | MATCH |  |
| show me everything that's changed | QUERY | action:changes_query | `changes_query` @0.95 | MATCH |  |
| any changes since the last deploy | QUERY | action:changes_query | `changes_query` @0.92 | MATCH |  |
| give me the activity since yesterday's standup | QUERY | action:changes_query | `changes_query` @0.92 | MATCH |  |
| any updates since this morning | QUERY | action:changes_query | `changes_query` @0.95 | MATCH |  |
| what needs attention right now | QUERY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| this project needs my attention today | QUERY | action:attention_query | `attention_query` @0.85 | MATCH |  |
| show me what needs the most attention | QUERY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| the items that need attention haven't been touched | QUERY | action:attention_query | `attention_query` @0.85 | MATCH |  |
| please list the attention items for review | QUERY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| which repository is my default | QUERY | action:get_default_repo | `get_default_repo` @0.95 | MATCH |  |
| please show my default repository | QUERY | action:get_default_repo | `get_default_repo` @0.95 | MATCH |  |
| my default repository | QUERY | action:get_default_repo | `get_default_repo` @0.95 | MATCH |  |
| what do you know about my work habits | MEMORY | action:pull_insights | `pull_insights` @0.95 | MATCH |  |
| tell me what you've learned about my habits | MEMORY | action:pull_insights | `pull_insights` @0.95 | MATCH |  |
| what insights do you have about my productivity | MEMORY | action:pull_insights | `pull_insights` @0.95 | MATCH |  |
| show me what you've learned about my preferences | MEMORY | action:pull_insights | `pull_insights` @0.95 | MATCH |  |
| what patterns have you noticed in my work | MEMORY | action:pull_insights | `pull_insights` @0.95 | MATCH |  |
| what have you noticed about my habits lately | MEMORY | action:pull_insights | `pull_insights` @0.95 | MATCH |  |
| what branch am i on right now | QUERY | action:local_git_status_query | `local_git_status_query` @0.95 | MATCH |  |
| which branch are we on at the moment | QUERY | action:local_git_status_query | `local_git_status_query` @0.95 | MATCH |  |
| can you tell me the current branch | QUERY | action:local_git_status_query | `local_git_status_query` @0.95 | MATCH |  |
| what's the working tree status | QUERY | action:local_git_status_query | `local_git_status_query` @0.95 | MATCH |  |
| are there any uncommitted changes | QUERY | action:local_git_status_query | `local_git_status_query` @0.95 | MATCH |  |
| do we have a dirty working tree | QUERY | action:local_git_status_query | `local_git_status_query` @0.95 | MATCH |  |
| are we ahead of origin right now | QUERY | action:local_git_status_query | `local_git_status_query` @0.85 | MATCH |  |
| are we behind upstream at all | QUERY | action:local_git_status_query | `local_git_status_query` @0.85 | MATCH |  |
| do we have any unpushed commits | QUERY | action:local_git_status_query | `local_git_status_query` @0.95 | MATCH |  |
| can you show the local git status | QUERY | action:local_git_status_query | `local_git_status_query` @0.95 | MATCH |  |
| please run git status for me | QUERY | action:local_git_status_query | `local_git_status_query` @0.95 | MATCH |  |
| show me my productivity report | QUERY | action:productivity_query | `productivity` @0.95 | MATCH |  |
| can you share my productivity metrics | QUERY | action:productivity_query | `productivity` @0.95 | MATCH |  |
| i'd like to check my productivity this week | QUERY | action:productivity_query | `productivity` @0.95 | MATCH |  |
| what have we created so far | QUERY | action:session_activity_query | `session_activity_query` @0.92 | MATCH |  |
| what did we make earlier | QUERY | action:session_activity_query | `session_activity_query` @0.85 | MATCH |  |
| what did i create this session | QUERY | action:session_activity_query | `session_activity_query` @0.99 | MATCH |  |
| what did we do this session | QUERY | action:session_activity_query | `session_activity_query` @0.95 | MATCH |  |
| what issues did we open during the call | QUERY | action:session_activity_query | `session_activity_query` @0.92 | MATCH |  |

## Control (rule of 2026-09-29, step 3): the 9 rows that regressed vs the 10-04 full run, ×6, old vs new `complete_todo` text

Same session, same model (Haiku via the Anthropic provider seam), same minute. "OLD" = the pre-change description
("…never a deletion"), "NEW" = the shipping text with the targets/exclude mini-grammar. Counts over 6 samples.

| phrase | NEW text | OLD text | reading |
|---|---|---|---|
| add octocat/hello-world to the project | link_repo×5, clarify×1 | link_repo×5, clarify×1 | identical — the row expects `manage_repos`; `link_repo` is the 10-05 rail op (expectation stale, not drift) |
| connect octocat/hello-world to the project | link_repo×6 | link_repo×6 | identical — same |
| link mediajunkie/test-piper-morgan to the project | link_repo×6 | link_repo×6 | identical — same |
| link my repository to the project | clarify×6 | clarify×6 | identical — no repo named; the ask is honest; expectation (`manage_repos`) stale |
| please unlink my repository from this project | clarify×6 | clarify×6 | identical — no repo named; expectation (`unlink_repo`) stale |
| show today's tasks | list_todos_query×3, attention_query×3 | attention_query×4, list_todos_query×2 | split under BOTH texts — ambiguous row, not drift |
| what are my projects? | list_projects×6 | manage_portfolio×6 | **differs by text** — the new text moves it to the specific list op; the row expects the umbrella `manage_portfolio` (in PPM's re-judge set) |
| what are the key tasks for this sprint | get_contextual_guidance×6 | get_contextual_guidance×6 | identical — expectation `floor` predates get_contextual_guidance's rail entry (read_canonical, 10-05) |
| what's my available time | week_calendar×5, clarify×1 | week_calendar×6 | identical — expectation `floor` predates the calendar rail ops |

**Attribution:** 8 of 9 route the same under either description — those verdict changes are the 10-05 grammar growth
(link_repo / unlink_repo / read_canonical / calendar ops entering the catalog) meeting row expectations written before those
ops existed, plus one genuinely ambiguous row. They are **not** caused by this change. The 1 of 9 that differs moves
*toward* the specific op the catalog now offers. Row re-judgements go to PPM/CXO (the 2026-09-29 rule: attribute, then fix at the
cause — here the cause is the expectation, not the router).

## Control 2: the rows behind the gate pins this report would flip, ×6, old vs new text

| phrase | NEW text | OLD text | reading |
|---|---|---|---|
| is my calendar showing any conflict | week_calendar×6 | week_calendar×6 | identical — the CALENDAR_QUERY ledger row expects `floor` (10-01 ruling); the router now consistently offers the week view. Re-judge: is `week_calendar` an acceptable served answer for a conflict question? |
| what am I working on? | session_activity_query×6 | session_activity_query×6 | identical — expects `floor` (CXO 10-01 ownership ruling); router picks the session-recall op under both texts |
| edit my project description | update_document×6 | update_document×6 | identical — the #1933 protective-literal case, unchanged |
| update my project name to Atlas | clarify×5, update_document×1 | clarify×6 | identical within noise — now a floor MATCH (CLARIFY) under both; the 10-04 pin assumed `update_document_query` |
| what projects do I have? | list_projects×6 | manage_portfolio×3, list_projects×3 | **differs by text, toward the specific op** — in PPM's manage_portfolio re-judge set |

**Status of this report:** published as the measurement of record for the args change (EXECUTION 26/30, args 12/13 → 13/13
after the one row's exclude was relaxed), **not yet wired into `PHASE3_REPORTS`**. Wiring it flips five gate pins whose
rows are listed above; both controls attribute every flip to the 10-05 catalog growth meeting stale expectations, not to
this change. It is wired in the same commit that re-judges those rows (PPM/CXO) and updates the pins.

Control 3 — the STATUS census row that became `row_ok` under this report: `what's the project landscape` → list_projects×6 under
BOTH texts (identical; not this change). Issue #1951 carries the full re-judge list.
