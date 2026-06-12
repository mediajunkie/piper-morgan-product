---
from: PA (Piper Alpha)
to: Dispatch (xian, CEO)
cc: Lead Developer
date: 2026-06-12
subject: Re: Hardcoded model IDs — 5 of 6 sites fixed and on main; .env manual; structural proposal enclosed
priority: standard
response-requested: none — informational + 1 PM action (.env)
in-reply-to: memo-dispatch-to-pa-hardcoded-model-ids-investigate-fix-before-june-15-2026-06-11.md
---

# Model ID fixes shipped — one manual step + structural proposal

Fixes landed on `origin/main` at commit `49704d06a`. Summary:

## What's fixed (5 of 6 code sites)

| Site | Old | New | Status |
|---|---|---|---|
| `services/llm/config.py` — `CLAUDE_SONNET` | `claude-sonnet-4-20250514` | `claude-sonnet-4-6` | ✅ fixed |
| `services/llm/config.py` — `CLAUDE_OPUS` | `claude-opus-4-7` | `claude-opus-4-8` | ✅ fixed |
| `services/llm/config.py` — `MODELS_WITHOUT_TEMPERATURE` set + comment | `claude-opus-4-7` | `claude-opus-4-8` | ✅ fixed |
| `tests/aaxt/conftest.py` | `claude-sonnet-4-20250514` | `claude-sonnet-4-6` | ✅ fixed |
| `tests/aaxt/test_golden_scenarios.py` | `claude-sonnet-4-20250514` | `claude-sonnet-4-6` | ✅ fixed |
| `tests/e2e/test_canonical_conversations.py` | `claude-sonnet-4-20250514` | `claude-sonnet-4-6` | ✅ fixed |
| `.github/workflows/e2e-aaxt.yml` | `claude-sonnet-4-20250514` | `claude-sonnet-4-6` | ✅ fixed |

The `CLAUDE_OPUS` / `MODELS_WITHOUT_TEMPERATURE` updates were included in the same pass per your instructions — the Opus 4.7 ID was also stale.

## One manual step required: `.env` (PM action)

`.env` is access-restricted and cannot be edited programmatically. **Before June 15**, update line 23:

```
ANTHROPIC_DEFAULT_MODEL=claude-sonnet-4-6
```

This is the only remaining site. Without it, the server's env-var fallback will use the deprecated ID. All other resolution paths go through `config.py` (now fixed), so runtime impact is limited to cases where `ANTHROPIC_DEFAULT_MODEL` is read directly — but it should be corrected.

## Also noted: comment-only references in `clients.py` (non-urgent)

`services/llm/clients.py` lines 30 and 420 reference `claude-opus-4-7` in code comments only — not in any string passed to the API. No production risk. Flag for next cleanup pass.

## Structural fix proposal: `MODEL_ALIASES` map

The root issue is that model ID strings are scattered across code, config, and test files with no single resolution layer. The Klatch pattern — a `MODEL_ALIASES` dict that translates deprecated IDs to current ones — is the right fix. Here's a concrete proposal for `services/llm/config.py`:

```python
# Map deprecated model IDs to current equivalents.
# Update this dict when Anthropic deprecates a model — downstream code that
# passes a deprecated ID gets silently resolved to the current one.
MODEL_ALIASES: dict[str, str] = {
    "claude-sonnet-4-20250514": "claude-sonnet-4-6",
    "claude-opus-4-7": "claude-opus-4-8",
}

def resolve_model_alias(model_id: str) -> str:
    """Translate a deprecated model ID to its current equivalent."""
    return MODEL_ALIASES.get(model_id, model_id)
```

`LLMClient` would call `resolve_model_alias(model_id)` before building the request payload. This means:
- Future deprecations require updating one dict entry, not grep-and-replacing 6+ files
- Old IDs in `.env`, test env-vars, and user config resolve gracefully instead of hard-erroring
- The alias map is visible and auditable in one place

For Lead Dev to evaluate: the main question is whether to wire `resolve_model_alias` into `LLMClient.build_request()` or at the `resolve_model()` level in config. I'd suggest `build_request()` — it's the lowest choke point, catches any path including direct model-string injection.

A DB migration for user-stored model IDs (as Klatch does) isn't needed here yet — we don't store model preferences per-user. Add it if/when BYO-key (#1185) introduces user-configurable model selection.

## Verification recommended

Lead Dev: before June 15, consider running `pytest tests/aaxt/ -k "not slow"` with `AAXT_ENABLED=true` to confirm the judge model resolves cleanly under the new ID. The CI workflow will also pick up the change on the next triggered run.

— PA, 2026-06-12 ~06:45 PT
