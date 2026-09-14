# #1788 executed 6 of 7 — and the lane disagrees with you on DocumentDB, with evidence I've verified

**From**: Lead · **Date**: 2026-09-13 ~22:1x PT · **Cc**: ppm, xian (ceo)

Your ruling is executed for six of seven models. The seventh stopped on the disagreement
clause I briefed, and I've independently checked the load-bearing facts rather than relaying
them — they hold.

**The five cat-(2) twins: your call confirmed by an independent census**, including your
domain-`Intent` count of 26 reproduced exactly. Checker configured off with your reason line,
printed every run, plus a stale-entry guard that fails the build if an entry outlives its
model. Disposal issue **#1797** filed for the five as a set. `SessionActivityDB` converter
written, read path verified rather than assumed (`list_for_session` → `row.to_domain()` →
three live consumers), 7 round-trip tests against a real DB with a negative control.

**Two small corrections to the evidence, neither changing the ruling**: "zero importers
outside their own module" is imprecise — the five have in-package importers, but those form a
closed dead subgraph (nothing imports `from services.database import …`; the repo classes and
`RepositoryFactory` have zero external callers). The precise claim is **zero live consumers**.
And #1788's "zero repository-layer conversion hits" was wrong: `TaskRepository.create_from_domain`
is exactly that, with zero callers.

## The disagreement: DocumentDB

**Your discriminator was measured on one side only.** `DocumentDB` is live — one real importer,
as you found. But its **domain twin is dead**: I checked, and domain `Document` has zero
importers across `services/` + `web/`; its only production references are
`Artifact.from_document`/`to_document` inside `models.py` itself.

**And the two classes are not the same thing.** Domain `Document` is content-bearing
(`content: str` is its central field). `DocumentDB` has no content column at all — its own
docstring says it is the **ADR-071 D2 owner-anchor row** for the ChromaDB-only doc store,
linked by `chromadb_base_id`.

**So a `from_domain()` here would have to invent `chromadb_base_id`** — a NOT NULL unique
natural key the domain object has no concept of — **and would drop `owner_id` and
`is_global_pm_domain`, the D1/D2 security fields.** That is a converter whose signature
promises a round-trip it cannot perform, on the row that anchors ownership. Worse shape than
the five dead twins, not better.

**The generalizable point, which I'd want in the ruling either way: liveness must be measured
on BOTH sides.** A live DB class with a dead domain twin fails the round-trip test exactly as
a dead DB class with a live domain twin does — your `Intent` case, inverted.

**Your call, two options**: (a) re-rule DocumentDB as cat (2) — a sixth registry entry, which
also opens the separate question of what dead domain `Document` is for; or (b) cat (1) stands
and the converter gets written with the security fields handled explicitly, in which case
please say how `owner_id` should be resolved, because the lane must not guess at an ownership
field.

PM-056 job 2 is **honestly red on DocumentDB alone** — down from 13 issues across 7 models to
2 across 1. It cannot go green until this is ruled, and I'd rather it stay red and accurate.

— Lead
