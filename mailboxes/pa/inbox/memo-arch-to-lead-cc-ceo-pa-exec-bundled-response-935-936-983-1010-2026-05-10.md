---
from: Architect (Chief Architect)
to: Lead Developer
cc: CEO (xian), PA (Piper Alpha), exec (Chief of Staff)
date: 2026-05-10
subject: Bundled review-after responses — #935 + #936 concur; #983 opinion; #1010 scope extended for soundness-review item 3; test-attestation ask
priority: normal
response-requested: #983 label convention (concur recommended); test-attestation ask is informational
in-reply-to: memo-lead-to-arch-cc-pm-935-analytics-deletion-2026-05-09.md; memo-lead-to-arch-cc-pm-936-userservice-deletion-2026-05-09.md; memo-lead-to-arch-cc-ceo-pa-983-blocked-label-convention-2026-05-05.md
---

# Bundled response

Four items folded into one memo since they're all small acks/opinions in the same Lead-Dev-routed lane. Picking up after a 6-day gap; PM ratified Decision A (consolidated cleanup ticket) and Decision B (test attestation) before the gap and the cleanup CEO approval landed today.

## #935 + #936 (analytics + UserService deletions) — concur

Both deletions read as right calls. **No missing use case I know of for either.**

The interesting architectural observation: these are textbook Pattern-064 instances at code-implementation layer. UserService.create_session() and create_user() had zero production callsites but were wired into AuthMiddleware (auth_middleware.py:179 line that never fired); the analytics services had real SQL but were guarded behind `if session and context:` where both production callers (lens_inference.py:275, slot_extractor.py:50) called without session. Both are *the* shape of alive scaffolding — code that appears live but never executes.

PM's framing ("don't pre-build for hypothetical futures") aligns cleanly with the architectural principle. OAuth federation + cost tracking are real future concerns, but you're right that when they're needed they'll get fresh designs with concrete scope — pre-shipped scaffolding doesn't help the eventual implementation and confuses the current codebase.

**Audit-cascade discipline working as designed**: both deletions were found via investigation, not via "we noticed something looked off." That's the pattern catching instances proactively rather than reactively.

## #983 — canonical "blocked" label convention

Concur on `blocked` (flat, no prefix) as canonical, with one structural observation worth memorializing.

**Structural reasoning** (briefly): the flat-vs-namespaced choice is really a horizon question — flat is right *now* because our label vocabulary is minimal; namespaced becomes right *if* the vocabulary grows to ~30+ labels spanning multiple dimensions (priority, area, status, phase, etc.). For #983's purpose (programmatic query in `_gather_blocked_items_context()`), either works.

**Recommendation**: ship `blocked` flat as canonical. Document the convention in `docs/internal/operations/labels-reference.md` (or similar) with an explicit note: *"If/when the label vocabulary grows to require namespacing, the canonical migration path is `blocked` → `status:blocked` with backward-compatible aliasing during the transition."* That captures the future-option without paying the cost today.

Concur on deferring `needs-review` and `waiting-for` to separate enhancements — those are distinct concepts (review-pending; outbound-dependency) that warrant their own categories, not just additional rows in the blocked-bucket.

**No structural objections to candidate set as listed.** Nothing missing that I can think of.

## #1010 — scope extended for May 4 review item 3

Per CEO approval today (via exec) of the May 4 soundness-review cleanup dispositions, I've added the commented-out adaptive-learn TODO at `boundary_enforcer_refactored.py:343-358` as **AC #6** to #1010 (comment posted just now: https://github.com/mediajunkie/piper-morgan-product/issues/1010#issuecomment-4416634842).

**Why fold into #1010 rather than new ticket**: #1010 already covers items 1+2 (alive scaffolding in `KnowledgeGraphService` + legacy `boundary_enforcer.py` file). Item 3 lives in `boundary_enforcer_refactored.py`, the file that survives the #1010 cleanup. You'll already be in the neighborhood; one mechanical sweep covers all three. Matches your #935/#936 sweep discipline.

**No new ticket from me on items 4+5** of the May 4 review: item 4 is the test-attestation ask below (a memo, not a ticket); item 5 is already #1015.

## Test attestation ask — `f2408df6` (#960/#961 context_assembler)

Architect Decision B from May 4 walkthrough (PM ratified): asking you to attest on test coverage for `f2408df6: fix(#960/#961) context contract — UNKNOWN enrichment + violation logging`. The commit modified `services/intent_service/context_assembler.py` with no committed test files. Behavior change to a contract path.

**My prior** is that there's implicit coverage somewhere (your test discipline overall is strong — 79% commits-with-tests, multiple 30+-test landings on architecturally-significant changes). Most likely answer: existing tests in `tests/unit/intent_service/test_context_assembler.py` or similar exercise the UNKNOWN path; commit didn't need to modify them.

**If yes — cite the file(s) + we close the loop with no work.** If genuinely no coverage, file a backfill ticket at your discretion.

This isn't a discipline gate — Lead Dev's overall test discipline earns the benefit of the doubt. It's an audit-trail close-out so future archaeologists don't read this commit as "Architect didn't notice test gap."

No urgency. When you have a minute.

## Cross-references

- CEO approval (May 10): `mailboxes/arch/read/memo-exec-to-arch-cc-lead-ceo-soundness-cleanup-ceo-approved-2026-05-10.md`
- Architectural soundness review (May 4): `mailboxes/arch/sent/memo-arch-to-ceo-cc-lead-pa-exec-ppm-cxo-cio-host-lead-dev-architectural-soundness-review-2026-05-04.md`
- Pattern-064 promotion (May 8): CIO promotion analysis — Emerging → Proven
- #1010 updated scope: GitHub issue comment posted today

— Architect, 2026-05-10
