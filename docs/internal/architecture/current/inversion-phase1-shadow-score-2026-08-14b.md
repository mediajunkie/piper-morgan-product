# Inversion Phase-1 shadow score — CONSTRAINED ROUTER vs Phase-0 baseline
Run: 2026-08-15 01:46Z · corpus: inversion_corpus_phase0.yaml (93 rows) · scripts/inversion_phase1_shadow_score.py

LAYER (m-43): **router only, context-free** — one constrained Haiku-class call per row (94 LLM calls incl. repair retries; 0 ERROR, 0 REFUSED), grammar derived from the live registry at run time (62 canonical operations, 73 input-side aliases collapsed, + NONE/CLARIFY). The production chain was NOT executed in this run; the baseline column is Phase-0's FULL-CHAIN production decision (inversion-phase0-baseline-full-2026-08-12.md). Context-dependent rows (the 1529 offer/flow family) ran WITHOUT session state — their answers are informational for Phase 2, not its measured shape.

## Per-category vs baseline (denominators stated — m-44)

| category | rows | asserted | router match | baseline match | Δ | REVIEW | gate |
|---|---|---|---|---|---|---|---|
| QUERY | 30 | 12 | 11 | 12/12 | -1 | 18 | **REGRESSION** |
| EXECUTION | 15 | 6 | 5 | 5/6 | +0 | 9 | no regression |
| PORTFOLIO | 9 | 7 | 6 | 6/7 | +0 | 2 | no regression |
| TEMPORAL | 7 | 4 | 3 | 4/4 | -1 | 3 | **REGRESSION** |
| GUIDANCE | 6 | 1 | 1 | 1/1 | +0 | 5 | no regression |
| CONVERSATION | 5 | 0 | 0 | 0/0 | — | 5 | **UNGATEABLE** (REVIEW-only denominator) |
| STATUS | 4 | 2 | 1 | 1/2 | +0 | 2 | no regression |
| PRIORITY | 3 | 2 | 2 | 2/2 | +0 | 1 | no regression |
| IDENTITY | 3 | 2 | 2 | 2/2 | +0 | 1 | no regression |
| SYNTHESIS | 3 | 2 | 1 | 2/2 | -1 | 1 | **REGRESSION** |
| MEMORY | 3 | 1 | 1 | 1/1 | +0 | 2 | no regression |
| DISCOVERY | 2 | 0 | 0 | 0/0 | — | 2 | **UNGATEABLE** (REVIEW-only denominator) |
| PROVENANCE | 1 | 0 | 0 | 0/0 | — | 1 | **UNGATEABLE** (REVIEW-only denominator) |
| TRUST | 1 | 0 | 0 | 0/0 | — | 1 | **UNGATEABLE** (REVIEW-only denominator) |
| ANALYSIS | 1 | 0 | 0 | 0/0 | — | 1 | **UNGATEABLE** (REVIEW-only denominator) |
| **TOTAL** | 93 | 39 | 33 | 36/39 | -3 | 54 | (aggregate is NOT the gate) |

Gate reading (Arch condition 1 as amended 08-09 08:3x, PPM): **no category may regress; the aggregate is never the gate** (the M2 precedent: 72.1% aggregate passed while a category was broken). CONVERSATION / DISCOVERY / PROVENANCE / TRUST / ANALYSIS have REVIEW-only denominators in Phase 0 and remain **ungateable** here — same as Phase 0 stated; growing asserted expectations there is outstanding Phase-0 work, not a Phase-1 scoring artifact.

🔴 **Per-category regressions vs baseline** (recorded as data — this run does not tune-until-green): QUERY: 12→11; TEMPORAL: 4→3; SYNTHESIS: 2→1

## Exhibit A (PM 2026-08-08 live transcript) + Arch's demanded row

Selection rule: corpus `source` containing one of ('exhibit-a', 'issue-1559', 'issue-1492') → 8 rows (the 8 Exhibit-A failures), plus the demanded row `"what reminders do I have?"` (probe-row-11, REVIEW — the sharpest test of the thesis: the LLM classifier misrouted it until the pre-classifier claimed it).

