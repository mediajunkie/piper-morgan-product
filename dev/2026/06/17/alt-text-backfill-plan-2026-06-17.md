# Alt-Text Backfill Plan
**Filed**: 2026-06-17 · **Owner**: Web (Unicorn Web Designer) · **Status**: READY TO EXECUTE

---

## What and why

276 posts are missing `imageAlt` in `data/blog-metadata.csv`. This is the rendering source: `blog-metadata.csv` → `fetch-blog-posts.js` → `medium-posts.json` → `BlogPost.imageAlt` → rendered as `alt=""` on each post's cover image in `BlogPostCard`. The current fallback is the post title, which is a headline, not an image description — poor for accessibility (WCAG) and wasted SEO opportunity.

**Note on two CSVs**: `data/editorial-calendar.csv` also has an `altText` column (used by the admin UI / gap tracker, not the renderer). After the backfill, sync matching values back to `editorial-calendar.csv` to keep tracking in sync.

**Goal**: fill the `imageAlt` column for all 276 missing-alt posts in `blog-metadata.csv`. Each entry should be a brief, descriptive caption for the cover image. All entries have `imageSlug` (the actual image filename — primary signal for writing thematic alt text).

---

## Scope

| Bucket | Count | How to handle |
|--------|-------|---------------|
| Missing `imageAlt`, has excerpt in medium-posts.json | 132 | Write agent (imageSlug + excerpt + title) |
| Missing `imageAlt`, imageSlug only (no excerpt) | 144 | Write agent (imageSlug + title — still informative) |
| Already has `imageAlt` | 55 | Skip |
| **Total target** | **276** | **10 batches of 30** |

---

## Data sources

- **`data/blog-metadata.csv`** — rendering source of truth; `imageAlt` is the target field. All 331 entries have `imageSlug` (image filename — primary agent signal).
- **`src/data/medium-posts.json`** — contains `excerpt`, `tags` per post, keyed by slug. Supplemental context for 132 of the 276 missing entries.
- **`data/editorial-calendar.csv`** — admin tracking only; sync `altText` column here AFTER blog-metadata.csv is updated.

---

## Alt text format

One sentence, ~10–20 words. Thematic (describes what the image represents, given the post topic) rather than literal (we can't see the pixels). Examples:

- `"Abstract diagram of interconnected system layers representing architectural design choices"`
- `"A developer at a whiteboard planning a software build in public"`
- `"Split screen showing a prototype evolving into production code"`

Tone: professional, descriptive, no marketing language. Should make sense to a screen-reader user who hasn't seen the image.

---

## Process

### Phase 1 — Write agent (batched)

**Input**: CSV rows where `status=published` AND `altText` is blank AND `mediumURL` is non-empty (286 posts).

**Agent task** (per batch of ~30 posts):
1. Read each post's `title`, `theme` (from CSV) and `excerpt`, `tags` (from medium-posts.json, joined on slug/title).
2. Write a single thematic alt text sentence for the cover image.
3. Output as a patch: `{ "title": "...", "altText": "..." }` for each row.

**Batching**: 30 posts per agent call (~10 batches total). Keeps context tight; makes audit tractable.

**Output format**: JSONL or a patch CSV — one entry per post, `title` + `altText`. Do NOT write directly to the CSV in the first pass; collect output for audit.

### Phase 2 — Audit agent

**Input**: the patch output from Phase 1 (all 286 entries).

**Audit criteria** (flag any that):
- Are too generic (e.g., "Blog post about AI")
- Repeat the title verbatim
- Are longer than 25 words
- Contain marketing language ("revolutionary", "powerful", etc.)
- Don't make sense without context

**Output**: flagged items with specific suggested corrections. Approved items marked `ok`.

### Phase 3 — Merge

Web applies the audit-approved patch to the CSV. One commit per batch or one commit for the full backfill — PM's call.

Merge script (or manual): for each approved `{ title, altText }`, find the matching row in the CSV by `title`, set `altText`. Commit with message format:
`content(a11y): alt-text backfill batch N/10 (NN posts)`

### Phase 4 — Verification

After each batch merges:
1. Run `node scripts/fetch-blog-posts.js` to confirm no parse errors on the CSV.
2. Check the editorial calendar admin route (`/admin/calendar/`) — it shows missing-alt gaps. Count should decrease.
3. Spot-check 3–5 blog post cards at `pipermorgan.ai/blog` — inspect `alt=""` in DevTools on a card that was in the batch.

---

## Progress tracking

The CSV is the tracker. The gap-detection function in `src/lib/editorial-calendar.ts` (`getMissingAltTextGaps()`) already filters published posts with no `altText`. Run it or check the admin route at any time to see the current count.

**Starting count**: 318 missing (2026-06-17).
**Target**: 0 missing (or 32 remaining if no-Medium-URL posts are deferred).

---

## 32 no-Medium-URL posts

These posts are either: placeholder rows, early posts without archived Medium URLs, or entries that were never published to Medium. **Do not guess** alt text for these — the post content is unavailable without the URL. Options:
- PM reviews the list and either provides a URL or marks them as skip/archive
- Web generates the list as a separate deliverable for PM

List can be extracted with:
```bash
python3 -c "
import csv
with open('data/editorial-calendar.csv') as f:
    for r in csv.DictReader(f):
        if r['status']=='published' and not r['altText'].strip() and not r['mediumURL'].strip():
            print(r['title'][:80])
"
```

---

## Going forward

Once the backfill is complete: fill `altText` at publish time (it's already in the `publish-post.js` flow's data model). The `getMissingAltTextGaps()` admin-route check catches any that slip through.

---

## Resumption checkpoint

If this process is paused mid-execution, the state is fully recoverable from the CSV: any row with a non-empty `altText` is done; empty rows are remaining work. No external state to reconcile.
