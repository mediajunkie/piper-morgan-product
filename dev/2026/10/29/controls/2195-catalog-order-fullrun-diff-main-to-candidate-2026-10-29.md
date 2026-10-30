shared asserted rows: 550 · old MATCH 495 · new MATCH 477 · net -18
only in old: 0 · only in new: 0

## IMPROVED (→MATCH) (11)
| category | phrase | expected | old route | new route | old→new verdict |
|---|---|---|---|---|---|
| ANALYSIS | What does this document say? | action:analyze_document | `CLARIFY` @0.4 | `analyze_document` @0.7 | MISMATCH→MATCH |
| EXECUTION | edit the meeting notes document | action:update_document_query | `CLARIFY` @0.4 | `update_document` @0.85 | MISMATCH→MATCH |
| GUIDANCE | advise me on this decision | action:get_contextual_guidance | `CLARIFY` @0.4 | `get_contextual_guidance` @0.7 | MISMATCH→MATCH |
| PORTFOLIO | edit my project description | floor | `update_document` @0.85 | `CLARIFY` @0.6 | MISMATCH→MATCH |
| PRIORITY | let's focus on today's priorities | action:get_top_priority | `attention_query` @0.85 | `get_top_priority` @0.85 | MISMATCH→MATCH |
| PRIORITY | show priorities for this sprint | floor | `prioritize` @0.85 | `get_top_priority` @0.85 | MISMATCH→MATCH |
| PROVENANCE | Where did you get that from? | action:explain_suggestion | `CLARIFY` @0.4 | `explain_suggestion` @0.6 | MISMATCH→MATCH |
| QUERY | this project needs my attention today | action:attention_query | `NONE` @0.95 | `attention_query` @0.85 | MISMATCH→MATCH |
| STATUS | any upcoming milestones for this project | action:list_milestones | `CLARIFY` @0.4 | `list_milestones` @0.85 | MISMATCH→MATCH |
| STATUS | tasks I'm actively working on | action:list_todos_query | `attention_query` @0.72 | `list_todos_query` @0.85 | MISMATCH→MATCH |
| STATUS | what's the project landscape | action:get_project_status | `list_projects` @0.85 | `get_project_status` @0.72 | MISMATCH→MATCH |

## WORSENED (MATCH→) (29)
| category | phrase | expected | old route | new route | old→new verdict |
|---|---|---|---|---|---|
| DISCOVERY | open the help menu | action:get_capabilities | `get_capabilities` @0.95 | `NONE` @0.95 | MATCH→MISMATCH |
| DISCOVERY | what are your limits as an assistant | action:get_capabilities | `get_capabilities` @0.92 | `explain_trust` @0.92 | MATCH→MISMATCH |
| EXECUTION | Actually, change the title to 'Implement full-text sear | action:update_issue | `update_issue` @0.85 | `CLARIFY` @0.4 | MATCH→MISMATCH |
| EXECUTION | modify the onboarding checklist with the new steps | action:update_document_query | `update_document` @0.72 | `CLARIFY` @0.4 | MATCH→MISMATCH |
| EXECUTION | modify the status document | action:update_document_query | `update_document` @0.72 | `CLARIFY` @0.4 | MATCH→MISMATCH |
| GUIDANCE | just getting started here | action:greeting | `greeting` @0.85 | `NONE` @0.95 | MATCH→MISMATCH |
| GUIDANCE | where should I focus this week | action:get_top_priority | `get_top_priority` @0.85 | `get_contextual_guidance` @0.72 | MATCH→MISMATCH |
| MEMORY | what did we discuss in our last session | action:get_memory | `get_memory` @0.92 | `NONE` @0.95 | MATCH→MISMATCH |
| PORTFOLIO | update my project name to Atlas | floor | `CLARIFY` @0.4 | `manage_portfolio` @0.85 | MATCH→MISMATCH |
| PRIORITY | mark this as priority one | action:prioritize | `prioritize` @0.85 | `CLARIFY` @0.4 | MATCH→MISMATCH |
| PRIORITY | what's the most critical thing | action:attention_query | `attention_query` @0.92 | `get_top_priority` @0.92 | MATCH→MISMATCH |
| PRIORITY | where should my focus be today | action:attention_query | `attention_query` @0.92 | `get_top_priority` @0.92 | MATCH→MISMATCH |
| QUERY | Update issue #123 | action:update_issue | `update_issue` @0.6 | `CLARIFY` @0.4 | MATCH→MISMATCH |
| QUERY | are we behind upstream at all | action:local_git_status_query | `local_git_status_query` @0.72 | `CLARIFY` @0.4 | MATCH→MISMATCH |
| QUERY | list all pull requests from this sprint | action:list_prs_query | `list_prs` @0.85 | `CLARIFY` @0.4 | MATCH→MISMATCH |
| QUERY | milestones due this month | action:list_milestones_query | `list_milestones` @0.95 | `NONE` @0.85 | MATCH→MISMATCH |
| QUERY | what did we make earlier | action:session_activity_query | `session_activity_query` @0.85 | `CLARIFY` @0.6 | MATCH→MISMATCH |
| QUERY | what meetings do i have | action:meeting_time | `meeting_time` @0.85 | `CLARIFY` @0.6 | MATCH→MISMATCH |
| STATUS | show me my portfolio | action:manage_portfolio | `manage_portfolio` @0.95 | `list_projects` @0.95 | MATCH→MISMATCH |
| TEMPORAL | I need to remember to submit my timesheet | action:create_todo | `create_todo` @0.95 | `create_reminder` @0.92 | MATCH→MISMATCH |
| TEMPORAL | show all appointments | action:week_calendar | `week_calendar` @0.85 | `NONE` @0.85 | MATCH→MISMATCH |
| TEMPORAL | show all events | action:week_calendar | `week_calendar` @0.72 | `CLARIFY` @0.6 | MATCH→MISMATCH |
| TEMPORAL | walk me through my events | action:week_calendar | `week_calendar` @0.85 | `CLARIFY` @0.6 | MATCH→MISMATCH |
| TEMPORAL | what's my available time | action:week_calendar | `week_calendar` @0.85 | `CLARIFY` @0.6 | MATCH→MISMATCH |
| TEMPORAL | when am i free | action:week_calendar | `week_calendar` @0.85 | `CLARIFY` @0.6 | MATCH→MISMATCH |
| TEMPORAL | when do I have free time | action:week_calendar | `week_calendar` @0.85 | `CLARIFY` @0.6 | MATCH→MISMATCH |
| TEMPORAL | when is my team meeting | action:meeting_time | `meeting_time` @0.85 | `CLARIFY` @0.4 | MATCH→MISMATCH |
| TRUST | how do we work together on this project | action:explain_trust | `explain_trust` @0.85 | `get_contextual_guidance` @0.85 | MATCH→MISMATCH |
| TRUST | i didn't ask you to do that | action:explain_trust | `explain_trust` @0.85 | `NONE` @0.95 | MATCH→MISMATCH |

