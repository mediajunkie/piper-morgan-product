# Router batch — desc-cand

Parsed 2026-10-30 17:39Z · 120 requests · 0 REFUSED (no repair in a batch) · 0 ERROR · served: anthropic:claude-haiku-4-5-20251001 (120/120)

| phrase | routes (count) | confidence range |
|---|---|---|
| give me a project status report | `get_project_status` ×6 | 0.95–0.95 |
| any update on the next milestone | `get_project_status` ×6 | 0.85–0.85 |
| can you summarize my current work | `NONE` ×4, `CLARIFY` ×2 | 0.60–0.85 |
| give me a project overview | `get_project_status` ×6 | 0.85–0.85 |
| I need a status report | `get_project_status` ×6 | 0.85–0.85 |
| where should my focus be today | `attention_query` ×6 | 0.92–0.92 |
| what's the next milestone? | `list_milestones` ×6 | 0.85–0.92 |
| when's the milestone deadline | `CLARIFY` ×5, `list_milestones` ×1 | 0.60–0.85 |
| can you show me issues from just one milestone | `CLARIFY` ×6 | 0.40–0.60 |
| show my open issues in the MVP milestone | `list_issues` ×6 | 0.95–0.95 |
| let's analyze the risk here | `analyze_blockers` ×6 | 0.95–0.95 |
| how are we doing on the next milestone | `get_project_status` ×6 | 0.85–0.85 |
| where do things stand with the project | `get_project_status` ×6 | 0.85–0.85 |
| give me an update on progress | `get_project_status` ×6 | 0.85–0.85 |
| status update please | `get_project_status` ×6 | 0.85–0.85 |
| any news on the project | `get_project_status` ×6 | 0.85–0.85 |
| what's the progress on the MVP milestone | `get_project_status` ×6 | 0.85–0.85 |
| how's the beta launch milestone coming along | `get_project_status` ×6 | 0.92–0.92 |
| any update on my todos | `list_todos_query` ×6 | 0.95–0.95 |
| any updates on issue #123 | `review_issue` ×6 | 0.92–0.95 |
