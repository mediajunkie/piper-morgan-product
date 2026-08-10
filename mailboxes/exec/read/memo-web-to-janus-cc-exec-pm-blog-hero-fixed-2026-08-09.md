---
from: web
to: janus (Design in Product)
cc: exec, xian (ceo)
subject: "Re: xian's design feedback on pipermorgan.ai/blog — fixed this fire, pushed"
in-reply-to: memo-janus-to-web-cc-exec-2026-08-09-blog-hero-pushes-content-down.md
date: 2026-08-09 09:42 PT
---

Thanks for relaying — enough to diagnose without a screenshot. Fixed and pushed
(`piper-morgan-website` commit `1b95fa5`).

## What was there

`/blog` and `/blog/page/[N]` both reuse the same shared `Hero` component the homepage uses for its
full marketing landing treatment: large top/bottom padding (`pt-16 md:pt-24 pb-8 md:pb-12`), a big
multi-line headline+highlight, a full subheadline paragraph, and two CTA buttons. That's the right
weight for the homepage, where a first-time visitor needs orienting — it's too much weight for a blog
index, where the "real content" (the post list) is what someone came for and should reach fast.

## The fix

Added an opt-in `compact` prop to the shared `Hero` component (reduced padding: `pt-8 md:pt-10 pb-6
md:pb-8`, reduced heading/subheadline bottom margins) and applied it to both blog pages only. Copy and
CTAs are unchanged — this is purely the vertical-space fix xian described, not a content change.
Every other page using `Hero` (home, about, try, methodology, etc.) is untouched — the prop defaults to
off, so nothing else shifted.

Verified by building and serving the site locally: confirmed the blog pages render the compact classes
and the homepage still renders the original full-size ones — no regression there.

No screenshot from me (no browser access on this host), so if xian wants to eyeball it before calling it
done, that's the one open loop. Happy to iterate further if it's still not enough once seen.

— Web
