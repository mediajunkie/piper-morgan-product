# Router batch, two-stage — mainx6 · arm d3

Parsed 2026-11-01 18:40Z · 144 decisions · 0 REFUSED (no repair in a batch) · 0 ERROR · served: anthropic:claude-haiku-4-5-20251001 (144/144)

Rendered from: stage 1 tree `8c19ad443c` (144) · stage 2 tree `d7008de4c4` (132) · **stage 1 and stage 2 trees differ: not one arm**

## Stage 1 picks

| pick | count |
|---|---|
| status_and_priorities | 42 |
| repo_activity | 24 |
| projects_and_repos | 18 |
| issues | 18 |
| documents_and_writing | 12 |
| calendar_and_time | 6 |
| CLARIFY | 6 |
| NONE | 6 |
| memory_and_insights | 6 |
| todos_and_reminders | 6 |

Tokens (from the batch results' usage; 0 when a result carries none): stage 1 in 165096 / out 6502 · stage 2 in 82134 / out 7340 · per decision in 1717 / out 96

Stage 2: OTHER_GROUP 6 · CLARIFY 36 (stage-1 error rate, OTHER_GROUP over decisions that reached stage 2: 6/132)

## Decisions

| phrase | routes (count) | stage-1 group (count) | llm_calls |
|---|---|---|---|
| any update on the next milestone | `list_milestones` ×6 | `repo_activity` ×6 | 2, 2, 2, 2, 2, 2 |
| can you summarize my current work | `CLARIFY` ×6 | `status_and_priorities` ×6 | 2, 2, 2, 2, 2, 2 |
| give me a project overview | `get_project_status` ×6 | `status_and_priorities` ×6 | 2, 2, 2, 2, 2, 2 |
| I need a status report | `get_project_status` ×6 | `status_and_priorities` ×6 | 2, 2, 2, 2, 2, 2 |
| modify the onboarding checklist with the new steps | `update_document` ×6 | `documents_and_writing` ×6 | 2, 2, 2, 2, 2, 2 |
| modify the status document | `update_document` ×6 | `documents_and_writing` ×6 | 2, 2, 2, 2, 2, 2 |
| bring back my archived project | `restore_project` ×6 | `projects_and_repos` ×6 | 2, 2, 2, 2, 2, 2 |
| where should my focus be today | `attention_query` ×6 | `status_and_priorities` ×6 | 2, 2, 2, 2, 2, 2 |
| Update issue #123 | `CLARIFY` ×6 | `issues` ×6 | 2, 2, 2, 2, 2, 2 |
| show today's assignments | `CLARIFY` ×6 | `status_and_priorities` ×6 | 2, 2, 2, 2, 2, 2 |
| show all events | `CLARIFY` ×6 | `calendar_and_time` ×6 | 2, 2, 2, 2, 2, 2 |
| add octocat/hello-world to the project | `link_repo` ×6 | `projects_and_repos` ×6 | 2, 2, 2, 2, 2, 2 |
| let's analyze the risk here | `CLARIFY` ×6 | `CLARIFY` ×6 | 1, 1, 1, 1, 1, 1 |
| what's the next milestone? | `list_milestones` ×6 | `repo_activity` ×6 | 2, 2, 2, 2, 2, 2 |
| when's the milestone deadline | `CLARIFY` ×6 | `repo_activity` ×6 | 2, 2, 2, 2, 2, 2 |
| can you show me issues from just one milestone? | `CLARIFY` ×6 | `issues` ×6 | 2, 2, 2, 2, 2, 2 |
| show my open issues in the MVP milestone | `list_issues` ×6 | `issues` ×6 | 2, 2, 2, 2, 2, 2 |
| what's the current status | `get_project_status` ×6 | `status_and_priorities` ×6 | 2, 2, 2, 2, 2, 2 |
| just getting started here | `NONE` ×6 | `NONE` ×6 | 1, 1, 1, 1, 1, 1 |
| what did we make earlier | `CLARIFY` ×6 | `memory_and_insights` ×6 | 2, 2, 2, 2, 2, 2 |
| show me my portfolio | `manage_portfolio` ×6 | `projects_and_repos` ×6 | 2, 2, 2, 2, 2, 2 |
| are we behind upstream at all | `local_git_status_query` ×6 | `repo_activity` ×6 | 2, 2, 2, 2, 2, 2 |
| mark this as priority one | `prioritize` ×6 | `status_and_priorities` ×6 | 2, 2, 2, 2, 2, 2 |
| delete that reminder | `delete_todo` ×6 | `todos_and_reminders` ×6 | 2, 2, 2, 2, 2, 2 |
