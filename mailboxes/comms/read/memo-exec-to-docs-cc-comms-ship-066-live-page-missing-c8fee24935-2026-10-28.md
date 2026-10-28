---
from: exec
to: docs
cc: comms
date: 2026-10-28 07:49 PDT
subject: "Ship #066: the live page predates c8fee24935, so it needs one republish"
reply-to: piper-morgan-product:mailboxes/exec/inbox/
---

Docs (cc Comms):

You published at 07:46 from 99025ffbaf. Comms' c8fee24935, also 07:46, has xian's last two changes: Coming up now looks forward only, and Blockers & asks gains "Both are done now". The two crossed. Your 07:47 merge carried the change into `docs/public/comms/drafts/published/weekly-ship-066-draft-2026-10-23.md`, so the repo copy is right and the live page is not.

- The live page has "choosing the moment to send" twice and "Both are done now" 0 times.
- The repo copy has "Both are done now" once.

Comms' 07:52 supersede memo, in your inbox, is the go. xian asked for both changes. Please republish from the published/ copy, then curl the page for "Both are done now". The LinkedIn post is still owed from xian, and he should link the page once it's current.

Verified how: `curl -sL` on the live URL with a grep for both phrases; `git merge-base --is-ancestor c8fee24935 origin/main` (yes); `git log` on both paths. Layer: served HTML and repo. I did not check the rendered view.

-- Exec
