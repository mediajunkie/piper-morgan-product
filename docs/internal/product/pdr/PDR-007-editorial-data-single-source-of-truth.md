# PDR-007: Editorial Data — Single Source of Truth

**Status**: DRAFT — **Arch ✅ and Web ✅ reviewed, no objection from either. Awaiting CIO** (one boundary question, §Implications). PM asked for this draft 2026-07-29 after raising the underlying question directly.
**✅ Arch review COMPLETE 2026-07-30 — no objection to ratifying the commitment.** Constraint 1 survives *with two corrections*, Option C stays rejected, Option B is the right implementation to evaluate, and the sequencing deferral is endorsed **"even harder"** — conditional on a threshold. Arch's central correction, applied throughout: **I staked the recommendation on Constraint 1, the most contestable claim in the document, when Option C was already dead on the class analysis** (it fixes only Class 1, and Class 1 was mitigated 07-29). A reader who disagreed about git ergonomics would have believed they'd reopened C. They hadn't.
⚠️ **And the catch that mattered most: my measurement window had NO SUCCESS CRITERION, so it could not fail.** Arch: *"a decision procedure with no falsification condition is m-44's shape applied to a decision instead of an instrument."* A PDR citing m-44 twice should not contain one. **Threshold now pre-registered** (see Recommendation) before the window runs, rather than chosen after seeing the result.
**✅ Web review COMPLETE 2026-07-29 22:05 — no objection to Option B, agrees with the sequencing, and CORRECTED THE COST ESTIMATE DOWNWARD.** Web read the PDR itself and checked the code rather than reacting to my characterization, and found I had **undercounted one surface and overcounted the cost**: the public blog page (`src/app/(public)/blog/[slug]/page.tsx`) imports `blog-content.json` and `medium-posts.json` directly as build-time modules — a bigger surface than the build scripts — **but it needs zero modification**, because it already treats both as pure generated data (reads, never writes, indifferent to provenance). That is exactly Option B's shape. Web also found a third affected script I missed (`copy-editorial-calendar.js`) and flagged their own `loadCalendarLive()` (shipped today, `18be9d1`, reads the CSV via the GitHub Contents API at request time) as **theirs to repoint, tracked to them, not orphaned**. Corrections applied below.
*Provenance note, because it's the good version of the pattern this file keeps citing: **Web corrected the estimate against their own interest.** A defensively inflated cost would have argued for Option A and less work in their lane; they said so explicitly and gave the honest number instead.*
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

1. **The SOURCE OF TRUTH must preserve the git audit trail and localize conflict.** *(Both halves corrected 2026-07-30 per Arch.)*
   - **Scope**: this binds the source of truth **only** — not derived artifacts. Constraint 3 makes those generated, and a generated binary index would be perfectly acceptable. As originally written ("any implementation") this forbade optimizations there is no reason to forbid.
   - **The binding property is provenance, not diffability.** *"We lose diff"* is arguable and invites *"just use a diff tool."* The real claim: **this cohort's primary audit mechanism for "who changed this claim, when, and why" is the commit log.** This PDR reconstructs the 7/14 and 7/28 incidents from commit history; Arch recovered a probe's timing from `reflog`. A binary blob does not degrade that audit trail — **it removes it.**
   - **"Mergeable" was the wrong property; the right one is conflict LOCALIZATION.** A single CSV *is* mergeable and contends constantly anyway, because all 418 rows live in one file. Arch verified the traffic independently: **170 commits / 60 days, and 38 of 48 active days had more than one commit — 79%.** Multi-writer days are the norm. So Option B's real win isn't better merging: **two agents editing different posts never touch the same file, so conflicts become impossible rather than resolvable.** That is a structural argument, not an ergonomic preference.
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

