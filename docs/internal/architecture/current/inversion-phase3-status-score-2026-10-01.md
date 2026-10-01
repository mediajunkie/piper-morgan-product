# Inversion Phase-1 shadow score — CONSTRAINED ROUTER vs Phase-0 baseline
Run: 2026-10-01 20:33Z · corpus: inversion_corpus_phase0.yaml (46 rows) · scripts/inversion_phase1_shadow_score.py
Served (#1620 — resolved, post-fallback, per row): anthropic:claude-haiku-4-5 (46/46)

LAYER (m-43): **router only, context-free** — one constrained Haiku-class call per row (46 LLM calls incl. repair retries; 0 ERROR, 0 REFUSED), grammar derived from the live registry at run time (64 canonical operations, 83 input-side aliases collapsed, + NONE/CLARIFY). The production chain was NOT executed in this run; the baseline column is Phase-0's FULL-CHAIN production decision (inversion-phase0-baseline-full-2026-08-12.md). Context-dependent rows (the 1529 offer/flow family) ran WITHOUT session state — their answers are informational for Phase 2, not its measured shape.

## Per-category vs baseline (denominators stated — m-44)

| category | rows | asserted | router match | baseline match | Δ | REVIEW | gate |
|---|---|---|---|---|---|---|---|
| STATUS | 46 | 46 | 15 | 1/4 | +14 | 0 | no regression |
| **TOTAL** | 46 | 46 | 15 | 36/39 | -21 | 0 | (aggregate is NOT the gate) |

Gate reading (Arch condition 1 as amended 08-09 08:3x, PPM): **no category may regress; the aggregate is never the gate** (the M2 precedent: 72.1% aggregate passed while a category was broken). CONVERSATION / DISCOVERY / PROVENANCE / TRUST / ANALYSIS have REVIEW-only denominators in Phase 0 and remain **ungateable** here — same as Phase 0 stated; growing asserted expectations there is outstanding Phase-0 work, not a Phase-1 scoring artifact.

⚠️ **m-44: the table above compares two different denominators** (this run's 116-row corpus vs the baseline's 93-row corpus) — its `Δ`/`gate` cells are INFORMATIONAL ONLY from this run forward. The shared-subset table below, scored on rows asserted in BOTH corpora, is the actual gate.

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
- [STATUS] time for my stand-up
- [STATUS] give me my stand up
- [STATUS] give me a standup update
- [STATUS] give me a standup report
- [STATUS] what's my daily standup
- [STATUS] show today's standup
- [STATUS] show me my portfolio
- [STATUS] list my active projects for this quarter
- [STATUS] any upcoming milestones for this project
- [STATUS] what's my current project
- [STATUS] can you summarize my current work
- [STATUS] what are my current projects
- [STATUS] give me a project overview
- [STATUS] what's the project landscape
- [STATUS] what projects am I working on
- [STATUS] tell me what I'm working on
- [STATUS] quick check, working on now?
- [STATUS] what are my active projects
- [STATUS] show my active work
- [STATUS] what's my status
- [STATUS] give me a status update
- [STATUS] what is my status
- [STATUS] what's my work status
- [STATUS] show the current status
- [STATUS] what's the current status
- [STATUS] I need a status report
- [STATUS] what's my progress
- [STATUS] give me a progress update
- [STATUS] I need a progress report
- [STATUS] what's the progress on this
- [STATUS] show today's progress
- [STATUS] what's the current progress
- [STATUS] how's the progress going
- [STATUS] what's the progress looking like
- [STATUS] what are my tasks
- [STATUS] show me my current tasks
- [STATUS] what are my active tasks
- [STATUS] show today's tasks
- [STATUS] list today's tasks
- [STATUS] tasks I'm actively working on
- [STATUS] what tasks do I have
- [STATUS] what's the task status
- [STATUS] what are my assignments
- [STATUS] show me my current assignments
- [STATUS] what's assigned to me
- [STATUS] show today's assignments

## Exhibit A (PM 2026-08-08 live transcript) + Arch's demanded row

Selection rule: corpus `source` containing one of ('exhibit-a', 'issue-1559', 'issue-1492') → 0 rows (the 8 Exhibit-A failures), plus the demanded row `"what reminders do I have?"` (probe-row-11, REVIEW — the sharpest test of the thesis: the LLM classifier misrouted it until the pre-classifier claimed it).

| phrase | expected | router route @conf | verdict | source |
|---|---|---|---|---|

## REVIEW rows — the router's answers as data (informational, unscored)

These 54 rows are the Inversion's question book (36 probe-DISAGREEs by construction + PM's live failures). Nothing here is scored; the router's answer is recorded so the questions accumulate evidence.

| phrase | category | router route @conf | rationale | source |
|---|---|---|---|---|

