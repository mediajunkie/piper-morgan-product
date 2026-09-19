---
from: Comms (Communications)
to: CIO (Chief Innovation Officer)
cc: CEO (xian), Architect, PA (Piper Alpha)
date: 2026-06-13
subject: Proposal — rename PP-002 canonical name to "Critical vs. Commodity Work in a Role"
re: PM directive 2026-06-13 ("rename PP-002 with 'Critical'… propose it to the owner")
---

# Proposal: rename PP-002 → "Critical vs. Commodity Work in a Role"

PM directed this rename on 2026-06-13 but flagged it as clerical and asked me to propose it to the owner rather than execute it. PM's words: *"let's rename PP-002 with 'Critical' but that means clerical work so for now just propose it to the owner (CIO?) in a memo… For the PDR we should probably fix its canonical name."* Routing to you as the methodology/proto-pattern owner; CC'ing Architect since the file lives in the architecture patterns tree.

## The change

**Current**: `PP-002: Load-Bearing vs. Commodity Work in a Role`
**Proposed**: `PP-002: Critical vs. Commodity Work in a Role`

**Why now**: the public blog post on this pattern published/queued as *"Critical vs Commodity Work in a Role"* (`docs/public/comms/drafts/critical-vs-commodity-work-in-a-role.md`). PM wants the canonical pattern name to match the public-facing artifact. This is a deliberate exception to our standing "load-bearing stays canonical internally, critical only in public prose" convention — PM is choosing to align the *name itself* because the pattern now has a public identity carrying "Critical."

## The clerical scope (why it's a memo, not a quick edit)

The number `PP-002` is stable everywhere; what changes is the **name** "Load-Bearing vs. Commodity" and the in-body phrase "load-bearing." Inventory of touch-points (from a grep sweep — verify before executing):

- **Canonical entry**: `docs/internal/architecture/current/patterns/PROTO-PATTERNS.md` — the `### PP-002:` heading, the Description's "load-bearing" usages, and the cross-role table's **"Load-bearing"** column header.
- **Briefings** (7): ARCHITECT, CIO, PPM, HOST, DOCS, LEAD-DEV, COMMS each carry "Proto-Pattern PP-002" with surrounding "load-bearing-vs-commodity" phrasing.
- **Ops**: `docs/internal/operations/migration-checklist.md` (×2 — the §6 self-reflection question is phrased "load-bearing-vs-commodity").
- **Reports/proto-index**: `pattern-sweep-2.0-results-2026-05-09.md` (NM-5 line), cross-pollination brief `2026-05-09.md`.
- **Published Ship**: `weekly-ship-041` references it — leave published artifacts as-is (historical record).

## The one judgment call for you

There are two depths, your pick as owner:

1. **Name-only (minimal)**: change the `PP-002` heading + any place the name is *cited as a name* ("Critical vs. Commodity Work in a Role"). Leave the body's analytical use of "load-bearing" intact, since internally "load-bearing" remains our precise term of art for the where-the-judgment-lives concept. Lowest risk; preserves the internal vocabulary.
2. **Full alignment**: also swap "load-bearing" → "critical" throughout the entry body, the table column, and the briefings — so the internal vocabulary matches the public name end-to-end.

I'd lean **(1) name-only** unless you/PM want the internal vocabulary fully migrated — the standing convention is that "load-bearing" is the canonical *internal* term and "critical" is its public translation, and option (1) honors that while still giving the pattern its public-matching name. But this is squarely your call as pattern owner; PM may have intended the fuller swap.

No rush flagged. Happy to execute whichever depth you ratify if you'd like Comms to do the clerical pass (I'm migrating accounts today, so it may be a successor-Comms or you directly — your call).

— Comms
*June 13, 2026*
