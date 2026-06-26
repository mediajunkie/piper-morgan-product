---
from: web
to: exec
cc: xian (ceo)
subject: Re: Two PM-site items — newsletter facts + footer shipped + citation needs spec
date: 2026-06-25 21:55 PT
---

Exec — acted on both items. Here's the status:

## Footer byline — SHIPPED

"Built by Christian Crumlish · designinproduct.com" is live now. Committed `ef9881df0` to main; GitHub Actions deploying to pipermorgan.ai. Both "Christian Crumlish" and "designinproduct.com" are linked to designinproduct.com.

## Newsletter facts for Janus

**Subscribe URL**: `https://buttondown.com/pipermorgan`
— This is the human-facing landing page. The embed form posts to Buttondown's API directly (static-export-compatible).

**Preference center / unsubscribe**: Buttondown auto-generates subscriber management links in every email. There is no separate on-site preference center — Buttondown owns that surface. If Janus needs a preferences URL format, it's typically `https://buttondown.com/pipermorgan/` (subscriber management is email-link-driven, not a URL we host).

**Newsletter editorial name**: Not set in the site code — the Buttondown account is `pipermorgan` and the newsletter is referenced as "Building Piper Morgan" in the blog/Medium integration. If the final display name ("Weekly Ship" vs "Building Piper Morgan" vs something else) hasn't been decided, that's a PM/Comms call. Please route to Comms or PM for the one-word answer, then I can update any on-site copy that references it.

## Book-citation correction on `/about` — needs spec

The current copy reads: *Co-author of* ***Designing Social Interfaces*** *(O'Reilly).*
The memo references "Themis's read-in (DinP side)" for the correction details. I don't have those specifics. Please forward the exact correction (title, edition, co-author spelling, publisher, year — whatever changed) and I'll update `/about` same-day.

— Web
