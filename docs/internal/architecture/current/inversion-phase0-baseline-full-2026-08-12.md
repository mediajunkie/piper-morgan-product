# Inversion Phase-0 baseline — FULL CHAIN (production decision)
Run: 2026-08-12 19:42Z · corpus: inversion_corpus_phase0.yaml (93 rows) · scripts/inversion_phase0_baseline.py

LAYER (m-43): full classification chain — surface 1 where it claims, LLM otherwise. Rails/floor are downstream and NOT measured here.

## Per-category (denominators stated — m-44)

| category | rows | s1-claimed | asserted-expected | match | REVIEW (open questions) |
|---|---|---|---|---|---|
| QUERY | 30 | 26 | 12 | 12 | 18 |
| EXECUTION | 15 | 14 | 6 | 5 | 9 |
| PORTFOLIO | 9 | 7 | 7 | 6 | 2 |
| TEMPORAL | 7 | 6 | 4 | 4 | 3 |
| GUIDANCE | 6 | 5 | 1 | 1 | 5 |
| CONVERSATION | 5 | 3 | 0 | 0 | 5 |
| STATUS | 4 | 4 | 2 | 1 | 2 |
| PRIORITY | 3 | 3 | 2 | 2 | 1 |
| IDENTITY | 3 | 1 | 2 | 2 | 1 |
| SYNTHESIS | 3 | 2 | 2 | 2 | 1 |
| MEMORY | 3 | 3 | 1 | 1 | 2 |
| DISCOVERY | 2 | 2 | 0 | 0 | 2 |
| PROVENANCE | 1 | 1 | 0 | 0 | 1 |
| TRUST | 1 | 1 | 0 | 0 | 1 |
| ANALYSIS | 1 | 1 | 0 | 0 | 1 |
| **TOTAL** | 93 | 79 | 39 | 36 | 54 |

## Row detail

