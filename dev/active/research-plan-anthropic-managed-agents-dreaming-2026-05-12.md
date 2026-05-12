# Research Plan — Anthropic Managed Agents "Dreaming" vs. Piper Morgan's Dreaming Concept

**Prepared by**: PA (Piper Alpha)
**Date**: 2026-05-12
**Trigger**: Argus 5/11 sweep finding (Klatch `docs/intel/2026-05-11-sweep-curated.md`) — Anthropic shipped "Managed Agents Dreaming" at "Code with Claude" event May 6, 2026. CEO directive to PA same morning to plan deep-dive research.
**Status**: PLAN (not the research itself; awaits PM go-ahead to execute)

---

## Why this research matters now

The xpoll brief frames the Anthropic announcement as *"reframes Step 11 differentiation: don't compete with SDK-level memory primitives; compete on conversation-as-substrate and cross-channel context assembly."* That's a strategic-positioning take. What it isn't is a deep examination of **what Anthropic actually shipped** and **how it relates to Piper's specific dreaming concept** — which has a feature (Type 2 anxiety dreams) that Janus's Apr 12 prior-art survey confirmed has no equivalent in any of 20+ external memory systems.

The strategic framing alone is incomplete because Piper's concept isn't just "memory primitives" — it has three components:

1. **Type 1: Filing dreams** (consolidation / indexing — the part that overlaps most with what SDK memory primitives are likely to provide)
2. **Type 2: Anxiety dreams** (threat simulation / risk rehearsal — genuinely novel per Janus)
3. **Unihemispheric extension** (partial rotating cycles for power users without idle time — not yet designed)

A surface-level "they shipped memory; we should reframe" risks missing whether Anthropic's tooling can host (1), enables but doesn't provide (2), and is silent on (3) — each of which has different implications for PM architecture.

## Three primary research questions

### Q1 — What did Anthropic actually ship?

The xpoll brief tells us **that** they shipped, not **what** they shipped. Specifically need to answer:
- API surface: what does the developer interface look like?
- Mechanism: does the SDK do anything at idle time, or is it purely retrieval-and-store?
- Scope: per-session memory, cross-session, cross-agent?
- Triggers: what causes "dreaming" to happen — schedule, idle detection, manual, compaction, something else?
- Trust / quality control: any post-hoc reflection or just first-pass storage?
- Token economics: does it consume model budget, or is it sidechannel?

### Q2 — Where does it land on Piper's three-component dreaming map?

For each of Piper's three components, classify the Anthropic offering:
- **Replaces** — Anthropic does this; PM should delegate
- **Provides primitives for** — Anthropic supplies the substrate; PM builds the layer above
- **Silent on** — Anthropic doesn't address this; PM still owns it
- **Conceptually incompatible** — Anthropic's model conflicts with PM's framing in a way that requires careful bridging

The most important sub-question: **does Anthropic's framework include any Type 2 / threat-rehearsal capability**, or is it pure consolidation? If Type 2 is absent (likely per Janus survey), PM's distinctive value-proposition is preserved.

### Q3 — What should PM do differently in response?

Three response shapes to evaluate:
- **Delegate** — adopt Anthropic's primitives for Type 1 work; remove PM's composting/InsightJournal scope where Anthropic now provides equivalent
- **Build on top** — keep PM's architecture; layer Anthropic's primitives as substrate; surface Type 2 / unihemispheric as PM-distinctive assembly
- **Extend the framework** — contribute back to Anthropic's model with PM's distinctive concepts (likely too ambitious for current cycle; flag for future)

The decision likely splits per-component: delegate Type 1, build on for Type 2, design unihemispheric separately.

## Methodology

### Phase 1 — Anthropic mechanism survey (~3-4 hours)

Sources to read, in priority order:
1. **Klatch's `docs/intel/2026-05-11-sweep-curated.md`** — Argus's full sweep with primary source links (entry point)
2. **Anthropic's "Code with Claude" announcement** (May 6, 2026) — official content; likely a blog post + developer docs + perhaps a video. Use WebFetch.
3. **Anthropic SDK changelogs** — between the SDK version that existed pre-May-6 and current; identify the specific memory-tooling commit/release
4. **Anthropic developer documentation** for the new memory features — API surface, intended use cases, example code
5. **Third-party developer commentary** (HackerNews, Discord, X, dev blogs) within ~7 days of announcement — what early adopters discovered about the actual behavior vs. the marketing
6. **Janus's Apr 12 memory prior-art survey** (`mailboxes/docs/read/memo-janus-to-docs-memory-prior-art-response-2026-04-12.md`) — 20+ external systems; check if any have evolved since Apr 12, especially anyone Anthropic might have absorbed

**Output**: a "what Anthropic actually shipped" summary section, 1-2 pages, with citations.

### Phase 2 — Piper concept inventory + comparison matrix (~2 hours)

Sources to consolidate:
1. **`dev/2026/04/12/dreaming-concept-provenance-2026-04-12.md`** — Docs's chronological provenance of the dreaming concept (Type 1 + Type 2 + unihemispheric)
2. **`docs/internal/architecture/current/composting-learning-architecture.md`** — full spec for Type 1 (CompostBin, Decomposer, LearningExtractor, InsightJournal, EmergentCreator; SCHEDULED trigger 2-5 AM; AGE/IRRELEVANCE/MANUAL/SCHEDULED/CONTRADICTION trigger types)
3. **MUX-VISION-LEARNING-UX docs** (`docs/internal/design/mux/`) — the user-facing layer of the dreaming concept
4. **Recent M2d shipped work**: #1033 MUX-COMPOSTED-EXPERIENCE ("filing dreams" framing), #1035 MUX-COMPOSTING-ACTIVATION, #1030 MUX-INSIGHT-PULL
5. **The corrupted CIO unihemispheric memo** (`dev/2026/01/11/` area) + the Architect-revised version — may need PM to provide a clean copy if recovery is needed

