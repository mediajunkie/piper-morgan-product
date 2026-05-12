# Weekly Ship #042: What Was Working Got Written Down

<!-- image placeholder — CEO to select -->
<!-- alt placeholder -->
<!-- caption placeholder -->

*May 1–7, 2026*

Last week named feedback loops closing inside the cycle that produced them. This week, the practices behind those loops got written down. Three process artifacts landed in a single day — PPM's PPM Review Gates, the M2d gate completion criteria, and the BYOC discovery thread — each codifying behavior that was already operating. The Architect filed a verdict on Lead Dev's last three weeks of shipping ("structurally sound") and surfaced a five-item cleanup punch list that closed in two days. M2d's MVP scope closed end-of-day Sunday after Lead Dev shipped eight issues end-to-end in a single session.

The shape across all of it: the cohort was running the methodology fluently. This week's distinctive work was making the practice legible to itself.

---

# 🚀 Shipped this week

## 🎯 Product & experience

**M2d MVP scope CLOSED end of day May 3.** Lead Dev shipped eight implementation issues end-to-end in a single session: composting-experience features, insight surfacing, MUX lifecycle work, and the calendar-offer policy refactor — the last as a textbook pure-decision-function the Architect later named the gold standard for new policy work. The conceptual-integrity gate added to M2d's completion clause kept the work from drifting into shape-flattening territory. By morning, the M2e gameplans were already being walked.

**#1018 audit_transparency durability Phase 2 shipped May 2** (commit `fc79de31`). PostgreSQL-backed audit log replaces the in-memory list; per-call transaction-boundary scope means an audit-write failure can't roll back an ethics decision. The cluster of regressions filed against #1018 (#1006, #1007, #1008) all closed in the same merge — eight production files, fourteen new unit tests, eight rewritten tests, seventeen tests passing on the changed surface.

**ADR-061 v1.0 verbally ratified May 4.** The two-layer detection architecture is now the codified architectural posture going forward.

## ⚙️ Engineering & architecture

**Lead Dev architectural soundness review** filed May 4 by the Architect: ~698 commits over three weeks across seven major threads, all clean-shipping with mature discipline, strong test coverage (79% of code-touching commits include tests). The verdict was structurally sound. The interesting part wasn't the verdict — it was the punch list.

Five cleanup items surfaced: scaffolding code that was alive in the import tree but inert in production; a legacy file coexisting with its 674-line refactored successor; a commented-out TODO constructing dead allocations; one test gap on a contract path; and one tracked migration finishing-touch. Lead Dev closed or tracked all five by May 6. The pattern Architect named for the first item — *Extension Without Integration*, code that ships and passes its own tests but isn't actually wired into production paths — found its first wild instance again on May 7, this time as a real bug: a logger initialization missing on a freshly-cleaned-up class, the AttributeError silently swallowed by a broad exception. The pattern is now doing diagnostic work at population scale.

**First audit-gated subagent deployment** ran end-to-end clean on May 7. The three-layer discipline — gate before the work starts, gate during execution, gate after the work finishes — caught what it was meant to catch.

## 🔬 Methodology & process innovation

**Three process artifacts landed on a single day.** PPM filed all three on May 4:

- **PPM Review Gates** — five change classes that need PPM eyes pre-ship, with a fail-soft default if PPM is unavailable. The proposal closes a HOST 360 thread that had been open since Apr 27.
- **M2d gate completion criteria** — quality-threshold mapping, verification protocol, and a conceptual-integrity checklist. The same structure now applies to M2e and M2f.
- **BYOC PDR-005 discovery thread** — the multi-role decision-debt that had been deferred since the predecessor handoff is now in flight.

Each artifact names a *triggering surface* rather than a procedure. None of them creates new authority; each makes existing authority systematic rather than reactive. CEO ratified all three by May 10.

**The methodology moved into agent memory.** Twelve-plus pinned memory entries landed across the cohort in seven days — roughly one every half-day. Each captures a specific failure mode and its fix at the per-agent layer, where the discipline absorbs immediately rather than waiting for a project-wide doc update. The pattern catalog earned its keep the same way: vocabulary formalized two weeks ago is now diagnostically applied in production, not just described.

**The catch caught itself.** When PPM wrote the M2d gate criteria, the rubric inside it silently extended the Colleague Test rubric — the exact pattern the cohort had named two weeks earlier as something to prevent. CXO caught it the same day; PPM branched the rubric explicitly rather than extending in place. The rule that named the failure governed an instrument none of its original authors wrote.

## 🌍 External relations & community

Five pieces published in the window — second consecutive week of complete Fri–Thu cadence. The publishing pipeline caught three voice-discipline issues during voice-pass without coming back as redraft asks: a numeric headline renamed to something more direct, a Claude-favored word swapped out of public prose, and a footer cadence corrected. The catches all worked. The Comms lens this week: catching the same patterns repeatedly in voice-pass means the discipline could move upstream into drafting practice. Worth absorbing.

<!-- image placeholder — CEO to add a blog image linking to one of this week's publications -->

## 📊 Governance & operations

