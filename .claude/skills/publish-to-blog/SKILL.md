---
name: publish-to-blog
description: Publish a finished blog post from this repo to the pipermorgan.ai website
  repo. Use when PM says "publish this post", "push to the blog", or when a draft
  is marked ready in the editorial calendar. Bridges piper-morgan → piper-morgan-website.
scope: role-specific
version: 0.6
created: 2026-03-16
updated: 2026-04-11
---

# publish-to-blog

Publish a finished markdown blog post to the pipermorgan.ai website repository.

## When to Use

Use this skill when:
- PM says a draft is ready to publish to the blog
- A piece in the editorial calendar has status `ready` or `queued` with today's pubDate
- PM asks to "push to the blog" or "publish this post"

## Prerequisites

- The draft markdown file must exist in `docs/public/comms/drafts/`
- The image must be in the same directory (PM provides)
- Image metadata should be in the draft's comment block (see below) or provided conversationally

## Draft Metadata Convention

PM includes a comment block at the top of the draft (after the H1 title):

```markdown
# Post Title

<!-- image: filename.png -->
<!-- alt: Description of the image for screen readers -->
<!-- caption: "Caption text in quotes" -->
```

If the comment block is missing, ask PM for image filename, alt text, and caption.

The skill MUST strip these comment lines when converting to HTML.

## Procedure

### Step 1: Read Draft and Extract Metadata

```python
# Parse the draft file
# 1. H1 line → title
# 2. <!-- image: ... --> → image filename
# 3. <!-- alt: ... --> → alt text
# 4. <!-- caption: ... --> → caption (strip outer quotes)
# 5. Everything else → body content for HTML conversion
```

Look up the next post in the editorial calendar for the footer teaser.
Determine category from the editorial calendar (`building`, `insight`, or `ship`).

### Step 2: Generate hashId

**Blog-first posts** (not yet on Medium):
```bash
python3 -c "import uuid; print(uuid.uuid4().hex[:12])"
```
hashId MUST be valid hex (0-9, a-f only) — the content lookup regex requires this.

**Backlog posts** (already on Medium): Extract hashId from the Medium URL's last segment.

### Step 3: Full Pipeline (Single Script)

Run this as one Python script to minimize round-trips:

```python
import csv, json, re, os, subprocess

# Inputs
DRAFT_PATH = "docs/public/comms/drafts/{filename}.md"
WEBSITE_REPO = "../piper-morgan-website"
HASH_ID = "{generated_hex}"
SLUG = "{slug}"

# 1. Read draft, extract metadata, strip H1 + comments
# 2. Convert markdown → HTML
# 3. Prepare image: sips -Z 1200, cwebp -q 80 → website/public/assets/blog-images/
# 4. Add to website blog-metadata.csv (13 columns)
# 5. Add HTML to website blog-content.json
# 6. Run sync + fetch pipeline
# 7. Verify post appears in medium-posts.json
```

#### HTML Conversion Rules

Strip from output:
- H1 title line (the FIRST `# Title` only — see heading note below)
- Comment block lines (`<!-- ... -->`)

**Heading convention**: PM writes drafts with `#` for section headings (not `##`). This is because LinkedIn renders `##` as small headings when pasted, so the source uses `#` for impact when syndicated. The publish-to-blog conversion must:
1. Strip ONLY the first H1 (the title at line 1)
2. Convert all subsequent `# Section` lines to `<h2>Section</h2>` (NOT `<h1>`)
3. Convert `## Subsection` to `<h2>` as well (treat both as section headers)
4. Convert `### Sub-subsection` to `<h3>`

```python
# In conversion loop, track whether title H1 has been stripped:
title_stripped = False
for line in body_lines:
    if line.startswith('# ') and not title_stripped:
        title_stripped = True
        continue  # skip the title line
    if line.startswith('## '):
        emit(f'<h2>{line[3:]}</h2>')
    elif line.startswith('# '):  # subsequent H1 = section
        emit(f'<h2>{line[2:]}</h2>')
    elif line.startswith('### '):
        emit(f'<h3>{line[4:]}</h3>')
```

Convert:
- `---` → `<hr>`
- Paragraphs with inline: `**bold**`, `*italic*`, `[links](url)`
- `_italic standalone lines_` → `<p><em>...</em></p>`
- `*italic standalone lines*` → `<p><em>...</em></p>`
- Em dashes: ` -- ` → ` — `
- Unordered lists: `- item` → `<ul><li>item</li></ul>`

#### Image Preparation

```bash
sips -Z 1200 "{source_image}" >/dev/null 2>&1
cwebp -q 80 "{source_image}" -o "{website_repo}/public/assets/blog-images/{slug}.webp"
```

### Step 4: Sync and Fetch

```bash
cd {website_repo}
node scripts/sync-csv-to-json.js
node scripts/fetch-blog-posts.js
```

Verify the post appears with correct slug, category, thumbnail, and content.

### Step 5: Build and Push Website

```bash
cd {website_repo}
npm run build  # This also re-runs fetch — ensure CSV data persists
git add data/blog-metadata.csv src/data/blog-content.json src/data/medium-posts.json public/assets/blog-images/{imageSlug}
git commit -m "Add blog post: {title}"
git push origin main
```

**CRITICAL**: `npm run build` regenerates `medium-posts.json` from RSS + CSV. Manual edits to that file do NOT persist. All post data must flow through `blog-metadata.csv`.

