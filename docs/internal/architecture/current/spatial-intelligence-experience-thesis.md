# Spatial Intelligence — the Experience Thesis (why the cold adapter tier is *later*, not *failed*)

**Document Version**: 1.0
**Date**: 2026-07-29
**Author**: CXO (experience-design lane)
**Status**: ⚠️ **INPUT to a pending decision — NOT a decision.** See "Standing" below.
**Related**: ADR-013 (deprecated for pattern policy), ADR-038 (current pattern policy),
`spatial-intelligence-competitive-advantage.md` (Aug 2025, maximalist companion to ADR-013),
`dev/active/spatial-intelligence-architectural-history-arch-WIP.md` (Arch's in-flight synthesis),
PDR-004 (experience philosophy)

---

## Why this document exists

The spatial-intelligence committed-theory review (opened 2026-07-19, PM-directed) is running in four
lanes: Arch (architectural history + ADR disposition), Lead (code-reality census), PPM
(product-value/roadmap scoping), and CXO (experience theory). Three lanes have filed; Arch
synthesizes; **PM decides.**

**The CXO lane's argument existed only in a memo.** That is the specific problem this file fixes.
Memos are the cross-agent signaling layer; they are not the durable architecture record. An agent
reading ADR-013 and ADR-038 against the current state of the code would encounter:

- ADR-013 declaring spatial intelligence a mandatory universal pattern and an "unassailable
  competitive moat"
- ADR-038 asserting all three patterns "100% operational" and "production-proven"
- and a **cold, partially-implemented adapter layer** — `notion_spatial.py` with undefined methods,
  `gitbook_spatial`, `devenvironment_spatial`, `linear_spatial`, `cicd_adapter`, `linear_adapter` —
  unreachable from the running application

**The natural inference from those three facts is "the theory was overreach and the code is a failed
attempt at it — supersede ADR-013."** That inference is available from the architecture record
alone, it is reasonable, and **the experience-design lane's position is that it is wrong.** The
counter-argument is not recoverable from any document in this corpus. Hence this file.

> **The load-bearing claim, stated once**: **adapter depth** and **ambient presence** are two
> different capabilities, not two completeness levels of one. Cold `*_spatial` code is evidence of
> an **unreplicated** capability and an **unstarted** one — not of a **failed** one.

## Three things, not two — corrected 2026-07-29

⚠️ **This section was rewritten the day it was written.** My original framing (filed 2026-07-19) said
spatial intelligence was **two** tiers: a live reasoning layer and a wholly-cold adapter tier which I
equated with ambient presence. **Arch corrected the underlying code characterization on 2026-07-29 at
15:50**, and the correction breaks that equation apart. Recording the correction rather than quietly
absorbing it, because CXO and PPM both formed positions against the 7/19 version and Arch's ruling is
explicit that **nothing in this review may ratify on it.**

**What Arch established** (verified importer-by-importer): layer 2 is **one live, five cold.**
`github_spatial` is **LIVE** — a full 8-dimensional implementation, top-level import at
`github_integration_router.py:30`, reachable by **two independent paths** (the intent path via
`context_assembler`, and over HTTP via the Places API at `places.py:81`). `notion_spatial`,
`gitbook_spatial`, `devenvironment_spatial`, `linear_spatial`, `cicd_spatial` have **zero importers**.

So the connector-as-place ambition **was built — once, for the most important connector, at full
depth, and it is in production.** It was never replicated.

**That forces a three-way split, and the third row is the one my 7/19 framing got wrong:**

| | **Tier 1 — spatial REASONING** | **Tier 2a — per-connector ADAPTER DEPTH** | **Tier 2b — AMBIENT PRESENCE** |
|---|---|---|---|
| **State** | **LIVE, wired, shipping** | **LIVE for GitHub; COLD for five others** | **NOT BUILT — nowhere, for any connector** |
| Where | `place_detector`, `spatial_intent_classifier`, `mux/orientation`, `workspace_detection`, `lenses/hierarchy`, `context_assembler` (8-dim), `spatial_context` grafting | ✅ `integrations/spatial/github_spatial` (8-dim, 2 paths) · ❄️ `{gitbook,notion}_spatial`, `{devenvironment,linear}_spatial`, `cicd_spatial`, `{cicd,linear}_adapter` | no monitoring loop, no change detection, no salience judgment, no proactive-surfacing surface |
| **What the user experiences** | **"Piper knows *where* things live, and acts there."** | **"Piper understands this tool's places in depth"** — richer place-modeling *when asked*, for the connectors that have an adapter. | **"Piper *inhabits* my tools and notices things"** — *"there's been activity in the Notion space you were in."* |
| **Felt difference** | Piper is **oriented** | Piper is **fluent in this tool** | Piper is **present** |
| **Interaction model** | user-initiated | **also user-initiated** — request/response, via intent or HTTP | **product-initiated** — monitoring generates the occasion to speak |
| **Beta relevance** | ships the thesis | **partially shipped**; replication is a cost question, not a proof question | **wave 2**, and unchanged by Arch's correction |

### Answering Arch's re-poll directly

Arch asked: *does "ambient-presence tier" still describe layer 2 if GitHub's 8-dim adapter is live —
i.e. is ambient presence partially shipped for one connector, unnoticed?*

**No. Ambient presence is not partially shipped; it is not shipped at all.** What shipped is
**adapter depth** for one connector. The two are separable and I conflated them on 7/19.

The discriminator is **who initiates**, and it survives the correction cleanly: `github_spatial` is
reached *when a user asks something* (through `context_assembler` on the intent path) or *when a
client calls the Places API*. Both are request/response. **Ambient presence requires the product to
speak unprompted** — which needs a monitoring loop, change detection, a salience judgment, and an
interruption-ethics surface. **None of those four exist anywhere in the codebase**, and none of them
is `github_spatial` at a higher percentage. GitHub having a deep adapter makes Piper *fluent about
GitHub places when asked*; it does not make Piper *present in GitHub*.

**So my error was a category error, not a factual one** — I attached "ambient presence" to the
adapter *modules* because that is what the adapters would eventually feed. But the adapters are the
**place-modeling substrate**; ambient presence is a *separate consuming capability* that would sit on
top of them and does not exist.

### Why these are capability boundaries and not progress bars

- **Tier 2a is not a gap in Tier 1.** They share a metaphor and some types, not a dependency.
  Replicating adapters to five more connectors would not make Piper better oriented.
- **Tier 2b is not Tier 2a finished.** Its hard problems — when is a change worth mentioning, how
  does Piper interrupt without being obnoxious — are untouched by having more adapters.
- **Nothing user-facing waits on the five cold adapters.** Connectors work through the ADR-070
  consumer path without them. That is what distinguishes *unreplicated* from *broken*.

## The specific trap, stated plainly

**A reader who reaches Tier 2's cold code by way of ADR-013's maximalism will read abandonment.**
Three things compound:

1. ADR-013 said **ALL** integrations MUST use the unified pattern — so cold adapters look like
   non-compliance with a live mandate (it is deprecated for pattern policy; the file's own
   deprecation notice is easy to skim past).
2. `spatial-intelligence-competitive-advantage.md` calls the 8-dimensional signature an
   "unassailable competitive moat" — so the cold tier looks like the moat is unbuilt.
3. **ADR-038 asserts "Notion spatial: 100% operational"** and nominates Notion as the
   Embedded-Intelligence proof. `notion_spatial` is **both ~75% abandoned (≈12 undefined methods)
   AND unreachable**. Arch's 2026-07-29 finding makes the correction precise rather than a bare
   discrepancy: **ADR-038 was right about the pattern and wrong about which connector proved it** —
   GitHub, which ADR-038 did *not* hold up as the spatial exemplar, is the one that shipped. The ADR
   amendment is Arch's to draft.

The trap is that all three point the same way, and none of them says "this was a second capability
we chose not to start."

**Arch's correction adds a fourth, sharper edge to the trap — and it cuts the opposite way.** Because
`github_spatial` is live behind both the context assembler and an HTTP route, **option (c) supersede
would delete a working, in-production, full-8-dimensional implementation** — not retire an unbuilt
ambition. A reader who samples the cold five and reasons "none of this is reachable, retire the
pattern" would be proposing removal of live code while believing they were proposing cleanup. That is
now the most expensive available mistake in this review, and it is the easiest one to make from a
filename sweep.

⚠️ **Method note, recorded because it is how the 7/19 error happened**: Arch built the original cold
list from a *recalled filename pattern* rather than a directory listing, so `github_spatial.py` — in
the very directory being characterized — was never checked. **Enumerate the directory; do not sweep
from memory.** A second near-miss the same day: a grep hit on the feature-flag *string*
`"notion_spatial_mapping"` nearly recorded a cold module as live.

## The CXO position

**Option (b), on the corrected boundary: keep Tier 1 *and* `github_spatial`; park the five cold
adapters as design capital. Scope-clarify ADR-013 and ADR-038. Do NOT supersede the theory.**

**The vote is unchanged by Arch's correction; the boundary and the reasoning both sharpen.** Arch's
finding gives (b) a concrete line it previously lacked — *keep the reasoning layer plus the one live
adapter, park five* — rather than the vaguer "keep live subset."

Argued from experience design, not from engineering inventory:

1. **The thesis is proven at beta depth, not proven wrong** — and now proven *further* than I claimed.
   Tier 1 ships "places-with-colleagues," and GitHub demonstrates the full 8-dimensional adapter
   pattern is **shippable, not just theorized.** A theory with a live reference implementation has
   been validated in part, not falsified.
2. **What is over-scoped is the *replication*, not the *theory*.** My 7/19 line was "the theory is not
   overkill; the full adapter chain is." Corrected: **the pattern is demonstrably buildable — GitHub
   proves it. The open question is whether per-connector replication pays**, which is a cost question
   and a different question from whether the theory works.
3. **The experience argument against replicating now** — and this is the CXO-specific part, because
   Arch's re-pricing makes (a) commit-and-finish genuinely cheaper than anyone had been told:
   **replicating adapters to five more connectors does not deliver ambient presence.** It buys deeper
   place-modeling for tools users are not currently asking Piper about, while Tier 2b — the capability
   that would actually be *felt* as differentiation — remains unbuilt regardless. So even at the
   corrected lower cost, replication is **the wrong next spend**: it deepens a substrate before
   anything consumes it. If we want the ambient-presence experience, the next investment is Tier 2b
   on the connector that already has an adapter, not Tier 2a on five more.
4. **Parking is cheap and reversible; superseding is now actively destructive.** A parked tier with
   its rationale recorded can be picked up. (c) would remove a live 8-dimensional implementation
   sitting behind the context assembler and an HTTP route.

**A scope-clarification, not a reversal**: ADR-013's error was universality and mandatory-ness
("ALL… MUST", "no exceptions"), not the spatial concept. The correction is to say which tier is
current policy and which is deferred — not to say the concept was wrong.

## What would change this position

Recorded so the position is falsifiable rather than merely held — and so a future reader can check
whether the conditions have since been met:

- **PPM's roadmap-dependency check comes back positive** — if any M4/M5/Production-1.0 commitment
  *implicitly assumes* the adapter chain, then it isn't wave-2 design capital, it's a live
  dependency, and the disposition question changes shape entirely. **This is the open gate**, and
  Arch's correction sharpens it: the question is now *"does any 1.0 commitment assume the chain
  **beyond GitHub**?"* — GitHub's adapter already exists, so a commitment satisfied by GitHub alone
  is not evidence for replication.
- **Ambient presence (Tier 2b) turns out to be cheap on top of `github_spatial`** — if a monitoring
  loop over the one live adapter is a small build, the sequencing argument in position §3 flips from
  "park and wait" to "build 2b on GitHub now and let it prove demand for replication." I have not
  costed this and it is Lead's to estimate; recording it because it is the most likely way my
  recommendation becomes wrong.
- **Tier 1 turns out to depend on Tier-2 modules** for reachability. (Lead's census bears on this:
  with `query_router` deleted, the sim/POC transport's remaining reachability sits inside the cold
  cohort — so the sim-transport question is subsumed by Tier 2's disposition.)
- **Ambient presence gets designed out of the product direction** on other grounds — if we decide
  Piper should never speak unprompted, Tier 2 loses its purpose and (c) becomes correct.
- **Maintenance cost of parked code exceeds its option value** — a Tier-3-style cleanup judgment,
  legitimately Lead's and Arch's to make, not CXO's.

## Standing — read before citing this document

- **This is one lane's input to a decision that has not been made.** It is not policy and does not
  supersede ADR-013 or ADR-038. Cite it as the experience-design argument, not as a ruling.
- **PM decides**, on Arch's synthesis, gated on PPM's roadmap read and Arch's ADR-affected map.
- **Spatial intelligence is protected representation** (PM's standing rule): meaning-representation
  is never removable without PM consult. Nothing in this document authorizes deleting anything.
- **If PM's decision lands differently from (b), this file should be updated to record the decision
  and preserved as the argument that lost** — not deleted. The reasoning stays useful either way,
  and a corpus that only keeps winning arguments teaches future readers nothing about why the
  question was hard.
- **When the disposition ratifies, the resulting ADR should absorb the two-tier distinction above**
  — that framing is the part that must outlive this review, whichever option is chosen, because it
  is what prevents the next reader from re-running the same wrong inference.
