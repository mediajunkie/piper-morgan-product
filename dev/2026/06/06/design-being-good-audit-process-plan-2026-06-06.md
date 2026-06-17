# "Being Good" — Design-Discovery Audit + Process Plan (v0.1)

**Owner**: CXO (PM-watched track) | **Date**: 2026-06-06 | **Status**: DRAFT v0.1 — first-pass audit + proposed process, per the 2026-06-06 PM session.
**Parent frame**: `design-leadership-framing-web-ui-2026-06-03.md` v0.3 (the "not being bad" / "being good" model).

**What this is**: the audit that identifies which Piper experiences need the full design-discovery process (discovery → design research → sketch → iterate → prototype → test) rather than conform-to-paradigm execution — and triages how *deep* a process each needs. This is the PM-watched track.

---

## 0. Forensic-first — we are extending existing work, not starting from zero

Per PM (2026-06-06): *"forensic research and investigation of our own past plans and docs is as always part of our discovery process."* The audit's first move is to inventory what our own corpus already says. It says a great deal:

**The foundational discovery corpus (already exists):**
- **`piper-morgan-ux-foundations-and-open-questions.md`** (Nov 2025) — the load-bearing one. Already articulates the colleague metaphor, the Radar-O'Reilly proactive-presence pattern, 8 UX principles, and — critically — **Part IV "Open Questions"** (world model; transparency/auditability/legibility; dreaming/background; artifacts/outputs; canvas-vs-structure; trust-gradient mechanics; session-logging/journaling) and **Part V "Tensions requiring POV decisions"** (where-to-be-opinionated; **proactive-vs-reactive presence**; recognition-vs-articulation). **These open questions + tensions ARE a pre-articulated discovery backlog.**
- **`piper-morgan-ux-strategy-synthesis.md`** — the companion synthesis.
- **MUX surface docs** — Surfaces **2** (privacy/per-conversation controls), **4** (integration setup wizards), **7** (error/degraded/audit-read states) are **v0.2-locked** (substantial prior design); plus `insight-surfacing-rules`, `provenance-display-patterns`, `composting-experience-design`, `journal-architecture-spec`, `learning-visibility-spec`, `trust-learning-access-rules`, `contextual-hint-ux-spec-v1`, `multi-entry-ftux-exploration-v1`.
- **PDR-004** (experience philosophy), **PDR-005 §experience** (EC framework + identity-coherence), **Colleague Test rubric**, **empty-state-voice-guide-v1**, `views-catalog` / `objects-catalog` / `product-concept-model`.

