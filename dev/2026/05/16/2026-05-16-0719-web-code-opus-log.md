# Web session — 2026-05-16 07:19

**Role**: Unicorn Web Designer (piper-morgan-website)
**Trigger**: Re-orient after ~6.5 week dormancy; PM asked for triage on the Mar 29 docs memo + scoping on a Publishing UI ask.

## Read

- `mailboxes/web/inbox/memo-docs-to-web-blog-first-fixes-2026-03-29.md` (Mar 29 docs memo, in full)
- `.claude/skills/publish-to-blog/SKILL.md` (v0.9, updated 5/15)
- Website: `scripts/fetch-blog-posts.js` (focus: 300-470, the merge/blog-first block)
- Website: `scripts/sync-csv-to-json.js` (focus: 19-80, the CSV destructure)
- Website: `scripts/csv-parser.js` (focus: field count + imageAlt/imageCaption handling)
- Website: `src/components/organisms/BlogPostContent.tsx` (full)
- Website: `src/components/molecules/BlogPostCard.tsx` (full)
- Website: `src/app/blog/page.tsx`, `src/app/blog/BlogContent.tsx` (1-100)
- Sampled: `src/data/medium-posts.json` — 33 blog-first entries present, all with `/blog/{slug}` URLs

## Verified (Mar 29 triage)

| Item | Status | Evidence |
|------|--------|----------|
| Critical: blog-first URL preservation | ✅ shipped | `fetch-blog-posts.js:313-470` builds blog-first posts fresh from CSV (line 442-459); syndicated RSS hits matched by slug are skipped (line 341-347). All 33 blog-first entries in current `medium-posts.json` carry `/blog/{slug}`. |
| "Published:" date display | ✅ working | BlogPostCard renders `publishedAt` ("May 14, 2026" format); blog-first dates flow from CSV `pubDate` via `formatDate()` in fetch-blog-posts.js:447. |
| Category filter counts | ✅ working | `BlogContent.tsx:83-84` computes building/insight counts from `allSortedPosts`. Category data flows through (sampled posts have `category: "building"` / `"insight"`). |
| Alt text rendering | ❌ not shipped | `BlogPostCard.tsx:77` and `BlogPostContent.tsx:161` both hardcode `alt={title}` / `alt={post.title}`. CSV has the column, csv-parser.js reads it, but `fetch-blog-posts.js:442-459` does not include `imageAlt` in the constructed post object; `BlogPost` interface doesn't declare it either. |
| Figcaption rendering | ⚠️ partial | `BlogPostContent.tsx:45-57` extracts caption from a `<figure>` in content HTML — works for Medium RSS posts that have figure markup, fails silently for blog-first posts (their content has no figure). CSV `imageCaption` is unused. |

## Latent bug noted (not in Mar 29 scope)

`scripts/sync-csv-to-json.js:62-73` destructures the CSV row into 11 fields, omitting `imageAlt`/`imageCaption`. The script currently only writes `cluster/category/featured/notes` back to JSON, so it functions — but the layout is stale relative to the canonical 13-column schema and will desync if anyone ever extends the script. Worth one-line fix when convenient; not urgent.

## Plan (this session)

1. Write triage memo to docs (this file, then memo).
2. No code changes this session — the ask is forward-looking triage + scoping.
3. Defer Publishing UI build until shape decision is in.

## Cross-repo automation — my read

Three options were named in the Mar 29 addendum: GH Action trigger, shared dir (submodule/subtree), API-based publish. My recommendation in the memo: **none of those three first**. The actual friction isn't the cross-repo hop — it's that the publish pipeline is encoded only in a skill (prose + Python snippets) rather than a single script. Codifying it as `scripts/publish-post.js` in piper-morgan-website (input: draft path + image path) gives ~80% of the relief at near-zero cost. Cross-repo automation becomes a thin wrapper later.

## Publishing UI — initial shape

Open shape question; my lean is to **start with a build-time admin dashboard** (e.g. `/admin/publish-queue`) generated from `editorial-calendar.csv`, gated noindex. Surface: drafts ready, recently published, syndication gaps, cross-post URLs. Zero new infra (static export friendly). Layer interactivity later via CLI wrapper around `scripts/publish-post.js`. Full reasoning in the memo.

## Next

- Send memo to docs (CC PM via mailbox routing).
- Wait for shape decision before committing to UI build.

---

## Work shipped (continued after PM standing instruction)

PM gave standing instruction at ~07:24: do unblocked work, batch questions, don't meter on availability for routine forward motion. Banked as feedback memory `feedback_unblocked_work_batched_questions.md`.

### Commit 1 — be0fd1329 `fix(blog): render imageAlt + imageCaption from CSV for blog-first posts`

Closes the Mar 29 outstanding ask. Threaded `imageAlt` and `imageCaption` from CSV → `medium-posts.json` → React props → `<img alt>` + `<figcaption>` (CSV-sourced caption preferred over HTML-extracted; falls back for Medium RSS posts).

Files: `scripts/fetch-blog-posts.js`, `src/app/blog/BlogContent.tsx`, `src/app/blog/[slug]/page.tsx` (subtitle TS cast), `src/components/molecules/BlogPostCard.tsx`, `src/components/organisms/BlogPostContent.tsx`, regenerated `medium-posts.json` + `blog-content.json` (RSS picked up 1 new syndicated post).

Verified: 32 blog-first posts now carry imageAlt and 41 carry imageCaption in the regenerated JSON. Type-check passes; build passes. Static-HTML verification limited because BlogPostContent is a client component (DOM creation happens at hydration), but serialized React payload contains both fields — strong indicator.

### Commit 2 — f320c6192 `fix(sync): correct sync-csv-to-json field destructure (11 → 13 cols)`

Adjacent latent-bug fix flagged in the triage memo. The destructure was off by 2 columns since the CSV grew from 11 → 13 fields (imageAlt/imageCaption added). Symptoms exposed when I re-ran the script:

- 307 posts had `cluster` set to a date string (actually pubDate from CSV col 8) instead of an era slug — silently breaking era filtering for non-blog-first posts
- 3 posts had `category` set to a date string (actually workDate from CSV col 7) instead of `building`/`insight`/`ship`

`fetch-blog-posts.js` was unaffected because it goes through `csv-parser.js` (which already had the right 13-field shape). Only this script's local destructure was stale.

Regenerated `medium-posts.json` + `backup-sync` reflect the corrections.

### Surprise finding (not yet fixed): blog-content.json syndication duplicates

Discovered during the alt-text fix verification. `fetch-blog-posts.js:updateBlogContent()` adds RSS posts to `blog-content.json` keyed by their Medium hashId, without checking whether they're syndication duplicates of an existing blog-first post (which lives under a different hashId). Result: 31 "fat" RSS-style entries in `blog-content.json`, 23 of which have titles matching existing blog-first entries.

Functionally harmless — `medium-posts.json` correctly points to the blog-first hashId, so the duplicate fat entries are never looked up. But the file is bloated and confusing during debug.

Not fixing this round — it's bigger than a one-liner and the right scope (fix root cause vs clean up existing vs both vs leave alone) is a PM call. Flagged in the follow-up memo.

## Outbox

- `mailboxes/docs/inbox/memo-web-to-docs-mar29-fix-shipped-and-new-findings-2026-05-16.md` — follow-up to morning's triage memo

## Stop point

Halting after two shipped fixes. Open items now batched for PM:
1. blog-content.json duplicate handling (fix root cause / clean up existing / both / leave)
2. Four questions from the morning's triage memo (publish-script direction, dashboard auth shape, CLI CWD, who the UI is for)

