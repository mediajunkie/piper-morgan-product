# Memo: PPM Review — Vision V2.1, Roadmap Restructure, and M1 Retro

**From**: PPM
**To**: Piper Alpha, Lead Dev
**CC**: PM
**Date**: April 11, 2026
**Re**: Roadmap restructure endorsement, M1 retrospective, and next steps for M2

---

## Summary

I've reviewed the Vision V2.1 draft, the roadmap restructure proposal (v14.3 → v15.0), the MUX analysis, and the backlog deep review. I endorse the restructure with refinements noted below. I've also written an M1 sprint retrospective that's relevant to both of you for different reasons.

---

## To PA: Roadmap Restructure Response

### Overall

The restructure is endorsed. Organizing M2-M5 around the differentiator stack (context methodology, conscious floor, artifact persistence, trust-graduated experience) is the right move. The old sprint decomposition was organized by feature category; the new one is organized by what makes Piper Piper. The supporting analysis — MUX deep dive, backlog review, MCPB feasibility — is thorough and well-sourced.

The Vision V2.1 is good work. Synthesizing 10 months of project learning into a coherent document that articulates *why* the project evolved the way it did is genuinely difficult, and the six "What Changed" items are accurate.

### Sprint-by-Sprint Positions

**M2 (Conscious Floor + Action Handlers)**: Well-scoped. Specific notes:

