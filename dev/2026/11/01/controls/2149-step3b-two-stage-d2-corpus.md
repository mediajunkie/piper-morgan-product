# Router batch, two-stage — main · arm d2

Parsed 2026-11-01 18:40Z · 616 decisions · 0 REFUSED (no repair in a batch) · 0 ERROR · served: anthropic:claude-haiku-4-5-20251001 (616/616)

Rendered from: stage 1 tree `8c19ad443c` (616) · stage 2 tree `115fcf0558` (568) · **stage 1 and stage 2 trees differ: not one arm**

## Stage 1 picks

| pick | count |
|---|---|
| status_and_priorities | 124 |
| calendar_and_time | 87 |
| repo_activity | 71 |
| projects_and_repos | 67 |
| todos_and_reminders | 53 |
| assistant_and_conversation | 52 |
| CLARIFY | 42 |
| issues | 41 |
| memory_and_insights | 40 |
| documents_and_writing | 23 |
| NONE | 11 |
| calendar_and_time,projects_and_repos | 1 |
| todos_and_reminders,assistant_and_conversation | 1 |
| status_and_priorities,todos_and_reminders | 1 |
| projects_and_repos,status_and_priorities | 1 |
| status_and_priorities,projects_and_repos | 1 |

Tokens (from the batch results' usage; 0 when a result carries none): stage 1 in 706566 / out 28180 · stage 2 in 375079 / out 29675 · per decision in 1756 / out 94

Stage 2: OTHER_GROUP 24 · CLARIFY 59 (stage-1 error rate, OTHER_GROUP over decisions that reached stage 2: 24/563)

## Decisions

| phrase | routes (count) | stage-1 group (count) | llm_calls |
|---|---|---|---|
| give me my standup | `show_standup` ×1 | `status_and_priorities` ×1 | 2 |
| what's on my calendar today? | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| when is my next meeting? | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| what am I working on? | `CLARIFY` ×1 | `status_and_priorities` ×1 | 2 |
| what should I focus on today? | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| what are my top priorities? | `get_top_priority` ×1 | `status_and_priorities` ×1 | 2 |
| who am I? | `pull_insights` ×1 | `memory_and_insights` ×1 | 2 |
| what's my role? | `pull_insights` ×1 | `memory_and_insights` ×1 | 2 |
| how do I create a ticket? | `get_contextual_guidance` ×1 | `assistant_and_conversation` ×1 | 2 |
| create a ticket for the login bug | `create_issue` ×1 | `issues` ×1 | 2 |
| analyze the file I uploaded | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| summarize the document | `summarize_document` ×1 | `documents_and_writing` ×1 | 2 |
| what time is it? | `get_current_time` ×1 | `calendar_and_time` ×1 | 2 |
| show my open issues | `list_issues` ×1 | `issues` ×1 | 2 |
| show my open pull requests | `list_prs` ×1 | `repo_activity` ×1 | 2 |
| any stale PRs? | `stale_prs` ×1 | `repo_activity` ×1 | 2 |
| what needs my attention? | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| what changed since yesterday? | `changes_query` ×1 | `status_and_priorities` ×1 | 2 |
| how productive was I this week? | `productivity` ×1 | `status_and_priorities` ×1 | 2 |
| list my projects | `list_projects` ×1 | `projects_and_repos` ×1 | 2 |
| close issue 42 | `close_issue` ×1 | `issues` ×1 | 2 |
| comment on issue 42: looks good | `comment_issue` ×1 | `issues` ×1 | 2 |
| what have you learned about my workstyle? | `pull_insights` ×1 | `memory_and_insights` ×1 | 2 |
| set my default repo to acme/widgets | `set_default_repo` ×1 | `repo_activity` ×1 | 2 |
| what is my default repo? | `get_default_repo` ×1 | `repo_activity` ×1 | 2 |
| write a short update for the CEO on where we are | `write_stakeholder_update` ×1 | `documents_and_writing` ×1 | 2 |
| update the project plan doc with the new dates | `update_document` ×1 | `documents_and_writing` ×1 | 2 |
| can you clarify what you meant? | `NONE` ×1 | `NONE` ×1 | 1 |
| give me a project status report | `get_project_status` ×1 | `status_and_priorities` ×1 | 2 |
| can we connect my github? | `CLARIFY` ×1 | `projects_and_repos` ×1 | 2 |
| connect my slack | `NONE` ×1 | `NONE` ×1 | 1 |
| link mediajunkie/test-piper-morgan to the project | `link_repo` ×1 | `projects_and_repos` ×1 | 2 |
| help me set up github | `get_contextual_guidance` ×1 | `assistant_and_conversation` ×1 | 2 |
| show me my archived projects | `list_archived_projects` ×1 | `projects_and_repos` ×1 | 2 |
| list my archived projects | `list_archived_projects` ×1 | `projects_and_repos` ×1 | 2 |
| what projects have I archived? | `list_archived_projects` ×1 | `projects_and_repos` ×1 | 2 |
| what have you learned about my work style? | `pull_insights` ×1 | `memory_and_insights` ×1 | 2 |
| connect my github | `CLARIFY` ×1 | `projects_and_repos` ×1 | 2 |
| connect my notion | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| link my google calendar | `NONE` ×1 | `NONE` ×1 | 1 |
| add a repo to my portfolio | `CLARIFY` ×1 | `projects_and_repos` ×1 | 2 |
| show me my todos | `list_todos_query` ×1 | `todos_and_reminders` ×1 | 2 |
| connect my calendar | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| what reminders do I have? | `list_reminders_query` ×1 | `todos_and_reminders` ×1 | 2 |
| hello | `greeting` ×1 | `assistant_and_conversation` ×1 | 2 |
| goodbye | `farewell` ×1 | `assistant_and_conversation` ×1 | 2 |
| thank you! | `thanks` ×1 | `assistant_and_conversation` ×1 | 2 |
| what can you do? | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| why did you suggest that? | `explain_suggestion` ×1 | `memory_and_insights` ×1 | 2 |
| why can't you create issues? | `explain_trust` ×1 | `assistant_and_conversation` ×1 | 2 |
| what do you remember about me? | `get_memory` ×1 | `memory_and_insights` ×1 | 2 |
| what's my default repo? | `get_default_repo` ×1 | `repo_activity` ×1 | 2 |
| set my default repo to mediajunkie/piper-morgan-product | `set_default_repo` ×1 | `repo_activity` ×1 | 2 |
| write a short update for the CEO on the beta | `write_stakeholder_update` ×1 | `documents_and_writing` ×1 | 2 |
| update the roadmap doc with the new dates | `update_document` ×1 | `documents_and_writing` ×1 | 2 |
| tell me more about the github integration | `get_feature_info` ×1 | `assistant_and_conversation` ×1 | 2 |
| who are you? | `get_identity` ×1 | `assistant_and_conversation` ×1 | 2 |
| show my recurring meetings | `recurring_meetings` ×1 | `calendar_and_time` ×1 | 2 |
| what's my week look like? | `week_calendar` ×1 | `calendar_and_time` ×1 | 2 |
| what's the next milestone? | `list_milestones` ×1 | `repo_activity` ×1 | 2 |
| what branch are we on? | `local_git_status_query` ×1 | `repo_activity` ×1 | 2 |
| what did we ship this week? | `shipped_this_week` ×1 | `repo_activity` ×1 | 2 |
| show stale prs | `stale_prs` ×1 | `repo_activity` ×1 | 2 |
| close issue #123 | `close_issue` ×1 | `issues` ×1 | 2 |
| reopen issue #123 | `reopen_issue` ×1 | `issues` ×1 | 2 |
| comment on issue #123 | `comment_issue` ×1 | `issues` ×1 | 2 |
| how many open issues do we have? | `list_issues` ×1 | `issues` ×1 | 2 |
| show my prs | `list_prs` ×1 | `repo_activity` ×1 | 2 |
| show issue #123 | `review_issue` ×1 | `issues` ×1 | 2 |
| show milestones | `list_milestones` ×1 | `repo_activity` ×1 | 2 |
| what did we create this session? | `session_activity_query` ×1 | `memory_and_insights` ×1 | 2 |
| what's my productivity? | `productivity` ×1 | `status_and_priorities` ×1 | 2 |
| remind me to review the roadmap tomorrow | `create_reminder` ×1 | `todos_and_reminders` ×1 | 2 |
| complete todo 3 | `complete_todo` ×1 | `todos_and_reminders` ×1 | 2 |
| show all my todos | `list_todos_query` ×1 | `todos_and_reminders` ×1 | 2 |
| what's my next todo? | `list_todos_query` ×1 | `todos_and_reminders` ×1 | 2 |
| when did I complete the onboarding project? | `check_completion_status` ×1 | `status_and_priorities` ×1 | 2 |
| how do I get started? | `get_contextual_guidance` ×1 | `assistant_and_conversation` ×1 | 2 |
| what's blocking the milestone? | `analyze_blockers` ×1 | `status_and_priorities` ×1 | 2 |
| what are my priorities? | `prioritize` ×1 | `status_and_priorities` ×1 | 2 |
| can you show me issues from just one milestone? | `CLARIFY` ×1 | `issues` ×1 | 2 |
| MVP | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| Mark the first three complete and leave the fourth one pending. | `complete_todo` ×1 | `todos_and_reminders` ×1 | 2 |
| Mark the first one complete and leave the second one pending. | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| I want you to clear 'check the test card again,' and 'review the pr' — mark them done | `complete_todo` ×1 | `todos_and_reminders` ×1 | 2 |
| clear the first two reminders | `clear_todos` ×1 | `todos_and_reminders` ×1 | 2 |
| take care of the last reminder | `clear_todos` ×1 | `todos_and_reminders` ×1 | 2 |
| clear all my reminders except the first one | `clear_todos` ×1 | `todos_and_reminders` ×1 | 2 |
| delete the first two reminders | `delete_todo` ×1 | `todos_and_reminders` ×1 | 2 |
| delete that reminder | `delete_todo` ×1 | `todos_and_reminders` ×1 | 2 |
| delete a reminder | `CLARIFY` ×1 | `todos_and_reminders` ×1 | 2 |
| mark all my reminders done except for 'revise the pr' | `complete_todo` ×1 | `todos_and_reminders` ×1 | 2 |
| mark the first two complete | `complete_todo` ×1 | `todos_and_reminders` ×1 | 2 |
| complete the last one | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| mark #2 as done | `close_issue` ×1 | `issues` ×1 | 2 |
| mark todo 3 as complete | `complete_todo` ×1 | `todos_and_reminders` ×1 | 2 |
| mark 1, 2 and 4 done | `complete_todo` ×1 | `todos_and_reminders` ×1 | 2 |
| complete 'review the pr' | `complete_todo` ×1 | `todos_and_reminders` ×1 | 2 |
| finish the second one | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| I'm done with the first and the third | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| mark the PR review todo as done | `complete_todo` ×1 | `todos_and_reminders` ×1 | 2 |
| mark everything done except the last one | `complete_todo` ×1 | `todos_and_reminders` ×1 | 2 |
| update my project name to Atlas | `CLARIFY` ×1 | `projects_and_repos` ×1 | 2 |
| edit my project description | `CLARIFY` ×1 | `projects_and_repos` ×1 | 2 |
| show me all project plans | `CLARIFY` ×1 | `status_and_priorities` ×1 | 2 |
| do a standup | `show_standup` ×1 | `status_and_priorities` ×1 | 2 |
| let's do a standup | `show_standup` ×1 | `status_and_priorities` ×1 | 2 |
| Yes please | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| end standup | `CLARIFY` ×1 | `status_and_priorities` ×1 | 2 |
| i am not doing the standup right now. restore CoVa | `restore_project` ×1 | `projects_and_repos` ×1 | 2 |
| restore CoVa | `restore_project` ×1 | `projects_and_repos` ×1 | 2 |
| Please list my archived projects | `list_archived_projects` ×1 | `projects_and_repos` ×1 | 2 |
| what projects do I have? | `list_projects` ×1 | `projects_and_repos` ×1 | 2 |
| what are my projects? | `list_projects` ×1 | `projects_and_repos` ×1 | 2 |
| remind me at 3pm tomorrow to review the PR | `create_reminder` ×1 | `todos_and_reminders` ×1 | 2 |
| remind me at 9:41 today to check in with the lead developer | `create_reminder` ×1 | `todos_and_reminders` ×1 | 2 |
| Remind me tomorrow at 3pm to review the PR | `create_reminder` ×1 | `todos_and_reminders` ×1 | 2 |
| list my archive projects | `list_archived_projects` ×1 | `projects_and_repos` ×1 | 2 |
| Archive my project Test. | `archive_project` ×1 | `projects_and_repos` ×1 | 2 |
| Archive my project "Test" | `archive_project` ×1 | `projects_and_repos` ×1 | 2 |
| Archive the project called Test | `archive_project` ×1 | `projects_and_repos` ×1 | 2 |
| Archive my Test project, please. | `archive_project` ×1 | `projects_and_repos` ×1 | 2 |
| Archive my project called "Test" please | `archive_project` ×1 | `projects_and_repos` ×1 | 2 |
| archive CoVa | `archive_project` ×1 | `projects_and_repos` ×1 | 2 |
| delete my reminders | `delete_todo` ×1 | `todos_and_reminders` ×1 | 2 |
| delete my hydrate reminder | `delete_todo` ×1 | `todos_and_reminders` ×1 | 2 |
| remind me | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| hi piper, connect my github | `NONE` ×1 | `NONE` ×1 | 1 |
| what time is it? also connect my github | `PLAN[get_current_time→manage_repos]` ×1 | `calendar_and_time,projects_and_repos` ×1 | 3 |
| please clear the reminders except for "Review the PR" - also, are you able to set my default repo for me conversationally? | `PLAN[clear_todos→get_capabilities]` ×1 | `todos_and_reminders,assistant_and_conversation` ×1 | 3 |
| are you able to set my default repo for me conversationally? | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| use the interview from now on | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| use the standup interview format by default from now on | `CLARIFY` ×1 | `memory_and_insights` ×1 | 2 |
| change the status of issue #108 to Done | `update_issue` ×1 | `issues` ×1 | 2 |
| please mark issue #108 in the mediajunkie/test-piper-morgan repo complete | `close_issue` ×1 | `issues` ×1 | 2 |
| add a reminder: test the safe clarification | `create_reminder` ×1 | `todos_and_reminders` ×1 | 2 |
| please remind me: ask Lead how to test "outwardness disclosure" today | `create_reminder` ×1 | `todos_and_reminders` ×1 | 2 |
| please mark 1, 2, 4, and 5 done | `complete_todo` ×1 | `todos_and_reminders` ×1 | 2 |
| Create a doc from this conversation | `CLARIFY` ×1 | `documents_and_writing` ×1 | 2 |
| add a todo to web test one | `create_todo` ×1 | `todos_and_reminders` ×1 | 2 |
| Add three todos for the launch: draft brief, book venue, send invites | `create_todo` ×1 | `todos_and_reminders` ×1 | 2 |
| show my last two new issues | `list_issues` ×1 | `issues` ×1 | 2 |
| show my open issues in the MVP milestone | `list_issues` ×1 | `issues` ×1 | 2 |
| open bugs labeled needs-triage | `list_issues` ×1 | `issues` ×1 | 2 |
| what closed issues do I have | `list_issues` ×1 | `issues` ×1 | 2 |
| Add a project called Baz with description testing the description | `add_project` ×1 | `projects_and_repos` ×1 | 2 |
| add todo buy oat milk | `create_todo` ×1 | `todos_and_reminders` ×1 | 2 |
| set a reminder for the dentist appointment | `create_reminder` ×1 | `todos_and_reminders` ×1 | 2 |
| create a reminder to call the plumber | `create_reminder` ×1 | `todos_and_reminders` ×1 | 2 |
| don't let me forget to submit the report | `create_reminder` ×1 | `todos_and_reminders` ×1 | 2 |
| I need to remember to submit my timesheet | `create_reminder` ×1 | `todos_and_reminders` ×1 | 2 |
| what are my reminders | `list_reminders_query` ×1 | `todos_and_reminders` ×1 | 2 |
| show reminders | `list_reminders_query` ×1 | `todos_and_reminders` ×1 | 2 |
| do I have any reminders | `list_reminders_query` ×1 | `todos_and_reminders` ×1 | 2 |
| show todos | `list_todos_query` ×1 | `todos_and_reminders` ×1 | 2 |
| list my todos | `list_todos_query` ×1 | `todos_and_reminders` ×1 | 2 |
| what are my todos | `list_todos_query` ×1 | `todos_and_reminders` ×1 | 2 |
| show me completed todos | `list_todos_query` ×1 | `todos_and_reminders` ×1 | 2 |
| show all todos | `list_todos_query` ×1 | `todos_and_reminders` ×1 | 2 |
| next todo | `list_todos_query` ×1 | `todos_and_reminders` ×1 | 2 |
| what should I do next | `get_top_priority` ×1 | `status_and_priorities` ×1 | 2 |
| what do I have next to do | `get_top_priority` ×1 | `status_and_priorities` ×1 | 2 |
| where should I focus this week | `get_top_priority` ×1 | `status_and_priorities` ×1 | 2 |
| I could use some guidance on this | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| do you have a recommendation | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| what's your advice here | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| ok that's merged, what now? | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| what are the next steps | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| what should I do about this bug | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| advise me on this decision | `NONE` ×1 | `NONE` ×1 | 1 |
| what's the process for filing a bug | `get_contextual_guidance` ×1 | `assistant_and_conversation` ×1 | 2 |
| can you help me setup the integration | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| can you help me configure the connector | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| I need to setup my projects | `manage_portfolio` ×1 | `projects_and_repos` ×1 | 2 |
| how do I configure my projects | `get_contextual_guidance` ×1 | `assistant_and_conversation` ×1 | 2 |
| how do I setup the connector | `get_contextual_guidance` ×1 | `assistant_and_conversation` ×1 | 2 |
| how do I configure the connector | `get_contextual_guidance` ×1 | `assistant_and_conversation` ×1 | 2 |
| just getting started here | `NONE` ×1 | `NONE` ×1 | 1 |
| can you help me set up the integration | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| I want to set up my projects | `CLARIFY` ×1 | `projects_and_repos` ×1 | 2 |
| how do I set up the connector | `get_contextual_guidance` ×1 | `assistant_and_conversation` ×1 | 2 |
| I'd like to set up my portfolio | `manage_portfolio` ×1 | `projects_and_repos` ×1 | 2 |
| what's my top priority | `get_top_priority` ×1 | `status_and_priorities` ×1 | 2 |
| this is top priority for the team | `CLARIFY` ×1 | `status_and_priorities` ×1 | 2 |
| this is the highest priority item | `CLARIFY` ×1 | `status_and_priorities` ×1 | 2 |
| mark this as priority one | `prioritize` ×1 | `status_and_priorities` ×1 | 2 |
| show priorities for this sprint | `prioritize` ×1 | `status_and_priorities` ×1 | 2 |
| list priorities for the team | `prioritize` ×1 | `status_and_priorities` ×1 | 2 |
| what are my current priorities | `get_top_priority` ×1 | `status_and_priorities` ×1 | 2 |
| what are the key priorities this quarter | `strategic_planning` ×1 | `status_and_priorities` ×1 | 2 |
| what's most important right now | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| what matters most this week | `get_top_priority` ×1 | `status_and_priorities` ×1 | 2 |
| what are the key tasks for this sprint | `get_project_status` ×1 | `status_and_priorities` ×1 | 2 |
| what are the key items on my plate | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| should i focus on the bug first | `get_top_priority` ×1 | `status_and_priorities` ×1 | 2 |
| what could I focus on | `get_top_priority` ×1 | `status_and_priorities` ×1 | 2 |
| where should my focus be today | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| what are my focus areas this sprint | `show_standup` ×1 | `status_and_priorities` ×1 | 2 |
| let's focus on today's priorities | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| what's my focus this week | `get_top_priority` ×1 | `status_and_priorities` ×1 | 2 |
| not sure what to focus next | `get_top_priority` ×1 | `status_and_priorities` ×1 | 2 |
| what's urgent right now | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| what are my urgent tasks | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| what are my urgent items | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| what's my urgent work today | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| what's the most urgent thing | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| what needs my focus today | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| what requires attention right now | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| what's critical right now | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| what are my critical tasks | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| what are my critical items | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| what's my critical work today | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| what's the most critical thing | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| what should I do first | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| what should I tackle next | `get_top_priority` ×1 | `status_and_priorities` ×1 | 2 |
| what's next for me | `get_top_priority` ×1 | `status_and_priorities` ×1 | 2 |
| what should I review first | `get_top_priority` ×1 | `status_and_priorities` ×1 | 2 |
| which project should get my focus today | `get_top_priority` ×1 | `status_and_priorities` ×1 | 2 |
| which task should get my focus next | `get_top_priority` ×1 | `status_and_priorities` ×1 | 2 |
| not sure what to do about this | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| what is on my calendar | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| show me my calendar today | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| calendar today please | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| what meetings today | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| do i have any meetings | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| do i have meetings | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| what meetings do i have | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| what meetings are coming up | `week_calendar` ×1 | `calendar_and_time` ×1 | 2 |
| what's my schedule today | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| today's schedule please | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| what's the schedule for today | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| what's my agenda today | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| what's my agenda tomorrow | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| what's my agenda this week | `week_calendar` ×1 | `calendar_and_time` ×1 | 2 |
| what's my agenda next week | `week_calendar` ×1 | `calendar_and_time` ×1 | 2 |
| show me my agenda | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| show me calendar for tomorrow | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| tomorrow's calendar please | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| how many meetings do I have tomorrow | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| what's the schedule tomorrow | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| tomorrow's schedule please | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| what's happening tomorrow | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| show calendar this week | `week_calendar` ×1 | `calendar_and_time` ×1 | 2 |
| show calendar next week | `week_calendar` ×1 | `calendar_and_time` ×1 | 2 |
| what's the schedule this week | `week_calendar` ×1 | `calendar_and_time` ×1 | 2 |
| what's the schedule next week | `week_calendar` ×1 | `calendar_and_time` ×1 | 2 |
| how many meetings this week | `week_calendar` ×1 | `calendar_and_time` ×1 | 2 |
| how many meetings next week | `week_calendar` ×1 | `calendar_and_time` ×1 | 2 |
| how much time in meetings do I have | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| how much time do I spend sitting in meetings | `productivity` ×1 | `status_and_priorities` ×1 | 2 |
| time spent in meetings is high lately | `analyze_data` ×1 | `status_and_priorities` ×1 | 2 |
| what's my meeting time today | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| let's review my recurring meetings | `recurring_meetings` ×1 | `calendar_and_time` ×1 | 2 |
| audit my standing meetings | `recurring_meetings` ×1 | `calendar_and_time` ×1 | 2 |
| recurring meetings keep piling up | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| show me my week | `week_calendar` ×1 | `calendar_and_time` ×1 | 2 |
| what's the week ahead look like | `week_calendar` ×1 | `calendar_and_time` ×1 | 2 |
| show the week calendar | `week_calendar` ×1 | `calendar_and_time` ×1 | 2 |
| check my calendar for conflicts | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| is my calendar showing any conflict | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| does my calendar overlap with hers | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| is there a conflict on my calendar | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| find time for a 1:1 with sarah | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| find some time for a sync | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| schedule a quick call | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| book a slot with the team | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| what's the time | `get_current_time` ×1 | `calendar_and_time` ×1 | 2 |
| current time please | `get_current_time` ×1 | `calendar_and_time` ×1 | 2 |
| give me the time now | `get_current_time` ×1 | `calendar_and_time` ×1 | 2 |
| tell me the time | `get_current_time` ×1 | `calendar_and_time` ×1 | 2 |
| what day is it | `get_current_time` ×1 | `calendar_and_time` ×1 | 2 |
| what's the date | `get_current_time` ×1 | `calendar_and_time` ×1 | 2 |
| current date please | `get_current_time` ×1 | `calendar_and_time` ×1 | 2 |
| today's date please | `get_current_time` ×1 | `calendar_and_time` ×1 | 2 |
| what's today | `get_current_time` ×1 | `calendar_and_time` ×1 | 2 |
| give me the date and time | `get_current_time` ×1 | `calendar_and_time` ×1 | 2 |
| what day of the week is it | `get_current_time` ×1 | `calendar_and_time` ×1 | 2 |
| tell me the date | `get_current_time` ×1 | `calendar_and_time` ×1 | 2 |
| what date is it | `get_current_time` ×1 | `calendar_and_time` ×1 | 2 |
| remind me today's day | `get_current_time` ×1 | `calendar_and_time` ×1 | 2 |
| pull up my calendar | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| show the team calendar | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| pull up my schedule | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| show the team schedule | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| calendar check for today | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| schedule check for today | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| walk me through my appointments | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| show all appointments | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| walk me through my meetings | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| what are the upcoming meetings | `recurring_meetings` ×1 | `calendar_and_time` ×1 | 2 |
| when is my team meeting | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| when am i in a meeting | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| meeting check for today | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| meeting check for tomorrow | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| walk me through my events | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| show all events | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| what are the upcoming events | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| events check for today | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| events check for tomorrow | `meeting_time` ×1 | `calendar_and_time` ×1 | 2 |
| when's the next event | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| what did I work on today | `changes_query` ×1 | `status_and_priorities` ×1 | 2 |
| what happened in the meeting yesterday | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| did I finish the report yesterday | `check_completion_status` ×1 | `status_and_priorities` ×1 | 2 |
| a lot happened yesterday | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| when was the last time I worked on this | `CLARIFY` ×1 | `memory_and_insights` ×1 | 2 |
| how long have I been working on this | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| this week's priorities, remind me | `prioritize` ×1 | `status_and_priorities` ×1 | 2 |
| next week's priorities, remind me | `PLAN[prioritize→create_reminder]` ×1 | `status_and_priorities,todos_and_reminders` ×1 | 3 |
| this month's numbers, remind me | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| when am i free | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| when's my next free slot | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| what's my available time | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| when do I have free time | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| what are my open slots | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| what shipped recently | `shipped_this_week` ×1 | `repo_activity` ×1 | 2 |
| can you show what has shipped | `shipped_this_week` ×1 | `repo_activity` ×1 | 2 |
| what has shipped this past week | `shipped_this_week` ×1 | `repo_activity` ×1 | 2 |
| show our stale pull requests | `stale_prs` ×1 | `repo_activity` ×1 | 2 |
| any old prs lying around | `stale_prs` ×1 | `repo_activity` ×1 | 2 |
| prs needing review | `list_prs` ×1 | `repo_activity` ×1 | 2 |
| close the completed issue | `CLARIFY` ×1 | `issues` ×1 | 2 |
| please close this issue | `close_issue` ×1 | `issues` ×1 | 2 |
| re-open issue 88 | `reopen_issue` ×1 | `issues` ×1 | 2 |
| reopen the old issue | `CLARIFY` ×1 | `issues` ×1 | 2 |
| re-open the old issue | `reopen_issue` ×1 | `issues` ×1 | 2 |
| add comment to issue 99 | `comment_issue` ×1 | `issues` ×1 | 2 |
| reply to issue 99 | `comment_issue` ×1 | `issues` ×1 | 2 |
| comment on 99 | `comment_issue` ×1 | `issues` ×1 | 2 |
| review issue 101 | `review_issue` ×1 | `issues` ×1 | 2 |
| issue 101 details | `review_issue` ×1 | `issues` ×1 | 2 |
| get issue 101 | `review_issue` ×1 | `issues` ×1 | 2 |
| what are my issues | `list_issues` ×1 | `issues` ×1 | 2 |
| list the issues please | `list_issues` ×1 | `issues` ×1 | 2 |
| show the issues | `list_issues` ×1 | `issues` ×1 | 2 |
| what's the issue count | `list_issues` ×1 | `issues` ×1 | 2 |
| which issues are assigned to engineering | `list_issues` ×1 | `issues` ×1 | 2 |
| what issues are assigned to me? | `list_issues` ×1 | `issues` ×1 | 2 |
| show my pull requests | `list_prs` ×1 | `repo_activity` ×1 | 2 |
| what are my prs looking like | `list_prs` ×1 | `repo_activity` ×1 | 2 |
| where are my pull requests | `list_prs` ×1 | `repo_activity` ×1 | 2 |
| list the prs | `list_prs` ×1 | `repo_activity` ×1 | 2 |
| list all pull requests from this sprint | `list_prs` ×1 | `repo_activity` ×1 | 2 |
| any open prs waiting on me | `list_prs` ×1 | `repo_activity` ×1 | 2 |
| any prs assigned to me | `list_prs` ×1 | `repo_activity` ×1 | 2 |
| any pull requests assigned to me | `list_prs` ×1 | `repo_activity` ×1 | 2 |
| list the milestones for this quarter | `list_milestones` ×1 | `repo_activity` ×1 | 2 |
| any update on the next milestone | `list_milestones` ×1 | `repo_activity` ×1 | 2 |
| what milestones do we have | `list_milestones` ×1 | `repo_activity` ×1 | 2 |
| milestones due this month | `list_milestones` ×1 | `repo_activity` ×1 | 2 |
| when's the milestone deadline | `CLARIFY` ×1 | `repo_activity` ×1 | 2 |
| any recent releases | `list_releases` ×1 | `repo_activity` ×1 | 2 |
| show me the releases | `list_releases` ×1 | `repo_activity` ×1 | 2 |
| list our releases | `list_releases` ×1 | `repo_activity` ×1 | 2 |
| what version are we on | `list_releases` ×1 | `repo_activity` ×1 | 2 |
| what's the current release | `list_releases` ×1 | `repo_activity` ×1 | 2 |
| what's our latest release | `list_releases` ×1 | `repo_activity` ×1 | 2 |
| what labels do we use | `list_labels` ×1 | `repo_activity` ×1 | 2 |
| show me the labels | `list_labels` ×1 | `repo_activity` ×1 | 2 |
| list the labels | `list_labels` ×1 | `repo_activity` ×1 | 2 |
| what are the issue labels | `list_labels` ×1 | `repo_activity` ×1 | 2 |
| labels count please | `list_labels` ×1 | `repo_activity` ×1 | 2 |
| all labels please | `list_labels` ×1 | `repo_activity` ×1 | 2 |
| show me the active branches | `list_branches` ×1 | `repo_activity` ×1 | 2 |
| show which branches exist | `list_branches` ×1 | `repo_activity` ×1 | 2 |
| list the branches | `list_branches` ×1 | `repo_activity` ×1 | 2 |
| what feature branches do we have | `list_branches` ×1 | `repo_activity` ×1 | 2 |
| what are the current branches | `list_branches` ×1 | `repo_activity` ×1 | 2 |
| what branches do we have | `list_branches` ×1 | `repo_activity` ×1 | 2 |
| what's my most important task right now | `get_top_priority` ×1 | `status_and_priorities` ×1 | 2 |
| what is my most important work today | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| what should I work on next | `get_top_priority` ×1 | `status_and_priorities` ×1 | 2 |
| time for my stand-up | `show_standup` ×1 | `status_and_priorities` ×1 | 2 |
| give me my stand up | `show_standup` ×1 | `status_and_priorities` ×1 | 2 |
| give me a standup update | `show_standup` ×1 | `status_and_priorities` ×1 | 2 |
| give me a standup report | `show_standup` ×1 | `status_and_priorities` ×1 | 2 |
| what's my daily standup | `show_standup` ×1 | `status_and_priorities` ×1 | 2 |
| show today's standup | `show_standup` ×1 | `status_and_priorities` ×1 | 2 |
| show me my portfolio | `manage_portfolio` ×1 | `projects_and_repos` ×1 | 2 |
| list my active projects for this quarter | `list_projects` ×1 | `projects_and_repos` ×1 | 2 |
| any upcoming milestones for this project | `list_milestones` ×1 | `repo_activity` ×1 | 2 |
| what's my current project | `CLARIFY` ×1 | `status_and_priorities` ×1 | 2 |
| can you summarize my current work | `CLARIFY` ×1 | `status_and_priorities` ×1 | 2 |
| what are my current projects | `list_projects` ×1 | `projects_and_repos` ×1 | 2 |
| give me a project overview | `get_project_status` ×1 | `status_and_priorities` ×1 | 2 |
| what's the project landscape | `CLARIFY` ×1 | `status_and_priorities` ×1 | 2 |
| what projects am I working on | `list_projects` ×1 | `projects_and_repos` ×1 | 2 |
| tell me what I'm working on | `CLARIFY` ×1 | `status_and_priorities` ×1 | 2 |
| quick check, working on now? | `CLARIFY` ×1 | `status_and_priorities` ×1 | 2 |
| what are my active projects | `list_projects` ×1 | `projects_and_repos` ×1 | 2 |
| show my active work | `CLARIFY` ×1 | `status_and_priorities` ×1 | 2 |
| what's my status | `CLARIFY` ×1 | `status_and_priorities` ×1 | 2 |
| give me a status update | `get_project_status` ×1 | `status_and_priorities` ×1 | 2 |
| what is my status | `CLARIFY` ×1 | `status_and_priorities` ×1 | 2 |
| what's my work status | `show_standup` ×1 | `status_and_priorities` ×1 | 2 |
| show the current status | `get_project_status` ×1 | `status_and_priorities` ×1 | 2 |
| what's the current status | `get_project_status` ×1 | `status_and_priorities` ×1 | 2 |
| I need a status report | `get_project_status` ×1 | `status_and_priorities` ×1 | 2 |
| what's my progress | `CLARIFY` ×1 | `status_and_priorities` ×1 | 2 |
| give me a progress update | `get_project_status` ×1 | `status_and_priorities` ×1 | 2 |
| I need a progress report | `CLARIFY` ×1 | `documents_and_writing` ×1 | 2 |
| what's the progress on this | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| show today's progress | `show_standup` ×1 | `status_and_priorities` ×1 | 2 |
| what's the current progress | `get_project_status` ×1 | `status_and_priorities` ×1 | 2 |
| how's the progress going | `get_project_status` ×1 | `status_and_priorities` ×1 | 2 |
| what's the progress looking like | `get_project_status` ×1 | `status_and_priorities` ×1 | 2 |
| what are my tasks | `list_todos_query` ×1 | `todos_and_reminders` ×1 | 2 |
| show me my current tasks | `list_todos_query` ×1 | `todos_and_reminders` ×1 | 2 |
| what are my active tasks | `list_todos_query` ×1 | `todos_and_reminders` ×1 | 2 |
| show today's tasks | `list_todos_query` ×1 | `todos_and_reminders` ×1 | 2 |
| list today's tasks | `list_todos_query` ×1 | `todos_and_reminders` ×1 | 2 |
| tasks I'm actively working on | `CLARIFY` ×1 | `status_and_priorities` ×1 | 2 |
| what tasks do I have | `list_todos_query` ×1 | `todos_and_reminders` ×1 | 2 |
| what's the task status | `get_project_status` ×1 | `status_and_priorities` ×1 | 2 |
| what are my assignments | `CLARIFY` ×1 | `status_and_priorities` ×1 | 2 |
| show me my current assignments | `CLARIFY` ×1 | `status_and_priorities` ×1 | 2 |
| what's assigned to me | `list_issues` ×1 | `issues` ×1 | 2 |
| show today's assignments | `CLARIFY` ×1 | `status_and_priorities` ×1 | 2 |
| what are your capabilities? | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| what services can you provide? | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| what do you offer as an assistant? | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| what features does piper have? | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| what can you help me do today? | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| show me your capabilities | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| give me a menu of services | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| can you list your capabilities | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| I want to understand your capabilities better | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| pull up the capability menu | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| open the capabilities menu | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| show me the menu | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| what are you able to do for my project | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| show me the features you offer | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| what's available in terms of features | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| help | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| open the help menu | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| can you show help topics | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| I need help understanding something | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| what is blocking this release | `analyze_blockers` ×1 | `status_and_priorities` ×1 | 2 |
| what tasks are blocking our sprint | `analyze_blockers` ×1 | `status_and_priorities` ×1 | 2 |
| blockers for the release | `analyze_blockers` ×1 | `status_and_priorities` ×1 | 2 |
| what's the main obstacle here | `analyze_blockers` ×1 | `status_and_priorities` ×1 | 2 |
| what's in the way of finishing this | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| let's analyze the risk here | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| I'd like a risk assessment for this project | `analyze_blockers` ×1 | `status_and_priorities` ×1 | 2 |
| can you run an impact analysis on this change | `CLARIFY` ×1 | `documents_and_writing` ×1 | 2 |
| is there a bottleneck analysis available | `analyze_blockers` ×1 | `status_and_priorities` ×1 | 2 |
| what risks does this project have | `analyze_blockers` ×1 | `status_and_priorities` ×1 | 2 |
| what risk do we have in this plan | `analyze_blockers` ×1 | `status_and_priorities` ×1 | 2 |
| please identify the risks in this plan | `analyze_blockers` ×1 | `status_and_priorities` ×1 | 2 |
| risks we should flag before launch | `analyze_blockers` ×1 | `status_and_priorities` ×1 | 2 |
| threats to our timeline this week | `analyze_blockers` ×1 | `status_and_priorities` ×1 | 2 |
| what could threaten this deadline | `analyze_blockers` ×1 | `status_and_priorities` ×1 | 2 |
| why won't you create issues for me | `explain_trust` ×1 | `assistant_and_conversation` ×1 | 2 |
| why don't you just do it yourself | `NONE` ×1 | `NONE` ×1 | 1 |
| why are you always cautious about this suggestion | `explain_suggestion` ×1 | `memory_and_insights` ×1 | 2 |
| what can't you do here | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| what are your limits as an assistant | `explain_trust` ×1 | `assistant_and_conversation` ×1 | 2 |
| what's the capability boundary here | `get_capabilities` ×1 | `assistant_and_conversation` ×1 | 2 |
| how well do you know me by now | `pull_insights` ×1 | `memory_and_insights` ×1 | 2 |
| do you trust me with this decision | `explain_trust` ×1 | `assistant_and_conversation` ×1 | 2 |
| how much do you trust my judgment | `explain_trust` ×1 | `assistant_and_conversation` ×1 | 2 |
| what's our relationship like these days | `pull_insights` ×1 | `memory_and_insights` ×1 | 2 |
| how do you see our relationship evolving | `NONE` ×1 | `NONE` ×1 | 1 |
| how do we work together on this project | `explain_trust` ×1 | `assistant_and_conversation` ×1 | 2 |
| why did you go ahead without asking | `CLARIFY` ×1 | `memory_and_insights` ×1 | 2 |
| why do you always ask me the same thing | `pull_insights` ×1 | `memory_and_insights` ×1 | 2 |
| i didn't ask you to do that | `NONE` ×1 | `NONE` ×1 | 1 |
| what can you remember about our last conversation | `get_memory` ×1 | `memory_and_insights` ×1 | 2 |
| do you remember my last project update | `get_memory` ×1 | `memory_and_insights` ×1 | 2 |
| remember when we shipped the last release? | `get_memory` ×1 | `memory_and_insights` ×1 | 2 |
| can you show my conversation history | `get_memory` ×1 | `memory_and_insights` ×1 | 2 |
| our history together has been good | `CLARIFY` ×1 | `memory_and_insights` ×1 | 2 |
| let's look at past conversations we've had | `get_memory` ×1 | `memory_and_insights` ×1 | 2 |
| pull up my previous messages please | `get_memory` ×1 | `memory_and_insights` ×1 | 2 |
| can I see the conversation log | `get_memory` ×1 | `memory_and_insights` ×1 | 2 |
| find when I mentioned this bug before | `get_memory` ×1 | `memory_and_insights` ×1 | 2 |
| search history for that conversation topic | `get_memory` ×1 | `memory_and_insights` ×1 | 2 |
| what did we discuss in our last session | `get_memory` ×1 | `memory_and_insights` ×1 | 2 |
| what we discussed yesterday was helpful | `NONE` ×1 | `NONE` ×1 | 1 |
| how long is your memory exactly | `get_memory` ×1 | `memory_and_insights` ×1 | 2 |
| link my repository to the project | `CLARIFY` ×1 | `projects_and_repos` ×1 | 2 |
| connect my repository to the project | `CLARIFY` ×1 | `projects_and_repos` ×1 | 2 |
| connect octocat/hello-world to the project | `link_repo` ×1 | `projects_and_repos` ×1 | 2 |
| add octocat/hello-world to the project | `link_repo` ×1 | `projects_and_repos` ×1 | 2 |
| please unlink my repository from this project | `CLARIFY` ×1 | `projects_and_repos` ×1 | 2 |
| please remove my repository from this project | `unlink_repo` ×1 | `projects_and_repos` ×1 | 2 |
| please disconnect my repository from this project | `unlink_repo` ×1 | `projects_and_repos` ×1 | 2 |
| please show my linked repos | `list_repos` ×1 | `projects_and_repos` ×1 | 2 |
| which repo connected to this project should i check | `CLARIFY` ×1 | `projects_and_repos` ×1 | 2 |
| can you show project repositories for this account | `list_repos` ×1 | `projects_and_repos` ×1 | 2 |
| list my repos on github | `list_repos` ×1 | `projects_and_repos` ×1 | 2 |
| show all of my repos | `list_repos` ×1 | `projects_and_repos` ×1 | 2 |
| what's changed since last week | `changes_query` ×1 | `status_and_priorities` ×1 | 2 |
| show me the changes since last monday | `changes_query` ×1 | `status_and_priorities` ×1 | 2 |
| show me everything that's changed | `changes_query` ×1 | `status_and_priorities` ×1 | 2 |
| any changes since the last deploy | `changes_query` ×1 | `status_and_priorities` ×1 | 2 |
| give me the activity since yesterday's standup | `changes_query` ×1 | `status_and_priorities` ×1 | 2 |
| any updates since this morning | `changes_query` ×1 | `status_and_priorities` ×1 | 2 |
| what needs attention right now | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| this project needs my attention today | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| show me what needs the most attention | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| the items that need attention haven't been touched | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| please list the attention items for review | `attention_query` ×1 | `status_and_priorities` ×1 | 2 |
| which repository is my default | `get_default_repo` ×1 | `repo_activity` ×1 | 2 |
| please show my default repository | `get_default_repo` ×1 | `repo_activity` ×1 | 2 |
| my default repository | `get_default_repo` ×1 | `repo_activity` ×1 | 2 |
| what do you know about my work habits | `pull_insights` ×1 | `memory_and_insights` ×1 | 2 |
| tell me what you've learned about my habits | `pull_insights` ×1 | `memory_and_insights` ×1 | 2 |
| what insights do you have about my productivity | `pull_insights` ×1 | `memory_and_insights` ×1 | 2 |
| show me what you've learned about my preferences | `pull_insights` ×1 | `memory_and_insights` ×1 | 2 |
| what patterns have you noticed in my work | `pull_insights` ×1 | `memory_and_insights` ×1 | 2 |
| what have you noticed about my habits lately | `pull_insights` ×1 | `memory_and_insights` ×1 | 2 |
| what branch am i on right now | `local_git_status_query` ×1 | `repo_activity` ×1 | 2 |
| which branch are we on at the moment | `local_git_status_query` ×1 | `repo_activity` ×1 | 2 |
| can you tell me the current branch | `local_git_status_query` ×1 | `repo_activity` ×1 | 2 |
| what's the working tree status | `local_git_status_query` ×1 | `repo_activity` ×1 | 2 |
| are there any uncommitted changes | `local_git_status_query` ×1 | `repo_activity` ×1 | 2 |
| do we have a dirty working tree | `local_git_status_query` ×1 | `repo_activity` ×1 | 2 |
| are we ahead of origin right now | `local_git_status_query` ×1 | `repo_activity` ×1 | 2 |
| are we behind upstream at all | `local_git_status_query` ×1 | `repo_activity` ×1 | 2 |
| do we have any unpushed commits | `local_git_status_query` ×1 | `repo_activity` ×1 | 2 |
| can you show the local git status | `local_git_status_query` ×1 | `repo_activity` ×1 | 2 |
| please run git status for me | `local_git_status_query` ×1 | `repo_activity` ×1 | 2 |
| show me my productivity report | `productivity` ×1 | `status_and_priorities` ×1 | 2 |
| can you share my productivity metrics | `productivity` ×1 | `status_and_priorities` ×1 | 2 |
| i'd like to check my productivity this week | `productivity` ×1 | `status_and_priorities` ×1 | 2 |
| what have we created so far | `list_projects` ×1 | `projects_and_repos` ×1 | 2 |
| what did we make earlier | `CLARIFY` ×1 | `memory_and_insights` ×1 | 2 |
| what did i create this session | `session_activity_query` ×1 | `memory_and_insights` ×1 | 2 |
| what did we do this session | `session_activity_query` ×1 | `memory_and_insights` ×1 | 2 |
| what issues did we open during the call | `list_issues` ×1 | `issues` ×1 | 2 |
| Write a short update for the client CEO on where we are with the Piper Morgan alpha testing. | `write_stakeholder_update` ×1 | `documents_and_writing` ×1 | 2 |
| help me setup my projects | `CLARIFY` ×1 | `projects_and_repos` ×1 | 2 |
| help me setup projects | `CLARIFY` ×1 | `projects_and_repos` ×1 | 2 |
| How do I setup my projects? | `get_contextual_guidance` ×1 | `assistant_and_conversation` ×1 | 2 |
| setup my projects | `CLARIFY` ×1 | `projects_and_repos` ×1 | 2 |
| help me set up my portfolio | `manage_portfolio` ×1 | `projects_and_repos` ×1 | 2 |
| Help me set up my projects | `CLARIFY` ×1 | `projects_and_repos` ×1 | 2 |
| When did I complete the API migration? | `check_completion_status` ×1 | `status_and_priorities` ×1 | 2 |
| When did I complete the migration? | `check_completion_status` ×1 | `status_and_priorities` ×1 | 2 |
| When did we launch the beta? | `CLARIFY` ×1 | `repo_activity` ×1 | 2 |
| Who are you and what do you do? | `get_identity` ×1 | `assistant_and_conversation` ×1 | 2 |
| What's your name? | `get_identity` ×1 | `assistant_and_conversation` ×1 | 2 |
| what date did I finish the onboarding project | `check_completion_status` ×1 | `status_and_priorities` ×1 | 2 |
| show me when we shipped the API | `shipped_this_week` ×1 | `repo_activity` ×1 | 2 |
| when was the migration completed | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| how long ago did we ship the dashboard | `shipped_this_week` ×1 | `repo_activity` ×1 | 2 |
| show my archived projects | `list_archived_projects` ×1 | `projects_and_repos` ×1 | 2 |
| show archived projects | `list_archived_projects` ×1 | `projects_and_repos` ×1 | 2 |
| view my archived projects | `list_archived_projects` ×1 | `projects_and_repos` ×1 | 2 |
| show my projects | `list_projects` ×1 | `projects_and_repos` ×1 | 2 |
| list my archived projects (show all names) | `list_archived_projects` ×1 | `projects_and_repos` ×1 | 2 |
| What date did I finish the database project? | `get_memory` ×1 | `memory_and_insights` ×1 | 2 |
| How long ago did I finish the redesign? | `get_memory` ×1 | `memory_and_insights` ×1 | 2 |
| When was the auth refactor shipped? | `shipped_this_week` ×1 | `repo_activity` ×1 | 2 |
| list my archived projects and summarize my current work | `PLAN[list_archived_projects→show_standup]` ×1 | `projects_and_repos,status_and_priorities` ×1 | 3 |
| list all projects | `list_projects` ×1 | `projects_and_repos` ×1 | 2 |
| view my projects | `list_projects` ×1 | `projects_and_repos` ×1 | 2 |
| summarize my current work and I need the archived list too | `PLAN[show_standup→list_archived_projects]` ×1 | `status_and_priorities,projects_and_repos` ×1 | 3 |
| Where did you get that from? | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| How did you know about that? | `CLARIFY` ×1 | `memory_and_insights` ×1 | 2 |
| What made you mention the priority? | `explain_suggestion` ×1 | `memory_and_insights` ×1 | 2 |
| How do you know about my schedule? | `CLARIFY` ×1 | `memory_and_insights` ×1 | 2 |
| Why is that on your list? | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| Based on what? | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| What's that based on? | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| hide the project Beta | `archive_project` ×1 | `projects_and_repos` ×1 | 2 |
| put the old project away | `CLARIFY` ×1 | `projects_and_repos` ×1 | 2 |
| delete my project Gamma | `CLARIFY` ×1 | `projects_and_repos` ×1 | 2 |
| remove the project Delta | `archive_project` ×1 | `projects_and_repos` ×1 | 2 |
| get rid of my test project | `archive_project` ×1 | `projects_and_repos` ×1 | 2 |
| restore project Epsilon | `restore_project` ×1 | `projects_and_repos` ×1 | 2 |
| unarchive the old project | `restore_project` ×1 | `projects_and_repos` ×1 | 2 |
| bring back my archived project | `restore_project` ×1 | `projects_and_repos` ×1 | 2 |
| search projects for budget | `search_projects` ×1 | `projects_and_repos` ×1 | 2 |
| find project deadline | `CLARIFY` ×1 | `status_and_priorities` ×1 | 2 |
| add a new project | `add_project` ×1 | `projects_and_repos` ×1 | 2 |
| I'd like to start a new project | `add_project` ×1 | `projects_and_repos` ×1 | 2 |
| what's your name | `get_identity` ×1 | `assistant_and_conversation` ×1 | 2 |
| your role | `get_identity` ×1 | `assistant_and_conversation` ×1 | 2 |
| what do you do | `get_identity` ×1 | `assistant_and_conversation` ×1 | 2 |
| tell me about yourself | `get_identity` ×1 | `assistant_and_conversation` ×1 | 2 |
| introduce yourself | `get_identity` ×1 | `assistant_and_conversation` ×1 | 2 |
| edit the meeting notes document | `update_document` ×1 | `documents_and_writing` ×1 | 2 |
| modify the status document | `update_document` ×1 | `documents_and_writing` ×1 | 2 |
| change the spec doc | `CLARIFY` ×1 | `documents_and_writing` ×1 | 2 |
| add to the notes document new items | `update_document` ×1 | `documents_and_writing` ×1 | 2 |
| append to the log doc | `update_document` ×1 | `documents_and_writing` ×1 | 2 |
| update project plan with new deadline | `update_document` ×1 | `documents_and_writing` ×1 | 2 |
| edit the report with corrections | `update_document` ×1 | `documents_and_writing` ×1 | 2 |
| modify the onboarding checklist with the new steps | `update_document` ×1 | `documents_and_writing` ×1 | 2 |
| change the title of issue 108 to test new regressions | `update_issue` ×1 | `issues` ×1 | 2 |
| Tell me about Notion | `NONE` ×1 | `NONE` ×1 | 1 |
| How does the Slack integration work? | `get_feature_info` ×1 | `assistant_and_conversation` ×1 | 2 |
| What is the Notion integration? | `get_feature_info` ×1 | `assistant_and_conversation` ×1 | 2 |
| I'd like to learn more about the GitHub integration. | `get_feature_info` ×1 | `assistant_and_conversation` ×1 | 2 |
| Can you give me information about the Slack integration? | `get_feature_info` ×1 | `assistant_and_conversation` ×1 | 2 |
| Draft a status update for the board | `write_stakeholder_update` ×1 | `documents_and_writing` ×1 | 2 |
| Write something to send to Jake about the beta timeline | `write_stakeholder_update` ×1 | `documents_and_writing` ×1 | 2 |
| I need a stakeholder update on the alpha program | `write_stakeholder_update` ×1 | `documents_and_writing` ×1 | 2 |
| finish todo about deployment | `complete_todo` ×1 | `todos_and_reminders` ×1 | 2 |
| Can we just mark done here? | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| complete todo for the deploy checklist | `complete_todo` ×1 | `todos_and_reminders` ×1 | 2 |
| use mediajunkie/piper-morgan-product as my default repo | `set_default_repo` ×1 | `repo_activity` ×1 | 2 |
| make mediajunkie/piper-morgan-product my default repo | `set_default_repo` ×1 | `repo_activity` ×1 | 2 |
| My default repo should be mediajunkie/piper-morgan-product. | `set_default_repo` ×1 | `repo_activity` ×1 | 2 |
| Actually, change the title to 'Implement full-text search across nav and global search bar' | `update_issue` ×1 | `issues` ×1 | 2 |
| Also we should call it out in the release notes | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| Create a GitHub issue: "Served check colon quotes" in dinp-machine/piper-test-activity | `create_issue` ×1 | `issues` ×1 | 2 |
| Create a GitHub issue: "Served check bare form" | `create_issue` ×1 | `issues` ×1 | 2 |
| Show me that issue. | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| Update issue #123 | `CLARIFY` ×1 | `issues` ×1 | 2 |
| Find time for a 1:1 with the team lead | `CLARIFY` ×1 | `calendar_and_time` ×1 | 2 |
| Analyze this document | `CLARIFY` ×1 | `documents_and_writing` ×1 | 2 |
| What does this document say? | `CLARIFY` ×1 | `CLARIFY` ×1 | 1 |
| Summarize this file | `summarize_document` ×1 | `documents_and_writing` ×1 | 2 |
| Analyze the document called PRD Writing Guidelines | `analyze_document` ×1 | `documents_and_writing` ×1 | 2 |

## Group confusion (expected group × picked stage-1 group)

| expected | picked | count |
|---|---|---|
| status_and_priorities | status_and_priorities | 97 |
| calendar_and_time | calendar_and_time | 74 |
| n/a | repo_activity | 44 |
| projects_and_repos | projects_and_repos | 44 |
| todos_and_reminders | todos_and_reminders | 44 |
| assistant_and_conversation | assistant_and_conversation | 43 |
| n/a | issues | 28 |
| memory_and_insights | memory_and_insights | 26 |
| repo_activity | repo_activity | 21 |
| n/a | documents_and_writing | 12 |
| n/a | projects_and_repos | 11 |
| documents_and_writing | documents_and_writing | 10 |
| floor | calendar_and_time | 10 |
| n/a | status_and_priorities | 10 |
| assistant_and_conversation | projects_and_repos | 9 |
| floor | CLARIFY | 9 |
| floor | status_and_priorities | 9 |
| n/a | assistant_and_conversation | 9 |
| n/a | todos_and_reminders | 9 |
| assistant_and_conversation | CLARIFY | 8 |
| assistant_and_conversation | NONE | 7 |
| issues | issues | 7 |
| n/a | CLARIFY | 7 |
| n/a | memory_and_insights | 6 |
| status_and_priorities | CLARIFY | 6 |
| status_and_priorities | repo_activity | 5 |
| todos_and_reminders | CLARIFY | 5 |
| assistant_and_conversation | memory_and_insights | 4 |
| floor | issues | 4 |
| memory_and_insights | CLARIFY | 4 |
| n/a | calendar_and_time | 4 |
| n/a | NONE | 3 |
| plan | status_and_priorities | 3 |
| status_and_priorities | memory_and_insights | 3 |
| documents_and_writing | CLARIFY | 2 |
| floor | projects_and_repos | 2 |
| memory_and_insights | status_and_priorities | 2 |
| assistant_and_conversation | status_and_priorities | 1 |
| calendar_and_time | status_and_priorities | 1 |
| documents_and_writing | status_and_priorities | 1 |
| floor | memory_and_insights | 1 |
| floor | repo_activity | 1 |
| memory_and_insights | NONE | 1 |
| memory_and_insights | issues | 1 |
| memory_and_insights | projects_and_repos | 1 |
| plan | CLARIFY | 1 |
| plan | projects_and_repos | 1 |
| plan | todos_and_reminders | 1 |
| projects_and_repos | status_and_priorities | 1 |
| status_and_priorities | documents_and_writing | 1 |
| todos_and_reminders | issues | 1 |
| todos_and_reminders | status_and_priorities | 1 |

Agreement: 366/616
