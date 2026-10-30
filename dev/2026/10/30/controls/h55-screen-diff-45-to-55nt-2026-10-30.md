shared asserted rows: 550 · old MATCH 488 · new MATCH 473 · net -15
only in old: 0 · only in new: 0

## IMPROVED (→MATCH) (38)
| category | phrase | expected | old route | new route | old→new verdict |
|---|---|---|---|---|---|
| ANALYSIS | What does this document say? | action:analyze_document | `CLARIFY` @0.4 | `analyze_document` @0.8 | MISMATCH→MATCH |
| ANALYSIS | what's in the way of finishing this | action:analyze_blockers | `CLARIFY` @0.4 | `analyze_blockers` @0.85 | MISMATCH→MATCH |
| ANALYSIS | what's the main obstacle here | action:analyze_blockers | `CLARIFY` @0.4 | `analyze_blockers` @0.85 | MISMATCH→MATCH |
| EXECUTION | add to the notes document new items | action:update_document_query | `CLARIFY` @0.4 | `update_document` @0.8 | MISMATCH→MATCH |
| EXECUTION | append to the log doc | action:update_document_query | `CLARIFY` @0.4 | `update_document` @0.8 | MISMATCH→MATCH |
| EXECUTION | change the spec doc | action:update_document_query | `CLARIFY` @0.4 | `update_document` @0.8 | MISMATCH→MATCH |
| EXECUTION | delete a reminder | action:delete_todo | `CLARIFY` @0.6 | `delete_todo` @0.5 | MISMATCH→MATCH |
| EXECUTION | delete that reminder | action:delete_todo | `CLARIFY` @0.4 | `delete_todo` @0.6 | MISMATCH→MATCH |
| EXECUTION | edit the meeting notes document | action:update_document_query | `CLARIFY` @0.4 | `update_document` @0.8 | MISMATCH→MATCH |
| EXECUTION | edit the report with corrections | action:update_document_query | `CLARIFY` @0.4 | `update_document` @0.8 | MISMATCH→MATCH |
| EXECUTION | please close this issue | action:close_issue_query | `CLARIFY` @0.3 | `close_issue` @0.8 | MISMATCH→MATCH |
| EXECUTION | update project plan with new deadline | action:update_document_query | `CLARIFY` @0.4 | `update_document` @0.8 | MISMATCH→MATCH |
| GUIDANCE | advise me on this decision | action:get_contextual_guidance | `CLARIFY` @0.4 | `get_contextual_guidance` @0.7 | MISMATCH→MATCH |
| GUIDANCE | ok that's merged, what now? | action:get_contextual_guidance | `get_top_priority` @0.85 | `get_contextual_guidance` @0.85 | MISMATCH→MATCH |
| MEMORY | search history for that conversation topic | action:get_memory | `CLARIFY` @0.4 | `get_memory` @0.85 | MISMATCH→MATCH |
| PORTFOLIO | bring back my archived project | action:restore_project | `CLARIFY` @0.4 | `restore_project` @0.8 | MISMATCH→MATCH |
| PORTFOLIO | find project deadline | action:search_projects | `CLARIFY` @0.4 | `search_projects` @0.6 | MISMATCH→MATCH |
| PRIORITY | let's focus on today's priorities | action:get_top_priority | `attention_query` @0.85 | `get_top_priority` @0.8 | MISMATCH→MATCH |
| PRIORITY | what are my focus areas this sprint | action:get_top_priority | `get_contextual_guidance` @0.72 | `get_top_priority` @0.6 | MISMATCH→MATCH |
| PRIORITY | what are the key priorities this quarter | action:get_top_priority | `strategic_planning` @0.85 | `get_top_priority` @0.7 | MISMATCH→MATCH |
| PRIORITY | what is my most important work today | action:get_top_priority | `attention_query` @0.92 | `get_top_priority` @0.8 | MISMATCH→MATCH |
| PRIORITY | what matters most this week | action:get_top_priority | `attention_query` @0.85 | `get_top_priority` @0.7 | MISMATCH→MATCH |
| PRIORITY | what's my focus this week | action:get_top_priority | `week_calendar` @0.72 | `get_top_priority` @0.6 | MISMATCH→MATCH |
| PROVENANCE | Based on what? | action:explain_suggestion | `CLARIFY` @0.95 | `explain_suggestion` @0.8 | MISMATCH→MATCH |
| PROVENANCE | How did you know about that? | action:explain_suggestion | `explain_trust` @0.85 | `explain_suggestion` @0.5 | MISMATCH→MATCH |
| PROVENANCE | What's that based on? | action:explain_suggestion | `CLARIFY` @0.5 | `explain_suggestion` @0.7 | MISMATCH→MATCH |
| PROVENANCE | Where did you get that from? | action:explain_suggestion | `CLARIFY` @0.5 | `explain_suggestion` @0.7 | MISMATCH→MATCH |
| PROVENANCE | Why is that on your list? | action:explain_suggestion | `CLARIFY` @0.4 | `explain_suggestion` @0.7 | MISMATCH→MATCH |
| QUERY | Show me that issue. | action:review_issue_query | `CLARIFY` @0.3 | `review_issue` @0.55 | MISMATCH→MATCH |
| QUERY | Update issue #123 | action:update_issue | `CLARIFY` @0.6 | `update_issue` @0.8 | MISMATCH→MATCH |
| QUERY | this project needs my attention today | action:attention_query | `NONE` @0.95 | `attention_query` @0.9 | MISMATCH→MATCH |
| QUERY | what issues are assigned to me? | action:list_issues_query | `NONE` @0.95 | `list_issues` @0.85 | MISMATCH→MATCH |
| STATUS | any upcoming milestones for this project | action:list_milestones | `CLARIFY` @0.4 | `list_milestones` @0.85 | MISMATCH→MATCH |
| STATUS | can you summarize my current work | action:get_project_status | `NONE` @0.85 | `get_project_status` @0.5 | MISMATCH→MATCH |
| STATUS | what am I working on? | floor | `session_activity_query` @0.7 | `get_top_priority` @0.5 | MISMATCH→MATCH |
| STATUS | what's my current project | action:get_project_status | `CLARIFY` @0.6 | `get_project_status` @0.7 | MISMATCH→MATCH |
| STATUS | what's the progress on this | action:get_project_status | `CLARIFY` @0.3 | `get_project_status` @0.55 | MISMATCH→MATCH |
| TEMPORAL | show all events | action:week_calendar | `CLARIFY` @0.6 | `week_calendar` @0.55 | MISMATCH→MATCH |

