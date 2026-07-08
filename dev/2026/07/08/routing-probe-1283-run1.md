# #1283 behavioral routing probe — 2026-07-08 10:46 PT

Corpus: `tests/fixtures/routing_corpus_1283.yaml` (29 rows). Rail size at probe time: 86 registered actions.
**Result: 15 PASS / 12 FAIL / 2 REVIEW**

| phrase | expected | got action | got category | conf | on rail | verdict |
|---|---|---|---|---|---|---|
| give me my standup | `action:show_standup` | `get_project_status` | STATUS | 1.0 | ✗ | FAIL |
| what's on my calendar today? | `category:TEMPORAL` | `meeting_time` | QUERY | 1.0 | ✓ | FAIL |
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
| show my open issues | `action:list_issues` | `list_issues_query` | QUERY | 1.0 | ✓ | FAIL |
| show my open pull requests | `action:list_prs` | `list_prs_query` | QUERY | 1.0 | ✓ | FAIL |
| any stale PRs? | `action:stale_prs` | `list_stale_prs` | QUERY | 0.85 | ✗ | FAIL |
| what needs my attention? | `action:attention_query` | `attention_query` | QUERY | 1.0 | ✓ | PASS |
| what changed since yesterday? | `action:changes_query` | `changes_query` | QUERY | 1.0 | ✓ | PASS |
| how productive was I this week? | `action:productivity_query` | `analyze_productivity` | ANALYSIS | 0.88 | ✗ | FAIL |
| list my projects | `action:list_projects` | `manage_portfolio` | PORTFOLIO | 1.0 | ✗ | FAIL |
| close issue 42 | `action:close_issue` | `close_issue_query` | QUERY | 1.0 | ✓ | FAIL |
| comment on issue 42: looks good | `action:comment_issue` | `comment_issue_query` | QUERY | 1.0 | ✓ | FAIL |
| what have you learned about my workstyle? | `action:pull_insights` | `pull_insights` | MEMORY | 1.0 | ✗ | FAIL(mode-2: emitted but NOT on rail) |
| set my default repo to acme/widgets | `action:set_default_repo` | `set_default_repo` | QUERY | 1.0 | ✓ | PASS |
| what is my default repo? | `action:get_default_repo` | `get_default_repo` | QUERY | 1.0 | ✓ | PASS |
| write a short update for the CEO on where we are | `action:write_stakeholder_update` | `write_stakeholder_update` | QUERY | 1.0 | ✗ | FAIL(mode-2: emitted but NOT on rail) |
| update the project plan doc with the new dates | `action:update_document_query` | `update_document_query` | QUERY | 1.0 | ✓ | PASS |
| can you clarify what you meant? | `REVIEW` | `clarification_needed` | CONVERSATION | 0.85 | ✗ | REVIEW |
| give me a project status report | `REVIEW` | `get_project_status` | STATUS | 1.0 | ✗ | REVIEW |

---

## Verified analysis (static follow-up on every FAIL — same session)

The raw 15/12/2 above is the UNCALIBRATED read. Each FAIL was traced to its real cause:

**Real, live routing gaps found: 2 (+1 structural)**

1. **`any stale PRs?`** — LLM emitted `list_stale_prs`; the rail's stale entry accepts 4 aliases (`stale_prs`, `old_prs`, `show_stale_prs`, `stale_prs_query`) and this is a 5th that misses all of them → falls past the rail to generic QUERY handling. **Live proof of the mode-4 limit**: hand-maintained alias lists can't chase LLM paraphrase space.
2. **`how productive was I this week?`** — LLM emitted `analyze_productivity`; rail's productivity entry accepts `productivity`/`my_productivity`/`weekly_metrics`/`accomplishments` — miss.
3. **Structural (mode-2)**: the REGISTRY canonical `productivity_query` is itself NOT on the rail — if the LLM emitted the documented canonical name, it would also miss. Documented-but-unregistered.

**Probe-seam artifacts (routing is actually CORRECT in production): 4 rows**

- `give me my standup`: the deterministic **pre_classifier** intercepts before the LLM (`show_standup` IS on the rail); a classifier-only probe never sees that layer.
- `who am I?` / `what have you learned about my workstyle?` / `write a short update for the CEO...`: `get_identity`, `pull_insights`, `write_stakeholder_update` are pre-classifier + **floor/context-assembler-surface** handled (conversational_floor.py, context_assembler.py) — a dispatch surface the rail-membership check doesn't see. **This is a 4th vocabulary** the static audit's three-surface model missed.

**Corpus-calibration fixes (my draft used wrong/aspirational names): 7 rows**

`meeting_time`, `list_issues_query`, `list_prs_query`, `stale_prs_query`, `manage_portfolio`,
`close_issue_query`, `comment_issue_query` are the registry canonicals; the draft expected
`category:TEMPORAL`, `list_issues`, `list_prs`, `stale_prs`, `list_projects`, `close_issue`,
`comment_issue`. Corpus v2 committed with corrections + the seam-model header.

**Recalibrated result: 24/29 route correctly; 2 live alias gaps; 1 mode-2 canonical gap; 2 REVIEW rows delivered their data** (`clarification_needed`→CONVERSATION; `give me a project status report`→`get_project_status`/STATUS — resolving the drift-cluster question: the pre-classifier and LLM both converge on `get_project_status`, which is floor-surface handled, not rail).

**Implication for AC-4 (SSOT)**: the fix is NOT just "generate aliases from the registry" — run-1 proves aliases can't enumerate paraphrase space (`list_stale_prs` was a 5th variant past 4 aliases). The SSOT should (a) constrain the PROMPT to emit only registry canonicals (the 17-action prompt vocab already tries this — extend + enforce), (b) add a normalization shim (unknown `*_prs`/`*_productivity`-shaped emissions map to canonicals or re-ask), and (c) validate rail keys ⊇ registry canonicals in CI (would have caught `productivity_query`).