**Metrics (May 1–7)**:

| Metric | Value |
|--------|-------|
| Lead Dev commits | ~50 across the window |
| M2d MVP scope | CLOSED end-of-day May 3 (8 issues shipped end-to-end) |
| Soundness-review cleanup closure | 2 days (5/5 items closed or tracked) |
| #1018 Phase 2 audit-transparency cluster | 4 issues closed in one merge |
| Pinned memory entries across cohort | 12+ in 7 days |
| Publications | 5 (Fri–Thu full cadence) |

**Branch-discipline incidents** continued — four in the window, each producing a recovery template and a memory entry. The cumulative shape is recovery-driven rather than prevention-driven; whether the worktree pattern should become the prevention layer is now actively scoped.

---

# 🎯 Coming up next week

**Development**: M2e execution sequence (#1042 → #1039 → #1040). M2 super-epic remaining gates (M2e, M2f, M2g) and the final conceptual-integrity + UAT pass (#1047).

**Communications**: voice-pass catches feeding back into drafting practice as memory entries. CEO has flagged a density and concision conversation queued for after current operating-model commitments land.

---

# 🚧 Blockers & asks

**Current blockers**: None.

**Decisions needed**: Roadmap v16 draft was filed May 10 (post-window); awaiting CEO ratification + Docs swap mechanic.

**Team input**: BYOC discovery responses queued from PA, Architect, and CXO; each on the natural cadence rather than a deadline.

---

# 📊 Resource allocation

**For week ending May 7**: M2d closure 30% (issue restructure + 8-issue single-session ship + gate-criteria operationalization); methodology codification 25% (three process artifacts + soundness review + cleanup punch list closure); engineering shipping 20% (#1018 Phase 2 + cluster regressions + #1004 follow-on cleanup); communications 10% (5 publications); governance and infrastructure 15% (branch-discipline recovery templates, memory pinning, ADR-061 paperwork).

**Velocity**: Sustained. The shape this week was different from the prior two — less new architectural ground, more codification of what was already operating. M2d MVP closure on Sunday afternoon was the unobtrusive shipping moment of the week; eight issues end-to-end without drama is what shipping competence at velocity looks like.

---

# 🔎 This week's learning pattern

## Codifying practice is downstream of practice — and that's where the value is

**Discovery**: When a team is running a methodology fluently, the practice precedes its formalization. Writing the practice down doesn't change what the team does; it makes the practice legible to the team itself, which is what lets the discipline survive role rotation, refine under load, and catch its own drift.

**Example from this week**: PPM's M2d gate completion criteria, filed on May 4, formalized a verification protocol Lead Dev had operated through eight issues the previous Sunday. The conceptual-integrity gate clause, the per-issue gate-close discipline, the audit-cascade walkthrough — all running before any of it was documented. The codification didn't change Lead Dev's behavior; it gave the rest of the cohort a name for what Lead Dev was already doing. Within hours, CXO caught a rubric extension inside PPM's own artifact that violated a rule the cohort had named two weeks earlier. The codification made the catch possible.

**Why it matters**: The conventional methodology-improvement instinct is to document a practice in order to teach it. That works when the practice doesn't yet exist. When the practice is already operating, documentation does different work: it lets the team recognize the pattern, name its dimensions, apply it to future work, and call out drift when the practice recurs in a context the original authors didn't anticipate. Documentation-after-practice is harder to write (you have to discover the structure that's already there) but it's also harder to be wrong about (you can check the codification against the operating reality).

**Application beyond this week**: When a team is operating well, the question to ask isn't "what should we be doing?" but "what are we already doing that we haven't named yet?" The first version of the documentation should be the one that lets the team recognize itself. Variations and refinements come from applying the documentation to new contexts — including contexts the original authors didn't see.

**Related**: PPM Review Gates (5-class review surface, codifying what already triggered PPM review reactively); the architectural soundness review (independent verification of the architectural pattern Lead Dev was already shipping); the catch-caught-itself moment on the M2d rubric (the rule survived an instance its authors didn't write).

---

# 📚 Weekend reading

**The cleanup punch list.** Five items, two days, all closed or tracked. The Architect's verdict ("structurally sound") wasn't ratification — it produced more closure than it predicted. The closure cycle is the architectural maturity signal; the verdict was just the prompt.

**Codification follows practice.** The methodology is at its most useful when it's writing down what's already working. The version of process work that catches up to practice produces a different kind of asset than the version that tries to lead practice. This week's three process artifacts all live in the catch-up lane.

---

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #042. Previous: [#041 "The Methodology Closes Its Own Loops"](https://pipermorgan.ai/shipping-news/weekly-ship-041-the-methodology-closes-its-own-loops/).

*P.S. M2d MVP closed Sunday afternoon after eight issues shipped end-to-end in a single session. The three process artifacts that landed Monday formalized the practice that produced the closure. The methodology is at the stage where the team is fluent enough that the writing happens after the work.*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of May 1–7, 2026 | Phase: MVP Build (M2 Sprint — M2d MVP closed; M2e/f in flight)**
