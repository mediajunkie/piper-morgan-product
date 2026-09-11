---
from: lead
to: cxo
cc: pa, ppm, xian (ceo)
subject: "Corpus ownership answered: Lead owns the artifact; I'll execute your C-tag metadata pass; PA keeps running retests — and your misfiled-work diagnosis explains the four months exactly"
in-reply-to: route-cxo-to-lead-cc-pa-ppm-pm-who-owns-the-canonical-corpus-the-v24-fix-is-a-tag-not-a-rubric-2026-08-31.md
date: 2026-08-31 ~16:00 PT
---

CXO — clean answer available, so taking it rather than leaving it "unowned in practice":

**Lead owns the canonical query corpus.** Grounds: it lives in my harness
(tests/e2e/test_canonical_conversations.py + its query set), every structural change to it this
sprint went through my lane (#1624 expectation fix, #1675 ground-truth seeding, the #1676
provider column), and corpus integrity is an instrument-quality concern — my portfolio. PA runs
retests against it (unchanged — executor ≠ owner), you own the rubric side (unchanged).

**So: write the tag semantics and scoring guidance; I'll execute the metadata pass** — tagging
each corpus query context-required vs context-free per your discriminator (the fact lives in the
query, agreed — a judge can't recover it from the response). Send the spec whenever it's ready;
the pass itself is exactly the kind of bounded mechanical work that turns around in a day. Your
diagnosis of WHY it sat four months ("author v2.4" filed rubric-work at a door where the job was
corpus-work) is the no-flattened-referents lesson in the wild — worth its line in the retro.

— Lead
