# Docs Tree Flattening Plan — 2026-08-11

**Author**: Docs
**Status**: ✅ **`roadmap/CORE/` flatten EXECUTED 2026-08-29** — PM approved 2026-08-29 after 18
days on the attention board ("Ah yes, the doc-tree! I requested this... Overall the plan looks
good and prudent"). PM added a timing constraint the same day: do not touch ADR/pattern/
methodology paths while they're in active review (Arch's forensic history pass + the ratified
trigger-retrofit requirement) — that constraint doesn't affect this plan's one executed candidate,
`roadmap/CORE/`, which was never in that path space. See "Execution record" below.
**Origin**: PM asked mid-#1584 (2026-08-10) whether to flatten parts of the docs tree, having just
watched me fix off-by-one `../` bugs caused by directory depth. This document is the requested plan.

## The evidence, gathered from real defects, not a general impression

Depth alone isn't the defect. **Depth combined with either (a) redundant nesting that duplicates
information already in the filename, or (b) a directory reorganization whose cross-links were never
updated** is the defect. Both classes produced real, shipped bugs this week:

- `docs/internal/architecture/current/models/` (5 levels) — 77+20 links used a leftover `models/`
  prefix because the linking files had themselves been moved *into* `models/` without their
  self-references being updated. Fixed in #1584 (`a0fd56987`).
- `docs/public/user-guides/legacy-user-guides/` and `docs/public/getting-started/
  legacy-getting-started/` (4 levels each) — ~27 links assumed sibling directories
  (`development/`, `production/`, `architecture/`) that don't exist at that depth; the real
  targets live 3-4 levels further down under `docs/internal/`. Fixed in #1584 (`253b46855`,
  `003185bea`).
- `docs/internal/planning/roadmap/CORE/GREAT/` — 4 near-duplicate files
  (`CORE-GREAT-4E.md`/`-COMPLETE.md`/`-COMPLETE-100-PERCENT.md`/`-FINAL-WITH-EVIDENCE.md`),
  zero inbound references anywhere, clearly successive drafts nobody cleaned up after the
  epic closed. Reconciled in #1585 (`33c945eb7`).

**Counter-evidence, equally important**: `docs/internal/architecture/current/adrs/` (4 levels,
82 files) and `docs/internal/architecture/current/patterns/` (4 levels, 80 files) are just as deep
and just as large, and had **zero broken links** in today's full-tree audit (#1583/#1584). Depth
by itself didn't hurt them. What's different: both use flat, sequentially-numbered filenames
(`adr-NNN-*.md`, `pattern-NNN-*.md`) with minimal cross-directory relative-path traversal, and
neither has been reorganized recently.

**So the discriminator for any given directory is**: does the nesting carry information the
filename doesn't already encode, and has it been reorganized without a corresponding link-fix
pass? If yes to either, it's fragile. If no to both, depth isn't the problem.

## A related structural finding, filed separately (#1593)

While researching this plan, found that `.github/workflows/link-checker.yml` (lychee, runs on
every push to `docs/**` + weekly) **correctly detects every broken link** — its own log shows the
exact same defects #1584 found independently — but **the workflow always reports success anyway**.
This is very likely why ~240 broken links accumulated silently: an active-looking CI check that
structurally cannot fail. Fixing #1593 matters more than any one flattening pass — it's the
difference between "flatten once" and "stay flat," and it applies regardless of what this plan
recommends.

## Flattening candidates, ranked by confidence

### High confidence — recommend flattening

**`docs/internal/planning/roadmap/CORE/` (9 subdirectories, 76 files)**

Every file across all 9 sub-epic directories (ALPHA, AUTH, CRAFT, GREAT, KEYS, KNOW, PREF, USERS,
UX) is already named `CORE-{EPIC}-{topic}.md` — the epic identity is fully encoded in the
filename. The subdirectory layer is **100% redundant** with information the filename already
carries. Flattening to `docs/internal/planning/roadmap/CORE/*.md` directly:
- Loses zero information (grep/sort by prefix still groups by epic trivially)
- Removes one full level of depth for the tree's single largest concentration of markdown files
  outside adrs/patterns
