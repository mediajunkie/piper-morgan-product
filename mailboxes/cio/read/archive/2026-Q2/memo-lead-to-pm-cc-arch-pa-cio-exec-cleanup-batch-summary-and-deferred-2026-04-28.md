---
from: Lead Developer
to: PM (xian)
cc: Chief Architect, PA (Piper Alpha), CIO, exec (Chief of Staff)
date: 2026-04-29
subject: Tue cleanup batch shipped — Excellence Flywheel + #1012 + #1013; three items deferred for PM input
priority: normal
response-requested: PM — review at convenience; three deferred items below need your call when ready
---

# Tue Cleanup Batch — Shipped + Deferred Summary

Per your Tue evening directive ("work through all three methodically, saving up anything that needs my input for a summary when done"). Three issues + closures, plus three deferred items below for your call.

## Shipped to main

| Item | Commit chain | Result |
|---|---|---|
| Excellence Flywheel retirement (CIO A3) | `adfd453b` → `95897c73` (merge) | 6 files deleted + 1 file edited; standalone tests still pass; #1026 pre-existing test failure filed as discovered work |
| #1012 small dead-code sweep | `36d3be8d` → `95897c73` | 4 of 5 items shipped; item 4 deferred (below); closed |
| #1013 `/auth`+`/setup` → `/api/v1/` | `469bd7c8` → `95897c73` | 17 files migrated (routers + middleware + frontend + 11 test files); closed; live UI smoke test deferred |
| Branch | `claude/cleanup-batch-2026-04-28` | merged to main no-ff |

Both #1012 and #1013 closed properly via close-issue-properly skill: descriptions updated with all ACs marked, status banners ✅ COMPLETE, closing comments with implementation evidence + deferred items tables.

## Three items deferred for PM input

### 1. #1012 Item 4 — `LLMModel.CLAUDE_OPUS` semantic inversion

The enum reads `CLAUDE_OPUS = "claude-sonnet-4-20250514"` (name says Opus, value is Sonnet 4). Comment in code: *"Use Sonnet 4 as 'heavy' tier until Opus 4 available"*. AC marked this "PM call":
- **(a) Rename to `CLAUDE_HEAVY`** — more honest about what it currently is; mild churn (callers across `services/llm/`)
- **(b) Leave alone** — re-point to actual Opus 4 when it ships; cheaper; self-correcting

I did NOT change. My weak lean is **(b) leave alone** because we'll re-point soon enough and the comment in code already explains the inversion. But (a) is also defensible and PM can override.

### 2. PERPLEXITY broader sweep — out of #1012's scope

The Apr 27 disposition memo's grep on PERPLEXITY found only the `LLMProvider` enum value. My investigation found the literal `"perplexity"` + a separate `ProviderType.PERPLEXITY` enum still appear in:
- `services/config/llm_config_service.py` (separate enum + ProviderConfig + key validation)
- `services/security/provider_key_validator.py` (validation rules)
- `services/infrastructure/keychain_service.py` (known providers list)
- `services/analytics/cost_estimator.py` (cost estimates)

I removed only the `LLMProvider.PERPLEXITY` enum value (literal AC compliance). The deeper Perplexity scaffolding that survives is its own scoping question. **My recommendation: file as separate cleanup issue rather than expanding #1012.** Want me to file it, or leave it for someone else to surface later?

### 3. #1012 Item 2 — `APIUsageTracker` direction

I defaulted to **(b) remove the dead instantiation** in `services/llm/clients.py`. The class itself is still used elsewhere (Issue #271 cost tracking in `llm_domain_service.py`); only the unwired scaffolding here was removed.

The other path was **(a) wire it in** — but the call-site comments say wiring needs DB session in async context, which is bigger work than #1012's "~10 minutes per item" envelope.

If PM prefers wiring (which would unblock cost tracking from `LLMClient` directly), I can file as separate enhancement issue. Otherwise we're done with this one.

## Process notes worth flagging

- **Excellence Flywheel scope discovered broader than disposition memo named**: 6 files instead of 5, plus mixed-scope edits to `test_unit_orchestration_standalone.py`. Persisted through per "anything unblocked." Surfaced in commit message + this memo.
- **Pre-existing test failure** `test_decompose_moderate_task` filed as #1026 (Discovered Work Discipline). Joins the cluster #1005, #1006, #1007, #1008 of pre-existing failures from recent regression sweeps.
- **Live UI smoke test for #1013** deferred — no dev server running today. Imports + route prefix verification done programmatically. Smoke test on next dev-server boot.

## Sign-off checklist (per Docs Apr 28 norm)

```
$ git status                                         # → clean
$ git log --oneline @{u}..HEAD                       # → empty
$ git fetch origin && git log --oneline main..HEAD   # → empty
```

All three pass. No stranded work. `claude/phase-f-flag-flip` (held) and `claude/cleanup-batch-2026-04-28` (merged) both on origin.

## Total day output

13 commits on main + 1 held feature branch + 4 issue closures (#992 closure prep already drafted yesterday + #1012 + #1013 closed today + #1026 filed as discovered work) + 4 inbox memos triaged + 7 outbound memos (ADR-061 review, PA scoping, #1007/#1008 overlap, PA concur+status, Docs SessionStop scoping, issue triage, this summary).

— Lead Developer, 2026-04-29 (Tuesday's wrap)
