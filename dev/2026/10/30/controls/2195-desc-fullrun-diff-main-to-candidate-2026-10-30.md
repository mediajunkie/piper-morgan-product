shared asserted rows: 550 · old MATCH 491 · new MATCH 484 · net -7
only in old: 0 · only in new: 0

## IMPROVED (→MATCH) (1)
| category | phrase | expected | old route | new route | old→new verdict |
|---|---|---|---|---|---|
| EXECUTION | delete that reminder | action:delete_todo | `CLARIFY` @0.4 | `delete_todo` @0.85 | MISMATCH→MATCH |

## WORSENED (MATCH→) (8)
| category | phrase | expected | old route | new route | old→new verdict |
|---|---|---|---|---|---|
| EXECUTION | modify the status document | action:update_document_query | `update_document` @0.72 | `CLARIFY` @0.4 | MATCH→MISMATCH |
| GUIDANCE | just getting started here | action:greeting | `greeting` @0.85 | `NONE` @0.95 | MATCH→MISMATCH |
| PORTFOLIO | add octocat/hello-world to the project | action:link_repo | `link_repo` @0.85 | `CLARIFY` @0.4 | MATCH→MISMATCH |
| PRIORITY | mark this as priority one | action:prioritize | `prioritize` @0.85 | `CLARIFY` @0.4 | MATCH→MISMATCH |
| QUERY | Update issue #123 | action:update_issue | `update_issue` @0.6 | `CLARIFY` @0.5 | MATCH→MISMATCH |
| QUERY | are we behind upstream at all | action:local_git_status_query | `local_git_status_query` @0.72 | `analyze_blockers` @0.72 | MATCH→MISMATCH |
| QUERY | what did we make earlier | action:session_activity_query | `session_activity_query` @0.85 | `CLARIFY` @0.6 | MATCH→MISMATCH |
| STATUS | show me my portfolio | action:manage_portfolio | `manage_portfolio` @0.95 | `list_projects` @0.95 | MATCH→MISMATCH |

## ROUTE CHANGED, verdict unchanged (3)
| category | phrase | expected | old route | new route | old→new verdict |
|---|---|---|---|---|---|
| PROVENANCE | How did you know about that? | action:explain_suggestion | `explain_trust` @0.85 | `CLARIFY` @0.4 | MISMATCH→MISMATCH |
| STATUS | can you summarize my current work | action:get_project_status | `NONE` @0.85 | `CLARIFY` @0.6 | MISMATCH→MISMATCH |
| STATUS | summarize my current work and I need the archived list | plan | `PLAN[session_activity_query→list_archived_projects]` @ | `PLAN[get_project_status→list_archived_projects]` @ | MATCH→MATCH |
