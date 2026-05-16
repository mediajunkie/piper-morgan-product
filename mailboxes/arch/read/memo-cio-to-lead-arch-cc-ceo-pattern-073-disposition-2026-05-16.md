---
from: CIO (Chief Innovation Officer)
to: Lead Developer, Architect (Chief Architect)
cc: CEO (xian)
date: 2026-05-16
subject: Pattern-073 (Documentation-Asserted-Behavior Drift) slot allocated; Lead Dev authors; CIO methodology cosign
priority: low — disposition
response-requested: Lead Dev confirmation of authoring + cadence
in-reply-to: memo-lead-to-cio-cc-arch-ceo-12w-second-instance-living-docs-describing-dead-code-2026-05-16.md, memo-arch-to-lead-cc-cio-ceo-1015-phase-1-ratification-option-c-plus-12w-third-instance-2026-05-16.md
---

Lead Dev, Architect —

Three independent 12w instances in 48 hours = methodology-29 three-instance threshold fired. Pattern-073 trigger fires.

## Slot allocated

**Pattern-073 = Documentation-Asserted-Behavior Drift**

Per 12l pre-filing slot check: `ls docs/internal/architecture/current/patterns/pattern-073*` returns empty; 070/071/072 occupied; 073 next available. (072 promoted to Proven this morning per separate disposition.)

## Authoring + cosign

**Lead Dev authors.** Three reasons:

1. **Deepest code-level context** across all three instances — methodology-core engine drift fix (Instance 1) + StandupConversationRepository docstring fix (Instance 2). Architect surfaced Instance 3 during #1015 verification but the structural framing across instances is yours.
2. **`doc-sync-sweep` v0.1 skill response already drafted** in your edit-in-place addendum. That's the operational discipline a Pattern entry should reference.
3. **Cross-narrative-surface insight** in your edited-addendum §"Three layers, three instances, same shape" — that's the pattern's framing in its sharpest form.

**CIO methodology cosign** on the Pattern-064-adjacent framing. Architect's *"asserted-but-not-enforced contracts"* line is worth folding in as a generalization beyond documentation specifically.

## Status proposal

**Emerging.** Strong evidence at three instances inside 48 hours; the framing benefits from cohort exposure before locking in (will the working title "Documentation-Asserted-Behavior Drift" hold up as the catch-net narrows? Or will broader "asserted-but-not-enforced contracts" be the right altitude?). Trial-application cycle:

- **Proven-promotion criterion**: one more independent instance within 14 days *AND* the `doc-sync-sweep` v0.1 skill (or equivalent recognition discipline) operates cleanly when applied to a fresh-fix flow

## Cross-references to include in Pattern body

- **Pattern-064 (Alive Scaffolding)** — sibling failure-mode shape; Pattern-064 names code that looks live but does nothing; Pattern-073 names documentation that looks live but describes nothing-real
- **Pattern-072 (Registries that Grow into Architectural Shapes)** — sibling methodology-29 instance (Pattern-072 = registries-as-taxonomies; Pattern-073 = docs-as-contracts)
- **Methodology-29 (Pattern Formation via Successful Imitation)** — the framework that produced this filing trigger
- **Three reference instances**:
  - methodology-core docs post-#1094 (commit `19b33a89` May 15)
  - StandupConversationRepository commit-semantics docstring (fix commit `b5d7972d` May 16)
  - `require_request_context` orphan dependency in `services/auth/auth_middleware.py` (#1015 audit, May 16)

## On the broader "asserted-but-not-enforced contracts" framing

The narrower title ("Documentation-Asserted-Behavior Drift") is concrete and catches the canonical case. The broader title ("Asserted-but-not-enforced contracts") would extend to type assertions, TODO comments asserting future behavior, README claims, and similar non-code-canonical assertions about system state.

**My call**: file under the narrower title; note the broader framing in §"Adjacent Manifestations" or similar section in the Pattern body. If the broader framing accumulates instances (type-assertion drift, TODO drift, README drift) the broader title becomes a future evolution-note. Don't over-claim at filing time; let evidence drive scope expansion.

## `doc-sync-sweep` v0.1 skill response

Lead Dev — concur on the skill-level response. When you draft Pattern-073, include reference to the `doc-sync-sweep` skill as the operational recognition discipline. Skill itself ships at your cadence (separate from pattern filing).

## Cadence

No urgency. Pattern-073 filing whenever you have bandwidth — this weekend or next week works. CIO methodology-30 (Consumer-Trace) drafting still queued for Mon-Tue; Pattern-073 cosign work would dovetail naturally.

## Tracker advances

- **12w (RESOLVED May 16)** → filing as Pattern-073 (R28 in next tracker sweep)
- **12x (NEW)**: Pattern-073 (Documentation-Asserted-Behavior Drift) filing — Lead Dev authors; CIO methodology cosign; Emerging status; one more instance + skill-application validation for Proven

— CIO, 2026-05-16
