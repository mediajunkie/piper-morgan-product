---
name: update-calendar
description: Update the editorial calendar CSV when PM reports a publication,
  new draft, status change, or URL. Use when PM says "published X on Medium",
  "add Y to the calendar", "update the URL for Z", or provides syndication URLs
  after a publish.
scope: role-specific
version: 1.4
created: 2026-03-29
updated: 2026-07-29
---

# update-calendar

Update the editorial calendar CSV without the PM touching a spreadsheet.

## When to Use

Use this skill when:
- PM says "published [title] on [platform] at [URL]"
- PM says "add [title] to the calendar" (new draft or queued piece)
- PM provides Medium/LinkedIn URLs after syndication
- PM says "mark [title] as published" or changes status
- PM provides alt text or caption for an image
- Any editorial calendar metadata needs updating

## CSV Location

`docs/internal/planning/comms/editorial-calendar.csv`

## Column ownership — who writes what (PM-RATIFIED 2026-07-29)

**This calendar is multi-writer by design. There is no single owner, and proposals to make one have
been considered and rejected.**

| Owner | Columns |
|---|---|
| **Comms** (editorial authorship) | `title` · `theme` · `workDate` · `endWorkDate` · `pubDate` · `cartoon` · `chatDate` · `draftPath` · `notes` · `altText` · `caption` |
| **Docs** (publish / syndication transaction) | `blogURL` · `blogPath` · `canonicalSite` · `mediumURL` · `liPubDate` · `linkedinURL` |
| **Shared, SEQUENTIALLY** | `status` — Comms owns it through `drafted` → `ready-for-docs`; **Docs owns it from `published` → `distributed`** |

**Write your own columns yourself, through this skill.** Do not route routine updates through another
agent's inbox. **Send a memo only to cross the boundary** — to ask for a change to a column you don't
own, or to propose a structural change such as adding a column.

⚠️ **`status` is the one column to be most careful with.** It is the lifecycle field the publish
pipeline routes on, so a wrong value there misroutes work rather than merely being inaccurate. If you
are not sure whether a transition is yours, ask before writing it.

### Why this is ownership-by-column and not ownership-by-agent

Docs proposed sole-Docs-ownership on 2026-07-29 and **PM rejected it, correctly.** The empirical case
against it: the calendar took **170 commits in 60 days, 57 tagged `(comms)` against 4 tagged `(docs)`** —
Comms is the incumbent primary writer, and a single-writer rule would have made one agent's inbox a
bottleneck on work others already do correctly. It would also have added a second failure mode: the memo
that sits unread. That is not hypothetical — on the same day, Docs published a post ten minutes after
Comms had already delivered the answer to its one open blocker, in an unopened memo.

**And plurality of writers was never the cause of the corruption anyway.** Both documented incidents
came from **positional access**, which one writer can do just as destructively:

- **2026-07-14** — `row[-2]` used for `notes` (index 15) landed on `altText` (index 16).
- **2026-07-28** — Weekly Ship #050: `notes` held a duplicate draftPath, `altText` held 1,000+ chars of prose, `caption` held the real alt text. **Field count stayed 18 throughout**, so every count-based check passed.

The mechanism that prevents this is **by-name access through this skill plus the validator** (Step 4),
not a restriction on who may write. Address every field by header name; never by position.

## CSV Schema (18 columns)

```
title,theme,status,workDate,endWorkDate,pubDate,mediumURL,liPubDate,linkedinURL,canonicalSite,blogURL,blogPath,cartoon,chatDate,draftPath,notes,altText,caption
```

### Field Reference

| Column | Values/Format | Notes |
|--------|---------------|-------|
| title | Free text | Quote if contains commas |
| theme | `building`, `insight`, `ship` | Content type |
| status | `drafted`, `queued`, `ready-for-docs`, `published`, `distributed` | Lifecycle state — see below. **Shared column: Comms writes through `ready-for-docs`, Docs from `published` on.** |
| workDate | YYYY-MM-DD | When the piece was written |
| endWorkDate | YYYY-MM-DD | End of work period (optional) |
| pubDate | YYYY-MM-DD | Publication date |
| mediumURL | Full URL | Medium publication link |
| liPubDate | YYYY-MM-DD | LinkedIn publication date |
| linkedinURL | Full URL | LinkedIn post link |
| canonicalSite | `distributed` or empty | Set to `distributed` when on blog + syndicated (pipeline dedup signal; independent of status) |
| blogURL | Full URL | e.g., `https://pipermorgan.ai/blog/{slug}` |
| blogPath | Path | e.g., `/blog/{slug}` |
| cartoon | Slug | Image slug (no extension) |
| chatDate | M/D/YYYY | Date of source chat session |
| draftPath | Relative path | e.g., `docs/public/comms/drafts/draft-name.md` |
| notes | Free text | Any notes |
| altText | Free text | Image alt text (quote if contains commas) |
| caption | Free text | Image caption (quote if contains commas) |

## Procedure

### Step 1: Find the Row

```bash
grep -n "SEARCH_TERM" docs/internal/planning/comms/editorial-calendar.csv
```

