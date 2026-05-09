# Pattern-063: Parallel-Authoring Drift

## Status

**Proven** — Promoted from Emerging May 8, 2026 (CIO promotion authority per `methodology-audit-policy-updates-2026-03-16.md`). Trial-application evidence: diagnostic operated at origin (Apr 26 C-axis incident); branch-or-anchor rule shipped to two surfaces (methodology-24 + CT v2.3) without subsequent silent-extension recurrence; Architect May 4 architectural-soundness review identified parallel-authoring instance at code layer (legacy/refactored boundary_enforcer.py coexistence) using pattern's framing. Three independent surface validations. Originally identified April 26, 2026 (CXO + PPM rubric C-axis reconciliation incident); filed Emerging Apr 27 under CIO self-approval authority + PM concurrence on slot allocation. Promotion analysis at `dev/active/cio-pattern-promotion-analysis-2026-05-08.md`.

## Product Relevance

**Portable** — Any team maintaining canonical specifications (rubrics, schemas, contracts, vocabulary, configuration) will encounter this when extending those specs in parallel without anchoring. The pattern operates at the *specification layer*, which means it cuts across code, documentation, evaluation instruments, and process artifacts.

## Context

When a canonical reference (rubric, schema, term, principle, slot reservation) is extended in parallel by two or more authors, each acting in good faith and producing individually correct work, the extensions can diverge silently at the semantic layer while appearing convergent at the surface layer. The failure becomes visible only when the parallel artifacts are applied to the same case and produce divergent results.

This pattern is a sibling sub-pattern of **Pattern-062 (Assembly Assumption)** at the *specification* layer, distinct from Pattern-064 (Extension Without Integration) which operates at the *integration-contract* layer. Both are sub-patterns of 062; both involve individually-correct components composing into incomplete or wrong outcomes; the difference is in the failure mechanism.

### Relationship to Pattern-062 and Pattern-064

| Pattern | Layer | Failure mechanism |
|---|---|---|
| 062 (parent) | General | Individually correct components, unverified composition |
| 063 (this) | Specification | Two parallel extensions of shared semantics drift; verdicts converge while methodology diverges |
| 064 (Architect, planned) | Integration contract | One extension passes own tests but breaks on realistic composition |

Pattern-063 is about **parallel authoring** producing semantic drift. Pattern-064 is about **single-path extension** without integration verification. Different mechanisms, both children of 062.

## Problem

### The Failure Mode

Two authors extend the same canonical reference at roughly the same time, working independently:

```
Canonical doc v1 ─┬─→ Author A: extends with adaptation X
                  └─→ Author B: extends with adaptation Y

Both extensions: individually correct.
Both extensions: use shared label/identifier from v1.
Surface: converged (same label, similar verdict on test cases).
Semantic: diverged (different criteria, different consequences).
```

The failure becomes detectable only when the parallel artifacts are applied to the same case and produce different scores, decisions, or actions — by which point both have propagated to downstream consumers.

### Why It Happens

Three forces converge:

1. **Canonical references are extension surfaces by design.** Rubrics, schemas, and decision frameworks are written to be extended for local needs. The act of extension is encouraged; the discipline of *how* to extend is rarely formalized.

2. **Parallel work is the operating mode.** In multi-agent or multi-author systems, the assumption is that authors do not need to coordinate at every extension. Each author reads the canonical doc, drafts an adaptation, ships it. No structural moment forces consultation between authors.

3. **Surface convergence masks semantic divergence.** When two parallel extensions produce the same verdict on a test case (both score "PASS", both call a query "high-risk"), the agreement reads as validation. The validation is illusory: the two methods may agree in the trivial cases while diverging arbitrarily in the non-trivial ones.

### Diagnostic Question

> *"If I asked the two authors to score each other's work using the other's rubric, would they get the same answer?"*

If the answer is "I'm not sure," the parallel-authoring drift pattern is operating. The agreement on the surface tells you nothing; the divergence is at the semantic layer where the two authors haven't yet checked each other's work.

A second diagnostic phrasing (cross-cuts to Pattern-045 + Pattern-062): **"What would have to be true for these to be wrong in the same direction?"** When two divergent methods produce the same answer, the answer is robust to method variation in the trivial cases — which tells you nothing about the non-trivial cases.

### Concrete Example: Phase E vs. CT v2 C-axis Incident (Apr 26, 2026)

Two scoring instruments shared the canonical reference's letter "C" with materially different criteria:

| Rubric | Author | Date | C-axis label | C=2 criterion | C=3 criterion |
|---|---|---|---|---|---|
| Phase E rubric | Lead Dev | Apr 23 | **Clarity** | "States decline but no reason" | "Offers user a constructive path forward" |
| Colleague Test v2 | CXO (Code) | Apr 25 | **Context** | "Generic LLM competence" | "Project-context injection visible" |

Both rubrics were authored in good faith. Both were individually correct. Both extended the same canonical predecessor (Colleague Test v1) without explicit anchoring or branching. The drift surfaced Apr 26 when the same Phase E transcripts were scored under both rubrics — verdicts converged at PASS, but C-axis scores diverged systematically.

