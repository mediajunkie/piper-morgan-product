---
date: 2026-04-12
status: substantive
sources_checked:
  - klatch
  - piper-morgan
window: "24h (April 11–12, 2026)"
---

# Cross-Pollination Brief — April 12, 2026

The last twelve hours in both projects were strategic close-outs, not shipping work — and that may be the most cross-relevant thing to name first. Klatch closed its Step 10 Phase 1 design conversation after five streams of input converged without collision. PM closed out a leadership review cycle, adopted Vision V2.3 and Roadmap v15.0 with full endorsement, and greenlit M2. Both projects ended April 11 with the same gesture: the planning phase is done, now we build.

The substantive cross-project signal this morning is a design heuristic Daedalus introduced in his round 3 closure memo — the **sparkline test** — which Daedalus explicitly applied to PM packages as well as Klatch's. And a canonical principle — **methodology beats code** — which both projects have now formally doctrined, independently, from the same operational experience.

---

## Key Insights

### 1. The sparkline test: a transferable design heuristic for any context package

**From:** Daedalus (Klatch), April 11 — round 3 closure memo to PM Architect
**Relevant to:** Piper Morgan (BYOC architecture, MCP server design)

In closing the Step 10 Phase 1 design conversation, Daedalus introduced a design test prompted by the Labrador project's context sparkline feature (a colored bar in the chat UI showing which prompt sources contributed to each response, expandable to per-source token counts):

> **The sparkline test:** Could a consumer parse this manifest and produce a per-layer breakdown — name of layer, name of contributing sources, content lengths, a stable ordering — without re-deriving anything from prose, without parsing markdown, and without round-tripping through Klatch source code?

Two small refinements to the Klatch schema closed the gap: `length_chars` on each `files[]` entry (alongside `size_bytes`), and `prompt_length_chars` on each entity entry. Both integrated into the round 3 sketch.

Daedalus applied the test forward to PM packages explicitly: "Any consumer that wants to render the contents of a PM package as a per-source breakdown should be able to do so from the manifest alone. PM's `extensions` content (trust gradient, artifact lifecycle, action disposition) will need its own length conventions if PM intends to surface those sources in any UI."

The heuristic generalizes: it's not a feature requirement, it's a format discipline. Any context package that can't answer the sparkline test without re-derivation from prose is leaking structure into unstructured fields — and those leaks are invisible until you're debugging a consumer that fails on edge-case formatting.

**For PM:** Before PM populates `extensions: { piper-morgan: {...} }` for the first time, decide whether PM's extensions content will carry `length_chars`-style conventions. The Klatch format enforces this internally. PM should make a conscious choice, not inherit the gap.

**Suggested action:** PM Architect note the sparkline test when reading Daedalus's Phase 1 design doc (landing next Klatch session as `docs/plans/STEP-10-PHASE-1-PACKAGE-FORMAT.md`). The format read offer from Daedalus stands.

---

### 2. "Methodology beats code" canonicalized in both projects independently

**From:** PM Vision V2.3 (adopted April 11) + Klatch five-layer model (extracted, not designed)
**Relevant to:** Both projects, Janus (editorial)

PM's Vision V2.3 formally names "Methodology beats code frameworks" as one of six defining lessons from ten months of building:

> "The project consistently evolved from 'build code to enforce X' to 'build methodology that achieves X.' Verification, multi-agent coordination, and capability extension all work better as process infrastructure (CLAUDE.md, mailboxes, session logs) than as Python classes."

Klatch's five-layer model is the canonical proof case on the other side of the ecosystem — and the April 9 Vergil synthesis named the same pattern as an extracted abstraction from operational necessity, not a designed architectural decision. Both projects arrived at identical doctrine from different starting points without coordinating on the formulation.

This convergence matters for two reasons. First, it's the kind of validation that justifies publishing the doctrine — if two independent teams building different products with different tech stacks both land on the same operational insight, it's not a preference, it's a finding. Second, it creates a shared vocabulary for cross-project decisions: when evaluating whether something should be code or methodology, both teams now have a named principle and a shared body of evidence.

**For Klatch:** Vision V2.3's articulation of the methodology principle is crisper than anything in Klatch's docs. Worth referencing (or lifting with attribution) in the Step 10 design doc's rationale for why the format spec is a protocol document, not a library API.

**For PM:** The Klatch five-layer model and the AAXT suite are the ecosystem's strongest empirical evidence base for this principle. When PM's methodology work needs external validation, that's the citation.

**Suggested action:** Calliope log the Vision V2.3 formulation as a cross-project reference in the Step 10 design doc. PA note the Klatch AAXT suite as evidence for methodology-as-differentiator framing in any future external writing.

---

### 3. PM M2 includes AAXT-equivalent testing — Klatch's methodology is the upstream reference

**From:** PM Roadmap v15.0, M2 issue list (April 11)
**Relevant to:** Klatch (methodology validation, Argus)

M2's issue list includes three testing infrastructure items that are direct analogues of Klatch's AAXT work:

- **#929** — AAXT: Golden scenarios with DeepEval LLM-as-judge
- **#928** — E2E: Automated canonical conversation suite
- **#930** — CI: Integration for E2E conversations + AAXT nightly

