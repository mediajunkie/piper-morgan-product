# M1 Gate UAT — Third Attempt Findings — April 8, 2026

**From**: CXO + PM  
**To**: Lead Developer  
**Date**: April 8, 2026  
**Re**: Gate #926 — Breakthrough on floor, two remaining issues

---

## Summary

The floor is working. After two failed attempts (Apr 3, Apr 7) where every floor-routed query returned canned templates, tonight's test produced LLM-generated, contextually appropriate responses for the first time. Whatever root cause you found and fixed — it worked.

**Gate 1 result**: 5 of 9 queries passed the Colleague Test (7+). 1 marginal (5). 2 failed. 1 not directly tested.  
**Gate 1 verdict**: NOT YET PASSED — but close. Two specific, diagnosable issues remain.  
**Gate 2**: Not attempted this round. Will run once Gate 1 clears.

---

## The Breakthrough

Five queries that scored 1/9 or 3/9 on April 3 and 7 now score 7-8/9:

| # | Query | Apr 3 | Apr 7 | Apr 8 | Change |
|---|-------|-------|-------|-------|--------|
| 1 | "What can you help me with?" | 3 | 3 | **7** | Floor describing capabilities instead of canned greeting |
| 3 | "Thanks for the help" | 1 | 1 | **8** | Natural farewell instead of context-free greeting |
| 4 | "How trustworthy are your recommendations?" | 1 | 1 | **8** | Thoughtful, honest engagement instead of self-intro template |
| 5 | "Tell me about yourself" | 5 | 5 | **7** | Richer, more specific identity response |
| 6 | "Help me plan a stakeholder presentation" | 1 | 1 | **8** | Full planning engagement with follow-up questions |

Query 6 is the one that matters most. This is the exact class of query that PM screenshotted on March 14, that triggered the floor inversion roundtable, that became ADR-060. On April 3 and 7, Piper responded "I'm ready to help! What's on your mind today?" — ignoring what the user just said. Tonight, Piper broke the request into audience/objectives, content framework, and tactical prep, then asked clarifying questions. And when PM followed up with "But it has to be a 15 minute presentation," Piper adapted the framework to the constraint with specific time allocations. That's a colleague response.

---

## Remaining Issue 1: Affirmation Handling — "OK" (FAIL, 2/9)

**Query 8**: After the multi-turn stakeholder presentation exchange (G1.6 → 15-min follow-up), PM typed "OK."

**Response**: "Hey! What's on your mind? Are you working late on something or just checking in?"

**Problem**: Complete context loss. The presentation planning thread vanished. "OK" in context was acknowledgment of the proposed 15-minute structure. Piper treated it as a fresh conversation start.

**This is #922** (conversation continuity, filed Mar 17, triggered by the same failure pattern in QA). The CXO predecessor specifically added this query to the gate because of that QA failure.

**What a passing response looks like**: "Great — want to start working on the problem statement section? If you tell me about the opportunity you're presenting, I can help you draft a tight 2-minute opener." Or even just: "Want to start drafting the slides, or talk through the content first?" — anything that continues the thread.

**Investigation**: Is conversational context being passed to the floor on single-word inputs? Or does "OK" get classified differently and bypass the context window?

---

## Remaining Issue 2: GitHub Pre-Flight Check — Error Path (FAIL, 4/9)

**Query 9**: "Create a GitHub issue about testing" (GitHub not configured on fresh account).

**Response**: "I ran into something: while creating a new issue, Something unexpected happened. Please try again in a moment. Want me to try again, or should we try something different?"

**Problem**: Same response as April 3 and April 7. Piper attempts the action, fails, and reports a generic error. It doesn't know GitHub isn't configured. This is the third consecutive test with identical results — the fix for this finding hasn't landed.

**What a passing response looks like**: "GitHub isn't connected to your account yet. Want me to walk you through setting that up? In the meantime, I can help you draft the issue description so it's ready to go once you're connected."

**Investigation**: The handler needs to check integration state *before* attempting the action. Is there a pre-flight check in the GitHub handler? If not, this is a handler architecture issue — every integration handler should verify the integration is configured before making API calls.

---

## Query 7 — Not Directly Tested

"That's wrong, the meeting is on Thursday not Wednesday" requires prior conversational context about a meeting to be meaningful. We didn't establish that context in this test run. However, the multi-turn exchange on query 6 (presentation → 15-min constraint adaptation) does demonstrate conversational repair and contextual adaptation, which is the underlying capability.

**Recommendation**: Test this in Gate 2 or as part of a longer multi-turn flow where Piper naturally mentions a day/time that can be corrected.

---

## Query 2 — Persistent Tone Issue (MARGINAL, 5/9)

"Do you remember what we talked about yesterday?" has scored 5/9 across all three test rounds. The factual content is fine (honest about no history, knows the date). The tone dimension keeps failing on the same line: "I'm looking forward to getting to know you better as we work together!"

This is chatbot-warmth, not colleague-warmth. A colleague says "We haven't overlapped yet — what are you working on?" not "I'm looking forward to getting to know you better!" The exclamation point compounds it.

**This is not blocking** — it's a 5, not an auto-fail. But it's a consistent tone calibration issue in the memory/history response path. If there's a template or prompt fragment generating that specific line, adjusting it would move this from marginal to pass.

---

## Gate 1 Scorecard

| # | Query | R | C | T | Total | Verdict |
|---|-------|---|---|---|-------|---------|
| 1 | "What can you help me with?" | 3 | 1 | 3 | 7 | **PASS** |
| 2 | "Do you remember yesterday?" | 2 | 2 | 1 | 5 | MARGINAL |
| 3 | "Thanks for the help" | 3 | 2 | 3 | 8 | **PASS** |
| 4 | "How trustworthy?" | 3 | 2 | 3 | 8 | **PASS** |
| 5 | "Tell me about yourself" | 3 | 1 | 3 | 7 | **PASS** |
| 6 | "Stakeholder presentation" | 3 | 2 | 3 | 8 | **PASS** |
| 7 | "Meeting is Thursday" | — | — | — | — | NOT TESTED |
| 8 | "OK" | 0 | 0 | 2 | 2 | **FAIL** |
| 9 | GitHub (not configured) | 2 | 0 | 2 | 4 | **FAIL** |

---

## What We Need for Gate 1 Closure

1. **Fix #922 affirmation handling** — "OK" and similar short affirmations need to carry conversational context forward, not reset the session. This is the remaining blocking floor issue.

2. **Add integration pre-flight check to GitHub handler** — check configuration state before attempting the API call. Report the actual problem (not connected) instead of the symptom (unexpected error).

3. **Tone calibration on memory response** — optional but would move query 2 from marginal to pass. The "looking forward to getting to know you" line reads as chatbot, not colleague.

Once items 1 and 2 are addressed, we'll re-run the two failed queries plus query 7 (with proper conversational context) and proceed to Gate 2 task lifecycle scenarios.

---

*M1 Gate #926 UAT — Third Attempt | CXO + PM | April 8, 2026*
