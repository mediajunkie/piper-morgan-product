# Isolation on the corpus set: 616 decisions per arm

## d1 (edited op's group: calendar_and_time): moved 8 / 616; inside the group 5; OUTSIDE 3
   OUTSIDE  'what are my priorities?': main get_top_priority [status_and_priorities] -> d1 prioritize [status_and_priorities]
   OUTSIDE  'please remove my repository from this project': main unlink_repo [projects_and_repos] -> d1 CLARIFY [projects_and_repos]
   OUTSIDE  'summarize my current work and I need the archived list too': main PLAN[show_standup→list_archived_projects] [status_and_priorities,projects_and_repos] -> d1 PLAN[get_project_status→list_archived_projects] [status_and_priorities,projects_and_repos]
   inside   'show me my agenda': main meeting_time [calendar_and_time] -> d1 week_calendar [calendar_and_time]
   inside   'how much time in meetings do I have': main meeting_time [calendar_and_time] -> d1 CLARIFY [calendar_and_time]
   inside   'pull up my schedule': main CLARIFY [calendar_and_time] -> d1 week_calendar [calendar_and_time]
   inside   'what are the upcoming meetings': main recurring_meetings [calendar_and_time] -> d1 week_calendar [calendar_and_time]
   inside   'what are the upcoming events': main CLARIFY [calendar_and_time] -> d1 week_calendar [calendar_and_time]

## d2 (edited op's group: status_and_priorities): moved 7 / 616; inside the group 6; OUTSIDE 1
   OUTSIDE  'list my archived projects and summarize my current work': main PLAN[list_archived_projects→get_project_status] [projects_and_repos,status_and_priorities] -> d2 PLAN[list_archived_projects→show_standup] [projects_and_repos,status_and_priorities]
   inside   'what are my priorities?': main get_top_priority [status_and_priorities] -> d2 prioritize [status_and_priorities]
   inside   "what's most important right now": main get_top_priority [status_and_priorities] -> d2 attention_query [status_and_priorities]
   inside   'what are my focus areas this sprint': main get_project_status [status_and_priorities] -> d2 show_standup [status_and_priorities]
   inside   "let's focus on today's priorities": main get_top_priority [status_and_priorities] -> d2 attention_query [status_and_priorities]
   inside   "what's the most critical thing": main get_top_priority [status_and_priorities] -> d2 attention_query [status_and_priorities]
   inside   "what's my work status": main get_project_status [status_and_priorities] -> d2 show_standup [status_and_priorities]

## d3 (edited op's group: status_and_priorities): moved 5 / 616; inside the group 5; OUTSIDE 0
   inside   'what are my priorities?': main get_top_priority [status_and_priorities] -> d3 prioritize [status_and_priorities]
   inside   "let's focus on today's priorities": main get_top_priority [status_and_priorities] -> d3 attention_query [status_and_priorities]
   inside   'time spent in meetings is high lately': main analyze_data [status_and_priorities] -> d3 productivity [status_and_priorities]
   inside   'what is my most important work today': main attention_query [status_and_priorities] -> d3 get_top_priority [status_and_priorities]
   inside   'summarize my current work and I need the archived list too': main PLAN[show_standup→list_archived_projects] [status_and_priorities,projects_and_repos] -> d3 PLAN[get_project_status→list_archived_projects] [status_and_priorities,projects_and_repos]

