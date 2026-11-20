# Classifier batch — p2-cand-A

Parsed 2026-11-20 21:11Z · 60 requests · 0 ERROR or UNPARSED · served: anthropic:claude-sonnet-4-6 (60/60)

| phrase | outcome (count) | raw action (count) |
|---|---|---|
| delete that reminder | `execution/delete_todo` ×4, `execution/delete_reminder` ×2 | delete_reminder ×6 |
| delete a reminder | `execution/delete_todo` ×3, `execution/delete_reminder` ×3 | delete_reminder ×6 |
| use the interview from now on | `conversation/unregistered` ×6 | clarification_needed ×6 |
| does my calendar overlap with hers | `temporal/unregistered` ×4, `temporal/meeting_time` ×2 | calendar_overlap_check ×3, meeting_time ×2, check_calendar_overlap ×1 |
| any upcoming milestones for this project | `temporal/unregistered` ×3, `temporal/meeting_time` ×3 | get_milestones ×3, meeting_time ×3 |
| link my repository to the project | `execution/link_repository` ×4, `execution/link_repository_to_project` ×2 | link_repository ×4, link_repository_to_project ×2 |
| which repo connected to this project should i check | `guidance/unregistered` ×6 | provide_guidance ×6 |
| Can we just mark done here? | `execution/complete_todo` ×6 | mark_done ×6 |
| Show me that issue. | `query/get_issue` ×6 | get_issue ×6 |
| make clear mark them done | `execution/complete_todo` ×6 | mark_done ×6 |
