# Weekly Ship #035: Pour the Floor

*March 13–19, 2026*

Last week's "Measure First, Then Act" ended with M1's diagnostic phase revealing that most canonical test failures were wiring bugs, not AI problems. This week we discovered something worse: Piper Morgan — with its 19 intent categories, 62 patterns, trust gradients, and guided workflows — was less useful than a generic ChatGPT wrapper for any question that didn't match a pre-built handler. A PM asked a reasonable question about managing agents. Piper replied: "I don't have that capability yet! Try asking 'What can you do?'" The team asked: are we doing it backwards? The answer was yes. We'd built the flying buttresses without pouring the floor.

---

## 🚀 Shipped this week

### 🎯 Product & experience

**Floor-first routing architecture (ADR-060).** Four leadership roles independently diagnosed the same problem in under two hours: the LLM was being used to classify messages but never to respond to them. The principle that emerged — "Piper is always at least as good as a well-prompted LLM with the user's context; structured handlers make it better, not different" — is now formalized as an ADR. The LLM conversational floor is the default response path. Structured handlers are enhancements for actions the LLM can't perform (API calls, state mutations, guided workflows). The user never hits a dead end.

**Workflow hijack bugs resolved.** The onboarding and standup workflows that trapped user sessions (#888, #889) were fixed on Friday with offer-first activation, escape commands, and timeout auto-suspend. The governing principle: "the session belongs to the user, not the workflow." By the following Thursday, the onboarding workflow was removed entirely (ADR-059) — Gall's Law applied. Rather than patching a broken system, simplify to a working one.

**Workflow dispatcher rebuilt (ADR-059).** Three independent offer/acceptance systems were racing for control of user affirmations, causing #922 (conversation continuity bug: "Sure" → dead end). The Lead Dev traced the root cause, drafted the ADR, received Architect approval, and completed implementation in a single morning. A registry-based dispatcher replaced the competing systems.

**Nine product decisions shipped.** From offer-first onboarding and the session-belongs-to-user principle (Friday) through the floor-first consensus and "never say I can't" voice rule (Saturday-Monday) to onboarding removal (Thursday). The spec pipeline operated at peak velocity twice: hijack design sprint on Friday (question to implementation in 8 hours) and floor roundtable on Saturday (question to unanimous consensus in under 3 hours).

### ⚙️ Engineering & architecture

**Two ADRs created, two annotated.** ADR-060 (Floor-First Routing) and ADR-059 (Workflow Dispatcher) formalize the week's architectural shifts. ADR-039 annotated as routing-superseded; ADR-049 annotated as pending review.

**Action Registry.** 34 intent-action pairs cataloged with disposition-based routing — the systemic fix for classification extending independently of handling.

**200+ new tests.** Suite at ~6,190 passing (net +143, plus 228 skipped for disabled onboarding). E2E infrastructure created: 16 tests across health, auth, query, and project CRUD.

### 🔬 Methodology & process innovation

**Agent 360: first organization-wide feedback.** HOSR's questionnaire achieved 100% response rate. Strongest signal: every respondent cited briefing staleness. Six of nine said handoff memos were more useful than briefings for orientation. Root cause — time-sensitive info hardcoded instead of deferred to CURRENT-STATE — was fixed in a Tuesday audit repairing 8 of 12 briefing files.

**CIO methodology audit completed.** Six-week review assessed methodology as strongest since project founding. Two policy changes approved: trigger-based audit cadence (replacing calendar-based) and CIO self-approval for Emerging patterns (fixing 25-day pipeline latency).

**Pattern-063 (Extension Without Integration).** Six bugs from the same structural cause: one layer extended without verifying downstream contracts, stubs absorbing the gap. A sub-pattern of Assembly Assumption (Pattern-062), now documented at a fourth scale.

**Mailbox v3 shipped.** Canonical directory, delivery log, per-role manifests, and a three-phase delivery skill. First run caught a routing error on day one.

### 🌍 External relations & community

**Five publications in one week** — the highest output since the daily publishing era ended in November. Four blog posts plus Ship #034 on LinkedIn. Content pipeline remains well-stocked.

**IAC presentation drafted.** 16-slide deck with speaker notes for "Ethics as Information Architecture" (April 17, Philadelphia).

**Blog pipeline complete.** 269 posts with image metadata (100%). Medium repatriation finished. Publish-to-blog skill battle-tested and updated to v0.2.

### 📊 Governance & operations

**Metrics (Mar 13–19)**: ~45 sessions across 7 days. ~25 issues closed, ~20 created. 200+ new tests (suite at ~6,190). 2 ADRs created, 2 annotated. 5 publications. Agent 360: 9/9 responses.

**Three chat handoffs executed.** CXO, PPM, and Architect predecessor chats retired at upload limits after ~3 months each. Handoff pattern now proven across six roles.

**Living open items tracker created.** Persistent cross-session tracking for the Chief of Staff, replacing reconstruct-from-logs. Fourteen-day disposition policy forces conscious decisions on carried items.

---

## 🎯 Coming up next week

### Development priorities

Floor migration Phases 2-3 (remaining intent categories). Post-migration canonical retest to replace projections with measurement. #922 conversation continuity fix via the new workflow dispatcher.

### Alpha testing & onboarding

Monitor alpha email responses (13 recipients, no replies yet). Dominique follow-up on v0.8.6 and Traefik. Ted's Security.md and Methodology.md reviews pending.

### Communications

Weekend publications scheduled: Discovery is the Bottleneck (Sat) and Wiring vs. Wizardry (Sun). IAC slide refinement continues.

---

## 🚧 Blockers & asks

**Current blockers**: None blocking M1 execution. Floor migration and canonical retest are the critical path.

**Decisions needed**: M1 gate criteria — should be data-driven (canonical retest results) not calendar-driven.

**Team input**: Colleague Test formalization (CXO). Roundtable Synthesis documentation (PPM). Both surfaced in Agent 360 as undocumented core processes.

---

## 📊 Resource allocation

**For week ending March 19**: Core development 40% (hijack fixes, floor implementation, E2E, dispatcher rebuild), governance and planning 25% (Agent 360, methodology audit, workstream reviews), methodology 20% (Mailbox v3, editorial calendar, briefing repairs), communications 15% (5 publications, IAC deck, pipeline inventory).

**Velocity**: Peak — highest sustained output in project history. PPM and Architect both note this pace isn't sustainable and shouldn't be expected to repeat. The remaining M1 work (wiring verification, floor quality, canonical retest) is slower and less dramatic than the bug-fix sprint.

---

## 🔎 This week's learning pattern

### The roundtable format — independent convergence over sequential review

**Discovery**: When multiple leadership roles review the same question independently (no anchoring) and then synthesize, the result is both faster and higher-quality than sequential review chains.

**Example from this week**: PM asked "Are we doing it backwards?" on Saturday. Four roles wrote independent memos without seeing each other's work. All four arrived at the same diagnosis and the same fix — but each found a different facet: PPM identified layer inversion, CXO framed it as bouncer-vs-concierge, the Architect spotted technical waste ("we spent LLM tokens deciding we can't help, then don't use the LLM to actually help"), and the CIO identified the strategic risk. PPM synthesized all four into binding direction. The ethics constraint, the no-actions boundary, and the voice guidance all emerged from the synthesis — none were in any single memo.

**Why it matters**: Sequential review chains anchor on the first response. The parallel-then-synthesize approach eliminates anchoring bias and produces complementary perspectives. It also takes less wall-clock time — four parallel responses in two hours vs. four sequential reviews over two days.

**Application beyond this week**: Pose the same question to each reviewer independently, collect responses without sharing, then have one role synthesize — finding convergence, identifying productive divergence, and flagging what no single memo covered. Works with 3-6 reviewers.

**Related patterns**: Pattern-059 (Leadership Caucus), Pattern-062 (Assembly Assumption — the roundtable diagnosed this at the product level)

---

## 📚 Weekend reading

**Cross-Pollination Hub** (designinproduct.com/internal/): Our new internal knowledge-sharing surface between sibling projects. Daily intelligence briefs surface insights from Klatch and Piper Morgan that matter to each other. Six cross-relevant insights in the first brief.

**"Extension Without Integration"**: The systemic pattern behind six bugs this week. If you're building features in parallel slices and wondering why composition keeps breaking, this is why — and the Action Registry is one structural fix.

---

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #035. Previous: [#034 "Measure First, Then Act"](https://www.linkedin.com/pulse/weekly-ship-034-measure-first-then-act/).

*P.S. We built a sophisticated PM assistant with 62 patterns and 19 intent categories. Then a $0 ChatGPT wrapper would have done better at answering a basic PM question. The fix took one afternoon. The humility to ask the question took ten months.*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of March 13–19, 2026 | Phase: MVP Build (M1 Sprint)**
