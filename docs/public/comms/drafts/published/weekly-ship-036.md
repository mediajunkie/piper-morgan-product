Weekly Ship #036: Approaching the Gate

*March 20–26, 2026*

Last week's "Pour the Floor" established the principle that Piper should always be at least as good as a well-prompted LLM with context. This week, that principle and everything else we've been building converged toward M1's finish line. Three engineering tiers cleared. The Product entity model resolved through a 4-role coordination chain in 90 minutes. PDR-004 codified ten days of product thinking into four experience principles. The M1 gate was filed, reviewed by CXO and PPM independently, and Gates 3-4 verified. By Thursday, all that remained was the gate itself — 14 manual test scenarios waiting for the PM to sit down with Piper and have a conversation.

---

# 🚀 Shipped this week

## 🎯 Product & experience

**Product entity model (#717) resolved.** Five design decisions landed through a 4-role coordination chain in 90 minutes with zero PM mediation. The most interesting: CXO and PPM disagreed on navigation (emergence vs. orchestration mental models) and converged on a both-models approach — Product as a visible grouping header within Projects, clickable to detail view, neither model privileged. The Architect validated the schema, specified cascade behavior, and documented the PDR-003 divergence path.

**PDR-004 (Experience Philosophy) ratified.** Four principles from ten days of product decisions: presence over performance, specificity as care, honest boundaries, growth through use.

**M1 gate shaped and partially verified.** CXO and PPM independently refined the gate criteria: fresh-account testing, Colleague Test rubric (7+ threshold), multi-turn integration, capability registry check. Gates 3-4 verified — 6,310 tests, zero failures. Gates 1-2 await PM user acceptance testing.

**Piper Alpha briefing assembled.** Five roles contributed: CIO structure, CXO voice guidance ("express investment through specificity, not declared feelings"), PPM Tier 1 tasks, Architect constraints, HOSR session protocols. Launch-ready pending PM review.

## ⚙️ Engineering & architecture

**M1 Tier 3 completed in one session.** Four issues closed March 22: #902 (GitHub close/reopen — 75% pattern, MCP adapter missing), #903 (reminders across 5 integration points), #904 (todo completion verified and formally closed), #883 (lazy workflow — pre-creation was 100% wasted).

**#706 closed.** Objects catalog, views catalog, MVP prioritization matrix. PM-led discovery, not code.

**120+ new tests.** Suite at 6,310 passing, zero failures. First E2E smoke test through `/api/v1/intent` (#927).

## 🔬 Methodology & process innovation

**Agent 360 action items completed.** All three from HOSR's survey executed same-evening March 21: CXO formalized the Colleague Test (rubric with 5 worked examples), PPM documented Roundtable Synthesis (methodology-22 with template and 3 case studies), exec delivered CIO reassurance memo with 7 evidence threads.

**Cross-Pollination Hub operational.** First brief published March 21 — six insights across Klatch and Piper Morgan, including the five-layer context model directly relevant to session-start overhead.

**Ship process guide completed.** v1.1 with exec feedback applied same day. Ship #036 is the validation pilot.

## 🌍 External relations & community

**Five publications in seven days.** Four blog posts plus Ship #035 on LinkedIn.

**13 content pieces drafted in one session** (March 26). Acts 3-6 of the building narrative, four March insight pieces, three February gap-closing insights. February content gap declared CLOSED. Pipeline has shifted from "mine more content" to "sequence and publish thoughtfully."

**Editorial integrity.** PM rejected a "Convergent Discovery" insight — the cross-project parallels were deliberate transfers, not independent convergence. Dropped, not reframed.

## 📊 Governance & operations

**Metrics (Mar 20–26)**: ~30 sessions across 7 days. ~12 issues closed. 120+ new tests (suite at 6,310). M1 at ~95%. PA briefing v0.2 ready. 5 publications. 15 content pieces drafted.

**Service disruption.** Anthropic issues on March 26 interrupted the Docs session, stranding commits until March 28. The Comms session completed before the disruption. Combined with a day off March 25, the window had reduced capacity — but the engineering work was done.

**Documentation infrastructure.** 106 files committed. Weekly audit corrected 5 stale indexes. TODO triage filed 5 issues (#932-936).

---

# 🎯 Coming up next week

## Development priorities

M1 gate execution: PM user acceptance testing (14 scenarios across Gates 1-2). Canonical retest (target ≥85% on implemented queries). If gate passes, M1 closes and M2 planning begins.

## Alpha testing & onboarding

Alpha email responses still pending (sent Mar 14, 13 recipients). Ted's Security.md and Methodology.md reviews pending. Piper Alpha launch pending PM review of briefing v0.2.

## Communications

IAC presentation refinement (April 17, approaching). Next building narrative publication: Are We Doing It Backwards? Content pipeline deep — sequencing is the constraint.

---

# 🚧 Blockers & asks

**Current blockers**: M1 gate closure depends on PM manual testing. This is the right dependency — the PM should verify the product feels right.

**Decisions needed**: PA launch timing. M2 scope planning (expansion risk lessons from M0 apply).

**Team input**: CXO briefing refresh still carried (stale since Agent 360 flagged it Mar 19).

---

# 📊 Resource allocation

**For week ending March 26**: Core development 35% (Tier 3 closure, gate verification, #706/#717 resolution), governance and coordination 30% (Agent 360 execution, PA assembly, gate review, process guide), communications 25% (5 publications, 13 drafts, February gap closure), methodology 10% (cross-pollination hub, Colleague Test, Roundtable Synthesis docs).

**Velocity**: High but sustainable. The sprint is in its verification phase — slower, less dramatic than the bug-fix weeks, but this is where quality gets confirmed.

---

# 🔎 This week's learning pattern

## The asynchronous decision chain — coordination without synchronization

**Discovery**: Multi-role product decisions can resolve through asynchronous memo exchange faster and with better outcomes than synchronous discussion, when roles have clear responsibilities and structured handoff conventions.

**Example from this week**: The Product entity model (#717) needed five design decisions, including a navigation question where CXO and PPM held different views. The Lead Dev sent validation requests to the Architect and a navigation gut-check to CXO. The Architect approved the schema and specified cascade behavior. CXO recommended Option B (section within Projects), disagreeing with PPM's preference for first-class navigation. PPM revised to accommodate both mental models. CXO confirmed the final design detail (visible header, section-title typography). The Lead Dev consolidated everything into a design doc and closed the issue. Four roles, five memos, two productive disagreements resolved, 90 minutes — and the PM didn't mediate a single step.

**Why it matters**: The conventional assumption is that disagreements require synchronous discussion. This chain showed that structured memos with clear rationale allow each role to engage with the substance of the disagreement rather than the social dynamics. CXO cited PDR-003's own language to ground the position. PPM responded to the substance, not the person. The result was a design neither would have reached alone.

**Application beyond this week**: Any team with defined roles and a memo/document culture can use this pattern. The prerequisites: each role must know its decision authority, memos must include rationale (not just positions), and someone must synthesize and close. The synthesizer role is key — without it, memos accumulate without resolution.

**Related patterns**: Pattern-059 (Leadership Caucus), Methodology-22 (Roundtable Synthesis — the synchronous variant)

---

# 📚 Weekend reading

**Cross-Pollination Hub** (designinproduct.com/internal/): Now publishing daily intelligence briefs between Klatch and Piper Morgan. The March 21 brief surfaced Anthropic ecosystem releases and Klatch's five-layer context model — both directly relevant to Piper's architecture.

**PDR-004: Experience Philosophy**: "Presence over performance, specificity as care, honest boundaries, growth through use." Four principles governing how Piper interacts — worth reading if you're designing AI assistant experiences.

---

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #036. Previous: [#035 "Pour the Floor"](https://www.linkedin.com/pulse/weekly-ship-035-pour-the-floor/).

*P.S. A four-role product decision chain resolved two disagreements in 90 minutes through memos alone. No meeting, no PM mediation, no compromise — synthesis. Sometimes the best coordination is the kind where nobody's in the same room.*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of March 20–26, 2026 | Phase: MVP Build (M1 Sprint — Gate Verification)**
