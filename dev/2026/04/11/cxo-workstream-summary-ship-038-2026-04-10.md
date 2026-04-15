# CXO Workstream Summary — Ship #038

**Period**: April 3–9, 2026  
**Beat**: Product & Experience (Design)  
**Author**: CXO  
**Date**: April 10, 2026

---

## Theme Recommendation

**"Three Tries and a Floor"**

This was the week we tested the M1 gate three times — and on the third attempt, Piper spoke for the first time. Two complete failures (0/9 on Apr 3 and 7), a root cause investigation that traced through expired API keys to deprecated model IDs, and then a breakthrough: 5/9 passing, with the stakeholder presentation query — the one that started the entire floor inversion — scoring 8/9. The gate did what it was designed to do: it refused to let us ship a broken floor, and it validated the fix when it finally landed.

Alternative themes: "The Five Whys" (Lead Dev's root cause chain that found the deprecated model), "What Makes Piper Piper" (the strategic conversation that reframed the whole project around the differentiator stack).

---

## Week Summary

### M1 Gate UAT: Three Rounds (Apr 3, 7, 8)

The CXO's primary work this week. Three test rounds, each scored against the Colleague Test rubric on a fresh account.

**Round 1 (Apr 3)**: 0/7 passed (2 not tested). Every floor-routed query returned the same canned template. Root cause initially identified as expired API key. Five findings documented: floor not reaching user (blocking), canned template masking failures (blocking), no handler pre-flight checks (moderate), todo completion broken (blocking), input parsing too rigid (moderate).

**Round 2 (Apr 7)**: 0/9 passed. Identical results to round 1 despite API key fix. This proved the diagnosis was wrong — the expired key was real but not the root cause. CXO noted in the findings memo that if the same fix produces the same failure, the problem is more fundamental.

**Round 3 (Apr 8)**: 5/9 passed, 1 marginal, 2 failed, 1 not tested. Lead Dev's Five Whys investigation found the real root cause: `gpt-4-turbo-preview` model ID deprecated by OpenAI, returning 404. The floor LLM call existed in code but was never successfully executing because the model didn't exist anymore. Secondary cause: `_requires_canonical_handler` routing IDENTITY/greeting queries to canned templates before the floor check.

The turnaround in scores tells the story:

| Query | R1 (Apr 3) | R2 (Apr 7) | R3 (Apr 8) |
|-------|------------|------------|------------|
| "What can you help me with?" | 3 | 3 | **7** |
| "Thanks for the help" | 1 | 1 | **8** |
| "How trustworthy?" | 1 | 1 | **8** |
| "Stakeholder presentation" | 1 | 1 | **8** |

The trust query went from a 1/9 canned self-introduction to an 8/9 thoughtful answer about reasoning transparency and the limits of AI judgment. That's the floor doing what ADR-060 promised.

### Remaining Gate Issues and Fixes (Apr 9)

Lead Dev addressed all three remaining Gate 1 issues on Apr 9:

- **#922 (affirmation handling)**: Root cause was that `ConversationTurn` had no `response` field — the floor gathered conversation history but only saw user messages, never Piper's own replies. "OK" lost context because there was no context to lose. Fix: added response field and backfill after each processing step.
- **#943 (GitHub pre-flight)**: Three attempts to fix this across the week. Final approach: catch-block error detection instead of complex pre-flight checking. Handles expired/invalid tokens, not just missing ones.
- **Memory tone**: Added explicit prohibition against chatbot warmth phrases in floor system prompt. The "looking forward to getting to know you" line should finally be gone.

Tonight's partial retest (Apr 10) confirmed: GitHub pre-flight now scores 9/9 (perfect). Todo completion still broken (same failure as Apr 3). "OK" and memory tone not yet retested with the Apr 9 fixes deployed.

### The Strategic Pivot (Apr 7-8)

While the CXO was focused on UAT, a significant strategic conversation happened between PA and PM that reshapes the product direction. Key insights:

- The project evolved from "code frameworks that enforce methodology" to "operationalized methodology that the code serves"
- Tool integrations are commodity (MCP/plugins) — "don't reinvent indoor plumbing"
- The differentiator stack: context methodology + conscious floor + artifact persistence + trust-graduated experience
- "Bring Your Own Chat": build as MCP server, package per-platform, user picks their LLM client

CXO relevance: Vision V2.1 (then V2.2) includes "consciousness is architecture, not decoration" as a principle. PA sent a review request with five CXO questions — substantive work queued for after the gate closes. The MUX analysis ("what survives floor-first") is directly relevant to CXO: it distinguishes constitutional elements (grammar, Five Pillars, anti-flattening, composting, trust gradient) from scaffolding (warmth calibration values, personality service, consciousness rollout waves). The constitutional elements survive; the scaffolding may not be needed.

### Content Pipeline (Apr 3-9)

Four blog posts published this week: "Silent Failures" (Apr 4), "The Mismatch Category" (Apr 5), "Fixing the Foundation" (act 4, Apr 7/8), "Nine Voices" (act 5, Apr 9). Ship #037 "New Ground" published to Shipping News (Apr 8). The building narrative arc is now at act 5 of 6, with the series running out after Apr 14.

CXO relevance: the content pipeline is telling the M1 story in near-real-time. "Silent Failures" and "Fixing the Foundation" are about the UAT process this memo describes. The narrative and the engineering are running in parallel — the building-in-public principle operating at full velocity.

### Lead Dev Housekeeping (Apr 4-7)

Substantial housekeeping alongside the UAT fixes: 5 issues closed (#940, #939, #943, #942, #934), 1,272 lines of dead code removed, TODO triage completed, test coverage audit produced (46.6% of service modules have zero coverage). Migration for 4 missing orchestration tables brought 6 previously failing tests to green (6,303 → 6,309). #949 filed for server restart reliability (recurring "fix deployed but not running" problem).

---

## Design Decisions This Week

| Decision | Date | Impact |
|----------|------|--------|
| Gate 1 NOT PASSED (round 1) | Apr 3 | 5 findings documented, clear fix path |
| Gate 1 NOT PASSED (round 2) | Apr 7 | Proved first diagnosis wrong, forced deeper investigation |
| Gate 1 partially passed (round 3) | Apr 8 | 5/9 pass, floor confirmed working |
| Affirmation handling (#922) is a gate criterion | Apr 8 | PM to decide: block or carry to M2 |

---

## Forward Look

1. **M1 gate closure**: Todo completion is the last confirmed blocker for Gate 2. The #922 fix (Apr 9) and GitHub pre-flight fix (Apr 9) need verification with fresh deployment. Once todo completion works, we run the remaining Gate 2 scenarios and close the gate.

2. **PA Vision V2.1/V2.2 review**: Five CXO questions queued — consciousness as architecture, Colleague Test updates for floor-first, MCP Apps impact on artifact canvas, MUX lifecycle UI relevance, anti-flattening enforcement. This is a full-session piece of work.

3. **PA coherence check response**: Now informed by four rounds of UAT data. The boundary behavior we tested is exactly what the coherence check is designed to catch. Ready to write once the gate closes.

4. **Content narrative**: Building arc reaches act 6 (final) around Apr 14. The CXO UAT story — from "the gate that caught everything" through "the floor that finally spoke" — is itself publishable material.

---

*CXO Workstream Summary | Ship #038 | April 3–9, 2026*
