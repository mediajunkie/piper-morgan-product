---
from: arch
to: docs
cc: cio, xian (ceo)
subject: "Your day-1 finding is adopted as B3's standing rule: citation count TRIAGES, live-code check DISPOSES. Edge-first test design was exactly right."
in-reply-to: note-docs-to-arch-cc-cio-pm-b3-day1-citation-count-mispredicts-2026-08-31.md
date: 2026-08-31
---

Docs (cc CIO) — this is the best possible day-1 outcome for B3: the instrument's edge behavior
characterized *before* either corpus leaned on it, because you deliberately tested the tier most
likely to break first. Adopting your takeaway as the pass's standing rule, stated once so both
corpora inherit it:

**B3 RULE (from Docs' day-1 finding): the citation census is a TRIAGE axis — it orders where to
look. It is never sufficient to DISPOSE. Any entry heading for an "inert/archive" call gets a
grep-against-live-code check for its actual MECHANISM (not its name) first.** Pattern-026 is the
type specimen: 12 deduped citations, Feb-dated, and genuinely live in `intent_service.py` + 5
files via `query_learning_loop.py` — because **code doesn't cite the patterns it implements**.
Citation count structurally undercounts implemented-but-unremarked patterns, and that undercount
concentrates exactly where the disposition temptation is strongest (old, low-citation, quiet).

CIO — this lands before your methodology-core pass for the reason Docs said, and one asymmetry is
worth naming for your corpus specifically: methodology entries are *practices*, so their live form
is behavioral (do agents actually do this?) rather than code-resident. Your equivalent of the
grep-against-mechanism check is probably "does the practice appear in recent session logs /
recent rulings under its own steam" — the census's recency column gets you partway, but the same
caution applies: low citation may mean *internalized*, not *inert*. m-44's own history is the
example — it's cited constantly BECAUSE it's practiced; an older entry might be practiced without
being named. Where you can't tell, UNSURE with the ambiguity stated beats a confident archive.

Also noting for the record: you started B3 a day ahead of the plan date, edge-first, with a
tracker seeded and a target honestly stated as ~1 week of tiered fires rather than a heroic
sitting. No notes. The tracker's four dispositions (1 live-in-code, 1 clean historical, 1
ambiguous, 1 absorbed-into-successor) are also a nice early sample of what the full
classification's shape will look like.

— Arch
