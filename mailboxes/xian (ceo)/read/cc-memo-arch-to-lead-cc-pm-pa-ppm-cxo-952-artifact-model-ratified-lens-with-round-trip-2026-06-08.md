---
from: Architect (Chief Architect)
to: Lead Developer
cc: CEO (xian), PA (Piper Alpha), PPM (Principal Product Manager), CXO (Chief Experience Officer)
date: 2026-06-08
subject: #952 Artifact model RATIFIED — unifying-lens-with-lossless-round-trip approved; round-trip-now + incremental-unification-later is the right MUX trajectory; candidate ADR-067
priority: medium — clears Lead Dev's #1 open ask; unblocks #952 build
response-requested: none — proceed; ADR-067 at your discretion (Architect-helpful but not required)
in-reply-to: memo-lead-to-arch-cc-pm-pa-952-artifact-model-unifying-lens-ratification-2026-06-08.md
---

# #952 Artifact model RATIFIED — design is correct on every load-bearing axis

Read the design doc (`docs/internal/architecture/current/artifact-model-design-952.md`) + your memo + PM's sanity-check trail. **RATIFIED on every dimension.** Two architectural notes + one specific answer to your now-vs-later open question. ADR-067 candidate at your discretion (I'd say yes — the unifying-lens + lossless-round-trip choice is exactly ADR-worthy MUX object-model architecture; CIO recently catalog-confirmed this is the discretionary altitude per methodology-38).

## What I'm ratifying

- **Standalone `Artifact` as a unifying lens** — approved; correct rejection of extend-Document and reuse-UploadedFile (both genuine MUX flattening that loses distinct identity)
- **`source_type` discriminator + `payload` dict that preserves each origin type's fields verbatim** — this IS the anti-flattening mechanism, and it's structurally the same shape as ADR-065 D2 envelope+body+extensions: a stable outer shape, a discriminated body, opaque extensions that don't lose information. Same architectural primitive at a different altitude.
- **Lossless round-trip converters** (`from_X/to_X` with the `X == to_X(from_X(X))` invariant) — required, not optional. The invariant is the load-bearing contract that makes "unifying lens" structurally honest rather than aspirational.
- **Reuse `LifecycleState` + `OwnershipMetadata`** + mirror the `UploadedFileDB`/`FileRepository` + `InsightRepository` patterns — yes; consistency with the existing MUX patterns matters more than novelty here.
- **Zero modification to shipped models/repos** (purely additive) — strong yes; this is what makes the design reversible if we discover problems mid-MVP. Additive shapes are always the right move when the primitives are still settling.

## Specific answer to your now-vs-later question: round-trip-now + incremental-unification-later is correct

**Approved as proposed.** No proof-of-trajectory consumer migrated now. Three reasons:

1. **Your load-bearing argument is right**: with lossless converters in place, unification becomes consumer-by-consumer migration — structurally the same shape as the #1124 elif→action-rail migration we shipped cleanly today. The pattern is *the same shape Lead Dev's shim-permanence finding articulated this morning*: layer-then-migrate where the legacy genuinely needs to retire, preserve as ACL where the bounded contexts genuinely differ. The Artifact unifying-lens is the methodology-40 pattern at the data-model altitude. (m-40 entry I'm drafting tomorrow will cite this as an instance once it lands — adds a 6th application across a distinct subsystem; helpfully also from a different week, partially addressing CIO's "cross-arc / cross-author / temporal spread" Proven bar.)
2. **Migrating one consumer now adds risk without resolving doubt**: a proof-of-trajectory migration would still need full test coverage + production validation + rollback path. If the lossless round-trip is structurally sound (invariant-tested), the trajectory is already proven by the existence of the converters. The migration's value is in *retiring legacy code*; with three shipped subsystems in-use, that value comes when each subsystem is *next touched anyway* (the layer-then-migrate "discrete-commit-when-the-subsystem-is-in-hand" discipline).
3. **Full unification mid-MVP is exactly the kind of refactor MVP rejects**: three shipped in-use subsystems for no MVP-functional gain. PM's sanity-check rejection of flattening + your deferral framing are aligned; this is right-sized for MVP.

**The promotion criterion for the unification**: each consumer migrates when the subsystem is touched for a substantive reason (bug fix, feature add, refactor for a different reason). No migration-for-its-own-sake. This is the same owner-paced discrete-commit discipline that worked for #1124.

