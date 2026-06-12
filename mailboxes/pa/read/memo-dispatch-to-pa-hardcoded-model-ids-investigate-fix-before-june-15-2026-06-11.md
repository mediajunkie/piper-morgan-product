---
from: Dispatch (xian, CEO)
to: Piper Alpha (PA)
cc: Lead Developer
date: 2026-06-11
subject: Hardcoded model IDs — investigate and propose fix before June 15
priority: high — hard production failure if unresolved by June 15
response-requested: yes — investigation findings + fix plan by June 13
---

# Hardcoded model IDs — investigate and propose fix before June 15

Six files in piper-morgan-product have `claude-sonnet-4-20250514` hardcoded. Anthropic deprecates that model ID on June 15 — four days from now. When it goes, every call site that references it will hard-error.

## The six sites

1. **`services/llm/config.py` line 19** — `CLAUDE_SONNET = "claude-sonnet-4-20250514"` (production config — this is the critical one)
2. **`.env` line 23** — `ANTHROPIC_DEFAULT_MODEL=claude-sonnet-4-20250514`
3. **`.github/workflows/e2e-aaxt.yml` line 288** — fallback default in CI
4. **`tests/aaxt/conftest.py` line 25** — test judge model default
5. **`tests/aaxt/test_golden_scenarios.py` line 27** — test judge model default
6. **`tests/e2e/test_canonical_conversations.py` line 308** — test judge model default

Also: **`services/llm/config.py` line 18** has `claude-opus-4-7` — verify whether that's a valid model ID. Latest known is `claude-opus-4-6`. If it's wrong, fix it in the same pass.

## Two asks

### 1. Immediate fix (before June 15)

Update all six sites to current model IDs. Straightforward string replacements, but verify each one — some may be intentionally pinned for test reproducibility, in which case the pin should move to the current version, not be removed.

### 2. Structural fix (propose)

Propose a pattern that avoids hardcoding model IDs going forward. Worth looking at Klatch's approach as a reference: they use a `MODEL_ALIASES` map that translates deprecated IDs to current ones, plus a DB migration that bulk-rewrites legacy IDs at startup. The idea is that when Anthropic deprecates a model, we update one map entry and everything downstream resolves — no grep-and-replace across six files.

This doesn't need to ship by June 15, but the proposal should be ready so Lead Dev can evaluate it.

## Why this is high priority

This is the only item in the June 15 deprecation cluster that will cause a **hard production failure** — not degraded behavior, not a warning, but actual errors on every LLM call. The test sites (items 3–6) will additionally break CI, which blocks all other work.

— Dispatch
*2026-06-11*
