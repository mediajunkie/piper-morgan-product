# Weekly Ship #039: The Voice Takes Shape

<!-- image: 'piper-ship.png' -->
<!-- alt: 'A person leads a small boat crewed by robots.' -->
<!-- no caption -->

*April 10–16, 2026*

Last week's "The Floor Comes Alive" ended with the floor finally generating real responses after three rounds of UAT failures. This week, the question changed. Not "does the floor work?" but "how does the floor sound?" 

M1 closed on Friday after 33 days and four UAT rounds. By the following Thursday, M2a, M2b, and M2c were all complete — three sub-epics in five working days, the fastest sprint execution in project history. 

The canonical retest baseline went from 59% quality to 72.1%. The floor prompt got its Five Pillars and grammar — conceived by the CXO, drafted by the Lead Dev, approved, implemented, and measured in a single day. The ethics boundary got a voice design. 

And a small paraphrase error in an omnibus log — "presence over performance" written as "patience over performance" — triggered a correction chain across four agents that ended with canonical term verification built into the omnibus skill itself. The methodology's own instruments turned inward and found that while the practices were strong, their documentation had degraded beneath them. Eight formulations of the Excellence Flywheel across nine months, zero canonical document citations. The concept was alive; the documentation was dead. That's fixable. And fixing it is what this sprint is for.

---

# 🚀 Shipped this week

## 🎯 Product & experience

