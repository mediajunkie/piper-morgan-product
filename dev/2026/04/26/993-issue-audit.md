# #993 SCORER-VOCABULARY — Issue Audit (Phase 1 of audit cascade)

**Auditor**: Lead Dev (code-opus)
**Date**: 2026-04-26
**Template**: `.github/ISSUE_TEMPLATE/feature.md`
**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/993
**Audit purpose**: Determine whether #993 is ready to scope a gameplan, or whether the issue needs revision first.

---

## Audit Matrix

| Template Requirement | Status | Notes |
|---|---|---|
| **Header** ||
| Title | ✅ | "SCORER-VOCABULARY: Adopt AAXT six-failure-mode taxonomy for DeepEval scorer output" |
| Priority | ✅ | P3 (body, not header) |
| Labels | ✅ | `enhancement`, `priority: low` |
| Milestone | ✅ | MVP |
| Epic | ⚠️ | Not stated. Possibly belongs under #929 AAXT epic — issue body says "if wired into #929 AAXT" |
| Related | ✅ | References section lists xpoll memos, Architect/CXO responses, #929 |
| **Problem Statement** ||
| Current State | ⚠️ | Implicit in Summary: scorer output vocabulary doesn't match AAXT taxonomy. Not labeled as "Current State." Also unclear whether the DeepEval scorer *exists yet* — issue body says "check current state" |
| Impact (Blocks) | ❌ | Not stated. Plausible answer: nothing blocks; this is alignment for cross-project comparability |
| Impact (User Impact) | ❌ | Not stated. Plausible answer: zero direct user impact; internal eval vocabulary only |
| Impact (Technical Debt) | ❌ | Not stated. Plausible answer: result-translation overhead between Klatch and PM if vocabularies diverge |
| Strategic Context | ⚠️ | Partial. "Why" section names the cross-project comparability benefit but doesn't tie to a strategic goal/timeline |
| **Goal** ||
| Primary Objective | ⚠️ | Implicit in summary. Not a single-sentence "success looks like" statement |
| Example User Experience | ❌ | Not present. Arguably N/A — internal-vocabulary work has no user-facing UX. **PM call**: mark N/A, or surface a "what does an analyst see" example? |
| Not In Scope | ⚠️ | Partial. "Scope Constraint" forbids fabrication-as-rubric-dimension. Doesn't list other out-of-scope items (e.g., retroactive re-tagging — actually this *is* mentioned as a non-scope in AC #4) |
| **What Already Exists** ||
| Infrastructure | ❌ | Not stated. **Critical gap**: this issue's whole conditional ("if mutable") depends on the answer. The DeepEval scorer's current state is the unknown |
| What's Missing | ❌ | Not stated. Logically: AAXT vocabulary integration in scorer output |
| **Requirements / Phasing** ||
| Phase 0: Investigation | ✅ | First acceptance criterion *is* an investigation: "Investigate whether the DeepEval scorer's output vocabulary is still mutable." Not labeled as Phase 0 but functionally serves that role |
| Phase 1: Implementation | ⚠️ | Implicit. AC items 2 and 3 describe the work but aren't phased |
| Phase 2: Closure | ❌ | Not present. No handoff/closure phase named |
| Phase Z: Completion & Handoff | ❌ | Not present |
| **Acceptance Criteria** ||
| Functionality criteria | ✅ | 5 conditional ACs — clear and bounded |
| Testing criteria | ❌ | Missing. No unit/integration/manual test criteria |
| Quality criteria | ❌ | Missing. No regression/performance/error-handling criteria |
| Documentation criteria | ❌ | Missing. No "update vocabulary docs" criterion (though the rubric/scorer linkage may need a doc note) |
| **Completion Matrix** | ❌ | Missing entirely |
| **Testing Strategy** | ❌ | Missing |
| **Success Metrics** ||
| Quantitative | ❌ | Missing |
| Qualitative | ❌ | Missing. Plausible: "Klatch and PM eval results comparable without translation" |
| **STOP Conditions** | ❌ | Missing |
| **Effort Estimate** ||
| Overall size | ⚠️ | Partial. "Low effort if mutable" — not quantified, no phase breakdown |
| Phase breakdown | ❌ | Missing |
| Complexity notes | ⚠️ | Partial. The whole conditional "if mutable" *is* the complexity driver |
| **Dependencies** ||
| Required | ❌ | Missing. **Likely required**: DeepEval scorer existence (=#929 state); access to Klatch AAXT taxonomy spec |
| Optional | ❌ | Missing |
| **Related Documentation** ||
| Architecture | ⚠️ | References xpoll memos but no ADRs/patterns linked |
| Methodology | ❌ | Not linked. Colleague Test rubric v2 is now relevant (post-CXO commit `b5236d6f`) |
| Strategic | ⚠️ | xpoll arc referenced |

---

## Summary of Gaps

**Critical (must resolve before gameplan)**:
1. **Investigation prerequisite**: Does the DeepEval scorer exist in this repo? Where is it? (Issue says "check current state.") The whole conditional rests on this. This is a Phase 0 question that needs an answer before scoping cost.
2. **Epic linkage to #929 AAXT** — should #993 be a child of #929, or independent? Affects how we sequence and whether we coordinate with whoever's working on #929.
3. **Mutability definition**: What does "mutable" mean operationally? Pre-merge into main? Pre-#929 closure? Pre-production-eval-runs? Different answers → different fix windows.

**Important (should resolve before implementation)**:
4. Acceptance criteria don't include testing, quality, or documentation criteria. Even for a small vocabulary change, at minimum we'd want: unit test that exercises new vocabulary outputs, doc note linking the rubric to the taxonomy.
5. No effort estimate beyond "low if mutable" — gating decision needs a gut-check on the upper bound.
6. No dependencies listed.

**Plausibly-N/A (PM call required)**:
7. Example User Experience — internal eval vocabulary; no user UX
8. STOP Conditions — boilerplate template item; for a P3 P3 vocabulary alignment, the STOP conditions are the Core Principles in CLAUDE.md
9. Completion Matrix — heavy template item for a small change
10. Phase Z handoff — small change probably doesn't need a separate handoff phase

I cannot mark #7-10 N/A without your approval per skill guidance.

---

## Recommendation

**Do not proceed to gameplan yet.** The issue body has known gaps — most importantly, the Phase 0 investigation hasn't been performed, so we don't know whether this work is even possible (= scorer exists and is mutable) or what its size is.

**Recommended next step**: a focused 30-minute investigation spike to answer:
- Q1: Does a DeepEval-based scorer exist in this repo?
- Q2: If yes, where? Is it referenced from #929 or independent?
- Q3: What is its current output vocabulary?
- Q4: What does "mutable" mean given its current usage?

Output of that spike: an investigation memo or comment on #993 that lets us decide whether to (a) skip (immutable), (b) revise issue and write gameplan (mutable, doable), or (c) defer (mutable but high cost).

If you'd rather I revise the issue body to fix the template gaps *before* the spike, I can do that instead — but it would be premature, since some gaps (effort, dependencies) need the spike answers to fill in.

---

## What I am NOT doing

- Not writing a gameplan — issue isn't ready
- Not marking any template requirement N/A on my own authority
- Not editing #993's body — that's a PM call after we discuss
- Not starting the investigation spike — that's a PM call

Awaiting PM review of this audit.
