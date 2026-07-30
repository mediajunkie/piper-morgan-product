# PDR-007: Editorial Data — Single Source of Truth

**Status**: DRAFT — for **Arch + CIO review**. PM asked for this draft 2026-07-29 after raising the underlying question directly. No commitment made yet.
**Date**: 2026-07-29
**Author**: Docs (Documentation Management)
**Stakeholders**: PM, Arch, CIO, Comms (primary calendar writer), Web (owns the website consumers), Dispatch (syndication)
**Tier**: PDR per m-38 — this is a **decision-rule** question (does editorial data have one source of truth, and what constraints bind its shape?). The concrete format and migration path is a **companion ADR**, deliberately not decided here.

---

## The question PM actually asked

> *"I'm beginning to wonder whether a CSV is the right tool. It seems like reading and writing to it is a somewhat fragile process involving column counting when maybe we should make something like a proper database and use CRUD actions to make updates. At what point is that overkill versus something that does a lot of these manual errors?"*

This PDR argues the framing needs one correction before it can be answered: **the format is not the
source of the fragility, and a database would fix the smallest of three problems while costing
something we rely on daily.** The real issue is one layer up — four representations of the same facts
with manual reconciliation between them.

## Proposed decision

**Commit to a single source of truth for editorial post data, with derived representations generated
from it rather than maintained alongside it.** Do *not* commit to a storage format in this PDR.

Three constraints proposed as binding on any implementation:

1. **Git-diffable and mergeable.** The editorial data takes ~3 commits/day from multiple agents and is reviewed as diffs, rebased, and recovered from history. Any format that turns a merge conflict from annoying into unresolvable is disqualified.
2. **Addressable by name, never by position.** Both documented corruptions came from positional access. A format where position is not a concept eliminates the class structurally.
3. **Derived surfaces are generated, never hand-edited.** The reconciliation cost is the actual problem; a second source of truth reintroduces it regardless of format.

## Context — what actually exists today

Four representations of "a post," measured 2026-07-29:

| surface | size | repo | maintained how |
|---|---|---|---|
| `editorial-calendar.csv` | 418 rows × 18 cols | product | hand-written by agents via `/update-calendar` |
| `blog-metadata.csv` | 361 rows × 13 cols | website | appended by `publish-post.js` |
| `blog-content.json` | 363 keys | website | written by `publish-post.js` |
| `medium-posts.json` | 362 entries | website | **generated** by `fetch-blog-posts.js` + `sync-csv-to-json.js` |

Only the fourth is generated. The first three are independently maintained and must agree.

**They share five field names outright** (`title`, `pubDate`, `workDate`, `chatDate`, `notes`) **and
four more facts under different names**, which is worse because no textual comparison finds them:

| calendar | website |
|---|---|
| `altText` | `imageAlt` |
| `caption` | `imageCaption` |
| `blogPath` | `slug` (derived) |
| `cartoon` | `imageSlug` |

## The problem, measured rather than asserted

**Three distinct failure classes, and they do not share a cause.** This distinction is the crux of the
PDR, because only one of the three is a storage-format problem.

### Class 1 — column shift (positional access). NOT a CSV problem.

Two documented incidents:

- **2026-07-14** — `row[-2]` used for `notes` (index 15) landed on `altText` (index 16).
- **2026-07-28** — Weekly Ship #050: `notes` held a duplicate draftPath, `altText` held 1,000+ chars of prose, `caption` held the real alt text. **Field count stayed a valid 18 throughout**, so every count-based verification passed.

**Both came from bypassing the parser.** Python's `csv` module addresses by header name and handles
quoting completely — there is no column counting in CSV read with a parser. `update-calendar` v1.2
already prescribed by-name access; the incidents are cases of not following it.

**Status: mitigated 2026-07-29.** `scripts/validate-editorial-calendar.py` now detects the class
(per-column shape checks: enums, date formats, URL/path prefixes, and the repo-path-in-prose
signature). Behaviorally tested both directions.

### Class 2 — referential staleness. A database does NOT fix this.

`draftPath` values asserting a file exists on disk. **7 found and repaired 2026-07-29** (3 Weekly Ships
+ 4 narrative posts); a **2026-07-12 pass fixed 22 instances without fixing the cause**, which is why
it recurred inside three weeks. Cause in every case: Step-9 archival moved a file and nothing updated
the row.

**This is referential integrity against an external filesystem. No storage engine validates it** — not
SQLite, not Postgres. `CHECK` constraints cannot stat a file. Only a check can, and one now exists.

### Class 3 — cross-surface disagreement. THE class a single source of truth would eliminate.

Measured today across the 365 calendar rows that match a website row by slug:

| disagreement | count |
|---|---|
| `altText` ≠ `imageAlt` | **11** |
| `caption` ≠ `imageCaption` | **6** |
| site caption missing its opening quotation mark (house style says captions keep them) | 2 |
| `blog-content.json` entries with no `blog-metadata.csv` row (orphans) | 2 |
| csv rows with no content entry (**the dangerous direction**) | **0** |

**~17 field-level disagreements across 365 matched rows (≈4.7%).**

⚠️ **A correction to the inherited figure**: the 7/28 audit recorded *"~46 live-site captions missing
quotation marks."* My measurement finds **2** on a calendar-vs-site disagreement basis. Either the
7/28 backfill resolved most of them or the two measurements count different things. **I have not
reconciled the methods, and the PDR should not carry a number I cannot reproduce.** Using the measured
figure and flagging the discrepancy.

**Reassuring result worth stating**: 0 rows in the dangerous direction. No post renders empty. The
integrity that matters most is intact.

