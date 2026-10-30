# Router batch — main

Parsed 2026-10-30 02:35Z · 108 requests · 0 REFUSED (no repair in a batch) · 0 ERROR · served: anthropic:claude-haiku-4-5-20251001 (108/108)

| phrase | routes (count) | confidence range |
|---|---|---|
| give me a project status report | `get_project_status` ×6 | 0.95–0.95 |
| any update on the next milestone | `get_project_status` ×5, `analyze_blockers` ×1 | 0.72–0.72 |
| can you summarize my current work | `NONE` ×6 | 0.85–0.85 |
| give me a project overview | `get_project_status` ×6 | 0.75–0.85 |
| I need a status report | `get_project_status` ×6 | 0.85–0.85 |
| modify the onboarding checklist with the new steps | `update_document` ×6 | 0.72–0.72 |
| modify the status document | `update_document` ×6 | 0.72–0.85 |
| bring back my archived project | `CLARIFY` ×5, `restore_project` ×1 | 0.40–0.72 |
| where should my focus be today | `get_top_priority` ×3, `attention_query` ×3 | 0.92–0.95 |
| Update issue #123 | `update_issue` ×4, `CLARIFY` ×2 | 0.50–0.60 |
| show today's assignments | `NONE` ×6 | 0.85–0.85 |
| show all events | `week_calendar` ×6 | 0.72–0.72 |
| add octocat/hello-world to the project | `link_repo` ×6 | 0.85–0.85 |
| let's analyze the risk here | `analyze_blockers` ×6 | 0.95–0.95 |
| what's the next milestone? | `list_milestones` ×6 | 0.85–0.92 |
| when's the milestone deadline | `CLARIFY` ×6 | 0.40–0.50 |
| can you show me issues from just one milestone? | `CLARIFY` ×6 | 0.40–0.40 |
| show my open issues in the MVP milestone | `list_issues` ×6 | 0.95–0.95 |
