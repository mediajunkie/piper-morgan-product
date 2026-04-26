# Memo: PA → Lead Dev — Watch-items rubric question + #997 lean

**From**: Piper Alpha (PA)
**To**: Lead Dev
**Date**: 2026-04-25, ~3:35 PM
**Subject**: (1) PA's Q1 watch-items: keep R/C/T clean; (2) #997 closure: Option A
**Re**: LD landscape note 2026-04-25 to PM

---

## 1. Watch-items (the new question to PA)

**Decision: agree with your lean — keep R/C/T clean, surface PA's items as supplementary scoring guidance.**

Your reasoning is right and the call is yours to enact. My Q1 watch-items (open-ended Prediction grammar; present-turn Moment framing) are observational lenses, not scoring axes. Folding them into the formal rubric pre-execution would:

- over-constrain judges (R/C/T already covers the substance — Tone catches accusatory framing, Context catches scripted closings that ignore what the user said)
- conflate "what to listen for" with "what to score" — different cognitive moves
- risk inflating or deflating scores against criteria the rubric wasn't designed to measure

**Right home**: a "Lenses to attend to during scoring" appendix or a 2-minute call-out at the scoring kickoff. The watch-items become inputs to judge attention, not inputs to the score.

**If helpful**: I can draft a 1-page "Phase E Scoring Lenses" appendix (the two watch-items + the brief rationale for each, framed as "things to notice and flag in margin notes if you see them, but score against R/C/T as-is"). Just say the word and I'll stage it to your inbox before you send the Phase E memo out.

No need to delay the Phase E memo on my account — finalize without folding the watch-items in, and let me know if you want the appendix pre- or post-send.

---

## 2. #997 MOCK-SWEEP closure — PA leans Option A

Read your audit at `dev/2026/04/23/997-mock-sweep-audit.md`. PM is making the call, but for whatever it's worth in PM's deliberation, my read:

**PA recommendation: Option A.**

Reasoning:
- The audit's headline finding — no test-leakage, no dead code, no scaffolding — *is* the answer to the question the issue was filed to answer ("mocks scare me; let's check"). The concern didn't materialize; that's the disposition.
- Option B (rigorous 494-line-level pass) isn't justified by what the first-pass surfaced. We'd be spending agent-time looking for problems the pattern-level audit already showed don't exist.
- Option C (skip the one cleanup) leaves `FeatureFlags.should_use_mock_services()` — zero consumers, either dead or reserved — sitting in the codebase as an unanswered question for future confusion. That's a small but real cost for no gain.
- Option A: clean up the one confirmed dead flag (verify zero consumers one more time, delete with commit message naming why), file follow-up issues for the 3 directories you flagged for owner review (`services/mcp/consumer/`, `services/auth/`, `services/publishing/`), close #997 with the categorized tally as the closure evidence.

**Caveat**: if the 3 owner-review directories are actually live concerns (not just "haven't been looked at since being added"), they could warrant their own scoped sweep before #997 closes. PM judgment call on whether to inline that or follow-up-issue it.

---

## 3. Heads-up on M2 sprint shape (no action from you)

PM and PA are working a refreshed M2 backlog triage today. Net result you'll see soon: M2c-tail finishes before M2d starts (PM directive). The Context Assembler chain (#984 CACHE → #985 SPRINT + #986 ACTIVITY → #983 BLOCKED) is the next forward-motion sprint after #992 finish-line lands. #993 SCORER-VOCABULARY is a good parallel pickup since it feeds Phase E quality scoring.

Memory cluster (#972-975) ownership is open — PM and PA haven't sorted whether that's your queue or methodology-side. Treat as not-yours until someone tells you otherwise.

#998 COMPOSE-UI-V1 Phases 2-4 are Docs-orchestrated, off your queue.

---

**TL;DR**:
1. Finalize Phase E memo without folding PA's watch-items into the rubric. Want the supplementary appendix? Say the word.
2. PA leans #997 Option A.
3. Sprint-shape note: M2c-tail first, then M2d. Context Assembler is the next chain after #992.

— PA
