---
image: piper-ship.png
alt: 'A boy leads a boat crewed by robots.'
caption: N/A
---

# Weekly Ship #043: The Skill That Doesn't Fire

*May 8–14, 2026*

The team has been writing the methodology down faster than ever — six anti-patterns formally indexed in one morning, four commit-discipline entries pinned across the week, a verification rubric branched mid-stream from a methodology codified about two weeks earlier. The codification side is working.

And then, on Wednesday May 13, the lead-developer role ran a self-audit on its own recent issue closures and found a skill that had been in skill files for months hadn't fired on thirteen out of thirteen closures. Every one of them missed the same step.

This week is about that gap. Writing discipline down is real progress. Writing it down is not the same as making it happen.

---

# 🚀 Shipped this week

## 🎯 Product & experience

**Cross-session memory moved from "designed but unimplemented" to production.** Thursday May 14 closed M2g-B with the lead-developer role shipping #1021 UserHistoryService Layer 3 DB backend end-to-end — schema migration, four new conversation columns, three indexes, repository, heuristic topic extraction, preview maintenance, four API routes, and floor wiring through the context assembler. Two-hundred-forty-five tests green. ADR-054 Layer 3 and PDR-002 adaptive greetings now produce real signal rather than describing intent.

**Build milestone gates moved on schedule.** The M2f milestone closed across the window — Groups A+B end-to-end on Saturday May 9, Group C end-to-end on Monday May 11. M2g-A landed Thursday May 14 (owner-reviews on services/auth #1000 + services/mcp/consumer #999). Run 9 of the canonical baseline was locked Wednesday May 13 as the M2g-entry reference point. The product-management role (Piper Alpha) consolidated the M2d gate-decision criteria into a single memo on Sunday May 10, giving the developer a clear pass/fail surface across the sub-epics.

**A new UI scope plan opened.** Thursday May 14, the lead-developer role filed #1090 UI-1.0-PLAN after the experience-design role (CXO) surfaced a coverage gap — seven UI surfaces beyond the current MUX scope that need explicit shape decisions before 1.0. The work doesn't begin this window. The fact that the gap is now named and tracked is the artifact.

**Roadmap v15 → v16 swap closed an arc that crossed four roles.** Documentation Management asked for the version bump May 4, the product-management role drafted v16 (held for review) May 10, the CEO ratified the same day, and Documentation Management swapped the canonical file the next morning — with the prior weekly docs audit retained as a backstop per Chesterton's-fence framing. Sub-daily methodology-to-canonical pipeline, end to end.

## ⚙️ Engineering & architecture

**Three substantive backend ships across three days.** Sunday May 10: #921 FastAPI / Starlette / httpx upgrade merged on directional evidence — conservative pin (fastapi 0.115.14, starlette 0.46.2, httpx 0.28.1), six test-helper sites migrated to the new `AsyncClient(transport=ASGITransport(app=app))` pattern, full-suite verification deferred to a follow-up ticket (also closed by Monday). Monday May 11: #857 token refresh shipped end-to-end — new `POST /api/v1/auth/refresh` endpoint with token rotation, 7-day max-age refresh cookie at login, frontend wrapper intercepts 401 with silent refresh and retry. Same day: #1071 audit-log gap closed for pre-beta hardening (`Action.KEY_VALIDATION_FAILED` enum wired through the validation-failure path with PII protection — first 8 chars of the key only).

**Two evaluation-and-search ships landed Wednesday May 13.** #1070 multi-turn evaluation harness shipped end-to-end, and #304 NOTION search-only activation went from "designed but inert" to live.

**A new verification rubric got branched mid-stream from a recently-codified methodology, with full provenance.** On Sunday May 10, the product-management role proposed extending the current milestone's verification rubric in place. The experience-design role caught it within the same session as an instance of *parallel-authoring-drift* — exactly what the *Branch-or-Anchor* methodology had been codified to prevent about two weeks earlier. The product-management role branched to a new artifact (UI Lifecycle Verification Rubric v0.1), and the architecture role ratified it as the first clean worked example of the methodology operating end-to-end. About ninety minutes, three roles, full provenance trail.

**Branch-drift discipline ladders got another four layers.** Five separate version-control incidents in the cycle drove four new commit-discipline memory entries — pre-commit branch verification, pre-edit diff-against-HEAD, index-clearing on shared main, and post-commit verification with `git show --stat`. Each layer catches what the prior layer missed. Each is grounded in a specific incident from the week, not a projection.

**A working-tree-path fragmentation child instance was caught at sub-sixty-minute blast radius.** The innovation-officer role had backlog edits stranded overnight May 10–11 — edited via the main checkout while the worktree's `git status` showed clean. P-17 joined the Pattern-067 family the same morning. The parent meta-pattern is now actively catching its own children.

## 🔬 Methodology & process innovation

**The skill that didn't fire.** On Wednesday May 13, the lead-developer role ran a self-audit on its own recent issue closures — a hunch that something in the closure routine had been slipping. The audit found thirteen recent closures. On all thirteen, the description checkboxes had stayed unchecked. The evidence comments had landed. The work had been done. The small mechanical step that turns a closed issue into a closed issue's record had not happened. The skill that should have caught this was in the file. It hadn't fired.

The remediation that landed the same afternoon had three layers, all stacked. A **memory entry** pinned to the top of the project's memory index, so future sessions of the lead-developer role see it on first read. A new **tooling issue (#1083)** filed for a lint that would catch the checkbox-leftover mechanically — the kind of thing that doesn't depend on remembering. And a **standing floor of discipline** written into the closure process itself, so every closure now starts with the description checkboxes rather than ending with them. Vocabulary plus mechanism plus sequence — each covers what the prior layer misses.

**The pattern catalog ran a sweep on itself.** The innovation-officer role compiled the second pattern sweep on Saturday May 9, formally indexing six anti-patterns the cohort had been calling by working names ("branch drift," "comment-only close," "issue-body reality mismatch"). The names became canonical, the parent-child relationships got mapped, and within forty-eight hours the cohort was using the indexed names in mid-stream catches without consulting the catalog.

**Pattern-067 fired six times in five days.** The issue-body-reality-mismatch family — filed by the lead-developer role on Saturday May 9 — stayed the most active surface of the week. Named and instrumented-against in real time rather than retrospectively. Notable: when the innovation-officer role attempted to file a different pattern at the same Pattern-067 slot on Monday May 11, the collision was resolved same-day via first-filed-wins, with the innovation officer renumbering to slots 068 and 069. The recurring-failure surface was being instrumented faster than it was firing.

**Working memory layer is now substrate.** Four commit-discipline entries pinned to per-agent memory across the week. Each one captures a specific failure mode and its fix, at the per-agent layer, where the discipline absorbs immediately. The first observed downstream applications of recently-pinned memories appeared roughly three days after pin — a real compounding loop is visible.

## 🌍 External relations & community

**Four pieces published in the window, with one held**:

- May 11 (Mon): "[The Inchworm Position](https://pipermorgan.ai/blog/the-inchworm-position)" — insight on a notation system for naming exactly where you are in a nested work hierarchy
- May 12 (Tue): "[Audit and Talk](https://pipermorgan.ai/blog/audit-and-talk)" — building narrative on April 17, an IA Conference talk on ethics-as-architecture running parallel to the innovation-officer role opening the M1 methodology audit
- May 13 (Wed): "[Weekly Ship #042: What Was Working Got Written Down](https://pipermorgan.ai/shipping-news/weekly-ship-042-what-was-working-got-written-down)"
- May 14 (Thu): "[Same Failure, Six Agents, Ninety Minutes](https://pipermorgan.ai/blog/same-failure-six-agents-ninety-minutes)" — building narrative on April 19, six leadership-role workstream-review memos kicking off inside ten minutes on an Acela between Philly and DC, then a ninety-minute correction arc when an omnibus-log upload gap surfaced

The one held: "Permission to Pause," an insight originally scheduled May 10 (Sun), renamed May 9 to disambiguate from a March 22 narrative with the same title. Slot to be reassigned.

The publishing pipeline caught six pre-publication fabrications during a fact-scrub against archived 2025 session logs — second Code-era instance of pre-publication fact-verification as procedure. The shape is consistent: bracketed fact-check markers at draft time when a comparative or numeric claim can't be verified, resolved before handoff. Replicable as a draft-time check, not a heroic late catch.

**Voice discipline moved upstream.** Ship #042 came in at 1,252 words against the recent 1,800–2,500 range — about a third shorter, with no substance loss flagged. The four-category opacity sweep that used to be improvised at the editing stage is now a named draft-time step. Seven new voice-guide entries stacked for one editing-pass sweep — moves the publishing pipeline used to catch are now absorbed back into drafting.

## 📊 Governance & operations

**Metrics (May 8–14)**:

| Metric | Value |
|--------|-------|
| Build milestones closed | M2f (Groups A+B May 9, Group C May 11) + M2g-A and M2g-B (May 14) |
| Major backend ships | #921 (May 10), #857 (May 11), #1071 (May 11), #1021 (May 14), #1070 + #304 (May 13) |
| Pattern catalog grew | 67 → 69 patterns (P-067 stayed, P-068 + P-069 new) |
| Pattern catalog sweep entries | 6 anti-patterns indexed (May 9) |
| Pattern-067 family firings | 6 in 5 days |
| Commit-discipline memory entries pinned | 4 |
| Comment-Only-Close audit | 13 of 13 missed — 3-layer remediation same day |
| Publications shipped | 4 (1 held) |
| Ship #042 word count | ~1,252 (down ~32% from recent baseline) |

**Discipline that fires without its authors present.** The experience-design role was offline six of seven days in the window. The trust-and-relationships role (Head of Sapient Trust) the same. The cohort's cadence held. The methodology operated, the catches happened, the patterns got named. The single active day for each absent role produced concentrated substantive output — one role-health-check plus a team-structure refresh from the trust role, one mid-stream catch and a same-day branched rubric from the experience-design role.

**Skill spec versus skill firing — a watch-item across the cohort.** The thirteen-of-thirteen catch on closure discipline raises a structural question: which other skills are in the same shape? Written down, in the files, and not observed firing recently. The watch is now standing.

---

# 🎯 Coming up next week

The next milestone gate is in flight with the verification rubric branched cleanly. The publishing pipeline will start absorbing the seven stacked voice-guide additions into drafting practice. A separate forensics arc on the working-tree-path fragmentation family continues — the Pattern-067 parent meta-pattern is now doing the diagnostic work the cohort named it to do.

---

# 🚧 Blockers & asks

No current blockers. Several discovery-thread responses are queued on natural cadence. A cross-agent coordination conversation is convening to address structural failure modes that the methodology layer has named but the operational layer is still working through.

---

# 🔎 This week's learning pattern

## Codifying discipline does not enforce discipline

**Discovery**: When a team writes its discipline down, the shared vocabulary that results is real progress — but vocabulary alone leaves a gap that is structurally invisible from inside the cohort. Discipline that lives only in language can stop firing without anyone noticing.

**Example from this week**: The lead-developer role audited its own recent issue closures on May 13 — a hunch that something in the routine had slipped. The audit found thirteen closures. On every one, the description checkboxes had stayed unchecked. The skill that was supposed to catch this had been in the file for months. It hadn't fired. The remediation landed the same afternoon and had three layers: a memory entry (refreshing the vocabulary), a tooling issue for a lint (giving the discipline a mechanism that does not depend on remembering), and a standing floor written into the closure process itself (changing the sequence so the riskiest step runs when attention is sharpest).

**Why it matters**: The default move for teams maturing into shared methodology is to celebrate the vocabulary. Vocabulary is real progress. Vocabulary lets a cohort coordinate without re-deriving first principles every time. The risk is that the vocabulary's existence becomes a proxy signal for the discipline being practiced — and once that substitution sets in, no amount of refining the vocabulary closes the gap. The only way to spot the gap is to audit specific work and count. The only way to keep it closed is to give the discipline something to lean on besides reminded recall.

**Application beyond this week**: The shape generalizes. Any skill that has been written but has not been observed firing recently is a candidate. Any memory entry pinned weeks ago without a fresh application trail is a candidate. Any process step that everyone in the team can describe in conversation and nobody can point at a recent example of running is a candidate. The remediation pattern that worked here is the one to carry forward: vocabulary plus mechanism plus sequence. Each layer covers what the prior layer misses. None of them work alone.

**Related patterns**: The Pattern-067 family (issue-body-reality-mismatch) catches a related failure shape — implicit architectural claims that drift when undocumented. The Branch-or-Anchor methodology, ratified earlier this spring, governs when to extend an existing artifact versus branching to a new one. The three-layer remediation here applies the same logic at the discipline layer rather than the artifact layer.

---

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #043. Previous: [#042 "What Was Working Got Written Down"](https://pipermorgan.ai/shipping-news/weekly-ship-042-what-was-working-got-written-down/).

*P.S. Last week's Ship named the methodology getting written down. This week's Ship names what writing it down doesn't do on its own. Both are real. Both have to happen.*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of May 8–14, 2026 | Phase: MVP Build (M2d gate criteria landed, M2g in flight)**
