# Parity, row by row (expected = action:<op> rows only count): flat right & two-stage wrong 88; two-stage right & flat wrong 9

## lost by category: {'TEMPORAL': 18, 'GUIDANCE': 17, 'QUERY': 16, 'STATUS': 11, 'TRUST': 8, 'DISCOVERY': 6, 'EXECUTION': 3, 'PRIORITY': 2, 'ANALYSIS': 2, 'PORTFOLIO': 2, 'IDENTITY': 1, 'MEMORY': 1, 'SYNTHESIS': 1}
## lost by shape: {'stage-2 CLARIFY/OTHER_GROUP': 36, 'stage-1 NONE/CLARIFY': 25, 'wrong group': 23, 'wrong op in right group': 4} 

| category | phrase | expected | flat | two-stage | stage-1 group |
|---|---|---|---|---|---|
| ANALYSIS | Analyze this document | analyze_document | analyze_document | CLARIFY | documents_and_writing |
| ANALYSIS | let's analyze the risk here | analyze_blockers | analyze_blockers | CLARIFY | CLARIFY |
| DISCOVERY | is there a bottleneck analysis available | get_capabilities | get_capabilities | analyze_blockers | status_and_priorities |
| DISCOVERY | open the capabilities menu | get_capabilities | get_capabilities | NONE | NONE |
| DISCOVERY | open the help menu | get_capabilities | get_capabilities | NONE | NONE |
| DISCOVERY | pull up the capability menu | get_capabilities | get_capabilities | NONE | NONE |
| DISCOVERY | show me the menu | get_capabilities | get_capabilities | NONE | NONE |
| DISCOVERY | what are your limits as an assistant | get_capabilities | get_capabilities | explain_trust | assistant_and_conversation |
| EXECUTION | I'm done with the first and the third | complete_todo | complete_todo | CLARIFY | CLARIFY |
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
| GUIDANCE | how do I configure the connector | get_contextual_guidance | get_contextual_guidance | CLARIFY | CLARIFY |
| GUIDANCE | how do I set up the connector | get_contextual_guidance | get_contextual_guidance | CLARIFY | CLARIFY |
| GUIDANCE | how do I setup the connector | get_contextual_guidance | get_contextual_guidance | CLARIFY | CLARIFY |
| GUIDANCE | just getting started here | greeting | greeting | NONE | NONE |
| GUIDANCE | setup my projects | get_contextual_guidance | get_contextual_guidance | CLARIFY | projects_and_repos |
| GUIDANCE | what are the next steps | get_contextual_guidance | get_contextual_guidance | CLARIFY | CLARIFY |
| GUIDANCE | what should I do about this bug | get_contextual_guidance | get_contextual_guidance | CLARIFY | status_and_priorities |
| IDENTITY | who am I? | get_identity | get_identity | pull_insights | memory_and_insights |
| MEMORY | remember when we shipped the last release? | check_completion_status | check_completion_status | get_memory | memory_and_insights |
| PORTFOLIO | add octocat/hello-world to the project | link_repo | link_repo | CLARIFY | projects_and_repos |
| PORTFOLIO | put the old project away | archive_project | archive_project | CLARIFY | projects_and_repos |
| PRIORITY | what should I do first | get_top_priority | get_top_priority | CLARIFY | CLARIFY |
| PRIORITY | what's the most critical thing | attention_query | attention_query | get_top_priority | status_and_priorities |
| QUERY | Tell me about Notion | get_feature_info | get_feature_info | NONE | NONE |
| QUERY | any changes since the last deploy | changes_query | changes_query | analyze_commits | repo_activity |
| QUERY | can we connect my github? | get_contextual_guidance | get_contextual_guidance | CLARIFY | projects_and_repos |
| QUERY | connect my slack | get_contextual_guidance | get_contextual_guidance | NONE | NONE |
| QUERY | do i have any meetings | meeting_time | meeting_time | CLARIFY | calendar_and_time |
| QUERY | do i have meetings | meeting_time | meeting_time | CLARIFY | calendar_and_time |
| QUERY | help me set up github | get_contextual_guidance | get_contextual_guidance | NONE | NONE |
| QUERY | how much time do I spend sitting in meetings | meeting_time | meeting_time | productivity | status_and_priorities |
| QUERY | show me the changes since last monday | changes_query | changes_query | analyze_commits | repo_activity |
| QUERY | what did we make earlier | session_activity_query | session_activity_query | CLARIFY | memory_and_insights |
| QUERY | what do I have next to do | get_top_priority | get_top_priority | list_todos_query | todos_and_reminders |
| QUERY | what have we created so far | session_activity_query | session_activity_query | list_projects | projects_and_repos |
| QUERY | what is on my calendar | week_calendar | week_calendar | CLARIFY | calendar_and_time |
| QUERY | what issues did we open during the call | session_activity_query | session_activity_query | list_issues | issues |
| QUERY | what meetings are coming up | week_calendar | week_calendar | CLARIFY | calendar_and_time |
| QUERY | what meetings do i have | meeting_time | meeting_time | CLARIFY | calendar_and_time |
| STATUS | I need a progress report | generate_report | generate_report | get_project_status | status_and_priorities |
| STATUS | What date did I finish the database project? | check_completion_status | check_completion_status | get_memory | memory_and_insights |
| STATUS | When did we launch the beta? | check_completion_status | check_completion_status | CLARIFY | repo_activity |
| STATUS | When was the auth refactor shipped? | check_completion_status | check_completion_status | shipped_this_week | repo_activity |
| STATUS | how long ago did we ship the dashboard | check_completion_status | check_completion_status | shipped_this_week | repo_activity |
| STATUS | show today's progress | session_activity_query | session_activity_query | show_standup | status_and_priorities |
| STATUS | time for my stand-up | show_standup | show_standup | CLARIFY | calendar_and_time |
| STATUS | what is my status | get_project_status | get_project_status | CLARIFY | status_and_priorities |
| STATUS | what's my progress | get_project_status | get_project_status | CLARIFY | status_and_priorities |
| STATUS | what's my status | get_project_status | get_project_status | CLARIFY | status_and_priorities |
| STATUS | when was the migration completed | check_completion_status | check_completion_status | CLARIFY | repo_activity |
| SYNTHESIS | I need a stakeholder update on the alpha program | write_stakeholder_update | write_stakeholder_update | get_project_status | status_and_priorities |
| TEMPORAL | I need to remember to submit my timesheet | create_todo | create_todo | create_reminder | todos_and_reminders |
| TEMPORAL | a lot happened yesterday | changes_query | changes_query | NONE | NONE |
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
| TRUST | do you trust me with this decision | explain_trust | explain_trust | NONE | NONE |
| TRUST | how do you see our relationship evolving | explain_trust | explain_trust | NONE | NONE |
| TRUST | how much do you trust my judgment | explain_trust | explain_trust | pull_insights | memory_and_insights |
| TRUST | i didn't ask you to do that | explain_trust | explain_trust | NONE | NONE |
| TRUST | what's our relationship like these days | explain_trust | explain_trust | pull_insights | memory_and_insights |
| TRUST | why did you go ahead without asking | explain_trust | explain_trust | CLARIFY | CLARIFY |
| TRUST | why do you always ask me the same thing | explain_trust | explain_trust | pull_insights | memory_and_insights |
| TRUST | why don't you just do it yourself | explain_trust | explain_trust | NONE | NONE |

## gained (two-stage right, flat wrong)
| category | phrase | expected | flat | two-stage | stage-1 group |
|---|---|---|---|---|---|
| EXECUTION | Actually, change the title to 'Implement full-text search across nav and global search bar' | update_issue | CLARIFY | update_issue | issues |
| EXECUTION | delete that reminder | delete_todo | CLARIFY | delete_todo | todos_and_reminders |
| IDENTITY | what do you do | get_identity | get_capabilities | get_identity | assistant_and_conversation |
| MEMORY | search history for that conversation topic | get_memory | CLARIFY | get_memory | memory_and_insights |
| PRIORITY | let's focus on today's priorities | get_top_priority | attention_query | get_top_priority | status_and_priorities |
| PRIORITY | what matters most this week | get_top_priority | attention_query | get_top_priority | status_and_priorities |
| PRIORITY | what's my focus this week | get_top_priority | week_calendar | get_top_priority | status_and_priorities |
| STATUS | any upcoming milestones for this project | list_milestones | CLARIFY | list_milestones | repo_activity |
| STATUS | what's the task status | get_project_status | CLARIFY | get_project_status | status_and_priorities |
