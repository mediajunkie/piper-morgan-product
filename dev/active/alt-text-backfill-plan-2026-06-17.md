# Alt-Text Backfill Plan
**Filed**: 2026-06-17 · **Owner**: Web (Unicorn Web Designer) · **Status**: READY TO EXECUTE

---

## What and why

318 published blog posts are missing `altText` in `data/editorial-calendar.csv`. The CSV is the source of truth: the `altText` field flows through `editorial-calendar.ts` → `BlogPost.imageAlt` → rendered as `alt=""` on each post's cover image in `BlogPostCard`. The current fallback is the post title, which is a headline, not an image description — poor for accessibility (WCAG) and wasted SEO opportunity.

**Goal**: fill the `altText` column for all 318 missing-alt published posts. Each entry should be a brief, descriptive caption for the cover image (thematic, since agents can't see the image directly).

---

## Scope

| Bucket | Count | How to handle |
|--------|-------|---------------|
| Published, missing `altText`, has Medium URL | 286 | Write agent (batch) |
| Published, missing `altText`, no Medium URL | 32 | Skip for now — flag for manual PM review |
| Not yet published | ~76 | Out of scope — fill at publish time going forward |

---

## Data sources

- **`data/editorial-calendar.csv`** — source of truth; `altText` and `caption` are the target fields
- **`src/data/medium-posts.json`** — contains `title`, `excerpt`, `content` (truncated), `thumbnail` URL, `tags` per post, keyed by path/slug. Agent uses this to understand what the post is about.
- **Title from CSV** — always available; join key to medium-posts.json by matching title or slug

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
