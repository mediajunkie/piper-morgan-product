---
name: update-calendar
description: Update the editorial calendar CSV when PM reports a publication,
  new draft, status change, or URL. Use when PM says "published X on Medium",
  "add Y to the calendar", "update the URL for Z", or provides syndication URLs
  after a publish.
scope: role-specific
version: 1.2
created: 2026-03-29
updated: 2026-07-14
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

## CSV Schema (18 columns)

```
title,theme,status,workDate,endWorkDate,pubDate,mediumURL,liPubDate,linkedinURL,canonicalSite,blogURL,blogPath,cartoon,chatDate,draftPath,notes,altText,caption
```

### Field Reference

| Column | Values/Format | Notes |
|--------|---------------|-------|
| title | Free text | Quote if contains commas |
| theme | `building`, `insight`, `ship` | Content type |
| status | `drafted`, `queued`, `published`, `distributed` | Lifecycle state — see below |
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
*v1.3 — Added `distributed` status value (PM-ratified 2026-07-19): published = live on pipermorgan.ai; distributed = blog + cross-posted. Bulk-migrated 243 rows from status=published to status=distributed (all rows with canonicalSite=distributed). Added status semantic anchor to Step 4 verification. Updated lifecycle table and anti-patterns.*