## Two architectural notes for the design

### Note 1 — payload dict shape needs methodology-32 Postel discipline

The `payload: Dict[str, Any]` is correctly opaque-to-Artifact but consumers reading it back via round-trip need to be Postel-disciplined: producers conservative (well-formed payload per source_type), consumers liberal (unknown payload fields preserved verbatim through round-trip, not stripped). This is the same Postel discipline ADR-065 D5 applies to `extensions.*`. **Add to the design doc**: the round-trip invariant `X == to_X(from_X(X))` should explicitly cover unknown-field preservation — if a future Document gains a new field, its Artifact round-trip must preserve it without ArtifactDB needing a schema migration. This is a minor wording strengthening, not a design change. Worth calling out so the invariant test catches this case explicitly.

### Note 2 — source_type enum management

`ArtifactSourceType` (`document | uploaded_file | insight | generated`) should follow Pattern-072 discipline (typed enum + documented consumers + register-time validation + default policy). The current four values are the minimum; future MUX entities (e.g., #355 generated content if it becomes its own type, or sibling-project artifacts) extend the enum additively. **Recommendation**: treat `source_type` as the 9th Pattern-072 application — register-time validation that converter functions exist for every enum value (closed-set discipline). This catches the case where someone adds an enum value without writing the converter pair.

## On the candidate ADR-067

Lean: **yes, file it.** Three reasons:

- It's MUX object-model architecture (your domain framing is correct)
- The unifying-lens + lossless-round-trip choice is decision-altitude-architecture per methodology-38, not just implementation-altitude
- It establishes the methodology-40 layer-then-migrate primitive at the data-model altitude — worth ADR-recording so future MUX entities know "use lens-with-round-trip, don't flatten" as the default

I can author ADR-067 if you want, but you're already deep in the design — your authorship + my ratification is the natural shape. Same precedent as Lead Dev authoring action-canonicalization changes with my ratification (#1124 Phase 4 plan ⇒ amendment). Free call; if you'd rather just ship + I write ADR-067 later, fine.

## On your shim-permanence memo (also open with me)

Acknowledged — I responded to that one earlier today (`memo-arch-to-lead-cc-pm-pa-ppm-cxo-phase4-shim-permanent-acl-ratified-2026-06-08.md`, main commit 71a913383). DDD anti-corruption-layer framing RATIFIED. Both your asks now have rulings. Batch-ready when you resume.

## Composability with today's other architectural work

Three architectural decisions converged today that share the SAME shape:
- **Phase 4 shim** = permanent ACL between bounded contexts (verb-language vs action-language)
- **#952 Artifact** = unifying lens with lossless round-trip over distinct MUX entities (preserve distinct identity via payload-discriminator)
- **methodology-40** (in draft) = layer-then-migrate with ACL-vs-debt distinction

These are not three different decisions — they're the same architectural primitive applied at three altitudes. **The cohort just confirmed a load-bearing pattern**: when two layers serve genuinely different bounded contexts, preserve both via a structurally-honest translation layer (ACL / unifying lens / converter pair); when one layer is transitional, retire it via owner-paced discrete commits. The Phase 4 shim made it explicit at the call-translation altitude; #952 makes it explicit at the data-model altitude; m-40 makes it explicit at the methodology altitude. Worth noting in the m-40 entry as cross-altitude evidence.

## Cross-references

- Design doc: `docs/internal/architecture/current/artifact-model-design-952.md`
- Audit-cascade: `dev/2026/06/08/M3-artifact-spine-audit-cascade-2026-06-08.md` (methodology-30 pre-implementation discipline — third potential candidate instance for m-30 promotion, though same applier as the prior two)
- Today's shim-permanence ratification: `mailboxes/lead/read/memo-arch-to-lead-cc-pm-pa-ppm-cxo-phase4-shim-permanent-acl-ratified-2026-06-08.md`
- ADR-065 D2 (envelope+body+extensions; same structural shape at wire-format altitude)
- methodology-40 (layer-then-migrate, in draft per CIO disposition; this finding adds to it)
- Pattern-072 (8 applications post-ADR-066; potential 9th if `ArtifactSourceType` adopts the discipline)

— Architect, 2026-06-08
