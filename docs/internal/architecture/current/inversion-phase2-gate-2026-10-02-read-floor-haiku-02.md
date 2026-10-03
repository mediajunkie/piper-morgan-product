# Inversion Phase-2.1 gate — SNAPSHOT-AWARE router vs context-free, per category
Run: 2026-10-03 02:22Z · corpora: inversion_corpus_phase0.yaml (447 rows, untouched) + inversion_corpus_phase2_armed.yaml (14 rows: 7 armed + 7 control twins) · scripts/inversion_phase2_gate.py

LAYER (m-43): **router only, against corpus fixtures** — one constrained Haiku-class call per (row, condition) (468 LLM calls incl. repair retries across 468 routed (row, condition) pairs; 0 ERROR, 0 REFUSED), grammar derived from the live registry at run time (64 canonical operations, 83 input-side aliases collapsed, + NONE/CLARIFY). NOT live traffic, NOT the production chain, NOT handler behavior: a MATCH here means the router would have picked the right destination, not that the destination's handler succeeds (the #1651 extraction failure lived one layer below routing). Armed-state session context is FIXTURE-built via the real `SessionSnapshot` dataclass and `serialize_for_prompt` — the exact shadow-path serialization, but the field VALUES are corpus assertions, not live store reads.

## Part 1 — phase0 corpus rerun, context-free (denominators stated — m-44)

Method identical to Phase 1b (inversion-phase1-shadow-score-2026-08-14b.md: 33/39). Baseline column is Phase-0's FULL-CHAIN production decision (inversion-phase0-baseline-full-2026-08-12.md: 36/39).

| category | rows | asserted | router match | baseline match | Δ | REVIEW | gate |
|---|---|---|---|---|---|---|---|
| QUERY | 129 | 114 | 108 | 12/13 | +96 | 15 | no regression |
| TEMPORAL | 69 | 66 | 60 | 4/4 | +56 | 3 | no regression |
| STATUS | 54 | 50 | 44 | 1/4 | +43 | 4 | no regression |
| PRIORITY | 44 | 43 | 32 | 2/2 | +30 | 1 | no regression |
| GUIDANCE | 26 | 21 | 15 | 1/1 | +14 | 5 | no regression |
| EXECUTION | 26 | 16 | 14 | 5/6 | +9 | 10 | no regression |
| DISCOVERY | 25 | 24 | 22 | 0/0 | +22 | 1 | no regression |
| PORTFOLIO | 17 | 15 | 14 | 6/7 | +8 | 2 | no regression |
| MEMORY | 17 | 15 | 9 | 1/1 | +8 | 2 | no regression |
| ANALYSIS | 15 | 14 | 10 | 0/0 | +10 | 1 | no regression |
| TRUST | 11 | 10 | 10 | 0/0 | +10 | 1 | no regression |
| CONVERSATION | 5 | 0 | 0 | 0/0 | — | 5 | **UNGATEABLE** (REVIEW-only denominator) |
| SYNTHESIS | 4 | 2 | 2 | 2/2 | +0 | 2 | no regression |
| IDENTITY | 3 | 2 | 2 | 2/2 | +0 | 1 | no regression |
| PROVENANCE | 2 | 1 | 0 | 0/0 | +0 | 1 | no regression |
| **TOTAL** | 447 | 393 | 342 | 36/39 | +306 | 54 | (aggregate is NOT the gate) |

Gate reading (Arch condition 1 as amended 08-09 08:3x, PPM): **no category may regress; the aggregate is never the gate**. REVIEW-only-denominator categories remain ungateable, same as Phase 0/1 stated.

## Part 2 — ARMED-STATE rows: with-snapshot vs without (the gate question)

**Armed-state delta: 5/7 with-snapshot vs 1/7 without-snapshot** (asserted armed rows; the same expectation scored under both conditions). Does context flip the loss class: **YES** — the snapshot flips rows the context-free router loses.

Each armed row: fixture → real `SessionSnapshot` → `serialize_for_prompt` → `RouterSnapshot(state_block=…)`. Control twins (same text, no fixture) run once: an empty snapshot's with/without prompts are byte-identical by construction, so a second call would measure only stochasticity.

