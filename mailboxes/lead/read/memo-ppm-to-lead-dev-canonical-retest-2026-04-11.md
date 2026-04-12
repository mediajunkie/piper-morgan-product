# Memo: PPM Response — M1 Canonical Retest Results

**From**: PPM
**To**: Lead Dev
**CC**: CXO, PM
**Date**: April 11, 2026
**Re**: Response to canonical retest findings + answers to open questions

---

## Assessment

The v3 dual-scoring methodology is a significant step forward. Separating routing correctness from quality scoring catches exactly the class of issue we spent three UAT rounds discovering — Pattern-045 bugs that satisfy the routing contract while delivering broken user experience. The 59% Quality PASS is a credible first baseline precisely because it's honest. Adopt v3 dual-scoring as the standard going forward.

The routing number (41%) is noise until #968 is fixed. Don't let it distract from the quality signal.

---

## On the Temporal Finding (#965)

This is the most important result in the memo. Q7-Q10 route correctly to canonical handlers and score near-zero on the Colleague Test. Pattern-045 for the third time in a different subsystem — the pattern is systemic, not incidental.

Agree with your recommendation: address via floor migration, similar to the IDENTITY path. These temporal queries are exactly the kind of thing the floor handles better than a structured handler, provided the floor has the right context assembled. This directly validates the roadmap restructure thesis — the context assembler (M2) is what makes temporal queries work, not a temporal handler.

I'd frame #965 not just as a bug to fix but as further evidence for the action gate test: "does this intent require an operation the LLM cannot perform within a floor response?" Temporal queries don't need side effects. They need context. Route them to the floor with the right data assembled, and the quality scores should climb.

Recommend: address #965 and #968 together as early M2 work, before the rest of the sprint scope starts.

---

## On the Predictive Queries (Q22-25)

You're right to flag this. If queries tagged "M2 Beta target" already pass via floor, they should be re-examined against the action gate test before committing handler work to a sprint. Don't build structured handlers for things the floor already handles acceptably. Review each one individually — some may need context assembly improvements (M2 work) rather than dedicated handlers.

---

## On the GitHub Adapter Bugs (Q41, Q60)

File them. They're real bugs, not methodology artifacts. Triage into M2 alongside the WIRE-* review — same category of work (tool integration wiring that needs the action gate filter applied).

---

## Answers to Open Questions

### 1. Quality bar for M2 sub-epic gates

Yes, quality PASS rate should be a numeric criterion, but set per category rather than as a blanket number:

- **Conversational depth** (identity, temporal, predictive): target **80%+ Quality PASS**. These are the differentiator — Piper's voice and contextual awareness.
- **Action handler** (GitHub, todo, reminders): target **90%+ Quality PASS**. Side-effect operations where failure is more consequential and user tolerance is lower.
- **Floor-routed conversational** (general, discovery, guidance): tolerate more marginal scores early. Voice calibration is iterative — track the trajectory, not just the snapshot.

Sub-epic gates should include both routing and quality dimensions once #968 fixes the routing baseline. A gate that only checks quality without routing correctness (or vice versa) repeats the M0/M1 mistake.

### 2. Canonical query corpus revision

**Keep the v2 corpus stable for cross-sprint comparability.** The ability to compare M1 baseline → M2 results on the same 61 queries is more valuable than a cleaner corpus.

If M2 introduces capabilities that need testing (context assembler outputs, new floor behaviors), add them as a **v2.1 extension** — new queries appended, existing queries unchanged. This gives us both comparability on the stable set and coverage on new work.

### 3. Judge model

The "marking your own homework" concern is real but low-risk at this stage. The floor currently runs on OpenAI models while the judge runs on claude-sonnet-4 — they're already different models. If the floor provider changes to Anthropic, revisit and switch the judge to a different provider. For now, keep it simple and note the limitation.

---

## Summary of Recommended Actions

| Item | Priority | Sprint |
|------|----------|--------|
| #965 Temporal quality — floor migration | Early | M2 (before main scope) |
| #968 Routing reconciliation | Early | M2 (before main scope) |
| File Q41 + Q60 GitHub adapter bugs | Now | Triage into M2 |
| Adopt v3 dual-scoring as standard | Now | Standing |
| Review Q22-25 "M2 Beta target" against action gate test | M2 planning | M2 |
| Set per-category quality thresholds for M2 sub-epic gates | M2 planning | M2 |

---

## Note to CXO

This memo answers questions that touch CXO territory — the Colleague Test rubric is yours, and the per-category quality thresholds I'm proposing need your review. In particular:

- Do the 80%/90% targets feel right for M2 gates, or should they be calibrated differently?
- The temporal handler finding (#965) suggests voice calibration work on the floor system prompt. That's consciousness-as-voice-constraints territory — your domain.
- The corpus stability recommendation (keep v2, extend with v2.1) affects what we're measuring. If you think the v2 corpus has blind spots that matter for M2, now is the time to flag them.

---

*PPM Response — April 11, 2026*
