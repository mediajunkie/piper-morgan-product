# Architectural Review 2026 — Discovery Plan

**Version**: v0.1 (draft for PM refinement — not yet dispatched)
**Authors**: Chief Architect, from PM+Arch kickoff conversation 2026-08-29
**Status**: DRAFT — awaiting PM review before any agent is dispatched

---

## Charter

PM's framing, 2026-08-29: what's missing is *"a top-down strong POV from leadership on the essence
of Piper Morgan's architecture (philosophy, design, plans, current status) today, as opposed to
circa July 2025 +/- a series of changes."* This review exists to produce that POV — with
reorientation and realignment to whatever extent the findings warrant.

**Context the review must hold honestly**: the project leapt from *"xian wants to make an assistant
he can truly own"* to *"enterprise-grade multi-tenant SaaS"* through a series of decisions made
without an explicit bet-shaped gate (PM's own retrospective framing). LLMs default to
industry-standard architecture; absent a deliberate counter-pressure, we architected like the median
Stack Overflow answer would. Some of that was right. Some of it produced brittleness and scope
inflation. Discovery's job is to tell those apart **with evidence, not vibes** — drift vs.
deliberate variance vs. correction, per era.

**The organizing question** (PM's phrase, adopted as the review's spine): *which parts are essential
for us to say Piper Morgan is "happening"?* Everything discovered gets classified against it:
**essence / extension / experiment / superseded / dead**.

## Scope statement (what this review is NOT)

Per my standing state-the-scope rule — naming what a reader would most plausibly assume is covered:

- **Not a redesign of the BYOC track.** PA+PM are steering its convergence with the post-beta
  roadmap first; this review informs that work, doesn't preempt it.
- **Not decomposition execution.** PM and Arch agreed 08-29: molecules get cut along essence seams
  *after* the essence document exists, not along today's accidental module boundaries.
- **Not a freeze on MVP work.** The review runs alongside current sprint work, not as a gate on it.
- **Not a referendum on any individual's past decisions.** The blame is shared freely (PM's words)
  and the review's currency is evidence about *decisions*, never performance of *people or agents*.

---

## The four legs of discovery

Run in parallel. Each leg's researchers work **blind to the other legs' findings** until synthesis
(see Method Disciplines below for why).

### Leg A — Forensic history (how we got here)

**Corpus**: the full ADR trail (~80 ADRs + amendments), PDRs, `decisions.log`, milestone/sweep
history, session-log record where it captures architectural pivots, and the omnibus archive.

**Three agents, three deliberately different framings** (not one prompt template three times):

- **A1 — the decisions trail, read forward.** Walk the ADR/PDR corpus chronologically. For each
  era: what was the operative vision, what were its governing assumptions, and when did they
  change? Classify every major shift: **drift** (unchosen accumulation) / **deliberate variance**
  (chosen, recorded, reasoned) / **correction** (fixing a recognized mistake). The eras themselves
  are a finding — name them.