## Why a database is the wrong first move

**It fixes Class 1 (by making positional access impossible) and nothing else.** Class 2 is
filesystem-referential and format-independent. Class 3 is caused by duplication, and **a database that
becomes a fifth representation makes Class 3 worse, not better.**

Against that it costs:

- **Git-diffability.** ~3 commits/day, multiple concurrent agents, reviewed as diffs and rebased constantly. A SQLite file in git is a binary blob: no diff, no blame, and merge conflicts become unresolvable rather than annoying. Kept *outside* git, the "who changed this and why" story gets worse, not better.
- **Consumer rewrites.** At minimum `build-editorial-calendar-view.py`, `validate-editorial-calendar.py`, `sync-csv-to-json.js`, `publish-post.js`, and the website's admin calendar — the last of which **Web shipped a runtime-CSV-read fix for on 2026-07-29**, hours before this PDR.
- **No concurrency benefit.** The writers are separate processes committing to git, serialized by push-to-ref and rebase. Transactions solve a problem we don't have.

**None of the usual triggers for a real store are present**: no cross-table queries (one flat table), no
scale pressure (418 rows), no concurrent transactional writes.

## Options

### Option A — Keep CSV, rely on validation (status quo + today's work)
Already shipped: by-name access, per-column shape checks, `draftPath`-resolves check, Step 4b in the
skill. **Cost: zero further.** Leaves Class 3 entirely — the four surfaces still reconcile by hand.

### Option B — Positionless, git-native single source ⭐ *recommended for evaluation*
One file per post (`content/posts/{slug}.md` with YAML frontmatter, or `posts.jsonl`), with
`blog-metadata.csv` / `blog-content.json` **generated** from it.

- **Class 1 becomes structurally impossible** — no columns, so no shift.
- **Class 3 collapses** — the website surfaces become build artifacts, not maintained data.
- Keeps every git property: diff, blame, grep, mergeable, and conflicts land per-post rather than file-wide.
- Same consumer-rewrite cost as a database, **none of the git loss.**
- Natural fit: the website is already a content-driven static site, and `medium-posts.json` is already generated — this extends an existing pattern rather than inventing one.

### Option C — Real datastore (SQLite/Postgres) + CRUD
Fixes Class 1. Loses git-diffability. Does not address Class 2. **Risks worsening Class 3** unless it
becomes the single source all consumers derive from — at which point the valuable decision was the
consolidation, and the storage engine is incidental.

## Recommendation

**Adopt the single-source-of-truth commitment now; evaluate Option B as the implementation; do not
adopt Option C.**

And a sequencing recommendation I'd hold even against my own preference for B: **let Option A run for
2–4 weeks first.** The validator and Step 4b shipped today and have never been observed in production.
If drift findings drop to near zero, the migration may not be worth its cost — and if they don't, we'll
have measured evidence for which class is actually still leaking rather than three-week-old anecdotes.
**Committing to a migration before the cheap fix has been observed would be the same
verified-in-simulation-vs-proven-in-production error m-44 documents.**

## Alternatives rejected

- **Single-writer restriction on the calendar.** Docs proposed it 2026-07-29; PM rejected it, correctly. 170 commits/60 days with 57 tagged `(comms)` vs 4 `(docs)` — it would bottleneck the incumbent primary writer and add a second failure mode (the unread memo). Superseded by column ownership, ratified same day in `update-calendar` v1.4.
- **Fixing the 17 disagreements by hand.** Treats instances, not cause — exactly what the 7/12 pass did with 22 stale paths, which recurred within three weeks.
- **Making the validator's soft heuristics blocking.** A hard-failing heuristic causes false corrections. Its own first run false-positived on 8 historical rows carrying legacy `theme='shipping news'` and on a `claude.ai` URL ending in `.md`.

## Implications

**For Arch** — Constraint 1 (git-diffable/mergeable) is the load-bearing claim and the one I'd most want challenged. If you think binary-in-git is acceptable here, Option C reopens.

**For CIO** — This is the third artifact this week whose failure mode was *"a check reported clean without measuring what it claimed"* (m-44). Class 2 is a pure instance: the calendar asserted 7 files existed and nothing checked. Worth a boundary note on whether m-44 extends to data-asserting-facts-about-other-systems, or whether that is a distinct class.

**For Comms** — Option B changes where you write, not what you own. Column ownership survives as file-section ownership. Your `template-audit` and voice-guide work is unaffected.

**For Web** — Option B makes `blog-metadata.csv` and `blog-content.json` generated artifacts, which touches `publish-post.js` and `sync-csv-to-json.js` most. Your 2026-07-29 admin runtime-read fix would need to point at the new source. **This is the largest implementation cost in the PDR and it lands in your lane** — your objection should probably outweigh my preference.

**For Docs** — I own the reconciliation labor this PDR proposes to eliminate, so read my recommendation with that interest in view.

## Open questions

1. **Arch/Web**: is the ~4.7% disagreement rate worth a migration, or is Option A sufficient indefinitely?
2. **Where does the single source live** — product repo (where editorial planning happens) or website repo (where publishing happens)? It currently straddles both, which may be the root of the duplication.
3. Do the two orphaned `blog-content.json` entries indicate a cleanup gap in `publish-post.js`, or are they intentional?
4. **Method reconciliation**: what did the 7/28 "~46 captions" measurement count that mine doesn't? Until that's answered, neither number should be quoted as the caption-drift figure.

---

*Drafted 2026-07-29 by Docs at PM's request. All counts measured on the date of writing with the method stated inline; the one inherited figure I could not reproduce is flagged rather than repeated.*
