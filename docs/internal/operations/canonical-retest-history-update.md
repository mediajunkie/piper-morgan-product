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
| `serving_provider` | **#1676** — which provider ACTUALLY answered this run's queries. Copy verbatim from the harness's end-of-run report (see below). Vocabulary: a provider name (`anthropic`/`openai`/`gemini`), `mixed` (more than one served — the run is its own confound; details go in serving_model), `none` (zero LLM calls served), or `unrecorded` (pre-#1676 rows only — never write this for a new run, and never guess) |
| `serving_model` | **#1676** — the model id that answered (e.g. `claude-haiku-4-5`), same source. For `mixed` runs: every `provider:model(count)` pair joined with `;` (never commas — this CSV is unquoted). `unrecorded` for pre-#1676 rows only |

### Where serving_provider / serving_model come from (#1676)

**Read them off the harness — never off config.** The suite records which provider+model each successful LLM call was actually served by (`SERVING_MODEL_RECORD` in `services/llm/clients.py`, incremented only at a successful provider-call return — so a silent cross-provider fallback, e.g. openai 429 → anthropic, is captured as what it is). At module teardown the suite:

- prints a `=== CANONICAL RUN SERVING LLM (#1676) ===` block with the CSV-ready values, and
- writes the same report to `dev/active/canonical-retest-serving-llm.json` (timestamped, survives terminal scrollback).

Why this exists: Run 14 vs Run 15's Q36 routing flip was fully explainable by the two runs classifying on different models behind an identical-looking history row (#1676, found during #1674). A `mixed` value is a finding, not a formatting problem — it means the instrument changed identity mid-run.

Note: the Tier-2 **judge** model is NOT what these columns record (the judge is a direct SDK client, outside the serving path). Keep recording the judge model in `notes` (e.g. `judge=claude-sonnet-4-6`) as Run 14 did.

## C-axis reporting is per-bucket, never pooled (context_requirement — 2026-08-31)

Every corpus query carries a `context_requirement` tag (`required` / `optional` / `not_applicable`) — the sixth field of each `CANONICAL_QUERIES` row in `tests/e2e/test_canonical_conversations.py`. Semantics + scoring floors: `docs/internal/testing/context-requirement-tag-spec.md` (CXO spec; supports 1674 / 1676 instrument work).

**When a judged run reports C-axis results, report C per bucket — a single pooled C mean across `required` and `not_applicable` queries answers no question anyone has.** Carry this line in the run's `notes` (or the run report it links):

> `C-axis: required n=__ mean=__ · optional n=__ mean=__ · not_applicable n=__ (excluded from the context-assembly signal)`

The **`required` bucket alone is the context-assembly health signal.** A `not_applicable` query scoring C=2 is full marks, not a deficiency — do not read historical C=2 clustering as a context-assembly failure without first splitting by bucket (spec §5).

Tagging-pass distribution (2026-08-31, the spec's §5 finding): **required=49 · optional=2 (Q23, Q24 — §7 flags, CXO adjudicates) · not_applicable=10 (Q1–5, Q6, Q26–28, Q50) · total=61.**

## One-liner append (from repo root)

```bash
echo "YYYY-MM-DD,Run N,63,57,6,90.5%,48,8,1,77.4%,0,Short note here,anthropic,claude-haiku-4-5" \
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
