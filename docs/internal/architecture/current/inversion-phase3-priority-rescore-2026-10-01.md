# Inversion Phase-1 shadow score — CONSTRAINED ROUTER vs Phase-0 baseline
Run: 2026-10-01 13:51Z · corpus: inversion_corpus_phase0.yaml (38 rows) · scripts/inversion_phase1_shadow_score.py
Served (#1620 — resolved, post-fallback, per row): openai:gpt-4o-mini (38/38)

LAYER (m-43): **router only, context-free** — one constrained Haiku-class call per row (38 LLM calls incl. repair retries; 0 ERROR, 0 REFUSED), grammar derived from the live registry at run time (64 canonical operations, 83 input-side aliases collapsed, + NONE/CLARIFY). The production chain was NOT executed in this run; the baseline column is Phase-0's FULL-CHAIN production decision (inversion-phase0-baseline-full-2026-08-12.md). Context-dependent rows (the 1529 offer/flow family) ran WITHOUT session state — their answers are informational for Phase 2, not its measured shape.

## Per-category vs baseline (denominators stated — m-44)

| category | rows | asserted | router match | baseline match | Δ | REVIEW | gate |
|---|---|---|---|---|---|---|---|
| PRIORITY | 38 | 38 | 35 | 2/2 | +33 | 0 | no regression |
| **TOTAL** | 38 | 38 | 35 | 36/39 | -1 | 0 | (aggregate is NOT the gate) |

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
- [PRIORITY] what's my top priority
- [PRIORITY] this is top priority for the team
- [PRIORITY] this is the highest priority item
- [PRIORITY] mark this as priority one
- [PRIORITY] show priorities for this sprint
- [PRIORITY] list priorities for the team
- [PRIORITY] what are my current priorities
- [PRIORITY] what are the key priorities this quarter
- [PRIORITY] what's most important right now
- [PRIORITY] what matters most this week
- [PRIORITY] what are the key tasks for this sprint
- [PRIORITY] what are the key items on my plate
- [PRIORITY] should i focus on the bug first
- [PRIORITY] what could I focus on
- [PRIORITY] where should my focus be today
- [PRIORITY] what are my focus areas this sprint
- [PRIORITY] let's focus on today's priorities
- [PRIORITY] what's my focus this week
- [PRIORITY] not sure what to focus next
- [PRIORITY] what's urgent right now
- [PRIORITY] what are my urgent tasks
- [PRIORITY] what are my urgent items
- [PRIORITY] what's my urgent work today
- [PRIORITY] what's the most urgent thing
- [PRIORITY] what needs my focus today
- [PRIORITY] what requires attention right now
- [PRIORITY] what's critical right now
- [PRIORITY] what are my critical tasks
- [PRIORITY] what are my critical items
- [PRIORITY] what's my critical work today
- [PRIORITY] what's the most critical thing
- [PRIORITY] what should I do first
- [PRIORITY] what should I tackle next
- [PRIORITY] what's next for me
- [PRIORITY] what should I review first
- [PRIORITY] which project should get my focus today
- [PRIORITY] which task should get my focus next
- [PRIORITY] not sure what to do about this

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
| what's my top priority | PRIORITY | action:get_top_priority | `get_top_priority` @1.0 | MATCH |  |
| this is top priority for the team | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| this is the highest priority item | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| mark this as priority one | PRIORITY | action:prioritize | `prioritize` @0.9 | MATCH |  |
| show priorities for this sprint | PRIORITY | floor | `get_top_priority` @0.9 | MISMATCH | OPERATION |
| list priorities for the team | PRIORITY | floor | `NONE` @1.0 | MATCH | NONE |
| what are my current priorities | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| what are the key priorities this quarter | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| what's most important right now | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| what matters most this week | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| what are the key tasks for this sprint | PRIORITY | floor | `NONE` @1.0 | MATCH | NONE |
| what are the key items on my plate | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| should i focus on the bug first | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| what could I focus on | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| where should my focus be today | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| what are my focus areas this sprint | PRIORITY | action:get_top_priority | `get_contextual_guidance` @0.9 | MISMATCH |  |
| let's focus on today's priorities | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| what's my focus this week | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| not sure what to focus next | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| what's urgent right now | PRIORITY | action:attention_query | `attention_query` @0.9 | MATCH |  |
| what are my urgent tasks | PRIORITY | action:attention_query | `attention_query` @0.9 | MATCH |  |
| what are my urgent items | PRIORITY | action:attention_query | `attention_query` @0.9 | MATCH |  |
| what's my urgent work today | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| what's the most urgent thing | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| what needs my focus today | PRIORITY | action:attention_query | `attention_query` @0.9 | MATCH |  |
| what requires attention right now | PRIORITY | action:attention_query | `attention_query` @1.0 | MATCH |  |
| what's critical right now | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| what are my critical tasks | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| what are my critical items | PRIORITY | action:attention_query | `attention_query` @0.9 | MATCH |  |
| what's my critical work today | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| what's the most critical thing | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| what should I do first | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| what should I tackle next | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| what's next for me | PRIORITY | action:get_top_priority | `get_contextual_guidance` @0.9 | MISMATCH |  |
| what should I review first | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| which project should get my focus today | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| which task should get my focus next | PRIORITY | action:get_top_priority | `get_top_priority` @0.9 | MATCH |  |
| not sure what to do about this | PRIORITY | action:get_contextual_guidance | `get_contextual_guidance` @0.9 | MATCH |  |
