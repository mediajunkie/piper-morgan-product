# Classifier batch — p2-cand-B

Parsed 2026-11-20 21:11Z · 66 requests · 0 ERROR or UNPARSED · served: anthropic:claude-sonnet-4-6 (66/66)

| phrase | outcome (count) | raw action (count) |
|---|---|---|
| look at this project/repository. Give me quick feedback and then help me to move forward. | `analysis/analyze_repository` ×5, `analysis/analyze_document` ×1 | analyze_repository ×5, analyze_document ×1 |
| end standup | `execution/complete_todo` ×6 | end_standup ×6 |
| Create a doc from this conversation | `synthesis/unregistered` ×3, `execution/unregistered` ×3 | create_document_from_conversation ×3, create_document ×3 |
| show all events | `temporal/unregistered` ×6 | list_events ×6 |
| what issues are assigned to me? | `query/list_assigned_issues` ×6 | list_assigned_issues ×6 |
| can you summarize my current work | `status/show_standup` ×5, `synthesis/unregistered` ×1 | show_standup ×5, summarize_current_work ×1 |
| I need help understanding something | `guidance/unregistered` ×6 | provide_guidance ×6 |
| what's in the way of finishing this | `status/unregistered` ×6 | get_blockers ×6 |
| can you run an impact analysis on this change | `analysis/unregistered` ×6 | analyze_impact ×6 |
| make clear mark them done | `execution/complete_todo` ×4, `query/set_clear_preference_done` ×2 | mark_done ×3, set_clear_preference_done ×2, mark_items_done ×1 |
| forget my take care of preference | `query/forget_clear_preference` ×6 | forget_clear_preference ×6 |
