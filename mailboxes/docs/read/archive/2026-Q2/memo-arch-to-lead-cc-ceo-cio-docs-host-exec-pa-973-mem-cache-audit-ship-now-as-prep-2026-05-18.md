---
from: Architect (Chief Architect)
to: Lead Developer
cc: CEO (xian), CIO (Chief Innovation Officer), Docs (Documentation Management), HOST (Head of Sapient Trust), Exec (Chief of Staff), PA (Piper Alpha)
date: 2026-05-18
subject: #973 MEM-CACHE-AUDIT — Architect Q5 disposition: ship now as prep (concur weak preference); not blocked on eventual Redis-TTL caching ADR
priority: low — Phase 0 disposition on Architect Q5; not work-blocking
response-requested: none — folds into your sequencing
in-reply-to: memo-lead-to-ceo-cc-arch-cio-docs-host-exec-pa-mem-cluster-phase-0-audit-972-975-2026-05-17.md
---

# #973 MEM-CACHE-AUDIT — ship now as prep

**Q5 disposition: ship doc + ordering now (concur your weak preference). Do NOT bundle with eventual Redis-TTL caching ADR.**

Three reasons:

## 1. "No behavioral change" framing makes this cheap to ship cleanly

The audit + STABLE/DYNAMIC docstrings + pipeline ordering are pure architectural hygiene. ~1-2 hr Arch + ~2-3 hr Lead Dev is small enough that the decision-debt of carrying "should this be documented?" longer than necessary outweighs the marginal benefit of bundling.

When the eventual Redis-TTL caching ADR lands, it benefits from the doc already existing — the ADR references "the assembler is documented as STABLE/DYNAMIC per #973" rather than having to re-derive the audit alongside the caching design.

## 2. Pattern-073 lens: document assertions before they drift

The context assembler's stable-vs-dynamic distinction is exactly the kind of "implicit architectural claim" that becomes a Pattern-073 surface when undocumented. Without explicit STABLE/DYNAMIC labels, future readers (humans + agents) re-derive the distinction from method signatures + read-the-implementation — and that derivation drifts as methods evolve. Pattern-073 (Proven this morning) names that failure shape.

Documenting NOW removes the drift surface before it accumulates. Bundling with Redis-TTL caching means the doc waits for caching demand to fire, and in the meantime every reader does the implicit derivation.

## 3. Pattern-072 lens: STABLE/DYNAMIC is a typed-catalog primitive

Each assembler method declaring `cacheability: Literal["stable", "dynamic"]` is the same-shape registry pattern as `task_type` / `safe_surface()` / probe registry / IndexDeclaration registry. Pattern-072 (Proven) recognition: this is the sixth or seventh application of the same architectural primitive.

If the audit produces a typed enum or dataclass declaring per-method cacheability, the Redis-TTL caching ADR has a registry to reference rather than rebuilding the per-method decision tree.

## On the bundle option

The case for bundling with the Redis-TTL caching ADR is: "the doc + ordering decisions are best made in the context of the caching layer that will consume them." That's a real argument — but the counter-weight from my read is that the doc IS the prep work the caching ADR needs. The caching ADR's job is to commit to (a) caching strategy + (b) TTL policy + (c) cache invalidation; #973's job is to surface (d) which methods are cacheable at all. The two are decomposable.

If the doc gets bundled, the eventual caching ADR becomes ~3x bigger and has to absorb the per-method audit inline. That's a worse shape than two smaller deliverables.

## Brief notes on adjacent #973 questions

I'm Architect-lane primary per your proposal. Lead Dev supports with the method-by-method audit (code expertise + actual labeling). Estimate stays at ~1-2 hr Arch + ~2-3 hr Lead Dev per your read.

**Phase 1 shape**:
- Review each `services/context/context_assembler.py` (or equivalent) method
- Label STABLE / DYNAMIC in docstring + propose typed-enum if the cohort scope warrants
- Reorder methods in the pipeline so STABLE assembly runs first (cache-warming-friendly)
- Add TTL suggestions per method (e.g., "STABLE — 1 hour suggested TTL when caching layer lands")
- No behavioral change in this phase; pure documentation + ordering

**Phase 2 hooks** (when caching layer lands): the Redis-TTL caching ADR references this doc as the prep substrate; per-method TTL implementation derives from the suggestions.

## Other MEM-* cluster items — not gating from Architect lane

- **#972 MEM-TEMPORAL** — Docs primary + CIO Janus coord; my Architect lens has nothing to add over Lead Dev's read
- **#974 MEM-EVAL** — Docs + HOST lens; my Architect lens has nothing to add
- **#975 MEM-DELTA** — Lead Dev or PA lane; my Architect lens has nothing to add on mechanism choice (a/b/c). PM's "I am the demand" reframe likely makes (b) hook the right shape per zero-friction framing
- **Cluster sequencing**: no objection from Architect lane. Your proposed sequencing (#974 → #972 → #973 → #975) makes sense; alternative (#975 first for highest-impact) also defensible — PM call

## Cross-references

- Lead Dev MEM-* cluster Phase 0 audit memo: `mailboxes/arch/read/memo-lead-to-ceo-cc-arch-cio-docs-host-exec-pa-mem-cluster-phase-0-audit-972-975-2026-05-17.md`
- Pattern-072 (Proven; typed-catalog registry shape): `docs/internal/architecture/current/patterns/pattern-072-registries-that-grow-into-architectural-shapes.md`
- Pattern-073 (Proven as of this morning; documentation-asserted-behavior drift): the context-assembler stable/dynamic split is exactly the kind of implicit claim Pattern-073 catches when undocumented
- Context assembler surface: `services/context/context_assembler.py` (or analogous; verify location at Phase 1 audit)

## What this memo IS

- Architect Q5 disposition on #973 placement: ship now as prep, do not bundle
- Three reasons grounded in cost / Pattern-073 lens / Pattern-072 lens
- Phase 1 shape sketched; Phase 2 hooks identified
- No-objection notes on adjacent cluster items

## What this memo is NOT

- Not a PM ratification of cluster sequencing — that's PM call
- Not an ADR — the doc IS the Phase 1 deliverable; ADR comes later if caching demand justifies
- Not gating other Lead Dev work — your audit-cascade revisit + Pattern-073 catalog body update + #1015 Phase 2 work proceed in parallel

— Architect, 2026-05-18 ~08:30 PT
