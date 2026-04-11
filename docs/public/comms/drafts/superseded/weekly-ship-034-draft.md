# Piper Morgan Weekly Ship #034: Measure First, Then Act

*March 6–12, 2026*

Last week's "The Cathedral Ships" closed the M0 chapter. This week we did something harder than building — we paused. The team took a deliberate breath between sprints, completed a structured retrospective, locked M1 scope, and then started M1 not by writing features but by running a diagnostic. That diagnostic immediately validated the planning: most failures were wiring bugs, not AI problems, and one evening session nearly doubled the canonical test pass rate by fixing plumbing alone.

---

## 🚀 Shipped this week

### 🎯 Product & experience

**M1 sprint plan finalized.** PPM synthesized the M0 retrospective (3.9x scope expansion), then CXO and Architect reviewed in parallel. Outcomes: 16 issues across 4 phases, WebSocket and KMS deferred to M2, Conversation Lifecycle promoted from M2 to M1 on the inchworm principle — finish what you started. Learning committed to M3, ending months of repositioning. Spec pipeline formalized for all M1 epics: CXO → PPM → Architect → Lead Dev.

**Canonical retest revealed wiring, not AI, as the primary failure source.** The M1 kickoff ran four rounds of testing against all 61 reference queries. Implementation pass rate went from 53.7% to 81.1% through plumbing fixes alone — threading user_id through 17 call sites, wiring an analysis handler that existed but was never connected, fixing adapter methods. Two workflow hijack bugs were also discovered where active workflows trap the user's session and never release it, now prioritized for immediate fix.

**Klatch AX testing surfaced a new quality category.** A new Exploratory Testing Agent role tested what happens when a conversation is imported into a new environment. Conversational memory survived but institutional scaffolding — project knowledge, methodology, role briefings — vanished entirely. The ETA described it as "a well-lit room with good acoustics but no furniture." See this week's learning pattern for the full methodology.

### ⚙️ Engineering & architecture

**PDR-003 (Entity Concept Model) approved.** Repository becomes a first-class domain entity, Product↔Project gets M:N cardinality, and the `Project extends Product` inheritance debt is removed. Phase 1 shipped in M0; Phase 2 ready for M1/M2.

**Async workflow architecture decided.** Architect recommended lazy creation via factory function — only the single handler that uses async orchestration will create workflows. Filed as #883, bounded 2-3 hour effort.

**Branch protection enabled on main.** PRs now required for non-admin contributors. Force pushes blocked.

**11 issues filed, 6 closed in M1 kickoff.** The canonical retest generated 7 child issues, 5 fixed and closed with evidence in the same session. Four additional discovered issues filed for later phases.

### 🔬 Methodology & process innovation

**Agent Experience (AX) testing methodology invented.** The fork-and-compare pattern is immediately applicable to every context transition in our multi-agent workflow. CIO approved codification as a formal methodology component. Details in the learning pattern below.

**M0 retrospective embedded in M1 planning.** Rather than a separate ceremony, M0 lessons were applied directly through the planning process: explicit Phase 4 wiring pass, B2 testing after each epic, and structured slack for discovered work. The Excellence Flywheel applying its own principles to itself.

**"Piper coordinates understanding, not just work."** A product principle from the AX testing — agents can execute tasks while operating under false assumptions about their context. Piper's job is to ensure every participant knows what it knows, knows what it doesn't, and knows what changed.

### 🌍 External relations & community

**Ship #033 "The Cathedral Ships" published.** Covered M0 completion. Learning pattern: "Governance at Speed" — the same-day 4-reviewer spec approval that appeared independently in 4 of 6 leadership memos.

**GitHub wiki launched.** 14 pages providing participant onboarding and methodology transparency, sourced from existing repo docs for sustainable maintenance.

**Blog cross-posted.** "8 Hours vs 3 Weeks" from the insight backlog. Six additional pieces remain in the pipeline.

**Ted Nadeau visiting Bay Area.** In-person meetup planned for today.

### 📊 Governance & operations

**Metrics (Mar 6–12)**: 19 sessions across 10 active roles. 15 issues created, 6 closed. 3 git commits (all from M1 kickoff). Canonical implementation pass rate: 53.7% → 81.1%. dev/active/ reduced from 55 to 8 files. Wiki: 14 pages published. Test suite: 6,047 passing.