## WORSENED (MATCH→) (53)
| category | phrase | expected | old route | new route | old→new verdict |
|---|---|---|---|---|---|
| DISCOVERY | is there a bottleneck analysis available | action:get_capabilities | `get_capabilities` @0.92 | `analyze_blockers` @0.82 | MATCH→MISMATCH |
| DISCOVERY | what are your limits as an assistant | action:get_capabilities | `get_capabilities` @0.92 | `explain_trust` @0.7 | MATCH→MISMATCH |
| EXECUTION | Also we should call it out in the release notes | floor | `CLARIFY` @0.4 | `generate_content` @0.35 | MATCH→MISMATCH |
| EXECUTION | I'm done with the first and the third | action:complete_todo | `complete_todo` @0.92 | `REFUSED` @ | MATCH→MISMATCH |
| EXECUTION | close the completed issue | floor | `CLARIFY` @0.4 | `close_issue` @0.72 | MATCH→MISMATCH |
| EXECUTION | mark the PR review todo as done | action:complete_todo | `complete_todo` @0.95 | `complete_todo` @0.93 | MATCH→ARGS_MISMATCH |
| EXECUTION | re-open the old issue | floor | `CLARIFY` @0.4 | `reopen_issue` @0.85 | MATCH→MISMATCH |
| EXECUTION | reopen the old issue | floor | `CLARIFY` @0.4 | `reopen_issue` @0.85 | MATCH→MISMATCH |
| GUIDANCE | I could use some guidance on this | floor | `CLARIFY` @0.4 | `get_contextual_guidance` @0.7 | MATCH→MISMATCH |
| GUIDANCE | do you have a recommendation | floor | `CLARIFY` @0.4 | `get_contextual_guidance` @0.7 | MATCH→MISMATCH |
| GUIDANCE | just getting started here | action:greeting | `greeting` @0.85 | `get_contextual_guidance` @0.8 | MATCH→MISMATCH |
| GUIDANCE | what's your advice here | floor | `CLARIFY` @0.3 | `get_contextual_guidance` @0.85 | MATCH→MISMATCH |
| MEMORY | remember when we shipped the last release? | action:check_completion_status | `check_completion_status` @0.85 | `list_releases` @0.55 | MATCH→MISMATCH |
| PORTFOLIO | update my project name to Atlas | floor | `CLARIFY` @0.4 | `update_document` @0.5 | MATCH→MISMATCH |
| PRIORITY | list priorities for the team | floor | `NONE` @0.85 | `prioritize` @0.6 | MATCH→MISMATCH |
| PRIORITY | not sure what to do about this | floor | `CLARIFY` @0.3 | `get_contextual_guidance` @0.55 | MATCH→MISMATCH |
| PRIORITY | what needs my focus today | action:attention_query | `attention_query` @0.95 | `get_top_priority` @0.7 | MATCH→MISMATCH |
| PRIORITY | what should I focus on today? | action:attention_query | `attention_query` @0.95 | `get_top_priority` @0.8 | MATCH→MISMATCH |
| PRIORITY | what's next for me | action:get_top_priority | `get_top_priority` @0.92 | `get_contextual_guidance` @0.6 | MATCH→MISMATCH |
| PRIORITY | what's the most critical thing | action:attention_query | `attention_query` @0.92 | `get_top_priority` @0.8 | MATCH→MISMATCH |
| PRIORITY | where should my focus be today | action:attention_query | `attention_query` @0.92 | `get_top_priority` @0.8 | MATCH→MISMATCH |
| QUERY | analyze the file I uploaded | action:analyze_document | `analyze_document` @0.95 | `summarize_document` @0.6 | MATCH→MISMATCH |
| QUERY | any update on the next milestone | action:get_project_status | `get_project_status` @0.85 | `list_milestones` @0.6 | MATCH→MISMATCH |
| QUERY | find time for a 1:1 with sarah | floor | `NONE` @0.85 | `get_contextual_guidance` @0.5 | MATCH→MISMATCH |
| QUERY | recurring meetings keep piling up | floor | `NONE` @0.85 | `recurring_meetings` @0.6 | MATCH→MISMATCH |
| QUERY | time spent in meetings is high lately | floor | `NONE` @0.95 | `meeting_time` @0.7 | MATCH→MISMATCH |
| QUERY | what do I have next to do | action:get_top_priority | `get_top_priority` @0.95 | `list_todos_query` @0.85 | MATCH→MISMATCH |
| QUERY | what is on my calendar | action:week_calendar | `week_calendar` @0.85 | `meeting_time` @0.5 | MATCH→MISMATCH |
| QUERY | what issues did we open during the call | action:session_activity_query | `session_activity_query` @0.92 | `list_issues` @0.6 | MATCH→MISMATCH |
| QUERY | what meetings are coming up | action:week_calendar | `week_calendar` @0.85 | `meeting_time` @0.7 | MATCH→MISMATCH |
| QUERY | what meetings do i have | action:meeting_time | `meeting_time` @0.85 | `REFUSED` @ | MATCH→MISMATCH |
| QUERY | what should I do next | action:get_top_priority | `get_top_priority` @0.95 | `get_contextual_guidance` @0.85 | MATCH→MISMATCH |
| QUERY | when's the milestone deadline | floor | `CLARIFY` @0.5 | `list_milestones` @0.8 | MATCH→MISMATCH |
| STATUS | I need a progress report | action:generate_report | `generate_report` @0.85 | `write_stakeholder_update` @0.6 | MATCH→MISMATCH |
| STATUS | give me a progress update | action:get_project_status | `get_project_status` @0.85 | `write_stakeholder_update` @0.55 | MATCH→MISMATCH |
| STATUS | show me my current assignments | floor | `NONE` @0.85 | `attention_query` @0.55 | MATCH→MISMATCH |
| STATUS | show today's progress | action:session_activity_query | `session_activity_query` @0.85 | `show_standup` @0.6 | MATCH→MISMATCH |
| STATUS | what are my assignments | floor | `NONE` @0.95 | `attention_query` @0.55 | MATCH→MISMATCH |
| STATUS | what's assigned to me | floor | `NONE` @0.95 | `list_issues` @0.6 | MATCH→MISMATCH |
| SYNTHESIS | Write something to send to Jake about the beta timeline | action:write_stakeholder_update | `write_stakeholder_update` @0.92 | `generate_content` @0.8 | MATCH→MISMATCH |
| TEMPORAL | I need to remember to submit my timesheet | action:create_todo | `create_todo` @0.95 | `REFUSED` @ | MATCH→MISMATCH |
| TEMPORAL | how long have I been working on this | floor | `CLARIFY` @0.3 | `check_completion_status` @0.45 | MATCH→MISMATCH |
| TEMPORAL | pull up my schedule | action:week_calendar | `week_calendar` @0.85 | `meeting_time` @0.5 | MATCH→MISMATCH |
| TEMPORAL | remind me today's day | action:get_current_time | `get_current_time` @0.85 | `create_reminder` @0.6 | MATCH→MISMATCH |
| TEMPORAL | this month's numbers, remind me | plan | `PLAN[generate_report→create_reminder]` @ | `CLARIFY` @0.5 | MATCH→MISMATCH |
| TEMPORAL | walk me through my events | action:week_calendar | `week_calendar` @0.85 | `meeting_time` @0.5 | MATCH→MISMATCH |
| TEMPORAL | walk me through my meetings | action:week_calendar | `week_calendar` @0.85 | `meeting_time` @0.6 | MATCH→MISMATCH |
| TEMPORAL | what are my open slots | action:week_calendar | `week_calendar` @0.85 | `meeting_time` @0.5 | MATCH→MISMATCH |
| TEMPORAL | what are the upcoming meetings | action:week_calendar | `week_calendar` @0.85 | `meeting_time` @0.7 | MATCH→MISMATCH |
| TEMPORAL | what's my available time | action:week_calendar | `week_calendar` @0.85 | `meeting_time` @0.6 | MATCH→MISMATCH |
| TEMPORAL | when do I have free time | action:week_calendar | `week_calendar` @0.85 | `meeting_time` @0.7 | MATCH→MISMATCH |
| TEMPORAL | when was the last time I worked on this | floor | `CLARIFY` @0.4 | `check_completion_status` @0.6 | MATCH→MISMATCH |
| TRUST | i didn't ask you to do that | action:explain_trust | `explain_trust` @0.85 | `NONE` @0.6 | MATCH→MISMATCH |

