# Inversion Phase-1 shadow score — CONSTRAINED ROUTER vs Phase-0 baseline
Run: 2026-08-14 19:58Z · corpus: inversion_corpus_phase0.yaml (93 rows) · scripts/inversion_phase1_shadow_score.py

LAYER (m-43): **router only, context-free** — one constrained Haiku-class call per row (93 LLM calls incl. repair retries; 0 ERROR, 0 REFUSED), grammar derived from the live registry at run time (62 canonical operations, 73 input-side aliases collapsed, + NONE/CLARIFY). The production chain was NOT executed in this run; the baseline column is Phase-0's FULL-CHAIN production decision (inversion-phase0-baseline-full-2026-08-12.md). Context-dependent rows (the 1529 offer/flow family) ran WITHOUT session state — their answers are informational for Phase 2, not its measured shape.

## Per-category vs baseline (denominators stated — m-44)

| category | rows | asserted | router match | baseline match | Δ | REVIEW | gate |
|---|---|---|---|---|---|---|---|
| QUERY | 30 | 12 | 7 | 12/12 | -5 | 18 | **REGRESSION** |
| EXECUTION | 15 | 6 | 4 | 5/6 | -1 | 9 | **REGRESSION** |
| PORTFOLIO | 9 | 7 | 3 | 6/7 | -3 | 2 | **REGRESSION** |
| TEMPORAL | 7 | 4 | 3 | 4/4 | -1 | 3 | **REGRESSION** |
| GUIDANCE | 6 | 1 | 0 | 1/1 | -1 | 5 | **REGRESSION** |
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
| **TOTAL** | 93 | 39 | 24 | 36/39 | -12 | 54 | (aggregate is NOT the gate) |

Gate reading (Arch condition 1 as amended 08-09 08:3x, PPM): **no category may regress; the aggregate is never the gate** (the M2 precedent: 72.1% aggregate passed while a category was broken). CONVERSATION / DISCOVERY / PROVENANCE / TRUST / ANALYSIS have REVIEW-only denominators in Phase 0 and remain **ungateable** here — same as Phase 0 stated; growing asserted expectations there is outstanding Phase-0 work, not a Phase-1 scoring artifact.

🔴 **Per-category regressions vs baseline** (recorded as data — this run does not tune-until-green): QUERY: 12→7; EXECUTION: 5→4; PORTFOLIO: 6→3; TEMPORAL: 4→3; GUIDANCE: 1→0; SYNTHESIS: 2→1

## Exhibit A (PM 2026-08-08 live transcript) + Arch's demanded row

Selection rule: corpus `source` containing one of ('exhibit-a', 'issue-1559', 'issue-1492') → 8 rows (the 8 Exhibit-A failures), plus the demanded row `"what reminders do I have?"` (probe-row-11, REVIEW — the sharpest test of the thesis: the LLM classifier misrouted it until the pre-classifier claimed it).

