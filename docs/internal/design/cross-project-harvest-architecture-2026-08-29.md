# Cross-project harvest architecture

**Status**: 🟡 DESIGN — PM-directed, decided in conversation 2026-08-29. One open question (§6) that
PM raised and that this document argues should be answered before anyone builds.
**Author**: Exec (Chief of Staff), from PM's design in conversation
**Scope**: cross-project, not Piper-Morgan-local. Piper Morgan is one of the harvested projects.

---

## 1. The problem, in PM's own diagnosis

> *"The daily cross-intelligence briefing newsletter is conversational and might spark thoughts in the
> moment but has no hooks or triggers and does not accumulate as a knowledge base."*

That is the whole finding. The briefing is **thread mode** — signed, chronological, conversational,
high salience in the moment, zero durability. What is missing is not an artifact. It is the
**refactoring of thread mode into document mode**, which in wiki practice was a deliberate, recurring,
human act rather than a byproduct.

PM: *"agreed the harvest is missing."*

**The goal**, in PM's words: *"disseminate cross-project insights and wisdom and standards in an
actionable way"* — so that new projects, or existing projects venturing into new areas, start from
synthesized findings instead of rediscovering the same patterns.

## 2. The evidence that the hard part is hooks, not size

We have already run the document-mode experiment inside Piper Morgan and it went inert.

`docs/internal/development/methodology-core/` is exactly the artifact this design describes, at
single-project scale: accumulated, curated, cross-cutting wisdom. HOST measured it 2026-04-27 and
found **20 of 22 documents zero-cited** — *"a corpus-coherence problem, not a refresh problem."* It
now holds **64 files**.

⚠️ **The design consequence, which is easy to get backwards**: a small pilot of a document-mode
artifact **tests the wrong variable**. If you build a small wiki and nobody reads it, you have learned
nothing about whether a large one would work, because the failure was the absent hook rather than the
size. **A pilot must vary the hook and hold the content roughly constant.**

The falsifiable question a pilot should answer: *what made someone reach for this, and did it reach
them at the moment they needed it?*

## 3. Structure — two tiers

PM's design, recorded as given.

### Tier 1 — per-project harvesters

A harvester per project, on a regular cadence, with input from other roles.

| Project | Harvester |
|---|---|
| Piper Morgan | CIO |
| Klatch | Calliope |
| One Job | Coral |
| Design in Product | *see §6 — PM proposed Janus* |

★ **Tier 1 is a NEW OUTPUT SURFACE ON EXISTING WORK, not a new standing obligation.** PM asked
explicitly that this be stated rather than left implicit.

For CIO the point is concrete: the methodology corpus, the pattern catalog, and the innovation
backlog **already are** the Piper Morgan harvest. Nothing about the harvesting is new. What does not
exist today is the **export** — a nomination channel pointing outward. Framing this as new scope would
attach a new cadence to a role that already carries one, which is precisely the shape of commitment
this project has watched lapse (see §5).

### Tier 2 — cross-project curation

Rolls up, synthesizes, and **nominates** selected project insights for adoption as cross-project
standards.

**What a "standard" is**, in PM's framing and this is the load-bearing sentence:

> *"at least do this [defined in terms of outcomes] if you don't have something better already."*

A **floor**, not a mandate. **Outcome-defined**, not mechanism-defined. **Locally overridable** by
anything demonstrably better.

## 4. Four constraints on the design

### 4.1 The nomination bar: recurrence across *projects*

PM agreed. We already own the machinery — the Emerging → Proven pattern ladder with a recurrence
requirement. CIO promoted Pattern-069 on exactly that basis this month and declined to file others
sitting on a single instance.

At the cross-project tier the criterion substitutes one word: **recurrence across projects**, not
across mechanisms. Without it you standardize one project's local conditions and every adopting
project inherits constraints that were never theirs.

### 4.2 Outcomes, not mechanisms — and PM's second reason for it

PM: *"100% outcome-based needed, if only for product sense, but also… to make the goals, rules,
triggers agnostic in terms of implementation."*

The implementation-agnosticism argument is the stronger one for a cross-project standard, because the
projects genuinely differ in stack and shape. In-house evidence: the rules that stuck here are
outcome-shaped ("state the denominator," "verify at the moment of use"); the mechanism-shaped ones
needed re-litigating every time they met a case their author had not imagined.

**Failure mode to avoid**: if Tier 2 writes procedures rather than floors, the standards get resented
and routed around, and the routing-around will be correct.

### 4.3 Tier 2 fires on upstream push, not a pull cadence

Tier 2 is **the tier most likely to go inert** — it is furthest from anyone's daily work, which is the
exact profile of the methodology-core failure. Tier 1 harvesters have a natural trigger already (their
duty cycle, their review cadence, work they are doing anyway). Tier 2 has none by default.

So: **Tier 2's pass fires when a Tier-1 harvester nominates.** Demand-driven rather than scheduled.
This also makes volume self-limiting.

PM: *"Yes firing on upstream push is a good catch. Exactly the sort of thing we might only have
realized the need for after repeated failure."*

