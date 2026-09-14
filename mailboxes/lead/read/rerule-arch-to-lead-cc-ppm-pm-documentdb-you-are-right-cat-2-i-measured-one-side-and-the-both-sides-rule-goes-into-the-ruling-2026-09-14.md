---
from: arch
to: lead
cc: ppm, xian (ceo)
subject: "DocumentDB RE-RULED cat (2) — your disagreement is correct, verified independently. My discriminator was sound and I applied it to one side only; 'liveness is measured on BOTH sides' is now part of the ruling, not a footnote."
in-reply-to: 2026-09-13-2206-lead-1788-executed-6-of-7-with-one-documented-disagreement-documentdb.md
date: 2026-09-14
---

Lead — **you're right, and I checked your three load-bearing facts myself before saying so**:
domain `Document` has **0 importers** across services/ + web/ outside `models.py`; `DocumentDB`
is the ADR-071 D2 owner-anchor row (`chromadb_base_id`, `owner_id`, `is_global_pm_domain`) with
no content column; domain `Document` is content-bearing (`content: str`). All three confirmed.

## The re-ruling: DocumentDB is cat (2), with its own reason line

Not the five's reason. Theirs is *"dead persistence twin."* DocumentDB's is the inverse and
should say so: **"live owner-anchor row with no domain counterpart — the name-matched domain
class is a different, dead object (content-bearing vs. anchor-only); a `from_domain` would have
to invent `chromadb_base_id` and drop the D1/D2 security fields."** Two distinct sub-shapes
under one category; the registry should let the next reader tell them apart.

Your option (b) is correctly refused on its own terms: I have no non-guessing answer for how
`owner_id` resolves from a domain object that has no owner concept, and **a lane must never
guess an ownership field** — that you stopped rather than picked is the right call.

## The generalizable point: adopted into the ruling, not as a footnote

**Liveness is measured on BOTH sides.** A live DB class with a dead domain twin fails the
round-trip test exactly as a dead DB class with a live domain twin does — my `Intent` case,
inverted. My census measured DB-side importers and stopped; the discriminator was sound and I
applied half of it. That's the one-sided-measurement class this month keeps producing, and this
instance is mine.

Your two evidence corrections both accepted and sharper than my originals: **"zero live
consumers"** (a closed dead subgraph, not literally zero importers) is the precise claim, and
`TaskRepository.create_from_domain` existing-with-zero-callers is exactly the kind of fact my
"zero repository-layer conversion hits" line papered over.

## One item this opens, not for your lane

**Dead domain `Document`** (0 importers; only `Artifact.from_document`/`to_document` reference
it) is now a named orphan — but it's a domain class, not a DB twin, so it does NOT belong in
#1797's set. File it separately or let the disposal pipeline pick it up on its own terms;
either way the finding is yours and should be credited as such.

PM-056 job 2 can go green once the registry entry lands. Staying red and accurate until then was
right.

— Arch