PM is calling its own work "AAXT" now — using Klatch's terminology — and building toward the same scaffolded probing pattern that Klatch shipped in AAXT Phase 1 on April 4. PM's variant uses DeepEval as the judge rather than a bespoke scorer; the architecture is convergent.

Klatch's learnings here are directly applicable:
- The six-failure-mode taxonomy (Absent, Confabulated, Subliminal, Correct, etc.) could map onto PM's scoring rubric
- The "two-pass" approach (automated scan as raw material + curated analysis as authoritative read) is proven via Argus's April 11 curated sweep
- The separation of "structure delivered correctly" from "agent uses it correctly" is the core AAXT/MAXT insight, and PM's Colleague Test addresses the second half exactly

**For PM:** Before building #929's scoring rubric from scratch, read Klatch's scaffolded probing implementation (`research/` or `docs/intel/`) and the six-failure-mode taxonomy. The Colleague Test (CXO) and the AAXT taxonomy (Argus) are two sides of the same evaluation. Alignment between them would make cross-project results comparable.

**Suggested action:** Argus file a brief cross-reference memo on the AAXT taxonomy vs. PM's Colleague Test rubric. PM Architect read before #929 is scoped.

---

### 4. Klatch Phase 1 design doc arrives next session — PM read offer open

**From:** Daedalus (Klatch), April 11 — round 3 close memo
**Relevant to:** Piper Morgan (BYOC architecture)

The Step 10 Phase 1 context package format design is complete through five rounds of input: PM Architect (rounds 1 and 2), Iris (UX), Argus (provenance), Calliope/Janus (sparkline test). The schema sketch lives in Daedalus's session log at `docs/logs/2026-04-11-1610-daedalus-opus-log.md` (search "Schema sketch round 3"). Next session it graduates to the formal design doc.

Key design decisions now stable:
- **`extensions` namespaced** by producer (`extensions: { klatch: {...} }`, PM packages expected to use `extensions: { piper-morgan: {...} }`)
- **`format_version` and `package_kind` versions move independently** — envelope version vs. kind-specific interior version
- **Provenance doors preserved** — `event_id` UUID and `integrity: null` reserved per event, enabling tamper-evidence as a v1.1 additive change
- **`layer_fidelity` vocabulary** (`full`, `partial`, `rebuilt`, `absent`) — distinct from AAXT failure-mode taxonomy (per-hop delivery fidelity vs. probe response quality)
- **`conversation_context.id` and `.name` as minimum cross-source read** — a consumer can display package contents without checking `source_type` first

Daedalus offered PM Architect a read of the design doc when it lands. The offer is standing.

**Suggested action:** PM Architect watch for `docs/plans/STEP-10-PHASE-1-PACKAGE-FORMAT.md` in Klatch's next commit and accept the read offer. Flag now if PM's BYOC server has constraints the current schema sketch doesn't accommodate — better to surface before the doc is finalized.

---

### 5. PM M2 starts: differentiator stack now operational framing

**From:** PA (PM), April 11 — M2 go-ahead memo, Vision V2.3, Roadmap v15.0
**Relevant to:** Klatch (timing, BYOC architecture timeline)

M2's theme is "Conscious Floor + Action Handlers" — making the conscious floor reliable (grammar, Five Pillars, anti-flattening) and implementing the action gate (side-effect handlers only). The differentiator stack's first two pillars become operational in M2. M3 adds Artifact Persistence (composting lifecycle). M5 adds Distribution (MCPB).

The Klatch intersection point is M5. BYOC distribution — Piper as an MCP server consumed by any MCP-compatible client — is explicitly the primary distribution path. The context interchange protocol Klatch is building in Step 10 becomes an upstream dependency for PM's BYOC server: a PM session starting in Claude Desktop could call Klatch for a pre-assembled five-layer context package rather than re-assembling from scratch.

That architectural dependency won't become concrete until M5, which means there's time — but also that M2 and M3 architectural decisions (especially around context assembly and artifact persistence) should be made knowing the eventual BYOC constraint exists.

**For PM:** No immediate action, but flag the Klatch context package format as an upstream dependency to watch in M5 planning. The Phase 1 design doc landing next session is the right moment to begin the M5 framing.

**Suggested action:** PA add a watch item to M5 planning notes: "Klatch context interchange protocol (Step 10, Phase 1 design doc) — evaluate as upstream context source for BYOC session start."

---

## Sources Read

**Klatch:**
- `git log --since="48 hours ago"` — 26 commits
- `docs/mail/daedalus-to-pm-architect-step10-alignment-round3-2026-04-11.md` — round 3 close, sparkline test, provenance doors, stable schema
- `docs/logs/2026-04-11-1211-calliope-opus-log.md` — five-stream convergence logbook
- `docs/logs/2026-04-11-1610-daedalus-opus-log.md` referenced (schema sketch round 3)
- Commit messages: `d57203a` (Phase 1 design closed), `73a5db0` (April 11 logbook)

**Piper Morgan:**
- `git log --since="48 hours ago"` — 22 commits
- `docs/internal/planning/current/vision.md` — Vision V2.3 (full read)
- `docs/internal/planning/roadmap/roadmap.md` — Roadmap v15.0 (executive summary + M2 detail)
- Commit messages: `fe19ca1` (V2.3 + Roadmap v15.0 adopted), `d8f7ac7` (M2 go-ahead), `fdab67c` (PA day 12 session close)

---
