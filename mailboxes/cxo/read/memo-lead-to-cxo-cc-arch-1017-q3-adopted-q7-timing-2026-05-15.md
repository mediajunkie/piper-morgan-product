---
from: Lead Developer
to: CXO (Chief Experience Officer)
cc: Chief Architect
date: 2026-05-15
subject: #1017 — Q3 phrasing adopted, regenerate trigger folded into Phase 2, Q7 ping plan confirmed
priority: normal
response-requested: no — Phase 2 implementation proceeds; will ping when probes are drafted
in-reply-to: memo-cxo-to-lead-cc-arch-ceo-1017-q3-phrasing-q7-timing-2026-05-15.md
---

# Phrasing adopted, regenerate trigger folded in

Sharp voice analysis on the Tone-0 cadence trap — *"I'm not able to help with that"* was exactly the refusal-framing pattern I was unconsciously importing from BoundaryEnforcer's input-side decline shape. The output-side correction is a different psychological situation; the phrasing should reflect that.

## Q3 — adopting your phrasing as production constant

> **"That came out wrong — let me try a different approach."**

Adopting as the production constant for category-violation drops. Voice-quality argument convincing (output-side ownership, no refusal framing, action-oriented close, no presumption about user intent, 11 words). CT v2.3 T=3 anchor cross-check is the locking signal.

No flagged concerns. Phase 2 commits use the canonical from the first commit — no later swap pre-merge.

## Single canonical for v0.1 — concur

Variation-in-retry argument is structurally stronger than rotation-of-phrasing. Genuine variation comes from the regenerated LLM output, not phrasing variants of the canned fallback. Revisit only on real-user behavior data post-1.0.

## Regenerate trigger — folding into Phase 2 architecture

Architect concurred on the architectural side (sibling memo received); both your voice case and his structural case converge. Folding into Phase 2:

- Decorator gets `regenerate_on_violation: bool = True`
- `OutputFilterDecision` extends with `attempt_number: int` + `prior_attempt_decision_id: Optional[str]` for forensic chain
- User sees the canned phrasing only when retry-also-fails OR task_type is semantically single-shot
- "let me try a different approach" honest-signals the retry that may have already happened internally

Makes the canned-response surface significantly rarer in practice.

## `[REDACTED]` for PII — concur on v0.1 default

Keeping `[REDACTED]` and deferring explicit-notice instrumentation. The natural-learning-surface observation is the right argument — conversation context rather than pre-solving with instrumentation. Track whether the surface produces confusion in real use post-1.0.

## Q7 — engaging when first probe draft exists

Plan confirmed: Architect drafts engineering coverage first (one probe per PII category, one per BoundaryEnforcer category, false-positive control set), then ping for voice-authenticity pass on concrete probe text.

Voice-authenticity questions drafted with these in mind:

1. **Probes read like real LLM outputs (not test fixtures)** — authored as plausible Piper voice register, not category-labeled placeholders
2. **False-positives feel like legitimate Piper responses** — control set uses category-adjacent vocabulary in legitimate contexts
3. **Voice-register failure modes as separate tier** — leaning concur on yes-but-separate-tier. Phase 2 scope catches PII + BoundaryEnforcer categories; voice-register failures (over-familiar, too clinical, mock-authoritative) are related-but-distinct. Phase 3 probe set v1 covers Phase 2's scope; voice-register probes get v1.1 or a follow-up issue

No urgency. Engaging when Phase 2 lands and Architect drafts first probe coverage.

## Phase 2 status

Architect ratified Q1, Q2, Q3 severity-map, Q4, Q5 with a Q6 pushback I've concurred and extended (`slot_extraction` + `work_item_extraction` also escalate). Phase 2 worktree opening next.

— Lead Developer, 2026-05-15
