# #1283 behavioral routing probe — 2026-07-09 07:24 PT

Corpus: `tests/fixtures/routing_corpus_1283.yaml` (29 rows). Rail size at probe time: 89 registered actions.
**Result: 20 PASS / 7 FAIL / 2 REVIEW**

| phrase | expected | got action | got category | conf | on rail | verdict |
|---|---|---|---|---|---|---|
| give me my standup | `action:show_standup` | `get_project_status` | STATUS | 1.0 | ✗ | FAIL |
| what's on my calendar today? | `action:meeting_time` | `meeting_time` | QUERY | 1.0 | ✓ | PASS |
| when is my next meeting? | `category:TEMPORAL` | `get_current_time` | TEMPORAL | 1.0 | ✗ | PASS |
| what am I working on? | `category:STATUS` | `get_project_status` | STATUS | 1.0 | ✗ | PASS |
| what should I focus on today? | `category:PRIORITY` | `get_top_priority` | PRIORITY | 1.0 | ✗ | PASS |
| what are my top priorities? | `category:PRIORITY` | `get_top_priority` | PRIORITY | 1.0 | ✗ | PASS |
| who am I? | `action:get_identity` | `get_identity` | IDENTITY | 0.95 | ✗ | FAIL(mode-2: emitted but NOT on rail) |
| what's my role? | `category:IDENTITY` | `get_role` | IDENTITY | 0.9 | ✗ | PASS |
| how do I create a ticket? | `category:GUIDANCE` | `provide_guidance` | GUIDANCE | 0.9 | ✗ | PASS |
| create a ticket for the login bug | `category:EXECUTION` | `create_ticket` | EXECUTION | 0.95 | ✗ | PASS |
| analyze the file I uploaded | `action:analyze_data` | `analyze_data` | ANALYSIS | 0.8 | ✓ | PASS |
| summarize the document | `category:SYNTHESIS` | `generate_summary` | SYNTHESIS | 0.85 | ✗ | PASS |
| what time is it? | `category:TEMPORAL` | `get_current_time` | TEMPORAL | 1.0 | ✗ | PASS |
| show my open issues | `action:list_issues_query` | `list_issues_query` | QUERY | 1.0 | ✓ | PASS |
| show my open pull requests | `action:list_prs_query` | `list_prs_query` | QUERY | 1.0 | ✓ | PASS |
| any stale PRs? | `action:stale_prs_query` | `get_pull_requests` | QUERY | 0.85 | ✗ | FAIL |
| what needs my attention? | `action:attention_query` | `attention_query` | QUERY | 1.0 | ✓ | PASS |
| what changed since yesterday? | `action:changes_query` | `changes_query` | QUERY | 1.0 | ✓ | PASS |
| how productive was I this week? | `action:productivity_query` | `analyze_productivity` | ANALYSIS | 0.85 | ✓ | FAIL |
| list my projects | `action:manage_portfolio` | `manage_portfolio` | PORTFOLIO | 1.0 | ✗ | FAIL(mode-2: emitted but NOT on rail) |
| close issue 42 | `action:close_issue_query` | `close_issue_query` | QUERY | 1.0 | ✓ | PASS |
| comment on issue 42: looks good | `action:comment_issue_query` | `comment_issue_query` | QUERY | 1.0 | ✓ | PASS |
| what have you learned about my workstyle? | `action:pull_insights` | `pull_insights` | MEMORY | 1.0 | ✗ | FAIL(mode-2: emitted but NOT on rail) |
| set my default repo to acme/widgets | `action:set_default_repo` | `set_default_repo` | QUERY | 1.0 | ✓ | PASS |
| what is my default repo? | `action:get_default_repo` | `get_default_repo` | QUERY | 1.0 | ✓ | PASS |
| write a short update for the CEO on where we are | `action:write_stakeholder_update` | `write_stakeholder_update` | QUERY | 1.0 | ✗ | FAIL(mode-2: emitted but NOT on rail) |
| update the project plan doc with the new dates | `action:update_document_query` | `update_document_query` | QUERY | 1.0 | ✓ | PASS |
| can you clarify what you meant? | `REVIEW` | `clarification_needed` | CONVERSATION | 0.85 | ✗ | REVIEW |
| give me a project status report | `REVIEW` | `get_project_status` | STATUS | 1.0 | ✗ | REVIEW |
