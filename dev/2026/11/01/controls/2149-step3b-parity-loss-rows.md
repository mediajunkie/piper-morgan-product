# Parity, row by row (expected = action:<op> rows only count): flat right & two-stage wrong 76; two-stage right & flat wrong 17

## lost by category: {'TEMPORAL': 18, 'GUIDANCE': 14, 'QUERY': 13, 'STATUS': 11, 'TRUST': 6, 'EXECUTION': 5, 'DISCOVERY': 3, 'ANALYSIS': 2, 'IDENTITY': 1, 'PRIORITY': 1, 'MEMORY': 1, 'PORTFOLIO': 1}
## lost by shape: {'stage-2 CLARIFY/OTHER_GROUP': 34, 'wrong group': 19, 'stage-1 NONE/CLARIFY': 18, 'wrong op in right group': 5} 

| category | phrase | expected | flat | two-stage | stage-1 group |
|---|---|---|---|---|---|
| ANALYSIS | Analyze this document | analyze_document | analyze_document | CLARIFY | documents_and_writing |
| ANALYSIS | let's analyze the risk here | analyze_blockers | analyze_blockers | CLARIFY | CLARIFY |
| DISCOVERY | is there a bottleneck analysis available | get_capabilities | get_capabilities | analyze_blockers | status_and_priorities |
| DISCOVERY | show me the menu | get_capabilities | get_capabilities | CLARIFY | CLARIFY |
| DISCOVERY | what are your limits as an assistant | get_capabilities | get_capabilities | explain_trust | assistant_and_conversation |
| EXECUTION | I'm done with the first and the third | complete_todo | complete_todo | CLARIFY | CLARIFY |
| EXECUTION | Mark the first one complete and leave the second one pe | complete_todo | complete_todo | CLARIFY | ? |
| EXECUTION | add a todo to web test one | create_todo | create_todo | create_todo | todos_and_reminders |
| EXECUTION | complete the last one | complete_todo | complete_todo | CLARIFY | CLARIFY |
| EXECUTION | mark #2 as done | complete_todo | complete_todo | close_issue | issues |
| GUIDANCE | Help me set up my projects | get_contextual_guidance | get_contextual_guidance | CLARIFY | projects_and_repos |
| GUIDANCE | I need to setup my projects | get_contextual_guidance | get_contextual_guidance | manage_portfolio | projects_and_repos |
| GUIDANCE | I want to set up my projects | get_contextual_guidance | get_contextual_guidance | CLARIFY | projects_and_repos |
| GUIDANCE | I'd like to set up my portfolio | get_contextual_guidance | get_contextual_guidance | manage_portfolio | projects_and_repos |
| GUIDANCE | can you help me configure the connector | get_contextual_guidance | get_contextual_guidance | CLARIFY | CLARIFY |
| GUIDANCE | can you help me set up the integration | get_contextual_guidance | get_contextual_guidance | CLARIFY | CLARIFY |
| GUIDANCE | can you help me setup the integration | get_contextual_guidance | get_contextual_guidance | CLARIFY | CLARIFY |
| GUIDANCE | help me set up my portfolio | get_contextual_guidance | get_contextual_guidance | manage_portfolio | projects_and_repos |
| GUIDANCE | help me setup my projects | get_contextual_guidance | get_contextual_guidance | CLARIFY | projects_and_repos |
| GUIDANCE | help me setup projects | get_contextual_guidance | get_contextual_guidance | CLARIFY | projects_and_repos |
| GUIDANCE | just getting started here | greeting | greeting | NONE | NONE |
| GUIDANCE | setup my projects | get_contextual_guidance | get_contextual_guidance | CLARIFY | projects_and_repos |
| GUIDANCE | what are the next steps | get_contextual_guidance | get_contextual_guidance | CLARIFY | CLARIFY |
| GUIDANCE | what should I do about this bug | get_contextual_guidance | get_contextual_guidance | CLARIFY | CLARIFY |
| IDENTITY | who am I? | get_identity | get_identity | pull_insights | memory_and_insights |
| MEMORY | remember when we shipped the last release? | check_completion_status | check_completion_status | get_memory | memory_and_insights |
| PORTFOLIO | put the old project away | archive_project | archive_project | CLARIFY | projects_and_repos |
| PRIORITY | what's the most critical thing | attention_query | attention_query | get_top_priority | status_and_priorities |
| QUERY | Tell me about Notion | get_feature_info | get_feature_info | NONE | NONE |
| QUERY | analyze the file I uploaded | analyze_document | analyze_document | CLARIFY | CLARIFY |
| QUERY | any update on the next milestone | get_project_status | get_project_status | list_milestones | repo_activity |
| QUERY | can we connect my github? | get_contextual_guidance | get_contextual_guidance | CLARIFY | projects_and_repos |
| QUERY | connect my slack | get_contextual_guidance | get_contextual_guidance | NONE | NONE |
| QUERY | do i have any meetings | meeting_time | meeting_time | CLARIFY | calendar_and_time |
| QUERY | do i have meetings | meeting_time | meeting_time | CLARIFY | calendar_and_time |
| QUERY | how much time do I spend sitting in meetings | meeting_time | meeting_time | productivity | status_and_priorities |
| QUERY | what did we make earlier | session_activity_query | session_activity_query | CLARIFY | memory_and_insights |
| QUERY | what have we created so far | session_activity_query | session_activity_query | list_projects | projects_and_repos |
| QUERY | what is on my calendar | week_calendar | week_calendar | CLARIFY | calendar_and_time |
| QUERY | what issues did we open during the call | session_activity_query | session_activity_query | list_issues | issues |
| QUERY | what meetings do i have | meeting_time | meeting_time | CLARIFY | calendar_and_time |
| STATUS | How long ago did I finish the redesign? | check_completion_status | check_completion_status | get_memory | memory_and_insights |
| STATUS | I need a progress report | generate_report | generate_report | CLARIFY | documents_and_writing |
| STATUS | What date did I finish the database project? | check_completion_status | check_completion_status | get_memory | memory_and_insights |
| STATUS | When did we launch the beta? | check_completion_status | check_completion_status | CLARIFY | repo_activity |
| STATUS | When was the auth refactor shipped? | check_completion_status | check_completion_status | shipped_this_week | repo_activity |
| STATUS | how long ago did we ship the dashboard | check_completion_status | check_completion_status | shipped_this_week | repo_activity |
| STATUS | show today's progress | session_activity_query | session_activity_query | show_standup | status_and_priorities |
| STATUS | what is my status | get_project_status | get_project_status | CLARIFY | status_and_priorities |
| STATUS | what's my progress | get_project_status | get_project_status | CLARIFY | status_and_priorities |
| STATUS | what's my status | get_project_status | get_project_status | CLARIFY | status_and_priorities |
| STATUS | when was the migration completed | check_completion_status | check_completion_status | CLARIFY | CLARIFY |
| TEMPORAL | I need to remember to submit my timesheet | create_todo | create_todo | create_reminder | todos_and_reminders |
| TEMPORAL | a lot happened yesterday | changes_query | changes_query | CLARIFY | CLARIFY |
| TEMPORAL | pull up my calendar | week_calendar | week_calendar | CLARIFY | calendar_and_time |
| TEMPORAL | pull up my schedule | week_calendar | week_calendar | CLARIFY | calendar_and_time |
| TEMPORAL | show all appointments | week_calendar | week_calendar | CLARIFY | calendar_and_time |
| TEMPORAL | show all events | week_calendar | week_calendar | CLARIFY | calendar_and_time |
| TEMPORAL | walk me through my appointments | week_calendar | week_calendar | CLARIFY | calendar_and_time |
| TEMPORAL | walk me through my events | week_calendar | week_calendar | CLARIFY | calendar_and_time |
| TEMPORAL | walk me through my meetings | week_calendar | week_calendar | CLARIFY | calendar_and_time |
| TEMPORAL | what are my open slots | week_calendar | week_calendar | CLARIFY | calendar_and_time |
| TEMPORAL | what are the upcoming events | week_calendar | week_calendar | CLARIFY | calendar_and_time |
| TEMPORAL | what are the upcoming meetings | week_calendar | week_calendar | recurring_meetings | calendar_and_time |
| TEMPORAL | what did I work on today | session_activity_query | session_activity_query | changes_query | status_and_priorities |
| TEMPORAL | what's my available time | week_calendar | week_calendar | CLARIFY | calendar_and_time |
| TEMPORAL | when am i free | week_calendar | week_calendar | CLARIFY | calendar_and_time |
| TEMPORAL | when do I have free time | week_calendar | week_calendar | CLARIFY | calendar_and_time |
| TEMPORAL | when is my team meeting | meeting_time | meeting_time | CLARIFY | calendar_and_time |
| TEMPORAL | when's the next event | meeting_time | meeting_time | CLARIFY | calendar_and_time |
| TRUST | how do you see our relationship evolving | explain_trust | explain_trust | NONE | NONE |
| TRUST | i didn't ask you to do that | explain_trust | explain_trust | NONE | NONE |
| TRUST | what's our relationship like these days | explain_trust | explain_trust | pull_insights | memory_and_insights |
| TRUST | why did you go ahead without asking | explain_trust | explain_trust | CLARIFY | memory_and_insights |
| TRUST | why do you always ask me the same thing | explain_trust | explain_trust | pull_insights | memory_and_insights |
| TRUST | why don't you just do it yourself | explain_trust | explain_trust | NONE | NONE |