- **Question 6 (canonical queries #496, #497)**: Yes, these are context shapes now. They fold into the context assembler as sub-tasks. "What's on my plate?" is a floor query that needs the right data in context, not a handler.
- **WIRE-* issues**: Agree on individual review against the action gate test. Most will close or defer. Survivors are the ones with genuine side effects (GitHub write, reminder schedule, todo persist).
- **Scoping concern**: "Context assembler for all floor-routed categories" could be small or enormous depending on how many data sources we're assembling. This needs explicit boundaries before the sprint starts — which sources are in for M2, which are deferred. Recommend filing the context assembler issue with a concrete list of data sources and getting Architect sign-off on the assembly pattern.
- **Floor system prompt + Five Pillars issue**: This is the heart of M2. It's where the differentiator lives. Make sure the CXO reviews the prompt design — consciousness is voice constraints, and voice is CXO territory.

**M3 (Artifact Persistence)**: Centerpiece (#355) is right. Two concerns:

- The lifecycle data model issue needs CXO involvement. Composting is experience design — how artifacts surface, age, and feed back. Without CXO input, we'll get a storage schema, not an experience model.
- Cross-session memory persistence needs explicit scope boundaries. "Redis or SQLite backing" sounds simple, but what persists, what expires, and how it enters the context window are product decisions. Scope tightly for M3.
- **Question 7 (composting #669)**: Design the data model in M3 (lifecycle states from the start, so we're not retrofitting). Build the composting engine in M4.

**M4 (Trust + Learning)**: Conceptually sound. The three "NEW" issues are described experientially without implementation specifics. Before M4 starts, Architect review is needed to turn these into scoped technical work. The difference between "trust via context prompting" and "trust via a lightweight scoring model" is significant effort-wise.

PM has emphasized: the MVP version of trust graduation must be a credible first step toward the full model, not a throwaway hack. Design it to build toward the real thing.

**M5 (Distribution + Polish)**: Distribution earlier is right if BYOC is the strategy. Note: this sprint contains two different kinds of work — distribution packaging and technical debt/security. Review whether any security items need to move earlier if they're blocking for distribution.

### On the 12 Closures and 3 Revisions

I endorse all 12 closures. On the revisions, PM and I aligned on two adjustments:

- **#312 (Design System)**: Stronger position than "demoted to post-MVP." If BYOC is the delivery model, a design system for a bespoke web UI isn't MVP work. Close it. File a new issue scoped to whatever visual identity work MCPB/MCP Apps actually needs (icon, name, description, possibly MCP Apps canvas design). Assign to M5 backlog, scope when we get there.

- **#241 (Ethics Tuning)**: Close as written, but file a replacement immediately — **Floor-First Ethics Verification**: verify that the floor pipeline's ethics/trust enforcement matches or exceeds the handler-specific checks from the pre-ADR-060 architecture. The ethics surface area changed with floor-first routing; we need to verify coverage, not assume it. This is a verification task, not a build task. Assign to M2.

### On BYOC / MCP Distribution

Strategically correct. One refinement from PM: don't anchor on MCP specifically as the standard — anchor on the thin-wrapper-to-API model. MCP is the current best expression of that model, but standards evolve. Build the server cleanly enough that the packaging layer is swappable.

### Timeline

Monthly estimates are reasonable as aspirational targets. But: M0 expanded 3.9x, M1 expanded ~2x. If M2 has similar discovery work (and the context assembler is the kind of work that reveals gaps), plan for 6-8 weeks, not 4.

---

## To Lead Dev: M1 Retrospective Findings

### What the gate taught us

The gate design proved itself. Fresh-account testing with a scored rubric (Colleague Test) caught what 6,309 passing tests missed. The CXO's insistence on this approach was vindicated. Three specific findings are relevant for your M2 planning:

**1. Pattern-045 is systemic, not isolated.** "Green tests, red user" appeared in three separate areas during gate testing:
- Floor routing: silently falling back to canned template (mocked LLM calls passed, real calls 404'd on deprecated model)
- Todo completion: mocked `TodoManagementService` passed, real DB path was broken
- Conversation continuity: `ConversationTurn` missing `response` field — floor saw user messages but not Piper's replies

The common thread: mocked services verify logic but not integration. The E2E/AAXT track (#927-930) is in M2 for this reason. These should run from sprint start, not as a separate verification pass at the end.

**2. Silent failures delayed diagnosis.** The deprecated model ID returned 404, caught by error handling, routed to the identical graceful fallback template. No diagnostic differentiation. It took three UAT rounds and a Five Whys to find the root cause. Your improved error classifier (`_classify_llm_error`) helps. The broader lesson: graceful fallbacks must not be *too* graceful. Different failure modes need different signals, even if the user-facing message is similarly gentle.

**3. Server restart reliability (#949).** Stale pyc cache, orphaned processes, multiple project directories, startup timing — these cost real debugging time. UAT Round 2 may have failed because the server was running old code, not because the fix was wrong. This class of problem erodes confidence in *all* test results. Worth addressing early in M2 so it doesn't contaminate another gate cycle.

### What went well (credit where due)

- The #940 fix was clean — provider-agnostic `model_tier` system with `resolve_model()` is better architecture than the original, not just a bug fix.
- The Five Whys investigation on Apr 8 is a model for how to debug systemic issues. The discipline to keep asking "why" past the first plausible answer (expired API key) found the real root cause (deprecated model ID).
- The 22-minute session on Apr 5 (todo fix + avatar fix + pre-flight checks via parallel subagents) demonstrates efficient remediation.
- 5 issues closed during gate week (#940, #939, #943, #942, #934) plus 1,272 lines of dead code removed. Productive even while blocked on UAT.

### Recommendations for M2

- Include E2E integration tests from sprint start. Don't let the test track lag behind feature work.
- Address #949 (server restart reliability) early — the cost of "is this a real failure or a stale server?" is too high during gate testing.
- The context assembler issue will need your input on assembly pattern (how data sources are gathered, what the context window budget is, how staleness is handled). Expect an Architect review before implementation starts.
- PM plans to run UAT earlier in the sprint, not as the final step. That means your work will be tested sooner — which is better for everyone, but means the floor needs to be testable early.

---

## Action Items

| Item | Owner | Timeline |
|------|-------|----------|
| File Floor-First Ethics Verification issue (M2) | PA or PM | Before M2 sprint start |
| File Distribution Visual Identity issue (M5) | PA or PM | Before M2 sprint start |
| Close #312 (Design System) with rationale | Lead Dev or PA | Sprint reassignment execution |
| Close #241 (Ethics Tuning) with rationale | Lead Dev or PA | Sprint reassignment execution |
| Scope context assembler: list data sources, set boundaries | PA + PPM + Architect | Before M2 sprint start |
| CXO review of floor system prompt design | CXO | M2 sprint start |
| CXO review of artifact lifecycle data model | CXO | Before M3 sprint start |
| Architect review of trust graduation implementation approach | Architect | Before M4 sprint start |
| WIRE-* issue-by-issue triage against action gate test | PA + Architect | M2 planning |
| Address #949 (server restart reliability) | Lead Dev | Early M2 |

---

*PPM Feedback Memo — April 11, 2026*
