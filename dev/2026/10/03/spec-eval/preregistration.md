---
type: preregistration
title: "Spec evaluation: pre-registered metrics and thresholds"
date: 2026-10-03
written: before any D0 script was run
rule: Do not edit after D0 starts. Any change is appended under "Amendments" with date and reason; the original text stays.
---

# Pre-registration

All measurements use the snapshot SHAs in `snapshot.md`. "Product change" (PC) means a non-merge
commit that touches `services/`, `web/`, `templates/`, `alembic/`, `main.py`, or `cli/`. Commits
that only touch `tests/` count as a separate series, TC. Months are calendar months, UTC.

Baseline window **B = 2026-01-01 → 2026-03-31**: the period before the cohort scaled up, when commits were
under 500/month. Recent window **R = 2026-08-01 → 2026-09-30**.

**Known confound (stated in advance):** model generations changed during the period. Opus/Sonnet
releases happened inside the 2025-06 → 2026-10 span. A change in quality or throughput can come from
better models rather than from process. D0 marks known model-release dates on every time series. A
hypothesis verdict that the model timeline explains equally well is reported as **inconclusive**.

## H1: coordination cost dominates
- **M1.1** Product throughput per month: PC count, and the lines added+deleted in PC commits under
  product paths.
- **M1.2** Coordination volume per month: commits whose subject starts with mail / log / hb /
  hb-last-invoked / stop / heartbeat, plus merge commits. Separately, bytes added under `mailboxes/`
  and `dev/` (dated session logs, `dev/active/`).
- **M1.3** Token proxy: bytes added under `mailboxes/` + `dev/` + `docs/briefing/` per month ÷ 4 ≈ tokens
  written. Read cost is estimated separately by D-measure (session-start load per role × fires).
- **M1.4** PM-attention proxy: memos delivered to `mailboxes/xian (ceo)/inbox/` per week, plus items
  in attention rollups, where those can be counted.
- **Ratio** C/P = M1.2 commits ÷ PC per month; also M1.2 bytes ÷ PC lines.
- **Supported if both hold:** (a) mean C/P in R is ≥ 2× mean C/P in B, **and** (b) PC/month in R grew by
  less than half as much as M1.2/month did (growth measured as the R-mean ÷ B-mean ratio).
- **Refuted if** C/P in R is ≤ 1.25× B, or PC growth ≥ coordination growth.
- Anything in between: **partially supported**, reported with the numbers.

## H1b: redundancy (PM-added)
- **M1b.1** Shared reading: for each document loaded at session start or by the duty-cycle skill,
  how many roles load it × its token size, against the total session-start load. Source: D-measure.
- **M1b.2** Overlapping PM-facing recurring outputs: list every recurring artifact addressed to PM
  (rollups, Weekly Ship, current-state, digests, Cowork jobs if PM/Exec provide an inventory) with
  cadence and topics. Two outputs overlap if more than half their topic headings recur in the other
  within the same week. Measured on a sample of ≥ 2 weeks.
- **M1b.3** Duplicate watchers: mechanisms that monitor the same signal (liveness, staleness,
  merges, CI).
- **Supported if any two hold:** ≥ 3 overlapping PM-facing outputs; ≥ 2 signals each watched by ≥ 2
  mechanisms with no distinct failure mode between them; per-role session-start load where the
  role-specific share is < 25% (everything else shared).
- **Unobservable from the repo:** Cowork jobs scheduled on PM's machine. They go on the unobservables list.

## H2: the ruleset is costly and a poor fit for current models
- **M2.1** Tokens loaded automatically at session start for a typical role (CLAUDE.md, imported
  files, the role briefing the protocol requires, hook output). Counted with a tokenizer
  approximation of chars ÷ 4, with the method stated.
- **M2.2** Defects in the ruleset: contradictions, stale paths or references, and rules superseded but still
  present. Combines D-measure's grep results and `/checkup prompt-audit` findings, deduplicated.
- **M2.3** Narrative share: the fraction of CLAUDE.md lines that are incident history, dates, or rationale
  rather than an instruction. Classified on all 745 lines (D-measure); the classifier's rule is
  written into its output.
- **M2.4** Rules that don't hold: rules marked HARD, CRITICAL, NEVER, or MANDATORY that were violated
  again after being written, per history and logs.
- **Supported if** M2.1 ≥ 20k tokens **and** at least two of: M2.2 ≥ 15 items; M2.3 ≥ 40%; M2.4 ≥ 5 rules.
- **Refuted if** M2.1 < 12k and M2.2 < 5.

## H3: docs have drifted from reality
- **M3.1** The claims ledger (L): a stratified sample of **n ≥ 40** checkable factual claims. Strata:
  BRIEFING-CURRENT-STATE, README / PROJECT, architecture docs, roadmap/vision, CLAUDE.md
  operational facts. Each is rated holds / partly / false / uncheckable against A, B, C, D0 evidence or
  a direct check.
- **Supported if** fewer than 80% of the checkable claims hold fully. **Refuted if** ≥ 90% hold.

## H4: the process buys the quality (counter-hypothesis)
- **Defect signals per month, normalized per PC:**
  - (d1) reverts: subject starts with "Revert" or contains "revert";
  - (d2) fix-on-fix: a `fix` commit touching a file that a `feat`/`fix` commit touched in the previous 72h;
  - (d3) issues reopened, if the GitHub API allows;
  - (d4) bug-labelled issues opened.
- **Mechanism introduction dates**, determined from git by D0: first mailbox commit; first
  duty-cycle-tick skill commit; hooks added under `.claude/hooks`; CLAUDE.md growth spurts (any month
  with > 25% growth).
- **Interrupted time series:** compare 60 days before and 60 days after each mechanism.
- **Supported if** for ≥ 2 of the mechanisms, the defect rate per PC after is ≥ 25% lower than before,
  **and** PC did not fall more than 25% in the after-window (which rules out "less shipped, so fewer
  defects").
- **Refuted if** no mechanism shows a ≥ 10% drop, or defect rates rise.
- Plus the model-timeline confound check (top of file).

## Do-nothing baseline (for recommendations)
Each recommendation states what happens over 30 days if nothing changes, projected from the R-window
trend. It has to show a better expected outcome than that projection, net of migration cost.

## Amendments
(none)