## gained (two-stage right, flat wrong)

| category | phrase | expected | flat | two-stage | stage-1 group |
|---|---|---|---|---|---|
| ANALYSIS | what's the main obstacle here | analyze_blockers | CLARIFY | analyze_blockers | status_and_priorities |
| EXECUTION | Actually, change the title to 'Implement full-text sear | update_issue | CLARIFY | update_issue | ? |
| EXECUTION | add to the notes document new items | update_document_query | CLARIFY | update_document | documents_and_writing |
| EXECUTION | append to the log doc | update_document_query | CLARIFY | update_document | documents_and_writing |
| EXECUTION | delete that reminder | delete_todo | CLARIFY | delete_todo | todos_and_reminders |
| EXECUTION | edit the meeting notes document | update_document_query | CLARIFY | update_document | documents_and_writing |
| EXECUTION | edit the report with corrections | update_document_query | CLARIFY | update_document | documents_and_writing |
| EXECUTION | please close this issue | close_issue_query | CLARIFY | close_issue | issues |
| EXECUTION | update project plan with new deadline | update_document_query | CLARIFY | update_document | documents_and_writing |
| IDENTITY | what do you do | get_identity | get_capabilities | get_identity | assistant_and_conversation |
| MEMORY | search history for that conversation topic | get_memory | CLARIFY | get_memory | memory_and_insights |
| PRIORITY | let's focus on today's priorities | get_top_priority | attention_query | get_top_priority | status_and_priorities |
| PRIORITY | what matters most this week | get_top_priority | attention_query | get_top_priority | status_and_priorities |
| PRIORITY | what's my focus this week | get_top_priority | week_calendar | get_top_priority | status_and_priorities |
| QUERY | what issues are assigned to me? | list_issues_query | NONE | list_issues | issues |
| STATUS | any upcoming milestones for this project | list_milestones | CLARIFY | list_milestones | repo_activity |
| STATUS | what's the task status | get_project_status | CLARIFY | get_project_status | status_and_priorities |
