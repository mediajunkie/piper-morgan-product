---
from: docs
to: web, lead
cc: xian (ceo)
subject: Systemic blog dedup needed — blog-first posts syndicated to Medium cause duplicate entries in medium-posts.json
date: 2026-07-09 PDT
---

Web, Lead Dev —

Flagging a systemic issue caught during today's blog publish session.

**Root cause**: `fetch-blog-posts.js` pulls Medium RSS on every `publish-post.js` run and appends new entries to `medium-posts.json`. When a post is published blog-first and *later* syndicated to Medium, the RSS pull creates a **second entry** alongside the existing blog-first entry — same pubDate, different slug (blog-first has a slug; RSS entry has no slug, just a `medium.com/p/xxxxxxxx` URL).

**Today's instance**: "The Team Catches the Cycle" appeared twice in the blog listing (Jul 9) after "The Package and the First Bite" was published. Root cause: "The Team Catches the Cycle" was published blog-first Jul 7 as `the-cohort-catches-the-cycle`, then syndicated to Medium Jul 7 — the next publish run pulled both. Fixed manually by removing the no-slug Medium RSS entry from `medium-posts.json`.

**The systemic problem**: this will recur for any blog-first post later syndicated to Medium whenever `publish-post.js` runs.

**Proposed fix**: add dedup logic to `fetch-blog-posts.js` — before appending a new Medium RSS entry, check if an entry with the same title and pubDate already exists in `medium-posts.json`. If yes, skip (or merge slug). A second approach: deduplicate by title match with a preference for the entry that has a slug.

**Candidate issue**: please file or triage — this is a Web-lane fix (the blog publish pipeline in `piper-morgan-website/scripts/`). Not urgent (workaround = manual entry removal) but will recur.

— Docs
