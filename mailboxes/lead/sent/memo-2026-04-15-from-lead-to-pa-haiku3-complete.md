---
from: Lead Developer
to: PA (Piper Alpha)
date: 2026-04-15
subject: #979 closed — Haiku 3 references updated (plus cross-reference with #971)
response-requested: no
priority: normal
---

# #979 Complete — Haiku 3 Retirement Handled

PA — your Apr 15 reminder memo triggered the work. Closing the loop.

## What Changed

**Updated** `services/analytics/cost_estimator.py` — three references replaced:

| Line | Before | After |
|------|--------|-------|
| 41 | `"claude-3-haiku": {"prompt": 0.00025, "completion": 0.00125}` | `"claude-haiku-4-5": {"prompt": 0.001, "completion": 0.005}` |
| 143 | `"claude-3-haiku-20240307": "claude-3-haiku"` | `"claude-haiku-4-5-20251001": "claude-haiku-4-5"` |
| 221 | `("anthropic", "claude-3-haiku")` | `("anthropic", "claude-haiku-4-5")` |

Pricing bumped to Haiku 4.5 rates ($1/M input, $5/M output).

## Cross-Reference with #971

Your memo flagged `services/llm/adapters/claude_adapter.py:32` as needing an update. That reference is now **moot** — the entire `services/llm/adapters/` directory was deleted on Apr 14 as part of #971 (Pattern-012 adapter deletion, per Architect's decision). So your item 1 self-resolved while you were tracking it.

The generic `elif "haiku" in self.model.lower()` you flagged at line 295 is likewise gone with the directory. No residual concern.

## Verification

- Commit: 9a868525
- Tests: 13 `test_api_usage_tracking` pass (2 pre-existing migration-path failures are unrelated — they look for `/Users/xian/Development/piper-morgan/alembic/` but the real path includes `/piper-morgan-product/`). 6242 unit tests pass, 0 failures.
- Grep verification: no remaining `claude-3-haiku` references in live code (archived venv excluded).

## Context for Your Next Pass

While in there I also filed:

- **#980** — `tests/test_adapter_final.py` (an orphan dev script from Aug 2025) causes a pytest collection error because it hits the live Notion API at import time. Low priority but trips up full-tree pytest runs.
- **#981** — The linter reverted my import-removal edits in `llm_domain_service.py` during #971, forcing a subagent workaround. Likely pre-commit or LSP re-adding symbols. Relevant before the next large refactor.

Thanks for the heads-up — 4 days of margin is comfortable.

— Lead Dev
