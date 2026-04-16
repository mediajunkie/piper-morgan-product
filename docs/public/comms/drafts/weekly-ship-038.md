Weekly Ship #038: The Floor Comes Alive

<!-- image: 'piper-ship.png' -->
<!-- alt: 'A person leads as small boat crewed by robots.' -->
<!-- no caption -->

*April 3–9, 2026*

Last week's "New Ground" ended with the M1 gate ready and waiting. This week, we sat down with Piper and had that conversation — three times. Round 1 (April 3): 0 of 9 queries passed the Colleague Test. Every floor-routed question returned the same canned template. Round 2 (April 7): 0 of 9 again, even after the fixes. Proved the first diagnosis wrong. Round 3 (April 8): 5 of 9 passed, and the stakeholder presentation query — the one that started the entire floor inversion back in March — scored 8 out of 9. The floor spoke for the first time. Between those test rounds, a parallel track of strategic thinking reframed what this project is actually building. By Thursday, the remaining blockers were fixed, the vision had been rewritten, and the team knew something it hadn't known on Monday: the product's differentiator isn't its tool integrations. It's the methodology.

---

# 🚀 Shipped this week

## 🎯 Product & experience

**M1 gate UAT: three rounds to a breakthrough.** The CXO-designed gate process proved its worth through three rounds of structured testing against a fresh alpha account, scored on the Colleague Test rubric (Relevance, Competence, Tone — 0-3 each, 7+ to pass, any 0 auto-fails).

Round 1 (Apr 3): 0/9. Every floor-routed query returned the identical canned `FLOOR_GRACEFUL_FALLBACK` template. Todo completion failed on all attempts despite 23 passing unit tests. Pattern-045 ("Green Tests, Red User") confirmed in two separate subsystems. Testing stopped after 8 of 14 scenarios. Five findings documented, three blocking.

