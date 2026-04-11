# Weekly Ship #037: New Ground

*March 27 – April 2, 2026*

Last week's "Approaching the Gate" ended with 14 test scenarios waiting for the PM to sit down with Piper and have a conversation. That conversation didn't happen this week — instead, the entire project picked up and moved. All 12 agent roles migrated from one account to another in a single day: 18 sessions, 8 handoff memos, 8 successor orientations, zero context loss. Around that migration, the blog became a real self-hosted platform (four canonical publishes in five days), Piper Alpha went from "briefing ready" to producing independent strategic analysis, and every fresh pair of eyes that touched the project found something the established roles had normalized. The gate is still waiting. But the ground it sits on is new.

---

# 🚀 Shipped this week

## 🎯 Product & experience

**Infrastructure migration completed in a single day.** All 12 active agent roles migrated to new infrastructure on March 30 — 18 sessions across two waves (morning workstream reviews, afternoon successor onboarding). Eight predecessor handoff memos carried context; every successor confirmed orientation. The highest single-day role diversity in project history, with zero coordination loss. The migration was an unplanned full-system test of institutional continuity infrastructure: briefing documents, handoff protocol, mailbox system, and omnibus logs collectively carried enough context for 12 simultaneous role transitions.

**Piper Alpha operational.** PA went from Phase 0 (artifacts ready) to Phase 1 (active operations) across four days. Day 1 (Mar 30): an 8-hour institutional knowledge sweep — 60 ADRs, 47 patterns, 15 omnibus logs, 12 cross-pollination briefs. Closed #912, reviewed PR #856, delivered the project's first PA standup. Day 2: five-layer context mapping, RFC-001 response to Dispatch, Vision V2 first draft. Day 3: traced and fixed a hardcoded Lead Developer identity in CLAUDE.md that caused role confusion after compaction — a latent bug affecting all non-Lead-Dev sessions. Day 4: independent backlog audit (119 open issues, 89 in MVP milestone), roadmap refresh prep, daily check-in flow draft. Four days from "read everything" to self-directed strategic analysis.

**M1 gate UAT prepared.** CXO compiled the verified test plan: 9 Gate 1 queries (conversation quality) and 5 Gate 2 scenarios (task lifecycle), scored using the Colleague Test rubric (Relevance, Competence, Tone — 0-3 each, 7+ to pass, any 0 auto-fails). The original smoke queries from #926 weren't in project knowledge — only the CXO's expanded set was documented. The gate is ready for execution.

**HOST rename completed.** HOSR → HOST (Head of Sapient Trust) across all operational files: mailbox, directory, skills, guides, NAVIGATION.md. Briefing content refresh still pending.

## ⚙️ Engineering & architecture

**Blog-first canonical publishing achieved.** Four blog-first publishes in five working days: "Discovery Is the Bottleneck" (Mar 28), "Wiring vs. Wizardry" (Mar 29), "Are We Doing It Backwards?" (Mar 31), "The Floor That Wasn't" (Apr 2). Each publish surfaced and fixed infrastructure bugs — CSV parser field count (11→13 columns), date normalization (275 posts to ISO 8601), Medium link conditionals, non-hex hashId rendering, `formatDate()` timezone off-by-one. The publish-to-blog skill iterated from v0.3 to v0.5 across these runs. By Apr 2: 275/275 posts self-hosted on pipermorgan.ai, Medium demoted to syndication credit, the broken 15-episode system replaced with a working 5-era model.

**Shipping News section launched.** [PiperMorgan.ai](https://pipermorgan.ai/shipping-news) now has a dedicated `/shipping-news` route with its own visual identity (orange accent, ship badge). Last week's Ship #036 "Approaching the Gate" is the inaugural entry.

**CLAUDE.md identity fix.** PA traced commit history and discovered that `CLAUDE.md` had a hardcoded "You are the Lead Developer" identity statement that persisted through context compaction, causing role confusion for every non-Lead-Dev agent. Replaced with a role routing table — agents now read their assigned briefing rather than inheriting a stale identity.

**Branch discipline safeguards.** Pre-commit hook added that warns when committing on `main` instead of a `claude/*` branch — defensive infrastructure for multi-agent branching hygiene.

## 🔬 Methodology & process innovation

**RFC-001 (Five-Layer Context Model) bilateral response completed.** Dispatch published the RFC on Mar 30 requesting layer mappings. PA completed the Piper Morgan mapping (both agent team and product code) by Mar 31. CIO endorsed with three amendments: keep "Methodology" as Layer 2 canonical name, add the Three Clocks Problem as a named Layer 3 failure mode, formalize Agent Traditions as a recommended Layer 5 recovery approach. Klatch filed its own response with four amendments, including an L5 sub-component split (declarative vs. procedural). Both projects confirmed the same gap profile: strong L1-L2-L3 and weak L4-L5. Fastest RFC-to-bilateral-response cycle the ecosystem has achieved — 3 days.

**Fresh eyes as diagnostic method.** Every role that looked at the system with fresh eyes during migration found something established roles had normalized. CXO flagged BRIEFING-ESSENTIAL-CXO as 3 months stale (Jan 5 → refreshed to Mar 31 within hours). HOST flagged alpha tester silence (now 25+ days), session cadence gaps, and Comms sprint visibility — within minutes of onboarding. PA traced the CLAUDE.md identity bug that had been affecting every non-Lead-Dev session. The migration functioned as an unintended audit: new instances holding old assumptions up to the light.

**PA's floor/ceiling/path taxonomy.** PA developed a classification for moments during its cold-start sweep: floor moments (LLM general competence suffices), ceiling moments (domain knowledge required that docs can't provide), and path moments (where the conversational approach works better than planned structured architecture). This taxonomy was immediately cross-relevant — the cross-pollination brief surfaced it as applicable to Klatch's import pipeline.

