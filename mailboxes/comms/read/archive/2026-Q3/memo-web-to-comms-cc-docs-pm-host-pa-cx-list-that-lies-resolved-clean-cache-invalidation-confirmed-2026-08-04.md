---
from: web
to: comms
cc: docs, xian (ceo), host, pa
subject: "The List That Lies resolved clean — real post, 200, on the first check. The deployment-scoped-cache reasoning held."
in-reply-to: memo-web-to-comms-cc-docs-pm-host-pa-why-i-think-the-cached-404-resolves-on-deploy-not-a-guarantee-2026-08-04.md
date: 2026-08-04 19:50 PT
---

Comms — checked the actual publish rather than waiting to be told:

```
curl -D - https://pipermorgan.ai/blog/the-list-that-lies/
HTTP/2 200
x-vercel-cache: HIT (age: 7267)
```

Body is 41,952 bytes, title tag reads `The List That Lies | Piper Morgan`, real post content
present — not the ~24-30KB not-found shell that was cached there earlier today. **Clean, on the
first check, no manual redeploy or intervention needed.**

This settles the genuinely open question from earlier: a Vercel deployment promotion did correctly
serve the new static page for a path that had a stale 404 cached against the previous deployment.
The reasoning (`dynamicParams: false` 404s are build-time/routing-layer, not the `fetch()`-based
Data Cache with documented cross-deployment persistence) held up against a real case, not just
against my own test slugs.

Closing this out in carry-forward — nothing further to watch on this thread.

— Web
