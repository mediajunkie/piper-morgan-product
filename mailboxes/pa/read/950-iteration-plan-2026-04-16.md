# #950 Iteration Plan — Identity Context + Prompt Sharpening

**Date**: 2026-04-16
**Author**: Lead Dev (code-opus)
**CC**: Piper Alpha (pa)
**Status**: In progress — approved by PM 2026-04-16 13:30

## Why an Iteration

First canonical retest (Apr 16 morning) showed the #950 prompt evolution did NOT move Identity from MARGINAL to PASS. Per-dimension analysis revealed this is **not a prompt-tone problem**. The scores:

| Identity Query | Relevance | Context | Tone | Verdict |
|---------------|-----------|---------|------|---------|
| Q1 "What's your name?" | 3 | 1 | 2 | MARGINAL |
| Q2 "What can you help me with?" | 3 | 1 | 3 | PASS |
| Q3 "Are you working properly?" | 3 | 1 | 2 | MARGINAL |
| Q4 "How do I get help?" | 3 | 1 | 2 | MARGINAL |
| Q5 "What makes you different?" | 3 | 3 | 3 | PASS |

Judge rationale for Context=1 is consistent: "Generic response that could apply to any user or situation." Tone is at PASS boundary (2 or 3) — the Five Pillars work is landing. The remaining gap is **Context**.

This is the same Pattern-062 ("Assembly Assumption") gap #951 closed for Temporal. The prompt tells the LLM to use context, but the assembler for IDENTITY category provides only capabilities + integrations (global/systemic info), not user-anchoring data.

CXO's approval memo (2026-04-16 draft review) explicitly said "first runs are diagnostic — iterations don't need rework approval." Proceeding directly.

## Option 3 Scope

**Both** sides of the chain:

### Part A — Extend `_gather_identity_context`

Add user-anchoring fields so the LLM has specific ground to stand on:

- User's stated projects (from `user_context_service.get_user_context`, same as STATUS gatherer uses)
- Recent conversation topics (from `conversation_context`, same pattern as MEMORY gatherer)
- Trust stage summary (brief — "new user" / "building" / etc.)
- Approximate interaction history ("first session" / "N turns in current session")

Not in scope: adding project portfolio depth (that's #983), real-time GitHub activity (#984), calendar events (already in TEMPORAL/STATUS gatherers via #951 — if Identity queries benefit from "it's 3pm and you have a CXO 1:1 coming up", we can add later).

### Part B — Sharpen prompt's context-usage instruction

Current language (from #950 commit d9f9b3f2):
> "Use the context you have. The [Available context] block in the user's message carries real information about this user — projects they're tracking, meetings they actually have, trust stage, recent conversation topics. Prefer specificity grounded in that context over generic PM advice. If context for a category is absent, say so plainly rather than answering as if you knew."

Proposed update — add one sentence that names the "generic response" failure mode and gives the escape route:
> (append) "Do not produce responses that could apply to any user. If you can't anchor specifics from the context block, ask a concrete question instead of answering generically."

That's it. Don't rewrite the paragraph — just add the anti-generic-response guidance. Keeps scope tight, preserves the working language.

## Expected Effect

- Identity Context scores: target ≥ 2 on majority (currently 4 of 5 at 1). Real target: at least 3 of 5 at Context ≥ 2.
- No Tone regressions — the Five Pillars work should still land
- No new Pattern-062 gaps introduced — Part A delivers what Part B instructs the LLM to use
- No effect on Fabrication guard (#960) — those queries depend on explicit-absence signaling which we're preserving

## Out of Scope (Defer)

- Full user-history rollup (multi-session memory, onboarding state summaries)
- Dynamic trust-stage adjustment (#923 territory)
- Identity-query routing refinement (classifier-side work)
- Per-session activity timeline

## Test Strategy

1. **Unit**: add 1-2 tests for the new identity context fields; verify existing Identity gatherer tests still pass
2. **Canonical retest**: re-run `dev/2026/04/11/canonical-retest-m1.py`, compare Identity Context scores to the Apr 16 morning baseline
3. **Manual smoke**: 5 Identity queries through curl, verify responses reference user-specific details when available
4. **Fabrication regression**: 10 "do you see my X?" queries with empty context, verify "I don't see..." responses unchanged

## STOP Conditions

- Identity Context scores don't improve → Pattern-062 still present on a deeper layer; escalate
- Fabrication guard weakens → immediate rollback
- Tone scores regress (go below 2 anywhere) → Pillar prompt too diluted; revert Part B only
- Temporal/STATUS Context scores regress → shared prompt logic affecting other categories; debug

## Rollback

Single commit covering both parts. `git revert <sha>` reverses cleanly. Server restart required to re-load prompt constant.

## Distribution

- Lead Developer implements
- PA copied on this plan doc (per PM standing request 2026-04-16)
- No CXO re-review needed (approval memo covered first-run iterations)
- PM approved Option 3 scope 2026-04-16 13:30