- **A2 — the incident record, read backward.** Ignore the ADRs. Read only issues, incident docs,
  and forensics writeups (e.g. the summarize-intent forensics, the spatial-intelligence review, the
  #1481/#1484 Slack hold, the merge-drop incidents). What actually broke, and what does each break
  reveal about where the *implicit* architecture disagreed with the documented one? Breaks are
  ground truth about load-bearing walls.
- **A3 — the scope inflections, traced specifically.** Find the concrete decisions that constituted
  the own-assistant → multi-tenant-SaaS leap. For each: what did it cost (in architecture carried,
  complexity added, optionality foreclosed), what did it buy, and — the question nobody asks in the
  moment — *was the buyer ever identified?* (Enterprise-grade assumptions purchased for a customer
  who doesn't exist yet are the definition of speculative complexity.)

**Deliverables**: era timeline with governing assumptions per era; change taxonomy
(drift/deliberate/correction) with citations; inventory of speculative-complexity purchases with
their present-day carrying cost.

### Leg B — Live-state census (where "here" actually is)

**Method**: code-first, **docs-blind** — the agents in this leg read the codebase and runtime
surfaces, explicitly instructed NOT to consult ADRs or architecture docs (the comparison between
their findings and the docs happens at synthesis, and the deltas are the finding).

- Entry-point tracing from the real surfaces: `main.py`, web routes, the MCP surface, the Slack
  path (held), CLI. What is *reachable* from a real user action?
- `scripts/reachability-map.py` runs (existing tooling from the spatial review — extend if needed).
- Classification of every module: **load-bearing / extension / experiment / shim / dead /
  75%-pattern** — with per-module evidence (callers, tests, config gates).
- Known partial inputs to verify rather than trust: the spatial-intelligence layer map (08-scoped,
  all 11 modules ruled disposed but disposal unexecuted), `services/intent_service/unwired_writes.py`
  (the honest-gaps inventory), the two-router migration state (legacy classifier vs. Inversion —
  which operations ride which rail today), the connector reality check (which adapters make real
  MCP calls vs. shim over REST — PA's 08-27 finding, extend to all four).

**Deliverable**: a live-state map — what the system actually is today, one classification per
module, every classification cited. This is the document Leg D's paper-rebuild gets compared
against.

### Leg C — External comparables (what the field proves is possible/unnecessary)

**Four categories, researched by separate agents with separate framings** — not one "survey the
field" pass:

- **C1 — Personal AI assistants / agentic products** (open-source and commercial): what is their
  minimal architectural spine? What did they *decline* to build? How fast did they reach real
  users, and what did the architecture look like at first-user?
- **C2 — Own-your-own-knowledge harnesses** (personal knowledge tools with LLM layers): how do they
  handle the data-ownership/portability question Piper's original vision centered on?
- **C3 — PM-specific agents/copilots** (the direct competitive category): what do they treat as the
  irreducible product core?
- **C4 — Connector-layering patterns in LLM apps**: host-mediated connectors (the LLM client's own
  integrations relaying to the app) vs. backend-owned connectors (the app holding its own grants) vs.
  hybrid. This one directly feeds the review's first live test case (below).
- **C5 — Dialog (Chris Ivester)**: pending Granola transcripts or PM paste-in. PM flags this as
  informative precisely because it's *not* necessarily succeeding while taking the
  ship-early-find-the-easier-path approach PM now wishes he'd held onto — which makes it evidence
  about the approach's real trade-offs, not a success story to copy.

**Per category**: what's their minimal shippable spine; what did they cut; how do they get users
soon. **Deliverable**: comparables brief, one section per category, each ending with "what this
proves is possible" and "what this proves is unnecessary."

### Leg D — The paper rebuild test (cheap, early, falsifiable)

The delete-the-codebase thought experiment, run as a paper exercise now rather than a real rebuild
later. **This is a falsifiable test of documentation sufficiency** — it converts "our docs have
drifted" from a feeling into a list.

**Protocol**:
1. **Curation step (Arch, with PM review)**: assemble the doc set a fresh team would get — specs,
   ADRs judged current, the glossary, PIPER.md, key design docs. *The curation itself is a
   finding*: what we reach for reveals what we believe describes the system.
2. **Fresh agent, no repo access beyond the curated set** (different model/provider if practical;
   at minimum a clean context): asked to produce a build plan where **one working feature ships
   end-to-end to real users before the next begins** — PM's ship-early principle encoded as the
   plan's hard constraint, not a preference.
3. **Required outputs**: the plan itself; **every question the docs could not answer** (the drift
   measure); every place it had to guess and what it guessed (the ambiguity measure).
4. **Analysis at synthesis**: the unanswerable-questions list prioritizes step 7's doc updates; the
   shape of its plan vs. our actual build history is the "median technical architect" check — if a
   fresh agent with our docs plans the same over-engineering, the docs carry the bias; if it plans
   leaner, the accretion was ours.

**Run early, in parallel with A–C** — its output feeds synthesis like any other leg.

---

## Method disciplines (each one paid for by a real cohort incident)

1. **Independence requires different methods, not different agents.** Five seats once converged on
   the same wrong answer because they inherited the same unexamined probe default. Hence: every
   parallel agent in this plan gets a *structurally different* framing, and no shared prompt
   template carries a hidden assumption into all of them.
2. **Blind until synthesis.** No discovery agent sees another's findings. Convergence between
   independently-derived findings is evidence; convergence between agents reading each other is
   contamination.
3. **Every claim cited.** File, commit, ADR, or issue — per the evidence-required standing rule. A
   finding without a citation doesn't enter the synthesis.
4. **Name the layer, state the denominator.** Every coverage claim in every deliverable says what
   it covered and what it didn't. "All modules classified" must mean *all*, with the count.
5. **Arch writes the synthesis personally.** Delegating reading is fine; delegating judgment is
   not. The synthesis report and the essence document are authored, not assembled.

---

## First live test case: the connector-layering question

PM+PA's recent work surfaced the question concretely: a user in an LLM host running Piper skills
against a Piper MCP could get connector data via (at least) **(a)** Piper's backend holding its own
connector grants, **(b)** the host LLM's own connectors relaying data into Piper, or **(c)** hybrid
per-connector splits. This touches PDR-006, ADR-070, the BYOC track, the Slack descope, and the
08-28 GitHub-adapter ruling — five live threads, one seam.

**The review's framework must answer this cleanly, or the framework isn't done.** It's the
acceptance test for the essence document: essence should say which of those layers is *Piper being
Piper* and which is deployment topology.

---

## Deliverables (numbered, so nothing silently drops)

1. Era timeline + change taxonomy (Leg A)
2. Live-state map, every module classified with evidence (Leg B)
3. Comparables brief (Leg C)
4. Paper-rebuild plan + unanswerable-questions list (Leg D)
5. **Arch synthesis report** (Arch-authored, cited, cross-leg)
6. **"Essence of Piper Morgan" v0.1** — the POV document; the review's central artifact
7. Reorientation plan (if warranted): keep/eliminate/change, with owners, order, and definitions of
   done — drafted with PM, then socialized (CXO + PPM as the directional trifecta first, then full
   leadership), feedback synthesized, hard calls made by PM

## Sequencing

- **Phase 0 (now)**: PM refines this plan. Granola/Dialog material lands (or is pasted). Doc-set
  curation for Leg D happens here — it needs Arch judgment + PM's eye, not an agent.
- **Phase 1**: dispatch all four legs in parallel. Given duty-cycle cadence and agent turnaround,
  findings should land within a few days, not weeks.
- **Phase 2**: Arch synthesis (deliverable 5).
- **Phase 3**: PM+Arch discussion, as many rounds as needed.
- **Phase 4**: keep/eliminate/change decisions → Essence v0.1 (deliverable 6).
- **Phase 5–7**: reorientation planning → socialization → architecture-doc updates riding the
  decisions (per the two-surface recording rule: ADR-worthy decisions get ADRs; the rest goes to
  decisions.log).

## Success criteria for discovery (not the whole review)

- Every module in the live-state map carries a classification and a citation. Denominator stated.
- Every architectural era is named with its governing assumptions and its ending trigger.
- The connector-layering question is answerable from the framework without a new investigation.
- The paper-rebuild's unanswerable-questions list exists and is prioritized.
- PM can hand the essence document to a smart stranger and they know what Piper Morgan *is* —
  not its history, not its aspirations: what it is.

---

*Draft v0.1 — Chief Architect, 2026-08-29. Refinements welcome; nothing dispatches until PM has
shaped this.*