## ROUTE CHANGED, verdict unchanged (14)
| category | phrase | expected | old route | new route | old→new verdict |
|---|---|---|---|---|---|
| PRIORITY | what are the key priorities this quarter | action:get_top_priority | `strategic_planning` @0.85 | `get_contextual_guidance` @0.72 | MISMATCH→MISMATCH |
| PRIORITY | what matters most this week | action:get_top_priority | `attention_query` @0.85 | `week_calendar` @0.65 | MISMATCH→MISMATCH |
| PROVENANCE | How did you know about that? | action:explain_suggestion | `explain_trust` @0.85 | `CLARIFY` @0.4 | MISMATCH→MISMATCH |
| QUERY | find some time for a sync | floor | `NONE` @0.85 | `CLARIFY` @0.4 | MATCH→MATCH |
| QUERY | recurring meetings keep piling up | floor | `NONE` @0.85 | `CLARIFY` @0.55 | MATCH→MATCH |
| STATUS | can you summarize my current work | action:get_project_status | `NONE` @0.85 | `CLARIFY` @0.6 | MATCH→MATCH |
| STATUS | what is my status | action:get_project_status | `get_project_status` @0.7 | `CLARIFY` @0.4 | MATCH→MATCH |
| STATUS | what's my status | action:get_project_status | `get_project_status` @0.85 | `CLARIFY` @0.4 | MATCH→MATCH |
| STATUS | what's my work status | action:get_project_status | `get_project_status` @0.85 | `CLARIFY` @0.6 | MATCH→MATCH |
| STATUS | what's the current status | action:get_project_status | `get_project_status` @0.75 | `CLARIFY` @0.45 | MATCH→MATCH |
| STATUS | what's the task status | action:get_project_status | `get_project_status` @0.7 | `CLARIFY` @0.4 | MATCH→MATCH |
| TEMPORAL | next week's priorities, remind me | plan | `PLAN[week_calendar→create_reminder]` @ | `PLAN[get_top_priority→create_reminder]` @ | MATCH→MATCH |
| TEMPORAL | this month's numbers, remind me | plan | `PLAN[generate_report→create_reminder]` @ | `PLAN[analyze_data→create_reminder]` @ | MATCH→MATCH |
| TEMPORAL | when's my next free slot | action:week_calendar | `meeting_time` @0.92 | `CLARIFY` @0.6 | MISMATCH→MISMATCH |
