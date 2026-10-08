# P2 — Classification report (2026-10-08, 16:2x PDT)

Two independent Sonnet 5.5 passes over every eligible insight (published, confidentiality `clear`, not draft), one primary topic each from the frozen six-topic codebook plus a free-text tag. Pre-registered: taxonomy frozen by Janus (C3) before the run; gold set pre-labelled by Janus before the run; **xian's confirmation column is still empty, so accuracy below is against Janus's labels only** and will be recomputed when xian's marks land.

## Run

- Eligible: **581 of 632** insights (excluded: 39 drafts, 9 name-only mentions, 3 confidentiality-excluded). All 581 classified; 0 skipped for missing body.
- Cost from usage fields at skill prices: **$3.41** (est. was $3.60). Tokens: in 961,967 · out 127,157 · cache read 996,765 · cache write 6,041.
- Pass A/B framing: subject-matter vs where-a-practitioner-would-file. Model `claude-sonnet-5-5`, default sampling, no thinking. 13 transient JSON errors in the log, all recovered on retry (parser takes the first complete JSON object).
- Wall time: ~75 min sequential for the first 88, then a 6-worker pool did the remaining 493 in ~6 min.

## Agreement (consistency, not accuracy)

- A vs B agree on **527 of 581 (90.7%)**; Cohen's κ = **0.88**.
- Per pass-A topic: 1 agent coordination & process: 83/94 · 2 verification & testing: 147/159 · 3 tooling & infrastructure: 137/150 · 4 documentation & knowledge: 61/68 · 5 product & user-facing: 78/86 · 6 governance & security: 21/24
- Disagreement pairs (unordered): 2↔3: 13, 1↔4: 10, 3↔5: 9, 1↔2: 6, 3↔4: 4, 2↔6: 4, 1↔5: 3, 1↔3: 2, 3↔6: 2, 2↔5: 1
- Self-reported confidence: median 0.62, 10th pct 0.50.

## Accuracy against Janus's gold labels (n = 100 of 100; xian's column pending)

- Pass A: **75/100** (75%) · Pass B: **75/100** (75%) · Consensus (where A=B, n=92): **72/92** (78%).
- Per Janus topic (pass A correct / gold rows): 1: 9/13 · 2: 28/32 · 3: 20/22 · 4: 7/10 · 5: 7/16 · 6: 4/7

Confusion, rows = Janus label, cols = pass A:

| Janus \ A | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| 1 | 9 | 0 | 2 | 2 | 0 | 0 |
| 2 | 1 | 28 | 3 | 0 | 0 | 0 |
| 3 | 1 | 1 | 20 | 0 | 0 | 0 |
| 4 | 0 | 0 | 3 | 7 | 0 | 0 |
| 5 | 0 | 1 | 4 | 4 | 7 | 0 |
| 6 | 0 | 1 | 2 | 0 | 0 | 4 |

## The nine `architecture`-tagged rows (Janus's boundary: internal structure → 3, user-visible → 5)

- 9 tagged rows in the gold set. Classifier agreed with Janus's boundary on **6/9** (pass A) and **6/9** (pass B); A and B agreed with each other on 8/9.
- Rows (id · Janus · A · B): `2025-06-01#1` 5/3/3; `2025-06-27#2` 3/3/3; `2025-06-27#3` 3/3/3; `2025-10-04#3` 3/3/3; `2026-03-14#1` 5/5/5; `2026-03-15#1` 5/3/2; `2026-03-20#1` 5/3/3; `2026-06-13#1` 3/3/3; `2026-10-03#1` 3/3/3
- **Disposition**: the classifiers mostly follow the boundary; add Janus's boundary sentence to the codebook as clarification, no topic change.

## Corpus label distribution (pass A, all 581)

| Topic | n | % |
|---|---|---|
| 1 agent coordination & process | 94 | 16% |
| 2 verification & testing | 159 | 27% |
| 3 tooling & infrastructure | 150 | 26% |
| 4 documentation & knowledge | 68 | 12% |
| 5 product & user-facing | 86 | 15% |
| 6 governance & security | 24 | 4% |

## What happens next
- xian marks the gold set (ok / number / ?); rows marked `?` drop; corrected rows weight double; accuracy recomputed and this file updated.
- Disagreements (A≠B) go to an Opus adjudicator pass only if xian's marks show accuracy below 80% on any topic; otherwise consensus = A where A=B, else A with a `contested` flag.
- Labels are written to `insights.jsonl` as `topic`/`tag`/`topic_source=sonnet-5-5-2pass-2026-10-08` in P3's build; gold-set rows carry `topic_source=gold`.
- Verified how: numbers computed this turn by a script over `classify_full.jsonl` (581 rows) and the hub gold-set file (100 rows, Janus column); cost from the API usage fields, not the estimate.

