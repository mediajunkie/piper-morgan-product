# Memo: Mar 29 Alt-Text Fix Shipped + Adjacent Findings

**From**: Unicorn Web Designer (web)
**To**: Documentation Management (docs)
**CC**: PM (xian)
**Date**: 2026-05-16
**Re**: Follow-up to morning triage — Mar 29 outstanding item shipped, plus a latent-bug fix and one new finding for PM

---

## TL;DR

- **Mar 29 outstanding (alt text + figcaption for blog-first)** — shipped, commit `be0fd1329`.
- **Latent sync-csv-to-json.js bug** I flagged this morning — also shipped, commit `f320c6192`. Turned out to be live (not just latent): had been corrupting `cluster` on ~300 posts and `category` on 3 — quietly breaking era-filter coverage. Fixed.
- **New finding** I want a PM call on: `blog-content.json` has accumulated 23 duplicate-title pairs from syndicated blog-first posts. Functionally harmless, bigger than a one-liner. Batched as a question below.
- **Four open questions from this morning's triage memo are still open** — relisted at the bottom for convenience.

---

## (1) Mar 29 alt text + figcaption — shipped

Commit `be0fd1329` on `main`. Threads `imageAlt` and `imageCaption` from CSV through to the rendered DOM.

**Changes**:
- `scripts/fetch-blog-posts.js` — copies `imageAlt`/`imageCaption` onto post objects in the RSS-merge path, blog-first-build path, and the all-posts backfill pass (the backfill ensures the 32 existing cached blog-first posts pick up the fields too, not just new ones)
- `BlogPostCard` — `alt={imageAlt || title}` on the thumbnail
- `BlogPostContent` — `alt={imageAlt || title}` on the featured image; **prefers CSV-sourced caption** over the HTML-extracted caption (the HTML extractor only catches Medium RSS `<figure>` markup, so blog-first captions were being silently dropped)
- `BlogContent` — threads `imageAlt` prop to `BlogPostCard` in both list and grouped views
- `[slug]/page.tsx` — one-line TS cast on `content?.subtitle` (pre-existing error, surfaced during type-check this morning)

**Verified**: 32 blog-first posts now carry `imageAlt` and 41 carry `imageCaption` in the regenerated `medium-posts.json`. Type-check passes, build passes. Caveat: static-HTML grep can't see the rendered `<img alt>` because `BlogPostContent` is a `'use client'` component (DOM creation happens at hydration), but the serialized React payload contains both fields — strong evidence the wiring is right.

## (2) sync-csv-to-json.js destructure — shipped, with a surprise

Commit `f320c6192` on `main`. The fix itself is one line (11 names → 13 names in the destructure). The surprise was the magnitude of the latent damage it exposed.

Running the corrected script regenerated `medium-posts.json` with **307 cluster corrections** and **3 category corrections**. Before the fix, the script had been silently writing:

- `cluster` ← actually `pubDate` from CSV col 8 → 307 posts had `cluster: "2026-05-13"` (a date string) instead of an era slug. Era filter would never match these.
- `category` ← actually `workDate` from CSV col 7 → 3 posts had `category: "2025-10-05"` instead of `building`/`insight`/`ship`.

`fetch-blog-posts.js` was unaffected throughout — it goes through `csv-parser.js`, which already had the right 13-field shape. Only this script's local destructure was stale.

The data is now correct. Net effect on the live site: era filter coverage gets meaningfully better for the back-catalog of non-blog-first (RSS-sourced) posts.

## (3) New finding for PM — blog-content.json syndication duplicates

While verifying the alt-text fix, I noticed the `fetch-blog-posts.js` run had added one new entry to `blog-content.json` for "Same Failure, Six Agents, Ninety Minutes" — a post that already exists as a blog-first entry. Audit findings:

- **`blog-content.json` total entries: 333**
- **Minimal (blog-first-style `{title, content}`): 302**
- **Fat (RSS-style with `canonicalLink`, `author`, `filename`): 31**
- **Titles appearing in multiple entries: 23 pairs**

Example: "Are We Doing It Backwards?" exists under both `7bf92ff5bff6` (blog-first) and `abb0dc2d0d80` (Medium-syndicated RSS).

**Root cause**: `fetch-blog-posts.js:updateBlogContent()` (line ~611) iterates RSS posts and writes them to `blog-content.json` keyed by the Medium hashId, **without** checking whether the RSS post is a syndication duplicate of a blog-first post. The slug-based skip logic exists in `mergeArchive` (lines 313-347) and correctly keeps the duplicate out of `medium-posts.json`, but `updateBlogContent` runs on the unfiltered `rssPosts` list and adds the fat entry anyway.

**Functional impact**: zero, today. `medium-posts.json` correctly points to the blog-first hashId, so when `[slug]/page.tsx` looks up content, it finds the canonical blog-first entry. The 31 fat entries are dead data — bloating the file (~50KB+) but never rendered.

**Why I'm flagging**: every future syndication of a blog-first post will add another duplicate. Left alone, the file grows steadily and confuses future debugging ("which entry is canonical for this slug?").

**Options I see** — want PM to pick:

| Option | Effort | Risk | Effect |
|--------|--------|------|--------|
| **(a) Fix root cause only** — `updateBlogContent` skips RSS posts whose slug matches a blog-first post in current state | ~30 min | Low — same slug-set logic that already works elsewhere | Prevents future duplicates; existing 31 fat entries stay |
| **(b) Clean up existing only** — one-shot script to identify and remove the 23 confirmed duplicate fat entries (keep the 8 standalone fat entries) | ~1 hr (incl. audit) | Medium — must avoid removing fat entries that don't have a blog-first counterpart (would break those posts) | Removes accumulated cruft; bug will recur on next syndication |
| **(c) Both** | ~1.5 hr | Same as (b) | Permanent fix |
| **(d) Leave alone** | 0 | 0 | File keeps growing slowly; debug confusion continues |

My lean is **(c)** — small enough, root cause is clear, cleanup is worth doing once we're touching it. But **(d)** is defensible if the publishing cadence is moving toward a unified pipeline (`scripts/publish-post.js` from this morning's memo), since that might restructure how `blog-content.json` is maintained anyway.

## (4) Still-open questions from this morning's triage memo

For convenience, re-listing the four open questions PM input would unblock the larger Publishing UI work:

1. **Direction**: does codifying the publish-to-blog skill as `scripts/publish-post.js` (Step 1 of my recommendation) align with how you want to invest? Or alt-text-style cleanups higher priority first?
2. **Dashboard auth**: noindex meta + obscure slug acceptable, or do you want some form of soft auth?
3. **CLI CWD**: should `publish-post.js` be invokable from `piper-morgan-website` (the natural home) or from `piper-morgan-product` too (with cross-repo path resolution)?
4. **UI audience**: Publishing UI is *for PM*, right? Or is it meant to be agent-facing (something Claude Code reads to decide what to publish next)?

No deadline on any of these — happy to keep finding adjacent unblocked work while you batch responses.

---

*Session log: `dev/2026/05/16/2026-05-16-0719-web-code-opus-log.md`. Commits on `main`: `be0fd1329`, `f320c6192`. Both deployed to `pipermorgan.ai` via the normal Actions pipeline.*
