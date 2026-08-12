# Janus → Docs (cc Comms, PM) — pinch-hit publish while the team was offline

**Date:** 2026-08-11 · **From:** Janus (Design in Product, DinP's resident agent) · **Re:** "The Write-Path Chase"

The 11-agent PM team was out of weekly quota this evening. PM had already edited and proofread
the draft and wanted today's scheduled post (pubDate 2026-08-11) to go out on time, so he asked me
to run the `publish-to-blog` pipeline directly rather than wait for a reset. I'm not a PM-repo
resident agent — flagging everything I touched so nothing here reads as silent.

## What shipped

- **Live:** https://pipermorgan.ai/blog/the-write-path-chase/ — verified by content (grepped
  "code island" and the title against the live response, not just a status code — per your own
  v0.22 discipline in the skill).
- Website repo (`piper-morgan-website`): `09b1ddd` — blog-metadata.csv row, blog-content.json
  entry, webp image, medium-posts.json regenerated, editorial-calendar.csv mirror re-synced by the
  normal `prebuild` step.
- Product repo (this one): `6ae9c75ab` — calendar row updated via `/update-calendar` (status→
  `published`, blogURL, blogPath, canonicalSite→`distributed`). Only the Docs-owned columns
  touched; I left `notes` alone since that's Comms' column.

## One content decision made, at PM's explicit direction

Your notes on this row carried an unresolved fact-check flag: "found out a field ... is never set
**in the database**" — you'd correctly left it rather than guess whether `Intent.original_message`
is actually a persisted DB column. I surfaced it to PM before publishing rather than deciding it
myself. He confirmed: cut "in the database," lose nothing. Draft and live page both read "...is
never set (sad trombone)" now. Flagging here so the resolution is on record, not just in the commit
diff.

## What I deliberately did NOT do

- **Step 9 (drafts folder cleanup)** — draft + image still sit in `docs/public/comms/drafts/`, not
  archived to `published/`. The validator now reports this row as a warning (non-blocking by
  design) — expected, not a defect.
- **Syndication (Step 8)** — no Medium/LinkedIn cross-post. That's explicitly PM's manual step and
  needs footer-teaser/cross-post judgment I shouldn't make unilaterally on your behalf.
- **The stale "still blocking" note text** — the row's notes still read like art was missing;
  it wasn't (frontmatter had image/alt/caption filled in already by the time I looked). I didn't
  edit `notes` to correct this — that's your column, your call on how to annotate it.

## One real bug I hit, worth knowing about independent of this post

`piper-morgan-website`'s `node_modules` wasn't installed in my checkout (`rss-parser` missing),
which made `publish-post.js` fail partway through (image + CSV + blog-content.json had already
mutated before the fetch step died). I ran `PUPPETEER_SKIP_DOWNLOAD=true npm install` and re-ran
the fetch/sync/build steps manually to complete it cleanly — not a pipeline bug, just an
uninstalled-dependencies gap in my own worktree. Also caught and worked around: `publish-post.js`
defaults `--pub-date` to the system clock's UTC "today," which at the time of this publish (~7pm
Pacific) had already rolled to the next calendar day. Passed `--pub-date` explicitly to avoid a
second instance of the class of bug your v0.17 note already covers for `--work-date`. Might be
worth the same "never let it default" treatment for `--pub-date`, your call.

Nothing else needed from me — normal ownership resumes when you're back.

— Janus
