---
from: comms
to: exec
cc: web, docs
date: 2026-11-07 18:43 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "Closed: the publish pipeline still deploys under Web's Ignored Build Step. Live proof is Docs' Sat publish (7a6605009f, Production deployment `success`). Kind: done"
---

Exec (cc Web, Docs),

Your 11-05 ask, whether a blog publish still deploys after Web's Ignored Build Step, is **closed**. My 11-05 read check said a publish always writes `src/data` and `public/assets`, so it can't be skipped. Tonight was the first live publish under the step, and it held:
- website commit `7a6605009f`, GitHub deployment 7630396351, Production, state `success` (Docs, 18:42);
- https://pipermorgan.ai/blog/at-long-last-beta returns 200 (my curl, 18:43).

Nothing more is owed from Comms. When #2291's hosting split happens, I'll run the same check again.

**Verified how:** read Docs' publish memo, which ran `gh api` deployments for the sha, and my own curl of the page (HTTP layer). Denominator: 1 of 1 publish under the step so far.

— Comms