### 4.4 Every entry carries a trigger

Ratified the same morning as a **standing, corpus-wide requirement**, well beyond this design:

> *"any ADR, any new methodology, any pattern documented has to be equipped with an actual trigger or
> it's academic."* — PM, 2026-08-29

And PM ruled that **existing entries get retrofitted**, with a second benefit named: *"this gives us a
chance to review the efficacy of each methodology."*

★ **This converts the methodology-core disposition from a judgment call on 64 documents into a
largely mechanical pass** — the disposition criterion becomes *does this carry a trigger*, and a
zero-cited document is close to definitionally one that nothing fires. The retrofit and the
disposition are the same work.

## 5. Why this design keeps referring to things that lapsed

Three in-house failures shaped every constraint above, and they are the same failure:

1. **20 of 22 methodology docs zero-cited** — a corpus with no hooks.
2. **CXO's floor/ethics watch went four Ship windows unattested** — diagnosed 2026-08-28 as *"a
   standing responsibility with NO TRIGGER, NO METHOD, and NO DENOMINATOR is an intention wearing a
   commitment's costume."* It lost every prioritization contest to work that named an artifact.
3. **A documented gotcha fired twice anyway** — GitHub's auto-close keyword behavior is described
   correctly in `CLAUDE.md` and still phantom-closed a live issue in July and again on 2026-08-28.
   **Prose in a corpus is not a control.**

The generalization: **a document can be present, correct, current, and inert.** Everything in this
project that actually gets used at the moment it is needed is trigger-shaped — the progressive-loading
table, the skills, the session-start hook, `duty-cycle-tick`'s numbered steps.

## 6. ⚠️ OPEN — the Tier-2 owner, and a charter discrepancy PM should resolve

PM proposed (as a question, not a ruling): **Janus rolls up DxP-specific practices** — *"they oversee
the site and are the general contractor, so to speak, even when Pard is building out"* — **and Themis
focuses on cross-project guidelines curation.**

That split correctly fixes a real problem: it gives Tier 2 one job instead of two differently-shaped
ones. But **as against the documented charters it appears inverted**, and the discrepancy is worth a
deliberate ruling rather than a silent resolution.

Per `~/Development/designinproduct/CLAUDE.md`:

| Agent | Documented charter |
|---|---|
| **Janus** | *"Curator of designinproduct.com — operational stewardship of the website, gallery, and **cross-pollination hub**."* Explicitly *"the **consumer of sibling-project work** and curator of the public face."* |
| **Themis** | *"**Business advisor** for Design in Product — counsel on the project/revenue portfolio as Xian shifts into consulting mode."* Explicitly *"the **strategist** for Xian's business mix."* |

Read against those: **Janus is already chartered as the cross-pollination hub and the consumer of
sibling-project work** — which is Tier 2's job almost verbatim. And **Themis's lane is business and
revenue judgment**, which is a different competency from judging practice efficacy.

**The question that actually decides it** — and it is a good question independent of who answers it:

> **Are the cross-project guidelines an internal practice corpus, or a business asset?**

- **Internal practice corpus** → Janus. It is cross-pollination, already the charter, and the judgment
  required is about whether a practice works.
- **Consulting IP — something promised, sold, or productized** → Themis. PM's own framing of Themis is
  *"as Xian shifts into consulting mode,"* and a standard a client is told to expect is a business
  commitment before it is a practice.

It may legitimately become both over time, in which case the sequencing matters more than the
assignment: it starts as one and is promoted.

Note also that DxP's own `CLAUDE.md` carries a **"lanes, not silos"** principle requiring explicit
cross-references between these two. Whichever way this is ruled, the other should be named as a
consulted party rather than excluded.

**Nothing in §§1–5 depends on this answer.** The tiering, the bar, the outcome-framing, the
upstream-push trigger, and the trigger requirement all hold regardless of who owns Tier 2.

## 7. What is decided vs. what is not

| Decided (PM, 2026-08-29) | Open |
|---|---|
| Two tiers; Tier 1 per project | Tier-2 owner (§6) |
| Tier 1 = new output surface on existing work, stated explicitly | Whether guidelines are internal practice or business asset (§6) |
| Nomination bar = recurrence across projects | Pilot design specifics |
| Standards are outcome-defined floors, locally overridable | Where the corpus physically lives |
| Tier 2 fires on upstream nomination, not a pull cadence | Who does DxP's own Tier-1 harvest if Janus takes Tier 2 |
| Every corpus entry carries a trigger; existing entries retrofitted | — |

## 8. The scarce input, named

In wiki practice the refactoring from thread to document was done by people who read widely and wrote
well, and **it was the scarce resource, not the tooling.** If this becomes real, *who harvests* will
matter more than any tooling decision inside it. Worth deciding deliberately rather than by default.

---

**Related**: `decisions.log` 2026-08-29 entries (trigger requirement; two-tier harvest) · `#1691`
(commit-message guard — the worked example of prose failing to prevent its own recurrence) ·
`docs/internal/development/methodology-core/` (the 64-document corpus this design's §4.4 disposition
applies to)
