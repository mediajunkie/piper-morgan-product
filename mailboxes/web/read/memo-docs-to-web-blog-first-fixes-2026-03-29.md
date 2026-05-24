# Memo: Blog-First Publishing — Website Fixes Needed

**From**: Documentation Management (docs)
**To**: Unicorn Web Designer (web)
**Date**: March 29, 2026
**Re**: Blog-first post support in piper-morgan-website

---

## Context

We've begun publishing blog posts canonically to pipermorgan.ai first, then syndicating to Medium and LinkedIn. Two posts have shipped this way so far:

- **Discovery Is the Bottleneck** (Mar 29): `/blog/discovery-is-the-bottleneck`
- **Wiring vs. Wizardry** (Mar 30): `/blog/wiring-vs-wizardry`

The website infrastructure was originally built for Medium-first posts (RSS ingest → display). Blog-first posts exposed several issues that a local agent partially fixed, but one systemic issue remains and a few improvements are needed.

## Critical Fix: Blog Index Links Point to Medium

**Problem**: After running `fetch-blog-posts.js`, blog-first posts in the index link to their Medium URLs instead of local `/blog/{slug}` paths. The fetch script pulls from Medium RSS and overwrites the corrected local URLs.

**Root cause**: `fetch-blog-posts.js` doesn't preserve `source: "blog-first"` entries when merging RSS data. Medium RSS entries for syndicated posts have the Medium URL, which overwrites the local URL.

**Fix needed**: When merging RSS data in `fetch-blog-posts.js`, if an existing entry has `source: "blog-first"`, do NOT overwrite its `url` field with the Medium URL. The local `/blog/{slug}` URL must win.

**Acceptance criteria**: After running `node scripts/fetch-blog-posts.js`, entries with `source: "blog-first"` in `medium-posts.json` retain `url: /blog/{slug}` (not `medium.com/...`).

## Fixes Already Applied (For Your Awareness)

These were done by a local agent on Mar 29 and are already committed:

1. **csv-parser.js**: Updated field count 11 → 13 (imageAlt, imageCaption columns added)
2. **BlogPostContent.tsx**: "View original on Medium" link conditional on `post.guid.startsWith('http')` — blog-first posts use synthetic guids like `blog-first-a2ba24488d1c`
3. **sync-csv-to-json.js**: `extractHashId()` guards against undefined guid
4. **blog-metadata.csv**: Both blog-first entries have correct columns, imageSlug, pubDate

## Future Improvements (Lower Priority)

These would make blog-first publishing smoother but aren't blocking:

1. **Alt text support**: `imageAlt` and `imageCaption` columns exist in CSV but aren't rendered in blog post templates. The `<img>` tags need `alt` attribute from `imageAlt` and a `<figcaption>` from `imageCaption`.

2. **"Published:" date display**: Blog-first posts show "Published:" with no date on the index cards when pubDate parsing fails. Ensure the date parser handles `YYYY-MM-DD` format from CSV.

3. **Category filter counts**: "Building (0)" and "Insights (1)" in the index nav — verify category assignment flows through from CSV to the filter UI for blog-first posts.

## Data Format Reference

Blog-first entries in `blog-metadata.csv` (13 columns):
```
slug,hashId,title,chatDate,imageSlug,workDate,pubDate,category,cluster,featured,extra,imageAlt,imageCaption
```

Blog-first entries in `medium-posts.json` should have:
```json
{
  "slug": "wiring-vs-wizardry",
  "url": "/blog/wiring-vs-wizardry",
  "source": "blog-first",
  "guid": "blog-first-a2ba24488d1c",
  "thumbnail": "/assets/blog-images/wiring-vs-wizardry.webp",
  "featuredImage": "/assets/blog-images/wiring-vs-wizardry.webp",
  "category": "insight",
  "pubDate": "2026-03-30"
}
```

---

*Questions? Reach docs via mailbox or PM.*

---

## Addendum: Cross-Repository Access (Discussion Topic)

The current publish workflow requires PM to manually carry files and run scripts between piper-morgan-product and piper-morgan-website. This creates friction and debugging overhead.

**Topic for discussion**: Could we establish a mechanism for agents in either repo to push changes to the other? Options include:

1. **GitHub Action trigger**: A workflow in piper-morgan-product that pushes publish packages to piper-morgan-website via GitHub API (e.g., `create_or_update_file`).
2. **Shared publish directory**: A git submodule or subtree linking the two repos' publish surfaces.
3. **API-based publish**: A lightweight endpoint or Action in piper-morgan-website that accepts a POST with slug, HTML, metadata, and image URL.

PM would like to discuss deepening the relationship between the two repositories to reduce manual handoff. This is not urgent but would significantly streamline the publishing cadence as we move toward 2-3 posts/week.
