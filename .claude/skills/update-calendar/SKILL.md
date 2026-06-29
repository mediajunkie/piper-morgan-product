---
name: update-calendar
description: Update the editorial calendar CSV when PM reports a publication,
  new draft, status change, or URL. Use when PM says "published X on Medium",
  "add Y to the calendar", "update the URL for Z", or provides syndication URLs
  after a publish.
scope: role-specific
version: 1.1
created: 2026-03-29
updated: 2026-06-29
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
| status | `drafted`, `queued`, `published` | Lifecycle state |
| workDate | YYYY-MM-DD | When the piece was written |
| endWorkDate | YYYY-MM-DD | End of work period (optional) |
| pubDate | YYYY-MM-DD | Publication date |
| mediumURL | Full URL | Medium publication link |
| liPubDate | YYYY-MM-DD | LinkedIn publication date |
| linkedinURL | Full URL | LinkedIn post link |
| canonicalSite | `distributed` or empty | Set to `distributed` when on blog + syndicated |
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

### Step 2: Update Existing Row

Use the Edit tool to replace the matching row. **Always read the current row first** to avoid clobbering existing data. Only change the fields PM specified — preserve everything else.

Common updates:
- **Published with URLs**: Set status→published, add mediumURL, liPubDate, linkedinURL
- **Blog-first publish**: Set status→published, blogURL, blogPath, canonicalSite→distributed
- **New draft**: Set status→drafted, workDate, theme, draftPath
- **Scheduled**: Set status→queued, pubDate

### Step 3: Add New Row (if entry doesn't exist)

Append a new row at the end of the file. Use proper CSV quoting:
- Quote fields containing commas: `"Ten Roles, One Day"`
- Quote fields containing quotes: `"""quoted text"""`

### Step 4: Verify

```bash
grep "TITLE" docs/internal/planning/comms/editorial-calendar.csv
```

Confirm the row looks correct and column count matches (18 fields).

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
| Forget to quote commas in titles | Use `"Title, With Comma"` |
| Leave status as `queued` after publishing | Update to `published` |
| Skip the blogURL for blog-first posts | Always set blogURL + blogPath + canonicalSite |

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