**Verdict-convergence as the masking signal**: the same transcripts received PASS under both rubrics. The agreement on output level masked the divergence on methodology level. Without the cross-application that surfaced the divergence, both rubrics could have continued diverging through subsequent applications, with quality-threshold decisions silently depending on which rubric an author happened to consult.

## Solution

### The Branch-or-Anchor Decision Rule

When extending a canonical reference (rubric, schema, term, principle, slot allocation), the author must explicitly choose **anchor** or **branch**:

- **Anchor**: cite the canonical doc by version, use the canonical criteria unchanged, do not silently extend. If the canonical doesn't fit local needs, branch.
- **Branch**: rename the local artifact explicitly, version it as a derivative, document the deviation from canonical. The new name signals to all downstream consumers that this is no longer the canonical artifact.

**Silent extension** — using the canonical's label while changing the criteria — is the failure mode this rule prevents.

### Concrete Application

For the canonical example above (CT v2 C=Context vs Phase E C=Clarity):

- **Anchor path** (the resolution adopted Apr 26): Phase E rubric supersedes its draft with a one-liner pointing to CT v2; uses C=Context as defined.
- **Branch path** (a hypothetical alternative): Phase E rubric explicitly renames as "Activation-Gate Clarity Rubric v1, derived from CT v2 with C=Clarity replacing C=Context." Same downstream consumers can now see the divergence in the name.

Both options resolve the drift. **Silent extension cannot.**

### Implementation Surfaces

The rule lives in two complementary surfaces (per CXO Apr 26 belt-and-suspenders concurrence):