**M1 gate closed (April 11).** Four UAT rounds across 8 days (Apr 3, 7, 8, 10). Final: 7/9 Gate 1 passed, 1 marginal (memory tone), 1 known carry-forward (#922 affirmation handling, assigned to M2). All four gates passed. The trajectory — 0/9 → 0/9 → 5/9 → 7/9 — is the gate methodology's proof of concept. M1 ran 33 days (Mar 10 – Apr 11) with an expansion factor of ~2x (15 planned issues → 30+), better than M0's 3.9x.

**Vision V2.3 adopted, Roadmap v15.0 published.** PA synthesized four independent leadership reviews (PPM, CXO, CIO, Architect) — all endorsed the strategic direction with complementary refinements. Three-layer anti-flattening (CXO), methodology maintenance cost awareness (CIO), thin-wrapper-to-API distribution philosophy (PPM). Roadmap restructured around the differentiator stack: context methodology, conscious floor, artifact persistence, trust-graduated experience. Three issues filed from the review cycle: #964 (Floor-First Ethics Verification), #966 (Distribution Visual Identity), #967 (Surviving Edges).

**Quality baseline established and improved twice.** Three canonical retest runs tell the story:

- Run 1 (Apr 11): routing 41%, quality 59% — first honest baseline after M1 closure
- Run 2 (Apr 12): routing 95.1%, quality 65.6% — after #965 temporal quality and #968 routing reconciliation (methodology fix, not code change)
- Run 3 (Apr 16): quality 72.1% — after #950 Five Pillars + grammar in the floor prompt

The routing jump from 41% to 95.1% was a methodology fix: the retest runner was scoring against outdated expected-routing values. The quality jump from 65.6% to 72.1% was the floor prompt directly improving response quality. Both matter; neither would have been visible without the canonical retest infrastructure.

**Floor prompt design cycle completed in one day (#950, April 16).** CXO provided direction (Five Pillars: Identity, Time, Space, Agency, Prediction; Grammar: "Entities experience Moments in Places"). Lead Dev drafted. CXO reviewed and approved with refinements. Lead Dev implemented. Canonical retest measured. Quality improved. Conceived-to-measured in a single day — the spec pipeline at peak velocity.

**Ethics voice guidance delivered (#964, April 16).** CXO designed how Piper should sound at ethical boundaries: "The enforcer detects, but Piper speaks." Consciousness-as-architecture applied to the ethics boundary — the BoundaryEnforcer catches violations, but the response comes through Piper's voice, not a system message. Lead Dev discovered the BoundaryEnforcer was disabled in production; activation requires false-positive rate validation against the canonical corpus first.

## ⚙️ Engineering & architecture

**M2 executed at historic velocity.** Three sub-epics completed in five working days:

*M2a (Foundation Cleanup)*: 10/10 issues closed by April 12. Seven in a single day on Apr 12: #965 temporal quality, #968 routing reconciliation, #969 GitHub adapter bugs, #946 keychain consent, #947 dual LLM Phase 1, #962 inversion sweep, #949 server restart. The most concentrated single-day execution in project history.

*M2b (Testing Infrastructure)*: Complete by April 15. The entire three-tier CI pipeline — E2E on every PR, canonical regression on conversation changes, AAXT golden scenarios nightly — built and shipping in one afternoon (Apr 14). #929 AAXT verified 4/5 pass; one genuine quality finding (#922 context retention), not infrastructure. #971 executed per Architect direction: 10 files deleted (Pattern-012 adapters, ProviderSelector), llm_domain_service.py simplified by 160 lines. Principle: "don't maintain infrastructure for a future that hasn't been designed yet."

*M2c (Floor Prompt & Voice)*: Complete by April 16. #950 floor prompt (Five Pillars + Grammar + anti-flattening). #951 calendar context assembly. #964 ethics verification (voice guidance delivered, activation pending). #979 Haiku 3 retirement shipped 4 days before the Apr 19 deprecation deadline. Ruff migration (#981): black/isort/flake8 consolidated, 74 files reformatted.

**Floor inversion trilogy completed (April 13).** #925 migrated STATUS and PRIORITY categories to floor-first routing, completing the ADR-060 implementation. All read-only categories now route to the floor. The architectural promise of "LLM is the floor, not the ceiling" is fully realized in the routing layer.

**~18 issues closed, ~2,200 lines of dead code removed.** A remarkably productive week for the Lead Dev — sustained execution across all seven days with no wasted sessions. Test suite stabilized at 6,242 passing after deletions brought the count down from 6,309 (deleted tests > new tests, which is healthy cleanup).

## 🔬 Methodology & process innovation

**CIO methodology audit delivered (April 17).** M1 audit covering Mar 15 – Apr 11, with 12 recommendations across three tiers. Headline finding: the methodology is operationally the strongest it has been; its documentation is the weakest it has been. The Excellence Flywheel has 8 materially distinct formulations across 9 months. 20 of 22 numbered methodology docs went uncited in 128 session logs. The operational principles migrated to CLAUDE.md and role briefings while the methodology-core directory became a library nobody visits.

**Excellence Flywheel reformulation decided.** Three-layer canonical version: concept, practice, mnemonic. New fifth practice added: "Audit the composition" — Pattern-062 (Assembly Assumption) codified as a flywheel practice. CLAUDE.md decision: Option B — principles stand without the Flywheel label.

**PDR-004 correction chain (April 16).** CXO discovered that an omnibus log had paraphrased PDR-004's principle as "patience over performance" instead of the canonical "presence over performance." The error had propagated into two published blog posts. CXO sent a correction memo to Docs; Docs updated the omnibus skill to include a canonical term verification step; Comms flagged the affected posts for correction. A four-agent chain that turned a naming error into a systemic safeguard.

**Stacked Silent Failures formalized.** The CIO named the diagnostic pattern from the M1 gate arc: multiple independent failures at different architectural layers, each masking its own symptoms, producing composite behavior that appears to be a single problem.

## 🌍 External relations & community

**Six-act inversion arc complete.** "The Closing Sprint" (Apr 14) finished the series that began with "Ten Roles, One Day" on March 26 — six acts, six weeks of publication. The longest sustained narrative arc in project history. Seven new drafts produced (3 gate narrative pieces, 2 bridging narratives, 2 insight pieces), refilling the pipeline.

- April 11: "[The No-Anchoring Roundtable](https://pipermorgan.ai/blog/the-no-anchoring-roundtable/)" — insight piece from March 14, cross-posted here
- April 12: "[Archaeological Debugging](https://pipermorgan.ai/blog/archaeological-debugging/)" — insights from December 22, also cross-posted
- April 14: "[The Closing Sprint](https://pipermorgan.ai/blog/the-closing-sprint/)" — build narrative from March 20 to 22
- April 16: "[The Migration](https://pipermorgan.ai/blog/the-migration/)" — build narrative from March 28 to 30.

<!-- image: 'https://pipermorgan.ai/assets/blog-images/ai-finish.webp' -->
<!-- link: (https://pipermorgan.ai/blog/the-closing-sprint/)>
<!-- alt: 'A runner crosses a finish line on a newly solid track while ghostly alternate paths converge behind them, guided by glowing, translucent AI companions assembling the final pieces in midair.' -->
<!-- caption: '"Almost there!"' -->

**IAC conference.** I arrived in Philadelphia in time for the conference start on Thursday, April 16, prepared to present "Ethics as Information Architecture: Why AI Safety Requires IA Thinking" delivered in Philadelphia the following day.

## 📊 Governance & operations

**Metrics (Apr 10–16)**: ~37 sessions across 7 days (peak: 9 sessions on Apr 10 and Apr 11). M1 closed. M2a/M2b/M2c complete. ~18 issues closed. ~2,200 LOC removed. Quality: 59% → 72.1%. Routing: 41% → 95.1%. 9 publications. 28 commits on Apr 16 alone. Testing infrastructure fully operational.

**Sprint reassignment executed.** PA created 10 new issues with detailed acceptance criteria. 12 closures, ~40 reassignments across milestones. Roadmap v15.0 restructured around the differentiator stack.

**PM mail delivery bottleneck visible.** April 16: 37+ memos routed across agents, PM manually shuttling between filesystem and Claude Chat throughout the day. Scaling constraint on high-coordination days.

---

# 🎯 Coming up next week

## Development priorities

M2d (Context Assembly) and M2e (Conversation Features) next in the super-epic sequence. #922 (affirmation handling) carried from M1. BoundaryEnforcer activation (#964) pending false-positive validation. PPM quality thresholds: 80%+ conversational, 90%+ action handlers.

## Alpha testing & onboarding

Alpha tester silence: 33+ days, zero responses from 13 testers. HOST has flagged five times across multiple agents. PM considering phase ending. 

## Communications

Gate narrative arc ready (3 pieces drafted Apr 13). Building narrative pipeline refilled. Weekend thematic pairing continues.

---

# 🚧 Blockers & asks

**Current blockers**: None. M2d/M2e execution is next; prerequisites complete.

**Decisions needed**: Alpha tester phase ending. BoundaryEnforcer activation timing. Colleague Test v2 distribution (CXO completed formalization Apr 19).

**Team input**: CIO Flywheel Phase 2 resolution timing. HOST briefing rename still pending. PM mail delivery bottleneck — structural fix needed?

---

# 📊 Resource allocation

**For week ending April 16**: M2 execution 40% (M2a 10 issues, M2b testing infra, M2c floor prompt + ethics + cleanup), quality measurement 15% (3 canonical retest runs), methodology 15% (CIO audit, Flywheel reformulation, PDR-004 correction chain), communications 15% (9 publications, 7 new drafts, six-act arc complete), strategic planning 10% (Vision V2.3, Roadmap v15.0, sprint reassignment), governance 5% (weekly audit, calendar backfill).

**Velocity**: The most productive week in project history by any measure. Three M2 sub-epics in five working days. Quality from 59% to 72.1%. And the methodology audit revealed that the project's self-knowledge hadn't kept pace with its execution — which is itself a sign of health, because the audit caught it.

---

# 🔎 This week's learning pattern

## Execution velocity can outrun self-knowledge — and the fix is built-in auditing, not slower execution

**Discovery**: A project can sprint at peak velocity while its own documentation silently degrades. The Excellence Flywheel — the project's most referenced methodology concept — existed in 8 materially distinct formulations across 9 months, with zero canonical document citations in 128 session logs. The practices were strong; the documentation was broken.

**Why it matters**: The conventional response is "slow down and document." But the CIO's audit suggests the opposite: the documentation degraded *because* the methodology was working — practitioners absorbed the practices and stopped referencing the source documents. The gap isn't between doing and documenting; it's between documenting and maintaining documentation.

**The fix**: Not slower execution, but maintenance mechanisms built into the sprint cadence. The PDR-004 correction chain shows what catching drift looks like in practice: CXO spots a wrong term → Docs adds verification to the omnibus skill → Comms flags affected posts → correction propagates. Four agents, one afternoon, systemic safeguard installed.

**Application beyond this week**: Any team that tracks its own methodology should build in periodic "does the documentation match the practice?" audits. The CIO's approach — surveying 128 session logs for methodology doc citations — is lightweight enough to run quarterly and revealing enough to catch drift before it becomes folklore.

**Related patterns**: Pattern-062 (Assembly Assumption), the Excellence Flywheel (now with a fifth practice: "Audit the composition"), the PDR-004 correction chain

---

# 📚 Weekend reading

**The Five Pillars.** Identity, Time, Space, Agency, Prediction. The floor prompt's organizing framework for how Piper understands user context. Combined with the Grammar ("Entities experience Moments in Places"), this gives the floor a consistent way to parse any query. The #950 implementation went from CXO direction to measured quality improvement in a single day.

**The differentiator stack.** Context assembly methodology, conscious conversational floor, artifact persistence, trust-graduated experience. Everything below this is commodity plumbing. The stack is now the organizing principle for the roadmap (v15.0). If you're building AI-powered tools, the question isn't "what integrations do you support?" It's "what do you do with the context once you have it?"

---

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #039. Previous: [#038 "The Floor Comes Alive"](https://pipermorgan.ai/shipping-news/weekly-ship-038-the-floor-comes-alive/).

*P.S. Three sub-epics in five working days. Quality from 59% to 72.1%. The floor inversion complete. And the methodology audit found eight formulations of its own flagship concept. The project's execution outran its self-knowledge — and the audit caught it. Sometimes the most important thing you build is the instrument that tells you what you've forgotten.*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of April 10–16, 2026 | Phase: MVP Build (M2 Sprint — Foundation + Testing + Voice)**
