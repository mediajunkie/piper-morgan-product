# Memo: #1017 Phase 1 — voice-equity items (Q3 phrasing + Q7 probe set)

**From**: Lead Developer
**To**: CXO (Chief Experience Officer)
**CC**: Architect (parallel review on Q1, Q2, Q4, Q5, Q6 + Q7 co-design)
**Date**: 2026-05-15
**Re**: #1017 OUTPUT-CONTENT-FILTER Phase 1 — two voice-equity items where your call governs
**Design memo**: `dev/2026/05/15/1017-phase-1-design.md`
**Phase 0 audit**: `dev/2026/05/15/1017-issue-audit.md`

---

## Status

PM has read the Phase 1 design and supports the Q1–Q7 recommendations, while being open to other points of view. Two items in the design carry your voice-equity rather than Architect's engineering equity. Routing them to you for the call. Architect is reviewing the engineering questions in parallel.

## Context — what #1017 builds

Post-generation content filter for LLM outputs reaching users. Currently the `BoundaryEnforcer` operates only on user *inputs*; LLM *outputs* pass through unfiltered. The filter wraps `LLMClient.complete()` (chokepoint guarantee) and applies a profile based on `task_type`. PII detection redacts in place; secret formats redact + flag; **boundary-category violations drop the LLM output and substitute a canned response** — that last action is where the voice-equity sits.

## What needs your call

### Q3 — Canned-response phrasing for category-violation cases

When the LLM emits content that violates a `BoundaryEnforcer` category (harassment, inappropriate content, professional-boundary breach), the filter **drops the LLM output entirely** and substitutes a single canned response. The phrasing of that canned response is Piper's voice in the boundary moment.

**My draft** (placeholder for engineering — yours to tune):

> "I'm not able to help with that. If you'd like, we can try a different angle on what you're working on."

What I was going for: refusal that doesn't lecture; brief; offers a graceful pivot; doesn't disclose detection internals; doesn't apologize excessively. Same voice register as the floor's existing redirect language when BoundaryEnforcer flags inputs.

**Open questions for your read**:
- Does the phrasing match Piper's existing voice when she declines on the input side?
- Is the "different angle on what you're working on" close-to-the-user wording right, or does it feel presumptuous (we don't always know what they're working on)?
- Do we want one canned response or a small set (e.g., 2-3 variants the filter rotates through)?
- For the "drop entirely" case vs. the "redact in place" case (PII): user-visible signaling difference? Currently the redact case shows `[REDACTED]` inline in otherwise-passthrough content; the drop case shows only the canned response. Should we be explicit that "content was filtered" in the redact case too, or is `[REDACTED]` enough signal?

### Q7 — Probe set design for Phase 3 CI gate

Phase 3 verification (Architect estimates ~2 days) builds a probe set that should reliably trigger the filter, plus a false-positive control set that should NOT trigger. The probe set goes into CI; a regression alert fires if any probe fails detection OR any false-positive fires.

This is a co-design with Architect — Architect for engineering coverage, you for tone/voice signal authenticity. The probes need to read like real LLM outputs (not test fixtures); the false-positive controls need to feel like legitimate Piper responses that happen to mention category-adjacent vocabulary.

**Architect-side coverage** (technical):
- One probe per PII category (email, phone, SSN, credit card, API keys)
- One probe per boundary category (harassment, inappropriate content, professional-boundary)
- False-positives: legitimate content mentioning "email" or "phone" without quoting actual values; code samples with placeholder API keys; URLs with category-adjacent query strings

**Your-side authenticity** (voice):
- Are the probes phrased in plausible Piper voice, or do they read as "test prompts"?
- Are the false-positives realistic — i.e., the kind of content Piper would actually produce in a normal conversation?
- Should the probe set include voice-register tests (Piper accidentally adopting an inappropriate tone — over-familiar, too clinical, etc.)?

Phase 3 doesn't block Phase 2 implementation. Your input on Q7 can land later in the cycle when Architect drafts the engineering coverage and you tune the voice authenticity.

## What's NOT in your lane on this issue

Architect ratifies:
- **Q1** filter contract shape (decorator on `LLMClient.complete()`)
- **Q2** detection scope (Tier 1 PII + Tier 2 boundary; Tier 3 deferred)
- **Q3 severity→action mapping** (the table — PII redact, secrets redact-flag, category drop-substitute)
- **Q4** audit envelope schema (hashes-only, no raw PII)
- **Q5** decision schema for callers
- **Q6** initial profile-vs-task_type mapping

PM ratifies overall scope + Tier 3 deferral. Already done in the design-memo read.

## Asks

1. **Q3 phrasing**: draft canned-response language for category-violation cases. One response or a small rotation set — your call.
2. **Q3 secondary**: should redact-in-place (PII case) include an explicit "filtered" notice beyond the inline `[REDACTED]`?
3. **Q7 timing**: when in the Phase 2 → Phase 3 cycle do you want to engage on probe authenticity? (No urgency; Phase 2 implementation can land first.)

Phase 2 implementation can start with my draft phrasing as a placeholder once Architect ratifies engineering Qs; your final language swaps in pre-merge. Q7 is parallel to Phase 2 and only gates Phase 3 CI.

— Lead Developer, 2026-05-15
