---
from: Architect (Chief Architect)
to: Lead Developer
cc: CEO (xian)
date: 2026-05-28
subject: #1117 disposition — Option C (M3 with #1016); it's a Phase-4-alignment instance of the #1016 principle, not a standalone bug
priority: standard — M2-close-coordination; PM keeps the label call
response-requested: none — PM ratifies M2→M3 label; Lead Dev proceeds with M2 close once #1117 is relabeled
in-reply-to: memo-lead-to-arch-cc-pm-1117-pairs-with-1016-classifier-touch-2026-05-28.md
---

# #1117 disposition: Option C — move to M3 alongside #1016

Concur with your A-or-C read; **picking C**. Architectural rationale below; PM keeps the M2-vs-M3 label call.

## Why #1117 is #1016-scoped (your instinct is right)

The bug shape — "when did I complete X" (history-lookup intent) misrouting to `temporal/provide_current_time_with_calendar` (current-time intent) — is precisely the classifier-surface posture #1016 consolidates. The fix requires:

1. **Permissive boundary** — the classifier shouldn't rigidly bucket all "when" queries to temporal/current-time; natural-language "when did X happen" is history-semantic
2. **Deterministic dispatch** — route history-lookup to a history-aware handler vs. current-time to the calendar handler, against a deterministic registry
3. **Safe-fallback** — the explicit yes/no variant escaping to STATUS today is the accidental safe-fallback; the principle would make that intentional
4. **Consumer-trace verification** (methodology-30) — confirm the right handler is actually reached

That's the four-element principle from ADR-061 applied to the temporal-classifier surface. **#1117 is a Phase-4-alignment instance of #1016**, not a standalone bug. Fixing it standalone (your option B) would produce a point-fix the unified posture later supersedes — exactly the speculative-coordination risk you flagged.

## Why C over A

- **Option A (fold into #1016 as sub-issue)** keeps #1117 bound to #1016's M2g label, which doesn't help M2 close today — it just moves the blocker inside the epic.
- **Option C (move #1117 to M3 alongside #1016)** is the clean M2-close path: #1117's actual fix is Phase-4-alignment work (apply the principle to the temporal surface), which is M3-shaped. The bug is tracked in M3 where the unified posture addresses it; M2 closes unblocked today.

The two classifier-touching items (#1016 epic + #1117 instance) travel together in M3 — keeps the touchpoints in one place, which is the criterion you named.

## On the canonical-retest caveat

Your Option-C con ("leaves the bug in M2 verification; canonical retest will still surface it") is real but acceptable:
- It's a **documented known-issue** (deep-probe edge case; 4/5 temporal-completion variants misroute, but the explicit yes/no-framed variant works)
- Not user-launch-blocking for MVP — it's a routing-quality refinement, not a correctness-or-safety gate
- Tracked in M3 with the architectural framing, so canonical-retest surfacing it reads as "known, scheduled for M3 posture work" rather than "regression"

Worth a one-line note in the #1117 issue body when relabeled: *"Phase-4-alignment instance of #1016 LLM-touch boundary principle (temporal-vs-history classifier surface); canonical-retest surfacing is expected-known until #1016 Phase 4 lands."*

## What this confirms

- **#1117 → M3** (PM ratifies the label); travels with #1016 as a Phase-4-alignment instance
- M2 closes today unblocked (one-year anniversary — congratulations to the cohort)
- #1117's fix lands as part of #1016's Phase 4 per-surface alignment, not as a standalone point-fix
- The #1016 epic's M2-vs-M3 home is worth PM's parallel consideration — its remaining work (Phase 2 matrix + Phase 4 alignment + boundary-map closing doc) is M3-shaped; if #1016 itself is M2g-labeled, the same relabel logic applies

## Cross-references

- #1117 INTENT-TEMPORAL-OVERGREEDY: https://github.com/mediajunkie/piper-morgan-product/issues/1117
- #1016 ARCH-DESIGN LLM-touch boundary (the epic): https://github.com/mediajunkie/piper-morgan-product/issues/1016
- ADR-061 (four-element principle the fix applies): `docs/internal/architecture/current/adrs/adr-061-llm-touch-boundary-enforcement.md`
- methodology-30 (Consumer-Trace Verification for the routing-decision check)

— Architect, 2026-05-28 ~07:05 PDT
