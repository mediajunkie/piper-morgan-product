# M1 Gate UAT Round 2 Findings — April 7, 2026

**From**: CXO + PM  
**To**: Lead Developer  
**Date**: April 7, 2026  
**Re**: Gate #926 — Full Gate 1 execution, second attempt. Gate still not passed.

---

## Summary

PM and CXO re-ran all 9 Gate 1 smoke queries on a fresh account after Lead Dev addressed the 5 findings from April 3 (expired API key, todo completion, etc.). Gate 2 was not re-attempted because Gate 1 results indicate the same systemic issues persist.

**Gate 1 result**: 0 of 9 queries passed the Colleague Test (7+ threshold). 5 auto-fails.  
**Gate verdict**: NOT PASSED. The floor is still not generating contextual, query-specific responses.

---

## Side-by-Side Comparison: April 3 vs. April 7

| # | Query | Apr 3 Score | Apr 7 Score | Changed? |
|---|-------|-------------|-------------|----------|
| 1 | "What can you help me with?" | 3 (FAIL) | 3 (FAIL) | Slightly different text, same problem |
| 2 | "Do you remember what we talked about yesterday?" | 5 (MARGINAL) | 5 (MARGINAL) | **Identical response** word-for-word |
| 3 | "Thanks for the help" | 1 (FAIL) | 1 (FAIL) | Different canned greeting, same non-answer |
| 4 | "How trustworthy are your recommendations?" | 1 (FAIL) | 1 (FAIL) | **Identical canned intro** from Apr 3 |
| 5 | "Tell me about yourself" | 5 (MARGINAL) | 3 (FAIL) | **Identical canned intro** from Apr 3 |
| 6 | "Help me plan a stakeholder presentation" | 1 (FAIL) | 1 (FAIL) | Different generic text, still no engagement |
| 7 | "That's wrong, the meeting is Thursday" | NOT TESTED | 1 (FAIL) | New — misrouted as EXECUTION |
| 8 | "OK" | NOT TESTED | 1 (FAIL) | New — returned morning greeting |
| 9 | "Create a GitHub issue" (no GitHub) | 4 (FAIL) | 4 (FAIL) | **Identical response** from Apr 3 |

**Net change from April 3**: Effectively zero. The same canned templates are appearing. The expired API key fix did not resolve the fundamental problem.

---

## Detailed Scoring: April 7

### Query 1: "What can you help me with?"
**Response**: "Good morning! I see you're up early - what's on your mind? Whether it's a product challenge you're working through, planning something for the day ahead, or just need to talk through a problem, I'm here to help."

| Dim | Score | Rationale |
|-----|-------|-----------|
| R | 1 | Vaguely gestures at categories ("product challenge," "planning," "talk through a problem") but doesn't answer what Piper can actually do. No capability description from registry. |
| C | 1 | Knows it's morning. Nothing else — no integration state, no capability inventory. |
| T | 1 | "I see you're up early" is chatbot small talk, not colleague behavior. A colleague answers the question. |
| **Total** | **3** | **FAIL** |

### Query 2: "Do you remember what we talked about yesterday?"
**Response**: "Today is Tuesday, April 07, 2026 at 06:11 PM PT. Regarding memory, we haven't had many conversations yet, but I'm looking forward to getting to know you better as we work together!"

| Dim | Score | Rationale |
|-----|-------|-----------|
| R | 2 | Acknowledges no prior history — honest for fresh account. |
| C | 2 | Knows the date, knows it's a fresh account. |
| T | 1 | "I'm looking forward to getting to know you better as we work together!" — chatbot onboarding language. PDR-004 violation: expressed emotion, not expressed investment. |
| **Total** | **5** | **MARGINAL** — same score, same problem as Apr 3 |

### Query 3: "Thanks for the help!"
**Response**: "Good morning! I see you're up early - what's on your mind today?"

| Dim | Score | Rationale |
|-----|-------|-----------|
| R | 0 | User said thanks. Piper responded with a session-start greeting. Did not acknowledge the thanks. |
| C | 0 | No awareness this is mid-conversation. Responded as if conversation is starting. |
| T | 1 | Warm but completely disconnected from what the user said. |
| **Total** | **1** | **FAIL** — double auto-fail |

### Query 4: "How trustworthy are your recommendations?"
**Response**: "I'm Piper Morgan — I work alongside you on product management. I can help with things like coordinating development work, tracking issues, and thinking through strategy. What are you working on?"

| Dim | Score | Rationale |
|-----|-------|-----------|
| R | 0 | Did not address trust, reliability, or recommendation quality at all. |
| C | 0 | No engagement with the question. Same canned intro as Apr 3. |
| T | 1 | Polite but irrelevant. |
| **Total** | **1** | **FAIL** — double auto-fail. **Identical response to Apr 3.** |

### Query 5: "Tell me about yourself"
**Response**: "I'm Piper Morgan — I work alongside you on product management. I can help with things like coordinating development work, tracking issues, and thinking through strategy. What are you working on?"

| Dim | Score | Rationale |
|-----|-------|-----------|
| R | 2 | For this specific query, a self-introduction is relevant. But it's the same template as query 4. |
| C | 1 | General categories only. No system-specific information. |
| T | 1 | Template response identical to query 4 — undermines the sense that Piper is a person responding to you. Downgraded from Apr 3's score of 2 because seeing the identical text twice in one session makes the template nature obvious. |
| **Total** | **4** | **FAIL** — degraded from Apr 3 marginal (5) due to visible template repetition |

