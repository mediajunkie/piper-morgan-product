# Inversion Phase-1 shadow score — CONSTRAINED ROUTER vs Phase-0 baseline
Run: 2026-09-25 23:34Z · corpus: inversion_corpus_phase0.yaml (116 rows) · scripts/inversion_phase1_shadow_score.py
Served (#1620 — resolved, post-fallback, per row): openai:gpt-4o-mini (116/116)

LAYER (m-43): **router only, context-free** — one constrained Haiku-class call per row (117 LLM calls incl. repair retries; 0 ERROR, 0 REFUSED), grammar derived from the live registry at run time (64 canonical operations, 83 input-side aliases collapsed, + NONE/CLARIFY). The production chain was NOT executed in this run; the baseline column is Phase-0's FULL-CHAIN production decision (inversion-phase0-baseline-full-2026-08-12.md). Context-dependent rows (the 1529 offer/flow family) ran WITHOUT session state — their answers are informational for Phase 2, not its measured shape.

## Per-category vs baseline (denominators stated — m-44)

| category | rows | asserted | router match | baseline match | Δ | REVIEW | gate |
|---|---|---|---|---|---|---|---|
| QUERY | 31 | 13 | 11 | 12/13 | -1 | 18 | **REGRESSION** |
| EXECUTION | 18 | 8 | 7 | 5/6 | +2 | 10 | no regression |
| PORTFOLIO | 16 | 14 | 9 | 6/7 | +3 | 2 | no regression |
| TEMPORAL | 14 | 10 | 8 | 4/4 | +4 | 4 | no regression |
| STATUS | 8 | 4 | 3 | 1/4 | +2 | 4 | no regression |
| GUIDANCE | 6 | 1 | 0 | 1/1 | -1 | 5 | **REGRESSION** |
| CONVERSATION | 5 | 0 | 0 | 0/0 | — | 5 | **UNGATEABLE** (REVIEW-only denominator) |
| SYNTHESIS | 4 | 2 | 2 | 2/2 | +0 | 2 | no regression |
| PRIORITY | 3 | 2 | 2 | 2/2 | +0 | 1 | no regression |
| IDENTITY | 3 | 2 | 2 | 2/2 | +0 | 1 | no regression |
| MEMORY | 3 | 1 | 1 | 1/1 | +0 | 2 | no regression |
| DISCOVERY | 2 | 0 | 0 | 0/0 | — | 2 | **UNGATEABLE** (REVIEW-only denominator) |
| PROVENANCE | 1 | 0 | 0 | 0/0 | — | 1 | **UNGATEABLE** (REVIEW-only denominator) |
| TRUST | 1 | 0 | 0 | 0/0 | — | 1 | **UNGATEABLE** (REVIEW-only denominator) |
| ANALYSIS | 1 | 0 | 0 | 0/0 | — | 1 | **UNGATEABLE** (REVIEW-only denominator) |
| **TOTAL** | 116 | 57 | 45 | 36/39 | +9 | 59 | (aggregate is NOT the gate) |

Gate reading (Arch condition 1 as amended 08-09 08:3x, PPM): **no category may regress; the aggregate is never the gate** (the M2 precedent: 72.1% aggregate passed while a category was broken). CONVERSATION / DISCOVERY / PROVENANCE / TRUST / ANALYSIS have REVIEW-only denominators in Phase 0 and remain **ungateable** here — same as Phase 0 stated; growing asserted expectations there is outstanding Phase-0 work, not a Phase-1 scoring artifact.

🔴 **Per-category regressions vs baseline** (recorded as data — this run does not tune-until-green): QUERY: 12→11; GUIDANCE: 1→0

## Exhibit A (PM 2026-08-08 live transcript) + Arch's demanded row

Selection rule: corpus `source` containing one of ('exhibit-a', 'issue-1559', 'issue-1492') → 16 rows (the 8 Exhibit-A failures), plus the demanded row `"what reminders do I have?"` (probe-row-11, REVIEW — the sharpest test of the thesis: the LLM classifier misrouted it until the pre-classifier claimed it).

| phrase | expected | router route @conf | verdict | source |
|---|---|---|---|---|
| Yes please | REVIEW | `CLARIFY` @0.5 | REVIEW (informational) | exhibit-a/1529 (test_offer_binding_1529.py PM_YE |
| end standup | REVIEW | `CLARIFY` @0.8 | REVIEW (informational) | exhibit-a/1529 (test_offer_binding_1529.py PM_EN |
| i am not doing the standup right now. restore CoVa | REVIEW | `manage_portfolio` @0.9 | REVIEW (informational) | exhibit-a/1529 (test_flow_escape_1529.py PM_REFU |
| restore CoVa | action:manage_portfolio | `manage_portfolio` @0.9 | MATCH | exhibit-a/1529 (PM live 2026-08-08 13:22, v38 —  |
| Please list my archived projects | action:manage_portfolio | `list_archived_projects` @1.0 | MISMATCH | exhibit-a/1529 (PM live 2026-08-08 13:22, v38 —  |
| what projects do I have? | action:manage_portfolio | `list_projects` @1.0 | MISMATCH | exhibit-a/1530 (chat omitted active CoVa; wrong  |
| what are my projects? | action:manage_portfolio | `list_projects` @1.0 | MISMATCH | exhibit-a/1530 (PM live 2026-08-08 13:19, v38 —  |
| remind me at 3pm tomorrow to review the PR | action:create_reminder | `create_reminder` @1.0 | MATCH | issue-1559 (turn-1 PM verbatim, #1517 T4 2026-08 |
| remind me at 9:41 today to check in with the lead develope | action:create_reminder | `create_reminder` @1.0 | MATCH | issue-1559 (adjacency gap: 'remind me at <time>  |
| Remind me tomorrow at 3pm to review the PR | action:create_reminder | `create_reminder` @1.0 | MATCH | issue-1490 (PM 8/7 original verbatim: date-then- |
| Archive my project Test. | action:manage_portfolio | `manage_portfolio` @0.9 | MATCH | issue-1492 (trailing punctuation breaks extracti |
| Archive my project "Test" | action:manage_portfolio | `manage_portfolio` @0.9 | MATCH | issue-1492 (quoted name breaks extraction) |
| Archive the project called Test | action:manage_portfolio | `manage_portfolio` @0.9 | MATCH | issue-1492 ('called X' phrasing breaks extractio |
| Archive my Test project, please. | action:manage_portfolio | `manage_portfolio` @0.9 | MATCH | issue-1492 (PM 8/7 EXACT verbatim: adjective-pos |
| Archive my project called "Test" please | action:manage_portfolio | `manage_portfolio` @0.9 | MATCH | issue-1492 (PM 8/7 EXACT verbatim: quoted 'calle |
| archive CoVa | action:manage_portfolio | `manage_portfolio` @0.9 | MATCH | issue-1492 comment (PM live T6, 2026-08-08 13:19 |
| what reminders do I have? | REVIEW | `list_reminders_query` @1.0 | REVIEW (informational) | probe-row-11 |

## REVIEW rows — the router's answers as data (informational, unscored)

These 54 rows are the Inversion's question book (36 probe-DISAGREEs by construction + PM's live failures). Nothing here is scored; the router's answer is recorded so the questions accumulate evidence.

| phrase | category | router route @conf | rationale | source |
|---|---|---|---|---|
| can you clarify what you meant? | QUERY | `CLARIFY` @0.9 | User is asking for clarification, not a specific operation. | corpus-1283 |
| show me my archived projects | QUERY | `list_archived_projects` @1.0 | User requested a list of archived projects. | corpus-1283 + issue-1579 (PORTFOLIO list |
| what have you learned about my work style? | MEMORY | `pull_insights` @1.0 | User is asking about insights on work style. | probe-row-2 |
| connect my github | GUIDANCE | `get_contextual_guidance` @0.8 | User requests guidance on connecting GitHub. | probe-row-3 |
| connect my notion | GUIDANCE | `get_contextual_guidance` @0.9 | User requests guidance on connecting an integration. | probe-row-4 |
| link my google calendar | GUIDANCE | `get_contextual_guidance` @0.8 | User requests help with integration setup. | probe-row-6 |
| add a repo to my portfolio | PORTFOLIO | `manage_repos` @0.9 | User wants to add a repo, related to managing repos. | probe-row-7 |
| show me my todos | QUERY | `list_todos_query` @1.0 | User requested their todo list. | probe-row-8 |
| connect my calendar | GUIDANCE | `get_contextual_guidance` @0.9 | User requests guidance on connecting an integration. | probe-row-10 |
| what reminders do I have? | TEMPORAL | `list_reminders_query` @1.0 | User is asking for their reminder list. | probe-row-11 |
| hello | CONVERSATION | `greeting` @1.0 | User is initiating a conversation with a greeting. | probe-row-12 |
| goodbye | CONVERSATION | `farewell` @1.0 | User is saying goodbye. | probe-row-13 |
| thank you! | CONVERSATION | `thanks` @1.0 | User expressed gratitude. | probe-row-14 |
| what can you do? | DISCOVERY | `get_capabilities` @1.0 | User is asking about assistant's capabilities. | probe-row-15 |
| why did you suggest that? | PROVENANCE | `explain_suggestion` @1.0 | User is asking for explanation of a prior suggestion. | probe-row-16 |
| why can't you create issues? | TRUST | `get_capabilities` @0.9 | User is inquiring about assistant's capabilities. | probe-row-17 |
| what do you remember about me? | MEMORY | `get_memory` @1.0 | User is asking about stored context. | probe-row-18 |
| what's my default repo? | QUERY | `get_default_repo` @1.0 | User is asking for their default repository. | probe-row-19 |
| set my default repo to mediajunkie/piper-morgan-product | EXECUTION | `set_default_repo` @1.0 | User explicitly requests to set a default repo. | probe-row-20 |
| write a short update for the CEO on the beta | SYNTHESIS | `write_stakeholder_update` @0.9 | User requested a stakeholder update for the CEO. | probe-row-21 |
| update the roadmap doc with the new dates | EXECUTION | `update_document` @0.9 | User requests to update a specific document. | probe-row-22 |
| tell me more about the github integration | QUERY | `get_feature_info` @1.0 | User is asking for details about a specific feature. | probe-row-23 |
| who are you? | IDENTITY | `get_identity` @1.0 | User is asking about the assistant's role. | probe-row-24 |
| show my recurring meetings | QUERY | `recurring_meetings` @1.0 | User requested to see recurring meetings. | probe-row-28 |
| what's my week look like? | QUERY | `week_calendar` @1.0 | User is asking for their weekly schedule. | probe-row-29 |
| what's the next milestone? | STATUS | `list_milestones` @0.9 | User is asking about upcoming milestones. | probe-row-30 |
| what branch are we on? | QUERY | `local_git_status_query` @1.0 | User is asking for the current branch status. | probe-row-31 |
| what did we ship this week? | QUERY | `shipped_this_week` @1.0 | User is asking about shipments this week. | probe-row-32 |
| show stale prs | QUERY | `stale_prs` @1.0 | User explicitly requested to show stale pull requests. | probe-row-33 |
| close issue #123 | EXECUTION | `close_issue` @1.0 | User explicitly requested to close a specific issue. | probe-row-34 |
| reopen issue #123 | EXECUTION | `reopen_issue` @1.0 | User explicitly requests to reopen a specific issue. | probe-row-35 |
| comment on issue #123 | EXECUTION | `comment_issue` @1.0 | User explicitly requests to comment on a specific issue. | probe-row-36 |
| how many open issues do we have? | QUERY | `list_issues` @0.9 | User is inquiring about the count of open issues. | probe-row-37 |
| show my prs | QUERY | `list_prs` @0.9 | User is asking to see their pull requests. | probe-row-38 |
| show issue #123 | QUERY | `list_issues` @0.9 | User is asking to view a specific issue. | probe-row-39 |
| show milestones | QUERY | `list_milestones` @1.0 | User requested to show milestones. | probe-row-40 |
| what did we create this session? | QUERY | `session_activity_query` @1.0 | Directly matches the session activity recall query. | probe-row-41 |
| what's my productivity? | QUERY | `productivity` @1.0 | User is asking for a productivity query. | probe-row-42 |
| remind me to review the roadmap tomorrow | EXECUTION | `create_reminder` @1.0 | User requested to create a reminder for a specific task. | probe-row-43 |
| complete todo 3 | EXECUTION | `complete_todo` @1.0 | User explicitly requested to complete a specific todo. | probe-row-44 |
| show all my todos | QUERY | `list_todos_query` @1.0 | User requested to see their todos. | probe-row-45 |
| what's my next todo? | QUERY | `list_todos_query` @1.0 | User is asking for their next todo item. | probe-row-46 |
| when did I complete the onboarding project? | STATUS | `check_completion_status` @0.9 | User asks about completion history of a project. | probe-row-47 |
| how do I get started? | GUIDANCE | `get_contextual_guidance` @0.9 | User is asking for guidance on getting started. | probe-row-49 |
| what's blocking the milestone? | ANALYSIS | `analyze_blockers` @1.0 | User is asking about blockers for a milestone. | probe-row-50 |
| what are my priorities? | PRIORITY | `get_top_priority` @0.9 | User is asking about their priorities. | probe-row-52 |
| Yes please | CONVERSATION | `CLARIFY` @0.5 | User's intent is unclear without context. | exhibit-a/1529 (test_offer_binding_1529. |
| end standup | CONVERSATION | `CLARIFY` @0.8 | Unclear if user wants to end a standup meeting or something  | exhibit-a/1529 (test_offer_binding_1529. |
| i am not doing the standup right now. restore CoVa | PORTFOLIO | `manage_portfolio` @0.9 | User requested to restore a project named CoVa. | exhibit-a/1529 (test_flow_escape_1529.py |
| delete my reminders | TEMPORAL | `delete_todo` @0.9 | User requested to delete reminders, interpreted as deleting  | issue-1527 (greedy portfolio delete patt |
| hi piper, connect my github | EXECUTION | `get_contextual_guidance` @0.8 | User requests guidance on connecting GitHub. | issue-1505 (multi-intent path drops the  |
| what time is it? also connect my github | TEMPORAL | `get_current_time` @1.0 | User asked for the current time. | issue-1755 (found during the 1505 fix, 2 |
| please clear the reminders except for "Review the PR" - | TEMPORAL | `delete_todo` @0.9 | User requested to clear reminders. | issue-1606 (PM live 2026-08-12: request  |
| are you able to set my default repo for me conversation | DISCOVERY | `NONE` @1.0 | User is asking about capabilities, not requesting an action. | issue-1606 (interrogative parsed as impe |
| use the interview from now on | STATUS | `CLARIFY` @0.8 | Unclear if referring to a specific operation or context. | issue-1606 comment 2026-08-13 (PM 3:27-3 |
| use the standup interview format by default from now on | STATUS | `NONE` @1.0 | User request is a preference change, not an actionable opera | issue-1606 comment 2026-08-13 (floor imp |
| please mark issue #108 in the mediajunkie/test-piper-mo | EXECUTION | `complete_todo` @0.9 | User requests to mark an issue as complete. | issue-1606 comment 2026-08-13 (cross-dom |
| please mark 1, 2, 4, and 5 done | EXECUTION | `complete_todo` @0.9 | User requests to mark specific todos as done. | PM live 2026-08-12 (#1603 session; multi |
| Create a doc from this conversation | SYNTHESIS | `generate_content` @0.8 | User wants to create a document from conversation. | issue-1674 (canonical Q36 mode-4 drift,  |

## Row detail (asserted rows)

| phrase | category | expected | router route @conf | verdict | note |
|---|---|---|---|---|---|
| give me my standup | STATUS | action:show_standup | `show_standup` @1.0 | MATCH |  |
| what's on my calendar today? | TEMPORAL | action:meeting_time | `week_calendar` @0.9 | MISMATCH |  |
| when is my next meeting? | TEMPORAL | action:meeting_time | `meeting_time` @1.0 | MATCH |  |
| what am I working on? | STATUS | category:STATUS | `get_top_priority` @0.9 | MISMATCH |  |
| what should I focus on today? | PRIORITY | category:PRIORITY | `get_top_priority` @0.9 | MATCH |  |
| what are my top priorities? | PRIORITY | category:PRIORITY | `get_top_priority` @0.9 | MATCH |  |
| who am I? | IDENTITY | action:get_identity | `get_identity` @1.0 | MATCH |  |
| what's my role? | IDENTITY | category:IDENTITY | `get_identity` @1.0 | MATCH |  |
| how do I create a ticket? | GUIDANCE | category:GUIDANCE | `CLARIFY` @0.8 | MISMATCH | CLARIFY |
| create a ticket for the login bug | EXECUTION | action:create_issue | `create_issue` @0.9 | MATCH |  |
| analyze the file I uploaded | QUERY | action:analyze_data | `analyze_document` @0.9 | MISMATCH |  |
| summarize the document | SYNTHESIS | action:summarize_document | `summarize_document` @1.0 | MATCH |  |
| what time is it? | TEMPORAL | category:TEMPORAL | `get_current_time` @1.0 | MATCH |  |
| show my open issues | QUERY | action:list_issues_query | `list_issues` @0.9 | MATCH |  |
| show my open pull requests | QUERY | action:list_prs_query | `list_prs` @0.9 | MATCH |  |
| any stale PRs? | QUERY | action:stale_prs_query | `stale_prs` @1.0 | MATCH |  |
| what needs my attention? | QUERY | action:attention_query | `attention_query` @1.0 | MATCH |  |
| what changed since yesterday? | QUERY | action:changes_query | `changes_query` @1.0 | MATCH |  |
| how productive was I this week? | QUERY | action:productivity_query | `productivity` @0.9 | MATCH |  |
| list my projects | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @1.0 | MATCH |  |
| close issue 42 | EXECUTION | action:close_issue_query | `close_issue` @1.0 | MATCH |  |
| comment on issue 42: looks good | EXECUTION | action:comment_issue_query | `comment_issue` @1.0 | MATCH |  |
| what have you learned about my workstyle? | MEMORY | action:pull_insights | `pull_insights` @1.0 | MATCH |  |
| set my default repo to acme/widgets | EXECUTION | action:set_default_repo | `set_default_repo` @1.0 | MATCH |  |
| what is my default repo? | QUERY | action:get_default_repo | `get_default_repo` @1.0 | MATCH |  |
| write a short update for the CEO on where we are | SYNTHESIS | action:write_stakeholder_update | `write_stakeholder_update` @0.9 | MATCH |  |
| update the project plan doc with the new dates | EXECUTION | action:update_document_query | `update_document` @0.9 | MATCH |  |
| give me a project status report | EXECUTION | action:update_issue | `get_project_status` @1.0 | MISMATCH |  |
| can we connect my github? | QUERY | action:get_contextual_guidance | `get_contextual_guidance` @0.9 | MATCH |  |
| connect my slack | QUERY | action:get_contextual_guidance | `get_contextual_guidance` @0.9 | MATCH |  |
| link mediajunkie/test-piper-morgan to the project | QUERY | action:manage_repos | `manage_repos` @1.0 | MATCH |  |
| help me set up github | QUERY | action:get_contextual_guidance | `get_contextual_guidance` @0.9 | MATCH |  |
| list my archived projects | PORTFOLIO | action:manage_portfolio | `list_archived_projects` @1.0 | MISMATCH |  |
| what projects have I archived? | PORTFOLIO | action:list_archived_projects | `list_archived_projects` @1.0 | MATCH |  |
| show me all project plans | QUERY | action:search_documents | `list_projects` @0.9 | MISMATCH |  |
| do a standup | STATUS | action:show_standup | `show_standup` @0.9 | MATCH |  |
| let's do a standup | STATUS | action:show_standup | `show_standup` @0.9 | MATCH |  |
| restore CoVa | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.9 | MATCH |  |
| Please list my archived projects | PORTFOLIO | action:manage_portfolio | `list_archived_projects` @1.0 | MISMATCH |  |
| what projects do I have? | PORTFOLIO | action:manage_portfolio | `list_projects` @1.0 | MISMATCH |  |
| what are my projects? | PORTFOLIO | action:manage_portfolio | `list_projects` @1.0 | MISMATCH |  |
| remind me at 3pm tomorrow to review the PR | TEMPORAL | action:create_reminder | `create_reminder` @1.0 | MATCH |  |
| remind me at 9:41 today to check in with the lead devel | TEMPORAL | action:create_reminder | `create_reminder` @1.0 | MATCH |  |
| Remind me tomorrow at 3pm to review the PR | TEMPORAL | action:create_reminder | `create_reminder` @1.0 | MATCH |  |
| list my archive projects | PORTFOLIO | action:manage_portfolio | `list_archived_projects` @1.0 | MISMATCH |  |
| Archive my project Test. | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.9 | MATCH |  |
| Archive my project "Test" | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.9 | MATCH |  |
| Archive the project called Test | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.9 | MATCH |  |
| Archive my Test project, please. | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.9 | MATCH |  |
| Archive my project called "Test" please | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.9 | MATCH |  |
| archive CoVa | PORTFOLIO | action:manage_portfolio | `manage_portfolio` @0.9 | MATCH |  |
| delete my hydrate reminder | TEMPORAL | action:delete_todo | `delete_todo` @0.9 | MATCH |  |
| remind me | TEMPORAL | action:create_reminder | `CLARIFY` @0.8 | MISMATCH | CLARIFY |
| change the status of issue #108 to Done | EXECUTION | action:update_issue | `update_issue` @0.9 | MATCH |  |
| add a reminder: test the safe clarification | TEMPORAL | action:create_reminder | `create_reminder` @0.9 | MATCH |  |
| please remind me: ask Lead how to test "outwardness dis | TEMPORAL | action:create_reminder | `create_reminder` @1.0 | MATCH |  |
| add todo buy oat milk | EXECUTION | action:create_todo | `create_todo` @1.0 | MATCH |  |

---
## Lead's read (2026-09-25 16:4x PT) — what the numbers license, and what the gate column hides

**Denominator caveat on the gate column (m-44, in our own instrument).** `Δ` compares the router's
match count on the CURRENT corpus against the baseline's count on the 2026-08-12 corpus. The corpus
grew 108→116 today (and from 93 before that), so "TEMPORAL 8/10 vs 4/4, +4, no regression" is two
different denominators. On the FOUR rows the baseline actually asserted, the router matches
**3/4**: `what's on my calendar today?` → `week_calendar` (baseline and expectation:
`meeting_time`). That is a within-wave misroute (today's calendar rendered as the week) and, on
the shared denominator, a regression the column reports as an improvement. The script should score
the shared subset alongside the total; filed as a fix to the instrument, not to the ruling.

**Model served**: `openai:gpt-4o-mini` on all 116 rows — the developer key's default provider, not
the Haiku the docstring names. The live router follows the requesting user's own key (#1812), so
this run measured one provider. Not a reason to distrust the direction; a reason to say which one.

**Decisions this licenses** (each is one flag token; revert = remove it):
- `create_reminder` — asserted reminder rows 3/3 at @1.0 including #1559's verbatim; bare
  `remind me` → CLARIFY, which is honest. **Flip.**
- `read_strategic` — PRIORITY 2/2, the rest REVIEW-only; nothing asserted regresses. **Flip.**
- `read_temporal` — **HOLD** on the shared-denominator miss above. Cheap fix: the grammar derives
  operation descriptions from the registry, so sharpen `meeting_time` ("today / next / a specific
  day") vs `week_calendar` ("the week ahead") in their registry descriptions and re-score the 14
  TEMPORAL rows (14 calls). No pattern is touched.

**Corpus-expectation question, not a router defect** (5 of PORTFOLIO's 5 mismatches + 1 in QUERY):
the router picks `list_archived_projects` / `list_projects` where the corpus asserts the legacy
`manage_portfolio` (the pre-classifier's coarse destination, pinned in corpus-1283 row 137). The
#1570 rail keys ARE the intended destinations (corpus-1283 row 139 says so for the sibling
phrasing). Whether those rows' expectations move to the specific op is PPM/Arch's call; until then
PORTFOLIO's number under-reports the router.

**Genuine router misses to carry as corpus data**: `how do I create a ticket?` → CLARIFY (GUIDANCE
regression, 1/1 → 0/1); `show me all project plans` → `list_projects` (expected `search_documents`);
`what am I working on?` → `get_top_priority` (expected STATUS); `analyze the file I uploaded` →
`analyze_document` (expected `analyze_data`, both read_referent — near-synonym). `give me a project
status report` → `get_project_status` where the corpus asserts `update_issue` looks like a corpus
error, not a router one.
