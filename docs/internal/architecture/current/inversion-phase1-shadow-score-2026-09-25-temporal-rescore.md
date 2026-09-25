# Inversion Phase-1 shadow score — CONSTRAINED ROUTER vs Phase-0 baseline
Run: 2026-09-25 23:46Z · corpus: inversion_corpus_phase0.yaml (14 rows) · scripts/inversion_phase1_shadow_score.py
Served (#1620 — resolved, post-fallback, per row): openai:gpt-4o-mini (14/14)

LAYER (m-43): **router only, context-free** — one constrained Haiku-class call per row (14 LLM calls incl. repair retries; 0 ERROR, 0 REFUSED), grammar derived from the live registry at run time (64 canonical operations, 83 input-side aliases collapsed, + NONE/CLARIFY). The production chain was NOT executed in this run; the baseline column is Phase-0's FULL-CHAIN production decision (inversion-phase0-baseline-full-2026-08-12.md). Context-dependent rows (the 1529 offer/flow family) ran WITHOUT session state — their answers are informational for Phase 2, not its measured shape.

## Per-category vs baseline (denominators stated — m-44)

| category | rows | asserted | router match | baseline match | Δ | REVIEW | gate |
|---|---|---|---|---|---|---|---|
| TEMPORAL | 14 | 10 | 9 | 4/4 | +5 | 4 | no regression |
| **TOTAL** | 14 | 10 | 9 | 36/39 | -27 | 4 | (aggregate is NOT the gate) |

Gate reading (Arch condition 1 as amended 08-09 08:3x, PPM): **no category may regress; the aggregate is never the gate** (the M2 precedent: 72.1% aggregate passed while a category was broken). CONVERSATION / DISCOVERY / PROVENANCE / TRUST / ANALYSIS have REVIEW-only denominators in Phase 0 and remain **ungateable** here — same as Phase 0 stated; growing asserted expectations there is outstanding Phase-0 work, not a Phase-1 scoring artifact.

⚠️ **m-44: the table above compares two different denominators** (this run's 116-row corpus vs the baseline's 93-row corpus) — its `Δ`/`gate` cells are INFORMATIONAL ONLY from this run forward. The shared-subset table below, scored on rows asserted in BOTH corpora, is the actual gate.

## Shared-subset score vs 2026-08-12 baseline (m-44 fix — THIS is the gate)

Matching rule: phrase normalized (strip + collapse whitespace + casefold), exact match required; on a miss, fall back to an unambiguous ≥20-char prefix match in either direction (markdown row-detail tables truncate long phrases with no ellipsis, at different fixed lengths in different docs). Only rows asserted (non-REVIEW) on BOTH sides are scored here; the per-category table above compares two different denominators and is informational only from this point forward.

| category | shared asserted | router match | baseline match | gate |
|---|---|---|---|---|
| TEMPORAL | 4 | 4/4 | 4/4 | no regression |

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

Added (current-asserted, not in the 08-12 baseline):
- [TEMPORAL] remind me at 3pm tomorrow to review the PR
- [TEMPORAL] Remind me tomorrow at 3pm to review the PR
- [TEMPORAL] delete my hydrate reminder
- [TEMPORAL] remind me
- [TEMPORAL] add a reminder: test the safe clarification
- [TEMPORAL] please remind me: ask Lead how to test "outwardness disclosure" today

## Exhibit A (PM 2026-08-08 live transcript) + Arch's demanded row

Selection rule: corpus `source` containing one of ('exhibit-a', 'issue-1559', 'issue-1492') → 3 rows (the 8 Exhibit-A failures), plus the demanded row `"what reminders do I have?"` (probe-row-11, REVIEW — the sharpest test of the thesis: the LLM classifier misrouted it until the pre-classifier claimed it).

| phrase | expected | router route @conf | verdict | source |
|---|---|---|---|---|
| remind me at 3pm tomorrow to review the PR | action:create_reminder | `create_reminder` @1.0 | MATCH | issue-1559 (turn-1 PM verbatim, #1517 T4 2026-08 |
| remind me at 9:41 today to check in with the lead develope | action:create_reminder | `create_reminder` @1.0 | MATCH | issue-1559 (adjacency gap: 'remind me at <time>  |
| Remind me tomorrow at 3pm to review the PR | action:create_reminder | `create_reminder` @1.0 | MATCH | issue-1490 (PM 8/7 original verbatim: date-then- |
| what reminders do I have? | REVIEW | `list_reminders_query` @1.0 | REVIEW (informational) | probe-row-11 |

## REVIEW rows — the router's answers as data (informational, unscored)

These 54 rows are the Inversion's question book (36 probe-DISAGREEs by construction + PM's live failures). Nothing here is scored; the router's answer is recorded so the questions accumulate evidence.

| phrase | category | router route @conf | rationale | source |
|---|---|---|---|---|
| what reminders do I have? | TEMPORAL | `list_reminders_query` @1.0 | User is asking for their reminders. | probe-row-11 |
| delete my reminders | TEMPORAL | `delete_todo` @0.9 | User is requesting to delete reminders, interpreted as todos | issue-1527 (greedy portfolio delete patt |
| what time is it? also connect my github | TEMPORAL | `get_current_time` @0.9 | User asked for the current time. | issue-1755 (found during the 1505 fix, 2 |
| please clear the reminders except for "Review the PR" - | TEMPORAL | `delete_todo` @0.9 | User requested to clear reminders. | issue-1606 (PM live 2026-08-12: request  |

## Row detail (asserted rows)

| phrase | category | expected | router route @conf | verdict | note |
|---|---|---|---|---|---|
| what's on my calendar today? | TEMPORAL | action:meeting_time | `meeting_time` @1.0 | MATCH |  |
| when is my next meeting? | TEMPORAL | action:meeting_time | `meeting_time` @1.0 | MATCH |  |
| what time is it? | TEMPORAL | category:TEMPORAL | `get_current_time` @1.0 | MATCH |  |
| remind me at 3pm tomorrow to review the PR | TEMPORAL | action:create_reminder | `create_reminder` @1.0 | MATCH |  |
| remind me at 9:41 today to check in with the lead devel | TEMPORAL | action:create_reminder | `create_reminder` @1.0 | MATCH |  |
| Remind me tomorrow at 3pm to review the PR | TEMPORAL | action:create_reminder | `create_reminder` @1.0 | MATCH |  |
| delete my hydrate reminder | TEMPORAL | action:delete_todo | `delete_todo` @0.9 | MATCH |  |
| remind me | TEMPORAL | action:create_reminder | `CLARIFY` @0.8 | MISMATCH | CLARIFY |
| add a reminder: test the safe clarification | TEMPORAL | action:create_reminder | `create_reminder` @0.9 | MATCH |  |
| please remind me: ask Lead how to test "outwardness dis | TEMPORAL | action:create_reminder | `create_reminder` @1.0 | MATCH |  |

---
**Lead's read (2026-09-25 16:5x PT)**: partial run, TEMPORAL only (14 rows, 14 calls, PM-budgeted),
after `bdf9a06b1e` sharpened the `meeting_time` / `week_calendar` registry descriptions. On the
four rows shared with the 08-12 baseline the router is now **4/4** (was 3/4 this afternoon) —
`what's on my calendar today?` → `meeting_time` @1.0. The one asserted miss, bare `remind me` →
CLARIFY, is the honest route for a reminder with no task and no time. **`read_temporal` is
licensed to flip.** Served `openai:gpt-4o-mini` 14/14 (dev key's provider); the description change
is the only difference between the two runs.
