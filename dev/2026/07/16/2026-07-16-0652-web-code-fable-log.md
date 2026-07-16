# Web session — 2026-07-16 (Thursday)

**Role**: Unicorn Web Designer (piper-morgan-website)
**Account**: DinP (xian@designinproduct.com)
**Model**: Claude Fable 5 (continued session)
**Trigger**: duty-cycle START fire 06:52
**Branch**: claude/condescending-jackson-c9a65b worktree → pushes to main

---

## Boot (06:52)

### Continuity from 2026-07-15 close

**Jul 15 log**: DAY-CLOSED ✓ (verified at START Step 0). Big day: DNS cutover fully
resolved (3-bug chain: Vercel redirect target → Hover trailing-dot CNAME → cert
propagation lag), pipermorgan.ai live on Vercel end-to-end. Ship normalization
Phase A proven live (ship #51). Phase B nudge sent to Docs, no reply yet.

**Carry-forward state**: 
- Dated trigger armed: Phase 6 cleanup (remove gh-pages deploy) — Fri 2026-07-17
- Ship Phase B: awaiting Docs's backfill draftPath values (#36–43, #50)
- Advisory: stash@{0} in product repo confirmed byte-identical/redundant, left for
  PM to drop explicitly (not forced past auto-mode denial)
- PM was going to trial compose on "into-production" (7/16 scheduled post) — today

### Mailbox sweep
Inbox: empty (MANIFEST only).

### Website repo
Already has ship #51 commit (cccf3f448) from yesterday's activity; no new commits.

---

## Fire log

| Fire | Time | Action | Notes |
|------|------|--------|-------|
| 06:52 tick | 06:52 | START | Jul-15 close verified. Inbox zero. Website unchanged since yesterday. Phase 6 trigger (tomorrow) and Phase B nudge (Docs) both still pending externally. Holding. |
| PM | 07:24–08:2x | WORK | **PM successfully edited today's post in production compose** — first real editorial use of the Vercel admin, confirmed working. PM requested image upload next; approved dropping the confirmed-safe stash from 7/15 (done). Asked ship-folding status: relayed unchanged (Phase A live/proven, Phase B still awaiting Docs). Then **unblocked Phase 3 (Image Upload)** — open since Jul 9 — via explicit choice: uploads land in the product repo alongside the draft (reuses the existing GitHub API path; smallest build). **Built + shipped same session**: `uploadBinaryFile()` in github-drafts.ts (new-file PUT, 409 on existing-file collision since there's no prior SHA to conflict-check against); `/api/compose/upload` API route (auth-gated, png/jpg/jpeg/gif/webp allowlist, ~4MB cap — flagged explicitly that Vercel's platform request-body limit is ~4.5MB and can't be raised, so this fails loud rather than as an opaque platform 413); file-picker UI next to the Image filename field in ComposeApp.tsx, slug-prefixed sanitized filenames. Scoped deliberately narrow: does NOT replicate publish-post.js's cwebp/Pillow webp-conversion (no such binary/lib in serverless) — that still runs unchanged at actual publish time; this endpoint only automates placing the *source* file, same as manual practice today. Verified live end-to-end: auth-rejected unauthenticated, fs-mode upload+placement, duplicate-file 409, bad-extension 400, GitHub-API-mode upload actually committed to product main (67b4aefab) then cleaned up. Type-check/lint/build all clean. Website commit pushed + verified on origin. Mid-session mail-sync hiccup (2nd instance this week): another agent's mailbox triage collided with a stash-based git sync; resolved the same rigorous way as 7/15 (byte-diff every conflicted file against HEAD before touching, not a spot-check) — all 3 files confirmed identical, safely resolved + redundant stash dropped. Surfaced-but-not-actioned: a Docs/Comms-lane memo about a canonicalSite calendar-validation bug (38 legacy rows) — noted to PM as background, not Web's lane. |
| Comms | 09:52–10:3x | WORK | **Calendar-staleness bug: diagnosed + fixed, not just explained.** Comms reported PM's compose UI showing "The Migration Wave" as drafted and Ship #051 missing entirely; hypothesized blog-metadata.csv sync gap. Actual mechanism (Web knows this system): compose reads data/editorial-calendar.csv, a BUILD-TIME copy of the product-repo canonical CSV made by copy-editorial-calendar.js — blog-metadata.csv is unrelated. Root cause deeper than my own Vercel-migration audit anticipated: the copy script only worked with a local sibling checkout present — true in dev, NEVER true on Vercel/GitHub Actions — so every real deploy silently kept whatever was last committed (Jul 12, 4 days stale), refreshed only by accident when local dev happened to rebuild+commit. Fix shipped same-session: copy-editorial-calendar.js now falls back to the GitHub Contents API (reusing GITHUB_DRAFT_TOKEN — no new secrets) when no sibling exists; verified all 3 paths (local-sibling untouched, API-fetch live-tested: 413 rows/ship-051 present/Migration-Wave-published, graceful no-token placeholder) + full prebuild integration. Refreshed the committed snapshot immediately too, not waiting for next deploy. Website commit pushed+verified. Replied to Comms (cc PM) with full diagnosis + fix + one flagged residual gap (build-time-fresh, not live-read — noted for later, not actioned). Inbox triaged. |
| PM | 11:15–17:xx | WORK | **PM asked about routine Vercel "build failed" notifications + a Comms miscommunication report.** Comms concern: false alarm — verified my calendar-sync reply was correctly delivered to mailboxes/comms/inbox/ at 09:56, catalogued in their MANIFEST; Comms likely just hadn't refreshed. Vercel alerts: investigated properly rather than guessing — GH Actions 100% green for days (ruled out), then found the real cause: `gh-pages` branch (still force-pushed every deploy by the old deploy.yml) has no package.json; if Vercel auto-builds all branches, every routine force-push = guaranteed-fail preview build. Verified DNS fully stable (5/5 consistent lookups, ~20h post-cutover) and proposed doing the already-scheduled Phase 6 (Fri 7/17) TODAY instead, since evidence showed active daily pain and no remaining reason to wait. **PM approved moving it up.** Executed: deleted deploy.yml entirely (Vercel's own GitHub integration already deploys every main push independently of GH Actions); removed the now-dead repository_dispatch step from update-blog-posts.yml; attempted GH Pages deactivation via gh api — blocked (422 "not allowed"), left as a manual-if-wanted step, harmless since DNS moved; added NEXT_PUBLIC_STATIC_EXPORT-gated fallback notice to /admin/login + AdminGate so a static-fallback hit shows a clear message instead of the exact dead-login 405 confusion from 7/15. Verification note: naive curl+grep on the rendered HTML gave false negatives (login page's Suspense boundary + AdminGate's client-only render meant curl saw near-empty shells in BOTH build modes) — switched to precise compiled-bundle-content grep, which correctly showed static build = notice-only, server build = form-only. Both builds + lint + type-check clean. Website commit pushed+verified. Incidentally discovered (NOT touched, flagged to PM only): "Update Medium Blog Posts" workflow has been `disabled_manually` since 2026-04-14 — three months old, unrelated to any of this week's work. |