**The headline finding**: most of the being-good *discovery questions are already named* (in the foundations doc's open-questions + tensions). So this track is less "discover from scratch" and more **resolve the already-articulated open questions + tensions through design, and complete the partially-designed MUX surfaces.** That's the "extending existing work" PM means.

## 1. The selection test (an experience earns the design-discovery process when all 3 hold)

1. **No dominant paradigm** for the Piper-specific part (the dividing line from v0.3).
2. **Core to the trusted-colleague / unique value** — not a nice-to-have.
3. **Genuine unknowns** — there's something to *discover*, not just execute.

## 2. Depth-triage — not everything that qualifies needs the full loop

| Tier | Process depth | When |
|---|---|---|
| **Light** | Forensic-mine existing design + sketch + prototype + Colleague-Test | Substantial prior design already exists (e.g. v0.2-locked surfaces); mostly completion/realization |
| **Medium** | + design research (industry patterns, our own usage) + iteration | Real open questions but bounded; some prior thinking |
| **Heavy** | + structured discovery + dogfood/user testing | Genuinely novel, high trust-stakes, the right shape is unknown |

## 3. The process (right-sized; honest about our user reality)

Forensic research (mine our own docs) → discovery (resolve the named open questions) → design research (industry + our own usage) → sketch → iterate → prototype → **test** → ship behind the **#683 two-layer DoD** gate.

**Honest note on "user testing"**: at this stage that's realistically **dogfooding + PM-as-primary-user + the cohort**, not formal user research — we don't yet have a user base. Right-size now; graduate to real user testing when there is one. Don't promise rigor we can't run.

**Bounding discipline (per v0.3)**: every being-good bet carries a **hypothesis** (what relevant thing it surfaces the user would otherwise miss) + a **landing test** (Colleague Test). No "cooler?" without a why, a for-whom, and a how-we-know.

## 4. First-pass run over the candidates

Format per item: *existing thinking → conform-part vs discover-part → open discovery questions → tier*.

### History panel *(PM example — straddles)*
- **Existing**: journaling/session-logging open question (foundations Part IV); `journal-architecture-spec`; `composting-experience-design`; canvas-vs-structure tension; Insight Journal (#1031, already built but isolated per #1142).
- **Conform**: "list of past conversations + search" is a solved paradigm → *not-being-bad*.
- **Discover**: history that surfaces *what Piper remembers about you and your work* and *resurfaces the relevant thing* — memory-as-history, no paradigm, core to value.
- **Open Qs**: scratch vs. lifelong history (foundations names this); what resurfaces, when, why; how it relates to "composting."
- **Tier**: Medium.

### Notifications / proactive presence *(PM example — pure being-good)*
- **Existing**: **foundations Part V "Proactive vs Reactive Presence"** — the observation→offer→action spectrum, the self-threat research, the Radar-O'Reilly pattern. Already a named tension with research grounding.
- **Conform**: ~none — there's no good paradigm for *a trusted colleague proactively surfacing relevance without being annoying.*
- **Discover**: where on the observe/offer/act spectrum by default; how it evolves with the trust gradient; cross-surface behavior; the trust model.
- **Open Qs**: all of Part V's proactive-presence decision, unresolved.
- **Tier**: **Heavy** (high trust-stakes, genuinely novel).

### Memory surfacing *(what Piper knows about you, made visible)*
- **Existing**: World-model open question (Part IV); `learning-visibility-spec`; `trust-learning-access-rules`; transparency-vs-cognitive-load tension; industry memory patterns (Part VI Q4).
- **Discover**: how much is visible by default vs. on request (the transparency tension); how the user inspects/corrects what Piper "knows."
- **Tier**: Medium–Heavy.

### Lifecycle indicators / work-state *(the Standup surface, #704)*
- **Existing**: STATUS canonical query; trust-gradient; the lifecycle-indicator + experience-phrase architecture (landed but not rendering, per #1142).
- **Conform**: basic status display has conventions → partly *not-being-bad*.
- **Discover**: what a *trusted-colleague work-state* feels like vs. a dashboard (foundations explicitly excludes "dashboard you read").
- **Tier**: Medium.

### Integration-awareness *(what's connected, what Piper can see)*
- **Existing**: **Surface 4 (integration setup wizards) is v0.2-locked** — substantial prior design; "meet users where they are" principle.
- **Discover**: lighter — setup is largely designed; the *ambient awareness* surfacing (what Piper can currently see) may need a light pass.
- **Tier**: **Light** (leverage Surface 4).

### Trust / audit transparency *(why Piper did X)*
- **Existing**: **Surface 7 (audit-read states) is v0.2-locked** + ADR-063; the Transparency/Auditability/Legibility open question (Part IV); `provenance-display-patterns`.
- **Discover**: lighter — the read-surface is designed; the how-much-by-default tension remains.
- **Tier**: **Light–Medium** (leverage Surface 7).

### Type 2 dreaming — the "what I'm prepared for" surface *(added 2026-06-06; cross-tracked in #1166)*
- **Existing**: **methodology-27** (canonical framing — threat-rehearsal, Revonsuo-grounded, PM-side-only); PA Dreams research (Phase 1–3); Arch architectural review; foundations Part IV "Dreaming/Background Processing." PM: *"a true innovation worth at least exploring further."*
- **Conform**: ~none — no external operational equivalent exists (confirmed vs. Anthropic's Dreams API).
- **Discover**: the user-facing surfacing of threat-rehearsal walkthroughs / risk surfaces — how much surfaces, when, how it avoids the over-anxious failure mode (methodology-27 names it), trust-gradient relationship.
- **Cross-cutting**: also needs PPM (roadmap-fit) + Arch (the large undefined design surface) — **#1166** is the three-way convergence home. CXO owns the experience-surface lens within it.
- **Tier**: Heavy (genuinely novel; but gated on the #1166 roadmap-fit decision before deep discovery).

### On-the-fly generative GUIs *(PM's "can we be cooler?")*
- **Existing**: "generative, not consumptive" principle; canvas-vs-structure tension.
- **Status**: **Parked — explicitly later.** Per v0.3 + PM: earn it on top of text-chat-that-works. Genuinely novel, heavy, but *sequenced after* the floor.
- **Tier**: Heavy / **deferred**.

## 5. What this first pass tells us (the "few things or more things" answer)

**~6 active candidates + 1 deferred.** But the load is uneven, and that's the useful finding:
- **3 are Light** (integration-awareness, trust/audit) **or partly-conform** (lifecycle, history's list-part) — because **prior design already exists** (Surfaces 4/7 v0.2-locked; lifecycle architecture built). These are mostly *completion/realization*, not net-new discovery.
- **2–3 are genuinely Heavy** (proactive presence/notifications; memory surfacing; on-the-fly GUIs) — real, novel discovery. *And even these have their questions pre-named* in the foundations doc.

So: **it's a moderate set, front-loaded by existing work, with a small number of genuinely-deep discovery threads.** Not overwhelming. The deep ones (especially proactive presence) are where PM's watch matters most.

## 6. Output — the being-good design backlog

Each active candidate becomes a backlog item with: existing-design pointers · conform-part split off to the not-being-bad track · open discovery questions · tier · hypothesis + landing test. PM watches this backlog; we run items at their tier, deliberately paced, gated by the two-layer DoD.

## 7. Proposed first move

Given the forensic finding (questions pre-named; surfaces partly designed), the highest-leverage first being-good thread is **proactive presence / notifications** — it's Heavy, it's pure unique-value, its discovery questions are already framed in foundations Part V, and it cuts across every surface (so resolving it informs the others). Recommend it as the first deep discovery thread, *after* the not-being-bad floor is moving in parallel.

---

*Draft v0.1 — CXO, 2026-06-06. For PM review (this is the PM-watched track). Next on PM's nod: convert the active candidates into backlog items + open the proactive-presence discovery thread.*
