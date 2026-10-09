# Inversion Phase-1 shadow score — CONSTRAINED ROUTER vs Phase-0 baseline
Run: 2026-10-09 20:23Z · corpus: inversion_corpus_phase0.yaml (46 rows) · scripts/inversion_phase1_shadow_score.py
Served (#1620 — resolved, post-fallback, per row): anthropic:claude-haiku-4-5 (46/46)

LAYER (m-43): **router only, context-free** — one constrained Haiku-class call per row (46 LLM calls incl. repair retries; 0 ERROR, 0 REFUSED), grammar derived from the live registry at run time (72 canonical operations, 86 input-side aliases collapsed, + NONE/CLARIFY). The production chain was NOT executed in this run; the baseline column is Phase-0's FULL-CHAIN production decision (inversion-phase0-baseline-full-2026-08-12.md). Context-dependent rows (the 1529 offer/flow family) ran WITHOUT session state — their answers are informational for Phase 2, not its measured shape.

## Per-category vs baseline (denominators stated — m-44)

| category | rows | asserted | router match | baseline match | Δ | REVIEW | gate |
|---|---|---|---|---|---|---|---|
| EXECUTION | 14 | 14 | 7 | 5/6 | +2 | 0 | no regression |
| PORTFOLIO | 12 | 9 | 7 | 6/7 | +1 | 3 | no regression |
| PROVENANCE | 7 | 7 | 1 | 0/0 | +1 | 0 | no regression |
| IDENTITY | 5 | 5 | 4 | 2/2 | +2 | 0 | no regression |
| QUERY | 5 | 5 | 5 | 12/13 | -7 | 0 | **REGRESSION** |
| SYNTHESIS | 3 | 3 | 3 | 2/2 | +1 | 0 | no regression |
| **TOTAL** | 46 | 43 | 27 | 36/39 | -9 | 3 | (aggregate is NOT the gate) |

Gate reading (Arch condition 1 as amended 08-09 08:3x, PPM): **no category may regress; the aggregate is never the gate** (the M2 precedent: 72.1% aggregate passed while a category was broken). CONVERSATION / DISCOVERY / PROVENANCE / TRUST / ANALYSIS have REVIEW-only denominators in Phase 0 and remain **ungateable** here — same as Phase 0 stated; growing asserted expectations there is outstanding Phase-0 work, not a Phase-1 scoring artifact.

⚠️ **m-44: the table above compares two different denominators** (this run's 116-row corpus vs the baseline's 93-row corpus) — its `Δ`/`gate` cells are INFORMATIONAL ONLY from this run forward. The shared-subset table below, scored on rows asserted in BOTH corpora, is the actual gate.

🔴 **Per-category regressions vs baseline (informational totals comparison — see shared-subset table below for the gate)**: QUERY: 12→5

## Shared-subset score vs 2026-08-12 baseline (m-44 fix — THIS is the gate)

Matching rule: phrase normalized (strip + collapse whitespace + casefold), exact match required; on a miss, fall back to an unambiguous ≥20-char prefix match in either direction (markdown row-detail tables truncate long phrases with no ellipsis, at different fixed lengths in different docs). Only rows asserted (non-REVIEW) on BOTH sides are scored here; the per-category table above compares two different denominators and is informational only from this point forward.

| category | shared asserted | router match | baseline match | gate |
|---|---|---|---|---|

**Denominator deltas (m-44)** — rows in the 08-12 baseline no longer asserted in the current corpus (dropped), and rows asserted now that the baseline never saw (added). Neither is scored above; both are why the totals table's Δ column is informational, not the gate.

Dropped (baseline-asserted, not in current corpus):
- [EXECUTION] create a ticket for the login bug
- [EXECUTION] close issue 42
- [EXECUTION] comment on issue 42: looks good
- [EXECUTION] set my default repo to acme/widgets
- [EXECUTION] update the project plan doc with the new dates
- [EXECUTION] give me a project status report
- [GUIDANCE] how do I create a ticket?
- [IDENTITY] who am I?
- [IDENTITY] what's my role?
- [MEMORY] what have you learned about my workstyle?
- [PORTFOLIO] list my projects
- [PORTFOLIO] list my archived projects
- [PORTFOLIO] what projects have I archived?
- [PORTFOLIO] what projects do I have?
- [PORTFOLIO] Archive my project Test.
- [PORTFOLIO] Archive my project "Test"
- [PORTFOLIO] Archive the project called Test
- [PRIORITY] what should I focus on today?
- [PRIORITY] what are my top priorities?
- [QUERY] analyze the file I uploaded
- [QUERY] show my open issues
- [QUERY] show my open pull requests
- [QUERY] any stale PRs?
- [QUERY] what needs my attention?
- [QUERY] what changed since yesterday?
- [QUERY] how productive was I this week?
- [QUERY] what is my default repo?
- [QUERY] can we connect my github?
- [QUERY] connect my slack
- [QUERY] link mediajunkie/test-piper-morgan to the project
- [QUERY] help me set up github
- [STATUS] give me my standup
- [STATUS] what am I working on?
- [SYNTHESIS] summarize the document
- [SYNTHESIS] write a short update for the CEO on where we are
- [TEMPORAL] what's on my calendar today?
- [TEMPORAL] when is my next meeting?
- [TEMPORAL] what time is it?
- [TEMPORAL] remind me at 9:41 today to check in with the lead developer

Added (current-asserted, not in the 08-12 baseline):
- [EXECUTION] edit the meeting notes document
- [EXECUTION] modify the status document
- [EXECUTION] change the spec doc
- [EXECUTION] add to the notes document new items
- [EXECUTION] append to the log doc
- [EXECUTION] update project plan with new deadline
- [EXECUTION] edit the report with corrections
- [EXECUTION] modify the onboarding checklist with the new steps
- [EXECUTION] change the title of issue 108 to test new regressions
- [EXECUTION] finish todo about deployment
- [EXECUTION] Can we just mark done here?
- [EXECUTION] complete todo for the deploy checklist
- [EXECUTION] use mediajunkie/piper-morgan-product as my default repo
- [EXECUTION] make mediajunkie/piper-morgan-product my default repo
- [IDENTITY] what's your name
- [IDENTITY] your role
- [IDENTITY] what do you do
- [IDENTITY] tell me about yourself
- [IDENTITY] introduce yourself
- [PORTFOLIO] hide the project Beta
- [PORTFOLIO] put the old project away
- [PORTFOLIO] restore project Epsilon
- [PORTFOLIO] unarchive the old project
- [PORTFOLIO] bring back my archived project
- [PORTFOLIO] search projects for budget
- [PORTFOLIO] find project deadline
- [PORTFOLIO] add a new project
- [PORTFOLIO] I'd like to start a new project
- [PROVENANCE] Where did you get that from?
- [PROVENANCE] How did you know about that?
- [PROVENANCE] What made you mention the priority?
- [PROVENANCE] How do you know about my schedule?
- [PROVENANCE] Why is that on your list?
- [PROVENANCE] Based on what?
- [PROVENANCE] What's that based on?
- [QUERY] Tell me about Notion
- [QUERY] How does the Slack integration work?
- [QUERY] What is the Notion integration?
- [QUERY] I'd like to learn more about the GitHub integration.
- [QUERY] Can you give me information about the Slack integration?
- [SYNTHESIS] Draft a status update for the board
- [SYNTHESIS] Write something to send to Jake about the beta timeline
- [SYNTHESIS] I need a stakeholder update on the alpha program

## Exhibit A (PM 2026-08-08 live transcript) + Arch's demanded row

Selection rule: corpus `source` containing one of ('exhibit-a', 'issue-1559', 'issue-1492') → 0 rows (the 8 Exhibit-A failures), plus the demanded row `"what reminders do I have?"` (probe-row-11, REVIEW — the sharpest test of the thesis: the LLM classifier misrouted it until the pre-classifier claimed it).

| phrase | expected | router route @conf | verdict | source |
|---|---|---|---|---|

## REVIEW rows — the router's answers as data (informational, unscored)

These 54 rows are the Inversion's question book (36 probe-DISAGREEs by construction + PM's live failures). Nothing here is scored; the router's answer is recorded so the questions accumulate evidence.

