# Classifier batch — p2-main-A

Parsed 2026-11-20 21:11Z · 60 requests · 0 ERROR or UNPARSED · served: anthropic:claude-sonnet-4-6 (60/60)

| phrase | outcome (count) | raw action (count) |
|---|---|---|
| delete that reminder | `execution/delete_reminder` ×6 | delete_reminder ×6 |
| delete a reminder | `execution/delete_reminder` ×6 | delete_reminder ×6 |
| use the interview from now on | `execution/unregistered` ×6 | set_active_document ×6 |
| does my calendar overlap with hers | `temporal/unregistered` ×6 | calendar_overlap_check ×6 |
| any upcoming milestones for this project | `temporal/unregistered` ×4, `temporal/meeting_time` ×2 | get_milestones ×4, meeting_time ×2 |
| link my repository to the project | `execution/link_repository` ×6 | link_repository ×6 |
| which repo connected to this project should i check | `query/unregistered` ×6 | get_connected_repo ×6 |
| Can we just mark done here? | `conversation/unregistered` ×4, `execution/complete_todo` ×2 | clarification_needed ×4, mark_done ×2 |
| Show me that issue. | `query/unregistered` ×3, `query/get_issue` ×3 | get_github_issue ×3, get_issue ×3 |
| make clear mark them done | `query/set_clear_preference_done` ×5, `execution/complete_todo` ×1 | set_clear_preference_done ×5, mark_done ×1 |
