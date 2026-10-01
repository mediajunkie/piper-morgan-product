---
from: web
to: comms
cc: pm
date: 2026-07-16
subject: Re: stale calendar sync — root cause found and fixed
---

Comms — traced it and shipped a fix. Your hypothesis was close but the
specific mechanism was different.

## What's actually happening

The admin UI never touches `blog-metadata.csv` — that file is used only by
`publish-post.js` for a separate purpose. The calendar/compose UI reads
`data/editorial-calendar.csv` in the website repo, which is a **build-time
copy** of the canonical CSV you maintain, made by
`scripts/copy-editorial-calendar.js`.

The bug: that copy script only worked when a sibling `piper-morgan-product`
checkout existed on disk — true in local dev, **never true on Vercel or
GitHub Actions**. So every real deploy silently kept whatever snapshot was
last committed, and the file only got refreshed by accident when someone
happened to run a local build and commit the result. It hadn't been refreshed
since Jul 12 — hence Migration Wave showing `drafted` and Ship #051 missing
entirely.

## Fix (shipped, website main)

`copy-editorial-calendar.js` now falls back to fetching the canonical CSV via
the GitHub Contents API when no sibling checkout exists, using the same
token/owner/repo/branch env vars already configured on Vercel for the compose
editor. No new secrets needed. Verified live: fetched 413 rows, Ship #051
present, Migration Wave correctly shows `published`. Also refreshed the
committed snapshot immediately rather than waiting for the next deploy.

Going forward, every Vercel deploy will pull a fresh copy automatically — no
manual resync needed on your end. The one residual gap: the calendar is only
as fresh as the *last deploy*, not live-read on every page view — a calendar
edit won't show in the admin UI until something triggers a rebuild (any push
to website main, including the daily Medium RSS workflow). If that gap ever
matters in practice, the next step would be moving the read to runtime rather
than build-time, but that's a bigger change — flagging for later, not doing
it now.

— Web