## Row detail (asserted rows)

| phrase | category | expected | router route @conf | verdict | note |
|---|---|---|---|---|---|
| time for my stand-up | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| give me my stand up | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| give me a standup update | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| give me a standup report | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| what's my daily standup | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| show today's standup | STATUS | action:show_standup | `show_standup` @0.95 | MATCH |  |
| show me my portfolio | STATUS | action:manage_portfolio | `manage_portfolio` @0.95 | MATCH |  |
| list my active projects for this quarter | STATUS | action:manage_portfolio | `manage_portfolio` @0.92 | MATCH |  |
| any upcoming milestones for this project | STATUS | action:get_project_status | `list_milestones` @0.85 | MISMATCH |  |
| what's my current project | STATUS | action:get_project_status | `NONE` @0.85 | MISMATCH | NONE |
| can you summarize my current work | STATUS | action:get_project_status | `NONE` @0.85 | MISMATCH | NONE |
| what are my current projects | STATUS | action:get_project_status | `manage_portfolio` @0.95 | MISMATCH |  |
| give me a project overview | STATUS | action:get_project_status | `get_project_status` @0.85 | MATCH |  |
| what's the project landscape | STATUS | action:get_project_status | `get_project_status` @0.72 | MATCH |  |
| what projects am I working on | STATUS | action:get_project_status | `manage_portfolio` @0.95 | MISMATCH |  |
| tell me what I'm working on | STATUS | action:get_project_status | `attention_query` @0.85 | MISMATCH |  |
| quick check, working on now? | STATUS | action:get_project_status | `session_activity_query` @0.72 | MISMATCH |  |
| what are my active projects | STATUS | action:get_project_status | `manage_portfolio` @0.95 | MISMATCH |  |
| show my active work | STATUS | action:get_project_status | `attention_query` @0.85 | MISMATCH |  |
| what's my status | STATUS | action:get_project_status | `get_project_status` @0.7 | MATCH |  |
| give me a status update | STATUS | action:get_project_status | `get_project_status` @0.85 | MATCH |  |
| what is my status | STATUS | action:get_project_status | `CLARIFY` @0.5 | MISMATCH | CLARIFY |
| what's my work status | STATUS | action:get_project_status | `CLARIFY` @0.6 | MISMATCH | CLARIFY |
| show the current status | STATUS | action:get_project_status | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| what's the current status | STATUS | action:get_project_status | `CLARIFY` @0.5 | MISMATCH | CLARIFY |
| I need a status report | STATUS | action:get_project_status | `generate_report` @0.85 | MISMATCH |  |
| what's my progress | STATUS | action:get_project_status | `CLARIFY` @0.6 | MISMATCH | CLARIFY |
| give me a progress update | STATUS | action:get_project_status | `get_project_status` @0.85 | MATCH |  |
| I need a progress report | STATUS | action:get_project_status | `generate_report` @0.85 | MISMATCH |  |
| what's the progress on this | STATUS | action:get_project_status | `CLARIFY` @0.3 | MISMATCH | CLARIFY |
| show today's progress | STATUS | action:get_project_status | `session_activity_query` @0.75 | MISMATCH |  |
| what's the current progress | STATUS | action:get_project_status | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| how's the progress going | STATUS | action:get_project_status | `get_project_status` @0.85 | MATCH |  |
| what's the progress looking like | STATUS | action:get_project_status | `get_project_status` @0.85 | MATCH |  |
| what are my tasks | STATUS | action:get_project_status | `list_todos_query` @0.95 | MISMATCH |  |
| show me my current tasks | STATUS | action:get_project_status | `list_todos_query` @0.95 | MISMATCH |  |
| what are my active tasks | STATUS | action:get_project_status | `list_todos_query` @0.95 | MISMATCH |  |
| show today's tasks | STATUS | action:get_project_status | `list_todos_query` @0.95 | MISMATCH |  |
| list today's tasks | STATUS | action:get_project_status | `list_todos_query` @0.95 | MISMATCH |  |
| tasks I'm actively working on | STATUS | action:get_project_status | `list_todos_query` @0.85 | MISMATCH |  |
| what tasks do I have | STATUS | action:get_project_status | `list_todos_query` @0.95 | MISMATCH |  |
| what's the task status | STATUS | action:get_project_status | `CLARIFY` @0.5 | MISMATCH | CLARIFY |
| what are my assignments | STATUS | action:get_project_status | `attention_query` @0.85 | MISMATCH |  |
| show me my current assignments | STATUS | action:get_project_status | `attention_query` @0.85 | MISMATCH |  |
| what's assigned to me | STATUS | action:get_project_status | `attention_query` @0.85 | MISMATCH |  |
| show today's assignments | STATUS | action:get_project_status | `meeting_time` @0.6 | MISMATCH |  |
