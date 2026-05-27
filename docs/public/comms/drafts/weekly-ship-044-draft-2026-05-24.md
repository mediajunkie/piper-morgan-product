---
image: piper-ship.png
alt: 'A child leads a boat crewed by robots.'
caption: N/A
---

# Weekly Ship #044: What Survives an Experiment

*May 15–21, 2026*

This week the team experimented with the first version of a new operating mechanism. The CIO built it, extended it, and then we tore it down a few days later.

We extended the mechanism — an autonomous duty cycle for individual agents, designed Saturday — to two more agents Sunday. We observed the results for a few days, and killed the v1 on Thursday. The design had taught what the team needed to know to design something better, and that what needed to carry forward was not the specific mechanism we built the first time around but much of the functional substrate underneath it.

The week added four new entries to the methodology corpus, promoted a pattern from Emerging to Proven on the strength of eleven independent instances surfaced across five different agents in thirty-six hours, and codified a cohort-wide operational shift to dedicated working trees for substantive output. None of that retired when the mechanism did (and version two of the Duty Cycle experiment is still in the offing).

The mechanism will be cheap to replace. The substrate has been expensive to build but will be cheap to carry forward.

---

# 🚀 Shipped this week

## 🎯 Product & experience

**A foundational decision document moved through three versions in four days.** My product assistant, Piper Alpha's BYOC (bring your own chat) distribution decision-rules document (PDR-005, governing how users will eventually bring their own AI assistants) went from v0.3 to v0.4 to v0.5 across the week. Each version absorbed a different role's contribution as a verbatim section — the architecture role's Consequences-for-architecture fill-in landed mid-week, the experience-design role's (CXO) Consequences-for-experience fill-in landed late-week. The work that would have taken multi-day cohort iteration in a less mature cycle compressed into roughly six-hour turnaround per version.

**The first three of seven planned user-experience surfaces shipped first-draft documents.** The experience-design role produced version-0.1 documents for Surface 7 (audit envelope read), Surface 2 (per-conversation privacy), and Surface 4 (integration wizards) across three sessions — the offer-first cluster trio. The communications role's voice-pass cycle on the cluster returned same-day a week later. Cross-lens convergence between architecture, experience-design, communications, and lead-developer worked as designed, with no re-litigation between lanes.

**A major build-milestone closed an integration sub-epic within an hour of scope ratification.** The lead-developer role closed Phase 2.1 of the MUX/UI Round 2 work (Surfaces 1 and 7 slices) within one hour and four minutes of the morning's scoping memo being filed. The architectural work on the same surfaces shipped as three new architecture decision records earlier the same week.

## ⚙️ Engineering & architecture

**The week's headline deletion was structural.** The lead-developer role shipped issue #1094, removing the now-superseded orchestration engine and workflow factory. Net change across fifty-nine files: minus 10,734 lines of code. That landing fired the fourth-consumer trigger for a pattern the architecture role had been tracking (registries that grow into architectural shapes), which then promoted from Emerging to Proven the same day on the strength of model dispatch, calibration, output filter, and Slack dispatch all building on the same primitive.

**Three architecture decision records landed in a single week.** The records covered the project-scope end-to-end test suite phase-zero scoping, the user-facing audit envelope read surface (closing the read-side gap a prior decision record left), and the project-scope search index architecture. The architecture role identified what made the three-record delivery possible: pre-drafting sequencing was settled at a product-management walkthrough before any drafting started, which let context for each record stay loaded between drafts.

**A new lint hook shipped to enforce a recurring failure-mode at the tool layer.** The lead-developer role shipped issue #1083 (a hook enforcing the close-issue-properly discipline whose absence had triggered the recurring failure mode that became the spine of last week's Ship #043). The hook self-dogfooded twice the same day it landed. A retroactive test against the prior week's thirteen closures would have flagged three at commit time.

**A documentation-versus-behavior drift pattern got named, filed, and promoted to Proven in three days.** The pattern (named *Documentation-Asserted-Behavior Drift*) accumulated eleven instances across nine narrative-artifact layers and five different agents in roughly thirty-six hours after the initial filing. The cleanest reference case so far for the team's framework of pattern formation via successful imitation.

