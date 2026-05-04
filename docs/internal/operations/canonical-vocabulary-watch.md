# Canonical Vocabulary Watch List

**Purpose**: Joint-stewardship target file for the canonical-term-drift weekly audit (per CIO M1 audit S1 + Apr 27 explicit-checklist proposal + Apr 29 Docs concur with watch-file shape + May 4 CIO concur on file shape).

**Stewardship**:
- **CIO** files additions when new methodology-core entries / patterns / ADRs / PDRs land with load-bearing vocabulary. Single-line edits; no memo-routing required for additions.
- **Docs** operates the weekly scan (Pattern-062 / "Audit the Composition" derivative; the existing #996-style weekly audit gets a new "Canonical vocabulary drift" section that reads from this file).
- **CIO** trims the list at audit cadence (sprint-gate closure + 2 weeks; 8-week max interval) — vocabulary that's no longer load-bearing gets pruned to keep the weekly scan tractable.

**Disposition rules** (from CIO Apr 27 §"Disposition" proposal):
- **Minor drift** (paraphrase of canonical wording where citation would have been right): fix in-pass; note the catch in the weekly audit.
- **Material drift** (vocabulary changed enough that meaning shifts; or: a new term used as if canonical when it isn't): file to the owning role for resolution; the weekly audit notes the route.
- **Pattern-eligible drift** (recurring across ≥2 instances by ≥2 authors): flag as candidate for branch-or-anchor decision (methodology-24); CIO assesses for pattern-catalog escalation.

---

## Watch List (v1)

### Methodology + framework canonical vocabulary

- **Excellence Flywheel** (concept name + the **five practices' canonical names**: Verify Before Building / Test What Matters Not What's Easy / Coordinate Through Structure / Track to Completion with Evidence / Audit the Composition + mnemonic-layer terms when role-cited). Canonical: `docs/internal/development/methodology-core/methodology-00-EXCELLENCE-FLYWHEEL.md` (v2.0, three-layer).
- **Pattern-062 (Assembly Assumption)** + sub-patterns:
  - Pattern-063 (Parallel-Authoring Drift)
  - Pattern-064 (Extension Without Integration) — slot reserved
  - Pattern-065 (Continuity Memo Before the Seam)
- **Indoor plumbing vs. bathing experience** scope filter — methodology-26.
- **Branch-or-anchor decision rule** — methodology-24.
- **Workstream Review Cadence** — methodology-25; Fri-Tue write window, Wed publish, **two senses of "primary"** (reading-order primary = omnibus first; source-authority primary = session logs are authoritative; per CEO May 4 clarification + Exec memo `memo-exec-to-leadership-cc-ceo-pa-docs-cio-primary-sense-clarification-2026-05-04.md`).

### Architectural + product canonical vocabulary

- **PDR-004 principles** (presence over performance, four modes, etc.). Canonical: `docs/internal/product/pdr/PDR-004-experience-philosophy.md`.
- **ADR-060 (Floor-First Routing)** + the floor-vs-ceiling vocabulary. Canonical: `docs/internal/architecture/current/adrs/adr-060-floor-first-routing.md`.
- **Object-model grammar**: *"Entities experience Moments in Places"* (verbatim). Canonical: `docs/internal/architecture/current/adrs/adr-045-object-model.md`.
- **ADR-061 (LLM-Touch Boundary Enforcement)** — calibration-related vocabulary (alpha catch-22, simulation-first calibration, three-phase reframe). Canonical: `docs/internal/architecture/current/adrs/adr-061-*.md` (v1.0 ratification pending PM).

### Cross-project + meta canonical vocabulary

- **Five-layer context model** (RFC-001) — cross-project canonical (Klatch ↔ Piper Morgan).
- **Differentiator stack** (Vision V2.3): the four pillars by name. Canonical: vision doc.

### Operational vocabulary on watch (proto-canonical)

These are recently-coined terms that are propagating through the project; watch for paraphrase drift as they stabilize:

- **Alpha catch-22** (PM Apr 30) — operational tier candidate; vocabulary worth watching as it propagates across calibration / deployment-phase planning.
- **"From Diagnosis to Discipline in 24 Hours"** — proposed Ship #041 framing (Exec May 4 v2 kickoff). If it ships, watch for paraphrase drift in successor narratives.

---

## Operating Notes

**On adding entries** (CIO):
- Single-line addition is the discipline. Format: bullet with name, brief parenthetical, canonical-source pointer.
- If vocabulary needs more than a single line of context, it probably belongs in its own canonical doc — file there first, then add a one-line entry here.

**On scanning** (Docs weekly audit):
- Scan recent omnibus logs + briefings + ADR/PDR/Pattern files for the watch-list terms.
- Disposition per the rules above (minor / material / pattern-eligible).
- Audit notes go in the weekly audit doc; this file is the watch target, not the audit log.

**On pruning** (CIO at audit cadence):
- Drop vocabulary that's stabilized (no drift in two consecutive audit cycles + still in active use).
- Drop vocabulary that's been retired or superseded.
- Trim aggressively. The weekly scan has to remain tractable.

---

## History

- **2026-04-17**: M1 methodology audit §9 surfaced canonical-term-drift as a recommendation (S1).
- **2026-04-27**: CIO files explicit-checklist proposal (`memo-cio-to-docs-cc-pm-exec-audit-s1-canonical-term-drift-explicit-2026-04-27.md`) with starter-vocabulary list.
- **2026-04-29**: Docs concurs (`memo-docs-to-cio-cc-pm-exec-audit-s1-canonical-term-drift-concur-2026-04-29.md`) with one refinement — joint-stewardship watch-file shape.
- **2026-05-04**: CIO concurs on watch-file shape (`memo-cio-to-docs-cc-pm-exec-s1-watch-file-shape-concur-2026-05-04.md`); Docs creates this file (v1) with starter list verbatim + CIO May-period additions (methodology-25 two-senses framing per CEO May 4 clarification, alpha catch-22, Ship #041 candidate framing).

---

*Stewards: CIO (additions, audit-cadence pruning) + Docs (weekly scan, disposition routing).*
*This is the watch target, not the audit log. Audit findings go in the weekly #996-cycle audit doc.*