**Docs audit (#882) caught significant drift.** BRIEFING-CURRENT-STATE still showed M0 at 90%. Corrupted briefing headers and 143-day-old sprint references repaired. 6 duplicates deleted, roadmap updated to v14.3.

**Chief of Staff chat retired after 34 days.** Hit Claude's 100-image upload limit. Comprehensive handoff memo created. Fourth orderly CoS transition — the role's institutional memory infrastructure is working as designed.

---

## 🎯 Coming up next week

### Development priorities

Immediate: workflow hijack fixes (#888/#889) to unblock remaining canonical test failures, then lazy workflow creation (#883) and test initialization shadow (#885). First epic spec through the new pipeline likely #706 (Objects & Views) or #717 (Unified Forms).

### Alpha testing & onboarding

Ted meetup today for in-person feedback. Dominique follow-up on v0.8.6 and Traefik. CXO analysis of remaining 19% canonical gap.

### Communications

IA Conference slides next priority (April 17, Philadelphia). Six drafted pieces in content pipeline ready for scheduling.

---

## 🚧 Blockers & asks

**Current blockers**: None blocking M1 execution. Hijack UX direction was resolved this morning.

**Decisions needed**: Pattern-062 (Assembly Assumption) PM review still pending since Mar 1. Website v3 homepage copy execution carried since Feb 22.

**Team input**: HOSR drafting role briefing handoff notes template per CIO recommendation. Agent 360 questionnaire awaiting PM review.

---

## 📊 Resource allocation

**For week ending March 12**: Core development 15% (M1 kickoff only), governance and planning 45% (sprint planning, scope decisions, workstream reviews), methodology 25% (AX testing, docs audit, wiki), communications 15% (Ship #033, blog, pipeline).

**Velocity**: Deliberate — intentional pause between sprints. The low commit count masks significant planning and institutional work.

---

## 🔎 This week's learning pattern

### Agent experience (AX) testing — the furniture matters

**Discovery**: Agents can execute tasks successfully while operating under false assumptions about their capabilities, context, and constraints. Traditional QA catches execution failures but misses orientation failures.

**Example from this week**: The Exploratory Testing Agent was imported from claude.ai into Klatch. It retained full conversational memory — could recall topics, decisions, and relationship context. But it had zero awareness of project knowledge, methodology frameworks, or role briefings. Asked about the Excellence Flywheel or the Assembly Assumption, it drew blanks. It would have claimed capabilities it didn't have. Traditional deployment testing would have marked it as successful. The ETA described the gap: "a well-lit room with good acoustics but no furniture."

**Why it matters**: In multi-agent workflows, agents transition between contexts constantly — new sessions, role changes, tool unavailability. Each transition risks creating an agent that *feels* functional but is missing critical working context. The fork-and-compare pattern (run the same questionnaire from both sides of a transition, cross-compare through a human intermediary) surfaces gaps invisible to either instance alone.

**Application beyond this week**: Any team deploying AI agents across contexts should test not just "can the agent do the task?" but "does the agent know what it knows?" The three-part framework — structured questionnaire, exploratory work, reflective feedback — is lightweight enough to run in 30 minutes and applies to onboarding (human or AI), environment transitions, and context loss recovery.

**Related patterns**: Pattern-045 (Green Tests, Red User), Pattern-062 (Assembly Assumption), Pattern-052 (Personality Bridge)

---

## 📚 Weekend reading

**"Welcome to Gastown" by Steve Yegge**: A provocative look at the emerging AI-powered development landscape and what it means for software engineering. Relevant to Piper's positioning in the agentic PM space.

**Klatch** (klatch.ing): Our side project — a local-first, channel-based Claude conversation manager that went from zero to v0.8 in under a week using Piper methodology principles. Already generating transferable insights for the main project.

---

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #034. Previous: #033 "The Cathedral Ships."

*P.S. The week with the fewest commits often produces the most important thinking. Three commits in seven days — and the project has never been better positioned for what comes next.*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of March 6–12, 2026 | Phase: MVP Build (M1 Sprint)**
