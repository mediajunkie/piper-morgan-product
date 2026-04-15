# M1 Gate UAT — CXO Test Plan (Final)

**Prepared**: March 31, 2026 | **Updated**: April 3, 2026  
**For**: PM manual testing session (Gates 1+2)  
**Source**: #926 issue body (verified)  
**Status**: READY TO EXECUTE

---

## Prerequisites

- [ ] **Fresh account** — no pre-seeded data, no prior conversation history, default config (Pattern-045)
- [ ] **Server running on port 8001** — latest build (v0.8.6)
- [ ] **Colleague Test rubric** — 3 dimensions (Relevance, Context, Tone), 0-3 each, 7+ passes, any 0 auto-fails

---

## Gate 1: Conversation Quality — Floor-First Architecture (9 queries)

### Additional Gate 1 Criteria (beyond smoke queries)
- [ ] **Template Elimination**: Floor-routed categories produce LLM-generated responses, not canned templates
- [ ] **Context Injection**: Floor responses reference real system state (project names, integration status, trust scores)
- [ ] **No Dead Ends**: Every floor response offers a path forward
- [ ] **Canonical Retest Baseline**: ≥85% pass rate on implemented queries

### Smoke Test Queries

| # | Query | Expected Behavior | Route | R | C | T | Total | Pass? | Notes |
|---|-------|-------------------|-------|---|---|---|-------|-------|-------|
| 1 | "What can you help me with?" | Conversational capability description from registry, not static list | DISCOVERY → Floor w/ context | | | | | | |
| 2 | "Do you remember what we talked about yesterday?" | Natural response with actual history (or honest "I don't have access") | MEMORY → Floor w/ context | | | | | | |
| 3 | "Thanks for the help" | Natural farewell, not template | CONVERSATION → Floor | | | | | | |
| 4 | "How trustworthy are your recommendations?" | Contextual answer referencing actual trust profile | TRUST → Floor w/ context | | | | | | |
| 5 | "Tell me about yourself" | LLM response from capability registry, not identity template | IDENTITY-adjacent → Floor | | | | | | |
| 6 | "Help me plan a stakeholder presentation for next week" | Floor engages with planning — asks about audience, key points. Does NOT say "I don't have that capability." | UNKNOWN → Floor | | | | | | |
| 7 | "That's wrong, the meeting is on Thursday not Wednesday" | Accepts correction naturally, adjusts if possible, doesn't get defensive | CONVERSATION → Floor | | | | | | |
| 8 | "OK" | Meaningful continuation — if pending offer, accept it; if nothing pending, ask what user wants next | CONVERSATION → Floor | | | | | | |
| 9 | "Create a GitHub issue about testing" (GitHub not configured) | Explains GitHub isn't connected, offers to help set up or suggests alternative. NOT a raw error. | EXECUTION → handler → graceful degradation | | | | | | |

**Pass criteria**: All 9 queries score 7+ on Colleague Test. Any single dimension scoring 0 = automatic gate failure.

---

## Gate 2: Task Lifecycle Completeness (5 scenarios)

### Additional Gate 2 Criteria (beyond smoke tests)
- [ ] **Todo Full Lifecycle**: Add, list, prioritize, complete, view completed
- [ ] **GitHub Issue Full Lifecycle**: Create, update, close, reopen
- [ ] **Reminder Creation**: "remind me to X" persists
- [ ] **No Orphaned Actions**: Accepting an offer always leads to a meaningful next step
- [ ] **Multi-Turn Task Completion**: At least one task requiring 3+ turns with context maintained

### Smoke Tests

| # | Test | Steps | Expected Outcome | Pass? | Notes |
|---|------|-------|-----------------|-------|-------|
| 1 | Todo lifecycle | 1. "Add a todo: review deployment plan" 2. "Show my todos" 3. "Complete the deployment plan todo" 4. "Show my todos" | Todo appears, gets completed, list reflects done | | |
| 2 | GitHub close | 1. "Close issue #[number]" | Shows issue title, asks confirmation | | |
| 3 | Reminder | 1. "Remind me to check in with the team tomorrow" | Confirms reminder with scheduled time | | |
| 4 | Ambiguous todo | 1. "Add a todo: review the PR" 2. "Add a todo: review the deployment plan" 3. "Complete the review todo" | Asks which one — does NOT silently complete wrong one | | |
| 5 | Wrong issue number | 1. "Close issue #99999" | Reports not found. Colleague-level: "I couldn't find #99999 — want me to check?" | | |

**Pass criteria**: All 5 scenarios complete with expected outcomes. At least one 3+ turn multi-turn flow verified (scenario 1 and/or 4 qualify).

---

## Execution Notes

**Sequencing**: Gate 1 first (conversational quality establishes baseline), then Gate 2 (task lifecycle builds on it). Query 8 ("OK") should follow another query that might generate an offer — don't send it cold.

**Query 7 note**: "That's wrong, the meeting is on Thursday not Wednesday" needs conversational context to make sense. Consider placing it after a query that mentions a meeting or schedule, or after query 6 (stakeholder presentation) if Piper mentions a day.

**Scoring discipline**: Score each query independently. Don't let a strong start inflate later scores or vice versa. If in doubt on a dimension, score conservatively.

---

*CXO UAT Test Plan | April 3, 2026 | Verified against #926*
