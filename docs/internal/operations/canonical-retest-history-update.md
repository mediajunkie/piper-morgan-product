# Canonical Retest History — Update Instructions

**Table**: `docs/internal/operations/canonical-retest-history.csv`

Append one row after each canonical-retest run. The table exists so Lead Dev can answer "is 12 env-errors normal?" in under 30 seconds without reconstructing history from memory.

## CSV columns

| Column | What to fill |
|---|---|
| `date` | Run date (YYYY-MM-DD) |
| `run` | Sequential name: Run 14, Run 15 … or Run N INVALID for discarded runs |
| `queries_total` | Total queries in the corpus that run |
| `routing_pass` | Count routing PASS |
| `routing_fail` | Count routing FAIL |
| `routing_pct` | Routing pass % (routing_pass / queries_total) |
| `quality_pass` | Count quality PASS (judge ≥7) |
| `quality_fail` | Count quality FAIL (judge <5 or auto-fail) |
| `quality_skip` | Count skipped (NOT_IMPL, ERROR, excluded) |
| `quality_pct` | Quality pass % — use judged-only denominator: quality_pass / (queries_total - quality_skip) |
| `env_errors` | Count of environment/service errors (Slack not configured, etc.) |
| `notes` | Free text: what changed since last run, gate status, known flakes |

## One-liner append (from repo root)

```bash
echo "YYYY-MM-DD,Run N,63,57,6,90.5%,48,8,1,77.4%,0,Short note here" \
  >> docs/internal/operations/canonical-retest-history.csv
git add docs/internal/operations/canonical-retest-history.csv
git commit -m "ops: canonical-retest Run N results (YYYY-MM-DD)"
git push origin main
```

## For INVALID runs

Still append a row — invalid runs are load-bearing context (they explain why the baseline didn't advance). Use `Run N INVALID` in the run column, leave numeric fields blank, put the failure cause in notes.

## Env-error baseline

As of Run 12 (2026-06-04): **12 env-errors is normal** — these are Slack/Productivity/Todos/Calendar/Knowledge integrations unconfigured in the test environment. They don't reflect a regression; they reflect which connectors are wired up. If env_errors rises above 12 unexpectedly, investigate before attributing to routing regression.

## History at a glance (as of 2026-06-19)

| Run | Date | Routing % | Quality % | Notes |
|-----|------|-----------|-----------|-------|
| M0 | 2026-03-12 | 70.5% | — | Routing-only baseline |
| M1 | 2026-04-11 | 93.4% | 86.7% | M1 gate |
| M2f-baseline | 2026-05-08 | 93.4% | 66.7% | Pre-M2 work |
| Run 7 | 2026-05-09 | 93.4% | 70.0% | Recovering |
| Run 8 | 2026-05-13 | 93.7% | 69.4% | +2 queries |
| Run 9 | 2026-05-13 | 93.7% | 71.0% | M2g baseline |
| Run 10 | 2026-05-28 | 93.7% | 82.0% | **M2 gate MET** |
| Run 11 | 2026-06-03 | 93.4% | 80.3% | Phantom=6 |
| Run 12 | 2026-06-04 | 93.4% | 85.2% | Prior baseline |
| Run 15 | 2026-07-12 | 88.5%* | 92.0% | **#1386 criterion-2 run** (judge on; 61 routing / 25 judged). *Routing: all 7 misses triaged = 6 corpus-expectation drift (`expected floor, got action/canonical` — the #1220/#1383/Slack/canonicalization handlers now catch what floored when the corpus was written) + Q51 (drift + harness non-UUID user id crashing a UUID-typed owner query; unreachable in prod). **No product routing regression; corpus rev required (ADR-077 D5, Arch ratification) before the routing % is face-readable.** Quality 92% = above the 80–86% normal band. Runs 15/15b identical totals (stable). |

Routing has been stable at 93.4–93.7% since M1 (Apr 11). Quality trend: 66.7% → 85.2% across M2 work. **Normal quality range: 80–86%.** A single run outside that range is judge variance; two consecutive runs outside it is a signal.
