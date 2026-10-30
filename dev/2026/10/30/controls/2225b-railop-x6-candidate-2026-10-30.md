# Router batch — sb-cand-x6

Parsed 2026-10-30 23:55Z · 78 requests · 0 REFUSED (no repair in a batch) · 0 ERROR · served: anthropic:claude-haiku-4-5-20251001 (78/78)

| phrase | routes (count) | confidence range |
|---|---|---|
| Set my default GitHub repository to owner/name | `set_default_github_repo` ×6 | 0.95–0.95 |
| make dinp-machine/piper-test-activity my default repo | `set_default_repo` ×6 | 0.95–0.99 |
| change my default GitHub repository to acme/widgets | `set_default_github_repo` ×6 | 0.99–0.99 |
| what's my default repository? | `get_default_repo` ×6 | 0.99–0.99 |
| add octocat/hello-world to the project | `link_repo` ×6 | 0.75–0.75 |
| what's the next milestone? | `list_milestones` ×6 | 0.85–0.92 |
| show my open issues in the MVP milestone | `list_issues` ×6 | 0.95–0.95 |
| when's the milestone deadline | `list_milestones` ×4, `CLARIFY` ×2 | 0.40–0.85 |
| let's analyze the risk here | `analyze_blockers` ×6 | 0.95–0.95 |
| any update on the next milestone | `list_milestones` ×6 | 0.75–0.85 |
| modify the status document | `CLARIFY` ×6 | 0.40–0.40 |
| what's the current status | `get_project_status` ×6 | 0.72–0.72 |
| where should my focus be today | `attention_query` ×6 | 0.92–0.95 |