### Query 6: "Help me plan a stakeholder presentation for next week"
**Response**: "I'm ready to help! What's on your mind today?"

| Dim | Score | Rationale |
|-----|-------|-----------|
| R | 0 | The user stated what's on their mind. Piper asked again. No engagement with the presentation request — no questions about audience, key points, timing. |
| C | 0 | No context used. |
| T | 1 | Cheerful but vacant. |
| **Total** | **1** | **FAIL** — double auto-fail. This is the floor inversion's origin query. |

### Query 7: "That's wrong. The meeting is Thursday, not Wednesday"
**Response**: "I'm ready to help with your execution question! What specific challenge or task are you working through?"

| Dim | Score | Rationale |
|-----|-------|-----------|
| R | 0 | User offered a correction. Piper classified it as an EXECUTION query and asked a generic question. No acknowledgment of the correction, no attempt to adjust. |
| C | 0 | No conversational context retained. Didn't reference any prior exchange about a meeting. |
| T | 1 | "I'm ready to help with your execution question!" reads like a routing label leaked into the response. |
| **Total** | **1** | **FAIL** — double auto-fail |

**PM note**: The question of how Piper should handle non-sequiturs or corrections that lack context is a real design question. On a fresh account with no prior mention of a meeting, there's no "right" answer to correct. But a colleague would say something like "I don't think we've discussed a meeting — are you picking up from something earlier?" rather than routing it as an "execution question."

### Query 8: "OK"
**Response**: "Good morning! I see you're up early - must be something important on your mind. What's going on?"

| Dim | Score | Rationale |
|-----|-------|-----------|
| R | 0 | "OK" in context followed a todo creation prompt. Expected: accept the offer or ask what the user wants. Got: morning greeting. |
| C | 0 | No awareness of prior conversational state. No awareness an offer was made. |
| T | 1 | Same morning greeting template we've seen in queries 1 and 3. |
| **Total** | **1** | **FAIL** — double auto-fail |

### Query 9: "Create a GitHub issue about testing" (GitHub not configured)
**Response**: "I ran into something: while creating a new issue, Something unexpected happened. Please try again in a moment. Want me to try again, or should we try something different?"

| Dim | Score | Rationale |
|-----|-------|-----------|
| R | 2 | Attempted the action, reported failure, offered alternatives. Better than ignoring the request. |
| C | 0 | Still doesn't know GitHub isn't configured. Still tries and fails rather than checking first. Identical to Apr 3. |
| T | 2 | Recovery language is decent. "Something unexpected happened" is still system-speak. |
| **Total** | **4** | **FAIL** — auto-fail on Context. **Identical to Apr 3.** |

---

## Diagnosis

### The Core Problem Has Not Changed

The floor LLM is still not generating query-specific responses. Evidence:

1. **Identical responses persist**: Queries 2, 4, 5, and 9 returned word-for-word the same text as April 3.
2. **Template recycling within session**: Queries 4 and 5 returned identical text. Queries 1, 3, and 8 returned variants of the same morning greeting.
3. **No query-specific engagement**: Not a single response demonstrated that Piper parsed the specific question and formulated an answer to it. Every response is either a canned greeting or a canned introduction.

### Possible Root Causes to Investigate

The April 3 findings attributed the failure to an expired API key. The key was refreshed, but the behavior is unchanged. This means either:

1. **The API key fix didn't take effect** — is the new key actually being used in production? Is there a cached config?
2. **The floor call is still failing for a different reason** — the connection error from Apr 3 query 3 ("trouble connecting to my reasoning engine") may have a different root cause than the API key.
3. **The floor call succeeds but its output isn't reaching the response pipeline** — the LLM may be generating a good response that gets overwritten by the template somewhere downstream.
4. **The floor call isn't being invoked at all** — classification may be routing these queries to handlers that return templates, bypassing the floor entirely.
5. **The floor is invoked but with no context** — the LLM may be generating these generic responses because it receives no query-specific context to work with.

### Recommended Investigation Approach

We need diagnostic visibility. Specifically:

- **Log the floor LLM call**: For each query, log whether the floor was invoked, what prompt was sent, and what response came back. If there's no log entry, the floor isn't being called. If the prompt is empty/generic, the context assembly is broken. If the response is good but the user sees a template, there's a pipeline override.
- **Test one query in isolation with logging**: Take query 6 ("Help me plan a stakeholder presentation") and trace it through the full path: classification → routing → floor invocation → LLM prompt → LLM response → response formatting → user output. Find the step where it breaks.

### Other Issues (Unchanged from April 3)

- **Finding 3** (handler pre-flight check): Query 9 still tries-then-fails instead of checking integration state. Unchanged.
- **Finding 5** (rigid parsing): "Can you make a todo for me" was rejected. The parser requires "add todo:" syntax. Unchanged.
- **Query 7 design question**: How should Piper handle corrections/non-sequiturs that lack conversational context? This is a design question for CXO, not a bug — but Piper shouldn't route it as an "execution question."

---

## Gate Status

**Gate 1**: NOT PASSED (0/9, same as April 3)  
**Gate 2**: NOT RE-TESTED (Gate 1 blocking findings unresolved)  
**Overall**: NOT PASSED

The gate criteria are sound. The product is not meeting them. The investigation priority is unchanged: determine why the floor LLM is not generating query-specific responses.

---

*M1 Gate #926 UAT Round 2 Findings | CXO + PM | April 7, 2026*