**Output**: a comparison matrix with axes for each dreaming component vs. each Anthropic capability:
- Consolidation / indexing
- Cross-session continuity
- Threat simulation / risk rehearsal
- Trigger types
- Idle-time vs. always-on
- Token / cost surface
- User-facing surface
- Multi-agent coordination

### Phase 3 — Architectural implications for PM (~2-3 hours)

For each component of PM's dreaming concept, determine:
- **What stays in PM's scope** (assembly-layer, Type 2, unihemispheric)
- **What shifts to SDK delegation** (if Type 1 mechanisms map to Anthropic's primitives)
- **What new design surface opens** (e.g., if Anthropic provides per-session memory, can PM's InsightJournal layer be thinner?)
- **What's at risk** (e.g., does Anthropic's framing of memory conflict with PM's "anxiety dream" framing in a way that creates a vocabulary collision?)

Specific architectural questions to address:
- Does Anthropic's offering change the answer to **#984 (CONTEXT-CACHE Redis TTL)** Phase 0 architecture questions still pending PM decision?
- Does it change the **M3 (Artifact Persistence) sprint scope** in roadmap v15.0?
- Does it affect the **#952 ARTIFACT-MODEL** or **#953 CONTEXT-PERSIST** issues?
- Does it create a coordination need with the BYOC PDR-005 work currently in discovery (since BYOC defines what PM ships as MCP server, and if Anthropic provides memory primitives at the SDK layer, PM's MCP surface positions differently)?

**Output**: a "what PM should do differently" section with concrete recommendations to Architect, CIO, and PM.

### Phase 4 — Synthesis memo + routing (~1 hour)

Write up the research as a memo:
- **To**: Architect, CIO, CXO, PPM
- **CC**: PM (xian), exec
- Cross-pollination route: **back to Klatch via Janus** — Argus surfaced the original signal; Calliope is doing the parallel reframe for Step 11; PM's deeper-dive findings should flow back so all three projects converge

**Output**: memo at `mailboxes/{role}/inbox/memo-pa-to-...-anthropic-dreaming-research-findings-2026-05-XX.md`.

### Phase 5 (optional, if signal warrants) — coordination conversation

If the findings suggest joint design opportunity with Klatch (e.g., shared assembly-layer protocol that both projects can build), route a coordination request via Janus.

## Effort estimate

- **Phase 1**: 3-4 hours
- **Phase 2**: 2 hours
- **Phase 3**: 2-3 hours
- **Phase 4**: 1 hour
- **Phase 5**: 1-2 hours optional

**Total**: 8-12 hours of substantive PA work. Realistically a 2-3 session span given PM's current OpenLaws-focused cadence; PA can execute in pieces.

## Deliverables

1. **Research memo** (~3-5 pages) covering Q1/Q2/Q3 with comparison matrix
2. **Architectural recommendations** to Architect / CIO
3. **Possible follow-up issues filed** if implications require new tracked work
4. **Possible Janus routing** back to Klatch with PM-side findings
5. **Possible memory update** if findings shift PM's design center enough to warrant a new memory entry

## Open questions for PM before executing

1. **Audience and tone** — Is this for PM's own situational awareness (internal memo), or for cross-project consumption (Klatch + others see findings)? My lean: write for internal first; cross-pollinate via Janus afterward if findings warrant.
2. **Time-sensitivity** — Is this informing a specific upcoming decision (#984, M3 scope, BYOC PDR-005, calibration-window enhancement)? If yes, the research priority shifts accordingly.
3. **Coordination with Klatch's Calliope** — Calliope is doing the parallel reframe for Klatch Step 11. Should PA coordinate with Calliope via Janus before starting (to avoid duplicate work), or after (to compare independently-derived findings)? My lean: **after** — independent reads followed by reconciliation surfaces more signal than coordinated reads.
4. **WebFetch budget** — Anthropic source material may require multiple WebFetch calls. Want me to surface estimated count before fetching?
5. **What to do if the CIO unihemispheric memo can't be recovered cleanly** — proceed with Architect's revised version + the omnibus references, or block on memo recovery? My lean: proceed; the omnibus + provenance doc carry enough.
6. **Cross-project IP discipline** — Janus's relay convention applies. Confirm that "OpenLaws-derived framings" are NOT in scope (this is internal PM research about PM's design); the Janus relay is for routing the final memo, not for upstream input.

## Out of scope (explicit)

- Not implementing any of PM's dreaming concept in this research cycle — pure analysis
- Not changing roadmap v15.0 — recommendations may inform a future update
- Not coordinating with Anthropic directly — this is a one-way absorption of public material
- Not benchmarking PM's existing composting code against Anthropic's primitives — that's an implementation question, not an architectural one

## Recommendation to PM

Endorse Phase 1 as immediate next action; treat Phase 2-4 as conditional on Phase 1 surfacing enough substance to justify deeper dive. If Phase 1 finds Anthropic's offering is thinner than expected (e.g., just persistent KV-store with retrieval), the research can compress to a short summary memo rather than the full 8-12 hour arc.

If Phase 1 finds Anthropic shipped something substantial (e.g., actual offline-time reflection passes with model invocation), the full arc is warranted.

— PA, 2026-05-12