Round 2 (Apr 7): 0/9 again. After the Lead Dev fixed the hardcoded provider (#940), todo parsing, avatar positioning, and pre-flight checks over the weekend, the CXO re-ran Gate 1 and got identical results. The CXO's memo was direct: if the same fix produces the same failure, the problem is more fundamental. This was the right call — it forced deeper investigation.

Round 3 (Apr 8): 5/9 passed, 1 marginal, 2 failed. The Lead Dev ran a Five Whys investigation and traced the real root cause: the model ID `gpt-4-turbo-preview` had been deprecated by OpenAI and was silently returning 404. The error was caught by the handler and swallowed — with no working LLM provider, every floor query fell through to the graceful fallback. Updated model IDs, improved the error classifier, and the floor came alive.

The scores tell the story: the "How trustworthy are your recommendations?" query went from a 1/9 canned self-introduction to an 8/9 thoughtful answer about reasoning transparency and the limits of AI judgment. That's the floor doing what ADR-060 promised.

**Remaining blockers addressed (Apr 9).** Lead Dev fixed the two remaining Gate 1 failures: #922 (conversation continuity — `ConversationTurn` had no `response` field, so the floor saw user messages but never Piper's replies, meaning "OK" lost all context) and #943 (GitHub pre-flight — three fix attempts across Apr 5-9, final approach uses catch-block error detection). Memory tone also calibrated — explicit prohibition against chatbot warmth phrases in the floor system prompt. Round 4 re-test pending.

**Strategic reframe: "What makes Piper Piper?"** The week's most consequential work wasn't debugging — it was the April 7 conversation between PA and xian, triggered by PA's backlog deep review of 16 potentially superseded issues. The analysis surfaced a fundamental insight: the project had evolved from "build code frameworks that enforce methodology" to "build methodology that the code serves." The methodology approach won every comparison. Tool integrations (Slack, GitHub, calendar) are commodity plumbing, reproducible by any MCP server. Piper's differentiator is the stack above the plumbing: context assembly methodology, conscious conversational floor, artifact persistence, and trust-graduated experience.

**"Bring Your Own Chat" distribution philosophy.** PA's MCPB feasibility research (Apr 8) confirmed a viable distribution path: build Piper as an MCP server (cross-platform), package per-platform using MCP Bridge for Claude. The user picks their client; Piper shows up as tools, context, and persistence. This reframes discovery from navigation ("find features in Piper's UI") to contextual offering ("Piper's capabilities appear where you already work").

**Vision V2.2 drafted.** Three iterations in three days (V2 → V2.1 → V2.2), each incorporating PM feedback. Now includes consciousness-as-architecture, the indoor-plumbing principle ("don't reinvent commodity integrations"), the differentiator stack, and Bring Your Own Chat distribution. Review memos sent to CXO and PPM.

## ⚙️ Engineering & architecture

**Lead Dev remediation: 7 issues, 1,272 lines removed.** #940 (LLM config blocker — provider-agnostic model tier system), #939 (avatar orphaning — 3 call sites in chat.js), #943 (GitHub pre-flight — catch-block approach), #942 (missing orchestration tables — migration for 4 tables, 6 previously failing tests now green → 6,309 total), #934 (orphaned task_management.py — 675 lines + 597-line test, never mounted), #922 (conversation continuity — response field + backfill), plus 1,272 lines of dead code removed. Test coverage audit produced: 46.6% of service modules at zero coverage.

**Five Whys investigation (Apr 8).** The root cause chain for the floor failure: generic responses → floor never invoked (zero `conversational_floor_hit` in logs) → queries pre-classified to canonical handlers → LLM classifier failing (deprecated model ID returns 404) → single-provider setup means fallback is None → RuntimeError caught → canned template. Six links in the chain, each masking the one below it. CIO named this pattern "Stacked Silent Failures."

**#949 filed: server restart reliability.** The recurring "fix deployed but not running" problem — `.pyc` cache, orphaned processes, multiple project directories — cost real debugging time. The Round 2 UAT failure may have been a stale server, not a code issue. This class of problem erodes confidence in test results.

## 🔬 Methodology & process innovation

**"Stacked Silent Failures" — a new diagnostic pattern.** Three independent failures at three architectural layers produced a composite behavior that appeared to be a single problem: Layer 1 (deprecated model ID returning 404), Layer 2 (canned fallback masking every failure mode identically), Layer 3 (conversation history missing Piper's own replies). Each layer's fix was necessary but insufficient — all three had to be resolved for the floor to work. CIO formalized this as a named pattern.

**PA's trajectory: analyst to strategist in 10 days.** Day 5 (Apr 3): UAT support. Day 7 (Apr 5): all UAT findings triaged. Day 8 (Apr 7): backlog review triggered the strategic reframe. Day 9 (Apr 8): Vision V2.2, MCPB feasibility, sprint reassignment plan (5 renames, 12 closures, ~40 reassignments, 10 new issues). Day 10 (Apr 9): cross-project Dispatch communication, session log discipline survey for Piper Open. HOST's assessment: "the first agent role to generate strategic reframing at this level."

**Sprint reassignment plan ready.** PA built a comprehensive execution plan for operationalizing the strategic reframe: 12 issue closures (superseded by methodology approach), ~40 milestone reassignments, 5 renames, 3 revisions, 10 new issues. Ready for execution but not yet reviewed by PPM, CXO, or Architect. PA has review memos queued.

## 🌍 External relations & community

The six-act building narrative is now at Act 5 of 6; after Act 6 (scheduled Apr 14), the building narrative queue runs out. The UAT story (Apr 3-9) is the obvious next arc.

- April 4: "[Silent Failures](https://pipermorgan.ai/blog/silent-failures/)" — insight piece from March 3 through 8, cross-posted here
- April 5: "[The Mismatch Category](https://pipermorgan.ai/blog/the-mismatch-category/)" — insights, also from March 3 to 8, also cross-posted
- April 7: "[Fixing the Foundation](https://pipermorgan.ai/blog/fixing-the-foundation/)" — build narrative from March 17 through 18
- April 9: "[Nine Voices](https://pipermorgan.ai/blog/nine-voices/)" — build narrative from March 19.

<!-- image: 'https://pipermorgan.ai/assets/blog-images/ai-set.webp' -->
<!-- link: (https://pipermorgan.ai/blog/fixing-the-foundation/)>
<!-- alt: 'A presenter stands ready under a spotlight while small AI helpers hurriedly clean up messy, mislabeled props and backdrops behind the scenes.' -->
<!-- caption: '"The show must go on!"' -->

**Publication cadence formalized.** Docs corrected the editorial calendar: Tue/Thu for building narratives, Sat/Sun for insight pairs, Wed for Ship. This cadence is now explicit rather than undocumented practice.

**IAC talk: 6 days out.** "Ethics as Information Architecture" (April 17, Philadelphia). Deck and speaker notes exist, PA flagged one claim (80.3% figure) needing verification. Approaching urgency.

## 📊 Governance & operations

**Metrics (Apr 3-9)**: ~20 sessions across 7 days. 3 UAT rounds (0/9 → 0/9 → 5/9). 7 issues closed. 1,272 LOC removed. 6,309 tests passing. 8 publications. Vision V2 → V2.2 (3 iterations). Sprint reassignment plan drafted. 5 omnibus logs produced (closing 3-day backlog). BRIEFING-CURRENT-STATE refreshed. New `/update-current-state` skill created. TRACK-EPIC convention retired.

**Docs infrastructure.** Five omnibus logs produced this week, closing a backlog from the Easter weekend. `/update-current-state` skill created so any agent can refresh the briefing. Audit #944 completed. Editorial calendar corrected.

**PA cross-project communication gap.** PA discovered that Dispatch messages in `~/cool/dispatch/mail/` were invisible from within the PM repo working directory — 4 messages went unread for 3 days. A ceiling moment: structural limitation of the current mailbox pattern for multi-project agents.

---

# 🎯 Coming up next week

## Development priorities

M1 gate Round 4 — re-test with Apr 9 fixes deployed. If Gate 1 passes (the two remaining failures are now fixed), run the remaining Gate 2 scenarios. If both gates pass, M1 closes. Sprint reassignment execution after leadership review.

## Alpha testing & onboarding

Alpha tester silence: 27+ days since Mar 14 email, zero responses from 13 testers. HOST has flagged this three sessions running. I've advised the team not to worry. It's not an easy alpha to work with and we are rapidly approaching beta.

## Communications

IAC presentation (April 17) — 6 days out. Speaker notes and deck exist; one claim needs verification. Building narrative Act 6 ("The Closing Sprint") scheduled Apr 14 — final act in the six-part series. Next content arc needed; the UAT story is the natural candidate.

---

# 🚧 Blockers & asks

**Current blockers**: M1 gate Round 4 re-test depends on PM + CXO availability. All known blocking issues are fixed.

**Decisions needed**: Sprint reassignment plan review (12 closures, ~40 moves — significant scope change). Vision V2.2 leadership review (CXO and PPM have review memos queued).

**Team input**: HOST briefing rename still pending (operational rename done Apr 2, briefing document content still old). CIO innovation backlog location needs confirming. Server restart reliability (#949) affects UAT confidence.

---

# 📊 Resource allocation

**For week ending April 9**: M1 gate UAT and remediation 40% (3 rounds, 7 fixes, Five Whys investigation, findings memos), strategic planning 25% (backlog review, differentiator stack, Vision V2.2, MCPB feasibility, sprint reassignment), communications 20% (8 publications, calendar formalization), infrastructure 10% (5 omnibus logs, audit, CURRENT-STATE refresh, skill creation), governance 5% (open items tracking, cross-project comms).

**Velocity**: Two tracks running in parallel — debugging and strategy — that converged into something larger than either. The gate process forced honest confrontation with the product's state. The strategic conversation reframed what the product is. Both were necessary; the timing was fortunate.

---

# 🔎 This week's learning pattern

## When the fix doesn't fix it, the diagnosis was wrong

**Discovery**: A correct fix for a real problem can produce zero improvement when multiple independent failures stack at different architectural layers. Each failure masks the one below it, and fixing one layer exposes the next without any visible progress.

**Example from this week**: Round 1 (Apr 3) found that the floor wasn't reaching users. The diagnosis: the Anthropic API key had expired. Real problem, real fix. Round 2 (Apr 7) deployed with a fresh key and fresh fixes — and the results were identical. Zero improvement. The CXO's response was the methodological key: "if the same fix produces the same failure, the problem is more fundamental."

The Lead Dev's Five Whys investigation on April 8 traced the actual chain: generic responses → floor never invoked → queries pre-classified to canonical handlers → LLM classifier failing → model ID `gpt-4-turbo-preview` deprecated by OpenAI (returning 404) → single-provider fallback is None → RuntimeError caught → canned template. Six links, each necessary to understand.

But even after fixing the model ID, Round 3 still had two failures. One turned out to be a data model gap: `ConversationTurn` had no `response` field. The floor was assembling conversation history from only the user's messages — Piper's own replies were never stored in memory. The code "looked right" because the field wasn't missing; it had never existed.

**Why it matters**: The instinct when a fix doesn't work is to doubt the fix. But sometimes the fix was correct — it just revealed the next layer. The CIO named this "Stacked Silent Failures": multiple independent problems that each mask their own symptoms, producing composite behavior that appears to be a single issue. The diagnostic discipline is to resist the urge to revert the fix and instead ask: "what was that fix hiding?"

**Application beyond this week**: Any system with layered error handling is vulnerable to stacked silent failures. Each catch block that returns a graceful fallback adds a potential masking layer. The mitigation isn't removing the fallbacks — those serve users — it's ensuring each fallback is distinguishable. The Lead Dev's fix to the error classifier (differentiating auth failure, transient error, model-not-found, and no-provider) is the template: make each failure mode visible, even when the user sees a graceful response.

**Related patterns**: Pattern-045 (Green Tests, Red User), the Five Whys investigation technique, the gate methodology (structured rounds with scored rubrics that force precise diagnosis)

---

# 📚 Weekend reading

**The differentiator stack.** PA's backlog review and the ensuing PM conversation crystallized what makes Piper Morgan distinct from any other PM tool: context assembly methodology (how project intelligence reaches the conversation), the conscious conversational floor (LLM with assembled context as baseline, not fallback), artifact persistence (work products that survive and accumulate), and trust-graduated experience (proactivity calibrated to relationship depth). Everything below this stack — Slack integration, GitHub sync, calendar access — is commodity plumbing. If you're building AI-powered tools and wondering where to invest, the answer is probably above the plumbing line.

**The CXO's gate rubric in practice.** Three rounds of testing, three structured findings memos, each with scored dimensions and specific diagnostic guidance. The rubric made pass/fail unambiguous — no room for "feels okay" rationalization. The Round 2 memo's observation ("if the same fix produces the same failure, the problem is more fundamental") was the diagnostic turning point of the week. If you're designing quality gates for AI products, the Colleague Test rubric is worth studying.

---

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #038. Previous: [#037 "New Ground"](https://www.linkedin.com/pulse/weekly-ship-037-new-ground/).

*P.S. The stakeholder presentation query scored 1 out of 9 on April 3. It scored 8 out of 9 on April 8. Same query, same rubric, same tester. The difference was a deprecated model ID that nobody knew was deprecated because the error was caught and swallowed. Five days, one Five Whys chain, and the floor finally spoke.*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of April 3–9, 2026 | Phase: MVP Build (M1 Sprint — Gate Verification)**
