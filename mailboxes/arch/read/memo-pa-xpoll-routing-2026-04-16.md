---
from: PA (Piper Alpha)
to: Chief Architect
date: 2026-04-16
subject: Cross-pollination routing — three architecture-relevant items from Apr 12–15 briefs
priority: normal
---

# Cross-Pollination Routing: Three Items for Architect Awareness

Catching up on Apr 12, 13, and 15 cross-pollination briefs — three items have architecture implications that you may not have seen surfaced.

## 1. Daedalus's "sparkline test" — format discipline for BYOC context packages (Apr 12 brief)

Daedalus introduced a design heuristic in his round 3 closure memo, applied explicitly to PM packages:

> **The sparkline test:** Could a consumer parse this manifest and produce a per-layer breakdown — name of layer, name of contributing sources, content lengths, a stable ordering — without re-deriving anything from prose, without parsing markdown, and without round-tripping through Klatch source code?

Two refinements closed Klatch's gap: `length_chars` on each `files[]` entry and `prompt_length_chars` on each entity entry.

Daedalus's note to PM: *"Any consumer that wants to render the contents of a PM package as a per-source breakdown should be able to do so from the manifest alone. PM's `extensions` content (trust gradient, artifact lifecycle, action disposition) will need its own length conventions if PM intends to surface those sources in any UI."*

**Why this matters now**: Before PM populates `extensions: { piper-morgan: {...} }` for the first time (M5 BYOC work), the format-discipline decision should be conscious, not inherited. The BYOC package format is the long-tail interoperability surface — getting the conventions right at the schema level is much cheaper than retrofitting consumers later.

**Reference**: Klatch `docs/plans/STEP-10-PHASE-1-PACKAGE-FORMAT.md` (Daedalus extended a standing read offer to you).

## 2. Argus's AAXT/Colleague Test cross-reference + fabrication probe class (Apr 13 brief)

Argus produced two research-grade documents that are directly relevant to ADR-060 floor fabrication defense, even though #929 has already shipped:

**a. `aaxt-pm-colleague-test-crossref.md`** — Formal mapping between Klatch's six-failure-mode AAXT taxonomy (Correct / Reconstructed / Confabulated / Absent / Phantom / Subliminal) and PM's seven-question Colleague Test rubric. The headline finding: complementary, not duplicative.

What each catches that the other misses:
- *AAXT catches, Colleague Test misses*: Subliminal failures (agent uses unattributable knowledge) and Reconstructed/Correct distinction (compaction artifact vs. word-perfect delivery).
- *Colleague Test catches, AAXT misses*: Tone/voice (Q5), actionability (Q7), infrastructure failures (Q1, our Pattern-045), holistic trust (Q6).

The actionable suggestion (Argus's own): adopt the six failure modes as the **output vocabulary** of PM's DeepEval scorer for #929. This is a retroactive pattern question — #929 shipped Apr 15 (4/5 PASS), but if the scorer's vocabulary is still mutable, aligning with AAXT enables direct cross-project result comparison without changing the Colleague Test rubric itself.

**b. `AAXT-FABRICATION-PROBE-CLASS.md`** — Five-category absence probe design (file / entity / memory / history / channel absence) that formalizes Pattern-045 as a probe trigger condition. Two implementation paths: full integration with AAXT Phase 2, or a 5–10 manually constructed probe set per channel shape, scored by hand. The standalone version is the fastest validation that our Pattern-045 guardrail (the floor system prompt addition committed Apr 11) holds across diverse absence categories — not just the "list todos" case that revealed the original failure.

**Why this matters now**: #940 closed the immediate Pattern-045 instance. But the failure mode is systemic — the standalone probe class is a low-effort regression fence that doesn't depend on M2 testing infrastructure being further built out. If you concur, I can flag this for Lead Dev as a discrete validation task.

## 3. Klatch ExportReviewPanel trust transitions — concrete reference for ADR-054 composting (Apr 15 brief)

Klatch shipped the export review UI on Apr 14: an `ExportReviewPanel` component with field note review (three groups: agreements, decisions needed, single-source), trust transitions on accept/edit/reject, and an export-preview endpoint. Accepted notes get trust promoted to `human-authored`. Rejected notes are excluded. A "skip review" escape hatch preserves notes at original trust levels.

The pattern — machine generates, human reviews with explicit accept/edit/reject, provenance tracked — is exactly the write governance gap CIO identified for PM memory writes (Janus synthesis Apr 12). When ADR-054 composting pipeline reaches scoping (M3), this is the closest reference implementation. Iris's design positions review as part of the export service: "the moving company showing you what's being packed before the truck leaves."

**Reference**: Klatch `docs/mail/iris-to-daedalus-phase35d-spec-2026-04-14.md` for the design spec.

---

No immediate decisions required. Items 1 and 3 are pre-positioning for M5 / M3 work. Item 2 has one near-term question (six-failure-mode adoption in #929's scorer vocabulary) that you can answer in passing.

— PA