| pair | phrase | armed expected | WITH snapshot | WITHOUT snapshot | control (stateless) |
|---|---|---|---|---|---|
| verb-question | delete | flow:delete_todo | `delete_todo` @0.6 → MATCH | `CLARIFY` @0.3 → MISS(CLARIFY) | REVIEW: `CLARIFY` @0.3 → REVIEW |
| confirm-aside | please note that I'll need to figure out lat | route:NONE | `NONE` @0.95 → MATCH | `explain_trust` @0.92 → MISS(explain_trust) | route:NONE: `explain_trust` @0.92 → MISS(explain_trust) |
| draft-file-command | file as is thanks | flow:create_issue | `create_issue` @0.95 → MATCH | `NONE` @0.95 → MISS(NONE) | REVIEW: `NONE` @0.95 → REVIEW |
| draft-body-prose | The problem: deleting a project (a destructi | flow:create_issue | `update_document` @0.95 → MISS(update_document) | `NONE` @0.95 → MISS(NONE) | REVIEW: `NONE` @0.95 → REVIEW |
| reminder-time-answer | at 3pm | flow:create_reminder | `create_reminder` @0.95 → MATCH | `CLARIFY` @0.95 → MISS(CLARIFY) | REVIEW: `CLARIFY` @0.95 → REVIEW |
| standup-todo-offer | Yes mark the overdue todo done. | flow:complete_todo | `complete_todo` @0.95 → MATCH | `complete_todo` @0.85 → MATCH | action:complete_todo: `complete_todo` @0.85 → MATCH |
| repo-question-answer | in the test-Piper-Morgan repository | flow:create_issue | `set_default_repo` @0.92 → MISS(set_default_repo) | `CLARIFY` @0.5 → MISS(CLARIFY) | REVIEW: `CLARIFY` @0.5 → REVIEW |

### Armed-family raw router output (verbatim rationales)

| pair | condition | route @conf | rationale | error |
|---|---|---|---|---|
| verb-question | with-snapshot | `delete_todo` @0.6 | User answers open question about reminder clearing; ambiguous between delete and mark-done intent. |  |
| verb-question | without-snapshot | `CLARIFY` @0.3 | Delete what? Clarify target: todo, reminder, issue, project, document, or something else? |  |
| verb-question | control | `CLARIFY` @0.3 | Delete what? Clarify target: todo, reminder, issue, project, document, or something else. |  |
| confirm-aside | with-snapshot | `NONE` @0.95 | User is making a meta-comment about assistant behavior, not answering the confirmation or requesting an operation. |  |
| confirm-aside | without-snapshot | `explain_trust` @0.92 | User questioning why assistant made a destructive assumption; trust/conduct issue |  |
| confirm-aside | control | `explain_trust` @0.92 | User questioning why assistant made a destructive assumption; trust/conduct issue |  |
| draft-file-command | with-snapshot | `create_issue` @0.95 | User confirms draft issue ready; 'file as is' answers open question to proceed with creation. |  |
| draft-file-command | without-snapshot | `NONE` @0.95 | Conversational acknowledgment; no operation requested or implied. |  |
| draft-file-command | control | `NONE` @0.95 | Conversational acknowledgment; no operation requested or implied. |  |
| draft-body-prose | with-snapshot | `update_document` @0.95 | User answered the open question with specific body content for the drafted issue. |  |
| draft-body-prose | without-snapshot | `NONE` @0.95 | User is describing a product issue or feature request, not asking Piper to perform an operation. |  |
| draft-body-prose | control | `NONE` @0.95 | User is describing a product issue or feature request, not asking Piper to perform an operation. |  |
| reminder-time-answer | with-snapshot | `create_reminder` @0.95 | User answers open reminder-time question with specific time. |  |
| reminder-time-answer | without-snapshot | `CLARIFY` @0.95 | Fragment lacks context; could be reminder, meeting, or other time-based action |  |
| reminder-time-answer | control | `CLARIFY` @0.95 | Fragment lacks context; could be reminder, meeting, or other time-based action |  |
| standup-todo-offer | with-snapshot | `complete_todo` @0.95 | User explicitly confirms marking the overdue todo done; answers open question. |  |
| standup-todo-offer | without-snapshot | `complete_todo` @0.85 | User confirms marking the overdue todo as done from prior context. |  |
| standup-todo-offer | control | `complete_todo` @0.85 | User confirms marking the overdue todo as done |  |
| repo-question-answer | with-snapshot | `set_default_repo` @0.92 | User answers open repo question; routes to flow handler, not fresh operation |  |
| repo-question-answer | without-snapshot | `CLARIFY` @0.5 | Fragment names a repo but lacks a verb or intent; unclear what action is requested |  |
| repo-question-answer | control | `CLARIFY` @0.5 | Fragment names a repo but lacks a verb or intent—set default, list issues, query status, or something else? |  |

## Part 3 — phase0 REVIEW rows (informational, unscored)

| phrase | category | router route @conf | rationale |
|---|---|---|---|
| can you clarify what you meant? | QUERY | `CLARIFY` @0.95 | User asks for clarification of a prior statement, but no pri |
| what have you learned about my work style? | MEMORY | `pull_insights` @0.95 | User explicitly asks what-have-you-learned question about wo |
| connect my github | GUIDANCE | `get_contextual_guidance` @0.95 | Request to set up or connect GitHub integration — onboarding |
| connect my notion | GUIDANCE | `get_contextual_guidance` @0.95 | User requests setup/configuration of Notion integration; mat |
| link my google calendar | GUIDANCE | `get_contextual_guidance` @0.95 | User requests setup/configuration of a calendar integration; |
| add a repo to my portfolio | PORTFOLIO | `manage_repos` @0.95 | User explicitly asks to add a repo to their portfolio. |
| show me my todos | QUERY | `list_todos_query` @0.99 | User explicitly requests to see their todo list |
| connect my calendar | GUIDANCE | `get_contextual_guidance` @0.95 | Request to set up or configure calendar integration — onboar |
| what reminders do I have? | TEMPORAL | `list_reminders_query` @0.99 | User asks for their reminders list |
| hello | CONVERSATION | `greeting` @0.99 | User sent a simple greeting |
| goodbye | CONVERSATION | `farewell` @1.0 | User said goodbye; farewell operation applies. |
| thank you! | CONVERSATION | `thanks` @0.99 | Message is only an expression of gratitude. |
| what can you do? | DISCOVERY | `get_capabilities` @0.99 | User explicitly asks what the assistant can do |
| why did you suggest that? | PROVENANCE | `explain_suggestion` @0.95 | User asking for provenance of a prior suggestion |
| why can't you create issues? | TRUST | `explain_trust` @0.95 | User asks why the assistant can't do something—a trust/condu |
| what do you remember about me? | MEMORY | `get_memory` @0.95 | Direct question about what the assistant remembers about the |
| what's my default repo? | QUERY | `get_default_repo` @1.0 | Direct query for default repository setting |
| set my default repo to mediajunkie/piper-morgan-product | EXECUTION | `set_default_repo` @0.99 | User explicitly requests setting default repo to a specific  |
| write a short update for the CEO on the beta | SYNTHESIS | `write_stakeholder_update` @0.95 | User explicitly asks to draft an update for a named audience |
| update the roadmap doc with the new dates | EXECUTION | `update_document` @0.85 | User asks to update a document with specific content (new da |
| tell me more about the github integration | QUERY | `get_feature_info` @0.99 | User explicitly asks for details about a specific Piper feat |
| who are you? | IDENTITY | `get_identity` @0.99 | Direct who-are-you question about the assistant's role and i |
| show my recurring meetings | QUERY | `recurring_meetings` @0.99 | User explicitly asks to show recurring meetings |
| what's my week look like? | QUERY | `week_calendar` @0.99 | User asking for calendar overview of the week ahead |
| what's the next milestone? | STATUS | `list_milestones` @0.92 | User asking for the next milestone; list_milestones retrieve |
| what branch are we on? | QUERY | `local_git_status_query` @0.95 | Direct question about current git branch status |
| what did we ship this week? | QUERY | `shipped_this_week` @0.95 | Direct query about shipped releases this week |
| show stale prs | QUERY | `stale_prs` @0.95 | User explicitly requests stale PRs listing |
| close issue #123 | EXECUTION | `close_issue` @0.99 | User explicitly requests closing a specific issue by number. |
| reopen issue #123 | EXECUTION | `reopen_issue` @0.99 | User explicitly requests reopening a specific issue by numbe |
| comment on issue #123 | EXECUTION | `comment_issue` @0.95 | User explicitly asks to comment on a specific issue number. |
| how many open issues do we have? | QUERY | `list_issues` @0.95 | User asks for a count of open issues in their default repo. |
| show my prs | QUERY | `list_prs` @0.95 | User asks to show their pull requests |
| what did we create this session? | QUERY | `session_activity_query` @0.95 | User asking what was created in current session |
| what's my productivity? | QUERY | `productivity` @0.95 | Direct productivity query asking for productivity metrics or |
| remind me to review the roadmap tomorrow | EXECUTION | `create_reminder` @0.95 | User explicitly requests a reminder for a specific task and  |
| complete todo 3 | EXECUTION | `complete_todo` @0.95 | User explicitly requests marking todo 3 as done |
| show all my todos | QUERY | `list_todos_query` @0.99 | User explicitly requests to see all their todos |
| what's my next todo? | QUERY | `list_todos_query` @0.95 | User asking for their next todo item to work on |
| when did I complete the onboarding project? | STATUS | `check_completion_status` @0.95 | User asks when past work (onboarding project) was completed. |
| how do I get started? | GUIDANCE | `get_contextual_guidance` @0.95 | Getting-started question; user seeks onboarding or initial s |
| what's blocking the milestone? | ANALYSIS | `analyze_blockers` @0.95 | User asks what is blocking the milestone—a direct blocker an |
| what are my priorities? | PRIORITY | `get_top_priority` @0.95 | User asking what to prioritize or work on first |
| Yes please | CONVERSATION | `CLARIFY` @0.0 | No prior context; 'Yes please' is ambiguous without a preced |
| end standup | CONVERSATION | `NONE` @0.85 | Conversational command to end a standup session; no catalog  |
| i am not doing the standup right now. restore CoVa | PORTFOLIO | `manage_portfolio` @0.95 | User declines standup and requests project restore; restore  |
| delete my reminders | TEMPORAL | `delete_todo` @0.85 | User requests deletion of all reminders; delete_todo handles |
| hi piper, connect my github | EXECUTION | `get_contextual_guidance` @0.95 | User requests to set up/connect GitHub integration — onboard |
| what time is it? also connect my github | TEMPORAL | `PLAN[get_current_time→get_contextual_guidance]` |  |
| use the interview from now on | STATUS | `CLARIFY` @0.3 | Ambiguous: unclear what 'the interview' refers to or what ac |
| use the standup interview format by default from now on | STATUS | `NONE` @0.85 | User preference/configuration request; no catalog operation  |
| please mark issue #108 in the mediajunkie/test-piper-mo | EXECUTION | `close_issue` @0.95 | User asks to mark issue complete, which maps to closing it. |
| please mark 1, 2, 4, and 5 done | EXECUTION | `complete_todo` @0.95 | User explicitly requests marking multiple todos as done |
| Create a doc from this conversation | SYNTHESIS | `CLARIFY` @0.4 | Ambiguous: generate_content (draft text), update_document (f |

## Row detail — phase0 asserted rows

| phrase | category | expected | router route @conf | verdict | note |
|---|---|---|---|---|---|
| give me my standup | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| what's on my calendar today? | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| when is my next meeting? | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| what am I working on? | STATUS | floor | `attention_query` @0.7 | MISMATCH | OPERATION |
| what should I focus on today? | PRIORITY | action:attention_query | `attention_query` @0.92 | MATCH |  |
| what are my top priorities? | PRIORITY | category:PRIORITY | `get_top_priority` @0.95 | MATCH |  |
| who am I? | IDENTITY | action:get_identity | `get_identity` @0.95 | MATCH |  |
| what's my role? | IDENTITY | category:IDENTITY | `get_identity` @0.95 | MATCH |  |
| how do I create a ticket? | GUIDANCE | category:GUIDANCE | `get_contextual_guidance` @0.95 | MATCH |  |
| create a ticket for the login bug | EXECUTION | action:create_issue | `create_issue` @0.92 | MATCH |  |
| analyze the file I uploaded | QUERY | action:analyze_data | `analyze_document` @0.95 | MISMATCH |  |
| summarize the document | SYNTHESIS | action:summarize_document | `summarize_document` @0.95 | MATCH |  |
| what time is it? | TEMPORAL | category:TEMPORAL | `get_current_time` @1.0 | MATCH |  |
| show my open issues | QUERY | action:list_issues_query | `list_issues` @0.99 | MATCH |  |
| show my open pull requests | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| any stale PRs? | QUERY | action:stale_prs_query | `stale_prs` @0.95 | MATCH |  |
| what needs my attention? | QUERY | action:attention_query | `attention_query` @0.99 | MATCH |  |
| what changed since yesterday? | QUERY | action:changes_query | `changes_query` @1.0 | MATCH |  |
| how productive was I this week? | QUERY | action:productivity_query | `productivity` @0.95 | MATCH |  |
| list my projects | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.99 | MATCH |  |
| close issue 42 | EXECUTION | action:close_issue_query | `close_issue` @0.95 | MATCH |  |
| comment on issue 42: looks good | EXECUTION | action:comment_issue_query | `comment_issue` @0.99 | MATCH |  |
| what have you learned about my workstyle? | MEMORY | action:pull_insights | `pull_insights` @0.95 | MATCH |  |
| set my default repo to acme/widgets | EXECUTION | action:set_default_repo | `set_default_repo` @0.99 | MATCH |  |
| what is my default repo? | QUERY | action:get_default_repo | `get_default_repo` @0.99 | MATCH |  |
| write a short update for the CEO on where we are | SYNTHESIS | action:write_stakeholder_update | `write_stakeholder_update` @0.95 | MATCH |  |
| update the project plan doc with the new dates | EXECUTION | action:update_document_query | `update_document` @0.72 | MATCH |  |
| give me a project status report | EXECUTION | action:generate_report | `get_project_status` @0.95 | MISMATCH |  |
| can we connect my github? | QUERY | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| connect my slack | QUERY | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| link mediajunkie/test-piper-morgan to the project | QUERY | action:manage_repos | `manage_repos` @0.95 | MATCH |  |
| help me set up github | QUERY | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| show me my archived projects | PORTFOLIO | action:list_archived_projects | `list_archived_projects` @0.99 | MATCH |  |
| list my archived projects | PORTFOLIO | action:list_archived_projects | `list_archived_projects` @0.99 | MATCH |  |
| what projects have I archived? | PORTFOLIO | action:list_archived_projects | `list_archived_projects` @0.99 | MATCH |  |
| show issue #123 | QUERY | action:review_issue_query | `review_issue` @0.99 | MATCH |  |
| show milestones | QUERY | action:list_milestones | `list_milestones` @0.95 | MATCH |  |
| show me all project plans | QUERY | action:search_documents | `NONE` @0.85 | MISMATCH | NONE |
| do a standup | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| let's do a standup | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| restore CoVa | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| Please list my archived projects | PORTFOLIO | action:list_archived_projects | `list_archived_projects` @0.99 | MATCH |  |
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
| please clear the reminders except for "Review the PR" - | TEMPORAL | plan | `PLAN[delete_todo→get_capabilities]` | MATCH | PLAN[delete_todo→get_capabilities] |
| are you able to set my default repo for me conversation | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| change the status of issue #108 to Done | EXECUTION | action:update_issue | `update_issue` @0.95 | MATCH |  |
| add a reminder: test the safe clarification | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| please remind me: ask Lead how to test "outwardness dis | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| add todo buy oat milk | EXECUTION | action:create_todo | `create_todo` @0.99 | MATCH |  |
| set a reminder for the dentist appointment | TEMPORAL | action:create_reminder | `create_reminder` @0.75 | MATCH |  |
| create a reminder to call the plumber | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| don't let me forget to submit the report | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| I need to remember to submit my timesheet | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| what are my reminders | TEMPORAL | action:list_reminders_query | `list_reminders_query` @0.99 | MATCH |  |
| show reminders | TEMPORAL | action:list_reminders_query | `list_reminders_query` @0.95 | MATCH |  |
| do I have any reminders | TEMPORAL | action:list_reminders_query | `list_reminders_query` @0.99 | MATCH |  |
| show todos | QUERY | action:list_todos_query | `list_todos_query` @0.99 | MATCH |  |
| list my todos | QUERY | action:list_todos_query | `list_todos_query` @0.99 | MATCH |  |
| what are my todos | QUERY | action:list_todos_query | `list_todos_query` @0.99 | MATCH |  |
| show me completed todos | QUERY | action:list_todos_query | `list_todos_query` @0.95 | MATCH |  |
| show all todos | QUERY | action:list_todos_query | `list_todos_query` @0.95 | MATCH |  |
| next todo | QUERY | action:list_todos_query | `list_todos_query` @0.95 | MATCH |  |
| what should I do next | QUERY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| what do I have next to do | QUERY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| where should I focus this week | GUIDANCE | action:get_top_priority | `get_top_priority` @0.85 | MATCH |  |
| I could use some guidance on this | GUIDANCE | action:get_contextual_guidance | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| do you have a recommendation | GUIDANCE | action:get_contextual_guidance | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| what's your advice here | GUIDANCE | action:get_contextual_guidance | `CLARIFY` @0.3 | MISMATCH | CLARIFY |
| ok that's merged, what now? | GUIDANCE | action:get_contextual_guidance | `get_top_priority` @0.72 | MISMATCH |  |
| what are the next steps | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.85 | MATCH |  |
| what should I do about this bug | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.85 | MATCH |  |
| advise me on this decision | GUIDANCE | action:get_contextual_guidance | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| what's the process for filing a bug | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| can you help me setup the integration | GUIDANCE | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
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
| mark this as priority one | PRIORITY | action:prioritize | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| show priorities for this sprint | PRIORITY | floor | `prioritize` @0.85 | MISMATCH | OPERATION |
| list priorities for the team | PRIORITY | floor | `NONE` @0.85 | MATCH | NONE |
| what are my current priorities | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| what are the key priorities this quarter | PRIORITY | action:get_top_priority | `get_top_priority` @0.72 | MATCH |  |
| what's most important right now | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| what matters most this week | PRIORITY | action:get_top_priority | `attention_query` @0.85 | MISMATCH |  |
| what are the key tasks for this sprint | PRIORITY | floor | `list_todos_query` @0.72 | MISMATCH | OPERATION |
| what are the key items on my plate | PRIORITY | action:attention_query | `attention_query` @0.92 | MATCH |  |
| should i focus on the bug first | PRIORITY | action:get_top_priority | `get_top_priority` @0.85 | MATCH |  |
| what could I focus on | PRIORITY | action:get_top_priority | `get_top_priority` @0.85 | MATCH |  |
| where should my focus be today | PRIORITY | action:attention_query | `attention_query` @0.92 | MATCH |  |
| what are my focus areas this sprint | PRIORITY | action:get_top_priority | `get_contextual_guidance` @0.72 | MISMATCH |  |
| let's focus on today's priorities | PRIORITY | action:get_top_priority | `attention_query` @0.85 | MISMATCH |  |
| what's my focus this week | PRIORITY | action:get_top_priority | `week_calendar` @0.65 | MISMATCH |  |
| not sure what to focus next | PRIORITY | action:get_top_priority | `get_top_priority` @0.85 | MATCH |  |
| what's urgent right now | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what are my urgent tasks | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what are my urgent items | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what's my urgent work today | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what's the most urgent thing | PRIORITY | action:get_top_priority | `attention_query` @0.95 | MISMATCH |  |
| what needs my focus today | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what requires attention right now | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what's critical right now | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what are my critical tasks | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what are my critical items | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what's my critical work today | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what's the most critical thing | PRIORITY | action:get_top_priority | `attention_query` @0.92 | MISMATCH |  |
| what should I do first | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| what should I tackle next | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| what's next for me | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| what should I review first | PRIORITY | action:get_top_priority | `get_top_priority` @0.85 | MATCH |  |
| which project should get my focus today | PRIORITY | action:get_top_priority | `get_top_priority` @0.92 | MATCH |  |
| which task should get my focus next | PRIORITY | action:get_top_priority | `get_top_priority` @0.95 | MATCH |  |
| not sure what to do about this | PRIORITY | action:get_contextual_guidance | `CLARIFY` @0.6 | MISMATCH | CLARIFY |
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
| audit my standing meetings | QUERY | action:recurring_meetings | `recurring_meetings` @0.85 | MATCH |  |
| recurring meetings keep piling up | QUERY | floor | `NONE` @0.85 | MATCH | NONE |
| show me my week | QUERY | action:week_calendar | `week_calendar` @0.95 | MATCH |  |
| what's the week ahead look like | QUERY | action:week_calendar | `week_calendar` @0.95 | MATCH |  |
| show the week calendar | QUERY | action:week_calendar | `week_calendar` @0.95 | MATCH |  |
| check my calendar for conflicts | QUERY | floor | `NONE` @0.85 | MATCH | NONE |
| is my calendar showing any conflict | QUERY | floor | `CLARIFY` @0.6 | MATCH | CLARIFY |
| does my calendar overlap with hers | QUERY | floor | `CLARIFY` @0.3 | MATCH | CLARIFY |
| is there a conflict on my calendar | QUERY | floor | `meeting_time` @0.75 | MISMATCH | OPERATION |
| find time for a 1:1 with sarah | QUERY | floor | `NONE` @0.95 | MATCH | NONE |
| find some time for a sync | QUERY | floor | `CLARIFY` @0.4 | MATCH | CLARIFY |
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
| remind me today's day | TEMPORAL | action:get_current_time | `get_current_time` @0.92 | MATCH |  |
| pull up my calendar | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| show the team calendar | TEMPORAL | floor | `NONE` @0.95 | MATCH | NONE |
| pull up my schedule | TEMPORAL | action:week_calendar | `week_calendar` @0.75 | MATCH |  |
| show the team schedule | TEMPORAL | floor | `CLARIFY` @0.4 | MATCH | CLARIFY |
| calendar check for today | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| schedule check for today | TEMPORAL | action:meeting_time | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| walk me through my appointments | TEMPORAL | action:week_calendar | `week_calendar` @0.75 | MATCH |  |
| show all appointments | TEMPORAL | action:week_calendar | `week_calendar` @0.72 | MATCH |  |
| walk me through my meetings | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| what are the upcoming meetings | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| when is my team meeting | TEMPORAL | action:meeting_time | `meeting_time` @0.85 | MATCH |  |
| when am i in a meeting | TEMPORAL | action:meeting_time | `meeting_time` @0.85 | MATCH |  |
| meeting check for today | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| meeting check for tomorrow | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| walk me through my events | TEMPORAL | action:week_calendar | `CLARIFY` @0.6 | MISMATCH | CLARIFY |
| show all events | TEMPORAL | action:week_calendar | `CLARIFY` @0.6 | MISMATCH | CLARIFY |
| what are the upcoming events | TEMPORAL | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| events check for today | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| events check for tomorrow | TEMPORAL | action:meeting_time | `meeting_time` @0.92 | MATCH |  |
| when's the next event | TEMPORAL | action:meeting_time | `meeting_time` @0.85 | MATCH |  |
| what did I work on today | TEMPORAL | action:session_activity_query | `session_activity_query` @0.95 | MATCH |  |
| what happened in the meeting yesterday | TEMPORAL | floor | `NONE` @0.95 | MATCH | NONE |
| did I finish the report yesterday | TEMPORAL | action:check_completion_status | `check_completion_status` @0.92 | MATCH |  |
| a lot happened yesterday | TEMPORAL | action:changes_query | `changes_query` @0.95 | MATCH |  |
| when was the last time I worked on this | TEMPORAL | floor | `CLARIFY` @0.4 | MATCH | CLARIFY |
| how long have I been working on this | TEMPORAL | floor | `CLARIFY` @0.4 | MATCH | CLARIFY |
| this week's priorities, remind me | TEMPORAL | plan | `PLAN[get_top_priority→create_reminder]` | MATCH | PLAN[get_top_priority→create_reminder] |
| next week's priorities, remind me | TEMPORAL | plan | `PLAN[get_top_priority→create_reminder]` | MATCH | PLAN[get_top_priority→create_reminder] |
| this month's numbers, remind me | TEMPORAL | plan | `PLAN[analyze_data→create_reminder]` | MATCH | PLAN[analyze_data→create_reminder] |
| when am i free | TEMPORAL | action:week_calendar | `week_calendar` @0.72 | MATCH |  |
| when's my next free slot | TEMPORAL | floor | `meeting_time` @0.85 | MISMATCH | OPERATION |
| what's my available time | TEMPORAL | floor | `CLARIFY` @0.6 | MATCH | CLARIFY |
| when do I have free time | TEMPORAL | action:week_calendar | `CLARIFY` @0.6 | MISMATCH | CLARIFY |
| what are my open slots | TEMPORAL | action:week_calendar | `week_calendar` @0.72 | MATCH |  |
| what shipped recently | QUERY | action:shipped_query | `shipped_this_week` @0.95 | MATCH |  |
| can you show what has shipped | QUERY | action:shipped_query | `shipped_this_week` @0.92 | MATCH |  |
| what has shipped this past week | QUERY | action:shipped_query | `shipped_this_week` @0.95 | MATCH |  |
| show our stale pull requests | QUERY | action:stale_prs_query | `stale_prs` @0.95 | MATCH |  |
| any old prs lying around | QUERY | action:stale_prs_query | `stale_prs` @0.95 | MATCH |  |
| prs needing review | QUERY | floor | `list_prs` @0.95 | MISMATCH | OPERATION |
| close the completed issue | EXECUTION | floor | `CLARIFY` @0.4 | MATCH | CLARIFY |
| please close this issue | EXECUTION | action:close_issue_query | `CLARIFY` @0.3 | MISMATCH | CLARIFY |
| re-open issue 88 | EXECUTION | action:reopen_issue_query | `reopen_issue` @0.95 | MATCH |  |
| reopen the old issue | EXECUTION | floor | `CLARIFY` @0.3 | MATCH | CLARIFY |
| re-open the old issue | EXECUTION | floor | `CLARIFY` @0.4 | MATCH | CLARIFY |
| add comment to issue 99 | EXECUTION | action:comment_issue_query | `comment_issue` @0.95 | MATCH |  |
| reply to issue 99 | EXECUTION | action:comment_issue_query | `comment_issue` @0.85 | MATCH |  |
| comment on 99 | EXECUTION | action:comment_issue_query | `comment_issue` @0.85 | MATCH |  |
| review issue 101 | QUERY | action:review_issue_query | `review_issue` @0.99 | MATCH |  |
| issue 101 details | QUERY | action:review_issue_query | `review_issue` @0.95 | MATCH |  |
| get issue 101 | QUERY | action:review_issue_query | `review_issue` @0.95 | MATCH |  |
| what are my issues | QUERY | action:list_issues_query | `list_issues` @0.95 | MATCH |  |
| list the issues please | QUERY | action:list_issues_query | `list_issues` @0.95 | MATCH |  |
| show the issues | QUERY | action:list_issues_query | `list_issues` @0.95 | MATCH |  |
| what's the issue count | QUERY | action:list_issues_query | `list_issues` @0.95 | MATCH |  |
| which issues are assigned to engineering | QUERY | action:list_issues_query | `list_issues` @0.85 | MATCH |  |
| show my pull requests | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| what are my prs looking like | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| where are my pull requests | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| list the prs | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| list all pull requests from this sprint | QUERY | action:list_prs_query | `list_prs` @0.85 | MATCH |  |
| any open prs waiting on me | QUERY | action:list_prs_query | `list_prs` @0.92 | MATCH |  |
| any prs assigned to me | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| any pull requests assigned to me | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| list the milestones for this quarter | QUERY | action:list_milestones_query | `list_milestones` @0.92 | MATCH |  |
| any update on the next milestone | QUERY | action:get_project_status | `get_project_status` @0.75 | MATCH |  |
| what milestones do we have | QUERY | action:list_milestones_query | `list_milestones` @0.95 | MATCH |  |
| milestones due this month | QUERY | action:list_milestones_query | `list_milestones` @0.95 | MATCH |  |
| when's the milestone deadline | QUERY | floor | `CLARIFY` @0.4 | MATCH | CLARIFY |
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
| show me the active branches | QUERY | action:list_branches_query | `list_branches` @0.92 | MATCH |  |
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
| list my active projects for this quarter | STATUS | action:manage_portfolio | `manage_portfolio` @0.92 | MATCH |  |
| any upcoming milestones for this project | STATUS | action:list_milestones | `list_milestones` @0.85 | MATCH |  |
| what's my current project | STATUS | action:get_project_status | `NONE` @0.85 | MATCH | FLOOR-expected: NONE |
| can you summarize my current work | STATUS | action:get_project_status | `NONE` @0.85 | MATCH | FLOOR-expected: NONE |
| what are my current projects | STATUS | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| give me a project overview | STATUS | action:get_project_status | `get_project_status` @0.85 | MATCH |  |
| what's the project landscape | STATUS | action:get_project_status | `manage_portfolio` @0.85 | MISMATCH |  |
| what projects am I working on | STATUS | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| tell me what I'm working on | STATUS | floor | `attention_query` @0.7 | MISMATCH | OPERATION |
| quick check, working on now? | STATUS | action:get_project_status | `session_activity_query` @0.72 | MISMATCH |  |
| what are my active projects | STATUS | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| show my active work | STATUS | floor | `attention_query` @0.75 | MISMATCH | OPERATION |
| what's my status | STATUS | action:get_project_status | `get_project_status` @0.7 | MATCH |  |
| give me a status update | STATUS | action:get_project_status | `get_project_status` @0.85 | MATCH |  |
| what is my status | STATUS | action:get_project_status | `CLARIFY` @0.4 | MATCH | FLOOR-expected: CLARIFY |
| what's my work status | STATUS | action:get_project_status | `get_project_status` @0.7 | MATCH |  |
| show the current status | STATUS | action:get_project_status | `get_project_status` @0.75 | MATCH |  |
| what's the current status | STATUS | action:get_project_status | `CLARIFY` @0.4 | MATCH | FLOOR-expected: CLARIFY |
| I need a status report | STATUS | action:generate_report | `generate_report` @0.85 | MATCH |  |
| what's my progress | STATUS | action:get_project_status | `get_project_status` @0.72 | MATCH |  |
| give me a progress update | STATUS | action:get_project_status | `get_project_status` @0.85 | MATCH |  |
| I need a progress report | STATUS | action:generate_report | `generate_report` @0.85 | MATCH |  |
| what's the progress on this | STATUS | action:get_project_status | `CLARIFY` @0.3 | MATCH | FLOOR-expected: CLARIFY |
| show today's progress | STATUS | action:get_project_status | `session_activity_query` @0.85 | MISMATCH |  |
| what's the current progress | STATUS | action:get_project_status | `CLARIFY` @0.4 | MATCH | FLOOR-expected: CLARIFY |
| how's the progress going | STATUS | action:get_project_status | `get_project_status` @0.85 | MATCH |  |
| what's the progress looking like | STATUS | action:get_project_status | `get_project_status` @0.85 | MATCH |  |
| what are my tasks | STATUS | action:list_todos_query | `list_todos_query` @0.95 | MATCH |  |
| show me my current tasks | STATUS | action:list_todos_query | `list_todos_query` @0.95 | MATCH |  |
| what are my active tasks | STATUS | action:list_todos_query | `list_todos_query` @0.95 | MATCH |  |
| show today's tasks | STATUS | action:list_todos_query | `list_todos_query` @0.95 | MATCH |  |
| list today's tasks | STATUS | action:list_todos_query | `list_todos_query` @0.95 | MATCH |  |
| tasks I'm actively working on | STATUS | action:list_todos_query | `list_todos_query` @0.85 | MATCH |  |
| what tasks do I have | STATUS | action:list_todos_query | `list_todos_query` @0.95 | MATCH |  |
| what's the task status | STATUS | action:get_project_status | `CLARIFY` @0.4 | MATCH | FLOOR-expected: CLARIFY |
| what are my assignments | STATUS | floor | `NONE` @0.95 | MATCH | NONE |
| show me my current assignments | STATUS | floor | `NONE` @0.95 | MATCH | NONE |
| what's assigned to me | STATUS | floor | `NONE` @0.95 | MATCH | NONE |
| show today's assignments | STATUS | action:get_project_status | `NONE` @0.85 | MATCH | FLOOR-expected: NONE |
| what are your capabilities? | DISCOVERY | action:get_capabilities | `get_capabilities` @1.0 | MATCH |  |
| what services can you provide? | DISCOVERY | action:get_capabilities | `get_capabilities` @0.99 | MATCH |  |
| what do you offer as an assistant? | DISCOVERY | action:get_capabilities | `get_capabilities` @0.99 | MATCH |  |
| what features does piper have? | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| what can you help me do today? | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| show me your capabilities | DISCOVERY | action:get_capabilities | `get_capabilities` @1.0 | MATCH |  |
| give me a menu of services | DISCOVERY | action:get_capabilities | `get_capabilities` @0.99 | MATCH |  |
| can you list your capabilities | DISCOVERY | action:get_capabilities | `get_capabilities` @1.0 | MATCH |  |
| I want to understand your capabilities better | DISCOVERY | action:get_capabilities | `get_capabilities` @0.99 | MATCH |  |
| pull up the capability menu | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| open the capabilities menu | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| show me the menu | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| what are you able to do for my project | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| show me the features you offer | DISCOVERY | action:get_capabilities | `get_capabilities` @0.99 | MATCH |  |
| what's available in terms of features | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| help | DISCOVERY | action:get_capabilities | `get_capabilities` @0.99 | MATCH |  |
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
| can you run an impact analysis on this change | ANALYSIS | action:analyze_blockers | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| is there a bottleneck analysis available | DISCOVERY | action:get_capabilities | `get_capabilities` @0.92 | MATCH |  |
| what risks does this project have | ANALYSIS | action:analyze_blockers | `analyze_blockers` @0.85 | MATCH |  |
| what risk do we have in this plan | ANALYSIS | action:analyze_blockers | `analyze_blockers` @0.75 | MATCH |  |
| please identify the risks in this plan | ANALYSIS | action:analyze_blockers | `analyze_blockers` @0.72 | MATCH |  |
| risks we should flag before launch | ANALYSIS | action:analyze_blockers | `analyze_blockers` @0.85 | MATCH |  |
| threats to our timeline this week | ANALYSIS | action:analyze_blockers | `analyze_blockers` @0.92 | MATCH |  |
| what could threaten this deadline | ANALYSIS | action:analyze_blockers | `analyze_blockers` @0.85 | MATCH |  |
| why won't you create issues for me | TRUST | action:explain_trust | `explain_trust` @0.95 | MATCH |  |
| why don't you just do it yourself | TRUST | action:explain_trust | `explain_trust` @0.85 | MATCH |  |
| why are you always cautious about this suggestion | PROVENANCE | action:explain_suggestion | `explain_trust` @0.95 | MISMATCH |  |
| what can't you do here | DISCOVERY | action:get_capabilities | `get_capabilities` @0.95 | MATCH |  |
| what are your limits as an assistant | DISCOVERY | action:get_capabilities | `explain_trust` @0.92 | MISMATCH |  |
| what's the capability boundary here | DISCOVERY | action:get_capabilities | `get_capabilities` @0.92 | MATCH |  |
| how well do you know me by now | MEMORY | action:pull_insights | `explain_trust` @0.95 | MISMATCH |  |
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
| remember when we shipped the last release? | MEMORY | action:check_completion_status | `get_memory` @0.85 | MISMATCH |  |
| can you show my conversation history | MEMORY | action:get_memory | `get_memory` @0.95 | MATCH |  |
| our history together has been good | MEMORY | action:get_memory | `NONE` @0.95 | MISMATCH | NONE |
| let's look at past conversations we've had | MEMORY | action:get_memory | `get_memory` @0.95 | MATCH |  |
| pull up my previous messages please | MEMORY | action:get_memory | `get_memory` @0.95 | MATCH |  |
| can I see the conversation log | MEMORY | action:get_memory | `get_memory` @0.85 | MATCH |  |
| find when I mentioned this bug before | MEMORY | action:get_memory | `get_memory` @0.85 | MATCH |  |
| search history for that conversation topic | MEMORY | action:get_memory | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| what did we discuss in our last session | MEMORY | action:get_memory | `session_activity_query` @0.92 | MISMATCH |  |
| what we discussed yesterday was helpful | MEMORY | action:get_memory | `NONE` @0.95 | MISMATCH | NONE |
| how long is your memory exactly | MEMORY | action:get_memory | `get_memory` @0.92 | MATCH |  |

## Honest caveats — what this measures and does not (m-43 / m-44)

- **Routing layer only, corpus fixtures only.** Not live traffic, not handlers, not the floor. A route:NONE MATCH says the router declined to steal a non-answer turn; a flow: MATCH says the router named the armed flow's own completing operation — whether the 2.2 seam then consumes it as a binding (and whether the floor stays honest when nothing does — #1648's fabrication class) are separate lanes this run cannot see.
- **Fixture `pending_offer_question` values exceed today's live assembly.** Arm sites currently store `summary`, not their rendered ask, so live snapshots carry question=None for most kinds (snapshot_assembly.py module docstring). The fixtures carry the ask copy the user actually saw (quoted from each arm site's own question-copy functions) — measuring the contract as designed for Phase 2.2 threading. A live shadow rerun BEFORE arm sites carry their asks would see weaker context than this run did.
- **route:NONE conflates two readings on one pair.** For the confirm-aside pair, NONE is correct both as 'aside, not an answer' and as 'answer belongs to the flow' — the rationale column, not the verdict, shows which reading the router took.
- **Armed answer-turn expectations follow the #1663 Arch ruling** (option (b), ratified 2026-08-19): flow-binding (`flow:<op>`) — the armed flow's own completing operation, consumed by the 2.2 seam, never fresh-dispatched. Non-answer turns keep route:NONE. Runs before 2026-09-12 scored answer-turns against route:NONE (the pre-ruling reading of session_snapshot.py's serialized RULE) — compare across runs only via the 2026-08-19 doc's #1663 addendum. Required condition rides the ruling: per-flow confirmation-adequacy must be confirmed before wiring each binding (EffectClass tier vs the arm-time ask).
- **Single run per condition.** No repetition; margin rows can flip run-to-run (the Phase-1b calendar-flip precedent). Deltas of ±1 on any category are within observed stochasticity.
- **is_confirm=true on the repo-question fixture is faithful to live assembly** (the repo question rides CONFIRM_PENDING_ACTION_WORKFLOW), but renders '(yes/no confirm)' on a which-repo question — a rendering wrinkle for Phase 2.2 to consider (flagged as discovered work).

Cost/duration: 468 LLM calls incl. repair retries across 468 routed (row, condition) pairs; 0 ERROR, 0 REFUSED; wall time 532s.
