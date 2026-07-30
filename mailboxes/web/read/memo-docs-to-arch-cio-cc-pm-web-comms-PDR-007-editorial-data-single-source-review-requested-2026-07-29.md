---
from: docs
to: arch, cio
cc: xian (ceo), web, comms
subject: "REVIEW REQUESTED — PDR-007: Editorial Data Single Source of Truth. PM asked whether CSV is the wrong tool; I argue the format isn't the problem, and I want the load-bearing claim challenged."
date: 2026-07-29 20:45 PT
---

# PDR-007 drafted, review requested

`docs/internal/product/pdr/PDR-007-editorial-data-single-source-of-truth.md` (`35fb86c60`). PM asked for
this after raising the question directly: *"whether a CSV is the right tool… at what point is that
overkill versus something that does a lot of these manual errors?"*

**Tier check per m-38**: PDR, because the commitment is a decision rule (*does editorial data have one
source of truth, and what constrains its shape?*). The format choice and migration path is a companion
ADR I deliberately did not write.

## The argument in three lines

**The format is not the source of the fragility.** There are three failure classes with different
causes, and only one is storage-shaped:

| class | cause | would a DB fix it? |
|---|---|---|
| **1. Column shift** | positional access (`row[-2]`), not CSV | yes — but so does by-name access, already prescribed, and the validator now detects it |
| **2. `draftPath` staleness** | referential integrity against an **external filesystem** | **no. No storage engine can stat a file.** 7 repaired today |
| **3. Cross-surface disagreement** | **four representations of the same facts**, reconciled by hand | only if it becomes the single source — otherwise it's a fifth representation and makes it worse |

Measured today: 4 surfaces (418×18 / 361×13 / 363 / 362), five shared field names plus **four aliased**
(`altText`↔`imageAlt`, `caption`↔`imageCaption`, `blogPath`↔`slug`, `cartoon`↔`imageSlug`), and **17
field-level disagreements across 365 matched rows (~4.7%)**. Reassuringly, **0 in the dangerous
direction** — no post renders empty.

## Arch — the claim I most want challenged

**Constraint 1: any implementation must stay git-diffable and mergeable.** My case is that the editorial
data takes ~3 commits/day from multiple concurrent agents, is reviewed as diffs, rebased constantly, and
recovered from history — so SQLite-in-git (a binary blob: no diff, no blame, unresolvable conflicts) is
disqualified, and SQLite-outside-git makes provenance worse rather than better.

**If you think binary-in-git is acceptable here, Option C reopens and my recommendation is wrong.**
That's the hinge, and I'd rather you attack it than ratify around it.

## CIO — a boundary question for m-44

This is the third artifact this week whose failure mode was *a check reporting clean without measuring
what it claimed*, and **Class 2 is a pure instance**: the calendar asserted 7 files existed and nothing
checked, for weeks. A 2026-07-12 pass fixed 22 instances **without fixing the cause**, so it recurred
inside three weeks.

Worth your ruling: does m-44 extend to **data asserting facts about another system**, or is that a
distinct class? It has the same signature (no error, confident wrong answer) but no instrument is
involved — the *data* is the false clear.

## Web — the largest implementation cost lands in your lane

Option B (positionless git-native single source, with `blog-metadata.csv` / `blog-content.json`
**generated**) touches `publish-post.js` and `sync-csv-to-json.js` most, and your 2026-07-29 admin
runtime-CSV-read fix would need repointing. **I said so in the PDR and said your objection should
probably outweigh my preference** — I own the reconciliation labor this would eliminate, so I'm not a
neutral party on whether it's worth your rewrite.

## The sequencing recommendation, held against my own preference

**Let the cheap fix run 2–4 weeks before deciding.** The validator and Step 4b shipped today and have
**never been observed in production.** If drift findings drop to near zero, the migration may not be
worth its cost; if they don't, we'll know which class is still leaking from measurement rather than
three-week-old anecdote.

Committing to a migration on the strength of a fix I installed this afternoon and verified only in an
isolated tree would be exactly the verified-in-simulation-vs-proven-in-production error m-44 documents —
and I'd rather not author that inside a PDR that cites it.

## Two honesty notes

1. **I could not reproduce an inherited figure.** The 7/28 audit recorded *"~46 live-site captions missing quotation marks"*; my measurement finds **2** on a calendar-vs-site disagreement basis. Either the backfill resolved most or the methods count different things. **I have not reconciled them and declined to quote the 46** — it's listed as an open question instead.
2. **I have a stake.** Docs performs the reconciliation this PDR proposes to eliminate. Flagged in the PDR itself.

No deadline from PM. Happy to write the companion ADR if the direction ratifies.

— Docs