- Eliminates the entire class of off-by-one relative-path bugs for this subtree going forward
- Also surfaces (didn't fix yet) a real duplicate-artifact filename found while inspecting this
  subtree: `CORE-CRAFT-UPDATED (1).md` — a literal `" (1)"` sync/download artifact, same shape as
  the `roadmap-v3.0 2.md` ghost file found and removed in #1584.

**Risk**: low. 76 files, mechanical `git mv`, then a link-integrity re-scan (the same Python check
used throughout #1583/#1584/#1585) to confirm nothing broke. Estimated: one focused session.

### Lower confidence — needs a human decision, not mechanical

**`docs/public/comms/growing-piper/analysis/analysis_code_independent/` and
`analysis_cursor_independent/`** (5 levels, 7+5 files) — these carry real information (which
analysis method produced them), not redundant with filename. Not a flattening candidate by the
discriminator above, but worth Comms confirming both are still referenced/needed.

### Not flattening candidates — explicitly ruled out, with reasons

- **`docs/internal/architecture/current/adrs/`, `.../patterns/`** — deep, large, zero defects.
  Sequential numbering already does the job flattening would do elsewhere. Leave alone.
- **`docs/public/user-guides/legacy-user-guides/`, `.../getting-started/legacy-getting-started/`**
  — the "legacy" grouping carries real information (distinguishing legacy from current guides).
  The bug wasn't the depth, it was stale cross-links after a past reorg — already fixed in
  #1584. Flattening would *lose* the legacy/current distinction for no gain. The real fix here
  is #1593 (make link-checker.yml actually gate), not restructuring.
- **`docs/assets/images/blog/comms/blog/published/YYYY/MM/DD/`** (7-9 levels) — chronological
  image archive, same shape as `dev/YYYY/MM/DD/` session logs elsewhere in the repo. Depth here
  is doing real work (date-based organization) and these are leaf folders with no internal
  cross-references to break. Not a candidate.

## Proposed execution, if PM approves

Staged, not a big-bang sweep — matching how Finding 1 and #1584/#1585 were actually done this
week:

1. **File #1593's fix first** (or confirm it's already being worked) — a working link-check gate
   makes every subsequent step self-verifying instead of relying on a manual re-scan each time.
2. **`roadmap/CORE/` flatten** (the one high-confidence candidate): `git mv` all 76 files up one
   level, delete the now-empty subdirectories, fix the one `" (1)"` artifact filename found along
   the way, re-run the link-integrity check used throughout this week's work, commit in batches
   under the 20-file hook threshold.
3. **Everything else**: no action from this plan. The "not flattening" list stays as-is; the
   "lower confidence" pair goes to Comms for a decision, not executed unilaterally.

## What this plan does NOT propose

No action on `adrs/`, `patterns/`, the legacy-guides directories, or the image archive. No
renaming convention changes. No action beyond the `roadmap/CORE/` flatten without a further
explicit go-ahead — this document is the plan PM asked for, not a standing authorization to keep
restructuring the tree.

## Execution record — 2026-08-29

**#1593 confirmed already closed** (2026-08-12) — the link-checker CI gate genuinely fails on
broken links (`exit 1`, verified by reading the workflow, not just trusting the closed status).
Prerequisite satisfied.

**76 files flattened** across all 9 sub-epic directories (ALPHA, AUTH, CRAFT, GREAT, KEYS, KNOW,
PREF, USERS, UX) to `roadmap/CORE/*.md` directly. Zero cross-file link references existed into or
across the subdirectories (checked both directions before moving anything). Committed in 6 batches
(under the 20-file broad-staging-hook threshold — the plan's own stated constraint, which fired as
designed on the first attempt at a single 77-file commit). Also fixed the `" (1)"` duplicate-sync
artifact (`CORE-CRAFT-UPDATED (1).md` → `CORE-CRAFT-UPDATED.md`) and one pre-existing
filename/directory mismatch found along the way (`CORE-AUTH-CONTAINER-issue.md` had been misfiled
under `ALPHA/`, not `AUTH/`).

**The mandated re-verification found a real, separate bug**: `scripts/check_links.py` (the check
this plan named as the re-verification step) had a hardcoded pre-worktree absolute path
(`/Users/xian/Development/piper-morgan/docs`) that doesn't exist on this host. `os.walk()` on a
nonexistent directory silently iterates zero files, so the script had been reporting "0 links
found, 0 broken" regardless of actual repo state — indistinguishable from a genuine clean pass.
Fixed to derive the repo root from the script's own location (`e560cedab`); re-run found 2,542 real
links, 81 pre-existing broken ones repo-wide, **none caused by this flatten** — the one broken pair
found inside the flattened set (`CORE-ALPHA-LEARNING-BASIC.md`, 2 links to files that never
existed anywhere reachable) was confirmed pre-existing via git's rename-detection (file content
byte-identical, only path moved) and filed separately as #1692, since fixing it is a content
decision, not a mechanical path fix.

All 9 now-empty subdirectories removed. Final state: 76 files, one flat directory, zero
subdirectories, zero broken links attributable to the move.

## PM's deeper question, answered with evidence — 2026-08-29

PM asked (relayed by Exec) whether the taxonomy layers themselves — `internal/`, `current/` in
paths like `.../architecture/current/adrs/` — earn their depth, a sharper cut than "which
directories should be flattened." Exec offered a read as input; investigated both with real data
rather than react to the framing.

**`internal/` earns its keep.** `docs/internal/` holds 774 markdown files; `docs/public/` plus a
dozen other top-level directories (`accessibility/`, `api/`, `features/`, `guides/`,
`installation/`, `integrations/`, `legal/`, `releases/`, `security/`, `setup/`, etc.) hold 252 —
a real, substantial, genuinely-distinct public-facing corpus, not a hollow prefix. Applying Exec's
own test ("name a reader who makes a different choice because of it"): a public-docs-site build,
an external contributor, or a search index all route differently based on this boundary. Keep it.

**`current/` does not currently earn its keep, with concrete evidence, not just a hypothesis.**
`docs/internal/architecture/current/adrs/` holds 82 files; its only structural sibling,
`docs/internal/architecture/archive/`, holds 12 completely unrelated old planning documents
(entity-relationship diagrams, deployment guides) — **no ADR has ever actually been moved out of
`current/` on supersession.** Meanwhile `adr-028-verification-pyramid.md` has carried
`**Status**: SUPERSEDED` in its own frontmatter since 2026-07-26 (dated, ratified: the runtime
package it specified was deleted as a dead island) while still sitting in `current/adrs/` — over a
month of exactly the drift Exec predicted: *"if superseded ADRs are marked by status line rather
than by path... one of the two will drift."* The Status line is the actual, trustworthy source of
truth (sampled across dozens of ADRs: Accepted, Proposed, SUPERSEDED, all present and legible);
the directory layer adds a second, unmaintained encoding of the same fact, and it's already wrong
at least once. A reader relying on the path gets actively misled, not just uninformed.

**Recommendation, not executed**: fold `current/` out of the ADR/pattern paths (e.g.
`docs/internal/architecture/adrs/`, not `.../current/adrs/`), with the Status line as the single
source of truth for current-vs-superseded — matching how the documents already work in practice.
**Deliberately not executed now** — this falls squarely inside PM's own timing constraint from the
same conversation ("since ADRs, patterns, and methodology are all in review... not change them
right now"), a different reason than this plan's original "wary of precipitous changes" caution
but the same practical conclusion. Recorded here, evidence-backed and ready, so it doesn't need
re-deriving once Arch's review concludes.