**⭐ But there is a move upstream of the check** *(Arch, 2026-07-30 — and it is a better illustration of
this PDR's own thesis than anything I originally wrote).* **`draftPath` is a stored assertion about
another system, and that is the defect itself.** Storing a fact about the filesystem means storing
something that can silently stop being true — which is exactly what happened 22 times by 7/12 and 7
more by 7/29. Two structural cures:

- **Derive it.** If drafts are discoverable by slug convention, `draftPath` becomes a lookup rather than a column and **the class stops existing.** Same move as ADR-072's frontmatter-derive and #1106's MANIFEST-derive — we have the pattern twice already.
- **If it must be stored, stamp it.** Carry `draftPath_verified_at` alongside, so a stale value is *visibly* stale rather than confidently wrong. (HOST's self-expiring-clause pattern from ADR-079 D4a; PPM's `last_verified` from #972 — also already convention.)

The validator stays as a catch-layer, but **it detects a class that a derive removes.** For the
companion ADR. And it sharpens the PDR's thesis: **the reconciliation problem and the staleness problem
have the same cure — stop maintaining what you can generate.**

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

### Why Option C is rejected — the class analysis, not the git argument

*Restructured 2026-07-30 per Arch: I had staked this on Constraint 1, which is the most contestable
claim in the document, and that let a reader who disagrees about git ergonomics believe they had
reopened C. They haven't.*

**Option C fixes Class 1 and only Class 1 — and Class 1 was mitigated on 2026-07-29.** The validator
ships per-column shape checks, behaviorally tested both directions. So C's entire remaining value is
*"structurally prevent a class we now detect,"* a marginal gain over a shipped mitigation, against a
real cost in consumer rewrites. **C loses on value before the git question is asked at all.** The
provenance argument below is supporting, not load-bearing.

### The sequencing deferral — with a PRE-REGISTERED success criterion

Hold Option A for **2–4 weeks** before committing to any migration. The validator and Step 4b shipped
2026-07-29 and have never been observed in production; committing on a fix verified only in an isolated
tree is the error m-44 documents.

⚠️ **As originally written this window could not fail** — no threshold was stated, so any result would
have been read to fit whatever the reader already believed. Arch caught it: *"a decision procedure with
no falsification condition is m-44's shape applied to a decision instead of an instrument."* A PDR that
cites m-44 twice should not contain one. **Criterion registered now, before the window runs:**

> **Window**: 2026-07-30 → 2026-08-27 (4 weeks). **Baseline** (measured 2026-07-29): Class-1 escapes 0 · Class-2 stale `draftPath` **0** (after 7 repairs) · Class-3 field-level disagreements **17 across 365 matched rows**, 0 in the dangerous direction.
>
> **Option A is sufficient — PDR-007 closes as adopted-without-migration — if ALL THREE hold at window end:**
> 1. **Class 1: zero** column-shift instances reaching `origin/main` undetected.
> 2. **Class 2: zero** unresolvable `draftPath` values.
> 3. **Class 3: ≤ 17** field-level disagreements on the matched set (i.e. **no growth** over baseline).
>
> **Otherwise Option B proceeds.**

Thresholds 1 and 2 are zero deliberately: both classes now have a known cause and a shipped
countermeasure, so any recurrence means the countermeasure isn't holding rather than that the bar is
too strict. Threshold 3 is no-growth rather than a reduction, because Option A's job is to stop drift
being *generated* — healing the existing 17 is a separate backfill, and folding it in would let a
backfill I could run in an afternoon disguise a mechanism that is still leaking.

**The measurement is shipped, not described.** A threshold nobody can reproduce measuring is the same
defect one layer down, so:

```bash
python3 scripts/measure-editorial-drift.py            # Classes 2 + 3 vs the criterion
python3 scripts/validate-editorial-calendar.py        # Class 1 (exit status)
```

`measure-editorial-drift.py` was written 2026-07-30 for exactly this window and **verified to reproduce
the 07-29 baseline** (365 matched rows, 0 stale paths, 17 disagreements). It carries the thresholds as
constants, reports rather than gates, and states in its own output that the decision is made once at
window end. Deliberately non-gating: it measures, PDR-007 decides.

## Alternatives rejected

- **Single-writer restriction on the calendar.** Docs proposed it 2026-07-29; PM rejected it, correctly. 170 commits/60 days with 57 tagged `(comms)` vs 4 `(docs)` — it would bottleneck the incumbent primary writer and add a second failure mode (the unread memo). Superseded by column ownership, ratified same day in `update-calendar` v1.4.
- **Fixing the 17 disagreements by hand.** Treats instances, not cause — exactly what the 7/12 pass did with 22 stale paths, which recurred within three weeks.
- **Making the validator's soft heuristics blocking.** A hard-failing heuristic causes false corrections. Its own first run false-positived on 8 historical rows carrying legacy `theme='shipping news'` and on a `claude.ai` URL ending in `.md`.

## Implications

**For Arch** — ✅ **REVIEWED 2026-07-30. No objection to ratifying the commitment; Constraint 1 survives with the two corrections now applied; Option C stays rejected; Option B is the right implementation to evaluate; sequencing deferral endorsed "even harder," conditional on the pre-registered threshold now added.** Arch's central correction: **I staked the recommendation on Constraint 1, the most contestable claim in the document, when Option C was already dead on the class analysis.** Applied throughout — the rejection now leads with "C fixes only Class 1, and Class 1 is mitigated," and the git argument is explicitly supporting.

**For CIO** — This is the third artifact this week whose failure mode was *"a check reported clean without measuring what it claimed"* (m-44). Class 2 is a pure instance: the calendar asserted 7 files existed and nothing checked. Worth a boundary ruling on whether m-44 extends to data-asserting-facts-about-other-systems, or whether that is a distinct class.
**Arch's read, offered as input rather than a ruling (2026-07-30)**: Class 2 *is* m-44's shape **with the data as the instrument** — a `draftPath` asserting a file exists is a claim that was never measured, and it reads identically whether true or three weeks stale. Five states, one output. The rule extends without strain: *an instrument must assert what it looked at* → **a stored field asserting an external fact must carry when it was last verified, or be derived rather than stored.** Arch would fold it in as a sub-shape rather than mint a new entry. **You own the catalog; that call is yours.**

**For Comms** — Option B changes where you write, not what you own. Column ownership survives as file-section ownership. Your `template-audit` and voice-guide work is unaffected.

**For Web** — ✅ **REVIEWED 2026-07-29; no objection, and the cost is SMALLER than I estimated.** Web's corrected scope:

- **The render layer needs ZERO modification.** `src/app/(public)/blog/[slug]/page.tsx` imports `blog-content.json` and `medium-posts.json` as build-time modules — the live path for every published post, and a surface I omitted entirely — but it only ever *reads* them and is indifferent to how they were produced. Generation repoints at the new source, emits the same JSON shape, and the page components never know. **The surface I missed turns out to be the reason the cost is bounded, not the reason it's large.**
- **Real cost is confined to the generation scripts**: `publish-post.js`, `sync-csv-to-json.js`, and **`copy-editorial-calendar.js`** — Web's find, whose local-sibling-checkout path assumption needs revisiting under *any* source format, so that one is owed regardless of this PDR.
- **Not** the admin pages, **not** the compose editor.
- `loadCalendarLive()` (`18be9d1` — reads the CSV via the GitHub Contents API at request time) needs repointing if the source moves. **Web owns that rewrite and asked to do it rather than have me guess at their own function's internals.** Correct, and recorded so it isn't orphaned.

**My "your objection should probably outweigh my preference" framing is superseded** — Web has no objection, and the point they pressed hardest was agreeing with the deferral.

**For Docs** — I own the reconciliation labor this PDR proposes to eliminate, so read my recommendation with that interest in view.

## Open questions

1. ~~**Arch/Web**: is the ~4.7% disagreement rate worth a migration, or is Option A sufficient indefinitely?~~ **ANSWERED — both.** *Web (07-29)*: decide from the measurement window, not a fixed position now. *Arch (07-30), reframing the question rather than answering the rate*: **don't answer it as a rate.** 17 disagreements with **0 in the dangerous direction** is not a quality crisis, it is a **labor cost, borne almost entirely by Docs.** So the real question is *"is hand-reconciliation the cheapest available mechanism?"* — plainly not, but the alternative spends Web's time. **That tradeoff is precisely what the window exists to price, which is why the window needs its now-registered threshold.** ✅ Closed.
2. ~~**Where does the single source live** — product repo or website repo?~~ **ANSWERED — Web and Arch concur independently: the PRODUCT REPO.** *Web (07-29)*: Comms and Docs author there, and the website copies are already downstream via `copy-editorial-calendar.js`. *Arch (07-30), with the structural reason*: putting the source in the website repo would **invert an existing dependency to no benefit, and inverted dependencies are how you get two sources again.** Same shape as ADR-070's server-owned-state family — one owner, everything downstream derived. ✅ Closed; carry into the companion ADR.
3. Do the two orphaned `blog-content.json` entries indicate a cleanup gap in `publish-post.js`, or are they intentional?
4. ~~**Method reconciliation**: what did the 7/28 "~46 captions" measurement count that mine doesn't?~~ **ANSWERED 2026-07-31 — and it overturns the framing, not just the number.**

   Both figures were correct; they measured different things:

   | basis | what it counts | result |
   |---|---|---|
   | **A** (mine, 07-30) | calendar caption quoted **and** site's not — a *disagreement* | **2** |
   | **B** (the "~46") | **all** site captions lacking an opening quote — *absolute* | **45** of 89 non-empty |
   | **C** (the decisive one, nobody had run it) | **all _calendar_ captions** lacking an opening quote | **45** of 92 non-empty |

   🔴 **Basis C is the finding.** The 7/28 note recorded this as *"~46 live-site captions missing quotation marks — the calendar is right and the live site is wrong."* **The calendar is not right: it carries the same 45, and 43 of them are the identical slugs.** The two surfaces *agree*.

   **So this was never Class-3 drift and does not belong in the disagreement count.** It is a **house-style question** — whether every caption must be quoted — on which *neither* surface conforms. It was miscategorised as a sync defect for three days, and the miscategorisation would have inflated the migration case in this PDR's favour.

   **Consequence for the Class-3 baseline: unchanged at 17.** The pre-registered criterion stands as written; had I folded the 45 in, the baseline would have been wrong by a factor of three and the window would have measured the wrong thing.

---

*Drafted 2026-07-29 by Docs at PM's request. All counts measured on the date of writing with the method stated inline; the one inherited figure I could not reproduce is flagged rather than repeated.*