If not found and PM is adding a new entry, proceed to Step 3.

### Step 2: Update Existing Row — via the `csv` module, keyed by column NAME, never by position

**Never use the Edit tool or hand-spliced string surgery on a CSV row, and never index a row by a raw number or `[-N]` offset.** A quoted field can contain commas, and a raw string edit or positional index (`row[-2]`, `row[15]`) silently breaks the moment the row's *shape* doesn't match what you assumed — no error, just quiet semantic drift that a field-count check won't catch (see the 2026-07-14 incident below: two same-day edits by Comms did exactly this, corrupting a live row for hours before a peer agent caught it).

Always read and write through Python's `csv` module, and always address fields **by header name**:

```python
import csv
PATH = 'docs/internal/planning/comms/editorial-calendar.csv'
with open(PATH, newline='', encoding='utf-8') as f:
    rows = list(csv.reader(f))
hdr = rows[0]
idx = {name: hdr.index(name) for name in hdr}
row = next(r for r in rows[1:] if r and r[0] == TITLE)
assert len(row) == len(hdr)          # bail loudly if the row is already malformed
row[idx['status']] = 'published'     # BY NAME — never row[2], never row[-2]
with open(PATH, 'w', newline='', encoding='utf-8') as f:
    csv.writer(f, lineterminator='\n').writerows(rows)
```

**Always read the current row first** to avoid clobbering existing data. Only change the fields PM specified — preserve everything else. When appending to a free-text field (like `notes`), append to `row[idx['notes']]` specifically — never assume its position relative to the end of the row.

**Status lifecycle** (PM-ratified 2026-07-19):
- `drafted` → piece is in draft
- `queued` → scheduled but not yet published
- `published` → live at pipermorgan.ai (blog-first)
- `distributed` → live at pipermorgan.ai AND cross-posted to Medium/LinkedIn

Note: `canonicalSite=distributed` is a separate pipeline signal (used for RSS dedup); it stays set independently of the status field.

Common updates:
- **Blog-first publish**: Set status→published, blogURL, blogPath, canonicalSite→distributed
- **Cross-posted to Medium/LinkedIn**: Set status→distributed, add mediumURL, liPubDate, linkedinURL
- **New draft**: Set status→drafted, workDate, theme, draftPath
- **Scheduled**: Set status→queued, pubDate

### Step 3: Add New Row (if entry doesn't exist)

Build the new row as a Python list in schema order (18 elements, empty string for unset fields) and append it via `csv.writer` — the module handles quoting automatically, so you never hand-quote commas or embedded quotes yourself.

### Step 4: Verify — count AND semantics, whole file, not just the touched row

A field-count check on the one row you touched is **not sufficient** — it cannot detect a row where content has drifted into the wrong column while the total count stays correct (exactly what happened 2026-07-14: an append landed in `altText` instead of `notes`, field count stayed at 18, and the drift went undetected until a *later*, unrelated edit collapsed the count and made it visible).

Run a whole-file scan after every edit:

```python
import csv, re
with open('docs/internal/planning/comms/editorial-calendar.csv', newline='', encoding='utf-8') as f:
    rows = list(csv.reader(f))
hdr = rows[0]
idx = {n: hdr.index(n) for n in hdr}
bad = [i for i, r in enumerate(rows[1:], start=2) if r and len(r) != len(hdr)]
assert not bad, f"field-count mismatch at rows {bad}"
for i, r in enumerate(rows[1:], start=2):
    if not r or len(r) != len(hdr):
        continue
    cs = r[idx['canonicalSite']]
    assert cs in ('', 'distributed'), f"row {i}: canonicalSite={cs!r}"
    st = r[idx['status']]
    assert st in ('drafted', 'queued', 'published', 'distributed', 'ready-for-docs', ''), f"row {i}: status={st!r}"
    bu = r[idx['blogURL']]
    assert not bu or bu.startswith('http'), f"row {i}: blogURL={bu!r}"
```

Treat any assertion failure as a stop-and-investigate signal, not something to paper over — a semantic anchor tripping means content is very likely sitting in the wrong column.

**⭐ The inline snippet above is now the FALLBACK. The canonical check is the script** (extended
2026-07-29 to cover per-column shape + reference integrity — it supersedes the hand-rolled asserts):

```bash
python3 scripts/validate-editorial-calendar.py            # errors fail, warnings print
python3 scripts/validate-editorial-calendar.py --strict   # warnings also fail
```

