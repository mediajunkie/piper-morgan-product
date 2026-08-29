# Branch-or-Anchor Discipline

## Overview

The **Branch-or-Anchor decision rule** is a methodology principle for any author about to extend a canonical reference (rubric, schema, contract, principle, vocabulary, slot allocation). The rule forces an explicit choice between two paths and forbids a third, silent path:

- **Anchor**: cite the canonical doc by version, use it unchanged. If the canonical doesn't fit local needs, branch.
- **Branch**: rename the local artifact explicitly, version it as a derivative, document the deviation. The new name signals to all downstream consumers that this is no longer the canonical artifact.
- **(Forbidden) Silent extension**: using the canonical's label while changing the criteria.

The rule was formalized April 2026 in response to the Phase E rubric C-axis incident. It is the structural fix for **Pattern-063 (Parallel-Authoring Drift)** — a sub-pattern of Pattern-062 (Assembly Assumption) at the specification layer.

## Why This Methodology

### The Failure Mode (Pattern-063)

When a canonical reference is extended in parallel by two or more authors, each acting in good faith and producing individually correct work, the extensions can diverge silently at the semantic layer while appearing convergent at the surface layer. The failure becomes visible only when the parallel artifacts are applied to the same case and produce divergent results — by which point both have propagated to downstream consumers.

The Apr 26 canonical example: Phase E rubric (Lead Dev, Apr 23) and Colleague Test v2 (CXO, Apr 25) both used the letter "C" for the middle scoring axis with materially different criteria (Clarity vs. Context). Both authored in good faith. Both individually correct. Surface convergence (same label) masked semantic divergence (different criteria) until the same transcripts were scored under both rubrics and produced systematically different C-axis scores.

### The Discipline Question

When you're about to extend a canonical reference, the right question is not "what should I add?" — it's "anchor or branch?" The decision is structural: either you're using the canonical as-is (cite and use) or you're creating a new artifact (rename and version). Silent extension is the path between these two that produces parallel-authoring drift.

## When to Apply

### Apply this rule when

- Drafting a new rubric or scoring instrument that adapts an existing canonical rubric
- Defining a contract or schema that extends a shared canonical contract
- Coining vocabulary derived from canonical terms (especially methodology vocabulary, principle names, axis labels)
- Reserving a slot in a shared catalog (pattern numbers, ADR numbers, methodology numbers, issue ranges)
- Creating any artifact that downstream consumers will conflate with the canonical if the surface looks similar

### This rule does not apply when

- You are versioning the canonical itself (v1 → v2 with full ownership and downstream coordination)
- The new artifact is genuinely independent of any canonical reference
- The canonical is being deprecated and replaced (this is a versioned upgrade, not a parallel extension)

## Core Principles

### 1. Anchor explicitly when anchoring

When you choose to anchor, the citation must be unambiguous:

- Reference the canonical doc by **path AND version** in the consuming artifact's metadata or opening section
- Do not paraphrase the canonical criteria in the consuming artifact (cite, don't restate)
- If the consuming artifact needs to be self-contained (e.g., a scoring instrument that the scorer reads in isolation), include a verbatim block of the relevant canonical criteria with attribution, not your own paraphrase

**Example (anchor)**: A Phase F scoring rubric document that says: *"Use Colleague Test v2.3 (`docs/internal/testing/colleague-test-rubric.md` as of commit `<sha>`) without modification. Score on the R/C/T axes as defined there. No local adaptations."*

### 2. Branch explicitly when branching

When you choose to branch, the rename must signal divergence to downstream consumers:

- New artifact has a **new name** that does not collide with the canonical's label
- Metadata includes **derivation lineage**: "Derived from `<canonical>` v`<version>` with the following deviations: `<list>`"
- Downstream consumers can see at a glance that this is a derived artifact, not the canonical

**Example (branch)**: A future activation gate that genuinely needs Clarity-as-distinct-axis: *"Activation-Gate Clarity Rubric v1, derived from Colleague Test v2.3 R/C/T with C=Clarity replacing C=Context. Used only for activation-gate scoring; does not supersede CT v2.3 for general use."*

### 3. Silent extension is the failure mode this rule prevents

If you find yourself adapting a canonical doc and you are *not* explicitly citing-as-anchor or renaming-as-branch, you are silently extending. Stop. The drift you are about to introduce will not be visible until the next application of the parallel artifacts produces divergent results.

## Diagnostic Tools

### The author's question (apply at authoring time)

> *"Am I citing this canonical reference unchanged, or am I creating a new artifact?"*

If "neither," you are about to silently extend. Choose one explicitly.

### The reviewer's question (apply at cross-application)

> *"If I asked the two authors to score each other's work using the other's rubric, would they get the same answer?"*

If "I'm not sure," parallel-authoring drift is likely operating. The agreement on outputs tells you nothing; the divergence is at the semantic layer.

### The verdict-convergence diagnostic (cross-cuts to Pattern-045 + Pattern-062)

> *"What would have to be true for these to be wrong in the same direction?"*

When two divergent methods produce the same answer, agreement-on-output ≠ validation-of-process. The answer is robust to method variation in the trivial cases — which tells you nothing about the non-trivial cases.

## Implementation Surfaces (Belt-and-Suspenders)

The rule lives in two complementary places, because the populations of authors that consult them do not fully overlap:

### Surface 1: Methodology-core entry (this document)

For authors who consult methodology *before* drafting an extension. Standalone, searchable, durable.

### Surface 2: Embedded "How to extend this" section in canonical documents themselves

For authors who go directly to the canonical to extend it (the actual high-failure path — Lead Dev's Apr 23 Phase E rubric drafting was exactly this pattern). The embedded note is read-by-default for anyone using the canonical; the methodology-core entry requires deliberate consultation.

**Operational example**: Colleague Test v2.3 (CXO, forthcoming) will include a "How to extend this rubric" section above Provenance, stating the branch-or-anchor rule explicitly with one worked example.

Both surfaces close the loop. Authors who consult methodology before drafting hit Surface 1; authors who jump straight to the canonical hit Surface 2.

## Complementary Operational Hygiene (Not Sufficient Alone)

These are useful but secondary to the underlying discipline:

| Hygiene | What it does | What it doesn't do |
|---|---|---|
| **Naming-collision grep** at authoring time | Catches accidental label collisions cheaply | Doesn't address the deeper question of whether you should branch |
| **Version-stamp norm** in artifact metadata | Makes drift detectable post-hoc | Doesn't prevent the drift |
| **Canonical-reference registry** | Aids discovery of canonical artifacts | Itself an extension surface that can drift |

The discipline is "anchor or branch, never silent." The hygiene tools are defense in depth, not substitutes.

## Anti-Patterns

| Don't Do This | Why | Do This Instead |
|---|---|---|
| Adapt a canonical's label with new criteria silently | Silent extension is the failure mode this rule prevents | Branch with explicit rename, or anchor without modification |
| Defer reconciliation to "v2.x" when drift is noticed | Silent drift compounds during the deferral window | Treat the moment of noticing as the discipline issue; reconcile immediately |
| Trust verdict-convergence on parallel artifacts as validation | Agreement on outputs ≠ agreement on methodology | Apply the diagnostic question; cross-application is the only validation |
| Reserve catalog slots informally in handoffs | Soft reservations fail under parallel authoring (the Apr 26 Pattern-063 slot conflict is itself a meta-instance) | Take the next available number when you formalize, or claim the slot with a visible filed artifact |
| Implement only registry/version-stamps without the underlying rule | Diagnostic aids don't prevent the failure mode they help detect | Branch-or-anchor first; registry/stamps as defense in depth |

## Related Patterns and Methodologies

- **Pattern-063 (Parallel-Authoring Drift)**: The pattern this rule addresses. `docs/internal/architecture/patterns/pattern-063-parallel-authoring-drift.md`.
- **Pattern-062 (Assembly Assumption)**: The parent pattern. Pattern-063 is the specification-layer instance.
- **Pattern-045 (Green Tests, Red User)**: Verdict-convergence-as-dangerous-signal cross-cuts here.
- **Methodology-00 (Excellence Flywheel) Practice 5 ("Audit the Composition")**: The parent methodology principle.
- **PDR-004 paraphrase-drift correction chain (Apr 16, 2026)**: The canonical model for catching canonical-vocabulary drift in published prose. The branch-or-anchor rule is the analog at the rubric/specification layer.
- **`create-omnibus` skill, Step 7 (Verify Canonical References)**: Operational implementation of the same discipline at the omnibus-synthesis layer.

## Evolution

### Origin (April 26, 2026)
Phase E rubric C-axis incident: Phase E rubric (Lead Dev, Apr 23) and Colleague Test v2 (CXO, Apr 25) drifted on the C-axis label (Clarity vs. Context). PPM caught the drift during scoring exchange and framed it as a discipline issue per PM directive on terminology drift.

### Rule Naming (April 26, 2026)
PPM's reconciliation memo proposed three candidate safeguards. CIO's methodology framing memo named the branch-or-anchor decision rule as the structural fix and recommended adoption as methodology-core entry. CXO concurred and proposed belt-and-suspenders embedding (methodology-core + canonical-doc-embedded).

### Filing (April 27, 2026)
Methodology-core entry filed under CIO authority with PM concurrence. Pattern-063 (Parallel-Authoring Drift) filed concurrently as Emerging. Colleague Test v2.3 to land with embedded "How to extend this rubric" section per CXO.

### Promotion Criteria
This methodology entry stays in current state until one full cycle of trial application surfaces whether the rule and diagnostic question produce reliable catches in practice. Phase F+ scoring is the natural test environment. Promotion would mean wider citation across non-rubric canonical artifacts (schemas, contracts, slot allocations).

## References

### Canonical Documents

- **Pattern-063 catalog entry**: `docs/internal/architecture/patterns/pattern-063-parallel-authoring-drift.md`
- **PPM reconciliation memo (Apr 26)**: `mailboxes/cio/read/memo-ppm-to-cxo-lead-cio-cc-pm-pa-arch-exec-rubric-c-axis-reconciliation-2026-04-26.md`
- **CIO methodology framing memo (Apr 26)**: `mailboxes/cio/sent/memo-cio-to-ppm-cc-cxo-lead-pm-pa-arch-exec-rubric-drift-methodology-2026-04-26.md`
- **CXO belt-and-suspenders concurrence (Apr 26)**: `mailboxes/cio/read/memo-cxo-to-cio-cc-ppm-lead-pm-pa-arch-exec-pattern-063-and-rule-embedding-2026-04-26.md`
- **CIO slot-resolution memo (Apr 27)**: `mailboxes/cio/sent/memo-cio-to-arch-cxo-cc-pm-ppm-lead-pa-exec-pattern-063-slot-and-rule-2026-04-27.md`

### Operational Implementation

- **Colleague Test v2.3** (CXO, forthcoming) — embedded "How to extend this rubric" section.
- **`create-omnibus` skill Step 7** — analog operational implementation at omnibus-synthesis layer.

---

*Methodology entry created: April 27, 2026*
*Origin: Apr 26 Phase E rubric C-axis reconciliation incident*
*Author: CIO (with PPM, CXO, Architect cross-input)*
*Status: Filed under CIO authority with PM concurrence*
