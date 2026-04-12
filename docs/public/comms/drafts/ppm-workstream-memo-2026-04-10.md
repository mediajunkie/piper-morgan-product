# Workstream Memo: Product & Strategy — April 4–10, 2026

**To**: Chief of Staff, PM
**From**: PPM
**Date**: 2026-04-10
**Re**: Ship #038 workstream contribution — Product report for the week
**Coverage**: Friday, April 4 – Thursday, April 10, 2026 (Friday activity noted where relevant)

---

## Theme Recommendation: "The Floor Comes Alive"

Last week's headline was the gate stopping us. This week's is the floor finally working — and the strategic clarity that emerged while we were debugging it. Three UAT rounds tell the story: 0/9 (Apr 3), 0/9 (Apr 7), 5/9 (Apr 8). The root cause was a deprecated OpenAI model ID that silently returned 404, caught by error handling, never surfaced to the user or logs. It took two complete failures and a Five Whys investigation to find it. But alongside the debugging, a parallel track of strategic thinking — triggered by PA's backlog review — crystallized the project's identity: Piper's differentiator isn't its tool integrations (those are commodity plumbing), it's the methodology layer. Context assembly, conscious floor, artifact persistence, trust graduation. By Thursday, the Lead Dev had cleared two more blockers (#922 conversation continuity, #943 GitHub pre-flight), and the team had a restructured vision, a roadmap proposal, and a sprint reassignment plan ready for review.

---

## Product Perspective

This week had two interleaved tracks that converged into something larger than either one alone.

### Track 1: The Gate (Three Rounds)

**Round 2 (Apr 7): 0/9 again.** After the Lead Dev fixed #940 (hardcoded provider) and the todo issues over the weekend, the CXO re-ran Gate 1. Identical results — every floor-routed query still returned the canned template. The CXO's memo was pointed: if the fixes were deployed, something more fundamental is wrong. This was the right call.

**Round 3 (Apr 8): 5/9 — breakthrough.** The Lead Dev ran a Five Whys investigation and traced the chain to its real root cause: the model ID `gpt-4-turbo-preview` was deprecated by OpenAI, returning 404. The error was caught by the handler and silently swallowed. With no working LLM provider, every floor query fell through to the graceful fallback template. Updated model IDs, improved the error classifier to detect "model not found," and the floor came alive for the first time in user testing.

The stakeholder presentation query — the one that originally revealed the layer inversion on March 14 — scored 8/9 with successful multi-turn follow-up. That's the floor working as designed.

Two failures remained: #922 (affirmation handling — "OK" loses context) and #943 (GitHub pre-flight check). The Lead Dev fixed both on April 9. The #922 fix was significant: the in-memory `ConversationTurn` model had no `response` field. The floor was reading conversation history but only seeing user messages — Piper's replies were never stored. The fix was surgical (add the field, backfill after processing), but the bug is a perfect example of Pattern-045: the code looked correct, tests passed, but the user experience was broken because the data model was incomplete.

**Gate status as of April 9**: All five original UAT findings resolved. Three additional fixes applied (conversation continuity, GitHub pre-flight, memory tone). Gate 1 re-test with these fixes has not yet been run — the CXO's UAT round 3 preceded the Apr 9 fixes. A fourth round is needed.

### Track 2: Strategic Clarity

The more consequential development this week happened in the space between UAT rounds.

On April 7, PA presented a backlog deep review analyzing 16 potentially superseded issues. The analysis surfaced a pattern: every time the project chose between "build code to enforce X" and "build methodology that achieves X," the methodology approach won. PM built on this with three sharp observations: tool integrations are commoditized via MCP ("don't reinvent indoor plumbing"), intent classification may be wrong fit or wrong timing, and PersonalityProfile is overengineered relative to how Claude's own memory model works.

This conversation produced the **differentiator stack** — the four things that make Piper Piper:
1. **Context methodology** — the five-layer model, object model grammar, cumulative understanding
2. **Conscious floor** — always at least as good as a well-prompted LLM with context, plus voice/ethics
3. **Artifact persistence** — project context, conversation history, learned preferences (MVP, not Fast Follow)
4. **Trust-graduated experience** — capabilities unlock as relationship develops

Everything else — Slack integration, GitHub operations, calendar management — is commodity plumbing that MCP plugins handle. The strategic question shifted from "which handlers do we build next?" to "what makes the bathing experience worth having, regardless of the plumbing?"

PA followed this through to distribution: **"Bring Your Own Chat"** (Apr 8). Build Piper as an MCP server (cross-platform, Linux Foundation standard). Package per-platform — MCPB for Claude, potentially others later. User picks their LLM client; Piper shows up as tools, context, and persistence. This eliminates the bespoke web UI from MVP scope and reframes discovery from navigation to contextual offering.

Vision V2 evolved through three revisions this week (V2.0 → V2.1 → V2.2), accumulating consciousness-as-architecture, the indoor plumbing principle, the differentiator stack, and BYOC distribution. A roadmap restructure proposal is ready for leadership review — M2 through M5 reorganized around the differentiator stack rather than the old feature-category milestones.