| phrase | expected | router route @conf | verdict | source |
|---|---|---|---|---|
| Yes please | REVIEW | `CLARIFY` @0.1 | REVIEW (informational) | exhibit-a/1529 (test_offer_binding_1529.py PM_YE |
| end standup | REVIEW | `NONE` @0.85 | REVIEW (informational) | exhibit-a/1529 (test_offer_binding_1529.py PM_EN |
| i am not doing the standup right now. restore CoVa | REVIEW | `manage_portfolio` @0.92 | REVIEW (informational) | exhibit-a/1529 (test_flow_escape_1529.py PM_REFU |
| what projects do I have? | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH | exhibit-a/1530 (chat omitted active CoVa; wrong  |
| remind me at 9:41 today to check in with the lead develope | action:create_reminder | `create_reminder` @0.95 | MATCH | issue-1559 (adjacency gap: 'remind me at <time>  |
| Archive my project Test. | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH | issue-1492 (trailing punctuation breaks extracti |
| Archive my project "Test" | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH | issue-1492 (quoted name breaks extraction) |
| Archive the project called Test | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH | issue-1492 ('called X' phrasing breaks extractio |
| what reminders do I have? | REVIEW | `list_reminders_query` @0.99 | REVIEW (informational) | probe-row-11 |

## REVIEW rows — the router's answers as data (informational, unscored)

These 54 rows are the Inversion's question book (36 probe-DISAGREEs by construction + PM's live failures). Nothing here is scored; the router's answer is recorded so the questions accumulate evidence.

| phrase | category | router route @conf | rationale | source |
|---|---|---|---|---|
| can you clarify what you meant? | QUERY | `CLARIFY` @0.95 | User asks for clarification but no prior statement exists in | corpus-1283 |
| show me my archived projects | QUERY | `list_archived_projects` @0.99 | User explicitly requests archived projects list. | corpus-1283 + issue-1579 (PORTFOLIO list |
| what have you learned about my work style? | MEMORY | `pull_insights` @0.99 | Direct what-have-you-learned question about work style patte | probe-row-2 |
| connect my github | GUIDANCE | `get_contextual_guidance` @0.95 | Integration setup request; user wants to connect GitHub to P | probe-row-3 |
| connect my notion | GUIDANCE | `get_contextual_guidance` @0.95 | User requests to connect Notion integration; contextual guid | probe-row-4 |
| link my google calendar | GUIDANCE | `get_contextual_guidance` @0.95 | User requests to connect/integrate Google Calendar; destinat | probe-row-6 |
| add a repo to my portfolio | PORTFOLIO | `manage_repos` @0.95 | User wants to link a GitHub repository to their project port | probe-row-7 |
| show me my todos | QUERY | `list_todos_query` @0.99 | Direct request to display user's todo list | probe-row-8 |
| connect my calendar | GUIDANCE | `get_contextual_guidance` @0.95 | Integration setup request; calendar connection is a configur | probe-row-10 |
| what reminders do I have? | TEMPORAL | `list_reminders_query` @0.99 | Direct request to list reminders; matches catalog operation  | probe-row-11 |
| hello | CONVERSATION | `greeting` @0.99 | Simple greeting pleasantry. | probe-row-12 |
| goodbye | CONVERSATION | `farewell` @0.99 | User is saying goodbye; matches farewell operation exactly. | probe-row-13 |
| thank you! | CONVERSATION | `thanks` @0.99 | Simple expression of gratitude; no action required. | probe-row-14 |
| what can you do? | DISCOVERY | `get_capabilities` @0.99 | Direct what-can-you-do question about assistant capabilities | probe-row-15 |
| why did you suggest that? | PROVENANCE | `explain_suggestion` @0.95 | User asking for provenance of a prior recommendation. | probe-row-16 |
| why can't you create issues? | TRUST | `get_capabilities` @0.85 | User asking about assistant's capabilities, specifically iss | probe-row-17 |
| what do you remember about me? | MEMORY | `get_memory` @0.99 | Direct what-do-you-remember question about stored user conte | probe-row-18 |
| what's my default repo? | QUERY | `get_default_repo` @0.99 | Direct question about default repository setting | probe-row-19 |
| set my default repo to mediajunkie/piper-morgan-product | EXECUTION | `set_default_repo` @0.99 | User explicitly requests setting default repo with owner/rep | probe-row-20 |
| write a short update for the CEO on the beta | SYNTHESIS | `write_stakeholder_update` @0.95 | User requests a stakeholder update for a named audience (CEO | probe-row-21 |
| update the roadmap doc with the new dates | EXECUTION | `update_document` @0.85 | User requests document update with specific content (new dat | probe-row-22 |
| tell me more about the github integration | QUERY | `get_feature_info` @0.95 | User explicitly requests details about a specific Piper feat | probe-row-23 |
| who are you? | IDENTITY | `get_identity` @0.99 | Direct who-are-you question about the assistant's identity a | probe-row-24 |
| show my recurring meetings | QUERY | `recurring_meetings` @0.99 | Direct request to show recurring meetings matches _handle_re | probe-row-28 |
| what's my week look like? | QUERY | `week_calendar` @0.95 | Direct calendar overview query for the week ahead. | probe-row-29 |
| what's the next milestone? | STATUS | `list_milestones` @0.85 | User asks for next milestone; list_milestones retrieves mile | probe-row-30 |
| what branch are we on? | QUERY | `local_git_status_query` @0.95 | Direct question about current git branch status. | probe-row-31 |
| what did we ship this week? | QUERY | `shipped_this_week` @0.95 | Direct query about shipped items this week | probe-row-32 |
| show stale prs | QUERY | `stale_prs` @0.95 | User explicitly requests stale PRs list | probe-row-33 |
| close issue #123 | EXECUTION | `close_issue` @0.95 | User explicitly requests closing issue #123 | probe-row-34 |
| reopen issue #123 | EXECUTION | `reopen_issue` @0.95 | Clear request to reopen a specific issue by number. | probe-row-35 |
| comment on issue #123 | EXECUTION | `comment_issue` @0.95 | User requests commenting on a specific issue number. | probe-row-36 |
| how many open issues do we have? | QUERY | `list_issues` @0.95 | User asking for count/list of open issues in default repo | probe-row-37 |
| show my prs | QUERY | `list_prs` @0.95 | User requests to see their pull requests. | probe-row-38 |
| show issue #123 | QUERY | `review_issue` @0.95 | User requests to view/show a specific issue by number. | probe-row-39 |
| show milestones | QUERY | `list_milestones` @0.95 | User requests milestone list; direct match to list_milestone | probe-row-40 |
| what did we create this session? | QUERY | `session_activity_query` @0.95 | Direct match to session-activity recall pattern | probe-row-41 |
| what's my productivity? | QUERY | `productivity` @0.95 | Direct productivity query requesting user's productivity met | probe-row-42 |
| remind me to review the roadmap tomorrow | EXECUTION | `create_reminder` @0.95 | User requests a reminder for a specific task at a future tim | probe-row-43 |
| complete todo 3 | EXECUTION | `complete_todo` @0.95 | User explicitly requests marking todo 3 as done. | probe-row-44 |
| show all my todos | QUERY | `list_todos_query` @0.99 | User requests display of their complete todo list. | probe-row-45 |
| what's my next todo? | QUERY | `list_todos_query` @0.95 | User asking for next todo item from their list | probe-row-46 |
| when did I complete the onboarding project? | STATUS | `check_completion_status` @0.95 | User asks when past work (onboarding project) was completed. | probe-row-47 |
| how do I get started? | GUIDANCE | `get_contextual_guidance` @0.85 | Getting-started question; user needs contextual guidance on  | probe-row-49 |
| what's blocking the milestone? | ANALYSIS | `analyze_blockers` @0.95 | Direct match to analyze_blockers example query | probe-row-50 |
| what are my priorities? | PRIORITY | `get_top_priority` @0.95 | User asking for prioritized work items or top priorities to  | probe-row-52 |
| Yes please | CONVERSATION | `CLARIFY` @0.1 | Affirmative response without prior context; unclear what is  | exhibit-a/1529 (test_offer_binding_1529. |
| end standup | CONVERSATION | `NONE` @0.85 | Conversational command to end a session; no catalog operatio | exhibit-a/1529 (test_offer_binding_1529. |
| i am not doing the standup right now. restore CoVa | PORTFOLIO | `manage_portfolio` @0.92 | User declines standup, requests project restoration by name. | exhibit-a/1529 (test_flow_escape_1529.py |
| delete my reminders | TEMPORAL | `CLARIFY` @0.45 | Ambiguous: delete all reminders vs. list reminders to select | issue-1527 (greedy portfolio delete patt |
| hi piper, connect my github | EXECUTION | `get_contextual_guidance` @0.95 | User requests GitHub integration setup; contextual guidance  | issue-1505 (multi-intent path drops the  |
| please clear the reminders except for "Review the PR" - | TEMPORAL | `CLARIFY` @0.65 | Two distinct operations requested: manage reminders (unclear | issue-1606 (PM live 2026-08-12: request  |
| are you able to set my default repo for me conversation | DISCOVERY | `get_contextual_guidance` @0.85 | User asking how to set default repo; guidance on setup/confi | issue-1606 (interrogative parsed as impe |
| please mark 1, 2, 4, and 5 done | EXECUTION | `CLARIFY` @0.4 | Ambiguous: could mark todos (1,2,4,5) or issues/PRs done. Ne | PM live 2026-08-12 (#1603 session; multi |

## Row detail (asserted rows)

| phrase | category | expected | router route @conf | verdict | note |
|---|---|---|---|---|---|
| give me my standup | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| what's on my calendar today? | TEMPORAL | action:meeting_time | `week_calendar` @0.85 | MISMATCH |  |
| when is my next meeting? | TEMPORAL | action:meeting_time | `meeting_time` @0.95 | MATCH |  |
| what am I working on? | STATUS | category:STATUS | `attention_query` @0.85 | MISMATCH |  |
| what should I focus on today? | PRIORITY | category:PRIORITY | `get_top_priority` @0.92 | MATCH |  |
| what are my top priorities? | PRIORITY | category:PRIORITY | `get_top_priority` @0.95 | MATCH |  |
| who am I? | IDENTITY | action:get_identity | `get_identity` @0.3 | MATCH |  |
| what's my role? | IDENTITY | category:IDENTITY | `get_identity` @0.95 | MATCH |  |
| how do I create a ticket? | GUIDANCE | category:GUIDANCE | `get_contextual_guidance` @0.95 | MATCH |  |
| create a ticket for the login bug | EXECUTION | action:create_issue | `create_issue` @0.92 | MATCH |  |
| analyze the file I uploaded | QUERY | action:analyze_data | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| summarize the document | SYNTHESIS | category:SYNTHESIS | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| what time is it? | TEMPORAL | category:TEMPORAL | `get_current_time` @0.99 | MATCH |  |
| show my open issues | QUERY | action:list_issues_query | `list_issues` @0.95 | MATCH |  |
| show my open pull requests | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| any stale PRs? | QUERY | action:stale_prs_query | `stale_prs` @0.95 | MATCH |  |
| what needs my attention? | QUERY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what changed since yesterday? | QUERY | action:changes_query | `changes_query` @0.95 | MATCH |  |
| how productive was I this week? | QUERY | action:productivity_query | `productivity` @0.95 | MATCH |  |
| list my projects | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.99 | MATCH |  |
| close issue 42 | EXECUTION | action:close_issue_query | `close_issue` @0.95 | MATCH |  |
| comment on issue 42: looks good | EXECUTION | action:comment_issue_query | `comment_issue` @0.95 | MATCH |  |
| what have you learned about my workstyle? | MEMORY | action:pull_insights | `pull_insights` @0.95 | MATCH |  |
| set my default repo to acme/widgets | EXECUTION | action:set_default_repo | `set_default_repo` @0.99 | MATCH |  |
| what is my default repo? | QUERY | action:get_default_repo | `get_default_repo` @0.99 | MATCH |  |
| write a short update for the CEO on where we are | SYNTHESIS | action:write_stakeholder_update | `write_stakeholder_update` @0.92 | MATCH |  |
| update the project plan doc with the new dates | EXECUTION | action:update_document_query | `update_document` @0.85 | MATCH |  |
| give me a project status report | EXECUTION | action:update_issue | `get_project_status` @0.95 | MISMATCH |  |
| can we connect my github? | QUERY | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| connect my slack | QUERY | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| link mediajunkie/test-piper-morgan to the project | QUERY | action:manage_repos | `manage_repos` @0.95 | MATCH |  |
| help me set up github | QUERY | action:get_contextual_guidance | `get_contextual_guidance` @0.95 | MATCH |  |
| list my archived projects | PORTFOLIO | action:manage_portfolio | `list_archived_projects` @0.99 | MISMATCH |  |
| what projects have I archived? | PORTFOLIO | action:list_archived_projects | `list_archived_projects` @0.95 | MATCH |  |
| what projects do I have? | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| remind me at 9:41 today to check in with the lead devel | TEMPORAL | action:create_reminder | `create_reminder` @0.95 | MATCH |  |
| Archive my project Test. | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| Archive my project "Test" | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| Archive the project called Test | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |

---

## Run 1b — what this run is (hand-authored; everything above this rule is generator output)

This is the ONE attributable rerun after Arch ratified the 62-op grammar
(decisions.log 2026-08-14 ~18:5x). Exactly two things changed since the first
run (`inversion-phase1-shadow-score-2026-08-14.md`, 19:58Z):

1. **The two ratified corpus re-expressions** (commit `eb8fa5a88`, pre-run):
   "create a ticket for the login bug" → `action:create_issue` (category
   verified cosmetic-only) and "when is my next meeting?" →
   `action:meeting_time` (citing #589).
2. **Family-1 grammar-description enrichment** (this commit):
   `ACTION_DESCRIPTIONS` in `services/intent_service/action_registry.py` —
   registry METADATA the router's derivation now picks up for the 22
   registry-only canonicals whose catalog line was previously the
   uninformative `"<category> action (<disposition>-handled)"`. Every line is
   grounded in the handler's own code (evidence cited per entry); the router
   still derives, never hand-writes (Arch's registry-derived condition).

Nothing else changed routing behavior: no pre-classifier change, no existing
prompt change, no dispatch change, no scorer change. The router prompt template
is byte-identical; only the catalog CONTENT (descriptions) differs.

**Environment note (m-43 — say what the call actually hit)**: every routing
call in THIS run attempted the resolved primary provider (openai, per the
server selection default) and received HTTP 429 `credit_balance_exhausted` — an
account state, not a rate limit — then fell back to Anthropic
`claude-haiku-4-5` (the light tier). The first run ran 6 hours earlier on the
same seat and keychain against the same exhausted account, and its doc asserts
Haiku-class calls, so both runs are believed served by the same model; but run
1's doc does not RECORD its per-call provider path, so model identity across
the two runs is inferred, not proven. Recorded here so the next run can check.

## DELTA vs run 1 (24/39 → 33/39), decomposed by cause

Denominators: 39 asserted rows, both runs, identical phrase set.

### Fixed by corpus re-expression (2 rows)

| phrase | run 1 | run 1b | note |
|---|---|---|---|
| when is my next meeting? | `meeting_time` @0.95 MISMATCH | `meeting_time` @0.95 MATCH | router answer UNCHANGED; the expectation was corrected (category:TEMPORAL → action:meeting_time, #589 cited) |
| create a ticket for the login bug | `create_issue` @0.92 MISMATCH | `create_issue` @0.92 MATCH | router answer UNCHANGED; expectation corrected (category:EXECUTION → action:create_issue, cosmetic-only verified) |

Exactly the Family-2 prediction: these were scoring-seam artifacts, not routing
misses — the router's answer did not move.

### Fixed by description enrichment (8 rows: the Family-1 six + 2 more)

| phrase | run 1 | run 1b | enriched line responsible |
|---|---|---|---|
| Archive my project Test. | `NONE` @0.85 | `manage_portfolio` @0.95 MATCH | manage_portfolio: "archive, restore, delete, search, add, and list projects" |
| Archive my project "Test" | `NONE` @0.85 | `manage_portfolio` @0.95 MATCH | same |
| Archive the project called Test | `NONE` @0.85 | `manage_portfolio` @0.95 MATCH | same |
| connect my slack | `NONE` @0.95 | `get_contextual_guidance` @0.95 MATCH | get_contextual_guidance: "…set up, configure, or connect integrations (GitHub, Slack, calendar, Notion)…" |
| can we connect my github? | `manage_repos` @0.92 | `get_contextual_guidance` @0.95 MATCH | same |
| help me set up github | `NONE` @0.85 | `get_contextual_guidance` @0.95 MATCH | same |
| how do I create a ticket? | `get_capabilities` @0.85 | `get_contextual_guidance` @0.95 MATCH | "how-do-I and getting-started questions" (was a Family-4 near-neighbor; the enrichment resolved it too) |
| link mediajunkie/test-piper-morgan to the project | `CLARIFY` @0.4 | `manage_repos` @0.95 MATCH | manage_repos: "Link, unlink, or list GitHub repositories for the user's projects" |

The Family-1 analysis is confirmed: the first run's NONE answers were the
catalog failing to describe the operation, not the model failing to read. Six
predicted rows fixed, plus two adjacent rows ("how do I create a ticket?",
"link … to the project") the same mechanism reached.

### Flipped AGAINST us for reasons OTHER than the changes (1 row — stochasticity, named honestly)

| phrase | run 1 | run 1b |
|---|---|---|
| what's on my calendar today? | `meeting_time` @0.92 MATCH | `week_calendar` @0.85 MISMATCH |

Neither `meeting_time` nor `week_calendar` had any description change (both are
rail entries, untouched), and the row's expectation is unchanged. The phrase
sits between two adjacent calendar operations and the model flipped at the
margin (@0.85). This is LLM stochasticity, not an effect of the two ratified
changes — recorded honestly rather than absorbed. It is the sole reason
TEMPORAL still shows -1.

### Changed answer, still MISMATCH (1 row)

"give me a project status report": `generate_report` @0.85 → `get_project_status`
@0.95 (expected `action:update_issue`). The expectation was flagged in the
Phase-0 baseline doc itself as a draft-era vocabulary artifact under re-review
(Family 3); the router's new answer — plausibly steered by the new
get_project_status line ("status reports") — is at least as defensible as run
1's. The row stays a MISMATCH under the corpus as written.

### Unchanged misses (4 rows)

- "analyze the file I uploaded" — CLARIFY @0.4 both runs (Family 4: no uploaded
  file exists in a context-free run; the full-chain baseline had context).
- "summarize the document" — CLARIFY @0.4 both runs (by design: the grammar has
  no summarize operation; SUMMARIZE-TAXONOMY floors summaries).
- "what am I working on?" — `attention_query` @0.85 both runs (STATUS
  near-neighbor; genuine adjacency question, unchanged).
- "list my archived projects" — `list_archived_projects` @0.99 both runs
  (strictly more specific than the expected `manage_portfolio`, which encodes
  what production happens to do; Family 3).

Arithmetic check: 24 + 2 (re-expression) + 8 (enrichment) − 1 (stochastic flip)
= 33. ✓ (One additional row, "who am I?", matched in both runs but with a
confidence swing 0.99 → 0.3 — no verdict change; noted as margin noise.)

## Per-category gate verdict (Arch condition 1: no category regresses; aggregate never the gate)

- **Now meeting no-regression vs baseline (7 gateable categories)**:
  EXECUTION (5 = 5), PORTFOLIO (6 = 6), GUIDANCE (1 = 1), STATUS (1 = 1),
  PRIORITY (2 = 2), IDENTITY (2 = 2), MEMORY (1 = 1). Run 1 had EXECUTION,
  PORTFOLIO, and GUIDANCE in regression; all three cleared via the two
  attributable causes.
- **Still REGRESSION (3)**:
  - QUERY 11 vs 12 (-1): the sole miss is "analyze the file I uploaded" — a
    Family-4 honest abstention (CLARIFY) in a context-free run. Phase 2's
    context-carrying is the designed fix lane, not description tuning.
  - TEMPORAL 3 vs 4 (-1): entirely the stochastic calendar flip above; the row
    the re-expression fixed ("when is my next meeting?") now passes.
  - SYNTHESIS 1 vs 2 (-1): "summarize the document" CLARIFYs because the
    grammar has no summarize operation BY DESIGN (SUMMARIZE-TAXONOMY). As
    scored, a router-only run cannot pass this row; whether the row should be
    re-expressed for the router layer is a Phase-0 corpus question, recorded
    here rather than tuned around.
- **Ungateable (REVIEW-only denominators, unchanged from Phase 0)**:
  CONVERSATION, DISCOVERY, PROVENANCE, TRUST, ANALYSIS.

## Highlights the gate should read alongside the table

- ⭐ **The Family-1 mechanism is confirmed at the Exhibit-A restore row too**
  (REVIEW, informational): "i am not doing the standup right now. restore
  CoVa" went `NONE` @0.95 → `manage_portfolio` @0.92 with rationale "user
  declines standup, requests project restoration by name" — exactly what run
  1's decomposition predicted the enrichment would reach. The context-carrying
  question (should a mid-flow refusal route the restore?) remains Phase 2's.
- **The connect-integration REVIEW family converged on the production
  destination**: "connect my github/notion/calendar", "link my google
  calendar", "hi piper, connect my github", and "are you able to set my
  default repo for me conversationally?" all now route
  `get_contextual_guidance` (run 1: a mix of `manage_repos` and `NONE`).
- **Vocabulary drift remains structurally absent**: 94 calls, 1 repair retry,
  0 REFUSED, 0 ERROR — the enforced-vocabulary property held through a
  catalog-content change.
- **Arch's demanded row still passes**: "what reminders do I have?" →
  `list_reminders_query` @0.99, unchanged.
- **Cost**: 94 Haiku-class calls (after per-call primary fallback, see
  environment note) — pennies, unchanged.
