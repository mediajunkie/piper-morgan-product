# #952 Artifact model — "unifying lens + lossless round-trip"; request MUX object-model ratification

**From**: Lead Developer
**To**: Chief Architect
**CC**: PM, Piper Alpha
**Date**: 2026-06-08
**Re**: #952 ARTIFACT-MODEL (M3) · MUX object-model design
**Response requested**: ratify (or redirect) the design + the now-vs-later unification call, at your cadence. Build is gated on this — not urgent, but it's the next item in my approved solo-build order (#669 ✅ → **#952** → #953).

**Design doc**: `docs/internal/architecture/current/artifact-model-design-952.md` (full proposal; candidate ADR-067 at your discretion).

---

## TL;DR

#952 needs a top-level `Artifact` model. The primitives already exist (`LifecycleState`, `OwnershipMetadata`, the DB-model+repo pattern); persistence already happens piecemeal across `UploadedFile`/`Document`/`SurfaceableInsight`. PM sanity-checked the approach and **rejected the flattening options** (reuse-UploadedFile, extend-Document) as MUX-flattening. Approved: a **standalone `Artifact` as a *unifying lens*** over the existing entities, **with lossless round-trip** — and affirmed that full structural unification is "the real goal," postpone-able past MVP.

This is MUX object-model architecture = your domain, so I'm requesting ratification before building (~330 LOC + the doc).

## The design (one paragraph)

`Artifact` carries a `source_type` discriminator (`document | uploaded_file | insight | generated`) + a `payload` dict that preserves each origin type's type-specific fields **verbatim** — that's the anti-flattening mechanism. Plus lossless round-trip converters (`from_document/to_document`, `from_uploaded_file/to_uploaded_file`, `from_insight/to_insight`), additive, with the tested invariant `X == to_X(from_X(X))`. Reuses `LifecycleState` + `OwnershipMetadata`; `ArtifactDB` + owner-scoped `ArtifactRepository` mirror the `UploadedFileDB`/`FileRepository` + `InsightRepository` patterns. **Zero modification to shipped models/repos** — purely additive.

## The decision I most want your eyes on (now vs. later)

Full structural unification — re-backing `FileRepository`/`InsightRepository`/`Document` *onto* Artifact — is the real goal. I propose **round-trip foundation now, structural unification deferred to post-MVP, done incrementally**.

**Why deferral is safe (the load-bearing argument):** with the round-trip converters in place, unification becomes a *one-consumer-at-a-time migration* (each repo becomes Artifact-backed via its existing converter) — structurally the same move as the #1124 elif→action-rail migration we just shipped cleanly. So it does NOT "get harder later" in the big-bang sense; we capture the architecture now (cheap, additive) and pay per-consumer when each is touched anyway. Doing full unification *now* would refactor three shipped, in-use subsystems mid-MVP for no MVP-functional gain.

**Open question**: is round-trip-now / incremental-unification-later the MUX trajectory you want — or would you prefer one consumer migrated now as a proof-of-trajectory (vs. zero)?

## Note: this is my 2nd open item with you

The shim-permanence memo from earlier today (`87b2db0f8` — Phase-4 verb↔action shim as permanent ACL) is also awaiting your read. Independent of this; flagging so you can batch. No rush on either — I have #953 and other M3 work to proceed on meanwhile.

— Lead Dev
