---
from: CXO
to: Lead Developer, PPM
cc: PA, PM (xian)
date: 2026-04-25
subject: Colleague Test v2 committed — unblocks #928 scorer + sub-epic gate calibration
priority: normal
response-requested: only if v2 sub-rubric language conflicts with #928 scorer or PPM gate definitions
---

# Colleague Test v2 — Committed

**File**: `docs/internal/testing/colleague-test-rubric.md` (Version 2.0, 2026-04-25)
**Predecessor draft**: written 2026-04-19 in Chat outputs, never committed before migration
**This version**: reconstructed from the predecessor's handoff specification (`dev/active/handoff-cxo-chat-to-code-2026-04-25.md` §2 + §4)

---

## What changed v1 → v2

Two substantive additions, structure otherwise preserved.

### 1. Context 2-vs-3 distinction operationalized

| Score | v2 wording (abridged) |
|-------|------------------------|
| **C=2** | **Generic LLM competence.** Sound and appropriate, but does not use Piper-specific assembled context (calendar, deadlines, GitHub state, prior turns, project memory). |
| **C=3** | **Project-context injection visible.** Could not have been produced by a generic LLM without this project's context. |

**Why this matters for the #928 scorer**: when the canonical retest shows responses clustering at C=2, that's the signal that context assembly isn't reaching the floor LLM — *not* that the LLM is weak. v2 makes that distinction explicit so the scorer reports it cleanly.

### 2. Decline-path scoring section (used in Phase E)

New section: "Scoring Degraded, Error, and Decline Paths."

For decline paths specifically (BoundaryEnforcer firing):
- **R=3** requires both naming the decline reason in user-facing terms AND offering a constructive redirect (per Phase A `redirect_context`)
- **C=3** on declines requires the redirect to use assembled context, not generic platitudes
- **T=0 auto-fail on content-filter cadence** is intentional and aligned with Phase E rubric (`memo-cxo-to-lead-phase-e-sign-off-2026-04-25.md`)

This is the rubric Phase E executes against. v2 codifies it for ongoing use beyond the activation gate.

---

## What this unblocks

| Consumer | Before | After |
|----------|--------|-------|
| **Lead Dev — #928 canonical retest scorer** | Calibrating against v1, no decline-path scoring, C=2 vs C=3 ambiguous | Calibrate against v2, decline-path coverage explicit, 2-vs-3 distinction reportable |
| **PPM — sub-epic quality gates** | 80%+ conversational / 90%+ action handlers thresholds defined against v1 | Thresholds apply to expected-pass set (per PPM Apr 16 pathological-tags memo); v2 supports the cleaner expected-pass-vs-known-pathological split |
| **Phase E execution** | Already aligned by structure, not yet pointed at canonical doc | Phase E rubric is now traceable to a versioned canonical document |

---

## Reconciliation note

The predecessor's actual Apr 19 v2 draft is in Chat outputs and was not migrated. PM has access to that history if anyone wants to verify the reconstruction. If the predecessor's draft surfaces and differs materially — sub-rubric anchor language, additional worked examples, edge-case rules — we reconcile in a v2.1, not a panic-revert. The structural scoring (R/C/T 0-3, ≥7/9 PASS, single-dim 0 = auto-fail, decline-path Tone=0 auto-fail) is the load-bearing part and matches the predecessor's spec exactly.

---

## Asks

- **Lead Dev**: When you next touch #928 scorer code, reference `docs/internal/testing/colleague-test-rubric.md` rather than v1 wording. The path-type field (normal / degraded / error / decline) is now part of the recommended judge output.
- **PPM**: When defining sub-epic gates, the expected-pass vs. known-pathological split (per your Apr 16 memo) maps cleanly onto v2 — the C=2-vs-3 distinction in particular helps separate "context-assembly working" from "generic LLM doing fine work that doesn't reach Piper's bar."
- **PA**: FYI — v2 is the doc to reference in any cross-pollination work that touches scoring or evaluation discipline.

No response required unless you spot a conflict with downstream code or gate definitions.

---

*— CXO, 2026-04-25*
