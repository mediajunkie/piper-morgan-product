# Inversion Phase-1 shadow score — CONSTRAINED ROUTER vs Phase-0 baseline
Run: 2026-10-01 20:11Z · corpus: inversion_corpus_phase0.yaml (53 rows) · scripts/inversion_phase1_shadow_score.py
Served (#1620 — resolved, post-fallback, per row): anthropic:claude-haiku-4-5 (53/53)

LAYER (m-43): **router only, context-free** — one constrained Haiku-class call per row (53 LLM calls incl. repair retries; 0 ERROR, 0 REFUSED), grammar derived from the live registry at run time (64 canonical operations, 83 input-side aliases collapsed, + NONE/CLARIFY). The production chain was NOT executed in this run; the baseline column is Phase-0's FULL-CHAIN production decision (inversion-phase0-baseline-full-2026-08-12.md). Context-dependent rows (the 1529 offer/flow family) ran WITHOUT session state — their answers are informational for Phase 2, not its measured shape.

## Per-category vs baseline (denominators stated — m-44)

| category | rows | asserted | router match | baseline match | Δ | REVIEW | gate |
|---|---|---|---|---|---|---|---|
| QUERY | 45 | 45 | 40 | 12/13 | +28 | 0 | no regression |
| EXECUTION | 8 | 8 | 5 | 5/6 | +0 | 0 | no regression |
| **TOTAL** | 53 | 53 | 45 | 36/39 | +9 | 0 | (aggregate is NOT the gate) |

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
- [EXECUTION] close the completed issue
- [EXECUTION] please close this issue
- [EXECUTION] re-open issue 88
- [EXECUTION] reopen the old issue
- [EXECUTION] re-open the old issue
- [EXECUTION] add comment to issue 99
- [EXECUTION] reply to issue 99
- [EXECUTION] comment on 99
- [QUERY] what shipped recently
- [QUERY] can you show what has shipped
- [QUERY] what has shipped this past week
- [QUERY] show our stale pull requests
- [QUERY] any old prs lying around
- [QUERY] prs needing review
- [QUERY] review issue 101
- [QUERY] issue 101 details
- [QUERY] get issue 101
- [QUERY] what are my issues
- [QUERY] list the issues please
- [QUERY] show the issues
- [QUERY] what's the issue count
- [QUERY] which issues are assigned to engineering
- [QUERY] show my pull requests
- [QUERY] what are my prs looking like
- [QUERY] where are my pull requests
- [QUERY] list the prs
- [QUERY] list all pull requests from this sprint
- [QUERY] any open prs waiting on me
- [QUERY] any prs assigned to me
- [QUERY] any pull requests assigned to me
- [QUERY] list the milestones for this quarter
- [QUERY] any update on the next milestone
- [QUERY] what milestones do we have
- [QUERY] milestones due this month
- [QUERY] when's the milestone deadline
- [QUERY] any recent releases
- [QUERY] show me the releases
- [QUERY] list our releases
- [QUERY] what version are we on
- [QUERY] what's the current release
- [QUERY] what's our latest release
- [QUERY] what labels do we use
- [QUERY] show me the labels
- [QUERY] list the labels
- [QUERY] what are the issue labels
- [QUERY] labels count please
- [QUERY] all labels please
- [QUERY] show me the active branches
- [QUERY] show which branches exist
- [QUERY] list the branches
- [QUERY] what feature branches do we have
- [QUERY] what are the current branches
- [QUERY] what branches do we have

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
| what shipped recently | QUERY | action:shipped_query | `shipped_this_week` @0.85 | MATCH |  |
| can you show what has shipped | QUERY | action:shipped_query | `shipped_this_week` @0.85 | MATCH |  |
| what has shipped this past week | QUERY | action:shipped_query | `shipped_this_week` @0.95 | MATCH |  |
| show our stale pull requests | QUERY | action:stale_prs_query | `stale_prs` @0.95 | MATCH |  |
| any old prs lying around | QUERY | action:stale_prs_query | `stale_prs` @0.95 | MATCH |  |
| prs needing review | QUERY | action:stale_prs_query | `list_prs` @0.95 | MISMATCH |  |
| close the completed issue | EXECUTION | action:close_issue_query | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| please close this issue | EXECUTION | action:close_issue_query | `close_issue` @0.6 | MATCH |  |
| re-open issue 88 | EXECUTION | action:reopen_issue_query | `reopen_issue` @0.95 | MATCH |  |
| reopen the old issue | EXECUTION | action:reopen_issue_query | `CLARIFY` @0.3 | MISMATCH | CLARIFY |
| re-open the old issue | EXECUTION | action:reopen_issue_query | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| add comment to issue 99 | EXECUTION | action:comment_issue_query | `comment_issue` @0.95 | MATCH |  |
| reply to issue 99 | EXECUTION | action:comment_issue_query | `comment_issue` @0.85 | MATCH |  |
| comment on 99 | EXECUTION | action:comment_issue_query | `comment_issue` @0.95 | MATCH |  |
| review issue 101 | QUERY | action:review_issue_query | `review_issue` @0.95 | MATCH |  |
| issue 101 details | QUERY | action:review_issue_query | `review_issue` @0.95 | MATCH |  |
| get issue 101 | QUERY | action:review_issue_query | `NONE` @0.95 | MISMATCH | NONE |
| what are my issues | QUERY | action:list_issues_query | `list_issues` @0.95 | MATCH |  |
| list the issues please | QUERY | action:list_issues_query | `list_issues` @0.95 | MATCH |  |
| show the issues | QUERY | action:list_issues_query | `list_issues` @0.95 | MATCH |  |
| what's the issue count | QUERY | action:list_issues_query | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| which issues are assigned to engineering | QUERY | action:list_issues_query | `list_issues` @0.85 | MATCH |  |
| show my pull requests | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| what are my prs looking like | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| where are my pull requests | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| list the prs | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| list all pull requests from this sprint | QUERY | action:list_prs_query | `list_prs` @0.85 | MATCH |  |
| any open prs waiting on me | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| any prs assigned to me | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| any pull requests assigned to me | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| list the milestones for this quarter | QUERY | action:list_milestones_query | `list_milestones` @0.95 | MATCH |  |
| any update on the next milestone | QUERY | action:review_issue_query | `get_project_status` @0.75 | MISMATCH |  |
| what milestones do we have | QUERY | action:list_milestones_query | `list_milestones` @0.95 | MATCH |  |
| milestones due this month | QUERY | action:list_milestones_query | `list_milestones` @0.95 | MATCH |  |
| when's the milestone deadline | QUERY | action:list_milestones_query | `list_milestones` @0.75 | MATCH |  |
| any recent releases | QUERY | action:list_releases_query | `list_releases` @0.95 | MATCH |  |
| show me the releases | QUERY | action:list_releases_query | `list_releases` @0.95 | MATCH |  |
| list our releases | QUERY | action:list_releases_query | `list_releases` @0.95 | MATCH |  |
| what version are we on | QUERY | action:review_issue_query | `local_git_status_query` @0.72 | MISMATCH |  |
| what's the current release | QUERY | action:list_releases_query | `list_releases` @0.85 | MATCH |  |
| what's our latest release | QUERY | action:list_releases_query | `list_releases` @0.95 | MATCH |  |
| what labels do we use | QUERY | action:list_labels_query | `list_labels` @0.95 | MATCH |  |
| show me the labels | QUERY | action:list_labels_query | `list_labels` @0.95 | MATCH |  |
| list the labels | QUERY | action:list_labels_query | `list_labels` @0.95 | MATCH |  |
| what are the issue labels | QUERY | action:list_labels_query | `list_labels` @0.95 | MATCH |  |
| labels count please | QUERY | action:list_labels_query | `list_labels` @0.85 | MATCH |  |
| all labels please | QUERY | action:list_labels_query | `list_labels` @0.95 | MATCH |  |
| show me the active branches | QUERY | action:list_branches_query | `list_branches` @0.92 | MATCH |  |
| show which branches exist | QUERY | action:list_branches_query | `list_branches` @0.95 | MATCH |  |
| list the branches | QUERY | action:list_branches_query | `list_branches` @0.95 | MATCH |  |
| what feature branches do we have | QUERY | action:list_branches_query | `list_branches` @0.85 | MATCH |  |
| what are the current branches | QUERY | action:list_branches_query | `list_branches` @0.95 | MATCH |  |
| what branches do we have | QUERY | action:list_branches_query | `list_branches` @0.95 | MATCH |  |