| phrase | expected | router route @conf | verdict | source |
|---|---|---|---|---|
| Yes please | REVIEW | `CLARIFY` @0.0 | REVIEW (informational) | exhibit-a/1529 (test_offer_binding_1529.py PM_YE |
| end standup | REVIEW | `NONE` @0.85 | REVIEW (informational) | exhibit-a/1529 (test_offer_binding_1529.py PM_EN |
| i am not doing the standup right now. restore CoVa | REVIEW | `NONE` @0.95 | REVIEW (informational) | exhibit-a/1529 (test_flow_escape_1529.py PM_REFU |
| what projects do I have? | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH | exhibit-a/1530 (chat omitted active CoVa; wrong  |
| remind me at 9:41 today to check in with the lead develope | action:create_reminder | `create_reminder` @0.98 | MATCH | issue-1559 (adjacency gap: 'remind me at <time>  |
| Archive my project Test. | action:manage_portfolio | `NONE` @0.85 | MISMATCH | issue-1492 (trailing punctuation breaks extracti |
| Archive my project "Test" | action:manage_portfolio | `NONE` @0.85 | MISMATCH | issue-1492 (quoted name breaks extraction) |
| Archive the project called Test | action:manage_portfolio | `NONE` @0.85 | MISMATCH | issue-1492 ('called X' phrasing breaks extractio |
| what reminders do I have? | REVIEW | `list_reminders_query` @0.99 | REVIEW (informational) | probe-row-11 |

## REVIEW rows — the router's answers as data (informational, unscored)

These 54 rows are the Inversion's question book (36 probe-DISAGREEs by construction + PM's live failures). Nothing here is scored; the router's answer is recorded so the questions accumulate evidence.

| phrase | category | router route @conf | rationale | source |
|---|---|---|---|---|
| can you clarify what you meant? | QUERY | `NONE` @0.95 | User asks for clarification of prior context, but no prior m | corpus-1283 |
| show me my archived projects | QUERY | `list_archived_projects` @0.99 | Direct match to archived-projects list query operation. | corpus-1283 + issue-1579 (PORTFOLIO list |
| what have you learned about my work style? | MEMORY | `pull_insights` @0.95 | Direct memory-action query about learned work-style patterns | probe-row-2 |
| connect my github | GUIDANCE | `manage_repos` @0.92 | User wants to add/connect a GitHub repo to their portfolio | probe-row-3 |
| connect my notion | GUIDANCE | `manage_repos` @0.72 | User wants to add/connect a new integration (Notion). Portfo | probe-row-4 |
| link my google calendar | GUIDANCE | `NONE` @0.95 | Calendar linking is account setup, not in catalog scope. | probe-row-6 |
| add a repo to my portfolio | PORTFOLIO | `manage_repos` @0.95 | User explicitly requests adding a repo to portfolio | probe-row-7 |
| show me my todos | QUERY | `list_todos_query` @0.99 | Direct request to display user's todo list | probe-row-8 |
| connect my calendar | GUIDANCE | `NONE` @0.95 | Calendar connection is setup/configuration, not a catalog op | probe-row-10 |
| what reminders do I have? | TEMPORAL | `list_reminders_query` @0.99 | Direct request to list reminders; matches canonical pattern. | probe-row-11 |
| hello | CONVERSATION | `greeting` @0.99 | Simple greeting; canonical conversation action. | probe-row-12 |
| goodbye | CONVERSATION | `farewell` @0.99 | User said goodbye; matches farewell conversation action. | probe-row-13 |
| thank you! | CONVERSATION | `thanks` @0.99 | User expressing gratitude; canonical conversation action. | probe-row-14 |
| what can you do? | DISCOVERY | `get_capabilities` @0.99 | Direct discovery question about assistant capabilities. | probe-row-15 |
| why did you suggest that? | PROVENANCE | `explain_suggestion` @0.95 | User asking for provenance/reasoning behind a suggestion. | probe-row-16 |
| why can't you create issues? | TRUST | `NONE` @0.95 | User asking about capability limitations; conversational/met | probe-row-17 |
| what do you remember about me? | MEMORY | `get_memory` @0.99 | Direct memory recall query matching canonical handler | probe-row-18 |
| what's my default repo? | QUERY | `get_default_repo` @0.99 | Direct query for default repository setting | probe-row-19 |
| set my default repo to mediajunkie/piper-morgan-product | EXECUTION | `set_default_repo` @0.99 | Explicit request to set default repo with owner/repo format. | probe-row-20 |
| write a short update for the CEO on the beta | SYNTHESIS | `write_stakeholder_update` @0.92 | User requests stakeholder update for executive audience on s | probe-row-21 |
| update the roadmap doc with the new dates | EXECUTION | `update_document` @0.85 | User requests document update via slot-filling pattern with  | probe-row-22 |
| tell me more about the github integration | QUERY | `get_feature_info` @0.95 | User requests detailed information about a specific feature. | probe-row-23 |
| who are you? | IDENTITY | `get_identity` @1.0 | Direct identity question matches canonical greeting/identity | probe-row-24 |
| show my recurring meetings | QUERY | `recurring_meetings` @0.99 | Direct match to recurring_meetings_query catalog operation. | probe-row-28 |
| what's my week look like? | QUERY | `week_calendar` @0.95 | Direct calendar query for weekly overview | probe-row-29 |
| what's the next milestone? | STATUS | `list_milestones` @0.85 | User asking for milestone information; list_milestones retri | probe-row-30 |
| what branch are we on? | QUERY | `local_git_status_query` @0.95 | Direct query about current Git branch status. | probe-row-31 |
| what did we ship this week? | QUERY | `shipped_this_week` @0.95 | Direct query about shipped items this week; matches _handle_ | probe-row-32 |
| show stale prs | QUERY | `stale_prs` @0.95 | Direct request to show stale pull requests. | probe-row-33 |
| close issue #123 | EXECUTION | `close_issue` @0.95 | User explicitly requests closing issue #123. | probe-row-34 |
| reopen issue #123 | EXECUTION | `reopen_issue` @0.95 | Clear reopen-issue request with issue number. | probe-row-35 |
| comment on issue #123 | EXECUTION | `comment_issue` @0.85 | User requests comment on specific issue; needs comment text  | probe-row-36 |
| how many open issues do we have? | QUERY | `list_issues` @0.95 | User asks for count of open issues; list_issues with open fi | probe-row-37 |
| show my prs | QUERY | `list_prs` @0.95 | User requests list of pull requests; direct match to list_pr | probe-row-38 |
| show issue #123 | QUERY | `review_issue` @0.95 | User requests to view/show a specific issue by number. | probe-row-39 |
| show milestones | QUERY | `list_milestones` @0.95 | User requests milestone list; direct match to list_milestone | probe-row-40 |
| what did we create this session? | QUERY | `session_activity_query` @0.95 | Direct match to session-activity recall example in catalog | probe-row-41 |
| what's my productivity? | QUERY | `productivity` @0.95 | Direct productivity query matching catalog operation. | probe-row-42 |
| remind me to review the roadmap tomorrow | EXECUTION | `create_reminder` @0.95 | Clear reminder creation request with task and time specified | probe-row-43 |
| complete todo 3 | EXECUTION | `complete_todo` @0.95 | User explicitly requests marking todo 3 as done. | probe-row-44 |
| show all my todos | QUERY | `list_todos_query` @0.99 | User explicitly requests to see all todos; direct match to l | probe-row-45 |
| what's my next todo? | QUERY | `list_todos_query` @0.95 | User asking for next todo item from their list | probe-row-46 |
| when did I complete the onboarding project? | STATUS | `check_completion_status` @0.92 | User asking when a specific project was completed—status/com | probe-row-47 |
| how do I get started? | GUIDANCE | `get_capabilities` @0.85 | User asking for onboarding/getting started guidance; discove | probe-row-49 |
| what's blocking the milestone? | ANALYSIS | `analyze_blockers` @0.95 | Direct match to blocker analysis query pattern | probe-row-50 |
| what are my priorities? | PRIORITY | `get_top_priority` @0.92 | User asking for prioritized work items; canonical priority q | probe-row-52 |
| Yes please | CONVERSATION | `CLARIFY` @0.0 | Affirmative response without prior context; cannot determine | exhibit-a/1529 (test_offer_binding_1529. |
| end standup | CONVERSATION | `NONE` @0.85 | Conversational command to end session; no catalog operation  | exhibit-a/1529 (test_offer_binding_1529. |
| i am not doing the standup right now. restore CoVa | PORTFOLIO | `NONE` @0.95 | User refuses standup and requests unknown action 'restore Co | exhibit-a/1529 (test_flow_escape_1529.py |
| delete my reminders | TEMPORAL | `CLARIFY` @0.45 | Ambiguous: delete all reminders, specific reminder(s), or cl | issue-1527 (greedy portfolio delete patt |
| hi piper, connect my github | EXECUTION | `manage_repos` @0.85 | User requests GitHub connection setup, portfolio management  | issue-1505 (multi-intent path drops the  |
| please clear the reminders except for "Review the PR" - | TEMPORAL | `CLARIFY` @0.65 | Two distinct operations requested: manage reminders (unclear | issue-1606 (PM live 2026-08-12: request  |
| are you able to set my default repo for me conversation | DISCOVERY | `NONE` @0.95 | User asking about capability/process, not requesting action | issue-1606 (interrogative parsed as impe |
| please mark 1, 2, 4, and 5 done | EXECUTION | `CLARIFY` @0.4 | Ambiguous: could mean mark todos #1,2,4,5 done OR mark issue | PM live 2026-08-12 (#1603 session; multi |

## Row detail (asserted rows)

| phrase | category | expected | router route @conf | verdict | note |
|---|---|---|---|---|---|
| give me my standup | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| what's on my calendar today? | TEMPORAL | action:meeting_time | `meeting_time` @0.92 | MATCH |  |
| when is my next meeting? | TEMPORAL | category:TEMPORAL | `meeting_time` @0.95 | MISMATCH |  |
| what am I working on? | STATUS | category:STATUS | `attention_query` @0.85 | MISMATCH |  |
| what should I focus on today? | PRIORITY | category:PRIORITY | `get_top_priority` @0.85 | MATCH |  |
| what are my top priorities? | PRIORITY | category:PRIORITY | `get_top_priority` @0.95 | MATCH |  |
| who am I? | IDENTITY | action:get_identity | `get_identity` @0.99 | MATCH |  |
| what's my role? | IDENTITY | category:IDENTITY | `get_identity` @0.85 | MATCH |  |
| how do I create a ticket? | GUIDANCE | category:GUIDANCE | `get_capabilities` @0.85 | MISMATCH |  |
| create a ticket for the login bug | EXECUTION | category:EXECUTION | `create_issue` @0.92 | MISMATCH |  |
| analyze the file I uploaded | QUERY | action:analyze_data | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| summarize the document | SYNTHESIS | category:SYNTHESIS | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| what time is it? | TEMPORAL | category:TEMPORAL | `get_current_time` @0.99 | MATCH |  |
| show my open issues | QUERY | action:list_issues_query | `list_issues` @0.95 | MATCH |  |
| show my open pull requests | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| any stale PRs? | QUERY | action:stale_prs_query | `stale_prs` @0.95 | MATCH |  |
| what needs my attention? | QUERY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what changed since yesterday? | QUERY | action:changes_query | `changes_query` @0.95 | MATCH |  |
| how productive was I this week? | QUERY | action:productivity_query | `productivity` @0.95 | MATCH |  |
| list my projects | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| close issue 42 | EXECUTION | action:close_issue_query | `close_issue` @0.95 | MATCH |  |
| comment on issue 42: looks good | EXECUTION | action:comment_issue_query | `comment_issue` @0.95 | MATCH |  |
| what have you learned about my workstyle? | MEMORY | action:pull_insights | `pull_insights` @0.95 | MATCH |  |
| set my default repo to acme/widgets | EXECUTION | action:set_default_repo | `set_default_repo` @0.99 | MATCH |  |
| what is my default repo? | QUERY | action:get_default_repo | `get_default_repo` @0.99 | MATCH |  |
| write a short update for the CEO on where we are | SYNTHESIS | action:write_stakeholder_update | `write_stakeholder_update` @0.92 | MATCH |  |
| update the project plan doc with the new dates | EXECUTION | action:update_document_query | `update_document` @0.85 | MATCH |  |
| give me a project status report | EXECUTION | action:update_issue | `generate_report` @0.85 | MISMATCH |  |
| can we connect my github? | QUERY | action:get_contextual_guidance | `manage_repos` @0.92 | MISMATCH |  |
| connect my slack | QUERY | action:get_contextual_guidance | `NONE` @0.95 | MISMATCH | NONE |
| link mediajunkie/test-piper-morgan to the project | QUERY | action:manage_repos | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| help me set up github | QUERY | action:get_contextual_guidance | `NONE` @0.85 | MISMATCH | NONE |
| list my archived projects | PORTFOLIO | action:manage_portfolio | `list_archived_projects` @0.99 | MISMATCH |  |
| what projects have I archived? | PORTFOLIO | action:list_archived_projects | `list_archived_projects` @0.95 | MATCH |  |
| what projects do I have? | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| remind me at 9:41 today to check in with the lead devel | TEMPORAL | action:create_reminder | `create_reminder` @0.98 | MATCH |  |
| Archive my project Test. | PORTFOLIO | action:manage_portfolio | `NONE` @0.85 | MISMATCH | NONE |
| Archive my project "Test" | PORTFOLIO | action:manage_portfolio | `NONE` @0.85 | MISMATCH | NONE |
| Archive the project called Test | PORTFOLIO | action:manage_portfolio | `NONE` @0.85 | MISMATCH | NONE |

---

## The 15 mismatches, decomposed (hand-authored analysis — understood, not just counted; everything above this rule is generator output)

Recorded as data per the Phase-1 brief: **no tuning was done in this pass.** The
families below are what the data says the next pass should look at — each is a
falsifiable claim about WHERE the miss lives, not an excuse for the number.

**Family 1 — grammar-description gaps (6 rows: Archive ×3, "connect my slack",
"can we connect my github?", "help me set up github").** The router never saw
that `manage_portfolio` covers archive/restore, or that
`get_contextual_guidance` is the integration-connect destination — the derived
catalog line for a registry-only operation is currently
`"<category> action (<disposition>-handled)"` plus one example. The router's
NONE @0.85 on "Archive my project Test." is the catalog failing to describe the
operation, not the model failing to read. The fix lane is richer
registry-derived descriptions (e.g. surfacing the canonical handler's operation
verbs as registry metadata) — a derivation improvement, never a hand-written
list. Same mechanism on the Exhibit-A "restore CoVa" row (rationale: "unknown
action 'restore CoVa'").

**Family 2 — registry-category artifacts (2 rows: "create a ticket for the
login bug" → `create_issue`, "when is my next meeting?" → `meeting_time`).**
The router picked operations a human reviewer would likely call CORRECT — but
the corpus asserts `category:EXECUTION` / `category:TEMPORAL`, and
`ACTION_REGISTRY` files `create_issue` and `meeting_time` under QUERY (rail-
migration history), so category-expectation scoring counts them as misses. This
is the `category:` scoring seam, not routing: an operation-emitting router is
being graded against category labels through a category map with historical
artifacts in it. Candidate Phase-0 follow-up: re-express these rows as
`action:` expectations.

**Family 3 — expectations already under review (2 rows).** "give me a project
status report" (expected `action:update_issue`) was flagged in the Phase-0
baseline doc itself as "a draft-era vocabulary artifact … candidate for
re-review" — the router's `generate_report` @0.85 is a defensible reading.
"list my archived projects" (expected `action:manage_portfolio`, which encodes
what production HAPPENS to do) drew the strictly more specific
`list_archived_projects` @0.99 — the same operation the corpus itself asserts
for the sibling phrasing "what projects have I archived?".

**Family 4 — honest abstentions under missing context/capability (5 rows).**
"analyze the file I uploaded" (CLARIFY — there is no uploaded file in a
context-free run), "summarize the document" (CLARIFY — the grammar has no
summarize operation by design: SUMMARIZE-TAXONOMY floors summaries), "link
mediajunkie/test-piper-morgan to the project" (CLARIFY), "what am I working
on?" (`attention_query` vs STATUS — a genuine near-neighbor disagreement),
"how do I create a ticket?" (`get_capabilities` vs GUIDANCE — near-neighbor).
Note the router's failure mode here is ASKING, not fabricating — 0 REFUSED,
0 ERROR, and no off-grammar emission in 93 calls is the enforced-vocabulary
property doing exactly what Arch ratified it for.

## Highlights the gate should read alongside the table

- ⭐ **Arch's demanded row passes the thesis test**: "what reminders do I
  have?" → `list_reminders_query` @0.99. The unconstrained LLM classifier
  misrouted this until the pre-classifier claimed it (stack doc, pin:
  reminder-query); the CONSTRAINED call routes it cleanly. (REVIEW row —
  informational, but it is the sharpest single data point in the run.)
- **Vocabulary drift was structurally absent**: 93/93 calls produced a valid
  grammar route on the first attempt (0 repairs, 0 REFUSED, 0 ERROR). The
  mode-4 disease (off-alias emissions) cannot occur by construction.
- **The 1529 context rows behaved as the context-carrying design predicts**:
  "Yes please" → CLARIFY (nothing to bind to without the pending-offer
  snapshot Phase 2 threads); "end standup" / "i am not doing the standup
  right now" → NONE with refusal-reading rationales. These are the rows the
  shadow observer's live SessionSnapshot exists for.
- **Cost**: 93 Haiku-class calls, zero retries — pennies, per the proposal's
  latency/cost case.
