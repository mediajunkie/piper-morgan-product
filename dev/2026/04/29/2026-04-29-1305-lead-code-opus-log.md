# Session Log: 2026-04-29-1305-lead-code-opus

**Role**: Lead Developer
**Model**: Claude Code (Opus)
**Date**: Wednesday, April 29, 2026
**Start Time**: 1:05 PM
**Branch**: `main` (worktree at `/Users/xian/cool/piper-morgan/piper-morgan-product`)

## Session Objectives

1. Verify Tue work all pushed (DONE — sign-off clean at start)
2. Check inbox (2 unread Docs memos re mailbox renames)
3. Surface open questions to PM + identify any blocked-on items
4. Resume work per PM direction

## Carryover from Tue Apr 28

**All shipped to main**:
- Excellence Flywheel retirement (CIO A3) — `adfd453b` → `95897c73`
- #1012 dead-code sweep (4/5 items) — `36d3be8d`
- #1013 `/auth`+`/setup` → `/api/v1/` — `469bd7c8`
- Cleanup batch merge → main: `95897c73`
- Day-summary memo to PM with 3 deferred items: `98086bb9`

**Held branch**: `claude/phase-f-flag-flip` (pre-staged Phase F flip; PM/PA Tue Apr 28 decision = wait for calibration window)

**3 deferred items waiting on PM input** (filed in `memo-lead-to-pm-cc-arch-pa-cio-exec-cleanup-batch-summary-and-deferred-2026-04-28.md`):
1. CLAUDE_OPUS rename vs wait-for-Opus-4
2. PERPLEXITY broader sweep (file as separate issue?)
3. APIUsageTracker direction (already removed; option to file wiring as enhancement)

**Discovered work filed**: #1026 (`test_decompose_moderate_task` pre-existing failure)

## 1:05 PM — Session start

Opened on main, sync clean. Today's logs already include `docs-code-opus` (8:21 AM). Lead Dev inbox had 2 new unread Docs memos (mailbox rename → `mailboxes/xian (ceo)/` is canonical now). Triaged to read (commit `652254d5`).

## 1:25 PM — PM directives received

PM responded to Tue summary's deferred items:
1. CLAUDE_OPUS — wait but need a trigger (file tracking issue) ✅
2. PERPLEXITY broader sweep — file separate issue ✅
3. APIUsageTracker — file separate enhancement ✅
4. Then proceed to #1014
5. After above, discuss flag-flip / saved items

## 1:30 PM — Three follow-up issues filed

- **#1027** — Re-point `LLMModel.CLAUDE_OPUS` to Opus 4 when Anthropic ships it (P5/no-rush; trigger-bound)
- **#1028** — PERPLEXITY broader sweep — 4 files still reference perplexity beyond LLMProvider enum (P3)
- **#1029** — Wire APIUsageTracker into LLMClient (P4 enhancement)

All three filed with proper AC, evidence pointers, cross-references to Apr 28 summary memo.

## 1:45 PM — #1014 AuthMiddleware exclude_paths refactor shipped (commit `d13d6035` → `fcbc0bcc`)

Architect Apr 27 batch-2 review Finding E. Refactored flat 23-entry exclude_paths (down from 34 after #1013 cleanup) into 7 named module-level category constants + `DEFAULT_EXCLUDE_PATHS` assembly.

Categories:
- EXEMPT_OPENAPI_PATHS (3), EXEMPT_HEALTH_PATHS (2), EXEMPT_AUTH_AND_SETUP_PATHS (6), EXEMPT_OPTIONAL_AUTH_PATHS (3), EXEMPT_OAUTH_CALLBACK_PATHS (6), EXEMPT_STATIC_ASSET_PATHS (2), EXEMPT_LOCALHOST_SCAFFOLD_PATHS (1)

Behavior verified preserved via path-exclusion smoke test (all 23 self-match; sub-route startswith preserved; auth-required paths still require auth). Pre-existing `test_login_success` DB-connect failure (port 5433) verified via git stash — not a regression.

Closed properly via close-issue-properly skill: body updated, status banner ✅ COMPLETE, closing comment with implementation evidence + categories table.

## Status mid-afternoon

| Item | Status | Commit |
|---|---|---|
| Triage 2 Docs mailbox memos | ✅ Done | `652254d5` |
| File #1027 (CLAUDE_OPUS trigger) | ✅ Filed | — |
| File #1028 (PERPLEXITY broader sweep) | ✅ Filed | — |
| File #1029 (APIUsageTracker wiring) | ✅ Filed | — |
| #1014 refactor + close | ✅ Shipped | `d13d6035` → `fcbc0bcc` |

Standing by for PM check-in on flag-flip + any saved items.