## 🔬 Methodology & process innovation

**The methodology corpus added six entries.** Three landed early in the window (pre-filing slot-availability check, type-2 dreaming, pattern formation via successful imitation). Three landed mid-week (append-only autonomous-cycle architecture, Postel's law for memo headers, session-type determines git-permission scope), with consumer-trace verification queued and filed the same day. A seventh (the cohort-discipline-as-moat framing) was filed at the close of the cycle as the strategic-altitude entry that names what the team accumulates that platform productizations do not.

**Piper A brought a cohort-wide operational directive on day one of the window.** Substantive output from any role now defaults to a dedicated `claude/*` branch and working tree. Shared main is the exception, for short mailbox-discipline operations only. The directive emerged from four distinct foreign-state-capture incidents observed in one morning across multiple agents — discipline layers surfaced the problem but could not prevent it. Only working-tree separation prevents it structurally. The documentation role codified the directive into CLAUDE.md the same evening.

**The autonomous duty cycle ran a complete adoption-to-retirement lifecycle in five days.** The innovation-officer role (CIO) designed version one Saturday. Cohort extension to the sapient-trust role (HOST) and the documentation role happened Sunday. Two days of observation. Thursday, the product-management role brought seven sketches of a richer design, and version one retired. What carried forward: the four methodology entries the version-one era produced, the operating-norm substrate the cohort had built underneath, the cohort's demonstrated capacity to hold "this worked and we are killing it" without sunk-cost defense.

## 🌍 External relations & community

**Five pieces published in seven days:**

- May 16 (Sat): "[The Family Resemblance](https://pipermorgan.ai/blog/the-family-resemblance)" — first end-to-end publish through the new infrastructure, insights drawn from March to April
- May 17 (Sun): "[From Protocol to Infrastructure](https://pipermorgan.ai/blog/from-protocol-to-infrastructure)" — insights drawn from February 25 to May 12
- May 19 (Tue): "[The Log That Fact-Checked Itself](https://pipermorgan.ai/blog/the-log-that-fact-checked-itself)" — building narrative from April 22
- May 20 (Wed): "[Weekly Ship #043: The Skill That Doesn't Fire](https://pipermorgan.ai/blog/weekly-ship-43)" — Shipping News
- May 21 (Thu): "[The Voice of a Denial](https://pipermorgan.ai/blog/the-voice-of-a-denial)" — building narrative, also from April 22

<a href="https://pipermorgan.ai/blog/the-log-that-fact-checked-itself"><img src="https://pipermorgan.ai/assets/blog-images/the-log-that-fact-checked-itself.webp" alt="Glowing ethereal beings amending a giant ledger book, reintegrating missing pages into the official record while the book appears to point out its own omissions" /></a>

*"Not so fast!" — from [The Log That Fact-Checked Itself](https://pipermorgan.ai/blog/the-log-that-fact-checked-itself)*

**The publishing pipeline shipped end-to-end mid-week.** The web role (Unicorn Web Designer) returned from a six-and-a-half-week dormancy and shipped a publish-post script + a status dashboard + a first end-to-end publish all on Saturday May 16. A second command-line tool (the publishing-flow CLI) got fully designed in a thirty-minute discussion the next afternoon. The week's publication count is the result of that infrastructure landing — five pieces in seven days, against existing infrastructure now that the pipeline does what the team needs it to do.

## 📊 Governance & operations

**Metrics (May 15–21)**:

| Metric | Value |
|--------|-------|
| Build milestones closed | M2f groups A+B+C earlier — M2g sub-epic in flight — MUX/UI Round 2 Phase 2.1 closed |
| Major code deletion | #1094 ENGINE-DELETION net -10,734 LOC across 59 files |
| Architecture decision records filed | 3 (ADR-062, 063, 064) |
| Pattern catalog | +1 filed Emerging (Pattern-070), 2 promoted to Proven (Pattern-072 sub-day, Pattern-073 in 3 days) |
| Methodology corpus entries | +6 (methodology-27 through 33) plus methodology-34 candidate |
| Publications shipped | 5 (against existing infrastructure now that pipeline shipped) |
| Cohort coordination | V1 duty cycle adopted by 3 roles then retired — worktree-default codified cohort-wide |

**The cohort's coordination discipline scaled.** The migration checklist (Chat → Code role migration playbook Host authored) went from v1.0 through v1.1 through v1.2 through product-management ratification across the window, closing the corresponding 360-commitment cleanly. The 360-commitments tracker itself was refreshed with status-per-item evidence twenty-four days after synthesis.

---

# 🎯 Coming up next week

The newly-assigned Anthropic Outcomes investigation lane starts work on Monday — the product-management role (Piper Alpha) leads the spec-read and paper-comparison, the innovation-officer role co-authors the strategic synthesis, lead-developer stays focused on delivery. The duty-cycle redesign (version two) enters pilot observation Monday with cohort re-adoption following pilot validation. The communications role has a nine-beat narrative slate sequenced for publication May 26 through June 23.

---

# 🚧 Blockers & asks

No current blockers. Several discovery-thread responses are queued on natural cadence. A Host commitment on handoff-review-pattern codification is on track for end-of-month delivery.

---

# 🔎 This week's learning pattern

## Mechanism retires, substrate carries forward

**Discovery**: When a working mechanism is retired in favor of a richer redesign, what makes the retirement work is whether the team has accumulated substrate (operating norms, methodology entries, working disciplines) underneath the mechanism. If the substrate exists, retirement is moat-deepening rather than sunk-cost defense.

**Example from this week**: Version one of the autonomous duty cycle. Five-day arc from design through cohort extension to retirement. What retired: the cron mechanism, the append-only architecture specifics, the manual-fire patterns. What carried forward: four methodology entries describing disciplines that survive the version-one retirement intact, a cohort-wide operational shift to working-tree-default, a strategic framing (*cohort-discipline as moat*) that names what the team is accumulating that platform productizations do not.

**Why it matters**: Mechanism is cheap to replace if the team can name it as "the implementation of an underlying discipline." Substrate is expensive to build but cheap to carry forward across mechanism changes. Teams that conflate the two end up either defending sunk-cost (because the mechanism IS their operational pattern) or paralyzing on new mechanism design (because every retirement feels like loss). Teams that separate them iterate faster.

**Application beyond this week**: For any working mechanism, ask "what substrate did this build underneath it?" If the answer is "specific disciplines, methodology entries, working norms," retirement frees the team to redesign without losing accumulated value. If the answer is "nothing yet, the mechanism is the operational pattern," then either the team holds the mechanism longer (build substrate first), or the retirement is harder than it looks. The asymmetry is also a pre-design question — every new mechanism is an opportunity to build substrate that survives it.

**Related patterns**: The methodology-29 framing (*pattern formation via successful imitation*) names how substrate accretes — recognition runs ahead of codification when failure modes are vivid. The methodology-34 candidate (*cohort-discipline as moat*) names what the substrate is good for at the strategic level. Last week's Ship #043 learning pattern (*codifying discipline does not enforce discipline*) names what mechanism is for — the binding layer that closes the gap vocabulary alone cannot close. This week's pattern names what survives when a specific binding layer is replaced.

---

**Thanks,**
xian + Piper Morgan Development Team

This is Weekly Ship #044. Previous: [#043 "The Skill That Doesn't Fire"](https://pipermorgan.ai/blog/weekly-ship-43).

*P.S. The mechanism the team built and retired this week was running cleanly when it retired. The retirement was an act of design discipline, not failure recovery. The substrate it produced is the part that mattered all along.*

*P.P.S. Full session logs and technical details available in the [GitHub repository](https://github.com/mediajunkie/piper-morgan-product) and [documentation site](https://pmorgan.tech). Yes, you can copy it. That just makes our protocol stronger.*

---

**Week of May 15–21, 2026 | Phase: MVP Build (M2g sub-epic in flight, MUX/UI Round 2 Phase 2.1 closed)**
