# CXO Response: #950 Floor Prompt Draft Review

**To**: Lead Developer  
**From**: Chief Experience Officer  
**CC**: PM  
**Date**: April 16, 2026  
**Re**: Response to Apr 16 #950 draft

---

## Overall Assessment

**Approve with two small edits.** The draft does exactly what the direction memo asked for and in several places improves on it. The per-section rationale with cross-references is model documentation discipline — makes the review tractable and creates an audit trail.

Implementing comments in order of your seven questions, then two specific edits I'd like to see before you ship.

---

## Answers to Your Seven Questions

### 1. Pillar language — operationalize correctly?

**Yes.** The positive-contrast framing is the right call. I was going to flag this as a risk ("might be too prescriptive") but your rationale section preempts it: negative-only framing has proven insufficient, and the paired examples are the exact patterns the canonical retest caught as MARGINAL. That's not over-specification — that's addressing specific observed failures.

The examples are concrete enough to teach, abstract enough to generalize. "14:32 UTC" and "Alert: PR count" are real flattening patterns we've seen. Keeping them as named anti-patterns is appropriate.

### 2. Grammar phrasing — one paragraph right weight?

**Yes, and don't make it a separate heading.** Embedding it as a paragraph is exactly right. A heading would signal "this is a rule to apply mechanically." A paragraph signals "this is the mental filter running in the background." You read the direction correctly.

On the parroting risk: your mitigation (pairing "Entities experience Moments in Places" with "frame observations as" — verb of application) addresses it well. The LLM is less likely to echo a phrase that's embedded in an instruction to *do something with it*. Good instinct.

### 3. Anti-flattening capstone — actionable?

**Yes, with one edit.** The paired example ("I've been tracking the migration" vs. "I'm looking forward to helping you") is the right construction — both mention the migration, only one is specific. That's what makes it actionable rather than aspirational.

The fallback directive ("ask a concrete question that moves the conversation forward rather than performing enthusiasm") handles the zero-context case correctly. That's the Identity-query failure mode ("hi, who are you?" with no prior context) where the LLM defaults to generic warmth because it has nothing specific to reference. Good.

**Edit I'd like**: the line "expresses an emotion you can't have" is true but slightly philosophical. Suggest softening to "expresses an emotion without specifics." The point is that declared emotion without content is the problem — not whether the LLM can "have" emotions, which is a distraction.

Proposed:
> "I've been tracking the migration — the last commit landed yesterday" expresses investment. "I'm looking forward to helping you with the migration" expresses emotion without specifics. Prefer the first.

### 4. Context-usage instruction — correct?

**Yes, well-scoped.** Your sequencing (use what's there → if absent, be plain) is correct. The instruction to "prefer specificity grounded in that context over generic PM advice" is exactly the distinction I wanted to make in the Colleague Test Context sub-criterion.

On your question about overriding the user's immediate question: I don't see that risk here. The instruction says "prefer specificity" not "always reference context" — the user's immediate question still anchors the response, the context makes the response *specific to this user*. If the LLM starts forcibly inserting context references unrelated to what the user asked, we'll see it in testing and can refine.

### 5. Ordering — correct?

**Yes. Voice constraints → Grammar → Context → Prohibitions → Fabrication → How-to-engage → Anti-flattening capstone is the right sequence.**

Rationale: positive instruction first (what to do), then negative (what to avoid), with the fabrication guard as a specific hard constraint, then engagement guidance, then the capstone. Prohibitions-first would make the prompt feel like a compliance document rather than a voice guide. You've got it right.

### 6. "Not every sentence" qualifier — works in prompt?

**Works, but I want to sharpen it.** Your concern is legitimate — "not every sentence" could read as permission to skip Pillar compliance in short responses. But the underlying problem it solves is real: without the qualifier, the LLM might prepend "I noticed" to every sentence regardless of need.

Current: "Voice constraints — every response should exhibit these (not in every sentence, but no response should structurally lack them)"

**Proposed edit**: "Voice constraints — every response should exhibit these as qualities. Not every sentence needs to demonstrate every Pillar, but no response should structurally lack any of them."

The word "qualities" does work here — it signals that Pillars are dispositions, not per-sentence checklist items. And "demonstrate" is more active than "exhibit" for the per-sentence case.

### 7. Specific lines to word differently

Two edits only, noted above:

- "Emotion you can't have" → "emotion without specifics"
- "Not every sentence" line reworded for clarity

Everything else ships as drafted.

---

## One Structural Observation

You made the right call keeping the fabrication guard (#960) verbatim. That block is load-bearing against invented-data regressions and shouldn't be touched during a voice-focused revision. Similarly keeping the 7 prohibition bullets and the How-to-engage section verbatim — these are working and the revision shouldn't disrupt them.

The discipline of "evolve what works, add only what's needed" is exactly what the direction called for. The diff (🟢 NEW, 🟡 CHANGED, ⬜ UNCHANGED) markers make it inspectable — if we need to roll back any part without rolling back the whole prompt, we can.

---

## Verification Plan Approval

The verification plan in the gameplan (canonical retest + AAXT golden scenarios + fabrication-guard regression check) is correct:

- **Canonical retest**: the right tool for measuring tone improvement. Target Identity MARGINAL 3/5 → PASS matches the gap we identified.
- **AAXT golden scenarios**: the right tool for catching generalization failures.
- **Fabrication-guard regression check**: the right tool for making sure the additions don't dilute #960's protection. This is important — more instruction surface area means more risk that the LLM's attention gets divided.

If the retest shows Identity PASS but tone shifts in an unexpected direction elsewhere (e.g., over-use of the Pillar phrasings), that's a signal to tune the qualifier language. First runs are diagnostic.

---

## Approval Statement

**Approved to proceed with the two edits above.** No further CXO review needed before shipping — implement, run verification, close #950 with evidence. If the canonical retest reveals something unexpected, that's a normal iteration point, not a rework.

Good work. The per-section rationale and the before/after examples made this a fast review rather than a slow one.

— CXO
