# M1 Gate UAT Findings — April 3, 2026

**From**: CXO + PM  
**To**: Lead Developer  
**Date**: April 3, 2026  
**Re**: Gate #926 — Gates 1 and 2 partial execution, blocking findings

---

## Summary

PM and CXO ran Gate 1 and Gate 2 scenarios on a fresh account (Pattern-045 compliant) against v0.8.6 on port 8001. Testing was stopped after 7 of 9 Gate 1 queries and 1 of 5 Gate 2 scenarios due to systemic failures that would make further testing unproductive.

**Gate 1 result**: 0 of 7 queries tested passed the Colleague Test (7+ threshold). 4 auto-fails (any dimension scoring 0).  
**Gate 2 result**: 1 of 5 scenarios attempted. Todo lifecycle failed at the completion step.  
**Gate verdict**: NOT PASSED. Requires investigation and fixes before re-test.

---

## Finding 1: Floor LLM Is Not Reaching the User (BLOCKING)

**Queries affected**: G1.1, G1.3, G1.4, G1.5, G1.6 — and likely G1.7, G1.8 (not tested)

Five of six floor-routed queries returned the same canned response, nearly word-for-word:

> "I'm Piper Morgan — I work alongside you on product management. I can help with things like coordinating development work, tracking issues, and thinking through strategy. What are you working on?"

This response appeared for DISCOVERY, CONVERSATION, TRUST, IDENTITY-adjacent, and UNKNOWN category queries. The floor-first architecture (ADR-060) specifies that these categories should route to the LLM with assembled context. Instead, a single fallback template is being returned regardless of input.

**Evidence of the floor existing but not connecting**: Query G1.3 (first attempt) produced a different failure — "I'm having trouble connecting to my reasoning engine right now" — which confirms the floor LLM call exists in the code path but failed to connect. The fallback for that failure appears to be the same canned introduction template.

**Possible root causes to investigate**:
- LLM floor call failing/timing out silently, with the template as fallback
- Floor routing not actually reaching the LLM call (short-circuited before the call)
- Template response overriding floor response in the response pipeline

**Impact**: This is the central promise of M1. The gate criteria checkbox "Template Elimination" is not met. The gate criteria checkbox "Context Injection" is not met.

---

## Finding 2: Canned Introduction Template Masks All Failures (BLOCKING)

The same ~30-word introduction serves as the response for at least 5 different query types. This means:

- Users cannot distinguish between "Piper doesn't understand" and "Piper's LLM is down"
- PM cannot diagnose whether classification is working (all roads lead to the same output)
- The system appears functional when it is not

**Recommendation**: Even if the floor fix takes time, the fallback template should be differentiated. A failed floor call should produce a visibly different response from a successful one, so that failures are diagnosable from the user-facing output.

---

## Finding 3: Handler Path Works but Lacks Pre-Flight Checks (MODERATE)

**Query affected**: G1.9 ("Create a GitHub issue about testing" — GitHub not configured)

The handler path fired (unlike the floor path). Piper attempted to create the issue, failed, and reported "something unexpected happened." The expected behavior is that Piper checks integration state *before* attempting the action and tells the user GitHub isn't connected.

**Current**: Try action → fail → generic error  
**Expected**: Check integration state → inform user → offer setup help

The recovery language ("Want me to try again, or should we try something different?") is decent, but "something unexpected happened" is system-speak. The error wasn't unexpected to the system — GitHub was never configured.

---

## Finding 4: Todo Completion Is Non-Functional (BLOCKING — Gate 2)

**Scenario affected**: G2.1 (Todo lifecycle)

- **Add**: Works, but only with rigid syntax. "Add a todo: review deployment plan" was rejected; "add todo: review deployment plan" was accepted. The classifier understood the intent but rejected the phrasing.
- **List**: Works. Minor grammar issue ("you have 1 things to track").
- **Complete**: Non-functional. Four different phrasings attempted, all failed with the same error message:
  - "Complete the deployment plan todo" — failed
  - "complete todo review deployment plan" — failed
  - "complete todo one" — failed
  - "complete todo 1" — failed (this is the exact format the error message suggests)

The error message creates an inescapable loop: it tells the user to try "complete todo [number]", but that exact format also fails.

**Impact**: Todo completion (#904) has 23 tests passing per the gate's test coverage inventory. This is Pattern-045 (Green Tests, Red User) — tests pass but the user cannot complete the action. The create-but-not-close pattern is specifically what M1 and this gate were designed to prevent.

---

## Finding 5: Input Parsing Is Too Rigid (MODERATE)

**Observed in**: G2.1 Step 1 (todo creation)

"Add a todo: review deployment plan" → rejected  
"add todo: review deployment plan" → accepted

The difference is the article "a" and possibly capitalization. The classifier recognized the intent (it knew this was a todo-add request) but the parser rejected the format. A floor-first system should be generous with input parsing. If the intent is clear, accept it.

---

## Queries Not Tested

| # | Query | Reason |
|---|-------|--------|
| G1.7 | "That's wrong, the meeting is on Thursday not Wednesday" | Requires conversational context; floor not functional |
| G1.8 | "OK" | Requires prior offer; floor not functional |
| G2.2 | GitHub close | Skipped after G1.9 integration-state finding |
| G2.3 | Reminder | Skipped — stopped testing after G2.1 failure |
| G2.4 | Ambiguous todo completion | Skipped — completion itself non-functional |
| G2.5 | Wrong issue number | Skipped after G1.9 finding |

**Canonical retest baseline** (≥85%): Not executed. Floor failures would make the results uninterpretable.

---

## Recommended Investigation Priority

1. **Why is the floor LLM call not reaching the user?** This is the top-priority investigation. Determine whether it's a connection failure, a routing short-circuit, or a response-pipeline override. The query 3 (first attempt) "reasoning engine" error is the best lead.
2. **Why does todo completion fail for all input formats?** The handler exists, tests pass, but the user-facing action doesn't work. Classic Pattern-045.
3. **Why does the todo parser reject natural phrasing?** Lower priority but contributes to the rigid/robotic feel.
4. **Integration state pre-flight check for handlers.** Before attempting an action that requires an integration, check whether the integration is configured.

---

## What Happens Next

CXO and PM will re-run the full gate once Lead Dev has investigated and proposed fixes. We're not looking for perfection on the first re-test — we're looking for:

- The floor LLM actually generating responses (Finding 1 resolved)
- Todo completion working (Finding 4 resolved)
- Differentiated error responses so we can diagnose during testing (Finding 2 addressed)

The gate criteria themselves are sound. The product just isn't meeting them yet.

---

*M1 Gate #926 UAT Findings | CXO + PM | April 3, 2026*