| phrase | category | router route @conf | rationale | source |
|---|---|---|---|---|
| delete my project Gamma | PORTFOLIO | `archive_project` @0.85 | User asks to delete project; archive_project is the reversib | phase3-rule10/PORTFOLIO_PATTERNS tests/u |
| remove the project Delta | PORTFOLIO | `archive_project` @0.85 | User asks to remove project; archive is the reversible remov | phase3-rule10/PORTFOLIO_PATTERNS tests/u |
| get rid of my test project | PORTFOLIO | `archive_project` @0.92 | User wants to remove a project; archive is reversible and st | phase3-rule10/PORTFOLIO_PATTERNS tests/u |

## Row detail (asserted rows)

| phrase | category | expected | router route @conf | verdict | note |
|---|---|---|---|---|---|
| Where did you get that from? | PROVENANCE | action:explain_suggestion | `CLARIFY` @0.6 | MISMATCH | CLARIFY |
| How did you know about that? | PROVENANCE | action:explain_suggestion | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| What made you mention the priority? | PROVENANCE | action:explain_suggestion | `explain_suggestion` @0.92 | MATCH |  |
| How do you know about my schedule? | PROVENANCE | action:explain_suggestion | `explain_trust` @0.95 | MISMATCH |  |
| Why is that on your list? | PROVENANCE | action:explain_suggestion | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| Based on what? | PROVENANCE | action:explain_suggestion | `CLARIFY` @0.95 | MISMATCH | CLARIFY |
| What's that based on? | PROVENANCE | action:explain_suggestion | `CLARIFY` @0.5 | MISMATCH | CLARIFY |
| hide the project Beta | PORTFOLIO | action:archive_project | `archive_project` @0.95 | MATCH |  |
| put the old project away | PORTFOLIO | action:archive_project | `archive_project` @0.85 | MATCH |  |
| restore project Epsilon | PORTFOLIO | action:restore_project | `restore_project` @0.99 | MATCH |  |
| unarchive the old project | PORTFOLIO | action:restore_project | `restore_project` @0.95 | MATCH |  |
| bring back my archived project | PORTFOLIO | action:restore_project | `CLARIFY` @0.6 | MISMATCH | CLARIFY |
| search projects for budget | PORTFOLIO | action:search_projects | `search_projects` @0.99 | MATCH |  |
| find project deadline | PORTFOLIO | action:search_projects | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| add a new project | PORTFOLIO | action:add_project | `add_project` @0.95 | MATCH |  |
| I'd like to start a new project | PORTFOLIO | action:add_project | `add_project` @0.95 | MATCH |  |
| what's your name | IDENTITY | action:get_identity | `get_identity` @0.99 | MATCH |  |
| your role | IDENTITY | action:get_identity | `get_identity` @0.95 | MATCH |  |
| what do you do | IDENTITY | action:get_identity | `get_capabilities` @0.99 | MISMATCH |  |
| tell me about yourself | IDENTITY | action:get_identity | `get_identity` @0.95 | MATCH |  |
| introduce yourself | IDENTITY | action:get_identity | `get_identity` @0.99 | MATCH |  |
| edit the meeting notes document | EXECUTION | action:update_document_query | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| modify the status document | EXECUTION | action:update_document_query | `update_document` @0.85 | MATCH |  |
| change the spec doc | EXECUTION | action:update_document_query | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| add to the notes document new items | EXECUTION | action:update_document_query | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| append to the log doc | EXECUTION | action:update_document_query | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| update project plan with new deadline | EXECUTION | action:update_document_query | `update_document` @0.72 | MATCH |  |
| edit the report with corrections | EXECUTION | action:update_document_query | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| modify the onboarding checklist with the new steps | EXECUTION | action:update_document_query | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| change the title of issue 108 to test new regressions | EXECUTION | action:update_issue | `update_issue` @0.95 | MATCH |  |
| Tell me about Notion | QUERY | action:get_feature_info | `get_feature_info` @0.85 | MATCH |  |
| How does the Slack integration work? | QUERY | action:get_feature_info | `get_feature_info` @0.95 | MATCH |  |
| What is the Notion integration? | QUERY | action:get_feature_info | `get_feature_info` @0.95 | MATCH |  |
| I'd like to learn more about the GitHub integration. | QUERY | action:get_feature_info | `get_feature_info` @0.95 | MATCH |  |
| Can you give me information about the Slack integration | QUERY | action:get_feature_info | `get_feature_info` @0.95 | MATCH |  |
| Draft a status update for the board | SYNTHESIS | action:write_stakeholder_update | `write_stakeholder_update` @0.95 | MATCH |  |
| Write something to send to Jake about the beta timeline | SYNTHESIS | action:write_stakeholder_update | `write_stakeholder_update` @0.92 | MATCH |  |
| I need a stakeholder update on the alpha program | SYNTHESIS | action:write_stakeholder_update | `write_stakeholder_update` @0.85 | MATCH |  |
| finish todo about deployment | EXECUTION | action:complete_todo | `complete_todo` @0.95 | MATCH |  |
| Can we just mark done here? | EXECUTION | action:complete_todo | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| complete todo for the deploy checklist | EXECUTION | action:complete_todo | `complete_todo` @0.92 | MATCH |  |
| use mediajunkie/piper-morgan-product as my default repo | EXECUTION | action:set_default_repo | `set_default_repo` @0.99 | MATCH |  |
| make mediajunkie/piper-morgan-product my default repo | EXECUTION | action:set_default_repo | `set_default_repo` @0.99 | MATCH |  |
