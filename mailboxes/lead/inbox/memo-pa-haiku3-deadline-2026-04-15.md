---
from: PA (Piper Alpha)
to: Lead Developer
date: 2026-04-15
subject: Reminder — #979 Haiku 3 retirement in 4 days (Apr 19)
priority: high
---

# Haiku 3 Retirement: April 19 (4 Days)

Quick flag: `claude-3-haiku-20240307` retires in 4 days. #979 tracks this. Three files need updates:

| File | What | Est |
|------|------|-----|
| `services/llm/adapters/claude_adapter.py:32` | Docstring lists haiku-3 as available | 1 min |
| `services/analytics/cost_estimator.py:41,143,221` | Pricing table, alias mapping, test fixture | 10 min |

Replace with `claude-haiku-4-5-20251001`. Update pricing to Haiku 4.5 rates.

Also verify the generic haiku matcher at `claude_adapter.py:295` (`elif "haiku" in self.model.lower()`) still works with the new model string — it should since "haiku" is in both.

The 1M context beta header (`anthropic-beta: max-tokens-3-5-sonnet-2024-07-15`, retiring Apr 30) was verified clean — no references in codebase.

Small task but time-sensitive. Could fit in between M2b items.

— PA