1. **Methodology-core entry**: standalone rule statement, accessible to authors who consult methodology before drafting.
2. **Embedded in the canonical document itself**: "How to extend this rubric/schema/contract" section, accessible to authors who go directly to the canonical to extend it. (This is the actual high-failure path — Lead Dev's Apr 23 Phase E rubric drafting was exactly this pattern.)

Two surfaces because the populations of authors don't fully overlap.

### Complementary Operational Hygiene (Not Sufficient Alone)

- **Naming-collision detection**: when authoring a new rubric or scoring instrument, do a five-second `grep` for similar axis labels in adjacent rubrics. Cheap, catches accidental collisions.
- **Version-stamp norm**: every artifact citing a canonical reference notes the canonical's version explicitly in metadata. Doesn't prevent drift; makes drift detectable post-hoc.
- **Canonical-reference registry**: an index of canonical artifacts and their owners. Diagnostic aid; doesn't prevent silent extension.

These are useful infrastructure but secondary to the underlying discipline. The discipline is: **do not extend a canonical reference silently.**

## Usage Guidelines

### When to Apply

- Two or more authors extending the same canonical reference in parallel
- Adapting a rubric, schema, principle, or contract for local use
- Reserving a slot in a shared catalog (pattern numbers, ADR numbers, issue numbers)
- Coining vocabulary derived from canonical terms
- Any moment where the discipline question is "extend or branch?"

### When This Pattern Doesn't Apply

- Single-author extensions with no parallel work happening
- Refactoring a canonical doc with full ownership and downstream coordination
- Cases where the canonical itself is being deliberately replaced (versioned upgrade, not parallel extension)

## Anti-Patterns

| Don't Do This | Why | Do This Instead |
|---|---|---|
| Extend a canonical's label with new criteria silently | Surface convergence masks semantic divergence | Branch with explicit rename |
| Defer reconciliation to a "v2.x" patch when drift is noticed | Silent drift compounds during the deferral window | Treat the moment of noticing as the discipline issue; reconcile immediately |
| Trust verdict-convergence as validation | Agreement on outputs ≠ agreement on methodology | Apply the diagnostic question: would each author score the other's work the same? |
| Reserve catalog slots informally in handoffs | Soft reservations fail under parallel authoring (this catalog itself, Apr 26 Pattern-063 slot conflict, is a meta-instance) | Use formal slot reservation with visible claim, or take the next available number when you formalize |
| Add only a registry/version-stamp without the underlying rule | Diagnostic aids don't prevent the failure mode | Implement the branch-or-anchor rule first; add registry/stamps as defense in depth |

## Related Patterns

- **Pattern-062 (Assembly Assumption)**: Parent pattern. Pattern-063 is the specification-layer instance.
- **Pattern-064 (Extension Without Integration)** — Architect, planned: sibling sub-pattern at the integration-contract layer.
- **Pattern-045 (Green Tests, Red User)**: Verdict-convergence-as-dangerous-signal cross-cuts here. Tests passing while users fail is the same shape as rubric verdicts agreeing while methodology diverges.
- **Pattern-049 (Audit Cascade)**: Anchor-or-branch is one of the discipline checks an audit cascade can run on canonical extensions.

## Evolution

### Discovery (April 26, 2026)
PPM noticed during Phase E scoring exchange that PPM (using CT v2) and CXO (using Phase E draft rubric) had diverged on the C-axis with different criteria but converging verdicts. Filed `memo-ppm-to-cxo-lead-cio-cc-pm-pa-arch-exec-rubric-c-axis-reconciliation-2026-04-26.md` framing the drift as a discipline issue per PM's Apr 26 directive on terminology drift.

### Naming and Methodology Framing (April 26, 2026)
CIO responded with `memo-cio-to-ppm-cc-cxo-lead-pm-pa-arch-exec-rubric-drift-methodology-2026-04-26.md` naming the pattern as "Parallel-Authoring Drift" and proposing it as Pattern-062 at the methodology layer. CXO concurred on substance + belt-and-suspenders rule embedding.

### Slot Conflict and Resolution (April 26–27, 2026)
Predecessor Architect's handoff (Apr 25) had reserved Pattern-063 for a related but distinct sub-pattern of 062, "Extension Without Integration" (single-path extension, integration-contract layer). Architect filed a slot-conflict memo Apr 26 noting both patterns were legitimate sub-instances of 062 and recommending CIO take Pattern-063 (fully drafted) while predecessor's claim shifts to Pattern-064 (to be formalized). PM concurred Apr 27.

The slot conflict was itself a meta-instance of Pattern-063 at the catalog-management layer: parallel-authoring drift around the catalog's next-available slot reservation.

### Filing (April 27, 2026)
Filed under CIO self-approval authority per `methodology-audit-policy-updates-2026-03-16.md` with PM concurrence on slot allocation.

## Success Metrics

- **Time-to-detect drift**: window between divergent extensions shipping and the drift being surfaced. Lower is better; trend toward zero indicates the discipline is operating at authoring time, not at application time.
- **Branch decisions per audit cycle**: count of explicit branches (vs. silent extensions) when authors adapt canonical artifacts. Higher branch count is healthy; it means authors are exercising the choice rather than defaulting to silent extension.
- **Cross-application reconciliation incidents**: instances like the Apr 26 C-axis case where parallel artifacts produce divergent results on the same case. Should trend toward zero as the discipline propagates.
- **Verdict-convergence false-positives** (harder to measure, more important): cases where parallel artifacts agree on output but diverge on method. Detection requires deliberate cross-application; if we never do the cross-application, we never see them. The diagnostic question (*"would each author score the other's work the same?"*) is the operational tool.

## References

### Canonical Documents

- **CIO methodology framing memo (Apr 26)**: `mailboxes/cio/sent/memo-cio-to-ppm-cc-cxo-lead-pm-pa-arch-exec-rubric-drift-methodology-2026-04-26.md`
- **PPM reconciliation memo (Apr 26)**: `mailboxes/cio/read/memo-ppm-to-cxo-lead-cio-cc-pm-pa-arch-exec-rubric-c-axis-reconciliation-2026-04-26.md`
- **CXO concurrence memo (Apr 26)**: `mailboxes/cio/read/memo-cxo-to-cio-cc-ppm-lead-pm-pa-arch-exec-pattern-063-and-rule-embedding-2026-04-26.md`
- **Architect slot-conflict memo (Apr 26)**: `mailboxes/cio/read/memo-arch-to-cio-pm-cc-cxo-lead-ppm-pa-exec-pattern-063-slot-conflict-2026-04-26.md`
- **CIO slot-resolution memo (Apr 27)**: `mailboxes/cio/sent/memo-cio-to-arch-cxo-cc-pm-ppm-lead-pa-exec-pattern-063-slot-and-rule-2026-04-27.md`

### Methodology Lineage

- **Excellence Flywheel v2.0**, Practice 5 ("Audit the Composition"): the parent methodology principle from which Pattern-062 + Pattern-063 + Pattern-064 derive.
- **PDR-004 paraphrase-drift incident** (Apr 16, 2026): the canonical model for same-week-safeguard installation. The `create-omnibus` skill Step 7 (canonical-term verification) is the analog at the omnibus-synthesis layer of what branch-or-anchor is at the rubric/specification layer.
- **CIO M1 methodology audit** (`dev/2026/04/17/methodology-audit-2026-04-17.md`): the audit that formalized "Audit the Composition" as the Flywheel's 5th practice and prefigured this pattern's emergence.

### Operational Implementation

- **Colleague Test v2.3** (CXO, forthcoming): will embed the branch-or-anchor rule in the rubric document's "How to extend this rubric" section.
- **Methodology-core entry** (CIO, forthcoming): will state the rule as a standalone methodology principle.

---

*Pattern created: April 27, 2026*
*Origin: Apr 26 Phase E rubric C-axis reconciliation incident*
*Author: CIO, with PPM + CXO + Architect cross-input*
*Status: Emerging (CIO self-approval, PM concurrence on slot)*
*Promotion criterion: one full cycle of trial application surfacing whether the diagnostic question and branch-or-anchor rule produce reliable catches in practice. Phase F+ scoring is the natural test environment.*
