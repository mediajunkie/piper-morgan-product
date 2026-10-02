# Inversion Phase 3 — surface-2 floor probe

Run 2026-10-02 18:27Z · 5 sample(s) per phrase · LAYER (m-43): `IntentClassifier._classify_with_reasoning` only (surface 1 bypassed, no session context, dev keychain key). Read by `scripts/inversion_phase3_deletion_gate.py` (SURFACE2_FLOOR_PROBES) to credit a category-reached row whose pattern the router does not replace: the row is OK to lose its pattern when EVERY sample lands in the expected action's own category.

served (#1620, resolved per call): anthropic:claude-sonnet-4-6

| phrase | sample | surface-2 category | surface-2 action | confidence | served |
|---|---|---|---|---|---|
| what should I do next | 1 | PRIORITY | `prioritize` | 0.85 | anthropic:claude-sonnet-4-6 |
| what should I do next | 2 | PRIORITY | `prioritize` | 0.85 | anthropic:claude-sonnet-4-6 |
| what should I do next | 3 | PRIORITY | `prioritize` | 0.88 | anthropic:claude-sonnet-4-6 |
| what should I do next | 4 | PRIORITY | `prioritize` | 0.88 | anthropic:claude-sonnet-4-6 |
| what should I do next | 5 | PRIORITY | `prioritize` | 0.85 | anthropic:claude-sonnet-4-6 |
| what do I have next to do | 1 | PRIORITY | `get_top_priority` | 0.88 | anthropic:claude-sonnet-4-6 |
| what do I have next to do | 2 | PRIORITY | `get_top_priority` | 0.88 | anthropic:claude-sonnet-4-6 |
| what do I have next to do | 3 | PRIORITY | `get_top_priority` | 0.88 | anthropic:claude-sonnet-4-6 |
| what do I have next to do | 4 | PRIORITY | `get_top_priority` | 0.88 | anthropic:claude-sonnet-4-6 |
| what do I have next to do | 5 | PRIORITY | `get_top_priority` | 0.88 | anthropic:claude-sonnet-4-6 |
| did I finish the report yesterday | 1 | STATUS | `get_project_status` | 0.88 | anthropic:claude-sonnet-4-6 |
| did I finish the report yesterday | 2 | STATUS | `get_project_status` | 0.88 | anthropic:claude-sonnet-4-6 |
| did I finish the report yesterday | 3 | STATUS | `get_project_status` | 0.88 | anthropic:claude-sonnet-4-6 |
| did I finish the report yesterday | 4 | STATUS | `get_project_status` | 0.88 | anthropic:claude-sonnet-4-6 |
| did I finish the report yesterday | 5 | STATUS | `get_project_status` | 0.88 | anthropic:claude-sonnet-4-6 |
| close issue 42 | 1 | EXECUTION | `close_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| close issue 42 | 2 | EXECUTION | `close_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| close issue 42 | 3 | EXECUTION | `close_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| close issue 42 | 4 | EXECUTION | `close_issue_query` | 0.95 | anthropic:claude-sonnet-4-6 |
| close issue 42 | 5 | EXECUTION | `close_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| comment on issue 42: looks good | 1 | EXECUTION | `comment_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| comment on issue 42: looks good | 2 | EXECUTION | `comment_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| comment on issue 42: looks good | 3 | EXECUTION | `comment_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| comment on issue 42: looks good | 4 | EXECUTION | `comment_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| comment on issue 42: looks good | 5 | EXECUTION | `comment_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| close issue #123 | 1 | EXECUTION | `close_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| close issue #123 | 2 | EXECUTION | `close_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| close issue #123 | 3 | EXECUTION | `close_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| close issue #123 | 4 | EXECUTION | `close_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| close issue #123 | 5 | EXECUTION | `close_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| reopen issue #123 | 1 | EXECUTION | `reopen_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| reopen issue #123 | 2 | EXECUTION | `reopen_issue_query` | 0.98 | anthropic:claude-sonnet-4-6 |
| reopen issue #123 | 3 | EXECUTION | `reopen_issue_query` | 0.98 | anthropic:claude-sonnet-4-6 |
| reopen issue #123 | 4 | EXECUTION | `reopen_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| reopen issue #123 | 5 | EXECUTION | `reopen_issue_query` | 0.98 | anthropic:claude-sonnet-4-6 |
| comment on issue #123 | 1 | EXECUTION | `comment_issue_query` | 0.95 | anthropic:claude-sonnet-4-6 |
| comment on issue #123 | 2 | EXECUTION | `comment_issue_query` | 0.95 | anthropic:claude-sonnet-4-6 |
| comment on issue #123 | 3 | EXECUTION | `comment_issue_query` | 0.95 | anthropic:claude-sonnet-4-6 |
| comment on issue #123 | 4 | EXECUTION | `comment_issue_query` | 0.95 | anthropic:claude-sonnet-4-6 |
| comment on issue #123 | 5 | EXECUTION | `comment_issue_query` | 0.95 | anthropic:claude-sonnet-4-6 |
| please close this issue | 1 | EXECUTION | `close_issue_query` | 0.82 | anthropic:claude-sonnet-4-6 |
| please close this issue | 2 | EXECUTION | `close_issue_query` | 0.85 | anthropic:claude-sonnet-4-6 |
| please close this issue | 3 | EXECUTION | `close_issue_query` | 0.85 | anthropic:claude-sonnet-4-6 |
| please close this issue | 4 | EXECUTION | `close_issue_query` | 0.85 | anthropic:claude-sonnet-4-6 |
| please close this issue | 5 | EXECUTION | `close_issue_query` | 0.85 | anthropic:claude-sonnet-4-6 |
| re-open issue 88 | 1 | EXECUTION | `reopen_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| re-open issue 88 | 2 | EXECUTION | `reopen_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| re-open issue 88 | 3 | EXECUTION | `reopen_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| re-open issue 88 | 4 | EXECUTION | `reopen_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| re-open issue 88 | 5 | EXECUTION | `reopen_issue_query` | 0.97 | anthropic:claude-sonnet-4-6 |
| add comment to issue 99 | 1 | EXECUTION | `comment_issue_query` | 0.95 | anthropic:claude-sonnet-4-6 |
| add comment to issue 99 | 2 | EXECUTION | `comment_issue_query` | 0.95 | anthropic:claude-sonnet-4-6 |
| add comment to issue 99 | 3 | EXECUTION | `comment_issue_query` | 0.95 | anthropic:claude-sonnet-4-6 |
| add comment to issue 99 | 4 | EXECUTION | `comment_issue_query` | 0.95 | anthropic:claude-sonnet-4-6 |
| add comment to issue 99 | 5 | EXECUTION | `comment_issue_query` | 0.95 | anthropic:claude-sonnet-4-6 |
| reply to issue 99 | 1 | EXECUTION | `comment_issue_query` | 0.85 | anthropic:claude-sonnet-4-6 |
| reply to issue 99 | 2 | EXECUTION | `comment_issue_query` | 0.9 | anthropic:claude-sonnet-4-6 |
| reply to issue 99 | 3 | EXECUTION | `comment_issue_query` | 0.85 | anthropic:claude-sonnet-4-6 |
| reply to issue 99 | 4 | EXECUTION | `comment_issue_query` | 0.9 | anthropic:claude-sonnet-4-6 |
| reply to issue 99 | 5 | EXECUTION | `comment_issue_query` | 0.85 | anthropic:claude-sonnet-4-6 |
| comment on 99 | 1 | EXECUTION | `comment_issue_query` | 0.85 | anthropic:claude-sonnet-4-6 |
| comment on 99 | 2 | EXECUTION | `comment_issue_query` | 0.85 | anthropic:claude-sonnet-4-6 |
| comment on 99 | 3 | EXECUTION | `comment_issue_query` | 0.85 | anthropic:claude-sonnet-4-6 |
| comment on 99 | 4 | EXECUTION | `comment_issue_query` | 0.85 | anthropic:claude-sonnet-4-6 |
| comment on 99 | 5 | EXECUTION | `comment_issue_query` | 0.85 | anthropic:claude-sonnet-4-6 |
| what are my top priorities? | 1 | PRIORITY | `prioritize` | 0.95 | anthropic:claude-sonnet-4-6 |
| what are my top priorities? | 2 | PRIORITY | `prioritize` | 0.95 | anthropic:claude-sonnet-4-6 |
| what are my top priorities? | 3 | PRIORITY | `prioritize` | 0.95 | anthropic:claude-sonnet-4-6 |
| what are my top priorities? | 4 | PRIORITY | `prioritize` | 0.95 | anthropic:claude-sonnet-4-6 |
| what are my top priorities? | 5 | PRIORITY | `prioritize` | 0.95 | anthropic:claude-sonnet-4-6 |
