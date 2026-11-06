# Router batch — main-full

Parsed 2026-11-06 15:27Z · 620 requests · 0 REFUSED (no repair in a batch) · 0 ERROR · served: anthropic:claude-haiku-4-5-20251001 (620/620)

| phrase | routes (count) | confidence range |
|---|---|---|
| give me my standup | `show_standup` ×1 | 0.95–0.95 |
| what's on my calendar today? | `meeting_time` ×1 | 0.95–0.95 |
| when is my next meeting? | `meeting_time` ×1 | 0.95–0.95 |
| what am I working on? | `session_activity_query` ×1 | 0.72–0.72 |
| what should I focus on today? | `attention_query` ×1 | 0.95–0.95 |
| what are my top priorities? | `get_top_priority` ×1 | 0.95–0.95 |
| who am I? | `get_identity` ×1 | 0.95–0.95 |
| what's my role? | `get_identity` ×1 | 0.95–0.95 |
| how do I create a ticket? | `get_contextual_guidance` ×1 | 0.95–0.95 |
| create a ticket for the login bug | `create_issue` ×1 | 0.85–0.85 |
| analyze the file I uploaded | `analyze_document` ×1 | 0.95–0.95 |
| summarize the document | `summarize_document` ×1 | 0.95–0.95 |
| what time is it? | `get_current_time` ×1 | 0.99–0.99 |
| show my open issues | `list_issues` ×1 | 0.95–0.95 |
| show my open pull requests | `list_prs` ×1 | 0.95–0.95 |
| any stale PRs? | `stale_prs` ×1 | 0.95–0.95 |
| what needs my attention? | `attention_query` ×1 | 0.99–0.99 |
| what changed since yesterday? | `changes_query` ×1 | 1.00–1.00 |
| how productive was I this week? | `productivity` ×1 | 0.95–0.95 |
| list my projects | `list_projects` ×1 | 0.99–0.99 |
| close issue 42 | `close_issue` ×1 | 0.95–0.95 |
| comment on issue 42: looks good | `comment_issue` ×1 | 0.95–0.95 |
| what have you learned about my workstyle? | `pull_insights` ×1 | 0.99–0.99 |
| set my default repo to acme/widgets | `set_default_repo` ×1 | 0.99–0.99 |
| what is my default repo? | `get_default_repo` ×1 | 0.99–0.99 |
| write a short update for the CEO on where we are | `write_stakeholder_update` ×1 | 0.95–0.95 |
| update the project plan doc with the new dates | `update_document` ×1 | 0.75–0.75 |
| can you clarify what you meant? | `CLARIFY` ×1 | 0.95–0.95 |
| give me a project status report | `get_project_status` ×1 | 0.95–0.95 |
| can we connect my github? | `get_contextual_guidance` ×1 | 0.95–0.95 |
| connect my slack | `get_contextual_guidance` ×1 | 0.95–0.95 |
| link mediajunkie/test-piper-morgan to the project | `link_repo` ×1 | 0.65–0.65 |
| help me set up github | `get_contextual_guidance` ×1 | 0.95–0.95 |
| show me my archived projects | `list_archived_projects` ×1 | 0.99–0.99 |
| list my archived projects | `list_archived_projects` ×1 | 0.99–0.99 |
| what projects have I archived? | `list_archived_projects` ×1 | 0.95–0.95 |
| what have you learned about my work style? | `pull_insights` ×1 | 0.99–0.99 |
| connect my github | `get_contextual_guidance` ×1 | 0.95–0.95 |
| connect my notion | `get_contextual_guidance` ×1 | 0.95–0.95 |
| link my google calendar | `get_contextual_guidance` ×1 | 0.95–0.95 |
| add a repo to my portfolio | `CLARIFY` ×1 | 0.40–0.40 |
| show me my todos | `list_todos_query` ×1 | 0.99–0.99 |
| connect my calendar | `get_contextual_guidance` ×1 | 0.95–0.95 |
| what reminders do I have? | `list_reminders_query` ×1 | 0.99–0.99 |
| hello | `greeting` ×1 | 0.99–0.99 |
| goodbye | `farewell` ×1 | 1.00–1.00 |
| thank you! | `thanks` ×1 | 1.00–1.00 |
| what can you do? | `get_capabilities` ×1 | 0.99–0.99 |
| why did you suggest that? | `explain_suggestion` ×1 | 0.95–0.95 |
| why can't you create issues? | `explain_trust` ×1 | 0.92–0.92 |
| what do you remember about me? | `get_memory` ×1 | 0.95–0.95 |
| what's my default repo? | `get_default_repo` ×1 | 0.99–0.99 |
| set my default repo to mediajunkie/piper-morgan-product | `set_default_repo` ×1 | 0.99–0.99 |
| write a short update for the CEO on the beta | `write_stakeholder_update` ×1 | 0.95–0.95 |
| update the roadmap doc with the new dates | `update_document` ×1 | 0.85–0.85 |
| tell me more about the github integration | `get_feature_info` ×1 | 0.99–0.99 |
| who are you? | `get_identity` ×1 | 0.99–0.99 |
| show my recurring meetings | `recurring_meetings` ×1 | 0.99–0.99 |
| what's my week look like? | `week_calendar` ×1 | 0.99–0.99 |
| what's the next milestone? | `list_milestones` ×1 | 0.85–0.85 |
| what branch are we on? | `local_git_status_query` ×1 | 0.95–0.95 |
| what did we ship this week? | `shipped_this_week` ×1 | 0.95–0.95 |
| show stale prs | `stale_prs` ×1 | 0.95–0.95 |
| close issue #123 | `close_issue` ×1 | 0.95–0.95 |
| reopen issue #123 | `reopen_issue` ×1 | 0.95–0.95 |
| comment on issue #123 | `comment_issue` ×1 | 0.95–0.95 |
| how many open issues do we have? | `list_issues` ×1 | 0.95–0.95 |
| show my prs | `list_prs` ×1 | 0.95–0.95 |
| show issue #123 | `review_issue` ×1 | 0.99–0.99 |
| show milestones | `list_milestones` ×1 | 0.95–0.95 |
| what did we create this session? | `session_activity_query` ×1 | 0.95–0.95 |
| what's my productivity? | `productivity` ×1 | 0.95–0.95 |
| remind me to review the roadmap tomorrow | `create_reminder` ×1 | 0.95–0.95 |
| complete todo 3 | `complete_todo` ×1 | 0.99–0.99 |
| show all my todos | `list_todos_query` ×1 | 0.99–0.99 |
| what's my next todo? | `list_todos_query` ×1 | 0.95–0.95 |
| when did I complete the onboarding project? | `check_completion_status` ×1 | 0.95–0.95 |
| how do I get started? | `get_contextual_guidance` ×1 | 0.95–0.95 |
| what's blocking the milestone? | `analyze_blockers` ×1 | 0.95–0.95 |
| what are my priorities? | `get_top_priority` ×1 | 0.95–0.95 |
| Set my default GitHub repository to owner/name | `set_default_repo` ×1 | 0.99–0.99 |
| what's the progress on the MVP milestone? | `get_project_status` ×1 | 0.85–0.85 |
| how is the Production milestone going | `get_project_status` ×1 | 0.85–0.85 |
| status of the Fast Follow milestone | `review_issue` ×1 | 0.60–0.60 |
| can you show me issues from just one milestone? | `CLARIFY` ×1 | 0.40–0.40 |
| MVP | `CLARIFY` ×1 | 0.30–0.30 |
| Mark the first three complete and leave the fourth one pending. | `complete_todo` ×1 | 0.95–0.95 |
| Mark the first one complete and leave the second one pending. | `complete_todo` ×1 | 0.95–0.95 |
| I want you to clear 'check the test card again,' and 'review the pr' — mark them done | `complete_todo` ×1 | 0.95–0.95 |
| clear the first two reminders | `clear_todos` ×1 | 0.95–0.95 |
| take care of the last reminder | `clear_todos` ×1 | 0.92–0.92 |
| clear all my reminders except the first one | `clear_todos` ×1 | 0.95–0.95 |
| delete the first two reminders | `delete_todo` ×1 | 0.95–0.95 |
| delete that reminder | `CLARIFY` ×1 | 0.40–0.40 |
| delete a reminder | `CLARIFY` ×1 | 0.60–0.60 |
| mark all my reminders done except for 'revise the pr' | `complete_todo` ×1 | 0.95–0.95 |
| mark the first two complete | `complete_todo` ×1 | 0.95–0.95 |
| complete the last one | `complete_todo` ×1 | 0.95–0.95 |
| mark #2 as done | `complete_todo` ×1 | 0.95–0.95 |
| mark todo 3 as complete | `complete_todo` ×1 | 0.99–0.99 |
| mark 1, 2 and 4 done | `complete_todo` ×1 | 0.99–0.99 |
| complete 'review the pr' | `complete_todo` ×1 | 0.95–0.95 |
| finish the second one | `CLARIFY` ×1 | 0.30–0.30 |
| I'm done with the first and the third | `complete_todo` ×1 | 0.92–0.92 |
| mark the PR review todo as done | `complete_todo` ×1 | 0.95–0.95 |
| mark everything done except the last one | `complete_todo` ×1 | 0.95–0.95 |
| update my project name to Atlas | `CLARIFY` ×1 | 0.60–0.60 |
| edit my project description | `update_document` ×1 | 0.85–0.85 |
| show me all project plans | `NONE` ×1 | 0.85–0.85 |
| do a standup | `show_standup` ×1 | 0.95–0.95 |
| let's do a standup | `show_standup` ×1 | 0.95–0.95 |
| Yes please | `CLARIFY` ×1 | 0.95–0.95 |
| end standup | `NONE` ×1 | 0.85–0.85 |
| i am not doing the standup right now. restore CoVa | `restore_project` ×1 | 0.95–0.95 |
| restore CoVa | `restore_project` ×1 | 0.95–0.95 |
| Please list my archived projects | `list_archived_projects` ×1 | 0.99–0.99 |
| what projects do I have? | `list_projects` ×1 | 0.95–0.95 |
| what are my projects? | `list_projects` ×1 | 0.95–0.95 |
| remind me at 3pm tomorrow to review the PR | `create_reminder` ×1 | 0.95–0.95 |
| remind me at 9:41 today to check in with the lead developer | `create_reminder` ×1 | 0.99–0.99 |
| Remind me tomorrow at 3pm to review the PR | `create_reminder` ×1 | 0.99–0.99 |
| list my archive projects | `list_archived_projects` ×1 | 0.95–0.95 |
| Archive my project Test. | `archive_project` ×1 | 0.99–0.99 |
| Archive my project "Test" | `archive_project` ×1 | 0.99–0.99 |
| Archive the project called Test | `archive_project` ×1 | 0.99–0.99 |
| Archive my Test project, please. | `archive_project` ×1 | 0.99–0.99 |
| Archive my project called "Test" please | `archive_project` ×1 | 0.99–0.99 |
| archive CoVa | `archive_project` ×1 | 0.95–0.95 |
| delete my reminders | `delete_todo` ×1 | 0.92–0.92 |
| delete my hydrate reminder | `delete_todo` ×1 | 0.95–0.95 |
| remind me | `CLARIFY` ×1 | 0.50–0.50 |
| hi piper, connect my github | `get_contextual_guidance` ×1 | 0.92–0.92 |
| what time is it? also connect my github | `PLAN[get_current_time→get_contextual_guidance]` ×1 | - |
| please clear the reminders except for "Review the PR" - also, are you able to set my default repo for me conversationally? | `PLAN[clear_todos→get_capabilities]` ×1 | - |
| are you able to set my default repo for me conversationally? | `get_capabilities` ×1 | 0.95–0.95 |
| use the interview from now on | `CLARIFY` ×1 | 0.30–0.30 |
| use the standup interview format by default from now on | `get_contextual_guidance` ×1 | 0.72–0.72 |
| change the status of issue #108 to Done | `update_issue` ×1 | 0.95–0.95 |
| please mark issue #108 in the mediajunkie/test-piper-morgan repo complete | `close_issue` ×1 | 0.95–0.95 |
| add a reminder: test the safe clarification | `create_reminder` ×1 | 0.95–0.95 |
| please remind me: ask Lead how to test "outwardness disclosure" today | `create_reminder` ×1 | 0.95–0.95 |
| please mark 1, 2, 4, and 5 done | `complete_todo` ×1 | 0.99–0.99 |
| Create a doc from this conversation | `CLARIFY` ×1 | 0.40–0.40 |
| add a todo to web test one | `create_todo` ×1 | 0.95–0.95 |
| Add three todos for the launch: draft brief, book venue, send invites | `create_todo` ×1 | 0.95–0.95 |
| show my last two new issues | `list_issues` ×1 | 0.85–0.85 |
| show my open issues in the MVP milestone | `list_issues` ×1 | 0.95–0.95 |
| open bugs labeled needs-triage | `list_issues` ×1 | 0.95–0.95 |
| what closed issues do I have | `list_issues` ×1 | 0.95–0.95 |
| Add a project called Baz with description testing the description | `add_project` ×1 | 0.95–0.95 |
| add todo buy oat milk | `create_todo` ×1 | 0.99–0.99 |
| set a reminder for the dentist appointment | `create_reminder` ×1 | 0.85–0.85 |
| create a reminder to call the plumber | `create_reminder` ×1 | 0.95–0.95 |
| don't let me forget to submit the report | `create_reminder` ×1 | 0.95–0.95 |
| I need to remember to submit my timesheet | `create_todo` ×1 | 0.95–0.95 |
| what are my reminders | `list_reminders_query` ×1 | 0.99–0.99 |
| show reminders | `list_reminders_query` ×1 | 0.95–0.95 |
| do I have any reminders | `list_reminders_query` ×1 | 0.95–0.95 |
| show todos | `list_todos_query` ×1 | 0.99–0.99 |
| list my todos | `list_todos_query` ×1 | 1.00–1.00 |
| what are my todos | `list_todos_query` ×1 | 0.99–0.99 |
| show me completed todos | `list_todos_query` ×1 | 0.85–0.85 |
| show all todos | `list_todos_query` ×1 | 0.99–0.99 |
| next todo | `list_todos_query` ×1 | 0.95–0.95 |
| what should I do next | `get_top_priority` ×1 | 0.92–0.92 |
| what do I have next to do | `get_top_priority` ×1 | 0.92–0.92 |
| where should I focus this week | `get_top_priority` ×1 | 0.85–0.85 |
| I could use some guidance on this | `CLARIFY` ×1 | 0.40–0.40 |
| do you have a recommendation | `CLARIFY` ×1 | 0.60–0.60 |
| what's your advice here | `CLARIFY` ×1 | 0.30–0.30 |
| ok that's merged, what now? | `get_top_priority` ×1 | 0.85–0.85 |
| what are the next steps | `get_contextual_guidance` ×1 | 0.85–0.85 |
| what should I do about this bug | `get_contextual_guidance` ×1 | 0.85–0.85 |
| advise me on this decision | `CLARIFY` ×1 | 0.40–0.40 |
| what's the process for filing a bug | `get_contextual_guidance` ×1 | 0.95–0.95 |
| can you help me setup the integration | `get_contextual_guidance` ×1 | 0.92–0.92 |
| can you help me configure the connector | `get_contextual_guidance` ×1 | 0.85–0.85 |
| I need to setup my projects | `get_contextual_guidance` ×1 | 0.92–0.92 |
| how do I configure my projects | `get_contextual_guidance` ×1 | 0.95–0.95 |
| how do I setup the connector | `get_contextual_guidance` ×1 | 0.85–0.85 |
| how do I configure the connector | `get_contextual_guidance` ×1 | 0.85–0.85 |
| just getting started here | `greeting` ×1 | 0.85–0.85 |
| can you help me set up the integration | `get_contextual_guidance` ×1 | 0.85–0.85 |
| I want to set up my projects | `get_contextual_guidance` ×1 | 0.95–0.95 |
| how do I set up the connector | `get_contextual_guidance` ×1 | 0.85–0.85 |
| I'd like to set up my portfolio | `get_contextual_guidance` ×1 | 0.95–0.95 |
| what's my top priority | `get_top_priority` ×1 | 0.95–0.95 |
| this is top priority for the team | `NONE` ×1 | 0.95–0.95 |
| this is the highest priority item | `NONE` ×1 | 0.95–0.95 |
| mark this as priority one | `CLARIFY` ×1 | 0.40–0.40 |
| show priorities for this sprint | `prioritize` ×1 | 0.85–0.85 |
| list priorities for the team | `NONE` ×1 | 0.85–0.85 |
| what are my current priorities | `get_top_priority` ×1 | 0.95–0.95 |
| what are the key priorities this quarter | `strategic_planning` ×1 | 0.85–0.85 |
| what's most important right now | `get_top_priority` ×1 | 0.95–0.95 |
| what matters most this week | `attention_query` ×1 | 0.85–0.85 |
| what are the key tasks for this sprint | `get_contextual_guidance` ×1 | 0.72–0.72 |
| what are the key items on my plate | `attention_query` ×1 | 0.92–0.92 |
| should i focus on the bug first | `get_top_priority` ×1 | 0.85–0.85 |
| what could I focus on | `get_top_priority` ×1 | 0.92–0.92 |
| where should my focus be today | `attention_query` ×1 | 0.92–0.92 |
| what are my focus areas this sprint | `get_contextual_guidance` ×1 | 0.72–0.72 |
| let's focus on today's priorities | `attention_query` ×1 | 0.85–0.85 |
| what's my focus this week | `week_calendar` ×1 | 0.72–0.72 |
| not sure what to focus next | `get_top_priority` ×1 | 0.85–0.85 |
| what's urgent right now | `attention_query` ×1 | 0.95–0.95 |
| what are my urgent tasks | `attention_query` ×1 | 0.95–0.95 |
| what are my urgent items | `attention_query` ×1 | 0.95–0.95 |
| what's my urgent work today | `attention_query` ×1 | 0.95–0.95 |
| what's the most urgent thing | `attention_query` ×1 | 0.95–0.95 |
| what needs my focus today | `attention_query` ×1 | 0.95–0.95 |
| what requires attention right now | `attention_query` ×1 | 0.95–0.95 |
| what's critical right now | `attention_query` ×1 | 0.95–0.95 |
| what are my critical tasks | `attention_query` ×1 | 0.92–0.92 |
| what are my critical items | `attention_query` ×1 | 0.95–0.95 |
| what's my critical work today | `attention_query` ×1 | 0.95–0.95 |
| what's the most critical thing | `attention_query` ×1 | 0.92–0.92 |
| what should I do first | `get_top_priority` ×1 | 0.95–0.95 |
| what should I tackle next | `get_top_priority` ×1 | 0.95–0.95 |
| what's next for me | `get_top_priority` ×1 | 0.92–0.92 |
| what should I review first | `get_top_priority` ×1 | 0.92–0.92 |
| which project should get my focus today | `get_top_priority` ×1 | 0.95–0.95 |
| which task should get my focus next | `get_top_priority` ×1 | 0.95–0.95 |
| not sure what to do about this | `CLARIFY` ×1 | 0.30–0.30 |
| what is on my calendar | `week_calendar` ×1 | 0.85–0.85 |
| show me my calendar today | `meeting_time` ×1 | 0.95–0.95 |
| calendar today please | `meeting_time` ×1 | 0.95–0.95 |
| what meetings today | `meeting_time` ×1 | 0.95–0.95 |
| do i have any meetings | `meeting_time` ×1 | 0.92–0.92 |
| do i have meetings | `meeting_time` ×1 | 0.85–0.85 |
| what meetings do i have | `meeting_time` ×1 | 0.85–0.85 |
| what meetings are coming up | `week_calendar` ×1 | 0.85–0.85 |
| what's my schedule today | `meeting_time` ×1 | 0.95–0.95 |
| today's schedule please | `meeting_time` ×1 | 0.95–0.95 |
| what's the schedule for today | `meeting_time` ×1 | 0.95–0.95 |
| what's my agenda today | `meeting_time` ×1 | 0.95–0.95 |
| what's my agenda tomorrow | `meeting_time` ×1 | 0.95–0.95 |
| what's my agenda this week | `week_calendar` ×1 | 0.95–0.95 |
| what's my agenda next week | `week_calendar` ×1 | 0.95–0.95 |
| show me my agenda | `meeting_time` ×1 | 0.85–0.85 |
| show me calendar for tomorrow | `meeting_time` ×1 | 0.95–0.95 |
| tomorrow's calendar please | `meeting_time` ×1 | 0.95–0.95 |
| how many meetings do I have tomorrow | `meeting_time` ×1 | 0.95–0.95 |
| what's the schedule tomorrow | `meeting_time` ×1 | 0.95–0.95 |
| tomorrow's schedule please | `meeting_time` ×1 | 0.95–0.95 |
| what's happening tomorrow | `meeting_time` ×1 | 0.85–0.85 |
| show calendar this week | `week_calendar` ×1 | 0.95–0.95 |
| show calendar next week | `week_calendar` ×1 | 0.95–0.95 |
| what's the schedule this week | `week_calendar` ×1 | 0.95–0.95 |
| what's the schedule next week | `week_calendar` ×1 | 0.95–0.95 |
| how many meetings this week | `week_calendar` ×1 | 0.95–0.95 |
| how many meetings next week | `week_calendar` ×1 | 0.95–0.95 |
| how much time in meetings do I have | `meeting_time` ×1 | 0.95–0.95 |
| how much time do I spend sitting in meetings | `meeting_time` ×1 | 0.92–0.92 |
| time spent in meetings is high lately | `NONE` ×1 | 0.95–0.95 |
| what's my meeting time today | `meeting_time` ×1 | 0.95–0.95 |
| let's review my recurring meetings | `recurring_meetings` ×1 | 0.95–0.95 |
| audit my standing meetings | `recurring_meetings` ×1 | 0.92–0.92 |
| recurring meetings keep piling up | `NONE` ×1 | 0.85–0.85 |
| show me my week | `week_calendar` ×1 | 0.95–0.95 |
| what's the week ahead look like | `week_calendar` ×1 | 0.95–0.95 |
| show the week calendar | `week_calendar` ×1 | 0.95–0.95 |
| check my calendar for conflicts | `NONE` ×1 | 0.95–0.95 |
| is my calendar showing any conflict | `NONE` ×1 | 0.95–0.95 |
| does my calendar overlap with hers | `NONE` ×1 | 0.95–0.95 |
| is there a conflict on my calendar | `NONE` ×1 | 0.95–0.95 |
| find time for a 1:1 with sarah | `NONE` ×1 | 0.85–0.85 |
| find some time for a sync | `NONE` ×1 | 0.85–0.85 |
| schedule a quick call | `NONE` ×1 | 0.95–0.95 |
| book a slot with the team | `NONE` ×1 | 0.95–0.95 |
| what's the time | `get_current_time` ×1 | 0.99–0.99 |
| current time please | `get_current_time` ×1 | 0.99–0.99 |
| give me the time now | `get_current_time` ×1 | 0.99–0.99 |
| tell me the time | `get_current_time` ×1 | 0.99–0.99 |
| what day is it | `get_current_time` ×1 | 0.95–0.95 |
| what's the date | `get_current_time` ×1 | 0.95–0.95 |
| current date please | `get_current_time` ×1 | 0.95–0.95 |
| today's date please | `get_current_time` ×1 | 0.95–0.95 |
| what's today | `get_current_time` ×1 | 0.95–0.95 |
| give me the date and time | `get_current_time` ×1 | 0.95–0.95 |
| what day of the week is it | `get_current_time` ×1 | 0.95–0.95 |
| tell me the date | `get_current_time` ×1 | 0.95–0.95 |
| what date is it | `get_current_time` ×1 | 0.95–0.95 |
| remind me today's day | `get_current_time` ×1 | 0.85–0.85 |
| pull up my calendar | `week_calendar` ×1 | 0.85–0.85 |
| show the team calendar | `NONE` ×1 | 0.95–0.95 |
| pull up my schedule | `week_calendar` ×1 | 0.85–0.85 |
| show the team schedule | `NONE` ×1 | 0.95–0.95 |
| calendar check for today | `meeting_time` ×1 | 0.95–0.95 |
| schedule check for today | `CLARIFY` ×1 | 0.40–0.40 |
| walk me through my appointments | `week_calendar` ×1 | 0.85–0.85 |
| show all appointments | `week_calendar` ×1 | 0.85–0.85 |
| walk me through my meetings | `week_calendar` ×1 | 0.85–0.85 |
| what are the upcoming meetings | `week_calendar` ×1 | 0.85–0.85 |
| when is my team meeting | `meeting_time` ×1 | 0.85–0.85 |
| when am i in a meeting | `meeting_time` ×1 | 0.95–0.95 |
| meeting check for today | `meeting_time` ×1 | 0.95–0.95 |
| meeting check for tomorrow | `meeting_time` ×1 | 0.95–0.95 |
| walk me through my events | `week_calendar` ×1 | 0.85–0.85 |
| show all events | `week_calendar` ×1 | 0.72–0.72 |
| what are the upcoming events | `week_calendar` ×1 | 0.85–0.85 |
| events check for today | `meeting_time` ×1 | 0.95–0.95 |
| events check for tomorrow | `meeting_time` ×1 | 0.92–0.92 |
| when's the next event | `meeting_time` ×1 | 0.92–0.92 |
| what did I work on today | `session_activity_query` ×1 | 0.95–0.95 |
| what happened in the meeting yesterday | `NONE` ×1 | 0.95–0.95 |
| did I finish the report yesterday | `check_completion_status` ×1 | 0.95–0.95 |
| a lot happened yesterday | `changes_query` ×1 | 0.92–0.92 |
| when was the last time I worked on this | `CLARIFY` ×1 | 0.30–0.30 |
| how long have I been working on this | `CLARIFY` ×1 | 0.30–0.30 |
| this week's priorities, remind me | `PLAN[get_top_priority→create_reminder]` ×1 | - |
| next week's priorities, remind me | `PLAN[week_calendar→create_reminder]` ×1 | - |
| this month's numbers, remind me | `PLAN[generate_report→create_reminder]` ×1 | - |
| when am i free | `week_calendar` ×1 | 0.85–0.85 |
| when's my next free slot | `meeting_time` ×1 | 0.92–0.92 |
| what's my available time | `week_calendar` ×1 | 0.85–0.85 |
| when do I have free time | `week_calendar` ×1 | 0.85–0.85 |
| what are my open slots | `week_calendar` ×1 | 0.85–0.85 |
| what shipped recently | `shipped_this_week` ×1 | 0.92–0.92 |
| can you show what has shipped | `shipped_this_week` ×1 | 0.92–0.92 |
| what has shipped this past week | `shipped_this_week` ×1 | 0.95–0.95 |
| show our stale pull requests | `stale_prs` ×1 | 0.95–0.95 |
| any old prs lying around | `stale_prs` ×1 | 0.95–0.95 |
| prs needing review | `list_prs` ×1 | 0.95–0.95 |
| close the completed issue | `CLARIFY` ×1 | 0.40–0.40 |
| please close this issue | `CLARIFY` ×1 | 0.30–0.30 |
| re-open issue 88 | `reopen_issue` ×1 | 0.95–0.95 |
| reopen the old issue | `CLARIFY` ×1 | 0.40–0.40 |
| re-open the old issue | `CLARIFY` ×1 | 0.40–0.40 |
| add comment to issue 99 | `comment_issue` ×1 | 0.95–0.95 |
| reply to issue 99 | `comment_issue` ×1 | 0.85–0.85 |
| comment on 99 | `comment_issue` ×1 | 0.95–0.95 |
| review issue 101 | `review_issue` ×1 | 0.95–0.95 |
| issue 101 details | `review_issue` ×1 | 0.95–0.95 |
| get issue 101 | `review_issue` ×1 | 0.95–0.95 |
| what are my issues | `list_issues` ×1 | 0.95–0.95 |
| list the issues please | `list_issues` ×1 | 0.95–0.95 |
| show the issues | `list_issues` ×1 | 0.85–0.85 |
| what's the issue count | `list_issues` ×1 | 0.95–0.95 |
| which issues are assigned to engineering | `list_issues` ×1 | 0.85–0.85 |
| what issues are assigned to me? | `NONE` ×1 | 0.95–0.95 |
| show my pull requests | `list_prs` ×1 | 0.95–0.95 |
| what are my prs looking like | `list_prs` ×1 | 0.95–0.95 |
| where are my pull requests | `list_prs` ×1 | 0.95–0.95 |
| list the prs | `list_prs` ×1 | 0.95–0.95 |
| list all pull requests from this sprint | `list_prs` ×1 | 0.85–0.85 |
| any open prs waiting on me | `list_prs` ×1 | 0.95–0.95 |
| any prs assigned to me | `list_prs` ×1 | 0.95–0.95 |
| any pull requests assigned to me | `list_prs` ×1 | 0.95–0.95 |
| list the milestones for this quarter | `list_milestones` ×1 | 0.85–0.85 |
| any update on the next milestone | `get_project_status` ×1 | 0.72–0.72 |
| what milestones do we have | `list_milestones` ×1 | 0.95–0.95 |
| milestones due this month | `list_milestones` ×1 | 0.92–0.92 |
| when's the milestone deadline | `CLARIFY` ×1 | 0.40–0.40 |
| any recent releases | `list_releases` ×1 | 0.95–0.95 |
| show me the releases | `list_releases` ×1 | 0.95–0.95 |
| list our releases | `list_releases` ×1 | 0.95–0.95 |
| what version are we on | `list_releases` ×1 | 0.95–0.95 |
| what's the current release | `list_releases` ×1 | 0.95–0.95 |
| what's our latest release | `list_releases` ×1 | 0.95–0.95 |
| what labels do we use | `list_labels` ×1 | 0.92–0.92 |
| show me the labels | `list_labels` ×1 | 0.95–0.95 |
| list the labels | `list_labels` ×1 | 0.95–0.95 |
| what are the issue labels | `list_labels` ×1 | 0.95–0.95 |
| labels count please | `list_labels` ×1 | 0.85–0.85 |
| all labels please | `list_labels` ×1 | 0.95–0.95 |
| show me the active branches | `list_branches` ×1 | 0.85–0.85 |
| show which branches exist | `list_branches` ×1 | 0.95–0.95 |
| list the branches | `list_branches` ×1 | 0.95–0.95 |
| what feature branches do we have | `list_branches` ×1 | 0.95–0.95 |
| what are the current branches | `list_branches` ×1 | 0.95–0.95 |
| what branches do we have | `list_branches` ×1 | 0.95–0.95 |
| what's my most important task right now | `get_top_priority` ×1 | 0.95–0.95 |
| what is my most important work today | `attention_query` ×1 | 0.92–0.92 |
| what should I work on next | `get_top_priority` ×1 | 0.95–0.95 |
| time for my stand-up | `show_standup` ×1 | 0.95–0.95 |
| give me my stand up | `show_standup` ×1 | 0.95–0.95 |
| give me a standup update | `show_standup` ×1 | 0.95–0.95 |
| give me a standup report | `show_standup` ×1 | 0.95–0.95 |
| what's my daily standup | `show_standup` ×1 | 0.95–0.95 |
| show today's standup | `show_standup` ×1 | 0.95–0.95 |
| show me my portfolio | `manage_portfolio` ×1 | 0.95–0.95 |
| list my active projects for this quarter | `list_projects` ×1 | 0.92–0.92 |
| any upcoming milestones for this project | `CLARIFY` ×1 | 0.40–0.40 |
| what's my current project | `NONE` ×1 | 0.85–0.85 |
| can you summarize my current work | `NONE` ×1 | 0.85–0.85 |
| what are my current projects | `list_projects` ×1 | 0.95–0.95 |
| give me a project overview | `get_project_status` ×1 | 0.85–0.85 |
| what's the project landscape | `list_projects` ×1 | 0.85–0.85 |
| what projects am I working on | `list_projects` ×1 | 0.95–0.95 |
| tell me what I'm working on | `session_activity_query` ×1 | 0.70–0.70 |
| quick check, working on now? | `session_activity_query` ×1 | 0.85–0.85 |
| what are my active projects | `list_projects` ×1 | 0.95–0.95 |
| show my active work | `attention_query` ×1 | 0.72–0.72 |
| what's my status | `get_project_status` ×1 | 0.85–0.85 |
| give me a status update | `get_project_status` ×1 | 0.85–0.85 |
| what is my status | `get_project_status` ×1 | 0.70–0.70 |
| what's my work status | `get_project_status` ×1 | 0.85–0.85 |
| show the current status | `get_project_status` ×1 | 0.72–0.72 |
| what's the current status | `get_project_status` ×1 | 0.72–0.72 |
| I need a status report | `get_project_status` ×1 | 0.85–0.85 |
| what's my progress | `get_project_status` ×1 | 0.72–0.72 |
| give me a progress update | `get_project_status` ×1 | 0.72–0.72 |
| I need a progress report | `generate_report` ×1 | 0.85–0.85 |
| what's the progress on this | `CLARIFY` ×1 | 0.40–0.40 |
| show today's progress | `session_activity_query` ×1 | 0.85–0.85 |
| what's the current progress | `get_project_status` ×1 | 0.85–0.85 |
| how's the progress going | `get_project_status` ×1 | 0.85–0.85 |
| what's the progress looking like | `get_project_status` ×1 | 0.85–0.85 |
| what are my tasks | `list_todos_query` ×1 | 0.95–0.95 |
| show me my current tasks | `list_todos_query` ×1 | 0.95–0.95 |
| what are my active tasks | `list_todos_query` ×1 | 0.95–0.95 |
| show today's tasks | `attention_query` ×1 | 0.85–0.85 |
| list today's tasks | `list_todos_query` ×1 | 0.95–0.95 |
| tasks I'm actively working on | `list_todos_query` ×1 | 0.85–0.85 |
| what tasks do I have | `list_todos_query` ×1 | 0.95–0.95 |
| what's the task status | `get_project_status` ×1 | 0.85–0.85 |
| what are my assignments | `NONE` ×1 | 0.85–0.85 |
| show me my current assignments | `NONE` ×1 | 0.85–0.85 |
| what's assigned to me | `NONE` ×1 | 0.95–0.95 |
| show today's assignments | `NONE` ×1 | 0.85–0.85 |
| what are your capabilities? | `get_capabilities` ×1 | 0.99–0.99 |
| what services can you provide? | `get_capabilities` ×1 | 0.99–0.99 |
| what do you offer as an assistant? | `get_capabilities` ×1 | 0.99–0.99 |
| what features does piper have? | `get_capabilities` ×1 | 0.99–0.99 |
| what can you help me do today? | `get_capabilities` ×1 | 0.95–0.95 |
| show me your capabilities | `get_capabilities` ×1 | 0.99–0.99 |
| give me a menu of services | `get_capabilities` ×1 | 0.95–0.95 |
| can you list your capabilities | `get_capabilities` ×1 | 0.99–0.99 |
| I want to understand your capabilities better | `get_capabilities` ×1 | 0.99–0.99 |
| pull up the capability menu | `get_capabilities` ×1 | 0.95–0.95 |
| open the capabilities menu | `get_capabilities` ×1 | 0.95–0.95 |
| show me the menu | `get_capabilities` ×1 | 0.95–0.95 |
| what are you able to do for my project | `get_capabilities` ×1 | 0.95–0.95 |
| show me the features you offer | `get_capabilities` ×1 | 0.99–0.99 |
| what's available in terms of features | `get_capabilities` ×1 | 0.95–0.95 |
| help | `get_capabilities` ×1 | 0.95–0.95 |
| open the help menu | `get_capabilities` ×1 | 0.95–0.95 |
| can you show help topics | `get_capabilities` ×1 | 0.95–0.95 |
| I need help understanding something | `CLARIFY` ×1 | 0.50–0.50 |
| what is blocking this release | `analyze_blockers` ×1 | 0.92–0.92 |
| what tasks are blocking our sprint | `analyze_blockers` ×1 | 0.92–0.92 |
| blockers for the release | `analyze_blockers` ×1 | 0.95–0.95 |
| what's the main obstacle here | `CLARIFY` ×1 | 0.40–0.40 |
| what's in the way of finishing this | `CLARIFY` ×1 | 0.40–0.40 |
| let's analyze the risk here | `analyze_blockers` ×1 | 0.95–0.95 |
| I'd like a risk assessment for this project | `analyze_blockers` ×1 | 0.72–0.72 |
| can you run an impact analysis on this change | `CLARIFY` ×1 | 0.40–0.40 |
| is there a bottleneck analysis available | `get_capabilities` ×1 | 0.92–0.92 |
| what risks does this project have | `analyze_blockers` ×1 | 0.85–0.85 |
| what risk do we have in this plan | `analyze_blockers` ×1 | 0.85–0.85 |
| please identify the risks in this plan | `analyze_blockers` ×1 | 0.72–0.72 |
| risks we should flag before launch | `analyze_blockers` ×1 | 0.85–0.85 |
| threats to our timeline this week | `analyze_blockers` ×1 | 0.92–0.92 |
| what could threaten this deadline | `analyze_blockers` ×1 | 0.85–0.85 |
| why won't you create issues for me | `explain_trust` ×1 | 0.95–0.95 |
| why don't you just do it yourself | `explain_trust` ×1 | 0.85–0.85 |
| why are you always cautious about this suggestion | `explain_suggestion` ×1 | 0.92–0.92 |
| what can't you do here | `get_capabilities` ×1 | 0.95–0.95 |
| what are your limits as an assistant | `get_capabilities` ×1 | 0.95–0.95 |
| what's the capability boundary here | `get_capabilities` ×1 | 0.92–0.92 |
| how well do you know me by now | `pull_insights` ×1 | 0.92–0.92 |
| do you trust me with this decision | `explain_trust` ×1 | 0.92–0.92 |
| how much do you trust my judgment | `explain_trust` ×1 | 0.95–0.95 |
| what's our relationship like these days | `explain_trust` ×1 | 0.92–0.92 |
| how do you see our relationship evolving | `explain_trust` ×1 | 0.85–0.85 |
| how do we work together on this project | `explain_trust` ×1 | 0.85–0.85 |
| why did you go ahead without asking | `explain_trust` ×1 | 0.95–0.95 |
| why do you always ask me the same thing | `explain_trust` ×1 | 0.92–0.92 |
| i didn't ask you to do that | `explain_trust` ×1 | 0.85–0.85 |
| what can you remember about our last conversation | `get_memory` ×1 | 0.95–0.95 |
| do you remember my last project update | `get_memory` ×1 | 0.95–0.95 |
| remember when we shipped the last release? | `check_completion_status` ×1 | 0.85–0.85 |
| can you show my conversation history | `get_memory` ×1 | 0.95–0.95 |
| our history together has been good | `NONE` ×1 | 0.95–0.95 |
| let's look at past conversations we've had | `get_memory` ×1 | 0.95–0.95 |
| pull up my previous messages please | `get_memory` ×1 | 0.95–0.95 |
| can I see the conversation log | `get_memory` ×1 | 0.85–0.85 |
| find when I mentioned this bug before | `get_memory` ×1 | 0.85–0.85 |
| search history for that conversation topic | `CLARIFY` ×1 | 0.40–0.40 |
| what did we discuss in our last session | `get_memory` ×1 | 0.92–0.92 |
| what we discussed yesterday was helpful | `NONE` ×1 | 0.95–0.95 |
| how long is your memory exactly | `get_memory` ×1 | 0.92–0.92 |
| link my repository to the project | `CLARIFY` ×1 | 0.40–0.40 |
| connect my repository to the project | `CLARIFY` ×1 | 0.40–0.40 |
| connect octocat/hello-world to the project | `link_repo` ×1 | 0.75–0.75 |
| add octocat/hello-world to the project | `link_repo` ×1 | 0.75–0.75 |
| please unlink my repository from this project | `CLARIFY` ×1 | 0.40–0.40 |
| please remove my repository from this project | `CLARIFY` ×1 | 0.40–0.40 |
| please disconnect my repository from this project | `unlink_repo` ×1 | 0.65–0.65 |
| please show my linked repos | `list_repos` ×1 | 0.95–0.95 |
| which repo connected to this project should i check | `CLARIFY` ×1 | 0.40–0.40 |
| can you show project repositories for this account | `list_repos` ×1 | 0.85–0.85 |
| list my repos on github | `list_repos` ×1 | 0.95–0.95 |
| show all of my repos | `list_repos` ×1 | 0.95–0.95 |
| what's changed since last week | `changes_query` ×1 | 0.95–0.95 |
| show me the changes since last monday | `changes_query` ×1 | 0.95–0.95 |
| show me everything that's changed | `changes_query` ×1 | 0.95–0.95 |
| any changes since the last deploy | `changes_query` ×1 | 0.92–0.92 |
| give me the activity since yesterday's standup | `changes_query` ×1 | 0.92–0.92 |
| any updates since this morning | `changes_query` ×1 | 0.95–0.95 |
| what needs attention right now | `attention_query` ×1 | 0.95–0.95 |
| this project needs my attention today | `attention_query` ×1 | 0.85–0.85 |
| show me what needs the most attention | `attention_query` ×1 | 0.95–0.95 |
| the items that need attention haven't been touched | `attention_query` ×1 | 0.85–0.85 |
| please list the attention items for review | `attention_query` ×1 | 0.95–0.95 |
| which repository is my default | `get_default_repo` ×1 | 0.95–0.95 |
| please show my default repository | `get_default_repo` ×1 | 0.95–0.95 |
| my default repository | `get_default_repo` ×1 | 0.95–0.95 |
| what do you know about my work habits | `pull_insights` ×1 | 0.95–0.95 |
| tell me what you've learned about my habits | `pull_insights` ×1 | 0.95–0.95 |
| what insights do you have about my productivity | `pull_insights` ×1 | 0.95–0.95 |
| show me what you've learned about my preferences | `pull_insights` ×1 | 0.95–0.95 |
| what patterns have you noticed in my work | `pull_insights` ×1 | 0.95–0.95 |
| what have you noticed about my habits lately | `pull_insights` ×1 | 0.95–0.95 |
| what branch am i on right now | `local_git_status_query` ×1 | 0.95–0.95 |
| which branch are we on at the moment | `local_git_status_query` ×1 | 0.95–0.95 |
| can you tell me the current branch | `local_git_status_query` ×1 | 0.95–0.95 |
| what's the working tree status | `local_git_status_query` ×1 | 0.95–0.95 |
| are there any uncommitted changes | `local_git_status_query` ×1 | 0.95–0.95 |
| do we have a dirty working tree | `local_git_status_query` ×1 | 0.95–0.95 |
| are we ahead of origin right now | `local_git_status_query` ×1 | 0.85–0.85 |
| are we behind upstream at all | `CLARIFY` ×1 | 0.40–0.40 |
| do we have any unpushed commits | `local_git_status_query` ×1 | 0.92–0.92 |
| can you show the local git status | `local_git_status_query` ×1 | 0.95–0.95 |
| please run git status for me | `local_git_status_query` ×1 | 0.95–0.95 |
| show me my productivity report | `productivity` ×1 | 0.95–0.95 |
| can you share my productivity metrics | `productivity` ×1 | 0.95–0.95 |
| i'd like to check my productivity this week | `productivity` ×1 | 0.95–0.95 |
| what have we created so far | `session_activity_query` ×1 | 0.92–0.92 |
| what did we make earlier | `session_activity_query` ×1 | 0.85–0.85 |
| what did i create this session | `session_activity_query` ×1 | 0.95–0.95 |
| what did we do this session | `session_activity_query` ×1 | 0.95–0.95 |
| what issues did we open during the call | `session_activity_query` ×1 | 0.92–0.92 |
| Write a short update for the client CEO on where we are with the Piper Morgan alpha testing. | `write_stakeholder_update` ×1 | 0.95–0.95 |
| help me setup my projects | `get_contextual_guidance` ×1 | 0.95–0.95 |
| help me setup projects | `get_contextual_guidance` ×1 | 0.95–0.95 |
| How do I setup my projects? | `get_contextual_guidance` ×1 | 0.95–0.95 |
| setup my projects | `get_contextual_guidance` ×1 | 0.92–0.92 |
| help me set up my portfolio | `get_contextual_guidance` ×1 | 0.95–0.95 |
| Help me set up my projects | `get_contextual_guidance` ×1 | 0.95–0.95 |
| When did I complete the API migration? | `check_completion_status` ×1 | 0.95–0.95 |
| When did I complete the migration? | `check_completion_status` ×1 | 0.95–0.95 |
| When did we launch the beta? | `check_completion_status` ×1 | 0.72–0.72 |
| Who are you and what do you do? | `get_identity` ×1 | 0.95–0.95 |
| What's your name? | `get_identity` ×1 | 0.99–0.99 |
| what date did I finish the onboarding project | `check_completion_status` ×1 | 0.92–0.92 |
| show me when we shipped the API | `shipped_this_week` ×1 | 0.60–0.60 |
| when was the migration completed | `check_completion_status` ×1 | 0.92–0.92 |
| how long ago did we ship the dashboard | `check_completion_status` ×1 | 0.92–0.92 |
| show my archived projects | `list_archived_projects` ×1 | 0.99–0.99 |
| show archived projects | `list_archived_projects` ×1 | 0.99–0.99 |
| view my archived projects | `list_archived_projects` ×1 | 0.99–0.99 |
| show my projects | `list_projects` ×1 | 0.95–0.95 |
| list my archived projects (show all names) | `list_archived_projects` ×1 | 0.95–0.95 |
| What date did I finish the database project? | `check_completion_status` ×1 | 0.92–0.92 |
| How long ago did I finish the redesign? | `check_completion_status` ×1 | 0.95–0.95 |
| When was the auth refactor shipped? | `check_completion_status` ×1 | 0.92–0.92 |
| list my archived projects and summarize my current work | `PLAN[list_archived_projects→get_project_status]` ×1 | - |
| list all projects | `list_projects` ×1 | 0.99–0.99 |
| view my projects | `list_projects` ×1 | 0.95–0.95 |
| summarize my current work and I need the archived list too | `PLAN[session_activity_query→list_archived_projects]` ×1 | - |
| Where did you get that from? | `CLARIFY` ×1 | 0.50–0.50 |
| How did you know about that? | `CLARIFY` ×1 | 0.40–0.40 |
| What made you mention the priority? | `explain_suggestion` ×1 | 0.92–0.92 |
| How do you know about my schedule? | `explain_trust` ×1 | 0.95–0.95 |
| Why is that on your list? | `CLARIFY` ×1 | 0.40–0.40 |
| Based on what? | `CLARIFY` ×1 | 0.95–0.95 |
| What's that based on? | `CLARIFY` ×1 | 0.50–0.50 |
| hide the project Beta | `archive_project` ×1 | 0.95–0.95 |
| put the old project away | `archive_project` ×1 | 0.85–0.85 |
| delete my project Gamma | `archive_project` ×1 | 0.85–0.85 |
| remove the project Delta | `archive_project` ×1 | 0.85–0.85 |
| get rid of my test project | `archive_project` ×1 | 0.85–0.85 |
| restore project Epsilon | `restore_project` ×1 | 0.99–0.99 |
| unarchive the old project | `restore_project` ×1 | 0.95–0.95 |
| bring back my archived project | `CLARIFY` ×1 | 0.40–0.40 |
| search projects for budget | `search_projects` ×1 | 0.99–0.99 |
| find project deadline | `CLARIFY` ×1 | 0.40–0.40 |
| add a new project | `add_project` ×1 | 0.95–0.95 |
| I'd like to start a new project | `add_project` ×1 | 0.95–0.95 |
| what's your name | `get_identity` ×1 | 0.95–0.95 |
| your role | `get_identity` ×1 | 0.95–0.95 |
| what do you do | `get_capabilities` ×1 | 0.95–0.95 |
| tell me about yourself | `get_identity` ×1 | 0.95–0.95 |
| introduce yourself | `get_identity` ×1 | 0.99–0.99 |
| edit the meeting notes document | `CLARIFY` ×1 | 0.50–0.50 |
| modify the status document | `CLARIFY` ×1 | 0.40–0.40 |
| change the spec doc | `CLARIFY` ×1 | 0.40–0.40 |
| add to the notes document new items | `CLARIFY` ×1 | 0.40–0.40 |
| append to the log doc | `CLARIFY` ×1 | 0.40–0.40 |
| update project plan with new deadline | `CLARIFY` ×1 | 0.40–0.40 |
| edit the report with corrections | `CLARIFY` ×1 | 0.40–0.40 |
| modify the onboarding checklist with the new steps | `update_document` ×1 | 0.72–0.72 |
| change the title of issue 108 to test new regressions | `update_issue` ×1 | 0.95–0.95 |
| Tell me about Notion | `get_feature_info` ×1 | 0.85–0.85 |
| How does the Slack integration work? | `get_feature_info` ×1 | 0.95–0.95 |
| What is the Notion integration? | `get_feature_info` ×1 | 0.95–0.95 |
| I'd like to learn more about the GitHub integration. | `get_feature_info` ×1 | 0.95–0.95 |
| Can you give me information about the Slack integration? | `get_feature_info` ×1 | 0.95–0.95 |
| Draft a status update for the board | `write_stakeholder_update` ×1 | 0.95–0.95 |
| Write something to send to Jake about the beta timeline | `write_stakeholder_update` ×1 | 0.92–0.92 |
| I need a stakeholder update on the alpha program | `write_stakeholder_update` ×1 | 0.92–0.92 |
| finish todo about deployment | `complete_todo` ×1 | 0.95–0.95 |
| Can we just mark done here? | `CLARIFY` ×1 | 0.40–0.40 |
| complete todo for the deploy checklist | `complete_todo` ×1 | 0.92–0.92 |
| use mediajunkie/piper-morgan-product as my default repo | `set_default_repo` ×1 | 0.99–0.99 |
| make mediajunkie/piper-morgan-product my default repo | `set_default_repo` ×1 | 0.99–0.99 |
| My default repo should be mediajunkie/piper-morgan-product. | `set_default_repo` ×1 | 0.99–0.99 |
| Actually, change the title to 'Implement full-text search across nav and global search bar' | `CLARIFY` ×1 | 0.40–0.40 |
| Also we should call it out in the release notes | `CLARIFY` ×1 | 0.40–0.40 |
| Create a GitHub issue: "Served check colon quotes" in dinp-machine/piper-test-activity | `create_issue` ×1 | 0.95–0.95 |
| Create a GitHub issue: "Served check bare form" | `create_issue` ×1 | 0.85–0.85 |
| Show me that issue. | `CLARIFY` ×1 | 0.30–0.30 |
| Update issue #123 | `update_issue` ×1 | 0.60–0.60 |
| Find time for a 1:1 with the team lead | `NONE` ×1 | 0.95–0.95 |
| Analyze this document | `analyze_document` ×1 | 0.85–0.85 |
| What does this document say? | `CLARIFY` ×1 | 0.40–0.40 |
| Summarize this file | `summarize_document` ×1 | 0.85–0.85 |
| Analyze the document called PRD Writing Guidelines | `analyze_document` ×1 | 0.95–0.95 |
