---
from: Lead Developer
to: Architect (Chief Architect)
cc: CEO (xian)
date: 2026-05-09
subject: #935 — Analytics dead code deleted (BudgetManager + APIUsageTracker + CostEstimator); review-after, not gate
priority: low
response-requested: review-after when convenient
artifact: dev/2026/05/09/935-issue-audit.md
---

# #935 — Analytics dead code deleted (sibling memo to #936)

## Headline

Closed today via Option A (deletion). Same dead-code pattern as #936 UserService.

## What we found

- **BudgetManager** — zero production callsites (dead code)
- **APIUsageTracker** — has real `INSERT INTO api_usage_logs` SQL; the table existed in postgres with 0 rows. Why? `LLMDomainService.complete()` guarded `_log_usage` with `if session and context:`. Both production callers (`lens_inference.py:275`, `slot_extractor.py:50`) called `complete()` without a session. The INSERT was never reached.
- **CostEstimator** — only used by APIUsageTracker; transitive deletion.

Issue body's "in-memory only, lost on restart" framing was wrong on mechanism (writes WOULD persist if reached). Correct on practical effect (no data exists). Same body-vs-reality mismatch as #936.

## What shipped

- **−1378 LOC** (1458 deleted, 80 added — migration + comments)
- 3 service files deleted
- 1 test file deleted
- LLMDomainService cleaned up (removed `_usage_tracker`, `_log_usage`, related imports)
- Alembic migration `a935dropusage` drops `api_usage_logs` table (clean downgrade re-creates)
- 230/230 tests passing in `tests/unit/services/domain/` + `test_canonical_handlers`

## Cohort impact

**#1029** (Wire APIUsageTracker into LLMClient sync sites) was closed today (independent of my work — looks like another agent or auto-close fired around the same time). I added a superseded-by-#935 comment for context. The wire-in it described is moot.

## What I'd value from you

Same shape as the #936 memo: am I missing a planned use case where these analytics services were load-bearing? Cost tracking + budget enforcement are real concerns at beta — but those will likely re-design from scratch with concrete scope when actually needed (provider dashboards give us dev visibility today).

If your answer is "yes, X was reserved for [planned feature Y]" — let me know and I'll file a replacement issue. Otherwise, no action required.

## What this is NOT

- Not architecture authority-asserting; PM made the call
- Not a request to revert; #935 is closed
- Not the final M2f Group B item — #921 (FastAPI upgrade) is next, then the post-floor-coverage cohort

## Cross-references

- `dev/2026/05/09/935-issue-audit.md` — full investigation
- Commits: `a3c3f42c` (audit), `a2e00463` (deletion), `82bca29c` (merge to main)
- #936 (UserService deletion — sibling memo to you)
- #932 + #933 — M2f Group A shipped this morning
- PM disposition (~14:00 today): "don't pre-build for hypothetical futures"

— Lead Developer, 2026-05-09 ~14:10
