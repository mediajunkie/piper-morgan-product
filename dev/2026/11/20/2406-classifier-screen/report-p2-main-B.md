# Classifier batch — p2-main-B

Parsed 2026-11-20 21:11Z · 66 requests · 0 ERROR or UNPARSED · served: anthropic:claude-sonnet-4-6 (66/66)

| phrase | outcome (count) | raw action (count) |
|---|---|---|
| look at this project/repository. Give me quick feedback and then help me to move forward. | `analysis/analyze_repository` ×5, `analysis/analyze_document` ×1 | analyze_repository ×5, analyze_document ×1 |
| end standup | `status/complete_todo` ×6 | end_standup ×6 |
| Create a doc from this conversation | `execution/unregistered` ×6 | create_document ×6 |
| show all events | `query/unregistered` ×6 | list_events ×6 |
| what issues are assigned to me? | `status/unregistered` ×6 | get_assigned_issues ×6 |
| can you summarize my current work | `synthesis/unregistered` ×6 | summarize_current_work ×6 |
| I need help understanding something | `conversation/unregistered` ×4, `guidance/unregistered` ×2 | clarification_needed ×4, provide_guidance ×2 |
| what's in the way of finishing this | `status/unregistered` ×6 | get_blockers ×6 |
| can you run an impact analysis on this change | `analysis/analyze_document` ×6 | analyze_document ×6 |
| make clear mark them done | `query/set_clear_preference_done` ×6 | set_clear_preference_done ×6 |
| forget my take care of preference | `query/forget_clear_preference` ×5, `query/forget_take_care_of_preference` ×1 | forget_clear_preference ×5, forget_take_care_of_preference ×1 |