| phrase | category | expected | s1 | decision | verdict | source |
|---|---|---|---|---|---|---|
| give me my standup | STATUS | action:show_standup | status/get_project_status | status/get_project_status | MISMATCH | corpus-1283 + probe-row-1 |
| what's on my calendar today? | TEMPORAL | action:meeting_time | query/meeting_time | query/meeting_time | MATCH | corpus-1283 + probe-row-27 |
| when is my next meeting? | TEMPORAL | category:TEMPORAL | temporal/get_current_time | temporal/get_current_time | MATCH | corpus-1283 |
| what am I working on? | STATUS | category:STATUS | status/get_project_status | status/get_project_status | MATCH | corpus-1283 + probe-row-51 |
| what should I focus on today? | PRIORITY | category:PRIORITY | priority/get_top_priority | priority/get_top_priority | MATCH | corpus-1283 |
| what are my top priorities? | PRIORITY | category:PRIORITY | priority/get_top_priority | priority/get_top_priority | MATCH | corpus-1283 |
| who am I? | IDENTITY | action:get_identity | declined | identity/get_identity | MATCH | corpus-1283 |
| what's my role? | IDENTITY | category:IDENTITY | declined | identity/get_role | MATCH | corpus-1283 |
| how do I create a ticket? | GUIDANCE | category:GUIDANCE | declined | guidance/provide_guidance | MATCH | corpus-1283 |
| create a ticket for the login bug | EXECUTION | category:EXECUTION | declined | execution/create_ticket | MATCH | corpus-1283 |
| analyze the file I uploaded | QUERY | action:analyze_data | declined | analysis/analyze_data | MATCH | corpus-1283 |
| summarize the document | SYNTHESIS | category:SYNTHESIS | declined | synthesis/generate_summary | MATCH | corpus-1283 |
| what time is it? | TEMPORAL | category:TEMPORAL | temporal/get_current_time | temporal/get_current_time | MATCH | corpus-1283 + probe-row-48 |
| show my open issues | QUERY | action:list_issues_query | query/list_issues_query | query/list_issues_query | MATCH | corpus-1283 |
| show my open pull requests | QUERY | action:list_prs_query | query/list_prs_query | query/list_prs_query | MATCH | corpus-1283 |
| any stale PRs? | QUERY | action:stale_prs_query | declined | query/stale_prs_query | MATCH | corpus-1283 |
| what needs my attention? | QUERY | action:attention_query | query/attention_query | query/attention_query | MATCH | corpus-1283 + probe-row-26 |
| what changed since yesterday? | QUERY | action:changes_query | query/changes_query | query/changes_query | MATCH | corpus-1283 + probe-row-25 |
| how productive was I this week? | QUERY | action:productivity_query | declined | analysis/analyze_productivity | MATCH | corpus-1283 |
| list my projects | PORTFOLIO | action:manage_portfolio | portfolio/manage_portfolio | portfolio/manage_portfolio | MATCH | corpus-1283 + probe-row-9 |
| close issue 42 | EXECUTION | action:close_issue_query | query/close_issue_query | query/close_issue_query | MATCH | corpus-1283 |
| comment on issue 42: looks good | EXECUTION | action:comment_issue_query | query/comment_issue_query | query/comment_issue_query | MATCH | corpus-1283 |
| what have you learned about my workstyle? | MEMORY | action:pull_insights | memory/pull_insights | memory/pull_insights | MATCH | corpus-1283 |
| set my default repo to acme/widgets | EXECUTION | action:set_default_repo | query/set_default_repo | query/set_default_repo | MATCH | corpus-1283 |
| what is my default repo? | QUERY | action:get_default_repo | query/get_default_repo | query/get_default_repo | MATCH | corpus-1283 |
| write a short update for the CEO on where we are | SYNTHESIS | action:write_stakeholder_update | query/write_stakeholder_update | query/write_stakeholder_update | MATCH | corpus-1283 |
| update the project plan doc with the new dates | EXECUTION | action:update_document_query | query/update_document_query | query/update_document_query | MATCH | corpus-1283 |
| can you clarify what you meant? | QUERY | REVIEW | declined | conversation/clarification_needed | REVIEW | corpus-1283 |
| give me a project status report | EXECUTION | action:update_issue | status/get_project_status | status/get_project_status | MISMATCH | corpus-1283 |
| can we connect my github? | QUERY | action:get_contextual_guidance | guidance/get_contextual_guidance | guidance/get_contextual_guidance | MATCH | corpus-1283 |
| connect my slack | QUERY | action:get_contextual_guidance | guidance/get_contextual_guidance | guidance/get_contextual_guidance | MATCH | corpus-1283 + probe-row-5 |
| link mediajunkie/test-piper-morgan to the project | QUERY | action:manage_repos | portfolio/manage_repos | portfolio/manage_repos | MATCH | corpus-1283 |
| help me set up github | QUERY | action:get_contextual_guidance | guidance/get_contextual_guidance | guidance/get_contextual_guidance | MATCH | corpus-1283 |
| show me my archived projects | QUERY | REVIEW | status/get_project_status | status/get_project_status | REVIEW | corpus-1283 + issue-1579 (PORTFOLIO list pattern r |
| list my archived projects | PORTFOLIO | action:manage_portfolio | portfolio/manage_portfolio | portfolio/manage_portfolio | MATCH | corpus-1283 + issue-1579 (the working sibling phra |
| what projects have I archived? | PORTFOLIO | action:list_archived_projects | declined | query/manage_portfolio | MISMATCH | corpus-1283 |
| what have you learned about my work style? | MEMORY | REVIEW | memory/pull_insights | memory/pull_insights | REVIEW | probe-row-2 |
| connect my github | GUIDANCE | REVIEW | guidance/get_contextual_guidance | guidance/get_contextual_guidance | REVIEW | probe-row-3 |
| connect my notion | GUIDANCE | REVIEW | guidance/get_contextual_guidance | guidance/get_contextual_guidance | REVIEW | probe-row-4 |
| link my google calendar | GUIDANCE | REVIEW | guidance/get_contextual_guidance | guidance/get_contextual_guidance | REVIEW | probe-row-6 |
| add a repo to my portfolio | PORTFOLIO | REVIEW | portfolio/manage_repos | portfolio/manage_repos | REVIEW | probe-row-7 |
| show me my todos | QUERY | REVIEW | query/list_todos_query | query/list_todos_query | REVIEW | probe-row-8 |
| connect my calendar | GUIDANCE | REVIEW | guidance/get_contextual_guidance | guidance/get_contextual_guidance | REVIEW | probe-row-10 |
| what reminders do I have? | TEMPORAL | REVIEW | query/list_reminders_query | query/list_reminders_query | REVIEW | probe-row-11 |
| hello | CONVERSATION | REVIEW | conversation/greeting | conversation/greeting | REVIEW | probe-row-12 |
| goodbye | CONVERSATION | REVIEW | conversation/farewell | conversation/farewell | REVIEW | probe-row-13 |
| thank you! | CONVERSATION | REVIEW | conversation/thanks | conversation/thanks | REVIEW | probe-row-14 |
| what can you do? | DISCOVERY | REVIEW | discovery/get_capabilities | discovery/get_capabilities | REVIEW | probe-row-15 |
| why did you suggest that? | PROVENANCE | REVIEW | provenance/explain_suggestion | provenance/explain_suggestion | REVIEW | probe-row-16 |
| why can't you create issues? | TRUST | REVIEW | trust/explain_trust | trust/explain_trust | REVIEW | probe-row-17 |
| what do you remember about me? | MEMORY | REVIEW | memory/get_memory | memory/get_memory | REVIEW | probe-row-18 |
| what's my default repo? | QUERY | REVIEW | query/get_default_repo | query/get_default_repo | REVIEW | probe-row-19 |
| set my default repo to mediajunkie/piper-morgan-product | EXECUTION | REVIEW | query/set_default_repo | query/set_default_repo | REVIEW | probe-row-20 |
| write a short update for the CEO on the beta | SYNTHESIS | REVIEW | query/write_stakeholder_update | query/write_stakeholder_update | REVIEW | probe-row-21 |
| update the roadmap doc with the new dates | EXECUTION | REVIEW | query/update_document_query | query/update_document_query | REVIEW | probe-row-22 |
| tell me more about the github integration | QUERY | REVIEW | query/get_feature_info | query/get_feature_info | REVIEW | probe-row-23 |
| who are you? | IDENTITY | REVIEW | identity/get_identity | identity/get_identity | REVIEW | probe-row-24 |
| show my recurring meetings | QUERY | REVIEW | query/recurring_meetings | query/recurring_meetings | REVIEW | probe-row-28 |
| what's my week look like? | QUERY | REVIEW | query/week_calendar | query/week_calendar | REVIEW | probe-row-29 |
| what's the next milestone? | STATUS | REVIEW | status/get_project_status | status/get_project_status | REVIEW | probe-row-30 |
| what branch are we on? | QUERY | REVIEW | query/local_git_status_query | query/local_git_status_query | REVIEW | probe-row-31 |
| what did we ship this week? | QUERY | REVIEW | query/shipped_query | query/shipped_query | REVIEW | probe-row-32 |
| show stale prs | QUERY | REVIEW | query/stale_prs_query | query/stale_prs_query | REVIEW | probe-row-33 |
| close issue #123 | EXECUTION | REVIEW | query/close_issue_query | query/close_issue_query | REVIEW | probe-row-34 |
| reopen issue #123 | EXECUTION | REVIEW | query/reopen_issue_query | query/reopen_issue_query | REVIEW | probe-row-35 |
| comment on issue #123 | EXECUTION | REVIEW | query/comment_issue_query | query/comment_issue_query | REVIEW | probe-row-36 |
| how many open issues do we have? | QUERY | REVIEW | query/list_issues_query | query/list_issues_query | REVIEW | probe-row-37 |
| show my prs | QUERY | REVIEW | query/list_prs_query | query/list_prs_query | REVIEW | probe-row-38 |
| show issue #123 | QUERY | REVIEW | query/review_issue_query | query/review_issue_query | REVIEW | probe-row-39 |
| show milestones | QUERY | REVIEW | query/review_issue_query | query/review_issue_query | REVIEW | probe-row-40 |
| what did we create this session? | QUERY | REVIEW | query/session_activity_query | query/session_activity_query | REVIEW | probe-row-41 |
| what's my productivity? | QUERY | REVIEW | query/productivity_query | query/productivity_query | REVIEW | probe-row-42 |
| remind me to review the roadmap tomorrow | EXECUTION | REVIEW | execution/create_reminder | execution/create_reminder | REVIEW | probe-row-43 |
| complete todo 3 | EXECUTION | REVIEW | execution/complete_todo | execution/complete_todo | REVIEW | probe-row-44 |
| show all my todos | QUERY | REVIEW | query/list_completed_todos | query/list_completed_todos | REVIEW | probe-row-45 |
| what's my next todo? | QUERY | REVIEW | query/next_todo_query | query/next_todo_query | REVIEW | probe-row-46 |
| when did I complete the onboarding project? | STATUS | REVIEW | status/check_completion_status | status/check_completion_status | REVIEW | probe-row-47 |
| how do I get started? | GUIDANCE | REVIEW | guidance/get_contextual_guidance | guidance/get_contextual_guidance | REVIEW | probe-row-49 |
| what's blocking the milestone? | ANALYSIS | REVIEW | analysis/analyze_blockers | analysis/analyze_blockers | REVIEW | probe-row-50 |
| what are my priorities? | PRIORITY | REVIEW | priority/get_top_priority | priority/get_top_priority | REVIEW | probe-row-52 |
| Yes please | CONVERSATION | REVIEW | declined | conversation/clarification_needed | REVIEW | exhibit-a/1529 (test_offer_binding_1529.py PM_YES_ |
| end standup | CONVERSATION | REVIEW | declined | execution/complete_todo | REVIEW | exhibit-a/1529 (test_offer_binding_1529.py PM_END_ |
| i am not doing the standup right now. restore CoVa | PORTFOLIO | REVIEW | portfolio/manage_portfolio | portfolio/manage_portfolio | REVIEW | exhibit-a/1529 (test_flow_escape_1529.py PM_REFUSA |
| what projects do I have? | PORTFOLIO | action:manage_portfolio | declined | query/manage_portfolio | MATCH | exhibit-a/1530 (chat omitted active CoVa; wrong so |
| remind me at 9:41 today to check in with the lead developer | TEMPORAL | action:create_reminder | declined | execution/set_reminder | MATCH | issue-1559 (adjacency gap: 'remind me at <time> <d |
| Archive my project Test. | PORTFOLIO | action:manage_portfolio | portfolio/manage_portfolio | portfolio/manage_portfolio | MATCH | issue-1492 (trailing punctuation breaks extraction |
| Archive my project "Test" | PORTFOLIO | action:manage_portfolio | portfolio/manage_portfolio | portfolio/manage_portfolio | MATCH | issue-1492 (quoted name breaks extraction) |
| Archive the project called Test | PORTFOLIO | action:manage_portfolio | portfolio/manage_portfolio | portfolio/manage_portfolio | MATCH | issue-1492 ('called X' phrasing breaks extraction) |
| delete my reminders | TEMPORAL | REVIEW | portfolio/manage_portfolio | portfolio/manage_portfolio | REVIEW | issue-1527 (greedy portfolio delete pattern claims |
| hi piper, connect my github | EXECUTION | REVIEW | guidance/get_contextual_guidance | guidance/get_contextual_guidance | REVIEW | issue-1505 (multi-intent path drops the connect as |
| please clear the reminders except for "Review the PR" - also | TEMPORAL | REVIEW | query/set_default_repo | query/set_default_repo | REVIEW | issue-1606 (PM live 2026-08-12: request 1 dropped; |
| are you able to set my default repo for me conversationally? | DISCOVERY | REVIEW | query/set_default_repo | query/set_default_repo | REVIEW | issue-1606 (interrogative parsed as imperative-wit |
| please mark 1, 2, 4, and 5 done | EXECUTION | REVIEW | execution/complete_todo | execution/complete_todo | REVIEW | PM live 2026-08-12 (#1603 session; multi-ordinal c |

## The three residual mismatches, each understood (not just counted)

1. **"give me my standup"** — routes to the derived standup DOWNSTREAM of classification
   (inside the STATUS handler, #1269's branch). corpus-1283's own seam annotation says a
   classification-layer probe reports this row as informational, never FAIL. **Runner
   refinement queued**: carry `seam:` through the builder and report seam rows separately.
2. **"give me a project status report"** — corpus-1283 asserts `action:update_issue`, which
   reads as a draft-era vocabulary artifact (run-1 calibrated most rows; this one looks
   uncalibrated). **Candidate for re-review, not a routing defect.**
3. **"what projects have I archived?"** — the genuine gap: the #1579/#1580 archived-list
   reachability family, a phrasing variant of PM's live failure. This one is real corpus
   material and stays a MISMATCH on merit.

## Reading this baseline (the whole point of per-category)

The aggregate (36/39) is NOT the gate — **no category may regress** (Arch condition 1 as
amended; the M2 precedent: 72.1% aggregate passed while IDENTITY CONTEXT scored 1).
CONVERSATION/DISCOVERY/PROVENANCE/TRUST/ANALYSIS have **zero asserted rows** — their
denominators are REVIEW-only, so those categories currently CANNOT be gated. Growing
asserted expectations in those categories is Phase-0 remaining work, not a scoring detail.

54 REVIEW rows are the Inversion's question book: 36 probe-DISAGREEs plus PM's live
failures. Phase 1's shadow scoring answers them; nothing in Phase 0 asserts them.
