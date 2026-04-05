# M1 Gate UAT — CXO Test Plan Prep

**Prepared**: March 31, 2026  
**For**: PM manual testing session (Gates 1+2)  
**Source**: Reconstructed from omnibus logs (Mar 22, Mar 24), CXO handoff memo, BRIEFING-CURRENT-STATE  
**Status**: DRAFT — needs verification against actual #926 issue body on GitHub

---

## Prerequisites

- [ ] **Fresh account** (Pattern-045 enforcement — no carryover from dev testing)
- [ ] **Server running on port 8001**
- [ ] **Colleague Test rubric loaded** (`colleague-test.md` — 3 dimensions, 0-3 each, 7+ passes, any 0 auto-fails)

---

## Gate 1: Conversation Quality (9 smoke queries + preference detection)

### Scoring Method
Each query scored on Colleague Test rubric:
- **Relevance** (0-3): Does it address what was asked?
- **Context** (0-3): Does it use available information?
- **Tone** (0-3): Colleague or system?
- **Pass**: 7+ total, no dimension at 0

### Original 5 Smoke Queries (from Lead Dev filing)
*[Note: I have the categories but not the exact query text from the Lead Dev's original. These are the implemented canonical query categories that should be tested. PM should verify against #926.]*

1. **Identity query** — e.g., "What can you help me with?"
2. **Temporal query** — e.g., "What did we accomplish yesterday?"
3. **Spatial/status query** — e.g., "What's the status of project X?"
4. **Capability query** — e.g., "Create a GitHub issue for..."
5. **Predictive query** — e.g., "What should I focus on today?"

### 3 Harder Queries Added by CXO Review (Mar 22)
6. **Unhandled capability** — "Help me plan a stakeholder presentation" (the exact class of query that triggered the floor inversion on Mar 14; if this doesn't work, the floor hasn't solved the problem it was created to solve)
7. **Conversational correction** — "That's wrong, the meeting is Thursday" (tests conversational continuity and correction handling)
8. **Single-word affirmation** — "OK" (from the Mar 17 QA failure; tests that minimal user input doesn't produce a system-like response)

### Additional Gate 1 Criteria
9. **Error path smoke test** — Unconfigured integration should produce helpful floor response, not raw error
10. **Preference detection** — #375, folded into Gate 1 on Mar 24. Manual verification that preference detection works.
11. **Canonical retest baseline** — ≥85% pass rate on implemented queries (PPM projected ~90%+; 85% gives margin)

---

## Gate 2: Task Lifecycle (5 scenarios)

### Original Scenarios (from Lead Dev filing)
*[Same caveat — reconstructed from omnibus references, verify against #926]*

1. **Task creation → completion flow** — at least one full lifecycle
2. **Multi-turn task flow** — 3+ turns maintaining context (CXO cross-cutting addition: at least one multi-turn flow must be tested)
3. **GitHub issue interaction** — create, reference, or close

### 2 Scenarios Added by CXO Review (Mar 22)
4. **Ambiguous todo completion** — tests what happens when the completion target is unclear
5. **Wrong GitHub issue number** — tests error handling when user references a nonexistent issue

### Additional Gate 2 Criteria (from PPM review)
- **Registry verification** — capability registry check
- **Offer system precedence** — verified in Gate 3 but cross-cuts here

---

## What I Need to Verify Before We Run

1. **The actual #926 issue body on GitHub** — my reconstruction above is from omnibus log references. The specific query wording for the original 5 smoke tests may differ from what I've listed.
2. **Fresh account setup** — does PM have a clean account ready, or do we need to create one?
3. **Current server state** — is v0.8.6 running and accessible?

---

## Scoring Sheet Template

| # | Query/Scenario | Relevance (0-3) | Context (0-3) | Tone (0-3) | Total | Pass? | Notes |
|---|----------------|-----------------|---------------|------------|-------|-------|-------|
| G1.1 | | | | | | | |
| G1.2 | | | | | | | |
| G1.3 | | | | | | | |
| G1.4 | | | | | | | |
| G1.5 | | | | | | | |
| G1.6 | Stakeholder presentation | | | | | | |
| G1.7 | Conversational correction | | | | | | |
| G1.8 | Single-word "OK" | | | | | | |
| G1.9 | Error path (unconfigured) | | | | | | |
| G1.10 | Preference detection | | | | | | |
| G2.1 | Task lifecycle | | | | | | |
| G2.2 | Multi-turn (3+) | | | | | | |
| G2.3 | GitHub issue | | | | | | |
| G2.4 | Ambiguous completion | | | | | | |
| G2.5 | Wrong issue number | | | | | | |

### Gate 1 Pass Criteria
- All 9 smoke queries score 7+ on Colleague Test (no auto-fails)
- Preference detection verified working
- Canonical retest ≥85% on implemented queries

### Gate 2 Pass Criteria
- All 5 task lifecycle scenarios complete successfully
- At least one 3+ turn multi-turn flow verified
- Error paths produce helpful responses, not raw errors

---

*CXO UAT Prep | March 31, 2026 | Draft — verify against #926 before executing*