## ROUTE CHANGED, verdict unchanged (16)
| category | phrase | expected | old route | new route | old→new verdict |
|---|---|---|---|---|---|
| ANALYSIS | can you run an impact analysis on this change | action:analyze_blockers | `CLARIFY` @0.4 | `NONE` @0.55 | MISMATCH→MISMATCH |
| EXECUTION | modify the onboarding checklist with the new steps | action:update_document_query | `CLARIFY` @0.4 | `REFUSED` @ | MISMATCH→MISMATCH |
| PORTFOLIO | connect my repository to the project | action:manage_repos | `CLARIFY` @0.4 | `get_contextual_guidance` @0.6 | MISMATCH→MISMATCH |
| PORTFOLIO | edit my project description | floor | `update_document` @0.85 | `manage_portfolio` @0.5 | MISMATCH→MISMATCH |
| PRIORITY | this is the highest priority item | action:get_top_priority | `NONE` @0.95 | `CLARIFY` @0.5 | MATCH→MATCH |
| PROVENANCE | How do you know about my schedule? | action:explain_suggestion | `explain_trust` @0.95 | `get_memory` @0.55 | MISMATCH→MISMATCH |
| QUERY | check my calendar for conflicts | floor | `NONE` @0.95 | `CLARIFY` @0.5 | MATCH→MATCH |
| QUERY | show me all project plans | action:search_documents | `NONE` @0.85 | `list_projects` @0.6 | MISMATCH→MISMATCH |
| QUERY | what did we make earlier | action:session_activity_query | `CLARIFY` @0.4 | `get_memory` @0.6 | MISMATCH→MISMATCH |
| STATUS | quick check, working on now? | action:get_project_status | `session_activity_query` @0.85 | `attention_query` @0.6 | MISMATCH→MISMATCH |
| STATUS | show today's assignments | action:get_project_status | `NONE` @0.85 | `attention_query` @0.55 | MISMATCH→MISMATCH |
| STATUS | summarize my current work and I need the archived list | plan | `PLAN[session_activity_query→list_archived_projects]` @ | `PLAN[generate_content→list_archived_projects]` @ | MATCH→MATCH |
| STATUS | tell me what I'm working on | floor | `session_activity_query` @0.7 | `get_project_status` @0.5 | MISMATCH→MISMATCH |
| TEMPORAL | next week's priorities, remind me | plan | `PLAN[week_calendar→create_reminder]` @ | `PLAN[get_top_priority→create_reminder]` @ | MATCH→MATCH |
| TEMPORAL | schedule check for today | action:week_calendar | `CLARIFY` @0.4 | `meeting_time` @0.85 | MISMATCH→MISMATCH |
| TEMPORAL | show the team schedule | floor | `NONE` @0.95 | `CLARIFY` @0.6 | MATCH→MATCH |