### Step 6: Update Editorial Calendar

Use the `/update-calendar` skill with:
- status → `published`
- pubDate → today
- canonicalSite → `distributed`
- blogURL → `https://pipermorgan.ai/blog/{slug}`
- blogPath → `/blog/{slug}`
- altText, caption from draft metadata

### Step 7: Commit Product Repo

```bash
git add docs/internal/planning/comms/editorial-calendar.csv
git commit -m "editorial calendar: {title} published"
git push origin main
```

### Step 8: PM Syndicates

PM does manually:
1. **Medium**: Paste content, set canonical URL to `https://pipermorgan.ai/blog/{slug}/` (trailing slash!)
2. PM provides Medium URL → Docs updates calendar via `/update-calendar`

### Step 9: Drafts Folder Cleanup (Final Step)

**ONLY after** verifying:
- ✅ Post is live at `https://pipermorgan.ai/blog/{slug}/`
- ✅ Editorial calendar updated with at least one syndication URL (mediumURL or linkedinURL)
- ✅ Calendar status is `published`

Then archive the draft and source image to keep `docs/public/comms/drafts/` lean:

```bash
# 1. Move final draft to published/
mv docs/public/comms/drafts/{filename}.md docs/public/comms/drafts/published/

# 2. Move any superseded/intermediate versions to superseded/
# (look for draft-{slug}-v1.md, draft-{slug}-v2.md, {slug}-draft.md, etc.)
for f in docs/public/comms/drafts/draft-{slug}*.md docs/public/comms/drafts/{slug}-draft*.md; do
  [ -f "$f" ] && mv "$f" docs/public/comms/drafts/superseded/
done

# 3. Move source image to images-archive/ (the webp is now in production)
mv docs/public/comms/drafts/{image}.png docs/public/comms/drafts/images-archive/
# (also try .jpg, .jpeg if .png doesn't exist)

# 4. Commit
git add docs/public/comms/drafts/
git commit -m "docs: archive {title} draft + image (published)"
git push origin main
```

**Why this is the final step**: Cleanup before verification risks losing the source if the publish fails. Cleanup after syndication confirms the post is live and the local source is no longer the canonical version.

**For ships**: Same procedure but `published/` and `superseded/` apply equally — the ship draft and any working versions get archived after the LinkedIn post is confirmed live.

## Ship Posts

For `category: ship` posts, the workflow is the same except:
- URL prefix is `/shipping-news/{slug}` (not `/blog/{slug}`)
- Image is always `piper-ship.webp` (no per-post image needed)
- Ships may publish without blog-content.json entry (shows LinkedIn link fallback)
- LinkedIn is the syndication target (not Medium)

## Website CSV Format (13 columns)

```
slug,hashId,title,chatDate,imageSlug,imageAlt,imageCaption,workDate,pubDate,category,cluster,featured,notes
```

**Do NOT confuse with the editorial calendar (18 columns).** Different schemas.

## Known Issues (as of v0.5)

1. **Captions**: BlogPostContent doesn't render captions from post metadata for blog-first posts. Captions are stored in the CSV but not displayed. Tracked as a website display bug.
2. **Image sizing**: Featured images may crop poorly depending on aspect ratio. Known design issue.
3. **Large file hook**: Images over 500KB may be rejected by pre-commit. Always compress with `sips -Z 1200` before committing.

## Anti-Patterns to Avoid

| Don't Do This | Why | Do This Instead |
|---------------|-----|-----------------|
| Publish to Medium first | Blog should be canonical | Blog first, then syndicate |
| Use non-hex hashId | Regex extraction fails silently | Always use `uuid.uuid4().hex[:12]` |
| Edit medium-posts.json manually | Gets wiped by `npm run build` | Add data via blog-metadata.csv |
| Use `echo >>` to append CSV rows | May corrupt CSV | Use Python csv writer |
| Skip field count verification | Silent column misalignment | Verify 18 fields (editorial) or 13 (website) |
| Forget trailing slash on canonical URL | Mismatch with site config | `trailingSlash: true` in next.config |

## Quality Checklist

After publishing:
- [ ] Blog post accessible at `https://pipermorgan.ai/blog/{slug}/`
- [ ] Featured image loads correctly
- [ ] Blog index shows post with thumbnail
- [ ] Editorial calendar updated (this repo) with syndication URL(s)
- [ ] Website repo committed and pushed
- [ ] GitHub Pages deploy completed
- [ ] Draft moved to `drafts/published/`
- [ ] Source image moved to `drafts/images-archive/`
- [ ] Any superseded drafts moved to `drafts/superseded/`

---

*v0.6 — Added Step 9 (drafts folder cleanup as final step after syndication confirmed). Cleanup includes: move final draft to published/, superseded versions to superseded/, source image to images-archive/. Rationale: cleanup before verification risks losing source if publish fails. Also documented heading convention: drafts use `#` for section headers (not `##`) because LinkedIn renders `##` as small. Conversion must strip only the FIRST H1 (title) and promote subsequent `#` and `##` to `<h2>`.*

*v0.5 — Added draft metadata convention (comment block for image/alt/caption). Documented hashId must be valid hex. Noted npm run build regenerates medium-posts.json (critical). Added ship post workflow. Added trailing slash requirement for canonical URLs. Removed remote execution mode (unused). Streamlined procedure.*