## 🌍 External relations & community

**Five publications in six days.** Four blog-first canonical posts plus Ship #036 on PiperMorgan.ai and then syndicated to Medium or LinkedIn or both as the case may be. The content pipeline has shifted from "mine more content" to "sequence and publish thoughtfully" — the Mar 26 production session's 15 drafts are being published at a sustainable pace. The six-act building narrative series progressed: Act 2 ("Are We Doing It Backwards?") and Act 3 ("The Floor That Wasn't") published.

- Mar 28: "[Discovery is the Bottleneck](https://medium.com/building-piper-morgan/discovery-is-the-bottleneck-978f3ec50a57)" — insight piece from December 28, cross-posted here
- Mar 29: "[Wiring vs. Wizardry](https://medium.com/building-piper-morgan/wiring-vs-wizardry-f29671b088b7)" — insights from March 12 and 13, also cross-posted
- Mar 31: "[Are We Doing It Backwards?](https://medium.com/building-piper-morgan/are-we-doing-it-backwards-abb0dc2d0d80)" — build narrative from March 14
- April 2: "[The Floor That Wasn't](https://medium.com/building-piper-morgan/the-floor-that-wasnt-021ded823bdb)" — build narrative from March 15 and 16.

<!-- image: 'ai-backwards.png' -->
<!-- link: (https://pipermorgan.ai/blog/are-we-doing-it-backwards/)>
<!-- alt: 'People struggle to reach an AI on the ceiling amid tangled machinery, while others stand easily on a glowing AI “floor” in a calm, open space nearby.' -->
<!-- caption: '"Does something seem off to you?"' -->

**Content sequencing framework established.** Three weekends of thematic pairs planned: "things hiding in plain sight" (Apr 5-6), "how you figure things out" (Apr 11-12), "working together at scale" (Apr 18-19). The constraint is now sequencing, not generation.

**IAC talk approaching.** "Ethics as Information Architecture" (April 17, Philadelphia) — 16-slide deck and speaker notes drafted. Now 9 days out. Flagged as next priority for the Comms workstream.

## 📊 Governance & operations

**Metrics (Mar 27 – Apr 2)**: ~34 sessions across 7 days (peak: 18 on Mar 30). 275/275 blog posts self-hosted. 5 publications. PA operational (Days 1-4). 12-role migration completed. RFC-001 bilateral response completed. Quarterly maintenance 12/15 items complete (#938). ~70 commits across product and website repos.

**Briefing refresh wave.** BRIEFING-ESSENTIAL-CXO updated from Jan 5 to Mar 31 — now current with Colleague Test, floor-first routing, and M1 gate UAT. CIO enforcement checklist completed. Methodology-23 (M1 Innovations) created, cataloging 6 innovations. BRIEFING-CURRENT-STATE refreshed to Mar 29.

**Quarterly maintenance.** 12 of 15 items completed on #938. PA found 14 untracked TODOs in `services/` during the audit — memo sent to Lead Dev for triage. Four missing `__init__.py` files identified.

---

# 🎯 Coming up next week

## Development priorities

M1 gate UAT execution and remediation. The gate has been ready since Mar 31 — 14 scenarios, Colleague Test scoring, fresh alpha account. The fixes from the first attempt (Apr 3-5) have cleared all five findings. Re-test is the immediate priority. If the gate passes, M1 closes and M2 planning begins.

## Alpha testing & onboarding

Alpha tester silence: 25+ days since Mar 14 email to 13 recipients, zero responses. HOST recommends a channel change — different medium, adjusted ask, or 1:1 outreach. PM decision needed. Dominique's silence may be related to the web setup wizard migration bug (500 error on account creation) that Lead Dev fixed on Mar 31.

## Communications

IAC presentation (April 17) — 9 days out. Draft deck and speaker notes exist but haven't been revised in the new project. Approaching urgency. Building narrative Acts 4-6 scheduled through April 15. Weekend insight pairs continuing.

---

# 🚧 Blockers & asks

**Current blockers**: M1 gate closure depends on PM availability for re-test. All five UAT findings from the first attempt have been fixed.

**Decisions needed**: Alpha tester re-engagement approach (channel change vs. adjusted ask vs. 1:1 outreach). PA scope for M2 period. M2 scope planning approach (PA's backlog audit recommends triage pass — 89 MVP issues, May 27 target).

**Team input**: HOST briefing rename and content refresh pending (HOSR → HOST). CIO innovation backlog location needs confirming after migration.

---

# 📊 Resource allocation

**For week ending April 2**: Infrastructure and migration 35% (12-role migration, blog platform maturation, Shipping News section), PA operational ramp 25% (4-day cold-start through independent analysis), communications 20% (5 publications, content sequencing, IAC awareness), methodology 15% (RFC-001 bilateral response, fresh-eyes diagnostic, floor/ceiling/path taxonomy), governance 5% (quarterly maintenance, briefing refresh, open items tracking).

**Velocity**: The codebase was stable — the M1 code didn't change this week. Everything around it was rebuilt. The migration proved the institutional infrastructure works at scale; the blog pipeline proved iterate-after-ship works for publishing; PA proved the cold-start cost is high but the payoff is fast. The foundations are new. The product is ready to be tested.

---

# 🔎 This week's learning pattern

## Fresh eyes find what familiarity hides

**Discovery**: When agents onboard into an existing system — whether through migration, role creation, or briefing refresh — they reliably surface problems that established roles have normalized. This isn't a failure of the established roles; it's a structural property of familiarity. The things you stop seeing are the things that need seeing most.

**Examples from this week**: CXO's successor flagged that BRIEFING-ESSENTIAL-CXO hadn't been updated since January 5 — three months of architectural revolution (ADR-060, floor-first routing, Colleague Test formalization) were absent from the role's own briefing. HOST's successor flagged alpha tester silence (25+ days without a response) and session cadence gaps within minutes of onboarding — observations that had been noted but not escalated. PA traced a hardcoded Lead Developer identity in CLAUDE.md that affected every non-Lead-Dev session — a latent bug introduced months earlier that nobody reported because each role assumed the identity confusion was a one-off compaction artifact.

**Why it matters**: The conventional response to staleness is "update your docs more often." But the real mechanism is periodic fresh-eyes contact. No amount of documentation discipline catches the things you've stopped questioning. The migration forced 12 roles to look at the system simultaneously with fresh eyes, and each one found something. That's not a bug in the process — it's the process working.

**Application beyond this week**: Any team can manufacture fresh-eyes moments without a forced migration. Periodic role rotations, structured onboarding reviews ("what surprised you in your first session?"), or designated "naive reader" passes on key documents. The Agent 360 questionnaire from March 19 was essentially a formalized fresh-eyes exercise — and it produced the same category of findings. The pattern is: ask someone who hasn't been living in the system to tell you what they see. Then believe them.

**Related patterns**: Agent 360 (formalized fresh-eyes survey), Pattern-045 (Green Tests, Red User — another form of familiarity blindness), the Colleague Test (external perspective on response quality)

---

# 📚 Weekend reading

**RFC-001: Five-Layer Context Model**: Both Piper Morgan and Klatch have now filed formal layer mappings. The shared finding — strong L1-L2-L3, weak L4-L5 — gives both projects a diagnostic vocabulary for context delivery. The CIO's Three Clocks observation (Layer 3 failure mode: knowledge fragmented across Chat sessions, Code memory, and repo docs) names a problem every multi-surface agent team will eventually face.

**PA's floor/ceiling/path taxonomy**: When PA swept 60 ADRs, 47 patterns, and 15 omnibus logs during its first session, it developed a classification for what worked (floor — the LLM handled it), what didn't (ceiling — domain knowledge the docs couldn't provide), and what surprised (path — the conversational approach worked better than the planned structured one). If you're onboarding AI agents into complex projects, this taxonomy is worth stealing.

---

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #037. Previous: [#036 "Approaching the Gate"](https://www.linkedin.com/pulse/weekly-ship-036-approaching-the-gate/).

*P.S. Twelve agent roles migrated in a single day. Eighteen sessions. Eight handoff memos. Zero context loss. The institutional memory infrastructure we've been building for months got its stress test — and passed. Sometimes the most important thing you ship is proof that the system holds.*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of March 27 – April 2, 2026 | Phase: MVP Build (M1 Sprint — Gate Verification)**
