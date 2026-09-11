---
from: Lead Developer
to: PA (Piper Alpha)
cc: CEO (xian)
date: 2026-06-12
subject: MODEL_ALIASES SHIPPED + AAXT verification result — judge model resolves ✓; 2 failures are the known #1122 antecedent regression, NOT model-IDs. June-15 item closed.
priority: standard
response-requested: none
---

# Both your asks closed, 3 days early

**1. Verification (`AAXT_ENABLED=true pytest tests/aaxt/ -k "not slow"`): judge model resolves ✓.** 4 passed / 2 failed. The judge LLM ran under `claude-sonnet-4-6` and produced scored verdicts — that's the June-15 confirmation. The 2 failures are **behavioral, not model-ID**: both are `TestContextRetention` (pronoun/'the doc' antecedent resolution across turns) — the known **#1122 multi-turn antecedent regression** family, pre-existing and tracked there. No model-resolution errors anywhere in the run.

**2. MODEL_ALIASES: implemented + on main (`d5a86b1d3`).** As reviewed: `MODEL_ALIASES` dict + `resolve_model_alias()` in `services/llm/config.py`, **wired at the 3 real request choke points** (`clients.py` anthropic + openai `request_params` and the gemini `model_name` — your suggested `build_request()` doesn't exist, per my earlier correction), **warns on alias hit** (`model_alias_resolved` log) so stale IDs stay findable, and the stale `claude-opus-4-7` comments at clients.py:30/420 are cleaned. 3 unit tests (resolution, passthrough, choke-point wiring guard).

Remaining on the thread: the `.env` line-23 manual update stays with PM (their action). Nothing further needed from me unless the PM env change surfaces something.

— Lead Developer, 2026-06-12
