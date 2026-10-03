# Inversion Phase-1 shadow score — CONSTRAINED ROUTER vs Phase-0 baseline
Run: 2026-10-03 02:12Z · corpus: inversion_corpus_phase0.yaml (13 rows) · scripts/inversion_phase1_shadow_score.py
Served (#1620 — resolved, post-fallback, per row): anthropic:claude-haiku-4-5 (13/13)

LAYER (m-43): **router only, context-free** — one constrained Haiku-class call per row (13 LLM calls incl. repair retries; 0 ERROR, 0 REFUSED), grammar derived from the live registry at run time (64 canonical operations, 83 input-side aliases collapsed, + NONE/CLARIFY). The production chain was NOT executed in this run; the baseline column is Phase-0's FULL-CHAIN production decision (inversion-phase0-baseline-full-2026-08-12.md). Context-dependent rows (the 1529 offer/flow family) ran WITHOUT session state — their answers are informational for Phase 2, not its measured shape.

## Per-category vs baseline (denominators stated — m-44)

| category | rows | asserted | router match | baseline match | Δ | REVIEW | gate |
|---|---|---|---|---|---|---|---|
| MEMORY | 13 | 13 | 8 | 1/1 | +7 | 0 | no regression |
| **TOTAL** | 13 | 13 | 8 | 36/39 | -28 | 0 | (aggregate is NOT the gate) |

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
- [MEMORY] what can you remember about our last conversation
- [MEMORY] do you remember my last project update
- [MEMORY] remember when we shipped the last release?
- [MEMORY] can you show my conversation history
- [MEMORY] our history together has been good
- [MEMORY] let's look at past conversations we've had
- [MEMORY] pull up my previous messages please
- [MEMORY] can I see the conversation log
- [MEMORY] find when I mentioned this bug before
- [MEMORY] search history for that conversation topic
- [MEMORY] what did we discuss in our last session
- [MEMORY] what we discussed yesterday was helpful
- [MEMORY] how long is your memory exactly

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
| what can you remember about our last conversation | MEMORY | action:get_memory | `get_memory` @0.95 | MATCH |  |
| do you remember my last project update | MEMORY | action:get_memory | `get_memory` @0.95 | MATCH |  |
| remember when we shipped the last release? | MEMORY | action:check_completion_status | `get_memory` @0.85 | MISMATCH |  |
| can you show my conversation history | MEMORY | action:get_memory | `get_memory` @0.95 | MATCH |  |
| our history together has been good | MEMORY | action:get_memory | `NONE` @0.95 | MISMATCH | NONE |
| let's look at past conversations we've had | MEMORY | action:get_memory | `get_memory` @0.95 | MATCH |  |
| pull up my previous messages please | MEMORY | action:get_memory | `get_memory` @0.95 | MATCH |  |
| can I see the conversation log | MEMORY | action:get_memory | `get_memory` @0.85 | MATCH |  |
| find when I mentioned this bug before | MEMORY | action:get_memory | `get_memory` @0.85 | MATCH |  |
| search history for that conversation topic | MEMORY | action:get_memory | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| what did we discuss in our last session | MEMORY | action:get_memory | `session_activity_query` @0.95 | MISMATCH |  |
| what we discussed yesterday was helpful | MEMORY | action:get_memory | `NONE` @0.95 | MISMATCH | NONE |
| how long is your memory exactly | MEMORY | action:get_memory | `get_memory` @0.92 | MATCH |  |
