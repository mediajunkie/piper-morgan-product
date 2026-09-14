---
from: arch
to: lead
cc: ppm, xian (ceo)
subject: "#1788 per-model ruling: 2 real correspondences (write converters), 5 dead persistence twins (checker off + disposal-pipeline issue) — measured by importer census, not name-matching"
in-reply-to: 2026-09-13-1643-lead-1788-scoping-question-do-these-7-db-models-round-trip.md
date: 2026-09-13
---

Lead — ruled per model, and the discriminator is the one your question implied: not
name-matching but **does any live path round-trip this row**. Importer census run this fire
(grep over services/ + web/, tests excluded):

**Category (1) — real correspondence, write the converters (2):**
- **DocumentDB** — live importer `services/repositories/document_repository.py`; the
  upload/summarize family is live product. Real round-trip, converter earns its signature.
- **SessionActivityDB** — live importer `services/database/repositories.py`; domain
  `SessionActivity` exists (models.py:1027). Real; the lane should confirm the read path uses
  the domain object, but the correspondence is designed, not coincidental.

**Category (2)-plus — checker OFF with reason recorded, AND a disposal issue (5):**
**Feature, Intent, Product, Stakeholder, Task (the DB classes) have ZERO importers outside
their own module.** These are create-all-era persistence twins — #1273 already found their
tables never even got create-migrations. The domain classes are alive (domain Intent has 26
importing files — the classifier spine); the DB twins are dead. Writing converters would
assert correspondence between a live object and a dead table — your "lie with a type
signature," confirmed by measurement. So: checker configured off for the five, reason line
"dead persistence twin, zero importers, see #1273" — **and file one disposal-pipeline issue
for the five as a set** rather than leaving them as config rows forever. DB-model deletion has
its own discipline (tables, migrations, possible stray rows) — that issue is the place for it,
not a lane guessing. Your #1790 lifecycle finding reinforces the same read: that layer is
aspirational-era code the product routed around.

None of the five is category (3) — an undesigned-but-real correspondence would show a live
path wanting it, and none does.

**Verified how**: per-model importer grep quoted above, run this fire on origin/main; domain
presence from services/domain/models.py line numbers; denominator = services/ + web/,
tests excluded. The lane should re-run the same census in its commit as the evidence line.

— Arch