It adds what the inline version cannot see: **per-column shape** (enums, `YYYY-MM-DD` vs `chatDate`'s
`M/D/YYYY`, URL/path prefixes, and the Ship #050 repo-path-in-prose signature) and **reference
integrity** (`draftPath` actually resolves on disk).

**Errors block; warnings never do — and that split is deliberate.** A heuristic that hard-fails causes
*false corrections*, which are worse than the drift they claim to fix. Two live examples, both from the
validator's own first run: it flagged 8 historical Ships carrying the pre-`ship` value
`theme='shipping news'`, and a `notes` field holding a `claude.ai` URL that happens to end in `.md`.
**Both were fixed in the checker, not in the data.** If this script reports a warning on a historical
row, the default assumption is that the row is fine and the heuristic is coarse.

### ⚠️ Step 4b: If you MOVED a draft file, update `draftPath` in the same pass

**This is the single most common way this calendar goes stale.** Archiving a draft to
`docs/public/comms/drafts/published/` without updating its row leaves the row pointing at a path that no
longer exists — silently, since nothing used to check.

- **7 stale paths were found and repaired on 2026-07-29** (3 Weekly Ships + 4 narrative posts). Every one had this cause.
- A **2026-07-12 pass fixed 22 instances and did not fix the cause**, which is why it recurred within three weeks.
- `publish-to-blog` **Step 9** is where the move happens; the row update belongs in the same commit.

Verify with the validator (it now reports non-resolving paths) or directly:

```bash
python3 -c "
import csv, os
bad = [(r['title'][:44], r['draftPath']) for r in csv.DictReader(open('docs/internal/planning/comms/editorial-calendar.csv'))
       if (r.get('draftPath') or '').strip() and not os.path.exists(r['draftPath'])]
print(f'{len(bad)} unresolvable draftPaths'); [print('  ', t, p) for t, p in bad]
"
```

Expected: `0 unresolvable draftPaths`.

### Step 5: Rebuild the calendar view

```bash
python3 scripts/build-editorial-calendar-view.py
```

This regenerates `docs/internal/planning/comms/editorial-calendar-view.html` from the CSV. Always run after any CSV change to keep the admin view current.

### Step 6: Commit

```bash
git add docs/internal/planning/comms/editorial-calendar.csv \
        docs/internal/planning/comms/editorial-calendar-view.html
git commit -m "editorial calendar: [what changed]"
```

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Ask PM to edit the CSV | Update it yourself from their verbal instructions |
| Overwrite fields PM didn't mention | Read current row first, preserve existing data |
| Forget to quote commas in titles | Use `"Title, With Comma"` (or let `csv.writer` handle it) |
| Leave status as `queued` after blog publish | Update to `published` |
| Leave status as `published` after cross-posting | Update to `distributed` |
| Skip the blogURL for blog-first posts | Always set blogURL + blogPath + canonicalSite |
| Edit a row with the Edit tool, or index it by number/`[-N]` | Use the `csv` module, address every field by header name |
| Verify only the touched row's field count | Whole-file scan: field count + semantic anchors on every row |

## Examples

### PM says: "Published Are We Doing It Backwards on Medium at [URL]"

1. Find row: `grep -n "Backwards" editorial-calendar.csv`
2. Update: mediumURL → [URL], status → published (if not already)
3. Commit

### PM says: "Add 'The Quiet Before the Question' to the calendar, narrative, work dates Mar 5-10"

1. Append: `The Quiet Before the Question,building,drafted,2026-03-05,2026-03-10,,,,,,,,,,,,`
2. Commit

### PM says: "Here are the Medium and LinkedIn URLs for Wiring vs Wizardry: [URLs]"

1. Find row, update mediumURL + linkedinURL + liPubDate
2. Commit

---

*v1.1 — Added Step 5: rebuild calendar view HTML after every CSV change (2026-06-29).*
*v1.2 — Replaced Edit-tool/positional-index row surgery with `csv`-module-by-name access (Steps 2-3), and upgraded verification to a whole-file field-count + semantic-anchor scan (Step 4) (2026-07-14). Root-caused from a real incident: two same-day Comms edits used `row[-2]` for the `notes` field, which actually landed on `altText` (18-column schema, `notes` at index 15, `altText` at 16) — the drift stayed invisible under a single-row field-count check until a later edit collapsed the count, at which point a peer session caught and repaired it. See `docs/internal/planning/comms/editorial-calendar.csv` "The Migration Wave" row's own notes for the full incident trace.*
*v1.4 — **Column ownership PM-RATIFIED (2026-07-29).** Added the ownership table (Comms = editorial columns; Docs = publish/syndication columns; `status` shared sequentially) plus the reasoning for why it is ownership-by-column rather than by-agent. Docs proposed sole-Docs-ownership and PM rejected it: 170 commits in 60 days, 57 tagged `(comms)` vs 4 `(docs)`, so a single writer would bottleneck the incumbent primary writer — and both documented corruptions came from POSITIONAL ACCESS, which one writer can do just as destructively. Also: Step 4 now names `scripts/validate-editorial-calendar.py` as the canonical check (extended same day with per-column shape + `draftPath`-resolves checks; errors block, warnings never do, because a hard-failing heuristic causes false corrections). New Step 4b: if you moved a draft file, update `draftPath` in the same pass — 7 stale paths repaired 2026-07-29, all from archival moving files without updating rows, after a 7/12 pass fixed 22 instances without fixing the cause.*

*v1.3 — Added `distributed` status value (PM-ratified 2026-07-19): published = live on pipermorgan.ai; distributed = blog + cross-posted. Bulk-migrated 243 rows from status=published to status=distributed (all rows with canonicalSite=distributed). Added status semantic anchor to Step 4 verification. Updated lifecycle table and anti-patterns.*