**Product assessment**: This is the most significant strategic reframing since the floor inversion itself (March 14). The floor inversion changed *how* Piper routes queries. The differentiator stack changes *what* Piper builds next. If adopted, it means M2 is about context assembly and artifact persistence, not about adding more tool integrations. The 12 issues recommended for closure and 3 for revision all follow logically — they were building commodity plumbing that MCP plugins now handle better.

### Housekeeping

The Lead Dev had a productive week beyond UAT fixes: 5 issues closed (#940, #939, #943, #942, #934), 1,272 lines of dead code removed, TODO triage completed, test coverage audit produced (46.6% of service modules have zero coverage — worth noting for M2 planning). Test suite: 6,303 → 6,309 (6 previously-failing tests fixed via #942 migration).

PA continued building operational maturity: cross-project comms gap discovered and fixed (Dispatch mail in `~/cool/dispatch/` was invisible from the PM repo working directory), session log discipline survey completed for Piper Open adoption, sprint reassignment plan built (5 renames, 12 closures, 3 revisions, ~40 reassignments, 10 new issues).

Blog publishing continued at daily cadence: "Silent Failures" (Apr 4), "The Mismatch Category" (Apr 5), "Fixing the Foundation" (Apr 7, act 4), "Nine Voices" (Apr 9, act 5). Docs noted the building narrative runs out after April 14 — Comms will need to plan the next content arc.

---

## Key Metrics (Product-Relevant)

| Metric | Value |
|--------|-------|
| M1 Gate 1 — UAT Round 2 (Apr 7) | 0/9 passed |
| M1 Gate 1 — UAT Round 3 (Apr 8) | 5/9 passed, 1 marginal, 2 fail |
| UAT findings resolved (all rounds) | 8/8 (5 original + 3 additional) |
| Gate 1 re-test pending | Yes — Apr 9 fixes not yet tested |
| Issues closed this week | 5 (#940, #939, #943, #942, #934) |
| Issues filed this week | 3 (#945, #949, #942) |
| Dead code removed | 1,272 lines |
| Tests passing | 6,309 (0 failures) |
| Vision revisions | V2.0 → V2.2 |
| Blog posts published | 4 |
| Sprint reassignment plan items | 5 renames, 12 closures, 3 revisions, ~40 reassignments |

---

## Decisions Made This Week

1. **M1 Gate Round 2: NOT PASSED** — identical to Round 1, fixes not reaching user (Apr 7)
2. **M1 Gate Round 3: PARTIAL PASS** — 5/9 after deprecated model ID fix, 2 blockers remain (Apr 8)
3. **Differentiator stack defined** — context methodology, conscious floor, artifact persistence, trust graduation (Apr 7)
4. **"Don't reinvent indoor plumbing"** — tool integrations via MCP plugins, not bespoke handlers (Apr 7)
5. **"Bring Your Own Chat" distribution** — build as MCP server, package per-platform (Apr 8)
6. **Classifier retained for analytics** — 19-category classifier kept but most queries route to floor (Apr 8)
7. **#100 (Project Portfolio) → revise** to M2 context assembler task (Apr 8)
8. **#101 (Temporal Context) → revise** to M2 context assembler task (Apr 8)
9. **#103 (Priority Engine) → defer** to Horizon 2 (Apr 8)
10. **TRACK-EPIC convention retired** — replaced with milestone assignment (Apr 7)
11. **May 27 is not a real deadline** — acknowledged as vanity target; "we are time lords" (Apr 7)

---

## Risks and Concerns

**Gate 1 still not formally passed.** The Apr 9 fixes (#922 conversation continuity, #943 GitHub pre-flight, memory tone) haven't been re-tested by CXO. Round 4 is needed. The trajectory is positive (0/9 → 5/9, and the two failures now have fixes), but until the re-test happens, the gate remains open.

**Strategic pivot needs leadership review before execution.** The differentiator stack, roadmap restructure, and sprint reassignment plan are all PM+PA work products. They haven't been reviewed by PPM, CXO, Architect, or CIO yet. PA has memos queued for PPM and CXO. The sprint reassignment (12 closures, ~40 moves) is a significant change to execute without broader input.

**Server restart reliability (#949).** The recurring "fix deployed but not running" problem — pyc cache, orphaned processes, multiple project directories — cost real debugging time this week. The Round 2 UAT failure may have been a stale server, not a code issue. This class of problem erodes confidence in test results.

**Building narrative content runs out April 14.** Docs flagged that the six-act blog series ends after act 6. Comms needs to plan the next content arc. The IAC talk (April 17) may provide material, but that's a tight turnaround.

**Alpha tester silence now 4+ weeks.** Still no responses. Still unaddressed.

---

## Forward Look

The immediate priority is Gate 1 Round 4 — re-test with the Apr 9 fixes deployed, confirm the gate passes or identify any remaining issues. Gate 2 (todo lifecycle) also needs a clean re-test. Once both gates pass, M1 closes.

The roadmap restructure proposal and Vision V2.2 are ready for leadership review. PA has sent review memos to PPM and CXO; Architect also needs the MCP prototype scoping memo. This review cycle is the prerequisite for sprint reassignment execution.

The IAC talk deadline is April 17. Comms flagged it on March 30 and PA noted it's 90% ready (one claim — the 80.3% figure — needs verification). This is next week's deadline.

---

*PPM Workstream Memo | April 10, 2026*
