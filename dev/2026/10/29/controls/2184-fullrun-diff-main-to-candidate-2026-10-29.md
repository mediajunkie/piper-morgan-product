shared asserted rows: 550 · old MATCH 494 · new MATCH 490 · net -4
only in old: 0 · only in new: 2

## IMPROVED (→MATCH) (3)
| category | phrase | expected | old route | new route | old→new verdict |
|---|---|---|---|---|---|
| QUERY | this project needs my attention today | action:attention_query | `NONE` @0.95 | `attention_query` @0.85 | MISMATCH→MATCH |
| QUERY | what did we make earlier | action:session_activity_query | `CLARIFY` @0.4 | `session_activity_query` @0.85 | MISMATCH→MATCH |
| STATUS | tasks I'm actively working on | action:list_todos_query | `attention_query` @0.72 | `list_todos_query` @0.85 | MISMATCH→MATCH |

## WORSENED (MATCH→) (7)
| category | phrase | expected | old route | new route | old→new verdict |
|---|---|---|---|---|---|
| EXECUTION | modify the onboarding checklist with the new steps | action:update_document_query | `update_document` @0.72 | `CLARIFY` @0.4 | MATCH→MISMATCH |
| EXECUTION | modify the status document | action:update_document_query | `update_document` @0.85 | `CLARIFY` @0.4 | MATCH→MISMATCH |
| PORTFOLIO | bring back my archived project | action:restore_project | `restore_project` @0.72 | `CLARIFY` @0.6 | MATCH→MISMATCH |
| PRIORITY | where should my focus be today | action:attention_query | `attention_query` @0.92 | `get_top_priority` @0.95 | MATCH→MISMATCH |
| QUERY | Update issue #123 | action:update_issue | `update_issue` @0.6 | `CLARIFY` @0.4 | MATCH→MISMATCH |
| STATUS | show today's assignments | action:get_project_status | `NONE` @0.85 | `attention_query` @0.75 | MATCH→MISMATCH |
| TEMPORAL | show all events | action:week_calendar | `week_calendar` @0.72 | `CLARIFY` @0.6 | MATCH→MISMATCH |

## ROUTE CHANGED, verdict unchanged (4)
| category | phrase | expected | old route | new route | old→new verdict |
|---|---|---|---|---|---|
| PROVENANCE | How did you know about that? | action:explain_suggestion | `CLARIFY` @0.4 | `explain_trust` @0.85 | MISMATCH→MISMATCH |
| QUERY | any update on the next milestone | action:get_project_status | `get_project_status` @0.85 | `list_milestones` @0.72 | MATCH→MATCH |
| STATUS | can you summarize my current work | action:get_project_status | `NONE` @0.85 | `CLARIFY` @0.5 | MATCH→MATCH |
| STATUS | what's my current project | action:get_project_status | `CLARIFY` @0.6 | `NONE` @0.85 | MATCH→MATCH |

## only in new: QUERY::how is the next milestone going?, QUERY::what's the progress on the MVP milestone?
